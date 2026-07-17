"""Prepara os dados do portal estático em docs/ e do dataset tratado em
data/processed/ -- lê o que já foi gerado pelo pipeline (outputs/tables/,
outputs/figures/) e pelas notebooks (outputs/reports/), sem recalcular
nenhuma análise. Roda depois de: src/load_data.py, src/fetch_populacao.py,
src/fetch_malha_municipios.py, e as 4 notebooks em notebooks/.

Uso: python -m src.build_site_data
"""

import json
import shutil
from pathlib import Path

import pandas as pd

from src.analysis.mapa_choropleth import carregar_taxa_periodo
from src.fetch_malha_municipios import carregar_malha_com_municipio

ROOT = Path(__file__).resolve().parent.parent
TABLES_DIR = ROOT / "outputs" / "tables"
FIGURES_DIR = ROOT / "outputs" / "figures"
REPORTS_DIR = ROOT / "outputs" / "reports"
MAPS_DIR = ROOT / "outputs" / "maps"
PROCESSED_DIR = ROOT / "data" / "processed"
DOCS_DATA_DIR = ROOT / "docs" / "assets" / "data"

TIPOS_CRIME = [
    "Ameaça",
    "Estupro",
    "Feminicídio Consumado",
    "Feminicídio Tentado",
    "Lesão Corporal",
]
MUNICIPIO_NAO_IDENTIFICADO = "NÃO INFORMADO"

# Mesmo recorte (2021-2025) usado em notebooks/analise_espacial.ipynb para os
# mapas e o ranking por taxa -- mantém o portal consistente com o notebook.
ANO_INICIO_MAPA = 2021
ANO_FIM_MAPA = 2025

# PNGs de outputs/figures/ que o portal embute como imagem estática (mapas
# LISA e a série de escolhas do estudo de Uruguaiana não são recomputáveis em
# JS; os demais também são copiados para complementar os gráficos
# interativos com a figura exata gerada pela notebook).
FIGURAS_PARA_PORTAL = [
    "choropleth_ameaca_2021_2025.png",
    "choropleth_estupro_2021_2025.png",
    "choropleth_feminicidio_consumado_2021_2025.png",
    "choropleth_feminicidio_tentado_2021_2025.png",
    "choropleth_lesao_corporal_2021_2025.png",
    "lisa_ameaca_2021_2025.png",
    "lisa_estupro_2021_2025.png",
    "lisa_lesao_corporal_2021_2025.png",
    "uruguaiana_perfil_taxa_vs_estado.png",
    "uruguaiana_serie_anual.png",
    "uruguaiana_serie_mensal.png",
    "uruguaiana_ranking_percentil.png",
    "uruguaiana_vs_corede_vs_estado.png",
    "uruguaiana_porte_fronteira.png",
    "exploratoria_totais_por_tipo.png",
    "exploratoria_serie_anual_tipo.png",
    "exploratoria_ranking_top15_absoluto.png",
    "exploratoria_concentracao_top10.png",
    "exploratoria_ranking_taxa_2012_2025.png",
    "exploratoria_ranking_taxa_2021_2025.png",
    "exploratoria_poa_vs_estado_taxa.png",
    "inferencial_tendencia_anual.png",
    "inferencial_sazonalidade_mensal.png",
    "inferencial_correlacao_matriz.png",
    "inferencial_quebra_estrutural.png",
]


def preparar_dataset_processado() -> None:
    """Copia violencia_anual_municipio_taxa.csv para data/processed/, como o
    dataset tratado e citável do projeto (versionado no git, ao contrário de
    outputs/tables/*.csv, que é regenerável e não versionado)."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(TABLES_DIR / "violencia_anual_municipio_taxa.csv")
    destino = PROCESSED_DIR / "violencia_rs_municipio_ano.csv"
    df.to_csv(destino, index=False)

    n_municipios = df.municipio.nunique()
    ano_min, ano_max = int(df.ano.min()), int(df.ano.max())
    n_linhas = len(df)

    readme = f"""# data/processed/violencia_rs_municipio_ano.csv

Dataset tratado e citável do projeto -- consolida casos de violência contra as mulheres
e meninas no Rio Grande do Sul (fonte: SIP/PROCERGS) com população (IBGE) e taxa por
100 mil habitantes, por município, ano e tipo de crime. Gerado por `src/build_site_data.py`
a partir de `outputs/tables/violencia_anual_municipio_taxa.csv` (esse, sim, regenerável e
não versionado -- ver `.gitignore`).

Ao contrário de `outputs/tables/`, este arquivo **é versionado no git**: é o dataset
tratado pensado para citação e reuso externo, disponível mesmo sem rodar o pipeline
localmente.

## Colunas

| Coluna | Descrição |
|---|---|
| `municipio` | Nome do município (maiúsculas, sem acento -- convenção das planilhas originais da SIP/PROCERGS), ou `NÃO INFORMADO` (ver limitações abaixo) |
| `ano` | Ano de referência |
| `tipo_crime` | Uma de: Ameaça, Estupro, Feminicídio Consumado, Feminicídio Tentado, Lesão Corporal |
| `casos_total` | Total de casos no ano, no município, para o tipo de crime |
| `populacao` | População total do município no ano (estimativa IBGE; ver limitações) |
| `taxa_por_100mil_hab` | `casos_total / populacao * 100_000` |

## Cobertura

- {n_municipios} municípios, anos {ano_min}-{ano_max}, {n_linhas} linhas.
- 2026 é ano parcial (dados só até por volta de junho/2026) e não tem estimativa de
  população do IBGE ainda -- `populacao`/`taxa_por_100mil_hab` ficam vazios nesse ano.

## Limitações (ver também README.md e CLAUDE.md na raiz do repositório)

- **Taxa usa população total, não só mulheres** -- o IBGE só quebra população por sexo
  no ano de Censo; as estimativas intercensitárias só têm população total.
- **População de 2023 é interpolada, não medida** -- o IBGE não publicou a estimativa
  municipal de 2023 (ver `src/fetch_populacao.py`).
- **"NÃO INFORMADO"** é um valor de município em 2018 (Ameaça e Lesão Corporal): casos
  sem município identificado na base original, mantidos para não perder casos do total,
  mas não é um município real -- exclua-o de qualquer análise por município.

## Licença e citação

CC BY 4.0 -- ver `LICENSE` e `CITATION.cff` na raiz do repositório.
"""
    (PROCESSED_DIR / "README.md").write_text(readme, encoding="utf-8")
    print(f"data/processed/ pronto — {n_linhas} linhas, {n_municipios} municípios ({ano_min}-{ano_max})")


def gerar_dados_mapas() -> None:
    """Gera outputs/maps/: a malha de contorno dos municípios (um arquivo,
    reaproveitado por todas as camadas do Leaflet) e a taxa por 100 mil hab.
    de cada tipo de crime (JSON pequeno, {tipo_crime: {municipio: taxa}}),
    juntados no cliente ao trocar o seletor de tipo de crime."""
    MAPS_DIR.mkdir(parents=True, exist_ok=True)

    malha = carregar_malha_com_municipio()[["municipio", "geometry"]].dropna(subset=["municipio"])
    malha.to_file(MAPS_DIR / "municipios_rs.geojson", driver="GeoJSON")

    taxas: dict[str, dict[str, float]] = {}
    for tipo in TIPOS_CRIME:
        agregado = carregar_taxa_periodo(tipo, ANO_INICIO_MAPA, ANO_FIM_MAPA)
        agregado = agregado[agregado.municipio != MUNICIPIO_NAO_IDENTIFICADO]
        taxas[tipo] = {
            row.municipio: round(row.taxa_por_100mil_hab, 3) for row in agregado.itertuples()
        }
    (MAPS_DIR / "taxa_por_municipio.json").write_text(
        json.dumps(
            {
                "ano_inicio": ANO_INICIO_MAPA,
                "ano_fim": ANO_FIM_MAPA,
                "taxas": taxas,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"outputs/maps/ pronto — malha de {len(malha)} municípios + taxas de {len(TIPOS_CRIME)} tipos de crime")


def gerar_tabela_municipios_resumo() -> pd.DataFrame:
    """Tabela compacta município x taxa por tipo de crime (2021-2025, mesmo
    recorte do mapa), para a tabela pesquisável/ordenável de municipios.html.
    Não é um output do pipeline nem de notebook -- é só uma pivotagem para
    exibição, feita aqui mesmo."""
    partes = []
    for tipo in TIPOS_CRIME:
        agregado = carregar_taxa_periodo(tipo, ANO_INICIO_MAPA, ANO_FIM_MAPA)
        agregado = agregado[agregado.municipio != MUNICIPIO_NAO_IDENTIFICADO]
        agregado = agregado.rename(
            columns={
                "casos_total": f"casos_{tipo}",
                "taxa_por_100mil_hab": f"taxa_{tipo}",
            }
        )[["municipio", f"casos_{tipo}", f"taxa_{tipo}"]]
        partes.append(agregado.set_index("municipio"))

    resumo = pd.concat(partes, axis=1).reset_index()
    resumo["casos_geral"] = resumo[[f"casos_{t}" for t in TIPOS_CRIME]].sum(axis=1)
    for tipo in TIPOS_CRIME:
        resumo[f"taxa_{tipo}"] = resumo[f"taxa_{tipo}"].round(2)
    return resumo


def _csv_para_json(caminho_csv: Path, caminho_json: Path) -> None:
    df = pd.read_csv(caminho_csv)
    caminho_json.parent.mkdir(parents=True, exist_ok=True)
    df.to_json(caminho_json, orient="records", force_ascii=False, indent=2)


def preparar_dados_docs() -> None:
    """Monta docs/assets/data/ inteiro: tables/, reports/, maps/, figures/ --
    a cópia publicada que o GitHub Pages serve (sem etapa de build)."""
    docs_tables = DOCS_DATA_DIR / "tables"
    docs_reports = DOCS_DATA_DIR / "reports"
    docs_maps = DOCS_DATA_DIR / "maps"
    docs_figures = DOCS_DATA_DIR / "figures"
    for d in (docs_tables, docs_reports, docs_maps, docs_figures):
        d.mkdir(parents=True, exist_ok=True)

    # reports/ -- todas as tabelas de resultado estatístico geradas pelas
    # notebooks (exploratória, inferencial, estudos de caso), convertidas 1:1
    # para JSON. Genérico por design: qualquer novo notebook que salve um CSV
    # em outputs/reports/ é publicado aqui automaticamente, sem precisar tocar
    # este script -- é assim que um futuro estudo de caso de outro município
    # entra no portal.
    for csv_path in sorted(REPORTS_DIR.glob("*.csv")):
        _csv_para_json(csv_path, docs_reports / f"{csv_path.stem}.json")

    # tables/ -- série anual estadual (gráfico da index.html) e resumo por
    # município (tabela pesquisável de municipios.html).
    _csv_para_json(
        REPORTS_DIR / "exploratoria_serie_anual_tipo.csv",
        docs_tables / "totais_anuais_estado.json",
    )
    _csv_para_json(
        REPORTS_DIR / "exploratoria_totais_por_tipo.csv",
        docs_tables / "totais_por_tipo.json",
    )
    resumo_municipios = gerar_tabela_municipios_resumo()
    resumo_municipios.to_json(
        docs_tables / "municipios_resumo.json", orient="records", force_ascii=False, indent=2
    )

    # maps/ -- geojson de contorno + taxas por tipo de crime.
    shutil.copy2(MAPS_DIR / "municipios_rs.geojson", docs_maps / "municipios_rs.geojson")
    shutil.copy2(MAPS_DIR / "taxa_por_municipio.json", docs_maps / "taxa_por_municipio.json")

    # figures/ -- cópia das PNGs relevantes (mapas + Uruguaiana + exploratória/inferencial).
    faltando = []
    for nome in FIGURAS_PARA_PORTAL:
        origem = FIGURES_DIR / nome
        if not origem.exists():
            faltando.append(nome)
            continue
        shutil.copy2(origem, docs_figures / nome)
    if faltando:
        print(f"AVISO: {len(faltando)} figura(s) esperada(s) não encontrada(s) em outputs/figures/: {faltando}")

    print(
        f"docs/assets/data/ pronto — {len(list(docs_reports.glob('*.json')))} reports, "
        f"{len(list(docs_tables.glob('*.json')))} tables, "
        f"{len(list(docs_maps.glob('*')))} maps, "
        f"{len(list(docs_figures.glob('*.png')))} figuras"
    )


def main() -> None:
    preparar_dataset_processado()
    gerar_dados_mapas()
    preparar_dados_docs()


if __name__ == "__main__":
    main()
