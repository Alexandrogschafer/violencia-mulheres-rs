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
