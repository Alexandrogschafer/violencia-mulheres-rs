"""Gera as figuras de mapa do capítulo (publicacoes/cap_geotecnologias/) em
qualidade de impressão -- classificação por quantis, piso populacional e
corpos d'água próprios, ao contrário do portal (rampa contínua, sem piso,
sem água, ver src/analysis/mapa_choropleth.py:gerar_mapa). Não toca em
outputs/figures/ nem em docs/: grava direto em
publicacoes/cap_geotecnologias/03_figuras/.

Feminicídio Consumado e Feminicídio Tentado ficam de fora de propósito
(diferente do portal, que mapeia as 5 categorias): são raras demais para
uma classificação por quantis municipal fazer sentido -- pd.qcut já
descartava cortes duplicados nelas (3 e 4 classes reais de 5 pedidas, ver
sessão anterior), e autocorrelacao_espacial.py não detecta autocorrelação
espacial significativa (Índice de Moran) para nenhuma das duas. Decisão
editorial do capítulo, não uma limitação técnica do pipeline.

N_CLASSES=5 é fixo -- comparamos 5 e 6 classes lado a lado (pasta v6_classes/,
descartada) e 5 venceu por discriminação cromática em leitura seriada: com 6
classes, tons adjacentes da rampa ficam próximos demais para distinguir com
segurança numa figura impressa pequena, especialmente em Feminicídio
Consumado/Tentado (já fora do capítulo) e nas categorias raras dentro de
Ameaça/Estupro/Lesão Corporal onde vários municípios caem perto dos cortes.

Período (ANO_INICIO/ANO_FIM) definido explicitamente aqui em vez de herdar
ANO_INICIO_PADRAO/ANO_FIM_PADRAO (2021-2025) de mapa_choropleth.py -- esse
default do módulo nunca teve justificativa registrada (só existe como valor
de constante desde o commit inicial, sem comentário). Para o capítulo, o
recorte segue o mesmo critério já documentado em src/analysis/tendencia.py:
2018 é quando a fonte (SSP/RS) passa a publicar com granularidade mensal e
layout padronizado (2012-2017 é um único arquivo consolidado por ano, sem
quebra mensal); 2026 fica de fora por ser ano parcial, ainda não comparável
aos anos fechados.

PALETA_OFICIAL="roxo" -- decisão editorial após comparar as três variantes
(azul/roxo/verde) lado a lado em publicacoes/cap_geotecnologias/03_figuras/
(paleta_azul/, paleta_roxo/, paleta_verde/, cada uma com sua versão pb/ em
escala de cinza). azul e verde foram descartadas e apagadas; o parâmetro
`paleta` continua disponível em gerar_mapa() (mapa_choropleth.PALETAS) caso
seja preciso comparar de novo no futuro, só não é mais gerado por padrão
aqui.

Sem título embutido (mostrar_titulo=False, ver mapa_choropleth.gerar_mapa):
a norma da editora coloca a legenda da figura no texto do capítulo, acima
da imagem -- um título de duas linhas embutido na própria figura duplicaria
essa informação. Sem o título, o layout padrão do matplotlib deixaria uma
faixa vazia no topo; gerar_mapa reduz a margem superior nesse caso para que
o mapa preencha o quadro.

Com escala gráfica e seta de norte (mostrar_escala=True): só faz sentido
geometricamente porque gerar_mapa desenha em EPSG:5880 (métrico, aspecto
1:1) -- ver _adiciona_escala_e_norte em mapa_choropleth.py. Posicionadas no
canto inferior direito, livre porque a legenda de classes do modo
"quantis" fica no inferior esquerdo.

Gera, só na paleta oficial:
1. Top-level (fig02/03/04_choropleth_*.png -- ver NUMERACAO_FIGURAS): 5
   classes, piso, corpos d'água, escala gráfica e seta de norte, paleta
   roxo, sem título embutido.
2. pb/: as mesmas 3 figuras convertidas para escala de cinza (simulando
   fotocópia monocromática), para checar a distinguibilidade das classes
   sem depender de cor.

Uso: python -m src.analysis.figuras_capitulo
"""

from pathlib import Path

from PIL import Image

from src.analysis.mapa_choropleth import gerar_mapa, slug_tipo_crime

FIGURAS_DIR = (
    Path(__file__).resolve().parent.parent.parent
    / "publicacoes"
    / "cap_geotecnologias"
    / "03_figuras"
)

# Categorias de ocorrência mapeadas no capítulo -- só 3 das 5 do portal
# (TIPOS_CRIME em src/build_site_data.py): ver justificativa da exclusão de
# Feminicídio Consumado/Tentado na docstring do módulo. Repetida aqui em vez
# de importada de lá para não acoplar a geração das figuras do capítulo à
# do portal.
#
# NUMERACAO_FIGURAS mapeia categoria -> número da figura no texto do
# capítulo, e define também a ordem de geração (dict preserva ordem de
# inserção). Figura 1 é reservada ao fluxograma do pipeline (Seção 4),
# produzido fora deste script -- por isso os mapas começam em 2, não em 1.
# A ordem de leitura do texto NÃO é alfabética: Lesão Corporal (fig. 3) vem
# antes de Estupro (fig. 4).
NUMERACAO_FIGURAS = {
    "Ameaça": 2,
    "Lesão Corporal": 3,
    "Estupro": 4,
}

# 2018-2025: mesmo critério documentado em src/analysis/tendencia.py (linhas
# 1-7) -- 2012-2017 fica de fora por não ter quebra mensal/layout padronizado
# na fonte SSP/RS, 2026 por ser ano parcial. Ver docstring do módulo.
ANO_INICIO = 2018
ANO_FIM = 2025

POP_MINIMA = 5000  # mesmo piso de notebooks/analise_exploratoria.ipynb e estudo_uruguaiana.ipynb
N_CLASSES = 5  # fixo -- ver justificativa (5 vs. 6) na docstring do módulo
DPI_IMPRESSAO = 300
FORMATO_IMPRESSAO = "png"

PALETA_OFICIAL = "roxo"  # ver justificativa na docstring do módulo


def _gerar_conjunto(diretorio: Path, paleta: str) -> list[dict]:
    diretorio.mkdir(parents=True, exist_ok=True)
    resultados = []
    for tipo_crime, i in NUMERACAO_FIGURAS.items():
        caminho_saida = (
            diretorio / f"fig{i:02d}_choropleth_{slug_tipo_crime(tipo_crime)}.{FORMATO_IMPRESSAO}"
        )
        caminho, gdf = gerar_mapa(
            tipo_crime=tipo_crime,
            ano_inicio=ANO_INICIO,
            ano_fim=ANO_FIM,
            caminho_saida=caminho_saida,
            classificacao="quantis",
            n_classes=N_CLASSES,
            pop_minima=POP_MINIMA,
            dpi=DPI_IMPRESSAO,
            formato=FORMATO_IMPRESSAO,
            paleta=paleta,
            mostrar_corpos_dagua=True,
            mostrar_titulo=False,
            mostrar_escala=True,
        )
        resultados.append(
            {
                "tipo_crime": tipo_crime,
                "caminho": caminho,
                "n_abaixo_piso": int(gdf["abaixo_piso"].sum()),
                "quantis_edges": gdf.attrs.get("quantis_edges"),
                "n_classes_reais": gdf.attrs.get("quantis_n_classes"),
            }
        )
    return resultados


def _gerar_pb(caminho_cor: Path, caminho_pb: Path) -> None:
    """Converte para escala de cinza via luminosidade (PIL "L") -- a mesma
    aproximação padrão de um scanner/fotocopiadora monocromática, para
    avaliar se as classes continuam distinguíveis sem depender de cor."""
    caminho_pb.parent.mkdir(parents=True, exist_ok=True)
    Image.open(caminho_cor).convert("L").save(caminho_pb)


def main() -> None:
    print(f"=== Conjunto oficial (paleta {PALETA_OFICIAL}, top-level de 03_figuras/) ===\n")
    resultados = _gerar_conjunto(FIGURAS_DIR, PALETA_OFICIAL)
    _imprimir_resultados(FIGURAS_DIR, PALETA_OFICIAL, resultados)

    diretorio_pb = FIGURAS_DIR / "pb"
    for r in resultados:
        caminho_pb = diretorio_pb / r["caminho"].name
        _gerar_pb(r["caminho"], caminho_pb)
    print(f"  -> {len(resultados)} versão(ões) em escala de cinza em {diretorio_pb}\n")

    print("=== Cortes de classe por categoria (4 casas decimais) ===")
    for r in resultados:
        edges = r["quantis_edges"]
        minimo, maximo = edges[0], edges[-1]
        razao = maximo / minimo if minimo else float("inf")
        edges_fmt = ", ".join(f"{v:.4f}" for v in edges)
        print(f"{r['tipo_crime']}:")
        print(f"    cortes: [{edges_fmt}]")
        print(f"    mínimo: {minimo:.4f}  máximo: {maximo:.4f}  razão (máximo/mínimo): {razao:.4f}")


def _imprimir_resultados(diretorio: Path, paleta: str, resultados: list[dict]) -> None:
    print(
        f"{len(resultados)} figura(s) gerada(s) em {diretorio} (paleta={paleta}, "
        f"classificacao=quantis, n_classes={N_CLASSES}, pop_minima={POP_MINIMA}, "
        f"dpi={DPI_IMPRESSAO}, formato={FORMATO_IMPRESSAO}, período {ANO_INICIO}-{ANO_FIM}):"
    )
    for r in resultados:
        edges_fmt = ", ".join(f"{v:.2f}" for v in r["quantis_edges"])
        print(f"- {r['caminho']}")
        print(f"    tipo_crime: {r['tipo_crime']}")
        print(f"    municípios abaixo do piso ({POP_MINIMA} hab.): {r['n_abaixo_piso']}")
        print(f"    classes reais: {r['n_classes_reais']} (pedido: {N_CLASSES})")
        print(f"    cortes de quantis: [{edges_fmt}]")


if __name__ == "__main__":
    main()
