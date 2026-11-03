# Verificação das referências — artigo espacial

Verificação, em 2026-11-02, dos marcadores de `afirmacoes_a_referenciar.md`. Para cada um há a
afirmação exata do manuscrito, a referência e a passagem que a sustenta, com página. Sem passagem
transcrita, a referência não entra na lista Vancouver. Há duas exceções, as citações de origem de
método (A07, A12) e de fonte de dados (A01, A10, A11), cujos critérios estão descritos em cada entrada.

Revisão de 2026-11-02, segunda rodada:
- o antigo A08 foi dividido em A08a e A08b;
- Knijnenburg et al. foram retirados;
- a autoria de Fischer foi corrigida para três autores;
- A10–A12 foram acrescentados;
- a referência da MUNIC está preparada, mas aguarda a nova primeira frase da Introdução.

Revisão de 2026-11-03: A07 (Assunção e Reis) passa a entrar na lista como citação de origem do método,
sem passagem transcrita, porque o texto completo não foi obtido. Os caminhos tentados estão na entrada.
Na mesma data, o repositório (A09) entrou como referência 11, e os marcadores foram numerados no
manuscrito; Fischer et al. passaram de 9 para 10. A01 segue pendente.

Revisão de 2026-11-03, segunda rodada: A01 foi reescrita e cita a MUNIC 2023, que entra como
referência 1 e desloca as demais. Os números desta página foram atualizados.

## Como ler

- **Sustenta:** a passagem diz o que a afirmação diz.
- **Sustenta, com ressalva:** a passagem sustenta a afirmação, mas há algo a decidir (fonte secundária,
  derivação, página).
- **Sem sustentação:** nenhuma passagem encontrada sustenta a afirmação como está escrita. Ela será
  reescrita; não se procurou outra fonte.
- **Não obtenível:** o texto completo da fonte não foi obtido. A fonte não foi citada pelo resumo.
- **Páginas:** é a numeração impressa no artigo. Nos artigos de paginação eletrônica (e03770, e240030,
  e210016), é a página dentro do artigo.
- **Conferência:** as transcrições de texto extraível foram conferidas por programa contra o texto da
  página indicada, desconsiderando quebras de linha e hifens. Números colados ao fim de palavras ou entre
  parênteses são chamadas de referência do original. Há duas exceções:
  - Benjamini e Hochberg é PDF digitalizado sem camada de texto e foi lido na página renderizada.
  - As fórmulas de Fischer, Barry e Ramdas foram transcritas da página, porque a extração corrompe os
    símbolos matemáticos.
- **Fontes:**
  - Barros et al. e Carvalho et al. estão em `pdf/`.
  - Oliveira et al. e Sá et al. foram baixados do SciELO.
  - Fischer et al. foi baixado do arXiv.
  - Benjamini e Hochberg é a cópia JSTOR hospedada na página do primeiro autor.

## Resumo

| ID | Afirmação, abreviada | Situação | Referências (número na lista) |
|---|---|---|---|
| A01 | delegacia especializada em 38 de 496 municípios | Fonte de dados, conferida na base | 1 |
| A02 | a distribuição não é homogênea | Sustenta | 2, 3 |
| A03 | estudos em municípios brasileiros usam autocorrelação espacial | Sustenta | 2, 4 |
| A04 | instabilidade das taxas em municípios pequenos e desfechos raros | Sustenta | 5 |
| A05 | multiplicidade e falsos positivos | Sustenta | 6 |
| A06 | subnotificação reconhecida e variável entre territórios | Sustenta, com ressalva | 2, 4 |
| A10 | fonte dos dados: divulgação da SSP-RS | Fonte de dados | 7 |
| A11 | populações municipais: estimativas do IBGE | Fonte de dados, com ressalva | 8 |
| A12 | indicador local (LISA) | Origem do método; texto completo não lido | 9 |
| A07 | ajuste de Assunção e Reis | Origem do método; **texto completo não obtido** | 10 |
| A08a | piso do p por permutação | Sustenta | 11 |
| A08b | regra de Benjamini-Hochberg | Sustenta | 6 |
| A09 | repositório público com versão etiquetada | Repositório citado; **etiqueta do artigo a criar** | 12 |

As linhas seguem a ordem do texto. São 12 referências na lista; o limite da RESS é 30.

---

## A01

**Afirmação (reescrita em 2026-11-03):** «A violência contra a mulher é problema de saúde pública e de
segurança, e os serviços especializados que a atendem distribuem-se de modo desigual entre os
municípios: no Rio Grande do Sul, em 2023, 38 dos 496 municípios que responderam ao quesito declararam
ter delegacia especializada no atendimento à mulher [n].»

**Situação: fonte de dados, conferida na base publicada.** A frase anterior («é no município que
funcionam os serviços de acolhimento, a delegacia...») não tinha sustentação e foi substituída. A
nova restringe-se ao que a MUNIC mede. A citação é da publicação do IBGE, e não do CSV processado
do repositório.

**Referência 1.** Instituto Brasileiro de Geografia e Estatística. Pesquisa de Informações Básicas
Municipais – MUNIC 2023: base de dados [Internet]. Rio de Janeiro: IBGE; 2024 [citado 2026 nov 3].
Disponível em: https://ftp.ibge.gov.br/Perfil_Municipios/2023/Base_de_Dados/Base_MUNIC_2023.xlsx

Passagens da base publicada, `Base_MUNIC_2023.xlsx`. O SHA-256 `511d50a2…6c759` confere com
`data/processed/rede_atendimento_proveniencia.csv`.

> Aba «Dicionário», quesito 6.3: «Estrutura existente» / «Existe no município:» / «Delegacia
> especializada no Atendimento à Mulher | MSEG168» (linhas 702–711 da aba)

> Aba «Dicionário», rodapé do bloco de segurança pública: «Fonte: IBGE, Pesquisa de Informações
> Básicas Municipais - 2023»

**Contagem, feita por programa sobre a aba «Segurança Pública»** e filtrada pelos códigos de município
iniciados em 43 (497 municípios):

| MSEG168 | Municípios |
|---|---:|
| Sim | 38 |
| Não | 286 |
| «-» (marcaram «Nenhuma das citadas», MSEG1611 = Sim) | 172 |
| Não informou | 1 |

- 38 «Sim» sobre 496 respondentes, ou seja, 497 menos o «Não informou».
- O «-» é ausência porque coincide exatamente com MSEG1611 = Sim, como em `src/fetch_rede_atendimento.py`.
- A contagem confere com `data/processed/rede_atendimento_municipio.csv`: 38 `tem`, 458 `nao_tem`,
  1 `sem_resposta`.
- **Ressalva:** a MUNIC é autodeclarada pela prefeitura. A frase diz «declararam», não «têm».

## A02

**Afirmação:** «Saber como os registros se distribuem entre municípios é, portanto, condição para dirigir
a resposta — e a distribuição não é homogênea [n,n].»

**Situação: sustenta**, quanto a "a distribuição não é homogênea", que é o que o marcador apoia.

**Referência 2.** Oliveira MR, Madeiro AP, Nascimento FF, Andrade JX, Rodrigues MTP, Mascarenhas MDM.
Rev Bras Epidemiol. 2024;27:e240030.

> «Constatou-se, neste estudo, heterogeneidade espacial nas taxas brutas de notificações de estupro por
> parceiro íntimo no Nordeste, com conglomerados mais altos nos estados do Ceará e de Pernambuco.» (p. 8)

**Referência 3.** Sá YRC, Moi PCP, Galvão ND, Silva AMC, Moi GP. Rev Bras Epidemiol.
2021;24(Supl 1):e210016.

> «The results of the present study show a very uneven distribution of the femicide rates per 100
> thousand women in Sergipe’s municipalities in the period studied» (p. 7)

> «There was not a random distribution of this rate with positive spatial autocorrelation (I = 0.0993881;
> p = 0.001 for 999 permutations).» (p. 5)

## A03

**Afirmação:** «Estudos que descrevem essa distribuição em municípios brasileiros recorrem a
estatísticas de autocorrelação espacial, que identificam agrupamentos de valores semelhantes em áreas
vizinhas [n,n].»

**Situação: sustenta.** Os dois estudos têm o município como unidade e usam o Moran global e local.

**Referência 4.** Barros SC, Oliveira CM, Silva APSC, Melo MFO, Pimentel DR, Bonfim CV. Rev Esc Enferm
USP. 2021;55:e03770.

> «Estudo ecológico que considerou como unidade espacial de análise os municípios do estado de
> Pernambuco e as regiões de saúde.» (p. 2)

> «Quanto mais próximo de 1, maior a semelhança entre os municípios vizinhos em relação à mortalidade.
> Para a delimitação das áreas críticas e de transição, bem como a identificação de clusters,
> empregou-se o índice de Moran local (Local Indicators of Spatial Association – LISA).» (p. 2)

**Referência 2.** Oliveira MR et al., 2024.

> «Na análise espacial, adotou-se o Índice Global e Local de Moran (IGM/ILM) univariado. Para a criação
> desse modelo, foi empregada na cartografia toda a extensão da macrorregião nordestina, tendo como
> unidades de análises os municípios e como evento de interesse a taxa de estupro.» (p. 2)

Dos oito PDFs, só Barros et al. tem o município como unidade e aplica Moran à violência contra a mulher:
- Bahia et al. usam microrregião, e Veiga e Bushatsky, mesorregião.
- Moroskoski et al. não aplicam Moran à taxa.
- Ceccon et al. tratam de grupos etários, não de mulheres.

Por isso a segunda referência veio do SciELO.

## A04

**Afirmação:** «A primeira é a instabilidade das taxas: municípios pequenos produzem taxas muito variáveis
a partir de poucos eventos, e desfechos raros agravam o problema [n].»

**Situação: sustenta.**

**Referência 5.** Carvalho AXY, Silva GDM, Almeida Júnior GR, Albuquerque PHM. Cad Saude Publica.
2012;28(7):1249-62.

> «Quando os municípios são pequenos, a estimação de taxas brutas é pouco indicada. Por serem pouco
> populosos, o baixo número de casos observados leva a estimativas pouco representativas ou até
> distorcidas e, por isso, com alta variabilidade 1.» (p. 1249)

> «A taxa bayesiana empírica diminui a variabilidade das estimativas ao restringir a flutuação aleatória
> ocasionada pelos eventos raros.» (p. 1251)

## A05

**Afirmação:** «A segunda é o número de testes: avaliar quinhentas áreas simultaneamente exige controle
de multiplicidade, sem o qual a quantidade de falsos positivos deixa de ser desprezível [n].»

**Situação: sustenta.**

**Referência 6.** Benjamini Y, Hochberg Y. J R Stat Soc Series B Stat Methodol. 1995;57(1):289-300.

> «When pursuing multiple inferences, researchers tend to select the (statistically) significant ones
> for emphasis, discussion and support of conclusions. An unguarded use of single-inference procedures
> results in a greatly increased false positive (significance) rate.» (p. 289; lida na página
> renderizada)

## A06

**Afirmação:** «A subnotificação da violência contra a mulher é reconhecida, e varia entre territórios
conforme a capacidade de acolhimento e a disposição de denunciar [n,n].»

**Situação: sustenta, com ressalva.**

**Referência 4.** Barros SC et al., 2021. A passagem atravessa a quebra de página, e o cabeçalho corrido
da p. 7 foi omitido.

> «Ainda é frequente, em municípios localizados em regiões menos urbanas, as mulheres [p. 6 | p. 7] não
> denunciarem a violência doméstica ou estupros, principalmente em ambientes familiares(26). Geralmente
> pelo medo do julgamento, que pode ser praticado pela sociedade local, medo de represálias e maior
> dificuldade de acesso a serviços de proteção às vítimas de violência, como as delegacias
> especializadas de atendimento à mulher(26).» (p. 6-7)

**Referência 2.** Oliveira MR et al., 2024.

> «Primeiro, é possível que tenha ocorrido subnotificação do estupro, tanto por conta da dificuldade de
> identificação da violência pela mulher como por provável barreira de acesso às unidades de saúde, uma
> vez que há número ainda insuficiente de unidades com atendimento especializado à violência sexual,
> estas geralmente concentradas em municípios de maior porte43.» (p. 8)

**Ressalva:** as duas passagens são discussão, não resultado, e ambas remetem a fontes próprias: a
referência 26 de Barros et al. e a 43 de Oliveira et al. Elas sustentam a frase como está, mas um
parecerista pode pedir a fonte primária. A citação, assim, é de autores que afirmam, não de quem
mediu a variação territorial da subnotificação.

## A07

**Afirmação:** «A autocorrelação foi estimada pelo índice de Moran global e pelo indicador local de
associação espacial (LISA) [n], ambos com o ajuste proposto por Assunção e Reis [n].»
O marcador é o segundo da frase; o primeiro é A12.

**Situação: citação de origem de método. O texto completo não foi obtido; não há passagem
transcrita.**

**Referência 10.** Assunção RM, Reis EA. A new proposal to adjust Moran's I for population density. Stat
Med. 1999;18(16):2147-62. doi:10.1002/(SICI)1097-0258(19990830)18:16<2147::AID-SIM179>3.0.CO;2-I

**Caminhos tentados:**

| Data | Caminho | Resultado |
|---|---|---|
| 2026-11-02 | Unpaywall, pelo DOI | `is_oa: false`; sem versão de acesso aberto |
| 2026-11-02 | Cópia do autor (páginas pessoais e institucionais) | Não localizada |
| 2026-11-02 | Cópia hospedada em outro sítio | Não localizada |
| 2026-11-03 | Portal de Periódicos CAPES | Não disponível, segundo informou o autor do manuscrito; a consulta não foi refeita aqui |

**Por que entra sem passagem:** a referência é a origem do método aplicado nos Métodos, e não fonte de
uma afirmação sobre o conteúdo do artigo. Entra pelo mesmo critério de A12 (Anselin): atribui o
método e não sustenta nenhuma afirmação específica. Por isso a frase dos Métodos passa a
separar a atribuição («o ajuste proposto por Assunção e Reis») da explicação da variância das taxas,
que é propriedade geral de uma taxa e não depende de fonte.

Se o PDF for obtido, transcrever a passagem que descreve o ajuste e revisar esta entrada.

## A08a e A08b

O antigo A08 (`[n,n]`) foi dividido quando a frase foi reescrita, para que cada fonte fique presa à
expressão que de fato enuncia. A derivação passou a ser declarada no texto.

**Afirmação:** «O menor valor p obtenível com m permutações é 1/(m+1) [n], e o procedimento de
Benjamini-Hochberg, com n áreas ao nível q, rejeita as hipóteses até o maior posto i cujo valor p
ordenado não excede q·i/n [n]. Combinando as duas expressões, o que nenhuma das duas fontes enuncia,
rejeitar uma hipótese nesse piso exige m+1 ≥ n/(q·i).»

### A08a — piso do p por permutação

**Situação: sustenta.**

**Referência 11.** Fischer L, Barry T, Ramdas A. arXiv:2404.15586v4, 2025. As fórmulas foram transcritas
da página.

> «In a classical Monte Carlo permutation test, we observe some test statistic Y0, generate B additional
> test statistics Y1, . . . , YB and calculate the permutation p-value by
> P_B^perm = (1 + Σ_{t=1}^{B} 1{Yt ≥ Y0}) / (1 + B). (1)
> In order to be able to reject the null hypothesis at level α, we would need to generate at least
> B ≥ 1/α − 1 permuted datasets with corresponding test statistics.» (p. 2)

Pela fórmula (1), o menor valor possível é 1/(1+B), que é o 1/(m+1) do manuscrito.

### A08b — regra de Benjamini-Hochberg

**Situação: sustenta.**

**Referência 6.** Benjamini e Hochberg, 1995, lida na página renderizada.

> «let k be the largest i for which P(i) ≤ (i/m) q*; then reject all H(i), i = 1, 2, . . ., k.» (p. 293)

### Sobre a desigualdade

- m+1 ≥ n/(q·i) resulta de combinar o piso (referência 11) com a regra (referência 6). O manuscrito agora
  o declara.
- Fischer et al. enunciam o caso de pior situação, em que um único p pequeno é testado a α/M; esse
  caso corresponde a i = 1:

> «Even if we use more powerful multiple testing procedures such as the Benjamini-Hochberg (BH) procedure
> [5], this lower bound for the total number of permutations usually remains. The problem is that B needs
> to be chosen in a manner that protects against the worst case in which all p-values are large except
> for one that is then essentially tested at level α/M.» (p. 2)

- "Nenhuma das duas fontes enuncia" vale, portanto, para a forma geral, com i. O caso i = 1 está em
  Fischer et al.
- **Autoria:** a v1 do arXiv (abril de 2024) era de Fischer e Ramdas; a v4 (agosto de 2025), a lida,
  inclui Timothy Barry. A autoria foi corrigida em `decisoes_artigo_espacial.md`. O manuscrito não
  nomeia os autores.

## A09

**Afirmação:** «O código, os dados processados e os parâmetros de execução estão depositados em
repositório público, em versão etiquetada correspondente aos resultados aqui apresentados [n].»

**Situação: repositório citado; a etiqueta do artigo ainda não existe.**

- A referência é o próprio repositório (`github.com/Alexandrogschafer/violencia-mulheres-rs`). Não há
  passagem a transcrever.
- A versão etiquetada deste artigo ainda não existe. O repositório tem as etiquetas `v1.0.0` e
  `artigo-reciis-v1`, de outros trabalhos. A afirmação só fica verdadeira quando a etiqueta for criada.
- Em 2026-11-03 o repositório entrou na lista como **referência 11**, por decisão do autor, com a
  autoria e o título de `CITATION.cff`, o DOI conceitual do Zenodo (10.5281/zenodo.21403499) e a
  versão marcada como «etiqueta do artigo a criar». Ao criar a etiqueta, substituir pelo DOI da versão.

## A10 — fonte dos dados

**Afirmação:** «Os dados provêm dos registros administrativos da Secretaria da Segurança Pública do Rio
Grande do Sul, em planilhas de divulgação pública por município e ano [n].»

**Situação: fonte de dados.** Não há afirmação a sustentar; a referência identifica a publicação.

**Referência 7.** Rio Grande do Sul, Secretaria da Segurança Pública. Indicadores da violência contra a
mulher – Lei Maria da Penha. Página consultada em 2026-11-02:
https://www.ssp.rs.gov.br/indicadores-da-violencia-contra-a-mulher

- Título da página, conferido no HTML: «Indicadores da Violência Contra a Mulher - Lei Maria da Penha».
  A página oferece as planilhas «Indicadores de violência contra a mulher geral e por município <ano>».
- As planilhas usadas trazem, na aba Geral, a célula «Fonte: SIP/PROCERGS - Atualizado em <data>». As
  datas de atualização vão de 9/1/2018 (2012–2017) a 3/7/2026 (2025 e 2026), segundo
  `outputs/tables/proveniencia_dados_brutos.csv`.
- **Anomalia, não corrigida:** a página publica hoje a planilha de 2025 «Atualizado em outubro de
  2026». O repositório usa a de 3/7/2026. Os números do artigo correspondem, portanto, a uma extração
  anterior à vigente, o que é coerente com a ressalva dos Métodos sobre revisão retroativa. Falta
  decidir se a extração será atualizada antes da submissão.

## A11 — estimativas populacionais

**Afirmação:** «As populações municipais anuais vieram das estimativas do IBGE [n].»

**Situação: fonte de dados, com ressalva.**

**Referência 8.** Instituto Brasileiro de Geografia e Estatística. Estimativas de População: tabela
6579, população residente estimada. Sistema IBGE de Recuperação Automática (SIDRA):
https://sidra.ibge.gov.br/tabela/6579

- Metadados conferidos na API de agregados do IBGE: tabela 6579, «População residente estimada»,
  pesquisa «Estimativas de População».
- **Ressalva: a frase não descreve exatamente o que foi feito.** Segundo `src/fetch_populacao.py`:
  - 2022 não vem das estimativas, e sim do Censo 2022 (tabela 4709), porque não há estimativa em ano de
    censo;
  - 2023 não existe em fonte oficial: o IBGE não publicou a estimativa municipal, e o valor foi
    interpolado linearmente entre 2022 e 2024.

  A frase precisa mencionar as duas exceções, e o Censo 2022 entra como segunda referência do IBGE.
  O Censo 2022 também é a fonte da razão feminina, e o Censo 2010 a da verificação de estabilidade.
  Nenhum dos dois tem marcador.

## A12 — indicador local

**Afirmação:** «A autocorrelação foi estimada pelo índice de Moran global e pelo indicador local de
associação espacial (LISA) [n], ambos com o ajuste proposto por Assunção e Reis [n].» O marcador é o
primeiro da frase.

**Situação: citação de origem de método. O texto completo não foi lido.**

**Referência 9.** Anselin L. Local indicators of spatial association—LISA. Geogr Anal.
1995;27(2):93-115. doi:10.1111/j.1538-4632.1995.tb00338.x

- Os metadados vêm do registro do DOI no Crossref, conferido em 2026-11-02: título «Local Indicators of
  Spatial Association—LISA»; autor Luc Anselin; Geographical Analysis, v. 27, n. 2, p. 93-115, abril
  de 1995.
- O PDF não foi obtido: a editora bloqueou o download automático, embora o Unpaywall registre acesso
  aberto. O texto completo não foi lido. A referência entra por instrução, como citação de origem do
  método. Ela não sustenta nenhuma afirmação específica sobre o conteúdo do artigo.

---

## Observações fora dos marcadores

- **Censos 2022 e 2010 sem marcador.** Os Métodos usam a razão feminina do Censo 2022 e a comparação
  com o Censo 2010, sem referência. Ver A11.
- **Arbia, Cardile, Nardelli e Salvini (arXiv:2610.13472)** constam em `decisoes_artigo_espacial.md`
  como referência a citar, mas o manuscrito não tem frase que os cite.
