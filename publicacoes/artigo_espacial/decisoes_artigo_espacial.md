# Artigo espacial — decisões fixadas

Arquivo de referência para quem trabalhar neste artigo, humano ou agente. Decisões já
tomadas: **não reabrir sem motivo novo**. Cada uma traz a razão, para que o motivo novo
possa ser reconhecido quando aparecer.

Última atualização: 2026-11-02.

## Escopo e destino

- **Este é o artigo substantivo**, não a nota metodológica. Descreve a distribuição
  espacial de quatro formas de violência contra a mulher nos 497 municípios do RS,
  2018–2025.
- **Periódico: *Epidemiologia e Serviços de Saúde*.** O leitor faz análise espacial em
  serviço de saúde; o prazo é de meses, não anos.
- O achado sobre permutações entra **na seção de métodos deste artigo**, como justificativa
  dos parâmetros. O argumento metodológico completo vai para a revisão sistemática, que é
  trabalho separado.
- **Sem modelo de fatores associados.** É o movimento padrão do gênero, concentra
  confundidores e transformaria um artigo focado em mais um artigo mediano.

## Parâmetros da análise

- **Autocorrelação:** Moran global e local com ajuste de Assunção e Reis (1999), pesos de
  contiguidade queen padronizados por linha.
- **Permutações: 99.999. Semente: 12345.** Não usar 999: com 497 áreas e FDR a 5%, o piso
  do p (`1/(m+1)`) exige 10 municípios no piso simultaneamente para que algo seja rejeitado.
  Em Feminicídio Tentado isso dá zero significativos em 20 de 20 sementes.
- **Multiplicidade: Benjamini-Hochberg a 5% sobre o p direcional do esda**, que é a
  convenção do GeoDa e da literatura. O FDR sobre o dobro do p entra como **análise de
  sensibilidade em seção própria**, nunca como critério principal.
- **Declarar a semente publicada:** 12345 dá o mínimo das vinte em Ameaça e Estupro pelo
  critério de sensibilidade.

## Critério de interpretação

- **Esperado ≥ 5 eventos**, calculado como pessoas-ano × taxa estadual do desfecho / 100
  mil. Pares abaixo disso **permanecem no cálculo** — excluí-los mudaria a matriz de pesos
  e portanto os resultados — mas **não entram na interpretação substantiva**. Caem 6 dos 68
  pares.
- **Não exigir Poisson p < 0,05 junto.** São perguntas diferentes: esperado ≥ 5 é
  suficiência de dado; o Poisson contra a taxa estadual pergunta se o município é incomum
  *para o estado*, enquanto o LISA pergunta se é incomum *em relação aos vizinhos*. Exigir
  os dois conflunde as perguntas e tiraria 4 municípios do bloco norte sem boa razão.
- **Reportar a razão observado/esperado ao lado de cada município significativo**, para que
  o leitor veja sozinho se um aglomerado é alto em termos absolutos ou só relativamente.
- O critério **não é contagem observada**. "Dez eventos observados", considerado antes, é o
  instrumento errado: Canudos do Vale tem 1 evento observado contra 23,24 esperados e é o
  achado mais forte; Vale Verde tem 0 contra 0,64 esperados e não é nada.

## Linguagem obrigatória

- **Não escrever "aglomerado de alta incidência".** O `Moran_Local_Rate` centra os valores
  padronizados na média municipal, que é negativa nos quatro desfechos porque a taxa
  estadual é ponderada por população e puxada pelas cidades. "Alto" no LISA significa
  **acima da média dos municípios, não acima da taxa estadual**. Seis pares em quadrante
  alto têm observado abaixo do esperado estadual, entre eles Porto Alegre em Estupro (0,98)
  e Capivari do Sul em Lesão Corporal (0,75). Usar "valores relativamente altos", com a
  referência explicitada.
- **Não descrever os quatro BB da sobreposição como "da Serra".** Estão em quatro COREDEs
  distintos — Serra, Vale do Caí, Hortênsias e Paranhana Encosta da Serra — e apenas três
  são contíguos. "Litoral Norte" também não é categoria dos dados: usar COREDE Litoral.
- **Ressalva obrigatória no bloco norte:** vizinhos compartilham vizinhos no cálculo do I
  local, portanto parte da contiguidade é esperada por construção e não é evidência
  independente de extensão.

## Estrutura de achados

| Posição | Achado |
|---|---|
| Principal | Bloco contíguo de 21 municípios AA no norte — COREDEs Médio Alto Uruguai, Celeiro, Rio da Várzea |
| Secundário | Sobreposição seletiva Lesão Corporal + Estupro em AA no COREDE Litoral, acima do acaso |
| Validade de medida | Déficits acentuados: Canudos do Vale (1 contra 23,24), Mariana Pimentel (0 contra 6,54), Dr. Maurício Cardoso (2 contra 7,54) |
| Nulo reportado | Feminicídio Consumado sem estrutura espacial: Moran ajustado 0,0114, p = 0,31 |
| Métodos | As permutações como justificativa dos parâmetros |

**Sobre a sobreposição:** não escrever que "não há sobreposição". Sob independência, o
esperado para três desfechos é 0,03 município, então observar zero não informa nada. As
sobreposições que ocorrem estão 5 a 6 vezes acima do acaso. O achado é a **seletividade**,
não a ausência.

## Rede de atendimento — encerrado

A comparação de cobertura **não discrimina e não entra como teste**. De 306 municípios
gaúchos abaixo de 7.500 habitantes, só 1 declara delegacia da mulher. A ausência de serviço
nos municípios de poucos eventos é o que o porte já prevê.

- **Censo SUAS: não insistir.** O portal do MDS estava em manutenção em 02/11. O CREAS
  usado é o autodeclarado da MUNIC, e isso fica declarado como limitação.
- Os dados levantados podem aparecer como caracterização descritiva, nunca como evidência
  de que a falta de serviço explica o sub-registro.

## Fonte de números

**`outputs/tables/resultados_consolidados.md` é a fonte única.** Nenhum número do artigo sai
de memória, nem da minha, nem de quem escrever. Isso não é formalidade: valores de Moran
foram citados errado de memória três vezes durante o desenvolvimento.

## Referências metodológicas a citar

- ASSUNÇÃO; REIS (1999) — o ajuste.
- ANSELIN (1995) — LISA.
- FISCHER; RAMDAS, arXiv:2404.15586 — o limite inferior de permutações sob correção de
  multiplicidade. **Citar, não reivindicar:** a desigualdade não é contribuição nossa.
- KNIJNENBURG et al., Bioinformatics 25(12), 2009 — limite de resolução do p por permutação.
- ARBIA; CARDILE; NARDELLI; SALVINI, arXiv:2610.13472 — correção de multiplicidade para
  LISA ajustada por dependência espacial, de outubro de 2026.

## Descartado, com motivo

- **Circularidade** (suavizar e então testar): sem alvo no corpus. 1 de 8 trabalhos, e só no
  Moran global.
- **A desigualdade como contribuição teórica:** já publicada.
- **Viés por quadrante** (outliers penalizados frente a agrupamentos): refutado. Comparados
  a agrupamentos de p próximo, os outliers retêm igual. O piso age sobre o tamanho do p.
- **Rede de atendimento como teste de validade:** sem poder discriminante, ver acima.
