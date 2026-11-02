# Esperado sob a taxa estadual frente ao observado, nos pares significativos do LISA

São os 68 pares município-desfecho significativos no LISA de Assunção e Reis, 2018-2025 (semente 12345, 99.999 permutações, FDR sobre o p direcional). Gerada por `src/analysis/esperado_vs_observado_lisa.py`.

- **Esperado** = pessoas-ano do município em 2018-2025 × taxa estadual / 100 mil. As pessoas-ano são a soma das oito populações anuais, o mesmo denominador do LISA, e equivalem a "população × 8 anos". Como verificação, há também uma coluna com a população de 2025 × 8.
- **Taxa estadual por 100 mil pessoas-ano**, soma dos 497 municípios, sem "NÃO INFORMADO": Ameaça 299,91; Estupro 20,81; Feminicídio Consumado 0,82; Feminicídio Tentado 2,54; Lesão Corporal 172,29.
- **Poisson na direção do quadrante:** P(X ≥ obs) em AA e AB; P(X ≤ obs) em BB e BA. É descritivo: não corrige para múltiplas comparações e ignora a vizinhança, que é o que o LISA mede.

## Por quadrante

| Quadrante | Pares | Esperado < 5 | Sobrevivem (esperado ≥ 5) | Esperado < 5, pop. 2025 × 8 | Poisson p < 0,05 | Esperado ≥ 5 e Poisson p < 0,05 |
| --- | --- | --- | --- | --- | --- | --- |
| AA | 33 | 1 | 32 | 1 | 22 | 22 |
| AB | 4 | 1 | 3 | 1 | 0 | 0 |
| BA | 3 | 1 | 2 | 1 | 2 | 2 |
| BB | 28 | 3 | 25 | 3 | 21 | 21 |
| Total | 68 | 6 | 62 | 6 | 45 | 45 |

## Por desfecho

| Desfecho | Pares | Esperado < 5 | Sobrevivem (esperado ≥ 5) | Esperado < 5, pop. 2025 × 8 | Poisson p < 0,05 | Esperado ≥ 5 e Poisson p < 0,05 |
| --- | --- | --- | --- | --- | --- | --- |
| Ameaça | 30 | 0 | 30 | 0 | 25 | 25 |
| Estupro | 16 | 2 | 14 | 2 | 5 | 5 |
| Feminicídio Tentado | 6 | 4 | 2 | 4 | 1 | 1 |
| Lesão Corporal | 16 | 0 | 16 | 0 | 14 | 14 |
| Total | 68 | 6 | 62 | 6 | 45 | 45 |

## Bloco norte em AA (21 municípios contíguos)

- **21 dos 21 municípios sobrevivem** ao critério de esperado ≥ 5, com ao menos um par acima do limiar. Em 20 deles, todos os pares estão acima.
- O bloco tem 23 pares. 1 ficam abaixo do limiar: ALPESTRE (Feminicídio Tentado, esperado 1,36).
- Com esperado ≥ 5 e também Poisson p < 0,05, sobrevivem 17 dos 21.

## Pares com o observado do lado oposto ao do quadrante

6 pares estão num quadrante "alto" (AA ou AB) com o observado abaixo do esperado estadual. Nenhum está num quadrante "baixo" com o observado acima. Isso não é erro de cálculo. `esda.Moran_Local_Rate` padroniza as taxas pelo método de Assunção e Reis em torno da taxa estadual, mas o LISA centra esses valores na média deles. Essa média é negativa nos quatro desfechos, porque a maioria dos municípios, pequenos, fica abaixo da taxa estadual. Assim, "alto" no LISA quer dizer acima da média dos municípios, não acima da taxa estadual. Nesses pares, P(X ≥ obs) fica acima de 0,5 por construção.

| Município | Desfecho | Quadrante | Observado | Esperado | Obs./esp. | Poisson, direção do quadrante | Esperado ≥ 5 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VISTA GAUCHA | Ameaça | AA | 63 | 68,05 | 0,93 | 0,7460 | sim |
| TAQUARUCU DO SUL | Ameaça | AA | 73 | 74,84 | 0,98 | 0,5995 | sim |
| PORTO ALEGRE | Estupro | AA | 2319 | 2.375,25 | 0,98 | 0,8781 | sim |
| CAPIVARI DO SUL | Lesão Corporal | AA | 45 | 60,23 | 0,75 | 0,9823 | sim |
| SARANDI | Ameaça | AB | 553 | 573,33 | 0,96 | 0,8074 | sim |
| BENTO GONCALVES | Estupro | AB | 200 | 205,73 | 0,97 | 0,6646 | sim |

## Os 68 pares

| Município | Desfecho | Quadrante | Observado | Esperado | Obs./esp. | Poisson, direção do quadrante | Esperado ≥ 5 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BOM PROGRESSO | Ameaça | AA | 61 | 48,47 | 1,26 | 0,0460 | sim |
| BOA VISTA DAS MISSOES | Ameaça | AA | 78 | 48,59 | 1,61 | < 0,0001 | sim |
| DOIS IRMAOS DAS MISSOES | Ameaça | AA | 50 | 49,60 | 1,01 | 0,4960 | sim |
| DERRUBADAS | Ameaça | AA | 95 | 66,73 | 1,42 | 0,0007 | sim |
| CRISTAL DO SUL | Ameaça | AA | 83 | 66,83 | 1,24 | 0,0309 | sim |
| VISTA GAUCHA | Ameaça | AA | 63 | 68,05 | 0,93 | 0,7460 | sim |
| TAQUARUCU DO SUL | Ameaça | AA | 73 | 74,84 | 0,98 | 0,5995 | sim |
| BRAGA | Ameaça | AA | 109 | 79,61 | 1,37 | 0,0010 | sim |
| VICENTE DUTRA | Ameaça | AA | 213 | 112,18 | 1,90 | < 0,0001 | sim |
| MIRAGUAI | Ameaça | AA | 220 | 112,34 | 1,96 | < 0,0001 | sim |
| RODEIO BONITO | Ameaça | AA | 184 | 151,50 | 1,21 | 0,0057 | sim |
| ALPESTRE | Ameaça | AA | 205 | 160,28 | 1,28 | 0,0004 | sim |
| CORONEL BICACO | Ameaça | AA | 201 | 161,85 | 1,24 | 0,0016 | sim |
| ERVAL SECO | Ameaça | AA | 228 | 164,58 | 1,39 | < 0,0001 | sim |
| IRAI | Ameaça | AA | 412 | 177,10 | 2,33 | < 0,0001 | sim |
| AMETISTA DO SUL | Ameaça | AA | 334 | 181,92 | 1,84 | < 0,0001 | sim |
| PLANALTO | Ameaça | AA | 382 | 247,07 | 1,55 | < 0,0001 | sim |
| REDENTORA | Ameaça | AA | 259 | 257,82 | 1,00 | 0,4790 | sim |
| TENENTE PORTELA | Ameaça | AA | 574 | 337,77 | 1,70 | < 0,0001 | sim |
| TRES PASSOS | Ameaça | AA | 997 | 598,03 | 1,67 | < 0,0001 | sim |
| FREDERICO WESTPHALEN | Ameaça | AA | 1133 | 776,17 | 1,46 | < 0,0001 | sim |
| CAPIVARI DO SUL | Estupro | AA | 12 | 7,27 | 1,65 | 0,0667 | sim |
| SENTINELA DO SUL | Estupro | AA | 15 | 9,13 | 1,64 | 0,0459 | sim |
| BALNEARIO PINHAL | Estupro | AA | 31 | 24,50 | 1,27 | 0,1150 | sim |
| OSORIO | Estupro | AA | 93 | 78,71 | 1,18 | 0,0629 | sim |
| TRAMANDAI | Estupro | AA | 148 | 89,69 | 1,65 | < 0,0001 | sim |
| PORTO ALEGRE | Estupro | AA | 2319 | 2.375,25 | 0,98 | 0,8781 | sim |
| ALPESTRE | Feminicídio Tentado | AA | 2 | 1,36 | 1,47 | 0,3934 | não |
| BRAGA | Lesão Corporal | AA | 52 | 45,74 | 1,14 | 0,1950 | sim |
| CAPIVARI DO SUL | Lesão Corporal | AA | 45 | 60,23 | 0,75 | 0,9823 | sim |
| CIDREIRA | Lesão Corporal | AA | 487 | 232,84 | 2,09 | < 0,0001 | sim |
| OSORIO | Lesão Corporal | AA | 704 | 651,73 | 1,08 | 0,0223 | sim |
| TRAMANDAI | Lesão Corporal | AA | 1366 | 742,70 | 1,84 | < 0,0001 | sim |
| SARANDI | Ameaça | AB | 553 | 573,33 | 0,96 | 0,8074 | sim |
| BENTO GONCALVES | Estupro | AB | 200 | 205,73 | 0,97 | 0,6646 | sim |
| SANTA MARIA DO HERVAL | Feminicídio Tentado | AB | 3 | 1,30 | 2,31 | 0,1425 | não |
| CANDELARIA | Feminicídio Tentado | AB | 10 | 6,18 | 1,62 | 0,0970 | sim |
| NOVA RAMADA | Ameaça | BA | 27 | 52,99 | 0,51 | < 0,0001 | sim |
| SILVEIRA MARTINS | Estupro | BA | 2 | 3,68 | 0,54 | 0,2882 | não |
| MARIANA PIMENTEL | Estupro | BA | 0 | 6,54 | 0,00 | 0,0014 | sim |
| LINHA NOVA | Ameaça | BB | 13 | 41,06 | 0,32 | < 0,0001 | sim |
| BOA VISTA DO SUL | Ameaça | BB | 16 | 66,96 | 0,24 | < 0,0001 | sim |
| PRESIDENTE LUCENA | Ameaça | BB | 22 | 72,56 | 0,30 | < 0,0001 | sim |
| COTIPORA | Ameaça | BB | 64 | 92,87 | 0,69 | 0,0010 | sim |
| PICADA CAFE | Ameaça | BB | 55 | 133,94 | 0,41 | < 0,0001 | sim |
| NOVA PETROPOLIS | Ameaça | BB | 336 | 541,28 | 0,62 | < 0,0001 | sim |
| GARIBALDI | Ameaça | BB | 482 | 843,76 | 0,57 | < 0,0001 | sim |
| SANTO EXPEDITO DO SUL | Estupro | BB | 1 | 3,91 | 0,26 | 0,0988 | não |
| DR MAURICIO CARDOSO | Estupro | BB | 2 | 7,51 | 0,27 | 0,0201 | sim |
| CACIQUE DOBLE | Estupro | BB | 6 | 8,10 | 0,74 | 0,3017 | sim |
| TUCUNDUVA | Estupro | BB | 8 | 9,38 | 0,85 | 0,4068 | sim |
| ALECRIM | Estupro | BB | 7 | 10,05 | 0,70 | 0,2156 | sim |
| FARROUPILHA | Estupro | BB | 65 | 120,14 | 0,54 | < 0,0001 | sim |
| SANTA ROSA | Estupro | BB | 109 | 126,43 | 0,86 | 0,0634 | sim |
| VALE VERDE | Feminicídio Tentado | BB | 0 | 0,68 | 0,00 | 0,5065 | não |
| PASSO DO SOBRADO | Feminicídio Tentado | BB | 0 | 1,29 | 0,00 | 0,2763 | não |
| SANTA CRUZ DO SUL | Feminicídio Tentado | BB | 16 | 27,15 | 0,59 | 0,0150 | sim |
| CANUDOS DO VALE | Lesão Corporal | BB | 1 | 23,34 | 0,04 | < 0,0001 | sim |
| LINHA NOVA | Lesão Corporal | BB | 7 | 23,59 | 0,30 | < 0,0001 | sim |
| BOA VISTA DO SUL | Lesão Corporal | BB | 13 | 38,47 | 0,34 | < 0,0001 | sim |
| SALVADOR DAS MISSOES | Lesão Corporal | BB | 7 | 38,99 | 0,18 | < 0,0001 | sim |
| PRESIDENTE LUCENA | Lesão Corporal | BB | 7 | 41,68 | 0,17 | < 0,0001 | sim |
| SAO PEDRO DO BUTIA | Lesão Corporal | BB | 10 | 41,78 | 0,24 | < 0,0001 | sim |
| TUPANDI | Lesão Corporal | BB | 31 | 68,98 | 0,45 | < 0,0001 | sim |
| PICADA CAFE | Lesão Corporal | BB | 25 | 76,95 | 0,32 | < 0,0001 | sim |
| CAMPINA DAS MISSOES | Lesão Corporal | BB | 40 | 78,52 | 0,51 | < 0,0001 | sim |
| BOQUEIRAO DO LEAO | Lesão Corporal | BB | 33 | 96,02 | 0,34 | < 0,0001 | sim |
| SALVADOR DO SUL | Lesão Corporal | BB | 40 | 102,76 | 0,39 | < 0,0001 | sim |
