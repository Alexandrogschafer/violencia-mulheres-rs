"""Testa se a série anual de casos por tipo de crime tem tendência
(crescente/decrescente) estatisticamente significativa no período
2018-2025.

2012-2017 fica de fora porque não tem quebra mensal (irrelevante aqui, mas
mantém a série anual consistente com o restante da Camada 2); 2026 fica de
fora por ser ano parcial (o total ainda não é comparável aos anos fechados).
"""

from pathlib import Path

import pandas as pd
from scipy import stats

TABLES_DIR = Path(__file__).resolve().parent.parent.parent / "outputs" / "tables"

ANO_INICIO = 2018
ANO_FIM = 2025


def carregar_serie_anual_estado(caminho: Path | None = None) -> pd.DataFrame:
    """Casos totais por tipo_crime e ano, somados entre todos os municípios
    (nível estado), restritos a ANO_INICIO-ANO_FIM.
    """
    caminho = caminho or TABLES_DIR / "violencia_anual_municipio.csv"
    df = pd.read_csv(caminho)
    df = df[(df["ano"] >= ANO_INICIO) & (df["ano"] <= ANO_FIM)]
    return df.groupby(["tipo_crime", "ano"], as_index=False)["casos_total"].sum()


def testar_tendencia(serie: pd.DataFrame) -> pd.DataFrame:
    """Para cada tipo de crime, ajusta uma regressão linear simples
    (ano -> casos) e reporta coeficiente angular, p-valor e R². Cruza com
    o teste de Mann-Kendall, mais robusto a tendências não-lineares.

    scipy não tem um teste de Mann-Kendall dedicado, mas ele é
    matematicamente equivalente à correlação de Kendall (mesma estatística
    S, mesma aproximação para o p-valor) entre a série e a ordem temporal,
    então stats.kendalltau(anos, casos) reproduz o teste sem precisar de
    uma dependência externa (ex.: pymannkendall).
    """
    resultados = []
    for tipo, grupo in serie.groupby("tipo_crime"):
        grupo = grupo.sort_values("ano")
        anos = grupo["ano"].to_numpy()
        casos = grupo["casos_total"].to_numpy()

        reg = stats.linregress(anos, casos)
        tau, p_mk = stats.kendalltau(anos, casos)

        resultados.append(
            {
                "tipo_crime": tipo,
                "n_anos": len(anos),
                "slope": reg.slope,
                "intercept": reg.intercept,
                "r2": reg.rvalue ** 2,
                "p_valor_linregress": reg.pvalue,
                "significativo_linregress_5pct": reg.pvalue < 0.05,
                "kendall_tau": tau,
                "p_valor_mann_kendall": p_mk,
                "significativo_mann_kendall_5pct": p_mk < 0.05,
            }
        )

    return (
        pd.DataFrame(resultados)
        .sort_values("tipo_crime")
        .reset_index(drop=True)
    )


def main() -> pd.DataFrame:
    serie = carregar_serie_anual_estado()
    return testar_tendencia(serie)


if __name__ == "__main__":
    pd.set_option("display.width", 160)
    print(main().to_string(index=False))
