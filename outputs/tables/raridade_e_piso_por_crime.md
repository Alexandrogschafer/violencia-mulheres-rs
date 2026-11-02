# Raridade do desfecho e piso de p, por crime

**Denominador:** população feminina anual ESTIMADA, não medida: população total do ano × razão feminina do município no Censo 2022 (razão suposta constante em 2018-2025).

Quatro crimes com LISA, 497 municípios, 2018-2025. Linhas da menor para a maior raridade,
pela contagem municipal mediana. Contagens no período inteiro; taxas por 100 mil mulheres-ano, com a população feminina
estimada como denominador. No piso significa p = 0,001 a 999 permutações e p = 0,00001 a 99.999. Significativo
significa sobreviver ao FDR de Benjamini-Hochberg com q = 0,05 sobre o `p_sim`.

| Crime | Eventos | Mediana municipal | Q1 municipal | Municípios com zero | Taxa média municipal | Taxa estadual | No piso a 999, mín./med./máx. | Sementes abaixo de 10 | Sementes sem significativos a 999 | No piso a 99.999, mín./med./máx. | Sementes sem significativos a 99.999 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ameaça | 269.917 | 116,0 | 50,0 | 0,0% | 527,4 | 579,9 | 12 / 17,5 / 26 | 0 | 0 | 0 / 2,0 / 3 | 0 |
| Lesão Corporal | 155.062 | 52,0 | 22,0 | 0,0% | 252,4 | 333,1 | 8 / 12,0 / 14 | 2 | 2 | 0 / 0,5 / 2 | 0 |
| Estupro | 18.726 | 8,0 | 4,0 | 4,6% | 37,3 | 40,2 | 5 / 11,5 / 16 | 7 | 7 | 0 / 0,0 / 1 | 0 |
| Feminicídio Tentado | 2.286 | 1,0 | 0,0 | 42,3% | 3,9 | 4,9 | 2 / 6,0 / 9 | 20 | 20 | 0 / 0,0 / 0 | 0 |

## Limiar

- A 999 permutações, o FDR só aceita p = 0,001 com pelo menos **10** municípios no piso
  (0,05 × 10/497 = 0,001006; com 9, 0,000905).
- A 99.999 permutações, o limiar para p = 0,00001 é **1**: 0,05 × 1/497 = 0,000101, cerca de dez vezes o piso.

## Confronto a 999 permutações

- Combinações crime-semente abaixo do limiar: 29. Com algum significativo: 0.
- Combinações crime-semente no limiar ou acima: 51. Sem nenhum significativo: 0.

## Confronto a 99.999 permutações

- Combinações crime-semente sem nenhum município no piso: 51 de 80. Mesmo nelas, o número de
  significativos vai de 5 a 32.
- Nenhuma combinação fica sem significativos: o FDR não precisa que algum município atinja o piso.
