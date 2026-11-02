# Esperado sob a taxa estadual frente ao observado, nos pares significativos do LISA

**Denominador:** população feminina anual ESTIMADA, não medida: população total do ano × razão feminina do município no Censo 2022 (razão suposta constante em 2018-2025).

São os 67 pares município-desfecho significativos no LISA de Assunção e Reis, 2018-2025 (semente 12345, 99.999 permutações, FDR sobre o p direcional). Gerada por `src/analysis/esperado_vs_observado_lisa.py`.

- **Esperado** = mulheres-ano do município em 2018-2025 × taxa estadual / 100 mil. As mulheres-ano são a soma das oito populações anuais, o mesmo denominador do LISA, e equivalem a "população × 8 anos". Como verificação, há também uma coluna com a população feminina estimada de 2025 × 8.
- **Taxa estadual por 100 mil mulheres-ano**, soma dos 497 municípios, sem "NÃO INFORMADO": Ameaça 579,91; Estupro 40,23; Feminicídio Consumado 1,59; Feminicídio Tentado 4,91; Lesão Corporal 333,15.
- **Poisson na direção do quadrante:** P(X ≥ obs) em AA e AB; P(X ≤ obs) em BB e BA. É descritivo: não corrige para múltiplas comparações e ignora a vizinhança, que é o que o LISA mede.

## Por quadrante

| Quadrante | Pares | Esperado < 5 | Sobrevivem (esperado ≥ 5) | Esperado < 5, pop. 2025 × 8 | Poisson p < 0,05 | Esperado ≥ 5 e Poisson p < 0,05 |
| --- | --- | --- | --- | --- | --- | --- |
| AA | 32 | 1 | 31 | 1 | 22 | 22 |
| AB | 4 | 1 | 3 | 1 | 0 | 0 |
| BA | 3 | 0 | 3 | 0 | 3 | 3 |
| BB | 28 | 3 | 25 | 3 | 21 | 21 |
| Total | 67 | 5 | 62 | 5 | 46 | 46 |

## Por desfecho

| Desfecho | Pares | Esperado < 5 | Sobrevivem (esperado ≥ 5) | Esperado < 5, pop. 2025 × 8 | Poisson p < 0,05 | Esperado ≥ 5 e Poisson p < 0,05 |
| --- | --- | --- | --- | --- | --- | --- |
| Ameaça | 31 | 0 | 31 | 0 | 26 | 26 |
| Estupro | 15 | 1 | 14 | 1 | 6 | 6 |
| Feminicídio Tentado | 6 | 4 | 2 | 4 | 1 | 1 |
| Lesão Corporal | 15 | 0 | 15 | 0 | 13 | 13 |
| Total | 67 | 5 | 62 | 5 | 46 | 46 |

## Bloco norte em AA (21 municípios contíguos)

- **21 dos 21 municípios sobrevivem** ao critério de esperado ≥ 5, com ao menos um par acima do limiar. Em 20 deles, todos os pares estão acima.
- O bloco tem 23 pares. 1 ficam abaixo do limiar: ALPESTRE (Feminicídio Tentado, esperado 1,29).
- Com esperado ≥ 5 e também Poisson p < 0,05, sobrevivem 17 dos 21.

## Pares com o observado do lado oposto ao do quadrante

4 pares estão num quadrante "alto" (AA ou AB) com o observado abaixo do esperado estadual. Nenhum está num quadrante "baixo" com o observado acima. Isso não é erro de cálculo. `esda.Moran_Local_Rate` padroniza as taxas pelo método de Assunção e Reis em torno da taxa estadual, mas o LISA centra esses valores na média deles. Essa média é negativa nos quatro desfechos, porque a maioria dos municípios, pequenos, fica abaixo da taxa estadual. Assim, "alto" no LISA quer dizer acima da média dos municípios, não acima da taxa estadual. Nesses pares, P(X ≥ obs) fica acima de 0,5 por construção.

| Município | Desfecho | Quadrante | Observado | Esperado | Obs./esp. | Poisson, direção do quadrante | Esperado ≥ 5 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VISTA GAUCHA | Ameaça | AA | 63 | 65,63 | 0,96 | 0,6438 | sim |
| CAPIVARI DO SUL | Lesão Corporal | AA | 45 | 58,56 | 0,77 | 0,9711 | sim |
| SARANDI | Ameaça | AB | 553 | 570,91 | 0,97 | 0,7787 | sim |
| BENTO GONCALVES | Estupro | AB | 200 | 204,98 | 0,98 | 0,6452 | sim |

## Os 67 pares

| Município | Desfecho | Quadrante | Observado | Esperado | Obs./esp. | Poisson, direção do quadrante | Esperado ≥ 5 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BOA VISTA DAS MISSOES | Ameaça | AA | 78 | 47,73 | 1,63 | < 0,0001 | sim |
| DOIS IRMAOS DAS MISSOES | Ameaça | AA | 50 | 47,86 | 1,04 | 0,3974 | sim |
| BOM PROGRESSO | Ameaça | AA | 61 | 48,16 | 1,27 | 0,0416 | sim |
| DERRUBADAS | Ameaça | AA | 95 | 63,93 | 1,49 | 0,0002 | sim |
| VISTA GAUCHA | Ameaça | AA | 63 | 65,63 | 0,96 | 0,6438 | sim |
| CRISTAL DO SUL | Ameaça | AA | 83 | 65,86 | 1,26 | 0,0232 | sim |
| TAQUARUCU DO SUL | Ameaça | AA | 73 | 71,77 | 1,02 | 0,4580 | sim |
| BRAGA | Ameaça | AA | 109 | 76,78 | 1,42 | 0,0003 | sim |
| VICENTE DUTRA | Ameaça | AA | 213 | 106,34 | 2,00 | < 0,0001 | sim |
| MIRAGUAI | Ameaça | AA | 220 | 109,08 | 2,02 | < 0,0001 | sim |
| RODEIO BONITO | Ameaça | AA | 184 | 147,39 | 1,25 | 0,0020 | sim |
| ALPESTRE | Ameaça | AA | 205 | 152,41 | 1,35 | < 0,0001 | sim |
| ERVAL SECO | Ameaça | AA | 228 | 157,17 | 1,45 | < 0,0001 | sim |
| CORONEL BICACO | Ameaça | AA | 201 | 157,60 | 1,28 | 0,0005 | sim |
| IRAI | Ameaça | AA | 412 | 171,17 | 2,41 | < 0,0001 | sim |
| AMETISTA DO SUL | Ameaça | AA | 334 | 175,47 | 1,90 | < 0,0001 | sim |
| PLANALTO | Ameaça | AA | 382 | 242,40 | 1,58 | < 0,0001 | sim |
| REDENTORA | Ameaça | AA | 259 | 245,78 | 1,05 | 0,2076 | sim |
| TENENTE PORTELA | Ameaça | AA | 574 | 336,58 | 1,71 | < 0,0001 | sim |
| TRES PASSOS | Ameaça | AA | 997 | 590,91 | 1,69 | < 0,0001 | sim |
| FREDERICO WESTPHALEN | Ameaça | AA | 1133 | 768,46 | 1,47 | < 0,0001 | sim |
| CAPIVARI DO SUL | Estupro | AA | 12 | 7,07 | 1,70 | 0,0567 | sim |
| SENTINELA DO SUL | Estupro | AA | 15 | 8,47 | 1,77 | 0,0266 | sim |
| BALNEARIO PINHAL | Estupro | AA | 31 | 24,62 | 1,26 | 0,1201 | sim |
| OSORIO | Estupro | AA | 93 | 78,06 | 1,19 | 0,0542 | sim |
| TRAMANDAI | Estupro | AA | 148 | 90,39 | 1,64 | < 0,0001 | sim |
| ALPESTRE | Feminicídio Tentado | AA | 2 | 1,29 | 1,55 | 0,3699 | não |
| BRAGA | Lesão Corporal | AA | 52 | 44,11 | 1,18 | 0,1339 | sim |
| CAPIVARI DO SUL | Lesão Corporal | AA | 45 | 58,56 | 0,77 | 0,9711 | sim |
| CIDREIRA | Lesão Corporal | AA | 487 | 234,59 | 2,08 | < 0,0001 | sim |
| OSORIO | Lesão Corporal | AA | 704 | 646,42 | 1,09 | 0,0132 | sim |
| TRAMANDAI | Lesão Corporal | AA | 1366 | 748,45 | 1,83 | < 0,0001 | sim |
| SARANDI | Ameaça | AB | 553 | 570,91 | 0,97 | 0,7787 | sim |
| BENTO GONCALVES | Estupro | AB | 200 | 204,98 | 0,98 | 0,6452 | sim |
| SANTA MARIA DO HERVAL | Feminicídio Tentado | AB | 3 | 1,22 | 2,45 | 0,1259 | não |
| CANDELARIA | Feminicídio Tentado | AB | 10 | 6,10 | 1,64 | 0,0908 | sim |
| NOVA RAMADA | Ameaça | BA | 27 | 49,50 | 0,55 | 0,0003 | sim |
| MARIANA PIMENTEL | Estupro | BA | 0 | 6,15 | 0,00 | 0,0021 | sim |
| PORTO ALEGRE | Estupro | BA | 2319 | 2.479,44 | 0,94 | 0,0006 | sim |
| CORONEL PILAR | Ameaça | BB | 3 | 36,47 | 0,08 | < 0,0001 | sim |
| LINHA NOVA | Ameaça | BB | 13 | 39,53 | 0,33 | < 0,0001 | sim |
| BOA VISTA DO SUL | Ameaça | BB | 16 | 62,76 | 0,25 | < 0,0001 | sim |
| PRESIDENTE LUCENA | Ameaça | BB | 22 | 67,85 | 0,32 | < 0,0001 | sim |
| COTIPORA | Ameaça | BB | 64 | 87,88 | 0,73 | 0,0047 | sim |
| PICADA CAFE | Ameaça | BB | 55 | 132,13 | 0,42 | < 0,0001 | sim |
| NOVA PETROPOLIS | Ameaça | BB | 336 | 538,04 | 0,62 | < 0,0001 | sim |
| GARIBALDI | Ameaça | BB | 482 | 830,88 | 0,58 | < 0,0001 | sim |
| SANTO EXPEDITO DO SUL | Estupro | BB | 1 | 3,79 | 0,26 | 0,1082 | não |
| DR MAURICIO CARDOSO | Estupro | BB | 2 | 7,33 | 0,27 | 0,0230 | sim |
| CACIQUE DOBLE | Estupro | BB | 6 | 7,88 | 0,76 | 0,3277 | sim |
| TUCUNDUVA | Estupro | BB | 8 | 9,44 | 0,85 | 0,3991 | sim |
| ALECRIM | Estupro | BB | 7 | 9,61 | 0,73 | 0,2572 | sim |
| FARROUPILHA | Estupro | BB | 65 | 119,57 | 0,54 | < 0,0001 | sim |
| SANTA ROSA | Estupro | BB | 109 | 125,49 | 0,87 | 0,0743 | sim |
| VALE VERDE | Feminicídio Tentado | BB | 0 | 0,65 | 0,00 | 0,5246 | não |
| PASSO DO SOBRADO | Feminicídio Tentado | BB | 0 | 1,27 | 0,00 | 0,2810 | não |
| SANTA CRUZ DO SUL | Feminicídio Tentado | BB | 16 | 27,49 | 0,58 | 0,0128 | sim |
| CANUDOS DO VALE | Lesão Corporal | BB | 1 | 21,77 | 0,05 | < 0,0001 | sim |
| LINHA NOVA | Lesão Corporal | BB | 7 | 22,71 | 0,31 | 0,0001 | sim |
| BOA VISTA DO SUL | Lesão Corporal | BB | 13 | 36,06 | 0,36 | < 0,0001 | sim |
| SALVADOR DAS MISSOES | Lesão Corporal | BB | 7 | 37,24 | 0,19 | < 0,0001 | sim |
| PRESIDENTE LUCENA | Lesão Corporal | BB | 7 | 38,98 | 0,18 | < 0,0001 | sim |
| SAO PEDRO DO BUTIA | Lesão Corporal | BB | 10 | 39,49 | 0,25 | < 0,0001 | sim |
| TUPANDI | Lesão Corporal | BB | 31 | 65,64 | 0,47 | < 0,0001 | sim |
| PICADA CAFE | Lesão Corporal | BB | 25 | 75,91 | 0,33 | < 0,0001 | sim |
| CAMPINA DAS MISSOES | Lesão Corporal | BB | 40 | 76,79 | 0,52 | < 0,0001 | sim |
| SALVADOR DO SUL | Lesão Corporal | BB | 40 | 99,91 | 0,40 | < 0,0001 | sim |
