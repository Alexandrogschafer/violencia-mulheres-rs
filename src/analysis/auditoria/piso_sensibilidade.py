"""Auditoria metodológica, item 2: quantifica o efeito do piso populacional
de 5.000 habitantes usado nas figuras do capítulo e faz análise de
sensibilidade com limiares alternativos (3.000, 5.000, 10.000, 15.000).

Para cada limiar e cada categoria mapeada (Ameaça, Estupro, Lesão
Corporal), calcula: número e percentual de municípios excluídos,
população estadual excluída e seu percentual, e casos excluídos e seu
percentual sobre o total da categoria no período 2018-2025.

Reaproveita calcular_taxas_municipio de tabela_agregacao_regional.py (que
já carrega taxa + população de referência + flag "elegivel") -- não
reimplementa a lógica de piso, só a aplica em mais limiares.

Uso: python -m src.analysis.auditoria.piso_sensibilidade
"""

from pathlib import Path

import pandas as pd

from src.analysis.periodo_padrao import ANO_FIM_ANALISE, ANO_INICIO_ANALISE
from src.analysis.tabela_agregacao_regional import calcular_taxas_municipio

SAIDA_DIR = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "publicacoes"
    / "cap_geotecnologias"
    / "00_gestao"
    / "auditoria"
)

LIMIARES = [3000, 5000, 10000, 15000]
CATEGORIAS = ["Ameaça", "Estupro", "Lesão Corporal"]


def calcular_efeito_piso(tipo_crime: str, pop_minima: int) -> dict:
    base = calcular_taxas_municipio(tipo_crime, ANO_INICIO_ANALISE, ANO_FIM_ANALISE, pop_minima)

    n_total = len(base)
    n_excluidos = int((~base["elegivel"]).sum())

    pop_total = base["populacao_referencia"].sum()
    pop_excluida = base.loc[~base["elegivel"], "populacao_referencia"].sum()

    casos_total = base["casos_total"].sum()
    casos_excluidos = base.loc[~base["elegivel"], "casos_total"].sum()

    return {
        "tipo_crime": tipo_crime,
        "pop_minima": pop_minima,
        "n_municipios_total": n_total,
        "n_municipios_excluidos": n_excluidos,
        "pct_municipios_excluidos": round(100 * n_excluidos / n_total, 2),
        "populacao_estadual_referencia": int(pop_total),
        "populacao_excluida": int(pop_excluida),
        "pct_populacao_excluida": round(100 * pop_excluida / pop_total, 2),
        "casos_periodo_total": int(casos_total),
        "casos_excluidos": int(casos_excluida := casos_excluidos),
        "pct_casos_excluidos": round(100 * casos_excluida / casos_total, 2) if casos_total else float("nan"),
    }


def main() -> pd.DataFrame:
    linhas = []
    for tipo in CATEGORIAS:
        for limiar in LIMIARES:
            linhas.append(calcular_efeito_piso(tipo, limiar))
    tabela = pd.DataFrame(linhas)

    SAIDA_DIR.mkdir(parents=True, exist_ok=True)
    caminho = SAIDA_DIR / "piso_sensibilidade_2018_2025.csv"
    tabela.to_csv(caminho, index=False)
    print(f"Salvo em {caminho}\n")

    pd.set_option("display.width", 200)
    print(tabela.to_string(index=False))
    return tabela


if __name__ == "__main__":
    main()
