# Capítulo — Geotecnologias

Material editorial do capítulo submetido à coletânea *Geotecnologias: análises,
técnicas e aplicações em pesquisa*, sobre o fluxo geotecnológico por trás do portal
deste projeto: a consolidação dos dados de violência contra a mulher da SSP/RS
(via SIP/PROCERGS), o acoplamento com a malha municipal do IBGE e a publicação do
mapa interativo de taxas por município.

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `00_gestao/` | Gestão do processo editorial (submissão, correspondência com a organização, prazos). |
| `01_referencias/` | Referências bibliográficas — ver `01_referencias/README.md`. |
| `02_texto/` | Seções do capítulo, uma por arquivo: `00_metadados`, `01_introducao`, `02_fundamentacao`, `03_materiais`, `04_metodo`, `05_resultados`, `06_limites`, `07_consideracoes`, `08_disponibilidade`. |
| `03_figuras/` | Figuras finais do capítulo, em resolução de impressão. |
| `04_versoes/` | Versões submetidas/revisadas do manuscrito. |

## Escopo

Esta pasta é **material editorial** e está **fora do escopo do registro de
programa de computador junto ao INPE/DIT**, que cobre apenas `src/` e `docs/`.

## Figuras

`03_figuras/` **é versionado** — diferente de `outputs/figures/` (saída
regenerável do pipeline, ignorada no git). As figuras aqui são produto final do
capítulo, no mesmo espírito de `data/processed/` e `docs/`: versionadas porque
representam o resultado citável, não um artefato intermediário descartável.

## Pendências

- [ ] Confirmar normas da editora (formatação, referências, template) e limite de páginas.
- [ ] Gerar as figuras do capítulo em resolução de impressão — hoje o pipeline
      (`src/analysis/`, notebooks) só produz PNG a 150 dpi, pensado para o portal
      web, não para publicação impressa.
- [ ] Obter/atualizar `01_referencias/*.bib` (fonte única de verdade das referências).
- [ ] Escrever as seções em `02_texto/`.
