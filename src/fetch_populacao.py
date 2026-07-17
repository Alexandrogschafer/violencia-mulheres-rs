"""Busca a população dos municípios do RS (API do IBGE) para calcular,
depois, taxas por habitante sobre os dados de violência.

Duas fontes, porque a série de estimativas do IBGE tem dois buracos:

- Tabela 6579 ("Estimativas de População"), variável 9324: usada para todos
  os anos exceto 2022. Não existe estimativa para 2022 porque é ano de
  Censo (o Censo substitui a estimativa nesse ano).
- Tabela 4709 (resultado do Censo Demográfico 2022), variável 93: usada
  só para 2022.

2023 é um segundo buraco, sem relação com o Censo: o IBGE reconheceu
publicamente que não cumpriu o calendário de divulgação das Estimativas de
População 2023 e nunca chegou a publicar essa estimativa municipal (nem em
2023, nem depois). Não existe valor oficial para preencher. Por decisão do
usuário, 2023 é interpolado linearmente entre 2022 (Censo) e 2024
(estimativa) — é um valor sintético, não uma medição do IBGE.

2026 também não tem estimativa ainda (sai em ago/set de 2026) — não é
gerada linha para 2026 nesta tabela.
"""

import gzip
import json
import time
import unicodedata
import urllib.request
from pathlib import Path

import pandas as pd

OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "outputs"
    / "tables"
    / "populacao_municipio_rs.csv"
)

UF_RS = 43
ANO_INICIO = 2012
ANO_FIM = 2025
ANO_CENSO = 2022  # sem estimativa na tabela 6579; população vem do Censo 2022
ANO_ESTIMATIVA_FALTANTE = 2023  # nunca publicado pelo IBGE; interpolado abaixo

URL_PERIODOS_ESTIMATIVA = "https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos"
URL_ESTIMATIVA = (
    "https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/{ano}"
    f"/variaveis/9324?localidades=N6[N3[{UF_RS}]]"
)
URL_CENSO_2022 = (
    "https://servicodados.ibge.gov.br/api/v3/agregados/4709/periodos/{ano}"
    f"/variaveis/93?localidades=N6[N3[{UF_RS}]]"
).format(ano=ANO_CENSO)

# Nomes em que a grafia oficial do IBGE diverge da já usada nas planilhas
# SSP/PROCERGS (violencia_*_municipio.csv). Mapeados comparando os 497
# municípios das duas fontes — sem isso, um join por município perderia
# justamente esses 7 (acentuação/hífen/abreviação à parte, já removidos
# por normaliza_municipio).
ALIAS_MUNICIPIO = {
    "BARAO DE COTEGIPE": "BARAO DO COTEGIPE",
    "DOUTOR MAURICIO CARDOSO": "DR MAURICIO CARDOSO",
    "ENTRE-IJUIS": "ENTRE IJUIS",
    "FAZENDA VILANOVA": "FAZENDA VILA NOVA",
    "NAO-ME-TOQUE": "NAO ME TOQUE",
    "SANT'ANA DO LIVRAMENTO": "SANTANA DO LIVRAMENTO",
    "XANGRI-LA": "XANGRILA",
}


def normaliza_municipio(nome_ibge: str) -> str:
    """Normaliza um nome de município do IBGE (ex.: "Água Santa - RS") para o
    padrão já usado no projeto: maiúsculas, sem acento, sem o sufixo de UF.
    """
    nome = nome_ibge.rsplit(" - ", 1)[0]
    nome = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode("ascii")
    nome = nome.upper().strip()
    return ALIAS_MUNICIPIO.get(nome, nome)


def get_json(url: str, tentativas: int = 3) -> object:
    """GET simples com retry. Alguns endpoints da API do IBGE mandam a
    resposta comprimida em gzip mesmo com Accept-Encoding: identity — por
    isso o corpo é inspecionado pelos bytes mágicos (1f 8b) e descomprimido
    manualmente quando preciso, em vez de confiar no cabeçalho do servidor.
    """
    req = urllib.request.Request(url, headers={"Accept-Encoding": "identity"})
    ultimo_erro = None
    for tentativa in range(1, tentativas + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                corpo = resp.read()
            if corpo[:2] == b"\x1f\x8b":
                corpo = gzip.decompress(corpo)
            return json.loads(corpo.decode("utf-8"))
        except Exception as erro:  # noqa: BLE001 - relançado após esgotar tentativas
            ultimo_erro = erro
            if tentativa < tentativas:
                time.sleep(2 * tentativa)
    raise RuntimeError(f"Falha ao buscar {url!r} após {tentativas} tentativas") from ultimo_erro


def _extrai_populacao_por_municipio(resposta: object, ano: int) -> list[tuple[str, int, int]]:
    """Extrai (município, ano, população) das séries de uma resposta da API
    de agregados do IBGE (mesmo formato para as tabelas 6579 e 4709).
    """
    series = resposta[0]["resultados"][0]["series"]
    registros = []
    for serie in series:
        municipio = normaliza_municipio(serie["localidade"]["nome"])
        valor = serie["serie"].get(str(ano))
        if valor is None or not valor.isdigit():
            raise ValueError(f"Valor de população inesperado para {municipio} em {ano}: {valor!r}")
        registros.append((municipio, ano, int(valor)))
    return registros


def anos_com_estimativa(ano_inicio: int, ano_fim: int) -> list[int]:
    """Anos com estimativa publicada na tabela 6579 dentro do intervalo
    pedido, excluindo o ano de Censo (tratado à parte). Consulta os períodos
    disponíveis em vez de assumir uma lista fixa, para se ajustar sozinho
    caso o IBGE publique retroativamente um ano hoje ausente (ex.: 2023).
    """
    periodos = get_json(URL_PERIODOS_ESTIMATIVA)
    anos_disponiveis = {int(p["id"]) for p in periodos}
    return sorted(
        ano
        for ano in range(ano_inicio, ano_fim + 1)
        if ano in anos_disponiveis and ano != ANO_CENSO
    )


def busca_populacao() -> pd.DataFrame:
    registros: list[tuple[str, int, int]] = []

    for ano in anos_com_estimativa(ANO_INICIO, ANO_FIM):
        resposta = get_json(URL_ESTIMATIVA.format(ano=ano))
        registros += _extrai_populacao_por_municipio(resposta, ano)

    resposta_censo = get_json(URL_CENSO_2022)
    registros += _extrai_populacao_por_municipio(resposta_censo, ANO_CENSO)

    df = pd.DataFrame(registros, columns=["municipio", "ano", "populacao"])

    if ANO_ESTIMATIVA_FALTANTE not in df.ano.unique():
        df = pd.concat([df, _interpola_ano_faltante(df, ANO_ESTIMATIVA_FALTANTE)], ignore_index=True)

    return df.sort_values(["municipio", "ano"]).reset_index(drop=True)


def _interpola_ano_faltante(df: pd.DataFrame, ano: int) -> pd.DataFrame:
    """Interpola linearmente a população de um ano sem estimativa oficial,
    usando o ano anterior e o seguinte disponíveis na série. Usado hoje só
    para 2023 (2022 Censo -> 2023 interpolado -> 2024 estimativa), mas
    funciona para qualquer buraco de um ano só.
    """
    ano_anterior = max(a for a in df.ano.unique() if a < ano)
    ano_seguinte = min(a for a in df.ano.unique() if a > ano)
    peso = (ano - ano_anterior) / (ano_seguinte - ano_anterior)

    antes = df[df.ano == ano_anterior].set_index("municipio")["populacao"]
    depois = df[df.ano == ano_seguinte].set_index("municipio")["populacao"]
    interpolado = (antes + (depois - antes) * peso).round().astype(int)

    return pd.DataFrame(
        {
            "municipio": interpolado.index,
            "ano": ano,
            "populacao": interpolado.values,
        }
    )


def main() -> None:
    df = busca_populacao()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Salvo em {OUTPUT_PATH} — {len(df)} linhas, {df.municipio.nunique()} municípios, anos {sorted(df.ano.unique())}")


if __name__ == "__main__":
    main()
