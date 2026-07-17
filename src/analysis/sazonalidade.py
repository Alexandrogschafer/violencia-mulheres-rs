"""Testa se existe diferença estatisticamente significativa entre os meses
do ano na série mensal (2018-2026), por tipo de crime.

2026 entra com os meses já ocorridos (o mensal_municipio.csv simplesmente
não tem linhas para meses futuros, então nada precisa ser filtrado aqui).
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

TABLES_DIR = Path(__file__).resolve().parent.parent.parent / "outputs" / "tables"

MESES_NOMES = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez",
}


def carregar_serie_mensal_estado(caminho: Path | None = None) -> pd.DataFrame:
    """Casos totais por tipo_crime, ano e mês, somados entre todos os
    municípios (nível estado).
    """
    caminho = caminho or TABLES_DIR / "violencia_mensal_municipio.csv"
    df = pd.read_csv(caminho)
    return df.groupby(["tipo_crime", "ano", "mes"], as_index=False)["casos"].sum()


def testar_sazonalidade(serie: pd.DataFrame) -> pd.DataFrame:
    """Kruskal-Wallis entre os 12 meses, por tipo de crime: cada grupo (mês)
    é formado pelas observações de todos os anos disponíveis. Não assume
    normalidade nem variâncias iguais entre meses, ao contrário de uma ANOVA.
    """
    resultados = []
    for tipo, grupo in serie.groupby("tipo_crime"):
        amostras_por_mes = [
            grupo.loc[grupo["mes"] == m, "casos"].to_numpy() for m in range(1, 13)
        ]
        h, p = stats.kruskal(*amostras_por_mes)
        resultados.append(
            {
                "tipo_crime": tipo,
                "n_obs": len(grupo),
                "estatistica_h": h,
                "p_valor": p,
                "significativo_5pct": p < 0.05,
            }
        )
    return pd.DataFrame(resultados).sort_values("tipo_crime").reset_index(drop=True)


def _holm_bonferroni(p_valores: np.ndarray) -> np.ndarray:
    """Correção de Holm-Bonferroni para as 12 comparações mês-vs-resto: menos
    conservadora que Bonferroni simples, mas ainda controla o erro
    família-wise (evita achar "destaques" só por acaso ao testar 12 meses).
    """
    n = len(p_valores)
    ordem = np.argsort(p_valores)
    ajustados = np.empty(n)
    maior_ate_agora = 0.0
    for rank, idx in enumerate(ordem):
        valor = p_valores[idx] * (n - rank)
        maior_ate_agora = max(maior_ate_agora, valor)
        ajustados[idx] = min(maior_ate_agora, 1.0)
    return ajustados


def identificar_meses_destaque(serie: pd.DataFrame, kruskal: pd.DataFrame) -> pd.DataFrame:
    """Para tipos de crime com diferença significativa entre meses (Kruskal-
    Wallis), compara cada mês (Mann-Whitney U) contra os demais 11 meses
    agrupados, com correção de Holm-Bonferroni. Meses com p ajustado < 0.05
    "se destacam" (para mais ou para menos que o resto do ano).
    """
    tipos_significativos = kruskal.loc[kruskal["significativo_5pct"], "tipo_crime"]
    linhas = []
    for tipo in tipos_significativos:
        grupo = serie[serie["tipo_crime"] == tipo]
        p_valores = []
        stats_mes = []
        for m in range(1, 13):
            valores_mes = grupo.loc[grupo["mes"] == m, "casos"].to_numpy()
            valores_resto = grupo.loc[grupo["mes"] != m, "casos"].to_numpy()
            _, p = stats.mannwhitneyu(valores_mes, valores_resto, alternative="two-sided")
            p_valores.append(p)
            stats_mes.append(
                {
                    "tipo_crime": tipo,
                    "mes": m,
                    "mes_nome": MESES_NOMES[m],
                    "media_casos": valores_mes.mean(),
                    "mediana_casos": float(np.median(valores_mes)),
                    "media_casos_resto_do_ano": valores_resto.mean(),
                }
            )
        p_ajustados = _holm_bonferroni(np.array(p_valores))
        for linha, p_bruto, p_adj in zip(stats_mes, p_valores, p_ajustados):
            linha["p_valor_mannwhitney"] = p_bruto
            linha["p_valor_ajustado_holm"] = p_adj
            linha["destaque_5pct"] = p_adj < 0.05
            linha["direcao"] = (
                "acima" if linha["media_casos"] > linha["media_casos_resto_do_ano"] else "abaixo"
            )
            linhas.append(linha)
    return pd.DataFrame(linhas)


def main() -> tuple[pd.DataFrame, pd.DataFrame]:
    serie = carregar_serie_mensal_estado()
    kruskal = testar_sazonalidade(serie)
    destaques = identificar_meses_destaque(serie, kruskal)
    return kruskal, destaques


if __name__ == "__main__":
    pd.set_option("display.width", 160)
    kruskal_df, destaques_df = main()
    print("=== Kruskal-Wallis: diferença entre meses, por tipo de crime ===")
    print(kruskal_df.to_string(index=False))
    print()
    print("=== Meses em destaque (só tipos com Kruskal-Wallis significativo) ===")
    if destaques_df.empty:
        print("(nenhum tipo de crime com diferença significativa entre meses)")
    else:
        print(destaques_df.to_string(index=False))
