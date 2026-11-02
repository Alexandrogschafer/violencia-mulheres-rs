"""Composição por quadrante do conjunto significativo, com 999 e 99.999 permutações.

Pergunta: o piso de p com 999 permutações penaliza outliers espaciais (AB, BA)
mais do que agrupamentos (AA, BB)? Lê estabilidade_lisa_sementes.csv e não roda
o LISA de novo.

Par é a combinação município-crime. O quadrante de um par só aparece no CSV quando
ele é significativo, e não varia entre sementes (estabilidade_lisa_sementes.py
confirma isso), então vale para todas as sementes em que ele aparece.

Critério principal: fdr. Critério de referência: fdr_p2x, sobre o dobro do p.

Uso: python -m src.analysis.composicao_quadrantes_por_permutacoes
"""

from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest

TABLES_DIR = Path(__file__).resolve().parent.parent.parent / "outputs" / "tables"
ENTRADA = TABLES_DIR / "estabilidade_lisa_sementes.csv"
SAIDA = TABLES_DIR / "composicao_quadrantes_por_permutacoes.md"

QUADRANTES = ["AA", "BB", "AB", "BA"]
OUTLIERS = {"AB", "BA"}
PERMUTACOES = [999, 99_999]
N_SEMENTES = 20
N_VIZINHOS_P = 5
# Julgamento, não regra estatística: abaixo disso, a comparação fica entregue a poucos municípios.
MIN_PARES_OUTLIER = 20
CRITERIOS = {
    "fdr": ("sobrevive_fdr", "categoria"),
    "fdr_p2x": ("sobrevive_fdr_p2x", "categoria_fdr_p2x"),
}


def pct(x: float) -> str:
    return "—" if pd.isna(x) else f"{100 * x:.1f}%".replace(".", ",")


def pct_p(p: float) -> str:
    return f"{p:.3f}".replace(".", ",")


def markdown(df: pd.DataFrame) -> str:
    linhas = [list(df.columns), ["---"] * df.shape[1], *df.astype(str).to_numpy().tolist()]
    return "\n".join("| " + " | ".join(map(str, linha)) + " |" for linha in linhas)


def celulas(contagens: pd.Series) -> dict:
    total = int(contagens.sum())
    saida = {"n": total}
    for q in QUADRANTES:
        saida[q] = f"{int(contagens[q])} ({pct(contagens[q] / total if total else np.nan)})"
    saida["AB+BA"] = pct(contagens[list(OUTLIERS)].sum() / total if total else np.nan)
    return saida


def composicao(tabela: pd.DataFrame, status: str, categoria: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    agregada, por_semente = [], []
    for (tipo, perm), g in tabela.groupby(["tipo_crime", "permutacoes"]):
        sig = g[g[status]]
        agregada.append(
            {
                "crime": tipo,
                "permutações": perm,
                **celulas(sig[categoria].value_counts().reindex(QUADRANTES, fill_value=0)),
            }
        )
        for semente, gs in g.groupby("semente"):
            contagens = gs.loc[gs[status], categoria].value_counts().reindex(QUADRANTES, fill_value=0)
            por_semente.append({"crime": tipo, "permutações": perm, "semente": semente, **celulas(contagens)})
    return pd.DataFrame(agregada), pd.DataFrame(por_semente)


def dispersao(tabela: pd.DataFrame, status: str, categoria: str) -> pd.DataFrame:
    linhas = []
    for (tipo, perm), g in tabela.groupby(["tipo_crime", "permutacoes"]):
        sig = g[g[status]]
        fracao = sig[categoria].isin(OUTLIERS).groupby(sig["semente"]).mean().astype(float)
        linhas.append(
            {
                "crime": tipo,
                "permutações": perm,
                "sementes com n > 0": len(fracao),
                "mínimo": pct(fracao.min()),
                "mediana": pct(fracao.median()),
                "máximo": pct(fracao.max()),
            }
        )
    return pd.DataFrame(linhas)


def pares(tabela: pd.DataFrame, status: str, categoria: str) -> pd.DataFrame:
    chave = ["tipo_crime", "municipio"]
    alto = tabela[tabela["permutacoes"] == 99_999].groupby(chave).agg(n_99999=(status, "sum"), p_99999=("p_sim", "mean"))
    baixo = tabela[tabela["permutacoes"] == 999].groupby(chave).agg(n_999=(status, "sum"))
    quadrante = tabela[tabela[status]].groupby(chave)[categoria].first().rename("quadrante")
    d = alto.join(baixo).join(quadrante).reset_index()
    d["grupo"] = np.where(d["quadrante"].isin(OUTLIERS), "outlier", "agrupamento")
    return d


def contar(d: pd.DataFrame) -> pd.DataFrame:
    linhas = []
    for tipo, g in [*d.groupby("tipo_crime"), ("Total", d)]:
        contagens = g["quadrante"].value_counts().reindex(QUADRANTES, fill_value=0)
        linhas.append({"crime": tipo, **{q: int(contagens[q]) for q in QUADRANTES}, "total": int(contagens.sum())})
    return pd.DataFrame(linhas)


def retencao(d: pd.DataFrame) -> pd.DataFrame:
    """Combinações par-semente a 999 sobre as a 99.999, entre os pares significativos a 99.999."""
    linhas = []
    for tipo, g in [*d.groupby("tipo_crime"), ("Total", d)]:
        linha = {"crime": tipo}
        for grupo, rotulo in [("agrupamento", "agrupamentos"), ("outlier", "outliers")]:
            h = g[g["grupo"] == grupo]
            soma = int(h["n_99999"].sum())
            linha[f"pares, {rotulo}"] = len(h)
            linha[f"nunca a 999, {rotulo}"] = int((h["n_999"] == 0).sum())
            linha[f"retenção, {rotulo}"] = (
                f"{int(h['n_999'].sum())}/{soma} ({pct(h['n_999'].sum() / soma)})" if soma else "—"
            )
        linhas.append(linha)
    return pd.DataFrame(linhas)


def outliers_pareados(d: pd.DataFrame) -> pd.DataFrame:
    """Cada outlier ao lado dos agrupamentos do mesmo crime com p a 99.999 mais próximo."""
    linhas = []
    for _, o in d[d["grupo"] == "outlier"].sort_values(["tipo_crime", "p_99999"]).iterrows():
        pares_crime = d[(d["tipo_crime"] == o["tipo_crime"]) & (d["grupo"] == "agrupamento")]
        distancia = (np.log(pares_crime["p_99999"]) - np.log(o["p_99999"])).abs()
        vizinhos = pares_crime.loc[distancia.nsmallest(N_VIZINHOS_P).index]
        linhas.append(
            {
                "crime": o["tipo_crime"],
                "município": o["municipio"],
                "quadrante": o["quadrante"],
                "sementes a 99.999": int(o["n_99999"]),
                "p médio a 99.999": f"{o['p_99999']:.5f}".replace(".", ","),
                "sementes a 999": int(o["n_999"]),
                f"média a 999, {N_VIZINHOS_P} agrupamentos de p próximo": f"{vizinhos['n_999'].mean():.1f}".replace(".", ","),
            }
        )
    return pd.DataFrame(linhas)


def crimes_informativos(d: pd.DataFrame) -> list[str]:
    """Crimes com os dois grupos a 99.999 e algum par significativo a 999."""
    return [
        tipo
        for tipo, g in d.groupby("tipo_crime")
        if g["grupo"].nunique() == 2 and g["n_999"].sum() > 0
    ]


def teste_estratificado(d: pd.DataFrame) -> tuple[int, float]:
    """Soma de sementes a 999 dos outliers e p exato unilateral, permutando rótulos dentro do crime."""
    distribuicao = np.array([0])
    observado = 0
    for tipo in crimes_informativos(d):
        g = d[d["tipo_crime"] == tipo]
        valores = g["n_999"].to_numpy()
        k = int((g["grupo"] == "outlier").sum())
        observado += int(g.loc[g["grupo"] == "outlier", "n_999"].sum())
        somas = np.array([sum(c) for c in combinations(valores, k)])
        distribuicao = np.add.outer(distribuicao, somas).ravel()
    return observado, float((distribuicao <= observado).mean())


def ic_exato(sucessos: int, n: int) -> str:
    if n == 0:
        return "—"
    ic = binomtest(sucessos, n).proportion_ci(method="exact")
    return f"{sucessos}/{n}: {pct(ic.low)} a {pct(ic.high)}"


def poder(d: pd.DataFrame) -> dict:
    informativos = crimes_informativos(d)
    u = d[d["tipo_crime"].isin(informativos)]
    out, agr = u[u["grupo"] == "outlier"], u[u["grupo"] == "agrupamento"]
    observado, p = teste_estratificado(d)
    return {
        "informativos": informativos,
        "n_out": len(out),
        "n_agr": len(agr),
        "ic_out": ic_exato(int((out["n_999"] == 0).sum()), len(out)),
        "ic_agr": ic_exato(int((agr["n_999"] == 0).sum()), len(agr)),
        "observado": observado,
        "p": p,
    }


def secao_criterio(tabela: pd.DataFrame, criterio: str) -> tuple[str, dict, pd.DataFrame]:
    status, categoria = CRITERIOS[criterio]
    agregada, por_semente = composicao(tabela, status, categoria)
    d = pares(tabela, status, categoria)
    alto = d[d["n_99999"] > 0]
    nunca = alto[alto["n_999"] == 0]
    so_999 = d[(d["n_99999"] == 0) & (d["n_999"] > 0)]
    info = poder(alto) if crimes_informativos(alto) else None
    linhas_poder = (
        "Sem crime em que os dois grupos possam ser comparados a 999."
        if info is None
        else (
            f"- Crimes comparáveis: {', '.join(info['informativos'])}. Pares outlier neles: {info['n_out']}; "
            f"de agrupamento: {info['n_agr']}.\n"
            f"- Pares que nunca aparecem a 999, com IC exato de 95%: outliers {info['ic_out']}; "
            f"agrupamentos {info['ic_agr']}.\n"
            f"- Teste exato unilateral permutando rótulos dentro do crime, sobre as sementes a 999: "
            f"soma observada dos outliers = {info['observado']}, p = {pct_p(info['p'])}. Serve só para descrever: os pares não são independentes, e o teste não controla o p a 99.999."
        )
    )
    secoes = [
        f"## Critério `{criterio}`",
        "### Composição agregada sobre as vinte sementes",
        "Contagens de combinações par-semente. Um mesmo par conta uma vez por semente em que é significativo.",
        markdown(agregada),
        "### Pares significativos a 99.999 em ao menos uma semente, por quadrante",
        markdown(contar(alto)),
        "### Pares significativos a 99.999 que nunca aparecem a 999, por quadrante",
        markdown(contar(nunca)),
        "### Pares que aparecem a 999 e nunca a 99.999, por quadrante",
        markdown(contar(so_999)),
        "### Retenção entre os pares significativos a 99.999",
        markdown(retencao(alto)),
        "A linha Total não serve para comparar os grupos: Feminicídio Tentado zera os dois grupos a 999 e concentra "
        "uma fatia maior dos outliers. A comparação válida é dentro de cada crime.",
        "### Cada par outlier, ao lado de agrupamentos de p próximo",
        markdown(outliers_pareados(alto)),
        "### Poder",
        linhas_poder,
        "### Participação de AB+BA entre as sementes",
        "Só entram as sementes com algum município significativo.",
        markdown(dispersao(tabela, status, categoria)),
        "### Composição por semente",
        markdown(por_semente),
    ]
    return "\n\n".join(secoes), info, alto


def main() -> None:
    tabela = pd.read_csv(ENTRADA)
    if tabela["semente"].nunique() != N_SEMENTES or set(tabela["permutacoes"]) != set(PERMUTACOES):
        raise ValueError("Entrada não tem as vinte sementes e as duas configurações esperadas.")

    secao_fdr, info, alto = secao_criterio(tabela, "fdr")
    secao_p2x, info_p2x, alto_p2x = secao_criterio(tabela, "fdr_p2x")
    n_out = int((alto["grupo"] == "outlier").sum())
    n_out_p2x = int((alto_p2x["grupo"] == "outlier").sum())
    if max(n_out, n_out_p2x) >= MIN_PARES_OUTLIER:
        raise ValueError("Há pares outlier suficientes para reavaliar a conclusão escrita abaixo.")
    contagem = alto["quadrante"].value_counts()

    conclusao = (
        "# Composição por quadrante com 999 e 99.999 permutações\n\n"
        "## Conclusão: indeterminado\n\n"
        f"Os dados não têm poder para responder a pergunta. Com 99.999 permutações, há só **{n_out} pares outlier** "
        f"no critério `fdr` ({contagem['AB']} AB e {contagem['BA']} BA), contra "
        f"{int((alto['grupo'] == 'agrupamento').sum())} de agrupamento, e {info['n_out']} deles estão nos crimes "
        f"comparáveis. No critério `fdr_p2x`, são {n_out_p2x} pares, e só {info_p2x['n_out']} num crime comparável. "
        "Isso não equivale a dizer que não há diferença.\n\n"
        f"Critério adotado: menos de {MIN_PARES_OUTLIER} pares outlier leva a “indeterminado”. "
        "O limiar é um julgamento, não uma regra estatística."
    )
    SAIDA.write_text("\n\n".join([conclusao, secao_fdr, secao_p2x]) + "\n", encoding="utf-8")
    print(f"Gravado em {SAIDA}")


if __name__ == "__main__":
    main()
