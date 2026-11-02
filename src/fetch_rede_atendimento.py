"""Rede de atendimento por município do RS: baixa a MUNIC/IBGE e grava presença/ausência.

Pergunta que serve: os municípios significativos no LISA com zero ou poucos eventos são
desprovidos de serviço? É validação de medida, não modelo.

Edições da MUNIC verificadas no FTP do IBGE (2018-2025; não há 2022 nem 2025), pelas abas
de cada base e pelo dicionário de variáveis:

| Edição | Política para mulheres | Delegacia da mulher | CREAS (Assistência social) |
| 2018   | sim (MPPM01)           | sim, no bloco mulheres (MPPM244) | sim (MASS253) |
| 2019   | não                    | sim, Segurança pública (MSEG168) | não           |
| 2020   | não                    | não                               | não           |
| 2021   | não                    | não                               | não           |
| 2023   | sim (MPPM01)           | sim, Segurança pública (MSEG168) | sim (MASS253) |
| 2024   | não                    | não                               | não           |

Codificação dos traços ("-"), verificada nos dados do RS:
- MPPM244 (2018) é "-" quando MPPM23 = "Não" (não há serviço especializado) ou quando
  MPPM2411 ("nenhum dos serviços citados") = "Sim". Nos dois casos, ausência.
- MSEG168 (2023) é "-" exatamente quando MSEG1611 ("nenhuma das citadas") = "Sim": ausência.
- MASS253 é "-" quando o quesito 6.6/2.6 inteiro veio em branco, sem filtro anterior que o
  justifique: não é ausência, é falta de resposta.
"Não informou" e "Não soube informar" são sempre falta de resposta.

O CREAS do Censo SUAS/MDS fica de fora: em 02/11/2026 aplicacoes.mds.gov.br redirecionava
para um aviso de "manutenção preventiva de segurança", e o dados.gov.br só aponta para lá.
Até ele voltar, o CREAS é o da MUNIC, autodeclarado.

Uso: python -m src.fetch_rede_atendimento  (baixa o que faltar com curl e processa)
"""

import hashlib
import subprocess
import zipfile
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw" / "rede_atendimento" / "munic"
SAIDA = RAIZ / "data" / "processed" / "rede_atendimento_municipio.csv"
PROVENIENCIA = RAIZ / "data" / "processed" / "rede_atendimento_proveniencia.csv"
CODIGOS = RAIZ / "outputs" / "tables" / "municipio_codigo_ibge.csv"
FTP = "https://ftp.ibge.gov.br/Perfil_Municipios"

ARQUIVOS = {
    2018: ("2018/Base_de_Dados/Base_MUNIC_2018_xlsx_20201103.zip", "Base_MUNIC_2018_xlsx_20201103.xlsx"),
    2019: ("2019/Base_de_Dados/Base_MUNIC_2019_20210817.xlsx", None),
    2023: ("2023/Base_de_Dados/Base_MUNIC_2023.xlsx", None),
}

# (indicador, edição, aba, variável)
INDICADORES = [
    ("deam", 2018, "Política para mulheres", "MPPM244"),
    ("deam", 2019, "Segurança pública", "MSEG168"),
    ("deam", 2023, "Segurança Pública", "MSEG168"),
    ("organismo_mulheres", 2018, "Política para mulheres", "MPPM01"),
    ("organismo_mulheres", 2023, "Política para Mulheres", "MPPM01"),
    ("creas_munic", 2018, "Assistência social", "MASS253"),
    ("creas_munic", 2023, "Assistência Social", "MASS253"),
]
SEM_RESPOSTA = {"Não informou", "não informou", "(*) Não soube informar", "*Não soube informar", "Recusa"}
N_MUNICIPIOS = 497


def baixar() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    for caminho, _ in ARQUIVOS.values():
        destino = RAW / Path(caminho).name
        if not destino.exists():
            subprocess.run(["curl", "-sSfL", "--max-time", "600", "-o", str(destino), f"{FTP}/{caminho}"], check=True)


def planilha(edicao: int) -> Path:
    caminho, interno = ARQUIVOS[edicao]
    arquivo = RAW / Path(caminho).name
    if interno is None:
        return arquivo
    extraido = RAW / f"x{edicao}" / interno
    if not extraido.exists():
        with zipfile.ZipFile(arquivo) as z:
            z.extract(interno, extraido.parent)
    return extraido


def aba_rs(edicao: int, aba: str) -> pd.DataFrame:
    d = pd.read_excel(planilha(edicao), sheet_name=aba, dtype=str)
    col = next(c for c in d.columns if c.upper().replace(" ", "").startswith("CODMUN"))
    d = d[d[col].str.startswith("43")].rename(columns={col: "codigo_ibge"})
    d["codigo_ibge"] = d["codigo_ibge"].astype(int)
    if len(d) != N_MUNICIPIOS or d["codigo_ibge"].duplicated().any():
        raise ValueError(f"MUNIC {edicao}, {aba}: {len(d)} linhas do RS, esperadas {N_MUNICIPIOS}.")
    return d.set_index("codigo_ibge")


def classificar(indicador: str, edicao: int, d: pd.DataFrame, var: str) -> pd.Series:
    v = d[var].fillna("-")
    status = pd.Series("sem_resposta", index=d.index)
    status[v == "Sim"] = "tem"
    status[v == "Não"] = "nao_tem"
    traco = v == "-"
    if indicador == "deam" and edicao == 2018:
        pulo = (d["MPPM23"] == "Não") | (d["MPPM2411"] == "Sim")
        status[traco & pulo] = "nao_tem"
    elif indicador == "deam" and edicao == 2023:
        status[traco & (d["MSEG1611"] == "Sim")] = "nao_tem"
    resto = ~v.isin(["Sim", "Não"]) & ~(traco & (status == "nao_tem"))
    desconhecido = set(v[resto]) - SEM_RESPOSTA - {"-"}
    if desconhecido:
        raise ValueError(f"{indicador} {edicao}: valores não previstos {desconhecido}")
    return status


def processar() -> pd.DataFrame:
    codigos = pd.read_csv(CODIGOS)
    if len(codigos) != N_MUNICIPIOS:
        raise ValueError("municipio_codigo_ibge.csv não tem 497 linhas.")
    linhas = []
    for indicador, edicao, aba, var in INDICADORES:
        d = aba_rs(edicao, aba)
        nao_informou = d.isin(SEM_RESPOSTA).sum(axis=1)
        status = classificar(indicador, edicao, d, var)
        linhas.append(
            pd.DataFrame(
                {
                    "codigo_ibge": d.index,
                    "indicador": indicador,
                    "fonte": "MUNIC/IBGE",
                    "edicao": edicao,
                    "aba": aba,
                    "variavel": var,
                    "valor_original": d[var].fillna("").to_numpy(),
                    "status": status.to_numpy(),
                    "itens_sem_resposta_na_aba": nao_informou.to_numpy(),
                }
            )
        )
    out = pd.concat(linhas).merge(codigos, on="codigo_ibge", how="left", validate="many_to_one")
    if out["municipio"].isna().any():
        raise ValueError("Código IBGE da MUNIC sem correspondência em municipio_codigo_ibge.csv.")
    cols = ["codigo_ibge", "municipio"] + [c for c in out.columns if c not in ("codigo_ibge", "municipio")]
    return out[cols].sort_values(["indicador", "edicao", "codigo_ibge"])


def proveniencia() -> pd.DataFrame:
    linhas = []
    for edicao, (caminho, _) in ARQUIVOS.items():
        arq = RAW / Path(caminho).name
        linhas.append(
            {
                "fonte": "MUNIC/IBGE",
                "edicao": edicao,
                "url": f"{FTP}/{caminho}",
                "sha256": hashlib.sha256(arq.read_bytes()).hexdigest(),
                "bytes": arq.stat().st_size,
            }
        )
    return pd.DataFrame(linhas)


def main() -> None:
    baixar()
    out = processar()
    out.to_csv(SAIDA, index=False)
    proveniencia().to_csv(PROVENIENCIA, index=False)
    print(f"{SAIDA}: {len(out)} linhas")
    print(out.pivot_table(index=["indicador", "edicao"], columns="status", values="codigo_ibge", aggfunc="count", fill_value=0))


if __name__ == "__main__":
    main()
