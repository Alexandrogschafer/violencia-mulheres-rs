"""Auditoria metodológica, item 5: reavalia a análise de sazonalidade do
litoral (razão verão/inverno), que hoje só existe como CSV ad hoc em
publicacoes/cap_geotecnologias/00_gestao/ -- sem nenhum código que a
reproduza (mesma lacuna que Tarefa 1 desta sessão já corrigiu para a
Tabela 2). Este módulo:

1. Explicita a definição de verão/inverno (dezembro-janeiro-fevereiro e
   junho-julho-agosto -- verão e inverno austral, já era o que os nomes de
   coluna do CSV ad hoc indicavam, mas em lugar nenhum estava dito em
   prosa).
2. Reproduz o grupo litoral (9 municípios) e o grupo controle (9
   municípios) já usados no CSV ad hoc -- ver GRUPO_LITORAL_ORIGINAL e
   GRUPO_CONTROLE_ORIGINAL abaixo. O critério de seleção dos 9 dentro dos
   21 municípios do COREDE Litoral NÃO estava documentado em nenhum lugar;
   foi reconstruído por engenharia reversa (comparando o CSV ad hoc contra
   outputs/tables/municipio_corede.csv e populacao_municipio_rs.csv) --
   ver docstring de GRUPO_LITORAL_ORIGINAL para o que essa reconstrução
   encontrou e o que ela NÃO consegue confirmar.
3. Roda um segundo grupo, baseado em regra clara e totalmente reprodutível
   (todo município do COREDE Litoral elegível pelo piso de 5.000 hab.,
   pareado por população mais próxima entre os NÃO-litorâneos elegíveis),
   como checagem de robustez independente da lista original.
4. Calcula incerteza da razão verão/inverno (intervalo de confiança pelo
   método delta em escala log, padrão para razão de duas contagens tipo
   Poisson) e verifica se o padrão se repete ano a ano (não só no
   acumulado 2018-2025).

5. Extensão pedida numa rodada seguinte: adota como GRUPO PRINCIPAL os 15
   municípios do COREDE Litoral acima do piso (não mais os 9 originais,
   que ficam só como registro histórico) e constrói um grupo de controle
   do mesmo tamanho por pareamento individual de população.

   Regra do pool de controle (POOL_CONTROLE_PRINCIPAL, ver função
   montar_grupo_principal): município do RS que (a) tem população
   residente MÉDIA 2018-2025 >= piso (5.000 hab. -- mesmo limiar do
   grupo litoral, e a mesma métrica de população usada no pareamento,
   não a população de um único ano de referência); (b) não pertence ao
   COREDE Litoral; (c) não tem frente oceânica -- excluídos
   explicitamente Rio Grande e São José do Norte, que ficam fora do
   COREDE Litoral mas têm litoral marítimo/lagunar direto (Rio Grande dá
   para a Lagoa dos Patos e o canal de acesso ao oceano; São José do
   Norte fica na restinga entre a Lagoa dos Patos e o Atlântico). Esta
   lista de exclusão foi fornecida explicitamente, não inferida por
   regra geográfica -- se houver outro município fora do COREDE Litoral
   com frente oceânica que não Rio Grande/São José do Norte, ele
   permanece no pool e este módulo não o filtra sozinho.

   Pareamento: para cada um dos 15 municípios do litoral, ordenados por
   população crescente, escolhe do pool o município ainda não usado com
   população média mais próxima (pareamento guloso, sem reposição -- um
   município do pool nunca entra em mais de um par). É determinístico
   (mesma população de entrada sempre produz o mesmo pareamento), não
   uma amostragem aleatória.

6. Extensão pedida numa rodada seguinte: para o grupo principal (15+15),
   resume a comparação litoral x controle numa única razão por categoria
   -- a razão entre a razão verão/inverno do litoral e a razão
   verão/inverno do controle ("razão das razões", R = R_litoral /
   R_controle). R > 1 indica que a concentração de casos no verão é
   proporcionalmente maior no litoral do que no controle; R = 1 indica
   nenhuma diferença entre os dois grupos nesse padrão sazonal.

   Erro-padrão (método delta em escala log, generalização do usado nas
   razões individuais em _razao_com_ic): sejam V_L, I_L, V_C, I_C os
   casos de verão/inverno do litoral (L) e do controle (C). Então

       log(R) = log(V_L) - log(I_L) - log(V_C) + log(I_C)
       SE(log R) = sqrt(1/V_L + 1/I_L + 1/V_C + 1/I_C)
       IC 95% = exp(log(R) ± 1.96 * SE(log R))

   Hipóteses assumidas (as mesmas do método delta em contagens tipo
   Poisson, agora com quatro termos em vez de dois):
   - V_L, I_L, V_C, I_C são contagens tipo Poisson, cada uma com
     variância aproximadamente igual à própria contagem (Var(log X) ≈
     1/X para X grande, por expansão de Taylor de primeira ordem --
     doença de precisão em contagens pequenas, ver abaixo);
   - as quatro contagens são mutuamente independentes: verão e inverno
     não se sobrepõem no tempo, e litoral e controle são conjuntos de
     municípios disjuntos por construção (pareamento sem reposição);
   - log(R) é aproximadamente normal (válido quando as quatro contagens
     não são muito pequenas -- para categorias raras como Feminicídio,
     que não entram em CATEGORIAS aqui, essa aproximação seria frágil);
   - não corrige para múltiplas comparações (uma razão por categoria,
     3 categorias) -- os IC devem ser lidos como individuais, não
     conjuntos.

Uso: python -m src.analysis.auditoria.sazonalidade_litoral
"""

from pathlib import Path

import numpy as np
import pandas as pd

TABLES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "outputs" / "tables"
SAIDA_DIR = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "publicacoes"
    / "cap_geotecnologias"
    / "00_gestao"
    / "auditoria"
)

ANO_INICIO, ANO_FIM = 2018, 2025
MESES_VERAO = [12, 1, 2]  # dezembro-janeiro-fevereiro (verão austral)
MESES_INVERNO = [6, 7, 8]  # junho-julho-agosto (inverno austral)
POP_MINIMA = 5000
CATEGORIAS = ["Ameaça", "Estupro", "Lesão Corporal"]

# Os 9 municípios usados no CSV ad hoc (tabela_apoio_sazonalidade_litoral_
# 2018_2025.csv) -- reconstruídos comparando esse arquivo contra
# municipio_corede.csv. São os 9 municípios de maior população dentre os
# 21 do COREDE Litoral que também estão entre praias/balneários -- mas
# essa reconstrução NÃO consegue confirmar a regra exata: dos 15
# municípios do COREDE Litoral acima do piso de 5.000 hab., Osório (48.999
# hab. em 2025, a 2ª maior população do COREDE) foi excluído do grupo
# original sem explicação registrada em nenhum lugar do repositório.
# Osório é sede administrativa/comercial regional, não um balneário -- uma
# hipótese razoável para a exclusão -- mas é uma hipótese, não um critério
# documentado. Ver montar_grupo_robustez() abaixo para uma versão com
# regra 100% explícita, calculada em paralelo como checagem, e
# montar_grupo_principal() para a versão adotada como grupo principal
# numa rodada seguinte (15+15, pareada por população média 2018-2025).
GRUPO_LITORAL_ORIGINAL = [
    "CIDREIRA", "TRAMANDAI", "IMBE", "CAPAO DA CANOA", "BALNEARIO PINHAL",
    "XANGRILA", "ARROIO DO SAL", "TORRES", "PALMARES DO SUL",
]
GRUPO_CONTROLE_ORIGINAL = [
    "CAPELA DE SANTANA", "CRISSIUMAL", "ESPUMOSO", "GETULIO VARGAS",
    "SERAFINA CORREA", "VERA CRUZ", "SAO LOURENCO DO SUL", "TAQUARA", "VACARIA",
]


def _populacao_2025() -> pd.Series:
    pop = pd.read_csv(TABLES_DIR / "populacao_municipio_rs.csv")
    return pop[pop["ano"] == 2025].set_index("municipio")["populacao"]


def montar_grupo_robustez() -> tuple[list[str], list[str]]:
    """Litoral = todo município do COREDE Litoral com população 2025 >=
    piso; controle = pareamento guloso pela população mais próxima entre
    os municípios do RS que NÃO são do COREDE Litoral e também atendem ao
    piso -- regra simples, sem escolha manual de quais municípios do
    COREDE entram."""
    pop = _populacao_2025()
    corede = pd.read_csv(TABLES_DIR / "municipio_corede.csv")
    litoral_corede = set(corede.loc[corede["corede"] == "Litoral", "municipio"])

    litoral = sorted(
        (m for m in litoral_corede if pop.get(m, 0) >= POP_MINIMA),
        key=lambda m: pop[m],
    )
    candidatos_controle = sorted(
        (m for m in pop.index if m not in litoral_corede and pop[m] >= POP_MINIMA),
        key=lambda m: pop[m],
    )

    controle, usados = [], set()
    for m in litoral:
        alvo = pop[m]
        melhor = min(
            (c for c in candidatos_controle if c not in usados),
            key=lambda c: abs(pop[c] - alvo),
        )
        controle.append(melhor)
        usados.add(melhor)

    return litoral, controle


# Municípios fora do COREDE Litoral com frente oceânica/lagunar direta,
# excluídos explicitamente do pool de controle -- lista fornecida, não
# inferida por regra geográfica automática (ver docstring do módulo).
MUNICIPIOS_FRENTE_OCEANICA_FORA_COREDE_LITORAL = ["RIO GRANDE", "SAO JOSE DO NORTE"]


def _populacao_media_2018_2025() -> pd.Series:
    """População residente média 2018-2025, por município -- média
    simples das 8 populações anuais (não pessoas-ano acumuladas: aqui o
    interesse é o porte típico do município no período, para parear
    litoral x controle, não um denominador de taxa)."""
    pop = pd.read_csv(TABLES_DIR / "populacao_municipio_rs.csv")
    pop = pop[(pop["ano"] >= ANO_INICIO) & (pop["ano"] <= ANO_FIM)]
    return pop.groupby("municipio")["populacao"].mean()


def montar_grupo_principal() -> tuple[list[str], list[str], pd.DataFrame]:
    """Grupo principal (extensão pedida numa rodada seguinte): os 15
    municípios do COREDE Litoral acima do piso (população média
    2018-2025 >= 5.000), pareados individualmente por população média
    2018-2025 com um município do pool de controle (fora do COREDE
    Litoral, acima do piso, sem frente oceânica -- ver
    MUNICIPIOS_FRENTE_OCEANICA_FORA_COREDE_LITORAL), sorteado sem
    reposição (pareamento guloso pela população mais próxima,
    determinístico, cada município do pool usado no máximo uma vez).

    Retorna (litoral, controle, tabela_de_pares) -- a terceira saída já
    pronta para gravar em CSV com a população média de cada par e a
    diferença entre elas.
    """
    media = _populacao_media_2018_2025()
    corede = pd.read_csv(TABLES_DIR / "municipio_corede.csv")
    litoral_corede = set(corede.loc[corede["corede"] == "Litoral", "municipio"])

    litoral = sorted(
        (m for m in litoral_corede if media.get(m, 0) >= POP_MINIMA),
        key=lambda m: media[m],
    )
    pool_controle = sorted(
        (
            m
            for m in media.index
            if m not in litoral_corede
            and m not in MUNICIPIOS_FRENTE_OCEANICA_FORA_COREDE_LITORAL
            and media[m] >= POP_MINIMA
        ),
        key=lambda m: media[m],
    )

    pares, usados = [], set()
    for m in litoral:
        alvo = media[m]
        melhor = min((c for c in pool_controle if c not in usados), key=lambda c: abs(media[c] - alvo))
        usados.add(melhor)
        pares.append(
            {
                "municipio_litoral": m,
                "populacao_media_litoral": round(alvo, 1),
                "municipio_controle": melhor,
                "populacao_media_controle": round(media[melhor], 1),
                "diferenca_populacao": round(abs(alvo - media[melhor]), 1),
            }
        )

    tabela_pares = pd.DataFrame(pares)
    controle = tabela_pares["municipio_controle"].tolist()
    return litoral, controle, tabela_pares


def carregar_mensal() -> pd.DataFrame:
    df = pd.read_csv(TABLES_DIR / "violencia_mensal_municipio.csv")
    return df[(df["ano"] >= ANO_INICIO) & (df["ano"] <= ANO_FIM)]


def _razao_com_ic(casos_verao: int, casos_inverno: int, confianca: float = 0.95) -> dict:
    """Razão verão/inverno com IC pelo método delta em escala log --
    SE(log razão) = sqrt(1/casos_verao + 1/casos_inverno), padrão para
    razão de duas contagens tipo Poisson independentes. Não definido se
    algum lado for 0."""
    if casos_verao == 0 or casos_inverno == 0:
        return {"razao": float("nan"), "ic_baixo": float("nan"), "ic_alto": float("nan")}
    from scipy import stats

    razao = casos_verao / casos_inverno
    erro_padrao_log = np.sqrt(1 / casos_verao + 1 / casos_inverno)
    z = stats.norm.ppf(1 - (1 - confianca) / 2)
    log_razao = np.log(razao)
    return {
        "razao": round(razao, 4),
        "ic_baixo": round(float(np.exp(log_razao - z * erro_padrao_log)), 4),
        "ic_alto": round(float(np.exp(log_razao + z * erro_padrao_log)), 4),
    }


def _razao_das_razoes_com_ic(
    casos_verao_litoral: int,
    casos_inverno_litoral: int,
    casos_verao_controle: int,
    casos_inverno_controle: int,
    confianca: float = 0.95,
) -> dict:
    """Razão entre a razão verão/inverno do litoral e a do controle (R =
    R_litoral / R_controle), com IC pelo método delta em escala log --
    SE(log R) = sqrt(1/V_L + 1/I_L + 1/V_C + 1/I_C), generalização de
    _razao_com_ic para quatro contagens tipo Poisson mutuamente
    independentes (fórmula e hipóteses documentadas no cabeçalho do
    módulo, item 6). Não definido se alguma das quatro contagens for 0."""
    contagens = (casos_verao_litoral, casos_inverno_litoral, casos_verao_controle, casos_inverno_controle)
    if any(c == 0 for c in contagens):
        return {
            "razao_litoral": float("nan"),
            "razao_controle": float("nan"),
            "razao_das_razoes": float("nan"),
            "ic_baixo": float("nan"),
            "ic_alto": float("nan"),
        }
    from scipy import stats

    razao_litoral = casos_verao_litoral / casos_inverno_litoral
    razao_controle = casos_verao_controle / casos_inverno_controle
    razao_das_razoes = razao_litoral / razao_controle
    erro_padrao_log = np.sqrt(sum(1 / c for c in contagens))
    z = stats.norm.ppf(1 - (1 - confianca) / 2)
    log_razao = np.log(razao_das_razoes)
    return {
        "razao_litoral": round(razao_litoral, 4),
        "razao_controle": round(razao_controle, 4),
        "razao_das_razoes": round(razao_das_razoes, 4),
        "ic_baixo": round(float(np.exp(log_razao - z * erro_padrao_log)), 4),
        "ic_alto": round(float(np.exp(log_razao + z * erro_padrao_log)), 4),
    }


def razao_das_razoes_grupo_principal(
    mensal: pd.DataFrame, litoral: list[str], controle: list[str]
) -> pd.DataFrame:
    """Para o grupo principal (15+15), uma linha por categoria com a razão
    das razões verão/inverno (litoral sobre controle) e seu IC 95% --
    ver _razao_das_razoes_com_ic e item 6 do cabeçalho do módulo."""
    grupo_litoral = mensal[mensal["municipio"].isin(litoral)]
    grupo_controle = mensal[mensal["municipio"].isin(controle)]
    linhas = []
    for tipo in CATEGORIAS:
        sub_l = grupo_litoral[grupo_litoral["tipo_crime"] == tipo]
        sub_c = grupo_controle[grupo_controle["tipo_crime"] == tipo]
        verao_l = int(sub_l[sub_l["mes"].isin(MESES_VERAO)]["casos"].sum())
        inverno_l = int(sub_l[sub_l["mes"].isin(MESES_INVERNO)]["casos"].sum())
        verao_c = int(sub_c[sub_c["mes"].isin(MESES_VERAO)]["casos"].sum())
        inverno_c = int(sub_c[sub_c["mes"].isin(MESES_INVERNO)]["casos"].sum())
        linha = {
            "tipo_crime": tipo,
            "casos_verao_litoral": verao_l,
            "casos_inverno_litoral": inverno_l,
            "casos_verao_controle": verao_c,
            "casos_inverno_controle": inverno_c,
        }
        linha.update(_razao_das_razoes_com_ic(verao_l, inverno_l, verao_c, inverno_c))
        linhas.append(linha)
    return pd.DataFrame(linhas)


def resumo_grupo(mensal: pd.DataFrame, municipios: list[str], rotulo: str) -> pd.DataFrame:
    linhas = []
    grupo = mensal[mensal["municipio"].isin(municipios)]
    for tipo in CATEGORIAS:
        sub = grupo[grupo["tipo_crime"] == tipo]
        verao = int(sub[sub["mes"].isin(MESES_VERAO)]["casos"].sum())
        inverno = int(sub[sub["mes"].isin(MESES_INVERNO)]["casos"].sum())
        linha = {"grupo": rotulo, "tipo_crime": tipo, "casos_verao": verao, "casos_inverno": inverno}
        linha.update(_razao_com_ic(verao, inverno))
        linhas.append(linha)
    return pd.DataFrame(linhas)


def resumo_ano_a_ano(mensal: pd.DataFrame, municipios: list[str], rotulo: str) -> pd.DataFrame:
    """Razão verão/inverno por ano civil -- o trimestre de verão de um ano
    (dez/jan/fev) atravessa a virada do ano; aqui "ano" é o ano de
    referência do registro na tabela mensal (dezembro do ano N conta como
    verão do ano N, não do N+1) -- suficiente para checar consistência
    ano a ano, não pretende isolar o verão calendário completo."""
    linhas = []
    grupo = mensal[mensal["municipio"].isin(municipios)]
    for tipo in CATEGORIAS:
        for ano, sub_ano in grupo[grupo["tipo_crime"] == tipo].groupby("ano"):
            verao = int(sub_ano[sub_ano["mes"].isin(MESES_VERAO)]["casos"].sum())
            inverno = int(sub_ano[sub_ano["mes"].isin(MESES_INVERNO)]["casos"].sum())
            razao = round(verao / inverno, 4) if inverno else float("nan")
            linhas.append(
                {"grupo": rotulo, "tipo_crime": tipo, "ano": int(ano), "casos_verao": verao,
                 "casos_inverno": inverno, "razao": razao}
            )
    return pd.DataFrame(linhas)


def pct_janeiro(mensal: pd.DataFrame, municipios: list[str], rotulo: str, tipo_crime: str = "Lesão Corporal") -> dict:
    """Percentual que janeiro representa do total de registros anuais
    (soma 2018-2025, não média de percentuais anuais) -- mesma lógica de
    soma-antes-de-dividir do resto do módulo, para não dar peso igual a
    anos de volume bem diferente."""
    grupo = mensal[(mensal["municipio"].isin(municipios)) & (mensal["tipo_crime"] == tipo_crime)]
    total = int(grupo["casos"].sum())
    janeiro = int(grupo[grupo["mes"] == 1]["casos"].sum())
    return {
        "grupo": rotulo,
        "tipo_crime": tipo_crime,
        "casos_janeiro": janeiro,
        "casos_total_ano": total,
        "pct_janeiro": round(100 * janeiro / total, 2) if total else float("nan"),
    }


def main() -> None:
    mensal = carregar_mensal()
    SAIDA_DIR.mkdir(parents=True, exist_ok=True)

    litoral_robustez, controle_robustez = montar_grupo_robustez()
    print(f"Grupo litoral (regra: COREDE Litoral, piso {POP_MINIMA}): {len(litoral_robustez)} municípios")
    print(f"  {litoral_robustez}")
    print(f"Grupo controle pareado (robustez): {len(controle_robustez)} municípios")
    print(f"  {controle_robustez}\n")

    pd.set_option("display.width", 200)

    print("=== Razão verão/inverno acumulada 2018-2025, com IC 95% (grupo original, 9+9) ===")
    resumo_original = pd.concat([
        resumo_grupo(mensal, GRUPO_LITORAL_ORIGINAL, "litoral_original"),
        resumo_grupo(mensal, GRUPO_CONTROLE_ORIGINAL, "controle_original"),
        resumo_grupo(mensal, list(mensal["municipio"].unique()), "estado"),
    ], ignore_index=True)
    print(resumo_original.to_string(index=False))
    resumo_original.to_csv(SAIDA_DIR / "sazonalidade_razao_original_com_ic.csv", index=False)

    print("\n=== Razão verão/inverno acumulada 2018-2025, com IC 95% (grupo de robustez, regra explícita) ===")
    resumo_robustez = pd.concat([
        resumo_grupo(mensal, litoral_robustez, "litoral_robustez"),
        resumo_grupo(mensal, controle_robustez, "controle_robustez"),
    ], ignore_index=True)
    print(resumo_robustez.to_string(index=False))
    resumo_robustez.to_csv(SAIDA_DIR / "sazonalidade_razao_robustez_com_ic.csv", index=False)

    print("\n=== Razão verão/inverno ano a ano (grupo original) -- checagem de consistência ===")
    ano_a_ano = pd.concat([
        resumo_ano_a_ano(mensal, GRUPO_LITORAL_ORIGINAL, "litoral_original"),
        resumo_ano_a_ano(mensal, GRUPO_CONTROLE_ORIGINAL, "controle_original"),
    ], ignore_index=True)
    print(ano_a_ano.to_string(index=False))
    ano_a_ano.to_csv(SAIDA_DIR / "sazonalidade_ano_a_ano.csv", index=False)

    print("\n=== Em quantos dos 8 anos o litoral supera o controle na razão verão/inverno? ===")
    pivot = ano_a_ano.pivot_table(index=["tipo_crime", "ano"], columns="grupo", values="razao")
    pivot["litoral_maior"] = pivot["litoral_original"] > pivot["controle_original"]
    resumo_consistencia = pivot.groupby("tipo_crime")["litoral_maior"].agg(["sum", "count"])
    resumo_consistencia.columns = ["anos_litoral_maior", "anos_totais"]
    print(resumo_consistencia.to_string())
    resumo_consistencia.to_csv(SAIDA_DIR / "sazonalidade_consistencia_anual.csv")

    # --- Extensão: grupo principal (15+15, pareado por população média
    # 2018-2025, pool de controle sem frente oceânica) ---
    litoral_principal, controle_principal, tabela_pares = montar_grupo_principal()
    caminho_pares = SAIDA_DIR / "sazonalidade_pares_grupo_principal.csv"
    tabela_pares.to_csv(caminho_pares, index=False)
    print(f"\n=== Grupo principal (15 municípios do COREDE Litoral acima do piso, pareados por população média 2018-2025) ===")
    print(f"Pares salvos em {caminho_pares}\n")
    print(tabela_pares.to_string(index=False))

    print("\n=== Razão verão/inverno acumulada 2018-2025, com IC 95% (grupo principal, 15+15) ===")
    resumo_principal = pd.concat([
        resumo_grupo(mensal, litoral_principal, "litoral_principal"),
        resumo_grupo(mensal, controle_principal, "controle_principal"),
    ], ignore_index=True)
    print(resumo_principal.to_string(index=False))
    resumo_principal.to_csv(SAIDA_DIR / "sazonalidade_razao_principal_com_ic.csv", index=False)

    print("\n=== Percentual de janeiro no total anual de Lesão Corporal (grupo principal) ===")
    pct_jan = pd.DataFrame([
        pct_janeiro(mensal, litoral_principal, "litoral_principal"),
        pct_janeiro(mensal, controle_principal, "controle_principal"),
    ])
    print(pct_jan.to_string(index=False))
    pct_jan.to_csv(SAIDA_DIR / "sazonalidade_pct_janeiro_lesao_corporal.csv", index=False)

    print("\n=== Razão das razões verão/inverno (litoral sobre controle), grupo principal 15+15, com IC 95% ===")
    razao_das_razoes = razao_das_razoes_grupo_principal(mensal, litoral_principal, controle_principal)
    print(razao_das_razoes.to_string(index=False))
    caminho_razao_das_razoes = TABLES_DIR / "sazonalidade_razao_das_razoes_grupo_principal.csv"
    razao_das_razoes.to_csv(caminho_razao_das_razoes, index=False)
    print(f"Gravado em {caminho_razao_das_razoes}")


if __name__ == "__main__":
    main()
