# 8. Disponibilidade de dados e código

O portal descrito neste capítulo está disponível em
`https://alexandrogschafer.github.io/violencia-mulheres-rs/`. O
código-fonte do pipeline e do portal, as tabelas consolidadas e a
documentação das decisões metodológicas estão no repositório
`https://github.com/Alexandrogschafer/violencia-mulheres-rs`.

O conjunto está depositado no Zenodo, com identificador persistente
`10.5281/zenodo.21403499`, e acompanha arquivo de metadados de citação no
repositório. Sugere-se a forma:

> [AUTORIA]. *[TÍTULO DO OBJETO]* [Software]. Versão [X.Y]. Zenodo,
> 2026. DOI 10.5281/zenodo.21403499

Os dados primários são públicos e podem ser obtidos junto à Secretaria da
Segurança Pública do Estado do Rio Grande do Sul, em
`[ENDEREÇO DA PÁGINA]`. Cabe aqui a ressalva que a Seção 6.6 desenvolve:
os arquivos publicados pela Secretaria são revisados retroativamente, de
modo que os obtidos hoje podem não coincidir com os que sustentaram estes
resultados. Por essa razão, o repositório inclui uma tabela de
proveniência dos dados brutos —
`outputs/tables/proveniencia_dados_brutos.csv` —, que registra, para cada
arquivo consumido, o *hash* de integridade e a data de atualização
declarada pela fonte. É essa tabela, e não apenas o código, que permite
determinar sobre qual versão da entrada os resultados aqui apresentados
foram produzidos.

---

## Notas para revisão

**Preencher.** Autoria, título do objeto e número de versão no modelo de
citação; endereço da página da SSP/RS, que aparece também nas Notas de
§1 e §3.

**Licença — decisão pendente e possivelmente incorreta como está.** A
versão anterior desta seção declarava Creative Commons Attribution 4.0
para o conjunto. As licenças Creative Commons são desaconselhadas pela
própria organização para código-fonte, por não tratarem de código-objeto,
patentes ou exclusão de garantia. O arranjo usual em repositório misto é
código sob licença de software permissiva (MIT, BSD-3-Clause, Apache-2.0)
e dados e documentação sob CC-BY 4.0. Removi a menção à licença em vez de
imprimir no capítulo uma que talvez mude: convém resolver com a DIT,
junto da questão de titularidade, e só então reintroduzir a frase. Note
que §3 afirma que todas as dependências têm licença permissiva — isso
descreve as dependências, não a licença do próprio conjunto, e as duas
coisas não devem ser confundidas na leitura.

**Título do objeto — divergência a resolver.** O `CITATION.cff` diz
"Pipeline de análise..."; o registro em preparação diz "Portal de
Monitoramento...". São dois nomes para o mesmo objeto, e o modelo de
citação acima exige escolher um. Sugestão: adotar o título do registro,
por ser o mais abrangente (o pipeline é parte do portal, não o
contrário), e alinhar o `CITATION.cff` a ele.

**Autoria — quatro nomes.** O Zenodo lista dois. A correção precisa ser
feita pela interface do Zenodo, já que editar o `CITATION.cff` no GitHub
não propaga para o depósito. Enquanto não for feita, a citação sugerida
nesta seção divergirá dos metadados que o DOI resolve — o que é
exatamente o tipo de inconsistência que o capítulo critica.

**DOI de conceito ou de versão.** Smith, Katz e Niemeyer (2016), citados
em §3, recomendam identificar a versão específica utilizada. O Zenodo
emite um DOI de conceito, que aponta sempre para a versão mais recente, e
um DOI por versão. Confirmar qual é o `21403499` e, se for o de conceito,
acrescentar o da versão que sustenta o capítulo.

**Coerência com §7.** O penúltimo parágrafo de §7 antecipa esta seção e
menciona "licença aberta, com identificador persistente e metadados de
citação". Se a licença sair daqui provisoriamente, essa frase de §7
precisa ser conferida.
