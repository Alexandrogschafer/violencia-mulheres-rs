# 6. Potencialidades e limites

> **Rascunho v1** — 30/08/2026. Marcadores `[VERIFICAR: ...]` indicam
> afirmações que dependem de checagem antes da versão final. Citações em
> formato autor-data, a converter para a norma da editora.

O fluxo descrito nas seções anteriores produz um artefato de aparência
inequívoca: um mapa que atribui a cada município um valor e uma cor. Essa
aparência é enganosa em três níveis — no que o dado mede, no denominador
que o converte em taxa, e na unidade em que é representado. Esta seção
examina os três, na convicção de que declarar os limites de um instrumento
é parte de disponibilizá-lo, e não uma concessão feita a contragosto.

## 6.1 O que o dado mede

A limitação de origem, da qual todas as demais são subordinadas, é que os
dados utilizados registram **ocorrências comunicadas à polícia**, não
ocorrências. Entre o fato e o registro interpõe-se uma cadeia de condições
— que a vítima reconheça a situação como crime, que decida comunicá-la,
que tenha acesso material a um posto de atendimento, que seja acolhida de
modo a completar o registro — e cada elo dessa cadeia varia
territorialmente. A literatura sobre fontes de informação em violência
contra a mulher no Brasil sistematiza essa distinção, separando os
registros oficiais das pesquisas de vitimização, que buscam justamente
alcançar a violência que não chega às estatísticas (SOUSA; UCHÔA;
BARRETO, 2024). A observação vale também para a literatura
internacional: a revisão de Beyer, Wallis e Hamberger (2015) registra que
taxas mais altas em áreas desfavorecidas podem decorrer de efeitos de
contexto ou de viés de notificação, e que boa parte dos estudos
revisados não separa as duas hipóteses.

A consequência para a leitura dos mapas apresentados é forte, e convém
enunciá-la sem atenuação: um município com taxa alta pode ser um município
onde há mais violência, ou um município onde a violência é mais
comunicada. Um serviço de atendimento especializado bem instalado, uma
delegacia da mulher em funcionamento, uma rede de acolhimento ativa —
todos elevam o número de registros sem que nada tenha ocorrido com a
incidência real. O mapa, nesses casos, distingue infraestrutura de
atendimento e não distribuição de violência. Veiga e Bushatsky (2021)
oferecem ilustração empírica dessa coincidência: em Pernambuco, a
mesorregião com maior número de boletins de ocorrência é também a que
concentra quatro das onze delegacias especializadas e onze dos vinte e
nove centros de atendimento do estado, enquanto a de menor registro
dispõe de um de cada.

Essa ambiguidade é irredutível com os dados disponíveis. Ela não invalida
o instrumento, mas define o que ele autoriza: identificar territórios que
merecem investigação, e não hierarquizar municípios por gravidade. É
também a razão pela qual as figuras deste capítulo adotam paleta neutra e
título descritivo, sem vocabulário de alarme — a escolha cromática de um
mapa participa do argumento que ele faz, e uma paleta de perigo
converteria uma medida de registro em veredito sobre o território.

## 6.2 O que cada categoria agrega

Os rótulos das categorias sugerem homogeneidade que os dados não têm, e o
caso mais consequente é o de Estupro. Conforme nota de rodapé dos próprios
arquivos, discutida na Seção 4, a categoria reúne os registros de Estupro
e de Estupro de Vulnerável — condutas distintas, com universos de vítimas
que se sobrepõem apenas parcialmente, entre os quais a segunda alcança
vítimas menores de catorze anos e pessoas sem discernimento para consentir.

A consequência cartográfica é que o mapa de Estupro apresentado na Figura
5 superpõe pelo menos dois fenômenos com dinâmicas territoriais
possivelmente distintas, sem que a proporção entre eles seja conhecida em
cada município. Um território que apareça na classe superior pode
concentrar predominantemente um ou outro. Nada nos dados publicados
permite desagregar, e nenhuma leitura do mapa deve supor que a variável
represente um fenômeno único. É provável que essa agregação responda por
parte da dispersão espacial notada na Seção 5.3, em contraste com os
padrões mais coerentes de Ameaça e Lesão Corporal.

O problema, note-se, não é da agregação em si — pode haver razão
operacional para ela — mas do fato de constar apenas em nota de rodapé, à
qual o consumidor do dado só chega se abrir o arquivo original e ler até o
fim da planilha. Um usuário que consuma a mesma informação por qualquer
intermediário que não reproduza a nota trabalhará com uma variável cujo
conteúdo desconhece.

Consideração análoga vale para o escopo do conjunto. Como registrado na
Seção 4, o enquadramento das ocorrências na Lei Maria da Penha consta
apenas do arquivo mais antigo da série; nos posteriores, o leitor precisa
inferi-lo. A diferença entre "ameaças contra mulheres" e "ameaças contra
mulheres em contexto doméstico ou familiar" é substantiva, e uma série
publicada sem essa qualificação transfere ao usuário uma decisão
interpretativa que caberia à fonte documentar.

## 6.3 O denominador

Duas limitações afetam o denominador das taxas, uma conhecida desde o
início e outra revelada pela própria análise.

A primeira é a impossibilidade de usar população feminina. O denominador
conceitualmente correto para taxas de violência contra a mulher é a
população exposta, e a série de população feminina por município no Rio
Grande do Sul cobre apenas o intervalo de 2010 a 2021. As taxas
apresentadas usam população total. Como a proporção de mulheres varia
pouco entre os municípios do estado, o ordenamento relativo é pouco
afetado; as magnitudes absolutas, porém, não devem ser lidas como
incidência sobre mulheres.

A segunda emergiu do exame da distribuição mensal apresentado na Seção
5.4. Nos municípios de população fortemente flutuante, o denominador
residente não acompanha a população efetivamente presente, e a taxa anual
superestima a exposição da população residente. O caso do litoral norte
gaúcho é nítido, mas o problema é geral: qualquer município com dinâmica
sazonal intensa — turística, universitária, agrícola de safra — está
sujeito ao mesmo desalinhamento. Vale notar que essa limitação não foi
antecipada no desenho do fluxo; ela apareceu porque a base mensal permitiu
testá-la. Bases com granularidade temporal inferior à do denominador
oferecem essa verificação de graça, e ela raramente é feita.

## 6.4 A malha municipal e os pequenos números

Das 497 unidades municipais do estado, 231 — quase metade — ficam abaixo
do piso de 5.000 habitantes adotado, nas figuras deste capítulo, para
exibição de taxas. Esse número
não decorre do limiar escolhido, e sim da estrutura do território gaúcho:
o Rio Grande do Sul é um estado de fragmentação municipal acentuada, com
grande número de municípios de população reduzida, muitos deles criados
por emancipação nas décadas de 1980 e 1990.

Convém declarar aqui uma divergência entre os dois produtos do mesmo
fluxo. A opção pela rampa contínua no portal e pela classificação no
impresso justifica-se pelo meio, conforme exposto em 4.4 e 5.2; a
ausência do piso populacional no mapa interativo, não. A instabilidade
da taxa de um município de população reduzida é a mesma nos dois
suportes, e o argumento que sustenta a exclusão no impresso sustenta-a
igualmente na web. Registra-se a divergência como limitação da versão
aqui descrita.

O efeito é que o município, como unidade de análise para violência contra
a mulher no Rio Grande do Sul, é adequado para as categorias frequentes e
inadequado para as raras. Em Ameaça e Lesão Corporal, os municípios
elegíveis acumulam contagens que sustentam uma taxa estável. Em Estupro, o
topo do ranking é ocupado por municípios com poucas dezenas de registros
em oito anos. Em Feminicídio, a instabilidade é tal que a representação
por taxa municipal deixa de ser informativa — razão pela qual essa
categoria não foi mapeada neste capítulo, ainda que conste do portal.

Vale registrar o que a mudança de recorte temporal revelou a esse
respeito. Na janela anterior de cinco anos, havia municípios elegíveis com
taxa zero em Estupro; na janela de oito anos, não há nenhum. O que o mapa
anterior exibia como ausência do fenômeno era, em parte, período de
observação insuficiente para que um evento dessa frequência se
manifestasse. A extensão da janela temporal é, portanto, um recurso
disponível contra a instabilidade de pequenos números — ao custo de
diluir mudanças recentes, que é precisamente o que se quer observar em
séries de política pública.

## 6.5 Escala e inferência

A demonstração apresentada na Seção 5.5 tem consequência direta sobre a
leitura dos mapas. Se a desigualdade territorial medida em Estupro cai de
34,3 vezes para 1,7 vez apenas mudando a fronteira de agregação, então
nenhuma afirmação sobre "a distribuição espacial do fenômeno" é completa
sem menção à unidade em que foi medida.

Some-se a isso a restrição clássica da inferência sobre dados agregados,
discutida em 2.3: correlações e valores observados entre unidades
territoriais não autorizam conclusões sobre os indivíduos que as
compõem. Que um município apresente
taxa elevada não informa nada sobre a probabilidade de uma mulher
específica, residente nele, sofrer violência — informa sobre o agregado.
Mapas coropléticos são particularmente propensos a induzir essa
transposição, porque a cor uniforme sobre a área sugere homogeneidade
interna que os dados não sustentam.

Há ainda um problema de atribuição espacial que precisa ser explicitado
[VERIFICAR: confirmar com a SSP/RS ou com a documentação do SIP se o
município do registro é o do fato ou o da delegacia que registrou]. Se o
registro é atribuído ao município da unidade policial, municípios-sede de
delegacias regionais concentram registros originados na vizinhança, o que
produziria concentração artificial em polos regionais. Esta é uma
verificação que não pôde ser feita com a documentação disponível e que
condiciona a leitura de qualquer mapa municipal construído sobre a fonte.

## 6.6 Recorte temporal, versão e transparência

Os mapas deste capítulo cobrem 2018 a 2025. O limite inferior corresponde
ao ano em que a fonte passou a publicar com granularidade mensal e layout
padronizado; o superior exclui 2026, ano parcial. Ambos os critérios são
factuais, mas nada os torna necessários: outras janelas seriam igualmente
defensáveis e produziriam ordenamentos diferentes.

Esse ponto merece generalização, porque é onde a experiência deste projeto
mais tem a oferecer a quem construa instrumentos semelhantes. Um portal
que apresenta séries temporais, testes estatísticos e mapas tende a
acumular recortes distintos, cada um herdado da rotina que o produziu —
uma série que usa todo o histórico disponível, um teste que exige
granularidade mensal, um mapa que herdou o período de um caderno de
análise. Cada recorte pode ser individualmente justificado e, ainda assim,
o conjunto apresentar ao leitor janelas diferentes do mesmo fenômeno sem
sinalização. A auditoria realizada durante a preparação deste capítulo
identificou exatamente essa situação no portal aqui descrito, e a correção
adotada foi dupla: unificar o recorte dos mapas ao critério documentado
dos testes de série, e explicitar em cada página o período representado.
A transparência quanto ao recorte é, nesse sentido, parte da
responsabilidade de quem publica dado territorial — e não é assegurada
pela publicação do código-fonte, já que o leitor do mapa não lê o
repositório.

Um segundo aspecto do mesmo problema diz respeito à estabilidade da
entrada, e ele tensiona um pressuposto corrente sobre reprodutibilidade.
Como registrado na Seção 4, a Secretaria revisa retroativamente os
arquivos publicados: anos encerrados continuam a ser reeditados, por vezes
três anos depois do período que descrevem. Uma consequência é que os
números aqui apresentados podem divergir dos que se obteria hoje na mesma
fonte, sem que nenhuma das duas versões esteja errada — a mais recente
incorpora correções, a utilizada aqui é a que sustentou a análise.

O ponto tem alcance além deste caso. O padrão corrente de
reprodutibilidade computacional pressupõe que os mesmos dados sejam
reanalisados a partir do código publicado (PENG, 2011), e a publicação
do código de fato assegura que o processamento seja auditável e
reexecutável. Mas reexecutar o mesmo código sobre uma fonte que mudou
não satisfaz esse padrão: não reproduz o resultado, produz um resultado
novo. Para fontes administrativas
sujeitas a revisão — categoria que abrange boa parte dos dados públicos
brasileiros de saúde e segurança — a reprodutibilidade exige registrar
também qual versão da entrada foi consumida. Foi o que motivou o registro
de proveniência descrito na Seção 4, construído a partir de informação que
os próprios arquivos já carregavam e que passava despercebida. Trata-se de
providência de custo desprezível, e cuja ausência só se torna visível
quando alguém tenta reproduzir o trabalho e obtém números diferentes sem
saber por quê.

## 6.7 Potencialidades

Enunciados os limites, cabe registrar o que o fluxo oferece.

O primeiro ganho é de disponibilidade. Os dados utilizados eram públicos
antes deste trabalho; o que não existia era a possibilidade de consultá-los
como informação territorial. A distância entre uma planilha anual
publicada em portal institucional e um mapa navegável por município é,
em termos de esforço, considerável — e é justamente essa distância que
separa o dado disponível do dado utilizável por gestores, jornalistas e
pesquisadores de outras áreas.

O segundo é de replicabilidade. Nenhuma etapa do fluxo depende de software
proprietário, licença institucional ou infraestrutura servidora. A malha
vem de serviço público, o denominador de serviço público, o processamento
de bibliotecas de código aberto, e a publicação de hospedagem estática sem
custo. Um fluxo com essas propriedades pode ser reproduzido por outra
unidade federativa, ou aplicado a outro tema de dado administrativo
municipalizado, com o custo de adaptar a etapa de harmonização — que é,
não por acaso, a única etapa específica da fonte.

O terceiro é de durabilidade. Projetos de pesquisa perdem financiamento, e
com ele costumam perder a infraestrutura que sustentava seus produtos. Um
conjunto de arquivos estáticos versionados não tem serviço que caia nem
dependência que expire, e permanece disponível sem intervenção — condição
modesta, mas rara, para que um instrumento sobreviva ao projeto que o
originou.

---

## Notas para revisão

### Ponto que exige decisão antes de publicar

**O portal ainda não tem piso populacional.** A divergência está agora
declarada em 6.4, o que resolve o problema editorial mínimo. Mas a
solução melhor continua sendo aplicar o piso também no portal: publicar
um capítulo que argumenta pela necessidade do piso enquanto o portal
descrito não o aplica é um flanco, ainda que declarado. Se a rodada de
atualização do portal aplicar o piso, o parágrafo correspondente de 6.4
deve ser removido e a frase de 5.2 e de 3.1, ajustada.

### Verificações necessárias

- **Município do registro vs. município do fato** (§6.5). Continua sendo
  a verificação mais importante em aberto. A nota de rodapé 27 de
  Itikawa (2023) indica que a base da SSP-SP mantém campos distintos
  para local da ocorrência e local do registro, o que permite formular o
  pedido de forma objetiva: perguntar se o SIP/PROCERGS faz a mesma
  distinção e qual dos campos alimenta os arquivos publicados. Caminho:
  Central de Informação do RS (LAI) ou Ouvidoria da SSP.
- **Categoria "NÃO INFORMADO"** — falta o volume de registros sem
  município identificado. Se for expressivo, merece parágrafo próprio.
- **Emancipações municipais no RS** (§6.4) — afirmei que muitos
  municípios pequenos resultam de emancipações das décadas de 1980 e
  1990. É conhecimento corrente, mas convém uma fonte, ou suavizar.
- **§6.6 no passado.** O parágrafo sobre a unificação do recorte e as
  notas de período em cada página descreve as correções como já
  adotadas. Isso só será verdadeiro depois da rodada de atualização do
  portal. Conferir antes de submeter.

### Incorporado nesta versão

- **§6.2 (nova)** — heterogeneidade das categorias: Estupro agrega
  Estupro e Estupro de Vulnerável, conforme nota de rodapé dos arquivos;
  e o enquadramento na Lei Maria da Penha consta apenas do arquivo de
  2012–2017. Subseções seguintes renumeradas.
- **§6.6** — revisão retroativa dos arquivos e a distinção entre publicar
  o processamento e registrar a versão da entrada.

### Ponto para checagem factual

O §6.2 afirma que Estupro de Vulnerável alcança vítimas menores de
catorze anos e pessoas sem discernimento para consentir. É a definição do
art. 217-A do Código Penal, mas vale conferir a redação vigente antes de
publicar, e considerar se convém citá-lo explicitamente.

### Escolhas editoriais tomadas

- Enfrentei a ambiguidade entre "mais violência" e "mais registro" logo na
  primeira subseção, em vez de deixá-la como ressalva final. É a
  limitação que condiciona todas as outras.
- Aproveitei a subseção 6.5 para transformar um problema encontrado no
  próprio portal em contribuição metodológica generalizável. Se preferir
  não expor a inconsistência anterior, o parágrafo pode ser reescrito em
  termos impessoais.

**Extensão:** cerca de 1.700 palavras.
