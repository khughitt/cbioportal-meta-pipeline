# t076 NaN-vs-0 Handling Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Distinguish "gene callable but unmutated" from "gene not callable or cancer absent from study" in the combined `gene_cancer_study` outputs.

**Architecture:** Reuse per-study `cancer_study.feather` inputs in the combined gene-cancer aggregation step. In the combined pivot, fill missing per-study `(cancer, gene)` cells with zero only when the cancer exists in that study cohort and the gene is callable for that study; leave all other missing cells as `NaN`.

**Tech Stack:** Python, pandas, Snakemake, pytest

---

### Task 1: Add the failing combined-step regression tests

**Files:**
- Modify: `code/scripts/tests/test_create_combined_gene_cancer_freq_table.py`
- Test: `code/scripts/tests/test_create_combined_gene_cancer_freq_table.py`

**Step 1: Write the failing test**

Add regression coverage for:
- callable + cancer-present + unmutated => fill per-study `num_*` and `ratio_*` with `0`
- cancer-absent => keep per-study cells as `NaN`
- gene-not-callable => keep per-study cells as `NaN`

**Step 2: Run test to verify it fails**

Run: `uv run --frozen pytest code/scripts/tests/test_create_combined_gene_cancer_freq_table.py -q`

Expected: FAIL because the combined step currently leaves callable-and-present missing cells as `NaN`.

### Task 2: Implement the minimal combined-step fix

**Files:**
- Modify: `code/scripts/create_combined_gene_cancer_freq_table.py`
- Modify: `code/workflows/Snakefile`

**Step 1: Thread per-study cancer-table inputs into the combined rule**

Update `rule create_combined_gene_cancer_freq_table` to pass per-study `cancer_study.feather` paths alongside the existing per-study `gene_cancer_study.feather` inputs.

**Step 2: Write minimal implementation**

In `create_combined_gene_cancer_freq_table.py`:
- load per-study cancer tables into a cancer-presence map
- build a study/gene callable mask from `panel_coverage` + `study_panel_map`
- fill missing combined per-study cells with zero only where both masks are true
- leave true missing cells as `NaN`

**Step 3: Run tests to verify they pass**

Run: `uv run --frozen pytest code/scripts/tests/test_create_combined_gene_cancer_freq_table.py -q`

Expected: PASS

### Task 3: Regression verification

**Files:**
- Test: `code/scripts/tests/test_create_freq_tables.py`
- Test: `code/scripts/tests/test_create_combined_gene_cancer_freq_table.py`

**Step 1: Run targeted regression suite**

Run: `uv run --frozen pytest code/scripts/tests/test_create_freq_tables.py code/scripts/tests/test_create_combined_gene_cancer_freq_table.py -q`

Expected: PASS

**Step 2: Run lint if code changed materially**

Run: `uv run --frozen ruff check code/scripts/create_combined_gene_cancer_freq_table.py code/scripts/tests/test_create_combined_gene_cancer_freq_table.py`

Expected: PASS

### Task 4: Commit

**Files:**
- Modify: `doc/plans/2026-04-22-t076-nan-vs-0-implementation-plan.md`
- Modify: implementation/test files above

**Step 1: Commit**

```bash
git add code/workflows/Snakefile code/scripts/create_combined_gene_cancer_freq_table.py code/scripts/tests/test_create_combined_gene_cancer_freq_table.py doc/plans/2026-04-22-t076-nan-vs-0-implementation-plan.md
git commit -m "fix: close t076 NaN-vs-0 handling"
```
