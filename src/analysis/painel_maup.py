"""Painel triplo do efeito da unidade de área modificável (MAUP) --
Seção 5.5 do capítulo, figura fig05_maup_tres_niveis.png: a mesma
categoria (Estupro) e o mesmo período (2018-2025), mapeados em três
níveis de agregação (município, COREDE, região geográfica intermediária)
com os MESMOS cortes de classe, calculados uma única vez sobre a
distribuição municipal (a mesma da fig04). Reaproveita
src.analysis.tabela_agregacao_regional (Tarefa 1 desta sessão) para as
taxas e a convenção de elegibilidade (piso), e
src.analysis.mapa_choropleth para paleta, CRS de plot e o desenho de
escala/norte -- figura e tabela não podem divergir porque usam as mesmas
funções.

Por que os três painéis usam os mesmos cortes: se cada nível fosse
classificado pela própria distribuição, os três painéis pareceriam
igualmente variados (cada um sempre tem uma classe mais clara e uma mais
escura, não importa a amplitude real dos valores) -- o oposto do que a
figura precisa mostrar. Com cortes fixos, o painel de menor amplitude
real (região intermediária) fica visualmente quase monocromático, e essa
falta de variação de cor *é* o resultado, não um defeito da figura.

Uso: python -m src.analysis.painel_maup
"""

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch
from PIL import Image

from src.analysis.mapa_choropleth import (
    COR_ABAIXO_PISO,
    CRS_PLOT,
    PALETAS,
    _adiciona_escala_e_norte,
    _classes_quantis,
    _fmt_brl,
)
from src.analysis.tabela_agregacao_regional import (
    ANO_FIM,
    ANO_INICIO,
    POP_MINIMA_PADRAO,
    calcular_agregacao_regional,
    calcular_taxas_municipio,
    carregar_mapeamento_corede,
    carregar_mapeamento_regioes_ibge,
)
from src.fetch_malha_municipios import carregar_malha_com_municipio

FIGURAS_DIR = (
    Path(__file__).resolve().parent.parent.parent
    / "publicacoes"
    / "cap_geotecnologias"
    / "03_figuras"
)

TIPO_CRIME = "Estupro"  # categoria de menor amplitude relativa, a que melhor evidencia o MAUP (Seção 5.3/5.5)
N_CLASSES = 5
PALETA = "roxo"
DPI_IMPRESSAO = 300

# Figura gerada JÁ no tamanho real de impressão (15 cm de largura), não num
# canvas maior reduzido depois: fontsize em matplotlib é em pontos (1/72 in),
# uma unidade física absoluta ligada ao figsize em polegadas no momento da
# criação -- gerar grande e encolher via bbox_inches/PIL depois faz o texto
# ficar ilegível no tamanho impresso real (~3-4 pt), mesmo que o padrão de
# cor continue legível. Ver diagnóstico desta sessão (simulação por
# redimensionamento com PIL do canvas antigo de figsize=(14, 5.4)).
LARGURA_FIG_IN = 15 / 2.54  # 15 cm, largura de impressão do capítulo
ALTURA_FIG_IN = 2.7  # linha de mapas (~1,86 in, aspecto do RS) + rótulos + legenda em 2 linhas abaixo

# Fronteira municipal OMITIDA no painel de município (edgecolor="none"): com
# ~266 unidades espremidas em ~1,9 in de largura, uma linha de fronteira --
# mesmo fina -- vira malha borrada, não textura. O painel municipal existe
# para comunicar "muitas unidades, muita variação", não para que se
# identifique município a município (isso já é o papel da fig04, em largura
# cheia) -- perda de legibilidade da fronteira aqui é intencional, não um
# defeito. COREDE e região intermediária têm poucas unidades grandes: a
# fronteira continua visível e comunicando algo (decisão explícita do
# usuário nesta sessão).
LARGURA_BORDA_MUNICIPIO = 0.0
LARGURA_BORDA_REGIONAL = 0.4

NIVEIS = [
    ("municipio", "Município"),
    ("corede", "COREDE"),
    ("regiao_intermediaria", "Região intermediária"),
]


def _malha_municipio() -> gpd.GeoDataFrame:
    return carregar_malha_com_municipio()[["municipio", "geometry"]]


def _malha_dissolvida(nivel: str) -> gpd.GeoDataFrame:
    """Geometria de COREDE ou região intermediária = união dos municípios
    que a compõem (mesma malha do IBGE usada no nível municipal -- não é
    uma malha própria de COREDE, que o IBGE não define)."""
    malha = _malha_municipio()
    if nivel == "corede":
        mapeamento = carregar_mapeamento_corede()[["municipio", "corede"]]
    else:
        mapeamento = carregar_mapeamento_regioes_ibge()[["municipio", "regiao_intermediaria"]]
    coluna = "corede" if nivel == "corede" else "regiao_intermediaria"
    unido = malha.merge(mapeamento, on="municipio", how="left")
    dissolvido = unido.dissolve(by=coluna, as_index=False)
    return dissolvido.rename(columns={coluna: "regiao"})


def _monta_camada(nivel: str) -> tuple[gpd.GeoDataFrame, pd.Series]:
    """Retorna (geometria+taxa+classe já em CRS_PLOT, série de piso quando
    nivel="municipio", None nos demais níveis)."""
    if nivel == "municipio":
        base = calcular_taxas_municipio(TIPO_CRIME, ANO_INICIO, ANO_FIM, POP_MINIMA_PADRAO)
        malha = _malha_municipio()
        camada = malha.merge(base, on="municipio", how="left")
        piso_mask = ~camada["elegivel"].fillna(False)
        return camada.to_crs(CRS_PLOT), piso_mask
    else:
        agregado = calcular_agregacao_regional(TIPO_CRIME, nivel, ANO_INICIO, ANO_FIM, POP_MINIMA_PADRAO)
        malha_diss = _malha_dissolvida(nivel)
        camada = malha_diss.merge(agregado, on="regiao", how="left")
        return camada.to_crs(CRS_PLOT), None


def gerar_painel() -> dict:
    cmap = PALETAS[PALETA]["cmap"]()
    faixa_lo, faixa_hi = PALETAS[PALETA]["faixa"]

    # Cortes calculados uma única vez, sobre a distribuição MUNICIPAL
    # elegível -- mesma função usada por mapa_choropleth.gerar_mapa no modo
    # "quantis", garantindo que batem com os da fig04 (conferido: sim, ver
    # diagnóstico desta sessão).
    base_municipio = calcular_taxas_municipio(TIPO_CRIME, ANO_INICIO, ANO_FIM, POP_MINIMA_PADRAO)
    valores_municipio = base_municipio.loc[base_municipio["elegivel"], "taxa_por_100mil_hab"]
    _, edges = _classes_quantis(valores_municipio, N_CLASSES)
    n_classes_reais = len(edges) - 1
    cores_classes = [
        cmap(faixa_lo + (faixa_hi - faixa_lo) * i / max(n_classes_reais - 1, 1))
        for i in range(n_classes_reais)
    ]

    fig, eixos = plt.subplots(1, 3, figsize=(LARGURA_FIG_IN, ALTURA_FIG_IN))
    # Posições dos eixos fixadas ANTES de plotar/rotular -- os rótulos abaixo
    # de cada painel usam fig.text() com o centro de ax.get_position(), não
    # ax.transAxes, para cair de forma confiável na margem inferior reservada
    # da FIGURA (fração fixa da altura real de 2,45 in), não numa fração da
    # caixa de cada eixo (que muda de tamanho conforme o aspecto do mapa
    # equal-aspect dentro dela).
    fig.subplots_adjust(top=0.99, bottom=0.31, left=0.01, right=0.99, wspace=0.025)

    resultados = {}
    for (nivel, rotulo), ax in zip(NIVEIS, eixos):
        camada, piso_mask = _monta_camada(nivel)
        taxas = camada["taxa_por_100mil_hab"]
        classes = pd.cut(taxas, bins=edges, labels=False, include_lowest=True)

        if piso_mask is not None:
            camada_valida = camada[~piso_mask]
            classes_validas = classes[~piso_mask]
        else:
            camada_valida = camada
            classes_validas = classes

        largura_borda = LARGURA_BORDA_MUNICIPIO if nivel == "municipio" else LARGURA_BORDA_REGIONAL
        cor_borda = "none" if largura_borda == 0 else "white"

        for i in range(n_classes_reais):
            subset_idx = classes_validas.index[classes_validas == i]
            if len(subset_idx) == 0:
                continue
            camada_valida.loc[subset_idx].plot(color=cores_classes[i], linewidth=largura_borda, edgecolor=cor_borda, ax=ax)

        if piso_mask is not None and piso_mask.any():
            camada[piso_mask].plot(color=COR_ABAIXO_PISO, linewidth=largura_borda, edgecolor=cor_borda, ax=ax)

        ax.set_axis_off()
        n_unidades = int((~piso_mask).sum()) if piso_mask is not None else len(camada)
        centro_x = (ax.get_position().x0 + ax.get_position().x1) / 2
        fig.text(
            centro_x, 0.27, f"{rotulo} (n = {n_unidades})",
            ha="center", va="top", fontsize=7,
        )

        n_por_classe = classes_validas.value_counts().reindex(range(n_classes_reais), fill_value=0).to_dict()
        resultados[nivel] = {
            "rotulo": rotulo,
            "n_unidades": n_unidades,
            "minimo": float(taxas[~piso_mask].min()) if piso_mask is not None else float(taxas.min()),
            "maximo": float(taxas[~piso_mask].max()) if piso_mask is not None else float(taxas.max()),
            "n_por_classe": n_por_classe,
        }

    for r in resultados.values():
        r["razao"] = r["maximo"] / r["minimo"] if r["minimo"] else float("inf")

    # Escala gráfica e norte uma única vez, no primeiro painel (município).
    # espaco_vertical maior que o padrão (ver docstring da função): este
    # painel é bem menor fisicamente que as figuras de mapa único do
    # capítulo, e o espaçamento default (calibrado para 8 pol.) fazia a
    # seta de norte sobrepor o texto "100 km" a este tamanho.
    _adiciona_escala_e_norte(eixos[0], espaco_vertical=3.5)

    # Legenda única, compartilhada pelos três painéis -- não uma por painel.
    legend_handles = [
        Patch(facecolor=cores_classes[i], edgecolor="none", label=f"{_fmt_brl(edges[i], 1)} – {_fmt_brl(edges[i + 1], 1)}")
        for i in range(n_classes_reais)
    ]
    legend_handles.append(
        Patch(facecolor=COR_ABAIXO_PISO, edgecolor="none", label=f"População inferior a {_fmt_brl(POP_MINIMA_PADRAO, 0)} hab.")
    )
    # Fonte de legenda/rótulo nunca menor que 6 pt reais (exigência do
    # usuário): como a figura já é gerada no tamanho físico final (15 cm,
    # LARGURA_FIG_IN), o fontsize abaixo É o tamanho impresso, sem
    # reescalonamento posterior.
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        ncol=3,
        fontsize=7,
        frameon=False,
        title=f"{TIPO_CRIME} — taxa por 100 mil hab. ({ANO_INICIO}–{ANO_FIM})",
        title_fontsize=7.5,
        bbox_to_anchor=(0.5, 0.01),
    )

    caminho_saida = FIGURAS_DIR / "fig05_maup_tres_niveis.png"
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    # Sem bbox_inches="tight": recortar a figura depois mudaria a largura
    # final em relação aos 15 cm pretendidos, alterando o tamanho impresso
    # relativo do texto (o próprio problema que esta reformulação corrige).
    # As margens já foram fixadas explicitamente via subplots_adjust acima.
    fig.savefig(caminho_saida, dpi=DPI_IMPRESSAO)
    plt.close(fig)

    return {"caminho": caminho_saida, "edges": edges, "resultados": resultados}


def _gerar_pb(caminho_cor: Path, caminho_pb: Path) -> None:
    caminho_pb.parent.mkdir(parents=True, exist_ok=True)
    Image.open(caminho_cor).convert("L").save(caminho_pb)


def main() -> None:
    saida = gerar_painel()
    caminho = saida["caminho"]
    edges = saida["edges"]
    resultados = saida["resultados"]

    caminho_pb = FIGURAS_DIR / "pb" / caminho.name
    _gerar_pb(caminho, caminho_pb)

    print(f"Painel MAUP salvo em {caminho}")
    print(f"Versão em escala de cinza em {caminho_pb}")
    print(f"\nCortes de classe ({TIPO_CRIME}, município, {ANO_INICIO}-{ANO_FIM}): "
          + ", ".join(f"{v:.4f}" for v in edges))
    print()
    for nivel, _ in NIVEIS:
        r = resultados[nivel]
        print(f"{r['rotulo']}:")
        print(f"    n = {r['n_unidades']}  mínimo = {r['minimo']:.4f}  máximo = {r['maximo']:.4f}  razão = {r['razao']:.4f}")
        print(f"    unidades por classe: {r['n_por_classe']}")


if __name__ == "__main__":
    main()
