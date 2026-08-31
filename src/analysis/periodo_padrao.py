"""Ponto único de decisão para o recorte temporal das análises (Camadas 2 e
3: tendência, sazonalidade, quebra estrutural, correlação, mapas/Moran/
LISA) e do mapa/tabela interativos do portal.

2018 é o primeiro ano em que a fonte (SIP/PROCERGS) publica com
granularidade mensal e layout padronizado por arquivo -- 2012-2017 é um
único arquivo consolidado por ano, sem quebra mensal (ver CLAUDE.md e a
docstring original de src/analysis/tendencia.py, de onde este critério
vem). 2025 é o último ano fechado -- 2026 é ano parcial (dados só até por
volta de junho, sem estimativa de população do IBGE ainda) e não é
comparável aos anos completos em nenhuma das análises acima.

A série histórica de index.html (volume ao longo do tempo, não teste
estatístico) é a única exceção deliberada a este recorte -- usa 2012-2025
(ver ANO_INICIO_SERIE_HISTORICA/ANO_FIM_SERIE_HISTORICA abaixo): ali o
objetivo é mostrar a evolução no maior período disponível, não inferir
sobre um período fechado e homogêneo. 2026 sai por ser parcial (o mesmo
motivo de sempre), mas 2012-2017 entra porque não há teste estatístico
que exija granularidade mensal ali.

Módulos que importam ANO_INICIO_ANALISE/ANO_FIM_ANALISE daqui: tendencia.py,
sazonalidade.py, quebra_estrutural.py (só a série do teste de Chow -- o
Mann-Whitney por mês equivalente já usa seus próprios conjuntos de anos
explícitos, {2018..ANO_ENCHENTE-1} vs {2024,2025}, que não incluem 2026 e
não precisam deste import), correlacao.py e mapa_choropleth.py (via
ANO_INICIO_PADRAO/ANO_FIM_PADRAO, de onde autocorrelacao_espacial.py,
clusters_lisa.py e notebooks/analise_espacial.ipynb -- que não passam
ano_inicio/ano_fim explicitamente -- herdam o recorte).

Não usado pelas figuras do capítulo (src/analysis/figuras_capitulo.py,
tabela_agregacao_regional.py) -- esses já hardcodam 2018-2025 de forma
independente, por decisão editorial do capítulo, fora do escopo desta
rodada de atualização do portal.
"""

ANO_INICIO_ANALISE = 2018
ANO_FIM_ANALISE = 2025

ANO_INICIO_SERIE_HISTORICA = 2012
ANO_FIM_SERIE_HISTORICA = 2025
