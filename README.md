# Violência contra as mulheres no RS

Análise de dados de violência contra as mulheres e meninas no Rio Grande do Sul, a partir das planilhas públicas do SIP/PROCERGS (2012-2026), com taxas por habitante calculadas sobre população do IBGE.

## Como citar

Se utilizar este software/dataset, cite-o conforme abaixo (ver também `CITATION.cff`):

> Schäfer, A. G., & Prates, L. A. (2026). *Pipeline de análise da violência contra a mulher no RS (2012-2026)* [Software]. https://github.com/Alexandrogschafer/violencia-mulheres-rs

Licenciado sob [CC BY 4.0](LICENSE) — Alexandro Gularte Schäfer e Lisie Alende Prates, 2026.

## Estrutura do projeto

```
data/raw/              planilhas .xlsx originais do SIP/PROCERGS (não versionadas, ver .gitignore)
src/load_data.py        parseia data/raw/ e gera as tabelas long em outputs/tables/
src/fetch_populacao.py  busca população dos municípios do RS na API do IBGE
notebooks/              análise exploratória em cima das tabelas geradas
outputs/tables/         CSVs gerados pelo pipeline (não versionados, regeneráveis)
outputs/figures/        figuras exportadas, se houver
```

Mais detalhes de arquitetura e das peculiaridades de cada arquivo bruto estão em `CLAUDE.md`.

## Como rodar o pipeline do zero

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/load_data.py        # gera violencia_mensal_municipio.csv e violencia_anual_municipio.csv
python src/fetch_populacao.py  # busca população no IBGE (rede), gera populacao_municipio_rs.csv
python src/load_data.py        # roda de novo: com a população presente, gera também violencia_anual_municipio_taxa.csv
```

`fetch_populacao.py` faz chamadas reais à API do IBGE (leva ~1 min) — rode antes da segunda chamada a `load_data.py` para obter a tabela de taxas; sem ele, `load_data.py` gera as duas tabelas de casos normalmente e só avisa que a tabela de taxa não foi gerada.

Depois, abra `notebooks/analise_exploratoria.ipynb` (kernel do `.venv`, precisa de `ipykernel`) e rode as células em ordem.

### Saídas geradas

| Arquivo | Cobertura | Granularidade |
|---|---|---|
| `outputs/tables/violencia_mensal_municipio.csv` | 2018-2026 | município, ano, mês, tipo_crime, casos |
| `outputs/tables/violencia_anual_municipio.csv` | 2012-2026 | município, ano, tipo_crime, casos_total |
| `outputs/tables/populacao_municipio_rs.csv` | 2012-2025 | município, ano, populacao |
| `outputs/tables/violencia_anual_municipio_taxa.csv` | 2012-2026 | as colunas acima + populacao, taxa_por_100mil_hab |

## Limitações de dados (leia antes de interpretar qualquer número)

- **2012-2017 não tem detalhe mensal por município.** O arquivo consolidado desse período só tem município × ano nas abas por tipo de crime; a quebra mensal por município só existe a partir de 2018 (por isso a tabela mensal começa em 2018, não em 2012).
- **Taxa por habitante usa população total, não só mulheres.** O IBGE só quebra população por sexo no ano de Censo — as estimativas intercensitárias (que cobrem os demais anos) só têm população total. A DEE-RS tem população feminina por município, mas só até 2021 (descontinuada após as enchentes de maio/2024). A planilha original da SSP calculava a taxa sobre população feminina; a taxa aqui não é diretamente comparável a essa métrica original. Ver docstring de `src/fetch_populacao.py` e a Seção 5 do notebook.
- **População de 2023 é interpolada, não medida.** O IBGE nunca publicou a estimativa municipal de 2023 (reconheceram publicamente que não cumpriram o calendário de divulgação). O valor usado é uma interpolação linear entre o Censo 2022 e a estimativa 2024 (ver `_interpola_ano_faltante` em `src/fetch_populacao.py`) — um valor sintético, não uma medição.
- **2026 é um ano parcial** (dados só até por volta de junho/2026, e sem estimativa de população do IBGE ainda — só sai em ago/set de 2026). Não há linha de população para 2026, e a tabela de taxa fica com `NaN` nesse ano em vez de um valor calculado sobre dado incompleto.
- **"NÃO INFORMADO"** aparece como um valor de município em 2018 (Ameaça e Lesão Corporal): são casos sem município identificado na base original, mantidos para não perder casos do total, mas não é um município real — exclua-o de qualquer análise por município.
