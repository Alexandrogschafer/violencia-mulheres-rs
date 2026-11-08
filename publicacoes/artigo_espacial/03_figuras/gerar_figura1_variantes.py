"""Gera a Figura 1 (variante A) e a Figura 2 (variante D) do artigo espacial, com as legendas.

As variantes B (cartograma) e C (símbolos nos centroides), consideradas na escolha, foram descartadas em
2026-11-08; o desenho anterior da Figura 1 (quatro painéis por quadrante) também. `gerar_figura1.py`
continua como módulo dos dados e da paleta, carregado aqui.

Base comum (denominador feminino, semente 12345, os pares significativos da Tabela 2 e da Tabela
suplementar 2, carregados e conferidos por `gerar_figura1.dados`).

Figura 1 (variante A) — geográfica com recortes, refeita em 2026-11-08 para nomes legíveis: os dois
recortes são os painéis principais, o bloco do norte nos COREDEs Médio Alto Uruguai, Celeiro e Rio da
Várzea (A) e o COREDE Litoral (B); o estado vira um localizador pequeno, num canto, com os retângulos dos
recortes.
- os municípios significativos nos quatro desfechos, num mapa só, com cor por direção: alto-alto,
  baixo-baixo e outlier espacial (alto-baixo e baixo-alto juntos). Um mapa só é possível porque nenhum
  município tem quadrantes diferentes em desfechos diferentes — o script confere isso antes de desenhar e
  para se deixar de valer;
- hachura nos municípios significativos em dois desfechos (nenhum é significativo em mais de dois — também
  conferido);
- anel vazado nos municípios com ao menos um par com menos de 5 eventos esperados;
- não significativos em cinza claro; legenda única, escala e norte; paleta conferida por luminosidade
  (CIE L* e nível de cinza), com os limiares de `gerar_figura1`;
- o localizador é pintado com as mesmas cores, sem texto, porque fora dos recortes ficam 31 municípios
  significativos (os 24 baixo-baixo entre eles) que, de outro modo, sairiam da figura;
- nos recortes, limites municipais visíveis, contorno dos COREDEs e só os municípios significativos
  nomeados (nome oficial do IBGE, em negrito, FONTE_NOME fixa); os vizinhos ficam desenhados e esmaecidos,
  sem nome. A posição dos nomes é escolhida em conjunto (`rotula`): nenhum nome toca outro, os anéis, a
  escala ou o norte, e nenhuma linha de chamada atravessa nome;
- tamanho impresso conferido antes de gravar: nomes e demais textos com pelo menos MINIMO_IMPRESSO_PT na
  menor entre a largura que a figura terá no documento e LARGURA_DOC_CM (15,3 cm); abaixo disso, o script
  para sem gravar.

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
import math
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
from matplotlib.text import Text  # noqa: E402
from matplotlib.transforms import Bbox  # noqa: E402
from PIL import Image  # noqa: E402
import shapely  # noqa: E402
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


def escala_e_norte(ax, km: int, canto: str = "dir", fonte: float = 6.5):
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
    ax.text((x_ini + x_fim) / 2, y_barra + altura * 0.015, f"{km} km", ha="center", va="bottom", fontsize=fonte,
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


# ---------------------------------------------------------------- variante A (Figura 1)

FONTE_NOME = 7.0  # pt, na largura nominal da figura (LARGURA_CM)
FONTE_TEXTO = 7.0  # títulos menores, legenda, nota, escala
LARGURA_DOC_CM = 15.3  # largura de conferência dentro do documento
MINIMO_IMPRESSO_PT = 6.0
# Candidatos de posição do nome, em pt a partir do ponto do município: primeiro no lugar, depois em anéis
# cada vez mais largos, começando pelas direções horizontais.
RAIOS = (0, 6, 10, 14, 18, 23, 28, 34, 40, 47, 55, 64, 74, 85)
ANGULOS = tuple(range(0, 360, 15))


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


def _candidatos(ax, r, m, obstaculos, folga, outros) -> tuple[str, list[dict]]:
    """Posições possíveis do nome de `m`: caixa (px) e linha de chamada de cada candidato que cabe no eixo e
    não toca os obstáculos. A caixa do texto é medida uma vez; as posições são deslocamentos dela.

    Custo: 1,5 por pt de afastamento, 6 pela linha de chamada e 30 por ponto de outro município significativo
    (`outros`, px) coberto pelo nome, para o nome não parecer de quem está embaixo."""
    p = ponto_rotulo(m.geometry)
    ancora = ax.transData.transform((p.x, p.y))
    texto = quebra(m["nome"])
    t = ax.text(p.x, p.y, texto, ha="center", va="center", fontsize=FONTE_NOME, fontweight="bold", linespacing=0.9)
    bb = t.get_window_extent(r)
    t.remove()
    meia_l, meia_a = bb.width / 2 + folga, bb.height / 2 + folga
    eixo = ax.get_window_extent(r)
    px = ax.figure.dpi / 72
    saida = []
    for raio in RAIOS:
        if raio == 0 and m["esperado_baixo"]:
            continue
        for ang in (ANGULOS if raio else (0,)):
            dx, dy = raio * math.cos(math.radians(ang)), raio * math.sin(math.radians(ang))
            cx, cy = ancora[0] + dx * px, ancora[1] + dy * px
            caixa = shapely.box(cx - meia_l, cy - meia_a, cx + meia_l, cy + meia_a)
            x0, y0, x1, y1 = caixa.bounds
            if x0 < eixo.x0 or x1 > eixo.x1 or y0 < eixo.y0 or y1 > eixo.y1:
                continue
            if any(caixa.intersects(o) for o in obstaculos):
                continue
            chamada = None
            if not caixa.contains(shapely.Point(ancora)):
                chamada = shapely.LineString([ancora, (cx, cy)]).difference(caixa)
            cobre = sum(caixa.contains(q) for q in outros)
            custo = 1.5 * raio + (6 if chamada is not None else 0) + 30 * cobre
            saida.append({"raio": raio, "ang": ang, "dx": dx, "dy": dy, "caixa": caixa, "chamada": chamada,
                          "custo": custo, "xy": (p.x, p.y)})
    return texto, saida


def _conflito(a, b) -> float:
    """Custo do par de posições: proibido (1e6) se as caixas se tocam ou uma linha atravessa a outra caixa;
    penalidade leve se as duas linhas de chamada se cruzam."""
    if a["caixa"].intersects(b["caixa"]):
        return 1e6
    if (a["chamada"] is not None and a["chamada"].intersects(b["caixa"])) or (
            b["chamada"] is not None and b["chamada"].intersects(a["caixa"])):
        return 1e6
    if a["chamada"] is not None and b["chamada"] is not None and a["chamada"].intersects(b["chamada"]):
        return 40
    return 0


def rotula(ax, sig, obstaculos, s_anel, rodadas=600, reinicios=30, passo_aleatorio=0.1,
           semente=12345) -> list[dict]:
    """Nomeia todos os municípios de `sig` (nomes com FONTE_NOME fixa; nunca retirados nem encolhidos).

    Cada nome tem candidatos em anéis (RAIOS × ANGULOS) em volta do ponto do município (`_candidatos`). A
    escolha é conjunta (busca local de mínimos conflitos): parte do melhor candidato de cada nome e, em
    rodadas, reescolhe o candidato de um nome em conflito dado o resto (às vezes, ao acaso, para sair de
    impasses), até não haver caixa tocando caixa nem linha de chamada atravessando nome. Com reinícios, fica a
    solução sem conflito de menor custo, depois de uma descida que leva cada nome ao candidato mais barato
    sem conflito (semente fixa, resultado reproduzível). A linha só é traçada quando o ponto do município fica fora da caixa
    do nome. Município com anel (esperado < 5) nunca recebe o nome no lugar, para o anel não cobri-lo. Para se
    sobrar conflito ou se algum nome não tiver candidato."""
    fig = ax.figure
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    folga = 1.5 * fig.dpi / 72
    obst = [shapely.box(o.x0, o.y0, o.x1, o.y1) for o in obstaculos]
    textos, cands = [], []
    pontos = [shapely.Point(ax.transData.transform((q.x, q.y))) for q in map(ponto_rotulo, sig.geometry)]
    for i, (_, m) in enumerate(sig.iterrows()):
        texto, c = _candidatos(ax, r, m, obst, folga, pontos[:i] + pontos[i + 1:])
        tabelas.confere(len(c) > 0, f"nenhuma posição possível para o nome de {m['nome']}")
        textos.append(texto)
        cands.append(c)
    n = len(cands)
    rng = np.random.default_rng(semente)

    def conflitos(esc):
        return [i for i in range(n) if any(_conflito(cands[i][esc[i]], cands[j][esc[j]]) >= 1e6
                                           for j in range(n) if j != i)]

    def total(esc):
        return sum(cands[i][esc[i]]["custo"] for i in range(n)) + sum(
            _conflito(cands[i][esc[i]], cands[j][esc[j]]) for i, j in combinations(range(n), 2))

    melhor_sol = None
    for reinicio in range(reinicios):
        # Primeiro reinício: o melhor candidato de cada nome; os demais, um dos cinco melhores ao acaso.
        escolha = [min(range(len(c)), key=lambda k: c[k]["custo"]) if reinicio == 0 else
                   int(rng.choice(sorted(range(len(c)), key=lambda k: c[k]["custo"])[:5])) for c in cands]
        for _ in range(rodadas):
            em_conflito = conflitos(escolha)
            if not em_conflito:
                break
            i = int(rng.choice(em_conflito))
            if rng.random() < passo_aleatorio:
                escolha[i] = int(rng.integers(len(cands[i])))
                continue
            custos = [cands[i][k]["custo"] + sum(_conflito(cands[i][k], cands[j][escolha[j]])
                                                 for j in range(n) if j != i) for k in range(len(cands[i]))]
            menor = min(custos)
            escolha[i] = int(rng.choice([k for k, c in enumerate(custos) if c <= menor + 1e-9]))
        if conflitos(escolha):
            continue
        # Descida: cada nome vai para o candidato mais barato que não cria conflito, até nada melhorar.
        melhorou = True
        while melhorou:
            melhorou = False
            for i in range(n):
                custos = [cands[i][k]["custo"] + sum(_conflito(cands[i][k], cands[j][escolha[j]])
                                                     for j in range(n) if j != i) for k in range(len(cands[i]))]
                k = min(range(len(custos)), key=custos.__getitem__)
                atual = custos[escolha[i]]
                if custos[k] < atual - 1e-9:
                    escolha[i] = k
                    melhorou = True
        if melhor_sol is None or total(escolha) < total(melhor_sol):
            melhor_sol = list(escolha)
    escolha = melhor_sol if melhor_sol is not None else escolha
    em_conflito = sorted({sig.iloc[i]["nome"] for i in conflitos(escolha)})
    tabelas.confere(not em_conflito, f"nomes que não se acomodam: {', '.join(em_conflito)}")

    saida = []
    for i, (_, m) in enumerate(sig.iterrows()):
        c = cands[i][escolha[i]]
        escuro = c["raio"] == 0 and m["direcao"] in ("BB", "AA")
        cor, halo = ("white", COR_TRACO) if escuro else ("#1a1a1a", "white")
        seta = None
        if c["chamada"] is not None:
            seta = {"arrowstyle": "-", "color": COR_TRACO, "lw": 0.5, "shrinkA": 1,
                    "shrinkB": (math.sqrt(s_anel) / 2 + 0.5) if m["esperado_baixo"] else 0}
        t = ax.annotate(textos[i], xy=c["xy"], xytext=(c["dx"], c["dy"]), textcoords="offset points", ha="center",
                        va="center", fontsize=FONTE_NOME, fontweight="bold", color=cor, linespacing=0.9, zorder=7,
                        arrowprops=seta, path_effects=[pe.withStroke(linewidth=1.6, foreground=halo, alpha=0.9)])
        if t.arrow_patch is not None:
            t.arrow_patch.set_path_effects([pe.withStroke(linewidth=1.6, foreground="white")])
        saida.append({"nome": m["nome"], "texto": t, "raio": c["raio"], "chamada": c["chamada"] is not None})
    # Conferência independente, no desenho final: nenhuma caixa de nome toca outra.
    fig.canvas.draw()
    caixas = [shapely.box(*_caixa_texto(s_["texto"], r)) for s_ in saida]
    tocam = [(saida[a]["nome"], saida[b]["nome"]) for a, b in combinations(range(n), 2)
             if caixas[a].intersects(caixas[b])]
    tabelas.confere(not tocam, f"nomes que se tocam no desenho final: {tocam}")
    return saida


def _caixa_texto(t, r):
    """Caixa só do texto de uma anotação (sem a linha de chamada), em px; vale depois de um draw, que fixa a
    posição deslocada da anotação."""
    b = Text.get_window_extent(t, r)
    return b.x0, b.y0, b.x1, b.y1


def _novos(ax, antes):
    return [a for a in ax.get_children() if a not in antes]


def recorte(ax, g, coredes, km, titulo, canto="esq", s_anel=70):
    dentro = g[g["corede"].isin(coredes)]
    ajusta(ax, dentro, folga=0.04)
    # Vizinhança em volta, esmaecida, para situar o recorte; sem nomes.
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    fora = g[~g["corede"].isin(coredes)].cx[x0:x1, y0:y1]
    pinta(ax, fora, borda=0.3)
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor="white", alpha=0.55, edgecolor="none", zorder=3))
    dentro.plot(ax=ax, color=dentro["direcao"].map(CORES), edgecolor="#6b6b6b", linewidth=0.35, zorder=4)
    duplos = dentro[dentro["n_desfechos"] == 2]
    if len(duplos):
        duplos.plot(ax=ax, facecolor="none", edgecolor=COR_HACHURA, linewidth=0, hatch=HACHURA, zorder=4.5)
        duplos.boundary.plot(ax=ax, color="#6b6b6b", linewidth=0.35, zorder=4.6)
    dentro.dissolve("corede").boundary.plot(ax=ax, color=COR_TRACO, linewidth=0.9, zorder=4.7)
    marc = dentro[dentro["esperado_baixo"]]
    pm = gpd.GeoSeries([ponto_rotulo(x) for x in marc.geometry])
    ax.scatter(pm.x, pm.y, s=s_anel, facecolor="none", edgecolor="white", linewidth=2.2, zorder=5)
    ax.scatter(pm.x, pm.y, s=s_anel, facecolor="none", edgecolor="black", linewidth=0.8, zorder=6)
    ax.set_title(titulo, loc="left", fontsize=8.5, fontweight="bold")
    antes = set(ax.get_children())
    escala_e_norte(ax, km, canto=canto, fonte=FONTE_TEXTO)
    ax.figure.canvas.draw()
    r = ax.figure.canvas.get_renderer()
    obst = [a.get_window_extent(r) for a in _novos(ax, antes)]
    # Os anéis também são obstáculos: nenhum nome por cima deles.
    raio_px = (math.sqrt(s_anel) / 2 + 1.2) * ax.figure.dpi / 72
    for x, y in ax.transData.transform(np.column_stack([pm.x, pm.y])) if len(pm) else []:
        obst.append(Bbox.from_extents(x - raio_px, y - raio_px, x + raio_px, y + raio_px))
    nomes = rotula(ax, dentro[dentro["direcao"] != "NS"], obst, s_anel)
    return dentro, nomes


def localizador(ax, g):
    """Miniatura do estado com as cores de direção (os significativos fora dos recortes continuam na figura),
    sem nomes, com os retângulos dos dois recortes."""
    pinta(ax, g, borda=0.08)
    g.dissolve().boundary.plot(ax=ax, color=COR_TRACO, linewidth=0.4)
    aneis(ax, g, s=9)
    ajusta(ax, g, folga=0.02)
    for coredes, letra, lado in ((NORTE, "A", "right"), (LITORAL, "B", "left")):
        x0, y0, x1, y1 = g[g["corede"].isin(coredes)].total_bounds
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor="none", edgecolor="black", linewidth=0.8,
                               zorder=8))
        ax.text(x0 if lado == "right" else x1, y1, f" {letra} ", ha=lado, va="top", fontsize=FONTE_TEXTO + 0.5,
                fontweight="bold", zorder=8)


def variante_a(g):
    largura_pol = LARGURA_CM / 2.54
    altura_pol = largura_pol * 0.80
    fig = plt.figure(figsize=(largura_pol, altura_pol))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.95, 1.0], height_ratios=[2.15, 1.0],
                          left=0.01, right=0.99, top=0.94, bottom=0.01, wspace=0.03, hspace=0.12)
    ax_n = fig.add_subplot(gs[0, 0])
    ax_lit = fig.add_subplot(gs[0, 1])
    baixo = gs[1, :].subgridspec(1, 3, width_ratios=[1.0, 1.25, 1.25], wspace=0.04)
    ax_loc = fig.add_subplot(baixo[0, 0])
    ax_nota = fig.add_subplot(baixo[0, 1])
    ax_leg = fig.add_subplot(baixo[0, 2])
    ax_nota.set_axis_off()
    ax_leg.set_axis_off()

    localizador(ax_loc, g)
    nor, nomes_nor = recorte(ax_n, g, NORTE, 20, "A  COREDEs Médio Alto Uruguai, Celeiro e Rio da Várzea")
    lit, nomes_lit = recorte(ax_lit, g, LITORAL, 20, "B  COREDE Litoral", canto="dir")
    nomes = nomes_nor + nomes_lit
    n_sig = int(((nor["direcao"] != "NS").sum() + (lit["direcao"] != "NS").sum()))
    tabelas.confere(len(nomes) == n_sig, "município significativo sem nome nos recortes")
    ax_leg.legend(handles=entradas_legenda(), loc="center left", frameon=False, fontsize=FONTE_TEXTO,
                  handlelength=1.6, labelspacing=0.8, borderaxespad=0)
    nota = ("Nos recortes, só os municípios\nsignificativos são nomeados; linha\ngrossa: limite de COREDE; em volta,\n"
            "esmaecidos, os municípios vizinhos.\nÀ esquerda, o estado, com os\nretângulos dos recortes A e B.")
    ax_nota.text(0.02, 0.5, nota, transform=ax_nota.transAxes, fontsize=FONTE_TEXTO, va="center", color="#333333",
                 linespacing=1.25)

    # Tamanho impresso: a figura entra no documento na largura que build_docx der a ela (17 cm, ou menos se a
    # altura passar de 19 cm); a conferência usa a menor entre essa e LARGURA_DOC_CM.
    altura_cm = LARGURA_CM * 0.80
    largura_doc = min(LARGURA_CM, 19.0 * LARGURA_CM / altura_cm, LARGURA_DOC_CM)
    fator = largura_doc / LARGURA_CM
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    textos = [t for a in fig.axes for t in a.texts] + [a.title for a in fig.axes if a.get_title(loc="left")]
    textos = [t for t in textos if t.get_text().strip()] + list(ax_leg.get_legend().get_texts())
    menor_nome = min(n["texto"].get_fontsize() for n in nomes) * fator
    menor_texto = min(t.get_fontsize() for t in textos) * fator
    tabelas.confere(menor_texto >= MINIMO_IMPRESSO_PT,
                    f"texto com {menor_texto:.2f} pt impressos a {largura_doc} cm, abaixo de {MINIMO_IMPRESSO_PT}")
    tabelas.confere(menor_nome >= MINIMO_IMPRESSO_PT,
                    f"nomes com {menor_nome:.2f} pt impressos a {largura_doc} cm, abaixo de {MINIMO_IMPRESSO_PT}")
    escalas = {k: escala_numerica(fig, a) for k, a in (("A", ax_n), ("B", ax_lit), ("localizador", ax_loc))}
    grava(fig, "figura1")
    return {"escalas": escalas, "n_lit": len(lit), "n_nor": len(nor), "nomes": len(nomes),
            "fora_do_lugar": sorted(n["nome"] for n in nomes if n["chamada"]), "largura_doc": largura_doc,
            "menor_nome_impresso": round(menor_nome, 2), "menor_texto_impresso": round(menor_texto, 2),
            "altura_cm": altura_cm}


def legenda_a(g) -> str:
    """Legenda no padrão RESS (o das tabelas): título sem ponto final, com local, anos e n; notas em letras
    minúsculas sobrescritas; sem detalhes de método, que ficam nos Métodos."""
    n_anel = int(g["esperado_baixo"].sum())
    return tabelas.legenda(
        "Figura 1",
        "Municípios com indicador local de associação espacial (LISA) significativo em ao menos um de quatro "
        "desfechos de violência contra a mulher (ameaça, lesão corporal, estupro e feminicídio tentado), por "
        "direção, nos Conselhos Regionais de Desenvolvimento (COREDEs) Médio Alto Uruguai, Celeiro e Rio da "
        "Várzea (A) e no COREDE Litoral (B), com o estado inteiro no mapa de localização, Rio Grande do Sul, "
        "2018-2025 (n = 497 municípios)",
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
    print(f"Figura 1 (A): municípios no recorte norte {a['n_nor']}, no Litoral {a['n_lit']}; {a['nomes']} nomes, "
          f"fora do lugar (com linha de chamada) {len(a['fora_do_lugar'])}: {', '.join(a['fora_do_lugar'])}; "
          f"figura {LARGURA_CM} × {a['altura_cm']:.1f} cm, conferida a {a['largura_doc']} cm: menor nome "
          f"{a['menor_nome_impresso']} pt, menor texto {a['menor_texto_impresso']} pt; escalas "
          + "; ".join(f"{k} 1:{v:,.0f}" for k, v in a["escalas"].items()))
    print("Figura 2 (D), escala:\n" + "\n".join(escala_d))
    print(f"Figura 2 (D): {info_d}")


if __name__ == "__main__":
    main()
