# Artigo espacial — manuscrito

<!-- Montado em 2026-11-02 a partir dos quatro rascunhos de seção. Título provisório. -->

## Resumo

**Objetivo:** descrever a distribuição espacial de quatro formas de violência contra a
mulher nos 497 municípios do Rio Grande do Sul entre 2018 e 2025 e examinar em que medida
os agrupamentos identificados coincidem entre si. **Métodos:** estudo ecológico de
delineamento transversal, com registros administrativos da Secretaria da Segurança Pública
estadual e taxas por 100 mil mulheres-ano. Estimaram-se os índices de Moran global e local
com o ajuste de Assunção e Reis, com significância por permutação aleatória no índice
global e condicional no local, 99.999 permutações e semente fixada, e controle de
multiplicidade por Benjamini-Hochberg a 5%. A interpretação restringiu-se aos pares com ao
menos cinco eventos esperados sob a taxa estadual. **Resultados:** o índice ajustado
decresceu com a raridade do desfecho, de 0,32 na ameaça a 0,09 no feminicídio tentado, e
não houve autocorrelação detectável no feminicídio consumado. Identificaram-se 67 pares
município-desfecho significativos em 58 municípios, entre eles um bloco contíguo de 21
municípios em quadrante alto-alto no norte do estado. A maioria dos municípios foi
significativa em um único desfecho; a coincidência mais expressiva em relação ao acaso
reuniu lesão corporal e estupro em três municípios contíguos do litoral. Três municípios
registraram contagens muito abaixo do esperado. **Conclusão:** os registros apresentam
estruturação espacial tanto mais nítida quanto mais frequente o desfecho. Os agrupamentos
descrevem a distribuição do registro, não necessariamente a da violência, e os déficits
acentuados sugerem lacunas de notificação.

**Palavras-chave:** Violência contra a Mulher; Análise Espacial; Sub-Registro; Estudos Ecológicos; Brasil.

## Introdução

A violência contra a mulher é problema de saúde pública e de segurança, e os serviços
especializados que a atendem distribuem-se de modo desigual entre os municípios: no Rio
Grande do Sul, em 2023, 38 dos 496 municípios que responderam ao quesito declararam ter
delegacia especializada no atendimento à mulher [1]. Saber como os registros se distribuem
entre municípios é, portanto, condição para dirigir a resposta — e a distribuição não é
homogênea [2,3].

Estudos que descrevem essa distribuição em municípios brasileiros recorrem a estatísticas
de autocorrelação espacial, que identificam agrupamentos de valores semelhantes em áreas
vizinhas [2,4]. Fora da escala municipal, variam a unidade e o desfecho. Em Minas Gerais,
a análise de feminicídios e homicídios de mulheres por microrregião de saúde detectou
cinco agrupamentos espaço-temporais, quatro deles comuns aos dois desfechos [5]. No
Paraná, as taxas suavizadas de denúncias de feminicídio foram maiores nas regiões
geográficas imediatas de maior área agricultável [6]. Em Pernambuco, entre os boletins de
ocorrência de violência doméstica agregados por mesorregião, o maior número de casos
esteve, em todos os anos, na Metropolitana do Recife [7]. A aplicação das estatísticas de
autocorrelação em escala municipal, porém, encontra duas dificuldades próprias. A primeira
é a instabilidade das taxas: municípios pequenos produzem taxas muito variáveis a partir
de poucos eventos, e desfechos raros agravam o problema [8]. A segunda é o número de
testes: avaliar quinhentas áreas simultaneamente exige controle de multiplicidade, sem o
qual a quantidade de falsos positivos deixa de ser desprezível [9].

Há ainda uma limitação que antecede a análise. Registros administrativos medem a
notificação, não a ocorrência. A subnotificação da violência contra a mulher é reconhecida,
e varia entre territórios conforme a capacidade de acolhimento e a disposição de denunciar
[2,4]. Um mapa construído sobre esses registros descreve, a rigor, a geografia do registro
— e distinguir o que nele é fenômeno do que é captação é parte da leitura, não uma ressalva
a acrescentar ao final.

A maior parte dos estudos disponíveis examina uma forma de violência por vez, usualmente o
homicídio ou o feminicídio. Com isso, permanece em aberto se as diferentes formas se
concentram nos mesmos territórios — pergunta com consequência direta para o planejamento,
já que a resposta é hoje organizada como se a violência contra a mulher fosse fenômeno
único.

Este estudo descreve a distribuição espacial de quatro formas de violência contra a mulher
nos 497 municípios do Rio Grande do Sul entre 2018 e 2025, e examina em que medida os
agrupamentos identificados coincidem entre si.

## Métodos

Estudo ecológico de delineamento transversal, tendo como unidade de análise os 497
municípios do Rio Grande do Sul.

### Fonte e desfechos

Os dados provêm dos registros administrativos da Secretaria da Segurança Pública do Rio
Grande do Sul, em planilhas de divulgação pública por município e ano [10]. Foram analisados
quatro desfechos de violência contra a mulher no período de 2018 a 2025: ameaça, lesão
corporal, estupro e feminicídio tentado. O feminicídio consumado foi analisado apenas
quanto à autocorrelação global, pela baixa ocorrência.

A categoria "estupro" da fonte reúne, sob rótulo único, estupro e estupro de vulnerável,
que são tipos penais distintos. Os arquivos divulgados são revisados retroativamente pela
secretaria, de modo que a mesma consulta em datas diferentes pode retornar valores
distintos; registrou-se a proveniência de cada extração, com data e soma de verificação.

As populações municipais anuais vieram do IBGE: de 2018 a 2021 e em 2024 e 2025, das
estimativas populacionais [11]; em 2022, do Censo Demográfico [12], porque a série de
estimativas não traz o ano censitário e, onde existe, a contagem medida é preferível à
projetada. Como o IBGE não publicou estimativa municipal para 2023, a população desse ano
foi interpolada linearmente entre 2022 e 2024, como a média dos dois anos arredondada ao
inteiro. O denominador adotado foi a população feminina, estimada como a população total
de cada ano multiplicada pela razão entre população feminina e total do município no Censo
2022 [12]. Essa razão mostrou-se estável entre os Censos de 2010 [13] e 2022, com variação
mediana absoluta de 0,48 ponto percentual e máximo de 2,60. As taxas são expressas por 100
mil mulheres-ano. Registre-se que a população feminina anual é estimada, não medida.

### Autocorrelação espacial

A vizinhança foi definida por contiguidade do tipo rainha, com matriz padronizada por
linha. A autocorrelação foi estimada pelo índice de Moran global e pelo indicador local de
associação espacial (LISA) [14], ambos com o ajuste proposto por Assunção e Reis [15]. O
ajuste responde à instabilidade da variância das taxas em áreas de tamanhos populacionais
desiguais: quanto menor a população do município, maior a variância da taxa estimada. O
índice ajustado é calculado a partir da contagem e da população sob risco, e não de taxas
previamente suavizadas: suavizar por método bayesiano e em seguida testar autocorrelação
induziria dependência por construção, já que a suavização toma emprestado dos vizinhos.

### Parâmetros do teste

A significância do índice global foi avaliada por permutação aleatória do vetor de taxas
ajustadas entre os municípios, e a do indicador local por permutação condicional, que
mantém fixo o valor de cada município e sorteia os valores de seus vizinhos entre os
demais. Nas duas, usaram-se **99.999 permutações** e semente fixada em **12345**. A
multiplicidade do indicador local foi tratada pelo procedimento de Benjamini-Hochberg a
5%, aplicado ao valor p direcional.

O número de permutações não é escolha indiferente. O menor valor p obtenível com m
permutações é 1/(m+1) [16], e o procedimento de Benjamini-Hochberg, com n áreas ao nível q,
rejeita as hipóteses até o maior posto i cujo valor p ordenado não excede q·i/n [9].
Combinando as duas expressões, o que nenhuma das duas fontes enuncia, rejeitar uma
hipótese nesse piso exige m+1 ≥ n/(q·i). Com 497 municípios ao nível de 5%, as 999
permutações usuais só permitiriam rejeição se ao menos dez municípios atingissem o piso
simultaneamente. Em verificação com vinte sementes, o feminicídio tentado não apresentou
nenhum município significativo em nenhuma das vinte execuções com 999 permutações, e
apresentou de cinco a seis com 99.999 — diferença atribuível exclusivamente ao parâmetro.

Como análise de sensibilidade, o procedimento foi repetido aplicando o controle de
multiplicidade ao dobro do valor p direcional; os resultados constam da seção de Resultados.

### Critério de interpretação

Para cada par município-desfecho significativo calculou-se o número esperado de eventos sob
a taxa estadual do desfecho, como mulheres-ano acumuladas no período multiplicadas pela taxa
e divididas por 100 mil. Pares com valor esperado inferior a cinco foram mantidos no
cálculo — excluí-los alteraria a matriz de vizinhança e, portanto, os resultados dos demais
— mas não receberam interpretação substantiva. A razão entre observado e esperado é
informada para cada município significativo.

Cabe uma observação sobre a leitura dos quadrantes. O procedimento padroniza as taxas em
relação à taxa estadual e, em seguida, centra os valores na média municipal. Como a taxa
estadual é ponderada pela população e, portanto, influenciada pelos municípios mais
populosos, a maioria dos municípios situa-se abaixo dela e a média dos valores
padronizados é negativa. Em consequência, os quadrantes designados "alto" indicam valores
acima da média municipal, e não necessariamente acima da taxa estadual.

### Processamento e reprodutibilidade

As análises foram conduzidas em Python, com as bibliotecas esda e libpysal. O código, os
dados processados e os parâmetros de execução estão depositados em repositório público, em
versão etiquetada correspondente aos resultados aqui apresentados [17].

## Resultados

### Ocorrência

Entre 2018 e 2025 foram registradas, nos 497 municípios do Rio Grande do Sul, 269.917
ameaças, 155.062 lesões corporais, 18.726 estupros, 2.286 feminicídios tentados e 739
feminicídios consumados contra mulheres. As taxas estaduais por 100 mil mulheres-ano foram
de 579,91; 333,15; 40,23; 4,91 e 1,59, respectivamente (Tabela 1).

Os desfechos diferem em ordem de grandeza e, com isso, na densidade com que ocorrem no
território. A contagem municipal mediana foi de 116 ameaças e 52 lesões corporais, contra 8
estupros e 1 feminicídio tentado. Nenhum município deixou de registrar ameaça ou lesão
corporal no período, enquanto 4,6% não registraram estupro, 42,3% não registraram
feminicídio tentado e 53,1% não registraram feminicídio consumado.

### Autocorrelação global

O índice de Moran ajustado decresceu de forma monótona na mesma ordem: 0,3198 para ameaça,
0,2962 para lesão corporal, 0,2194 para estupro e 0,0948 para feminicídio tentado, todos
com p < 0,001. O feminicídio consumado foi o único desfecho sem autocorrelação detectável
(I = 0,0122; p = 0,29; Tabela 1).

Os índices calculados sobre a taxa bruta foram menores que os ajustados nos desfechos mais
raros — 0,1713 contra 0,2194 no estupro —, como se espera quando a instabilidade da taxa em
populações pequenas atenua a medida.

### Agrupamentos locais

Foram identificados 67 pares município-desfecho significativos, distribuídos entre 58
municípios: 31 em ameaça, 15 em lesão corporal, 15 em estupro e 6 em feminicídio tentado
(Tabela 2 e Figura 1; pares listados na Tabela suplementar 2). Por quadrante, 32 pares
foram de valores altos cercados de altos, 28 de baixos cercados de baixos, 4 de altos
cercados de baixos e 3 de baixos cercados de altos. Cinco pares apresentaram menos de
cinco eventos esperados sob a taxa estadual e foram excluídos da interpretação, embora
mantidos no cálculo.

O achado de maior extensão foi um bloco contíguo de 21 municípios em quadrante alto-alto,
no norte do estado, distribuídos pelos Conselhos Regionais de Desenvolvimento Médio Alto
Uruguai (11), Celeiro (9) e Rio da Várzea (1). Todos satisfizeram o critério de cinco
eventos esperados. Cabe registrar que áreas vizinhas compartilham vizinhos no cálculo do
indicador local, de modo que parte da contiguidade observada é esperada por construção.

Os agrupamentos de valores baixos apresentaram padrão oposto: os 24 municípios envolvidos
distribuíram-se em dez blocos, de quatro municípios ou menos, três deles isolados. Os
outliers espaciais, nos quadrantes alto-baixo e baixo-alto, ocorreram todos isolados.

### Coincidência entre desfechos

Dos 58 municípios significativos, 49 o foram em um único desfecho e 9 em dois; nenhum em
três ou mais (Tabela 3). A ausência de coincidências triplas corresponde ao esperado sob
independência, inferior a uma unidade, e não constitui achado.

As coincidências observadas, em compensação, excederam largamente o acaso, e foram
espacialmente concentradas. A coincidência entre lesão corporal e estupro em quadrante
alto-alto ocorreu em três municípios contíguos do Conselho Regional de Desenvolvimento
Litoral — Capivari do Sul, Osório e Tramandaí —, contra 0,05 esperados sob independência
dentro do quadrante. A coincidência entre ameaça e lesão corporal em quadrante baixo-baixo
ocorreu em quatro municípios: Boa Vista do Sul, Linha Nova, Picada Café e Presidente
Lucena. As demais coincidências ocorreram em um município cada, e uma delas envolve par
excluído da interpretação por insuficiência de eventos esperados.

Nenhum município foi significativo em dois desfechos com quadrantes distintos: quando a
coincidência ocorre, a direção é a mesma nos dois.

### Déficits de registro

Três municípios apresentaram contagens muito abaixo do previsto pela taxa estadual, em
todas as vinte sementes testadas (Tabela suplementar 2). Em Canudos do Vale registrou-se
uma lesão corporal, contra 21,77 esperadas (p < 0,0001). Em Mariana Pimentel não houve
registro de estupro, contra 6,15 esperados (p = 0,0021). Em Doutor Maurício Cardoso
registraram-se dois estupros, contra 7,33 esperados (p = 0,0230).

### Sensibilidade

A aplicação do controle de multiplicidade ao dobro do valor p direcional reduziu o número de
municípios significativos em todos os desfechos — 20 em ameaça, 10 em lesão corporal, 8 em
estupro e 3 em feminicídio tentado — e ampliou a variação entre sementes, que alcançou de 6
a 12 municípios na lesão corporal e de 0 a 3 no feminicídio tentado.

Quatro pares classificados em quadrante alto apresentaram contagem observada inferior à
esperada pela taxa estadual (Tabela suplementar 2), entre eles Capivari do Sul em lesão
corporal, com razão de 0,77. Porto Alegre foi classificada como baixo-alto em estupro, com
observado em 0,94 do esperado (p = 0,0006); a significância decorre do tamanho da
população do município, não da magnitude do desvio.

A substituição do denominador feminino pela população total, apresentada na Tabela
suplementar 1, alterou o índice de Moran global em no máximo 0,014, o status de
significância de três municípios e o quadrante de um.

## Discussão

Os registros de violência contra a mulher no Rio Grande do Sul não se distribuem ao acaso
entre os municípios, e a intensidade dessa estruturação decresce com a raridade do
desfecho: forte na ameaça e na lesão corporal, moderada no estupro, fraca no feminicídio
tentado e indetectável no feminicídio consumado. O desfecho mais grave é, também, aquele
sobre cuja geografia menos se pode afirmar.

### O que os quadrantes dizem e o que não dizem

A leitura dos agrupamentos exige uma precaução que a nomenclatura convida a dispensar. O
procedimento compara cada município à média dos municípios, não à taxa do estado. Como a
taxa estadual é ponderada pela população e, portanto, puxada pelos municípios mais
populosos, a maioria dos municípios situa-se abaixo dela. Um agrupamento de valores "altos"
indica, assim, valores altos em relação à vizinhança — e quatro dos pares aqui
identificados em quadrante alto registraram, na verdade, menos eventos do que a taxa
estadual previa. Chamar esses agrupamentos de áreas de alta incidência seria incorreto, e é
a leitura que um gestor faria se o texto não a prevenisse.

Pela mesma razão, a razão entre observado e esperado é informada para cada município: ela
distingue o que é alto em termos absolutos do que é alto apenas em relação a vizinhos
baixos.

### O bloco do norte

O achado de maior extensão é um conjunto contíguo de 21 municípios no norte do estado.
Trata-se de municípios pequenos, e a contiguidade do bloco deve ser lida com reserva, já
que o indicador local compartilha vizinhos entre áreas adjacentes e tende, por construção,
a produzir conjuntos contíguos.

Este estudo não investiga as razões do padrão. Explicá-lo exigiria análise de fatores
associados, deliberadamente não realizada: num desenho transversal e com registros
administrativos, a associação entre características municipais e taxas registradas confunde
a ocorrência do evento com a sua captação pelo sistema de registro. O que o resultado
estabelece é onde a atenção deve ser dirigida, não por quê.

### Coincidência entre formas de violência

As formas de violência não compartilham território de modo geral — a maioria dos municípios
significativos o é em um único desfecho —, mas onde coincidem, coincidem muito acima do
acaso e sempre na mesma direção. Nenhum município apresentou valores altos para uma forma e
baixos para outra. Isso é compatível com uma propensão municipal ao registro, que afeta
todas as formas, mais do que com uma especificidade por tipo de violência.

A coincidência entre lesão corporal e estupro em três municípios contíguos do Conselho
Regional de Desenvolvimento Litoral merece ressalva adicional. A região litorânea recebe
população flutuante expressiva no verão, e o denominador utilizado é a população feminina
residente. Eventos envolvendo pessoas não residentes inflam o numerador sem alterar o denominador, de modo que parte do excesso pode
ser artefato de medida, e não concentração do fenômeno.

### Zero não é ausência

Três municípios registraram contagens muito abaixo do previsto: uma lesão corporal contra
21,77 esperadas, nenhum estupro contra 6,15, dois estupros contra 7,33. Em todos, o
resultado se manteve em todas as sementes testadas.

A leitura substantiva desses casos — territórios com pouca violência — é menos plausível
que a leitura de medida: territórios com pouco registro. Municípios pequenos e sem serviços
especializados oferecem menos pontos de notificação, e a ausência de registro não equivale
à ausência do evento.

Essa interpretação, porém, não pôde ser confirmada. A comparação da cobertura da rede de
atendimento entre os municípios de déficit e os demais não discrimina, porque serviços
especializados praticamente inexistem em municípios desse porte: de 306 municípios gaúchos
com menos de 7.500 habitantes, apenas um declara delegacia especializada. A ausência de
serviço nesses municípios é o que o porte já prevê, e não distingue as duas leituras.
Resolver a questão exigiria confronto com fonte independente de registro, como as
notificações compulsórias do sistema de saúde.

### Os dois extremos do teste

O indicador local é pouco potente onde a população é pequena e excessivamente potente onde
ela é grande. Nos municípios menores, poucos eventos esperados tornam o teste incapaz de
distinguir variação aleatória de padrão — razão pela qual cinco pares foram excluídos da
interpretação. Na capital, ao contrário, um desvio de 6% em relação à taxa estadual produz
p inferior a 0,001, por efeito do tamanho da população e não da magnitude do desvio.

Nenhum dos dois extremos sustenta interpretação substantiva isoladamente, e ambos
permanecem invisíveis em uma apresentação que informe apenas o mapa de quadrantes.

### Limitações

Os dados provêm de registros administrativos e medem a notificação, não a ocorrência. A
subnotificação da violência contra a mulher é reconhecida e variável entre territórios, o
que afeta diretamente a comparação espacial.

A categoria "estupro" da fonte reúne estupro e estupro de vulnerável, tipos penais
distintos cuja agregação não pode ser desfeita a partir dos dados divulgados.

Os arquivos de divulgação são revisados retroativamente, de modo que os valores aqui
analisados correspondem à extração datada e registrada, e não necessariamente ao que a mesma
consulta retornaria hoje.

O período foi agregado, de modo que o estudo descreve a distribuição acumulada em oito anos
e não permite afirmar nada sobre tendência ou deslocamento dos agrupamentos ao longo do
tempo.

Por fim, a unidade de análise é o município, e os resultados descrevem municípios, não as
mulheres que neles vivem: nenhuma conclusão sobre risco individual decorre deste
delineamento.

## Conclusão

Os registros de violência contra a mulher no Rio Grande do Sul apresentam estruturação
espacial consistente, tanto mais nítida quanto mais frequente o desfecho, e indetectável no
feminicídio consumado. As quatro formas analisadas raramente compartilham território; onde
compartilham, fazem-no muito acima do acaso e sempre na mesma direção.

Os agrupamentos descrevem a distribuição dos registros, não necessariamente a da violência.
Três municípios apresentaram contagens tão abaixo do previsto que a explicação mais
plausível é a lacuna de notificação, e sua verificação demanda confronto com fonte
independente, como as notificações compulsórias do sistema de saúde.

A interpretação de resultados desse tipo depende de parâmetros que raramente são
declarados. O número de permutações, a semente e o tratamento da multiplicidade determinam
o que o teste é capaz de detectar, e sua omissão impede que o leitor distingua a ausência
de agrupamento da incapacidade de encontrá-lo.

## Referências

<!-- Lista gerada por 01_referencias/renumerar_referencias.py em ordem de primeira aparição. Não editar à mão. -->

1. Instituto Brasileiro de Geografia e Estatística. Pesquisa de Informações Básicas Municipais –
   MUNIC 2023: base de dados [Internet]. Rio de Janeiro: IBGE; 2024 [citado 2026 nov 3]. Disponível
   em: https://ftp.ibge.gov.br/Perfil_Municipios/2023/Base_de_Dados/Base_MUNIC_2023.xlsx

2. Oliveira MR, Madeiro AP, Nascimento FF, Andrade JX, Rodrigues MTP, Mascarenhas MDM. Tendência e
   padrão espacial das notificações de estupro por parceiro íntimo contra mulheres no Nordeste do
   Brasil (2013–2022). Rev Bras Epidemiol. 2024;27:e240030. doi:10.1590/1980-549720240030.2

3. Sá YRC, Moi PCP, Galvão ND, Silva AMC, Moi GP. The geography of femicide in Sergipe, Brazil:
   matriarchy, human development, and income distribution. Rev Bras Epidemiol. 2021;24(Suppl
   1):e210016. doi:10.1590/1980-549720210016.supl.1

4. Barros SC, Oliveira CM, Silva APSC, Melo MFO, Pimentel DR, Bonfim CV. Análise espacial dos
   homicídios intencionais de mulheres. Rev Esc Enferm USP. 2021;55:e03770.
   doi:10.1590/S1980-220X2020037303770

5. Bahia CA, Pinto IV, Trindade CM, Silva CMA, Habkouk P, Simões TC, et al. Feminicídios em Minas
   Gerais, Brasil: da caracterização dos eventos à análise espaço-temporal. Cad Saude Publica.
   2025;41(1):e00015224. doi:10.1590/0102-311XPT015224

6. Moroskoski M, Azevedo LS, Brito FAM, Oliveira NN, Pereira ND, Carreira L, et al. Feminicídio:
   análise espacial e fatores associados aos crimes de gênero no Paraná, Brasil. Cien Saude Colet.
   2025;30(10):e10862025. doi:10.1590/1413-812320253010.10862025

7. Veiga BCS, Bushatsky M. Distribuição espacial da violência contra a mulher: uma análise por
   geoprocessamento. Rev Bras Cienc Crim. 2021;29(186):285-319.

8. Carvalho AXY, Silva GDM, Almeida Júnior GR, Albuquerque PHM. Taxas bayesianas para o mapeamento
   de homicídios nos municípios brasileiros. Cad Saude Publica. 2012;28(7):1249-62.
   doi:10.1590/S0102-311X2012000700004

9. Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach
   to multiple testing. J R Stat Soc Series B Stat Methodol. 1995;57(1):289-300.
   doi:10.1111/j.2517-6161.1995.tb02031.x

10. Rio Grande do Sul. Secretaria da Segurança Pública. Indicadores da violência contra a mulher –
    Lei Maria da Penha [Internet]. Porto Alegre: SSP; 2018-2026 [citado 2026 nov 2]. Disponível em:
    https://www.ssp.rs.gov.br/indicadores-da-violencia-contra-a-mulher

11. Instituto Brasileiro de Geografia e Estatística. Estimativas de População: tabela 6579 –
    população residente estimada [Internet]. Rio de Janeiro: IBGE; [citado 2026 nov 2]. Disponível
    em: https://sidra.ibge.gov.br/tabela/6579

12. Instituto Brasileiro de Geografia e Estatística. Censo Demográfico 2022: tabela 4709 – população
    residente, e tabela 9514 – população residente, por sexo, idade e forma de declaração da idade
    [Internet]. Rio de Janeiro: IBGE; [citado 2026 nov 3]. Disponível em:
    https://sidra.ibge.gov.br/tabela/4709 e https://sidra.ibge.gov.br/tabela/9514

13. Instituto Brasileiro de Geografia e Estatística. Censo Demográfico 2010: tabela 1378 – população
    residente, por situação do domicílio, sexo e idade [Internet]. Rio de Janeiro: IBGE; [citado
    2026 nov 3]. Disponível em: https://sidra.ibge.gov.br/tabela/1378

14. Anselin L. Local indicators of spatial association—LISA. Geogr Anal. 1995;27(2):93-115.
    doi:10.1111/j.1538-4632.1995.tb00338.x

15. Assunção RM, Reis EA. A new proposal to adjust Moran's I for population density. Stat Med.
    1999;18(16):2147-62. doi:10.1002/(SICI)1097-0258(19990830)18:16<2147::AID-SIM179>3.0.CO;2-I

16. Fischer L, Barry T, Ramdas A. Multiple testing with anytime-valid Monte Carlo p-values
    [Preprint]. arXiv:2404.15586v4 [stat.ME]. 2025 [citado 2026 nov 2]. Disponível em:
    https://arxiv.org/abs/2404.15586v4

17. Schäfer AG, Prates LA, Schäfer LP, Fernandes MAD. Pipeline de análise da violência contra a
    mulher no RS (2012-2026) [Internet]. Versão [etiqueta do artigo a criar]. Zenodo; 2026 [citado
    2026 nov 3]. doi:10.5281/zenodo.21403499. Disponível em:
    https://github.com/Alexandrogschafer/violencia-mulheres-rs
