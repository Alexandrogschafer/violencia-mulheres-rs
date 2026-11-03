"""Gera a Figura 1 do artigo espacial: quadrantes do LISA por município, um painel por desfecho.

Dados: os mesmos da Tabela 2 e da Tabela suplementar 2, com o denominador feminino, 2018-2025, semente
12345, 99.999 permutações, Benjamini-Hochberg a 5% sobre o p direcional e ajuste de Assunção e Reis.
Os pares significativos vêm de `carregar_lisa` (via `03_tabelas/gerar_tabelas.py`), e o esperado sob a
taxa estadual vem de `esperado_vs_observado_lisa.calcular`. Antes de desenhar, as contagens por desfecho
e quadrante são conferidas contra `outputs/tables/resultados_consolidados.md`.

Cartografia:
- SIRGAS 2000 / Brazil Polyconic (EPSG:5880), o CRS de desenho do restante do projeto
  (`mapa_choropleth.CRS_PLOT`);
- escala gráfica de 100 km e seta de norte em cada painel (`mapa_choropleth._adiciona_escala_e_norte`);
- legenda única para os quatro painéis, que são identificados por letras maiúsculas, como pede a RESS
  para mosaicos.

Cores: os cinco preenchimentos (quatro quadrantes e não significativo) precisam se distinguir pela
luminosidade, e não só pelo matiz, para a figura funcionar em escala de cinza. O script confere, antes de
desenhar, que a diferença de luminosidade CIE L* entre quaisquer dois preenchimentos é de pelo menos
`DELTA_L_MINIMO` e que os níveis de cinza (luminância de PIL «L», a de uma fotocópia) diferem em pelo menos
`DELTA_CINZA_MINIMO`. Pares com menos de 5 eventos esperados recebem um anel vazado preto com halo branco, legível sobre
qualquer preenchimento, que deixa a cor do município visível e tem entrada própria na legenda.

Saída em publicacoes/artigo_espacial/03_figuras/:
- `figura1.pdf`, vetorial, com as fontes embutidas como TrueType;
- `figura1.png`, a 300 dpi;
- `figura1_cinza.png`, a mesma figura convertida para escala de cinza, só para conferência;
- `figura1_legenda.md`, com a legenda.

Uso, da raiz do repositório:
    python3 publicacoes/artigo_espacial/03_figuras/gerar_figura1.py
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
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from PIL import Image  # noqa: E402

from src.analysis.esperado_vs_observado_lisa import LIMIAR, calcular  # noqa: E402
from src.analysis.mapa_choropleth import BARRA_ESCALA_KM, CRS_PLOT, _adiciona_escala_e_norte, montar_geodataframe  # noqa: E402
from src.analysis.moran_lisa_assuncao_reis import ANO_FIM, ANO_INICIO, N_MUNICIPIOS  # noqa: E402
from src.analysis.resultados_consolidados import LISA, QUADRANTES  # noqa: E402

_spec = importlib.util.spec_from_file_location("gerar_tabelas", RAIZ / "publicacoes/artigo_espacial/03_tabelas/gerar_tabelas.py")
tabelas = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tabelas)

SAIDA = Path(__file__).resolve().parent
TABLES = RAIZ / "outputs" / "tables"

# Do mais escuro ao mais claro. Vermelho para «alto», azul para «baixo», como na convenção do projeto
# (clusters_lisa.py); a ordem de luminosidade é o que garante a leitura em cinza.
CORES = {
    "BB": "#053061",
    "AA": "#c0392b",
    "BA": "#5a9bd0",
    "AB": "#f6b39a",
    "NS": "#f0efeb",
}
ROTULOS = {
    "AA": "Alto-alto",
    "BB": "Baixo-baixo",
    "AB": "Alto-baixo",
    "BA": "Baixo-alto",
    "NS": "Não significativo",
}
ROTULO_MARCA = f"Menos de {LIMIAR} eventos esperados: mantido no cálculo, fora da interpretação"
DELTA_L_MINIMO = 15.0
DELTA_CINZA_MINIMO = 40
LARGURA_CM = 17.0  # cabe em A4 com margens de 1,5 cm (18 cm úteis)
LETRAS = "ABCD"


# ---------------------------------------------------------------- cor


def _rgb(h: str) -> tuple[float, float, float]:
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


def luminosidade_lab(h: str) -> float:
    """L* da CIE 1976 a partir de sRGB (iluminante D65)."""
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in _rgb(h)]
    y = 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
    f = y ** (1 / 3) if y > 216 / 24389 else (24389 / 27 * y + 16) / 116
    return 116 * f - 16


def nivel_cinza(h: str) -> int:
    """Luminância de PIL «L» (ITU-R 601-2), a mesma de figuras_capitulo._gerar_pb."""
    r, g, b = (round(c * 255) for c in _rgb(h))
    return round(0.299 * r + 0.587 * g + 0.114 * b)


def confere_paleta() -> list[str]:
    linhas = []
    for a, b in combinations(CORES, 2):
        dl = abs(luminosidade_lab(CORES[a]) - luminosidade_lab(CORES[b]))
        dc = abs(nivel_cinza(CORES[a]) - nivel_cinza(CORES[b]))
        if dl < DELTA_L_MINIMO or dc < DELTA_CINZA_MINIMO:
            sys.exit(f"Paleta reprovada: {a} × {b} com ΔL* = {dl:.1f} e Δcinza = {dc}.")
    for k, c in CORES.items():
        linhas.append(f"{ROTULOS[k]}: {c}, L* = {luminosidade_lab(c):.1f}, cinza = {nivel_cinza(c)}")
    menor_l = min(abs(luminosidade_lab(CORES[a]) - luminosidade_lab(CORES[b])) for a, b in combinations(CORES, 2))
    menor_c = min(abs(nivel_cinza(CORES[a]) - nivel_cinza(CORES[b])) for a, b in combinations(CORES, 2))
    linhas.append(f"Menor diferença entre dois preenchimentos: ΔL* = {menor_l:.1f}; Δcinza = {menor_c}")
    return linhas


# ---------------------------------------------------------------- dados


def dados():
    sig = tabelas.significativos()
    ref = tabelas.le_tabela_md(TABLES / "resultados_consolidados.md", "Desfecho").set_index("Desfecho")
    for d in LISA:
        for q in QUADRANTES:
            n = int(((sig["tipo_crime"] == d) & (sig["categoria"] == q)).sum())
            tabelas.confere(str(n) == ref.loc[d, f"LISA {q}"], f"Figura 1, {d} {q}")
    pares, _, _ = calcular("feminina")
    abaixo = set(zip(pares.loc[pares["esperado"] < LIMIAR, "municipio"], pares.loc[pares["esperado"] < LIMIAR, "desfecho"]))
    malha = montar_geodataframe(LISA[0], ANO_INICIO, ANO_FIM)[["municipio", "geometry"]].to_crs(CRS_PLOT)
    tabelas.confere(len(malha) == N_MUNICIPIOS, "malha sem os 497 municípios")
    return sig, abaixo, malha


# ---------------------------------------------------------------- desenho


def desenha(sig, abaixo, malha):
    plt.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42, "font.size": 8})
    largura_pol = LARGURA_CM / 2.54
    fig, eixos = plt.subplots(2, 2, figsize=(largura_pol, largura_pol * 0.93))
    contorno = malha.dissolve()
    escalas = []
    for ax, letra, d in zip(eixos.flat, LETRAS, LISA):
        q = sig[sig["tipo_crime"] == d].set_index("municipio")["categoria"]
        g = malha.assign(classe=malha["municipio"].map(q).fillna("NS"))
        g.plot(ax=ax, color=g["classe"].map(CORES), edgecolor="white", linewidth=0.15)
        contorno.boundary.plot(ax=ax, color="#3a3a3a", linewidth=0.5)
        marcados = g[g["municipio"].isin({m for m, t in abaixo if t == d})]
        pontos = marcados.geometry.representative_point()
        # Anel vazado: o preenchimento do município continua visível dentro dele; o halo branco por baixo
        # mantém o anel legível sobre os preenchimentos escuros.
        ax.scatter(pontos.x, pontos.y, s=22, facecolor="none", edgecolor="white", linewidth=2.2, zorder=5)
        ax.scatter(pontos.x, pontos.y, s=22, facecolor="none", edgecolor="black", linewidth=0.8, zorder=6)
        ax.set_axis_off()
        ax.set_title(f"{letra}  {d.capitalize()}", loc="left", fontsize=9, fontweight="bold")
        _adiciona_escala_e_norte(ax, espaco_vertical=1.6)
        escalas.append((ax, marcados))
    entradas = [Patch(facecolor=CORES[k], edgecolor="#9a9a9a", linewidth=0.4, label=ROTULOS[k])
                for k in ["AA", "BB", "AB", "BA", "NS"]]
    entradas.append(Line2D([], [], marker="o", linestyle="", markersize=5, markerfacecolor="none",
                           markeredgecolor="black", markeredgewidth=0.8, label=ROTULO_MARCA))
    fig.legend(handles=entradas, loc="lower center", ncol=3, frameon=False, fontsize=7.5,
               handlelength=1.4, columnspacing=1.2, bbox_to_anchor=(0.5, 0.0))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.94, bottom=0.11, wspace=0.03, hspace=0.10)

    # Escala numérica na largura de impressão: largura do eixo em cm sobre a extensão em metros.
    fig.canvas.draw()
    ax = eixos.flat[0]
    largura_eixo_cm = ax.get_window_extent().width / fig.dpi * 2.54
    extensao_m = ax.get_xlim()[1] - ax.get_xlim()[0]
    escala = extensao_m * 100 / largura_eixo_cm
    return fig, escala, {d: len(m) for (_, m), d in zip(escalas, LISA)}


def legenda(escala: float, marcados: dict) -> str:
    arredondada = round(escala / 500_000) * 500_000
    return (
        "**Figura 1.** Municípios com indicador local de associação espacial (LISA) significativo, por quadrante, "
        "na ameaça (A), na lesão corporal (B), no estupro (C) e no feminicídio tentado (D), Rio Grande do Sul, "
        "2018-2025 (n = 497 municípios)\n\n"
        "Nota: taxas por 100 mil mulheres-ano, com o ajuste de Assunção e Reis. Significância por 99.999 "
        "permutações condicionais (semente 12345), com controle de Benjamini-Hochberg a 5% sobre o valor p "
        "direcional. Alto-alto e baixo-baixo: município com valor alto (baixo) cercado de vizinhos com valores "
        "altos (baixos); alto-baixo e baixo-alto: outliers espaciais. «Alto» e «baixo» referem-se à média dos "
        "municípios, e não à taxa estadual. O anel vazado marca os pares com menos de "
        f"{LIMIAR} eventos esperados sob a taxa estadual "
        f"({', '.join(f'{LETRAS[i]}: {marcados[d]}' for i, d in enumerate(LISA))}), mantidos no cálculo, mas "
        "sem interpretação substantiva. O feminicídio consumado não foi analisado no nível local, pela baixa "
        f"ocorrência. Projeção policônica, SIRGAS 2000. Escala gráfica de {BARRA_ESCALA_KM} km em cada painel; "
        f"na impressão com {br_cm(LARGURA_CM)} cm de largura, a escala é de cerca de 1:{milhar(arredondada)}."
    )


def milhar(x: float) -> str:
    return f"{x:,.0f}".replace(",", ".")


def br_cm(x: float) -> str:
    return f"{x:.1f}".replace(".", ",").replace(",0", "")


def main() -> None:
    paleta = confere_paleta()
    sig, abaixo, malha = dados()
    fig, escala, marcados = desenha(sig, abaixo, malha)
    tabelas.confere(sum(marcados.values()) == len(abaixo), "marcas de esperado < 5 não batem com os pares")
    fig.savefig(SAIDA / "figura1.pdf")
    fig.savefig(SAIDA / "figura1.png", dpi=300)
    plt.close(fig)
    Image.open(SAIDA / "figura1.png").convert("L").save(SAIDA / "figura1_cinza.png", dpi=(300, 300))
    texto = legenda(escala, marcados)
    (SAIDA / "figura1_legenda.md").write_text(
        "# Figura 1 — legenda\n\n<!-- Gerado por 03_figuras/gerar_figura1.py. Não editar à mão. -->\n\n"
        + texto + "\n\n## Conferência da paleta\n\n" + "\n".join(f"- {l}" for l in paleta) + "\n",
        encoding="utf-8",
    )
    print("\n".join(paleta))
    print(f"Escala na largura de impressão: 1:{escala:,.0f}; marcas por painel: {marcados}")


if __name__ == "__main__":
    main()
