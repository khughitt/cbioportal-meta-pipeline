---
type: plan
title: "Design: t052 \u2014 per-study cohort-stage descriptor (v2)"
status: active
created: '2026-04-24'
updated: '2026-06-28'
id: plan:0003-t052-cohort-stage-descriptor-design
related:
- task:t052
- topic:cohort-selection-bias-representativeness
source_refs:
- paper:Zehir2017
---

# Design: t052 — per-study cohort-stage descriptor (v2)

> **Revision history**
>
> - **v1 (2026-04-24, commit `4672e0a`)** — initial design.
> - **v2 (2026-04-25)** — incorporates user code review. Major changes: validation
>   scope drops EGFR/T790M and `tcga_mc3` (neither is on disk in the existing PoC
>   artifact) and adds `prad_tcga_pan_can_atlas_2018` as a prerequisite ingestion;
>   audit-trail columns split per axis; METASTATIC_SITE sentinel handling fixed;
>   value normalization added; registry validation added; mutation filtering uses
>   `variant_class` (not `consequence`) to match existing pipeline convention;
>   diagnostic uses a comparison-manifest TSV and imports `annotate_cohort_stage`
>   functions directly.

## Purpose

Ingest per-sample primary-vs-metastatic and treatment-status annotation from cBioPortal
clinical sample tables and roll it up to a per-study cohort-composition descriptor.
Validate the design by reproducing the published Zehir et al. [@Zehir2017] stage-driven bias signals
(AR 18% MSK metastatic vs 1% TCGA primary; ESR1 11% vs 4%) on the existing PoC pipeline
run, augmented with `prad_tcga_pan_can_atlas_2018` for the AR comparison.
This is the design surface for `task:t052` and belongs under
`topic:cohort-selection-bias-representativeness`.

## Scope

This task delivers:

1. **Descriptor ingestion** — per-sample `is_metastatic` and `is_pre_treated` flags
   driven by sample-level cBioPortal metadata with a study-level registry fallback.
2. **Per-study composition rollup** — a summary feather with per-study percentages and
   dominance classes (`primary_dominant` / `metastatic_dominant` / `mixed`).
3. **Diagnostic interpretation** — a one-shot stratified-rate comparison against the
   Zehir et al. [@Zehir2017] published numbers, with per-comparison verdicts and an aggregate
   closure-state.

Out of scope for t052:

- Rewriting the pooled-ratio surface to emit `pooled_ratio_primary` /
  `pooled_ratio_metastatic` columns. Gated on a `descriptor validated` aggregate
  closure-state.
- EGFR T790M validation (requires lung-cancer study ingestion + hotspot-aware
  mutation filtering — both absent from current configs). The diagnostic output
  schema reserves columns for hotspot-level work but does not exercise them.
- GENIE-based validation (GENIE is not in any current pipeline result on disk).
- Per-study cohort-stage descriptor in any cross-project knowledge graph.
- Treatment-status ingestion from patient-level (rather than sample-level) clinical
  tables.

## Architecture (Approach 1: per-study rule with summary rollup)

The annotation runs per-study and is rolled up at summary time, mirroring the existing
pipeline pattern (`annotate_drivers`, `annotate_ch`, `annotate_hypermutators`). The
diagnostic report is a standalone opt-in script, mirroring `compute_sbs1_lrr_bias_per_study.py`
from t126.

### Prerequisite ingestion step

Before the diagnostic can run, `prad_tcga_pan_can_atlas_2018` must exist as an
ingested study. The ingestion piggybacks on the existing `convert_to_feather.py`
pipeline rule:

1. Add `prad_tcga_pan_can_atlas_2018` to a new minimal config:
   `code/config/config-t052-validation.yml` (mirrors `config-poc.yml` but with the
   AR/ESR1 validation study list).
2. Run `convert_to_feather` for the new study only. This populates
   `results/<run-name>/studies/prad_tcga_pan_can_atlas_2018/` with `samples.feather`
   and `mut.feather`.
3. The diagnostic then operates against `results/poc-2026-04-17/` (existing) +
   `results/<t052-validation-run>/studies/prad_tcga_pan_can_atlas_2018/` (new).

Total expected runtime for the prerequisite: < 10 minutes (single study download +
convert, no annotation chain).

### File layout

| Path | Purpose |
|---|---|
| `data/cbioportal_study_cohort_profiles.tsv` | Hand-curated registry: per-study rows + family-pattern rows |
| `data/cohort_stage_validation_comparisons.tsv` | Comparison manifest for the diagnostic (one row per focal gene/cancer/cohort tuple) |
| `code/config/config-t052-validation.yml` | Minimal config for the prerequisite `prad_tcga` ingestion |
| `code/scripts/annotate_cohort_stage.py` | Per-study annotation |
| `code/scripts/build_study_cohort_composition.py` | Summary-level rollup |
| `code/scripts/compare_stage_stratified_gene_rates.py` | Diagnostic: AR/ESR1 per-stage rate table (standalone, opt-in) |
| `code/scripts/tests/test_annotate_cohort_stage.py` | Classification rules + precedence + value normalization |
| `code/scripts/tests/test_build_study_cohort_composition.py` | Rollup math |
| `code/scripts/tests/test_compare_stage_stratified_gene_rates.py` | Diagnostic stratification + verdict logic |
| `doc/interpretations/2026-04-25-t052-stage-stratified-ar-esr1.md` | AR/ESR1 closure note |

### Pipeline outputs

| Path | Content |
|---|---|
| `studies/<id>/metadata/samples_stage_annotated.feather` | Per-sample flags + per-axis audit trail |
| `summary/metadata/study_cohort_composition.feather` | Per-study percentages + dominance classes |
| `results/t052-stage-stratified-2026-04-25/summary/stage_stratified_gene_rates.feather` | Diagnostic output |

`samples_stage_annotated.feather` is consumed by `build_study_cohort_composition` and
joinable downstream by future stage-stratification rules.
`study_cohort_composition.feather` is **opt-in** — not in `rule all`. Consumers add it
explicitly to their config's `all` target list when they need it.

## Registry (`data/cbioportal_study_cohort_profiles.tsv`)

### Schema

| column | type | meaning |
|---|---|---|
| `pattern` | str | exact `study_id` OR glob pattern (e.g., `*_tcga_pan_can_atlas_*`) |
| `pattern_kind` | enum | `study_id` (exact match) or `glob` (fnmatch) |
| `default_is_metastatic` | enum str | `true` / `false` / `unknown` |
| `default_is_pre_treated` | enum str | `true` / `false` / `unknown` |
| `priority` | int | resolution rank when multiple patterns match (lower = wins) |
| `source` | str | one-sentence justification with citation. **Required**, validated non-empty. |
| `notes` | str | freeform |

### Storage convention

The TSV uses string enum values (`true` / `false` / `unknown`) for human readability.
The annotation script parses these into pandas nullable booleans (`True` / `False` /
`pd.NA`) for the output feather.

### Initial registry contents

| pattern | pattern_kind | default_is_metastatic | default_is_pre_treated | priority | source |
|---|---|---|---|---|---|
| `*_tcga_pan_can_atlas_*` | glob | false | false | 100 | TCGA accrual largely targets primary untreated specimens (Cancer Genome Atlas Research Network 2008); fallback default — sample-level metadata always wins |
| `tcga_mc3` | study_id | false | false | 50 | Ellrott et al. [@Ellrott2018] MC3 pseudo-study: TCGA matched-normal pan-cancer MAF, primary tumors |
| `msk_impact_*` | glob | unknown | unknown | 100 | MSK-IMPACT clinical sequencing: mixed primary/metastatic, sample-level fields override (Zehir et al. [@Zehir2017]) |
| `genie` | study_id | unknown | unknown | 100 | AACR GENIE: clinical sequencing, mixed; sample-level SAMPLE_TYPE drives override |
| `metastatic_solid_tumors_mich_2017` | study_id | true | unknown | 10 | MET500 cBioPortal study: all metastatic by design |
| `pog570_bcgsc_2020` | study_id | true | true | 10 | BCGSC POG-570: metastatic, post-treatment by design |

**Caveat noted in the source for the TCGA family glob**: SKCM in the TCGA pan-can-atlas
family contains a substantial metastatic fraction. The glob default is intended as a
**fallback only** — sample-level `sample_type` metadata, when present and non-empty,
always overrides this default per the resolution order below.

### Resolution order (per axis, applied independently)

1. **Sample-level metadata extraction** (highest precedence) — when `sample_type` /
   `sample_class` / `sample_type_detailed` carry a recognized value for the axis
   (after value normalization). For the metastatic axis only: a non-empty
   `METASTATIC_SITE` value that is **not** in the sentinel set forces
   `is_metastatic=True`.
2. **Registry row matching `study_id` exactly** with the lowest `priority` value.
3. **Registry row matching `glob` pattern** with the lowest `priority` value.
4. **Fallback `unknown`** (`pd.NA` in the output).

The two axes are resolved by the same step independently — one axis can resolve
via sample metadata while the other falls through to the registry.

### Registry validation (fail-loud at load time)

The annotation script validates the registry on load and raises `ValueError` for any of:

- `default_is_metastatic` or `default_is_pre_treated` not in `{true, false, unknown}`.
- `pattern_kind` not in `{study_id, glob}`.
- Duplicate `(pattern, pattern_kind)` rows.
- Two registry rows with the same `priority` matching the same study via the same
  `pattern_kind` (ambiguous resolution; require explicit priority differentiation).
- Empty or missing `source`.

## Sample-level metadata classification rules

### Source fields consulted (per axis, in priority order)

For `is_metastatic` (using actual `samples.feather` column names):

1. `sample_type` (most reliable when present)
2. `sample_class`
3. `sample_type_detailed` (renamed from raw `SAMPLE_TYPE_DETAILED` in `convert_to_feather`)
4. `METASTATIC_SITE` — passthrough column, **only** when its value is non-empty AND not
   in the sentinel set (see below)

For `is_pre_treated`:

1. `sample_type_detailed` (sometimes carries explicit "Post-treatment" markers)
2. `SPECIMEN_TYPE` — passthrough column, rare but occasionally informative
3. — most cBioPortal studies do not carry per-sample treatment status; falls through
   to the registry default

### METASTATIC_SITE sentinel handling

Empirically observed in `msk_impact_2017`:

```
Not Applicable    6130
Liver             1083
Lymph Node         907
...
```

Treating non-empty as metastatic would falsely flag 6,130 samples. Sentinel set
(matched after value normalization, see below):

```python
METASTATIC_SITE_SENTINELS = {
    "",
    "not applicable",
    "not available",
    "na",
    "n/a",
    "unknown",
    "none",
}
```

A METASTATIC_SITE value that is non-empty AND, after normalization, not in this set
forces `is_metastatic=True` even when `sample_type` is missing.

### Value normalization

Applied to BOTH the sample-metadata value AND the keys in the value-mapping tables before
lookup:

```python
def _normalize(value: str) -> str:
    return (
        value.strip()
        .casefold()
        .replace("-", " ")
        .replace("_", " ")
    )
    # collapse multiple spaces:
    # while "  " in s: s = s.replace("  ", " ")
```

This makes `"Treatment-naive"`, `"Treatment Naive"`, `"treatment_naive"`, and
`"  TREATMENT  NAIVE  "` resolve identically.

### Value mappings (post-normalization keys)

```python
METASTATIC_VALUE_MAP = {
    # -> True (is_metastatic)
    "metastasis": True,
    "metastatic": True,
    "recurrence": True,
    "local recurrence": True,
    "distant metastasis": True,
    # -> False
    "primary": False,
    "primary tumor": False,
    "primary solid tumor": False,
}

PRE_TREATED_VALUE_MAP = {
    # -> True
    "post treatment": True,    # normalized "Post-treatment"
    "pretreated": True,
    "treated": True,
    # -> False
    "pre treatment": False,    # normalized "Pre-treatment"
    "treatment naive": False,  # normalized "Treatment-naive" / "Treatment Naive"
    "naive": False,
}
```

Unknown values fall through cleanly.

## Output schemas

### `studies/<id>/metadata/samples_stage_annotated.feather`

| column | type | source | notes |
|---|---|---|---|
| (all existing `samples.feather` columns) | — | passthrough | preserves upstream schema |
| `is_metastatic` | nullable bool | derived | `True` / `False` / `pd.NA` |
| `is_pre_treated` | nullable bool | derived | `True` / `False` / `pd.NA` |
| `cohort_stage_metastatic_source` | category | derived | `sample_metadata:sample_type` / `sample_metadata:sample_class` / `sample_metadata:sample_type_detailed` / `sample_metadata:metastatic_site` / `registry_study` / `registry_glob` / `fallback_unknown` |
| `cohort_stage_treatment_source` | category | derived | parallel: `sample_metadata:sample_type_detailed` / `sample_metadata:specimen_type` / `registry_study` / `registry_glob` / `fallback_unknown` |

The `*_source` columns are the per-axis audit trail. Both columns combine the resolution
step AND the source field that resolved (if any) into a single category, so downstream
consumers can answer "which field said this sample was metastatic?" without rerunning
the rule.

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
| `dominant_site_class` | category | `primary_dominant` / `metastatic_dominant` / `mixed` / `unknown_dominant` (≥80% threshold) |
| `dominant_treatment_class` | category | parallel |

Empty-study edge case (`n_samples_total == 0`): all percentages are `0.0`,
`dominant_*_class = "unknown_dominant"`.

### `results/t052-stage-stratified-2026-04-25/summary/stage_stratified_gene_rates.feather`

One row per `(study_id, cancer_type, gene, target_variant, is_metastatic)` cell:

| column | type | meaning |
|---|---|---|
| `study_id` | str | |
| `cancer_type` | str | |
| `gene` | str | focal gene from comparison manifest |
| `target_variant` | str \| None | hgvsp_short hotspot label when comparison is hotspot-specific; `None` for gene-level |
| `is_metastatic` | nullable bool | stratification axis |
| `n_samples_in_stratum` | int | denominator (samples in cohort + cancer_type + stage) |
| `n_samples_panel_covers_gene` | int | denominator after panel-coverage check (≤ n_samples_in_stratum) |
| `n_mutated` | int | numerator (samples with ≥1 protein-altering mutation in gene; or matching `target_variant` when set) |
| `mutation_rate` | float | `n_mutated / n_samples_panel_covers_gene` |
| `expected_zehir2017` | float | published comparison value |
| `verdict` | category | `reproduces` / `partial` / `fails` / `underpowered` (per-comparison) |

Mutation filtering uses `variant_class ∈ PROTEIN_ALTERING_VARIANT_CLASSES` (imported
from `compute_per_sample_tmb.py`), matching existing TMB-numerator convention.

## Comparison manifest (`data/cohort_stage_validation_comparisons.tsv`)

The diagnostic does NOT hardcode study IDs, cancer types, or gene names. It loads them
from a small TSV manifest:

| column | type | meaning |
|---|---|---|
| `comparison_id` | str | short label (e.g., `ar_prostate_zehir2017`) |
| `gene` | str | HUGO symbol |
| `target_variant` | str | optional `hgvsp_short` for hotspot-level (e.g., `p.T790M`); empty = gene-level |
| `metastatic_study_id` | str | study contributing the metastatic stratum |
| `metastatic_cancer_type` | str | cancer_type filter on the metastatic side |
| `metastatic_expected_rate` | float | published rate, e.g., `0.18` |
| `primary_study_id` | str | study contributing the primary stratum |
| `primary_cancer_type` | str | cancer_type filter |
| `primary_expected_rate` | float | published rate, e.g., `0.01` |
| `expected_source` | str | citation (e.g., `Zehir2017_Fig5`) |
| `notes` | str | freeform |

### Initial manifest contents

| comparison_id | gene | target_variant | metastatic_study_id | metastatic_cancer_type | metastatic_expected_rate | primary_study_id | primary_cancer_type | primary_expected_rate | expected_source |
|---|---|---|---|---|---:|---|---|---:|---|
| ar_prostate_zehir2017 | AR | (empty) | msk_impact_2017 | Prostate Cancer | 0.18 | prad_tcga_pan_can_atlas_2018 | Prostate Adenocarcinoma | 0.01 | Zehir2017_Fig5 |
| esr1_breast_zehir2017 | ESR1 | (empty) | msk_impact_2017 | Breast Cancer | 0.11 | brca_tcga_pan_can_atlas_2018 | Breast Cancer | 0.04 | Zehir2017_Fig5 |

Adding the EGFR T790M comparison later: append a row with `target_variant=p.T790M` and
populate the appropriate study IDs once lung studies are ingested. No code change needed.

## Diagnostic report

### Source data

- `results/poc-2026-04-17/studies/msk_impact_2017/` (existing, contains all cancer types).
- `results/poc-2026-04-17/studies/brca_tcga_pan_can_atlas_2018/` (existing).
- `results/<t052-validation-run>/studies/prad_tcga_pan_can_atlas_2018/` (new, from
  the prerequisite ingestion).

### Workflow

1. Load `samples.feather` for each study referenced in the manifest.
2. Annotate stage in-memory by importing and calling functions from
   `annotate_cohort_stage.py` directly (no logic duplication). Inputs: the loaded
   samples + the registry.
3. For each comparison row in the manifest:
   a. Filter samples by `cancer_type`.
   b. Filter the metastatic-side cohort to `is_metastatic == True`.
      Filter the primary-side cohort to `is_metastatic == False`.
   c. **Panel coverage check** (panel cohorts only): for `msk_impact_2017`, intersect
      the panel BED for each sample's `panel_id` with the focal gene's coordinates
      from `data/grch37.tsv`. Samples whose panel does not cover the gene are
      excluded from the denominator. AR, ESR1, EGFR are all on MSK-IMPACT-341+, so
      the expectation is that all MSK samples pass this check; the rule asserts and
      logs the count for transparency.
   d. Count mutated samples: `variant_class ∈ PROTEIN_ALTERING_VARIANT_CLASSES`
      AND `symbol == gene`. If `target_variant` is set, additionally filter by
      `hgvsp_short == target_variant`.
   e. Compute `mutation_rate = n_mutated / n_samples_panel_covers_gene`.
   f. Apply per-comparison verdict (next section).
4. Emit one feather row per (comparison, stratum). Two strata per comparison:
   `is_metastatic=True` and `is_metastatic=False`.
5. Write the markdown closure note.

### Pre-registered verdict thresholds

The verdict is **per focal comparison**. Each comparison independently lands in one of
four states:

| Outcome | Definition | What it means |
|---|---|---|
| **reproduces** | Both metastatic and primary observed rates fall within ±3 percentage points of the published numbers | The descriptor mechanism works as intended for this gene |
| **partial** | Direction matches (`metastatic_rate > primary_rate`) but at least one observed rate differs from published by >3 pp | Descriptor captures real bias; a confound (cancer-type-detailed mismatch, mutation-call differences, panel version) is shifting absolute numbers |
| **fails** | Direction does not match (`metastatic_rate ≤ primary_rate`) | Indicates a problem with the classification rules for this gene/cancer pair |
| **underpowered** | Either stratum has `n_samples_panel_covers_gene < 20` | Reported but not interpreted; CI too wide to discriminate the other three outcomes |

The interpretation document reports both per-gene verdicts and an aggregate
**closure-state**:

| Closure-state | Definition | Action |
|---|---|---|
| **descriptor validated** | At least 1 of 2 comparisons `reproduces` or `partial`, and 0 land `fails`. Underpowered comparisons don't count against | Descriptor ready for downstream pooled-ratio rewrites in a follow-up task |
| **descriptor needs investigation** | Any comparison lands `fails` | Descriptor lands but does not validate against published numbers; investigate before stratifying pooled outputs |
| **insufficient evidence** | Both comparisons land `underpowered` | Descriptor lands but the diagnostic could not exercise it on this study list; rerun on a larger ingestion before drawing conclusions |

The shift from "2 of 3" (v1) to "1 of 2" (v2) reflects the dropped EGFR comparison.
With only two comparisons, requiring both to validate is too brittle (a single
SKCM-style edge case in the registry would tank closure); requiring at least one
keeps the bar reasonable and lets the diagnostic note any single-gene partial result
explicitly.

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
one-shot CLI invocation against the existing artifact + the prerequisite `prad_tcga`
ingestion run.

`build_study_cohort_composition` output is **opt-in** — not in `rule all`. Consumers add
it to their config's `all` target list when they need it (matches the t126 pattern).

## Testing

For `annotate_cohort_stage.py` (12 tests):

1. Sample-level metadata wins over registry when both apply (precedence).
2. Registry `study_id` row wins over `glob` row when both match.
3. Glob pattern with leading wildcard matches correctly.
4. Non-empty METASTATIC_SITE forces `is_metastatic=True` when value is **not** a
   sentinel (e.g., `"Liver"`).
5. METASTATIC_SITE sentinel values (`"Not Applicable"`, `""`, `"NA"`) do **not**
   force True — they fall through.
6. Each axis resolves independently (one axis can land `True`, the other `pd.NA`).
7. `cohort_stage_metastatic_source` and `cohort_stage_treatment_source` record the
   resolution path correctly per axis.
8. Unknown sample-metadata values (e.g., `"FFPE"`) fall through cleanly to registry.
9. Value normalization: `"Treatment-naive"`, `"treatment_naive"`, and
   `"  TREATMENT  NAIVE  "` all resolve to `is_pre_treated=False`.
10. Registry validation: invalid enum value raises `ValueError`.
11. Registry validation: duplicate `(pattern, pattern_kind)` raises `ValueError`.
12. Registry validation: missing/empty `source` raises `ValueError`.

For `build_study_cohort_composition.py` (3 tests):

1. Percentages sum to 1.0 within each axis when `n_samples_total > 0`.
2. `dominant_*_class` correctly assigns at the ≥80% threshold (test all four classes:
   primary_dominant, metastatic_dominant, mixed, unknown_dominant).
3. Empty-study edge case: explicit row, all percentages 0.0,
   `dominant_*_class = "unknown_dominant"`.

For `compare_stage_stratified_gene_rates.py` (5 tests):

1. Filtering by `is_metastatic` matches expected sample counts on a toy fixture.
2. Verdict `reproduces`: rates within ±3 pp of published.
3. Verdict `partial`: direction correct, magnitude off by >3 pp.
4. Verdict `fails`: direction wrong (metastatic ≤ primary).
5. Verdict `underpowered`: stratum n < 20, flagged and excluded from closure-state.

**Total**: 20 tests across 3 modules. Lint/format pass required before commit.

## Validation gate

Before claiming closure:

- All 20 tests pass.
- `uv run --frozen ruff check code/` passes for new files.
- `uv run --frozen ruff format --check code/` passes for new files.
- Snakemake `--lint` does not regress.
- Prerequisite `prad_tcga_pan_can_atlas_2018` ingestion completes successfully.
- Diagnostic produces both per-comparison verdicts and an aggregate closure-state in
  `doc/interpretations/2026-04-25-t052-stage-stratified-ar-esr1.md` with explicit
  numbers.

## Out of scope (potential follow-up tasks)

- Rewriting `gene_cancer_study_ratio_annotated.feather` to emit per-stage stratified
  ratio columns. Gated on a `descriptor validated` aggregate closure-state.
- EGFR T790M validation: requires lung-cancer study ingestion (e.g., `luad_tcga_pan_can_atlas_2018`)
  + GENIE access for the metastatic side. The diagnostic schema reserves the
  `target_variant` column for this future work.
- GENIE-based validation more broadly: requires GENIE-as-pseudo-study ingestion
  (planned but not currently in any config).
- Promoting treatment-status from cBioPortal patient-level clinical tables. Most
  studies don't carry it at sample level; patient-level promotion is its own
  ingestion challenge.
- Per-(study, cancer_type) composition rollup (current rollup is per-study only).
  Useful when a single cohort spans multiple cancer types with different stage
  compositions (msk_impact_2017 is the obvious case).
