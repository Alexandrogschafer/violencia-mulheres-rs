# Limite de 3.500 palavras da RESS: o que entra na conta

Verificação empírica feita em 2026-11-02. Contei as palavras de três artigos originais publicados na
*Epidemiologia e Serviços de Saúde* (RESS), seção a seção.

## Conclusão

**O limite de 3.500 palavras vale só para o corpo do texto.** Ficam fora o resumo, as referências e as
tabelas e figuras com suas legendas.

- **Corpo de texto corrido** (Introdução até a Conclusão, só a prosa, com subtítulos): **2.894 a 3.571
  palavras**, mediana de **2.928**. Os três artigos ficam perto de 3.500 ou abaixo. Um deles passa um pouco
  (3.571, +2%), o que cabe numa tolerância editorial ou na diferença entre o contador do Word e o meu.
- **Total do documento:** **5.157 a 6.314 palavras**, mediana de **5.819**. Fica de 1.650 a 2.800 palavras
  acima do limite, então o limite não pode estar contando tudo.
- **Corpo bruto**, contado literalmente de "Introdução" até imediatamente antes de "Referências": 3.864 a
  4.908 palavras, mediana de 4.508. Também passa de 3.500 nos três artigos. Isso porque esse trecho inclui o
  conteúdo das tabelas e figuras, as declarações finais e os cabeçalhos e rodapés de página. Logo, o
  conteúdo das tabelas também não entra no limite.

**Implicação para o artigo espacial:** o orçamento de 3.500 palavras vai para Introdução, Métodos,
Resultados, Discussão e Conclusão. Resumo, referências, tabelas, figuras e legendas ficam de fora. Para
ter folga, o alvo seguro é ficar em torno de 3.000 a 3.400 palavras, que é a faixa observada.

Ressalva: três artigos é uma amostra pequena. Artigos publicados podem ter sido aceitos com exceção ao
limite. Esta verificação não substitui a leitura das instruções aos autores, que eu não consultei aqui.

## Artigos analisados

Os três são os artigos mais recentes com o selo exato "ARTIGO ORIGINAL" no sumário do v. 35 (2026) no
SciELO. Excluí os itens dos números temáticos ("25 anos do EpiSUS", "EVIPNet") e os itens com esse selo
que são revisão ou relato de experiência. Baixei os PDFs em português com
`curl "https://www.scielo.br/j/ress/a/<id>/?format=pdf&lang=pt"`.

| Rótulo | Artigo | DOI | Páginas | Aprovado em |
|---|---|---|---|---|
| A | Soroprevalência de *Toxoplasma gondii* em gestantes, Piraquara, 2024 (estudo transversal) | 10.1590/S2237-96222026v35e20250708 | 13 | 24/4/2026 |
| B | Dimensão latente de comorbidades e depressão em idosos, PNS 2019 (estudo transversal) | 10.1590/S2237-96222026v35e20250722 | 12 | 14/6/2026 |
| C | Desigualdades em testes rápidos para HIV na APS, Paraná, 2013-2023 (estudo ecológico) | 10.1590/S2237-96222026v35e20250981 | 14 | 25/5/2026 |

## Resultados

### Os cinco números pedidos

| Medida | A | B | C | Mediana | Intervalo |
|---|---:|---:|---:|---:|---|
| Corpo de texto corrido (só prosa) | 2.894 | 2.928 | 3.571 | **2.928** | 2.894–3.571 |
| Resumo | 196 | 244 | 251 | 244 | 196–251 |
| Referências | 925 | 902 | 993 | 925 | 902–993 |
| Títulos e legendas de tabelas e figuras | 149 | 135 | 167 | 149 | 135–167 |
| Total do documento | 5.819 | 5.157 | 6.314 | **5.819** | 5.157–6.314 |

### Do corpo bruto ao corpo de texto corrido

O corpo bruto é tudo o que fica entre "Introdução" e "Referências". Esta tabela mostra o que sai dele até
sobrar só a prosa. As parcelas somam exatamente o corpo bruto nos três artigos.

| Parcela | A | B | C | Mediana |
|---|---:|---:|---:|---:|
| Corpo bruto (de "Introdução" até antes de "Referências") | 4.508 | 3.864 | 4.908 | 4.508 |
| − conteúdo das tabelas e figuras (células, rótulos de eixo e de mapa) | 1.253 | 582 | 1.002 | 1.002 |
| − títulos e legendas de tabelas e figuras | 149 | 135 | 167 | 149 |
| − declarações finais (conflito de interesses, dados, uso de IA, créditos de autoria) | 149 | 163 | 103 | 149 |
| − cabeçalhos e rodapés de página (DOI, "ARTIGO ORIGINAL", citação, número da página) | 63 | 56 | 65 | 63 |
| = **corpo de texto corrido** | **2.894** | **2.928** | **3.571** | **2.928** |

### Combinações que testam outras leituras do limite

| Combinação | A | B | C | Mediana |
|---|---:|---:|---:|---:|
| Corpo corrido + legendas | 3.043 | 3.063 | 3.738 | 3.063 |
| Corpo corrido + resumo | 3.090 | 3.172 | 3.822 | 3.172 |
| Corpo corrido + resumo + legendas | 3.239 | 3.307 | 3.989 | 3.307 |
| Corpo corrido + referências | 3.819 | 3.830 | 4.564 | 3.830 |

Duas leituras estão descartadas: o limite não pode incluir as referências, porque os três artigos passariam
de 3.500, nem pode ser o total. A rigor, resumo e legendas somados ao corpo ainda deixariam A e B abaixo do
limite. Mas o artigo C passaria por 238 a 489 palavras. A leitura que funciona para os três é a mais simples:
só o corpo do texto.

### Conferência com o `wc -w` sobre a saída de `pdftotext -layout`

| | A | B | C |
|---|---:|---:|---:|
| `wc -w` do texto extraído com `-layout` | 5.900 | 5.175 | 6.370 |
| Total pelo meu critério de palavra | 5.819 | 5.157 | 6.314 |

A diferença, de 18 a 81 palavras (até 1,4%), vem de duas regras de contagem descritas no método abaixo:
os símbolos soltos e os títulos espaçados letra a letra.

## Método

1. **Extração.** Usei `pdftotext -layout` para ler o texto e localizar os marcos (Resumo, Palavras-chave,
   Introdução, Referências). O PDF da RESS é diagramado em duas colunas, com tabelas de largura total. Com
   isso, no texto `-layout` uma mesma linha pode juntar a prosa de uma coluna com a célula de uma tabela.
   Por isso, para atribuir cada linha a uma seção, usei a saída `pdftotext -bbox-layout` da mesma
   ferramenta, que dá a página, a posição e a altura de fonte de cada linha.
2. **O que conta como palavra.** Um token separado por espaço que tenha ao menos uma letra ou um dígito.
   Números, chamadas de referência como `[4]` e endereços eletrônicos contam, como no contador do Word.
   Símbolos soltos (`•`, `–`, `|`) não contam. Títulos que o PDF espaça letra a letra ("In t r o d u ç ã o")
   contam como uma palavra só.
3. **Como cada seção foi delimitada.**
   - Resumo: da linha "Resumo" até antes de "Palavras-chave". As palavras-chave ficam de fora (9, 8 e 16
     palavras).
   - Referências: do título "Referências" até o fim do documento. Nos três PDFs, as referências são a
     última seção.
   - Corpo bruto: do título "Introdução" até antes de "Referências", em ordem de página e posição vertical.
     Nos três artigos, "Referências" é um título de largura total que vem depois das declarações finais.
   - Títulos e legendas: os blocos que começam com "Tabela N." ou "Figura N." (inclusive "Tabela N.
     Continuação") e as notas de rodapé das tabelas (fonte pequena, prosa, notas marcadas com letra
     sobrescrita).
   - Conteúdo das tabelas e figuras: as linhas do corpo bruto com altura de fonte diferente da fonte modal
     do corpo, com tolerância de ±0,8 pt. Isso pega células de tabela e rótulos de gráfico e de mapa. Os
     títulos de seção (Introdução, Métodos, Resultados, Discussão, Conclusão) ficam no corpo mesmo com
     fonte maior. A fonte modal varia de PDF para PDF: 11,0 pt em A e B, 13,5 pt em C.
   - Declarações finais: de "Conflito de interesses" até antes de "Referências".
   - Cabeçalhos e rodapés: as faixas do topo e do pé de cada página.
4. **Validação.** Inspecionei as linhas curtas atribuídas ao corpo e as linhas atribuídas a legendas e a
   conteúdo de tabela. Depois do ajuste pela fonte modal, o corpo ficou só com prosa e subtítulos. Sobrou
   um único resíduo, de 1 palavra, no artigo C. A soma das parcelas fecha exatamente com o corpo bruto nos
   três artigos.
5. **O que fica fora de todas as seções.** Estas palavras entram só no total: título do artigo, autores,
   afiliações, aspectos éticos, quadro editorial e cabeçalho da primeira página (181, 139 e 146 palavras).
