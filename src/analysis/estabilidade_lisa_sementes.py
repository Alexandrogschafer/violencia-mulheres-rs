"""Estabilidade do LISA com ajuste de Assunção e Reis frente à semente aleatória.

Roda a configuração principal de moran_lisa_assuncao_reis.py (mesma malha, mesma
matriz, 497 municípios, 2018-2025, quatro tipos com LISA) para vinte sementes, com
999 e com 99.999 permutações. Importa os cálculos daquele módulo, sem alterá-lo.

Critério de significância: Benjamini-Hochberg a 5%, por tipo de crime, semente e
número de permutações, sobre o p_sim do esda (sobrevive_fdr). Esse p é direcional
e equivale à metade do bilateral, como explica o módulo de origem; por isso a
tabela também traz o critério sobre o dobro dele (sobrevive_fdr_p2x).

Instável é o município que, num mesmo tipo de crime e número de permutações, muda
de status ou de categoria em pelo menos uma das vinte sementes. O I local e o
quadrante dependem só dos dados, e o script confirma que não variam entre
sementes; logo, a categoria só muda quando o status muda.

O pico de memória é o maior RSS do processo. As configurações rodam em ordem
crescente de permutações, então o valor lido ao fim de cada uma é o pico acumulado.

Uso: python -m src.analysis.estabilidade_lisa_sementes [--n-sementes N] [--saida CSV] [--resumo MD]
"""

import argparse
import resource
import time
from pathlib import Path

import numpy as np
import pandas as pd

from src.analysis.autocorrelacao_espacial import montar_pesos_espaciais
from src.analysis.mapa_choropleth import montar_geodataframe
from src.analysis.moran_lisa_assuncao_reis import (
    ANO_FIM,
    ANO_INICIO,
    N_MUNICIPIOS,
    QUADRANTES,
    SEED,
    TABLES_DIR,
    TIPOS_LISA,
    benjamini_hochberg,
    rodar_local,
)

SAIDA_PADRAO = TABLES_DIR / "estabilidade_lisa_sementes.csv"
RESUMO_PADRAO = TABLES_DIR / "estabilidade_lisa_sementes_resumo.md"

PERMUTACOES = [999, 99_999]
N_SEMENTES = 20
# A primeira é a semente publicada; as demais são fixas para a execução ser repetível.
PASSO_SEMENTE = 1000
NAO_SIGNIFICATIVO = "não significativo"
CATEGORIAS = {cod: nome.upper() for cod, nome in QUADRANTES.items()}
CRITERIOS = {"fdr": ("sobrevive_fdr", "categoria"), "fdr_p2x": ("sobrevive_fdr_p2x", "categoria_fdr_p2x")}


def pico_memoria_mb() -> float:
    """Maior RSS do processo até aqui (ru_maxrss vem em KiB no Linux)."""
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024


def carregar_dados() -> list[tuple]:
    dados = []
    for tipo in TIPOS_LISA:
        gdf = montar_geodataframe(tipo, ANO_INICIO, ANO_FIM)
        w = montar_pesos_espaciais(gdf)
        casos = gdf["casos_total"].to_numpy(dtype=float)
        pop = gdf["populacao_pessoas_ano"].to_numpy(dtype=float)
        if len(gdf) != N_MUNICIPIOS or np.isnan(casos).any() or np.isnan(pop).any() or w.islands:
            raise ValueError(f"{tipo}: universo diferente de {N_MUNICIPIOS} municípios completos.")
        dados.append((tipo, gdf["municipio"].to_numpy(), casos, pop, w))
    return dados


def categorias(q: np.ndarray, mascara: np.ndarray) -> np.ndarray:
    rotulos = np.array([CATEGORIAS[int(c)] for c in q], dtype=object)
    rotulos[~mascara] = NAO_SIGNIFICATIVO
    return rotulos


def calcular(n_sementes: int = N_SEMENTES) -> tuple[pd.DataFrame, pd.DataFrame]:
    sementes = [SEED + i * PASSO_SEMENTE for i in range(n_sementes)]
    dados = carregar_dados()
    blocos, execucao = [], []

    for permutacoes in PERMUTACOES:
        inicio_config = time.perf_counter()
        tempos = []
        for tipo, municipios, casos, pop, w in dados:
            referencia = None
            for semente in sementes:
                inicio = time.perf_counter()
                lisa = rodar_local("assuncao_reis", casos, pop, None, w, permutacoes, semente)
                tempos.append(time.perf_counter() - inicio)
                p = np.asarray(lisa.p_sim, dtype=float)
                i_local = np.asarray(lisa.Is, dtype=float)
                q = np.asarray(lisa.q)
                if referencia is None:
                    referencia = (i_local, q)
                elif not (np.array_equal(i_local, referencia[0]) and np.array_equal(q, referencia[1])):
                    raise ValueError(f"{tipo}: I local ou quadrante variou com a semente {semente}.")
                fdr = benjamini_hochberg(p)
                fdr_p2x = benjamini_hochberg(np.minimum(2 * p, 1.0))
                blocos.append(
                    pd.DataFrame(
                        {
                            "tipo_crime": tipo,
                            "municipio": municipios,
                            "permutacoes": permutacoes,
                            "semente": semente,
                            "i_local": i_local,
                            "p_sim": p,
                            "sobrevive_fdr": fdr,
                            "categoria": categorias(q, fdr),
                            "sobrevive_fdr_p2x": fdr_p2x,
                            "categoria_fdr_p2x": categorias(q, fdr_p2x),
                        }
                    )
                )
                del lisa
            print(f"{permutacoes} permutações | {tipo}: concluído", flush=True)
        execucao.append(
            {
                "permutacoes": permutacoes,
                "execucoes_lisa": len(tempos),
                "tempo_total_s": round(time.perf_counter() - inicio_config, 1),
                "tempo_medio_por_lisa_s": round(float(np.mean(tempos)), 3),
                "pico_memoria_acumulado_mb": round(pico_memoria_mb(), 0),
            }
        )
    return pd.concat(blocos, ignore_index=True), pd.DataFrame(execucao)


def distribuicao(tabela: pd.DataFrame) -> pd.DataFrame:
    """Número de municípios significativos por semente, resumido entre sementes."""
    linhas = []
    for criterio, (status, _) in CRITERIOS.items():
        contagens = tabela.groupby(["tipo_crime", "permutacoes", "semente"])[status].sum()
        for (tipo, permutacoes), serie in contagens.groupby(level=[0, 1]):
            frequencias = serie.value_counts().sort_index()
            linhas.append(
                {
                    "criterio": criterio,
                    "tipo_crime": tipo,
                    "permutacoes": permutacoes,
                    "minimo": int(serie.min()),
                    "q1": serie.quantile(0.25),
                    "mediana": serie.median(),
                    "q3": serie.quantile(0.75),
                    "maximo": int(serie.max()),
                    "media": round(serie.mean(), 2),
                    "dp": round(serie.std(), 2),
                    "frequencias": ", ".join(f"{int(k)} ({int(v)}x)" for k, v in frequencias.items()),
                }
            )
    return pd.DataFrame(linhas)


def instabilidade(tabela: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Contagens de instáveis e lista por município, tipo, permutações e critério."""
    contagens, listas = [], []
    chaves = ["tipo_crime", "permutacoes", "municipio"]
    for criterio, (status, categoria) in CRITERIOS.items():
        por_municipio = tabela.groupby(chaves, sort=True).agg(
            sementes_significativo=(status, "sum"),
            n_sementes=(status, "size"),
            n_categorias=(categoria, "nunique"),
            categorias=(categoria, lambda s: " | ".join(sorted(set(s)))),
            p_minimo=("p_sim", "min"),
            p_maximo=("p_sim", "max"),
        ).reset_index()
        por_municipio["troca_status"] = por_municipio["sementes_significativo"].between(
            1, por_municipio["n_sementes"] - 1
        )
        por_municipio["troca_categoria"] = por_municipio["n_categorias"] > 1
        por_municipio.insert(0, "criterio", criterio)

        for (tipo, permutacoes), g in por_municipio.groupby(["tipo_crime", "permutacoes"]):
            contagens.append(
                {
                    "criterio": criterio,
                    "tipo_crime": tipo,
                    "permutacoes": permutacoes,
                    "sempre_significativos": int((g["sementes_significativo"] == g["n_sementes"]).sum()),
                    "ao_menos_uma_semente": int((g["sementes_significativo"] > 0).sum()),
                    "trocam_status": int(g["troca_status"].sum()),
                    "trocam_categoria": int(g["troca_categoria"].sum()),
                }
            )
        for permutacoes, g in por_municipio.groupby("permutacoes"):
            instaveis = g[g["troca_status"] | g["troca_categoria"]]
            contagens.append(
                {
                    "criterio": criterio,
                    "tipo_crime": "municípios distintos, quatro tipos",
                    "permutacoes": permutacoes,
                    "sempre_significativos": int(
                        g.loc[g["sementes_significativo"] == g["n_sementes"], "municipio"].nunique()
                    ),
                    "ao_menos_uma_semente": int(g.loc[g["sementes_significativo"] > 0, "municipio"].nunique()),
                    "trocam_status": int(g.loc[g["troca_status"], "municipio"].nunique()),
                    "trocam_categoria": int(g.loc[g["troca_categoria"], "municipio"].nunique()),
                }
            )
            listas.append(instaveis)
    colunas = [
        "criterio",
        "tipo_crime",
        "permutacoes",
        "municipio",
        "sementes_significativo",
        "n_sementes",
        "categorias",
        "p_minimo",
        "p_maximo",
    ]
    return pd.DataFrame(contagens), pd.concat(listas, ignore_index=True)[colunas]


def tabela_markdown(df: pd.DataFrame) -> str:
    """Tabela Markdown sem depender de tabulate, ausente do requirements.txt."""
    linhas = [list(df.columns), ["---"] * df.shape[1], *df.astype(str).to_numpy().tolist()]
    return "\n".join("| " + " | ".join(map(str, linha)) + " |" for linha in linhas)


def escrever_resumo(tabela: pd.DataFrame, execucao: pd.DataFrame, destino: Path) -> str:
    dist = distribuicao(tabela)
    contagens, lista = instabilidade(tabela)
    n_sementes = tabela["semente"].nunique()
    texto = "\n\n".join(
        [
            "# Estabilidade do LISA de Assunção e Reis frente à semente",
            f"{n_sementes} sementes, de {tabela['semente'].min()} a {tabela['semente'].max()}, "
            f"de {PASSO_SEMENTE} em {PASSO_SEMENTE}. Critério `fdr`: Benjamini-Hochberg sobre o p_sim do esda. "
            "Critério `fdr_p2x`: sobre o dobro dele, limitado a 1.",
            "## Municípios significativos por semente",
            tabela_markdown(dist),
            "## Municípios que trocam de status ou categoria",
            tabela_markdown(contagens),
            "## Municípios instáveis",
            tabela_markdown(lista),
            "## Execução",
            tabela_markdown(execucao),
        ]
    )
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(texto + "\n", encoding="utf-8")
    return texto


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--n-sementes", type=int, default=N_SEMENTES)
    parser.add_argument("--saida", type=Path, default=SAIDA_PADRAO)
    parser.add_argument("--resumo", type=Path, default=RESUMO_PADRAO)
    args = parser.parse_args()

    inicio = time.perf_counter()
    tabela, execucao = calcular(args.n_sementes)
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    tabela.to_csv(args.saida, index=False)
    texto = escrever_resumo(tabela, execucao, args.resumo)
    print(texto)
    print(f"\nTabela gravada em {args.saida}")
    print(f"Resumo gravado em {args.resumo}")
    print(f"Tempo total: {time.perf_counter() - inicio:.1f} s")
    print(f"Pico de memória do processo: {pico_memoria_mb():.0f} MB")


if __name__ == "__main__":
    main()
