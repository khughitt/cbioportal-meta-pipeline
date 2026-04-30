# t173 GENIE dNdScv Influence Attribution Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Identify which GENIE cancer/build groups and gene-level dNdScv signals drive the
`exclude_genie` top-100 re-ranking seen in t173.

**Architecture:** Do a cheap attribution analysis from existing full-cohort and LOSO dNdScv
artifacts before considering any new Snakemake reruns. The analysis should produce ranked
gene-level and cancer/build-level attribution tables, then an interpretation note that states
which mechanism is most consistent with the evidence.

**Tech Stack:** Python, pandas, click, pytest, pyarrow/feather, uv.

---

## Context and Motivation

t173 was opened because t149 showed very low leave-one-study-out stability for the pooled-rate
ranking, but pooled-rate is a point estimate without explicit selection-test significance or
sample-size weighting. The dNdScv LOSO test was the decisive ranking-stability check.

The first dNdScv pilot excluded GENIE and failed the pre-specified fan-out gate:

- `exclude_genie`: Jaccard@100 = 0.429.

Two broad non-GENIE contrasts preserved the top-100 ranking:

- `exclude_msk_met_2021`: Jaccard@100 = 0.852.
- `exclude_pog570_bcgsc_2020`: Jaccard@100 = 0.923.

This pattern makes generic single-study sensitivity unlikely. The higher-value next step is to
explain the GENIE-specific mechanism: whether GENIE changes the ranking through a small number
of cancer/build groups, through broad sample-size dominance across many labels, through
panel-vs-WES ascertainment, or through label granularity / cancer-mix effects.

This plan should not be treated as a full P2 closure. It is a mechanism-finding analysis that
uses the completed dNdScv runs to decide what to inspect or rerun next.

## Data to Use

### Ranking and overlap inputs

- Canonical full-cohort pooled dNdScv ranking:
  `/data/packages/cbioportal/pan-cancer/summary/mut/table/dndscv_pooled.feather`
- Completed LOSO pooled rankings:
  - `/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_genie/summary/mut/table/dndscv_pooled.feather`
  - `/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_msk_met_2021/summary/mut/table/dndscv_pooled.feather`
  - `/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_pog570_bcgsc_2020/summary/mut/table/dndscv_pooled.feather`
- Existing LOSO summaries:
  - `/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/dndscv_loso_topk_overlap.feather`
  - `/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/dndscv_loso_summary.feather`

Relevant pooled columns:

- `symbol`
- `min_qglobal`
- `n_cancers_significant_q05`
- `n_cancers_significant_q01`
- `n_cancers_tested`
- `best_cancer_type`

### Per-cancer dNdScv evidence

Use the reconciled per-cancer outputs first:

- Full cohort:
  `/data/packages/cbioportal/pan-cancer/summary/mut/dndscv/per_cancer/*/genes.feather`
- Exclude-GENIE:
  `/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_genie/summary/mut/dndscv/per_cancer/*/genes.feather`
- Negative-control contrasts, if needed for calibration:
  - `/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_msk_met_2021/summary/mut/dndscv/per_cancer/*/genes.feather`
  - `/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_pog570_bcgsc_2020/summary/mut/dndscv/per_cancer/*/genes.feather`

Relevant reconciled per-cancer columns:

- `symbol`
- `cancer_type`
- `dndscv_qglobal_cv`
- `dndscv_significant_q05`
- `dndscv_input_status`
- `dndscv_input_modality`
- `dndscv_panel_only`
- `dndscv_n_samples`
- `dndscv_n_variants`
- `dndscv_split_build`
- `dndscv_refdb`

### Cancer/build metadata and build-level evidence

Use build-level files to distinguish label effects from build effects:

- Full cohort:
  `/data/packages/cbioportal/pan-cancer/summary/mut/dndscv/per_cancer_per_build/*/genes.feather`
  `/data/packages/cbioportal/pan-cancer/summary/mut/dndscv_input/*/cohort_meta.feather`
- Exclude-GENIE:
  `/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_genie/summary/mut/dndscv/per_cancer_per_build/*/genes.feather`
  `/data/packages/cbioportal/pan-cancer-dndscv-loso/exclude_genie/summary/mut/dndscv_input/*/cohort_meta.feather`

Relevant build-level columns:

- dNdScv result: `gene_name`, `qallsubs_cv`, `qmis_cv`, `qtrunc_cv`, `n_syn`, `n_mis`,
  `n_non`, `n_spl`, `wmis_cv`, `wnon_cv`, `wspl_cv`
- cohort metadata: `cancer_type`, `build`, `slug`, `n_samples`, `n_variants`, `modality`,
  `panel_only`, `below_threshold`, `min_samples_threshold`, `min_variants_threshold`

### Optional external overlays

Use only for interpretability, not for the primary attribution score:

- Annotated dNdScv overlay:
  `/data/packages/cbioportal/pan-cancer/summary/mut/table/gene_cancer_study_ratio_annotated_dndscv.feather`
- Bailey/CGC recovery is pre-t174 and affected by CDKN2A isoform symbols, so it should not be a
  gate for this analysis.

## Research Questions

1. **Which genes drive the `exclude_genie` top-100 instability?**
   - Which base top-100 genes are lost when GENIE is excluded?
   - Which genes are gained?
   - Which genes have the largest rank deltas among the top 150 or top 200?

2. **Which cancer labels support the lost and gained genes?**
   - For each affected gene, which full-cohort cancer labels have `dndscv_significant_q05=True`?
   - Which of those labels disappear, become below-threshold, or lose significance after GENIE is
     excluded?
   - Which labels become more influential in `exclude_genie`?

3. **Is the mechanism label presence or quantitative signal shift?**
   - `genie_only_label`: a cancer/build stratum is present or above-threshold in the full cohort
     but absent or below-threshold in `exclude_genie`.
   - `shared_label_shift`: the cancer/build stratum exists in both runs, but q-value or
     significance status changes enough to alter rank.
   - `mixed`: both mechanisms apply for the same gene or cancer label.
   - `weak_or_unclear`: affected genes are present, but no threshold transition occurs and the
     absolute q-evidence shift is below the configured threshold.

4. **Which cancer/build groups contribute most to rank disruption?**
   - Rank cancer/build groups by the number of affected genes they explain.
   - Rank them by summed absolute rank delta among affected genes.
   - Track whether the same groups explain lost genes, gained genes, or both.

5. **Do broad non-GENIE contrasts show the same attribution pattern?**
   - Use `exclude_msk_met_2021` and `exclude_pog570_bcgsc_2020` as negative controls.
   - A GENIE-specific driver should be much stronger in the full-vs-exclude-GENIE comparison than
     in the full-vs-broad-non-GENIE comparisons.

## What This Analysis Can Support

This analysis can support:

- A mechanistic interpretation of why GENIE is uniquely disruptive in t173.
- A ranked list of GENIE-associated cancer/build strata that should be inspected first.
- A decision about whether the next compute step should be:
  - targeted GENIE cancer/build reruns,
  - label-collapsing / cancer-type canonicalization checks,
  - panel-vs-WES ascertainment analysis,
  - or no further dNdScv rerun until t174 is resolved.
- A stronger P2 statement that GENIE disruption is structured rather than generic single-study
  sensitivity, if the attribution is concentrated and biologically/plausibly assay-linked.

This analysis cannot, by itself, prove:

- that GENIE is "wrong";
- that the full-cohort ranking should exclude GENIE;
- that all specialty studies are disruptive;
- that the effect is independent of panel design, cancer-label granularity, or sample-count
  imbalance.

## Proposed Outputs

Write outputs under:

`/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/genie_influence/`

Expected tables:

- `genie_gene_rank_delta.feather`
  - one row per gene in the union of base top 200 and `exclude_genie` top 200
  - columns: `symbol`, base rank, holdout rank, rank delta, base/holdout `min_qglobal`,
    base/holdout `n_cancers_significant_q05`, base/holdout `best_cancer_type`,
    top-100 status class (`lost`, `gained`, `stable`, `outside_top100`)
- `genie_gene_cancer_evidence.feather`
  - one row per affected gene × cancer label × comparison
  - columns: q-values, significance flags, input status, modality, sample/variant counts,
    support class
- `genie_cancer_build_influence.feather`
  - one row per cancer/build stratum
  - columns: affected gene counts, lost/gained support counts, summed rank delta, sample and
    variant deltas, modality, panel-only flag, mechanism class
- `negative_control_cancer_build_influence_<contrast>.feather`
  - one slim cancer/build influence table per `--negative-control` contrast
  - same rank/evidence/influence score columns needed for calibration, but scoped to the
    negative-control contrast rather than the full GENIE gene-evidence table
- `genie_influence_summary.json`
  - compact summary for docs and future automation
  - required top-level keys:
    - `parameters`: `holdout`, `negative_controls`, `top_k`, `diagnostic_top_n`, `q_floor`,
      `q_shift_threshold`, `q_floor_sensitivity`, `q_shift_threshold_sensitivity`
    - `loaded_counts`: per contrast counts for pooled rows, per-cancer rows, cohort-meta rows,
      cancer labels, build strata, and genes in the diagnostic union
    - `topk_gene_counts`: per contrast counts for `lost`, `gained`, `stable`, and
      `outside_top100`
    - `top_cancer_build_attributions`: top rows from `genie_cancer_build_influence.feather`
      with cancer type, build, mechanism class, affected-gene counts, summed rank delta,
      sample/variant deltas, and threshold transition counts
    - `negative_control_comparison`: per negative control, the maximum and median influence
      scores, overlap with top GENIE-attributed cancer/build groups, and top affected
      cancer/build groups
    - `sensitivity`: summary blocks for q-floor and q-shift-threshold sweeps
- Interpretation note:
  `doc/interpretations/2026-04-30-t173-genie-dndscv-influence.md`

## Analysis Design

### Gene rank delta

Compute ranks using the same t173 key as `analyze_dndscv_loso.py`:

1. `min_qglobal` ascending.
2. `n_cancers_significant_q05` descending.

Do not add an additional `symbol` tie-break in this script unless `analyze_dndscv_loso.py` is
changed in the same implementation. The published t173 numbers used
`rank_dndscv_genes()`, whose stable pandas sort preserves input feather-row order for ties. The
new script should import or mirror that helper exactly and test for exact rank parity.

Primary affected gene sets:

- `lost_top100`: base top 100 minus `exclude_genie` top 100.
- `gained_top100`: `exclude_genie` top 100 minus base top 100.
- `stable_top100`: intersection of base and `exclude_genie` top 100.

Secondary scope for diagnostics:

- union of base top 200 and `exclude_genie` top 200.

### Per-cancer support attribution

For each affected gene, compare full vs `exclude_genie` per-cancer rows by `symbol` and
`cancer_type`.

Classify each gene × cancer label:

- `lost_significance`: significant in full, not significant in `exclude_genie`.
- `gained_significance`: not significant in full, significant in `exclude_genie`.
- `stable_significant`: significant in both.
- `stable_not_significant`: not significant in either.
- `full_only_tested`: full has tested row, `exclude_genie` is missing or below-threshold.
- `holdout_only_tested`: `exclude_genie` has tested row, full is missing or below-threshold.

For q-value deltas, avoid ratios when either value is zero. Use:

- `neg_log10_q = -log10(max(q, 1e-300))`
- `delta_neg_log10_q = holdout_neg_log10_q - base_neg_log10_q`

The `1e-300` floor is arbitrary but explicit. It prevents infinite values while preserving the
ordering of extremely significant genes. Sensitivity checks should repeat summaries with
`1e-100` and with a binary significance-only score, and the CLI should write those sensitivity
summaries into `genie_influence_summary.json`.

### Cancer/build influence scoring

Use both cancer-level and build-level evidence.

Cancer-level score:

- `n_lost_top100_supported_full`: count of lost genes significant in full for this cancer label.
- `n_lost_top100_lost_significance`: count of lost genes significant in full and not significant
  after GENIE exclusion.
- `n_gained_top100_supported_holdout`: count of gained genes significant after GENIE exclusion.
- `sum_abs_rank_delta_supported`: sum of absolute rank deltas for affected genes supported by
  the cancer label.
- `median_delta_neg_log10_q`: median q-value evidence shift among affected genes.

Build-level score:

- same counts as cancer-level where build-level gene rows exist;
- `delta_n_samples = full_n_samples - exclude_genie_n_samples`;
- `delta_n_variants = full_n_variants - exclude_genie_n_variants`;
- `full_modality`, `holdout_modality`, `full_panel_only`, `holdout_panel_only`;
- `threshold_transition`: `tested_to_below_threshold`, `below_threshold_to_tested`,
  `tested_to_tested`, or `missing`.

Positive `delta_n_samples` and `delta_n_variants` mean the holdout removed samples or variants
from that cancer/build stratum. For the primary contrast, positive values therefore mean GENIE
contributed samples or variants to the full-cohort stratum.

Build identity must come from `cohort_meta.feather` columns (`cancer_type`, `build`, `slug`), not
from parsing `per_cancer_per_build` directory names. Current slugs look like
`acute_myeloid_leukemia__hg19`, but slug parsing should not be part of the analysis contract.

Assert threshold parity between full and holdout cohort metadata before assigning threshold
transitions:

- `min_samples_threshold` must match.
- `min_variants_threshold` must match.
- If either differs, fail early with the affected cancer/build stratum and both threshold values.

Mechanism label:

- `genie_only_label`: threshold transition or missingness explains the support loss.
- `shared_label_shift`: both runs are tested, but significance or `delta_neg_log10_q` changes.
- `mixed`: both are present across affected genes in the same cancer/build group.
- `weak_or_unclear`: affected genes are present, both runs are tested where rows exist, no
  threshold transition is observed, and `abs(delta_neg_log10_q) < q_shift_threshold` for the
  supported affected genes.

Use an explicit status constant in code:

- tested statuses: `tested_significant`, `tested_not_significant`
- non-tested statuses: `below_threshold`, `failed_qc`, `not_run`
- missing join rows should be represented internally as `missing`, not silently converted to a
  tested or below-threshold status

Initial default threshold for a meaningful q-value evidence shift:

- `abs(delta_neg_log10_q) >= 2`, equivalent to at least a 100-fold q-value change after flooring.

This threshold is a heuristic, not a biological boundary. It must be reported and sensitivity
checked at `>= 1` and `>= 3`.

### Negative-control calibration

Repeat the same attribution summaries for:

- full vs `exclude_msk_met_2021`
- full vs `exclude_pog570_bcgsc_2020`

Do not require every table to be as detailed as the GENIE table. The key calibration output is
whether the top GENIE-attributed cancer/build groups also appear as top drivers in the broad
non-GENIE contrasts. If they do, the interpretation should soften from GENIE-specific to general
sample-mix sensitivity for those labels.

For each negative control, write:

- `negative_control_cancer_build_influence_<contrast>.feather`
- a `negative_control_comparison[<contrast>]` block in `genie_influence_summary.json`

The comparison block must include:

- `jaccard_at_top_k`
- `lost_topk_count`, `gained_topk_count`, `stable_topk_count`
- top cancer/build rows by `sum_abs_rank_delta_supported`
- overlap count with the top GENIE cancer/build rows
- maximum and median `sum_abs_rank_delta_supported`

## QA and Hidden Assumption Checks

1. **Ranking reproducibility**
   - Verify rank order exactly matches `analyze_dndscv_loso.py` for base and `exclude_genie`.
   - Add a test fixture where tied `min_qglobal` values are ordered by
     `n_cancers_significant_q05`, and ties on both ranking keys preserve input row order.
   - If a symbol tie-break is later added, update `analyze_dndscv_loso.py`,
     `analyze_genie_dndscv_influence.py`, and both ranking tests in the same change.

2. **Zero q-values**
   - Many dNdScv q-values are `0.0` after numerical underflow.
   - Never divide q-values directly.
   - Use floored `-log10(q)` and report the floor.
   - Sensitivity check q-floor choices.

3. **CDKN2A isoform issue**
   - t174 remains unresolved.
   - Do not use Bailey/CGC recovery as a primary attribution score.
   - Preserve symbols exactly in the primary tables.
   - If a display table groups dot-suffixed symbols by prefix, label it as display-only.

4. **Cancer-label granularity**
   - GENIE may introduce or amplify more granular cancer labels.
   - Attribution should distinguish exact-label effects from possible synonym/canonicalization
     issues.
   - Labels with high influence should be checked against sample counts and known alias maps
     before interpreting them biologically.

5. **Build and modality confounding**
   - Build-level summaries must include `build`, `modality`, and `panel_only`.
   - If a top influence group is panel-only or mixed, interpret it as assay/callability-linked
     until checked.

6. **Sample-count dominance**
   - Large `delta_n_samples` or `delta_n_variants` can explain stronger evidence without a
     distinct biology signal.
   - Report sample and variant deltas next to each influence score.

7. **Threshold artifacts**
   - `below_threshold` changes can create apparent support loss.
   - Report threshold transitions separately from q-value shifts among tested cohorts.
   - Assert `min_samples_threshold` and `min_variants_threshold` parity before interpreting a
     tested/below-threshold transition.

8. **Negative-control sanity**
   - The top GENIE influence groups should not be equally prominent in `exclude_msk_met_2021`
     and `exclude_pog570_bcgsc_2020`.
   - If they are, the conclusion becomes "broad sample-mix sensitive" rather than
     "GENIE-specific."

9. **Parameter choices**
   - Primary K: 100, because t173 gate is Jaccard@100.
   - Secondary K: 10, 25, 50 for continuity with t173.
   - Diagnostic gene scope: top 200 union. Sensitivity check top 150 and top 300.
   - q-value evidence threshold: `abs(delta_neg_log10_q) >= 2`. Sensitivity check 1 and 3.
   - q-floor: primary `1e-300`. Sensitivity check `1e-100` and binary significance-only.

10. **Output integrity**
    - Fail early if expected full or `exclude_genie` per-cancer files are missing.
    - Fail early if required columns are absent.
    - Report the number of cancer labels and genes loaded per run.
    - Confirm output row counts are nonzero before writing interpretation claims.

## Implementation Tasks

### Task 1: Define Fixtures and Ranking Delta Tests

**Files:**

- Create: `code/scripts/tests/test_analyze_genie_dndscv_influence.py`
- Create: `code/scripts/analyze_genie_dndscv_influence.py`

- [ ] **Step 1: Write ranking delta tests**

Test these behaviors:

- rank sorting matches t173 exactly: `min_qglobal` ascending,
  `n_cancers_significant_q05` descending, and stable input order for remaining ties;
- `rank_pooled_dndscv()` matches `analyze_dndscv_loso.rank_dndscv_genes()` for a fixture with
  tied ranking keys;
- top-100 classes are assigned as `lost`, `gained`, `stable`, and `outside_top100`;
- rank deltas are computed as `holdout_rank - base_rank`, with missing ranks represented as
  null in output and handled in classification.

- [ ] **Step 2: Run the failing tests**

```bash
PYTHONPATH=code/scripts uv run --frozen pytest code/scripts/tests/test_analyze_genie_dndscv_influence.py -q
```

Expected: import failure because `analyze_genie_dndscv_influence.py` does not exist yet.

- [ ] **Step 3: Implement ranking delta helpers**

Implement focused pure functions:

- `rank_pooled_dndscv()`
- `build_gene_rank_delta()`
- `classify_topk_status()`

- [ ] **Step 4: Run tests**

```bash
PYTHONPATH=code/scripts uv run --frozen pytest code/scripts/tests/test_analyze_genie_dndscv_influence.py -q
```

Expected: ranking tests pass.

### Task 2: Per-Cancer Evidence Loader and Support Classes

**Files:**

- Modify: `code/scripts/analyze_genie_dndscv_influence.py`
- Modify: `code/scripts/tests/test_analyze_genie_dndscv_influence.py`

- [ ] **Step 1: Write evidence-classification tests**

Test these cases with tiny in-memory tables:

- significant in full but not holdout -> `lost_significance`;
- not significant in full but significant in holdout -> `gained_significance`;
- significant in both -> `stable_significant`;
- missing holdout row -> `full_only_tested`;
- tested statuses are defined by a module constant containing `tested_significant` and
  `tested_not_significant`;
- q-value zero is transformed using a floor and does not produce infinity.

- [ ] **Step 2: Run tests to verify failure**

```bash
PYTHONPATH=code/scripts uv run --frozen pytest \
  code/scripts/tests/test_analyze_genie_dndscv_influence.py -q
```

Expected: evidence helper functions are missing.

- [ ] **Step 3: Implement evidence loading and classification**

Implement:

- `load_per_cancer_genes(root: Path) -> pandas.DataFrame`
- `compare_gene_cancer_evidence(base: DataFrame, holdout: DataFrame, affected: DataFrame)`
- `neg_log10_q(q: Series, floor: float = 1e-300)`

Fail early if required columns are missing.

- [ ] **Step 4: Run tests**

```bash
PYTHONPATH=code/scripts uv run --frozen pytest \
  code/scripts/tests/test_analyze_genie_dndscv_influence.py -q
```

Expected: evidence tests pass.

### Task 3: Cancer/Build Influence Scoring

**Files:**

- Modify: `code/scripts/analyze_genie_dndscv_influence.py`
- Modify: `code/scripts/tests/test_analyze_genie_dndscv_influence.py`

- [ ] **Step 1: Write influence-score tests**

Test that a small gene-cancer evidence table produces:

- affected-gene counts per cancer/build group;
- separate lost and gained counts;
- summed absolute rank delta;
- mechanism labels `genie_only_label`, `shared_label_shift`, `mixed`, and `weak_or_unclear`.
- positive `delta_n_samples` and `delta_n_variants` when the full cohort has more samples or
  variants than the holdout;
- a failure when full and holdout `min_samples_threshold` or `min_variants_threshold` differ.

- [ ] **Step 2: Run tests to verify failure**

```bash
PYTHONPATH=code/scripts uv run --frozen pytest \
  code/scripts/tests/test_analyze_genie_dndscv_influence.py -q
```

Expected: influence scoring functions are missing.

- [ ] **Step 3: Implement influence scoring**

Implement:

- `load_cohort_meta(root: Path) -> pandas.DataFrame`
- `score_cancer_build_influence(evidence: DataFrame, cohort_meta: DataFrame)`
- `assign_mechanism_class(...)`

Keep the primary score transparent; do not fit a model for this first pass.
Read build identity from `cohort_meta.feather`; do not parse build names out of directory slugs
except as a last-resort integrity check against the metadata `slug` column.

- [ ] **Step 4: Run tests**

```bash
PYTHONPATH=code/scripts uv run --frozen pytest \
  code/scripts/tests/test_analyze_genie_dndscv_influence.py -q
```

Expected: influence scoring tests pass.

### Task 4: CLI and Outputs

**Files:**

- Modify: `code/scripts/analyze_genie_dndscv_influence.py`
- Modify: `code/scripts/tests/test_analyze_genie_dndscv_influence.py`

- [ ] **Step 1: Write CLI smoke test**

Create a temporary fixture tree with minimal pooled, per-cancer, and cohort-meta feathers. Assert
that the CLI writes:

- `genie_gene_rank_delta.feather`
- `genie_gene_cancer_evidence.feather`
- `genie_cancer_build_influence.feather`
- `negative_control_cancer_build_influence_exclude_msk_met_2021.feather`
- `genie_influence_summary.json`

Assert that `genie_influence_summary.json` contains `parameters`, `loaded_counts`,
`topk_gene_counts`, `top_cancer_build_attributions`, `negative_control_comparison`, and
`sensitivity`.

- [ ] **Step 2: Run smoke test to verify failure**

```bash
PYTHONPATH=code/scripts uv run --frozen pytest \
  code/scripts/tests/test_analyze_genie_dndscv_influence.py -q
```

Expected: CLI entrypoint is missing.

- [ ] **Step 3: Implement click CLI**

Arguments:

- `--base-root /data/packages/cbioportal/pan-cancer`
- `--loo-root /data/packages/cbioportal/pan-cancer-dndscv-loso`
- `--holdout exclude_genie`
- `--negative-control exclude_msk_met_2021`
- `--negative-control exclude_pog570_bcgsc_2020`
- `--out-dir /data/packages/cbioportal/pan-cancer/summary/dndscv_loso/genie_influence`
- `--top-k 100`
- `--diagnostic-top-n 200`
- `--q-floor 1e-300`
- `--q-shift-threshold 2.0`
- `--q-floor-sensitivity 1e-100`
- `--q-shift-threshold-sensitivity 1.0`
- `--q-shift-threshold-sensitivity 3.0`

- [ ] **Step 4: Run tests**

```bash
PYTHONPATH=code/scripts uv run --frozen pytest \
  code/scripts/tests/test_analyze_genie_dndscv_influence.py -q
```

Expected: all tests pass.

### Task 5: Run Real Analysis and Document Interpretation

**Files:**

- Create: `doc/interpretations/2026-04-30-t173-genie-dndscv-influence.md`
- Modify: `tasks/active.md`

- [ ] **Step 1: Run real analysis**

```bash
uv run --frozen python code/scripts/analyze_genie_dndscv_influence.py \
  --base-root /data/packages/cbioportal/pan-cancer \
  --loo-root /data/packages/cbioportal/pan-cancer-dndscv-loso \
  --holdout exclude_genie \
  --negative-control exclude_msk_met_2021 \
  --negative-control exclude_pog570_bcgsc_2020 \
  --out-dir /data/packages/cbioportal/pan-cancer/summary/dndscv_loso/genie_influence \
  --top-k 100 \
  --diagnostic-top-n 200 \
  --q-floor 1e-300 \
  --q-shift-threshold 2.0 \
  --q-floor-sensitivity 1e-100 \
  --q-shift-threshold-sensitivity 1.0 \
  --q-shift-threshold-sensitivity 3.0
```

- [ ] **Step 2: Inspect outputs**

Check:

```bash
uv run --frozen python -c "from pathlib import Path; import pandas as pd; root=Path('/data/packages/cbioportal/pan-cancer/summary/dndscv_loso/genie_influence'); print(pd.read_feather(root/'genie_gene_rank_delta.feather').shape); print(pd.read_feather(root/'genie_gene_cancer_evidence.feather').shape); print(pd.read_feather(root/'genie_cancer_build_influence.feather').head(20).to_string(index=False))"
```

Expected:

- GENIE primary tables are non-empty;
- one negative-control influence table exists for each requested negative control;
- top influence rows have interpretable cancer/build labels;
- summary JSON records loaded row counts and parameter choices.
- summary JSON records sensitivity summaries and one comparison block for each negative control.

- [ ] **Step 3: Write interpretation**

The interpretation must answer:

- Which genes drive the `exclude_genie` top-100 loss/gain?
- Which cancer/build groups explain the largest share of rank movement?
- Is the dominant mechanism `genie_only_label`, `shared_label_shift`, `mixed`, or
  `weak_or_unclear`?
- Do the MSK and POG negative controls show the same pattern?
- What targeted rerun or label audit, if any, is justified next?

- [ ] **Step 4: Update t173 task note**

Add the influence-plan and interpretation links to `tasks/active.md` under t173.

### Task 6: Verification

Run:

```bash
PYTHONPATH=code/scripts uv run --frozen pytest \
  code/scripts/tests/test_analyze_genie_dndscv_influence.py \
  code/scripts/tests/test_analyze_dndscv_loso.py \
  code/scripts/tests/test_build_dndscv_loso_manifest.py -q
uv run --frozen ruff check \
  code/scripts/analyze_genie_dndscv_influence.py \
  code/scripts/analyze_dndscv_loso.py \
  code/scripts/build_dndscv_loso_manifest.py \
  code/scripts/tests/test_analyze_genie_dndscv_influence.py \
  code/scripts/tests/test_analyze_dndscv_loso.py \
  code/scripts/tests/test_build_dndscv_loso_manifest.py
uv run --frozen ruff format --check \
  code/scripts/analyze_genie_dndscv_influence.py \
  code/scripts/analyze_dndscv_loso.py \
  code/scripts/build_dndscv_loso_manifest.py \
  code/scripts/tests/test_analyze_genie_dndscv_influence.py \
  code/scripts/tests/test_analyze_dndscv_loso.py \
  code/scripts/tests/test_build_dndscv_loso_manifest.py
uv run --frozen pyright \
  code/scripts/analyze_genie_dndscv_influence.py \
  code/scripts/analyze_dndscv_loso.py \
  code/scripts/build_dndscv_loso_manifest.py \
  code/scripts/tests/test_analyze_genie_dndscv_influence.py
```

Expected: all tests and checks pass.
