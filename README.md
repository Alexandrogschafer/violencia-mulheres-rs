# Violência contra as mulheres no RS

[🌐 Portal Interativo](https://alexandrogschafer.github.io/violencia-mulheres-rs/) • 📄 Artigo *(em breve)* • [📦 DOI](https://doi.org/10.5281/zenodo.21403499) • [📜 Licença CC BY 4.0](LICENSE)

## 🌐 Portal Interativo

Acesse o portal público do projeto — explore os resultados direto no navegador, sem instalar nada:

### **➡️ https://alexandrogschafer.github.io/violencia-mulheres-rs/**

Este repositório contém todo o **código-fonte, os notebooks de análise e os dados** utilizados no estudo sobre violência contra as mulheres e meninas no Rio Grande do Sul (2012-2026), a partir das planilhas públicas do SIP/PROCERGS, com taxas por habitante calculadas sobre população do IBGE.

Os resultados podem ser explorados diretamente pelo **portal web** acima — gráficos interativos, mapas, tabelas pesquisáveis e estudos de caso municipais — **sem necessidade de executar os notebooks**. Rodar o pipeline localmente só é preciso para quem quiser reproduzir, auditar ou estender a análise (ver [Como utilizar](#como-utilizar) abaixo).

## Como citar

Se utilizar este software/dataset, cite-o conforme abaixo (ver também `CITATION.cff`):

> Schäfer, A. G., & Prates, L. A. (2026). *Pipeline de análise da violência contra a mulher no RS (2012-2026)* [Software]. https://github.com/Alexandrogschafer/violencia-mulheres-rs. DOI: [10.5281/zenodo.21403499](https://doi.org/10.5281/zenodo.21403499)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21403499.svg)](https://doi.org/10.5281/zenodo.21403499)

Licenciado sob [CC BY 4.0](LICENSE) — Alexandro Gularte Schäfer e Lisie Alende Prates, 2026.

## Portal Web

O portal (`docs/`) é um site estático — HTML/CSS/JS puro, sem build step — com 8 páginas:

| Página | Conteúdo |
|---|---|
| **Início** | Visão geral do projeto, totais por tipo de crime (2012-2026) e gráfico interativo da série anual estadual. |
| **Metodologia** | Fonte dos dados (SIP/PROCERGS), os métodos de cada camada de análise (tendência, sazonalidade, correlação, quebra estrutural, autocorrelação espacial) e as limitações de dados. |
| **Resultados** | Os quatro testes estatísticos da análise inferencial estadual — tendência anual, sazonalidade mensal, correlação entre tipos de crime e quebra estrutural em torno das enchentes de maio/2024. |
| **Municípios** | Tabela pesquisável e ordenável com casos e taxa por 100 mil hab. dos ~497 municípios do RS. |
| **Mapas** | Mapa interativo (Leaflet) da taxa por município, com seletor de tipo de crime, e a galeria dos mapas de clusters espaciais (LISA). |
| **Estudos de Caso** | Recortes municipais sobre a mesma metodologia estadual — hoje, o estudo de caso de Uruguaiana (RS), com estrutura preparada para novos municípios. |
| **Dados** | Download do dataset tratado (`violencia_rs_municipio_ano.csv`) e dicionário de colunas. |
| **Sobre** | Autoria, como citar, licença e instituições participantes. |

> 🖼️ **Captura de tela da página inicial — em breve.** Este espaço será atualizado com um screenshot do portal assim que uma captura de tela estiver disponível.

## Como utilizar

Há duas formas de acessar este projeto:

### Opção 1 — Pelo portal web (recomendado para a maioria dos usuários)

Acesse **https://alexandrogschafer.github.io/violencia-mulheres-rs/** e explore os
gráficos, mapas e tabelas diretamente no navegador. Não é necessário instalar nada.

### Opção 2 — Executando os notebooks localmente (para reprodução científica)

Para quem quiser rodar o pipeline completo, auditar os cálculos ou estender a análise:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/load_data.py        # gera violencia_mensal_municipio.csv e violencia_anual_municipio.csv
python src/fetch_populacao.py  # busca população no IBGE (rede), gera populacao_municipio_rs.csv
python src/load_data.py        # roda de novo: com a população presente, gera também violencia_anual_municipio_taxa.csv
```

`fetch_populacao.py` faz chamadas reais à API do IBGE (leva ~1 min) — rode antes da segunda chamada a `load_data.py` para obter a tabela de taxas; sem ele, `load_data.py` gera as duas tabelas de casos normalmente e só avisa que a tabela de taxa não foi gerada.

Depois, abra `notebooks/analise_exploratoria.ipynb` (kernel do `.venv`, precisa de `ipykernel`) e rode as células em ordem. As 4 notebooks (`analise_exploratoria`, `analise_inferencial`, `analise_espacial`, `estudo_uruguaiana`) salvam suas figuras em `outputs/figures/` e suas tabelas de resultado em `outputs/reports/`.

#### Saídas geradas

| Arquivo | Cobertura | Granularidade |
|---|---|---|
| `outputs/tables/violencia_mensal_municipio.csv` | 2018-2026 | município, ano, mês, tipo_crime, casos |
| `outputs/tables/violencia_anual_municipio.csv` | 2012-2026 | município, ano, tipo_crime, casos_total |
| `outputs/tables/populacao_municipio_rs.csv` | 2012-2025 | município, ano, populacao |
| `outputs/tables/violencia_anual_municipio_taxa.csv` | 2012-2026 | as colunas acima + populacao, taxa_por_100mil_hab |

## Reprodutibilidade

Todo o portal é gerado a partir dos dados brutos por um fluxo linear e automatizado — nada no `docs/` é editado manualmente:

```
Dados brutos (data/raw/*.xlsx, SIP/PROCERGS)
   ↓
Notebooks (notebooks/*.ipynb — análise exploratória, inferencial, espacial, estudos de caso)
   ↓
src/build_site_data.py (converte outputs/ em JSON/GeoJSON prontos para o site)
   ↓
Portal GitHub Pages (docs/ — estático, publicado no push)
```

Cada seta é reproduzível de ponta a ponta rodando os comandos da Opção 2 de [Como utilizar](#como-utilizar) acima seguidos de `python -m src.build_site_data` — ver o passo a passo completo em [Como atualizar e publicar o portal](#como-atualizar-e-publicar-o-portal).

## Estrutura do projeto

```
data/raw/               planilhas .xlsx originais do SIP/PROCERGS (não versionadas, ver .gitignore)
data/processed/         dataset tratado e versionado (violencia_rs_municipio_ano.csv + dicionário de dados)
src/load_data.py        parseia data/raw/ e gera as tabelas long em outputs/tables/
src/fetch_populacao.py  busca população dos municípios do RS na API do IBGE
src/build_site_data.py  prepara data/processed/, outputs/reports/, outputs/maps/ e docs/assets/data/
notebooks/              análise exploratória, inferencial, espacial e estudo de caso (Uruguaiana)
outputs/tables/         CSVs gerados pelo pipeline (não versionados, regeneráveis)
outputs/figures/        figuras exportadas pelas notebooks (não versionadas, regeneráveis)
outputs/reports/        tabelas de resultado estatístico das notebooks 1, 2 e estudos de caso (não versionadas, regeneráveis)
outputs/maps/           geojson/json prontos para o mapa interativo (não versionados, regeneráveis)
docs/                   portal estático (GitHub Pages) — ver "Como atualizar e publicar o portal" abaixo
```

Mais detalhes de arquitetura e das peculiaridades de cada arquivo bruto estão em `CLAUDE.md`.

## Como atualizar e publicar o portal

O portal em `docs/` é **estático** — HTML/CSS/JS puro, sem build step, sem servidor,
sem banco de dados. O GitHub Pages serve o conteúdo de `docs/` diretamente do branch
`master`; não há nenhuma etapa de compilação entre o commit e o site no ar.

Para atualizar o portal depois de uma mudança nos dados ou nas notebooks:

```bash
# 1. Rodar o pipeline (se os dados brutos mudaram)
python src/load_data.py
python src/fetch_populacao.py
python src/load_data.py

# 2. Re-rodar as notebooks (gera/atualiza outputs/figures/ e outputs/reports/)
jupyter execute --inplace notebooks/analise_exploratoria.ipynb
jupyter execute --inplace notebooks/analise_inferencial.ipynb
jupyter execute --inplace notebooks/analise_espacial.ipynb
jupyter execute --inplace notebooks/estudo_uruguaiana.ipynb

# 3. Gerar data/processed/, outputs/maps/ e publicar em docs/assets/data/
python -m src.build_site_data

# 4. Commitar e publicar (docs/ e data/processed/ SÃO versionados — outputs/ não é)
git add docs/ data/processed/
git commit -m "Atualiza portal e dataset tratado"
git push
```

`src/build_site_data.py` é idempotente — pode ser rodado quantas vezes forem necessárias,
sempre a partir do estado atual de `outputs/tables/`, `outputs/reports/`, `outputs/figures/`
e `data/raw/malha_municipios_rs.geojson`. Para testar localmente antes de publicar:

```bash
cd docs && python3 -m http.server 8000
# depois abra http://localhost:8000 no navegador
```

(Abrir `docs/index.html` direto como arquivo, via `file://`, não funciona — as páginas
buscam os JSONs de `assets/data/` via `fetch()`, que exige um servidor http.)

## Limitações de dados (leia antes de interpretar qualquer número)

- **2012-2017 não tem detalhe mensal por município.** O arquivo consolidado desse período só tem município × ano nas abas por tipo de crime; a quebra mensal por município só existe a partir de 2018 (por isso a tabela mensal começa em 2018, não em 2012).
- **Taxa por habitante usa população total, não só mulheres.** O IBGE só quebra população por sexo no ano de Censo — as estimativas intercensitárias (que cobrem os demais anos) só têm população total. A DEE-RS tem população feminina por município, mas só até 2021 (descontinuada após as enchentes de maio/2024). A planilha original da SSP calculava a taxa sobre população feminina; a taxa aqui não é diretamente comparável a essa métrica original. Ver docstring de `src/fetch_populacao.py` e a Seção 5 do notebook.
- **População de 2023 é interpolada, não medida.** O IBGE nunca publicou a estimativa municipal de 2023 (reconheceram publicamente que não cumpriram o calendário de divulgação). O valor usado é uma interpolação linear entre o Censo 2022 e a estimativa 2024 (ver `_interpola_ano_faltante` em `src/fetch_populacao.py`) — um valor sintético, não uma medição.
- **2026 é um ano parcial** (dados só até por volta de junho/2026, e sem estimativa de população do IBGE ainda — só sai em ago/set de 2026). Não há linha de população para 2026, e a tabela de taxa fica com `NaN` nesse ano em vez de um valor calculado sobre dado incompleto.
- **"NÃO INFORMADO"** aparece como um valor de município em 2018 (Ameaça e Lesão Corporal): são casos sem município identificado na base original, mantidos para não perder casos do total, mas não é um município real — exclua-o de qualquer análise por município.
