# Estado metodológico da literatura de análise espacial

Classificação de oito trabalhos em cinco eixos: tratamento da taxa, permutações e semente, multiplicidade, reporte e fonte da justificativa.

## Como ler

- **Declarado:** o texto diz.
- **Ambíguo:** o texto trata do ponto, mas admite mais de uma leitura.
- **Omisso:** o texto não trata do ponto. Omisso é resultado e não tem passagem a transcrever. Foi confirmado por leitura dos métodos e resultados e por busca no texto integral de cada PDF.
- **Páginas:** indicam a numeração impressa e, quando ela difere, a página do arquivo (PDF). Bahia et al. e Veiga e Bushatsky são citados pela página do arquivo, a única visível no PDF.
- **Citações:** são literais e foram conferidas por programa contra o texto da página indicada, desconsiderando quebras de linha e hifens. Números colados ao fim de palavras são chamadas de referência do original.
- **Figuras:** a legenda da Figura 3 de Ceccon, Alves e Leite é imagem e foi lida na página renderizada. Nas demais figuras, valeram apenas o texto extraível e as legendas.

## Bahia et al. (2025)

Arquivo: `bahia_2025_feminicidios-minas-gerais.pdf`

BAHIA, Camila Alves; PINTO, Isabella Vitral; TRINDADE, Carla Machado da; SILVA, Camila Mattarelli de Abreu e; HABKOUK, Patricia; SIMÕES, Taynãna César; CÂMARA, Daniel Cardoso Portela; BEVILACQUA, Paula Dias. Feminicídios em Minas Gerais, Brasil: da caracterização dos eventos à análise espaço-temporal. **Cadernos de Saúde Pública**, Rio de Janeiro, v. 41, n. 1, e00015224, 2025. DOI: https://doi.org/10.1590/0102-311XPT015224.

A unidade de análise é a microrregião de saúde, não o município.

### Tratamento da taxa

- **Taxa bruta no mapa: declarado.**

> «mapearam-se as taxas observadas no período segundo microrregião de saúde» (PDF 3)

- **Suavização bayesiana empírica e ajuste tipo Assunção-Reis: omisso.** A única suavização mencionada é a das curvas temporais do GAM, que não é tratamento espacial da taxa:

> «As Figuras 1b e 1c são as curvas suavizadas geradas pelos modelos GAM para o risco de ocorrência de feminicídio e homicídio de mulheres.» (PDF 8)

- **Taxa usada no LISA: ambíguo.** O texto diz "taxas" sem qualificar se são as observadas. Não há registro de Moran ou LISA sobre taxa suavizada.

> «O mapeamento dos quadrantes resultantes da classificação do Índice Local de Moran Bivariado se apresentou estatisticamente significativo entre as duas taxas em 21 microrregiões (Figura 5).» (PDF 8)

### Permutações e semente

- **Moran local: omisso.**
- **Varredura espacial: declarado, 999 simulações.** O número pertence à varredura de Kulldorff, não ao Moran.

> «Utilizou-se 1 a 3 anos como janela temporal e 999 simulações do método Monte Carlo com um valor de significância igual a 5%» (PDF 4)

- **Semente: omisso.**

### Multiplicidade

- **Moran local: omisso.**
- **Varredura: ambíguo.** O texto diz que a estatística permite corrigir testes múltiplos, mas não diz que a correção foi aplicada nem como.

> «Utilizou-se a estatística de varredura proposta por Kulldorff 26, a qual permite: detectar clusters espaço-temporais utilizando a distribuição de probabilidade de Poisson discreta; testar significância estatística e corrigir testes múltiplos» (PDF 4)

### Reporte

**Declarado: mapa, contagem e nomes de parte das microrregiões, sem p individual.**

> «No sul do estado, concentraram-se as microrregiões com altas taxas de feminicídio e baixas taxas de homicídio de mulheres (Pouso Alegre e Lavras)» (PDF 8)

### Fonte da justificativa

**Omisso.** Não há suavização bayesiana a justificar.

## Barros et al. (2021)

Arquivo: `barros_2021_homicidios-mulheres.pdf`

BARROS, Sheyla Carvalho de; OLIVEIRA, Conceição Maria de; SILVA, Amanda Priscila de Santana Cabral; MELO, Marcella Fernandes de Oliveira; PIMENTEL, Dayane da Rocha; BONFIM, Cristine Vieira do. Análise espacial dos homicídios intencionais de mulheres. **Revista da Escola de Enfermagem da USP**, São Paulo, v. 55, e03770, 2021. DOI: https://doi.org/10.1590/S1980-220X2020037303770.

### Tratamento da taxa

- **Bayesiano empírico local: declarado.**

> «As taxas médias de mortalidade foram ajustadas pelo método bayesiano empírico local, com o propósito de minimizar os efeitos das flutuações decorrentes do pequeno número de óbitos em alguma das unidades territoriais.» (p. 2)

- **Ajuste tipo Assunção-Reis: omisso.**
- **Taxa bruta e suavizada no mapa: declarado.**

> «Figura 1 – Taxa média bruta (A), taxa média estimada pelo método bayesiano empírico local (B)» (p. 5)

- **Registro explícito: suaviza e depois calcula Moran global sobre a taxa suavizada. Declarado.**

> «O índice de Moran global das taxas suavizadas foi de 0,6 (p = 0,01).» (p. 3)

- **LISA: ambíguo.** O texto diz "taxas de mortalidade" sem qualificar. A sequência dos resultados não define qual taxa alimentou o Moran Map.

> «Foram construídos o Box Map e o Moran Map das taxas de mortalidade.» (p. 2)

### Permutações e semente

**Omisso nos dois pontos.** O valor de p é informado sem o procedimento de pseudo-significância.

### Multiplicidade

**Omisso.** Consta apenas o limiar de significância:

> «no Moran Map, permanecem os clusters com significância (p-valor < 0,05)» (p. 3)

### Reporte

**Declarado: mapa e contagem por regional de saúde, sem p individual por município.**

> «Os clusters (áreas Q1) estão localizados nas RS: I (dois municípios), III (oito municípios), IV (oito municípios), XII (dois municípios) e VI (três municípios, sendo um conglomerado e um município isolado)» (p. 3)

### Fonte da justificativa

**Omisso.** O propósito da suavização é declarado, mas a passagem citada no primeiro eixo não traz referência.

## Carvalho et al. (2011)

Arquivo: `carvalho_2011_td1662-taxas-bayesianas.pdf`

CARVALHO, Alexandre Xavier Ywata de; SILVA, Gabriela Drummond Marques da; ALMEIDA JÚNIOR, Gilberto Rezende de; ALBUQUERQUE, Pedro Henrique de Melo. **Mapeamento de taxas bayesianas, com aplicação ao mapeamento de homicídios nos municípios brasileiros**. Rio de Janeiro: Ipea, set. 2011. (Texto para Discussão, n. 1662). ISSN 1415-4765.

Referência metodológica. Tem autoria e tema comuns ao artigo de 2012, mas a redação e a extensão diferem, por isso as entradas são separadas.

### Tratamento da taxa

- **Taxa bruta: declarado, como base de comparação e criticada.**

> «Quando os municípios são muito pequenos, por exemplo, a estimação de taxas brutas (TBs) é pouco indicada.» (p. 7; PDF 8)

- **Bayesiano empírico global: declarado.**

> «A Taxa Empírica Bayesiana de um município é então uma soma ponderada entre a sua TB e a taxa global da região em que o município está inserido.» (p. 15; PDF 16)

- **Bayesiano empírico espacial: declarado.**

> «um recurso possível é convergir os valores observados para uma média local, que será a taxa média dos vizinhos e do próprio município» (p. 16; PDF 17)

- **Ajuste tipo Assunção-Reis: omisso.**
- **Uso no mapa: declarado.**

> «os mapas 1 a 5 apresentam a distribuição de cada uma das taxas para os municípios brasileiros em 2008» (p. 26; PDF 27)

- **Uso em teste de autocorrelação: omisso.** O termo "Moran" não aparece no texto.

### Permutações e semente

**Omisso nos dois pontos.** A única menção a simulações, na p. 17 (PDF 18), trata de estimação, não de teste.

### Multiplicidade

**Omisso quanto à análise do próprio trabalho.** Há apenas uma menção à literatura, sem aplicação:

> «Catelan, Lagazio e Biggeri (2010), por exemplo, sugerem a utilização de uma abordagem bayesiana hierárquica para a execução de múltiplos testes com os dados de riscos de doenças em uma determinada área.» (p. 8; PDF 9)

### Reporte

**Omisso.** O trabalho não define pertinência a cluster.

### Fonte da justificativa

**Declarado.** Clayton e Kaldor (1987) e Marshall (1991).

> «Clayton e Kaldor (1987) solucionaram esse problema por meio de uma suavização bayesiana.» (p. 7; PDF 8)

> «A Taxa Bayesiana Empírica (proposta por MARSHALL, 1991)» (p. 14; PDF 15)

## Carvalho et al. (2012)

Arquivo: `carvalho_2012_taxas-bayesianas-homicidios.pdf`

CARVALHO, Alexandre Xavier Ywata de; SILVA, Gabriela Drummond Marques da; ALMEIDA JÚNIOR, Gilberto Rezende de; ALBUQUERQUE, Pedro Henrique Melo de. Taxas bayesianas para o mapeamento de homicídios nos municípios brasileiros. **Cadernos de Saúde Pública**, Rio de Janeiro, v. 28, n. 7, p. 1249-1262, jul. 2012.

Referência metodológica.

### Tratamento da taxa

- **Taxa bruta: declarado, como base de comparação.**

> «A forma mais usual de mapeamento de taxas utiliza a chamada taxa bruta» (p. 1250; PDF 2)

- **Bayesiano empírico global: declarado.**

> «Tal medida é também chamada taxa bayesiana empírica global.» (p. 1251; PDF 3)

- **Bayesiano empírico local ou espacial: declarado.**

> «Assim, tem-se a taxa bayesiana empírica espacial, ou taxa bayesiana empírica local, que mantém a mesma estrutura de soma ponderada, substituindo-se, no entanto, a média global pela média local.» (p. 1251; PDF 3)

- **Ajuste tipo Assunção-Reis: omisso.**
- **Uso no mapa: declarado.**

> «Taxas espacial, bayesiana empírica, bayesiana empírica espacial e bayesiana empírica Clayton & Kaldor de homicídios nos municípios brasileiros em 2008.» (p. 1258; PDF 10)

- **Uso em teste de autocorrelação: omisso.** O termo "Moran" não aparece no texto.

### Permutações e semente

**Omisso nos dois pontos.**

### Multiplicidade

**Omisso.** A única ocorrência de "multiple testing" está no título de um item da lista de referências (PDF 14).

### Reporte

**Omisso.** O trabalho não define pertinência a cluster.

### Fonte da justificativa

**Declarado.** Clayton e Kaldor (ref. 2), Marshall (ref. 3) e Kafadar (ref. 9).

> «Esse problema foi solucionado, primeiramente, por meio de técnicas de suavização Bayesiana 2.» (p. 1249; PDF 1)

> «A taxa bayesiana empírica 3 de um município é uma soma ponderada entre a sua taxa bruta e a taxa média global de todo o mapa.» (p. 1250; PDF 2)

> «Tal região é composta pelo próprio município e seus vizinhos 9.» (p. 1250; PDF 2)

## Ceccon, Alves e Leite (2025)

Arquivo: `ceccon_2025_violencia-espirito-santo.pdf`

CECCON, Tamires Paulo; ALVES, Micael Franco; LEITE, Franciele Marabotti Costa. Mapeamento espacial das notificações e prevalências de violência entre grupos etários vulneráveis no estado do Espírito Santo. **Revista Brasileira de Pesquisa em Saúde**, Vitória, v. 27, supl. 2, e48408, p. 33-46, 2025. DOI: https://doi.org/10.47456/rbps.v27isupl_2.48408.

O objeto é a violência notificada em todos os grupos etários, não especificamente contra a mulher.

### Tratamento da taxa

- **Suavização bayesiana: declarado.** Os métodos não dizem se é global ou local, mas os resultados dizem que é global.

> «foram calculadas as prevalências de notificação de violência por 10.000, taxa suavizada bayesiana que leva em consideração algumas informações especiais como a área de cada município» (p. 35; PDF 3)

> «A distribuição espacial por faixa etária das prevalências suavizadas de incidência por 10.000 de violência para os municípios do ES através do método empírico Bayesiano global» (p. 40; PDF 8)

- **Ajuste tipo Assunção-Reis: omisso.**
- **Taxa bruta e suavizada no mapa: declarado.**

> «FIGURA 1. Distribuição das prevalências de incidência por 10.000 de notificação de violência» (p. 40; PDF 8)

> «FIGURA 2. Distribuição das prevalências bayesianas empíricas por 10.000 de notificação de violência» (p. 40; PDF 8)

- **LISA: ambíguo.** O texto não diz se usou a taxa bruta ou a suavizada, logo não se pode afirmar que calculou LISA sobre o resultado suavizado. Os valores citados no trecho (Laranja da Terra, 27,34; Itarana, 21,40; Serra, 6,07) também não coincidem com as taxas brutas correspondentes da Tabela 1 (12,96; 55,90; 9,85).

> «O índice de Moran local (li) para verificar a dependência espacial, mostrando a correlação da taxa de violência por 10.000 habitantes entre os municípios como um todo nos anos de 2011 a 2021.» (p. 41; PDF 9)

### Permutações e semente

**Omisso nos dois pontos.**

### Multiplicidade

**Omisso.** Consta apenas o nível de significância:

> «O nível alfa de significância utilizado em todas as análises foi de 5%.» (p. 35; PDF 3)

### Reporte

**Declarado: mapa e menção a poucos municípios, sem p individual.**

> «Nas faixas de 10 a 19 anos o município de Itarana (21,40/10,000 hab) apresentou taxa alta, mas não apresentou correlação espacial significativa com os outros municípios de divisa.» (p. 41; PDF 9)

### Fonte da justificativa

**Omisso.**

## Moroskoski et al. (2025)

Arquivo: `moroskoski_2025_feminicidio-parana.pdf`

MOROSKOSKI, Márcia; AZEVEDO, Lays Silva de; BRITO, Franciele Aline Machado de; OLIVEIRA, Natan Nascimento de; PEREIRA, Natan David; CARREIRA, Lígia; MOURA, Débora Regina de Oliveira; OLIVEIRA, Rosana Rosseto de. Feminicídio: análise espacial e fatores associados aos crimes de gênero no Paraná, Brasil. **Ciência & Saúde Coletiva**, Rio de Janeiro, v. 30, n. 10, e10862025, 2025. DOI: https://doi.org/10.1590/1413-812320253010.10862025.

### Tratamento da taxa

- **Suavização: declarado que houve. Tipo: omisso.** O texto não diz como suavizou nem emprega a palavra "bayesiano".

> «A distribuição espacial das taxas suavizadas foi apresentada em intervalos, das taxas mínimas às máximas» (p. 3)

- **Ajuste tipo Assunção-Reis: omisso.**
- **Uso no mapa: declarado.**

> «Figura 2. Localização do estado do Paraná e distribuição espacial das taxas suavizadas das denúncias de feminicídio» (p. 5)

- **Moran ou LISA sobre a taxa: omisso.** O único Moran relatado é o dos resíduos da regressão:

> «um índice de Moran (autocorrelação espacial) dos resíduos de 0,002» (p. 5)

- **Regressões: omisso.** O texto não diz se usaram a taxa suavizada.

### Permutações e semente

**Omisso nos dois pontos.**

### Multiplicidade

**Omisso.**

### Reporte

**Declarado: mapa e nomes de regiões, sem teste de cluster nem p individual.** O "padrão aleatório" é afirmado sem teste relatado para a taxa.

> «A distribuição espacial mostrou um padrão aleatório das denúncias, embora taxas mais expressivas foram observadas principalmente nas Regiões Imediatas de Guarapuava, Francisco Beltrão, Paranavaí, Cianorte, Santo Antônio da Platina, Campo Mourão e Umuarama (Figura 2).» (p. 4)

### Fonte da justificativa

**Omisso.**

## Oliveira et al. (2024)

Arquivo: `oliveira_2024_mortalidade-materna.pdf`

OLIVEIRA, Ianne Vitória Gomes; MARANHÃO, Thatiana Araújo; FROTA, Maria Madalena Cardoso da; ARAUJO, Thalis Kennedy Azevedo de; TORRES, Samir da Rocha Fernandes; ROCHA, Maria Izabel Félix; XAVIER, Maria Eduarda da Silva; SOUSA, George Jó Bezerra. Mortalidade materna no Brasil: análise de tendências temporais e agrupamentos espaciais. **Ciência & Saúde Coletiva**, Rio de Janeiro, v. 29, n. 10, e05012023, 2024. DOI: https://doi.org/10.1590/1413-812320242910.05012023.

### Tratamento da taxa

- **Bayesiano empírico local: declarado.**

> «Para minimizar a instabilidade das taxas brutas, estas foram posteriormente suavizadas por meio do método bayesiano empírico local para corrigir flutuações aleatórias casuais10.» (p. 3)

- **Ajuste tipo Assunção-Reis: omisso.**
- **Taxa bruta e suavizada no mapa: declarado.**

> «Figura 2. Razão da mortalidade materna bruta (A), razão suavizada pelo método bayesiano empírico local (B)» (p. 6)

- **Moran global sobre a taxa bruta, não sobre a suavizada: declarado.**

> «O índice de Moran global, calculado a partir das taxas brutas, demonstrou autocorrelação espacial positiva significativa (I = 0,0682; p = 0,001).» (p. 4)

- **LISA: ambíguo.** O texto não diz sobre qual taxa foi calculado.

> «Com isso, procedeu-se ao cálculo do índice de Moran local.» (p. 4)

### Permutações e semente

**Omisso nos dois pontos para Moran e LISA.** A permutação de Monte Carlo citada pertence à regressão por pontos de inflexão, não ao teste de autocorrelação:

> «testando se um ou mais pontos de inflexão devem ser adicionados ao modelo linear pela técnica estatística de permutação de Monte Carlo» (p. 2)

### Multiplicidade

**Omisso.** Consta apenas o limiar:

> «foram utilizados os métodos de autocorrelação espacial, varredura scan e a técnica Getis-Ord Gi*, considerando-se significância de 5%» (p. 3)

### Reporte

**Declarado: mapa e descrição por estado, sem p individual por município.**

> «utilizou-se o índice de Moran local (local index spatial analysis – LISA) para verificar agregados espaciais em cada município brasileiro, sendo seus resultados representados pelo Moran map» (p. 3)

### Fonte da justificativa

**Declarado.** A chamada 10 da passagem sobre suavização remete a Brasil, Ministério da Saúde, *Abordagens Espaciais na Saúde Pública* (2006).

> «Brasil. Ministério da Saúde (MS). Abordagens Espaciais na Saúde Pública [Internet]. 2006.» (p. 11)

## Veiga e Bushatsky (2021)

Arquivo: `veiga_2021_violencia-mulher-pernambuco.pdf`

VEIGA, Bruna Cristina dos Santos; BUSHATSKY, Magaly. Distribuição espacial da violência contra a mulher: uma análise por geoprocessamento. **Revista Brasileira de Ciências Criminais**, São Paulo, v. 186, ano 29, p. 285-319, dez. 2021.

A unidade de análise é a mesorregião, não o município.

### Tratamento da taxa

- **Bayesiano empírico local: declarado.**

> «A suavização dos dados foi realizada pelo método bayesiano empírico local (média entre os vizinhos).» (PDF 13)

- **Ajuste tipo Assunção-Reis: omisso.**
- **Uso no mapa: ambíguo.** A estratificação menciona número de observações e incidência, e as legendas falam em casos. Nenhuma passagem diz que o mapa exibe a taxa suavizada.

> «O comportamento da distribuição espacial foi estratificado, baseado no número de observações de eventos, com cores mais fortes concentradas nos lugares com maiores incidências de notificação de violência contra a mulher» (PDF 13)

> «Figura 2 - Mapa de georreferenciamento dos casos de violência doméstica por mesorregiões em Pernambuco, ano 2016» (PDF 15)

- **Uso em Moran: ambíguo.** O texto não diz se a variável é bruta ou suavizada. Nenhum valor de Moran aparece fora da seção de métodos.

> «A utilização do SaTScan viabilizou o cálculo do Índice de Moran Global, para quantificar quanto a variável notificação de violência é semelhante entre as mesorregiões.» (PDF 13)

### Permutações e semente

**Omisso nos dois pontos.**

### Multiplicidade

**Omisso.**

### Reporte

**Omisso quanto à pertinência a cluster.** Os métodos anunciam a detecção de clusters, mas os resultados apresentam mapas e números por mesorregião, sem clusters identificados.

> «O cálculo desse Índice possibilitará a detecção de clusters espaciais associados à notificação.» (PDF 13)

### Fonte da justificativa

**Omisso quanto à suavização.** A frase sobre suavização não traz referência. Brasil (2006b), *Abordagens espaciais na saúde pública*, é citado na frase anterior, sobre a estratificação do mapa. Bailey e Gatrell (1995) são citados a respeito do índice de Moran.

> «fornecendo uma medida geral da associação espacial (BAILEY; GATRELL, 1995)» (PDF 13)

## Quadro-resumo

D = declarado; A = ambíguo; O = omisso.

| Trabalho | Tratamento da taxa | Permutações e semente | Multiplicidade | Reporte | Fonte da justificativa |
|---|---|---|---|---|---|
| Bahia et al. (2025) | Bruta no mapa: D. Bayesiana e Assunção-Reis: O. LISA: A quanto à taxa | Moran: O. Varredura, 999 simulações: D. Semente: O | Moran: O. Varredura: A | D: mapa, contagem e nomes, sem p individual | O |
| Barros et al. (2021) | EB local: D. Assunção-Reis: O. Mapa bruto e suavizado: D. **Moran global sobre a suavizada: D.** LISA: A | O; O | O | D: mapa e contagem, sem p individual | O |
| Carvalho et al. (2011) | Bruta, EB global e EB espacial: D. Assunção-Reis: O. Mapa: D. Teste de autocorrelação: O | O; O | O (só menção à literatura) | O | D: Clayton e Kaldor; Marshall |
| Carvalho et al. (2012) | Bruta, EB global e EB local: D. Assunção-Reis: O. Mapa: D. Teste de autocorrelação: O | O; O | O | O | D: Clayton e Kaldor; Marshall; Kafadar |
| Ceccon, Alves e Leite (2025) | EB global: D. Assunção-Reis: O. Mapa bruto e suavizado: D. LISA: A | O; O | O | D: mapa e poucos municípios, sem p individual | O |
| Moroskoski et al. (2025) | Suavização: D. Tipo e Assunção-Reis: O. Mapa: D. Moran ou LISA sobre a taxa: O | O; O | O | D: mapa e nomes, sem p individual | O |
| Oliveira et al. (2024) | EB local: D. Assunção-Reis: O. Mapa bruto e suavizado: D. Moran global sobre a bruta: D. LISA: A | O; O | O | D: mapa e estados, sem p individual | D: Brasil (2006) |
| Veiga e Bushatsky (2021) | EB local: D. Assunção-Reis: O. Mapa: A. Moran: A | O; O | O | O | O |

EB = bayesiana empírica.
