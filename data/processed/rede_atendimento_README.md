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
