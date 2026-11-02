# Caracterização dos municípios significativos no LISA

59 municípios significativos em ao menos um de quatro desfechos, 2018-2025, semente 12345, 99.999 permutações, FDR sobre o p direcional. Piso populacional do projeto: 5.000 habitantes, avaliado na população de 2025. Gerada por `src/analysis/caracterizacao_municipios_significativos.py`.

## 1. Verificação de método

**O LISA foi calculado sobre os 497 municípios, sem aplicar o piso.** 25 dos 59 municípios e 30 dos 68 pares município-desfecho estão abaixo dele. O piso existe no projeto para marcar taxas instáveis nos mapas, e esses municípios são tratados lá como instáveis.

**BB está mais concentrado logo acima do piso do que o conjunto dos 497: 8/24 entre 5.000 e 7.499 habitantes, contra 3,6 esperados; AA tem 5/28, contra 4,2.** Como o LISA não usa o piso, ele não pode ter selecionado esses municípios. Mas a faixa foi escolhida depois de ver os dados, o excesso enfraquece com outros cortes, e 11/24 dos BB estão abaixo do piso, proporção próxima à dos 497 (46,5%). É uma questão de método a declarar e investigar, não um achado.

**Há pares significativos sustentados por pouquíssimos eventos, e eles são a fragilidade mais direta:** ver a lista abaixo.

### Distribuição de população, 2025

| Grupo | n | Mín. | Q1 | Mediana | Q3 | Máx. | Abaixo do piso |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AA | 28 | 1.968 | 3.290 | 6.862 | 14.968 | 1.388.794 | 11 (39,3%) |
| BB | 24 | 1.686 | 3.160 | 5.322 | 6.460 | 138.270 | 11 (45,8%) |
| AB | 4 | 6.486 | 19.152 | 26.574 | 54.326 | 127.977 | 0 (0,0%) |
| BA | 3 | 2.056 | 2.127 | 2.198 | 3.102 | 4.005 | 3 (100,0%) |
| Os 59 | 59 | 1.686 | 3.179 | 5.999 | 15.116 | 1.388.794 | 25 (42,4%) |
| Os 497 | 497 | 1.156 | 2.937 | 5.490 | 15.413 | 1.388.794 | 231 (46,5%) |

AA contra BB, Mann-Whitney bilateral: U = 383,0, p = 0,393. Descritivo.

### Por faixa

| Faixa de população | AA | BB | 497 |
| --- | --- | --- | --- |
| < 3 mil | 6 (21,4%) | 5 (20,8%) | 128 (25,8%) |
| 3 a 5 mil | 5 (17,9%) | 6 (25,0%) | 103 (20,7%) |
| 5 a 6 mil | 1 (3,6%) | 4 (16,7%) | 33 (6,6%) |
| 6 a 7,5 mil | 4 (14,3%) | 4 (16,7%) | 42 (8,5%) |
| 7,5 a 10 mil | 3 (10,7%) | 0 (0,0%) | 27 (5,4%) |
| 10 a 50 mil | 7 (25,0%) | 2 (8,3%) | 118 (23,7%) |
| ≥ 50 mil | 2 (7,1%) | 3 (12,5%) | 46 (9,3%) |

### Logo acima do piso, frente ao que se esperaria dos 497

As probabilidades são descritivas: as faixas foram escolhidas depois de ver os dados, e os municípios não são independentes.

| Faixa | Quadrante | No quadrante | Nos 497 | Esperado | P(tantos ou mais) |
| --- | --- | --- | --- | --- | --- |
| 5.000 a 5.999 | AA | 1/28 | 33/497 | 1,9 | 0,862 |
| 5.000 a 5.999 | BB | 4/24 | 33/497 | 1,6 | 0,066 |
| 5.000 a 7.499 | AA | 5/28 | 75/497 | 4,2 | 0,419 |
| 5.000 a 7.499 | BB | 8/24 | 75/497 | 3,6 | 0,018 |
| 5.000 a 9.999 | AA | 8/28 | 102/497 | 5,7 | 0,196 |
| 5.000 a 9.999 | BB | 8/24 | 102/497 | 4,9 | 0,095 |

### Eventos no desfecho em que o par é significativo

| Desfecho | Quadrante | Pares | Abaixo do piso | Eventos, mín.–máx. | Mediana de eventos | Pares com zero evento | Pares com até 5 eventos |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ameaça | AA | 21 | 10 | 50–1133 | 205,0 | 0 | 0 |
| Ameaça | AB | 1 | 0 | 553–553 | 553,0 | 0 | 0 |
| Ameaça | BA | 1 | 1 | 27–27 | 27,0 | 0 | 0 |
| Ameaça | BB | 7 | 4 | 13–482 | 55,0 | 0 | 0 |
| Estupro | AA | 6 | 1 | 12–2319 | 62,0 | 0 | 0 |
| Estupro | AB | 1 | 0 | 200–200 | 200,0 | 0 | 0 |
| Estupro | BA | 2 | 2 | 0–2 | 1,0 | 1 | 2 |
| Estupro | BB | 7 | 3 | 1–109 | 7,0 | 0 | 2 |
| Feminicídio Tentado | AA | 1 | 0 | 2–2 | 2,0 | 0 | 1 |
| Feminicídio Tentado | AB | 2 | 0 | 3–10 | 6,5 | 0 | 1 |
| Feminicídio Tentado | BB | 3 | 1 | 0–16 | 0,0 | 2 | 2 |
| Lesão Corporal | AA | 5 | 2 | 45–1366 | 487,0 | 0 | 0 |
| Lesão Corporal | BB | 11 | 6 | 1–40 | 13,0 | 0 | 1 |

### Pares significativos com até 5 eventos

| Município | Desfecho | Quadrante | Eventos | População 2025 | Sementes |
| --- | --- | --- | --- | --- | --- |
| MARIANA PIMENTEL | Estupro | BA | 0 | 4.005 | 20/20 |
| PASSO DO SOBRADO | Feminicídio Tentado | BB | 0 | 6.155 | 16/20 |
| VALE VERDE | Feminicídio Tentado | BB | 0 | 3.213 | 18/20 |
| SANTO EXPEDITO DO SUL | Estupro | BB | 1 | 2.395 | 20/20 |
| CANUDOS DO VALE | Lesão Corporal | BB | 1 | 1.686 | 20/20 |
| DR MAURICIO CARDOSO | Estupro | BB | 2 | 4.534 | 20/20 |
| SILVEIRA MARTINS | Estupro | BA | 2 | 2.056 | 19/20 |
| ALPESTRE | Feminicídio Tentado | AA | 2 | 7.235 | 20/20 |
| SANTA MARIA DO HERVAL | Feminicídio Tentado | AB | 3 | 6.486 | 20/20 |

### Os 59 municípios

Eventos no período inteiro. Entre parênteses, as sementes em que o par é significativo, de 20.

| Município | Quadrante | Significativo em | População 2025 | Frente ao piso | Ameaça | Estupro | Feminicídio Consumado | Feminicídio Tentado | Lesão Corporal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PORTO ALEGRE | AA | Estupro (20/20) | 1.388.794 | acima (+1.383.794) | 28556 | 2319 | 77 | 449 | 22597 |
| TRAMANDAI | AA | Estupro (20/20); Lesão Corporal (20/20) | 56.430 | acima (+51.430) | 2207 | 148 | 1 | 14 | 1366 |
| OSORIO | AA | Estupro (20/20); Lesão Corporal (20/20) | 48.999 | acima (+43.999) | 1200 | 93 | 1 | 9 | 704 |
| FREDERICO WESTPHALEN | AA | Ameaça (20/20) | 33.726 | acima (+28.726) | 1133 | 64 | 1 | 5 | 499 |
| TRES PASSOS | AA | Ameaça (20/20) | 26.304 | acima (+21.304) | 997 | 26 | 3 | 9 | 375 |
| CIDREIRA | AA | Lesão Corporal (20/20) | 17.583 | acima (+12.583) | 646 | 82 | 2 | 1 | 487 |
| BALNEARIO PINHAL | AA | Estupro (20/20) | 15.413 | acima (+10.413) | 468 | 31 | 3 | 6 | 373 |
| TENENTE PORTELA | AA | Ameaça (20/20) | 14.820 | acima (+9.820) | 574 | 23 | 1 | 3 | 314 |
| PLANALTO | AA | Ameaça (20/20) | 10.624 | acima (+5.624) | 382 | 22 | 2 | 5 | 126 |
| REDENTORA | AA | Ameaça (20/20) | 9.931 | acima (+4.931) | 259 | 16 | 2 | 3 | 180 |
| AMETISTA DO SUL | AA | Ameaça (20/20) | 7.826 | acima (+2.826) | 334 | 19 | 1 | 1 | 115 |
| IRAI | AA | Ameaça (20/20) | 7.619 | acima (+2.619) | 412 | 18 | 1 | 11 | 144 |
| ALPESTRE | AA | Ameaça (14/20); Feminicídio Tentado (20/20) | 7.235 | acima (+2.235) | 205 | 7 | 1 | 2 | 64 |
| ERVAL SECO | AA | Ameaça (20/20) | 6.892 | acima (+1.892) | 228 | 18 | 1 | 1 | 64 |
| RODEIO BONITO | AA | Ameaça (20/20) | 6.831 | acima (+1.831) | 184 | 12 | 2 | 0 | 56 |
| CORONEL BICACO | AA | Ameaça (20/20) | 6.214 | acima (+1.214) | 201 | 11 | 1 | 1 | 134 |
| SENTINELA DO SUL | AA | Estupro (20/20) | 5.424 | acima (+424) | 99 | 15 | 1 | 1 | 56 |
| VICENTE DUTRA | AA | Ameaça (20/20) | 4.741 | abaixo (-259) | 213 | 17 | 0 | 1 | 63 |
| MIRAGUAI | AA | Ameaça (20/20) | 4.501 | abaixo (-499) | 220 | 12 | 1 | 0 | 90 |
| CAPIVARI DO SUL | AA | Estupro (20/20); Lesão Corporal (20/20) | 4.080 | abaixo (-920) | 59 | 12 | 0 | 1 | 45 |
| BRAGA | AA | Ameaça (20/20); Lesão Corporal (20/20) | 3.322 | abaixo (-1.678) | 109 | 7 | 1 | 1 | 52 |
| TAQUARUCU DO SUL | AA | Ameaça (20/20) | 3.192 | abaixo (-1.808) | 73 | 2 | 0 | 1 | 35 |
| VISTA GAUCHA | AA | Ameaça (20/20) | 2.843 | abaixo (-2.157) | 63 | 7 | 0 | 0 | 20 |
| DERRUBADAS | AA | Ameaça (20/20) | 2.793 | abaixo (-2.207) | 95 | 6 | 0 | 0 | 30 |
| CRISTAL DO SUL | AA | Ameaça (20/20) | 2.745 | abaixo (-2.255) | 83 | 5 | 0 | 1 | 16 |
| BOM PROGRESSO | AA | Ameaça (20/20) | 2.132 | abaixo (-2.868) | 61 | 2 | 0 | 0 | 28 |
| DOIS IRMAOS DAS MISSOES | AA | Ameaça (20/20) | 2.132 | abaixo (-2.868) | 50 | 7 | 0 | 0 | 22 |
| BOA VISTA DAS MISSOES | AA | Ameaça (16/20) | 1.968 | abaixo (-3.032) | 78 | 3 | 0 | 1 | 24 |
| SANTA CRUZ DO SUL | BB | Feminicídio Tentado (20/20) | 138.270 | acima (+133.270) | 3260 | 203 | 7 | 16 | 1768 |
| SANTA ROSA | BB | Estupro (20/20) | 79.488 | acima (+74.488) | 2510 | 109 | 11 | 4 | 1088 |
| FARROUPILHA | BB | Estupro (20/20) | 72.552 | acima (+67.552) | 1582 | 65 | 4 | 8 | 854 |
| GARIBALDI | BB | Ameaça (20/20) | 35.563 | acima (+30.563) | 482 | 19 | 4 | 2 | 309 |
| NOVA PETROPOLIS | BB | Ameaça (20/20) | 23.934 | acima (+18.934) | 336 | 38 | 2 | 1 | 133 |
| SALVADOR DO SUL | BB | Lesão Corporal (20/20) | 7.184 | acima (+2.184) | 103 | 15 | 0 | 1 | 40 |
| ALECRIM | BB | Estupro (20/20) | 6.219 | acima (+1.219) | 195 | 7 | 1 | 1 | 49 |
| BOQUEIRAO DO LEAO | BB | Lesão Corporal (18/20) | 6.202 | acima (+1.202) | 118 | 14 | 0 | 1 | 33 |
| PASSO DO SOBRADO | BB | Feminicídio Tentado (16/20) | 6.155 | acima (+1.155) | 111 | 6 | 1 | 0 | 58 |
| CAMPINA DAS MISSOES | BB | Lesão Corporal (20/20) | 5.999 | acima (+999) | 114 | 6 | 1 | 1 | 40 |
| TUCUNDUVA | BB | Estupro (20/20) | 5.646 | acima (+646) | 131 | 8 | 0 | 1 | 71 |
| PICADA CAFE | BB | Ameaça (20/20); Lesão Corporal (20/20) | 5.473 | acima (+473) | 55 | 7 | 0 | 0 | 25 |
| TUPANDI | BB | Lesão Corporal (20/20) | 5.172 | acima (+172) | 70 | 8 | 1 | 0 | 31 |
| CACIQUE DOBLE | BB | Estupro (20/20) | 4.692 | abaixo (-308) | 95 | 6 | 1 | 2 | 114 |
| DR MAURICIO CARDOSO | BB | Estupro (20/20) | 4.534 | abaixo (-466) | 87 | 2 | 1 | 0 | 31 |
| COTIPORA | BB | Ameaça (20/20) | 3.926 | abaixo (-1.074) | 64 | 3 | 1 | 0 | 39 |
| VALE VERDE | BB | Feminicídio Tentado (18/20) | 3.213 | abaixo (-1.787) | 37 | 2 | 0 | 0 | 11 |
| PRESIDENTE LUCENA | BB | Ameaça (20/20); Lesão Corporal (20/20) | 3.166 | abaixo (-1.834) | 22 | 8 | 0 | 0 | 7 |
| SAO PEDRO DO BUTIA | BB | Lesão Corporal (20/20) | 3.142 | abaixo (-1.858) | 24 | 2 | 0 | 0 | 10 |
| SALVADOR DAS MISSOES | BB | Lesão Corporal (20/20) | 2.955 | abaixo (-2.045) | 18 | 5 | 1 | 0 | 7 |
| BOA VISTA DO SUL | BB | Ameaça (20/20); Lesão Corporal (20/20) | 2.815 | abaixo (-2.185) | 16 | 3 | 0 | 0 | 13 |
| SANTO EXPEDITO DO SUL | BB | Estupro (20/20) | 2.395 | abaixo (-2.605) | 26 | 1 | 0 | 1 | 9 |
| LINHA NOVA | BB | Ameaça (20/20); Lesão Corporal (20/20) | 1.721 | abaixo (-3.279) | 13 | 3 | 0 | 0 | 7 |
| CANUDOS DO VALE | BB | Lesão Corporal (20/20) | 1.686 | abaixo (-3.314) | 17 | 4 | 0 | 0 | 1 |
| BENTO GONCALVES | AB | Estupro (20/20) | 127.977 | acima (+122.977) | 2781 | 200 | 12 | 21 | 1852 |
| CANDELARIA | AB | Feminicídio Tentado (20/20) | 29.775 | acima (+24.775) | 803 | 51 | 5 | 10 | 411 |
| SARANDI | AB | Ameaça (20/20) | 23.374 | acima (+18.374) | 553 | 26 | 2 | 1 | 261 |
| SANTA MARIA DO HERVAL | AB | Feminicídio Tentado (20/20) | 6.486 | acima (+1.486) | 79 | 8 | 0 | 3 | 40 |
| MARIANA PIMENTEL | BA | Estupro (20/20) | 4.005 | abaixo (-995) | 55 | 0 | 0 | 2 | 28 |
| NOVA RAMADA | BA | Ameaça (20/20) | 2.198 | abaixo (-2.802) | 27 | 1 | 1 | 1 | 14 |
| SILVEIRA MARTINS | BA | Estupro (19/20) | 2.056 | abaixo (-2.944) | 48 | 2 | 0 | 0 | 13 |

## 2. Caracterização territorial

**O repositório não tem grau de urbanização.** A densidade abaixo é informação própria, não substituto.

### Contiguidade dentro de cada quadrante

Contiguidade de rainha, a mesma matriz do teste. Municípios vizinhos partilham vizinhos no cálculo do I local, de modo que a contiguidade dos significativos é em parte esperada e não é evidência independente.

| Quadrante | Municípios | Blocos contíguos | Tamanhos | Isolados |
| --- | --- | --- | --- | --- |
| AA | 28 | 4 | 21, 5, 1, 1 | 2 |
| BB | 24 | 10 | 4, 3, 3, 3, 3, 2, 2, 2, 1, 1 | 2 |
| AB | 4 | 4 | 1, 1, 1, 1 | 4 |
| BA | 3 | 3 | 1, 1, 1 | 3 |

### Blocos verificados

| Conjunto | Municípios e COREDE | Pares vizinhos | Bloco único | Partes |
| --- | --- | --- | --- | --- |
| Três do Litoral em AA, os da sobreposição | CAPIVARI DO SUL (Litoral); OSORIO (Litoral); TRAMANDAI (Litoral) | CAPIVARI DO SUL–OSORIO, OSORIO–TRAMANDAI | sim | CAPIVARI DO SUL, OSORIO, TRAMANDAI |
| Quatro em BB da sobreposição Ameaça + Lesão Corporal | BOA VISTA DO SUL (Serra); LINHA NOVA (Vale do Caí); PICADA CAFE (Hortênsias); PRESIDENTE LUCENA (Paranhana Encosta da Serra) | LINHA NOVA–PICADA CAFE, LINHA NOVA–PRESIDENTE LUCENA, PICADA CAFE–PRESIDENTE LUCENA | não | LINHA NOVA, PICADA CAFE, PRESIDENTE LUCENA / BOA VISTA DO SUL |
| Todos os AA do COREDE Litoral | BALNEARIO PINHAL (Litoral); CAPIVARI DO SUL (Litoral); CIDREIRA (Litoral); OSORIO (Litoral); TRAMANDAI (Litoral) | BALNEARIO PINHAL–CAPIVARI DO SUL, BALNEARIO PINHAL–CIDREIRA, CAPIVARI DO SUL–CIDREIRA, CAPIVARI DO SUL–OSORIO, CIDREIRA–OSORIO, CIDREIRA–TRAMANDAI, OSORIO–TRAMANDAI | sim | BALNEARIO PINHAL, CAPIVARI DO SUL, CIDREIRA, OSORIO, TRAMANDAI |
| Todos os BB do COREDE Serra | BOA VISTA DO SUL (Serra); COTIPORA (Serra); FARROUPILHA (Serra); GARIBALDI (Serra) | BOA VISTA DO SUL–GARIBALDI, FARROUPILHA–GARIBALDI | não | BOA VISTA DO SUL, FARROUPILHA, GARIBALDI / COTIPORA |

### Território dos 59

| Município | Quadrante | COREDE | Região funcional | Região imediata | Região intermediária | Densidade (hab./km²) | Bloco do quadrante (tamanho) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ALPESTRE | AA | Médio Alto Uruguai | RF9 | Nonoai | Passo Fundo | 22,2 | AA-1 (21) |
| AMETISTA DO SUL | AA | Médio Alto Uruguai | RF9 | Frederico Westphalen | Passo Fundo | 83,4 | AA-1 (21) |
| BOA VISTA DAS MISSOES | AA | Rio da Várzea | RF9 | Frederico Westphalen | Passo Fundo | 10,2 | AA-1 (21) |
| BOM PROGRESSO | AA | Celeiro | RF7 | Três Passos | Ijuí | 24,2 | AA-1 (21) |
| BRAGA | AA | Celeiro | RF7 | Três Passos | Ijuí | 25,1 | AA-1 (21) |
| CORONEL BICACO | AA | Celeiro | RF7 | Ijuí | Ijuí | 12,6 | AA-1 (21) |
| CRISTAL DO SUL | AA | Médio Alto Uruguai | RF9 | Frederico Westphalen | Passo Fundo | 28,4 | AA-1 (21) |
| DERRUBADAS | AA | Celeiro | RF7 | Três Passos | Ijuí | 7,8 | AA-1 (21) |
| DOIS IRMAOS DAS MISSOES | AA | Médio Alto Uruguai | RF9 | Palmeira das Missões | Passo Fundo | 9,4 | AA-1 (21) |
| ERVAL SECO | AA | Médio Alto Uruguai | RF9 | Frederico Westphalen | Passo Fundo | 19,4 | AA-1 (21) |
| FREDERICO WESTPHALEN | AA | Médio Alto Uruguai | RF9 | Frederico Westphalen | Passo Fundo | 127,3 | AA-1 (21) |
| IRAI | AA | Médio Alto Uruguai | RF9 | Frederico Westphalen | Passo Fundo | 41,6 | AA-1 (21) |
| MIRAGUAI | AA | Celeiro | RF7 | Três Passos | Ijuí | 34,5 | AA-1 (21) |
| PLANALTO | AA | Médio Alto Uruguai | RF9 | Nonoai | Passo Fundo | 46,8 | AA-1 (21) |
| REDENTORA | AA | Celeiro | RF7 | Três Passos | Ijuí | 32,6 | AA-1 (21) |
| RODEIO BONITO | AA | Médio Alto Uruguai | RF9 | Frederico Westphalen | Passo Fundo | 81,3 | AA-1 (21) |
| TAQUARUCU DO SUL | AA | Médio Alto Uruguai | RF9 | Frederico Westphalen | Passo Fundo | 41,9 | AA-1 (21) |
| TENENTE PORTELA | AA | Celeiro | RF7 | Três Passos | Ijuí | 44,1 | AA-1 (21) |
| TRES PASSOS | AA | Celeiro | RF7 | Três Passos | Ijuí | 97,4 | AA-1 (21) |
| VICENTE DUTRA | AA | Médio Alto Uruguai | RF9 | Frederico Westphalen | Passo Fundo | 24,6 | AA-1 (21) |
| VISTA GAUCHA | AA | Celeiro | RF7 | Três Passos | Ijuí | 30,9 | AA-1 (21) |
| BALNEARIO PINHAL | AA | Litoral | RF4 | Tramandaí - Osório | Porto Alegre | 150,0 | AA-2 (5) |
| CAPIVARI DO SUL | AA | Litoral | RF4 | Porto Alegre | Porto Alegre | 9,9 | AA-2 (5) |
| CIDREIRA | AA | Litoral | RF4 | Tramandaí - Osório | Porto Alegre | 72,4 | AA-2 (5) |
| OSORIO | AA | Litoral | RF4 | Tramandaí - Osório | Porto Alegre | 73,8 | AA-2 (5) |
| TRAMANDAI | AA | Litoral | RF4 | Tramandaí - Osório | Porto Alegre | 394,6 | AA-2 (5) |
| PORTO ALEGRE | AA | Metropolitano Delta do Jacuí | RF1 | Porto Alegre | Porto Alegre | 2.819,1 | AA-3 (1) |
| SENTINELA DO SUL | AA | Centro-Sul | RF1 | Camaquã | Porto Alegre | 19,2 | AA-4 (1) |
| LINHA NOVA | BB | Vale do Caí | RF1 | Novo Hamburgo - São Leopoldo | Porto Alegre | 26,9 | BB-1 (4) |
| NOVA PETROPOLIS | BB | Hortênsias | RF3 | Caxias do Sul | Caxias do Sul | 82,4 | BB-1 (4) |
| PICADA CAFE | BB | Hortênsias | RF3 | Caxias do Sul | Caxias do Sul | 64,9 | BB-1 (4) |
| PRESIDENTE LUCENA | BB | Paranhana Encosta da Serra | RF1 | Novo Hamburgo - São Leopoldo | Porto Alegre | 64,7 | BB-1 (4) |
| COTIPORA | BB | Serra | RF3 | Bento Gonçalves | Caxias do Sul | 22,7 | BB-10 (1) |
| BOA VISTA DO SUL | BB | Serra | RF3 | Bento Gonçalves | Caxias do Sul | 29,8 | BB-2 (3) |
| FARROUPILHA | BB | Serra | RF3 | Caxias do Sul | Caxias do Sul | 201,1 | BB-2 (3) |
| GARIBALDI | BB | Serra | RF3 | Bento Gonçalves | Caxias do Sul | 211,4 | BB-2 (3) |
| CAMPINA DAS MISSOES | BB | Fronteira Noroeste | RF7 | Santa Rosa | Ijuí | 26,8 | BB-3 (3) |
| SALVADOR DAS MISSOES | BB | Missões | RF7 | Cerro Largo | Ijuí | 31,1 | BB-3 (3) |
| SAO PEDRO DO BUTIA | BB | Missões | RF7 | Cerro Largo | Ijuí | 29,1 | BB-3 (3) |
| DR MAURICIO CARDOSO | BB | Fronteira Noroeste | RF7 | Três de Maio | Ijuí | 17,7 | BB-4 (3) |
| SANTA ROSA | BB | Fronteira Noroeste | RF7 | Santa Rosa | Ijuí | 162,5 | BB-4 (3) |
| TUCUNDUVA | BB | Fronteira Noroeste | RF7 | Santa Rosa | Ijuí | 31,2 | BB-4 (3) |
| PASSO DO SOBRADO | BB | Vale do Rio Pardo | RF2 | Santa Cruz do Sul | Santa Cruz do Sul - Lajeado | 23,2 | BB-5 (3) |
| SANTA CRUZ DO SUL | BB | Vale do Rio Pardo | RF2 | Santa Cruz do Sul | Santa Cruz do Sul - Lajeado | 188,6 | BB-5 (3) |
| VALE VERDE | BB | Vale do Rio Pardo | RF2 | Santa Cruz do Sul | Santa Cruz do Sul - Lajeado | 9,8 | BB-5 (3) |
| BOQUEIRAO DO LEAO | BB | Vale do Rio Pardo | RF2 | Lajeado | Santa Cruz do Sul - Lajeado | 23,2 | BB-6 (2) |
| CANUDOS DO VALE | BB | Vale do Taquari | RF2 | Lajeado | Santa Cruz do Sul - Lajeado | 20,2 | BB-6 (2) |
| CACIQUE DOBLE | BB | Nordeste | RF9 | Lagoa Vermelha | Passo Fundo | 23,1 | BB-7 (2) |
| SANTO EXPEDITO DO SUL | BB | Nordeste | RF9 | Tapejara - Sananduva | Passo Fundo | 19,2 | BB-7 (2) |
| SALVADOR DO SUL | BB | Vale do Caí | RF1 | Montenegro | Porto Alegre | 72,3 | BB-8 (2) |
| TUPANDI | BB | Vale do Caí | RF1 | Novo Hamburgo - São Leopoldo | Porto Alegre | 86,7 | BB-8 (2) |
| ALECRIM | BB | Fronteira Noroeste | RF7 | Santa Rosa | Ijuí | 19,8 | BB-9 (1) |
| BENTO GONCALVES | AB | Serra | RF3 | Bento Gonçalves | Caxias do Sul | 470,4 | AB-1 (1) |
| CANDELARIA | AB | Vale do Rio Pardo | RF2 | Santa Cruz do Sul | Santa Cruz do Sul - Lajeado | 31,5 | AB-2 (1) |
| SANTA MARIA DO HERVAL | AB | Paranhana Encosta da Serra | RF1 | Novo Hamburgo - São Leopoldo | Porto Alegre | 46,2 | AB-3 (1) |
| SARANDI | AB | Rio da Várzea | RF9 | Carazinho | Passo Fundo | 66,0 | AB-4 (1) |
| MARIANA PIMENTEL | BA | Centro-Sul | RF1 | Porto Alegre | Porto Alegre | 11,8 | BA-1 (1) |
| NOVA RAMADA | BA | Noroeste Colonial | RF7 | Ijuí | Ijuí | 8,6 | BA-2 (1) |
| SILVEIRA MARTINS | BA | Central | RF8 | Santa Maria | Santa Maria | 17,1 | BA-3 (1) |

## 3. Rede de atendimento

**Os dados não estão no repositório, e nenhuma comparação de cobertura foi feita.** A busca cobriu nomes de arquivos, conteúdo textual e colunas das tabelas de `data/` e `outputs/`, os JSON do portal e o histórico do Git.

| Item | Fonte esperada | No repositório | Processado |
| --- | --- | --- | --- |
| Organismo de políticas para mulheres | MUNIC/IBGE | não | não |
| Delegacia especializada | MUNIC/IBGE ou registro estadual | não | não |
| Conselho de direitos | MUNIC/IBGE | não | não |
| Casa abrigo | MUNIC/IBGE | não | não |
| CRAS | Censo SUAS | não | não |
| CREAS | Censo SUAS | não | não |

Para comparar, faltam: obter as bases, escolher as edições, definir cada indicador e cruzar por `codigo_ibge` com `outputs/tables/municipio_codigo_ibge.csv`, que já cobre os 497.
