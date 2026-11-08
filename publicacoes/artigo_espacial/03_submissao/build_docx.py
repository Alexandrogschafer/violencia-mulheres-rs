"""Monta os .docx de submissão do artigo espacial à RESS (Epidemiologia e Serviços de Saúde).

Adaptado de publicacoes/artigo_reciis/03_submissao/build_docx.py (ramo auditoria-metodologica,
último commit 435cd8f). O parser de lá era sob medida para um markdown exportado do Word pelo
Pandoc (tabelas em grade, imagens `![](media/...)`, escapes `\\`). Este lê os arquivos gerados
do artigo espacial, que têm outra forma:

- 02_texto/artigo_espacial_submissao.md -- manuscrito sem comentários HTML (gerado por
  02_texto/gerar_versao_submissao.py): `#` título, `##` seções, `###` subseções, negrito
  `**...**`, referências numeradas em texto;
- 03_tabelas/tabelas.md -- tabelas em pipe com título e notas (gerado por gerar_tabelas.py);
  cada tabela é conferida, célula a célula, contra o CSV de mesmo cabeçalho na mesma pasta;
- 03_figuras/figura1.png e 03_figuras/figura1_legenda.md (gerados por gerar_figura1.py).

Nenhum conteúdo é escrito aqui: todo texto, número, título e nota vem desses arquivos.

Saídas, em 03_submissao/:

- artigo_espacial_manuscrito.docx -- o "documento único" da RESS, na ordem das instruções:
  modalidade, título, resumo, palavras-chave, aspectos éticos, corpo (Introdução a Conclusão),
  disponibilidade de dados, uso de IA generativa, referências e, "ao final do texto, após as
  referências", as três tabelas e a Figura 1;
- artigo_espacial_suplementar.docx -- as duas tabelas suplementares. As instruções dizem que
  "poderão ser encaminhadas até duas tabelas e figuras suplementares em arquivo único", e o
  material suplementar não está entre os itens do documento único: vão em arquivo próprio;
- artigo_espacial_manuscrito.pdf e artigo_espacial_suplementar.pdf -- os mesmos .docx, já
  gravados e conferidos, convertidos pelo LibreOffice em modo headless, que é o renderizador com
  que a paginação foi conferida. Sem LibreOffice, o script tenta pandoc com um motor LaTeX e diz
  qual caminho usou; esse caminho não reproduz a paginação do Word/LibreOffice, e a conferência
  de paginação abaixo provavelmente o interrompe.

Formatação e origem de cada item (instruções da RESS lidas em 2026-11-07 em
https://www.scielo.br/journal/ress/about/; "RECIIS" = padrão do script de origem):

| Item | Valor | Origem |
|---|---|---|
| Fonte e corpo do texto | Times New Roman 12, inclusive título e legendas | RESS |
| Entrelinha | simples em todo o documento | RESS |
| Formato do arquivo | DOCX | RESS |
| Tabelas: fonte e entrelinha | Times New Roman 10, simples | RESS (mínimo 10) e RECIIS (10) |
| Tabelas: cabeçalho | "Repetir linhas de cabeçalho" | RESS |
| Tabelas: mesclagem | nenhuma | RESS ("evite mesclar"); a RECIIS mesclava |
| Tabelas: alinhamento | números à direita, texto à esquerda | RESS |
| Tabelas: títulos e notas | fora da grade; título acima, notas abaixo | RESS (fora da grade), RECIIS (posição) |
| Tabelas: bordas | só horizontais: topo, sob o cabeçalho, base | RECIIS |
| Tabelas: largura das colunas | ao menos a palavra mais longa do cabeçalho; o resto em proporção ao texto mais longo da coluna, medido em Times New Roman 10; soma igual à largura útil da página | próprio: a régua do Pandoc que a RECIIS usava não existe em tabela pipe |
| Notas de rodapé | letras minúsculas sobrescritas (formatação de sobrescrito do Word) | RESS |
| Ilustrações | ao final, após as referências, cada uma em página nova | RESS (posição); página nova é próprio |
| Figura | largura 17 cm, legenda e notas abaixo, presas à imagem | RECIIS |
| Aspectos éticos | em quadro (tabela de uma célula com borda) | RESS ("quadro") |
| Página | A4 retrato, margens de 2 cm | RECIIS (a RESS só fixa mínimo de 1,5 cm para tabelas e figuras) |
| Orientação das tabelas | paisagem quando as células não cabem, cada uma numa linha, na largura do retrato | RESS aceita retrato ou paisagem; o critério é próprio, para que cada tabela caiba nas duas páginas permitidas |
| Numeração de linhas | nenhuma | RECIIS (removida em 435cd8f); RESS não especifica |
| Numeração de páginas | nenhuma | RECIIS; RESS não especifica |
| Recuo de primeira linha | 0,5 cm nos parágrafos de corpo e no resumo | RECIIS |
| Alinhamento | corpo justificado; referências e palavras-chave à esquerda; título, legendas e notas centralizados | RECIIS |
| Espaço após parágrafo | 10 pt (herdado do modelo); 0 nas células de tabela | RECIIS; células: próprio |
| Título do artigo | negrito, centralizado, sem mudança de caixa | RECIIS (sem o 14 pt, que a RESS substitui por 12, e sem o `.capitalize()`: a fonte já está em caixa de frase) |
| Seções | negrito, sem numeração, rótulo como na fonte | RECIIS (negrito); a numeração era norma da Reciis |
| Subseções | negrito e itálico | próprio: sem numeração, é o que distingue o nível |
| Idioma do documento | pt-BR | próprio |
| Metadados do arquivo | autor e "modificado por" vazios | próprio, para a avaliação cega |

Conferências que interrompem o script sem gravar nada (as saídas vão primeiro para arquivo
temporário e só substituem as anteriores se tudo passar):

- a versão de submissão está em dia com 02_texto/artigo_espacial.md;
- seções na ordem das instruções; resumo em parágrafo único de até 250 palavras; cinco
  palavras-chave; até 5 tabelas e figuras, 30 referências e 2 suplementares; toda ilustração
  citada no texto;
- cada tabela de tabelas.md idêntica ao CSV correspondente;
- releitura dos .docx gravados: cada parágrafo e célula igual ao texto da fonte; mesmos números
  (multiconjunto) que os arquivos-fonte; cada tabela igual ao CSV;
- contagem de palavras do corpo no .docx igual à do .md (critério de
  00_protocolo/limite_palavras_ress.md);
- nenhum nome, ORCID iD ou afiliação de 02_texto/dados_submissao.md, nem o endereço ou o
  usuário do repositório, em nenhuma parte dos .docx (texto, metadados, relações);
- nos PDF: Author vazio; Title igual ao título do .docx (o do artigo); Creator e Producer sem
  caminho de arquivo, sem o usuário do sistema e sem nenhum dos identificadores acima; nenhum
  identificador no texto extraído nem nos metadados XMP;
- paginação dos PDF: o corpo termina antes da primeira ilustração, cada tabela (com título e
  notas) ocupa no máximo duas páginas e a figura, com legenda e notas, uma só -- os limites das
  instruções da RESS.

Os .docx só substituem os anteriores depois de conferidos; os PDF, depois de conferidos também.
Uma falha nos PDF deixa os .docx novos já gravados e os PDF anteriores intocados.

Nota não impeditiva: o título tem uma vírgula antes dos anos, e as instruções dizem que a
pontuação aceita no título são os dois pontos. Mantida por decisão dos autores (2026-11-07);
o script só a registra como nota.

Uso: python build_docx.py
"""

import csv
import getpass
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ARTIGO = Path(__file__).resolve().parent.parent
ROOT = ARTIGO.parent.parent
TEXTO_DIR = ARTIGO / "02_texto"
MANUSCRITO_MD = TEXTO_DIR / "artigo_espacial_submissao.md"
GERADOR_SUBMISSAO = TEXTO_DIR / "gerar_versao_submissao.py"
DADOS_SUBMISSAO = TEXTO_DIR / "dados_submissao.md"
TABELAS_DIR = ARTIGO / "03_tabelas"
TABELAS_MD = TABELAS_DIR / "tabelas.md"
FIGURAS_DIR = ARTIGO / "03_figuras"
LEGENDA_FIGURA1 = FIGURAS_DIR / "figura1_legenda.md"
IMAGEM_FIGURA1 = FIGURAS_DIR / "figura1.png"
SAIDA_DIR = ARTIGO / "03_submissao"
SAIDA_MANUSCRITO = SAIDA_DIR / "artigo_espacial_manuscrito.docx"
SAIDA_SUPLEMENTAR = SAIDA_DIR / "artigo_espacial_suplementar.docx"

FONTE_NOME = "Times New Roman"
FONTE_TAMANHO = Pt(12)
TABELA_TAMANHO = Pt(10)
MARGEM_CM = 2.0
LARGURA_UTIL_CM = 21.0 - 2 * MARGEM_CM  # retrato
LARGURA_UTIL_PAISAGEM_CM = 29.7 - 2 * MARGEM_CM
RECUO_CORPO = Cm(0.5)

# Ordem do "documento único" nas instruções da RESS, só com os itens deste artigo (sem registro
# de protocolo, que é para revisões e ensaios). Modalidade e título vêm antes, fora de seção.
SECOES_ESPERADAS = [
    "Resumo",
    "Aspectos éticos",
    "Introdução",
    "Métodos",
    "Resultados",
    "Discussão",
    "Conclusão",
    "Disponibilidade de dados",
    "Uso de inteligência artificial generativa",
    "Referências",
]
CORPO_INICIO, CORPO_FIM = "Introdução", "Conclusão"

# Limites da modalidade artigo original e das suplementares (instruções da RESS).
LIMITE_ILUSTRACOES = 5
LIMITE_REFERENCIAS = 30
LIMITE_SUPLEMENTARES = 2
LIMITE_PALAVRAS_RESUMO = 250
PALAVRAS_CHAVE = 5

SOBRESCRITOS = {"ᵃ": "a", "ᵇ": "b", "ᶜ": "c", "ᵈ": "d", "ᵉ": "e", "ᶠ": "f", "ᵍ": "g", "ʰ": "h"}
DE_VOLTA = {v: k for k, v in SOBRESCRITOS.items()}
RE_NUMERO = re.compile(r"\d+(?:[.,]\d+)*")
RE_NUMERICO = re.compile(r"^(?:[<>≤≥]\s?)?-?\d+(?:[.,]\d+)*$|^—$")


class Divergencia(Exception):
    """Qualquer falha de conferência: o script para sem gravar as saídas."""


# ---------------------------------------------------------------- leitura das fontes


def _sem_negrito(texto: str) -> str:
    return texto.replace("**", "")


def conta_palavras(texto: str) -> int:
    """Critério de 00_protocolo/limite_palavras_ress.md, o mesmo de
    01_referencias/renumerar_referencias.py: token com letra ou dígito."""
    return sum(1 for t in _sem_negrito(texto).split() if re.search(r"[0-9A-Za-zÀ-ÿ]", t))


def conferir_versao_submissao() -> str:
    """A versão de submissão tem de ser a que o gerador produziria hoje a partir do arquivo de
    trabalho -- senão o .docx sairia de um texto desatualizado."""
    spec = importlib.util.spec_from_file_location("gerar_versao_submissao", GERADOR_SUBMISSAO)
    gerador = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gerador)
    esperado = gerador.COMENTARIO.sub("", gerador.ENTRADA.read_text(encoding="utf-8"))
    esperado = re.sub(r"\n{3,}", "\n\n", esperado)
    atual = MANUSCRITO_MD.read_text(encoding="utf-8")
    if atual != esperado:
        raise Divergencia(
            f"{MANUSCRITO_MD.name} está desatualizado em relação a {gerador.ENTRADA.name}: "
            f"rode {GERADOR_SUBMISSAO.name} antes."
        )
    if "<!--" in atual:
        raise Divergencia(f"{MANUSCRITO_MD.name} ainda tem comentário HTML.")
    return atual


def _blocos(texto: str) -> list[str]:
    """Parágrafos lógicos: linhas não vazias consecutivas, juntadas por espaço."""
    blocos, atual = [], []
    for linha in texto.splitlines():
        if linha.strip():
            atual.append(linha.strip())
        elif atual:
            blocos.append(" ".join(atual))
            atual = []
    if atual:
        blocos.append(" ".join(atual))
    return blocos


def ler_manuscrito(texto: str) -> dict:
    blocos = _blocos(texto)
    if not blocos[0].startswith("**Modalidade:**"):
        raise Divergencia("O primeiro bloco do manuscrito não é a modalidade.")
    if not blocos[1].startswith("# "):
        raise Divergencia("O segundo bloco do manuscrito não é o título (# ...).")
    m = {"modalidade": blocos[0], "titulo": blocos[1][2:], "secoes": []}
    for bloco in blocos[2:]:
        if bloco.startswith("# "):
            raise Divergencia(f"Segundo título de nível 1: {bloco[:60]}")
        if bloco.startswith("## "):
            m["secoes"].append({"nome": bloco[3:], "itens": []})
        elif not m["secoes"]:
            raise Divergencia(f"Texto entre o título e a primeira seção: {bloco[:60]}")
        elif bloco.startswith("### "):
            m["secoes"][-1]["itens"].append(("subsecao", bloco[4:]))
        elif bloco.startswith("#"):
            raise Divergencia(f"Nível de título não previsto: {bloco[:60]}")
        else:
            m["secoes"][-1]["itens"].append(("paragrafo", bloco))
    nomes = [s["nome"] for s in m["secoes"]]
    if nomes != SECOES_ESPERADAS:
        raise Divergencia(f"Seções fora da ordem da RESS.\n  esperado: {SECOES_ESPERADAS}\n  fonte:    {nomes}")
    return m


def conferir_requisitos(m: dict, texto: str) -> list[str]:
    """Requisitos das instruções verificáveis no texto. Devolve notas que não param o script."""
    notas = []
    resumo = [t for k, t in _secao(m, "Resumo") if k == "paragrafo"]
    chaves = [t for t in resumo if t.startswith("**Palavras-chave:**")]
    corpo_resumo = [t for t in resumo if not t.startswith("**Palavras-chave:**")]
    if len(corpo_resumo) != 1:
        raise Divergencia(f"O resumo deve ser parágrafo único; a fonte tem {len(corpo_resumo)}.")
    n_resumo = conta_palavras(corpo_resumo[0])
    if n_resumo > LIMITE_PALAVRAS_RESUMO:
        raise Divergencia(f"Resumo com {n_resumo} palavras, acima de {LIMITE_PALAVRAS_RESUMO}.")
    if len(chaves) != 1:
        raise Divergencia("Falta a linha de palavras-chave no resumo.")
    termos = [t.strip().rstrip(".") for t in chaves[0].split("**", 2)[2].split(";") if t.strip()]
    if len(termos) != PALAVRAS_CHAVE:
        raise Divergencia(f"{len(termos)} palavras-chave; a RESS pede {PALAVRAS_CHAVE}.")
    refs = [t for k, t in _secao(m, "Referências") if k == "paragrafo"]
    numeros = [int(re.match(r"(\d+)\. ", r).group(1)) if re.match(r"\d+\. ", r) else None for r in refs]
    if numeros != list(range(1, len(refs) + 1)):
        raise Divergencia(f"Referências fora da numeração sequencial: {numeros}")
    if len(refs) > LIMITE_REFERENCIAS:
        raise Divergencia(f"{len(refs)} referências, acima de {LIMITE_REFERENCIAS}.")
    if re.search(r"[,;.!?]", m["titulo"]):
        notas.append(
            "o título tem pontuação além dos dois pontos (as instruções aceitam só os dois pontos); "
            f"mantida por decisão dos autores: «{m['titulo']}»"
        )
    m["n_resumo"] = n_resumo
    m["n_referencias"] = len(refs)
    return notas


def _secao(m: dict, nome: str) -> list:
    return next(s["itens"] for s in m["secoes"] if s["nome"] == nome)


def ler_csvs() -> dict:
    """Tabelas CSV de 03_tabelas, indexadas pelo cabeçalho (único por tabela)."""
    por_cabecalho = {}
    for caminho in sorted(TABELAS_DIR.glob("*.csv")):
        with caminho.open(encoding="utf-8-sig", newline="") as f:
            linhas = [linha for linha in csv.reader(f, delimiter=";")]
        chave = tuple(linhas[0])
        if chave in por_cabecalho:
            raise Divergencia(f"Dois CSVs com o mesmo cabeçalho: {caminho.name}")
        por_cabecalho[chave] = (caminho.name, linhas)
    return por_cabecalho


def ler_tabelas(csvs: dict) -> list[dict]:
    """Tabelas de tabelas.md (pipe + título + notas), cada uma conferida contra seu CSV."""
    texto = re.sub(r"<!--.*?-->", "", TABELAS_MD.read_text(encoding="utf-8"), flags=re.S)
    tabelas = []
    for pedaco in re.split(r"^---$", texto, flags=re.M)[1:]:
        linhas = [l.strip() for l in pedaco.strip().splitlines() if l.strip()]
        grade = [l for l in linhas if l.startswith("|")]
        resto = [l for l in linhas if not l.startswith("|")]
        if len(grade) < 3 or not re.fullmatch(r"\|(?:\s*-{3,}\s*\|)+", grade[1]):
            raise Divergencia(f"Tabela pipe malformada em {TABELAS_MD.name}: {pedaco[:80]!r}")
        celulas = [[c.strip() for c in l.strip("|").split("|")] for l in [grade[0]] + grade[2:]]
        titulos = [l for l in resto if l.startswith("**Tabela")]
        notas = [l for l in resto if not l.startswith("**Tabela")]
        if len(titulos) != 1 or len(notas) > 1:
            raise Divergencia(f"Tabela sem título único ou com mais de uma linha de notas: {titulos or resto}")
        alvo = csvs.get(tuple(celulas[0]))
        if alvo is None:
            raise Divergencia(f"Nenhum CSV com o cabeçalho da tabela «{titulos[0][:70]}»: {celulas[0]}")
        nome_csv, linhas_csv = alvo
        if celulas != linhas_csv:
            dif = next(
                (i, a, b) for i, (a, b) in enumerate(zip(celulas, linhas_csv + [[]] * len(celulas))) if a != b
            ) if len(celulas) >= len(linhas_csv) else (len(celulas), None, linhas_csv[len(celulas)])
            raise Divergencia(f"{TABELAS_MD.name} diverge de {nome_csv} na linha {dif[0]}:\n  md:  {dif[1]}\n  csv: {dif[2]}")
        tabelas.append(
            {
                "titulo": titulos[0],
                "notas": notas[0] if notas else None,
                "celulas": celulas,
                "csv": nome_csv,
                "suplementar": titulos[0].startswith("**Tabela suplementar"),
                "continuacao": "(continuação)" in titulos[0],
            }
        )
    usados = Counter(t["csv"] for t in tabelas)
    faltando = sorted({nome for nome, _ in csvs.values()} - set(usados))
    if faltando or any(n > 1 for n in usados.values()):
        raise Divergencia(f"Correspondência tabela-CSV não é um para um: sem tabela {faltando}, repetidos {usados}")
    return tabelas


def ler_legenda_figura1() -> tuple[str, str]:
    texto = re.sub(r"<!--.*?-->", "", LEGENDA_FIGURA1.read_text(encoding="utf-8"), flags=re.S)
    texto = texto.split("\n## ", 1)[0]  # a "Conferência da paleta" é nota interna, não legenda
    blocos = [b for b in _blocos(texto) if not b.startswith("# ")]
    if len(blocos) != 2 or not blocos[0].startswith("**Figura 1.**"):
        raise Divergencia(f"{LEGENDA_FIGURA1.name}: esperava título «**Figura 1.**» e uma linha de notas, achei {blocos}")
    return blocos[0], blocos[1]


def conferir_citacoes(m: dict, tabelas: list[dict]) -> None:
    corpo = " ".join(
        _sem_negrito(t) for s in m["secoes"] if s["nome"] not in ("Referências",) for _, t in s["itens"]
    )
    rotulos = []
    for t in tabelas:
        if t["continuacao"]:
            continue
        rotulos.append(re.match(r"\*\*(Tabela(?: suplementar)? \d+)\.\*\*", t["titulo"]).group(1))
    rotulos.append("Figura 1")
    for rotulo in rotulos:
        if not re.search(rf"\b{rotulo}\b", corpo):
            raise Divergencia(f"{rotulo} não é citada no texto.")
    citadas = set(re.findall(r"\b(Tabela suplementar \d+|Tabela \d+|Figura \d+)\b", corpo))
    sobra = citadas - set(rotulos)
    if sobra:
        raise Divergencia(f"O texto cita ilustrações que não existem: {sorted(sobra)}")
    n_ilustr = sum(1 for r in rotulos if not r.startswith("Tabela suplementar"))
    n_supl = len(rotulos) - n_ilustr
    if n_ilustr > LIMITE_ILUSTRACOES or n_supl > LIMITE_SUPLEMENTARES:
        raise Divergencia(f"{n_ilustr} tabelas e figuras e {n_supl} suplementares, acima do limite da RESS.")


# ---------------------------------------------------------------- formatação


def _documento(titulo: str) -> Document:
    doc = Document()
    secao = doc.sections[0]
    secao.page_height, secao.page_width = Cm(29.7), Cm(21.0)
    for lado in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
        setattr(secao, lado, Cm(MARGEM_CM))

    # Times New Roman e pt-BR nos padrões do documento, para que tudo herde (inclusive tabelas).
    padroes = doc.styles.element.find(qn("w:docDefaults")).find(qn("w:rPrDefault")).find(qn("w:rPr"))
    fontes = padroes.find(qn("w:rFonts"))
    for atributo in list(fontes.attrib):
        del fontes.attrib[atributo]
    for atributo in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        fontes.set(qn(atributo), FONTE_NOME)
    for tag in ("w:sz", "w:szCs"):
        padroes.find(qn(tag)).set(qn("w:val"), str(int(FONTE_TAMANHO.pt * 2)))
    idioma = padroes.find(qn("w:lang"))
    idioma.set(qn("w:val"), "pt-BR")
    idioma.set(qn("w:eastAsia"), "pt-BR")
    normal = doc.styles["Normal"]
    normal.font.name = FONTE_NOME
    normal.font.size = FONTE_TAMANHO
    normal.paragraph_format.line_spacing = 1.0

    cp = doc.core_properties
    cp.author = ""
    cp.last_modified_by = ""
    cp.comments = ""
    cp.keywords = ""
    cp.title = titulo
    return doc


def _runs(paragrafo, texto: str, tamanho=FONTE_TAMANHO, negrito_base=False, italico=False) -> None:
    """Texto com **negrito** e letras de nota sobrescritas (ᵃ → «a» sobrescrito)."""
    for parte in re.split(r"(\*\*.*?\*\*)", texto):
        if not parte:
            continue
        negrito = parte.startswith("**") and parte.endswith("**")
        conteudo = parte[2:-2] if negrito else parte
        for pedaco in re.split(f"([{''.join(SOBRESCRITOS)}]+)", conteudo):
            if not pedaco:
                continue
            sobrescrito = pedaco[0] in SOBRESCRITOS
            run = paragrafo.add_run("".join(SOBRESCRITOS[c] for c in pedaco) if sobrescrito else pedaco)
            run.bold = negrito or negrito_base
            run.italic = italico or None
            run.font.superscript = sobrescrito or None
            run.font.name = FONTE_NOME
            run.font.size = tamanho


def _paragrafo(doc_ou_celula, texto, alinhamento, recuo=None, **kw):
    p = doc_ou_celula.add_paragraph()
    p.alignment = alinhamento
    p.paragraph_format.line_spacing = 1.0
    if recuo is not None:
        p.paragraph_format.first_line_indent = recuo
    _runs(p, texto, **kw)
    return p


def _titulo_secao(doc, texto: str, nivel: int):
    p = _paragrafo(doc, texto, WD_ALIGN_PARAGRAPH.LEFT, negrito_base=True, italico=(nivel == 3))
    p.paragraph_format.space_before = Pt(12 if nivel == 2 else 6)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    return p


def _quebra_pagina(doc) -> None:
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def _orientar(secao, paisagem: bool) -> None:
    secao.orientation = WD_ORIENT.LANDSCAPE if paisagem else WD_ORIENT.PORTRAIT
    secao.page_width, secao.page_height = (Cm(29.7), Cm(21.0)) if paisagem else (Cm(21.0), Cm(29.7))


def _nova_pagina(doc, paisagem: bool) -> None:
    """Página nova; se a orientação muda, por quebra de seção."""
    if (doc.sections[-1].orientation == WD_ORIENT.LANDSCAPE) == paisagem:
        _quebra_pagina(doc)
    else:
        _orientar(doc.add_section(WD_SECTION.NEW_PAGE), paisagem)


def _largura_util(doc) -> float:
    s = doc.sections[-1]
    return (s.page_width - s.left_margin - s.right_margin) / Cm(1)


def _bordas(celula, lados: dict) -> None:
    """lados: {'top': 'single'|'nil', ...}; substitui as bordas existentes nesses lados."""
    tcPr = celula._tc.get_or_add_tcPr()
    bordas = tcPr.find(qn("w:tcBorders"))
    if bordas is None:
        bordas = OxmlElement("w:tcBorders")
        tcPr.append(bordas)
    for lado in ("top", "left", "bottom", "right"):
        if lado not in lados:
            continue
        existente = bordas.find(qn(f"w:{lado}"))
        if existente is not None:
            bordas.remove(existente)
        el = OxmlElement(f"w:{lado}")
        el.set(qn("w:val"), lados[lado])
        if lados[lado] != "nil":
            el.set(qn("w:sz"), "8")
            el.set(qn("w:space"), "0")
            el.set(qn("w:color"), "000000")
        bordas.append(el)
    # Ordem exigida pelo esquema dentro de tcBorders.
    for lado in ("top", "left", "bottom", "right"):
        el = bordas.find(qn(f"w:{lado}"))
        if el is not None:
            bordas.remove(el)
            bordas.append(el)


def _quadro(doc, titulo: str, paragrafos: list[str]) -> None:
    """Aspectos éticos: as instruções pedem um quadro."""
    tabela = doc.add_table(rows=1, cols=1)
    tabela.alignment = WD_TABLE_ALIGNMENT.CENTER
    celula = tabela.cell(0, 0)
    celula.width = Cm(LARGURA_UTIL_CM)
    _bordas(celula, {lado: "single" for lado in ("top", "left", "bottom", "right")})
    primeiro = celula.paragraphs[0]
    primeiro.paragraph_format.line_spacing = 1.0
    primeiro.paragraph_format.space_before = Pt(6)
    _runs(primeiro, titulo, negrito_base=True)
    for texto in paragrafos:
        _paragrafo(celula, texto, WD_ALIGN_PARAGRAPH.JUSTIFY)


CM_MARGENS_CELULA = 0.45  # margens internas padrão do Word, 0,19 cm de cada lado, com folga
# Times New Roman do sistema para medir o texto; Liberation Serif tem as mesmas métricas.
FONTES_MEDIDA = {
    False: ["/mnt/c/Windows/Fonts/times.ttf", "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"],
    True: ["/mnt/c/Windows/Fonts/timesbd.ttf", "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"],
}
_fontes_carregadas = {}


def _cm(texto: str, negrito: bool) -> float:
    """Largura do texto em Times New Roman 10, em cm. Sem a fonte no sistema, estimativa por
    caractere (0,19 cm, conservadora)."""
    if negrito not in _fontes_carregadas:
        from PIL import ImageFont

        caminho = next((c for c in FONTES_MEDIDA[negrito] if Path(c).exists()), None)
        _fontes_carregadas[negrito] = ImageFont.truetype(caminho, 1000) if caminho else None
    fonte = _fontes_carregadas[negrito]
    texto = "".join(SOBRESCRITOS.get(c, c) for c in texto)
    if fonte is None:
        return len(texto) * 0.19
    return fonte.getlength(texto) / 1000 * TABELA_TAMANHO.pt / 72 * 2.54


def _medidas(celulas: list[list[str]]) -> tuple[list, list]:
    minimo, desejado = [], []
    for j in range(len(celulas[0])):
        palavra = max(_cm(w, True) for w in celulas[0][j].split())
        celula = max(_cm(linha[j], False) for linha in celulas[1:])
        minimo.append(palavra + CM_MARGENS_CELULA)
        desejado.append(max(celula, palavra) + CM_MARGENS_CELULA)
    return minimo, desejado


def _em_paisagem(celulas: list[list[str]]) -> bool:
    """A tabela vai em página paisagem (a RESS aceita retrato ou paisagem) quando suas células
    não cabem, cada uma numa linha, na largura útil do retrato."""
    return sum(_medidas(celulas)[1]) > LARGURA_UTIL_CM


def _larguras(celulas: list[list[str]], util: float) -> list:
    """Cada coluna recebe ao menos a palavra mais longa do cabeçalho (para não partir palavra) e
    o que sobra da largura útil vai em proporção ao que falta para a célula mais longa caber
    numa linha."""
    minimo, desejado = _medidas(celulas)
    if sum(desejado) <= util:
        larguras = [d * util / sum(desejado) for d in desejado]
    elif sum(minimo) >= util:
        larguras = [m * util / sum(minimo) for m in minimo]
    else:
        sobra = util - sum(minimo)
        falta = [d - m for d, m in zip(desejado, minimo)]
        larguras = [m + sobra * f / sum(falta) for m, f in zip(minimo, falta)]
    return [Cm(x) for x in larguras]


def _tabela(doc, t: dict) -> None:
    celulas = t["celulas"]
    numericas = [all(RE_NUMERICO.match(linha[j]) for linha in celulas[1:]) for j in range(len(celulas[0]))]
    larguras = _larguras(celulas, _largura_util(doc))

    _paragrafo(doc, t["titulo"], WD_ALIGN_PARAGRAPH.CENTER).paragraph_format.keep_with_next = True
    tabela = doc.add_table(rows=len(celulas), cols=len(celulas[0]))
    tabela.alignment = WD_TABLE_ALIGNMENT.CENTER
    tabela.autofit = False
    for j, largura in enumerate(larguras):
        tabela.columns[j].width = largura  # w:gridCol, que é o que o LibreOffice respeita
    for i, linha in enumerate(celulas):
        for j, texto in enumerate(linha):
            celula = tabela.cell(i, j)
            celula.width = larguras[j]
            p = celula.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(0)
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if numericas[j] else WD_ALIGN_PARAGRAPH.LEFT
            _runs(p, texto, tamanho=TABELA_TAMANHO, negrito_base=(i == 0))
            _bordas(celula, {lado: "nil" for lado in ("top", "left", "bottom", "right")})
    for celula in tabela.rows[0].cells:
        _bordas(celula, {"top": "single", "bottom": "single"})
    for celula in tabela.rows[-1].cells:
        _bordas(celula, {"bottom": "single"})
    tabela.rows[0]._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
    if t["notas"]:
        nota = _paragrafo(doc, t["notas"], WD_ALIGN_PARAGRAPH.CENTER)
        nota.paragraph_format.space_before = Pt(6)


def _figura(doc, imagem: Path, titulo: str, notas: str) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(imagem), width=Cm(LARGURA_UTIL_CM))
    _paragrafo(doc, titulo, WD_ALIGN_PARAGRAPH.CENTER).paragraph_format.keep_with_next = True
    _paragrafo(doc, notas, WD_ALIGN_PARAGRAPH.CENTER)


# ---------------------------------------------------------------- montagem


def montar_manuscrito(m: dict, tabelas: list[dict], legenda: tuple[str, str]) -> Document:
    doc = _documento(_sem_negrito(m["titulo"]))
    _paragrafo(doc, m["modalidade"], WD_ALIGN_PARAGRAPH.LEFT)
    _paragrafo(doc, m["titulo"], WD_ALIGN_PARAGRAPH.CENTER, negrito_base=True)
    for secao in m["secoes"]:
        nome, itens = secao["nome"], secao["itens"]
        if nome == "Aspectos éticos":
            if any(k != "paragrafo" for k, _ in itens):
                raise Divergencia("Subseção dentro de Aspectos éticos.")
            _quadro(doc, nome, [t for _, t in itens])
            continue
        _titulo_secao(doc, nome, 2)
        for tipo, texto in itens:
            if tipo == "subsecao":
                _titulo_secao(doc, texto, 3)
            elif nome == "Referências" or texto.startswith("**Palavras-chave:**"):
                _paragrafo(doc, texto, WD_ALIGN_PARAGRAPH.LEFT)
            else:
                _paragrafo(doc, texto, WD_ALIGN_PARAGRAPH.JUSTIFY, recuo=RECUO_CORPO)
    for t in tabelas:
        if t["suplementar"]:
            continue
        if not t["continuacao"]:
            _nova_pagina(doc, _em_paisagem(t["celulas"]))
        _tabela(doc, t)
    _nova_pagina(doc, False)
    _figura(doc, IMAGEM_FIGURA1, *legenda)
    return doc


def montar_suplementar(m: dict, tabelas: list[dict]) -> Document:
    doc = _documento(_sem_negrito(m["titulo"]))
    _paragrafo(doc, m["titulo"], WD_ALIGN_PARAGRAPH.CENTER, negrito_base=True)
    primeira = True
    for t in tabelas:
        if not t["suplementar"]:
            continue
        if primeira:
            _orientar(doc.sections[0], _em_paisagem(t["celulas"]))  # o título acompanha a 1ª tabela
        else:
            _nova_pagina(doc, _em_paisagem(t["celulas"]))
        primeira = False
        _tabela(doc, t)
    return doc


# ---------------------------------------------------------------- conferência dos .docx gravados


def _texto_paragrafo(p) -> str:
    return "".join(
        "".join(DE_VOLTA[c] for c in r.text) if r.font.superscript else r.text for r in p.runs
    )


def _elementos(caminho: Path) -> list:
    """O corpo do .docx relido, em ordem: ('p', texto) ou ('t', grade de textos de célula)."""
    doc = Document(str(caminho))
    saida = []
    for el in doc.element.body.iterchildren():
        if el.tag == qn("w:p"):
            p = next(p for p in doc.paragraphs if p._p is el)
            texto = _texto_paragrafo(p)
            if texto:
                saida.append(("p", texto))
        elif el.tag == qn("w:tbl"):
            t = next(t for t in doc.tables if t._tbl is el)
            saida.append(("t", [["\n".join(_texto_paragrafo(p) for p in c.paragraphs) for c in r.cells] for r in t.rows]))
    return saida


def _esperado_tabela(t: dict) -> list:
    return [("p", _sem_negrito(t["titulo"])), ("t", t["celulas"])] + ([("p", t["notas"])] if t["notas"] else [])


def esperado_manuscrito(m, tabelas, legenda) -> list:
    saida = [("p", _sem_negrito(m["modalidade"])), ("p", _sem_negrito(m["titulo"]))]
    for s in m["secoes"]:
        if s["nome"] == "Aspectos éticos":
            saida.append(("t", [["\n".join([s["nome"]] + [_sem_negrito(t) for _, t in s["itens"]])]]))
            continue
        saida.append(("p", s["nome"]))
        saida += [("p", _sem_negrito(t)) for _, t in s["itens"]]
    for t in tabelas:
        if not t["suplementar"]:
            saida += _esperado_tabela(t)
    saida += [("p", _sem_negrito(legenda[0])), ("p", legenda[1])]
    return saida


def esperado_suplementar(m, tabelas) -> list:
    saida = [("p", _sem_negrito(m["titulo"]))]
    for t in tabelas:
        if t["suplementar"]:
            saida += _esperado_tabela(t)
    return saida


def _numeros(elementos: list) -> Counter:
    c = Counter()
    for tipo, conteudo in elementos:
        textos = [conteudo] if tipo == "p" else [x for linha in conteudo for x in linha]
        for texto in textos:
            c.update(RE_NUMERO.findall(texto))
    return c


def _numeros_brutos(*textos: str) -> Counter:
    c = Counter()
    for texto in textos:
        c.update(RE_NUMERO.findall(re.sub(r"<!--.*?-->", "", texto, flags=re.S)))
    return c


def conferir_docx(caminho: Path, esperado: list, numeros_fonte: Counter, csvs: dict) -> list:
    lidos = _elementos(caminho)
    for i, (a, b) in enumerate(zip(lidos, esperado)):
        if a != b:
            raise Divergencia(f"{caminho.name}, elemento {i}: o .docx diverge da fonte.\n  docx:  {str(a)[:300]}\n  fonte: {str(b)[:300]}")
    if len(lidos) != len(esperado):
        raise Divergencia(f"{caminho.name}: {len(lidos)} elementos no .docx, {len(esperado)} na fonte.")
    numeros_docx = _numeros(lidos)
    if numeros_docx != numeros_fonte:
        raise Divergencia(
            f"{caminho.name}: números diferentes dos arquivos-fonte.\n"
            f"  só no docx:  {dict(numeros_docx - numeros_fonte)}\n  só na fonte: {dict(numeros_fonte - numeros_docx)}"
        )
    for tipo, grade in lidos:
        if tipo == "t" and len(grade[0]) > 1:
            nome, linhas = csvs[tuple(grade[0])]
            if grade != linhas:
                raise Divergencia(f"{caminho.name}: tabela diverge de {nome}.")
    return lidos


def conferir_palavras(lidos: list, texto_md: str) -> int:
    trecho = texto_md[texto_md.index(f"## {CORPO_INICIO}"):]
    fim = trecho.find("\n## ", trecho.index(f"\n## {CORPO_FIM}") + 1)
    n_md = conta_palavras(trecho[:fim])
    paragrafos = [x for tipo, x in lidos if tipo == "p"]
    inicio = paragrafos.index(CORPO_INICIO)
    proxima = SECOES_ESPERADAS[SECOES_ESPERADAS.index(CORPO_FIM) + 1]
    n_docx = conta_palavras(" ".join(paragrafos[inicio:paragrafos.index(proxima)]))
    if n_docx != n_md:
        raise Divergencia(f"Corpo com {n_docx} palavras no .docx e {n_md} no .md.")
    return n_docx


def _identificadores() -> list[str]:
    """Nomes, ORCID iD e afiliações da tabela de autores de dados_submissao.md, mais o endereço,
    o usuário do repositório e o autor dos commits."""
    proibidos = []
    texto = DADOS_SUBMISSAO.read_text(encoding="utf-8")
    secao = texto.split("## Autores", 1)[1].split("\n## ", 1)[0]
    for linha in secao.splitlines():
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        if len(celulas) != 4 or not celulas[0].isdigit():
            continue
        _, nome, orcid, afiliacao = celulas
        partes = nome.split()
        proibidos += [nome, orcid, orcid.rsplit("/", 1)[-1], afiliacao.split(",")[0]]
        proibidos += [p for p in partes if len(p) > 3]
        proibidos.append(f"{partes[-1]} {''.join(p[0] for p in partes[:-1])}")  # «Sobrenome AB» (CRediT)
    if len(proibidos) < 2:
        raise Divergencia(f"Não achei a tabela de autores em {DADOS_SUBMISSAO.name}.")
    for comando in (["git", "remote", "get-url", "origin"], ["git", "config", "user.email"], ["git", "config", "user.name"]):
        r = subprocess.run(comando, cwd=ROOT, capture_output=True, text=True)
        valor = r.stdout.strip().removesuffix(".git")
        if valor:
            proibidos.append(valor)
            if "github.com/" in valor:
                proibidos += valor.split("github.com/", 1)[1].split("/")
    return sorted(set(proibidos), key=str.lower)


def conferir_anonimato(caminho: Path, proibidos: list[str]) -> None:
    with zipfile.ZipFile(caminho) as z:
        partes = {n: z.read(n).decode("utf-8", "replace") for n in z.namelist() if n.endswith((".xml", ".rels"))}
    achados = [
        (termo, nome)
        for nome, conteudo in partes.items()
        for termo in proibidos
        if termo.lower() in re.sub(r"<[^>]+>", "", conteudo).lower() or termo.lower() in conteudo.lower()
    ]
    if achados:
        raise Divergencia(f"{caminho.name} identifica autoria: {achados}")


# ---------------------------------------------------------------- PDF


def converter_pdf(docx: Path, pasta: Path) -> str:
    """Converte o .docx em PDF dentro de `pasta` e devolve a descrição do caminho usado."""
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if soffice:
        versao = subprocess.run([soffice, "--version"], capture_output=True, text=True).stdout.strip()
        # Perfil descartável: não depende nem altera o perfil do usuário, e não colide com uma
        # instância do LibreOffice já aberta.
        with tempfile.TemporaryDirectory() as perfil:
            r = subprocess.run(
                [soffice, f"-env:UserInstallation={Path(perfil).as_uri()}", "--headless",
                 "--convert-to", "pdf", "--outdir", str(pasta), str(docx)],
                capture_output=True, text=True, timeout=600,
            )
        if r.returncode != 0 or not (pasta / f"{docx.stem}.pdf").exists():
            raise Divergencia(f"LibreOffice não converteu {docx.name}: {r.stderr.strip() or r.stdout.strip()}")
        return f"LibreOffice headless ({' '.join(versao.split()[:2])})"
    pandoc = shutil.which("pandoc")
    motor = next((m for m in ("xelatex", "lualatex", "pdflatex") if shutil.which(m)), None)
    if pandoc and motor:
        r = subprocess.run(
            [pandoc, str(docx), "-o", str(pasta / f"{docx.stem}.pdf"), f"--pdf-engine={motor}"],
            capture_output=True, text=True, timeout=600,
        )
        if r.returncode != 0:
            raise Divergencia(f"pandoc não converteu {docx.name}: {r.stderr.strip()}")
        return f"pandoc com {motor} (sem LibreOffice; paginação diferente da do Word)"
    raise Divergencia("Nenhum conversor para PDF: falta LibreOffice (soffice) e pandoc com motor LaTeX.")


def _poppler(*args: str) -> str:
    programa = shutil.which(args[0])
    if not programa:
        raise Divergencia(f"Falta {args[0]} (poppler-utils) para conferir os PDF.")
    r = subprocess.run([programa, *args[1:]], capture_output=True, text=True)
    if r.returncode != 0:
        raise Divergencia(f"{args[0]} falhou: {r.stderr.strip()}")
    return r.stdout


def conferir_metadados_pdf(pdf: Path, titulo: str, proibidos: list[str]) -> dict:
    info = {}
    for linha in _poppler("pdfinfo", str(pdf)).splitlines():
        chave, _, valor = linha.partition(":")
        info[chave.strip()] = valor.strip()
    xmp = _poppler("pdfinfo", "-meta", str(pdf))
    problemas = []
    if info.get("Author"):
        problemas.append(f"Author preenchido: {info['Author']!r}")
    if info.get("Title") != titulo:
        problemas.append(f"Title diferente do título do artigo: {info.get('Title')!r}")
    pessoais = proibidos + [str(Path.home()), getpass.getuser()]
    for campo in ("Creator", "Producer", "Subject", "Keywords"):
        valor = info.get(campo, "")
        if re.search(r"[/\\]", valor):
            problemas.append(f"{campo} com caminho de arquivo: {valor!r}")
        problemas += [f"{campo} contém {t!r}" for t in pessoais if t.lower() in valor.lower()]
    texto = _poppler("pdftotext", str(pdf), "-")
    for origem, conteudo in (("texto", texto), ("XMP", xmp), ("metadados", "\n".join(info.values()))):
        problemas += [f"{origem} contém {t!r}" for t in pessoais if t.lower() in conteudo.lower()]
    if problemas:
        raise Divergencia(f"{pdf.name} pode identificar autoria: {sorted(set(problemas))}")
    return info


def conferir_paginacao_pdf(pdf: Path, rotulos: list[str], ultima_secao: str | None) -> list:
    """Página em que cada ilustração começa (pelo título «Rótulo N.» no início da linha) e
    quantas páginas ocupa até a próxima ilustração ou o fim do arquivo."""
    paginas = _poppler("pdftotext", "-layout", str(pdf), "-").split("\f")
    if paginas and not paginas[-1].strip():
        paginas.pop()
    inicio_busca = 0
    if ultima_secao:  # as ilustrações vêm depois das referências
        inicio_busca = next(
            (i for i, p in enumerate(paginas) if re.search(rf"^\s*{ultima_secao}\s*$", p, re.M)), None
        )
        if inicio_busca is None:
            raise Divergencia(f"{pdf.name}: não achei a seção {ultima_secao}.")
    inicios = []
    for rotulo in rotulos:
        padrao = re.compile(rf"^\s*{re.escape(rotulo)}\.", re.M)
        pagina = next((i for i in range(inicio_busca, len(paginas)) if padrao.search(paginas[i])), None)
        if pagina is None:
            raise Divergencia(f"{pdf.name}: não achei o título de {rotulo}.")
        if inicios and pagina <= inicios[-1][1]:
            raise Divergencia(f"{pdf.name}: {rotulo} começa na mesma página da ilustração anterior.")
        inicios.append((rotulo, pagina))
        inicio_busca = pagina
    spans = []
    for k, (rotulo, pagina) in enumerate(inicios):
        fim = inicios[k + 1][1] if k + 1 < len(inicios) else len(paginas)
        n = fim - pagina
        limite = 1 if rotulo.startswith("Figura") else 2
        if n > limite:
            raise Divergencia(f"{pdf.name}: {rotulo} ocupa {n} páginas; a RESS admite {limite}.")
        spans.append((rotulo, pagina + 1, n))
    return len(paginas), spans


def gerar_pdfs(m: dict, tabelas: list[dict], proibidos: list[str]) -> list:
    rotulos_principais = [
        re.match(r"\*\*(Tabela \d+)\.\*\*", t["titulo"]).group(1)
        for t in tabelas if not t["suplementar"] and not t["continuacao"]
    ] + ["Figura 1"]
    rotulos_supl = [re.match(r"\*\*(Tabela suplementar \d+)\.\*\*", t["titulo"]).group(1)
                    for t in tabelas if t["suplementar"]]
    titulo = _sem_negrito(m["titulo"])
    relatorio = []
    with tempfile.TemporaryDirectory() as pasta:
        pasta = Path(pasta)
        convertidos = []
        for docx, rotulos, ultima in (
            (SAIDA_MANUSCRITO, rotulos_principais, SECOES_ESPERADAS[-1]),
            (SAIDA_SUPLEMENTAR, rotulos_supl, None),
        ):
            caminho = converter_pdf(docx, pasta)
            pdf = pasta / f"{docx.stem}.pdf"
            info = conferir_metadados_pdf(pdf, titulo, proibidos)
            n_paginas, spans = conferir_paginacao_pdf(pdf, rotulos, ultima)
            convertidos.append(pdf)
            relatorio.append((SAIDA_DIR / pdf.name, caminho, n_paginas, spans, info))
        for pdf in convertidos:
            shutil.move(str(pdf), SAIDA_DIR / pdf.name)
    return relatorio


# ---------------------------------------------------------------- principal


def main() -> int:
    try:
        texto_md = conferir_versao_submissao()
        m = ler_manuscrito(texto_md)
        notas = conferir_requisitos(m, texto_md)
        csvs = ler_csvs()
        tabelas = ler_tabelas(csvs)
        legenda = ler_legenda_figura1()
        conferir_citacoes(m, tabelas)

        texto_tabelas = TABELAS_MD.read_text(encoding="utf-8")
        pedacos = re.split(r"^---$", re.sub(r"<!--.*?-->", "", texto_tabelas, flags=re.S), flags=re.M)[1:]
        supl = [p for p in pedacos if "**Tabela suplementar" in p]
        principais = [p for p in pedacos if "**Tabela suplementar" not in p]
        legenda_bruta = re.sub(r"<!--.*?-->", "", LEGENDA_FIGURA1.read_text(encoding="utf-8"), flags=re.S).split("\n## ", 1)[0]
        legenda_bruta = re.sub(r"^# .*$", "", legenda_bruta, flags=re.M)  # «# Figura 1 — legenda» rotula o arquivo
        titulo_bruto = "# " + m["titulo"]
        proibidos = _identificadores()

        SAIDA_DIR.mkdir(parents=True, exist_ok=True)
        resultados = {}
        for destino, doc, esperado, numeros in (
            (
                SAIDA_MANUSCRITO,
                montar_manuscrito(m, tabelas, legenda),
                esperado_manuscrito(m, tabelas, legenda),
                _numeros_brutos(texto_md, *principais, legenda_bruta),
            ),
            (
                SAIDA_SUPLEMENTAR,
                montar_suplementar(m, tabelas),
                esperado_suplementar(m, tabelas),
                _numeros_brutos(titulo_bruto, *supl),
            ),
        ):
            temporario = destino.with_suffix(".tmp.docx")
            doc.save(temporario)
            try:
                lidos = conferir_docx(temporario, esperado, numeros, csvs)
                conferir_anonimato(temporario, proibidos)
            except Divergencia:
                temporario.unlink()
                raise
            resultados[destino] = (temporario, lidos)

        n_corpo = conferir_palavras(resultados[SAIDA_MANUSCRITO][1], texto_md)
        for destino, (temporario, _) in resultados.items():
            os.replace(temporario, destino)
        pdfs = gerar_pdfs(m, tabelas, proibidos)
    except Divergencia as erro:
        print(f"PAROU: {erro}", file=sys.stderr)
        return 1

    n_tab = sum(1 for t in tabelas if not t["suplementar"] and not t["continuacao"])
    n_supl = sum(1 for t in tabelas if t["suplementar"])
    print(f"OK -- {SAIDA_MANUSCRITO.relative_to(ROOT)}: {n_tab} tabelas, 1 figura, "
          f"{m['n_referencias']} referências; resumo com {m['n_resumo']} palavras; corpo com {n_corpo} palavras.")
    print(f"OK -- {SAIDA_SUPLEMENTAR.relative_to(ROOT)}: {n_supl} tabelas suplementares.")
    print(f"Conferidos: texto e números contra as fontes, tabelas contra {len(csvs)} CSVs, "
          f"ausência de {len(proibidos)} identificadores de autoria.")
    for pdf, caminho, n_paginas, spans, info in pdfs:
        ilustracoes = "; ".join(f"{r} p. {p}" + (f"-{p + n - 1}" if n > 1 else "") for r, p, n in spans)
        print(f"OK -- {pdf.relative_to(ROOT)}: {n_paginas} páginas, por {caminho}. {ilustracoes}.")
        print(f"      metadados: Title={info.get('Title')!r} Author={info.get('Author', '')!r} "
              f"Creator={info.get('Creator')!r} Producer={info.get('Producer')!r}")
    for nota in notas:
        print(f"NOTA: {nota}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
