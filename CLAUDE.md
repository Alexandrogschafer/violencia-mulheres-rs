# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

This repository currently contains **only raw source data** — `src/`, `outputs/figures/`, and `outputs/tables/`
are empty placeholder directories. There is no build system, package manifest, linter, or test suite yet, and
this is not (yet) a git repository. Whatever pipeline processes `data/raw/` into `outputs/` still needs to be
built. When you add code, prefer creating the actual tooling (requirements.txt/pyproject.toml, a runner script,
etc.) rather than assuming one already exists elsewhere.

## What this data is

The `data/raw/*.xlsx` files are official monitoring spreadsheets on violence against women and girls in the
state of Rio Grande do Sul (RS), Brazil, sourced from SIP/PROCERGS (the state's public safety data system) and
published by an "Observatório" (the footer credits `SIP/PROCERGS`). They track crimes prosecuted under Brazil's
Lei Maria da Penha (domestic violence law):

- **Feminicídio Tentado** — attempted femicide
- **Feminicídio Consumado** — completed femicide
- **Ameaça** — threats
- **Estupro** — rape
- **Lesão Corporal** — bodily injury
- **Geral** — combined total across the above categories

There are two file shapes:

- `violencia_2012_2017.xlsx` — one consolidated historical workbook covering 2012–2017.
- `violencia_2018.xlsx` … `violencia_2026.xlsx` — one workbook per single year (2026 is a partial/in-progress
  year, updated as new months land).

## Raw workbook structure (read this before writing any parser)

Each workbook has a sheet per crime category plus a `Geral` (overview) sheet. **Sheet-to-file mapping (`rId` →
`sheetN.xml`) is not stable across workbooks** — resolve sheet names via `xl/workbook.xml` +
`xl/_rels/workbook.xml.rels` per file rather than assuming e.g. "Geral" is always `sheet1.xml` or `sheet2.xml`.

Two distinct table layouts appear, depending on sheet and file:

1. **`Geral` sheet, per-year files (2018+)**: state-wide monthly totals for a single year. Rows = crime
   categories (including a `Geral` total row), columns = `Jan…Dez` + `Total`. One block per file, starting
   around row 3/4.
2. **`Geral` sheet, the 2012–2017 consolidated file**: the same monthly-totals layout, but with one block per
   year stacked vertically (2012's block, then 2013's, etc.), each with its own title row, header row, and a
   trailing "Fonte: ..." source/footnote row. You must detect block boundaries (blank rows / repeated header
   text) rather than assuming a fixed row count per year.
3. **Per-category sheets (`Feminicídio Tentado`, `Feminicídio Consumado`, `Ameaça`, `Estupro`, `Lesão
   Corporal`)**: one row per RS municipality (all ~500 municipalities, uppercase names, no accents, e.g.
   `AGUA SANTA`, `AJURICABA`).
   - In per-year files: columns are `Jan…Dez` + `Total` for that single year.
   - In the 2012–2017 consolidated file: columns are one per year (`2012…2017`) + `Total` + `% vítimas/total`
     + `População de mulheres` + `Mulheres vítimas por 10.000 habitantes em 2016` (a normalized rate column —
     only computed for the file's reference year, not per-year).

Known inconsistencies across files to normalize/handle defensively:

- **Spelling changed**: sheets/labels say `Femicídio` in the 2012–2017 file but `Feminicídio` from 2018
  onward. Match on a normalized/fuzzy category name, not an exact string.
- **Sheet order changed**: `Feminicídio Tentado` and `Feminicídio Consumado` swap order starting with the 2023
  file. Match sheets by name, never by position/index.
- A hidden `Fórmulas - Demais indicadores` helper sheet exists in the 2012–2017, 2018, and 2019 files only;
  later files drop it.
- Month header labels vary between full names (`Janeiro`, `Fevereiro`, ...) in the 2012–2017 file and
  three-letter abbreviations (`Jan`, `Fev`, ...) in per-year files.
- Empty/not-yet-occurred months in the current partial year are empty strings, not zeros — don't coerce blindly
  to `0` without distinguishing "no data yet" from "zero incidents."
- Every `Geral` sheet ends with a `Fonte: SIP/PROCERGS - Atualizado em <date>` footer row and, in newer files,
  an "Observações" section noting that figures are provisional and subject to revision as investigations
  conclude (duplicate-record cleanup, forensic findings, etc.) — treat later-dated extracts of the same year as
  more authoritative than earlier ones.
- Some sheets also embed native Excel charts (`xl/charts/*.xml`) — irrelevant for data extraction, but they're
  why the `.xlsx` files are large.

No parsing library is currently installed in this environment (no `pip`, no `openpyxl`/`pandas`, no
LibreOffice/`ssconvert`). If you need to inspect a workbook's contents ad hoc without adding a dependency, treat
`.xlsx` as a zip of OOXML: read `xl/workbook.xml` + `xl/_rels/workbook.xml.rels` to resolve sheet names to
`xl/worksheets/sheetN.xml`, and resolve `t="s"` cell values via the `<si>` entries in `xl/sharedStrings.xml`
(both readable with Python's stdlib `zipfile` + `xml.etree.ElementTree`, no third-party packages needed).
