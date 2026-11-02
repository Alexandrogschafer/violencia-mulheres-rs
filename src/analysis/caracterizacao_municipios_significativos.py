"""Caracterização dos municípios significativos no LISA de Assunção e Reis.

Semente 12345, 99.999 permutações, FDR sobre o p direcional, quatro desfechos com LISA.
Só usa dados já presentes no repositório. Quadrante do município: é único nos 59, e o
script interrompe a execução se deixar de ser.

Sem dado de urbanização no repositório, a densidade demográfica entra como informação
própria, não como aproximação do grau de urbanização. Área em projeção cônica de Albers.

Uso: python -m src.analysis.caracterizacao_municipios_significativos
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import hypergeom, mannwhitneyu

from src.analysis.autocorrelacao_espacial import montar_pesos_espaciais
from src.analysis.mapa_choropleth import _populacao_referencia, montar_geodataframe
from src.analysis.moran_lisa_assuncao_reis import (
    ANO_FIM,
    ANO_INICIO,
    PISO_POPULACIONAL,
    SEED,
    TIPOS_MORAN,
)

TABLES_DIR = Path(__file__).resolve().parent.parent.parent / "outputs" / "tables"
SAIDA = TABLES_DIR / "caracterizacao_municipios_significativos.md"
ESTABILIDADE = TABLES_DIR / "estabilidade_lisa_sementes.csv"
PERMUTACOES = 99_999
N_ESPERADO = 59
QUADRANTES = ["AA", "BB", "AB", "BA"]
ALBERS_RS = "+proj=aea +lat_1=-27 +lat_2=-33 +lat_0=-30 +lon_0=-53 +datum=WGS84 +units=m"
FAIXAS = [(0, 3000), (3000, 5000), (5000, 6000), (6000, 7500), (7500, 10000), (10000, 50000), (50000, np.inf)]
ROTULOS_FAIXA = ["< 3 mil", "3 a 5 mil", "5 a 6 mil", "6 a 7,5 mil", "7,5 a 10 mil", "10 a 50 mil", "≥ 50 mil"]
BLOCOS = {
    "Três do Litoral em AA, os da sobreposição": ["CAPIVARI DO SUL", "OSORIO", "TRAMANDAI"],
    "Quatro em BB da sobreposição Ameaça + Lesão Corporal": [
        "BOA VISTA DO SUL",
        "LINHA NOVA",
        "PICADA CAFE",
        "PRESIDENTE LUCENA",
    ],
}


def br(x: float, casas: int = 0) -> str:
    return f"{x:,.{casas}f}".replace(",", " ").replace(".", ",").replace(" ", ".")


def markdown(df: pd.DataFrame) -> str:
    linhas = [list(df.columns), ["---"] * df.shape[1], *df.astype(str).to_numpy().tolist()]
    return "\n".join("| " + " | ".join(map(str, linha)) + " |" for linha in linhas)


def componentes(nomes: list[str], vizinhos: dict[str, set]) -> list[list[str]]:
    restantes, saida = set(nomes), []
    while restantes:
        pilha, grupo = [restantes.pop()], []
        while pilha:
            atual = pilha.pop()
            grupo.append(atual)
            ligados = vizinhos[atual] & restantes
            restantes -= ligados
            pilha.extend(ligados)
        saida.append(sorted(grupo))
    return sorted(saida, key=lambda g: (-len(g), g))


def carregar() -> dict:
    t = pd.read_csv(ESTABILIDADE)
    alto = t[t["permutacoes"] == PERMUTACOES]
    sig = alto[(alto["semente"] == SEED) & alto["sobrevive_fdr"]]
    if sig["municipio"].nunique() != N_ESPERADO or sig.groupby("municipio")["categoria"].nunique().max() != 1:
        raise ValueError("Conjunto significativo diferente do esperado.")
    estabilidade = alto.groupby(["tipo_crime", "municipio"])["sobrevive_fdr"].sum()

    casos = {}
    for tipo in TIPOS_MORAN:
        gdf = montar_geodataframe(tipo, ANO_INICIO, ANO_FIM)
        casos[tipo] = gdf.set_index("municipio")["casos_total"].astype(int)
        taxa = gdf.set_index("municipio")
        casos[f"pessoas_ano_{tipo}"] = taxa["populacao_pessoas_ano"]
    casos_df = pd.DataFrame({k: casos[k] for k in TIPOS_MORAN})
    pessoas_ano = casos[f"pessoas_ano_{TIPOS_MORAN[0]}"]

    w = montar_pesos_espaciais(gdf)
    nomes = gdf["municipio"].tolist()
    vizinhos = {nomes[i]: {nomes[j] for j in w.neighbors[i]} for i in range(len(nomes))}
    area = gdf.to_crs(ALBERS_RS).set_index("municipio").geometry.area / 1e6

    pop = _populacao_referencia(ANO_FIM)
    corede = pd.read_csv(TABLES_DIR / "municipio_corede.csv").set_index("municipio")
    regioes = pd.read_csv(TABLES_DIR / "municipio_regioes_ibge.csv").set_index("municipio")
    return dict(
        sig=sig,
        estabilidade=estabilidade,
        casos=casos_df,
        pessoas_ano=pessoas_ano,
        vizinhos=vizinhos,
        area=area,
        pop=pop,
        corede=corede,
        regioes=regioes,
        quadrante=sig.groupby("municipio")["categoria"].first(),
    )


def descrever_pop(rotulo: str, p: pd.Series) -> dict:
    return {
        "Grupo": rotulo,
        "n": len(p),
        "Mín.": br(p.min()),
        "Q1": br(p.quantile(0.25)),
        "Mediana": br(p.median()),
        "Q3": br(p.quantile(0.75)),
        "Máx.": br(p.max()),
        "Abaixo do piso": f"{int((p < PISO_POPULACIONAL).sum())} ({br(100 * (p < PISO_POPULACIONAL).mean(), 1)}%)",
    }


def faixas(d: dict) -> pd.DataFrame:
    grupos = {q: d["pop"][d["quadrante"].index[d["quadrante"] == q]] for q in ["AA", "BB"]}
    grupos["497"] = d["pop"]
    linhas = []
    for rotulo, (a, b) in zip(ROTULOS_FAIXA, FAIXAS):
        linha = {"Faixa de população": rotulo}
        for nome, p in grupos.items():
            n = int(((p >= a) & (p < b)).sum())
            linha[nome] = f"{n} ({br(100 * n / len(p), 1)}%)"
        linhas.append(linha)
    return pd.DataFrame(linhas)


def faixa_acima_piso(d: dict) -> pd.DataFrame:
    """Probabilidade hipergeométrica de ter tantos municípios na faixa ou mais, sorteando do conjunto dos 497."""
    linhas = []
    for a, b in [(5000, 6000), (5000, 7500), (5000, 10000)]:
        for q in ["AA", "BB"]:
            p = d["pop"][d["quadrante"].index[d["quadrante"] == q]]
            n, total = int(((p >= a) & (p < b)).sum()), int(((d["pop"] >= a) & (d["pop"] < b)).sum())
            linhas.append(
                {
                    "Faixa": f"{br(a)} a {br(b - 1)}",
                    "Quadrante": q,
                    "No quadrante": f"{n}/{len(p)}",
                    "Nos 497": f"{total}/497",
                    "Esperado": br(len(p) * total / len(d["pop"]), 1),
                    "P(tantos ou mais)": br(hypergeom.sf(n - 1, len(d["pop"]), total, len(p)), 3),
                }
            )
    return pd.DataFrame(linhas)


def pares(d: dict) -> pd.DataFrame:
    """Par município-desfecho significativo: eventos, taxa e posição frente ao piso."""
    s = d["sig"]
    linhas = []
    for _, r in s.iterrows():
        eventos = int(d["casos"].loc[r["municipio"], r["tipo_crime"]])
        pa = d["pessoas_ano"][r["municipio"]]
        linhas.append(
            {
                "tipo": r["tipo_crime"],
                "municipio": r["municipio"],
                "q": r["categoria"],
                "eventos": eventos,
                "taxa": eventos / pa * 100_000,
                "pop": int(d["pop"][r["municipio"]]),
            }
        )
    return pd.DataFrame(linhas)


def eventos_por_par(d: dict) -> pd.DataFrame:
    p = pares(d)
    linhas = []
    for (tipo, q), g in p.groupby(["tipo", "q"]):
        linhas.append(
            {
                "Desfecho": tipo,
                "Quadrante": q,
                "Pares": len(g),
                "Abaixo do piso": int((g["pop"] < PISO_POPULACIONAL).sum()),
                "Eventos, mín.–máx.": f"{g['eventos'].min()}–{g['eventos'].max()}",
                "Mediana de eventos": br(g["eventos"].median(), 1),
                "Pares com zero evento": int((g["eventos"] == 0).sum()),
                "Pares com até 5 eventos": int((g["eventos"] <= 5).sum()),
            }
        )
    return pd.DataFrame(linhas)


def tabela_municipios(d: dict) -> pd.DataFrame:
    s = d["sig"]
    linhas = []
    ordem = sorted(d["quadrante"].index, key=lambda m: (QUADRANTES.index(d["quadrante"][m]), -d["pop"][m]))
    for m in ordem:
        p = int(d["pop"][m])
        cel = [
            f"{r.tipo_crime} ({int(d['estabilidade'][r.tipo_crime, m])}/20)"
            for r in s[s["municipio"] == m].itertuples()
        ]
        linhas.append(
            {
                "Município": m,
                "Quadrante": d["quadrante"][m],
                "Significativo em": "; ".join(cel),
                "População 2025": br(p),
                "Frente ao piso": f"{'abaixo' if p < PISO_POPULACIONAL else 'acima'} ({p - PISO_POPULACIONAL:+,})".replace(",", "."),
                **{t: int(d["casos"].loc[m, t]) for t in TIPOS_MORAN},
            }
        )
    return pd.DataFrame(linhas)


def tabela_territorio(d: dict) -> pd.DataFrame:
    ids = {}
    for q in QUADRANTES:
        nomes = list(d["quadrante"].index[d["quadrante"] == q])
        for i, grupo in enumerate(componentes(nomes, d["vizinhos"]), start=1):
            for m in grupo:
                ids[m] = f"{q}-{i} ({len(grupo)})"
    linhas = []
    ordem = sorted(d["quadrante"].index, key=lambda m: (QUADRANTES.index(d["quadrante"][m]), ids[m], m))
    for m in ordem:
        linhas.append(
            {
                "Município": m,
                "Quadrante": d["quadrante"][m],
                "COREDE": d["corede"].loc[m, "corede"],
                "Região funcional": d["corede"].loc[m, "regiao_funcional"],
                "Região imediata": d["regioes"].loc[m, "regiao_imediata"],
                "Região intermediária": d["regioes"].loc[m, "regiao_intermediaria"],
                "Densidade (hab./km²)": br(d["pop"][m] / d["area"][m], 1),
                "Bloco do quadrante (tamanho)": ids[m],
            }
        )
    return pd.DataFrame(linhas)


def resumo_blocos(d: dict) -> pd.DataFrame:
    linhas = []
    for q in QUADRANTES:
        nomes = list(d["quadrante"].index[d["quadrante"] == q])
        grupos = componentes(nomes, d["vizinhos"])
        tamanhos = [len(g) for g in grupos]
        linhas.append(
            {
                "Quadrante": q,
                "Municípios": len(nomes),
                "Blocos contíguos": len(grupos),
                "Tamanhos": ", ".join(map(str, tamanhos)),
                "Isolados": sum(t == 1 for t in tamanhos),
            }
        )
    return pd.DataFrame(linhas)


def blocos_especificos(d: dict) -> pd.DataFrame:
    casos = dict(BLOCOS)
    q = d["quadrante"]
    c = d["corede"]["corede"]
    casos["Todos os AA do COREDE Litoral"] = sorted(m for m in q.index[q == "AA"] if c[m] == "Litoral")
    casos["Todos os BB do COREDE Serra"] = sorted(m for m in q.index[q == "BB"] if c[m] == "Serra")
    linhas = []
    for rotulo, nomes in casos.items():
        ligacoes = [f"{a}–{b}" for i, a in enumerate(nomes) for b in nomes[i + 1 :] if b in d["vizinhos"][a]]
        grupos = componentes(nomes, d["vizinhos"])
        linhas.append(
            {
                "Conjunto": rotulo,
                "Municípios e COREDE": "; ".join(f"{m} ({c[m]})" for m in nomes),
                "Pares vizinhos": ", ".join(ligacoes) or "nenhum",
                "Bloco único": "sim" if len(grupos) == 1 else "não",
                "Partes": " / ".join(", ".join(g) for g in grupos),
            }
        )
    return pd.DataFrame(linhas)


REDE = pd.DataFrame(
    [
        {"Item": "Organismo de políticas para mulheres", "Fonte esperada": "MUNIC/IBGE"},
        {"Item": "Delegacia especializada", "Fonte esperada": "MUNIC/IBGE ou registro estadual"},
        {"Item": "Conselho de direitos", "Fonte esperada": "MUNIC/IBGE"},
        {"Item": "Casa abrigo", "Fonte esperada": "MUNIC/IBGE"},
        {"Item": "CRAS", "Fonte esperada": "Censo SUAS"},
        {"Item": "CREAS", "Fonte esperada": "Censo SUAS"},
    ]
).assign(**{"No repositório": "não", "Processado": "não"})


def main() -> None:
    d = carregar()
    q = d["quadrante"]
    desc = pd.DataFrame(
        [descrever_pop(g, d["pop"][q.index[q == g]]) for g in QUADRANTES]
        + [descrever_pop("Os 59", d["pop"][q.index]), descrever_pop("Os 497", d["pop"])]
    )
    aa, bb = d["pop"][q.index[q == "AA"]], d["pop"][q.index[q == "BB"]]
    mw = mannwhitneyu(aa, bb, alternative="two-sided")
    p = pares(d)
    abaixo = int((d["pop"][q.index] < PISO_POPULACIONAL).sum())
    pares_abaixo = int((p["pop"] < PISO_POPULACIONAL).sum())
    faixa_bb = int(((bb >= 5000) & (bb < 7500)).sum())
    faixa_aa = int(((aa >= 5000) & (aa < 7500)).sum())
    frageis = p[p["eventos"] <= 5].sort_values(["eventos", "tipo", "municipio"]).assign(
        sementes=lambda g: [int(d["estabilidade"][t, m]) for t, m in zip(g["tipo"], g["municipio"])]
    )
    frageis = pd.DataFrame(
        {
            "Município": frageis["municipio"],
            "Desfecho": frageis["tipo"],
            "Quadrante": frageis["q"],
            "Eventos": frageis["eventos"],
            "População 2025": frageis["pop"].map(br),
            "Sementes": frageis["sementes"].map(lambda n: f"{n}/20"),
        }
    )
    texto = "\n\n".join(
        [
            "# Caracterização dos municípios significativos no LISA",
            f"{N_ESPERADO} municípios significativos em ao menos um de quatro desfechos, {ANO_INICIO}-{ANO_FIM}, semente {SEED}, "
            f"{br(PERMUTACOES)} permutações, FDR sobre o p direcional. Piso populacional do projeto: {br(PISO_POPULACIONAL)} habitantes, "
            f"avaliado na população de {ANO_FIM}. Gerada por `src/analysis/caracterizacao_municipios_significativos.py`.",
            "## 1. Verificação de método",
            f"**O LISA foi calculado sobre os 497 municípios, sem aplicar o piso.** {abaixo} dos {N_ESPERADO} municípios e "
            f"{pares_abaixo} dos {len(p)} pares município-desfecho estão abaixo dele. O piso existe no projeto para marcar "
            "taxas instáveis nos mapas, e esses municípios são tratados lá como instáveis.",
            f"**BB está mais concentrado logo acima do piso do que o conjunto dos 497: {faixa_bb}/24 entre 5.000 e 7.499 habitantes, "
            f"contra {br(24 * 75 / 497, 1)} esperados; AA tem {faixa_aa}/28, contra {br(28 * 75 / 497, 1)}.** Como o LISA não usa o piso, "
            "ele não pode ter selecionado esses municípios. Mas a faixa foi escolhida depois de ver os dados, o excesso enfraquece "
            f"com outros cortes, e {int((bb < PISO_POPULACIONAL).sum())}/24 dos BB estão abaixo do piso, proporção próxima à dos 497 (46,5%). "
            "É uma questão de método a declarar e investigar, não um achado.",
            "**Há pares significativos sustentados por pouquíssimos eventos, e eles são a fragilidade mais direta:** ver a lista abaixo.",
            "### Distribuição de população, 2025",
            markdown(desc),
            f"AA contra BB, Mann-Whitney bilateral: U = {br(mw.statistic, 1)}, p = {br(mw.pvalue, 3)}. Descritivo.",
            "### Por faixa",
            markdown(faixas(d)),
            "### Logo acima do piso, frente ao que se esperaria dos 497",
            "As probabilidades são descritivas: as faixas foram escolhidas depois de ver os dados, e os municípios não são independentes.",
            markdown(faixa_acima_piso(d)),
            "### Eventos no desfecho em que o par é significativo",
            markdown(eventos_por_par(d)),
            "### Pares significativos com até 5 eventos",
            markdown(frageis),
            "### Os 59 municípios",
            "Eventos no período inteiro. Entre parênteses, as sementes em que o par é significativo, de 20.",
            markdown(tabela_municipios(d)),
            "## 2. Caracterização territorial",
            "**O repositório não tem grau de urbanização.** A densidade abaixo é informação própria, não substituto.",
            "### Contiguidade dentro de cada quadrante",
            "Contiguidade de rainha, a mesma matriz do teste. Municípios vizinhos partilham vizinhos no cálculo do I local, "
            "de modo que a contiguidade dos significativos é em parte esperada e não é evidência independente.",
            markdown(resumo_blocos(d)),
            "### Blocos verificados",
            markdown(blocos_especificos(d)),
            "### Território dos 59",
            markdown(tabela_territorio(d)),
            "## 3. Rede de atendimento",
            "**Os dados não estão no repositório, e nenhuma comparação de cobertura foi feita.** A busca cobriu nomes de "
            "arquivos, conteúdo textual e colunas das tabelas de `data/` e `outputs/`, os JSON do portal e o histórico do Git.",
            markdown(REDE),
            "Para comparar, faltam: obter as bases, escolher as edições, definir cada indicador e cruzar por "
            "`codigo_ibge` com `outputs/tables/municipio_codigo_ibge.csv`, que já cobre os 497.",
        ]
    )
    SAIDA.write_text(texto + "\n", encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
