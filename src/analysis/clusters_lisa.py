"""LISA (Local Indicators of Spatial Association): o Moran Global
(autocorrelacao_espacial.py) diz SE existe cluster espacial; o LISA diz
ONDE -- para cada município, se ele e seus vizinhos formam um cluster de
taxa alta (Alto-Alto, "hot spot"), de taxa baixa (Baixo-Baixo, "cold
spot"), ou um outlier espacial (Alto-Baixo/Baixo-Alto: destoa dos
vizinhos), com significância própria por permutação.

Só roda por padrão para os tipos de crime com Moran Global significativo
(ver autocorrelacao_espacial.py): Ameaça, Lesão Corporal e Estupro --
Feminicídio Consumado/Tentado não têm padrão espacial global a localizar.
"""

from pathlib import Path

import esda
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch

from src.analysis.autocorrelacao_espacial import montar_pesos_espaciais
from src.analysis.mapa_choropleth import (
    ANO_FIM_PADRAO,
    ANO_INICIO_PADRAO,
    montar_geodataframe,
    slug_tipo_crime,
)

FIGURES_DIR = Path(__file__).resolve().parent.parent.parent / "outputs" / "figures"

# Tipos de crime com Moran Global significativo a 5% no período padrão
# (Ameaça I=0.31, Lesão Corporal I=0.27, Estupro I=0.10, todos p=0.001) --
# rodar LISA para Feminicídio Consumado/Tentado não teria padrão global a
# localizar (ver autocorrelacao_espacial.py: p=0.50 e p=0.14).
TIPOS_CRIME_PADRAO = ["Ameaça", "Estupro", "Lesão Corporal"]

N_PERMUTACOES = 999
SEED = 12345
CRIT_VALUE = 0.05

# Mesmo CRS projetado do choropleth, só para desenhar com proporção correta.
CRS_PLOT = "EPSG:5880"

# Convenção padrão de mapas LISA (GeoDa): vermelho = hot spot, azul = cold
# spot, tons intermediários = outliers, cinza = sem padrão local
# significativo. Cores extraídas da paleta categórica do projeto (ordem
# fixa, validada com scripts/validate_palette.js -- PASS, com WARN de
# contraste no magenta mitigado pela legenda com texto).
CORES_CLUSTER = {
    "Alto-Alto": "#e34948",
    "Baixo-Baixo": "#2a78d6",
    "Alto-Baixo": "#e87ba4",
    "Baixo-Alto": "#4a3aa7",
    "Não significativo": "#e1e0d9",
}

TRADUCAO_LABEL = {
    "High-High": "Alto-Alto",
    "Low-Low": "Baixo-Baixo",
    "High-Low": "Alto-Baixo",
    "Low-High": "Baixo-Alto",
    "Insignificant": "Não significativo",
}


def calcular_lisa(
    tipo_crime: str,
    ano_inicio: int = ANO_INICIO_PADRAO,
    ano_fim: int = ANO_FIM_PADRAO,
    crit_value: float = CRIT_VALUE,
):
    """Retorna (geodataframe com moran_local_i/p_sim/categoria por
    município, objeto esda.Moran_Local cru)."""
    gdf = montar_geodataframe(tipo_crime, ano_inicio, ano_fim)
    w = montar_pesos_espaciais(gdf)
    lisa = esda.Moran_Local(
        gdf["taxa_por_100mil_hab"].to_numpy(), w, permutations=N_PERMUTACOES, seed=SEED
    )

    gdf = gdf.copy()
    gdf["moran_local_i"] = lisa.Is
    gdf["p_sim"] = lisa.p_sim
    gdf["categoria"] = [
        TRADUCAO_LABEL[label] for label in lisa.get_cluster_labels(crit_value=crit_value)
    ]
    return gdf, lisa


def gerar_mapa_lisa(
    tipo_crime: str,
    ano_inicio: int = ANO_INICIO_PADRAO,
    ano_fim: int = ANO_FIM_PADRAO,
    crit_value: float = CRIT_VALUE,
    caminho_saida: Path | None = None,
):
    gdf, lisa = calcular_lisa(tipo_crime, ano_inicio, ano_fim, crit_value)
    gdf_plot = gdf.to_crs(CRS_PLOT)

    fig, ax = plt.subplots(figsize=(8, 8))
    for categoria, cor in CORES_CLUSTER.items():
        subset = gdf_plot[gdf_plot["categoria"] == categoria]
        if len(subset):
            subset.plot(ax=ax, color=cor, linewidth=0.2, edgecolor="white")
    ax.set_axis_off()
    ax.set_title(
        f"Clusters LISA — {tipo_crime}, taxa por 100 mil hab. ({ano_inicio}–{ano_fim})\n"
        "Rio Grande do Sul, por município"
    )
    ax.legend(
        handles=[Patch(color=cor, label=categoria) for categoria, cor in CORES_CLUSTER.items()],
        loc="lower left",
        fontsize=8,
        framealpha=0.9,
    )

    caminho_saida = caminho_saida or (
        FIGURES_DIR / f"lisa_{slug_tipo_crime(tipo_crime)}_{ano_inicio}_{ano_fim}.png"
    )
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(caminho_saida, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return caminho_saida, gdf


def main() -> None:
    pd.set_option("display.width", 160)
    for tipo in TIPOS_CRIME_PADRAO:
        caminho, gdf = gerar_mapa_lisa(tipo)
        print(f"=== {tipo} ({ANO_INICIO_PADRAO}-{ANO_FIM_PADRAO}) ===")
        print(f"Mapa salvo em {caminho}")
        print(gdf["categoria"].value_counts().to_string())
        print()

        hotspots = gdf[gdf["categoria"] == "Alto-Alto"].sort_values(
            "taxa_por_100mil_hab", ascending=False
        )
        print(f"Municípios Alto-Alto (hot spots) -- {len(hotspots)} no total:")
        print(
            hotspots[["municipio", "taxa_por_100mil_hab", "moran_local_i", "p_sim"]]
            .head(15)
            .to_string(index=False)
        )
        print()

        outliers = gdf[gdf["categoria"].isin(["Alto-Baixo", "Baixo-Alto"])].sort_values(
            "p_sim"
        )
        if len(outliers):
            print(f"Outliers espaciais (Alto-Baixo/Baixo-Alto) -- {len(outliers)} no total:")
            print(
                outliers[["municipio", "categoria", "taxa_por_100mil_hab", "p_sim"]]
                .head(10)
                .to_string(index=False)
            )
        print()


if __name__ == "__main__":
    main()
