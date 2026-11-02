"""Denominador das taxas da cadeia de análise do artigo: população feminina ou total.

POPULAÇÃO FEMININA ANUAL ESTIMADA, NÃO MEDIDA: população total do ano × razão feminina do
município no Censo 2022, suposta constante em 2018-2025 (ver denominador_feminino.py, que
também testa a suposição contra o Censo 2010). Como a razão é constante no período, as
mulheres-ano acumuladas são a razão vezes as pessoas-ano que montar_geodataframe já soma.

- "feminina" é o denominador do artigo e grava nos nomes canônicos de saída.
- "total" é o denominador do portal e da tabela suplementar; grava com o sufixo
  `_pop_total` e reproduz as tabelas anteriores a esta parametrização.

O piso populacional (5.000 habitantes) e a densidade continuam medidos em população total:
são porte do município, não denominador de taxa.

Pré-requisito do denominador feminino: python -m src.analysis.denominador_feminino, que
grava populacao_feminina_censos_rs.csv.
"""

import argparse
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

from src.analysis.mapa_choropleth import montar_geodataframe

TABLES_DIR = Path(__file__).resolve().parent.parent.parent / "outputs" / "tables"
POP_FEMININA_CSV = TABLES_DIR / "populacao_feminina_censos_rs.csv"
LISA_POR_MUNICIPIO_CSV = TABLES_DIR / "lisa_denominador_feminino_vs_total_2018_2025.csv"

DENOMINADORES = ("feminina", "total")
PADRAO = "feminina"
SUFIXO = {"feminina": "", "total": "_pop_total"}
CASOS_POR_HABITANTES = 100_000

UNIDADE = {"feminina": "mulheres-ano", "total": "pessoas-ano"}
DESCRICAO = {
    "feminina": (
        "população feminina anual ESTIMADA, não medida: população total do ano × razão feminina do "
        "município no Censo 2022 (razão suposta constante em 2018-2025)"
    ),
    "total": "população total (denominador do portal e da tabela suplementar)",
}


def validar(denominador: str) -> str:
    if denominador not in DENOMINADORES:
        raise ValueError(f"Denominador {denominador!r}; use um de {DENOMINADORES}.")
    return denominador


def caminho(base: Path, denominador: str) -> Path:
    """Nome canônico para o denominador feminino; sufixo _pop_total para o total."""
    return base.with_name(f"{base.stem}{SUFIXO[validar(denominador)]}{base.suffix}")


def razao_feminina() -> pd.Series:
    if not POP_FEMININA_CSV.exists():
        raise FileNotFoundError(
            f"{POP_FEMININA_CSV.name} ausente. Rode antes: python -m src.analysis.denominador_feminino"
        )
    return pd.read_csv(POP_FEMININA_CSV).set_index("municipio")["razao_feminina_2022"]


def fator(municipios: pd.Series, denominador: str) -> np.ndarray:
    """Multiplicador da população total: 1 no total, razão feminina no feminino."""
    if validar(denominador) == "total":
        return np.ones(len(municipios))
    r = municipios.map(razao_feminina())
    if r.isna().any():
        raise ValueError(f"Sem razão feminina para: {sorted(municipios[r.isna()])}")
    return r.to_numpy(dtype=float)


def montar_geodataframe_denominador(tipo: str, ano_inicio: int, ano_fim: int, denominador: str) -> gpd.GeoDataFrame:
    """montar_geodataframe com populacao_pessoas_ano e taxa no denominador pedido.

    As colunas mantêm os nomes originais para que os scripts a jusante não mudem; no
    feminino, populacao_pessoas_ano passa a conter mulheres-ano.
    """
    gdf = montar_geodataframe(tipo, ano_inicio, ano_fim)
    if validar(denominador) == "total":
        return gdf
    gdf = gdf.copy()
    gdf["populacao_pessoas_ano"] = gdf["populacao_pessoas_ano"] * fator(gdf["municipio"], denominador)
    gdf["taxa_por_100mil_hab"] = gdf["casos_total"] / gdf["populacao_pessoas_ano"] * CASOS_POR_HABITANTES
    return gdf


def lisa_referencia(denominador: str) -> pd.DataFrame:
    """LISA por município da semente 12345 e 99.999 permutações, calculado à parte por
    denominador_feminino.py; serve de conferência independente para a cadeia."""
    t = pd.read_csv(LISA_POR_MUNICIPIO_CSV)
    t = t[(t["denominador"] == validar(denominador)) & t["significativo_fdr"]]
    return t.assign(categoria=t["quadrante"].str.upper())[["tipo_crime", "municipio", "categoria"]]


def adicionar_argumento(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--denominador",
        choices=DENOMINADORES,
        default=PADRAO,
        help="feminina (artigo, nomes canônicos) ou total (portal e suplementar, sufixo _pop_total)",
    )
