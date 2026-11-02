# Resultados consolidados

> **Denominador: população feminina anual ESTIMADA, não medida: população total do ano × razão feminina do município no Censo 2022 (razão suposta constante em 2018-2025).**
> O IBGE só publica população municipal por sexo nos Censos. A suposição foi testada com o Censo 2010 em
> `denominador_feminino_vs_total.md`.

Fonte única de números do artigo. 497 municípios, 2018-2025, contiguidade de rainha padronizada
por linha, semente 12345, 99.999 permutações. Moran bruto: taxa por 100 mil mulheres-ano. Moran ajustado e
LISA: ajuste de Assunção e Reis. LISA: municípios que sobrevivem ao FDR de Benjamini-Hochberg com q = 0,05, por
desfecho, sobre o p direcional do esda. O menor p possível é 0,00001.

As colunas sem sufixo usam o denominador feminino e são as do artigo. As colunas marcadas **(pop. total)** repetem as
medidas com população total, o denominador do portal, e vão para a tabela suplementar; no Moran bruto, a taxa é por
100 mil pessoas-ano. Eventos, mediana e municípios com zero não dependem do denominador.

`sobreposicao_desfechos.md`, gerada pelo mesmo script, segue com população total.

Gerada por `src/analysis/resultados_consolidados.py`.

| Desfecho | Eventos | Mediana municipal | Municípios com zero | Moran bruto | p bruto | Moran ajustado | p ajustado | LISA AA | LISA BB | LISA AB | LISA BA | LISA total | Moran bruto (pop. total) | p bruto (pop. total) | Moran ajustado (pop. total) | p ajustado (pop. total) | LISA AA (pop. total) | LISA BB (pop. total) | LISA AB (pop. total) | LISA BA (pop. total) | LISA total (pop. total) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ameaça | 269.917 | 116,0 | 0,0% | 0,3134 | 0,00001 | 0,3198 | 0,00001 | 21 | 8 | 1 | 1 | 31 | 0,2995 | 0,00001 | 0,3055 | 0,00001 | 21 | 7 | 1 | 1 | 30 |
| Lesão Corporal | 155.062 | 52,0 | 0,0% | 0,2853 | 0,00001 | 0,2962 | 0,00001 | 5 | 10 | 0 | 0 | 15 | 0,2806 | 0,00001 | 0,2902 | 0,00001 | 5 | 11 | 0 | 0 | 16 |
| Estupro | 18.726 | 8,0 | 4,6% | 0,1713 | 0,00001 | 0,2194 | 0,00001 | 5 | 7 | 1 | 2 | 15 | 0,1762 | 0,00001 | 0,2228 | 0,00001 | 6 | 7 | 1 | 2 | 16 |
| Feminicídio Tentado | 2.286 | 1,0 | 42,3% | 0,0758 | 0,00470 | 0,0948 | 0,00058 | 1 | 3 | 2 | 0 | 6 | 0,0751 | 0,00487 | 0,0945 | 0,00059 | 1 | 3 | 2 | 0 | 6 |
| Feminicídio Consumado | 739 | 0,0 | 53,1% | -0,0085 | 0,42371 | 0,0122 | 0,29488 | não calculado | não calculado | não calculado | não calculado | não calculado | -0,0093 | 0,41073 | 0,0114 | 0,30563 | não calculado | não calculado | não calculado | não calculado | não calculado |
