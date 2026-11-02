"""Moran global e LISA de Assunção e Reis com população FEMININA como
denominador, comparados à versão atual com população total. Não altera o
pipeline: reutiliza a malha, a matriz e os parâmetros de
moran_lisa_assuncao_reis.py e grava em tabelas próprias.

POPULAÇÃO FEMININA ANUAL ESTIMADA, NÃO MEDIDA. O IBGE só publica população
municipal por sexo nos Censos; as estimativas anuais de 2018-2025 trazem só o
total. Suposição (decisão do usuário, 2026-11-02):

    mulheres-ano(m, t) = população total(m, t) × razão feminina(m, Censo 2022)

isto é, a proporção de mulheres de cada município fica constante de 2018 a
2025. Como a razão é constante no período, a soma de mulheres-ano é a razão
vezes a população-ano acumulada que o pipeline já usa.

Verificação da suposição: a razão feminina do Censo 2010 é comparada com a de
2022. Se ela foi estável em doze anos, mantê-la constante numa janela de oito
anos interna ao intervalo é defensável; os municípios com variação grande são
listados, porque é neles que a suposição pode distorcer a taxa.

Fontes (API de agregados do IBGE, variável 93 = população residente):
- Censo 2022: tabela 9514, sexo = mulheres (busca de auditoria/populacao_feminina.py);
  total de 2022 vem de populacao_municipio_rs.csv (tabela 4709, mesmo Censo).
- Censo 2010: tabela 1378, sexo = mulheres e total, na mesma consulta.
  Pinto Bandeira, instalado em 2013, não existe no Censo 2010 (496 municípios);
  seu território estava em Bento Gonçalves.

Parâmetros iguais aos do pipeline: ajuste de Assunção e Reis
(Moran_Rate/Moran_Local_Rate, adjusted=True), 99.999 permutações, semente
12345 reposta antes de cada cálculo, Benjamini-Hochberg sobre o p_sim
direcional do esda, alfa 0,05.

Uso: python -m src.analysis.denominador_feminino
"""

import time
from pathlib import Path

import numpy as np
import pandas as pd

from src.analysis.auditoria.populacao_feminina import buscar_populacao_feminina_2022
from src.analysis.autocorrelacao_espacial import montar_pesos_espaciais
from src.analysis.mapa_choropleth import montar_geodataframe
from src.analysis.moran_lisa_assuncao_reis import (
    ANO_FIM,
    ANO_INICIO,
    N_MUNICIPIOS,
    N_PERMUTACOES,
    QUADRANTES,
    SEED,
    TIPOS_LISA,
    benjamini_hochberg,
    rodar_global,
    rodar_local,
)
from src.fetch_populacao import get_json, normaliza_municipio

TABLES_DIR = Path(__file__).resolve().parent.parent.parent / "outputs" / "tables"
SAIDA_POP = TABLES_DIR / "populacao_feminina_censos_rs.csv"
SAIDA_LISA = TABLES_DIR / "lisa_denominador_feminino_vs_total_2018_2025.csv"
SAIDA_RESUMO = TABLES_DIR / "moran_lisa_denominador_feminino_2018_2025.csv"
SAIDA_MD = TABLES_DIR / "denominador_feminino_vs_total.md"
CSV_ATUAL = TABLES_DIR / "moran_lisa_assuncao_reis_2018_2025.csv"

URL_CENSO_2010 = (
    "https://servicodados.ibge.gov.br/api/v3/agregados/1378/periodos/2010/variaveis/93"
    "?localidades=N6[N3[43]]&classificacao=2[0,5]"
)
LIMIARES_PP = [1, 2, 5]
LIMIAR_LISTA_PP = 2.0
NOTA_DENOMINADOR = (
    "população feminina anual ESTIMADA, não medida: população total do ano × "
    "razão feminina do município no Censo 2022 (razão suposta constante em 2018-2025)"
)


def buscar_censo_2010() -> pd.DataFrame:
    resposta = get_json(URL_CENSO_2010)
    por_categoria = {}
    for resultado in resposta[0]["resultados"]:
        cat = next(iter(resultado["classificacoes"][0]["categoria"]))
        valores = {}
        for serie in resultado["series"]:
            valor = serie["serie"]["2010"]
            if not str(valor).isdigit():
                raise ValueError(f"Valor inesperado em 2010: {serie['localidade']['nome']} {valor!r}")
            valores[normaliza_municipio(serie["localidade"]["nome"])] = int(valor)
        por_categoria[cat] = valores
    df = pd.DataFrame({"pop_total_2010": por_categoria["0"], "pop_feminina_2010": por_categoria["5"]})
    return df.rename_axis("municipio").reset_index()


def montar_populacao_censos() -> pd.DataFrame:
    fem22 = buscar_populacao_feminina_2022().rename(columns={"populacao_feminina_2022": "pop_feminina_2022"})
    tot = pd.read_csv(TABLES_DIR / "populacao_municipio_rs.csv")
    tot22 = tot[tot["ano"] == 2022][["municipio", "populacao"]].rename(columns={"populacao": "pop_total_2022"})
    base = tot22.merge(fem22, on="municipio", how="outer", indicator=True)
    if (base["_merge"] != "both").any() or len(base) != N_MUNICIPIOS:
        raise RuntimeError(f"Censo 2022: municípios sem par\n{base[base['_merge'] != 'both']}")
    base = base.drop(columns="_merge")
    c10 = buscar_censo_2010()
    sem_par_2010 = sorted(set(c10["municipio"]) - set(base["municipio"]))
    if sem_par_2010:
        raise RuntimeError(f"Censo 2010: nomes sem par em 2022: {sem_par_2010}")
    base = base.merge(c10, on="municipio", how="left")
    base["razao_feminina_2022"] = base["pop_feminina_2022"] / base["pop_total_2022"]
    base["razao_feminina_2010"] = base["pop_feminina_2010"] / base["pop_total_2010"]
    base["variacao_pp_2010_2022"] = 100 * (base["razao_feminina_2022"] - base["razao_feminina_2010"])
    return base.sort_values("municipio").reset_index(drop=True)


def rodar(tipo: str, razao: pd.Series) -> tuple[list[dict], list[dict]]:
    gdf = montar_geodataframe(tipo, ANO_INICIO, ANO_FIM)
    w = montar_pesos_espaciais(gdf)
    casos = gdf["casos_total"].to_numpy(dtype=float)
    pop_total = gdf["populacao_pessoas_ano"].to_numpy(dtype=float)
    r = gdf["municipio"].map(razao).to_numpy(dtype=float)
    if len(gdf) != N_MUNICIPIOS or np.isnan(casos).any() or np.isnan(pop_total).any() or np.isnan(r).any():
        raise ValueError(f"{tipo}: universo diferente de {N_MUNICIPIOS} municípios completos.")
    denominadores = {"total": pop_total, "feminina": pop_total * r}

    resumo, municipios = [], []
    for nome, pop in denominadores.items():
        inicio = time.perf_counter()
        moran = rodar_global("assuncao_reis", casos, pop, None, w, N_PERMUTACOES, SEED)
        lisa = rodar_local("assuncao_reis", casos, pop, None, w, N_PERMUTACOES, SEED)
        p = np.asarray(lisa.p_sim, dtype=float)
        sig = benjamini_hochberg(p)
        q = np.asarray(lisa.q)
        linha = {
            "tipo_crime": tipo,
            "denominador": nome,
            "n_municipios": w.n,
            "permutacoes": N_PERMUTACOES,
            "semente": SEED,
            "moran_i": moran.I,
            "moran_ei": moran.EI,
            "moran_z_sim": moran.z_sim,
            "moran_p_sim": moran.p_sim,
            "lisa_total_fdr": int(sig.sum()),
            **{f"lisa_{qn}_fdr": int(((q == qc) & sig).sum()) for qc, qn in QUADRANTES.items()},
            "observacao": NOTA_DENOMINADOR if nome == "feminina" else "população total (pipeline atual)",
        }
        resumo.append(linha)
        for i, mun in enumerate(gdf["municipio"]):
            municipios.append({
                "tipo_crime": tipo, "municipio": mun, "denominador": nome,
                "casos_total": int(casos[i]), "populacao_ano": pop[i],
                "taxa_por_100mil": casos[i] / pop[i] * 100_000,
                "quadrante": QUADRANTES[int(q[i])], "p_sim": p[i], "significativo_fdr": bool(sig[i]),
            })
        print(f"{tipo} | {nome}: I={moran.I:.4f} p={moran.p_sim:.5f} LISA FDR={int(sig.sum())} "
              f"({time.perf_counter() - inicio:.1f}s)", flush=True)
    return resumo, municipios


def validar_contra_atual(resumo: pd.DataFrame) -> pd.DataFrame:
    """A versão total precisa reproduzir o CSV publicado do pipeline."""
    atual = pd.read_csv(CSV_ATUAL)
    atual = atual[atual["configuracao"] == "assuncao_reis"].set_index("tipo_crime")
    linhas = []
    for _, lin in resumo[resumo["denominador"] == "total"].iterrows():
        a = atual.loc[lin["tipo_crime"]]
        cols = ["lisa_total_fdr", "lisa_aa_fdr", "lisa_ba_fdr", "lisa_bb_fdr", "lisa_ab_fdr"]
        ok = np.isclose(lin["moran_i"], a["moran_i"]) and np.isclose(lin["moran_p_sim"], a["moran_p_sim"]) \
            and all(int(lin[c]) == int(a[c]) for c in cols)
        linhas.append({"tipo_crime": lin["tipo_crime"], "moran_i_atual": a["moran_i"],
                       "moran_i_recalculado": lin["moran_i"], "lisa_fdr_atual": int(a["lisa_total_fdr"]),
                       "lisa_fdr_recalculado": int(lin["lisa_total_fdr"]), "reproduz": ok})
    val = pd.DataFrame(linhas)
    if not val["reproduz"].all():
        raise RuntimeError(f"Versão total não reproduz o CSV atual:\n{val}")
    return val


def comparar(mun: pd.DataFrame) -> pd.DataFrame:
    largo = mun.pivot_table(index=["tipo_crime", "municipio"], columns="denominador",
                            values=["significativo_fdr", "quadrante"], aggfunc="first")
    linhas = []
    for tipo, g in largo.groupby(level=0):
        st, sf = g[("significativo_fdr", "total")].astype(bool), g[("significativo_fdr", "feminina")].astype(bool)
        qt, qf = g[("quadrante", "total")], g[("quadrante", "feminina")]
        linhas.append({
            "tipo_crime": tipo,
            "sig_total": int(st.sum()), "sig_feminina": int(sf.sum()),
            "entram": int((sf & ~st).sum()), "saem": int((st & ~sf).sum()),
            "permanecem": int((st & sf).sum()),
            "mudam_quadrante": int((st & sf & (qt != qf)).sum()),
            "lista_entram": ", ".join(g.index[sf & ~st].get_level_values(1)),
            "lista_saem": ", ".join(g.index[st & ~sf].get_level_values(1)),
            "lista_mudam": ", ".join(f"{m} ({a.upper()}→{b.upper()})" for m, a, b in zip(
                g.index[st & sf & (qt != qf)].get_level_values(1),
                qt[st & sf & (qt != qf)], qf[st & sf & (qt != qf)])),
        })
    return pd.DataFrame(linhas)


def fmt(x, casas=3):
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def tabela_md(df: pd.DataFrame) -> str:
    cab = "| " + " | ".join(df.columns) + " |"
    sep = "|" + "|".join("---" for _ in df.columns) + "|"
    return "\n".join([cab, sep] + ["| " + " | ".join(str(v) for v in lin) + " |" for lin in df.itertuples(index=False)])


def escrever_md(pop, resumo, comp, val, mun) -> None:
    r22 = pop["razao_feminina_2022"]
    v = pop["variacao_pp_2010_2022"].dropna()
    va = v.abs()
    sig_qualquer = (mun[mun["significativo_fdr"]].groupby("municipio")["tipo_crime"]
                    .apply(lambda s: ", ".join(sorted(set(s)))))
    grandes = pop[pop["variacao_pp_2010_2022"].abs() > LIMIAR_LISTA_PP].copy()
    grandes = grandes.reindex(grandes["variacao_pp_2010_2022"].abs().sort_values(ascending=False).index)

    l = []
    l.append("# População feminina vs. população total como denominador: Moran global e LISA, 2018-2025\n")
    l.append(f"> **Denominador feminino: {NOTA_DENOMINADOR}.** O IBGE só publica população municipal por "
             "sexo nos Censos; as estimativas anuais trazem só o total. A suposição é testada abaixo com o "
             "Censo 2010.\n")
    n_perm = f"{N_PERMUTACOES:_}".replace("_", ".")
    l.append("Gerado por `src/analysis/denominador_feminino.py`. Parâmetros iguais aos do pipeline "
             "(`moran_lisa_assuncao_reis.py`): ajuste de Assunção e Reis, contiguidade de rainha padronizada "
             f"por linha, {N_MUNICIPIOS} municípios, {n_perm} permutações, semente {SEED}, "
             "Benjamini-Hochberg (α = 0,05) sobre o p direcional do esda. Desfechos: "
             + ", ".join(TIPOS_LISA) + ".\n")

    l.append("## 1. Razão feminina/total por município (Censo 2022)\n")
    i_min, i_max = r22.idxmin(), r22.idxmax()
    l.append(tabela_md(pd.DataFrame([{
        "Mínimo": f"{fmt(r22.min())} ({pop.loc[i_min, 'municipio']})",
        "1º quartil": fmt(r22.quantile(.25)), "Mediana": fmt(r22.median()),
        "3º quartil": fmt(r22.quantile(.75)),
        "Máximo": f"{fmt(r22.max())} ({pop.loc[i_max, 'municipio']})"}])) + "\n")

    l.append("## 2. Verificação da suposição: razão feminina 2010 vs. 2022\n")
    l.append(f"Variação = razão 2022 − razão 2010, em pontos percentuais (p.p.), para os {len(v)} municípios "
             "presentes nos dois Censos. Pinto Bandeira (instalado em 2013) não existe no Censo 2010.\n")
    l.append(tabela_md(pd.DataFrame([{
        "Mínimo": fmt(v.min(), 2), "1º quartil": fmt(v.quantile(.25), 2), "Mediana": fmt(v.median(), 2),
        "3º quartil": fmt(v.quantile(.75), 2), "Máximo": fmt(v.max(), 2),
        "Mediana de |variação|": fmt(va.median(), 2)}])) + "\n")
    l.append(tabela_md(pd.DataFrame([{
        "Limiar": f"> {t} p.p.", "Municípios": int((va > t).sum()),
        "% dos municípios": fmt(100 * (va > t).mean(), 1)} for t in LIMIARES_PP])) + "\n")
    if len(grandes):
        l.append(f"Municípios com |variação| > {fmt(LIMIAR_LISTA_PP, 0)} p.p. (onde a suposição pode distorcer):\n")
        l.append(tabela_md(pd.DataFrame([{
            "Município": g.municipio, "Pop. total 2022": f"{int(g.pop_total_2022):,}".replace(",", "."),
            "Razão 2010": fmt(g.razao_feminina_2010), "Razão 2022": fmt(g.razao_feminina_2022),
            "Variação (p.p.)": fmt(g.variacao_pp_2010_2022, 2),
            "Significativo no LISA (qualquer versão)": sig_qualquer.get(g.municipio, "—")}
            for g in grandes.itertuples()])) + "\n")
    else:
        l.append(f"Nenhum município variou mais de {fmt(LIMIAR_LISTA_PP, 0)} p.p.\n")

    l.append("## 3. Moran global\n")
    rz = resumo.pivot(index="tipo_crime", columns="denominador")
    l.append(tabela_md(pd.DataFrame([{
        "Desfecho": t, "I (total)": fmt(rz.loc[t, ("moran_i", "total")], 4),
        "I (feminina)": fmt(rz.loc[t, ("moran_i", "feminina")], 4),
        "Diferença": fmt(rz.loc[t, ("moran_i", "feminina")] - rz.loc[t, ("moran_i", "total")], 4),
        "z (total)": fmt(rz.loc[t, ("moran_z_sim", "total")], 2),
        "z (feminina)": fmt(rz.loc[t, ("moran_z_sim", "feminina")], 2),
        "p (total)": fmt(rz.loc[t, ('moran_p_sim', 'total')], 5),
        "p (feminina)": fmt(rz.loc[t, ('moran_p_sim', 'feminina')], 5)} for t in TIPOS_LISA])) + "\n")

    l.append("## 4. LISA: municípios significativos (FDR)\n")
    c = comp.set_index("tipo_crime")
    l.append(tabela_md(pd.DataFrame([{
        "Desfecho": t, "Significativos (total)": c.loc[t, "sig_total"],
        "Significativos (feminina)": c.loc[t, "sig_feminina"], "Entram": c.loc[t, "entram"],
        "Saem": c.loc[t, "saem"], "Permanecem": c.loc[t, "permanecem"],
        "Mudam de quadrante": c.loc[t, "mudam_quadrante"]} for t in TIPOS_LISA])) + "\n")
    l.append("Entram = significativos só com denominador feminino; saem = só com o total; mudam de quadrante = "
             "significativos nas duas versões, em quadrantes diferentes.\n")
    l.append(tabela_md(pd.DataFrame([{
        "Desfecho": t, "Quadrante": qn.upper(),
        "Total": int(rz.loc[t, (f"lisa_{qn}_fdr", "total")]),
        "Feminina": int(rz.loc[t, (f"lisa_{qn}_fdr", "feminina")])}
        for t in TIPOS_LISA for qn in QUADRANTES.values()])) + "\n")
    mudancas = []
    pi = pop.set_index("municipio")
    for _, r in comp.iterrows():
        for rotulo, chave in [("entra", "lista_entram"), ("sai", "lista_saem"), ("muda de quadrante", "lista_mudam")]:
            for item in filter(None, r[chave].split(", ")):
                m = item.split(" (")[0]
                ml = mun[(mun["tipo_crime"] == r["tipo_crime"]) & (mun["municipio"] == m)].set_index("denominador")
                var = pi.loc[m, "variacao_pp_2010_2022"]
                mudancas.append({
                    "Desfecho": r["tipo_crime"], "Município": item, "Mudança": rotulo,
                    "Pop. total 2022": f"{int(pi.loc[m, 'pop_total_2022']):,}".replace(",", "."),
                    "Razão 2022": fmt(pi.loc[m, "razao_feminina_2022"]),
                    "Variação 2010-2022 (p.p.)": "—" if pd.isna(var) else fmt(var, 2),
                    "p (total)": fmt(ml.loc["total", "p_sim"], 5),
                    "p (feminina)": fmt(ml.loc["feminina", "p_sim"], 5)})
    if mudancas:
        l.append("Municípios que entram, saem ou mudam de quadrante:\n")
        l.append(tabela_md(pd.DataFrame(mudancas)) + "\n")

    l.append("## 5. Validação\n")
    l.append("A versão com população total, recalculada neste script, reproduz o CSV publicado "
             "(`moran_lisa_assuncao_reis_2018_2025.csv`, configuração `assuncao_reis`):\n")
    l.append(tabela_md(val.assign(
        moran_i_atual=val["moran_i_atual"].map(lambda x: fmt(x, 6)),
        moran_i_recalculado=val["moran_i_recalculado"].map(lambda x: fmt(x, 6)),
        reproduz=val["reproduz"].map({True: "sim", False: "NÃO"}))) + "\n")
    l.append("## Arquivos\n")
    l.append(f"- `{SAIDA_POP.name}`: população feminina e total dos Censos 2010 e 2022, razões e variação.")
    l.append(f"- `{SAIDA_RESUMO.name}`: Moran global e contagens do LISA por desfecho e denominador.")
    l.append(f"- `{SAIDA_LISA.name}`: classificação LISA por município, desfecho e denominador.")
    SAIDA_MD.write_text("\n".join(l) + "\n", encoding="utf-8")


def main() -> None:
    pop = montar_populacao_censos()
    pop.to_csv(SAIDA_POP, index=False)
    razao = pop.set_index("municipio")["razao_feminina_2022"]
    resumo, mun = [], []
    for tipo in TIPOS_LISA:
        r, m = rodar(tipo, razao)
        resumo += r
        mun += m
    resumo, mun = pd.DataFrame(resumo), pd.DataFrame(mun)
    val = validar_contra_atual(resumo)
    resumo.to_csv(SAIDA_RESUMO, index=False)
    mun.to_csv(SAIDA_LISA, index=False)
    comp = comparar(mun)
    escrever_md(pop, resumo, comp, val, mun)
    print(comp.drop(columns=["lista_entram", "lista_saem", "lista_mudam"]).to_string(index=False))
    print(f"Gravado: {SAIDA_MD}")


if __name__ == "__main__":
    main()
