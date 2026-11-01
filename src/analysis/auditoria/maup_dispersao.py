"""Auditoria metodológica, item 6: complementa a Tabela 2 do capítulo
(razão máximo/mínimo por nível de agregação) com medidas menos sensíveis
aos extremos e ao número de unidades -- amplitude interquartil (IQR),
coeficiente de variação ponderado pela população e índice de Gini
ponderado pela população.

Por que isso importa e a razão simples não basta sozinha: a razão máx/mín
depende só de dois pontos da distribuição (o maior e o menor valor) e,
como o número de unidades cai de 266 (município) para 28 (COREDE) para 8
(região intermediária), a chance de sortear um extremo junto cai também
-- parte da "redução da desigualdade" que a Tabela 2 mostra é reação real
à agregação espacial, mas parte é só um artefato de ter menos unidades
(com menos pontos, é estatisticamente menos provável observar um extremo
tão distante da média). IQR, CV ponderado e Gini ponderado usam toda a
distribuição, não só as pontas, e por isso são mais robustos a esse
artefato -- embora nenhum deles seja imune ao efeito do número de
unidades: é matematicamente impossível eliminar por completo a
dependência de n numa medida de dispersão entre um conjunto de exatamente
n unidades, e isso deve ser dito no texto, não escondido.

Uso: python -m src.analysis.auditoria.maup_dispersao
"""

from pathlib import Path

import numpy as np
import pandas as pd

from src.analysis.periodo_padrao import ANO_FIM_ANALISE, ANO_INICIO_ANALISE
from src.analysis.tabela_agregacao_regional import (
    POP_MINIMA_PADRAO,
    calcular_agregacao_regional,
    calcular_taxas_municipio,
)

SAIDA_DIR = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "publicacoes"
    / "cap_geotecnologias"
    / "00_gestao"
    / "auditoria"
)

CATEGORIAS = ["Ameaça", "Estupro", "Lesão Corporal"]
NIVEIS = ["municipio", "corede", "regiao_intermediaria"]


def _gini_pares(v: np.ndarray, w: np.ndarray) -> float:
    """Gini ponderado via diferença média relativa entre todos os pares
    (fórmula de Sen/Deaton) -- mais lenta (O(n^2)) mas inequívoca, usada
    como definição de referência para n pequeno (no máximo 266 aqui)."""
    n = len(v)
    w_total = w.sum()
    media_ponderada = np.sum(w * v) / w_total
    diffs = np.abs(v[:, None] - v[None, :])
    peso_pares = w[:, None] * w[None, :]
    return float(np.sum(peso_pares * diffs) / (2 * w_total**2 * media_ponderada))


def _cv_ponderado(valores: np.ndarray, pesos: np.ndarray) -> float:
    media = np.average(valores, weights=pesos)
    variancia = np.average((valores - media) ** 2, weights=pesos)
    return float(np.sqrt(variancia) / media)


def _resumo_dispersao(tipo_crime: str, nivel: str) -> dict:
    if nivel == "municipio":
        base = calcular_taxas_municipio(tipo_crime, ANO_INICIO_ANALISE, ANO_FIM_ANALISE, POP_MINIMA_PADRAO)
        elegiveis = base[base["elegivel"]]
        valores = elegiveis["taxa_por_100mil_hab"].to_numpy()
        pesos = elegiveis["populacao_referencia"].to_numpy()
    else:
        agregado = calcular_agregacao_regional(tipo_crime, nivel, ANO_INICIO_ANALISE, ANO_FIM_ANALISE, POP_MINIMA_PADRAO)
        valores = agregado["taxa_por_100mil_hab"].to_numpy()
        # A tabela de agregação regional guarda casos_total mas não
        # população_pessoas_ano diretamente -- reconstrói para ponderar
        # CV/Gini por população (não por casos, que já é o numerador).
        pesos = _populacao_por_unidade_regional(tipo_crime, nivel)

    q1, q3 = np.percentile(valores, [25, 75])
    n = len(valores)
    return {
        "tipo_crime": tipo_crime,
        "nivel": nivel,
        "n_unidades": n,
        "minimo": round(float(valores.min()), 4),
        "maximo": round(float(valores.max()), 4),
        "razao_max_min": round(float(valores.max() / valores.min()), 4),
        "q1": round(float(q1), 4),
        "mediana": round(float(np.median(valores)), 4),
        "q3": round(float(q3), 4),
        "amplitude_interquartil": round(float(q3 - q1), 4),
        "cv_ponderado_populacao": round(_cv_ponderado(valores, pesos), 4),
        "gini_ponderado_populacao": round(_gini_pares(valores, pesos), 4),
    }


def _populacao_por_unidade_regional(tipo_crime: str, nivel: str) -> np.ndarray:
    """Reconstrói população_pessoas_ano por unidade regional (COREDE ou
    região intermediária), na mesma ordem/filtro de
    calcular_agregacao_regional -- necessária para ponderar CV/Gini por
    população, não por casos."""
    base = calcular_taxas_municipio(tipo_crime, ANO_INICIO_ANALISE, ANO_FIM_ANALISE, POP_MINIMA_PADRAO)
    elegiveis = base[base["elegivel"]]
    agregado_pop = elegiveis.groupby(nivel)["populacao_referencia"].sum()
    # Mesma ordem de calcular_agregacao_regional: por taxa decrescente.
    ordenado = calcular_agregacao_regional(tipo_crime, nivel, ANO_INICIO_ANALISE, ANO_FIM_ANALISE, POP_MINIMA_PADRAO)
    return agregado_pop.reindex(ordenado["regiao"]).to_numpy()


def main() -> pd.DataFrame:
    linhas = [_resumo_dispersao(tipo, nivel) for tipo in CATEGORIAS for nivel in NIVEIS]
    tabela = pd.DataFrame(linhas)

    SAIDA_DIR.mkdir(parents=True, exist_ok=True)
    caminho = SAIDA_DIR / "maup_dispersao_2018_2025.csv"
    tabela.to_csv(caminho, index=False)
    print(f"Salvo em {caminho}\n")

    pd.set_option("display.width", 220)
    print(tabela.to_string(index=False))
    return tabela


if __name__ == "__main__":
    main()
