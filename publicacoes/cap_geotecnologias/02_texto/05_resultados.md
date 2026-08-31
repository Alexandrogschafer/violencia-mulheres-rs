# 5. Resultados: o portal e o mapeamento das ocorrências

> **Rascunho v2** — 30/08/2026. Incorpora o teste de sazonalidade do
> litoral, a numeração definitiva das figuras (3, 4 e 5) e a remoção da
> subseção sobre uso aplicado. Citações em formato autor-data, a converter
> para a norma da editora.

## 5.1 O portal

O produto público do fluxo descrito na seção anterior é um portal web de
acesso aberto, organizado em oito páginas. A página inicial apresenta a
série histórica estadual por categoria de ocorrência; uma página de
resultados reúne os testes estatísticos aplicados às séries; uma página de
mapas concentra a representação territorial das taxas; uma página de
consulta municipal permite localizar um município específico e ver seus
valores; e uma página de dados e metodologia documenta a origem dos
arquivos, as transformações aplicadas e as limitações reconhecidas.

**[FIGURA 2 — Captura de tela do portal, página de mapas. A gerar.]**

A interação com o mapa é estreita por decisão de projeto, justificada em
4.4: o usuário pode filtrar por categoria de ocorrência, recuperar o
valor de um município por sobrevoo ou clique e deslocar-se e aproximar-se
sobre a base cartográfica (ROTH, 2013b). Não há filtros de período, não
há reclassificação pelo usuário, não há sobreposição de camadas.

## 5.2 Do interativo ao impresso

Os mapas reproduzidos neste capítulo diferem dos publicados no portal em
um aspecto: a classificação. O portal representa as taxas por interpolação
contínua sobre uma rampa sequencial, sem divisão em classes; as figuras
aqui apresentadas usam classificação por quantis em cinco classes.

A divergência é deliberada e decorre do meio. No mapa interativo, o
operador de recuperação cumpre funcionalmente o papel das fronteiras de
classe: o leitor que precisa do valor exato de um município consulta o
valor, e a rampa contínua serve apenas para dar a impressão geral da
distribuição. No impresso não há consulta possível, e a classificação
passa a ser o único recurso de leitura comparativa disponível.

Os próprios cortes obtidos mostram que a escolha do método se
justificava, e não era mera preferência. Em Ameaça, os quatro
primeiros cortes distribuem-se entre 91,5 e 373,7 casos por 100 mil
habitantes, enquanto a classe superior sozinha se estende de 373,7 a
697,7: metade da amplitude total da variável concentra-se na última
classe, ocupada por poucos municípios. Sob normalização contínua entre
mínimo e máximo, esses poucos municípios comprimiriam todo o restante do
estado na base da rampa, e o mapa exibiria os extremos em lugar da
distribuição. O mesmo padrão de cauda longa aparece em Lesão Corporal
(191,3 a 365,9 na classe superior) e, de forma ainda mais acentuada, em
Estupro (26,4 a 60,7).

Um segundo aspecto distingue as figuras impressas: elas adotam um piso
populacional de 5.000 habitantes, abaixo do qual o município não recebe
cor de taxa e é representado em cinza neutro, com entrada própria na
legenda. O critério exclui 231 dos 497 municípios do estado. Essa
proporção — quase metade do território municipal gaúcho sem representação
de taxa — não é um artefato do limiar escolhido, e sim expressão de uma
característica estrutural do estado, discutida na Seção 6. Diferentemente
da classificação, esta divergência em relação ao portal não se justifica
pelo meio, e é tratada como tal em 6.4.

## 5.3 A distribuição territorial das taxas

As três categorias mapeadas apresentam padrões espaciais nitidamente
distintos, o que por si já constitui um resultado: a violência contra a
mulher não se distribui como fenômeno único no território, e políticas
desenhadas a partir de um indicador agregado tenderiam a errar o alvo em
pelo menos duas das três categorias.

### Ameaça

**[FIGURA 3 — Ameaça, taxa por 100 mil habitantes, 2018–2025.]**

Ameaça é a categoria de maior magnitude absoluta e a que desenha o padrão
regional mais coerente: uma concentração no norte e noroeste do estado. Os
municípios de maior taxa são Iraí (697,7), Palmeira das Missões (592,3),
Lagoa Vermelha (574,0), Soledade (558,4) e Ametista do Sul (550,6). No
nível dos COREDEs, o ordenamento reforça a leitura: Médio Alto Uruguai
(450,3), Celeiro (431,5) e Alto da Serra do Botucaraí (422,0) ocupam as
primeiras posições, enquanto Serra (237,8), Sul (251,6) e Centro-Sul
(265,0) fecham a lista.

### Lesão Corporal

**[FIGURA 4 — Lesão Corporal, taxa por 100 mil habitantes, 2018–2025.]**

Lesão Corporal desenha um padrão diferente e mais compacto. As cinco
maiores taxas do estado pertencem a municípios contíguos do litoral norte:
Imbé (365,9), Cidreira (360,4), Tramandaí (316,9), Balneário Pinhal
(316,8) e Capão da Canoa (287,7). O COREDE Litoral lidera a categoria
(257,4), seguido de Norte (241,6). Nas últimas posições aparecem Vale do
Taquari (118,9), Vale do Caí (130,2) e Serra (138,0).

### Estupro

**[FIGURA 5 — Estupro, taxa por 100 mil habitantes, 2018–2025.]**

Estupro apresenta as menores magnitudes e a distribuição mais dispersa. O
litoral volta a aparecer no topo — Cidreira (60,7), Palmares do Sul
(44,1), Arroio do Sal (40,8), Imbé (38,6), Xangri-Lá (36,8) —, e o COREDE
Litoral novamente lidera (31,0), acompanhado de Alto Jacuí (27,2) e
Metropolitano Delta do Jacuí (25,0). Convém, porém, ler estes valores com
reserva: a liderança de Cidreira corresponde a 82 registros acumulados em
oito anos, e vários municípios do topo têm contagens de duas dezenas.

## 5.4 Dois padrões transversais

Duas regularidades atravessam as três categorias e merecem exame.

### O litoral e o denominador sazonal

Cidreira e Tramandaí figuram entre os quinze maiores nas três categorias,
e Imbé em duas. Coincidência dessa ordem em fenômenos com dinâmicas
distintas sugere fator comum, e a distribuição mensal dos registros
permite examiná-lo.

Calculando a razão entre os casos do trimestre de verão (dezembro a
fevereiro) e os do trimestre de inverno (junho a agosto), os nove
municípios do COREDE Litoral apresentam valores de 1,72 em Ameaça, 1,62 em
Estupro e 2,53 em Lesão Corporal. Um grupo de controle de nove municípios
não litorâneos, pareado individualmente por população residente, registra
1,24, 1,39 e 1,37; o conjunto do estado, 1,23, 1,18 e 1,45. Em Lesão
Corporal, o mês de janeiro concentra sozinho 16,0% dos registros anuais no
litoral, contra 10,3% no grupo de controle e 10,4% no estado.

**[TABELA 1 — Razão verão/inverno por grupo e categoria, 2018–2025.]**

A proximidade entre o grupo de controle e o agregado estadual é o
elemento decisivo da comparação: ela indica que não se trata da
sazonalidade geral já identificada nas séries gaúchas, e sim de um efeito
específico do litoral. A leitura mais direta é que o denominador da taxa —
população residente estimada — não acompanha a variação sazonal da
população efetivamente presente nesses municípios, de modo que a taxa
anual superestima a incidência a que está exposta a população residente.
Não é possível, com os dados disponíveis, separar o efeito de denominador
de eventuais efeitos de contexto associados à temporada de veraneio; para
os fins deste capítulo, basta registrar que a taxa municipal anual é um
indicador inadequado para municípios de população fortemente flutuante, e
que sua leitura exige a ressalva correspondente.

O resultado ilustra um ponto de método com alcance além deste caso: a
adequação de uma taxa depende de que numerador e denominador se refiram à
mesma população, e essa correspondência pode falhar por razões temporais,
não apenas categoriais. É uma verificação de baixo custo, disponível
sempre que a série tenha granularidade inferior à do denominador, e que
raramente é feita.

### As grandes cidades

Nenhuma das seis maiores cidades do estado aparece entre os quinze
primeiros em qualquer categoria. Em Ameaça, Porto Alegre registra 250,2 e
Caxias do Sul 232,5 — ambas na segunda das cinco classes. O contraste com
a concentração absoluta de casos é instrutivo: a capital responde por
parcela expressiva do total estadual de ocorrências e, ainda assim, ocupa
posição intermediária quando a contagem é convertida em taxa. É a
diferença entre onde há mais casos e onde há maior incidência — distinção
que a cartografia de taxas torna visível e que a contagem absoluta oculta.

Em Lesão Corporal o quadro se inverte parcialmente: Uruguaiana (216,7),
Pelotas (201,1), Santa Maria (198,5) e Porto Alegre (198,0) situam-se na
classe superior, ao passo que Caxias do Sul (137,1) permanece na terceira.
A ausência de um padrão único por porte populacional reforça a leitura da
seção anterior: as categorias respondem a dinâmicas territoriais
distintas.

## 5.5 O efeito da unidade de agregação

A disponibilidade de três níveis de agregação para os mesmos dados —
município, COREDE e região geográfica intermediária — permite demonstrar
empiricamente o problema discutido na Seção 2. A Tabela 2 apresenta a
amplitude das taxas em cada nível.

**[TABELA 2 — Amplitude das taxas por nível de agregação, 2018–2025.]**

| Categoria | Nível | Unidades | Mín. | Máx. | Razão |
|---|---|---:|---:|---:|---:|
| Ameaça | Município | 266 | 91,5 | 697,7 | 7,6 |
| | COREDE | 28 | 237,8 | 450,3 | 1,9 |
| | Região intermediária | 8 | 256,3 | 404,4 | 1,6 |
| Estupro | Município | 266 | 1,8 | 60,7 | 34,3 |
| | COREDE | 28 | 9,7 | 31,0 | 3,2 |
| | Região intermediária | 8 | 14,5 | 24,6 | 1,7 |
| Lesão Corporal | Município | 266 | 49,3 | 365,9 | 7,4 |
| | COREDE | 28 | 118,9 | 257,4 | 2,2 |
| | Região intermediária | 8 | 137,1 | 195,1 | 1,4 |

Nenhum registro foi acrescentado ou removido entre os três níveis: são os
mesmos casos, o mesmo período e a mesma população. O que muda é apenas a
fronteira de agregação. Ainda assim, a desigualdade territorial medida
como razão entre o valor máximo e o mínimo cai, em Estupro, de 34,3 vezes
na escala municipal para 1,7 vez na escala das oito regiões
intermediárias. Um relatório que descrevesse a distribuição estadual de
Estupro a partir das regiões intermediárias concluiria, com razão
aritmética, que o fenômeno é relativamente homogêneo no território
gaúcho — conclusão que a escala municipal desmente.

Trata-se do efeito de escala do problema da unidade de área modificável,
discutido em 2.3 e aqui manifesto no material empírico do próprio
estudo: para uma mesma população e um mesmo conjunto de casos, a
definição das fronteiras de agregação altera o resultado obtido. A
implicação prática é direta: a escolha da
unidade territorial não é uma decisão de conveniência a ser resolvida pela
disponibilidade dos dados, mas parte da construção do resultado. O
município foi adotado neste trabalho por ser a unidade em que a fonte
publica e a unidade em que boa parte da política pública de atendimento
opera — mas essa escolha determina o que o mapa pode mostrar, e um
território representado como desigual em uma escala pode aparecer como
homogêneo em outra sem que nada tenha mudado no fenômeno.

---

## Notas para revisão

### Mudanças em relação à v1

- Subseção sobre Uruguaiana removida.
- Numeração das figuras acertada: Ameaça = Figura 3, Lesão Corporal =
  Figura 4, Estupro = Figura 5, coerente com os arquivos já renomeados.
- O parágrafo sobre o litoral deixou de ser inferência e passou a
  resultado com evidência própria, ganhando subseção.
- Os dois padrões transversais foram promovidos a subseção 5.4, e o MAUP
  passou a 5.5.

### Verificações pendentes

- **Grupo de controle.** São Lourenço do Sul tem frente para a Lagoa dos
  Patos. Não está no COREDE Litoral e o efeito é grande e consistente nos
  nove pares, de modo que a conclusão não depende dele. Sugiro uma nota
  de rodapé registrando a ressalva, em vez de refazer o pareamento.
- **Concentração absoluta de Porto Alegre.** Mantive "parcela expressiva"
  porque o número de 12,2% do resumo do projeto refere-se a 2012–2026 e à
  categoria Geral, não ao recorte desta seção. Se quiser o valor exato,
  precisa recalcular para 2018–2025 por categoria.
- **COREDEs com poucos municípios elegíveis.** Retirei Campos de Cima da
  Serra (3 municípios elegíveis) e Produção (4) das enumerações do texto
  para não apoiar afirmação em agregados instáveis. Vale uma nota
  explicando o critério, ou reincluí-los com ressalva.
- **Vigência da divisão em COREDEs.** Precisa constar a data da divisão
  utilizada.

### Ainda em aberto

- Figuras 1 (fluxograma, Seção 4) e 2 (captura do portal) a produzir.
- Tabelas 1 e 2 a formatar conforme a norma da editora.

**Extensão:** cerca de 1.700 palavras, sem contar as tabelas.
