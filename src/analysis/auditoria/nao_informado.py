"""Auditoria metodológica, item 4: quantifica, por ano e por categoria, os
registros classificados como "NÃO INFORMADO" (casos sem município
identificado na planilha original da fonte) e avalia se a proporção muda
no tempo -- teste de tendência simples (Mann-Kendall) sobre a série anual
do percentual, por categoria.

Usa violencia_anual_municipio.csv (a tabela consolidada ANTES do filtro
por município conhecido -- ao contrário de carregar_taxa_periodo/
calcular_taxas_municipio, que já excluem "NÃO INFORMADO" por design).

Uso: python -m src.analysis.auditoria.nao_informado
"""

from pathlib import Path

import pandas as pd
from scipy import stats

TABLES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "outputs" / "tables"
SAIDA_DIR = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "publicacoes"
    / "cap_geotecnologias"
    / "00_gestao"
    / "auditoria"
)

MUNICIPIO_NAO_INFORMADO = "NÃO INFORMADO"


def carregar_serie() -> pd.DataFrame:
    df = pd.read_csv(TABLES_DIR / "violencia_anual_municipio.csv")
    total_por_ano_tipo = df.groupby(["ano", "tipo_crime"], as_index=False)["casos_total"].sum().rename(
        columns={"casos_total": "casos_total_categoria"}
    )
    nao_informado = (
        df[df["municipio"] == MUNICIPIO_NAO_INFORMADO]
        .groupby(["ano", "tipo_crime"], as_index=False)["casos_total"]
        .sum()
        .rename(columns={"casos_total": "casos_nao_informado"})
    )
    serie = total_por_ano_tipo.merge(nao_informado, on=["ano", "tipo_crime"], how="left")
    serie["casos_nao_informado"] = serie["casos_nao_informado"].fillna(0).astype(int)
    serie["pct_nao_informado"] = (
        100 * serie["casos_nao_informado"] / serie["casos_total_categoria"]
    ).round(4)
    return serie.sort_values(["tipo_crime", "ano"]).reset_index(drop=True)


def testar_tendencia_pct(serie: pd.DataFrame) -> pd.DataFrame:
    """Mann-Kendall (via correlação de Kendall entre ano e percentual) por
    categoria -- só sobre anos com pelo menos 1 caso "NÃO INFORMADO" em
    algum ano da série, para não testar tendência de uma série de zeros."""
    linhas = []
    for tipo, grupo in serie.groupby("tipo_crime"):
        if grupo["casos_nao_informado"].sum() == 0:
            linhas.append(
                {"tipo_crime": tipo, "n_anos": len(grupo), "kendall_tau": float("nan"),
                 "p_valor": float("nan"), "observacao": "nenhum caso NÃO INFORMADO na série"}
            )
            continue
        tau, p = stats.kendalltau(grupo["ano"], grupo["pct_nao_informado"])
        linhas.append(
            {"tipo_crime": tipo, "n_anos": len(grupo), "kendall_tau": round(tau, 4),
             "p_valor": round(p, 4), "observacao": ""}
        )
    return pd.DataFrame(linhas)


def main() -> None:
    serie = carregar_serie()
    SAIDA_DIR.mkdir(parents=True, exist_ok=True)
    caminho_serie = SAIDA_DIR / "nao_informado_serie_2012_2026.csv"
    serie.to_csv(caminho_serie, index=False)

    tendencia = testar_tendencia_pct(serie)
    caminho_tendencia = SAIDA_DIR / "nao_informado_tendencia.csv"
    tendencia.to_csv(caminho_tendencia, index=False)

    pd.set_option("display.width", 200)
    print(f"Série completa salva em {caminho_serie}\n")
    print("=== Anos/categorias com algum caso NÃO INFORMADO ===")
    print(serie[serie["casos_nao_informado"] > 0].to_string(index=False))
    print()
    print("=== Total acumulado por categoria, todo o período disponível na fonte ===")
    resumo = serie.groupby("tipo_crime").agg(
        casos_nao_informado_total=("casos_nao_informado", "sum"),
        casos_categoria_total=("casos_total_categoria", "sum"),
    )
    resumo["pct_nao_informado_total"] = (100 * resumo["casos_nao_informado_total"] / resumo["casos_categoria_total"]).round(4)
    print(resumo.to_string())
    print()
    print(f"Teste de tendência (Kendall tau) salvo em {caminho_tendencia}\n")
    print(tendencia.to_string(index=False))


if __name__ == "__main__":
    main()
