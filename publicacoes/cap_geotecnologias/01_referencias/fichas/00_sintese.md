# Síntese do fichamento — Seção 2 (Fundamentação)

Cobre as seis referências originalmente pedidas para verificação, as duas
variantes de Roth encontradas na pasta, e três referências adicionais
fichadas numa rodada posterior (Itikawa, Beyer, Bastos & Camboim). Não
cobre as demais referências já citadas em `02_fundamentacao.md`
(Sousa/Uchôa/Barreto, Veiga/Bushatsky, Série Capacitação em
Geoprocessamento em Saúde, Peng, Wilkinson, Smith) — o próprio arquivo já
as marca como verificadas em sua seção "Notas para revisão", e não fazem
parte do lote pedido nesta tarefa.

Nenhum `.bib` existe no repositório (busca confirmada em todo o projeto) —
por isso a coluna abaixo é "Não" para todas as linhas, sem exceção.

| Referência | Está no `.bib`? | Sustenta qual seção do capítulo | Pendência |
|---|---|---|---|
| `brewer_pickle_2002` | Não (nenhum `.bib` no repo) | §2.4 — "quantis com cinco classes" na tabela de decisões da Seção 5 (nota do próprio §2.4: hoje **sem apoio verificado** no texto) | PDF não disponível. Não fichado. |
| `roth_2012` (identificado como ROTH, R. E. "Cartographic interaction primitives: Framework and synthesis." *The Cartographic Journal*, v.49, n.4, p.376-395, 2012 — via referência [26] de `roth_2013b.pdf`, não por conhecimento externo) | Não | Tabela de decisões da Seção 5 — nomeação do "operador de recuperação" (nota do §2.4: "não reintroduzir a expressão... enquanto não se resolver") | PDF não disponível. Não fichado. Ver achado abaixo sobre `roth_2013b`. |
| `openshaw_taylor_1979` | Não | §2.3 — formulação canônica do MAUP (hoje contornada citando BRASIL, 2024) | PDF não disponível. Não fichado. |
| `robinson_1950` | Não | §2.3 — demonstração da falácia ecológica (hoje contornada citando BRASIL, 2024) | **PDF errado foi fornecido**: `RobinsonFinalRG.pdf` é "A correction to Robinson's Ecological Correlations and the Behavior of Individuals" (te Grotenhuis, Eisinga, Subramanian — carta/errata, aparentemente 2009, sobre o artigo original), não o artigo de W. S. Robinson de 1950. Não fichado como `robinson_1950`. |
| `slocum_2022` | Não | §2.4 — método de classificação, número de classes, esquemas de cor, impresso vs. interativo | PDF não disponível. Não fichado. |
| `haklay_2008` | Não | Não identificável no texto atual de §2 — citado só na lista final de pendências do arquivo, sem afirmação específica atribuída a ele no corpo do texto | PDF não disponível. Não fichado. |
| `roth_2013a` (JOSIS, "Interactive maps: what we know and what we need to know") | Não | §2.4 — par representação/interação cartográfica; *brushing*, *focusing*, *linking* como operadores mais recorrentes | Já marcado como "verificado nesta rodada" pelo próprio `02_fundamentacao.md`. Não fichado formalmente em `fichas/` nesta tarefa (não foi pedido). Renomeado nesta sessão de `roth_2013.pdf`. |
| `roth_2013b` (IEEE TVCG, "An empirically-derived taxonomy of interaction primitives...") | Não | Ver achado abaixo | Fichado. `fichas/roth_2013b.md`. Renomeado de `roth_2013_2.pdf`. |
| `itikawa_2023` | Não | **Não citada em `02_fundamentacao.md`.** Encaixe temático mais próximo: §2.1, como precedente adicional ao lado de Veiga e Bushatsky (2021) — mesma família de estudo (geoprocessamento de microdados de violência contra a mulher obtidos por LAI, comparando padrão absoluto vs. relativo). Sugestão minha, não confirmação de citação existente. | **Fichado nesta rodada** (`fichas/itikawa_2023.md`). Decisão de uso no texto é sua. |
| `beyer_2015` | Não | **Não citada em `02_fundamentacao.md`.** Não há encaixe claro nas quatro decisões que §2 cobre hoje (registro administrativo, taxa, unidade de agregação, classificação/cor) — o objeto da revisão é interpretação epidemiológica de IPV, não escolha metodológica de mapeamento. Poderia servir a uma seção de discussão/interpretação dos padrões espaciais (ex. Seção 6), se existir. | **Fichado nesta rodada** (`fichas/beyer_2015.md`). Sem seção de destino óbvia no capítulo atual. |
| `bastos_camboim_2025` | Não | **Não citada em `02_fundamentacao.md`.** Tema é arquitetura de publicação de mapas na web (WMS/GeoJSON/Vector Tiles) — mais próximo do fluxo geotecnológico do portal (Seção 4, pipeline/publicação) do que da Fundamentação metodológica de §2. | **Fichado nesta rodada** (`fichas/bastos_camboim_2025.md`). Sem seção de destino óbvia em §2. |

## Achado que precisa de decisão sua (não decidi por conta própria)

A nota de `02_fundamentacao.md` associa o "operador de recuperação" da
tabela de decisões da Seção 5 a Roth (2012) — não consultado. Mas
`roth_2013b.pdf`, que agora **está** disponível e fichado, também define e
localiza um operador **retrieve** com página exata (p. 2363), derivado
empiricamente do próprio estudo de entrevistas + *card sorting* relatado
nesse artigo — não é a mesma obra que Roth (2012) (títulos e estudos
diferentes, confirmado pela lista de referências do próprio `roth_2013b`,
item [26]).

Isso não resolve automaticamente a pendência como estava formulada — só
muda o que está disponível: agora há uma fonte verificada com um operador
"retrieve" citável, mas é uma taxonomia diferente da que a nota original
tinha em mente. Três caminhos possíveis, para você decidir (não decidi
nenhum): (a) continuar buscando Roth (2012) especificamente; (b) citar
`roth_2013b` no lugar dele para o operador *retrieve*; (c) citar as duas
obras juntas, deixando explícito que são taxonomias distintas do mesmo
autor. Até a decisão, a instrução do próprio capítulo — não reintroduzir
"operador de recuperação" — continua valendo, por segurança.
