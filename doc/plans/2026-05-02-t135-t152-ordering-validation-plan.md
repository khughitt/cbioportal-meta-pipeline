# t135/t152 cBioPortal Ordering Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the cBioPortal ordering guardrail into validated, method-qualified trajectory evidence by implementing observation-event MHN inputs, callability masks, hypermutator stratification, and PCAWG/Vocht calibration for `task:t135` and `task:t152`.

**Architecture:** Build a small, testable analysis layer rather than changing the production frequency pipeline first. The layer should consume existing cBioPortal/GENIE mutation, sample, callability, hypermutator, and Sanchez-Vega pathway outputs; emit deterministic MHN-ready matrices; run synthetic calibration and the Vocht LUAD replication; then run a narrow per-histology pathway-level ordering pass only if calibration gates pass.

**Tech Stack:** Python, pandas/polars, numpy, scipy, pyarrow feather/parquet, pytest, `mhn` or a pinned local wrapper for Vocht/Schill observation-event MHN, existing `uv` project environment, existing `science-tool` graph commands.

---

## Scope And Evidence Gate

This plan does not run the ordering analysis yet. It defines the implementation path and the gates required before cBioPortal exports trajectory claims to meta:

- Cross-sectional ordering remains tier 3 inferred ordering until benchmarked against PCAWG or Vocht-style calibration.
- Results are per histology, never pan-cancer pooled.
- Pathway-level MHN is primary; gene-level ordering is a drill-down.
- Uncalled genes are missing by design, not wild type.
- Hypermutator, MSI/POLE/POLD1, clonal hematopoiesis, normal-contamination, and panel-composition flags are modeled or stratified before biological interpretation.

## Files

- Create: `code/scripts/build_mhn_ordering_inputs.py`
- Create: `code/scripts/run_mhn_simulation_calibration.py`
- Create: `code/scripts/run_mhn_histology_ordering.py`
- Create: `code/scripts/tests/test_build_mhn_ordering_inputs.py`
- Create: `code/scripts/tests/test_run_mhn_simulation_calibration.py`
- Create: `doc/interpretations/YYYY-MM-DD-mhn-luad-demo-and-simulation-calibration.md`
- Create: `doc/interpretations/YYYY-MM-DD-mhn-ordering-validation.md`
- Modify: `tasks/active.md`
- Modify after successful execution: `doc/reports/synthesis/h04-mhn-pathway-ordering.md`

## Task 1: Freeze Method Contract And Input Schema

**Files:**
- Create: `code/scripts/tests/test_build_mhn_ordering_inputs.py`
- Create: `code/scripts/build_mhn_ordering_inputs.py`

- [ ] **Step 1: Write the failing schema test**

```python
import pandas as pd

from build_mhn_ordering_inputs import build_binary_event_matrix


def test_build_binary_event_matrix_marks_uncalled_events_missing() -> None:
    mutations = pd.DataFrame(
        [
            {"sample_id": "s1", "event_id": "RTK_RAS"},
            {"sample_id": "s2", "event_id": "TP53_CELL_CYCLE"},
        ]
    )
    callability = pd.DataFrame(
        [
            {"sample_id": "s1", "event_id": "RTK_RAS", "is_callable": True},
            {"sample_id": "s1", "event_id": "TP53_CELL_CYCLE", "is_callable": False},
            {"sample_id": "s2", "event_id": "RTK_RAS", "is_callable": True},
            {"sample_id": "s2", "event_id": "TP53_CELL_CYCLE", "is_callable": True},
        ]
    )

    matrix, mask = build_binary_event_matrix(mutations, callability)

    assert matrix.loc["s1", "RTK_RAS"] == 1
    assert matrix.loc["s1", "TP53_CELL_CYCLE"] == 0
    assert mask.loc["s1", "TP53_CELL_CYCLE"] is False
    assert matrix.loc["s2", "RTK_RAS"] == 0
    assert mask.loc["s2", "RTK_RAS"] is True
```

- [ ] **Step 2: Verify RED**

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_build_mhn_ordering_inputs.py::test_build_binary_event_matrix_marks_uncalled_events_missing -q
```

Expected: import failure for `build_mhn_ordering_inputs`.

- [ ] **Step 3: Implement the input builder**

Create `build_binary_event_matrix(mutations, callability)` with explicit sample/event sorting. Return two `DataFrame`s with identical indexes and columns: `matrix` as 0/1 observed event state, `mask` as boolean callability. Missing callability rows are an error, not a silent false.

- [ ] **Step 4: Verify GREEN**

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_build_mhn_ordering_inputs.py -q
```

Expected: the schema test passes.

## Task 2: Add Histology, Hypermutator, And Pathway Inputs

**Files:**
- Modify: `code/scripts/tests/test_build_mhn_ordering_inputs.py`
- Modify: `code/scripts/build_mhn_ordering_inputs.py`

- [ ] **Step 1: Write the failing cohort-stratification test**

```python
from build_mhn_ordering_inputs import select_ordering_cohort


def test_select_ordering_cohort_filters_histology_and_returns_hypermutator_strata() -> None:
    samples = pd.DataFrame(
        [
            {"sample_id": "s1", "cancer_type": "Lung Adenocarcinoma", "is_hypermutator": False},
            {"sample_id": "s2", "cancer_type": "Lung Adenocarcinoma", "is_hypermutator": True},
            {"sample_id": "s3", "cancer_type": "Breast Cancer", "is_hypermutator": False},
        ]
    )

    cohort = select_ordering_cohort(samples, cancer_type="Lung Adenocarcinoma")

    assert list(cohort["sample_id"]) == ["s1", "s2"]
    assert cohort["analysis_stratum"].tolist() == ["non_hypermutator", "hypermutator"]
```

- [ ] **Step 2: Verify RED**

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_build_mhn_ordering_inputs.py::test_select_ordering_cohort_filters_histology_and_returns_hypermutator_strata -q
```

Expected: import failure for `select_ordering_cohort`.

- [ ] **Step 3: Implement cohort selection**

Implement `select_ordering_cohort(samples, cancer_type)` with deterministic row order and `analysis_stratum` values `non_hypermutator` or `hypermutator`. Use existing `is_hypermutator`, `is_hypermutator_absolute`, `is_hypermutator_relative`, `hypermutator_reason`, MSI, POLE, and POLD1 columns when present; fail early if the primary `is_hypermutator` column is absent.

- [ ] **Step 4: Add pathway aggregation**

Add `map_gene_events_to_sanchez_vega_pathways(mutations, pathway_map)` so pathway-level events are primary. Multiple genes in the same pathway collapse to one event per sample. Gene-level outputs are emitted separately only for drill-down.

- [ ] **Step 5: Verify input contract**

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_build_mhn_ordering_inputs.py -q
```

Expected: all input-builder tests pass.

## Task 3: Build Synthetic Calibration Harness

**Files:**
- Create: `code/scripts/tests/test_run_mhn_simulation_calibration.py`
- Create: `code/scripts/run_mhn_simulation_calibration.py`

- [ ] **Step 1: Write the failing recovery-metric test**

```python
from run_mhn_simulation_calibration import summarize_edge_recovery


def test_summarize_edge_recovery_counts_directional_matches() -> None:
    truth = {("MMR", "RTK_RAS"), ("RTK_RAS", "TP53_CELL_CYCLE")}
    inferred = {("MMR", "RTK_RAS"), ("TP53_CELL_CYCLE", "RTK_RAS")}

    summary = summarize_edge_recovery(truth, inferred)

    assert summary["true_edges"] == 2
    assert summary["directional_matches"] == 1
    assert summary["reversed_edges"] == 1
    assert summary["directional_recall"] == 0.5
```

- [ ] **Step 2: Verify RED**

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_run_mhn_simulation_calibration.py::test_summarize_edge_recovery_counts_directional_matches -q
```

Expected: import failure for `run_mhn_simulation_calibration`.

- [ ] **Step 3: Implement recovery metrics**

Implement `summarize_edge_recovery(truth, inferred)` and persist calibration summaries with `directional_recall`, `reversed_edge_rate`, `false_discovery_rate`, and bootstrap support.

- [ ] **Step 4: Implement simulation runner wrapper**

Add a CLI that can simulate pathway events under a known ordering, apply synthetic callability masks, fit observation-event MHN and cMHN baselines, and write `results/mhn/calibration/<run_id>/edge_recovery.tsv`.

- [ ] **Step 5: Verify calibration unit tests**

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_run_mhn_simulation_calibration.py -q
```

Expected: recovery-metric tests pass.

## Task 4: Replicate Vocht 2026 GENIE LUAD Demo

**Files:**
- Modify: `code/scripts/run_mhn_histology_ordering.py`
- Create: `doc/interpretations/YYYY-MM-DD-mhn-luad-demo-and-simulation-calibration.md`

- [ ] **Step 1: Add a dry-run CLI test**

Add a test that calls the CLI with `--dry-run --cancer-type "Lung Adenocarcinoma"` and asserts that output paths and required input files are resolved without fitting a model.

- [ ] **Step 2: Verify RED**

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_run_mhn_simulation_calibration.py code/scripts/tests/test_build_mhn_ordering_inputs.py -q
```

Expected: dry-run test fails until the CLI exists.

- [ ] **Step 3: Implement LUAD runner**

Use the existing GENIE/cBioPortal processed outputs. Fit LUAD pathway-level observation-event MHN in three strata: all callable samples, non-hypermutators only, and hypermutators only if sample count is adequate. Emit cMHN as a comparator, not as the exportable result.

- [ ] **Step 4: Benchmark against Vocht and PCAWG**

Compare LUAD edges against the Vocht 2026 demonstration and PCAWG chronology where overlap exists. A successful local demo requires stable direction for at least the top expected LUAD ordering relationships under bootstrap and leave-one-study-out sensitivity.

- [ ] **Step 5: Write interpretation**

Create `doc/interpretations/YYYY-MM-DD-mhn-luad-demo-and-simulation-calibration.md` with sections: data version, sample counts, callability missingness, hypermutator counts, observation-event versus cMHN differences, Vocht agreement, PCAWG agreement, failure modes, and promotion decision.

## Task 5: Run Narrow Per-Histology Ordering Only If Gates Pass

**Files:**
- Modify: `code/scripts/run_mhn_histology_ordering.py`
- Create: `doc/interpretations/YYYY-MM-DD-mhn-ordering-validation.md`

- [ ] **Step 1: Define eligible histologies**

Start with LUAD, colorectal cancer, breast cancer, and thyroid cancer only if each has sufficient callable sample count after per-event masking. Record excluded histologies and reasons.

- [ ] **Step 2: Fit primary pathway-level models**

For each eligible histology, fit observation-event MHN on Sanchez-Vega pathways. Bootstrap edges and run leave-one-study-out sensitivity. Do not fit pan-cancer pooled ordering.

- [ ] **Step 3: Run gene-level drill-downs**

Only for pathway edges passing stability gates, fit gene-level drill-downs for benchmark pairs such as APC/KRAS/TP53 in colorectal cancer, STK11/KEAP1 in LUAD, BRAF/TERT in thyroid cancer, and TP53/PIK3CA relationships in breast cancer.

- [ ] **Step 4: Write validation interpretation**

Create `doc/interpretations/YYYY-MM-DD-mhn-ordering-validation.md` with a table of each edge, evidence tier, layer, bootstrap support, leave-one-study-out support, callability caveat, hypermutator sensitivity, PCAWG/Vocht agreement, and export decision.

## Task 6: Update Tasks, Synthesis, And Graphs

**Files:**
- Modify: `tasks/active.md`
- Modify: `doc/reports/synthesis/h04-mhn-pathway-ordering.md`
- Modify: `knowledge/graph.trig`

- [ ] **Step 1: Update task statuses**

Mark `task:t152` done only if the LUAD demo plus simulation calibration has an explicit promotion decision. Mark `task:t135` done only if at least one local per-histology ordering run reaches a documented export decision.

- [ ] **Step 2: Update `hypothesis:0004` synthesis**

If calibration succeeds, promote `hypothesis:0004-mhn-pathway-ordering` only to "method-qualified inferred ordering" and state evidence tier 3 or tier 4 depending on benchmark agreement. If calibration fails, keep `hypothesis:0004-mhn-pathway-ordering` candidate and record the blocker.

- [ ] **Step 3: Build local graph**

Run:

```bash
uv run --project /home/keith/d/science/science-tool science-tool graph build
```

Expected: local cBioPortal graph materializes successfully.

- [ ] **Step 4: Refresh meta federation**

From `/mnt/ssd/Dropbox/cancer/meta`, run:

```bash
uv run --project /home/keith/d/science/science-tool science-tool graph build
uv run --project /home/keith/d/science/science-tool science-tool federation validate
uv run --project /home/keith/d/science/science-tool science-tool federation status
```

Expected: federation remains consistent and meta can cite only the calibrated export decisions.

## Promotion Criteria

- `task:t152` can close with either success or failure, but it must include the Vocht replication attempt, synthetic calibration, and a written decision.
- `task:t135` can export a trajectory claim only if observation-event MHN is fitted per histology with callability masks, hypermutator sensitivity, bootstrap stability, and benchmark comparison.
- Any result failing calibration remains a source-method guardrail, not biological chronology.
