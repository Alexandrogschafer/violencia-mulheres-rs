"""Auditoria metodológica, item 3: avalia a possibilidade de usar
população feminina como denominador em vez de população total.

Não existe série municipal ANUAL de população feminina cobrindo 2018-2025
(a DEE-RS tinha uma série, mas parou em 2021 -- ver src/load_data.py). O
IBGE, porém, publica população feminina por município no ano de Censo: a
tabela 9514 do SIDRA ("População residente, por sexo, idade e forma de
declaração da idade") tem população feminina municipal para 2022 -- o
único ano de Censo dentro do recorte 2018-2025 usado no capítulo.

Este módulo busca essa única série censitária (sem interpolar nenhum outro
ano -- não há como aproximar população feminina de anos não-censitários
sem inventar dado que a fonte não publicou) e compara, só para 2022,
contra a população total: taxas, ranking e classe de quantil por
município, para as 3 categorias mapeadas.

Limitação que o resultado NÃO resolve: é uma comparação de um único ano
(2022), não do período 2018-2025 usado nas figuras do capítulo -- não dá
para saber se a diferença encontrada em 2022 é representativa dos outros
7 anos.

Uso: python -m src.analysis.auditoria.populacao_feminina
"""

import json
import urllib.parse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from src.fetch_populacao import get_json, normaliza_municipio

TABLES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "outputs" / "tables"
SAIDA_DIR = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "publicacoes"
    / "cap_geotecnologias"
    / "00_gestao"
    / "auditoria"
)

ANO_CENSO = 2022
UF_RS = 43
TABELA_SIDRA = 9514  # "População residente, por sexo, idade e forma de declaração da idade"
CATEGORIA_MULHERES = 5
CATEGORIA_IDADE_TOTAL = 100362

MUNICIPIO_NAO_INFORMADO = "NÃO INFORMADO"
CATEGORIAS = ["Ameaça", "Estupro", "Lesão Corporal"]
N_CLASSES = 5


def buscar_populacao_feminina_2022() -> pd.DataFrame:
    """Busca direta na API do IBGE (tabela 9514) -- não usa nenhum arquivo
    já em outputs/tables/, porque nenhum contém população por sexo."""
    query = urllib.parse.urlencode(
        {"localidades": f"N6[N3[{UF_RS}]]", "classificacao": f"2[{CATEGORIA_MULHERES}]|287[{CATEGORIA_IDADE_TOTAL}]"},
        safe="[]|",
    )
    url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{TABELA_SIDRA}/periodos/{ANO_CENSO}/variaveis/93?{query}"
    resposta = get_json(url)
    series = resposta[0]["resultados"][0]["series"]
    linhas = []
    for serie in series:
        municipio = normaliza_municipio(serie["localidade"]["nome"])
        valor = serie["serie"].get(str(ANO_CENSO))
        if valor is None or not str(valor).isdigit():
            raise ValueError(f"População feminina inesperada para {municipio}: {valor!r}")
        linhas.append({"municipio": municipio, "populacao_feminina_2022": int(valor)})
    return pd.DataFrame(linhas)


def comparar_denominador(tipo_crime: str, pop_feminina: pd.DataFrame) -> pd.DataFrame:
    casos = pd.read_csv(TABLES_DIR / "violencia_anual_municipio.csv")
    casos_2022 = casos[
        (casos["tipo_crime"] == tipo_crime)
        & (casos["ano"] == ANO_CENSO)
        & (casos["municipio"] != MUNICIPIO_NAO_INFORMADO)
    ][["municipio", "casos_total"]]

    pop_total = pd.read_csv(TABLES_DIR / "populacao_municipio_rs.csv")
    pop_total_2022 = pop_total[pop_total["ano"] == ANO_CENSO][["municipio", "populacao"]].rename(
        columns={"populacao": "populacao_total_2022"}
    )

    base = casos_2022.merge(pop_total_2022, on="municipio", how="inner").merge(
        pop_feminina, on="municipio", how="inner"
    )
    if len(base) != 497:
        raise RuntimeError(
            f"Esperava 497 municípios após o join de {tipo_crime}, obteve {len(base)} -- "
            "checar nomes não casados entre as três fontes antes de prosseguir."
        )

    base["taxa_pop_total"] = base["casos_total"] / base["populacao_total_2022"] * 100_000
    base["taxa_pop_feminina"] = base["casos_total"] / base["populacao_feminina_2022"] * 100_000

    base["ranking_pop_total"] = base["taxa_pop_total"].rank(ascending=False, method="min")
    base["ranking_pop_feminina"] = base["taxa_pop_feminina"].rank(ascending=False, method="min")
    base["diferenca_ranking"] = (base["ranking_pop_total"] - base["ranking_pop_feminina"]).abs()

    base["classe_pop_total"] = pd.qcut(base["taxa_pop_total"], N_CLASSES, labels=False, duplicates="drop")
    base["classe_pop_feminina"] = pd.qcut(base["taxa_pop_feminina"], N_CLASSES, labels=False, duplicates="drop")
    base["mesma_classe"] = base["classe_pop_total"] == base["classe_pop_feminina"]

    base.insert(0, "tipo_crime", tipo_crime)
    return base


def main() -> None:
    print("Buscando população feminina por município (Censo 2022, tabela SIDRA 9514)...")
    pop_feminina = buscar_populacao_feminina_2022()
    SAIDA_DIR.mkdir(parents=True, exist_ok=True)
    pop_feminina.to_csv(SAIDA_DIR / "populacao_feminina_2022.csv", index=False)
    print(f"{len(pop_feminina)} municípios obtidos.\n")

    resultados = []
    for tipo in CATEGORIAS:
        comp = comparar_denominador(tipo, pop_feminina)
        resultados.append(comp)

        rho, p = stats.spearmanr(comp["taxa_pop_total"], comp["taxa_pop_feminina"])
        pct_mesma_classe = 100 * comp["mesma_classe"].mean()
        maior_salto_ranking = int(comp["diferenca_ranking"].max())

        print(f"=== {tipo} ({ANO_CENSO}, único ano de Censo no recorte) ===")
        print(f"  Spearman rho (taxa pop. total x taxa pop. feminina): {rho:.4f} (p={p:.2e})")
        print(f"  Municípios que ficam na mesma classe de quantil nos dois denominadores: {pct_mesma_classe:.1f}%")
        print(f"  Maior salto de posição no ranking entre os dois denominadores: {maior_salto_ranking} posições")
        print()

    tabela_completa = pd.concat(resultados, ignore_index=True)
    caminho = SAIDA_DIR / "comparacao_denominador_2022.csv"
    tabela_completa.to_csv(caminho, index=False)
    print(f"Tabela completa (497 municípios x 3 categorias) salva em {caminho}")


if __name__ == "__main__":
    main()
