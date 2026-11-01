"""Moran global e LISA em configuração revisada, ao lado da configuração
publicada. Não substitui autocorrelacao_espacial.py nem clusters_lisa.py, que
sustentam o estado atual do portal; só reutiliza a mesma malha e a mesma matriz.

Três configurações, todas com contiguidade de rainha padronizada por linha, os
497 municípios e o período 2018-2025:

- assuncao_reis (principal): esda.moran.Moran_Rate e Moran_Local_Rate, que
  recebem casos e população-ano acumulada. Estabiliza a variância das taxas
  antes do teste, de modo que municípios pequenos não dominem a estatística
  (Assunção e Reis, 1999).
- bruta (sensibilidade): a taxa por 100 mil hab., como na configuração atual.
- eb_espacial (sensibilidade): taxa suavizada por bayesiano empírico espacial
  (esda.smoothing.Spatial_Empirical_Bayes). ATENÇÃO: esta configuração INDUZ
  AUTOCORRELAÇÃO POR CONSTRUÇÃO. Cada taxa é puxada para a média da própria
  vizinhança, usando a mesma contiguidade do teste, e a permutação trata como
  intercambiáveis valores que já não são independentes. I e p servem só como
  referência, não como evidência de agrupamento espacial.

Significância local: esda calcula p_sim com alternative="directed", que escolhe
a cauda conforme o dado. A própria documentação do esda (calculate_significance)
avisa que esse p é a metade do bilateral e fica uniformemente pequeno demais. A
correção de Benjamini-Hochberg é aplicada por categoria e configuração sobre
esse p (fdr) e, como referência, sobre o dobro dele, limitado a 1 (fdr_p2x).

Semente: SEED é reposta antes de cada cálculo, global e local, a mesma de
autocorrelacao_espacial.py e clusters_lisa.py. Com --permutacoes 999, a
configuração bruta reproduz os valores publicados.

Uso: python -m src.analysis.moran_lisa_assuncao_reis [--permutacoes N] [--seed S] [--saida CSV]
"""

import argparse
import time
from pathlib import Path

import esda
import numpy as np
import pandas as pd
from esda.moran import Moran_Local_Rate, Moran_Rate
from esda.smoothing import Spatial_Empirical_Bayes
from libpysal.weights import Queen

from src.analysis.autocorrelacao_espacial import montar_pesos_espaciais
from src.analysis.mapa_choropleth import _populacao_referencia, montar_geodataframe

TABLES_DIR = Path(__file__).resolve().parent.parent.parent / "outputs" / "tables"
SAIDA_PADRAO = TABLES_DIR / "moran_lisa_assuncao_reis_2018_2025.csv"

ANO_INICIO = 2018
ANO_FIM = 2025
N_PERMUTACOES = 99_999
SEED = 12345
ALFA = 0.05
PISO_POPULACIONAL = 5000
N_MUNICIPIOS = 497
CASOS_POR_HABITANTES = 100_000

TIPOS_MORAN = ["Ameaça", "Estupro", "Feminicídio Consumado", "Feminicídio Tentado", "Lesão Corporal"]
TIPOS_LISA = ["Ameaça", "Estupro", "Lesão Corporal", "Feminicídio Tentado"]
CONFIGURACOES = ["assuncao_reis", "bruta", "eb_espacial"]

# Quadrantes do esda.Moran_Local com geoda_quads=False.
QUADRANTES = {1: "aa", 2: "ba", 3: "bb", 4: "ab"}

OBSERVACOES = {
    "assuncao_reis": "principal",
    "bruta": "sensibilidade; configuração atual do portal",
    "eb_espacial": "sensibilidade; induz autocorrelação por construção",
}


def benjamini_hochberg(p: np.ndarray, alfa: float = ALFA) -> np.ndarray:
    """Máscara booleana dos testes rejeitados por Benjamini-Hochberg."""
    p = np.asarray(p, dtype=float)
    n = p.size
    ordem = np.argsort(p)
    passou = p[ordem] <= alfa * np.arange(1, n + 1) / n
    mascara = np.zeros(n, dtype=bool)
    if passou.any():
        mascara[ordem[: np.nonzero(passou)[0].max() + 1]] = True
    return mascara


def taxa_eb_espacial(casos: np.ndarray, pop: np.ndarray, gdf) -> tuple[np.ndarray, int]:
    """Taxa suavizada e número de indefinições tratadas.

    Usa uma matriz própria porque Spatial_Rate altera w.transform do objeto
    recebido. Quando a taxa do município e a da vizinhança são zero, a fórmula
    resulta em 0/0; o valor suavizado é 0, a única estimativa compatível com
    esses dados.
    """
    w = Queen.from_dataframe(gdf, use_index=False)
    w.id_order = list(range(len(gdf)))
    with np.errstate(divide="ignore", invalid="ignore"):
        r = Spatial_Empirical_Bayes(casos, pop, w).r.flatten()
    indefinidos = np.isnan(r)
    if (casos[indefinidos] != 0).any():
        raise ValueError("Indefinição do bayesiano empírico em município com casos.")
    r[indefinidos] = 0.0
    return r, int(indefinidos.sum())


def rodar_global(config, casos, pop, y, w, permutacoes, seed):
    np.random.seed(seed)
    if config == "assuncao_reis":
        return Moran_Rate(casos, pop, w, adjusted=True, transformation="r", permutations=permutacoes)
    return esda.Moran(y, w, transformation="r", permutations=permutacoes)


def rodar_local(config, casos, pop, y, w, permutacoes, seed):
    if config == "assuncao_reis":
        return Moran_Local_Rate(
            casos, pop, w, adjusted=True, transformation="r", permutations=permutacoes, seed=seed
        )
    return esda.Moran_Local(y, w, transformation="r", permutations=permutacoes, seed=seed)


def contar_quadrantes(q: np.ndarray, mascara: np.ndarray) -> dict[str, int]:
    return {nome: int(((q == cod) & mascara).sum()) for cod, nome in QUADRANTES.items()}


def calcular(permutacoes: int = N_PERMUTACOES, seed: int = SEED) -> pd.DataFrame:
    linhas = []
    pop_ref = _populacao_referencia(ANO_FIM)
    abaixo_piso = set(pop_ref[pop_ref < PISO_POPULACIONAL].index)

    for tipo in TIPOS_MORAN:
        gdf = montar_geodataframe(tipo, ANO_INICIO, ANO_FIM)
        w = montar_pesos_espaciais(gdf)
        casos = gdf["casos_total"].to_numpy(dtype=float)
        pop = gdf["populacao_pessoas_ano"].to_numpy(dtype=float)
        if len(gdf) != N_MUNICIPIOS or np.isnan(casos).any() or np.isnan(pop).any() or w.islands:
            raise ValueError(f"{tipo}: universo diferente de {N_MUNICIPIOS} municípios completos.")
        no_piso = gdf["municipio"].isin(abaixo_piso).to_numpy()

        bruta = gdf["taxa_por_100mil_hab"].to_numpy(dtype=float)
        suavizada, n_indefinidos = taxa_eb_espacial(casos, pop, gdf)
        valores = {
            "assuncao_reis": None,
            "bruta": bruta,
            "eb_espacial": suavizada * CASOS_POR_HABITANTES,
        }

        for config in CONFIGURACOES:
            inicio = time.perf_counter()
            moran = rodar_global(config, casos, pop, valores[config], w, permutacoes, seed)
            linha = {
                "tipo_crime": tipo,
                "configuracao": config,
                "n_municipios": w.n,
                "permutacoes": permutacoes,
                "semente": seed,
                "moran_i": moran.I,
                "moran_ei": moran.EI,
                "moran_z_sim": moran.z_sim,
                "moran_p_sim": moran.p_sim,
                "tempo_global_s": round(time.perf_counter() - inicio, 2),
                "observacao": OBSERVACOES[config],
                "eb_indefinidos_zerados": n_indefinidos if config == "eb_espacial" else 0,
            }

            if tipo in TIPOS_LISA:
                inicio = time.perf_counter()
                lisa = rodar_local(config, casos, pop, valores[config], w, permutacoes, seed)
                p = np.asarray(lisa.p_sim, dtype=float)
                criterios = {
                    "sem_fdr": p < ALFA,
                    "fdr": benjamini_hochberg(p),
                    "fdr_p2x": benjamini_hochberg(np.minimum(2 * p, 1.0)),
                }
                for nome, mascara in criterios.items():
                    for quad, n in contar_quadrantes(lisa.q, mascara).items():
                        linha[f"lisa_{quad}_{nome}"] = n
                    linha[f"lisa_total_{nome}"] = int(mascara.sum())
                    linha[f"lisa_abaixo_piso_{nome}"] = int((mascara & no_piso).sum())
                linha["lisa_p_minimo"] = p.min()
                linha["tempo_lisa_s"] = round(time.perf_counter() - inicio, 2)
                del lisa

            linhas.append(linha)
            print(
                f"{tipo} | {config}: I={moran.I:.4f} p={moran.p_sim:.5f} "
                f"(global {linha['tempo_global_s']}s, LISA {linha.get('tempo_lisa_s', '-')}s)",
                flush=True,
            )
    return pd.DataFrame(linhas)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--permutacoes", type=int, default=N_PERMUTACOES)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--saida", type=Path, default=SAIDA_PADRAO)
    args = parser.parse_args()

    inicio = time.perf_counter()
    tabela = calcular(args.permutacoes, args.seed)
    total = time.perf_counter() - inicio
    tabela["tempo_total_execucao_s"] = round(total, 1)

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    tabela.to_csv(args.saida, index=False)
    print(f"Tabela gravada em {args.saida}")
    print(f"Tempo total: {total:.1f} s")


if __name__ == "__main__":
    main()
