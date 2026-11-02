# População feminina vs. população total como denominador: Moran global e LISA, 2018-2025

> **Denominador feminino: população feminina anual ESTIMADA, não medida: população total do ano × razão feminina do município no Censo 2022 (razão suposta constante em 2018-2025).** O IBGE só publica população municipal por sexo nos Censos; as estimativas anuais trazem só o total. A suposição é testada abaixo com o Censo 2010.

Gerado por `src/analysis/denominador_feminino.py`. Parâmetros iguais aos do pipeline (`moran_lisa_assuncao_reis.py`): ajuste de Assunção e Reis, contiguidade de rainha padronizada por linha, 497 municípios, 99.999 permutações, semente 12345, Benjamini-Hochberg (α = 0,05) sobre o p direcional do esda. Desfechos: Ameaça, Estupro, Lesão Corporal, Feminicídio Tentado.

## 1. Razão feminina/total por município (Censo 2022)

| Mínimo | 1º quartil | Mediana | 3º quartil | Máximo |
|---|---|---|---|---|
| 0,464 (CHARQUEADAS) | 0,492 | 0,501 | 0,510 | 0,540 (PORTO ALEGRE) |

## 2. Verificação da suposição: razão feminina 2010 vs. 2022

Variação = razão 2022 − razão 2010, em pontos percentuais (p.p.), para os 496 municípios presentes nos dois Censos. Pinto Bandeira (instalado em 2013) não existe no Censo 2010.

| Mínimo | 1º quartil | Mediana | 3º quartil | Máximo | Mediana de |variação| |
|---|---|---|---|---|---|
| -2,16 | -0,06 | 0,32 | 0,69 | 2,60 | 0,48 |

| Limiar | Municípios | % dos municípios |
|---|---|---|
| > 1 p.p. | 68 | 13,7 |
| > 2 p.p. | 5 | 1,0 |
| > 5 p.p. | 0 | 0,0 |

Municípios com |variação| > 2 p.p. (onde a suposição pode distorcer):

| Município | Pop. total 2022 | Razão 2010 | Razão 2022 | Variação (p.p.) | Significativo no LISA (qualquer versão) |
|---|---|---|---|---|---|
| MATO CASTELHANO | 2.553 | 0,477 | 0,503 | 2,60 | — |
| TOROPI | 2.554 | 0,471 | 0,495 | 2,33 | — |
| GENTIL | 1.744 | 0,470 | 0,493 | 2,27 | — |
| ARROIO DOS RATOS | 14.601 | 0,512 | 0,491 | -2,16 | — |
| PONTE PRETA | 1.575 | 0,472 | 0,493 | 2,13 | — |

## 3. Moran global

| Desfecho | I (total) | I (feminina) | Diferença | z (total) | z (feminina) | p (total) | p (feminina) |
|---|---|---|---|---|---|---|---|
| Ameaça | 0,3055 | 0,3198 | 0,0143 | 11,18 | 11,71 | 0,00001 | 0,00001 |
| Estupro | 0,2228 | 0,2194 | -0,0034 | 8,16 | 8,04 | 0,00001 | 0,00001 |
| Lesão Corporal | 0,2902 | 0,2962 | 0,0060 | 10,60 | 10,82 | 0,00001 | 0,00001 |
| Feminicídio Tentado | 0,0945 | 0,0948 | 0,0003 | 3,53 | 3,55 | 0,00059 | 0,00058 |

## 4. LISA: municípios significativos (FDR)

| Desfecho | Significativos (total) | Significativos (feminina) | Entram | Saem | Permanecem | Mudam de quadrante |
|---|---|---|---|---|---|---|
| Ameaça | 30 | 31 | 1 | 0 | 30 | 0 |
| Estupro | 16 | 15 | 0 | 1 | 15 | 1 |
| Lesão Corporal | 16 | 15 | 0 | 1 | 15 | 0 |
| Feminicídio Tentado | 6 | 6 | 0 | 0 | 6 | 0 |

Entram = significativos só com denominador feminino; saem = só com o total; mudam de quadrante = significativos nas duas versões, em quadrantes diferentes.

| Desfecho | Quadrante | Total | Feminina |
|---|---|---|---|
| Ameaça | AA | 21 | 21 |
| Ameaça | BA | 1 | 1 |
| Ameaça | BB | 7 | 8 |
| Ameaça | AB | 1 | 1 |
| Estupro | AA | 6 | 5 |
| Estupro | BA | 2 | 2 |
| Estupro | BB | 7 | 7 |
| Estupro | AB | 1 | 1 |
| Lesão Corporal | AA | 5 | 5 |
| Lesão Corporal | BA | 0 | 0 |
| Lesão Corporal | BB | 11 | 10 |
| Lesão Corporal | AB | 0 | 0 |
| Feminicídio Tentado | AA | 1 | 1 |
| Feminicídio Tentado | BA | 0 | 0 |
| Feminicídio Tentado | BB | 3 | 3 |
| Feminicídio Tentado | AB | 2 | 2 |

Municípios que entram, saem ou mudam de quadrante:

| Desfecho | Município | Mudança | Pop. total 2022 | Razão 2022 | Variação 2010-2022 (p.p.) | p (total) | p (feminina) |
|---|---|---|---|---|---|---|---|
| Ameaça | CORONEL PILAR | entra | 1.607 | 0,484 | 0,24 | 0,00365 | 0,00272 |
| Estupro | SILVEIRA MARTINS | sai | 2.028 | 0,496 | -0,29 | 0,00157 | 0,00197 |
| Estupro | PORTO ALEGRE (AA→BA) | muda de quadrante | 1.332.845 | 0,540 | 0,37 | 0,00036 | 0,00052 |
| Lesão Corporal | BOQUEIRAO DO LEAO | sai | 6.247 | 0,492 | 0,49 | 0,00152 | 0,00184 |

## 5. Validação

A versão com população total, recalculada neste script, reproduz o CSV publicado (`moran_lisa_assuncao_reis_2018_2025.csv`, configuração `assuncao_reis`):

| tipo_crime | moran_i_atual | moran_i_recalculado | lisa_fdr_atual | lisa_fdr_recalculado | reproduz |
|---|---|---|---|---|---|
| Ameaça | 0,305519 | 0,305519 | 30 | 30 | sim |
| Estupro | 0,222806 | 0,222806 | 16 | 16 | sim |
| Lesão Corporal | 0,290170 | 0,290170 | 16 | 16 | sim |
| Feminicídio Tentado | 0,094476 | 0,094476 | 6 | 6 | sim |

## Arquivos

- `populacao_feminina_censos_rs.csv`: população feminina e total dos Censos 2010 e 2022, razões e variação.
- `moran_lisa_denominador_feminino_2018_2025.csv`: Moran global e contagens do LISA por desfecho e denominador.
- `lisa_denominador_feminino_vs_total_2018_2025.csv`: classificação LISA por município, desfecho e denominador.
