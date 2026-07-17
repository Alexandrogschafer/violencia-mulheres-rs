"""Mapa choropleth dos municípios do RS pela taxa de um tipo de crime por
100 mil habitantes, num período configurável.

carregar_taxa_periodo é o carregador compartilhado com
autocorrelacao_espacial.py e clusters_lisa.py: taxa acumulada no período
(soma(casos)/soma(população)*100_000), não a média das taxas anuais -- mesma
metodologia de correlacao.py.
"""

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

from src.fetch_malha_municipios import carregar_malha_com_municipio
from src.load_data import CASOS_POR_HABITANTES

TABLES_DIR = Path(__file__).resolve().parent.parent.parent / "outputs" / "tables"
FIGURES_DIR = Path(__file__).resolve().parent.parent.parent / "outputs" / "figures"

MUNICIPIO_NAO_IDENTIFICADO = "NÃO INFORMADO"

TIPO_CRIME_PADRAO = "Estupro"
ANO_INICIO_PADRAO = 2021
ANO_FIM_PADRAO = 2025

# CRS projetado (SIRGAS 2000 / Brazil Polyconic) só para desenhar o mapa com
# proporção correta -- a malha crua vem em graus (EPSG:4326), que distorce a
# forma do RS num plot com eixos 1:1.
CRS_PLOT = "EPSG:5880"

# Rampa sequencial azul (claro->escuro) da paleta padrão do projeto, para
# codificar magnitude (taxa) -- um hue só, nunca arco-íris.
RAMPA_SEQUENCIAL_AZUL = [
    "#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7",
    "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b",
]
COR_SEM_DADO = "#e1e0d9"


def carregar_taxa_periodo(
    tipo_crime: str, ano_inicio: int, ano_fim: int, caminho: Path | None = None
) -> pd.DataFrame:
    """Taxa acumulada por 100 mil hab, por município, para um tipo de crime e
    intervalo de anos [ano_inicio, ano_fim] -- soma(casos)/soma(população
    no período)*100_000, a mesma metodologia (e mesmo motivo) de
    carregar_taxas_por_municipio em correlacao.py.
    """
    caminho = caminho or TABLES_DIR / "violencia_anual_municipio_taxa.csv"
    df = pd.read_csv(caminho)
    df = df[
        (df["tipo_crime"] == tipo_crime)
        & (df["ano"] >= ano_inicio)
        & (df["ano"] <= ano_fim)
        & (df["municipio"] != MUNICIPIO_NAO_IDENTIFICADO)
    ]
    df = df.dropna(subset=["populacao"])
    agregado = df.groupby("municipio", as_index=False).agg(
        casos_total=("casos_total", "sum"),
        populacao_pessoas_ano=("populacao", "sum"),
    )
    agregado["taxa_por_100mil_hab"] = (
        agregado["casos_total"] / agregado["populacao_pessoas_ano"] * CASOS_POR_HABITANTES
    )
    return agregado


def montar_geodataframe(tipo_crime: str, ano_inicio: int, ano_fim: int) -> gpd.GeoDataFrame:
    """Malha geográfica dos municípios do RS já com a taxa do período
    juntada (por nome de município, após a malha já ter sido resolvida por
    código IBGE em carregar_malha_com_municipio).
    """
    malha = carregar_malha_com_municipio()
    taxa = carregar_taxa_periodo(tipo_crime, ano_inicio, ano_fim)
    return malha.merge(taxa, on="municipio", how="left")


def slug_tipo_crime(texto: str) -> str:
    return (
        texto.lower()
        .replace(" ", "_")
        .replace("í", "i")
        .replace("é", "e")
        .replace("ã", "a")
        .replace("ç", "c")
    )


def gerar_mapa(
    tipo_crime: str = TIPO_CRIME_PADRAO,
    ano_inicio: int = ANO_INICIO_PADRAO,
    ano_fim: int = ANO_FIM_PADRAO,
    caminho_saida: Path | None = None,
) -> tuple[Path, gpd.GeoDataFrame]:
    gdf = montar_geodataframe(tipo_crime, ano_inicio, ano_fim)
    gdf_plot = gdf.to_crs(CRS_PLOT)

    cmap = LinearSegmentedColormap.from_list("taxa_azul", RAMPA_SEQUENCIAL_AZUL)

    fig, ax = plt.subplots(figsize=(8, 8))
    gdf_plot.plot(
        column="taxa_por_100mil_hab",
        cmap=cmap,
        linewidth=0.2,
        edgecolor="white",
        legend=True,
        legend_kwds={"label": "Casos por 100 mil hab.", "shrink": 0.6},
        missing_kwds={"color": COR_SEM_DADO, "label": "Sem dado"},
        ax=ax,
    )
    ax.set_axis_off()
    ax.set_title(f"{tipo_crime} — taxa por 100 mil hab. ({ano_inicio}–{ano_fim})\nRio Grande do Sul, por município")

    caminho_saida = caminho_saida or (
        FIGURES_DIR / f"choropleth_{slug_tipo_crime(tipo_crime)}_{ano_inicio}_{ano_fim}.png"
    )
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(caminho_saida, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return caminho_saida, gdf


def main() -> None:
    caminho, gdf = gerar_mapa()
    taxa = gdf["taxa_por_100mil_hab"]
    n_sem_dado = taxa.isna().sum()
    print(f"Mapa salvo em {caminho}")
    print(f"Municípios plotados: {len(gdf)}  |  sem dado de taxa: {n_sem_dado}")
    print(f"Taxa por 100 mil hab. — min={taxa.min():.2f}  media={taxa.mean():.2f}  max={taxa.max():.2f}")
    print()
    print("Top 10 municípios por taxa:")
    print(
        gdf[["municipio", "casos_total", "populacao_pessoas_ano", "taxa_por_100mil_hab"]]
        .sort_values("taxa_por_100mil_hab", ascending=False)
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
