# Estabilidade do LISA de Assunção e Reis frente à semente

20 sementes, de 12345 a 31345, de 1000 em 1000. Critério `fdr`: Benjamini-Hochberg sobre o p_sim do esda. Critério `fdr_p2x`: sobre o dobro dele, limitado a 1.

## Municípios significativos por semente

| criterio | tipo_crime | permutacoes | minimo | q1 | mediana | q3 | maximo | media | dp | frequencias |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fdr | Ameaça | 999 | 11 | 22.0 | 25.5 | 31.0 | 34 | 26.0 | 5.56 | 11 (1x), 20 (1x), 21 (1x), 22 (3x), 24 (2x), 25 (2x), 26 (1x), 27 (1x), 30 (2x), 31 (3x), 32 (2x), 34 (1x) |
| fdr | Ameaça | 99999 | 28 | 29.0 | 30.0 | 30.0 | 30 | 29.5 | 0.83 | 28 (4x), 29 (2x), 30 (14x) |
| fdr | Estupro | 999 | 0 | 0.0 | 10.5 | 13.0 | 22 | 8.9 | 7.5 | 0 (7x), 10 (3x), 11 (3x), 12 (1x), 13 (2x), 15 (1x), 20 (2x), 22 (1x) |
| fdr | Estupro | 99999 | 15 | 16.0 | 16.0 | 16.0 | 17 | 16.0 | 0.32 | 15 (1x), 16 (18x), 17 (1x) |
| fdr | Feminicídio Tentado | 999 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0.0 | 0.0 | 0 (20x) |
| fdr | Feminicídio Tentado | 99999 | 4 | 5.75 | 6.0 | 6.0 | 6 | 5.7 | 0.57 | 4 (1x), 5 (4x), 6 (15x) |
| fdr | Lesão Corporal | 999 | 0 | 10.0 | 11.0 | 13.0 | 20 | 10.65 | 5.4 | 0 (3x), 10 (4x), 11 (5x), 12 (2x), 13 (2x), 14 (2x), 20 (2x) |
| fdr | Lesão Corporal | 99999 | 15 | 16.0 | 16.0 | 16.0 | 16 | 15.9 | 0.31 | 15 (2x), 16 (18x) |
| fdr_p2x | Ameaça | 999 | 0 | 0.0 | 0.0 | 5.0 | 24 | 5.3 | 9.45 | 0 (15x), 20 (2x), 21 (2x), 24 (1x) |
| fdr_p2x | Ameaça | 99999 | 16 | 19.75 | 21.0 | 21.0 | 21 | 20.0 | 1.56 | 16 (2x), 19 (3x), 20 (4x), 21 (11x) |
| fdr_p2x | Estupro | 999 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0.0 | 0.0 | 0 (20x) |
| fdr_p2x | Estupro | 99999 | 5 | 5.0 | 7.0 | 8.0 | 10 | 6.8 | 1.67 | 5 (7x), 6 (2x), 7 (4x), 8 (3x), 9 (3x), 10 (1x) |
| fdr_p2x | Feminicídio Tentado | 999 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0.0 | 0.0 | 0 (20x) |
| fdr_p2x | Feminicídio Tentado | 99999 | 0 | 0.0 | 3.0 | 3.0 | 3 | 1.85 | 1.39 | 0 (6x), 1 (2x), 2 (1x), 3 (11x) |
| fdr_p2x | Lesão Corporal | 999 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0.0 | 0.0 | 0 (20x) |
| fdr_p2x | Lesão Corporal | 99999 | 5 | 6.0 | 6.5 | 7.0 | 7 | 6.45 | 0.6 | 5 (1x), 6 (9x), 7 (10x) |

## Municípios que trocam de status ou categoria

| criterio | tipo_crime | permutacoes | sempre_significativos | ao_menos_uma_semente | trocam_status | trocam_categoria |
| --- | --- | --- | --- | --- | --- | --- |
| fdr | Ameaça | 999 | 11 | 39 | 28 | 28 |
| fdr | Ameaça | 99999 | 28 | 30 | 2 | 2 |
| fdr | Estupro | 999 | 0 | 28 | 28 | 28 |
| fdr | Estupro | 99999 | 15 | 17 | 2 | 2 |
| fdr | Feminicídio Tentado | 999 | 0 | 0 | 0 | 0 |
| fdr | Feminicídio Tentado | 99999 | 4 | 6 | 2 | 2 |
| fdr | Lesão Corporal | 999 | 0 | 27 | 27 | 27 |
| fdr | Lesão Corporal | 99999 | 15 | 16 | 1 | 1 |
| fdr | municípios distintos, quatro tipos | 999 | 11 | 76 | 67 | 67 |
| fdr | municípios distintos, quatro tipos | 99999 | 54 | 59 | 7 | 7 |
| fdr_p2x | Ameaça | 999 | 0 | 29 | 29 | 29 |
| fdr_p2x | Ameaça | 99999 | 16 | 21 | 5 | 5 |
| fdr_p2x | Estupro | 999 | 0 | 0 | 0 | 0 |
| fdr_p2x | Estupro | 99999 | 5 | 10 | 5 | 5 |
| fdr_p2x | Feminicídio Tentado | 999 | 0 | 0 | 0 | 0 |
| fdr_p2x | Feminicídio Tentado | 99999 | 0 | 3 | 3 | 3 |
| fdr_p2x | Lesão Corporal | 999 | 0 | 0 | 0 | 0 |
| fdr_p2x | Lesão Corporal | 99999 | 5 | 7 | 2 | 2 |
| fdr_p2x | municípios distintos, quatro tipos | 999 | 0 | 29 | 29 | 29 |
| fdr_p2x | municípios distintos, quatro tipos | 99999 | 22 | 36 | 15 | 15 |

## Municípios instáveis

| criterio | tipo_crime | permutacoes | municipio | sementes_significativo | n_sementes | categorias | p_minimo | p_maximo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fdr | Ameaça | 999 | ALPESTRE | 10 | 20 | AA | não significativo | 0.002 | 0.006 |
| fdr | Ameaça | 999 | BARAO | 3 | 20 | BB | não significativo | 0.001 | 0.01 |
| fdr | Ameaça | 999 | BENTO GONCALVES | 5 | 20 | AB | não significativo | 0.002 | 0.01 |
| fdr | Ameaça | 999 | BOA VISTA DAS MISSOES | 5 | 20 | AA | não significativo | 0.002 | 0.007 |
| fdr | Ameaça | 999 | BOA VISTA DO SUL | 15 | 20 | BB | não significativo | 0.001 | 0.006 |
| fdr | Ameaça | 999 | BRAGA | 19 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr | Ameaça | 999 | CARLOS BARBOSA | 4 | 20 | BB | não significativo | 0.001 | 0.011 |
| fdr | Ameaça | 999 | CORONEL PILAR | 2 | 20 | BB | não significativo | 0.002 | 0.01 |
| fdr | Ameaça | 999 | COTIPORA | 10 | 20 | BB | não significativo | 0.001 | 0.006 |
| fdr | Ameaça | 999 | CRISTAL DO SUL | 19 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr | Ameaça | 999 | DERRUBADAS | 18 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr | Ameaça | 999 | DOIS IRMAOS DAS MISSOES | 18 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr | Ameaça | 999 | FELIZ | 2 | 20 | BB | não significativo | 0.002 | 0.013 |
| fdr | Ameaça | 999 | GARIBALDI | 16 | 20 | BB | não significativo | 0.001 | 0.006 |
| fdr | Ameaça | 999 | JABOTICABA | 1 | 20 | AA | não significativo | 0.002 | 0.012 |
| fdr | Ameaça | 999 | LINHA NOVA | 18 | 20 | BB | não significativo | 0.001 | 0.004 |
| fdr | Ameaça | 999 | MIRAGUAI | 13 | 20 | AA | não significativo | 0.001 | 0.006 |
| fdr | Ameaça | 999 | NOVA PETROPOLIS | 10 | 20 | BB | não significativo | 0.001 | 0.006 |
| fdr | Ameaça | 999 | NOVA PRATA | 5 | 20 | BB | não significativo | 0.001 | 0.012 |
| fdr | Ameaça | 999 | NOVA RAMADA | 11 | 20 | BA | não significativo | 0.001 | 0.005 |
| fdr | Ameaça | 999 | PRESIDENTE LUCENA | 18 | 20 | BB | não significativo | 0.001 | 0.003 |
| fdr | Ameaça | 999 | REDENTORA | 19 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr | Ameaça | 999 | RODEIO BONITO | 17 | 20 | AA | não significativo | 0.001 | 0.004 |
| fdr | Ameaça | 999 | SAO PEDRO DO BUTIA | 1 | 20 | BB | não significativo | 0.003 | 0.012 |
| fdr | Ameaça | 999 | SARANDI | 17 | 20 | AB | não significativo | 0.001 | 0.004 |
| fdr | Ameaça | 999 | SEBERI | 1 | 20 | AA | não significativo | 0.003 | 0.013 |
| fdr | Ameaça | 999 | TAQUARUCU DO SUL | 10 | 20 | AA | não significativo | 0.001 | 0.005 |
| fdr | Ameaça | 999 | VISTA GAUCHA | 13 | 20 | AA | não significativo | 0.001 | 0.004 |
| fdr | Estupro | 999 | ALECRIM | 8 | 20 | BB | não significativo | 0.001 | 0.005 |
| fdr | Estupro | 999 | BALNEARIO PINHAL | 12 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr | Estupro | 999 | BARRACAO | 1 | 20 | AB | não significativo | 0.001 | 0.008 |
| fdr | Estupro | 999 | BENTO GONCALVES | 8 | 20 | AB | não significativo | 0.001 | 0.003 |
| fdr | Estupro | 999 | BOA VISTA DO SUL | 3 | 20 | BB | não significativo | 0.001 | 0.007 |
| fdr | Estupro | 999 | CACIQUE DOBLE | 9 | 20 | BB | não significativo | 0.001 | 0.003 |
| fdr | Estupro | 999 | CAPIVARI DO SUL | 13 | 20 | AA | não significativo | 0.001 | 0.001 |
| fdr | Estupro | 999 | COTIPORA | 2 | 20 | BB | não significativo | 0.002 | 0.008 |
| fdr | Estupro | 999 | CRISSIUMAL | 3 | 20 | BB | não significativo | 0.001 | 0.008 |
| fdr | Estupro | 999 | DOIS LAJEADOS | 2 | 20 | BB | não significativo | 0.002 | 0.009 |
| fdr | Estupro | 999 | DR MAURICIO CARDOSO | 9 | 20 | BB | não significativo | 0.001 | 0.004 |
| fdr | Estupro | 999 | FAGUNDES VARELA | 3 | 20 | BB | não significativo | 0.001 | 0.007 |
| fdr | Estupro | 999 | FARROUPILHA | 8 | 20 | BB | não significativo | 0.001 | 0.005 |
| fdr | Estupro | 999 | FLORES DA CUNHA | 2 | 20 | BB | não significativo | 0.001 | 0.01 |
| fdr | Estupro | 999 | GUAPORE | 2 | 20 | BB | não significativo | 0.001 | 0.007 |
| fdr | Estupro | 999 | HORIZONTINA | 1 | 20 | BB | não significativo | 0.002 | 0.012 |
| fdr | Estupro | 999 | MARIANA PIMENTEL | 11 | 20 | BA | não significativo | 0.001 | 0.002 |
| fdr | Estupro | 999 | NOVA PALMA | 2 | 20 | AA | não significativo | 0.001 | 0.008 |
| fdr | Estupro | 999 | NOVO BARREIRO | 1 | 20 | BB | não significativo | 0.001 | 0.008 |
| fdr | Estupro | 999 | OSORIO | 13 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr | Estupro | 999 | PORTO ALEGRE | 12 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr | Estupro | 999 | PORTO MAUA | 2 | 20 | BB | não significativo | 0.001 | 0.01 |
| fdr | Estupro | 999 | SANTA ROSA | 8 | 20 | BB | não significativo | 0.001 | 0.004 |
| fdr | Estupro | 999 | SANTO EXPEDITO DO SUL | 7 | 20 | BB | não significativo | 0.001 | 0.005 |
| fdr | Estupro | 999 | SENTINELA DO SUL | 7 | 20 | AA | não significativo | 0.001 | 0.005 |
| fdr | Estupro | 999 | SILVEIRA MARTINS | 5 | 20 | BA | não significativo | 0.001 | 0.005 |
| fdr | Estupro | 999 | TRAMANDAI | 11 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr | Estupro | 999 | TUCUNDUVA | 13 | 20 | BB | não significativo | 0.001 | 0.002 |
| fdr | Lesão Corporal | 999 | BALNEARIO PINHAL | 3 | 20 | AA | não significativo | 0.001 | 0.005 |
| fdr | Lesão Corporal | 999 | BARAO | 2 | 20 | BB | não significativo | 0.001 | 0.007 |
| fdr | Lesão Corporal | 999 | BOA VISTA DO SUL | 14 | 20 | BB | não significativo | 0.001 | 0.003 |
| fdr | Lesão Corporal | 999 | BOQUEIRAO DO LEAO | 7 | 20 | BB | não significativo | 0.001 | 0.005 |
| fdr | Lesão Corporal | 999 | BRAGA | 16 | 20 | AA | não significativo | 0.001 | 0.005 |
| fdr | Lesão Corporal | 999 | CAMPINA DAS MISSOES | 10 | 20 | BB | não significativo | 0.001 | 0.004 |
| fdr | Lesão Corporal | 999 | CANUDOS DO VALE | 15 | 20 | BB | não significativo | 0.001 | 0.002 |
| fdr | Lesão Corporal | 999 | CAPIVARI DO SUL | 16 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr | Lesão Corporal | 999 | CIDREIRA | 14 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr | Lesão Corporal | 999 | CORONEL BICACO | 1 | 20 | AA | não significativo | 0.002 | 0.012 |
| fdr | Lesão Corporal | 999 | FORQUETINHA | 3 | 20 | BB | não significativo | 0.001 | 0.008 |
| fdr | Lesão Corporal | 999 | IMBE | 1 | 20 | AA | não significativo | 0.002 | 0.014 |
| fdr | Lesão Corporal | 999 | LINHA NOVA | 12 | 20 | BB | não significativo | 0.001 | 0.002 |
| fdr | Lesão Corporal | 999 | MARQUES DE SOUZA | 1 | 20 | BB | não significativo | 0.001 | 0.007 |
| fdr | Lesão Corporal | 999 | MIRAGUAI | 2 | 20 | AA | não significativo | 0.001 | 0.006 |
| fdr | Lesão Corporal | 999 | NOVA BRESCIA | 1 | 20 | BB | não significativo | 0.002 | 0.012 |
| fdr | Lesão Corporal | 999 | OSORIO | 17 | 20 | AA | não significativo | 0.001 | 0.001 |
| fdr | Lesão Corporal | 999 | PICADA CAFE | 16 | 20 | BB | não significativo | 0.001 | 0.002 |
| fdr | Lesão Corporal | 999 | PRESIDENTE LUCENA | 6 | 20 | BB | não significativo | 0.001 | 0.005 |
| fdr | Lesão Corporal | 999 | REDENTORA | 2 | 20 | AA | não significativo | 0.001 | 0.006 |
| fdr | Lesão Corporal | 999 | SALVADOR DAS MISSOES | 5 | 20 | BB | não significativo | 0.001 | 0.005 |
| fdr | Lesão Corporal | 999 | SALVADOR DO SUL | 7 | 20 | BB | não significativo | 0.001 | 0.003 |
| fdr | Lesão Corporal | 999 | SAO PEDRO DO BUTIA | 10 | 20 | BB | não significativo | 0.001 | 0.004 |
| fdr | Lesão Corporal | 999 | SARANDI | 2 | 20 | AB | não significativo | 0.001 | 0.006 |
| fdr | Lesão Corporal | 999 | SERIO | 1 | 20 | BB | não significativo | 0.002 | 0.011 |
| fdr | Lesão Corporal | 999 | TRAMANDAI | 17 | 20 | AA | não significativo | 0.001 | 0.001 |
| fdr | Lesão Corporal | 999 | TUPANDI | 12 | 20 | BB | não significativo | 0.001 | 0.003 |
| fdr | Ameaça | 99999 | ALPESTRE | 14 | 20 | AA | não significativo | 0.00253 | 0.00321 |
| fdr | Ameaça | 99999 | BOA VISTA DAS MISSOES | 16 | 20 | AA | não significativo | 0.0026 | 0.00325 |
| fdr | Estupro | 99999 | BOA VISTA DO SUL | 1 | 20 | BB | não significativo | 0.0017 | 0.0022 |
| fdr | Estupro | 99999 | SILVEIRA MARTINS | 19 | 20 | BA | não significativo | 0.00134 | 0.00164 |
| fdr | Feminicídio Tentado | 99999 | PASSO DO SOBRADO | 16 | 20 | BB | não significativo | 0.00038 | 0.00069 |
| fdr | Feminicídio Tentado | 99999 | VALE VERDE | 18 | 20 | BB | não significativo | 0.00043 | 0.00064 |
| fdr | Lesão Corporal | 99999 | BOQUEIRAO DO LEAO | 18 | 20 | BB | não significativo | 0.00131 | 0.0017 |
| fdr_p2x | Ameaça | 999 | AMETISTA DO SUL | 5 | 20 | AA | não significativo | 0.001 | 0.001 |
| fdr_p2x | Ameaça | 999 | BOA VISTA DO SUL | 2 | 20 | BB | não significativo | 0.001 | 0.006 |
| fdr_p2x | Ameaça | 999 | BOM PROGRESSO | 5 | 20 | AA | não significativo | 0.001 | 0.001 |
| fdr_p2x | Ameaça | 999 | BRAGA | 4 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr_p2x | Ameaça | 999 | CARLOS BARBOSA | 1 | 20 | BB | não significativo | 0.001 | 0.011 |
| fdr_p2x | Ameaça | 999 | CORONEL BICACO | 5 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr_p2x | Ameaça | 999 | COTIPORA | 3 | 20 | BB | não significativo | 0.001 | 0.006 |
| fdr_p2x | Ameaça | 999 | CRISTAL DO SUL | 3 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr_p2x | Ameaça | 999 | DERRUBADAS | 3 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr_p2x | Ameaça | 999 | DOIS IRMAOS DAS MISSOES | 3 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr_p2x | Ameaça | 999 | ERVAL SECO | 4 | 20 | AA | não significativo | 0.001 | 0.003 |
| fdr_p2x | Ameaça | 999 | FREDERICO WESTPHALEN | 5 | 20 | AA | não significativo | 0.001 | 0.001 |
| fdr_p2x | Ameaça | 999 | GARIBALDI | 2 | 20 | BB | não significativo | 0.001 | 0.006 |
| fdr_p2x | Ameaça | 999 | IRAI | 5 | 20 | AA | não significativo | 0.001 | 0.001 |
| fdr_p2x | Ameaça | 999 | LINHA NOVA | 4 | 20 | BB | não significativo | 0.001 | 0.004 |
| fdr_p2x | Ameaça | 999 | MIRAGUAI | 2 | 20 | AA | não significativo | 0.001 | 0.006 |
| fdr_p2x | Ameaça | 999 | NOVA PETROPOLIS | 2 | 20 | BB | não significativo | 0.001 | 0.006 |
| fdr_p2x | Ameaça | 999 | NOVA RAMADA | 2 | 20 | BA | não significativo | 0.001 | 0.005 |
| fdr_p2x | Ameaça | 999 | PICADA CAFE | 5 | 20 | BB | não significativo | 0.001 | 0.002 |
| fdr_p2x | Ameaça | 999 | PLANALTO | 5 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr_p2x | Ameaça | 999 | PRESIDENTE LUCENA | 4 | 20 | BB | não significativo | 0.001 | 0.003 |
| fdr_p2x | Ameaça | 999 | REDENTORA | 5 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr_p2x | Ameaça | 999 | RODEIO BONITO | 4 | 20 | AA | não significativo | 0.001 | 0.004 |
| fdr_p2x | Ameaça | 999 | SARANDI | 4 | 20 | AB | não significativo | 0.001 | 0.004 |
| fdr_p2x | Ameaça | 999 | TAQUARUCU DO SUL | 3 | 20 | AA | não significativo | 0.001 | 0.005 |
| fdr_p2x | Ameaça | 999 | TENENTE PORTELA | 5 | 20 | AA | não significativo | 0.001 | 0.001 |
| fdr_p2x | Ameaça | 999 | TRES PASSOS | 5 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr_p2x | Ameaça | 999 | VICENTE DUTRA | 4 | 20 | AA | não significativo | 0.001 | 0.002 |
| fdr_p2x | Ameaça | 999 | VISTA GAUCHA | 2 | 20 | AA | não significativo | 0.001 | 0.004 |
| fdr_p2x | Ameaça | 99999 | BRAGA | 18 | 20 | AA | não significativo | 0.00066 | 0.001 |
| fdr_p2x | Ameaça | 99999 | DOIS IRMAOS DAS MISSOES | 16 | 20 | AA | não significativo | 0.00082 | 0.00112 |
| fdr_p2x | Ameaça | 99999 | ERVAL SECO | 12 | 20 | AA | não significativo | 0.00073 | 0.00114 |
| fdr_p2x | Ameaça | 99999 | GARIBALDI | 17 | 20 | BB | não significativo | 0.00064 | 0.00108 |
| fdr_p2x | Ameaça | 99999 | RODEIO BONITO | 17 | 20 | AA | não significativo | 0.00077 | 0.00115 |
| fdr_p2x | Estupro | 99999 | BENTO GONCALVES | 6 | 20 | AB | não significativo | 0.00026 | 0.00052 |
| fdr_p2x | Estupro | 99999 | DR MAURICIO CARDOSO | 5 | 20 | BB | não significativo | 0.00033 | 0.00058 |
| fdr_p2x | Estupro | 99999 | MARIANA PIMENTEL | 12 | 20 | BA | não significativo | 0.00021 | 0.00046 |
| fdr_p2x | Estupro | 99999 | PORTO ALEGRE | 12 | 20 | AA | não significativo | 0.00027 | 0.00049 |
| fdr_p2x | Estupro | 99999 | SENTINELA DO SUL | 1 | 20 | AA | não significativo | 0.0005 | 0.00094 |
| fdr_p2x | Feminicídio Tentado | 99999 | CANDELARIA | 14 | 20 | AB | não significativo | 2e-05 | 0.00011 |
| fdr_p2x | Feminicídio Tentado | 99999 | SANTA CRUZ DO SUL | 12 | 20 | BB | não significativo | 6e-05 | 0.00018 |
| fdr_p2x | Feminicídio Tentado | 99999 | SANTA MARIA DO HERVAL | 11 | 20 | AB | não significativo | 9e-05 | 0.0002 |
| fdr_p2x | Lesão Corporal | 99999 | CIDREIRA | 10 | 20 | AA | não significativo | 0.00019 | 0.00045 |
| fdr_p2x | Lesão Corporal | 99999 | LINHA NOVA | 19 | 20 | BB | não significativo | 0.00015 | 0.00031 |

## Execução

| permutacoes | execucoes_lisa | tempo_total_s | tempo_medio_por_lisa_s | pico_memoria_acumulado_mb |
| --- | --- | --- | --- | --- |
| 999 | 80 | 1.9 | 0.023 | 287.0 |
| 99999 | 80 | 184.9 | 2.309 | 1049.0 |
