---
id: "plan:2026-04-24-t052-cohort-stage-descriptor-design"
type: "plan"
title: "Design: t052 — per-study cohort-stage descriptor"
status: "active"
related:
  - "task:t052"
  - "topic:cohort-selection-bias-representativeness"
source_refs:
  - "paper:Zehir2017"
created: "2026-04-24"
updated: "2026-04-24"
---

# Design: t052 — per-study cohort-stage descriptor

## Purpose

Ingest per-sample primary-vs-metastatic and treatment-status annotation from cBioPortal
clinical sample tables and roll it up to a per-study cohort-composition descriptor.
Validate the design by reproducing the published Zehir 2017 stage-driven bias signals
(AR 18% MSK metastatic vs 1% TCGA primary; ESR1 11% vs 4%; EGFR T790M 11.3% GENIE vs
2.2% TCGA) on the existing PoC pipeline run.

## Scope

This task delivers:

1. **Descriptor ingestion** — per-sample `is_metastatic` and `is_pre_treated` flags
   driven by sample-level cBioPortal metadata with a study-level registry fallback.
2. **Per-study composition rollup** — a summary feather with per-study percentages and
   dominance classes (`primary_dominant` / `metastatic_dominant` / `mixed`).
3. **Diagnostic interpretation** — a one-shot stratified-rate comparison against the
   Zehir 2017 published numbers, with a pre-registered verdict (`reproduces` / `partial`
   / `fails`).

Out of scope for t052: rewriting the pooled-ratio surface to emit
`pooled_ratio_primary` / `pooled_ratio_metastatic` columns. That is downstream work
gated on the diagnostic verdict landing as `reproduces` or `partial`.

## Architecture (Approach 1: per-study rule with summary rollup)

The annotation runs per-study and is rolled up at summary time, mirroring the existing
pipeline pattern (`annotate_drivers`, `annotate_ch`, `annotate_hypermutators`). The
diagnostic report is a standalone opt-in script, mirroring `compute_sbs1_lrr_bias_per_study.py`
from t126.

### File layout

| Path | Purpose |
|---|---|
| `data/cbioportal_study_cohort_profiles.tsv` | Hand-curated registry: per-study rows + family-pattern rows |
| `code/scripts/annotate_cohort_stage.py` | Per-study annotation: emits `samples_stage_annotated.feather` |
| `code/scripts/build_study_cohort_composition.py` | Summary-level rollup: emits `study_cohort_composition.feather` |
| `code/scripts/compare_stage_stratified_gene_rates.py` | Diagnostic: AR/ESR1 per-stage rate table (standalone, opt-in) |
| `code/scripts/tests/test_annotate_cohort_stage.py` | Classification rules + precedence |
| `code/scripts/tests/test_build_study_cohort_composition.py` | Rollup math |
| `code/scripts/tests/test_compare_stage_stratified_gene_rates.py` | Diagnostic stratification |
| `doc/interpretations/2026-04-24-t052-stage-stratified-ar-esr1.md` | AR/ESR1 closure note |

### Pipeline outputs

| Path | Content |
|---|---|
| `studies/<id>/metadata/samples_stage_annotated.feather` | Per-sample `is_metastatic`, `is_pre_treated`, audit-trail columns added to existing `samples.feather` schema |
| `summary/metadata/study_cohort_composition.feather` | Per-study percentages + dominance classes |
| `results/t052-stage-stratified-2026-04-24/summary/stage_stratified_gene_rates.feather` | Diagnostic output for AR/ESR1 validation |

## Registry (`data/cbioportal_study_cohort_profiles.tsv`)

### Schema

| column | type | meaning |
|---|---|---|
| `pattern` | str | exact `study_id` OR glob pattern (e.g., `*_tcga_pan_can_atlas_*`) |
| `pattern_kind` | enum | `study_id` (exact match) or `glob` (fnmatch) |
| `default_is_metastatic` | enum str | `true` / `false` / `unknown` |
| `default_is_pre_treated` | enum str | `true` / `false` / `unknown` |
| `priority` | int | resolution rank when multiple patterns match (lower = wins) |
| `source` | str | one-sentence justification with citation |
| `notes` | str | freeform |

### Storage convention

The TSV uses string enum values for human readability (diff-friendly text file). The
annotation script parses `true` / `false` / `unknown` strings into pandas nullable
booleans (`True` / `False` / `pd.NA`) for the output feather. Downstream consumers get
proper missing-value semantics.

### Initial registry contents (~6 rows)

| pattern | pattern_kind | default_is_metastatic | default_is_pre_treated | priority | source |
|---|---|---|---|---|---|
| `*_tcga_pan_can_atlas_*` | glob | false | false | 100 | TCGA mission: primary untreated specimens (Cancer Genome Atlas Research Network 2008) |
| `tcga_mc3` | study_id | false | false | 50 | Ellrott 2018: TCGA matched-normal pan-cancer MAF, primary tumor specimens |
| `msk_impact_*` | glob | unknown | unknown | 100 | MSK-IMPACT clinical sequencing: mixed primary/metastatic, sample-level fields override (Zehir 2017) |
| `genie` | study_id | unknown | unknown | 100 | AACR GENIE: clinical sequencing, mixed; sample-level SAMPLE_TYPE drives override |
| `metastatic_solid_tumors_mich_2017` | study_id | true | unknown | 10 | Robinson 2017 MET500: all metastatic by design |
| `pog570_bcgsc_2020` | study_id | true | true | 10 | BCGSC POG-570: metastatic, post-treatment by design |

### Resolution order

For each sample, each axis (metastatic, treatment) resolves independently:

1. **Sample-level metadata extraction** (highest precedence) — when `sample_type` /
   `sample_class` / `SAMPLE_TYPE_DETAILED` carry a recognized value for that axis.
2. **Registry row matching `study_id` exactly** with the lowest `priority` value.
3. **Registry row matching `glob` pattern** with the lowest `priority` value.
4. **Fallback `unknown`** (`pd.NA` in the output).

Each output row carries a `cohort_stage_source` column recording which step won
(`sample_metadata` / `registry_study` / `registry_glob` / `fallback_unknown`) for
audit trail.

## Sample-level metadata classification rules

### Source fields consulted (priority order per axis)

For `is_metastatic`:

1. `sample_type` (most reliable when present)
2. `sample_class`
3. `SAMPLE_TYPE_DETAILED`
4. `METASTATIC_SITE` (presence implies `is_metastatic=True`)

For `is_pre_treated`:

1. `SAMPLE_TYPE_DETAILED` (sometimes carries explicit "Post-treatment" markers)
2. `SPECIMEN_TYPE` (rare but occasionally informative)
3. — most cBioPortal studies do not carry per-sample treatment status; falls through
   to the registry default

### Value mappings

```python
METASTATIC_VALUE_MAP = {
    "Metastasis": True,
    "Metastatic": True,
    "Recurrence": True,
    "Local Recurrence": True,
    "Distant Metastasis": True,
    "Primary": False,
    "Primary Tumor": False,
    "Primary Solid Tumor": False,
}

PRE_TREATED_VALUE_MAP = {
    "Post-treatment": True,
    "Pretreated": True,
    "Treated": True,
    "Pre-treatment": False,
    "Treatment-naive": False,
    "Naive": False,
}
```

### Resolution rule per sample

- If a sample's source field value is in the mapping for either axis, that value wins
  for that axis (independently — one axis can resolve via metadata while the other
  falls through to registry).
- A non-empty `METASTATIC_SITE` value forces `is_metastatic = True` even if
  `sample_type` is missing.
- The two axes resolve **independently**: a sample can have `is_metastatic = True`
  (from `sample_type`) and `is_pre_treated = unknown` (no per-sample treatment field)
  in the same row.
- Unknown values (e.g., `"FFPE"` in `sample_type`) fall through cleanly to the registry
  default.

## Output schemas

### `studies/<id>/metadata/samples_stage_annotated.feather`

| column | type | source | notes |
|---|---|---|---|
| (all existing `samples.feather` columns) | — | passthrough | preserves upstream schema |
| `is_metastatic` | nullable bool | derived | `True` / `False` / `pd.NA` |
| `is_pre_treated` | nullable bool | derived | `True` / `False` / `pd.NA` |
| `cohort_stage_source` | category | derived | `sample_metadata` / `registry_study` / `registry_glob` / `fallback_unknown` |
| `cohort_stage_metastatic_field` | category | derived | which source field resolved the metastatic axis (`sample_type` / `METASTATIC_SITE` / `registry` / `none`) |
| `cohort_stage_treatment_field` | category | derived | parallel for the treatment axis |

The `*_field` columns are the audit trail — they let downstream consumers reconstruct
*why* a sample landed where it did without rerunning the rule.

### `summary/metadata/study_cohort_composition.feather`

One row per study:

| column | type | meaning |
|---|---|---|
| `study_id` | str | |
| `n_samples_total` | int | from `samples.feather` |
| `n_metastatic` | int | count where `is_metastatic == True` |
| `n_primary` | int | count where `is_metastatic == False` |
| `n_metastatic_unknown` | int | count where `is_metastatic` is `pd.NA` |
| `pct_metastatic` | float | `n_metastatic / n_samples_total` |
| `pct_primary` | float | parallel |
| `pct_metastatic_unknown` | float | parallel |
| `n_pre_treated` | int | count where `is_pre_treated == True` |
| `n_naive` | int | count where `is_pre_treated == False` |
| `n_pre_treated_unknown` | int | count where `is_pre_treated` is `pd.NA` |
| `pct_pre_treated` | float | |
| `pct_naive` | float | |
| `pct_pre_treated_unknown` | float | |
| `dominant_site_class` | category | `primary_dominant` / `metastatic_dominant` / `mixed` / `unknown_dominant` (≥80% threshold for "dominant") |
| `dominant_treatment_class` | category | parallel |

### `results/t052-stage-stratified-2026-04-24/summary/stage_stratified_gene_rates.feather`

One row per `(study_id, cancer_type, gene, is_metastatic)` cell:

| column | type | meaning |
|---|---|---|
| `study_id` | str | |
| `cancer_type` | str | |
| `gene` | str | restricted to focal genes (AR, ESR1, EGFR for the closure note) |
| `is_metastatic` | nullable bool | stratification axis |
| `n_samples` | int | denominator |
| `n_mutated` | int | numerator (samples with ≥1 non-silent mutation in gene) |
| `mutation_rate` | float | |
| `expected_zehir2017` | float | published comparison value where applicable |

## Diagnostic report

### Focal comparisons

| Gene | Cancer | Published bias (Zehir 2017) | Comparison cohorts |
|---|---|---|---|
| AR | Prostate Cancer | MSK metastatic 18% vs TCGA primary 1% | `msk_impact_2017` Prostate Cancer (`is_metastatic=True`) vs `tcga_mc3` PRAD |
| ESR1 | Breast Cancer | MSK metastatic 11% vs TCGA primary 4% | `msk_impact_2017` Breast Cancer (`is_metastatic=True`) vs `tcga_mc3` BRCA |
| EGFR (T790M) | Non-Small Cell Lung | MSK metastatic 11.3% vs TCGA primary 2.2% | reported only if both cohorts have ≥30 lung samples; otherwise omitted with explicit note |

### Source data

The existing `results/poc-2026-04-17/` PoC artifact already contains all 4 PoC studies'
`samples.feather` and `mut.feather` across all cancer types. No new pipeline run needed.

The diagnostic script:

1. Loads `samples.feather` for `tcga_mc3` and `msk_impact_2017`.
2. Re-runs the stage annotation in-memory using the registry + rules (so the diagnostic
   is self-contained and doesn't depend on having previously executed `annotate_cohort_stage`
   rules in Snakemake).
3. Filters samples by `cancer_type` + `is_metastatic` flag.
4. Counts gene mutations per stratum from `mut.feather` (filtering to non-synonymous
   `consequence` values).
5. Emits the stratified-rate feather + a markdown table for the interpretation doc.

### Pre-registered verdict thresholds

The verdict is **per focal comparison** (one each for AR / ESR1 / EGFR). Each comparison
independently lands in one of four states:

| Outcome | Definition | What it means |
|---|---|---|
| **reproduces** | Both metastatic and primary rates fall within ±3 percentage points of Zehir 2017 published numbers | The descriptor mechanism works as intended for this gene |
| **partial** | Direction matches (metastatic > primary) but at least one magnitude differs by >3 pp | Descriptor captures real bias but a confound (cancer-type-detailed mismatch, mutation-call differences, panel version) is shifting absolute numbers |
| **fails** | Direction does not match (metastatic ≤ primary) | Indicates a problem with the classification rules for this gene/cancer pair |
| **underpowered** | Either stratum has `n_samples < 20` | Reported but not interpreted; CI too wide to discriminate any of the other three outcomes |

The interpretation document reports all three per-gene verdicts plus an **aggregate
closure-state**:

- **descriptor validated** — at least 2 of 3 comparisons land `reproduces` or `partial`,
  and 0 land `fails` (underpowered comparisons don't count against). Closure: the
  descriptor is ready for downstream pooled-ratio rewrites in a follow-up task.
- **descriptor needs investigation** — any comparison lands `fails`. Closure: the
  descriptor lands but does not validate against published numbers; investigate before
  stratifying pooled outputs.
- **insufficient evidence** — fewer than 2 comparisons reach a verdict (i.e., majority
  underpowered). Closure: the descriptor lands but the diagnostic could not exercise it
  on this PoC surface; rerun on a larger study list before drawing conclusions.

## Snakemake integration

```python
rule annotate_cohort_stage:
    input:
        samples = "results/{run}/studies/{study}/metadata/samples.feather",
        registry = "data/cbioportal_study_cohort_profiles.tsv",
    output:
        "results/{run}/studies/{study}/metadata/samples_stage_annotated.feather",
    script:
        "../scripts/annotate_cohort_stage.py"

rule build_study_cohort_composition:
    input:
        expand(
            "results/{{run}}/studies/{study}/metadata/samples_stage_annotated.feather",
            study=config["studies"],
        ),
    output:
        "results/{run}/summary/metadata/study_cohort_composition.feather",
    script:
        "../scripts/build_study_cohort_composition.py"
```

`annotate_cohort_stage` consumes the existing per-study `samples.feather` from
`convert_to_feather` (no new dependency on other annotation rules). It runs in parallel
with `annotate_drivers` and `annotate_ch`. `build_study_cohort_composition` runs once at
summary time.

`compare_stage_stratified_gene_rates.py` is **not** wired into the Snakefile — it's a
one-shot CLI invocation against the existing `results/poc-2026-04-17/` artifact.

## Testing

For `annotate_cohort_stage.py` (7 tests):

1. Sample-level metadata wins over registry when both apply.
2. Registry `study_id` row wins over `glob` row when both match.
3. Glob pattern with leading wildcard matches correctly.
4. Non-empty `METASTATIC_SITE` forces `is_metastatic=True` even when `sample_type` is missing.
5. Each axis resolves independently (one axis can land `True`, the other `pd.NA`).
6. `cohort_stage_source` and `*_field` columns record the resolution path correctly.
7. Unknown sample-metadata values fall through cleanly to registry.

For `build_study_cohort_composition.py` (3 tests):

1. Percentages sum to 1.0 within each axis.
2. `dominant_*_class` correctly assigns at the ≥80% threshold.
3. Empty-study edge case (n_samples=0) doesn't produce NaN — explicit row with
   `dominant_*_class = "unknown_dominant"`.

For `compare_stage_stratified_gene_rates.py` (3 tests):

1. Filtering by `is_metastatic` matches expected sample counts on a 4-row toy fixture.
2. Verdict assignment respects the ±3 pp threshold (one test per outcome).
3. `n_samples < 20` strata are flagged as "underpowered" and not used in verdict assignment.

**Total**: 13 tests across 3 modules. Lint/format pass required before commit.

## Validation gate

Before claiming closure:

- All 13 tests pass.
- `uv run --frozen ruff check code/` passes for new files.
- `uv run --frozen ruff format --check code/` passes for new files.
- Snakemake `--lint` does not regress.
- The diagnostic produces a verdict (`reproduces` / `partial` / `fails`) with explicit
  numbers in `doc/interpretations/2026-04-24-t052-stage-stratified-ar-esr1.md`.

## Out of scope (potential follow-up tasks)

- Rewriting `gene_cancer_study_ratio_annotated.feather` to emit per-stage stratified
  ratio columns (`pooled_ratio_primary`, `pooled_ratio_metastatic`). Gated on a
  `reproduces` verdict from this task.
- Per-study cohort-stage descriptor rows in any cross-project knowledge graph.
- Treatment-status ingestion from cBioPortal patient-level (rather than sample-level)
  clinical tables. Most studies don't carry it at sample level; promoting from patient
  level is its own ingestion challenge.
