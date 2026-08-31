# 7. Considerações finais

> **Rascunho v2** — 30/08/2026. Citações em formato autor-data, a
> converter para a norma da editora.

A distância entre dado disponível e dado utilizável foi o objeto central
deste capítulo, e ela não é técnica por acidente. Publicar uma planilha
cumpre a exigência legal de transparência; produzir informação
territorial exige decisões — sobre denominador, sobre unidade de
agregação, sobre recorte temporal, sobre classificação — que a planilha
não toma e que, uma vez tomadas, determinam o que se pode afirmar.
Nenhuma dessas decisões é neutra, e a contribuição principal talvez
esteja menos nos mapas produzidos do que no registro explícito de cada
uma delas.

Do ponto de vista da replicação, o fluxo tem uma propriedade que a Seção
6.7 enuncia e que convém precisar aqui: apenas a primeira de suas quatro
etapas é específica da fonte.
A harmonização das planilhas da Secretaria não serve a mais nada; as
outras três — construção de denominador por consulta ao IBGE, acoplamento
à malha municipal por código, publicação estática pré-processada —
funcionam para qualquer dado administrativo municipalizado, em qualquer
unidade da federação. O custo de reproduzir o
percurso para outro tema, ou o mesmo tema em outro estado, concentra-se
na etapa de harmonização — que é, previsivelmente, a mais tediosa e a
menos publicável.

Vale registrar uma consequência inesperada do próprio exercício de
escrever este capítulo. A necessidade de descrever cada decisão de forma
defensável revelou decisões que não eram defensáveis: um recorte temporal
herdado sem justificativa, uma classificação cromática inadequada ao
suporte impresso, a ausência de registro sobre qual versão dos arquivos
brutos sustentava os resultados. As três foram corrigidas em decorrência
da redação, e não do uso: nenhuma comprometia o funcionamento do portal,
e nenhuma teria sido detectada por quem apenas o consultasse.
Documentar um instrumento com rigor é, nesse sentido, uma forma de
controle de qualidade sobre ele — e a redação acadêmica, quando incide
sobre um artefato próprio, funciona como auditoria.

O capítulo deixou deliberadamente de fora a análise de autocorrelação
espacial e a identificação de agrupamentos locais, que o mesmo conjunto de
dados permite e que constituem etapa distinta: o mapa coroplético mostra
onde os valores são altos; as estatísticas de associação espacial mostram
onde valores altos se agrupam com vizinhos altos, que é pergunta diferente
e exige tratamento próprio. A distinção entre as duas leituras merece
desenvolvimento que não caberia aqui.

Por fim, uma palavra sobre o que o instrumento autoriza. As três
categorias mapeadas desenham padrões territoriais distintos, e essa
distinção é informativa para quem desenhe políticas de enfrentamento. Mas
os dados medem ocorrências comunicadas, não ocorrências, e um mapa
construído sobre eles identifica territórios que merecem investigação — não
hierarquiza municípios por gravidade, nem autoriza conclusões sobre
indivíduos. Um instrumento que declara seus limites com precisão é mais
útil que um que os oculta, ainda que pareça menos conclusivo. A alternativa
— um mapa que sugira mais do que sustenta — seria pior que a ausência de
mapa, porque teria a aparência de conhecimento.

Todo o material descrito neste capítulo está disponível publicamente: o
pipeline de processamento, o portal, os dados tratados e a documentação
das decisões. A escolha por publicá-los com identificador persistente e
metadados de citação não é apêndice do trabalho — é parte do método
(WILKINSON et al., 2016; SMITH; KATZ; NIEMEYER, 2016). Com a ressalva,
discutida na Seção 6, de que a reprodutibilidade de um fluxo que consome
dado administrativo revisável exige registrar não apenas o processamento,
mas a versão da entrada que o alimentou — providência de que a Seção 8
informa a localização.

---

## Notas para revisão

### Alterações desta versão

- **Abertura cortada.** O primeiro parágrafo repetia, quase termo a
  termo, o ponto de disponibilidade de §6.7. A seção passa a abrir pela
  distância entre dado disponível e dado utilizável, que é o argumento
  próprio, e remete a §6.7 no parágrafo seguinte em vez de refazê-lo.
- **Durabilidade removida.** O argumento aparecia em §4.4, §6.7 e aqui.
  Mantido apenas em §6.7.
- **Auditoria.** O parágrafo agora afirma que as três decisões foram
  corrigidas — o que só é verdade depois da rodada de atualização do
  portal. Ver abaixo.
- **Licença.** A menção a "licença aberta" saiu do penúltimo parágrafo,
  em coerência com §8, onde a licença foi retirada até a decisão com a
  DIT. Reintroduzir nos dois lugares quando resolvido.

### Verificar antes de submeter

**O parágrafo da auditoria depende da rodada do portal.** Ele afirma que
as três decisões indefensáveis foram corrigidas. Hoje isso vale só para
o registro de proveniência; o recorte temporal dos mapas e a
classificação cromática dependem das alterações previstas em
`build_site_data.py` e nas páginas. Se a rodada não sair antes da
submissão, este parágrafo e o trecho correspondente de §6.6 precisam
voltar para o futuro, ou nomear apenas a correção já feita.

### Sobre o texto

- **Extensão:** cerca de 640 palavras, depois dos cortes. Considerações
  finais devem ser curtas; se houver folga no limite de páginas, o melhor
  uso dela é a Seção 2.
- A seção acrescenta três coisas que não estão nas anteriores: a
  precisão de que só a primeira etapa é específica da fonte; a observação
  sobre escrever como auditoria; e o fechamento sobre o que o instrumento
  autoriza.
- O parágrafo sobre a auditoria assume que você aceita expor que o portal
  tinha problemas antes deste trabalho. Considero que fortalece o texto —
  mostra método, não descuido —, mas se preferir, ele pode ser reescrito
  em termos gerais, sem admitir que os problemas eram do próprio portal.
- A menção à autocorrelação espacial e aos agrupamentos locais está
  coerente com a Introdução, que também não abre o assunto.
