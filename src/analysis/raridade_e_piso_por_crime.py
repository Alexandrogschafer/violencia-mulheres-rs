"""Raridade do desfecho e municípios no piso de p, por crime.

Cruza, para os quatro crimes com LISA, 497 municípios e 2018-2025, a contagem
municipal de eventos com o número de municípios que atingem o menor p possível
em estabilidade_lisa_sementes.csv. Sobrevivência ao FDR é o critério `fdr`.

O limiar é o menor k tal que piso <= q * k / n, isto é, quantos municípios precisam
estar no piso para que o FDR aceite esse p. Não se confunde com uma exigência geral:
um p maior que o piso tem limiar próprio, sempre mais alto.

Taxa: casos por 100 mil pessoas-ano, com a população total do município como
denominador, como em carregar_taxa_periodo.

Uso: python -m src.analysis.raridade_e_piso_por_crime
"""

import math
from pathlib import Path

import pandas as pd

from src.analysis.mapa_choropleth import montar_geodataframe
from src.analysis.moran_lisa_assuncao_reis import ALFA, ANO_FIM, ANO_INICIO, N_MUNICIPIOS, TIPOS_LISA

TABLES_DIR = Path(__file__).resolve().parent.parent.parent / "outputs" / "tables"
ENTRADA = TABLES_DIR / "estabilidade_lisa_sementes.csv"
SAIDA = TABLES_DIR / "raridade_e_piso_por_crime.md"
N_SEMENTES = 20
CASOS_POR_HABITANTES = 100_000


def br(x: float, casas: int = 1) -> str:
    return f"{x:,.{casas}f}".replace(",", " ").replace(".", ",").replace(" ", ".")


def limiar(permutacoes: int) -> int:
    """Menor k com 1/(permutacoes+1) <= ALFA * k / N_MUNICIPIOS, em aritmética exata."""
    return math.ceil(N_MUNICIPIOS / (ALFA * (permutacoes + 1)) - 1e-9)


def raridade(tipo: str) -> dict:
    gdf = montar_geodataframe(tipo, ANO_INICIO, ANO_FIM)
    casos = gdf["casos_total"].astype(float)
    if len(gdf) != N_MUNICIPIOS or casos.isna().any():
        raise ValueError(f"{tipo}: universo diferente de {N_MUNICIPIOS} municípios completos.")
    return {
        "total": int(casos.sum()),
        "mediana": casos.median(),
        "q1": casos.quantile(0.25),
        "zero": (casos == 0).mean(),
        "taxa_media": gdf["taxa_por_100mil_hab"].mean(),
        "taxa_estadual": casos.sum() / gdf["populacao_pessoas_ano"].sum() * CASOS_POR_HABITANTES,
    }


def piso(tabela: pd.DataFrame, permutacoes: int) -> pd.DataFrame:
    x = tabela[tabela["permutacoes"] == permutacoes]
    valor = 1 / (permutacoes + 1)
    if x["p_sim"].min() < valor * (1 - 1e-9):
        raise ValueError("Há p abaixo do piso teórico.")
    return (
        x.assign(no_piso=x["p_sim"] <= valor * (1 + 1e-9))
        .groupby(["tipo_crime", "semente"])
        .agg(no_piso=("no_piso", "sum"), significativos=("sobrevive_fdr", "sum"))
        .reset_index()
    )


def resumo_piso(g: pd.DataFrame) -> str:
    return f"{int(g['no_piso'].min())} / {br(g['no_piso'].median())} / {int(g['no_piso'].max())}"


def main() -> None:
    tabela = pd.read_csv(ENTRADA)
    baixo, alto = piso(tabela, 999), piso(tabela, 99_999)
    if baixo["semente"].nunique() != N_SEMENTES or alto["semente"].nunique() != N_SEMENTES:
        raise ValueError("Entrada não tem as vinte sementes esperadas.")
    limiar_baixo, limiar_alto = limiar(999), limiar(99_999)

    linhas = {tipo: raridade(tipo) for tipo in TIPOS_LISA}
    ordem = sorted(TIPOS_LISA, key=lambda t: (-linhas[t]["mediana"], -linhas[t]["total"]))
    cruzada = []
    for tipo in ordem:
        r = linhas[tipo]
        b, a = baixo[baixo["tipo_crime"] == tipo], alto[alto["tipo_crime"] == tipo]
        cruzada.append(
            {
                "Crime": tipo,
                "Eventos": br(r["total"], 0),
                "Mediana municipal": br(r["mediana"]),
                "Q1 municipal": br(r["q1"]),
                "Municípios com zero": f"{br(100 * r['zero'])}%",
                "Taxa média municipal": br(r["taxa_media"]),
                "Taxa estadual": br(r["taxa_estadual"]),
                "No piso a 999, mín./med./máx.": resumo_piso(b),
                f"Sementes abaixo de {limiar_baixo}": int((b["no_piso"] < limiar_baixo).sum()),
                "Sementes sem significativos a 999": int((b["significativos"] == 0).sum()),
                "No piso a 99.999, mín./med./máx.": resumo_piso(a),
                "Sementes sem significativos a 99.999": int((a["significativos"] == 0).sum()),
            }
        )
    df = pd.DataFrame(cruzada)
    tabela_md = "\n".join(
        "| " + " | ".join(map(str, linha)) + " |"
        for linha in [list(df.columns), ["---"] * df.shape[1], *df.to_numpy().tolist()]
    )

    abaixo, acima = baixo[baixo["no_piso"] < limiar_baixo], baixo[baixo["no_piso"] >= limiar_baixo]
    sem_piso = alto[alto["no_piso"] == 0]
    texto = f"""# Raridade do desfecho e piso de p, por crime

Quatro crimes com LISA, {N_MUNICIPIOS} municípios, {ANO_INICIO}-{ANO_FIM}. Linhas da menor para a maior raridade,
pela contagem municipal mediana. Contagens no período inteiro; taxas por 100 mil pessoas-ano, com a população
total como denominador. No piso significa p = 0,001 a 999 permutações e p = 0,00001 a 99.999. Significativo
significa sobreviver ao FDR de Benjamini-Hochberg com q = 0,05 sobre o `p_sim`.

{tabela_md}

## Limiar

- A 999 permutações, o FDR só aceita p = 0,001 com pelo menos **{limiar_baixo}** municípios no piso
  (0,05 × 10/497 = 0,001006; com 9, 0,000905).
- A 99.999 permutações, o limiar para p = 0,00001 é **{limiar_alto}**: 0,05 × 1/497 = 0,000101, cerca de dez vezes o piso.

## Confronto a 999 permutações

- Combinações crime-semente abaixo do limiar: {len(abaixo)}. Com algum significativo: {int((abaixo['significativos'] > 0).sum())}.
- Combinações crime-semente no limiar ou acima: {len(acima)}. Sem nenhum significativo: {int((acima['significativos'] == 0).sum())}.

## Confronto a 99.999 permutações

- Combinações crime-semente sem nenhum município no piso: {len(sem_piso)} de {len(alto)}. Mesmo nelas, o número de
  significativos vai de {int(sem_piso['significativos'].min())} a {int(sem_piso['significativos'].max())}.
- Nenhuma combinação fica sem significativos: o FDR não precisa que algum município atinja o piso.
"""
    SAIDA.write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
