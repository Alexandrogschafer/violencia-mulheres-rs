"""Dados e paleta da Figura 1 do artigo espacial, usados por `gerar_figura1_variantes.py`.

Este módulo não desenha nem grava nada. O desenho anterior da Figura 1 (quadrantes do LISA, um painel por
desfecho) foi substituído em 2026-11-08 pela variante A de `gerar_figura1_variantes.py`, que grava os
`figura1.*`; o que resta aqui é a parte de que aquele script depende.

Dados: os mesmos da Tabela 2 e da Tabela suplementar 1, com o denominador feminino, 2018-2025, semente
12345, 99.999 permutações, Benjamini-Hochberg a 5% sobre o p direcional e ajuste de Assunção e Reis.
Os pares significativos vêm de `carregar_lisa` (via `03_tabelas/gerar_tabelas.py`), e o esperado sob a
taxa estadual vem de `esperado_vs_observado_lisa.calcular`. Antes de devolver os dados, `dados` confere as
contagens por desfecho e quadrante contra `outputs/tables/resultados_consolidados.md`. A malha está em
SIRGAS 2000 / Brazil Polyconic (EPSG:5880), o CRS de desenho do restante do projeto
(`mapa_choropleth.CRS_PLOT`).

Cores: os preenchimentos precisam se distinguir pela luminosidade, e não só pelo matiz, para a figura
funcionar em escala de cinza. `luminosidade_lab` (CIE L*) e `nivel_cinza` (luminância de PIL «L», a de
uma fotocópia) medem isso, com os limiares `DELTA_L_MINIMO` e `DELTA_CINZA_MINIMO`.
"""

import importlib.util
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ))

from src.analysis.esperado_vs_observado_lisa import LIMIAR, calcular  # noqa: E402
from src.analysis.mapa_choropleth import BARRA_ESCALA_KM, CRS_PLOT, montar_geodataframe  # noqa: E402
from src.analysis.moran_lisa_assuncao_reis import ANO_FIM, ANO_INICIO, N_MUNICIPIOS  # noqa: E402
from src.analysis.resultados_consolidados import LISA, QUADRANTES  # noqa: E402

_spec = importlib.util.spec_from_file_location("gerar_tabelas", RAIZ / "publicacoes/artigo_espacial/03_tabelas/gerar_tabelas.py")
tabelas = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tabelas)

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
