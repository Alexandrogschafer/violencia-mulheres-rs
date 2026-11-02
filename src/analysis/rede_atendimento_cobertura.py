"""Cobertura da rede de atendimento nos grupos do LISA: os de zero ou poucos eventos são desprovidos de serviço?

Validação de medida, descritiva, sem teste: os grupos são pequenos demais. Grupos tirados do
mesmo conjunto significativo de caracterizacao_municipios_significativos (semente 12345,
99.999 permutações, FDR sobre o p direcional, 2018-2025). Os de "poucos eventos" são pares
município-desfecho, contados aqui pelo município do par.

Pré-requisito: python -m src.fetch_rede_atendimento
Uso: python -m src.analysis.rede_atendimento_cobertura
"""

from pathlib import Path

import pandas as pd

from src.analysis.caracterizacao_municipios_significativos import carregar, markdown, pares

RAIZ = Path(__file__).resolve().parent.parent.parent
REDE = RAIZ / "data" / "processed" / "rede_atendimento_municipio.csv"
CODIGOS = RAIZ / "outputs" / "tables" / "municipio_codigo_ibge.csv"
SAIDA = RAIZ / "outputs" / "tables" / "rede_atendimento_cobertura.md"
COLUNAS = [
    ("deam", 2018, "DEAM 2018¹"),
    ("deam", 2019, "DEAM 2019"),
    ("deam", 2023, "DEAM 2023"),
    ("organismo_mulheres", 2018, "Organismo 2018"),
    ("organismo_mulheres", 2023, "Organismo 2023"),
    ("creas_munic", 2018, "CREAS 2018²"),
    ("creas_munic", 2023, "CREAS 2023²"),
]


def grupos() -> dict[str, list[str]]:
    d = carregar()
    p = pares(d)
    q = d["quadrante"]
    g = {
        "Zero evento, significativos": sorted(p.loc[p["eventos"] == 0, "municipio"].unique()),
        "Pares com até 5 eventos": sorted(p.loc[p["eventos"] <= 5, "municipio"].unique()),
        "Pares com menos de 10 eventos": sorted(p.loc[p["eventos"] < 10, "municipio"].unique()),
        "AA": sorted(q.index[q == "AA"]),
        "BB": sorted(q.index[q == "BB"]),
    }
    esperado = {"Zero evento, significativos": 3, "Pares com até 5 eventos": 9, "AA": 28, "BB": 24}
    for k, n in esperado.items():
        if len(g[k]) != n:
            raise ValueError(f"{k}: {len(g[k])} municípios, esperados {n}.")
    g["pares"] = p
    return g


def celula(st: pd.Series) -> str:
    n, tem, sr = len(st), int((st == "tem").sum()), int((st == "sem_resposta").sum())
    validos = n - sr
    pct = f"{100 * tem / validos:.0f}%".replace(".", ",") if validos else "–"
    return f"{tem}/{validos} ({pct})" + (f"; s/r {sr}" if sr else "")


def tabela(rede: pd.DataFrame, g: dict) -> pd.DataFrame:
    todos = sorted(rede["municipio"].unique())
    conjuntos = {k: v for k, v in g.items() if k != "pares"} | {"Os 497": todos}
    linhas = []
    for nome, munis in conjuntos.items():
        linha = {"Grupo": nome, "n": len(munis)}
        for ind, ed, rot in COLUNAS:
            r = rede[(rede["indicador"] == ind) & (rede["edicao"] == ed)].set_index("municipio")
            linha[rot] = celula(r.loc[munis, "status"])
        linhas.append(linha)
    return pd.DataFrame(linhas)


def detalhe(rede: pd.DataFrame, g: dict) -> pd.DataFrame:
    p = g["pares"]
    p = p[p["eventos"] < 10].sort_values(["eventos", "municipio"])
    simb = {"tem": "sim", "nao_tem": "não", "sem_resposta": "s/r"}
    linhas = []
    for _, r in p.iterrows():
        linha = {
            "Município": r["municipio"],
            "Desfecho": r["tipo"],
            "Quadrante": r["q"],
            "Eventos": r["eventos"],
            "População 2025": f"{r['pop']:,}".replace(",", "."),
        }
        for ind, ed, rot in COLUNAS:
            s = rede[(rede["indicador"] == ind) & (rede["edicao"] == ed) & (rede["municipio"] == r["municipio"])]
            linha[rot] = simb[s["status"].iloc[0]]
        linhas.append(linha)
    return pd.DataFrame(linhas)


def concordancia(rede: pd.DataFrame) -> pd.DataFrame:
    w = rede.pivot_table(index="municipio", columns=["indicador", "edicao"], values="status", aggfunc="first")
    linhas = []
    for (ind, a), (_, b) in [(("deam", 2018), ("deam", 2019)), (("deam", 2019), ("deam", 2023)),
                             (("organismo_mulheres", 2018), ("organismo_mulheres", 2023)),
                             (("creas_munic", 2018), ("creas_munic", 2023))]:
        x, y = w[(ind, a)], w[(ind, b)]
        ok = (x != "sem_resposta") & (y != "sem_resposta")
        linhas.append({
            "Indicador": ind, "Edições": f"{a} → {b}", "Com resposta nas duas": int(ok.sum()),
            "Sim nas duas": int((ok & (x == "tem") & (y == "tem")).sum()),
            "Ganhou": int((ok & (x == "nao_tem") & (y == "tem")).sum()),
            "Perdeu": int((ok & (x == "tem") & (y == "nao_tem")).sum()),
            "Não nas duas": int((ok & (x == "nao_tem") & (y == "nao_tem")).sum()),
        })
    return pd.DataFrame(linhas)


def sem_resposta(rede: pd.DataFrame, g: dict) -> pd.DataFrame:
    sr = rede[rede["status"] == "sem_resposta"]
    alvo = set(g["Pares com menos de 10 eventos"]) | set(g["AA"]) | set(g["BB"])
    linhas = []
    for m, s in sr.groupby("municipio"):
        quad = "AA" if m in g["AA"] else "BB" if m in g["BB"] else ""
        linhas.append({
            "Município": m,
            "Sem resposta em": "; ".join(f"{i} {e} ({v or 'vazio'})" for i, e, v in zip(s["indicador"], s["edicao"], s["valor_original"])),
            "Em algum grupo": quad or ("poucos eventos" if m in alvo else "não"),
        })
    return pd.DataFrame(linhas)


def main() -> None:
    rede = pd.read_csv(REDE)
    g = grupos()
    t = tabela(rede, g)
    texto = f"""# Rede de atendimento nos municípios significativos do LISA

Pergunta: os municípios com zero ou poucos eventos e resultado significativo no LISA são desprovidos de serviço? Validação de medida, descritiva, sem teste de hipótese. Gerada por `src/analysis/rede_atendimento_cobertura.py` a partir de `data/processed/rede_atendimento_municipio.csv` (`src/fetch_rede_atendimento.py`). Grupos do LISA de Assunção e Reis, 2018-2025, semente 12345, 99.999 permutações, FDR sobre o p direcional.

Cada célula: municípios com o serviço / municípios que responderam (percentual); "s/r" conta os que não responderam ao quesito, fora do denominador. Os grupos de pares contam municípios, não pares.

## Cobertura por grupo

{markdown(t)}

¹ DEAM 2018 vem do bloco de política para mulheres (MPPM244, serviços especializados existentes), não do bloco de segurança pública de 2019 e 2023 (MSEG168, delegacias existentes no município). É outra pergunta, e outro informante.

² CREAS da MUNIC, autodeclarado. O Censo SUAS/MDS estava fora do ar quando a tabela foi gerada; ver o relatório.

## Pares com menos de 10 eventos, um a um

{markdown(detalhe(rede, g))}

## Mudança entre edições, nos 497

{markdown(concordancia(rede))}

## Municípios sem resposta em algum indicador

Nenhum município do RS recusou a MUNIC inteira nessas edições: a falta de resposta é por quesito.

{markdown(sem_resposta(rede, g))}
"""
    SAIDA.write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
