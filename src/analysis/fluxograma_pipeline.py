"""Gera a Figura 1 do capítulo (fluxograma do pipeline: fontes -> módulos ->
produtos intermediários -> portal/figuras), citada em publicacoes/
cap_geotecnologias/02_texto/10_versao_ecd_revisada.md ("Figura 1.
Fluxograma do fluxo geotecnológico...", embutida com `width=15cm`).

Não havia nenhum módulo-fonte para essa figura: o PNG foi commitado como
binário no commit fd45952, sem `.py` companheiro em lugar nenhum do
repositório ou do histórico do git. Este módulo fecha essa lacuna.

## Regra de tamanho de fonte (por nível hierárquico, nunca por caixa)

Import ante: a figura é sempre reproduzida no capítulo a `width=15cm`,
qualquer que seja o tamanho nativo em que este script desenha (300 dpi,
mas a largura nativa em polegadas quase nunca é 15 cm exatos, porque o
conteúdo -- 6 colunas na Etapa 1-3, caixas largas na Etapa 4 -- dita a
largura). Um `fontsize=9` do matplotlib é uma medida física (pontos = 1/72
polegada) *na imagem nativa*; ao reamostrar a imagem inteira para 15 cm de
largura, esse texto encolhe pelo mesmo fator que a imagem inteira. Por
isso NENHUM tamanho de fonte é escolhido diretamente em pontos nativos
aqui -- cada nível hierárquico (cabeçalho de etapa / conteúdo de caixa)
tem um tamanho-ALVO definido em pontos *já na reprodução de
15 cm* (`FONTE_..._15CM` abaixo), e o tamanho nativo usado no desenho é
derivado (`_pt_nativo`) multiplicando esse alvo pelo fator de ampliação
(largura nativa ÷ 15 cm) -- o inverso exato do encolhimento que a
reprodução vai aplicar depois. O resultado: o tamanho poderia crescer à
vontade em polegadas nativas (a caixa "aumenta" para caber, nunca a
fonte encolhe) e ainda assim a Figura 1, impressa a 15 cm, sempre mostra
exatamente os pontos-alvo -- ambos os níveis ficam acima do piso de 7pt
a 15cm (`MIN_PT_15CM_EXIGIDO`), verificado em `main()`.

Cada caixa mede a largura real do texto (via `renderer.get_window_extent`)
no tamanho nativo já determinado pelo nível hierárquico da caixa -- nunca
reduz esse tamanho para caber. Se uma linha não couber na largura da
caixa, `main()` levanta `ValueError` nomeando a caixa e a linha ofensora
(ver `_caixa`) -- índice, não silêncio. A mitigação correta, quando isso
acontece, é encurtar o texto ou alargar a coluna, nunca reduzir a fonte.

Todo conteúdo de caixa (fora cabeçalhos) é limitado a no máximo duas
linhas curtas (`MAX_LINHAS_CAIXA`). A figura contém só o diagrama --
caixas, setas e rótulos de etapa -- sem bloco de notas/legenda ao final:
o detalhe que não cabe em duas linhas curtas fica fora da figura, não
vira uma terceira linha nem uma fonte menor.

## Conteúdo: por que a Etapa 3 tem três ramos

Investigação desta sessão (perguntas respondidas por leitura de código,
não por inferência do nome do arquivo) confirmou que `fetch_coredes.py` e
`fetch_regioes_ibge.py` são fontes a montante, não uma agregação a
jusante:
- `municipio_corede.csv` (497 municípios, 28 COREDEs, 9 regiões
  funcionais -- contagem batida por leitura do CSV, confere com o
  capítulo) vem do Atlas Socioeconômico do RS, mantido pela SEPLAG/RS
  (`fetch_coredes.URL_XLSX`), planilha .xlsx sem API -- não é fonte IBGE.
  A planilha NÃO declara internamente (célula, aba, comentário, cabeçalho/
  rodapé de impressão, metadado OOXML custom) nenhuma data de vigência da
  divisão regional -- achado à parte, registrado em
  `outputs/tables/proveniencia_dados_brutos.csv` (coluna `aviso`), não
  nesta figura.
- `municipio_regioes_ibge.csv` vem do IBGE, pela MESMA API de localidades
  já usada por `fetch_malha_municipios.py` (`URL_LOCALIDADES`) -- resposta
  já traz `regiao-imediata`/`regiao-intermediaria` aninhados, sem endpoint
  adicional.
- Nenhum dos dois é importado por `tabela_agregacao_regional.py` como
  módulo Python -- este só lê, via `pd.read_csv`, os CSVs que aqueles
  scripts gravam em disco (mesmo padrão de `fetch_populacao.py`/
  `fetch_malha_municipios.py` com os demais módulos de Etapa 1-3).

Por isso a Etapa 3 (renomeada -- "Malha" já não descreve o conteúdo) tem
três ramos de coleta em paralelo (malha, região intermediária, COREDE), e
a caixa de `tabela_agregacao_regional.py` não repete "COREDE (28) / região
(8)" -- essa informação já está nas caixas de origem da Etapa 3.
`fetch_regioes_ibge.py`/`fetch_coredes.py` alimentam diretamente a
terceira coluna da Etapa 4 (`tabela_agregacao_regional.py`), sem passar
pela Junção nem pelo piso -- na Junção só entram malha, população e
tabelas de casos; regiões/COREDE só são cruzados com o município dentro
de `tabela_agregacao_regional.py`, depois do piso já aplicado ao dado
municipal.

Divergências identificadas mas NÃO corrigidas aqui, por ficarem fora do
escopo desta figura (texto do capítulo, não fluxo de dados):
- 04_metodo.md (rascunho v3) ainda registra "enquanto o portal não
  aplicar o piso..." -- desatualizado pela mudança em build_site_data.py.
- 10_versao_ecd_revisada.md diz "três fontes públicas" e lista quatro.
Reportadas, não implementadas.

Uso: python -m src.analysis.fluxograma_pipeline
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from PIL import Image

FIGURAS_DIR = (
    Path(__file__).resolve().parent.parent.parent / "publicacoes" / "cap_geotecnologias" / "03_figuras"
)
CAMINHO_SAIDA = FIGURAS_DIR / "figura1_fluxograma.png"

# PDF vetorial para a submissão à Reciis (pasta fora do versionamento, ver
# CLAUDE.md "Convenções de commit" -- gerado aqui a partir do mesmo desenho,
# não convertido do PNG.
FIGURAS_DIR_RECIIS = (
    Path(__file__).resolve().parent.parent.parent / "publicacoes" / "artigo_reciis" / "03_submissao" / "figuras"
)
CAMINHO_SAIDA_PDF = FIGURAS_DIR_RECIIS / "figura1_fluxograma.pdf"

DPI = 300
LARGURA_REPRODUCAO_CM = 15.0
LARGURA_REPRODUCAO_IN = LARGURA_REPRODUCAO_CM / 2.54

# --- Tamanhos-alvo por nível hierárquico, JÁ na reprodução de 15 cm (ver
# docstring do módulo) -- nunca um tamanho nativo direto. ---
FONTE_HEADER_15CM = 11.0
FONTE_CAIXA_15CM = 9.0
MIN_PT_15CM_EXIGIDO = 7.0

MAX_LINHAS_CAIXA = 2

LINESPACING = 1.30
PAD_V_IN = 0.14  # polegadas nativas de folga vertical total (topo+base) por caixa
PAD_H_FRAC = 0.90  # fração da largura da caixa disponível para o texto

# Paleta amostrada do PNG original (mesma linguagem visual: bege claro para
# fonte/dado bruto, bege escuro para produto tabular intermediário, branco
# para módulo/script, cinza-escuro para artefato final publicado).
COR_BORDA = "#1a1a1a"
COR_FONTE_CLARA = "#e8e6e1"
COR_PRODUTO_TABULAR = "#d3d0c8"
COR_SCRIPT = "#ffffff"
COR_ARTEFATO_FINAL = "#4a4a4a"
COR_TEXTO_ARTEFATO_FINAL = "#ffffff"
COR_TEXTO = "#111111"
COR_SETA = "#333333"

# --- Layout: coordenadas em polegadas nativas (== unidades de dados dos
# eixos), y cresce para baixo (ylim invertido). Todas as colunas de
# conteúdo (incl. o ramo de proveniência, COL0) têm a MESMA largura --
# nível hierárquico único também vale para o layout, não só a fonte: uma
# coluna mais larga só para caber um nome de arquivo violaria a mesma
# regra de "não adapte a exceção, encurte o conteúdo". ---
LARGURA_COL = 2.30
GAP = 0.16

COL0 = (0.0, LARGURA_COL)  # ramo de proveniência
_c1x0 = COL0[1] + GAP
COL1 = (_c1x0, _c1x0 + LARGURA_COL)
COL2 = (COL1[1] + GAP, COL1[1] + GAP + LARGURA_COL)
COL3 = (COL2[1] + GAP, COL2[1] + GAP + LARGURA_COL)  # Etapa 3a -- malha
COL4 = (COL3[1] + GAP, COL3[1] + GAP + LARGURA_COL)  # Etapa 3b -- região intermediária
COL5 = (COL4[1] + GAP, COL4[1] + GAP + LARGURA_COL)  # Etapa 3c -- COREDE
COLS_COLETA = [COL1, COL2, COL3, COL4, COL5]

SPAN_JUNCAO = (COL1[0], COL3[1])          # Junção/CSV/Piso: só casos+população+malha
SPAN_ETAPA3 = (COL3[0], COL5[1])          # cabeçalho combinado da Etapa 3
SPAN_BRANCH3 = (COL4[0], COL5[1])         # Etapa 4, terceiro ramo (regional)
SPAN_TOTAL = (COL1[0], COL5[1])           # cabeçalho da Etapa 4


def _centro(col):
    return (col[0] + col[1]) / 2


def _largura(col):
    return col[1] - col[0]


class ErroCaixaNaoCabe(ValueError):
    pass


def _medir_largura_max(fig, ax, renderer, linhas, fontsize, fontfamily, fontweight="normal"):
    larguras = []
    for linha in linhas:
        t = ax.text(0, 0, linha, fontsize=fontsize, fontfamily=fontfamily, fontweight=fontweight)
        bb = t.get_window_extent(renderer=renderer)
        larguras.append(bb.width / fig.dpi)
        t.remove()
    return larguras


def _caixa(fig, ax, renderer, nome, cx, cy, w, linhas, facecolor, fontsize_native, textcolor=COR_TEXTO,
           fontfamily="sans-serif", negrito=False, linewidth=1.3):
    """Desenha uma caixa de cantos arredondados com texto centralizado.
    A altura é CALCULADA a partir do número de linhas e do tamanho de
    fonte nativo (nunca o inverso) -- é a caixa que cresce para caber o
    texto no tamanho de fonte do seu nível hierárquico, nunca a fonte que
    encolhe para caber na caixa. clip_on=False no patch e no texto: sem
    isso, uma caixa cujo canto caia perto do xlim tem o arredondamento
    cortado em linha reta pelo clipping da área de plotagem (bug do PNG
    anterior).

    Levanta ErroCaixaNaoCabe, nomeando `nome` e a linha, se alguma linha
    não couber horizontalmente em `w` no tamanho de fonte nativo -- nunca
    reduz a fonte para evitar o erro (ver docstring do módulo)."""
    if len(linhas) > MAX_LINHAS_CAIXA:
        raise ErroCaixaNaoCabe(
            f"Caixa '{nome}': {len(linhas)} linhas > máximo de {MAX_LINHAS_CAIXA}. "
            "Encurte o texto."
        )

    larguras = _medir_largura_max(fig, ax, renderer, linhas, fontsize_native, fontfamily,
                                   "bold" if negrito else "normal")
    disponivel = w * PAD_H_FRAC
    for linha, largura in zip(linhas, larguras):
        if largura > disponivel:
            raise ErroCaixaNaoCabe(
                f"Caixa '{nome}': linha {linha!r} mede {largura:.3f}in a {fontsize_native:.1f}pt nativos, "
                f"mas só há {disponivel:.3f}in disponíveis (caixa de {w:.3f}in de largura). "
                "Encurte esta linha -- não é permitido reduzir a fonte."
            )

    n = len(linhas)
    line_h_in = fontsize_native * LINESPACING / 72.0
    h = n * line_h_in + PAD_V_IN

    patch = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0,rounding_size=0.055",
        facecolor=facecolor, edgecolor=COR_BORDA, linewidth=linewidth,
        clip_on=False, zorder=2,
    )
    ax.add_patch(patch)

    y0 = cy - (n - 1) * line_h_in / 2
    for i, linha in enumerate(linhas):
        ax.text(
            cx, y0 + i * line_h_in, linha, ha="center", va="center",
            fontsize=fontsize_native, fontweight="bold" if negrito else "normal", fontfamily=fontfamily,
            color=textcolor, zorder=3, clip_on=False,
        )
    return h


def _texto_livre(fig, ax, renderer, nome, cx, cy, w, linhas, fontsize_native, fontweight="bold",
                  fontfamily="sans-serif", color=COR_TEXTO, style="normal", ha="center", fundo_opaco=False):
    """Texto solto (sem caixa) -- cabeçalhos de etapa. Mesma checagem de
    largura de _caixa (sem limite de linhas: cabeçalhos já são só 2 por
    design).

    fundo_opaco=True desenha um retângulo branco sem borda atrás do texto
    (zorder entre as setas e o texto) -- usado só pelo cabeçalho "ETAPA 4",
    que fica na mesma faixa vertical das setas que saem do piso populacional
    e sobem/descem para os três ramos (nenhuma altura de linha entre as
    fileiras fica livre de seta na largura toda do cabeçalho, ver docstring
    de _desenhar) -- sem isso, as setas atravessariam visualmente o texto."""
    larguras = _medir_largura_max(fig, ax, renderer, linhas, fontsize_native, fontfamily, fontweight)
    disponivel = w * 0.98
    for linha, largura in zip(linhas, larguras):
        if largura > disponivel:
            raise ErroCaixaNaoCabe(
                f"Texto '{nome}': linha {linha!r} mede {largura:.3f}in a {fontsize_native:.1f}pt nativos, "
                f"mas só há {disponivel:.3f}in disponíveis. Encurte o texto."
            )
    if fundo_opaco:
        n = len(linhas)
        largura_mascara = max(larguras) * 1.08
        altura_mascara = n * fontsize_native * LINESPACING / 72.0 * 1.15
        ax.add_patch(plt.Rectangle(
            (cx - largura_mascara / 2, cy - altura_mascara / 2), largura_mascara, altura_mascara,
            facecolor="white", edgecolor="none", zorder=1.5, clip_on=False,
        ))
    ax.text(
        cx, cy, "\n".join(linhas), ha=ha, va="center", fontsize=fontsize_native,
        fontweight=fontweight, fontfamily=fontfamily, color=color, style=style,
        zorder=3, clip_on=False, linespacing=LINESPACING,
    )
    n = len(linhas)
    return n * fontsize_native * LINESPACING / 72.0


def _altura_caixa(n_linhas: int, fontsize_native: float) -> float:
    """Altura de uma caixa com n_linhas no tamanho de fonte nativo dado --
    calculada ANTES de desenhar (mesma fórmula usada dentro de _caixa),
    para que o layout possa posicionar cada linha do fluxograma pela
    altura real da anterior, em vez de só metade dela (bug corrigido nesta
    rodada: metade da altura, sozinha, subestima o espaço ocupado pela
    própria caixa e as caixas ficam empilhadas umas sobre as outras)."""
    return n_linhas * fontsize_native * LINESPACING / 72.0 + PAD_V_IN


def _altura_texto(n_linhas: int, fontsize_native: float) -> float:
    """Mesma ideia de _altura_caixa, para texto solto (sem PAD_V -- não há
    caixa/preenchimento, só a altura das linhas)."""
    return n_linhas * fontsize_native * LINESPACING / 72.0


def _seta(ax, de, para, tracejada=False):
    ax.annotate(
        "", xy=para, xytext=de,
        arrowprops=dict(
            arrowstyle="-|>", color=COR_SETA, lw=1.3,
            linestyle="dashed" if tracejada else "solid",
            shrinkA=0, shrinkB=0, mutation_scale=14,
        ),
        annotation_clip=False, zorder=1,
    )


def _desenhar(fig, ax, renderer, fontes_nativas) -> float:
    f_header = fontes_nativas["header"]
    f_caixa = fontes_nativas["caixa"]

    GAP_V = 0.35  # folga vertical padrão entre linhas do fluxograma

    def caixa(nome, *args, **kwargs):
        return _caixa(fig, ax, renderer, nome, *args, fontsize_native=f_caixa, **kwargs)

    def header(nome, *args, **kwargs):
        return _texto_livre(fig, ax, renderer, nome, *args, fontsize_native=f_header, **kwargs)

    # y é sempre o TOPO da próxima linha (nunca um centro) -- cada bloco:
    # (1) calcula a própria altura ANTES de desenhar (_altura_caixa/
    # _altura_texto, puras, sem precisar desenhar nada primeiro), (2)
    # desenha centrado em y + altura/2, (3) avança y por altura inteira +
    # GAP_V. Bug corrigido nesta rodada: a versão anterior avançava só
    # METADE da altura a cada linha (esquecendo que "y" ali era um centro,
    # não um topo), e as linhas do fluxograma saíam empilhadas umas sobre
    # as outras.
    # y=0 (não uma folga extra) -- a folga simétrica das quatro bordas já
    # vem inteira de margem_pol (ver gerar_fluxograma); somar uma folga
    # aqui também duplicaria a margem só do lado de cima (bug corrigido
    # nesta rodada -- media 235px no topo contra 112px na base antes desta
    # correção).
    y = 0.0

    # --- Cabeçalhos: Etapa 1, Etapa 2, Etapa 3 (combinado, 3 colunas) ---
    h_header1 = _altura_texto(2, f_header)
    for col, titulo in zip([COL1, COL2], [["ETAPA 1", "Coleta"], ["ETAPA 2", "Censo"]]):
        header(f"cabeçalho {titulo[0]}", _centro(col), y + h_header1 / 2, _largura(col), titulo)
    header("cabeçalho ETAPA 3", _centro(SPAN_ETAPA3), y + h_header1 / 2, _largura(SPAN_ETAPA3),
           ["ETAPA 3", "Malha e regiões"])
    y += h_header1 + GAP_V

    # --- Fontes de dado bruto (bege claro), 5 colunas ---
    fontes = [
        (COL1, ["SSP/RS", "(violência)"]),
        (COL2, ["IBGE", "(SIDRA)"]),
        (COL3, ["IBGE", "(malha)"]),
        (COL4, ["IBGE", "(regiões)"]),
        (COL5, ["SEPLAG/RS", "(COREDE)"]),
    ]
    h_fonte = _altura_caixa(2, f_caixa)
    y_fonte = y
    for col, linhas in fontes:
        caixa(f"fonte {linhas[0]}", _centro(col), y_fonte + h_fonte / 2, _largura(col), linhas, COR_FONTE_CLARA)
    y += h_fonte + GAP_V

    # --- Scripts de coleta (branco, monoespaçado), 5 colunas ---
    # Nomes abreviados (sem o prefixo "fetch_" comum nem o sufixo ".py") --
    # os nomes completos não cabem em duas linhas curtas dentro da largura
    # de uma coluna no tamanho de fonte do nível "caixa" (ver docstring do
    # módulo).
    scripts = [
        (COL1, ["load_data"]),
        (COL2, ["populacao"]),
        (COL3, ["malha_", "municipios"]),
        (COL4, ["regioes_", "ibge"]),
        (COL5, ["coredes"]),
    ]
    h_script = max(_altura_caixa(len(l), f_caixa) for _, l in scripts)
    y_script = y
    cy_script = y_script + h_script / 2
    for col, linhas in scripts:
        caixa(f"script {linhas[-1]}", _centro(col), cy_script, _largura(col), linhas, COR_SCRIPT,
              fontfamily="monospace")

    # --- Ramo lateral de proveniência (COL0), alinhado às linhas de script/produto ---
    _seta(ax, (COL1[0] + 0.05, y_fonte + h_fonte * 0.65), (_centro(COL0), cy_script - h_script / 2 - 0.03),
          tracejada=True)
    caixa("script proveniência", _centro(COL0), cy_script, _largura(COL0), ["verifica", "origem"],
          COR_SCRIPT, fontfamily="monospace")
    y += h_script + GAP_V

    # --- Produtos tabulares intermediários (bege escuro), 5 colunas ---
    # Rótulos curtos e genéricos -- ver comentário equivalente na linha de
    # scripts, mesmo motivo.
    produtos = [
        (COL1, ["tabelas", "longas"]),
        (COL2, ["população", "(CSV)"]),
        (COL3, ["malha", "municipal"]),
        (COL4, ["regiões", "(CSV)"]),
        (COL5, ["COREDE", "(CSV)"]),
    ]
    h_prod = _altura_caixa(2, f_caixa)
    y_prod = y
    cy_prod = y_prod + h_prod / 2
    for col, linhas in produtos:
        caixa(f"produto {linhas[0]}", _centro(col), cy_prod, _largura(col), linhas, COR_PRODUTO_TABULAR)
        _seta(ax, (_centro(col), cy_script + h_script / 2), (_centro(col), cy_prod - h_prod / 2))

    caixa("saída proveniência", _centro(COL0), cy_prod, _largura(COL0), ["registro", "de origem"],
          COR_PRODUTO_TABULAR)
    _seta(ax, (_centro(COL0), cy_script + h_script / 2), (_centro(COL0), cy_prod - h_prod / 2))
    y += h_prod + GAP_V + 0.10

    # --- Convergência para a Junção: só casos + população + malha (COL1-COL3) ---
    h_juncao = _altura_caixa(2, f_caixa)
    y_juncao = y
    cy_juncao = y_juncao + h_juncao / 2
    for col in [COL1, COL2, COL3]:
        _seta(ax, (_centro(col), cy_prod + h_prod / 2), (_centro(SPAN_JUNCAO), cy_juncao - h_juncao / 2))
    caixa(
        "Junção", _centro(SPAN_JUNCAO), cy_juncao, _largura(SPAN_JUNCAO),
        ["Junção por código do IBGE (497/497)", "taxa = Σ casos ÷ Σ pessoas-ano"],
        COR_SCRIPT,
    )
    y += h_juncao + GAP_V

    # --- CSV consolidado de taxas ---
    h_taxa = _altura_caixa(2, f_caixa)
    y_taxa = y
    cy_taxa = y_taxa + h_taxa / 2
    caixa("CSV de taxas", _centro(SPAN_JUNCAO), cy_taxa, _largura(SPAN_JUNCAO),
          ["violencia_anual_", "municipio_taxa.csv"], COR_PRODUTO_TABULAR, fontfamily="monospace")
    _seta(ax, (_centro(SPAN_JUNCAO), cy_juncao + h_juncao / 2), (_centro(SPAN_JUNCAO), cy_taxa - h_taxa / 2))
    y += h_taxa + GAP_V

    # --- Piso populacional: passo compartilhado antes da bifurcação da Etapa 4 ---
    h_piso = _altura_caixa(2, f_caixa)
    y_piso = y
    cy_piso = y_piso + h_piso / 2
    caixa(
        "Piso populacional", _centro(SPAN_JUNCAO), cy_piso, _largura(SPAN_JUNCAO),
        ["Piso populacional ≥ 5.000 hab.", "266 elegíveis · 231 abaixo (497)"],
        COR_SCRIPT,
    )
    _seta(ax, (_centro(SPAN_JUNCAO), cy_taxa + h_taxa / 2), (_centro(SPAN_JUNCAO), cy_piso - h_piso / 2))
    y += h_piso + GAP_V + 0.10

    # --- Etapa 4: publicação, três ramos ---
    h_header4 = _altura_texto(1, f_header)
    cy_header4 = y + h_header4 / 2
    header("cabeçalho ETAPA 4", _centro(SPAN_TOTAL), cy_header4, _largura(SPAN_TOTAL), ["ETAPA 4 — Publicação"],
           fundo_opaco=True)
    y += h_header4 + GAP_V

    scripts4 = [
        (COL1, ["build_", "site_data"]),
        (COL2, ["figuras_", "capitulo"]),
    ]
    h_script4 = max(
        _altura_caixa(2, f_caixa),
        _altura_caixa(2, f_caixa),  # ramo 3 (tabela_agregacao_regional.py) também tem 2 linhas
    )
    y_script4 = y
    cy_script4 = y_script4 + h_script4 / 2
    for col, linhas in scripts4:
        caixa(f"script4 {linhas[0]}", _centro(col), cy_script4, _largura(col), linhas,
              COR_SCRIPT, fontfamily="monospace", negrito=True)
    caixa("script4 regional", _centro(SPAN_BRANCH3), cy_script4, _largura(SPAN_BRANCH3),
          ["tabela_agregacao_", "regional.py"], COR_SCRIPT, fontfamily="monospace", negrito=True)

    # Ramo 1 e 2 recebem o piso diretamente; ramo 3 recebe o piso E os dois
    # ramos novos da Etapa 3 (região intermediária, COREDE) -- não passa
    # pela Junção nem pelo piso, ver docstring do módulo.
    _seta(ax, (_centro(SPAN_JUNCAO), cy_piso + h_piso / 2), (_centro(COL1), cy_script4 - h_script4 / 2))
    _seta(ax, (_centro(SPAN_JUNCAO), cy_piso + h_piso / 2), (_centro(COL2), cy_script4 - h_script4 / 2))
    _seta(ax, (_centro(SPAN_JUNCAO), cy_piso + h_piso / 2), (_centro(SPAN_BRANCH3), cy_script4 - h_script4 / 2))
    _seta(ax, (_centro(COL4), cy_prod + h_prod / 2), (_centro(COL4), cy_script4 - h_script4 / 2))
    _seta(ax, (_centro(COL5), cy_prod + h_prod / 2), (_centro(COL5), cy_script4 - h_script4 / 2))

    y += h_script4 + GAP_V

    saidas4 = [
        (COL1, ["Portal", "rampa+piso"]),
        (COL2, ["Figuras", "2 a 4"]),
    ]
    h_out4 = _altura_caixa(2, f_caixa)
    y_out4 = y
    cy_out4 = y_out4 + h_out4 / 2
    for col, linhas in saidas4:
        caixa(f"saída4 {linhas[0]}", _centro(col), cy_out4, _largura(col), linhas,
              COR_ARTEFATO_FINAL, textcolor=COR_TEXTO_ARTEFATO_FINAL)
        _seta(ax, (_centro(col), cy_script4 + h_script4 / 2), (_centro(col), cy_out4 - h_out4 / 2))
    caixa("saída4 regional", _centro(SPAN_BRANCH3), cy_out4, _largura(SPAN_BRANCH3),
          ["Tabela 1, Tabela 2", "Figura 5 (MAUP)"], COR_ARTEFATO_FINAL, textcolor=COR_TEXTO_ARTEFATO_FINAL)
    _seta(ax, (_centro(SPAN_BRANCH3), cy_script4 + h_script4 / 2), (_centro(SPAN_BRANCH3), cy_out4 - h_out4 / 2))

    y += h_out4

    return y


def _pt_nativo(pt_15cm: float, largura_nativa_in: float) -> float:
    """Converte um tamanho-alvo em pontos JÁ na reprodução de 15 cm para o
    tamanho nativo equivalente (ver docstring do módulo): a imagem inteira
    encolhe por (15cm / largura_nativa) quando reproduzida, então o
    tamanho nativo precisa ser o alvo dividido por esse fator."""
    fator_encolhimento = LARGURA_REPRODUCAO_IN / largura_nativa_in
    return pt_15cm / fator_encolhimento


def gerar_fluxograma(
    caminho_saida: Path = CAMINHO_SAIDA, caminho_saida_pdf: Path = CAMINHO_SAIDA_PDF, margem_pol: float = 0.25
) -> Path:
    """Desenha o fluxograma e grava em `caminho_saida` (PNG, 300 dpi) e em
    `caminho_saida_pdf` (PDF vetorial, mesmo desenho, para a submissão à
    Reciis) -- mesma figura matplotlib, dois `savefig`. margem_pol
    é a folga (em polegadas nativas) aplicada simetricamente nas quatro
    bordas via xlim/ylim -- não bbox_inches='tight' e não redução de escala
    do desenho: clip_on=False em todo patch/texto + limites dos eixos
    maiores que o conteúdo, nunca o inverso.

    A largura nativa é fixada pelas colunas (LARGURA_COL, GAP) ANTES de
    qualquer decisão de fonte -- não depende de texto, só da grade de
    layout -- o que permite derivar os tamanhos de fonte nativos (ver
    _pt_nativo) numa única passada, sem iteração."""
    largura_conteudo = SPAN_TOTAL[1] - COL0[0]  # == COL5[1], já que COL0[0] == 0
    largura_nativa_total = largura_conteudo + 2 * margem_pol

    fontes_nativas = {
        "header": _pt_nativo(FONTE_HEADER_15CM, largura_nativa_total),
        "caixa": _pt_nativo(FONTE_CAIXA_15CM, largura_nativa_total),
    }

    fig = plt.figure(figsize=(largura_nativa_total, 14.0), dpi=DPI)  # altura provisória
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-margem_pol, largura_conteudo + margem_pol)
    ax.set_ylim(14.0, -margem_pol)  # provisório, só para existir um renderer
    ax.set_axis_off()
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()

    y_max_conteudo = _desenhar(fig, ax, renderer, fontes_nativas)
    ax.set_ylim(y_max_conteudo + margem_pol, -margem_pol)

    altura_final = y_max_conteudo + 2 * margem_pol
    fig.set_size_inches(largura_nativa_total, altura_final)

    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(caminho_saida, dpi=DPI, facecolor="white")

    caminho_saida_pdf.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(caminho_saida_pdf, facecolor="white")

    plt.close(fig)
    return caminho_saida, fontes_nativas, largura_nativa_total, altura_final


def verificar_margens(caminho: Path, tolerancia_relativa: float = 0.35) -> dict:
    """Mede a distância do conteúdo (pixels não-brancos) até cada uma das
    quatro bordas do PNG e falha se alguma margem for nula ou se o par
    esquerda/direita (ou topo/base) for muito assimétrico."""
    im = Image.open(caminho).convert("RGB")
    a = np.array(im)
    mask = np.any(a < 250, axis=2)
    ys, xs = np.where(mask)
    if len(xs) == 0:
        raise AssertionError(f"{caminho}: nenhum conteúdo não-branco encontrado")
    largura, altura = im.size
    margens = {
        "esquerda": int(xs.min()),
        "direita": int(largura - 1 - xs.max()),
        "topo": int(ys.min()),
        "base": int(altura - 1 - ys.max()),
    }

    for nome, m in margens.items():
        if m <= 0:
            raise AssertionError(f"Margem '{nome}' nula ou negativa ({m}px) -- conteúdo cortado na borda")

    def _checar_par(a_nome, b_nome):
        ma, mb = margens[a_nome], margens[b_nome]
        maior, menor = max(ma, mb), min(ma, mb)
        if (maior - menor) / maior > tolerancia_relativa:
            raise AssertionError(
                f"Margens '{a_nome}' ({ma}px) e '{b_nome}' ({mb}px) assimétricas além da tolerância "
                f"({tolerancia_relativa:.0%}) -- possível corte ou desenho descentrado"
            )

    _checar_par("esquerda", "direita")
    _checar_par("topo", "base")
    return margens


def main() -> None:
    caminho, fontes_nativas, largura_nativa_in, altura_nativa_in = gerar_fluxograma()
    with Image.open(caminho) as im:
        largura_px, altura_px = im.size

    fator_encolhimento = LARGURA_REPRODUCAO_IN / largura_nativa_in
    print(f"{caminho}")
    print(f"{CAMINHO_SAIDA_PDF}")
    print(f"  {largura_px}x{altura_px}px @ {DPI} dpi -- nativo {largura_nativa_in:.3f}in x {altura_nativa_in:.3f}in")
    print(f"  reprodução no capítulo: {LARGURA_REPRODUCAO_CM:.1f} cm de largura "
          f"(fator de encolhimento {fator_encolhimento:.4f} = {LARGURA_REPRODUCAO_IN:.3f}in / {largura_nativa_in:.3f}in)")
    print(f"  proporção largura/altura = {largura_px / altura_px:.4f}")

    print("\n  Tamanho de fonte por nível hierárquico (nativo -> efetivo a 15 cm):")
    for nivel, pt_nativo in fontes_nativas.items():
        pt_15cm = pt_nativo * fator_encolhimento
        alvo = {"header": FONTE_HEADER_15CM, "caixa": FONTE_CAIXA_15CM}[nivel]
        status = "OK" if pt_15cm >= MIN_PT_15CM_EXIGIDO - 1e-6 else "FALHA -- abaixo do piso de 7pt"
        print(f"    {nivel:8s}: {pt_nativo:6.2f}pt nativos -> {pt_15cm:5.2f}pt a 15cm (alvo {alvo:.1f}pt) [{status}]")
        if pt_15cm < MIN_PT_15CM_EXIGIDO - 1e-6:
            raise AssertionError(f"Nível '{nivel}' fica com {pt_15cm:.2f}pt a 15cm, abaixo do piso de {MIN_PT_15CM_EXIGIDO}pt")

    margens = verificar_margens(caminho)
    print("\n  Margens (pixels nativos -> mm na reprodução de 15cm):")
    for lado, px in margens.items():
        mm_nativo = px / DPI * 25.4
        mm_15cm = mm_nativo * fator_encolhimento
        print(f"    {lado:9s}: {px:5d}px  ({mm_nativo:5.2f}mm nativos -> {mm_15cm:4.2f}mm a 15cm)")
    print("\n  OK -- margens não-nulas e simétricas dentro da tolerância; fontes acima do piso de 7pt a 15cm.")


if __name__ == "__main__":
    main()
