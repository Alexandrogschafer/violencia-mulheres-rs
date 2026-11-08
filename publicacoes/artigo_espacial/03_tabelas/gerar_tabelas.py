"""Gera as tabelas do artigo espacial a partir das tabelas de resultado do pipeline.

Nenhum número é digitado: tudo vem das funções e dos CSVs de `src/analysis/`, com os mesmos parâmetros do
artigo (denominador feminino, 2018-2025, semente 12345, 99.999 permutações, Benjamini-Hochberg a 5% sobre o
p direcional, ajuste de Assunção e Reis). Antes de gravar, cada tabela é conferida contra o arquivo de
resultado correspondente em `outputs/tables/`:
- Tabela 1 e Tabela 2 contra `resultados_consolidados.md`;
- Tabela 3 contra `sobreposicao_desfechos.md`;
- Suplementar 1 (pares significativos) contra `esperado_vs_observado_lisa.md`;
- Suplementar 2 (denominador) contra `denominador_feminino_vs_total.md`.
As suplementares são numeradas pela ordem de citação no texto (desde 2026-11-08: a dos pares, citada
primeiro nos Resultados, é a 1).
Se algo divergir, o script para sem gravar.

Nomes de município: os do pipeline são em maiúsculas e sem acento (convenção SSP/PROCERGS). Nas tabelas
entram os nomes oficiais do IBGE, tirados da coluna «Mun» da base da MUNIC 2023
(`data/raw/rede_atendimento/munic/Base_MUNIC_2023.xlsx`), com junção pelo código IBGE de
`outputs/tables/municipio_codigo_ibge.csv`. O COREDE vem de `outputs/tables/municipio_corede.csv`.

Saída, em publicacoes/artigo_espacial/03_tabelas/:
- `tabelas.md`, com todas as tabelas e as legendas abaixo de cada uma, no padrão da RESS;
- um CSV por tabela, para a diagramação. Os CSVs são em UTF-8, separados por ponto e vírgula, com os
  valores já formatados como na tabela (vírgula decimal).

Uso, da raiz do repositório:
    python3 publicacoes/artigo_espacial/03_tabelas/gerar_tabelas.py
"""

import re
import sys
from itertools import combinations
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ))

import pandas as pd  # noqa: E402

from src.analysis.denominador import caminho  # noqa: E402
from src.analysis.esperado_vs_observado_lisa import LIMIAR, calcular  # noqa: E402
from src.analysis.mapa_choropleth import montar_geodataframe  # noqa: E402
from src.analysis.moran_lisa_assuncao_reis import ANO_FIM, ANO_INICIO, N_MUNICIPIOS, SEED  # noqa: E402
from src.analysis.resultados_consolidados import (  # noqa: E402
    ESTABILIDADE_CSV,
    LISA,
    ORDEM_DESFECHOS,
    PERMUTACOES,
    QUADRANTES,
    carregar_feminino,
    carregar_lisa,
    carregar_moran,
)

TABLES = RAIZ / "outputs" / "tables"
SAIDA = Path(__file__).resolve().parent
MUNIC = RAIZ / "data" / "raw" / "rede_atendimento" / "munic" / "Base_MUNIC_2023.xlsx"
LISA_POR_MUNICIPIO = TABLES / "lisa_denominador_feminino_vs_total_2018_2025.csv"
FEMININO_CSV = TABLES / "moran_lisa_denominador_feminino_2018_2025.csv"

NOME_QUADRANTE = {"AA": "Alto-alto", "BB": "Baixo-baixo", "AB": "Alto-baixo", "BA": "Baixo-alto"}
# ---------------------------------------------------------------- formatação


def br(x: float, casas: int) -> str:
    return f"{x:,.{casas}f}".replace(",", " ").replace(".", ",").replace(" ", ".")


def fmt_p(p: float) -> str:
    return "< 0,0001" if p < 1e-4 else br(p, 4)


def markdown(df: pd.DataFrame) -> str:
    linhas = [list(df.columns), ["---"] * df.shape[1], *df.astype(str).to_numpy().tolist()]
    return "\n".join("| " + " | ".join(map(str, linha)) + " |" for linha in linhas)


def le_tabela_md(arquivo: Path, cabecalho_inicio: str, depois_de: str | None = None) -> pd.DataFrame:
    """Primeira tabela Markdown do arquivo cujo cabeçalho começa com `cabecalho_inicio`, opcionalmente
    procurando só depois da linha que contém `depois_de`."""
    texto = arquivo.read_text(encoding="utf-8")
    if depois_de is not None:
        texto = texto[texto.index(depois_de):]
    linhas = texto.splitlines()
    i = next(k for k, l in enumerate(linhas) if l.startswith("| " + cabecalho_inicio))
    bloco = []
    for l in linhas[i:]:
        if not l.startswith("|"):
            break
        bloco.append([c.strip() for c in l.strip().strip("|").split("|")])
    return pd.DataFrame(bloco[2:], columns=bloco[0])


def confere(condicao: bool, mensagem: str) -> None:
    if not condicao:
        sys.exit(f"Divergência com a tabela de resultado: {mensagem}. Nada foi gravado.")


# ---------------------------------------------------------------- dados de apoio


def nomes_oficiais() -> pd.Series:
    """Nome do pipeline (MAIÚSCULAS sem acento) → nome oficial do IBGE (base da MUNIC 2023)."""
    codigos = pd.read_csv(TABLES / "municipio_codigo_ibge.csv", dtype={"codigo_ibge": str})
    munic = pd.read_excel(MUNIC, sheet_name="Segurança Pública", usecols=["CodMun", "Mun"], dtype=str)
    m = codigos.merge(munic, left_on="codigo_ibge", right_on="CodMun", how="left")
    confere(len(m) == N_MUNICIPIOS and m["Mun"].notna().all(), "municípios sem nome na base da MUNIC 2023")
    return m.set_index("municipio")["Mun"]


def coredes() -> pd.Series:
    c = pd.read_csv(TABLES / "municipio_corede.csv").set_index("municipio")["corede"]
    confere(len(c) == N_MUNICIPIOS, "municipio_corede.csv sem os 497 municípios")
    return c


def significativos() -> pd.DataFrame:
    """Pares município-desfecho significativos na semente 12345, conferidos pelo próprio pipeline."""
    moran_fem = pd.read_csv(FEMININO_CSV)
    moran_fem = moran_fem[moran_fem["denominador"] == "feminina"]
    lisa = carregar_lisa(moran_fem, "feminina")
    return lisa[lisa["sobrevive_fdr"] & lisa["tipo_crime"].isin(LISA)].copy()


# ---------------------------------------------------------------- Tabela 1


def tabela1(estadual: dict) -> pd.DataFrame:
    fem = carregar_feminino(carregar_moran())
    bruta = fem[fem["configuracao"] == "bruta"].set_index("tipo_crime")
    ajust = fem[fem["configuracao"] == "assuncao_reis"].set_index("tipo_crime")
    linhas = []
    for tipo in ORDEM_DESFECHOS:
        casos = montar_geodataframe(tipo, ANO_INICIO, ANO_FIM)["casos_total"].astype(float)
        confere(len(casos) == N_MUNICIPIOS and not casos.isna().any(), f"{tipo}: universo incompleto")
        linhas.append({
            "Desfecho": tipo,
            "Eventos": br(casos.sum(), 0),
            "Contagem municipal mediana": br(casos.median(), 0),
            "Municípios sem registro (%)": br(100 * (casos == 0).mean(), 1),
            "Taxa estadual por 100 mil mulheres-ano": br(estadual[tipo], 2),
            "I de Moran, taxa bruta": br(bruta.loc[tipo, "moran_i"], 4),
            "p (bruta)": br(bruta.loc[tipo, "moran_p_sim"], 5),
            "I de Moran ajustado": br(ajust.loc[tipo, "moran_i"], 4),
            "p (ajustado)": br(ajust.loc[tipo, "moran_p_sim"], 5),
        })
    t = pd.DataFrame(linhas)

    ref = le_tabela_md(TABLES / "resultados_consolidados.md", "Desfecho").set_index("Desfecho")
    for _, r in t.iterrows():
        d = r["Desfecho"]
        confere(r["Eventos"] == ref.loc[d, "Eventos"], f"Tabela 1, eventos de {d}")
        confere(r["Municípios sem registro (%)"] + "%" == ref.loc[d, "Municípios com zero"], f"Tabela 1, zeros de {d}")
        confere(br(float(ref.loc[d, "Mediana municipal"].replace(",", ".")), 0) == r["Contagem municipal mediana"],
                f"Tabela 1, mediana de {d}")
        for col, col_ref in [("I de Moran, taxa bruta", "Moran bruto"), ("p (bruta)", "p bruto"),
                             ("I de Moran ajustado", "Moran ajustado"), ("p (ajustado)", "p ajustado")]:
            confere(r[col] == ref.loc[d, col_ref], f"Tabela 1, {col_ref} de {d}")
    return t




# ---------------------------------------------------------------- Tabela 2


def tabela2(sig: pd.DataFrame) -> pd.DataFrame:
    linhas = []
    for d in LISA:
        g = sig[sig["tipo_crime"] == d]
        linha = {"Desfecho": d}
        for q in QUADRANTES:
            linha[NOME_QUADRANTE[q]] = int((g["categoria"] == q).sum())
        linha["Total"] = len(g)
        linhas.append(linha)
    t = pd.DataFrame(linhas)
    total = {"Desfecho": "Total", **{c: int(t[c].sum()) for c in t.columns if c != "Desfecho"}}
    t = pd.concat([t, pd.DataFrame([total])], ignore_index=True)

    ref = le_tabela_md(TABLES / "resultados_consolidados.md", "Desfecho").set_index("Desfecho")
    for _, r in t.iloc[:-1].iterrows():
        for q in QUADRANTES:
            confere(str(r[NOME_QUADRANTE[q]]) == ref.loc[r["Desfecho"], f"LISA {q}"], f"Tabela 2, {r['Desfecho']} {q}")
        confere(str(r["Total"]) == ref.loc[r["Desfecho"], "LISA total"], f"Tabela 2, total de {r['Desfecho']}")
    return t




# ---------------------------------------------------------------- Tabela 3


def tabela3(sig: pd.DataFrame, nomes: pd.Series, abaixo_limiar: set) -> tuple[pd.DataFrame, pd.DataFrame]:
    gerais = {d: set(sig.loc[sig["tipo_crime"] == d, "municipio"]) for d in LISA}
    matriz = pd.DataFrame([{"Desfecho": a, **{b: len(gerais[a] & gerais[b]) for b in LISA}} for a in LISA])

    linhas = []
    for q in QUADRANTES:
        conj = {d: set(sig.loc[(sig["tipo_crime"] == d) & (sig["categoria"] == q), "municipio"]) for d in LISA}
        for k in range(2, len(LISA) + 1):
            for combo in combinations(LISA, k):
                dentro = set.intersection(*(conj[d] for d in combo))
                fora = set().union(*(conj[d] for d in LISA if d not in combo))
                exatos = sorted(dentro - fora, key=lambda m: nomes[m])
                if exatos:
                    rotulos = [nomes[m] + (SOBRESCRITO["c"] if any((m, d) in abaixo_limiar for d in combo) else "") for m in exatos]
                    linhas.append({"Quadrante": NOME_QUADRANTE[q], "Desfechos": " e ".join(combo),
                                   "Municípios": len(exatos), "Quais": ", ".join(rotulos)})
    comb = pd.DataFrame(linhas)

    # Conferência com sobreposicao_desfechos.md: matriz geral e combinações de cada quadrante.
    arq = TABLES / "sobreposicao_desfechos.md"
    ref = le_tabela_md(arq, "Desfecho", "## Qualquer quadrante").set_index("Desfecho")
    for a in LISA:
        for b in LISA:
            confere(str(matriz.set_index("Desfecho").loc[a, b]) == ref.loc[a, b], f"Tabela 3, matriz {a} × {b}")
    for q in QUADRANTES:
        r = le_tabela_md(arq, "Combinação", f"## Mesmo quadrante: {q}")
        r = r[r["Combinação"] != "nenhuma"]
        nossos = comb[comb["Quadrante"] == NOME_QUADRANTE[q]]
        confere(len(r) == len(nossos), f"Tabela 3, número de combinações em {q}")
        for (_, a), (_, b) in zip(r.iterrows(), nossos.iterrows()):
            confere(a["Combinação"].replace(" + ", " e ") == b["Desfechos"] and a["Municípios"] == str(b["Municípios"]),
                    f"Tabela 3, combinação {a['Combinação']} em {q}")
    mistos = sig.groupby("municipio")["categoria"].nunique()
    confere(int((mistos > 1).sum()) == 0, "há município em dois desfechos com quadrantes diferentes")
    return matriz, comb




# ---------------------------------------------------------------- Suplementar 2 (denominador)


def suplementar_denominador() -> pd.DataFrame:
    fem = pd.read_csv(FEMININO_CSV)
    fem = fem[(fem["configuracao"] == "assuncao_reis") & (fem["semente"] == SEED) & (fem["permutacoes"] == PERMUTACOES)]
    i = fem.pivot(index="tipo_crime", columns="denominador", values="moran_i")
    p = fem.pivot(index="tipo_crime", columns="denominador", values="moran_p_sim")
    n = fem.pivot(index="tipo_crime", columns="denominador", values="lisa_total_fdr")

    mun = pd.read_csv(LISA_POR_MUNICIPIO)
    sig = mun[mun["significativo_fdr"]]
    linhas = []
    for d in ORDEM_DESFECHOS:
        linha = {
            "Desfecho": d,
            "I (pop. total)": br(i.loc[d, "total"], 4), "I (pop. feminina)": br(i.loc[d, "feminina"], 4),
            "Diferença": br(i.loc[d, "feminina"] - i.loc[d, "total"], 4),
            "p (pop. total)": br(p.loc[d, "total"], 5), "p (pop. feminina)": br(p.loc[d, "feminina"], 5),
        }
        if d in LISA:
            t = sig[(sig["tipo_crime"] == d) & (sig["denominador"] == "total")].set_index("municipio")["quadrante"]
            f = sig[(sig["tipo_crime"] == d) & (sig["denominador"] == "feminina")].set_index("municipio")["quadrante"]
            comuns = t.index.intersection(f.index)
            confere(len(t) == int(n.loc[d, "total"]) and len(f) == int(n.loc[d, "feminina"]),
                    f"Suplementar 2, contagem do LISA de {d}")
            linha.update({
                "LISA (pop. total)": len(t), "LISA (pop. feminina)": len(f),
                "Só com pop. feminina": len(f.index.difference(t.index)),
                "Só com pop. total": len(t.index.difference(f.index)),
                "Mudam de quadrante": int((t[comuns] != f[comuns]).sum()),
            })
        else:
            linha.update({k: "—" for k in ["LISA (pop. total)", "LISA (pop. feminina)", "Só com pop. feminina",
                                           "Só com pop. total", "Mudam de quadrante"]})
        linhas.append(linha)
    s = pd.DataFrame(linhas)

    arq = TABLES / "denominador_feminino_vs_total.md"
    ref_i = le_tabela_md(arq, "Desfecho | I (total)").set_index("Desfecho")
    ref_l = le_tabela_md(arq, "Desfecho | Significativos").set_index("Desfecho")
    for _, r in s.iterrows():
        d = r["Desfecho"]
        if d in ref_i.index:
            confere(r["I (pop. total)"] == ref_i.loc[d, "I (total)"] and r["I (pop. feminina)"] == ref_i.loc[d, "I (feminina)"],
                    f"Suplementar 2, Moran de {d}")
        if d in ref_l.index:
            for col, col_ref in [("LISA (pop. total)", "Significativos (total)"), ("LISA (pop. feminina)", "Significativos (feminina)"),
                                 ("Só com pop. feminina", "Entram"), ("Só com pop. total", "Saem"),
                                 ("Mudam de quadrante", "Mudam de quadrante")]:
                confere(str(r[col]) == ref_l.loc[d, col_ref], f"Suplementar 2, {col_ref} de {d}")
    return s




# ---------------------------------------------------------------- Suplementar 1 (pares significativos)


def suplementar_pares(pares: pd.DataFrame, nomes: pd.Series, corede: pd.Series) -> pd.DataFrame:
    ordem_d = {d: k for k, d in enumerate(LISA)}
    ordem_q = {q: k for k, q in enumerate(QUADRANTES)}
    p = pares.assign(_d=pares["desfecho"].map(ordem_d), _q=pares["quadrante"].map(ordem_q),
                     _n=pares["municipio"].map(nomes))
    p = p.sort_values(["_d", "_q", "_n"])
    s = pd.DataFrame({
        "Município": p["_n"], "COREDE": p["municipio"].map(corede), "Desfecho": p["desfecho"],
        "Quadrante": p["quadrante"].map(NOME_QUADRANTE), "Observado": p["observado"].map(lambda v: br(v, 0)),
        "Esperado": p["esperado"].map(lambda v: br(v, 2)), "Razão O/E": p["razao"].map(lambda v: br(v, 2)),
        "p de Poisson": p["p_poisson"].map(fmt_p),
        f"Esperado ≥ {LIMIAR}": p["esperado"].map(lambda v: "sim" if v >= LIMIAR else "não"),
    })
    confere(s["COREDE"].notna().all(), "Suplementar 1, município sem COREDE")

    ref = le_tabela_md(TABLES / "esperado_vs_observado_lisa.md", "Município", "## Os 67 pares")
    chave_ref = set(zip(ref["Município"], ref["Desfecho"], ref["Quadrante"], ref["Observado"], ref["Esperado"],
                        ref["Obs./esp."], ref["Poisson, direção do quadrante"], ref[f"Esperado ≥ {LIMIAR}"]))
    chave = set(zip(p["municipio"], p["desfecho"], p["quadrante"], p["observado"].astype(int).astype(str), s["Esperado"],
                    s["Razão O/E"], s["p de Poisson"], s[f"Esperado ≥ {LIMIAR}"]))
    confere(len(s) == 67 and chave == chave_ref, "Suplementar 1 diverge de esperado_vs_observado_lisa.md")
    return s.reset_index(drop=True)




# ---------------------------------------------------------------- saída


# ---------------------------------------------------------------- legendas no padrão da RESS
#
# Regras da RESS (instruções aos autores, lidas em 2026-11-03): título sem ponto final, com local, anos e total;
# siglas no título; sem o tipo de ilustração; notas de rodapé identificadas por letras minúsculas sobrescritas,
# em ordem, separadas por ponto e vírgula; sem «Fonte:» nem detalhes metodológicos, que ficam nos Métodos;
# suplementares como «Tabela suplementar n». Os rótulos dos desfechos seguem a grafia do manuscrito.
# A formatação abaixo só é aplicada na saída, depois das conferências, que usam os nomes internos.

SOBRESCRITO = {"a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ", "e": "ᵉ"}
DESFECHO_TEXTO = {d: d[0] + d[1:].lower() for d in ORDEM_DESFECHOS}  # «Lesão Corporal» -> «Lesão corporal»
NOTA_QUADRANTE = (
    "alto-alto e baixo-baixo: município com valor alto (baixo) cercado de vizinhos com valores altos (baixos); "
    "alto-baixo e baixo-alto: outliers espaciais; «alto» e «baixo» referem-se à média dos municípios, e não à taxa "
    "estadual"
)
NOTA_ESPERADO = (
    f"menos de {LIMIAR} eventos esperados sob a taxa estadual: par mantido no cálculo, sem interpretação substantiva"
)


def s_(letras: str) -> str:
    return "".join(SOBRESCRITO[l] for l in letras.replace(",", ""))


def notas(itens: list[tuple[str, str]]) -> str:
    corpo = "; ".join(f"{SOBRESCRITO[l]} {texto}" for l, texto in itens) + "."
    return corpo[:2] + corpo[2].upper() + corpo[3:]


def rotula_desfechos(df: pd.DataFrame) -> pd.DataFrame:
    """Troca a grafia dos desfechos pela do manuscrito em células e cabeçalhos."""
    def troca(v):
        if not isinstance(v, str):
            return v
        for de, para in DESFECHO_TEXTO.items():
            v = v.replace(de, para)
        return v
    out = df.map(troca)
    out.columns = [troca(c) for c in df.columns]
    return out


def formata(df: pd.DataFrame, colunas: dict[str, str] | None = None, linhas: dict[str, str] | None = None) -> pd.DataFrame:
    """Acrescenta as letras de nota a cabeçalhos (colunas) e a rótulos da primeira coluna (linhas)."""
    out = df.copy()
    if linhas:
        primeira = out.columns[0]
        out[primeira] = out[primeira].map(lambda v: v + s_(linhas[v]) if v in linhas else v)
    if colunas:
        out = out.rename(columns={c: c + s_(l) for c, l in colunas.items()})
    return rotula_desfechos(out)


def legenda(rotulo: str, titulo: str, itens: list[tuple[str, str]]) -> str:
    texto = f"**{rotulo}.** {titulo}"
    return texto + ("\n\n" + notas(itens) if itens else "")


def pecas_formatadas(t1, t2, t3a, t3b, s_pares, s_denominador) -> list[tuple[str, pd.DataFrame, str]]:
    return [
        ("tabela1_desfechos",
         formata(t1, colunas={"Taxa estadual por 100 mil mulheres-ano": "a", "p (bruta)": "b",
                              "I de Moran ajustado": "c", "p (ajustado)": "b"}),
         legenda("Tabela 1", "Eventos registrados, contagem municipal, taxa estadual e índice de Moran global, por "
                 "desfecho de violência contra a mulher, Rio Grande do Sul, 2018-2025 (n = 497 municípios)",
                 [("a", "eventos do estado divididos pelas mulheres-ano acumuladas, multiplicados por 100 mil"),
                  ("b", "o menor valor p obtenível com 99.999 permutações é 0,00001"),
                  ("c", "com o ajuste de Assunção e Reis")])),
        ("tabela2_significativos_por_quadrante",
         formata(t2, colunas={"Desfecho": "a", "Alto-alto": "b", "Baixo-baixo": "b", "Alto-baixo": "b",
                              "Baixo-alto": "b", "Total": "c"}),
         legenda("Tabela 2", "Pares município-desfecho com indicador local de associação espacial (LISA) "
                 "significativo, por desfecho de violência contra a mulher e quadrante, Rio Grande do Sul, "
                 "2018-2025 (n = 67 pares)",
                 [("a", "o feminicídio consumado não foi analisado no nível local, pela baixa ocorrência"),
                  ("b", NOTA_QUADRANTE),
                  ("c", "um município significativo em dois desfechos conta uma vez em cada um")])),
        ("tabela3a_sobreposicao_matriz",
         formata(t3a, colunas={"Desfecho": "a,b"}),
         legenda("Tabela 3", "Municípios com indicador local de associação espacial (LISA) significativo em mais "
                 "de um desfecho de violência contra a mulher, em qualquer quadrante (A) e no mesmo quadrante (B), "
                 "Rio Grande do Sul, 2018-2025 (n = 58 municípios)",
                 [("a", "na diagonal, os municípios significativos em cada desfecho; fora dela, os significativos "
                        "nos dois desfechos"),
                  ("b", "nenhum município foi significativo em três ou mais desfechos, nem em dois desfechos com "
                        "quadrantes diferentes")])),
        ("tabela3b_sobreposicao_combinacoes",
         formata(t3b, colunas={"Quadrante": "a", "Municípios": "b"}),
         legenda("Tabela 3", "(continuação) (B) Combinações de desfechos no mesmo quadrante",
                 [("a", NOTA_QUADRANTE),
                  ("b", "municípios significativos exatamente naqueles desfechos, e em nenhum outro"),
                  ("c", NOTA_ESPERADO)])),
        ("suplementar1_pares_significativos",
         formata(s_pares, colunas={"Quadrante": "a", "Esperado": "b", "p de Poisson": "c", f"Esperado ≥ {LIMIAR}": "d"}),
         legenda("Tabela suplementar 1", "Pares município-desfecho com indicador local de associação espacial "
                 "(LISA) significativo, por Conselho Regional de Desenvolvimento (COREDE), com eventos observados "
                 "(O) e esperados (E), razão O/E e probabilidade de Poisson, Rio Grande do Sul, 2018-2025 "
                 "(n = 67 pares)",
                 [("a", NOTA_QUADRANTE),
                  ("b", "mulheres-ano acumuladas do município multiplicadas pela taxa estadual do desfecho e "
                        "divididas por 100 mil"),
                  ("c", "P(X ≥ O) em alto-alto e alto-baixo e P(X ≤ O) em baixo-baixo e baixo-alto; descritivo, "
                        "sem correção para comparações múltiplas e sem considerar a vizinhança"),
                  ("d", f"pares com esperado abaixo de {LIMIAR} foram mantidos no cálculo, sem interpretação "
                        "substantiva")])),
        ("suplementar2_denominador",
         formata(s_denominador, colunas={"I (pop. feminina)": "a", "Só com pop. feminina": "b", "Só com pop. total": "b",
                              "Mudam de quadrante": "c"}, linhas={"Feminicídio Consumado": "d"}),
         legenda("Tabela suplementar 2", "Índice de Moran global ajustado e municípios com indicador local de "
                 "associação espacial (LISA) significativo, com denominador de população feminina e de população "
                 "total, por desfecho de violência contra a mulher, Rio Grande do Sul, 2018-2025 "
                 "(n = 497 municípios)",
                 [("a", "população feminina anual estimada: população total do ano multiplicada pela razão "
                        "feminina do município no Censo 2022"),
                  ("b", "municípios significativos em apenas uma das versões"),
                  ("c", "municípios significativos nas duas versões, em quadrantes diferentes"),
                  ("d", "não analisado no nível local, pela baixa ocorrência")])),
    ]


def main() -> None:
    nomes, corede = nomes_oficiais(), coredes()
    sig = significativos()
    pares, estadual, _ = calcular("feminina")
    abaixo = set(zip(pares.loc[pares["esperado"] < LIMIAR, "municipio"], pares.loc[pares["esperado"] < LIMIAR, "desfecho"]))

    t1 = tabela1(estadual)
    t2 = tabela2(sig)
    t3a, t3b = tabela3(sig, nomes, abaixo)
    s_pares = suplementar_pares(pares, nomes, corede)
    s_denominador = suplementar_denominador()

    pecas = pecas_formatadas(t1, t2, t3a, t3b, s_pares, s_denominador)
    partes = [
        "# Tabelas — artigo espacial\n\n<!-- Gerado por 03_tabelas/gerar_tabelas.py a partir de outputs/tables/. "
        "Não editar à mão. -->"
    ]
    for nome, df, texto in pecas:
        df.to_csv(SAIDA / f"{nome}.csv", sep=";", index=False, encoding="utf-8")
        partes.append(markdown(df) + "\n\n" + texto)
    (SAIDA / "tabelas.md").write_text("\n\n---\n\n".join(partes) + "\n", encoding="utf-8")
    for nome, df, _ in pecas:
        print(f"{nome}: {len(df)} linhas")


if __name__ == "__main__":
    main()
