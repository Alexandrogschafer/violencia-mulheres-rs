"""Gera a Figura 1 (variante A) e a Figura 2 (variante D) do artigo espacial, com as legendas.

As variantes B (cartograma) e C (símbolos nos centroides), consideradas na escolha, foram descartadas em
2026-11-08; o desenho anterior da Figura 1 (quatro painéis por quadrante) também. `gerar_figura1.py`
continua como módulo dos dados e da paleta, carregado aqui.

Base comum (denominador feminino, semente 12345, os pares significativos da Tabela 2 e da Tabela
suplementar 2, carregados e conferidos por `gerar_figura1.dados`).

Figura 1 (variante A) — geográfica com recortes: o estado (A), o COREDE Litoral (B) e o bloco do norte,
nos COREDEs Médio Alto Uruguai, Celeiro e Rio da Várzea (C).
- os municípios significativos nos quatro desfechos, num mapa só, com cor por direção: alto-alto,
  baixo-baixo e outlier espacial (alto-baixo e baixo-alto juntos). Um mapa só é possível porque nenhum
  município tem quadrantes diferentes em desfechos diferentes — o script confere isso antes de desenhar e
  para se deixar de valer;
- hachura nos municípios significativos em dois desfechos (nenhum é significativo em mais de dois — também
  conferido);
- anel vazado nos municípios com ao menos um par com menos de 5 eventos esperados;
- não significativos em cinza claro; legenda única, escala e norte; paleta conferida por luminosidade
  (CIE L* e nível de cinza), com os limiares de `gerar_figura1`;
- nos recortes, limites municipais visíveis, contorno dos COREDEs e nomes oficiais do IBGE (significativos
  em negrito). Rótulos que se tocam têm a fonte reduzida até 3,4 pt, primeiro os de não significativos; os
  pares que ainda se tocam perdem o nome do não significativo. Todo significativo mantém o nome (o script
  confere): dois significativos que se tocam são afastados o mínimo necessário, e o script para se nenhum
  par sobrar ou se algum nome significativo sair.

Figura 2 (variante D; pensada como figura suplementar, mas as duas suplementares que a RESS admite já são
tabelas) — superfície contínua: um painel por desfecho com a taxa ajustada de
Assunção e Reis (`esda.smoothing.assuncao_rate`, a mesma que `Moran_Local_Rate` usa) padronizada pela
média e pelo desvio-padrão municipais — exatamente o valor cujo sinal define o quadrante do LISA. O script
confere, antes de desenhar, que esse valor reproduz o I de Moran ajustado da Tabela 1 e que o sinal do
valor e da defasagem espacial bate com o quadrante de cada par significativo. Escala divergente centrada
em zero (a média municipal), com cortes em ±2,5 desvios-padrão e as pontas abertas, na divergente clássica
de centro claro RdBu (invertida: vermelho acima da média, azul abaixo). Antes de desenhar, o script
confere a escala nas dez classes de 0,5 desvio-padrão entre −2,5 e +2,5 (ver `confere_escala_d`): os dois
braços chegam a luminosidade comparável, as classes adjacentes de cada braço se distinguem em visão normal
e sob protanopia e deuteranopia simuladas, e azul e vermelho de mesmo |z| também. A versão em cinza
continua sendo gravada, mas não é critério: numa divergente de centro claro os dois extremos dão o mesmo
cinza. Por cima, os municípios significativos contornados em preto (com halo branco) e o anel nos pares
com esperado < 5.

Saída em publicacoes/artigo_espacial/03_figuras/:
- `figura1.pdf` e `figura2.pdf`, vetoriais, fontes embutidas como TrueType;
- `figura1.png` e `figura2.png`, a 300 dpi (as que entram nos .docx);
- `figura1_cinza.png` e `figura2_cinza.png`, em escala de cinza, só para conferência;
- `figura1_legenda.md` e `figura2_legenda.md`, com a legenda no padrão RESS (a das tabelas)
  e a conferência da paleta ou da escala.

Uso, da raiz do repositório:
    python3 publicacoes/artigo_espacial/03_figuras/gerar_figura1_variantes.py
"""

import importlib.util
import sys
from itertools import combinations
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import esda  # noqa: E402
import geopandas as gpd  # noqa: E402
import numpy as np  # noqa: E402
from esda.smoothing import assuncao_rate  # noqa: E402
from matplotlib.colors import Normalize  # noqa: E402
import pandas as pd  # noqa: E402
import matplotlib.patheffects as pe  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch, Rectangle  # noqa: E402
from PIL import Image  # noqa: E402
from shapely.ops import polylabel  # noqa: E402

from src.analysis.autocorrelacao_espacial import montar_pesos_espaciais  # noqa: E402
from src.analysis.denominador import fator, montar_geodataframe_denominador  # noqa: E402
from src.analysis.esperado_vs_observado_lisa import LIMIAR  # noqa: E402
from src.analysis.mapa_choropleth import _populacao_referencia  # noqa: E402
from src.analysis.moran_lisa_assuncao_reis import ANO_FIM, ANO_INICIO  # noqa: E402

_spec = importlib.util.spec_from_file_location("gerar_figura1", Path(__file__).resolve().parent / "gerar_figura1.py")
fig1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fig1)
tabelas = fig1.tabelas

SAIDA = Path(__file__).resolve().parent
LARGURA_CM = fig1.LARGURA_CM
ANO_POP = 2025
COR_TRACO = "#3a3a3a"

# Mesmas cores da Figura 1 para alto-alto, baixo-baixo e não significativo; o outlier espacial, que junta
# alto-baixo e baixo-alto, fica num violeta de luminosidade intermediária entre o vermelho e o cinza claro.
CORES = {
    "BB": fig1.CORES["BB"],
    "AA": fig1.CORES["AA"],
    "OUT": "#ac94d4",
    "NS": fig1.CORES["NS"],
}
ROTULOS = {
    "AA": "Alto-alto",
    "BB": "Baixo-baixo",
    "OUT": "Outlier espacial\n(alto-baixo ou baixo-alto)",
    "NS": "Não significativo",
}
DIRECAO = {"AA": "AA", "BB": "BB", "AB": "OUT", "BA": "OUT"}
COR_HACHURA = "white"
HACHURA = "//////"
ROTULO_HACHURA = "Significativo em 2 desfechos"
ROTULO_MARCA = f"Ao menos um par com menos\nde {LIMIAR} eventos esperados"

NORTE = ["Médio Alto Uruguai", "Celeiro", "Rio da Várzea"]
LITORAL = ["Litoral"]


# ---------------------------------------------------------------- paleta


def confere_paleta() -> list[str]:
    for a, b in combinations(CORES, 2):
        dl = abs(fig1.luminosidade_lab(CORES[a]) - fig1.luminosidade_lab(CORES[b]))
        dc = abs(fig1.nivel_cinza(CORES[a]) - fig1.nivel_cinza(CORES[b]))
        if dl < fig1.DELTA_L_MINIMO or dc < fig1.DELTA_CINZA_MINIMO:
            sys.exit(f"Paleta reprovada: {a} × {b} com ΔL* = {dl:.1f} e Δcinza = {dc}.")
    linhas = [f"{ROTULOS[k]}: {c}, L* = {fig1.luminosidade_lab(c):.1f}, cinza = {fig1.nivel_cinza(c)}"
              for k, c in CORES.items()]
    pares = list(combinations(CORES, 2))
    menor_l = min(abs(fig1.luminosidade_lab(CORES[a]) - fig1.luminosidade_lab(CORES[b])) for a, b in pares)
    menor_c = min(abs(fig1.nivel_cinza(CORES[a]) - fig1.nivel_cinza(CORES[b])) for a, b in pares)
    linhas.append(f"Menor diferença entre dois preenchimentos: ΔL* = {menor_l:.1f}; Δcinza = {menor_c}")
    return linhas


# ---------------------------------------------------------------- dados


def dados() -> pd.DataFrame:
    """Malha dos 497 com direção, número de desfechos, marca de esperado < 5, COREDE, nome oficial e
    população feminina de 2025."""
    sig, abaixo, malha = fig1.dados()
    quad = sig.groupby("municipio")["categoria"].agg(lambda s: sorted(set(s)))
    mistos = quad[quad.map(len) > 1]
    tabelas.confere(mistos.empty, f"municípios com quadrantes diferentes entre desfechos: {dict(mistos)}")
    n = sig.groupby("municipio").size()
    tabelas.confere(n.max() <= 2, "município significativo em mais de dois desfechos")
    marcados = {m for m, _ in abaixo}

    g = malha.copy()
    g["direcao"] = g["municipio"].map(quad.str[0].map(DIRECAO)).fillna("NS")
    g["n_desfechos"] = g["municipio"].map(n).fillna(0).astype(int)
    g["esperado_baixo"] = g["municipio"].isin(marcados)
    g["corede"] = g["municipio"].map(tabelas.coredes())
    g["nome"] = g["municipio"].map(tabelas.nomes_oficiais())
    pop = _populacao_referencia(ANO_POP)
    tabelas.confere(pop.index.isin(g["municipio"]).sum() == len(g), f"população de {ANO_POP} incompleta")
    g["mulheres_2025"] = g["municipio"].map(pop) * fator(g["municipio"], "feminina")
    tabelas.confere(g[["corede", "nome", "mulheres_2025"]].notna().all().all(), "COREDE, nome ou população ausente")
    tabelas.confere(int((g["n_desfechos"] > 0).sum()) == sig["municipio"].nunique(), "contagem de municípios")
    tabelas.confere(int(g["n_desfechos"].sum()) == len(sig), "contagem de pares")
    for c in NORTE + LITORAL:
        tabelas.confere((g["corede"] == c).any(), f"COREDE {c} não encontrado")
    return g


# ---------------------------------------------------------------- desenho comum


def pinta(ax, g, borda=0.15, cor_borda="white"):
    g.plot(ax=ax, color=g["direcao"].map(CORES), edgecolor=cor_borda, linewidth=borda)
    duplos = g[g["n_desfechos"] == 2]
    if len(duplos):
        duplos.plot(ax=ax, facecolor="none", edgecolor=COR_HACHURA, linewidth=0, hatch=HACHURA)
        # Borda branca outra vez por cima da hachura, para o limite continuar nítido.
        duplos.boundary.plot(ax=ax, color=cor_borda, linewidth=borda)


def aneis(ax, g, s=22):
    pontos = g[g["esperado_baixo"]].geometry.representative_point()
    ax.scatter(pontos.x, pontos.y, s=s, facecolor="none", edgecolor="white", linewidth=2.2, zorder=5)
    ax.scatter(pontos.x, pontos.y, s=s, facecolor="none", edgecolor="black", linewidth=0.8, zorder=6)


def norte(ax, x_n, y_base, comprimento):
    y_topo = y_base + comprimento
    ax.plot([x_n, x_n], [y_base, y_topo - comprimento * 0.25], color=COR_TRACO, linewidth=1.2,
            solid_capstyle="butt", zorder=9)
    ax.annotate("", xy=(x_n, y_topo), xytext=(x_n, y_topo - comprimento * 0.28),
                arrowprops={"arrowstyle": "-|>,head_length=0.55,head_width=0.28", "color": COR_TRACO, "lw": 1.2,
                            "shrinkA": 0, "shrinkB": 0}, zorder=9)
    ax.text(x_n, y_topo + comprimento * 0.08, "N", ha="center", va="bottom", fontsize=7, fontweight="bold",
            color=COR_TRACO, zorder=9)


def escala_e_norte(ax, km: int, canto: str = "dir"):
    """Escala gráfica de `km` e seta de norte num canto inferior do eixo (CRS métrico, aspecto 1:1)."""
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    largura, altura = x1 - x0, y1 - y0
    barra = km * 1000
    if canto == "dir":
        x_fim = x0 + 0.95 * largura
        x_ini = x_fim - barra
    else:
        x_ini = x0 + 0.05 * largura
        x_fim = x_ini + barra
    y_barra = y0 + 0.04 * altura
    marca = altura * 0.008
    ax.plot([x_ini, x_fim], [y_barra, y_barra], color=COR_TRACO, linewidth=1.1, solid_capstyle="butt", zorder=9)
    for x in (x_ini, x_fim):
        ax.plot([x, x], [y_barra - marca, y_barra + marca], color=COR_TRACO, linewidth=1.1, zorder=9)
    ax.text((x_ini + x_fim) / 2, y_barra + altura * 0.015, f"{km} km", ha="center", va="bottom", fontsize=6.5,
            color=COR_TRACO, zorder=9)
    comprimento = min(altura * 0.09, largura * 0.12)
    norte(ax, (x_ini + x_fim) / 2, y_barra + altura * 0.07, comprimento)


def entradas_legenda():
    e = [Patch(facecolor=CORES[k], edgecolor="#9a9a9a", linewidth=0.4,
               label=ROTULOS[k] + (tabelas.s_("a") if k != "NS" else ""))
         for k in ["AA", "BB", "OUT", "NS"]]
    e.append(Patch(facecolor="#7a7a7a", edgecolor=COR_HACHURA, linewidth=0, hatch=HACHURA, label=ROTULO_HACHURA))
    e.append(Line2D([], [], marker="o", linestyle="", markersize=5, markerfacecolor="none", markeredgecolor="black",
                    markeredgewidth=0.8, label=ROTULO_MARCA + tabelas.s_("b")))
    return e


def configura():
    plt.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42, "font.size": 8, "hatch.linewidth": 0.6})


def ajusta(ax, g, folga=0.03):
    x0, y0, x1, y1 = g.total_bounds
    fx, fy = (x1 - x0) * folga, (y1 - y0) * folga
    ax.set_xlim(x0 - fx, x1 + fx)
    ax.set_ylim(y0 - fy, y1 + fy)
    ax.set_aspect("equal")
    ax.set_axis_off()


def escala_numerica(fig, ax) -> float:
    fig.canvas.draw()
    largura_cm = ax.get_window_extent().width / fig.dpi * 2.54
    return (ax.get_xlim()[1] - ax.get_xlim()[0]) * 100 / largura_cm


def grava(fig, nome: str) -> None:
    fig.savefig(SAIDA / f"{nome}.pdf", metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(SAIDA / f"{nome}.png", dpi=300)
    plt.close(fig)
    Image.open(SAIDA / f"{nome}.png").convert("L").save(SAIDA / f"{nome}_cinza.png", dpi=(300, 300))


# ---------------------------------------------------------------- variante A


def quebra(nome: str, limite: int = 11) -> str:
    """Quebra nomes longos em duas linhas, no espaço mais próximo do meio."""
    if len(nome) <= limite or " " not in nome:
        return nome
    espacos = [i for i, c in enumerate(nome) if c == " "]
    i = min(espacos, key=lambda k: abs(k - len(nome) / 2))
    return nome[:i] + "\n" + nome[i + 1:]


def ponto_rotulo(geom):
    """Polo de inacessibilidade da maior parte do polígono: o ponto interior mais longe da borda."""
    if geom.geom_type == "MultiPolygon":
        geom = max(geom.geoms, key=lambda x: x.area)
    return polylabel(geom, tolerance=50)


def _colisoes(fig, rotulos):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    caixas = [(t, s, t.get_window_extent(r)) for t, s in rotulos]
    return [(a, b) for a, b in combinations(caixas, 2) if a[2].overlaps(b[2])]


def desfaz_colisoes(fig, rotulos, minimo=3.4, passo=0.3, rodadas=12) -> tuple[int, list]:
    """Desfaz os rótulos que se tocam, em duas etapas.

    1. Reduz a fonte, primeiro a dos não significativos, até `minimo` pt.
    2. Nos pares que ainda se tocam, retira o nome do não significativo — um por vez, o que está em mais
       pares (empate: o de nome em ordem alfabética), até não sobrar par. Um par de dois significativos não
       se resolve assim: os dois rótulos são afastados o mínimo para não se tocarem (`_afasta`).

    Devolve quantos pares se tocavam ao fim da etapa 1, os nomes retirados e os pares afastados, com o
    deslocamento de cada rótulo em pt."""
    for _ in range(rodadas + 1):
        colisoes = _colisoes(fig, rotulos)
        if not colisoes:
            break
        mudou = False
        for a, b in colisoes:
            alvo = a if (not a[1] and b[1]) else b if (not b[1] and a[1]) else max(
                (a, b), key=lambda x: x[0].get_fontsize())
            if alvo[0].get_fontsize() - passo >= minimo - 1e-9:
                alvo[0].set_fontsize(alvo[0].get_fontsize() - passo)
                mudou = True
        if not mudou:
            break
    apos_fonte = len(_colisoes(fig, rotulos))
    retirados, afastados = [], []
    while colisoes := _colisoes(fig, rotulos):
        duplos = [(a, b) for a, b in colisoes if a[1] and b[1]]
        if duplos:
            a, b = duplos[0]
            nomes = (a[0].get_text().replace("\n", " "), b[0].get_text().replace("\n", " "))
            tabelas.confere(len(afastados) < 5 and nomes not in [n for n, _ in afastados],
                            f"rótulos de significativos que não se separam: {nomes}")
            afastados.append((nomes, _afasta(a, b)))
            continue
        contagem = {}
        for a, b in colisoes:
            for t, sig, _ in (a, b):
                if not sig:
                    contagem[t] = contagem.get(t, 0) + 1
        alvo = min(contagem, key=lambda t: (-contagem[t], t.get_text()))
        retirados.append(alvo.get_text().replace("\n", " "))
        alvo.remove()
        rotulos[:] = [(t, s) for t, s in rotulos if t is not alvo]
    return apos_fonte, retirados, afastados


def _afasta(a, b, folga_pt=0.5) -> float:
    """Afasta dois rótulos de significativos que se tocam, cada um metade da sobreposição mais `folga_pt`,
    no eixo (horizontal ou vertical) em que a sobreposição é menor. Devolve o deslocamento de cada um, em pt."""
    (ta, _, ca), (tb, _, cb) = a, b
    dx = min(ca.x1, cb.x1) - max(ca.x0, cb.x0)
    dy = min(ca.y1, cb.y1) - max(ca.y0, cb.y0)
    fig = ta.figure
    folga = folga_pt * fig.dpi / 72
    horizontal = dx <= dy
    passo = ((dx if horizontal else dy) + folga) / 2
    for t, c, sinal in ((ta, ca, -1), (tb, cb, 1)):
        if horizontal:
            sinal = sinal if ca.x0 <= cb.x0 else -sinal
            desl = (sinal * passo, 0)
        else:
            sinal = sinal if ca.y0 <= cb.y0 else -sinal
            desl = (0, sinal * passo)
        x, y = t.axes.transData.transform(t.get_position())
        t.set_position(t.axes.transData.inverted().transform((x + desl[0], y + desl[1])))
    return passo * 72 / fig.dpi


def recorte(ax, g, coredes, km, titulo, fonte, canto="esq"):
    dentro = g[g["corede"].isin(coredes)]
    ajusta(ax, dentro, folga=0.04)
    # Vizinhança em volta, esmaecida, para situar o recorte.
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    fora = g[~g["corede"].isin(coredes)].cx[x0:x1, y0:y1]
    pinta(ax, fora, borda=0.3)
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor="white", alpha=0.55, edgecolor="none", zorder=3))
    pinta_sobre = dentro.copy()
    pinta_sobre.plot(ax=ax, color=pinta_sobre["direcao"].map(CORES), edgecolor="#6b6b6b", linewidth=0.35, zorder=4)
    duplos = pinta_sobre[pinta_sobre["n_desfechos"] == 2]
    if len(duplos):
        duplos.plot(ax=ax, facecolor="none", edgecolor=COR_HACHURA, linewidth=0, hatch=HACHURA, zorder=4.5)
        duplos.boundary.plot(ax=ax, color="#6b6b6b", linewidth=0.35, zorder=4.6)
    dentro.dissolve("corede").boundary.plot(ax=ax, color=COR_TRACO, linewidth=0.9, zorder=4.7)
    rotulos = []
    for _, r in dentro.iterrows():
        p = ponto_rotulo(r.geometry)
        sig = r["direcao"] != "NS"
        escuro = r["direcao"] in ("BB", "AA")
        cor, halo = ("white", COR_TRACO) if escuro else ("#1a1a1a", "white")
        txt = ax.text(p.x, p.y, quebra(r["nome"]), ha="center", va="center", fontsize=fonte, linespacing=0.88,
                      fontweight="bold" if sig else "normal", color=cor, zorder=7,
                      path_effects=[pe.withStroke(linewidth=1.1, foreground=halo, alpha=0.9)])
        rotulos.append((txt, sig))
    marc = dentro[dentro["esperado_baixo"]]
    pm = gpd.GeoSeries([ponto_rotulo(x) for x in marc.geometry])
    # No recorte o anel envolve o nome, para não cobri-lo.
    ax.scatter(pm.x, pm.y, s=260, facecolor="none", edgecolor="white", linewidth=2.2, zorder=5)
    ax.scatter(pm.x, pm.y, s=260, facecolor="none", edgecolor="black", linewidth=0.8, zorder=6)
    ax.set_title(titulo, loc="left", fontsize=8.5, fontweight="bold")
    escala_e_norte(ax, km, canto=canto)
    return dentro, rotulos


def variante_a(g):
    largura_pol = LARGURA_CM / 2.54
    altura_pol = largura_pol * 1.24
    fig = plt.figure(figsize=(largura_pol, altura_pol))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.45, 1.0], height_ratios=[1.0, 1.0],
                          left=0.01, right=0.99, top=0.955, bottom=0.005, wspace=0.03, hspace=0.07)
    ax_rs = fig.add_subplot(gs[0, 0])
    ax_lit = fig.add_subplot(gs[0, 1])
    sub = gs[1, :].subgridspec(1, 2, width_ratios=[2.5, 1.0], wspace=0.02)
    ax_n = fig.add_subplot(sub[0, 0])
    ax_leg = fig.add_subplot(sub[0, 1])
    ax_leg.set_axis_off()

    pinta(ax_rs, g)
    g.dissolve().boundary.plot(ax=ax_rs, color=COR_TRACO, linewidth=0.5)
    aneis(ax_rs, g, s=16)
    ajusta(ax_rs, g, folga=0.01)
    escala_e_norte(ax_rs, fig1.BARRA_ESCALA_KM)
    ax_rs.set_title("A  Rio Grande do Sul", loc="left", fontsize=8.5, fontweight="bold")
    for coredes, letra in ((LITORAL, "B"), (NORTE, "C")):
        x0, y0, x1, y1 = g[g["corede"].isin(coredes)].total_bounds
        ax_rs.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor="none", edgecolor="black", linewidth=0.8,
                                  zorder=8))
        ax_rs.text(x1 if letra == "B" else x0, y1, f" {letra} ", ha="left" if letra == "B" else "right", va="top",
                   fontsize=8, fontweight="bold", zorder=8)

    lit, rot_lit = recorte(ax_lit, g, LITORAL, 20, "B  COREDE Litoral", 5.0, canto="dir")
    nor, rot_nor = recorte(ax_n, g, NORTE, 20, "C  COREDEs Médio Alto Uruguai, Celeiro e Rio da Várzea", 5.0)
    rotulos = rot_lit + rot_nor
    n_sig = sum(sig for _, sig in rotulos)
    apos_fonte, retirados, afastados = desfaz_colisoes(fig, rotulos)
    tabelas.confere(sum(sig for _, sig in rotulos) == n_sig, "nome de município significativo retirado")
    tabelas.confere(not _colisoes(fig, rotulos), "rótulos ainda se tocam")
    fontes = [t.get_fontsize() for t, _ in rotulos]
    ax_leg.legend(handles=entradas_legenda(), loc="center left", frameon=False, fontsize=7, handlelength=1.6,
                  labelspacing=0.9, borderaxespad=0)
    nota = ("Nos recortes, nomes em negrito: municípios\nsignificativos; onde não cabem, omitidos\n"
            "nomes de não significativos; linha grossa:\nlimite de COREDE; em volta, esmaecidos,\n"
            "os municípios vizinhos.")
    ax_leg.text(0.0, 0.08, nota, transform=ax_leg.transAxes, fontsize=6.3, va="bottom", color="#333333")
    escalas = {k: escala_numerica(fig, a) for k, a in (("A", ax_rs), ("B", ax_lit), ("C", ax_n))}
    grava(fig, "figura1")
    return {"escalas": escalas, "n_lit": len(lit), "n_nor": len(nor), "rotulos": len(rotulos) + len(retirados),
            "apos_fonte": apos_fonte, "retirados": retirados, "afastados": afastados, "fontes": (min(fontes), max(fontes))}


def legenda_a(g) -> str:
    """Legenda no padrão RESS (o das tabelas e da Figura 1 anterior): título sem ponto final, com local, anos
    e n; notas em letras minúsculas sobrescritas; sem detalhes de método, que ficam nos Métodos."""
    n_anel = int(g["esperado_baixo"].sum())
    return tabelas.legenda(
        "Figura 1",
        "Municípios com indicador local de associação espacial (LISA) significativo em ao menos um de quatro "
        "desfechos de violência contra a mulher (ameaça, lesão corporal, estupro e feminicídio tentado), por "
        "direção, no estado (A), no Conselho Regional de Desenvolvimento (COREDE) Litoral (B) e nos COREDEs Médio "
        "Alto Uruguai, Celeiro e Rio da Várzea (C), Rio Grande do Sul, 2018-2025 (n = 497 municípios)",
        [("a", tabelas.NOTA_QUADRANTE),
         ("b", f"{tabelas.NOTA_ESPERADO} ({n_anel} municípios)")],
    )


# ---------------------------------------------------------------- variante D

LIMITE_Z = 2.5
MAPA_D = "RdBu_r"
PASSO_CLASSE = 0.5
# Limiares do validador de paleta do guia de visualização (validate_palette.js): distância em OKLab ×100,
# simulação de Machado, Oliveira e Fernandes (2009) com severidade 1,0; ΔL mínimo entre degraus de rampa.
CVD_ALVO = 8.0
DELTA_L_DEGRAU_MINIMO = 0.06
DELTA_L_BRACOS_MAXIMO = 0.02
MACHADO = {
    "protanopia": np.array([[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216],
                            [-0.003882, -0.048116, 1.051998]]),
    "deuteranopia": np.array([[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413],
                              [-0.011820, 0.042940, 0.968881]]),
}


def mapa_cores_d():
    return matplotlib.colormaps[MAPA_D]


def _hex(rgba) -> str:
    return "#" + "".join(f"{round(c * 255):02x}" for c in rgba[:3])


def _linear(rgba) -> np.ndarray:
    c = np.asarray(rgba[:3], dtype=float)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _oklab(lin: np.ndarray) -> np.ndarray:
    lms = np.cbrt(np.array([[0.4122214708, 0.5363325363, 0.0514459929],
                            [0.2119034982, 0.6806995451, 0.1073969566],
                            [0.0883024619, 0.2817188376, 0.6299787005]]) @ lin)
    return np.array([[0.2104542553, 0.7936177850, -0.0040720468],
                     [1.9779984951, -2.4285922050, 0.4505937099],
                     [0.0259040371, 0.7827717662, -0.8086757660]]) @ lms


def delta_e(c1, c2, visao: str | None = None) -> float:
    """Distância em OKLab ×100, em visão normal ou sob a simulação de Machado et al. (2009)."""
    a, b = _linear(c1), _linear(c2)
    if visao:
        a, b = np.clip(MACHADO[visao] @ a, 0, 1), np.clip(MACHADO[visao] @ b, 0, 1)
    return float(100 * np.linalg.norm(_oklab(a) - _oklab(b)))


def confere_escala_d(cmap) -> list[str]:
    """Confere a escala nas classes de PASSO_CLASSE desvio-padrão (cor no centro de cada classe):

    - em cada braço, a luminosidade OKLab cai do centro para a ponta, com degrau de ao menos
      DELTA_L_DEGRAU_MINIMO entre classes adjacentes;
    - classes adjacentes do mesmo braço a pelo menos CVD_ALVO em visão normal, protanopia e deuteranopia;
    - os dois braços com luminosidade comparável: −z e +z a no máximo DELTA_L_BRACOS_MAXIMO em L;
    - azul e vermelho de mesmo |z| a pelo menos CVD_ALVO sob protanopia e deuteranopia, exceto na classe que
      encosta no zero, onde os dois braços convergem para o centro claro por construção.

    O par de classes que atravessa o zero não é cobrado: é o centro neutro da escala. A distância dele é
    informada no relatório."""
    centros = np.arange(-LIMITE_Z + PASSO_CLASSE / 2, LIMITE_Z, PASSO_CLASSE)
    cor = {round(z, 2): cmap((z + LIMITE_Z) / (2 * LIMITE_Z)) for z in centros}
    L = {z: _oklab(_linear(c))[0] for z, c in cor.items()}
    visoes = (None, "protanopia", "deuteranopia")
    falhas, linhas = [], []
    positivos = [z for z in cor if z > 0]
    for sinal in (-1, 1):
        braco = [sinal * z for z in positivos]
        for a, b in zip(braco, braco[1:]):
            dl = L[a] - L[b]
            des = [delta_e(cor[a], cor[b], v) for v in visoes]
            if dl < DELTA_L_DEGRAU_MINIMO:
                falhas.append(f"degrau de L entre {a:+.2f} e {b:+.2f}: {dl:.3f}")
            if min(des) < CVD_ALVO:
                falhas.append(f"classes {a:+.2f} e {b:+.2f} a ΔE {min(des):.1f}")
            linhas.append(f"{a:+.2f} → {b:+.2f}: ΔL {dl:.3f}; ΔE normal {des[0]:.1f}, protan. {des[1]:.1f}, "
                          f"deuteran. {des[2]:.1f}")
    for z in positivos:
        dl = abs(L[z] - L[-z])
        des = [delta_e(cor[-z], cor[z], v) for v in visoes]
        if dl > DELTA_L_BRACOS_MAXIMO:
            falhas.append(f"braços desiguais em ±{z:.2f}: ΔL {dl:.3f}")
        if z > PASSO_CLASSE and min(des[1:]) < CVD_ALVO:
            falhas.append(f"azul e vermelho em ±{z:.2f} a ΔE {min(des[1:]):.1f} sob daltonismo")
        linhas.append(f"±{z:.2f}: ΔL entre braços {dl:.3f}; ΔE normal {des[0]:.1f}, protan. {des[1]:.1f}, "
                      f"deuteran. {des[2]:.1f}" + (" (centro neutro, não cobrado)" if z <= PASSO_CLASSE else ""))
    if falhas:
        sys.exit("Escala da variante D reprovada: " + "; ".join(falhas))
    cores = ", ".join(f"{z:+.2f} {_hex(c)}" for z, c in cor.items())
    return [f"{MAPA_D}, classes de {PASSO_CLASSE} DP: {cores}"] + linhas


def superficies(g) -> dict:
    """Taxa ajustada de Assunção e Reis, padronizada (o z do LISA), por desfecho, conferida contra a
    Tabela 1 (I de Moran) e contra os quadrantes dos pares significativos."""
    sig, abaixo, _ = fig1.dados()
    ref = tabelas.le_tabela_md(fig1.TABLES / "resultados_consolidados.md", "Desfecho").set_index("Desfecho")
    coluna_i = "Moran ajustado"
    saida = {}
    for d in fig1.LISA:
        b = montar_geodataframe_denominador(d, ANO_INICIO, ANO_FIM, "feminina")
        w = montar_pesos_espaciais(b)
        w.transform = "r"
        y = assuncao_rate(b["casos_total"].to_numpy(float), b["populacao_pessoas_ano"].to_numpy(float))
        z = (y - y.mean()) / y.std()
        i = esda.Moran(y, w, permutations=0).I
        tabelas.confere(tabelas.br(i, 4) == ref.loc[d, coluna_i], f"variante D, {d}: I = {i:.4f} difere da Tabela 1")
        zs = pd.Series(z, index=b["municipio"])
        lag = pd.Series(w.sparse @ z, index=b["municipio"])
        s = sig[sig["tipo_crime"] == d]
        for m, q in zip(s["municipio"], s["categoria"]):
            tabelas.confere((zs[m] > 0) == (q[0] == "A") and (lag[m] > 0) == (q[1] == "A"),
                            f"variante D, {d}, {m}: sinal não bate com o quadrante {q}")
        saida[d] = {"z": zs, "sig": set(s["municipio"]), "abaixo": {m for m, t in abaixo if t == d}, "I": i,
                    "fora": int(((z < -LIMITE_Z) | (z > LIMITE_Z)).sum())}
    return saida


def variante_d(g):
    cmap = mapa_cores_d()
    escala_txt = confere_escala_d(cmap)
    sup = superficies(g)
    norma = Normalize(-LIMITE_Z, LIMITE_Z)
    largura_pol = LARGURA_CM / 2.54
    fig, eixos = plt.subplots(2, 2, figsize=(largura_pol, largura_pol * 1.0))
    for ax, letra, d in zip(eixos.flat, fig1.LETRAS, fig1.LISA):
        s = sup[d]
        b = g.assign(z=g["municipio"].map(s["z"]))
        tabelas.confere(b["z"].notna().all(), f"variante D, {d}: município sem valor")
        b.plot(ax=ax, column="z", cmap=cmap, norm=norma, edgecolor="#ffffff", linewidth=0.08)
        g.dissolve().boundary.plot(ax=ax, color=COR_TRACO, linewidth=0.5)
        dest = b[b["municipio"].isin(s["sig"])]
        dest.boundary.plot(ax=ax, color="white", linewidth=1.6, zorder=4)
        dest.boundary.plot(ax=ax, color="black", linewidth=0.7, zorder=5)
        marc = b[b["municipio"].isin(s["abaixo"])]
        pm = gpd.GeoSeries([ponto_rotulo(x) for x in marc.geometry])
        ax.scatter(pm.x, pm.y, s=22, facecolor="none", edgecolor="white", linewidth=2.2, zorder=6)
        ax.scatter(pm.x, pm.y, s=22, facecolor="none", edgecolor="black", linewidth=0.8, zorder=7)
        ajusta(ax, g, folga=0.01)
        ax.set_title(f"{letra}  {d.capitalize()}", loc="left", fontsize=9, fontweight="bold")
        escala_e_norte(ax, fig1.BARRA_ESCALA_KM)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.935, bottom=0.17, wspace=0.03, hspace=0.12)
    cax = fig.add_axes([0.06, 0.085, 0.42, 0.022])
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=norma, cmap=cmap), cax=cax, orientation="horizontal", extend="both")
    cb.set_ticks([-2, -1, 0, 1, 2])
    cb.set_ticklabels(["−2", "−1", "0", "+1", "+2"])
    cb.ax.tick_params(labelsize=7, length=2)
    cb.outline.set_linewidth(0.4)
    cb.set_label("Taxa ajustada de Assunção e Reis, em desvios-padrão\nem relação à média municipal (0)" + tabelas.s_("a"),
                 fontsize=7, linespacing=1.0)
    e = [Patch(facecolor="none", edgecolor="black", linewidth=1.0, label="LISA significativo" + tabelas.s_("b")),
         Line2D([], [], marker="o", linestyle="", markersize=5, markerfacecolor="none", markeredgecolor="black",
                markeredgewidth=0.8, label=f"Menos de {LIMIAR} eventos esperados" + tabelas.s_("c"))]
    fig.legend(handles=e, loc="lower left", bbox_to_anchor=(0.56, 0.055), frameon=False, fontsize=7.5,
               handlelength=1.6, labelspacing=0.9)
    grava(fig, "figura2")
    return escala_txt, {d: {"I": round(float(s["I"]), 4), "contornados": len(s["sig"]), "aneis": len(s["abaixo"]),
                            "fora_de_±2,5": s["fora"]} for d, s in sup.items()}


def legenda_d(info_d: dict) -> str:
    aneis = "; ".join(f"{fig1.LETRAS[i]}: {info_d[d]['aneis']}" for i, d in enumerate(fig1.LISA) if info_d[d]["aneis"])
    fora = "; ".join(f"{fig1.LETRAS[i]}: {info_d[d]['fora_de_±2,5']}" for i, d in enumerate(fig1.LISA))
    return tabelas.legenda(
        "Figura 2",
        "Taxa ajustada padronizada e municípios com indicador local de associação espacial (LISA) significativo, "
        "na ameaça (A), na lesão corporal (B), no estupro (C) e no feminicídio tentado (D), Rio Grande do Sul, "
        "2018-2025 (n = 497 municípios)",
        [("a", "taxa ajustada pelo método de Assunção e Reis, expressa em desvios-padrão em relação à média dos "
               "municípios; o sinal desse valor e o da média dos vizinhos definem o quadrante do LISA; classes "
               f"abertas abaixo de −{tabelas.br(LIMITE_Z, 1)} e acima de +{tabelas.br(LIMITE_Z, 1)} ({fora} "
               "municípios)"),
         ("b", "município significativo no desfecho do painel, em qualquer quadrante (direção na Figura 1)"),
         ("c", f"{tabelas.NOTA_ESPERADO} ({aneis})")],
    )


def grava_legenda(nome: str, rotulo: str, texto: str, secao: str, linhas: list[str]) -> None:
    (SAIDA / f"{nome}_legenda.md").write_text(
        f"# {rotulo} — legenda\n\n<!-- Gerado por 03_figuras/gerar_figura1_variantes.py. Não editar à mão. -->\n\n"
        + texto + f"\n\n## {secao}\n\n" + "\n".join(f"- {l}" for l in linhas) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    configura()
    paleta = confere_paleta()
    g = dados()
    a = variante_a(g)
    escala_d, info_d = variante_d(g)
    tabelas.confere(sum(v["aneis"] for v in info_d.values()) == 5, "Figura 2: pares com esperado < 5")
    grava_legenda("figura1", "Figura 1", legenda_a(g), "Conferência da paleta", paleta)
    grava_legenda("figura2", "Figura 2", legenda_d(info_d), "Conferência da escala", escala_d)
    print("\n".join(paleta))
    print(f"Municípios significativos: {int((g['n_desfechos'] > 0).sum())}; "
          f"em 2 desfechos: {int((g['n_desfechos'] == 2).sum())}; "
          f"por direção: {g.loc[g['n_desfechos'] > 0, 'direcao'].value_counts().to_dict()}; "
          f"com anel: {int(g['esperado_baixo'].sum())}")
    print(f"Figura 1 (A): municípios no recorte Litoral {a['n_lit']}, no recorte norte {a['n_nor']}; "
          f"{a['rotulos']} nomes; pares que se tocavam após reduzir a fonte {a['apos_fonte']}; "
          f"nomes retirados {len(a['retirados'])}: {', '.join(a['retirados'])}; "
          f"pares de significativos afastados: {[(f'{x} × {y}', round(float(d), 2)) for (x, y), d in a['afastados']]}; "
          f"fonte dos nomes {a['fontes'][0]:.1f}-{a['fontes'][1]:.1f} pt; escalas "
          + "; ".join(f"{k} 1:{v:,.0f}" for k, v in a["escalas"].items()))
    print("Figura 2 (D), escala:\n" + "\n".join(escala_d))
    print(f"Figura 2 (D): {info_d}")


if __name__ == "__main__":
    main()
