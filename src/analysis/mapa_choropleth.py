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
from matplotlib import colormaps
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch
from shapely import concave_hull
from shapely.ops import unary_union

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

# Município abaixo do piso populacional (pop_minima): preenchimento sólido,
# cinza claro neutro e quente (sem componente azulada -- não pode se
# confundir com a classe mais baixa de nenhuma rampa), mais escuro que
# COR_SEM_DADO para continuar distinto dele, e nunca branco. Tom suavizado
# (mais claro que a versão anterior, "#b5b0a1") para pesar menos no
# conjunto sem perder a distinção das duas outras cores neutras do mapa.
COR_ABAIXO_PISO = "#c5c0b1"

# Paletas sequenciais disponíveis para gerar_mapa(paleta=...). "azul" é a
# rampa customizada original do projeto (default -- garante que a saída do
# portal não muda); "roxo"/"verde" usam colormaps contínuos do matplotlib,
# sugeridos para comparação editorial das figuras do capítulo. Cada uma tem
# sua própria cor de corpo d'água, escolhida para não colidir com o hue da
# rampa nem com COR_ABAIXO_PISO -- ver gerar_mapa(mostrar_corpos_dagua=).
# "faixa" é o intervalo [0,1] amostrado dentro do colormap para as classes
# discretas do modo quantis (ver gerar_mapa, cores_classes). RAMPA_SEQUENCIAL_
# AZUL já começa num azul claro visível ("#cde2fb", não branco), por isso
# "azul" amostra o colormap inteiro (0,1) -- preserva a aparência já usada
# nas figuras anteriores do capítulo. "Purples"/"BuGn" do matplotlib, ao
# contrário, começam em branco/quase-branco -- amostrar (0,1) inteiro
# deixaria a classe mais clara ilegível (indistinguível do papel), então
# essas duas recortam a faixa para evitar as pontas quase-branca/quase-preta.
PALETAS = {
    "azul": {
        "cmap": lambda: LinearSegmentedColormap.from_list("taxa_azul", RAMPA_SEQUENCIAL_AZUL),
        "faixa": (0.0, 1.0),
        "cor_agua": "#7fbfae",  # verde-azulado (água), afastado dos tons de azul puro da rampa
    },
    "roxo": {
        "cmap": lambda: colormaps["Purples"],
        "faixa": (0.15, 0.95),
        "cor_agua": "#c9dce8",  # azul-cinza claro e dessaturado -- recua para o fundo em vez de competir com a rampa
    },
    "verde": {
        "cmap": lambda: colormaps["BuGn"],
        "faixa": (0.15, 0.95),
        "cor_agua": "#8b93d9",  # azul-violeta, afastado dos tons verde-azulados da rampa BuGn
    },
}


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


def _fmt_brl(valor: float, casas: int = 1) -> str:
    """Formata um número no padrão brasileiro (milhar com ponto, decimal com
    vírgula) -- para rótulos de legenda, não para dados (que seguem en-US
    nos CSVs do pipeline)."""
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "_MIL_").replace(".", ",").replace("_MIL_", ".")


def _populacao_referencia(ano_fim: int, tables_dir: Path = TABLES_DIR) -> pd.Series:
    """População por município no ano mais recente disponível até `ano_fim`,
    indexada por município -- usada para avaliar o piso `pop_minima` de
    gerar_mapa. Mesma convenção de POP_MINIMA nos notebooks
    (analise_exploratoria.ipynb, estudo_uruguaiana.ipynb): o piso é avaliado
    contra a população mais recente, não a soma de população-ano do período
    usada no denominador da taxa (carregar_taxa_periodo).
    """
    pop = pd.read_csv(tables_dir / "populacao_municipio_rs.csv")
    pop = pop[pop["ano"] <= ano_fim]
    ultimo_ano = pop["ano"].max()
    return pop[pop["ano"] == ultimo_ano].set_index("municipio")["populacao"]


def _classes_quantis(valores: pd.Series, n_classes: int) -> tuple[pd.Series, list[float]]:
    """Classifica `valores` em `n_classes` quantis (pd.qcut), retornando o
    índice de classe (0-based, por linha) e os limites de corte reais.

    Muitos municípios com taxa repetida/baixa podem gerar menos cortes únicos
    que n_classes -- duplicates="drop" aceita isso (classes reais < pedidas)
    em vez de levantar erro.
    """
    classes, edges = pd.qcut(valores, n_classes, labels=False, retbins=True, duplicates="drop")
    return classes, list(edges)


def _corpos_dagua(malha: gpd.GeoSeries, ratio: float = 0.05, n_maiores: int = 2) -> gpd.GeoSeries:
    """Deriva a silhueta de Lagoa dos Patos e Lagoa Mirim a partir da própria
    malha municipal do IBGE, sem depender de nenhuma fonte de dados nova.

    A malha (`data/raw/malha_municipios_rs.geojson`, via
    src/fetch_malha_municipios.py) só tem polígonos de município -- nenhuma
    feição de corpo d'água. As duas lagoas não formam um buraco fechado na
    malha (o teste de anéis interiores de unary_union(malha) dá zero buracos)
    porque as duas tocam a borda externa do estado (Patos abre para o
    oceano perto de Rio Grande, Mirim é fronteira com o Uruguai) em vez de
    ficarem cercadas por município em todos os lados.

    Em vez disso, comparamos um "concave hull" (contorno côncavo, que
    acompanha a costa de perto -- ratio pequeno) da união dos municípios
    contra a própria união: a diferença entre os dois recupera exatamente as
    reentrâncias da costa que a malha deixa vazias, e as duas maiores dessas
    reentrâncias são as duas lagoas -- confirmado comparando os limites
    (bounds) resultantes contra a extensão geográfica conhecida de cada uma
    (Patos: ~29,9-32,2°S x 50,5-52,3°W; Mirim, porção no RS: ~32,1-33,0°S x
    52,6-53,4°W). Com ratio=0.05 essas duas saem isoladas e >4x maiores que
    o próximo fragmento (concavidades reais da fronteira oeste/litoral norte,
    não tratadas aqui). Testamos alternativas antes de chegar nesta: (1)
    buracos internos -- zero, não fecham; (2) hull convexo -- mistura as
    lagoas com grandes concavidades da fronteira oeste (não-RS) num único
    polígono; (3) buscar a geometria em fontes externas (Overpass/OSM deu
    timeout; Nominatim só devolveu uma linha simplificada, sem polígono
    utilizável) -- descartado para não introduzir uma fonte de dados nova,
    não testada, fora do pipeline SIP/PROCERGS+IBGE já estabelecido.
    """
    uniao = unary_union(malha.values)
    hull = concave_hull(uniao, ratio=ratio)
    diff = hull.difference(uniao)
    geoms = list(diff.geoms) if diff.geom_type == "MultiPolygon" else [diff]
    geoms.sort(key=lambda p: p.area, reverse=True)
    return gpd.GeoSeries(geoms[:n_maiores], crs=malha.crs)


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
    classificacao: str = "continua",
    n_classes: int = 5,
    pop_minima: float | None = None,
    dpi: int = 150,
    formato: str = "png",
    paleta: str = "azul",
    mostrar_corpos_dagua: bool = False,
) -> tuple[Path, gpd.GeoDataFrame]:
    """Gera o mapa choropleth de um tipo de crime.

    Os defaults (classificacao="continua", pop_minima=None, dpi=150,
    formato="png", paleta="azul", mostrar_corpos_dagua=False) reproduzem
    exatamente o comportamento original -- rampa contínua min-max sobre os
    13 tons de RAMPA_SEQUENCIAL_AZUL, sem piso populacional, sem corpos
    d'água -- para não alterar a saída de quem já chama esta função
    (build_site_data.py via carregar_taxa_periodo, notebooks/analise_espacial.ipynb).

    paleta escolhe a rampa sequencial ("azul"/"roxo"/"verde", ver PALETAS).
    mostrar_corpos_dagua=True desenha Lagoa dos Patos e Lagoa Mirim (ver
    _corpos_dagua) numa cor própria por paleta, com entrada na legenda --
    sem isso, a malha do IBGE não tem feição de água e essa área some como
    fundo branco do eixo.

    classificacao="quantis" classifica em `n_classes` quantis (pd.qcut) em
    vez de interpolação contínua. pop_minima, se informado, tira da
    classificação os municípios com população abaixo do piso (mesma
    convenção de POP_MINIMA nos notebooks analise_exploratoria.ipynb e
    estudo_uruguaiana.ipynb) e os pinta com COR_ABAIXO_PISO (cinza claro
    neutro e quente, preenchimento sólido), numa entrada própria da
    legenda -- nunca branco, nunca igual à classe mais baixa da rampa azul
    nem a "sem dado" (COR_SEM_DADO, para município sem taxa por outro
    motivo, ex. malha sem correspondência de nome).

    dpi/formato controlam a saída (formato aceita "png", "pdf" ou "svg") --
    usados por src/analysis/figuras_capitulo.py para gerar em resolução de
    impressão, diferente do padrão do portal.

    Diagnóstico extra fica em gdf.attrs (não muda a assinatura de retorno):
    gdf.attrs["quantis_edges"]/["quantis_n_classes"] quando classificacao=
    "quantis"; coluna gdf["abaixo_piso"] quando pop_minima é informado.
    """
    if classificacao not in {"continua", "quantis"}:
        raise ValueError(f"classificacao inválida: {classificacao!r} (use 'continua' ou 'quantis')")
    if formato not in {"png", "pdf", "svg"}:
        raise ValueError(f"formato inválido: {formato!r} (use 'png', 'pdf' ou 'svg')")
    if paleta not in PALETAS:
        raise ValueError(f"paleta inválida: {paleta!r} (use {', '.join(repr(p) for p in PALETAS)})")

    gdf = montar_geodataframe(tipo_crime, ano_inicio, ano_fim)
    gdf_plot = gdf.to_crs(CRS_PLOT)

    sem_dado_mask = gdf_plot["taxa_por_100mil_hab"].isna()

    piso_mask = pd.Series(False, index=gdf_plot.index)
    if pop_minima is not None:
        pop_ref = _populacao_referencia(ano_fim)
        gdf_plot["populacao_referencia"] = gdf_plot["municipio"].map(pop_ref)
        piso_mask = (~sem_dado_mask) & (gdf_plot["populacao_referencia"] < pop_minima)
        gdf["abaixo_piso"] = piso_mask.values
        gdf.attrs["pop_minima"] = pop_minima

    normal_mask = ~sem_dado_mask & ~piso_mask

    cmap = PALETAS[paleta]["cmap"]()
    cor_agua = PALETAS[paleta]["cor_agua"]
    faixa_lo, faixa_hi = PALETAS[paleta]["faixa"]

    fig, ax = plt.subplots(figsize=(8, 8))

    if classificacao == "continua" and not piso_mask.any() and not mostrar_corpos_dagua and paleta == "azul":
        # Caminho original, inalterado -- garante saída idêntica ao
        # comportamento anterior para os defaults de sempre (e também
        # quando pop_minima é informado mas ninguém fica abaixo dele).
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
    elif classificacao == "continua":
        # pop_minima informado e com municípios abaixo dele: mesma rampa
        # contínua, mas o piso sai da normalização e vai por cima, com
        # preenchimento sólido próprio.
        gdf_plot[normal_mask].plot(
            column="taxa_por_100mil_hab",
            cmap=cmap,
            linewidth=0.2,
            edgecolor="white",
            legend=True,
            legend_kwds={"label": "Casos por 100 mil hab.", "shrink": 0.6},
            ax=ax,
        )
        if sem_dado_mask.any():
            gdf_plot[sem_dado_mask].plot(color=COR_SEM_DADO, linewidth=0.2, edgecolor="white", ax=ax)
        gdf_plot[piso_mask].plot(color=COR_ABAIXO_PISO, linewidth=0.2, edgecolor="white", ax=ax)
        legend_handles_secundaria = [
            Patch(
                facecolor=COR_ABAIXO_PISO,
                edgecolor="none",
                label=f"População inferior a {_fmt_brl(pop_minima, 0)} hab.",
            )
        ]
        if mostrar_corpos_dagua:
            agua = _corpos_dagua(gdf.geometry).to_crs(CRS_PLOT)
            agua.plot(color=cor_agua, linewidth=0.2, edgecolor="white", ax=ax)
            legend_handles_secundaria.append(
                Patch(facecolor=cor_agua, edgecolor="none", label="Corpos d'água (Lagoa dos Patos / Mirim)")
            )
        ax.legend(handles=legend_handles_secundaria, loc="lower right", fontsize=8, frameon=False)
    else:  # classificacao == "quantis"
        valores = gdf_plot.loc[normal_mask, "taxa_por_100mil_hab"]
        classes, edges = _classes_quantis(valores, n_classes)
        n_classes_reais = len(edges) - 1
        cores_classes = [
            cmap(faixa_lo + (faixa_hi - faixa_lo) * i / max(n_classes_reais - 1, 1))
            for i in range(n_classes_reais)
        ]
        gdf.attrs["quantis_edges"] = edges
        gdf.attrs["quantis_n_classes"] = n_classes_reais

        for i in range(n_classes_reais):
            subset_idx = valores.index[classes == i]
            if len(subset_idx) == 0:
                continue
            gdf_plot.loc[subset_idx].plot(color=cores_classes[i], linewidth=0.2, edgecolor="white", ax=ax)

        legend_handles = [
            Patch(
                facecolor=cores_classes[i],
                edgecolor="none",
                label=f"{_fmt_brl(edges[i], 1)} – {_fmt_brl(edges[i + 1], 1)}",
            )
            for i in range(n_classes_reais)
        ]
        if piso_mask.any():
            gdf_plot[piso_mask].plot(color=COR_ABAIXO_PISO, linewidth=0.2, edgecolor="white", ax=ax)
            legend_handles.append(
                Patch(
                    facecolor=COR_ABAIXO_PISO,
                    edgecolor="none",
                    label=f"População inferior a {_fmt_brl(pop_minima, 0)} hab.",
                )
            )
        if sem_dado_mask.any():
            gdf_plot[sem_dado_mask].plot(color=COR_SEM_DADO, linewidth=0.2, edgecolor="white", ax=ax)
            legend_handles.append(Patch(facecolor=COR_SEM_DADO, edgecolor="none", label="Sem dado"))
        if mostrar_corpos_dagua:
            agua = _corpos_dagua(gdf.geometry).to_crs(CRS_PLOT)
            agua.plot(color=cor_agua, linewidth=0.2, edgecolor="white", ax=ax)
            legend_handles.append(
                Patch(facecolor=cor_agua, edgecolor="none", label="Corpos d'água (Lagoa dos Patos / Mirim)")
            )

        ax.legend(
            handles=legend_handles,
            loc="lower left",
            fontsize=8,
            frameon=False,
            title="Casos por 100 mil hab.",
            title_fontsize=8,
        )

    ax.set_axis_off()
    ax.set_title(f"{tipo_crime} — taxa por 100 mil hab. ({ano_inicio}–{ano_fim})\nRio Grande do Sul, por município")

    caminho_saida = caminho_saida or (
        FIGURES_DIR / f"choropleth_{slug_tipo_crime(tipo_crime)}_{ano_inicio}_{ano_fim}.{formato}"
    )
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(caminho_saida, dpi=dpi, bbox_inches="tight")
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
