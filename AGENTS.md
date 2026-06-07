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
- The t077 pooled meta-analysis (`rule run_gene_cancer_meta_analysis`) is the only R rule in the
  default DAG and runs in an isolated conda env (`code/envs/r-meta.yml`: r-metafor / r-arrow /
  r-lme4). It is reached by the canonical `gene_cancer_study_ratio_annotated.feather` target, so a
  full `rule all` needs `--use-conda --conda-frontend mamba`. System R is **not** sufficient (lacks
  `arrow`). If the first env build dies with `sqlite3.OperationalError: database is locked` inside
  `conda_libmamba_solver` (a flaky repodata-shards race in conda-libmamba-solver ≥26.4 — many
  threads on one sqlite cache), prefix the invocation with `CONDA_REPODATA_THREADS=1` to serialize
  the shard fetches.

## Languages & Tools

- **Python**: pandas, pyarrow, scikit-learn, seaborn, snakemake
- **R**: one remaining summary.Rmd in `code/scripts/` (planned to be ported to Python/marimo)
- **Snakemake 9**: workflow orchestration
- **uv**: Python package management (never pip)
- **science**: installed as editable dev dependency

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

## Annotations applied in the pipeline

The canonical outputs of the cross-study aggregation are the **annotated** feathers — see
`doc/guides/canonical-outputs.md` for the full DAG and which outputs are intermediate vs
consumer-facing.

- **Bailey 2018 driver overlay** (`code/scripts/annotate_drivers.py`) — adds
  `bailey2018_driver` boolean + `bailey2018_source` version stamp to both the count table
  (`gene_cancer_study_annotated.feather`) and ratio table (chained into the CH annotation
  output below). Manual prereq: `data/bailey2018_table_s1.xlsx`.
- **CH-aware annotation** (`code/scripts/annotate_ch.py`, closes audit F3 / F7) — adds
  `ch_priority_gene` flag (7-gene Bolton 2020 list: DNMT3A, PPM1D, TET2, TP53, ASXL1, CHEK2,
  PRPF8) plus `mean_matched` / `mean_unmatched` stratified pooled ratios. Consumes the
  `matched_normal_studies` config list — populate per-run with study IDs known to use
  patient-matched normal sequencing. See `topic:clonal-hematopoiesis-contamination`.
- **Hypermutator / TMB annotation** (plan `doc/plans/2026-04-13-t081-hypermutator-annotation-
  pipeline-plan.md`; closes audit F1 / F4 / F6; tasks `t081` / `t092`–`t099`) — a staged
  pipeline that computes per-sample TMB (`compute_per_sample_tmb`), detects POLE/POLD1 hotspots
  (`detect_polymerase_hotspots`), ingests MSI status (`convert_to_feather.py` extension via
  `msi_normalization.py`), fits per-cancer-type GMM on log10 TMB (`fit_per_cancer_tmb_gmm`),
  and writes a canonical composite annotation at `metadata/samples_annotated.feather`
  (`annotate_hypermutators`). Columns: `hypermutation_score` (0-1), `is_hypermutator` (bool),
  `hypermutator_reason` (8-category audit trail: `pole_hotspot` / `pold1_hotspot` / `msi_h` /
  `gmm_upper_mode` / `gmm_lower_mode` / `zscore_fallback_high` / `zscore_fallback_low` /
  `tmb_unavailable`), plus three parallel views (`is_hypermutator_absolute` ≥10 mut/Mb
  Campbell 2017, `is_hypermutator_ultra` ≥100 mut/Mb, `is_hypermutator_relative` per-histology
  top-20% Samstein 2019). The rule ordering inside the composite is fixed by plan finding #4:
  POLE > POLD1 > MSI-H > GMM > z-score > NaN, so that clinical diagnostic categories win over
  TMB. `create_freq_tables.py` and `create_combined_gene_cancer_freq_table.py` emit paired
  `_inclusive` / `_exclusive` columns keyed on this flag (see
  `modality-guide:cross-study-aggregation` row `agg.15`). Threshold / filter configuration:
  `random_seed` (default 0 — reproducibility covenant, plan review finding #1),
  `gmm_min_samples` (default 100 — below this the rule falls back to a 10×median rule),
  `panel_callable_mb_override` + `wes_default_callable_mb` + `panel_callable_mb_tolerance`
  drive the TMB denominator via `build_panel_callable_sizes`. See
  `topic:tumor-mutational-burden`.

### Optional ingest-time label canonicalization

`convert_to_feather.py` applies deterministic t083 cleanup to clinical sample labels:
whitespace is stripped/collapsed for `cancer_type`, `cancer_type_detailed`, `primary_site`,
`sample_class`, `sample_type`, and `sample_type_detailed`; `oncotree_code` is also uppercased.
Run configs may provide `cancer_type_alias_map`, `cancer_type_detailed_alias_map`,
`primary_site_alias_map`, and `oncotree_code_alias_map` to collapse known study-specific labels
without adding an external OncoTree table.

### Mutational-signature exposure hardening (t178 / t179)

`code/scripts/run_restricted_sigprofiler_assignment.py` (rules
`run_restricted_sigprofiler_assignment` + `..._per_sample`) feeds per-sample signature
exposures into the h08 agnostic covariate-association scan
(`method:h08-agnostic-association-model`). Two audit/guard passes harden those exposures:

- **t178 — signature-reference + caller provenance.** The COSMIC SBS catalog version is
  pinned + logged at run time and asserted to exist (`signature_assignment_cosmic_version`,
  default `3.5` GRCh37 exome — no silent fallback). At load time each requested + positive-
  control signature (notably SBS9 / SBS54) is audited against the loaded reference; absent
  signatures emit a loud "would be absorbed by nearest neighbours" warning and are recorded
  in the `*.signature_audit.feather` sidecar. A per-study caller-consensus flag
  (`caller_consensus` column) is propagated from `multi_caller_consensus_studies` /
  `single_caller_studies` config lists — safe default = **unknown** (`None`), never assumed
  consensus (single-caller studies risk artefactual de-novo signatures, Jiang2025).
- **t179 — per-sample count floor + de-novo-vs-refit decision.** A configurable per-sample
  SBS-count floor (`signature_min_sbs_count_wes` default 383;
  `signature_min_sbs_count_matched_normal` default 100) adds `total_sbs_count`,
  `count_floor`, `passes_count_floor` columns; sub-floor samples are flagged (loud
  missingness), not silently dropped. A per-cancer-type {`de_novo`, `refit`} decision keyed
  on sample size (`signature_denovo_min_samples`, default 200) + caller provenance is
  recorded in the `*.denovo_decision.feather` sidecar. The script only *records* the
  decision; it remains assignment/refit-based and does not run a de-novo extractor.

The final ratio output `gene_cancer_study_ratio_annotated.feather` carries the gene-level
overlays, the CH-aware annotations, and the joined t077 pooled meta-analysis columns
(`pooled_*_{inclusive,exclusive}`, `k_studies_{inclusive,exclusive}`,
`status_{inclusive,exclusive}`, etc.). Consumers should prefer the `_annotated` versions; the
unannotated `gene_cancer_study.feather` and `gene_cancer_study_ratio.feather` are
intermediates.

## Alternate data sources

- **MC3 TCGA pan-cancer unified MAF** (`code/scripts/process_mc3.py`, closes audit F2 for the
  TCGA portion) — ingests the Ellrott 2018 unified 7-caller-consensus MAF as a single
  pseudo-study `tcga_mc3`. 2.9M PASS variants / 9,104 samples / 32 TCGA cancer types in one
  file, replacing heterogeneous per-study cBioPortal TCGA MAFs. **To enable**: add
  `"tcga_mc3"` to the `studies` list in your run config, and add it to
  `matched_normal_studies` as well (MC3 is matched-normal by design). Requires:
    - `data/mc3.v0.2.8.PUBLIC.maf.gz` (GDC PASS release, ~720 MB).
    - `data/tcga_case_to_project.tsv` (submitter_id -> TCGA project_id; fetched once from
      the GDC API).
    - source: https://gdc.cancer.gov/about-data/publications/mc3-2017

## External Reference Datasets (manual prerequisites)

Some pipeline rules depend on external datasets that cannot be auto-fetched:

- **`data/bailey2018_table_s1.xlsx`** — Bailey et al. 2018 (Cell) Table S1; PanCanAtlas
  299-driver consensus + per-cancer rosters. Manual download from the Cell article supplement
  (PMID 30096302). Consumed by `rule process_bailey2018_drivers` and
  `rule annotate_drivers_in_gene_cancer_table`.
- **`data/genie_v9.1-public/`** — AACR Project GENIE per-assay BED files. Requires a Synapse
  account + Data Use Agreement (https://www.synapse.org/Synapse:syn7222066,
  release v9.1 at syn24179663). Consumed by `rule process_genie_panel_coverage`.

Optional (R-dependent):

- **`code/scripts/run_dndscv.R`** runs Martincorena 2017's selection-based driver detection
  per study. Requires R + Bioconductor + `devtools::install_github("im3sanger/dndscv")`.
  Output `studies/{id}/mut/dndscv/genes.feather` is not in `rule all` by default — opt in
  by adding to your config or the `all` target list.

## Validation

```bash
# Science framework validation
uv run --frozen science validate --verbose

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

<!-- BEGIN: load-bearing-constraints (managed by /science:curate; edit core/decisions.md instead) -->
## Load-bearing constraints

<!-- One bullet per active decision in core/decisions.md, phrased as an
imperative rule. The "why" stays in core/decisions.md. -->

- _none yet — populated by `/science:curate` once `core/decisions.md` has entries._

<!-- END: load-bearing-constraints -->
