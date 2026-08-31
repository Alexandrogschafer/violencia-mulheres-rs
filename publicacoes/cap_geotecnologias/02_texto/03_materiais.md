# 3. Materiais

Esta seção inventaria o que entra no fluxo: as fontes de dados, as
divisões territoriais usadas como unidades de agregação e as ferramentas
computacionais. O detalhamento do que se faz com cada uma delas fica
para a Seção 4. Os componentes de software são listados nominalmente,
com licença, seguindo a recomendação de que o software empregado em
pesquisa seja citado nos mesmos termos que qualquer outro produto de
pesquisa (SMITH; KATZ; NIEMEYER, 2016).

## 3.1 Fontes de dados

Três fontes alimentam o fluxo, todas públicas e de acesso livre, e
nenhuma delas exigiu pedido de acesso à informação.

**Registros de violência.** Secretaria de Segurança Pública do Rio
Grande do Sul, que publica os indicadores de violência contra a mulher
em planilhas anuais, tendo como origem primária o sistema SIP/PROCERGS.
São dez arquivos, cobrindo de 2012 a 2026, com seis categorias — Geral,
Feminicídio Consumado, Feminicídio Tentado, Ameaça, Estupro e Lesão
Corporal — desagregadas pelos 497 municípios do estado, mais uma
categoria "NÃO INFORMADO" para registros sem município identificado. A
série não é homogênea: os anos de 2012 a 2017 vêm num único arquivo,
com granularidade anual, nomenclatura "Femicídio" e colunas de população
feminina presentes apenas em 2016; de 2018 em diante, a granularidade é
mensal e o layout, padronizado. O arquivo de 2026 é parcial. Essa
heterogeneidade é o que a etapa de consolidação (Seção 4.1) precisa
resolver, e é também o que motiva o recorte temporal do capítulo.

**População.** Estimativas do Instituto Brasileiro de Geografia e
Estatística, obtidas pela API do SIDRA, tabela 6579, para os municípios
gaúchos. A série tem duas descontinuidades tratadas explicitamente: 2022
é ano de Censo e não de estimativa, e 2023 foi obtido por interpolação,
decisão documentada no código. Não há, para todo o período, estimativa
de população feminina por município: a Fundação de Economia e
Estatística do Rio Grande do Sul descontinuou essa série, que cobre
apenas de 2010 a 2021. O denominador utilizado é, portanto, a população
total — limitação discutida em 6.3.

**Malha geográfica.** Serviço de malhas territoriais do IBGE, acessado
por API, com a generalização delegada à própria fonte por meio do
parâmetro de qualidade intermediária, em vez de simplificação local
posterior. O acoplamento aos dados de violência é feito pelo código
municipal do IBGE, com correspondência integral para os 497 municípios.

**Divisões regionais.** Para a demonstração do efeito da unidade de
agregação (Seção 5.5), além do município são usados dois níveis
superiores: os Conselhos Regionais de Desenvolvimento (COREDEs) e as
regiões intermediárias do IBGE.

| Fonte | Conteúdo | Recorte disponível | Acesso |
|---|---|---|---|
| SSP/RS (SIP/PROCERGS) | Registros de seis categorias, por município | 2012–2026 | Planilhas publicadas |
| IBGE / SIDRA (tab. 6579) | População municipal | 2012–2025 | API |
| IBGE / Malhas territoriais | Geometrias municipais | — | API |
| COREDEs | Agrupamento regional | — | Divisão oficial |
| IBGE / Regiões intermediárias | Agrupamento regional | — | Divisão oficial |

O recorte adotado no capítulo é 2018–2025: 2018 é o primeiro ano de
granularidade mensal e layout padronizado na fonte, e 2026 está
incompleto. As categorias mapeadas são Ameaça, Lesão Corporal e Estupro;
Feminicídio Consumado e Tentado ficam de fora por serem eventos raros
demais para sustentar taxas municipais estáveis. Nas figuras impressas
deste capítulo aplica-se ainda um piso populacional de cinco mil
habitantes, que exclui 231 dos 497 municípios e deixa 266 elegíveis para
receber cor de taxa; o mapa interativo do portal não aplica esse piso, e
a divergência é discutida em 6.4.

## 3.2 Ferramentas

O pipeline é escrito em Python e o portal, em HTML, CSS e JavaScript
sem framework. Todas as dependências têm licenças permissivas, sem
restrição à redistribuição do conjunto.

| Camada | Ferramenta | Licença | Função no fluxo |
|---|---|---|---|
| Dados | pandas | BSD-3-Clause | Consolidação e transformação das tabelas |
| Dados | openpyxl | MIT | Leitura das planilhas da fonte |
| Espacial | GeoPandas | BSD-3-Clause | Acoplamento à malha e operações geométricas |
| Estatística | SciPy | BSD-3-Clause | Testes e ajustes da camada inferencial |
| Figuras | Matplotlib | PSF/BSD | Geração das figuras impressas, em PNG a 300 dpi |
| Portal | Leaflet | BSD-2-Clause | Mapa interativo |
| Portal | Chart.js | MIT | Gráficos de série histórica |
| Portal | CartoDB (tiles) | — | Mapa-base, com atribuição na interface |

O desenvolvimento foi feito em ambiente Linux com Python em ambiente
virtual isolado, e o código está versionado em repositório público, com
identificador persistente atribuído por depósito no Zenodo. A Seção 8
detalha a disponibilidade.

Duas observações sobre o que não está na tabela. Não são usadas fontes
tipográficas remotas nem scripts de análise de audiência de terceiros:
o portal não faz requisições a domínios além do serviço de mapa-base. E
o serviço de *tiles* é a única dependência externa em tempo de execução
— tudo o mais é servido estaticamente, o que tem consequências para a
arquitetura de publicação discutidas em 4.4.

---

## Notas para revisão

**Preencher antes de fechar.** (a) O nome oficial da página da SSP/RS de
onde vêm as planilhas, e o endereço, que aparecem também na Seção 8. (b)
As versões das bibliotecas — a tabela lista nomes e licenças, mas um
capítulo sobre reprodutibilidade deveria dar versões. Extrair do
ambiente e acrescentar uma coluna, ou remeter ao arquivo de dependências
do repositório e dizer isso no texto. (c) Confirmar a licença do
Matplotlib como está no projeto (a licença é própria, derivada da PSF) e
os termos de uso dos *tiles* da CartoDB, hoje com traço na tabela. (d)
O nome corrente do órgão estadual de estatística: o texto diz "Fundação
de Economia e Estatística", mas a estrutura foi reorganizada e a série
pode estar hoje sob a Secretaria de Planejamento; conferir como citar.

**Decisão pendente — esda e libpysal.** O pipeline usa essas duas
bibliotecas para autocorrelação espacial e clusters LISA, mas esses
tópicos estão deliberadamente fora do escopo do capítulo. Deixei-as fora
da tabela, para que ela descreva o que o capítulo faz e não o que o
repositório contém. A alternativa é incluí-las com nota explicando que
pertencem a uma camada não abordada aqui. Se a Seção 8 aponta para o
repositório inteiro, talvez seja mais coerente mencioná-las uma vez, em
nota de rodapé, do que omiti-las.

**Verificar contra o pipeline.** Os números 497, 231/266, o recorte
2018–2025 e a lista de categorias mapeadas vêm das decisões registradas
e devem bater com o que o código efetivamente faz. O texto já declara
que o piso vale para as figuras e não para o portal; se a rodada de
atualização do portal passar a aplicá-lo, esta frase precisa ser
revista aqui e em 6.4.

**Referência a confirmar.** Smith, Katz e Niemeyer (2016) está
verificada e sustenta a decisão de citar as ferramentas nominalmente. Já
McKinney (2010), que consta do `.bib` como citação do pandas, não foi
verificada; se a intenção é citar formalmente cada biblioteca, isso
multiplica as referências e convém decidir se vale — a alternativa,
compatível com Smith et al., é citar o repositório e o identificador
persistente de cada dependência, não o artigo que a descreve.

**Categoria "NÃO INFORMADO".** Está mencionada como característica da
fonte, sem número. A pendência 6.2.2 pede o volume de registros nessa
categoria; quando houver, o lugar natural é aqui, com uma frase, e a
discussão do que isso implica fica em 6.1.
