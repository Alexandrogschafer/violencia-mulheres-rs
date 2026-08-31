# 4. Método: do dado administrativo ao mapa interativo

> **Rascunho v3** — 30/08/2026. A v2 corrigiu três erros da v1: a
> simplificação de geometria (não existe), o comportamento do endpoint
> alternativo da API (sem evidência) e a aplicação do filtro de 5.000
> habitantes (não incide sobre o mapa). Esta versão resolve a pendência
> da classificação cromática, substitui a referência de arquitetura de
> publicação e precisa a citação dos operadores de interação.

O percurso descrito nesta seção pode ser lido como um fluxo de quatro
etapas encadeadas: consolidação e harmonização das planilhas de origem;
construção do denominador populacional; acoplamento à malha municipal; e
publicação em ambiente web. As etapas são sequenciais no sentido de que
cada uma consome o produto da anterior, mas independentes no sentido de
que cada uma é executada por um módulo próprio, com entrada e saída em
disco. Essa separação é deliberada: permite reexecutar apenas o trecho
afetado quando uma fonte é atualizada, e torna cada resultado
intermediário inspecionável — condição prática para que o fluxo seja
auditável por terceiros (PENG, 2011). A Figura 1 sintetiza o
encadeamento.

**[FIGURA 1 — Fluxograma do pipeline: fontes → módulos → produtos
intermediários → portal. A gerar.]**

Todo o processamento foi implementado em Python, apoiado em pandas para a manipulação tabular e em GeoPandas para as operações com geometrias. A camada de apresentação
usa Leaflet para o mapa e Chart.js para os gráficos de série temporal.
Todas as bibliotecas são de código aberto e licença permissiva, e nenhuma
etapa depende de software proprietário ou de licença institucional —
requisito que se mostrará relevante na discussão sobre replicabilidade.

## 4.1 Consolidação e harmonização das séries

A Secretaria da Segurança Pública do Rio Grande do Sul publica os
indicadores de violência contra a mulher em planilhas eletrônicas anuais,
organizadas por município e por natureza da ocorrência. O conjunto
reunido para este trabalho compreende dez arquivos, cobrindo o intervalo
de 2012 a 2026. A publicação em formato de planilha é, do ponto de vista
da transparência, um avanço; do ponto de vista do reúso analítico,
porém, ela impõe um obstáculo característico: cada arquivo foi produzido
para ser lido por uma pessoa, em um ano específico, e não para ser
concatenado a outros.

O obstáculo se manifesta em três descontinuidades. A primeira é de
granularidade temporal: os arquivos de 2012 a 2017 apresentam contagens
anuais por município, ao passo que os de 2018 em diante desagregam os
mesmos indicadores por mês. A segunda é terminológica: a categoria hoje
denominada Feminicídio aparece como "Femicídio" nos arquivos mais
antigos, exigindo um mapeamento explícito para que a série não seja
interrompida artificialmente em 2018. A terceira é estrutural: o arquivo
de 2016 traz colunas adicionais de população feminina municipal, ausentes
em todos os demais — resíduo de uma prática de publicação que não se
manteve.

A harmonização consistiu em converter os dez arquivos a um formato longo
(*long*), no qual cada linha representa a combinação de município,
período e categoria de ocorrência, e uma única coluna armazena o valor.
Esse formato tem duas virtudes para o caso: acomoda sem perda as duas
granularidades temporais, e dispensa a redefinição do esquema a cada novo
arquivo publicado pela fonte. Foram geradas duas tabelas consolidadas:
uma mensal, cobrindo 2018 a 2026, com 253.494 linhas; e uma anual,
cobrindo todo o intervalo de 2012 a 2026, com 36.780 linhas. As seis
categorias preservadas são Geral, Feminicídio Consumado, Feminicídio
Tentado, Ameaça, Estupro e Lesão Corporal.

A leitura direta dos arquivos revelou duas particularidades das categorias
que não são evidentes em seus rótulos e que condicionam a interpretação
dos resultados. A primeira diz respeito ao escopo: apenas o arquivo de
2012 a 2017 qualifica as ocorrências, em célula de cabeçalho, como
delitos enquadrados na Lei Maria da Penha; os arquivos de 2018 em diante
suprimem essa qualificação, e nenhum deles emprega, em qualquer célula,
expressão que restrinja explicitamente as categorias ao contexto
doméstico, familiar ou de relação íntima. O usuário que trabalhe apenas
com os arquivos recentes precisa inferir o escopo a partir de legislação
que a planilha não menciona. Adota-se aqui a leitura de que o
enquadramento se mantém, por continuidade da série e por coerência com a
finalidade declarada do monitoramento, mas registra-se que se trata de
inferência, e não de informação documentada na fonte. Registre-se ainda
que o título das planilhas menciona mulheres e meninas até 2017 e apenas
mulheres a partir de 2018, sem que a mudança seja explicada.

A segunda particularidade está em nota de rodapé presente nos arquivos de
2018 em diante: a categoria Estupro agrega os registros de Estupro e de
Estupro de Vulnerável. São condutas juridicamente distintas, com
universos de vítimas que se sobrepõem apenas em parte, reunidas sob um
rótulo único. A consequência para a leitura cartográfica é direta e será
retomada na Seção 6: o mapa de Estupro não representa um fenômeno
homogêneo.

Uma decisão de arquitetura merece registro por sua consequência prática.
Os arquivos de origem incluem uma linha residual, "NÃO INFORMADO", que
agrega os registros sem município identificado. Essa linha é **preservada
na etapa de consolidação**, sendo tratada como qualquer outro valor da
coluna de município, e só é excluída mais adiante, nos módulos que
produzem mapas e dados do portal — onde a ausência de geometria
correspondente a torna inutilizável. A opção por não descartá-la na
origem tem uma razão: mantém as tabelas consolidadas fiéis ao total
publicado pela fonte, de modo que a soma estadual reproduz exatamente o
dado oficial, e desloca a exclusão para o ponto em que ela é
tecnicamente necessária. O princípio geral — preservar o dado bruto e
filtrar o mais tarde possível — reduz a chance de que uma decisão tomada
cedo se propague de forma invisível pelo restante do fluxo.

A validação da consolidação seguiu três verificações. A primeira,
elementar, confirmou a ausência de valores nulos e de linhas duplicadas.
A segunda, mais informativa, foi uma reconciliação cruzada: para os anos
em que ambas as granularidades estão disponíveis, a soma dos doze valores
mensais de cada município e categoria foi comparada ao valor anual
correspondente, com concordância integral. A terceira consistiu em
verificações de plausibilidade sobre casos conhecidos — a taxa de Estupro
em Porto Alegre em 2025, por exemplo, resultou em 19,8 por 100 mil
habitantes, valor compatível com a ordem de grandeza esperada para uma
capital brasileira. Registre-se ainda uma inconsistência pontual da
fonte, corrigida na leitura: uma célula do arquivo de 2018 traz um traço
em lugar do valor zero, normalizada na consolidação. O ano de 2026 é
parcial, cobrindo os registros até aproximadamente maio, e portanto não
deve ser comparado diretamente aos anos completos.

Uma última providência desta etapa merece registro, por razão que só se
tornou evidente durante a preparação deste capítulo. Os arquivos
publicados pela Secretaria são revisados retroativamente: cada planilha
traz, em célula própria, a data em que foi atualizada pela última vez, e
essas datas mostram que anos encerrados há muito continuam a ser
reeditados — os arquivos de 2012 a 2020 utilizados aqui foram
consolidados em maio de 2023, o de 2021 em dezembro de 2023 e o de 2023
em janeiro de 2026. Um arquivo referente a 2020, portanto, foi reeditado
três anos após o período que descreve.

A implicação é que a entrada do fluxo não é estável no tempo, e que
executar o mesmo código sobre a mesma fonte em momentos distintos pode
produzir resultados distintos sem que nada tenha mudado no processamento.
Adotou-se por isso um registro de proveniência: um módulo próprio percorre
os arquivos brutos e grava, em tabela versionada, o hash de integridade de
cada um, a data de atualização declarada pela Secretaria e o metadado
interno correspondente do arquivo. A tabela permite determinar exatamente
qual versão de cada arquivo sustenta os resultados aqui apresentados —
condição sem a qual a publicação do código não bastaria para tornar o
trabalho reproduzível.

## 4.2 Construção do denominador populacional

Contagens absolutas de ocorrências não são comparáveis entre municípios
de portes distintos: um número elevado em um município populoso pode
corresponder a uma incidência menor que um número modesto em um município
pequeno. A conversão a taxas por habitante é, por isso, condição para
qualquer leitura cartográfica que pretenda comparar territórios
(SOUZA et al., 2007). Essa conversão, porém, exige um denominador — e é
nele que reside a decisão metodológica mais delicada do fluxo.

As estimativas populacionais municipais foram obtidas por consulta
programática à API do SIDRA, do Instituto Brasileiro de Geografia e
Estatística. A série exigiu a combinação de duas fontes distintas, por
uma razão que não é evidente à primeira vista: o IBGE não publica
estimativa populacional para o próprio ano censitário. Assim, os anos
intercensitários vêm da tabela de estimativas da população residente,
enquanto 2022 é obtido da tabela do Censo Demográfico. Trata-se de
grandezas de natureza distinta — uma contagem e uma estimativa — reunidas
na mesma série, o que é a prática corrente, mas convém explicitar.

O ano de 2023 não constava da resposta da API no momento da extração e
foi obtido por interpolação linear entre os dois anos disponíveis
adjacentes, isto é, entre a contagem censitária de 2022 e a estimativa de
2024. A decisão está documentada no próprio código e é assinalada aqui
por transparência: introduz na base um valor não observado, ainda que a
variação populacional municipal em intervalo de dois anos torne o
procedimento de baixo risco.

A limitação mais relevante do denominador é de outra ordem. O
denominador conceitualmente correto para taxas de violência contra a
mulher é a população feminina, e não a população total. Essa
desagregação, contudo, não está disponível em série contínua na escala
municipal para o período estudado: a série de população feminina por
município produzida pelo Departamento de Economia e Estatística do Rio
Grande do Sul cobre apenas o intervalo de 2010 a 2021, tendo sido
descontinuada após as enchentes de maio de 2024. As taxas apresentadas
neste capítulo usam, portanto, população total como denominador. A
consequência é que os valores não devem ser lidos como incidência sobre a
população feminina, e sim como indicador comparativo entre territórios —
leitura que permanece válida na medida em que a proporção de mulheres na
população municipal varia pouco entre os municípios do estado, mas que
precisa ser declarada.

## 4.3 Acoplamento à malha municipal

A espacialização exigiu associar cada registro tabular à geometria do
município correspondente. A malha municipal do Rio Grande do Sul foi
obtida em formato GeoJSON pela API de Malhas Territoriais do IBGE, o que
elimina a etapa de download manual e garante que a versão da malha usada
seja identificável e reobtenível.

Dois parâmetros da requisição merecem comentário, por concentrarem
decisões que afetam todo o restante do fluxo. O primeiro é
`intrarregiao=municipio`, que determina a subdivisão interna retornada: é
ele que faz a API devolver os 497 municípios em vez do estado como
unidade única. O segundo é `qualidade=intermediaria`, que seleciona o
nível de generalização da geometria fornecido pelo próprio serviço. Essa
escolha reduz o arquivo de aproximadamente 3,8 MB, na resolução máxima,
para cerca de 900 KB — diferença decisiva para o tempo de carregamento em
conexões lentas e dispositivos móveis, sem perda perceptível na escala
estadual em que o mapa é lido.

Vale sublinhar o que essa opção representa em termos de método: a
generalização cartográfica foi **delegada ao provedor dos dados**, e não
executada localmente por operação de simplificação geométrica. A
diferença não é apenas de implementação. Uma malha simplificada por
parâmetro de requisição é reobtenível de forma idêntica por qualquer
pessoa que repita a chamada, ao passo que uma simplificação local
introduz no fluxo um parâmetro adicional — tolerância, algoritmo — que
precisa ser documentado e reproduzido para que o resultado seja o mesmo.
Delegar a generalização à fonte é, nesse sentido, uma decisão a favor da
reprodutibilidade, além de uma economia de código. Registre-se a
contrapartida: a resolução disponível é a que o serviço oferece, sem
controle fino sobre o grau de generalização.

A junção entre a tabela de ocorrências e a malha foi feita pelo código
municipal do IBGE, e não pelo nome do município. A opção é deliberada:
nomes de municípios apresentam variações de grafia, acentuação e caixa
entre fontes distintas, e a correspondência por cadeia de caracteres
tende a produzir perdas silenciosas justamente nos municípios de nome
menos usual. A junção por código resultou em correspondência integral,
497 de 497 municípios, verificada explicitamente como parte do fluxo.

## 4.4 Arquitetura de publicação

A quarta etapa distingue-se das anteriores por não produzir dados, e sim
por definir onde e quando o processamento ocorre. A decisão estruturante
foi separar o que é computado no momento da construção do site (*build
time*) do que é computado no navegador do usuário (*runtime*).

Todo o processamento analítico — consolidação, cálculo de taxas, junção
espacial, agregações por município e por período — ocorre no momento da
construção, executado pelo módulo `build_site_data.py`, que grava
arquivos JSON e GeoJSON pré-agregados no diretório do portal. Ao
navegador cabe apenas ler esses arquivos e renderizá-los: o Leaflet
desenha a malha temática e trata a interação por município, e o Chart.js
desenha as séries temporais. Nenhuma consulta é calculada no momento do
acesso.

A consequência é que o portal não requer servidor de aplicação nem banco
de dados: é um conjunto de arquivos estáticos, hospedado no GitHub Pages.
A opção distingue-se da arquitetura mais usual em geoportais
institucionais, baseada em geosserviços interoperáveis do padrão OGC,
que pressupõem infraestrutura servidora dedicada.

A escolha entre as duas não é de superioridade técnica, mas de
adequação ao caso, e o ponto de corte pode ser situado com precisão.
Bastos e Camboim (2025), comparando três métodos de disponibilização de
mapas na web — serviço WMS, arquivos GeoJSON e *vector tiles* —, medem
para o GeoJSON volumes da ordem de uma centena de megabytes em base
cartográfica vetorial na escala 1:25.000, contra alguns megabytes nas
outras duas abordagens, e concluem pela inadequação do formato quando a
densidade de feições é alta. A malha empregada aqui está três ordens de
grandeza abaixo desse patamar: cerca de 900 KB para os 497 polígonos
municipais generalizados. O GeoJSON servido diretamente é adequado
neste caso precisamente porque o volume é baixo, e o trabalho citado
indica onde deixaria de ser.

As demais condições que justificariam geosserviços também não se
aplicam: as camadas são atualizadas uma vez por ano, e o público-alvo
consulta pelo navegador, sem necessidade de consumo programático.
Nessas condições, a arquitetura estática oferece três vantagens: custo de
hospedagem nulo, ausência de superfície de manutenção — não há serviço
que possa cair, nem dependência a atualizar por questão de segurança — e
durabilidade, uma vez que o portal permanece disponível sem intervenção.
O custo correspondente é a ausência de
consulta dinâmica: qualquer recorte não previsto na etapa de construção
exige reexecutar o pipeline e republicar o site — operação de poucos
minutos, mas que não pode ser feita pelo usuário final.

A interação disponível no mapa restringe-se deliberadamente a um
conjunto reduzido de operadores, na acepção de Roth (2013b): filtragem
por categoria de ocorrência, recuperação do valor de um município por
sobrevoo ou clique, e deslocamento e aproximação sobre a base
cartográfica. Dos doze operadores de trabalho da taxonomia, portanto,
quatro estão implementados; não há reexpressão, sobreposição de camadas,
ressimbolização pelo usuário nem sequenciamento temporal. A contenção é
intencional. Interfaces cartográficas com muitos controles
transferem ao leitor decisões de representação que ele não tem elementos
para tomar, e o público visado inclui gestores e profissionais de
serviços de atendimento, não analistas espaciais.

A representação das taxas no portal emprega interpolação contínua sobre
uma rampa sequencial, normalizada entre os valores mínimo e máximo
observados, sem divisão em classes discretas; a legenda exibe marcas ao
longo do gradiente, para referência de leitura, sem que correspondam a
fronteiras de classe. As figuras impressas deste capítulo adotam solução
distinta — classificação por quantis em cinco classes, com piso
populacional —, e a divergência é deliberada.

Ela decorre do meio, e a taxonomia de operadores dá a formulação exata.
No mapa impresso, a classificação é o único recurso de recuperação de
valor disponível: se o corte não separa dois municípios, o leitor não
tem como distingui-los. No mapa interativo, o operador de recuperação
está disponível, e as fronteiras de classe deixam de ser o único
mecanismo pelo qual um valor individual pode ser obtido — de modo que a
rampa contínua pode cumprir o papel de dar a impressão geral da
distribuição, delegando à interação a leitura pontual. A Seção 5.2
apresenta os cortes obtidos e mostra por que, no impresso, a
classificação se justifica empiricamente.

A base cartográfica de fundo é servida por um provedor externo de
*tiles*, com a atribuição implementada conforme os termos de uso. À
exceção dessa dependência, o portal não realiza requisições a terceiros:
não há fontes tipográficas remotas nem scripts de análise de audiência —
decisão que reduz a superfície de rastreamento do usuário e que, em um
portal sobre violência contra a mulher, tem implicações que ultrapassam
a preferência técnica.

---

## Notas para revisão

### Correções aplicadas em relação à v1

1. **Simplificação de geometria** — a v1 descrevia uma operação de
   simplificação local que não existe. Substituída pela discussão dos
   parâmetros da requisição (`intrarregiao` e `qualidade`), que é o
   mecanismo real e, do ponto de vista do capítulo, um argumento melhor:
   generalização delegada à fonte favorece a reprodutibilidade.
2. **Endpoint alternativo** — removido. Não há registro no código nem no
   histórico do git sobre o comportamento de `v3/malhas/43`, e a v1
   afirmava algo que não se sustenta. Se você tiver memória do teste,
   pode voltar como nota; caso contrário, o parágrafo sobre
   `intrarregiao=municipio` já cumpre a mesma função.
3. **Filtro de 5.000 habitantes** — removido da 4.2. Ele não incide sobre
   o mapa: existe apenas nos notebooks, para os rankings por taxa. Isso
   tem consequência para a Seção 6 (ver abaixo).
4. **Ano censitário** — precisado: 2022 vem da tabela do Censo, os demais
   anos da tabela de estimativas, porque o IBGE não estima população no
   ano em que recenseia.
5. **"NÃO INFORMADO"** — o tratamento real (preservar na consolidação,
   excluir a jusante) rendeu um parágrafo sobre princípio de arquitetura
   de dados, que é conteúdo bom para o capítulo.

### Pendência resolvida

A classificação cromática está decidida: rampa contínua no portal,
quantis com cinco classes e piso populacional nas figuras impressas. A
divergência é justificada pelo meio, na formulação de Roth (2013b) — o
operador de recuperação supre, no interativo, o papel das fronteiras de
classe —, e a justificativa empírica dos cortes está em 5.2. Os
parágrafos correspondentes desta seção e de 2.4 foram alinhados.

Registre-se que a justificativa pelo meio **não se estende ao piso
populacional**: um município de população reduzida tem taxa instável nos
dois suportes. Enquanto o portal não aplicar o piso, a divergência
precisa ser declarada em 6.4.

### Ainda em aberto

- A Figura 1 (fluxograma) não existe e precisa ser produzida.
- Não mencionei versionamento e DOI aqui, deixando para a Seção 7.
- Um parágrafo sobre o processo de atualização anual do pipeline poderia
  fechar a 4.4 — avaliar se cabe no limite de páginas.

**Extensão:** cerca de 2.100 palavras.
