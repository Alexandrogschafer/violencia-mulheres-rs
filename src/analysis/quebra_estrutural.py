"""Investiga se há uma quebra estrutural na série mensal do estado em torno
de maio/2024 -- mês em que as enchentes históricas atingiram o RS (Porto
Alegre e região metropolitana ficaram parcialmente alagadas/com população
deslocada por semanas), o que pode ter afetado tanto a ocorrência quanto o
registro dos crimes (delegacias fechadas/deslocadas, vítimas em abrigos,
etc.).

Dois testes complementares, por tipo de crime:

1. Teste de Chow: compara o RSS de um único ajuste linear (tempo -> casos)
   sobre toda a série contra a soma dos RSS de dois ajustes separados (pré
   e pós quebra), sobre a série DESSAZONALIZADA (resíduo em relação à
   média histórica pré-enchente de cada mês do ano) -- sem dessazonalizar,
   qualquer teste de quebra seria confundido pela sazonalidade normal do
   ano (ver sazonalidade.py: Ameaça/Estupro/Lesão Corporal já têm pico em
   janeiro todo ano, break ou não).

2. Mann-Whitney U por mês equivalente (o pedido original, mais simples):
   para cada mês do ano, compara os casos daquele mês nos anos anteriores
   (2018-2023) contra o mesmo mês em 2024 e 2025. Amostra pequena por
   teste (6 vs 2 observações) -- pouco poder estatístico, é um
   complemento ao teste de Chow, não o substitui.
"""

from pathlib import Path

import pandas as pd
from scipy import stats

from src.analysis.sazonalidade import MESES_NOMES

TABLES_DIR = Path(__file__).resolve().parent.parent.parent / "outputs" / "tables"

ANO_ENCHENTE = 2024
MES_ENCHENTE = 5  # maio/2024

ANOS_ANTES_MANN_WHITNEY = set(range(2018, ANO_ENCHENTE))
ANOS_DEPOIS_MANN_WHITNEY = {2024, 2025}


def carregar_serie_mensal_estado(caminho: Path | None = None) -> pd.DataFrame:
    """Casos totais por tipo_crime, ano e mês, somados entre municípios,
    ordenados cronologicamente dentro de cada tipo de crime.
    """
    caminho = caminho or TABLES_DIR / "violencia_mensal_municipio.csv"
    df = pd.read_csv(caminho)
    serie = df.groupby(["tipo_crime", "ano", "mes"], as_index=False)["casos"].sum()
    return serie.sort_values(["tipo_crime", "ano", "mes"]).reset_index(drop=True)


def _dessazonalizar(serie: pd.DataFrame) -> pd.DataFrame:
    """Subtrai de cada observação a média histórica pré-enchente (2018 até
    o ano anterior à enchente) daquele mês do ano, por tipo de crime. A
    média de referência usa só o período pré-quebra para não deixar o
    próprio efeito da enchente vazar para dentro da linha de base sazonal.
    """
    base = serie[serie["ano"] < ANO_ENCHENTE]
    media_sazonal = (
        base.groupby(["tipo_crime", "mes"])["casos"].mean().rename("media_sazonal_base")
    )
    serie = serie.merge(media_sazonal, on=["tipo_crime", "mes"], how="left")
    serie["residuo"] = serie["casos"] - serie["media_sazonal_base"]
    return serie


def testar_quebra_chow(serie_dessazonalizada: pd.DataFrame) -> pd.DataFrame:
    """Teste de Chow: F alto / p baixo indica que o nível ou a inclinação da
    série muda na quebra, além do que a sazonalidade já explica.
    """
    resultados = []
    for tipo, grupo in serie_dessazonalizada.groupby("tipo_crime"):
        grupo = grupo.sort_values(["ano", "mes"]).reset_index(drop=True)
        t = grupo.index.to_numpy(dtype=float)
        y = grupo["residuo"].to_numpy()
        pos = (
            (grupo["ano"] > ANO_ENCHENTE)
            | ((grupo["ano"] == ANO_ENCHENTE) & (grupo["mes"] >= MES_ENCHENTE))
        ).to_numpy()

        k = 2  # parâmetros por modelo: intercepto + inclinação
        n = len(t)

        pooled = stats.linregress(t, y)
        rss_pooled = float(((y - (pooled.slope * t + pooled.intercept)) ** 2).sum())

        pre = stats.linregress(t[~pos], y[~pos])
        rss_pre = float(((y[~pos] - (pre.slope * t[~pos] + pre.intercept)) ** 2).sum())

        depois = stats.linregress(t[pos], y[pos])
        rss_pos = float(((y[pos] - (depois.slope * t[pos] + depois.intercept)) ** 2).sum())

        rss_separados = rss_pre + rss_pos
        f_stat = ((rss_pooled - rss_separados) / k) / (rss_separados / (n - 2 * k))
        p_valor = stats.f.sf(f_stat, k, n - 2 * k)

        resultados.append(
            {
                "tipo_crime": tipo,
                "n_meses_pre": int((~pos).sum()),
                "n_meses_pos": int(pos.sum()),
                "estatistica_f": f_stat,
                "p_valor": p_valor,
                "significativo_5pct": p_valor < 0.05,
                "slope_pre": pre.slope,
                "slope_pos": depois.slope,
                "intercepto_pre": pre.intercept,
                "intercepto_pos": depois.intercept,
            }
        )
    return pd.DataFrame(resultados).sort_values("tipo_crime").reset_index(drop=True)


def testar_mann_whitney_por_mes(serie: pd.DataFrame) -> pd.DataFrame:
    """Para cada tipo de crime e cada mês do ano, compara os casos daquele
    mês nos anos anteriores (2018-2023) contra 2024 e 2025.
    """
    linhas = []
    for tipo, grupo in serie.groupby("tipo_crime"):
        for mes in range(1, 13):
            valores_antes = grupo.loc[
                (grupo["mes"] == mes) & (grupo["ano"].isin(ANOS_ANTES_MANN_WHITNEY)), "casos"
            ].to_numpy()
            valores_depois = grupo.loc[
                (grupo["mes"] == mes) & (grupo["ano"].isin(ANOS_DEPOIS_MANN_WHITNEY)), "casos"
            ].to_numpy()
            if len(valores_depois) == 0 or len(valores_antes) == 0:
                continue
            _, p = stats.mannwhitneyu(valores_antes, valores_depois, alternative="two-sided")
            media_antes = valores_antes.mean()
            media_depois = valores_depois.mean()
            linhas.append(
                {
                    "tipo_crime": tipo,
                    "mes": mes,
                    "mes_nome": MESES_NOMES[mes],
                    "n_antes": len(valores_antes),
                    "n_depois": len(valores_depois),
                    "media_antes": media_antes,
                    "media_depois": media_depois,
                    "variacao_pct": (media_depois / media_antes - 1) * 100 if media_antes else float("nan"),
                    "p_valor_mannwhitney": p,
                    "significativo_5pct": p < 0.05,
                }
            )
    return pd.DataFrame(linhas).sort_values(["tipo_crime", "mes"]).reset_index(drop=True)


def main() -> tuple[pd.DataFrame, pd.DataFrame]:
    serie = carregar_serie_mensal_estado()
    serie_dessazonalizada = _dessazonalizar(serie)
    chow = testar_quebra_chow(serie_dessazonalizada)
    mann_whitney = testar_mann_whitney_por_mes(serie)
    return chow, mann_whitney


if __name__ == "__main__":
    pd.set_option("display.width", 160)
    chow_df, mw_df = main()
    print("=== Teste de Chow: quebra estrutural em maio/2024 (série dessazonalizada) ===")
    print(chow_df.to_string(index=False))
    print()
    print("=== Mann-Whitney U por mês: 2018-2023 vs. 2024/2025 ===")
    print(mw_df.to_string(index=False))
