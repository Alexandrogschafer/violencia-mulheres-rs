# Protocolo para registro no OSF — texto pronto

> Este arquivo é a **fonte de conteúdo** do registro. Preencher os dois campos marcados
> `[PREENCHER]` e depositar em OSF Registries, modelo *OSF Preregistration* ou
> *Open-Ended Registration*. Não usar PROSPERO: exige desfecho de saúde e recusa revisões
> de qualidade metodológica.

---

## Título

Reporte de parâmetros em testes de autocorrelação espacial na literatura brasileira sobre
violência e causas externas: protocolo de revisão sistemática metodológica

**English title.** Reporting of spatial autocorrelation test parameters in the Brazilian
literature on violence and external causes: protocol for a methodological systematic review

## Autores

- Alexandro Gularte Schäfer — Universidade Federal do Pampa, Campus Bagé, Programa de
  Pós-Graduação em Computação Aplicada. Bagé, RS, Brasil.
  ORCID 0000-0001-8700-0860
- Lisie Alende Prates — Universidade Federal do Pampa, Campus Uruguaiana, Curso de
  Enfermagem. Uruguaiana, RS, Brasil.
  ORCID 0000-0002-5151-0292

## Resumo

Estudos que descrevem a distribuição espacial de desfechos de violência em municípios
brasileiros recorrem rotineiramente a estatísticas de autocorrelação espacial — o I de
Moran global e os indicadores locais de associação espacial. O resultado desses testes
depende de escolhas que o analista faz e que o leitor não observa: o tratamento dado à taxa
em populações pequenas, o número de permutações do teste de pseudo-significância, a semente
do gerador aleatório, e o tratamento da multiplicidade quando centenas de testes locais são
avaliados simultaneamente. Esta revisão examina **o que dessas escolhas é declarado**, sem
avaliar se os resultados estão corretos. O desfecho de interesse é o reporte, não o achado.

**English.** Studies describing the spatial distribution of violence outcomes across
Brazilian municipalities routinely use spatial autocorrelation statistics. Their results
depend on analytical choices the reader cannot observe: rate treatment for small
populations, number of permutations, random seed, and multiplicity correction across
hundreds of local tests. This review examines which of these choices are reported. The
outcome of interest is reporting, not findings.

## Pergunta

Nos estudos brasileiros que aplicam estatística de autocorrelação espacial a desfechos de
violência e causas externas em escala municipal ou inferior, quais parâmetros do teste são
declarados na seção de métodos, e quais ficam por declarar?

**Secundárias:** o grau de omissão varia com o ano de publicação, com a escala da unidade
de análise, com o programa utilizado ou com o estrato do periódico?

## Critérios de elegibilidade

**Inclusão**
- artigo original de pesquisa;
- aplica estatística de autocorrelação espacial: I de Moran global, Moran local ou LISA,
  Getis-Ord, ou equivalente com teste de significância;
- unidade de análise igual ou inferior ao município brasileiro;
- desfecho de violência ou causa externa: feminicídio, homicídio, violência contra a
  mulher, agressão, suicídio, demais causas externas;
- publicado entre 2010 e 2026;
- português, inglês ou espanhol.

**Exclusão**
- revisão, editorial, carta, resumo de evento, resumo de dissertação ou tese;
- análise espacial apenas descritiva, sem estatística de teste;
- unidade de análise acima do município;
- seção de métodos inacessível.

**Registrado:** microrregião e mesorregião **são incluídas** e tratadas como variável de
escala, não como critério de exclusão.

## Fontes de informação

LILACS (via Biblioteca Virtual em Saúde), SciELO, PubMed/MEDLINE e Scopus. Complementadas
por rastreamento de citações para trás e para a frente a partir dos incluídos.

## Estratégia de busca

Três blocos em interseção, adaptados à sintaxe de cada base e com descritores controlados
onde existirem (DeCS: Análise Espacial, Violência, Brasil; MeSH: Spatial Analysis,
Violence, Brazil):

```
("autocorrelação espacial" OR "análise espacial" OR "Moran" OR "LISA"
 OR "Getis-Ord" OR "spatial autocorrelation" OR "spatial analysis")
AND
("violência" OR "feminicídio" OR "homicídio" OR "causas externas" OR "agressão"
 OR "suicídio" OR violence OR femicide OR homicide OR "external causes" OR suicide)
AND
(Brasil OR Brazil OR "municípios" OR municipalities)
```

A string exata executada em cada base, com data de execução e número de registros
recuperados, será depositada junto aos resultados.

## Seleção

Fluxo PRISMA 2020. Triagem dupla e independente por título e resumo, com concordância
medida por kappa de Cohen e divergência resolvida por discussão entre os dois avaliadores.
Mesma dupla na avaliação de texto completo, com motivo de exclusão registrado nessa etapa.

## Calibração da dupla

Antes da triagem propriamente dita, os dois avaliadores aplicam o instrumento
independentemente aos mesmos dez registros, escolhidos ao acaso entre os identificados.
Comparam-se as classificações eixo a eixo, discutem-se as divergências e, se necessário,
redige-se nota de esclarecimento ao instrumento — anexada ao registro como emenda datada,
sem alteração dos eixos. Essa rodada não conta como triagem e os dez registros voltam ao
conjunto.

A calibração é prática corrente em revisão sistemática e aqui tem função adicional: a
distinção entre **ambíguo** e **omisso** é o eixo mais sujeito a leitura divergente, e é
dela que depende o achado principal.

## Instrumento de extração

Nove eixos, cada um classificado em três estados — **declarado**, **ambíguo** (o texto
trata do ponto admitindo mais de uma leitura) e **omisso** (o texto não trata do ponto) —
com transcrição literal da passagem e página.

1. tratamento da taxa: bruta, suavizada por Bayes empírico, ou ajuste tipo Assunção-Reis;
   e se a taxa suavizada foi usada no mapa, no teste, ou em ambos;
2. número de permutações do teste de pseudo-significância;
3. semente do gerador aleatório;
4. correção para multiplicidade de testes;
5. reporte: p individual por área, ou apenas mapa e contagem agregada;
6. referência citada para justificar o tratamento da taxa;
7. programa utilizado;
8. unidade de análise, número de áreas, desfecho e período;
9. declaração de disponibilidade de dados ou código.

Não se inferirá parâmetro não declarado a partir do que seria usual. A distinção entre
ambíguo e omisso é central e não será relaxada.

## Síntese

Descritiva: frequência de cada estado por eixo, com intervalo de confiança. Cruzamentos
previstos: estado por ano de publicação, por escala da unidade, por programa e por estrato
do periódico. O eixo 7 permite examinar, entre os que não declaram permutações, qual seria
o padrão do programa utilizado — essa leitura será apresentada como inferência, nunca como
dado extraído.

## Busca exploratória anterior

Antes deste registro houve duas atividades exploratórias, ambas declaradas aqui.

**Levantamento de oito trabalhos**, não sistemático, reunidos por busca livre na web, que
orientou a construção do instrumento de extração. Esses oito serão reavaliados dentro do
fluxo formal, pela mesma dupla e pelos mesmos critérios, sem aproveitar a classificação
anterior.

**Busca de escopo no PubMed, executada em 01/11/2026**, antes deste registro, com a
seguinte string, que é também a string registrada para a busca formal:

```text
("spatial autocorrelation"[tiab] OR "spatial analysis"[tiab] OR Moran[tiab] OR LISA[tiab]
 OR "Getis-Ord"[tiab] OR "Spatial Analysis"[MeSH Terms])
AND (violence[tiab] OR femicide[tiab] OR homicide[tiab] OR "external causes"[tiab]
 OR suicide[tiab] OR "Violence"[MeSH Terms])
AND (Brazil[tiab] OR "Brazil"[MeSH Terms])
AND ("2010"[dp] : "2026"[dp])
```

Recuperou **83 registros**, nenhum triado. Os termos livres foram restritos a título e
resumo (`[tiab]`) para evitar o mapeamento automático de termos do PubMed; essa restrição
altera o resultado em relação a uma busca em todos os campos e fica registrada como parte
da estratégia. A string não será alterada em função do que esses 83 registros contêm.

**SciELO: não executada.** A interface de busca recusou acesso programático (HTTP 403,
verificação de navegador) e a API do ArticleMeta não faz busca por termos. A string abaixo
está preparada para execução manual na interface, com recorte de ano 2010–2026, e será
executada após este registro:

```text
("spatial autocorrelation" OR "spatial analysis" OR Moran OR LISA OR "Getis-Ord"
 OR "autocorrelação espacial" OR "análise espacial" OR "autocorrelación espacial"
 OR "análisis espacial")
AND (violence OR femicide OR homicide OR "external causes" OR suicide OR violência
 OR feminicídio OR homicídio OR "causas externas" OR suicídio OR violencia
 OR feminicidio OR homicidio OR suicidio)
AND (Brazil OR Brasil)
```

LILACS e Scopus também serão executadas após o registro.

## Alterações após o registro

Qualquer alteração em critério, string ou instrumento após esta data será registrada como
emenda datada, com justificativa, e reportada no artigo.
