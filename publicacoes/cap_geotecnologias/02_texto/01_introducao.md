# 1. Introdução

A violência contra a mulher costuma ser tratada como questão de
segurança pública ou de saúde. Quando se tenta mapeá-la, ela se revela
também territorial — e o mapa não confirma o que se esperava dele.
Itikawa (2023), espacializando as ocorrências registradas pela Secretaria
de Segurança Pública de São Paulo em 2018, encontrou os cinco tipos de
violência definidos pela Lei Maria da Penha distribuídos por toda a
mancha urbana do município. Em números absolutos, as maiores quantidades
estão em distritos periféricos e semiperiféricos; ao dividir pela
população residente, o retrato se inverte, e as maiores densidades
passam a estar nos distritos do centro expandido — Sé, Barra Funda, Bom
Retiro, Consolação, Bela Vista, República —, áreas de renda
diversificada, oferta de emprego, infraestrutura e serviços. A autora
lê nessa concentração central um recalque espacial: a violência não como
atributo da pobreza, mas como manifestação do tensionamento de normas
patriarcais, capitalistas e raciais sobre o padrão de uso e ocupação do
solo.

O achado interessa a este capítulo por duas razões. A primeira é
substantiva: a hipótese corrente de que a violência se concentra onde se
concentram a pobreza e a periferia não sobrevive ao mapa. A segunda é
metodológica, e é a que aqui importa mais — os dois mapas de Itikawa
usam os mesmos registros e produzem leituras opostas. A diferença está
inteiramente em dividir, ou não, pela população. É uma demonstração, em
dado brasileiro publicado, de que decisões que parecem técnicas
determinam o que o mapa afirma.

Do lado da literatura internacional, a relação entre ambiente
residencial e violência por parceiro íntimo acumula pesquisa desde os
anos 1990, revisada sistematicamente por Beyer, Wallis e Hamberger
(2015). A revisão é útil menos pelo que consolida do que pela geografia
do que reúne: entre os estudos norte-americanos que definiram vizinhança
geograficamente, onze adotaram o *census tract* como proxy, e os autores
registram como lacunas a consideração limitada de áreas não urbanas,
a escassez de informação sobre o mundo em desenvolvimento e o fato de
que as explicações disponíveis derivam sobretudo da teoria da
desorganização social, formulada em contextos urbanos estadunidenses e
que precisaria ser adaptada para dar conta de correlatos ambientais em
contextos rurais. Anotam ainda, ao avaliar estudos individuais, que
taxas mais altas em vizinhanças desfavorecidas podem decorrer de efeitos
contextuais ou de viés de notificação — e que boa parte dos trabalhos
revisados não separa as duas hipóteses.

O Rio Grande do Sul está fora do domínio dessa literatura em quase todos
os eixos. São 497 municípios, a maioria de pequeno porte e não urbana,
distribuídos por um estado cuja escala de análise pertinente não é a
intraurbana do *census tract* nem a do distrito paulistano, mas a
municipal. É um recorte para o qual a teoria disponível foi pouco
testada e a evidência empírica é escassa.

Os dados existem. A Secretaria de Segurança Pública do Rio Grande do Sul
publica, em seu Observatório da Violência Contra a Mulher, séries de
indicadores desagregados por município e por mês, em planilhas de acesso
livre — condição que distingue este trabalho de precedentes brasileiros
próximos, já que tanto Itikawa (2023) quanto Veiga e Bushatsky (2021),
que analisaram por geoprocessamento os boletins de ocorrência de
Pernambuco entre 2016 e 2019, precisaram recorrer à Lei de Acesso à
Informação para obter os registros. A publicação, porém, não é o mesmo
que a disponibilidade analítica. Entre o arquivo publicado e um mapa que
se possa ler há um percurso de consolidação de layouts que mudam ao
longo da série, obtenção de denominadores populacionais que a fonte não
fornece, acoplamento a uma malha geográfica externa e definição de uma
arquitetura de publicação. Cada uma dessas etapas embute decisões, e
nenhuma delas costuma ser descrita nos trabalhos que apresentam os
resultados.

É esse percurso o objeto deste capítulo. Não se trata de apresentar
achados sobre a distribuição da violência contra a mulher no Rio Grande
do Sul — embora eles apareçam, e alguns sejam relevantes —, mas de
descrever e justificar o fluxo geotecnológico que os produz, do dado
administrativo bruto ao mapa interativo publicado. A violência contra a
mulher é a aplicação que dá sentido ao fluxo e impõe suas restrições
específicas: eventos raros em municípios pequenos, categorias que
agregam fenômenos distintos, uma fonte que revisa retroativamente o que
publicou. Um fluxo desenhado para outro fenômeno seria diferente.

A contribuição pretendida é o método replicável, e três pontos que
emergiram de sua construção sustentam essa pretensão. O primeiro é uma
demonstração empírica do problema da unidade de área modificável com os
mesmos dados em três níveis de agregação: a razão entre o município de
maior e o de menor taxa de Estupro cai de 34,3, no nível municipal, para
3,2 por COREDE e 1,7 por região intermediária. Nenhum caso mudou de
lugar; apenas a fronteira. O segundo é a sazonalidade diferencial dos
municípios litorâneos, cuja razão verão/inverno se distancia
sistematicamente do padrão estadual e de um grupo de controle pareado
por população, evidência de que o denominador residente não acompanha a
população presente e de que a taxa anual é inadequada para municípios de
população flutuante. O terceiro é a constatação de que publicar o código
não basta para reproduzir um resultado quando a fonte revisa
retroativamente os arquivos já publicados, o que levou à implementação
de um registro de proveniência dos dados brutos.

O capítulo está organizado como segue. A Seção 2 reúne a fundamentação
sobre dados públicos, escala municipal e representação cartográfica,
percorrendo as quatro decisões que estruturam o fluxo. A Seção 3
descreve as fontes de dados e as ferramentas empregadas. A Seção 4
apresenta o método em quatro etapas — consolidação, denominador,
acoplamento à malha e arquitetura de publicação —, e é nela que se
descreve o registro de proveniência que responde ao terceiro achado. A
Seção 5 expõe os resultados: o portal, a passagem do mapa interativo ao
impresso, a distribuição das taxas e os achados sobre sazonalidade e
unidade de agregação. A Seção 6 discute os limites do que os dados
permitem afirmar e as potencialidades do fluxo, e a Seção 7 retoma o
argumento. A Seção 8 informa a disponibilidade dos dados e do código.

---

## Notas para revisão

**Verificado nesta rodada.** Todas as afirmações atribuídas a Itikawa
(2023) e a Beyer, Wallis e Hamberger (2015) foram conferidas contra o
texto das fontes. Referências completas:

> ITIKAWA, L. F. Recalque espacial: violência contra a mulher em São
> Paulo. **Revista Estudos Feministas**, Florianópolis, v. 31, n. 2,
> e83846, 2023. DOI: 10.1590/1806-9584-2023v31n283846

> BEYER, K.; WALLIS, A. B.; HAMBERGER, L. K. Neighborhood environment
> and intimate partner violence: a systematic review. **Trauma,
> Violence, & Abuse**, v. 16, n. 1, p. 16-47, 2015.
> DOI: 10.1177/1524838013515758

**Verificações a fazer no próprio pipeline antes de fechar.** (a) O
nome exato do portal da SSP/RS — usei "Observatório da Violência Contra
a Mulher", que é como aparece nas pendências, mas o rótulo oficial da
página precisa ser conferido. (b) A afirmação de que a maioria dos
municípios gaúchos é de pequeno porte e não urbana é plausível e
consistente com o piso populacional (231 de 497 excluídos), mas está
enunciada sem fonte; ou se cita o IBGE, ou se substitui pelo número de
exclusões pelo piso, que é próprio e verificável. (c) Os números da
razão máx/mín vêm de §5.5 e devem ser conferidos contra a tabela final.

**Decisão editorial em aberto.** A introdução hoje não menciona
autocorrelação espacial, Moran ou LISA, coerente com a exclusão
deliberada desses tópicos. Se o parecerista da coletânea estranhar a
ausência, o lugar de justificá-la é aqui, em uma frase, e não na Seção 3
do capítulo — mas por ora preferi não abrir o assunto na abertura.

**Encaixes já aplicados em outras seções.** (a) O contraste de Itikawa
entre números absolutos e relativos abre agora §2.2. (b) A observação de
Beyer et al. sobre efeitos contextuais versus viés de notificação entrou
em §6.1, ao lado do precedente de Veiga e Bushatsky para Pernambuco.
(c) A nota de rodapé 27 de Itikawa reorientou o pedido via LAI descrito
nas notas de §6: a pergunta passa a ser se o SIP/PROCERGS mantém campos
separados para local da ocorrência e local do registro, e qual deles
alimenta os arquivos publicados.

**Não usado.** O achado de que Itikawa declara setor censitário na
metodologia e apresenta os resultados por distrito ficou fora do texto.
Apontar inconsistência metodológica em fonte usada como precedente exige
certeza de leitura e rende pouco ao argumento. Registrado na ficha.
