"""Correlação de Spearman entre os 5 tipos de crime, calculada por
município: cada município vira uma observação, e a variável é o total
acumulado 2018-2025 (periodo_padrao.py) daquele tipo de crime ali. Mede se
municípios com mais casos de um tipo tendem a ter mais (ou menos) casos de
outro tipo -- não diz nada sobre a relação mês a mês dentro de um
município.

Usa Spearman (não Pearson) porque a relação entre volumes de crime entre
municípios tende a ser monotônica mas não linear (municípios grandes têm
muito mais casos de tudo, de forma desproporcional), e Spearman é robusto a
outliers como a capital/região metropolitana.

ANO_INICIO_ANALISE/ANO_FIM_ANALISE vêm do ponto único de decisão em
periodo_padrao.py -- as duas variantes (casos absolutos e taxa) usavam
janelas diferentes entre si (2012-2026 vs. 2012-2025, ver
carregar_taxas_por_municipio) só porque a taxa precisa de população e 2026
não tem estimativa do IBGE ainda; com o recorte comum a 2018-2025 essa
diferença desaparece -- 2026 já sai das duas por ser parcial, e agora
2012-2017 também sai (fora do escopo desta rodada: alinha correlação ao
mesmo recorte de tendência/sazonalidade/quebra/mapas).
"""

from itertools import combinations
from pathlib import Path

import pandas as pd
from scipy import stats

from src.analysis.periodo_padrao import ANO_FIM_ANALISE, ANO_INICIO_ANALISE
from src.load_data import CASOS_POR_HABITANTES

TABLES_DIR = Path(__file__).resolve().parent.parent.parent / "outputs" / "tables"

# Linha catch-all que aparece em algumas planilhas fonte (ex.: 2018, Ameaça e
# Lesão Corporal) para casos sem município identificado. Não é um município
# real e só tem dado em 2 das 5 categorias, o que gera NaN na tabela larga e
# quebra a correlação inteira (spearmanr propaga NaN entre colunas) -- por
# isso é excluída aqui, antes do pivot.
MUNICIPIO_NAO_IDENTIFICADO = "NÃO INFORMADO"


def carregar_totais_por_municipio(caminho: Path | None = None) -> pd.DataFrame:
    """Total acumulado ANO_INICIO_ANALISE-ANO_FIM_ANALISE por município e
    tipo de crime, em formato largo (uma coluna por tipo de crime, uma
    linha por município).
    """
    caminho = caminho or TABLES_DIR / "violencia_anual_municipio.csv"
    df = pd.read_csv(caminho)
    df = df[
        (df["municipio"] != MUNICIPIO_NAO_IDENTIFICADO)
        & (df["ano"] >= ANO_INICIO_ANALISE)
        & (df["ano"] <= ANO_FIM_ANALISE)
    ]
    totais = df.groupby(["municipio", "tipo_crime"], as_index=False)["casos_total"].sum()
    return totais.pivot(index="municipio", columns="tipo_crime", values="casos_total")


def carregar_taxas_por_municipio(caminho: Path | None = None) -> pd.DataFrame:
    """Taxa acumulada por município e tipo de crime, em formato largo.

    A taxa acumulada é soma(casos) / soma(população-ano) * 100 mil -- não a
    média simples das taxas anuais. Isso pondera corretamente os anos/
    municípios por tamanho da população (a mesma lógica de taxa de
    incidência usada em epidemiologia), em vez de dar peso igual a um ano
    com população pequena e um com população grande.

    Restrito a ANO_INICIO_ANALISE-ANO_FIM_ANALISE, igual à versão em
    número absoluto de casos (periodo_padrao.py já exclui 2026 nos dois
    casos -- o dropna(populacao) abaixo continua aqui como salvaguarda,
    não como o filtro principal de 2026).
    """
    caminho = caminho or TABLES_DIR / "violencia_anual_municipio_taxa.csv"
    df = pd.read_csv(caminho)
    df = df[
        (df["municipio"] != MUNICIPIO_NAO_IDENTIFICADO)
        & (df["ano"] >= ANO_INICIO_ANALISE)
        & (df["ano"] <= ANO_FIM_ANALISE)
    ]
    df = df.dropna(subset=["populacao"])
    agregado = df.groupby(["municipio", "tipo_crime"], as_index=False).agg(
        casos_total=("casos_total", "sum"),
        populacao_pessoas_ano=("populacao", "sum"),
    )
    agregado["taxa_por_100mil_hab"] = (
        agregado["casos_total"] / agregado["populacao_pessoas_ano"] * CASOS_POR_HABITANTES
    )
    return agregado.pivot(index="municipio", columns="tipo_crime", values="taxa_por_100mil_hab")


def calcular_matriz_correlacao(totais_largo: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Matriz de correlação de Spearman entre tipos de crime (colunas) e a
    matriz de p-valores correspondente, ambas indexadas por tipo_crime.
    """
    resultado = stats.spearmanr(totais_largo.to_numpy())
    tipos = totais_largo.columns
    matriz_corr = pd.DataFrame(resultado.statistic, index=tipos, columns=tipos)
    matriz_pvalor = pd.DataFrame(resultado.pvalue, index=tipos, columns=tipos)
    return matriz_corr, matriz_pvalor


def identificar_pares_fortes(matriz_corr: pd.DataFrame, matriz_pvalor: pd.DataFrame) -> pd.DataFrame:
    """Lista todos os pares de tipos de crime (sem repetir/duplicar),
    ordenados por força da correlação (|rho|) decrescente.
    """
    linhas = []
    for tipo_a, tipo_b in combinations(matriz_corr.columns, 2):
        linhas.append(
            {
                "tipo_crime_a": tipo_a,
                "tipo_crime_b": tipo_b,
                "rho": matriz_corr.loc[tipo_a, tipo_b],
                "p_valor": matriz_pvalor.loc[tipo_a, tipo_b],
                "significativo_5pct": matriz_pvalor.loc[tipo_a, tipo_b] < 0.05,
            }
        )
    return (
        pd.DataFrame(linhas)
        .sort_values("rho", key=lambda col: col.abs(), ascending=False)
        .reset_index(drop=True)
    )


def main() -> dict[str, tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
    """Roda a correlação nas duas variantes -- número absoluto de casos
    acumulados e taxa por 100 mil habitantes --, ambas na mesma janela
    ANO_INICIO_ANALISE-ANO_FIM_ANALISE (periodo_padrao.py). A versão em
    taxa controla o efeito óbvio de município grande = mais casos de tudo.
    """
    resultados = {}
    for nome, carregar in [
        ("casos_absolutos", carregar_totais_por_municipio),
        ("taxa_por_100mil_hab", carregar_taxas_por_municipio),
    ]:
        tabela_larga = carregar()
        matriz_corr, matriz_pvalor = calcular_matriz_correlacao(tabela_larga)
        pares = identificar_pares_fortes(matriz_corr, matriz_pvalor)
        resultados[nome] = (matriz_corr, matriz_pvalor, pares)
    return resultados


if __name__ == "__main__":
    pd.set_option("display.width", 160)
    for nome, (matriz_corr_df, matriz_pvalor_df, pares_df) in main().items():
        print(f"##### Variante: {nome} #####")
        print("=== Matriz de correlação de Spearman (rho) ===")
        print(matriz_corr_df.round(3).to_string())
        print()
        print("=== Pares de tipos de crime, do mais ao menos correlacionado ===")
        print(pares_df.to_string(index=False))
        print()
