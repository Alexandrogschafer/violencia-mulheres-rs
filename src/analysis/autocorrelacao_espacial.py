"""Índice de Moran Global: testa se a taxa de um tipo de crime por 100 mil
hab, num período configurável, tem autocorrelação espacial -- municípios
com taxa alta tendem a ficar espacialmente próximos (autocorrelação
positiva), ou a distribuição é espacialmente aleatória (I ~ 0)?

Contiguidade de rainha (Queen: municípios que compartilham fronteira ou só
um vértice) para a matriz de pesos espaciais -- mais permissiva que
contiguidade de torre (Rook, exige fronteira compartilhada) e a convenção
mais comum para vizinhança municipal, onde alguns vizinhos se tocam só num
ponto.

O p-valor reportado é o de permutação (esda.Moran.p_sim): recalcula I sobre
N_PERMUTACOES realocações aleatórias da taxa entre os municípios (mantendo
a malha fixa) e compara contra a estatística observada -- não assume
normalidade, ao contrário da aproximação p_norm (reportada só como
referência).
"""

from pathlib import Path

import esda
import numpy as np
import pandas as pd
from libpysal.weights import Queen

from src.analysis.mapa_choropleth import (
    ANO_FIM_PADRAO,
    ANO_INICIO_PADRAO,
    TIPO_CRIME_PADRAO,
    montar_geodataframe,
)

TABLES_DIR = Path(__file__).resolve().parent.parent.parent / "outputs" / "tables"

N_PERMUTACOES = 999
SEED = 12345

TIPOS_CRIME = ["Ameaça", "Estupro", "Feminicídio Consumado", "Feminicídio Tentado", "Lesão Corporal"]


def montar_pesos_espaciais(gdf) -> Queen:
    """Matriz de pesos espaciais por contiguidade de rainha, padronizada por
    linha (row-standardized: os vizinhos de cada município pesam 1/n_vizinhos
    cada, para que municípios com mais vizinhos não dominem a estatística).
    """
    w = Queen.from_dataframe(gdf, use_index=False)
    w.transform = "r"
    return w


def calcular_moran_global(
    tipo_crime: str = TIPO_CRIME_PADRAO,
    ano_inicio: int = ANO_INICIO_PADRAO,
    ano_fim: int = ANO_FIM_PADRAO,
) -> tuple[pd.DataFrame, Queen, esda.Moran]:
    gdf = montar_geodataframe(tipo_crime, ano_inicio, ano_fim)
    w = montar_pesos_espaciais(gdf)
    np.random.seed(SEED)
    moran = esda.Moran(gdf["taxa_por_100mil_hab"].to_numpy(), w, permutations=N_PERMUTACOES)
    return gdf, w, moran


def comparar_tipos_crime(
    ano_inicio: int = ANO_INICIO_PADRAO, ano_fim: int = ANO_FIM_PADRAO
) -> pd.DataFrame:
    """Roda o Moran Global para os 5 tipos de crime no mesmo período, lado a
    lado -- mesmo formato tabular usado em tendencia.py/sazonalidade.py.
    """
    resultados = []
    for tipo in TIPOS_CRIME:
        _, w, moran = calcular_moran_global(tipo, ano_inicio, ano_fim)
        resultados.append(
            {
                "tipo_crime": tipo,
                "moran_i": moran.I,
                "ei_esperado_h0": moran.EI,
                "z_sim": moran.z_sim,
                "p_valor_permutacao": moran.p_sim,
                "p_valor_normal": moran.p_norm,
                "significativo_5pct": moran.p_sim < 0.05,
                "n_municipios": w.n,
                "media_vizinhos": w.mean_neighbors,
                "n_ilhas": len(w.islands),
            }
        )
    return pd.DataFrame(resultados)


def main() -> None:
    gdf, w, moran = calcular_moran_global()
    print(
        f"Contiguidade de rainha ({TIPO_CRIME_PADRAO}, {ANO_INICIO_PADRAO}-{ANO_FIM_PADRAO}): "
        f"{w.n} municípios, média {w.mean_neighbors:.2f} vizinhos, {len(w.islands)} ilha(s) sem vizinho"
    )
    print()
    print(f"Índice de Moran global (I): {moran.I:.4f}")
    print(f"E[I] sob H0 (aleatoriedade espacial): {moran.EI:.4f}")
    print(f"z (permutação): {moran.z_sim:.4f}")
    print(f"p-valor (permutação, {N_PERMUTACOES} reamostragens): {moran.p_sim:.4f}")
    print(f"p-valor (aproximação normal, referência): {moran.p_norm:.4e}")
    print()

    print(f"=== Comparação entre os 5 tipos de crime ({ANO_INICIO_PADRAO}-{ANO_FIM_PADRAO}) ===")
    pd.set_option("display.width", 160)
    print(comparar_tipos_crime().to_string(index=False))


if __name__ == "__main__":
    main()
