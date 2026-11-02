# data/processed/violencia_rs_municipio_ano.csv

Dataset tratado e citável do projeto -- consolida casos de violência contra as mulheres
e meninas no Rio Grande do Sul (fonte: SIP/PROCERGS) com população (IBGE) e taxa por
100 mil habitantes, por município, ano e tipo de crime. Gerado por `src/build_site_data.py`
a partir de `outputs/tables/violencia_anual_municipio_taxa.csv` (esse, sim, regenerável e
não versionado -- ver `.gitignore`).

Ao contrário de `outputs/tables/`, este arquivo **é versionado no git**: é o dataset
tratado pensado para citação e reuso externo, disponível mesmo sem rodar o pipeline
localmente.

## Colunas

| Coluna | Descrição |
|---|---|
| `municipio` | Nome do município (maiúsculas, sem acento -- convenção das planilhas originais da SIP/PROCERGS), ou `NÃO INFORMADO` (ver limitações abaixo) |
| `ano` | Ano de referência |
| `tipo_crime` | Uma de: Ameaça, Estupro, Feminicídio Consumado, Feminicídio Tentado, Lesão Corporal |
| `casos_total` | Total de casos no ano, no município, para o tipo de crime |
| `populacao` | População total do município no ano (estimativa IBGE; ver limitações) |
| `taxa_por_100mil_hab` | `casos_total / populacao * 100_000` |

## Cobertura

- 498 municípios, anos 2012-2026, 36780 linhas.
- 2026 é ano parcial (dados só até por volta de junho/2026) e não tem estimativa de
  população do IBGE ainda -- `populacao`/`taxa_por_100mil_hab` ficam vazios nesse ano.

## Limitações (ver também README.md e CLAUDE.md na raiz do repositório)

- **Taxa usa população total, não só mulheres** -- o IBGE só quebra população por sexo
  no ano de Censo; as estimativas intercensitárias só têm população total.
- **População de 2023 é interpolada, não medida** -- o IBGE não publicou a estimativa
  municipal de 2023 (ver `src/fetch_populacao.py`).
- **"NÃO INFORMADO"** é um valor de município em 2018 (Ameaça e Lesão Corporal): casos
  sem município identificado na base original, mantidos para não perder casos do total,
  mas não é um município real -- exclua-o de qualquer análise por município.

## Licença e citação

CC BY 4.0 -- ver `LICENSE` e `CITATION.cff` na raiz do repositório.

---

# data/processed/rede_atendimento_municipio.csv

Presença ou ausência de serviço da rede de atendimento à mulher por município do RS, tirada
da MUNIC/IBGE. Gerado por `src/fetch_rede_atendimento.py`, que baixa as bases do FTP do IBGE
para `data/raw/rede_atendimento/` (não versionado). A proveniência, com URL e SHA-256 de cada
base, fica em `rede_atendimento_proveniencia.csv`.

Formato longo: uma linha por município, indicador e edição. 497 municípios × 7 combinações.

| Coluna | Descrição |
|---|---|
| `codigo_ibge`, `municipio` | Junção por `outputs/tables/municipio_codigo_ibge.csv` |
| `indicador` | `deam` (delegacia especializada de atendimento à mulher), `organismo_mulheres` (organismo executivo municipal de políticas para mulheres), `creas_munic` (CREAS declarado na MUNIC) |
| `edicao`, `aba`, `variavel` | Edição da MUNIC, aba da base e código da variável |
| `valor_original` | Valor como está na base do IBGE |
| `status` | `tem`, `nao_tem` ou `sem_resposta` |
| `itens_sem_resposta_na_aba` | Quantos itens da mesma aba o município deixou como "Não informou"/"Não soube informar" |

`sem_resposta` não é ausência. O "-" da MUNIC é tratado como ausência só quando um filtro
anterior o explica (em `deam` 2018: MPPM23 = Não ou MPPM2411 = Sim; em `deam` 2023: MSEG1611
= Sim); no CREAS, o "-" aparece com o quesito inteiro em branco e conta como falta de resposta.

Limitações: a MUNIC é autodeclarada pela prefeitura. `deam` 2018 vem de outra pergunta e de
outro bloco (política para mulheres) que `deam` 2019 e 2023 (segurança pública). O CREAS do
Censo SUAS/MDS ainda não entrou: o portal do MDS estava fora do ar em 02/11/2026.
