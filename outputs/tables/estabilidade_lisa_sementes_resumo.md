# Estabilidade do LISA de Assunção e Reis frente à semente

**Denominador:** população feminina anual ESTIMADA, não medida: população total do ano × razão feminina do município no Censo 2022 (razão suposta constante em 2018-2025).

20 sementes, de 12345 a 31345, de 1000 em 1000. Critério `fdr`: Benjamini-Hochberg sobre o p_sim do esda. Critério `fdr_p2x`: sobre o dobro dele, limitado a 1.

## Municípios significativos por semente

| criterio | tipo_crime | permutacoes | minimo | q1 | mediana | q3 | maximo | media | dp | frequencias |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fdr | Ameaça | 999 | 20 | 23.75 | 29.0 | 31.0 | 34 | 27.65 | 4.39 | 20 (2x), 23 (3x), 24 (1x), 25 (1x), 26 (1x), 27 (1x), 28 (1x), 30 (3x), 31 (4x), 32 (1x), 34 (2x) |
| fdr | Ameaça | 99999 | 30 | 31.0 | 31.0 | 31.0 | 32 | 31.1 | 0.45 | 30 (1x), 31 (16x), 32 (3x) |
| fdr | Estupro | 999 | 0 | 0.0 | 11.5 | 13.75 | 22 | 9.8 | 8.28 | 0 (7x), 10 (2x), 11 (1x), 12 (2x), 13 (3x), 16 (1x), 20 (1x), 22 (3x) |
| fdr | Estupro | 99999 | 15 | 15.0 | 15.0 | 15.0 | 15 | 15.0 | 0.0 | 15 (20x) |
| fdr | Feminicídio Tentado | 999 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0.0 | 0.0 | 0 (20x) |
| fdr | Feminicídio Tentado | 99999 | 5 | 6.0 | 6.0 | 6.0 | 6 | 5.95 | 0.22 | 5 (1x), 6 (19x) |
| fdr | Lesão Corporal | 999 | 0 | 10.0 | 12.0 | 13.25 | 22 | 11.95 | 5.35 | 0 (2x), 10 (4x), 11 (1x), 12 (6x), 13 (2x), 14 (2x), 20 (2x), 22 (1x) |
| fdr | Lesão Corporal | 99999 | 15 | 15.0 | 15.0 | 15.0 | 21 | 15.8 | 1.96 | 15 (17x), 20 (2x), 21 (1x) |
| fdr_p2x | Ameaça | 999 | 0 | 0.0 | 0.0 | 21.0 | 26 | 6.75 | 10.62 | 0 (14x), 21 (2x), 22 (2x), 23 (1x), 26 (1x) |
| fdr_p2x | Ameaça | 99999 | 20 | 21.0 | 21.0 | 22.0 | 23 | 21.25 | 0.72 | 20 (2x), 21 (12x), 22 (5x), 23 (1x) |
| fdr_p2x | Estupro | 999 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0.0 | 0.0 | 0 (20x) |
| fdr_p2x | Estupro | 99999 | 6 | 8.0 | 8.0 | 8.0 | 9 | 7.85 | 0.81 | 6 (2x), 7 (2x), 8 (13x), 9 (3x) |
| fdr_p2x | Feminicídio Tentado | 999 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0.0 | 0.0 | 0 (20x) |
| fdr_p2x | Feminicídio Tentado | 99999 | 0 | 0.75 | 3.0 | 3.0 | 3 | 2.0 | 1.34 | 0 (5x), 1 (2x), 2 (1x), 3 (12x) |
| fdr_p2x | Lesão Corporal | 999 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0.0 | 0.0 | 0 (20x) |
| fdr_p2x | Lesão Corporal | 99999 | 6 | 6.0 | 7.0 | 9.0 | 12 | 7.55 | 1.79 | 6 (9x), 7 (2x), 8 (3x), 9 (3x), 10 (2x), 12 (1x) |

## Municípios que trocam de status ou categoria

| criterio | tipo_crime | permutacoes | sempre_significativos | ao_menos_uma_semente | trocam_status | trocam_categoria |
| --- | --- | --- | --- | --- | --- | --- |
| fdr | Ameaça | 999 | 14 | 40 | 26 | 26 |
| fdr | Ameaça | 99999 | 30 | 32 | 2 | 2 |
| fdr | Estupro | 999 | 0 | 31 | 31 | 31 |
| fdr | Estupro | 99999 | 15 | 15 | 0 | 0 |
| fdr | Feminicídio Tentado | 999 | 0 | 0 | 0 | 0 |
| fdr | Feminicídio Tentado | 99999 | 5 | 6 | 1 | 1 |
| fdr | Lesão Corporal | 999 | 0 | 27 | 27 | 27 |
| fdr | Lesão Corporal | 99999 | 15 | 21 | 6 | 6 |
| fdr | municípios distintos, quatro tipos | 999 | 14 | 80 | 71 | 71 |
| fdr | municípios distintos, quatro tipos | 99999 | 56 | 60 | 9 | 9 |
| fdr_p2x | Ameaça | 999 | 0 | 31 | 31 | 31 |
| fdr_p2x | Ameaça | 99999 | 20 | 23 | 3 | 3 |
| fdr_p2x | Estupro | 999 | 0 | 0 | 0 | 0 |
| fdr_p2x | Estupro | 99999 | 6 | 10 | 4 | 4 |
| fdr_p2x | Feminicídio Tentado | 999 | 0 | 0 | 0 | 0 |
| fdr_p2x | Feminicídio Tentado | 99999 | 0 | 3 | 3 | 3 |
| fdr_p2x | Lesão Corporal | 999 | 0 | 0 | 0 | 0 |
| fdr_p2x | Lesão Corporal | 99999 | 6 | 12 | 6 | 6 |
| fdr_p2x | municípios distintos, quatro tipos | 999 | 0 | 31 | 31 | 31 |
| fdr_p2x | municípios distintos, quatro tipos | 99999 | 27 | 42 | 16 | 16 |

## Municípios instáveis

| criterio | tipo_crime | permutacoes | municipio | sementes_significativo | n_sementes | categorias | p_minimo | p_maximo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fdr | Ameaça | 999 | ALPESTRE | 12 | 20 | AA | não significativo | 0.001 | 0.005 |
| fdr | Ameaça | 999 | BARAO | 3 | 20 | BB | não significativo | 0.001 | 0.01 |
| fdr | Ameaça | 999 | BENTO GONCALVES | 6 | 20 | AB | não significativo | 0.001 | 0.008 |
| fdr | Ameaça | 999 | BOA VISTA DAS MISSOES | 7 | 20 | AA | não significativo | 0.002 | 0.006 |
| fdr | Ameaça | 999 | BOA VISTA DO SUL | 16 | 20 | BB | não significativo | 0.001 | 0.004 |
| fdr | Ameaça | 999 | CAMPO NOVO | 1 | 20 | AA | não significativo | 0.003 | 0.011 |
| fdr | Ameaça | 999 | CARLOS BARBOSA | 5 | 20 | BB | não significativo | 0.001 | 0.01 |
| fdr | Ameaça | 999 | CORONEL PILAR | 5 | 20 | BB | não significativo | 0.001 | 0.008 |
| fdr | Ameaça | 999 | COTIPORA | 14 | 20 | BB | não significativo | 0.001 | 0.005 |
| fdr | Ameaça | 999 | DERRUBADAS | 19 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr | Ameaça | 999 | DOIS IRMAOS DAS MISSOES | 19 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr | Ameaça | 999 | ERVAL SECO | 19 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr | Ameaça | 999 | FELIZ | 5 | 20 | BB | não significativo | 0.002 | 0.013 |
| fdr | Ameaça | 999 | GARIBALDI | 16 | 20 | BB | não significativo | 0.001 | 0.005 |
| fdr | Ameaça | 999 | JABOTICABA | 4 | 20 | AA | não significativo | 0.002 | 0.009 |
| fdr | Ameaça | 999 | LINHA NOVA | 18 | 20 | BB | não significativo | 0.001 | 0.004 |
| fdr | Ameaça | 999 | MIRAGUAI | 12 | 20 | AA | não significativo | 0.001 | 0.006 |
| fdr | Ameaça | 999 | NOVA PETROPOLIS | 14 | 20 | BB | não significativo | 0.001 | 0.005 |
| fdr | Ameaça | 999 | NOVA PRATA | 1 | 20 | BB | não significativo | 0.002 | 0.017 |
| fdr | Ameaça | 999 | NOVA RAMADA | 9 | 20 | BA | não significativo | 0.001 | 0.007 |
| fdr | Ameaça | 999 | PRESIDENTE LUCENA | 19 | 20 | BB | não significativo | 0.001 | 0.003 |
| fdr | Ameaça | 999 | RODEIO BONITO | 19 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr | Ameaça | 999 | SAO PEDRO DO BUTIA | 2 | 20 | BB | não significativo | 0.003 | 0.013 |
| fdr | Ameaça | 999 | SEBERI | 2 | 20 | AA | não significativo | 0.003 | 0.011 |
| fdr | Ameaça | 999 | TAQUARUCU DO SUL | 10 | 20 | AA | não significativo | 0.001 | 0.005 |
| fdr | Ameaça | 999 | VISTA GAUCHA | 16 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr | Estupro | 999 | ALECRIM | 9 | 20 | BB | não significativo | 0.001 | 0.005 |
| fdr | Estupro | 999 | BALNEARIO PINHAL | 13 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr | Estupro | 999 | BARRACAO | 1 | 20 | AB | não significativo | 0.002 | 0.008 |
| fdr | Estupro | 999 | BENTO GONCALVES | 9 | 20 | AB | não significativo | 0.001 | 0.003 |
| fdr | Estupro | 999 | BOA VISTA DO SUL | 4 | 20 | BB | não significativo | 0.001 | 0.007 |
| fdr | Estupro | 999 | CACIQUE DOBLE | 8 | 20 | BB | não significativo | 0.001 | 0.003 |
| fdr | Estupro | 999 | CAPIVARI DO SUL | 13 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr | Estupro | 999 | CERRO GRANDE DO SUL | 1 | 20 | AA | não significativo | 0.001 | 0.008 |
| fdr | Estupro | 999 | COTIPORA | 2 | 20 | BB | não significativo | 0.002 | 0.008 |
| fdr | Estupro | 999 | CRISSIUMAL | 3 | 20 | BB | não significativo | 0.001 | 0.008 |
| fdr | Estupro | 999 | DOIS LAJEADOS | 2 | 20 | BB | não significativo | 0.001 | 0.009 |
| fdr | Estupro | 999 | DR MAURICIO CARDOSO | 12 | 20 | BB | não significativo | 0.001 | 0.003 |
| fdr | Estupro | 999 | FAGUNDES VARELA | 5 | 20 | BB | não significativo | 0.001 | 0.007 |
| fdr | Estupro | 999 | FARROUPILHA | 9 | 20 | BB | não significativo | 0.001 | 0.004 |
| fdr | Estupro | 999 | FLORES DA CUNHA | 2 | 20 | BB | não significativo | 0.001 | 0.01 |
| fdr | Estupro | 999 | GUAPORE | 1 | 20 | BB | não significativo | 0.002 | 0.008 |
| fdr | Estupro | 999 | HORIZONTINA | 1 | 20 | BB | não significativo | 0.002 | 0.011 |
| fdr | Estupro | 999 | MARIANA PIMENTEL | 12 | 20 | BA | não significativo | 0.001 | 0.002 |
| fdr | Estupro | 999 | NOVA PALMA | 4 | 20 | AA | não significativo | 0.001 | 0.008 |
| fdr | Estupro | 999 | NOVO BARREIRO | 3 | 20 | BB | não significativo | 0.001 | 0.008 |
| fdr | Estupro | 999 | OSORIO | 13 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr | Estupro | 999 | PORTO ALEGRE | 12 | 20 | BA | não significativo | 0.001 | 0.002 |
| fdr | Estupro | 999 | PORTO MAUA | 2 | 20 | BB | não significativo | 0.001 | 0.01 |
| fdr | Estupro | 999 | SANTA ROSA | 9 | 20 | BB | não significativo | 0.001 | 0.004 |
| fdr | Estupro | 999 | SANTO EXPEDITO DO SUL | 8 | 20 | BB | não significativo | 0.001 | 0.005 |
| fdr | Estupro | 999 | SAO VALENTIM DO SUL | 1 | 20 | BB | não significativo | 0.002 | 0.008 |
| fdr | Estupro | 999 | SENTINELA DO SUL | 9 | 20 | AA | não significativo | 0.001 | 0.005 |
| fdr | Estupro | 999 | SILVEIRA MARTINS | 3 | 20 | BA | não significativo | 0.001 | 0.005 |
| fdr | Estupro | 999 | TOROPI | 1 | 20 | AB | não significativo | 0.002 | 0.01 |
| fdr | Estupro | 999 | TRAMANDAI | 11 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr | Estupro | 999 | TUCUNDUVA | 13 | 20 | BB | não significativo | 0.001 | 0.002 |
| fdr | Lesão Corporal | 999 | BALNEARIO PINHAL | 4 | 20 | AA | não significativo | 0.001 | 0.005 |
| fdr | Lesão Corporal | 999 | BARAO | 2 | 20 | BB | não significativo | 0.001 | 0.007 |
| fdr | Lesão Corporal | 999 | BOA VISTA DO SUL | 14 | 20 | BB | não significativo | 0.001 | 0.003 |
| fdr | Lesão Corporal | 999 | BOQUEIRAO DO LEAO | 6 | 20 | BB | não significativo | 0.001 | 0.008 |
| fdr | Lesão Corporal | 999 | BRAGA | 17 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr | Lesão Corporal | 999 | CAMPINA DAS MISSOES | 11 | 20 | BB | não significativo | 0.001 | 0.004 |
| fdr | Lesão Corporal | 999 | CANUDOS DO VALE | 16 | 20 | BB | não significativo | 0.001 | 0.002 |
| fdr | Lesão Corporal | 999 | CAPIVARI DO SUL | 17 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr | Lesão Corporal | 999 | CIDREIRA | 14 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr | Lesão Corporal | 999 | CORONEL BICACO | 1 | 20 | AA | não significativo | 0.002 | 0.009 |
| fdr | Lesão Corporal | 999 | FORQUETINHA | 4 | 20 | BB | não significativo | 0.001 | 0.005 |
| fdr | Lesão Corporal | 999 | LINHA NOVA | 16 | 20 | BB | não significativo | 0.001 | 0.002 |
| fdr | Lesão Corporal | 999 | MARQUES DE SOUZA | 2 | 20 | BB | não significativo | 0.001 | 0.007 |
| fdr | Lesão Corporal | 999 | MIRAGUAI | 3 | 20 | AA | não significativo | 0.001 | 0.005 |
| fdr | Lesão Corporal | 999 | NOVA BRESCIA | 1 | 20 | BB | não significativo | 0.002 | 0.012 |
| fdr | Lesão Corporal | 999 | OSORIO | 18 | 20 | AA | não significativo | 0.001 | 0.001 |
| fdr | Lesão Corporal | 999 | PICADA CAFE | 17 | 20 | BB | não significativo | 0.001 | 0.002 |
| fdr | Lesão Corporal | 999 | POCO DAS ANTAS | 1 | 20 | BB | não significativo | 0.001 | 0.009 |
| fdr | Lesão Corporal | 999 | PRESIDENTE LUCENA | 7 | 20 | BB | não significativo | 0.001 | 0.004 |
| fdr | Lesão Corporal | 999 | REDENTORA | 4 | 20 | AA | não significativo | 0.001 | 0.005 |
| fdr | Lesão Corporal | 999 | SALVADOR DAS MISSOES | 8 | 20 | BB | não significativo | 0.001 | 0.005 |
| fdr | Lesão Corporal | 999 | SALVADOR DO SUL | 9 | 20 | BB | não significativo | 0.001 | 0.004 |
| fdr | Lesão Corporal | 999 | SAO PEDRO DO BUTIA | 11 | 20 | BB | não significativo | 0.001 | 0.004 |
| fdr | Lesão Corporal | 999 | SARANDI | 3 | 20 | AB | não significativo | 0.001 | 0.006 |
| fdr | Lesão Corporal | 999 | SERIO | 1 | 20 | BB | não significativo | 0.002 | 0.01 |
| fdr | Lesão Corporal | 999 | TRAMANDAI | 18 | 20 | AA | não significativo | 0.001 | 0.001 |
| fdr | Lesão Corporal | 999 | TUPANDI | 14 | 20 | BB | não significativo | 0.001 | 0.003 |
| fdr | Ameaça | 99999 | BENTO GONCALVES | 3 | 20 | AB | não significativo | 0.00298 | 0.00368 |
| fdr | Ameaça | 99999 | CORONEL PILAR | 19 | 20 | BB | não significativo | 0.00238 | 0.00314 |
| fdr | Feminicídio Tentado | 99999 | VALE VERDE | 19 | 20 | BB | não significativo | 0.00044 | 0.0007 |
| fdr | Lesão Corporal | 99999 | BALNEARIO PINHAL | 3 | 20 | AA | não significativo | 0.0018 | 0.00224 |
| fdr | Lesão Corporal | 99999 | BOQUEIRAO DO LEAO | 3 | 20 | BB | não significativo | 0.00167 | 0.00206 |
| fdr | Lesão Corporal | 99999 | FORQUETINHA | 3 | 20 | BB | não significativo | 0.00173 | 0.00239 |
| fdr | Lesão Corporal | 99999 | MIRAGUAI | 1 | 20 | AA | não significativo | 0.00208 | 0.00271 |
| fdr | Lesão Corporal | 99999 | REDENTORA | 3 | 20 | AA | não significativo | 0.00184 | 0.0023 |
| fdr | Lesão Corporal | 99999 | SARANDI | 3 | 20 | AB | não significativo | 0.00175 | 0.00226 |
| fdr_p2x | Ameaça | 999 | ALPESTRE | 1 | 20 | AA | não significativo | 0.001 | 0.005 |
| fdr_p2x | Ameaça | 999 | AMETISTA DO SUL | 6 | 20 | AA | não significativo | 0.001 | 0.001 |
| fdr_p2x | Ameaça | 999 | BENTO GONCALVES | 1 | 20 | AB | não significativo | 0.001 | 0.008 |
| fdr_p2x | Ameaça | 999 | BOA VISTA DO SUL | 2 | 20 | BB | não significativo | 0.001 | 0.004 |
| fdr_p2x | Ameaça | 999 | BOM PROGRESSO | 6 | 20 | AA | não significativo | 0.001 | 0.001 |
| fdr_p2x | Ameaça | 999 | BRAGA | 5 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr_p2x | Ameaça | 999 | CORONEL BICACO | 6 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr_p2x | Ameaça | 999 | CORONEL PILAR | 1 | 20 | BB | não significativo | 0.001 | 0.008 |
| fdr_p2x | Ameaça | 999 | COTIPORA | 4 | 20 | BB | não significativo | 0.001 | 0.005 |
| fdr_p2x | Ameaça | 999 | CRISTAL DO SUL | 4 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr_p2x | Ameaça | 999 | DERRUBADAS | 4 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr_p2x | Ameaça | 999 | DOIS IRMAOS DAS MISSOES | 4 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr_p2x | Ameaça | 999 | ERVAL SECO | 5 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr_p2x | Ameaça | 999 | FREDERICO WESTPHALEN | 6 | 20 | AA | não significativo | 0.001 | 0.001 |
| fdr_p2x | Ameaça | 999 | GARIBALDI | 5 | 20 | BB | não significativo | 0.001 | 0.005 |
| fdr_p2x | Ameaça | 999 | IRAI | 6 | 20 | AA | não significativo | 0.001 | 0.001 |
| fdr_p2x | Ameaça | 999 | LINHA NOVA | 5 | 20 | BB | não significativo | 0.001 | 0.004 |
| fdr_p2x | Ameaça | 999 | MIRAGUAI | 1 | 20 | AA | não significativo | 0.001 | 0.006 |
| fdr_p2x | Ameaça | 999 | NOVA PETROPOLIS | 3 | 20 | BB | não significativo | 0.001 | 0.005 |
| fdr_p2x | Ameaça | 999 | NOVA RAMADA | 2 | 20 | BA | não significativo | 0.001 | 0.007 |
| fdr_p2x | Ameaça | 999 | PICADA CAFE | 6 | 20 | BB | não significativo | 0.001 | 0.002 |
| fdr_p2x | Ameaça | 999 | PLANALTO | 6 | 20 | AA | não significativo | 0.001 | 0.001 |
| fdr_p2x | Ameaça | 999 | PRESIDENTE LUCENA | 6 | 20 | BB | não significativo | 0.001 | 0.003 |
| fdr_p2x | Ameaça | 999 | REDENTORA | 6 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr_p2x | Ameaça | 999 | RODEIO BONITO | 6 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr_p2x | Ameaça | 999 | SARANDI | 6 | 20 | AB | não significativo | 0.001 | 0.003 |
| fdr_p2x | Ameaça | 999 | TAQUARUCU DO SUL | 4 | 20 | AA | não significativo | 0.001 | 0.005 |
| fdr_p2x | Ameaça | 999 | TENENTE PORTELA | 6 | 20 | AA | não significativo | 0.001 | 0.001 |
| fdr_p2x | Ameaça | 999 | TRES PASSOS | 6 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr_p2x | Ameaça | 999 | VICENTE DUTRA | 4 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr_p2x | Ameaça | 999 | VISTA GAUCHA | 2 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr_p2x | Ameaça | 99999 | COTIPORA | 4 | 20 | BB | não significativo | 0.00104 | 0.00151 |
| fdr_p2x | Ameaça | 99999 | ERVAL SECO | 18 | 20 | AA | não significativo | 0.0007 | 0.00106 |
| fdr_p2x | Ameaça | 99999 | NOVA PETROPOLIS | 3 | 20 | BB | não significativo | 0.00105 | 0.00147 |
| fdr_p2x | Estupro | 99999 | BENTO GONCALVES | 15 | 20 | AB | não significativo | 0.00024 | 0.00047 |
| fdr_p2x | Estupro | 99999 | DR MAURICIO CARDOSO | 18 | 20 | BB | não significativo | 0.00024 | 0.00043 |
| fdr_p2x | Estupro | 99999 | PORTO ALEGRE | 3 | 20 | BA | não significativo | 0.00037 | 0.00066 |
| fdr_p2x | Estupro | 99999 | SENTINELA DO SUL | 1 | 20 | AA | não significativo | 0.00045 | 0.00079 |
| fdr_p2x | Feminicídio Tentado | 99999 | CANDELARIA | 15 | 20 | AB | não significativo | 2e-05 | 0.00011 |
| fdr_p2x | Feminicídio Tentado | 99999 | SANTA CRUZ DO SUL | 12 | 20 | BB | não significativo | 7e-05 | 0.00021 |
| fdr_p2x | Feminicídio Tentado | 99999 | SANTA MARIA DO HERVAL | 13 | 20 | AB | não significativo | 8e-05 | 0.00018 |
| fdr_p2x | Lesão Corporal | 99999 | BOA VISTA DO SUL | 10 | 20 | BB | não significativo | 0.00034 | 0.00056 |
| fdr_p2x | Lesão Corporal | 99999 | BRAGA | 1 | 20 | AA | não significativo | 0.00057 | 0.00085 |
| fdr_p2x | Lesão Corporal | 99999 | CIDREIRA | 10 | 20 | AA | não significativo | 0.00021 | 0.00052 |
| fdr_p2x | Lesão Corporal | 99999 | SALVADOR DO SUL | 3 | 20 | BB | não significativo | 0.00047 | 0.00075 |
| fdr_p2x | Lesão Corporal | 99999 | SAO PEDRO DO BUTIA | 6 | 20 | BB | não significativo | 0.00033 | 0.00067 |
| fdr_p2x | Lesão Corporal | 99999 | TUPANDI | 1 | 20 | BB | não significativo | 0.00056 | 0.00095 |

## Execução

| permutacoes | execucoes_lisa | tempo_total_s | tempo_medio_por_lisa_s | pico_memoria_acumulado_mb |
| --- | --- | --- | --- | --- |
| 999 | 80 | 2.1 | 0.025 | 286.0 |
| 99999 | 80 | 237.3 | 2.964 | 1048.0 |
