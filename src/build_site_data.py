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

from src.analysis.figuras_capitulo import PALETA_OFICIAL
from src.analysis.mapa_choropleth import _populacao_referencia, carregar_taxa_periodo, paleta_stops
from src.analysis.periodo_padrao import ANO_FIM_ANALISE, ANO_INICIO_ANALISE
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

# Mesmo recorte (periodo_padrao.py, ver ANO_INICIO_ANALISE/ANO_FIM_ANALISE)
# usado em notebooks/analise_espacial.ipynb para os mapas e o ranking por
# taxa -- mantém o portal consistente com o notebook e com a Camada 2
# (tendência/sazonalidade/quebra/correlação). Import direto, não literal:
# este é o mesmo ponto único de decisão, não uma cópia que pode divergir.
ANO_INICIO_MAPA = ANO_INICIO_ANALISE
ANO_FIM_MAPA = ANO_FIM_ANALISE

# Auditoria metodológica, item 8: o mapa interativo mostra os 497
# municípios (nunca esconde nenhum, ao contrário das figuras estáticas do
# capítulo e da tabela de municípios, que já usam POP_MINIMA=5000 -- ver
# figuras_capitulo.py e tabela_agregacao_regional.py), mas os municípios
# abaixo do piso (a) são marcados como instáveis no popup/tooltip e (b)
# saem do cálculo do domínio (min/max) da rampa de cores -- mesmo piso e
# mesmo princípio de "sólido fora da rampa" das figuras estáticas
# (mapa_choropleth.py, COR_ABAIXO_PISO), aplicado aqui só à escala
# cromática do mapa interativo, não à visibilidade dos municípios.
POP_MINIMA_INSTABILIDADE = 5000

# PNGs de outputs/figures/ que o portal embute como imagem estática (a série
# de escolhas do estudo de Uruguaiana não é recomputável em
# JS; os demais também são copiados para complementar os gráficos
# interativos com a figura exata gerada pela notebook).
#
# choropleth_* (Camada 3, analise_espacial.ipynb) usam o sufixo
# {ANO_INICIO_ANALISE}_{ANO_FIM_ANALISE} = 2018_2025. exploratoria_ranking_
# taxa_2021_2025.png abaixo é diferente -- vem da Camada 1 (analise_
# exploratoria.ipynb), fora do escopo desta rodada, e continua com seu
# próprio recorte (2021-2025) independente deste.
# Relatórios de outputs/reports/ publicados em docs/assets/data/reports/, um
# JSON por CSV. A lista é a decisão de publicar, não o conteúdo da pasta: um
# CSV novo em outputs/reports/ só entra no portal se for acrescentado aqui
# (uruguaiana_lisa ficou de fora de propósito em 379f6b3).
RELATORIOS_PARA_PORTAL = [
    "exploratoria_concentracao_resumo",
    "exploratoria_concentracao_top10_com_poa",
    "exploratoria_concentracao_top10_sem_poa",
    "exploratoria_overlap_ranking_taxa",
    "exploratoria_poa_vs_estado_taxa",
    "exploratoria_ranking_taxa_2012_2025",
    "exploratoria_ranking_taxa_2021_2025",
    "exploratoria_ranking_top15_absoluto",
    "exploratoria_serie_anual_tipo",
    "exploratoria_totais_por_tipo",
    "inferencial_correlacao_matriz_casos_absolutos",
    "inferencial_correlacao_matriz_taxa_por_100mil_hab",
    "inferencial_correlacao_pares_casos_absolutos",
    "inferencial_correlacao_pares_taxa_por_100mil_hab",
    "inferencial_correlacao_pvalor_casos_absolutos",
    "inferencial_correlacao_pvalor_taxa_por_100mil_hab",
    "inferencial_quebra_estrutural_chow",
    "inferencial_quebra_estrutural_mannwhitney",
    "inferencial_sazonalidade_destaques",
    "inferencial_sazonalidade_kruskal",
    "inferencial_tendencia_anual",
    "uruguaiana_comparacao_corede",
    "uruguaiana_comparacao_porte",
    "uruguaiana_comparacao_sazonalidade",
    "uruguaiana_comparacao_tendencia",
    "uruguaiana_perfil",
    "uruguaiana_ranking_percentil",
    "uruguaiana_resumo_corede",
    "uruguaiana_resumo_porte",
]

FIGURAS_PARA_PORTAL = [
    "choropleth_ameaca_2018_2025.png",
    "choropleth_estupro_2018_2025.png",
    "choropleth_feminicidio_consumado_2018_2025.png",
    "choropleth_feminicidio_tentado_2018_2025.png",
    "choropleth_lesao_corporal_2018_2025.png",
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

    pop_referencia = _populacao_referencia(ANO_FIM_MAPA)
    municipios_abaixo_piso = sorted(pop_referencia[pop_referencia < POP_MINIMA_INSTABILIDADE].index)

    # Domínio da rampa de cores calculado aqui (server-side), não no cliente:
    # exclui os municípios abaixo do piso do min/max de cada tipo de crime,
    # para eles não esticarem a escala cromática dos ~266 municípios
    # elegíveis -- mesmo princípio das figuras estáticas do capítulo
    # (mapa_choropleth.py, classificacao="continua" com pop_minima), que já
    # tiram o piso da normalização da rampa contínua. Os municípios abaixo
    # do piso continuam em "taxas" (a consulta municipal precisa encontrá-
    # los) -- só saem do cálculo de min/max.
    abaixo_piso_set = set(municipios_abaixo_piso)
    dominio_por_tipo: dict[str, dict[str, float]] = {}
    for tipo, valores in taxas.items():
        elegiveis = [v for m, v in valores.items() if m not in abaixo_piso_set]
        dominio_por_tipo[tipo] = {
            "min": round(min(elegiveis), 3),
            "max": round(max(elegiveis), 3),
        }

    # Paleta gravada aqui, não hardcoded em maps.js: mesma fonte (PALETAS em
    # mapa_choropleth.py) e mesma paleta (PALETA_OFICIAL, hoje "roxo") que
    # figuras_capitulo.py usa para as figuras estáticas do capítulo/artigo --
    # ponto único de decisão de cor, o mapa interativo herda qualquer troca
    # futura de PALETA_OFICIAL sem editar JS. Ver mapa_choropleth.paleta_stops
    # e docs/assets/js/maps.js:rampColor (interpola linearmente entre esses
    # tons, mesma lógica de antes, só que os tons vêm do JSON agora).
    paleta_tons = paleta_stops(PALETA_OFICIAL)

    (MAPS_DIR / "taxa_por_municipio.json").write_text(
        json.dumps(
            {
                "ano_inicio": ANO_INICIO_MAPA,
                "ano_fim": ANO_FIM_MAPA,
                "taxas": taxas,
                "dominio_por_tipo": dominio_por_tipo,
                "piso_populacional_instabilidade": POP_MINIMA_INSTABILIDADE,
                "municipios_abaixo_piso": municipios_abaixo_piso,
                "paleta": paleta_tons,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(
        f"outputs/maps/ pronto — malha de {len(malha)} municípios + taxas de {len(TIPOS_CRIME)} tipos de crime "
        f"+ {len(municipios_abaixo_piso)} municípios marcados abaixo do piso de {POP_MINIMA_INSTABILIDADE}"
    )


def gerar_tabela_municipios_resumo() -> pd.DataFrame:
    """Tabela compacta município x taxa por tipo de crime (ANO_INICIO_MAPA-
    ANO_FIM_MAPA, mesmo recorte do mapa), para a tabela pesquisável/
    ordenável de municipios.html.
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

    # reports/ -- tabelas de resultado das notebooks, convertidas 1:1 para
    # JSON, só as de RELATORIOS_PARA_PORTAL.
    for nome in RELATORIOS_PARA_PORTAL:
        _csv_para_json(REPORTS_DIR / f"{nome}.csv", docs_reports / f"{nome}.json")

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


def gerar_populacao_censo(municipio: str, ano_censo: int = 2022) -> None:
    """População oficial do último Censo (2022) para um município -- não é
    uma estimativa intercensitária (o Censo substitui a estimativa no seu
    próprio ano, ver docstring de src/fetch_populacao.py). Não depende de
    nenhum notebook: lê direto de outputs/tables/populacao_municipio_rs.csv,
    a mesma tabela que load_data.py já usa para calcular taxa_por_100mil_hab.
    Genérico por município -- reaproveitável por qualquer estudo de caso."""
    pop = pd.read_csv(TABLES_DIR / "populacao_municipio_rs.csv")
    linha = pop[(pop.municipio == municipio) & (pop.ano == ano_censo)]
    if linha.empty:
        print(f"AVISO: sem população de {ano_censo} para {municipio} — {municipio}_populacao_censo.json não gerado")
        return

    docs_tables = DOCS_DATA_DIR / "tables"
    docs_tables.mkdir(parents=True, exist_ok=True)
    slug = municipio.lower().replace(" ", "_")
    dados = {
        "municipio": municipio,
        "ano_censo": ano_censo,
        "populacao_censo": int(linha.populacao.iloc[0]),
    }
    (docs_tables / f"{slug}_populacao_censo.json").write_text(
        json.dumps(dados, ensure_ascii=False), encoding="utf-8"
    )
    print(f"{slug}_populacao_censo.json pronto — {municipio}, Censo {ano_censo}: {dados['populacao_censo']} hab.")


def main() -> None:
    preparar_dataset_processado()
    gerar_dados_mapas()
    preparar_dados_docs()
    gerar_populacao_censo("URUGUAIANA")


if __name__ == "__main__":
    main()
