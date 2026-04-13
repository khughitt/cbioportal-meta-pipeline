# cbioportal — Agent Instructions

## Project Overview

`cbioportal` is a Snakemake-driven meta-analysis pipeline that aggregates somatic-mutation data
across public cBioPortal studies (plus AACR GENIE) to produce cross-study mutation-frequency
tables, gene x cancer matrices, per-study correlation matrices, and clusterings of both genes
and cancer types. The driving research question is: "What is the structure of somatic mutations
within and across cancer types, and which gene-cancer associations recur across independent
cBioPortal studies?"

## Active Roots

| Path | Purpose |
|------|---------|
| `code/workflows/` | Snakefile (master workflow) |
| `code/scripts/` | Python (+ one Rmd) scripts invoked by Snakemake rules |
| `code/config/` | Pipeline run configs (config-10k-genes.yml, config-full.yml, config-pan-cancer.yml) |
| `code/notebooks/` | Ad-hoc analysis notebooks (marimo preferred) |
| `data/` | Reference data (gene mappings, UniProt protein lengths, cancer type lists) |
| `doc/` | Science-managed documentation (questions, methods, datasets, searches, discussions, interpretations, reports, plans, meta, background) |
| `tasks/` | Task backlog managed via science-tool |
| `specs/` | Formal specifications / pre-registrations |
| `knowledge/` | Project knowledge graph artifacts |
| `results/` | Pipeline outputs (not committed) |
| `models/` | Serialized models / derived artifacts |
| `papers/` | Bibliography (BibTeX + `pdfs/` — pdfs gitignored) |
| `archive/` | Superseded material (old EDA, study-specific scratch, legacy R artifacts) |

## Running The Pipeline

```bash
uv sync
uv run snakemake -s code/workflows/Snakefile -j1 --configfile code/config/config-10k-genes.yml
```

Notes:
- Snakemake is invoked from the repo root so that `data/` input paths (e.g.,
  `data/uniprotkb_hsapiens_protein_lengths.tsv.gz`) resolve correctly.
- `script:` paths inside the Snakefile are relative to the Snakefile itself and point to
  `../scripts/*.py`.
- AACR GENIE requires a synapse.org account; those inputs must be downloaded manually into the
  configured `data_dir` before running the pipeline. See
  <https://www.synapse.org/Synapse:syn21683345>.

## Languages & Tools

- **Python**: pandas, pyarrow, scikit-learn, seaborn, snakemake
- **R**: one remaining summary.Rmd in `code/scripts/` (planned to be ported to Python/marimo)
- **Snakemake 9**: workflow orchestration
- **uv**: Python package management (never pip)
- **science-tool**: installed as editable dev dependency, resolved via `SCIENCE_TOOL_PATH` in `.env`

## Conventions

- Feather (`.feather`) is the canonical on-disk format for intermediate tables
- "Long" tables for per-entity counts/ratios; matrices for gene x cancer / gene x patient views
- File naming: row-index entity listed first, column-index entity second
  (e.g., `gene_cancer_dataset.feather` = genes along rows, (cancer, dataset) combined along columns)
- Files with `_ratio` in the name report sample-level mutation ratios
- Prefer `pathlib` over `os.path`; vectorized pandas; functional style
- Python: ruff formatting, 120-char line limit, type hints required
- Use `rich` for CLI output, `click` for multi-argument CLIs
- For ad-hoc analysis, prefer marimo notebooks with altair over Jupyter

## Validation

```bash
# Science framework validation
bash validate.sh --verbose

# Lint the Snakemake workflow
uv run snakemake --lint -s code/workflows/Snakefile --configfile code/config/config-10k-genes.yml

# Python checks
uv run --frozen ruff check code/
uv run --frozen ruff format --check code/
```

## Data Sensitivity

- cBioPortal study downloads are public and gitignored via `archive/` patterns; never commit bulk
  mutation TSVs to git.
- AACR GENIE data is access-controlled; never commit GENIE files.
- The small reference files in `data/` (gene mappings, cancer type lists, UniProt lengths) are
  version-controlled.

## Operational Constraints

- Do NOT create "legacy" / "compatibility" layers during refactors — target the new layout only.
- Preserve 100% of pipeline functionality when refactoring unless explicitly told otherwise.
- Document desired structure + clean-up lists in `doc/plans/` before large refactors.
- Use `uv add` / `uv run`; never `pip install`.
