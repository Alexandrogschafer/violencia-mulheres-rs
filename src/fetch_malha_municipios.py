"""Busca a malha geográfica (geojson) dos municípios do RS e a tabela de
código IBGE x nome de município, para a Camada 3 (análise espacial).

A malha (API de malhas territoriais do IBGE) só identifica cada polígono
pelo código IBGE de 7 dígitos ("codarea"), sem nome de município -- por
isso a tabela de código x nome (API de localidades) é buscada à parte e é
o que permite juntar a malha com violencia_anual_municipio_taxa.csv (que
usa nome, não código). Join por código é mais confiável que por nome: nome
normalizado ainda depende de mapear as poucas grafias em que o IBGE diverge
do padrão SSP/PROCERGS (ver ALIAS_MUNICIPIO em fetch_populacao.py).
"""

import json
from pathlib import Path

import geopandas as gpd
import pandas as pd

from src.fetch_populacao import get_json, normaliza_municipio

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "tables"

MALHA_PATH = RAW_DIR / "malha_municipios_rs.geojson"
CODIGO_NOME_PATH = OUTPUT_DIR / "municipio_codigo_ibge.csv"

UF_RS = 43

# "intermediaria" (~900KB) em vez de "maxima" (~3.8MB): resolução de borda
# mais que suficiente tanto para o choropleth estadual quanto para o cálculo
# de vizinhança (contiguidade) usado em autocorrelacao_espacial.py/
# clusters_lisa.py, a um quinto do tamanho de arquivo.
URL_MALHA = (
    "https://servicodados.ibge.gov.br/api/v3/malhas/estados/{uf}"
    "?formato=application/vnd.geo+json&intrarregiao=municipio&qualidade=intermediaria"
).format(uf=UF_RS)

URL_LOCALIDADES = (
    f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{UF_RS}/municipios"
)


def busca_malha() -> dict:
    """Busca o geojson dos ~497 municípios do RS. Cada feature tem só
    properties.codarea (código IBGE de 7 dígitos) -- sem nome de município.
    """
    return get_json(URL_MALHA)


def busca_codigo_nome() -> list[tuple[str, str]]:
    """Busca (codigo_ibge, municipio) para os municípios do RS, com o nome
    já normalizado no padrão do projeto (normaliza_municipio, reaproveitado
    de fetch_populacao.py -- mesma fonte de divergências de grafia).
    """
    municipios = get_json(URL_LOCALIDADES)
    return [(str(m["id"]), normaliza_municipio(m["nome"])) for m in municipios]


def carregar_malha_com_municipio() -> gpd.GeoDataFrame:
    """Carrega a malha geográfica (data/raw/malha_municipios_rs.geojson) já
    com a coluna 'municipio' (nome normalizado), via join por código IBGE
    contra outputs/tables/municipio_codigo_ibge.csv -- ver docstring do
    módulo sobre por que o join é por código, não por nome.
    """
    malha = gpd.read_file(MALHA_PATH)
    codigo_nome = pd.read_csv(CODIGO_NOME_PATH, dtype={"codigo_ibge": str})
    return malha.merge(codigo_nome, left_on="codarea", right_on="codigo_ibge", how="left")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    malha = busca_malha()
    with open(MALHA_PATH, "w", encoding="utf-8") as f:
        json.dump(malha, f, ensure_ascii=False)
    print(f"Salvo em {MALHA_PATH} — {len(malha['features'])} features")

    codigo_nome = busca_codigo_nome()
    with open(CODIGO_NOME_PATH, "w", encoding="utf-8") as f:
        f.write("codigo_ibge,municipio\n")
        for codigo, municipio in codigo_nome:
            f.write(f"{codigo},{municipio}\n")
    print(f"Salvo em {CODIGO_NOME_PATH} — {len(codigo_nome)} municípios")


if __name__ == "__main__":
    main()
