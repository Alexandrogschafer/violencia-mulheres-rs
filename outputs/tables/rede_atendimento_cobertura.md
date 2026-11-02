# Rede de atendimento nos municípios significativos do LISA

Pergunta: os municípios com zero ou poucos eventos e resultado significativo no LISA são desprovidos de serviço? Validação de medida, descritiva, sem teste de hipótese. Gerada por `src/analysis/rede_atendimento_cobertura.py` a partir de `data/processed/rede_atendimento_municipio.csv` (`src/fetch_rede_atendimento.py`). Grupos do LISA de Assunção e Reis, 2018-2025, semente 12345, 99.999 permutações, FDR sobre o p direcional.

Cada célula: municípios com o serviço / municípios que responderam (percentual); "s/r" conta os que não responderam ao quesito, fora do denominador. Os grupos de pares contam municípios, não pares.

## Cobertura por grupo

| Grupo | n | DEAM 2018¹ | DEAM 2019 | DEAM 2023 | Organismo 2018 | Organismo 2023 | CREAS 2018² | CREAS 2023² |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Zero evento, significativos | 3 | 0/3 (0%) | 0/3 (0%) | 0/3 (0%) | 0/3 (0%) | 1/3 (33%) | 0/2 (0%); s/r 1 | 0/3 (0%) |
| Pares com até 5 eventos | 9 | 0/9 (0%) | 0/9 (0%) | 0/9 (0%) | 1/9 (11%) | 2/9 (22%) | 0/8 (0%); s/r 1 | 0/8 (0%); s/r 1 |
| Pares com menos de 10 eventos | 15 | 0/15 (0%) | 0/15 (0%) | 0/15 (0%) | 2/15 (13%) | 3/15 (20%) | 0/14 (0%); s/r 1 | 1/14 (7%); s/r 1 |
| AA | 28 | 1/28 (4%) | 3/28 (11%) | 2/28 (7%) | 6/28 (21%) | 10/28 (36%) | 8/27 (30%); s/r 1 | 8/27 (30%); s/r 1 |
| BB | 24 | 3/24 (12%) | 2/24 (8%) | 2/24 (8%) | 7/24 (29%) | 7/24 (29%) | 4/23 (17%); s/r 1 | 6/24 (25%) |
| Os 497 | 497 | 33/497 (7%) | 31/497 (6%) | 38/496 (8%); s/r 1 | 121/497 (24%) | 164/497 (33%) | 118/487 (24%); s/r 10 | 134/491 (27%); s/r 6 |

¹ DEAM 2018 vem do bloco de política para mulheres (MPPM244, serviços especializados existentes), não do bloco de segurança pública de 2019 e 2023 (MSEG168, delegacias existentes no município). É outra pergunta, e outro informante.

² CREAS da MUNIC, autodeclarado. O Censo SUAS/MDS estava fora do ar quando a tabela foi gerada; ver o relatório.

## Pares com menos de 10 eventos, um a um

| Município | Desfecho | Quadrante | Eventos | População 2025 | DEAM 2018¹ | DEAM 2019 | DEAM 2023 | Organismo 2018 | Organismo 2023 | CREAS 2018² | CREAS 2023² |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MARIANA PIMENTEL | Estupro | BA | 0 | 4.005 | não | não | não | não | não | s/r | não |
| PASSO DO SOBRADO | Feminicídio Tentado | BB | 0 | 6.155 | não | não | não | não | não | não | não |
| VALE VERDE | Feminicídio Tentado | BB | 0 | 3.213 | não | não | não | não | sim | não | não |
| CANUDOS DO VALE | Lesão Corporal | BB | 1 | 1.686 | não | não | não | não | não | não | não |
| SANTO EXPEDITO DO SUL | Estupro | BB | 1 | 2.395 | não | não | não | não | não | não | não |
| ALPESTRE | Feminicídio Tentado | AA | 2 | 7.235 | não | não | não | não | não | não | não |
| DR MAURICIO CARDOSO | Estupro | BB | 2 | 4.534 | não | não | não | sim | sim | não | não |
| SILVEIRA MARTINS | Estupro | BA | 2 | 2.056 | não | não | não | não | não | não | s/r |
| SANTA MARIA DO HERVAL | Feminicídio Tentado | AB | 3 | 6.486 | não | não | não | não | não | não | não |
| CACIQUE DOBLE | Estupro | BB | 6 | 4.692 | não | não | não | não | sim | não | sim |
| ALECRIM | Estupro | BB | 7 | 6.219 | não | não | não | sim | não | não | não |
| LINHA NOVA | Lesão Corporal | BB | 7 | 1.721 | não | não | não | não | não | não | não |
| PRESIDENTE LUCENA | Lesão Corporal | BB | 7 | 3.166 | não | não | não | não | não | não | não |
| SALVADOR DAS MISSOES | Lesão Corporal | BB | 7 | 2.955 | não | não | não | não | não | não | não |
| TUCUNDUVA | Estupro | BB | 8 | 5.646 | não | não | não | não | não | não | não |

## Mudança entre edições, nos 497

| Indicador | Edições | Com resposta nas duas | Sim nas duas | Ganhou | Perdeu | Não nas duas |
| --- | --- | --- | --- | --- | --- | --- |
| deam | 2018 → 2019 | 497 | 25 | 6 | 8 | 458 |
| deam | 2019 → 2023 | 496 | 28 | 10 | 3 | 455 |
| organismo_mulheres | 2018 → 2023 | 497 | 91 | 73 | 30 | 303 |
| creas_munic | 2018 → 2023 | 484 | 114 | 19 | 2 | 349 |

## Municípios sem resposta em algum indicador

Nenhum município do RS recusou a MUNIC inteira nessas edições: a falta de resposta é por quesito.

| Município | Sem resposta em | Em algum grupo |
| --- | --- | --- |
| BOA VISTA DO SUL | creas_munic 2018 (-) | BB |
| BRAGA | creas_munic 2018 (-); creas_munic 2023 (-) | AA |
| GRAVATAI | creas_munic 2023 (Não informou) | não |
| JARI | creas_munic 2018 (-) | não |
| MARIANA PIMENTEL | creas_munic 2018 (-) | poucos eventos |
| MONTE BELO DO SUL | creas_munic 2018 (-); creas_munic 2023 (-) | não |
| NOVA PADUA | creas_munic 2018 (-) | não |
| NOVA ROMA DO SUL | creas_munic 2018 (-) | não |
| PINTO BANDEIRA | creas_munic 2018 (-); creas_munic 2023 (-) | não |
| SANTA TEREZA | creas_munic 2018 (-) | não |
| SILVEIRA MARTINS | creas_munic 2023 (Não informou) | poucos eventos |
| TAQUARI | creas_munic 2023 (Não informou); deam 2023 (Não informou) | não |
| URUGUAIANA | creas_munic 2018 (-) | não |
