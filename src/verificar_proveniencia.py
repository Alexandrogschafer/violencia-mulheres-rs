"""Registra a proveniência dos arquivos brutos de entrada do fluxo:
data/raw/violencia_*.xlsx (SSP/RS) e data/raw/municipios_corede_rf.xlsx
(SEPLAG/RS, ver src/fetch_coredes.py) -- esta última acrescentada porque é
entrada do fluxo (tabela_agregacao_regional.py) tanto quanto as planilhas de
violência, mas ficava fora do registro de proveniência até esta sessão.

Contexto: a SSP/RS revisa retroativamente os arquivos publicados (ex.: em
2026, a página mostra 2023 e 2024 "atualizados em janeiro de 2026", e 2021
"em dezembro de 2023") -- mas nada no repositório registrava qual versão
exata deste projeto usou, embora a informação já exista dentro dos próprios
arquivos: (1) a célula "Fonte: SIP/PROCERGS - Atualizado em <data>" na aba
Geral, escrita pela própria SSP/RS; e (2) o metadado OOXML
`docProps/core.xml:dcterms:modified`, atualizado pelo Excel a cada vez que a
SSP/RS salva o arquivo. As duas fontes concordam entre si em todos os
arquivos verificados manualmente antes de escrever este script -- ambas são
geradas pela SSP/RS e sobrevivem ao download e à renomeação para
`violencia_<ano>.xlsx` (nenhuma delas depende do nome do arquivo).

A planilha de COREDEs não tem aba "Geral" nem célula "Fonte:" -- não é um
arquivo da SSP/RS, e a checagem específica dessas duas fontes (achado à
parte, registrado ao investigar a vigência da divisão em COREDEs) não se
aplica a ela. Para essa planilha, `fonte_celula_verbatim`/
`fonte_data_atualizacao_iso` ficam vazios e `aviso` é preenchido -- não
porque a extração falhou, mas porque a fonte (Atlas Socioeconômico/SEPLAG-RS)
não declara, em lugar nenhum do arquivo (célula, aba, comentário,
cabeçalho/rodapé de impressão, metadado OOXML custom), uma data de vigência
da divisão regional; o único metadado de data disponível é
`ooxml_dcterms_modified` (quando o arquivo Excel foi salvo pela última vez
pela SEPLAG/RS, não quando os limites dos 28 COREDEs foram fixados ou
revisados). Essa ausência é registrada aqui como dado (coluna `aviso`), não
silenciada.

O que este script NÃO faz, de propósito: não infere nem uma data de
download real (só temos o mtime local do arquivo, que reflete quando este
projeto o *gravou em disco* -- pode coincidir com o download, mas também
pode ser de uma cópia/rsync/checkout posterior; por isso a coluna é rotulada
"aproximação", não "data de download"), não baixa nada das fontes para
comparar com a versão atual publicada, e só preenche a URL de origem quando
ela já está registrada em código (`fetch_coredes.URL_XLSX`, para a planilha
de COREDEs) -- para as planilhas da SSP/RS a URL de origem não está
registrada em nenhum módulo, e a coluna fica em branco, para preenchimento
manual.

Uso: python -m src.verificar_proveniencia
"""

import hashlib
import re
from datetime import datetime
from pathlib import Path

import openpyxl

from src.fetch_coredes import URL_XLSX as URL_COREDE

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
CAMINHO_COREDE = RAW_DIR / "municipios_corede_rf.xlsx"  # mesmo RAW_PATH de src/fetch_coredes.py
OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "outputs"
    / "tables"
    / "proveniencia_dados_brutos.csv"
)

# Mesma extensão de "Atualizado em D/M/AAAA" usada pela SSP/RS em todos os
# arquivos verificados (dia/mês sem zero à esquerda, ano com 4 dígitos).
PADRAO_DATA_ATUALIZACAO = re.compile(r"Atualizado em (\d{1,2})/(\d{1,2})/(\d{4})")


def sha256_arquivo(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def extrai_celula_fonte(caminho: Path) -> str | None:
    """Busca, na aba 'Geral', a célula cujo texto começa com "Fonte:" --
    verbatim, sem normalizar. Retorna None se a aba não existir ou a célula
    não for encontrada (não inventa nem tenta adivinhar em outra aba)."""
    wb = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
    try:
        if "Geral" not in wb.sheetnames:
            return None
        ws = wb["Geral"]
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and cell.value.strip().startswith("Fonte:"):
                    return cell.value.strip()
        return None
    finally:
        wb.close()


def extrai_modified_ooxml(caminho: Path) -> datetime | None:
    """dcterms:modified de docProps/core.xml, já como datetime (openpyxl
    parseia isso em wb.properties.modified -- não precisa ler o XML manualmente)."""
    wb = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
    try:
        return wb.properties.modified
    finally:
        wb.close()


def normaliza_data_atualizacao(fonte_verbatim: str | None) -> str | None:
    """Extrai D/M/AAAA de dentro do texto verbatim da célula "Fonte:" e
    normaliza para ISO (AAAA-MM-DD). O texto verbatim continua registrado à
    parte (coluna fonte_celula_verbatim) -- esta função é só conveniência de
    leitura, nunca a evidência em si."""
    if not fonte_verbatim:
        return None
    m = PADRAO_DATA_ATUALIZACAO.search(fonte_verbatim)
    if not m:
        return None
    dia, mes, ano = (int(x) for x in m.groups())
    return f"{ano:04d}-{mes:02d}-{dia:02d}"


def processa_arquivo(caminho: Path, url_origem: str = "") -> dict:
    fonte_verbatim = extrai_celula_fonte(caminho)
    modified_ooxml = extrai_modified_ooxml(caminho)
    mtime_local = datetime.fromtimestamp(caminho.stat().st_mtime)

    aviso = None
    if fonte_verbatim is None:
        aviso = (
            "AVISO: célula 'Fonte:' não encontrada (sem aba 'Geral' ou sem a célula) -- "
            "data de atualização declarada indisponível nesta planilha."
        )

    return {
        "arquivo": caminho.name,
        "sha256": sha256_arquivo(caminho),
        "fonte_celula_verbatim": fonte_verbatim or "",
        "fonte_data_atualizacao_iso": normaliza_data_atualizacao(fonte_verbatim) or "",
        "ooxml_dcterms_modified_iso": modified_ooxml.isoformat() if modified_ooxml else "",
        "mtime_local_aproximacao_download": mtime_local.isoformat(),
        "url_origem": url_origem,  # preenchimento manual quando não registrada em código -- ver docstring do módulo
        "aviso": aviso or "",
    }


def main() -> None:
    arquivos = sorted(RAW_DIR.glob("violencia_*.xlsx"))
    if not arquivos:
        raise FileNotFoundError(f"Nenhum violencia_*.xlsx encontrado em {RAW_DIR}")

    registros = [processa_arquivo(caminho) for caminho in arquivos]

    if CAMINHO_COREDE.exists():
        registros.append(processa_arquivo(CAMINHO_COREDE, url_origem=URL_COREDE))
    else:
        print(
            f"AVISO: {CAMINHO_COREDE} não encontrado -- planilha de COREDEs (SEPLAG/RS) não incluída "
            "no registro de proveniência nesta execução. Rode `python -m src.fetch_coredes` primeiro."
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    colunas = [
        "arquivo",
        "sha256",
        "fonte_celula_verbatim",
        "fonte_data_atualizacao_iso",
        "ooxml_dcterms_modified_iso",
        "mtime_local_aproximacao_download",
        "url_origem",
        "aviso",
    ]
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(",".join(colunas) + "\n")
        for r in registros:
            linha = [str(r[c]).replace('"', '""') for c in colunas]
            linha = [f'"{v}"' if ("," in v or '"' in v) else v for v in linha]
            f.write(",".join(linha) + "\n")

    n_com_aviso = sum(1 for r in registros if r["aviso"])
    print(f"Salvo em {OUTPUT_PATH} — {len(registros)} arquivo(s) processados.")
    if n_com_aviso:
        print(f"AVISO: {n_com_aviso} arquivo(s) sem célula 'Fonte:' encontrada (ver coluna 'aviso' no CSV):")
        for r in registros:
            if r["aviso"]:
                print(f"  - {r['arquivo']}")
    else:
        print("Célula 'Fonte:' encontrada em todos os arquivos.")


if __name__ == "__main__":
    main()
