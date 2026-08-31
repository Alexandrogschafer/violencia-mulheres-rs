"""Formaliza o cálculo da Tabela 2 do capítulo (amplitude das taxas por
nível de agregação -- município, COREDE, região geográfica intermediária,
Seção 5.5 de 02_texto/05_resultados.md).

Até esta sessão, esse cálculo só existia como o CSV já commitado em
publicacoes/cap_geotecnologias/00_gestao/tabela_apoio_regional_corede_regiao_2018_2025.csv
-- rodado uma vez, ad hoc, fora de qualquer arquivo versionado (achado do
diagnóstico da sessão anterior). Este script reproduz esse cálculo,
byte a byte (ver main() e a comparação ao final), fechando essa lacuna de
reprodutibilidade num capítulo cujo argumento central é justamente sobre
como o nível de agregação muda o resultado -- se o próprio cálculo que
sustenta esse argumento não é reprodutível, o argumento fica comprometido.

Piso populacional aplicado ANTES da agregação regional (não depois): um
COREDE ou região intermediária vira soma só dos municípios que já
apareceriam individualmente no nível municipal (POP_MINIMA_PADRAO=5000,
mesmo piso das figuras do capítulo e dos notebooks). A alternativa --
somar todos os municípios do COREDE, piso ou não, e só aplicar o piso ao
resultado agregado -- misturaria, no mesmo número, municípios que o
leitor nunca vê no mapa municipal (por estarem abaixo do piso lá) com
municípios que vê. Os três níveis deixariam de ser comparáveis: a mesma
pessoa/população apareceria em alguns níveis e não em outros. Aplicar o
piso primeiro garante que os três níveis são somas do mesmo conjunto de
municípios elegíveis -- só a fronteira de agregação muda, nunca a base de
dados, que é exatamente o que a Tabela 2 precisa demonstrar (MAUP: mesmos
casos, mesma população, resultado diferente só pela fronteira).

Uso: python -m src.analysis.tabela_agregacao_regional
"""

from pathlib import Path

import pandas as pd

from src.analysis.mapa_choropleth import _populacao_referencia, carregar_taxa_periodo

TABLES_DIR = Path(__file__).resolve().parent.parent.parent / "outputs" / "tables"
SAIDA_CSV = (
    Path(__file__).resolve().parent.parent.parent
    / "publicacoes"
    / "cap_geotecnologias"
    / "00_gestao"
    / "tabela_apoio_regional_corede_regiao_2018_2025.csv"
)

# Mesmo recorte documentado em src/analysis/tendencia.py e já usado nas
# figuras do capítulo (src/analysis/figuras_capitulo.py).
ANO_INICIO = 2018
ANO_FIM = 2025

# Mesma ordem do CSV já commitado -- preservada aqui para que a saída
# reproduza a ordem das linhas exatamente, não só os valores.
CATEGORIAS = ["Ameaça", "Estupro", "Lesão Corporal"]

POP_MINIMA_PADRAO = 5000  # mesmo piso de figuras_capitulo.py e dos notebooks


def carregar_mapeamento_corede() -> pd.DataFrame:
    """municipio -> corede, regiao_funcional (src/fetch_coredes.py)."""
    return pd.read_csv(TABLES_DIR / "municipio_corede.csv")[["municipio", "corede", "regiao_funcional"]]


def carregar_mapeamento_regioes_ibge() -> pd.DataFrame:
    """municipio -> regiao_intermediaria (src/fetch_regioes_ibge.py)."""
    return pd.read_csv(TABLES_DIR / "municipio_regioes_ibge.csv")[["municipio", "regiao_intermediaria"]]


def calcular_taxas_municipio(
    tipo_crime: str,
    ano_inicio: int = ANO_INICIO,
    ano_fim: int = ANO_FIM,
    pop_minima: int = POP_MINIMA_PADRAO,
) -> pd.DataFrame:
    """Taxa por município no período, com COREDE, região intermediária e a
    flag de elegibilidade (piso) anexadas -- base para os três níveis
    (o nível "município" é esta tabela filtrada por elegivel; COREDE e
    região intermediária agregam a partir dela). taxa_por_100mil_hab NÃO
    é arredondada aqui -- mesma convenção de carregar_taxa_periodo e de
    mapa_choropleth.py (só a saída CSV que reproduz o arquivo já commitado
    arredonda, para bater exatamente com o que já está publicado).
    """
    pop_ref = _populacao_referencia(ano_fim).rename("populacao_referencia")
    base = carregar_taxa_periodo(tipo_crime, ano_inicio, ano_fim)
    base = base.merge(pop_ref, left_on="municipio", right_index=True, how="left")
    base = base.merge(carregar_mapeamento_corede(), on="municipio", how="left")
    base = base.merge(carregar_mapeamento_regioes_ibge(), on="municipio", how="left")
    base["elegivel"] = base["populacao_referencia"] >= pop_minima
    return base


def calcular_agregacao_regional(
    tipo_crime: str,
    nivel: str,
    ano_inicio: int = ANO_INICIO,
    ano_fim: int = ANO_FIM,
    pop_minima: int = POP_MINIMA_PADRAO,
) -> pd.DataFrame:
    """Réplica exata da lógica ad hoc original para nivel em {"corede",
    "regiao_intermediaria"}: filtra elegíveis (piso), agrega, arredonda a
    taxa para 2 casas ANTES de ordenar (mesma ordem de operações do
    cálculo original -- necessário para que "posicao" e a ordem das linhas
    batam exatamente com o CSV já commitado).
    """
    if nivel not in {"corede", "regiao_intermediaria"}:
        raise ValueError(f"nivel inválido para agregação regional: {nivel!r}")

    base = calcular_taxas_municipio(tipo_crime, ano_inicio, ano_fim, pop_minima)
    elegiveis = base[base["elegivel"]].copy()

    agregado = (
        elegiveis.groupby(nivel)
        .agg(
            n_municipios_elegiveis=("municipio", "count"),
            casos_total=("casos_total", "sum"),
            populacao_pessoas_ano=("populacao_pessoas_ano", "sum"),
        )
        .reset_index()
        .rename(columns={nivel: "regiao"})
    )
    agregado["taxa_por_100mil_hab"] = (
        agregado["casos_total"] / agregado["populacao_pessoas_ano"] * 100_000
    ).round(2)
    agregado = agregado.sort_values("taxa_por_100mil_hab", ascending=False).reset_index(drop=True)
    agregado["posicao"] = agregado.index + 1
    agregado["tipo_crime"] = tipo_crime
    agregado["nivel_agregacao"] = nivel
    return agregado[
        ["tipo_crime", "nivel_agregacao", "posicao", "regiao", "n_municipios_elegiveis", "casos_total", "taxa_por_100mil_hab"]
    ]


def gerar_csv_regional(pop_minima: int = POP_MINIMA_PADRAO) -> pd.DataFrame:
    """Monta o CSV de COREDE + região intermediária, mesma estrutura e
    ordem do arquivo já commitado (nunca inclui o nível "município" -- ele
    não está no arquivo original; ver docstring do módulo)."""
    linhas = []
    for tipo in CATEGORIAS:
        for nivel in ("corede", "regiao_intermediaria"):
            linhas.append(calcular_agregacao_regional(tipo, nivel, pop_minima=pop_minima))
    return pd.concat(linhas, ignore_index=True)


def _resumo_nivel(tipo_crime: str, nivel: str, pop_minima: int = POP_MINIMA_PADRAO) -> dict:
    """n de unidades, mínimo, máximo e razão máx/mín da taxa, para um
    nível e categoria. Nível "municipio" usa a taxa não arredondada
    (precisão plena, mesma usada nos cortes de quantis de mapa_choropleth.
    py); "corede"/"regiao_intermediaria" usam a taxa já arredondada a 2
    casas da agregação (a mesma que consta na Tabela 2 do capítulo)."""
    if nivel == "municipio":
        base = calcular_taxas_municipio(tipo_crime, pop_minima=pop_minima)
        valores = base.loc[base["elegivel"], "taxa_por_100mil_hab"]
    else:
        valores = calcular_agregacao_regional(tipo_crime, nivel, pop_minima=pop_minima)["taxa_por_100mil_hab"]
    minimo, maximo = float(valores.min()), float(valores.max())
    return {
        "tipo_crime": tipo_crime,
        "nivel": nivel,
        "n_unidades": int(valores.shape[0]),
        "minimo": minimo,
        "maximo": maximo,
        "razao": maximo / minimo if minimo else float("inf"),
    }


def main() -> None:
    print(f"=== Tabela 2 -- amplitude das taxas por nível de agregação ({ANO_INICIO}-{ANO_FIM}) ===\n")
    for tipo in CATEGORIAS:
        print(f"{tipo}:")
        for nivel in ("municipio", "corede", "regiao_intermediaria"):
            r = _resumo_nivel(tipo, nivel)
            print(
                f"    {nivel:22s} n={r['n_unidades']:4d}  "
                f"mínimo={r['minimo']:.4f}  máximo={r['maximo']:.4f}  razão={r['razao']:.4f}"
            )
        print()

    tabela_regional = gerar_csv_regional()
    SAIDA_CSV.parent.mkdir(parents=True, exist_ok=True)
    caminho_temp = SAIDA_CSV.with_suffix(".novo.csv")
    tabela_regional.to_csv(caminho_temp, index=False)

    if SAIDA_CSV.exists():
        conteudo_novo = caminho_temp.read_bytes()
        conteudo_antigo = SAIDA_CSV.read_bytes()
        if conteudo_novo == conteudo_antigo:
            print(f"OK -- {caminho_temp.name} é byte a byte idêntico a {SAIDA_CSV.name}. Reescrevendo no lugar original.")
            caminho_temp.replace(SAIDA_CSV)
        else:
            print(
                f"DIVERGÊNCIA -- {caminho_temp.name} (gerado agora) NÃO é idêntico a {SAIDA_CSV.name} "
                "(já commitado). Arquivo novo mantido em .novo.csv para inspeção -- "
                "o original NÃO foi sobrescrito. Isso significa que o cálculo ad hoc "
                "original fez algo que este script não reproduz; investigar antes de "
                "usar qualquer um dos dois para a Tabela 2 do capítulo."
            )
    else:
        print(f"AVISO -- {SAIDA_CSV} não existe ainda; nada para comparar. Gravando {caminho_temp.name} como {SAIDA_CSV.name}.")
        caminho_temp.replace(SAIDA_CSV)


if __name__ == "__main__":
    main()
