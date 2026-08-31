# 2. Dados públicos, escala municipal e representação cartográfica

Mapear a violência contra a mulher a partir de dados públicos municipais
envolve quatro decisões encadeadas, e cada uma delas tem literatura
própria. É preciso saber o que um registro administrativo mede e o que
ele deixa de fora; converter contagens em taxas sem produzir artefatos
onde a população é pequena; escolher a unidade de agregação sabendo que
a escolha altera o resultado; e traduzir os valores em classes e cores
sem que a representação diga mais — ou menos — do que os dados
sustentam. Esta seção percorre as quatro, na ordem em que aparecem no
fluxo descrito na Seção 4.

## 2.1 O que é um registro administrativo

O levantamento de Sousa, Uchôa e Barreto (2024) mapeou 204 publicações
brasileiras sobre violência contra a mulher entre 2000 e 2023 e as
classificou segundo a metodologia de coleta. Pouco mais da metade
(53%) baseia-se em registros oficiais — polícia, justiça, sistema de
saúde, Central de Atendimento à Mulher; 10% são pesquisas de
vitimização, e o restante distribui-se entre pesquisas de opinião,
estudos sobre a rede de serviços e categorias mistas. A existência de
duas famílias distintas não é redundância metodológica: a pesquisa de
vitimização existe justamente para estimar o que o registro oficial não
alcança. As autoras registram, na mesma linha, a ordem de grandeza da
diferença — a edição de 2023 do *Visível e invisível* estima em 18,6
milhões o número de brasileiras de 16 anos ou mais que sofreram alguma
forma de violência ao longo de 2022, patamar incompatível com o volume
de ocorrências registradas no mesmo período.

A consequência para este capítulo é direta. O dado da SSP/RS não mede a
ocorrência de violência; mede o encontro entre a ocorrência e o aparato
estatal que a registra. Toda leitura espacial que se faça sobre ele é,
antes de mais nada, uma leitura da distribuição desse encontro. O ponto
é desenvolvido na Seção 6.1; aqui interessa apenas fixar que se trata de
uma característica da fonte, não de uma ressalva de praxe.

O arcabouço legal que produz esses dados é recente e tem finalidade
declarada. O artigo 8º, inciso II, da Lei nº 11.340/2006 estabeleceu a
promoção de estudos, pesquisas e estatísticas sobre violência doméstica
e familiar, com sistematização nacional; a Lei nº 14.232/2021 instituiu
a Política Nacional de Dados e Informações relacionadas à Violência
contra as Mulheres, cujos objetivos incluem disponibilidade,
autenticidade, integridade e comparabilidade das informações (SOUSA;
UCHÔA; BARRETO, 2024). São exatamente os atributos que a Seção 6.6
discute como não plenamente satisfeitos pela publicação em planilhas
revisadas retroativamente.

Vale registrar que a lógica territorial desses sistemas é
administrativa antes de ser analítica. Magalhães et al. (2006), tratando
dos sistemas de informação em saúde, observam que os dados são
localizados por referência às unidades da administração pública —
município, estado — porque é assim que os sistemas os coletam, embora os
processos sociais e ambientais que produzem os agravos não se limitem a
essas fronteiras. A observação transporta-se sem perda para os dados de
segurança pública: o município é a unidade porque é a unidade do
registro, não porque seja a unidade do fenômeno.

O precedente brasileiro mais próximo do que aqui se propõe é Veiga e
Bushatsky (2021), estudo ecológico que analisou por geoprocessamento os
boletins de ocorrência de violência doméstica e familiar em Pernambuco
entre 2016 e 2019, obtidos por pedido de acesso à informação junto à
Ouvidoria Geral do estado. As autoras encontram maior incidência de
registros na mesorregião Metropolitana do Recife e menor na do São
Francisco, e — no mesmo texto — inventariam a rede de atendimento:
quatro das onze delegacias especializadas e onze dos vinte e nove
centros especializados do estado concentram-se na primeira; a segunda
conta com um de cada. A leitura que oferecem é a de que a proximidade da
capital e a densidade de serviços favorecem a quebra do silêncio. Seja
qual for a interpretação preferida, o achado é metodologicamente
decisivo para qualquer mapa construído sobre registros policiais: parte
da variação espacial observada é variação na capacidade de registrar.

## 2.2 Contagem, taxa e pequenos números

A conversão de contagens em taxas é o passo que torna municípios de
portes diferentes comparáveis, e é também onde se instala o problema
mais conhecido do mapeamento por áreas. Que a decisão não seja neutra
tem demonstração publicada em dado brasileiro: Itikawa (2023),
mapeando as ocorrências de violência contra a mulher no município de São
Paulo em 2018, encontra as maiores quantidades absolutas em distritos
periféricos e semiperiféricos; ao dividir pela população residente de
cada distrito, o retrato se inverte, e as maiores densidades passam a
estar nos distritos do centro expandido. São os mesmos registros e a
mesma malha; muda apenas o denominador. Escolher entre contagem e taxa é
escolher o que o mapa vai afirmar.

O coeficiente é a razão entre o
número de casos e a população sob risco no mesmo período, multiplicada
por uma constante escolhida para evitar decimais de leitura difícil
(SOUZA-SANTOS et al., 2007). Os mesmos autores advertem que coeficientes
calculados para períodos curtos ou populações pequenas exigem cautela, e
sugerem, como alternativas, ampliar a janela temporal ou agregar a
unidade.

Souza et al. (2007) desenvolvem o ponto com um exemplo que vale como
diagnóstico geral. As taxas brutas são o estimador de risco mais simples
e mais usado, mas tornam-se instáveis quando o evento é raro e a
população da área é pequena: um ou dois casos a mais ou a menos produzem
variações abruptas que nada dizem sobre o fenômeno. A dispersão das
taxas municipais de mortalidade por acidentes de transporte no Brasil em
2004, plotada contra o logaritmo da população, assume a forma de funil,
com variabilidade máxima nos municípios de porte pequeno — e cerca de um
quarto dos municípios brasileiros tem menos de cinco mil habitantes. O
mapa de taxas brutas resultante, observam, não permite identificar
padrão algum por inspeção visual. O material mais recente do Ministério
da Saúde formula o mesmo trade-off pelo outro lado: quanto menor a área,
mais raros os eventos observáveis, o que origina flutuação aleatória
excessiva dos indicadores (BRASIL, 2024).

Convém explicitar que a resposta padrão da literatura a esse problema
não é a que este capítulo adota. Souza et al. (2007) tratam a
instabilidade como questão a ser resolvida por suavização — média móvel
espacial, estimador bayesiano empírico —, procedimentos que estabilizam
a estimativa de cada área tomando emprestada informação da vizinhança.
Veiga e Bushatsky (2021) seguem esse caminho, aplicando suavização
bayesiana empírica local aos dados de Pernambuco. A opção aqui é outra:
excluir do mapa os municípios abaixo de um piso populacional,
preservando para os demais o valor efetivamente observado. A razão é de
finalidade, não de mérito estatístico. Um portal público de consulta
municipal cujo mapa exibisse, para um município, um valor derivado dos
seus vizinhos entregaria ao leitor um número que não é o daquele
município — e é o número do município que o leitor foi ali procurar. A
exclusão custa cobertura e a torna explícita; a suavização preserva
cobertura e desloca o custo para dentro do valor exibido. As duas
decisões são defensáveis; a Seção 6.4 retoma a escolha e seus limites.

Resta o denominador. A taxa depende de uma estimativa populacional que é
ela própria um produto estatístico, com periodicidade, método e
descontinuidades próprios. O caso deste trabalho tem uma restrição
adicional, discutida na Seção 4.2: o denominador disponível para toda a
série é a população total, e não a população feminina, de modo que as
taxas calculadas não são taxas de incidência sobre a população em risco
no sentido estrito, mas indicadores de intensidade do registro por
habitante. A Seção 6.3 trata das consequências.

## 2.3 A unidade de agregação

Os dois problemas anteriores convergem numa mesma decisão: qual o
recorte espacial. Magalhães et al. (2006), discutindo critérios de
escolha da unidade espacial de análise, listam disponibilidade e
qualidade do dado, reconhecimento da unidade pela população, existência
de instâncias administrativas correspondentes, homogeneidade interna e
heterogeneidade externa. E enunciam o trade-off central: unidades
pequenas dão maior precisão na localização dos eventos, mas produzem
instabilidade de taxas; unidades maiores reduzem a instabilidade, mas
podem falsear informação ao construir médias que apagam diferenciais
internos. É a mesma tensão da subseção anterior, vista do outro extremo.

A formulação canônica desse efeito é o problema da unidade de área
modificável, que o material do Ministério da Saúde define de forma
econômica: para uma mesma população estudada, a definição espacial das
fronteiras afeta os resultados obtidos, de modo que se podem obter
resultados diferentes apenas alterando as fronteiras das zonas (BRASIL,
2024). Note-se que o problema não é de qualidade do dado nem de método
de análise: os casos são os mesmos, a população é a mesma, e ainda assim
o resultado muda. A Seção 5.5 apresenta uma demonstração empírica desse
efeito com os dados do Rio Grande do Sul em três níveis de agregação.

Ao lado do MAUP, e frequentemente confundida com ele, está a falácia
ecológica — a tentativa de estimar associações entre indivíduos a partir
de dados agregados, presumindo que tendências no nível do grupo se
aplicam aos indivíduos que o compõem (BRASIL, 2024). São problemas
distintos: o MAUP diz respeito à sensibilidade do resultado agregado ao
recorte; a falácia ecológica, à transposição indevida do agregado para o
indivíduo. Este capítulo trabalha inteiramente no nível agregado e não
formula hipóteses individuais; a distinção é retomada na Seção 6.5.

A escolha da unidade é, também, uma escolha sobre o que se torna
visível. Veiga e Bushatsky (2021) analisaram Pernambuco em cinco
mesorregiões, agrupando 187 municípios — recorte que estabiliza as taxas
e viabiliza a comparação inter-regional, ao custo de tornar invisível
qualquer heterogeneidade interna às mesorregiões. A opção deste trabalho
pelo município é a opção pelo extremo oposto, com os custos que a
subseção 2.2 já enunciou. Não há nível correto em abstrato; há níveis
adequados a perguntas.

## 2.4 Classificação, cor e o meio de publicação

O mapa coroplético é fácil de produzir e por isso mesmo exige cuidado.
Pina et al. (2006) são explícitos: nesses mapas os resultados dependem
inteiramente do método de classificação, do número de classes escolhido
e da configuração das áreas, de modo que variar um desses parâmetros
altera o mapa e, por vezes, a interpretação. A recomendação
procedimental que oferecem é anterior à escolha do método — conhecer a
distribuição dos dados, examiná-la por histograma, e só então decidir
quantos e quais os pontos de corte.

Sobre o número de classes há convergência entre as fontes consultadas.
Souza-Santos et al. (2007) registram que muitos autores consideram ideal
um número entre quatro e seis. Pina et al. (2006) fundamentam o limite
superior na percepção: o olho humano distingue com dificuldade mais de
seis tons dentro de uma mesma cor, e a dificuldade não está em ler a
legenda, onde os tons aparecem hierarquicamente ordenados, mas em
estabelecer a correspondência entre legenda e mapa, onde aparecem
misturados. Os mesmos autores reúnem critérios para a escolha de cores,
entre os quais um que interessa diretamente a este capítulo: testar a
leitura das cores escolhidas nos diferentes meios de veiculação —
impressão, projeção, internet —, porque as cores exibidas em monitor não
são as mesmas quando impressas.

Esse último critério aponta para uma distinção que a literatura
cartográfica trata como estrutural, e não como detalhe de produção.
Roth (2013a) organiza o campo em torno do par representação cartográfica
e interação cartográfica: a primeira trata de como os mapas são vistos e
compreendidos; a segunda, de como são manipulados pelo usuário, num
diálogo entre pessoa e mapa mediado por um dispositivo computacional.
Para a segunda, o mesmo autor propôs uma taxonomia derivada
empiricamente de entrevistas com vinte e um usuários experientes de
mapas interativos e de um exercício de ordenação de cartões com quinze
projetistas (ROTH, 2013b). A taxonomia distingue cinco operadores
habilitadores — importar, exportar, salvar, editar e anotar — de doze
operadores de trabalho, entre os quais está o operador de recuperação
(*retrieve*), pelo qual o usuário obtém detalhes adicionais sobre uma
feição individual do mapa.

A implicação para o desenho é a seguinte. No mapa impresso, a
classificação é o único instrumento de recuperação de valor de que o
leitor dispõe: se o corte de classe não separa dois municípios, eles são
indistinguíveis, e não há nada que o leitor possa fazer a respeito. No
mapa interativo, o operador de recuperação está disponível, e a
fronteira de classe deixa de ser o único mecanismo pelo qual um valor
individual pode ser obtido. Daí a divergência deliberada de escolhas
entre as duas saídas do mesmo fluxo, documentada na Seção 4.4 e retomada
em 5.2: classificação por quantis com cinco classes no impresso, rampa
contínua no portal. Não são duas soluções para o mesmo problema, mas
soluções para problemas que o meio torna diferentes.

---

## Notas para revisão

**Verificado.** Todas as afirmações atribuídas a Sousa, Uchôa e Barreto
(2024), Veiga e Bushatsky (2021), Itikawa (2023), Roth (2013a), Roth
(2013b) e aos três volumes da Série Capacitação e Atualização em
Geoprocessamento em Saúde foram conferidas contra o texto das fontes.

**Correção de autoria.** O artigo de *Serviço Social & Sociedade* é
SOUSA, Rosana de Vasconcelos; UCHÔA, Ana Maria de Vasconcelos; BARRETO,
Maria Raidalva Nery. *Fontes de informação sobre a violência contra a
mulher no Brasil*. Serv. Soc. Soc., São Paulo, v. 147, n. 2, e-6628376,
2024. DOI 10.1590/0101-6628.376. O sobrenome é **Sousa**, com S; o
arquivo circulava como `souza_2024`. Corrigir no `.bib` e em §6.1.

**Roth — resolvido, com dois 2013.** Não existe Roth (2012) como fonte
do operador; a indicação anterior nesta nota estava errada. A taxonomia
empírica com os doze operadores de trabalho é o artigo do IEEE TVCG, de
2013. São portanto duas obras do mesmo autor e do mesmo ano, que o
`.bib` precisa distinguir:

> ROTH, R. E. Interactive maps: what we know and what we need to know.
> **Journal of Spatial Information Science**, n. 6, p. 59-115, 2013a.

> ROTH, R. E. An empirically-derived taxonomy of interaction primitives
> for interactive cartography and geovisualization. **IEEE Transactions
> on Visualization and Computer Graphics**, v. 19, n. 12, p. 2356-2365,
> 2013b. DOI 10.1109/TVCG.2013.130

O operador de recuperação está definido em Roth (2013b), p. 2363.
Remover Roth (2012) do `.bib`. A expressão pode ser usada livremente no
texto e na tabela de decisões da Seção 5.

**Referências que não serão verificadas.** Brewer e Pickle (2002),
Openshaw e Taylor (1979), Robinson (1950), Slocum et al. (2022) e Haklay
et al. (2008) não foram obtidos e não há previsão de obtê-los. §2.3
sustenta-se sem Openshaw e Taylor e sem Robinson — MAUP e falácia
ecológica entram pela formulação brasileira —, e §2.4 sustenta-se sem
Slocum. Sugestão: remover Openshaw e Taylor, Robinson, Slocum e Haklay
do `.bib` em vez de mantê-los como referências não lidas. O PDF que
circulou como `RobinsonFinalRG` não é Robinson (1950), mas uma errata
posterior de outros autores, e não serve como substituto.

**Pendência aberta — quantis.** É a única afirmação do capítulo sem
apoio verificado: a escolha de quantis com cinco classes, na tabela de
decisões da Seção 5, apoia-se em Brewer e Pickle (2002), indisponível. O
número de classes está coberto (Souza-Santos et al., 2007; Pina et al.,
2006); o método, não. Duas saídas: obter o artigo pelo Portal CAPES via
CAFe, ou trocar a justificativa por um argumento empírico próprio — a
assimetria da distribuição das taxas municipais, que faz os métodos de
corte por intervalo produzirem classes quase vazias na cauda enquanto os
quantis preservam ocupação equilibrada. A segunda saída dispensa a
referência e é demonstrável com o histograma do próprio trabalho.

**Decisão de citação a tomar.** As passagens da Série foram atribuídas
aos autores dos capítulos (Magalhães et al., Pina et al., Souza-Santos
et al., Souza et al.), não aos organizadores dos volumes. É mais
preciso, mas conflita com a entrada "Santos & Souza (2007)" já existente
no `.bib`, que corresponde aos organizadores do volume 3. Padronizar:
sugiro `@incollection` por capítulo, com o volume como `booktitle`. Os
volumes são: v.1 SANTOS; BARCELLOS (org.), 2006; v.2 SANTOS;
SOUZA-SANTOS (org.), 2007; v.3 SANTOS; SOUZA (org.), 2007.

**Ano a confirmar.** O material do Profepi/OPAS citado como (BRASIL,
2024) — *Análise Espacial Aplicada à Vigilância em Saúde e Ambiente*,
conteudistas Mônica de Avelar F. M. Magalhães e Renata Gracie, ICICT/
Fiocruz — não traz ano na folha de rosto extraída; as fontes internas
mais recentes são de 2024. Confirmar antes de fechar o `.bib`.

**Impacto em outras seções.** (a) Veiga e Bushatsky (2021) documentam,
para Pernambuco, a concentração da rede de atendimento na mesorregião de
maior registro — precedente publicado para a verificação pendente 6.2.1
(município do registro vs. município do fato). Vale citá-lo em §6.1
mesmo antes da resposta ao pedido via LAI. (b) A distinção entre
exclusão por piso e suavização, agora explicitada em §2.2, precisa ser
espelhada em §6.4, e reforça o lado do capítulo na decisão em aberto
sobre aplicar o piso também no portal (pendência 6.3.4). (c) Peng
(2011), Wilkinson et al. (2016) e Smith et al. (2016) foram lidos e
verificados, mas pertencem a §4.4, §6.6 e §8 — não a esta seção. Peng
sustenta com precisão o achado (c) do capítulo: o padrão de
reprodutibilidade que ele define exige que **os mesmos dados** sejam
reanalisados, o que é exatamente o que a revisão retroativa da fonte
impede. (d) Itikawa (2023), agora citada em §2.2, também abre a Seção 1
e sua nota de rodapé 27 reorienta o pedido via LAI da pendência 6.2.1:
a base da SSP-SP mantém campos distintos para local da ocorrência e
local do registro, de modo que a pergunta a fazer à SSP/RS é se o
SIP/PROCERGS faz a mesma distinção e qual campo alimenta os arquivos
publicados. (e) Bastos e Camboim (2025) compara WMS, GeoJSON e Vector
Tiles para publicação de mapas na web e pertence à Seção 4.4; o uso
honesto exige confrontar o volume medido por eles para GeoJSON com o
volume real da malha servida pelo portal, e argumentar pela adequação ao
caso, não pela superioridade da abordagem.

**Ainda sem uso.** Beyer, Wallis e Hamberger (2015) foi verificada e
incorporada à Seção 1, como delimitação do nicho do capítulo. Não tem
encaixe nas quatro decisões que esta seção cobre e não deve ser forçada
aqui.
