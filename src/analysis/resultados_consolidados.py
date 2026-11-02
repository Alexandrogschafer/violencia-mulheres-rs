"""Tabela consolidada de resultados e sobreposição do LISA entre desfechos.

Tudo com semente 12345, 99.999 permutações e FDR de Benjamini-Hochberg sobre o p
direcional do esda (critério fdr), na configuração de Assunção e Reis para o LISA.

- resultados_consolidados.md: fonte única de números do artigo. Moran e contagens por
  quadrante vêm de moran_lisa_assuncao_reis_2018_2025.csv; eventos, mediana e zeros, de
  montar_geodataframe.
- sobreposicao_desfechos.md: lê o LISA por município de estabilidade_lisa_sementes.csv e
  confere as contagens com o CSV acima antes de gravar.

Feminicídio Consumado não tem LISA em moran_lisa_assuncao_reis.py, logo não entra na
sobreposição.

Uso: python -m src.analysis.resultados_consolidados
"""

from itertools import combinations
from pathlib import Path

import pandas as pd

from src.analysis.mapa_choropleth import montar_geodataframe
from src.analysis.moran_lisa_assuncao_reis import (
    ALFA,
    ANO_FIM,
    ANO_INICIO,
    N_MUNICIPIOS,
    SEED,
    SAIDA_PADRAO as MORAN_CSV,
    TIPOS_LISA,
    TIPOS_MORAN,
)

TABLES_DIR = Path(__file__).resolve().parent.parent.parent / "outputs" / "tables"
ESTABILIDADE_CSV = TABLES_DIR / "estabilidade_lisa_sementes.csv"
SAIDA_CONSOLIDADO = TABLES_DIR / "resultados_consolidados.md"
SAIDA_SOBREPOSICAO = TABLES_DIR / "sobreposicao_desfechos.md"

PERMUTACOES = 99_999
QUADRANTES = ["AA", "BB", "AB", "BA"]
ORDEM_DESFECHOS = ["Ameaça", "Lesão Corporal", "Estupro", "Feminicídio Tentado", "Feminicídio Consumado"]
LISA = [d for d in ORDEM_DESFECHOS if d in TIPOS_LISA]


def br(x: float, casas: int) -> str:
    return f"{x:,.{casas}f}".replace(",", " ").replace(".", ",").replace(" ", ".")


def markdown(df: pd.DataFrame) -> str:
    linhas = [list(df.columns), ["---"] * df.shape[1], *df.astype(str).to_numpy().tolist()]
    return "\n".join("| " + " | ".join(map(str, linha)) + " |" for linha in linhas)


def carregar_moran() -> pd.DataFrame:
    moran = pd.read_csv(MORAN_CSV)
    if set(moran["semente"]) != {SEED} or set(moran["permutacoes"]) != {PERMUTACOES}:
        raise ValueError("A tabela de Moran não está em semente 12345 e 99.999 permutações.")
    return moran


def carregar_lisa(moran: pd.DataFrame) -> pd.DataFrame:
    """LISA por município, conferido contra as contagens de moran_lisa_assuncao_reis."""
    t = pd.read_csv(ESTABILIDADE_CSV)
    t = t[(t["semente"] == SEED) & (t["permutacoes"] == PERMUTACOES)]
    referencia = moran[moran["configuracao"] == "assuncao_reis"].set_index("tipo_crime")
    for tipo in LISA:
        g = t[t["tipo_crime"] == tipo]
        if len(g) != N_MUNICIPIOS:
            raise ValueError(f"{tipo}: universo diferente de {N_MUNICIPIOS} municípios.")
        for q in QUADRANTES:
            if int((g["categoria"] == q).sum()) != int(referencia.loc[tipo, f"lisa_{q.lower()}_fdr"]):
                raise ValueError(f"{tipo}, {q}: contagem diverge entre as duas tabelas.")
    return t


def consolidado(moran: pd.DataFrame) -> str:
    bruta = moran[moran["configuracao"] == "bruta"].set_index("tipo_crime")
    ajustada = moran[moran["configuracao"] == "assuncao_reis"].set_index("tipo_crime")
    if set(ORDEM_DESFECHOS) != set(TIPOS_MORAN):
        raise ValueError("Desfechos diferentes dos de moran_lisa_assuncao_reis.")
    linhas = []
    for tipo in ORDEM_DESFECHOS:
        casos = montar_geodataframe(tipo, ANO_INICIO, ANO_FIM)["casos_total"].astype(float)
        if len(casos) != N_MUNICIPIOS or casos.isna().any():
            raise ValueError(f"{tipo}: universo diferente de {N_MUNICIPIOS} municípios completos.")
        linha = {
            "Desfecho": tipo,
            "Eventos": br(casos.sum(), 0),
            "Mediana municipal": br(casos.median(), 1),
            "Municípios com zero": f"{br(100 * (casos == 0).mean(), 1)}%",
            "Moran bruto": br(bruta.loc[tipo, "moran_i"], 4),
            "p bruto": br(bruta.loc[tipo, "moran_p_sim"], 5),
            "Moran ajustado": br(ajustada.loc[tipo, "moran_i"], 4),
            "p ajustado": br(ajustada.loc[tipo, "moran_p_sim"], 5),
        }
        for q in QUADRANTES:
            valor = ajustada.loc[tipo, f"lisa_{q.lower()}_fdr"]
            linha[f"LISA {q}"] = "não calculado" if pd.isna(valor) else int(valor)
        valor = ajustada.loc[tipo, "lisa_total_fdr"]
        linha["LISA total"] = "não calculado" if pd.isna(valor) else int(valor)
        linhas.append(linha)
    return f"""# Resultados consolidados

Fonte única de números do artigo. {N_MUNICIPIOS} municípios, {ANO_INICIO}-{ANO_FIM}, contiguidade de rainha padronizada
por linha, semente {SEED}, {br(PERMUTACOES, 0)} permutações. Moran bruto: taxa por 100 mil pessoas-ano. Moran ajustado e
LISA: ajuste de Assunção e Reis. LISA: municípios que sobrevivem ao FDR de Benjamini-Hochberg com q = {br(ALFA, 2)}, por
desfecho, sobre o p direcional do esda. O menor p possível é 0,00001.

Gerada por `src/analysis/resultados_consolidados.py`.

{markdown(pd.DataFrame(linhas))}
"""


def matriz(conjuntos: dict[str, set]) -> pd.DataFrame:
    linhas = []
    for a in LISA:
        linhas.append({"Desfecho": a, **{b: len(conjuntos[a] & conjuntos[b]) for b in LISA}})
    return pd.DataFrame(linhas)


def distribuicao(conjuntos: dict[str, set]) -> pd.DataFrame:
    contagem = pd.Series([m for s in conjuntos.values() for m in s]).value_counts()
    return pd.DataFrame(
        [{"Desfechos": k, "Municípios": int((contagem == k).sum())} for k in range(1, len(LISA) + 1)]
        + [{"Desfechos": "Ao menos um", "Municípios": len(contagem)}]
    )


def combinacoes(conjuntos: dict[str, set]) -> pd.DataFrame:
    """Combinações exatas: o município está nesses desfechos e em nenhum outro."""
    linhas = []
    for k in range(2, len(LISA) + 1):
        for combo in combinations(LISA, k):
            dentro = set.intersection(*(conjuntos[d] for d in combo))
            fora = set().union(*(conjuntos[d] for d in LISA if d not in combo))
            exatos = sorted(dentro - fora)
            if exatos:
                linhas.append({"Combinação": " + ".join(combo), "Municípios": len(exatos), "Quais": ", ".join(exatos)})
    if not linhas:
        return pd.DataFrame([{"Combinação": "nenhuma", "Municípios": 0, "Quais": "—"}])
    return pd.DataFrame(linhas)


def sobreposicao(lisa: pd.DataFrame, todas: pd.DataFrame) -> str:
    sig = lisa[lisa["sobrevive_fdr"] & lisa["tipo_crime"].isin(LISA)]
    gerais = {d: set(sig.loc[sig["tipo_crime"] == d, "municipio"]) for d in LISA}
    secoes = [
        "# Sobreposição do LISA entre desfechos",
        f"Semente {SEED}, {br(PERMUTACOES, 0)} permutações, FDR sobre o p direcional, ajuste de Assunção e Reis. Quatro "
        "desfechos com LISA. Diagonal das matrizes: municípios significativos naquele desfecho.",
        "## Qualquer quadrante",
        "Conta o município mesmo que o quadrante difira entre os desfechos.",
        markdown(matriz(gerais)),
        markdown(distribuicao(gerais)),
        "Combinações exatas, em que o município está nesses desfechos e em nenhum outro:",
        markdown(combinacoes(gerais)),
    ]
    for q in QUADRANTES:
        conjuntos = {d: set(sig.loc[(sig["tipo_crime"] == d) & (sig["categoria"] == q), "municipio"]) for d in LISA}
        secoes += [
            f"## Mesmo quadrante: {q}",
            markdown(matriz(conjuntos)),
            markdown(distribuicao(conjuntos)),
            markdown(combinacoes(conjuntos)),
        ]

    quadrantes = sig.groupby("municipio")["categoria"].nunique()
    mistos = sorted(quadrantes[quadrantes > 1].index)
    secoes += [
        "## Municípios em mais de um desfecho com quadrantes diferentes",
        ", ".join(mistos) if mistos else "Nenhum.",
    ]

    alto = todas[(todas["permutacoes"] == PERMUTACOES) & todas["tipo_crime"].isin(LISA)]
    estabilidade = alto.groupby(["tipo_crime", "municipio"])["sobrevive_fdr"].sum()
    n_desfechos = sig.groupby("municipio")["tipo_crime"].nunique()
    linhas = []
    for municipio in n_desfechos[n_desfechos >= 3].sort_values(ascending=False).index:
        linha = {"Município": municipio, "Desfechos": int(n_desfechos[municipio])}
        for d in LISA:
            g = sig[(sig["municipio"] == municipio) & (sig["tipo_crime"] == d)]
            linha[d] = f"{g['categoria'].iloc[0]} ({int(estabilidade[d, municipio])}/20)" if len(g) else "—"
        linhas.append(linha)
    lista = pd.DataFrame(linhas).sort_values(["Desfechos", "Município"], ascending=[False, True]) if linhas else None
    secoes += [
        "## Municípios significativos em três ou mais desfechos",
        "Em cada célula, o quadrante e em quantas das vinte sementes o par é significativo.",
        markdown(lista) if lista is not None else "Nenhum.",
    ]
    # As vinte sementes só qualificam a sobreposição; os números acima seguem a semente 12345.
    duplos = []
    for municipio in n_desfechos[n_desfechos >= 2].index:
        linha = {"Município": municipio}
        for d in LISA:
            g = sig[(sig["municipio"] == municipio) & (sig["tipo_crime"] == d)]
            linha[d] = f"{g['categoria'].iloc[0]} ({int(estabilidade[d, municipio])}/20)" if len(g) else "—"
        duplos.append(linha)
    por_semente = (
        alto[alto["sobrevive_fdr"]]
        .groupby(["semente", "municipio"])["tipo_crime"]
        .nunique()
        .groupby("semente")
        .agg(dois=lambda n: int((n == 2).sum()), tres=lambda n: int((n == 3).sum()), quatro=lambda n: int((n == 4).sum()))
    )
    faixa = pd.DataFrame(
        [
            {"Desfechos": rotulo, "Mínimo": int(por_semente[c].min()), "Mediana": br(por_semente[c].median(), 1), "Máximo": int(por_semente[c].max())}
            for rotulo, c in [(2, "dois"), (3, "tres"), (4, "quatro")]
        ]
    )
    secoes += [
        "## Estabilidade da sobreposição entre as vinte sementes",
        "Municípios em dois desfechos ou mais na semente 12345, com quadrante e sementes em que cada par é significativo:",
        markdown(pd.DataFrame(duplos).sort_values("Município")),
        "Municípios por número de desfechos, entre as vinte sementes:",
        markdown(faixa),
    ]
    return "\n\n".join(secoes) + "\n"


def main() -> None:
    moran = carregar_moran()
    todas = pd.read_csv(ESTABILIDADE_CSV)
    lisa = carregar_lisa(moran)
    SAIDA_CONSOLIDADO.write_text(consolidado(moran), encoding="utf-8")
    SAIDA_SOBREPOSICAO.write_text(sobreposicao(lisa, todas), encoding="utf-8")
    print(f"Gravados {SAIDA_CONSOLIDADO} e {SAIDA_SOBREPOSICAO}")


if __name__ == "__main__":
    main()
