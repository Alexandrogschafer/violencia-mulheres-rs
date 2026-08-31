# roth_2013b

## Referência (ABNT completa, conforme a folha de rosto do PDF)

ROTH, Robert E. An empirically-derived taxonomy of interaction primitives for interactive cartography and geovisualization. **IEEE Transactions on Visualization and Computer Graphics**, v. 19, n. 12, p. 2356-2365, dez. 2013.

(Folha de rosto: autor único, Robert E. Roth, Assistant Professor, University of Wisconsin-Madison — p. 2356. Confirmado explicitamente que **não é** o mesmo artigo que `roth_2013a.pdf` — este é o IEEE TVCG, aquele é o JOSIS "Interactive maps: What we know and what we need to know".)

## O que é (2-3 linhas)

Artigo de pesquisa empírico, método misto: (1) um estudo de entrevistas semiestruturadas e (2) um estudo de *card sorting*, conduzidos com profissionais especialistas. Objeto: construir uma taxonomia de primitivas de interação (metas, objetivos, operadores, operandos) específica para mapas interativos e geovisualização (p. 2356, resumo).

## Afirmações centrais (com página)

1. A taxonomia final tem quatro dimensões, alinhadas a quatro dos sete estágios do modelo de "estágios de (inter)ação" de Norman: metas (*goals*), objetivos (*objectives*), operadores (*operators*) e operandos (*operands*) (p. 2363, Seção 6, Conclusion).
2. Os operadores dividem-se em dois grupos: cinco operadores habilitadores (*enabling* — import, export, save, edit, annotate) e doze operadores de trabalho (*work* — reexpress, arrange, sequence, resymbolize, overlay, reproject, pan, zoom, filter, search, retrieve, calculate) (p. 2356, resumo; detalhados em p. 2360-2363, Seções 5.2-5.3).
3. O estudo de entrevistas envolveu 21 usuários especialistas de mapas interativos, recrutados em sete domínios de aplicação (ex.: resposta a emergências, epidemiologia e saúde pública, análise de inteligência), com sessões de 60-90 minutos cada (p. 2357, Seção 3.1).
4. O estudo de *card sorting* envolveu 15 designers especialistas de mapas interativos, conduzido on-line pela ferramenta WebSort, com duas tarefas de ordenação (objetivos e operadores) (p. 2357-2358, Seção 3.3).
5. A confiabilidade das categorias foi menor para objetivos (63,0% de similaridade entre subamostras) do que para operadores (83,3%) (p. 2358-2359, Seção 3.4/4.1).

## Respostas às perguntas dirigidas

**Existe um operador "retrieve"? Definição exata e página.** Sim. Item (11) dos doze operadores de trabalho, definido em p. 2363 (Seção 5.3): "The retrieve operator describes interactions that request specific details about a map feature" (citação literal, <15 palavras). O texto complementa (paráfrase, mesma página): o retrieve é sinônimo de "accessing extra information", "accessing exact information" e "details-on-demand" usados em outras taxonomias citadas pelo autor, e é tipicamente implementado por manipulação direta (ex.: passar o cursor sobre uma feição), embora o autor observe que não é exclusivo desse estilo de interface.

**Taxonomia completa de operadores:**
- *Habilitadores* (5, p. 2360-2361, Seção 5.2): import, export, save, edit, annotate.
- *De trabalho* (12, p. 2361-2363, Seção 5.3): reexpress, arrange, sequence, resymbolize, overlay, reproject, pan, zoom, filter, search, **retrieve**, calculate.
- A taxonomia completa (4 dimensões) inclui ainda: metas — procure, predict, prescribe (p. 2359-2360, Seção 4.3); objetivos — identify, compare, rank, associate, delineate (p. 2359-2360, Seção 4.4); operandos — space-alone, attributes-in-space, space-in-time (alvo de busca) e elementary/general (nível de busca) (p. 2358-2359, Seção 4.2).

**Como o trabalho foi construído (empírico? de que tipo?):** Sim, empírico, método misto sequencial: (1) entrevistas semiestruturadas com 21 usuários especialistas, transcritas e codificadas por dois codificadores independentes, gerando 545 declarações de objetivos e 823 de operadores, filtradas para 138 e 155 (p. 2357-2358, Seção 3.2); (2) essas declarações, somadas a definições da literatura, alimentaram um estudo de *card sorting* guiado com 15 designers especialistas, analisado por *clustering* hierárquico de concordância par a par (p. 2357-2358, Seções 3.3-3.4).

## Não responde a

- Não trata de classificação de dados em mapas coropléticos (número de classes, método de classificação por quantis etc.) — o objeto do artigo é a interação com o mapa (operadores/objetivos), não a simbolização/classificação de dados.
- Não discute esquemas de cor.
- Não aborda especificamente mapas de taxas epidemiológicas nem mapas estáticos impressos — o objeto é mapa interativo em geral; "Epidemiology & Public Health" aparece só como um dos sete domínios de recrutamento dos entrevistados (p. 2357), sem tratamento específico do tema.
- Nota lateral (não é resposta a pergunta dirigida, mas relevante para localizar a literatura): a lista de referências deste artigo (p. 2364, ref. [26]) identifica **ROTH, R. E. "Cartographic interaction primitives: Framework and synthesis." The Cartographic Journal, v. 49, n. 4, p. 376-395, 2012** — este parece ser o "roth_2012" original pedido, que não está na pasta. Registro só porque apareceu na lista de referências deste PDF, não é conhecimento externo meu.
