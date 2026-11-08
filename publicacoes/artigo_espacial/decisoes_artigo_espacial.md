# Artigo espacial — decisões fixadas

Arquivo de referência para quem trabalhar neste artigo, humano ou agente. Decisões já
tomadas: **não reabrir sem motivo novo**. Cada uma traz a razão, para que o motivo novo
possa ser reconhecido quando aparecer.

Última atualização: 2026-11-08 (figuras; limite de ilustrações; suplementares renumeradas).

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

- **Denominador: população feminina**, estimada como população total do ano × razão
  feminina do município no Censo 2022. Verificado: a razão é estável entre os Censos 2010 e
  2022 (mediana de variação 0,32 p.p.; 1% dos municípios acima de 2 p.p.; nenhum deles
  significativo no LISA). A troca para o denominador feminino muda o Moran global em no
  máximo 0,014 e, nos quatro desfechos somados, altera o status de significância de 3
  municípios, no máximo 1 por desfecho, e o quadrante de 1. **Declarar no texto que a
  população feminina anual é estimada, não medida.**
  - O **portal usa população total**. A diferença é imaterial e vai para **tabela
    suplementar** (a Tabela suplementar 2), com os dois denominadores lado a lado. A RESS
    permite duas suplementares e elas não contam no limite de palavras.
  - **Porto Alegre em Estupro passa de AA para BA** com o denominador feminino, por ter a
    maior razão feminina do estado (0,540). Único caso em que a classificação muda. Merece
    uma frase: a capital não é aglomerado robusto nesse desfecho sob nenhum dos dois
    denominadores.
- **Autocorrelação:** Moran global e local com ajuste de Assunção e Reis (1999), pesos de
  contiguidade queen padronizados por linha.
- **Permutações: 99.999. Semente: 12345.** Não usar 999: com 497 áreas e FDR a 5%, o piso
  do p (`1/(m+1)`) exige 10 municípios no piso simultaneamente para que algo seja rejeitado.
  Em Feminicídio Tentado isso dá zero significativos em 20 de 20 sementes.
- **Multiplicidade: Benjamini-Hochberg a 5% sobre o p direcional do esda**, que é a
  convenção do GeoDa e da literatura. O FDR sobre o dobro do p entra como **análise de
  sensibilidade**, nunca como critério principal. **Correção de 02/11:** não cabe seção
  própria no orçamento de 3.500 palavras; vira duas ou três frases nos Resultados.
- **Declarar a semente publicada:** 12345 dá o mínimo das vinte em Ameaça e Estupro pelo
  critério de sensibilidade.

## Critério de interpretação

- **Esperado ≥ 5 eventos**, calculado como mulheres-ano × taxa estadual do desfecho / 100
  mil. Pares abaixo disso **permanecem no cálculo** — excluí-los mudaria a matriz de pesos
  e portanto os resultados — mas **não entram na interpretação substantiva**. Caem 5 dos 67
  pares.
- **Não exigir Poisson p < 0,05 junto.** São perguntas diferentes: esperado ≥ 5 é
  suficiência de dado; o Poisson contra a taxa estadual pergunta se o município é incomum
  *para o estado*, enquanto o LISA pergunta se é incomum *em relação aos vizinhos*. Exigir
  os dois conflunde as perguntas e tiraria 4 municípios do bloco norte sem boa razão.
- **Reportar a razão observado/esperado ao lado de cada município significativo**, para que
  o leitor veja sozinho se um aglomerado é alto em termos absolutos ou só relativamente.
- O critério **não é contagem observada**. "Dez eventos observados", considerado antes, é o
  instrumento errado: Canudos do Vale tem 1 evento observado contra 21,77 esperados e é o
  achado mais forte; Vale Verde tem 0 contra 0,64 esperados e não é nada.

## Linguagem obrigatória

- **Não escrever "aglomerado de alta incidência".** O `Moran_Local_Rate` centra os valores
  padronizados na média municipal, que é negativa nos quatro desfechos porque a taxa
  estadual é ponderada por população e puxada pelas cidades. "Alto" no LISA significa
  **acima da média dos municípios, não acima da taxa estadual**. Quatro pares em quadrante
  alto têm observado abaixo do esperado estadual, entre eles Capivari do Sul em Lesão
  Corporal (0,77). Usar "valores relativamente altos", com a referência explicitada.
- **Não descrever os quatro BB da sobreposição como "da Serra".** Estão em quatro COREDEs
  distintos — Serra, Vale do Caí, Hortênsias e Paranhana Encosta da Serra — e apenas três
  são contíguos. "Litoral Norte" também não é categoria dos dados: usar COREDE Litoral.
- **Ressalva obrigatória no bloco norte:** vizinhos compartilham vizinhos no cálculo do I
  local, portanto parte da contiguidade é esperada por construção e não é evidência
  independente de extensão.
- **Porto Alegre em Estupro** é significativa como BA com observado em 0,94 do esperado e
  p = 0,0006. A significância vem do tamanho da população, não da magnitude do desvio. Não
  apresentar como achado substantivo; reportar a razão observado/esperado e registrar na
  discussão que o teste local é subdimensionado nos municípios pequenos e
  superdimensionado na capital.

## Estrutura de achados

| Posição | Achado |
|---|---|
| Principal | Bloco contíguo de 21 municípios AA no norte — COREDEs Médio Alto Uruguai, Celeiro, Rio da Várzea |
| Secundário | Sobreposição seletiva Lesão Corporal + Estupro em AA no COREDE Litoral, acima do acaso |
| Validade de medida | Déficits acentuados: Canudos do Vale (1 contra 21,77), Mariana Pimentel (0 contra 6,15), Dr. Maurício Cardoso (2 contra 7,33) |
| Nulo reportado | Feminicídio Consumado sem estrutura espacial: Moran ajustado 0,0122, p = 0,29 |
| Métodos | As permutações como justificativa dos parâmetros |

**Sobre a sobreposição:** não escrever que "não há sobreposição". Sob independência, o
esperado para três desfechos é 0,056 município, então observar zero não informa nada. A
coincidência Lesão Corporal + Estupro em AA tem 3 observados contra 0,05 esperados sob
independência, cerca de 60 vezes. O esperado é calculado dentro do quadrante: municípios AA
em Lesão Corporal × municípios AA em Estupro / 497 (5 × 5 / 497). O achado é a **seletividade**,
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
- FISCHER; BARRY; RAMDAS, arXiv:2404.15586 — o limite inferior de permutações sob correção de
  multiplicidade. **Citar, não reivindicar:** a desigualdade não é contribuição nossa.
- ARBIA; CARDILE; NARDELLI; SALVINI, arXiv:2610.13472 — correção de multiplicidade para
  LISA ajustada por dependência espacial, de outubro de 2026.

## Descartado, com motivo

- **Circularidade** (suavizar e então testar): sem alvo no corpus. 1 de 8 trabalhos, e só no
  Moran global.
- **A desigualdade como contribuição teórica:** já publicada.
- **Viés por quadrante** (outliers penalizados frente a agrupamentos): refutado. Comparados
  a agrupamentos de p próximo, os outliers retêm igual. O piso age sobre o tamanho do p.
- **Rede de atendimento como teste de validade:** sem poder discriminante, ver acima.


## Periódico e orçamento — fixados em 2026-11-02

**Epidemiologia e Serviços de Saúde (RESS)**, artigo original. Verificado empiricamente em
três artigos publicados do v. 35 (2026): o limite de 3.500 palavras vale **só para o corpo
do texto**. Resumo (196–251), referências (902–993) e tabelas — tanto o conteúdo
(582–1.253) quanto os títulos e legendas (135–167) — ficam de fora. Artigos publicados têm 2.894 a 3.571 palavras de prosa, mediana
2.928.

Evidência adicional a favor da RESS e contra *Cadernos de Saúde Pública*: a CSP recusou de
bancada, em quatro dias e sem avaliação por pares, o `CLIMAPAMPA-A01` — artigo descritivo de
epidemiologia municipal do mesmo projeto.

**Orçamento de palavras:** introdução 450, métodos 730, resultados 950, discussão 950,
conclusão 150. Total 3.230.

**Cinco figuras/tabelas, e o que não cabe:** o limite está **atingido** — ver «Figuras e
limite de ilustrações», abaixo. O painel do MAUP fica fora. Todo detalhe por
município vai para tabela, que não conta palavras. O parágrafo sobre o levantamento
exploratório dos oito trabalhos é o primeiro a cair se faltar espaço.

**Registro:** a entrada deste artigo no repositório `publicacoes` é `CLIMAPAMPA-A09`, promovida em
2026-11-03 da ideia `CLIMAPAMPA-I01`. A metade temporal daquela ideia se desmembra em ideia própria.

## Idioma e tradução — fixado em 2026-11-03

**Sem título, resumo ou texto em inglês na submissão. Não reabrir como pendência.** As instruções da
RESS, lidas em 2026-11-03 em https://www.scielo.br/journal/ress/about/, dizem que «os manuscritos
devem ser submetidos em português». Dizem também que «os artigos são traduzidos gratuitamente para o
inglês e o resumo, para o espanhol». Na produção editorial, a etapa 3 após a aprovação é «tradução do
texto completo do manuscrito para o inglês e do resumo para espanhol». Quem traduz é a revista, sem
custo para os autores.

## Figuras e limite de ilustrações — fixado em 2026-11-08

**Figura 1 = variante A, geográfica com recortes.** Os dois recortes são os painéis principais:
o bloco norte, nos COREDEs Médio Alto Uruguai, Celeiro e Rio da Várzea (A), e o COREDE Litoral
(B). Eles mostram os dois achados principais (bloco contíguo do norte; sobreposição no Litoral)
numa escala em que cada município se distingue e é nomeado. Só os significativos têm nome (22
no norte, 5 no Litoral), com pelo menos 6 pt impressos na largura de 15,3 cm. O estado inteiro
fica num **localizador pequeno, pintado com as cores de direção e sem texto**. Pintado porque fora
dos recortes há 31 municípios significativos, entre eles os 24 baixo-baixo, que de outro modo
sairiam da figura. Gerada por `03_figuras/gerar_figura1_variantes.py`.

**Figura 2 = variante D, superfície contínua, no corpo.** Mostra, por desfecho, a taxa ajustada
padronizada de cada município — o valor cujo sinal define o quadrante do LISA —, com os
significativos contornados. Foi pensada como figura suplementar, mas a RESS admite «até duas
tabelas e figuras suplementares em arquivo único», e as duas vagas já são tabelas. Por isso foi
para o corpo.

**Variantes descartadas** (na escolha de 2026-11-08; código e saídas apagados). A decisão entre as
cinco versões (a Figura 1 anterior e as variantes A a D) foi tomada **olhando a folha de
comparação**, com as cinco lado a lado, e não por propriedades declaradas.

- **B — cartograma contínuo** (área proporcional à população feminina). Descartada porque a
  mancha de maior área da figura corresponde a um outlier espacial de município populoso, e ela
  domina visualmente a imagem. A discussão do artigo afirma que esse caso não é substantivo — a
  significância decorre do tamanho da população, não da magnitude do desvio. Uma figura que
  destaca justamente o que o texto manda relativizar trabalha contra o argumento. As demais
  objeções (área não geográfica, ausência de escala de distância, dependência GPL-3.0, erro
  médio de área de cerca de 8%) são reais, mas secundárias: a razão é de leitura, não de
  técnica.
- **C — símbolos nos centroides.** Descartada por não nomear os municípios. Os achados do artigo
  são sobre lugares nomeados — os 22 significativos do norte (o bloco de 21 alto-alto e
  Sarandi), os três da sobreposição no Litoral, os três déficits de registro — e o leitor
  precisa conseguir cruzar a figura com as tabelas. Sem nome, vê a cor e não chega ao caso. A
  perda de extensão e contiguidade é consequência do símbolo pontual e pesou menos na decisão.
  - **Lacuna registrada em 2026-11-08:** os três déficits de registro — Canudos do Vale (Vale
    do Taquari), Mariana Pimentel (Centro-Sul) e Doutor Maurício Cardoso (Fronteira Noroeste) —
    ficam fora dos dois recortes da Figura 1. Lá aparecem só coloridos no localizador, sem nome,
    e só são nomeados na Tabela suplementar 1. Pendente: decidir se a figura deve nomeá-los.

**O corpo está no limite de cinco ilustrações:** Tabelas 1, 2 e 3 e Figuras 1 e 2. As duas
suplementares também estão no limite: a Tabela suplementar 1 (pares significativos) e a Tabela
suplementar 2 (denominador). **Qualquer tabela ou figura nova exige tirar outra**, no corpo ou
nas suplementares. As suplementares são numeradas pela ordem de citação no texto.
