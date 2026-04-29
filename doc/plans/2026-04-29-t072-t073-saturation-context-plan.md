# t072/t073 Saturation Context Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add explicit study-contribution and per-cancer saturation context columns to the
canonical gene-cancer wide outputs.

**Architecture:** Keep the change inside `create_combined_gene_cancer_freq_table.py`, where the
per-study wide table already has the denominator frames needed for per-cancer cohort size.
Use an explicit Lawrence 2014 reference table keyed by cancer labels, and mark unsupported cancer
labels as `no_lawrence_reference` rather than applying an implicit fallback.

**Tech Stack:** Python, pandas, Snakemake, pytest, pyarrow/feather.

---

### Task 1: Add Contribution Alias

**Files:**
- Modify: `code/scripts/create_combined_gene_cancer_freq_table.py`
- Test: `code/scripts/tests/test_create_combined_gene_cancer_freq_table.py`

- [x] Write a failing test asserting `_annotate_callability()` emits `n_studies_contributing`
  equal to the existing non-null inclusive per-study count.
- [x] Run the targeted pytest test and verify it fails on the missing column.
- [x] Add `n_studies_contributing` beside `n_contributing_studies` for both count and ratio
  outputs.
- [x] Re-run the targeted pytest test and verify it passes.

### Task 2: Add Lawrence 2014 Saturation Context

**Files:**
- Modify: `code/scripts/create_combined_gene_cancer_freq_table.py`
- Test: `code/scripts/tests/test_create_combined_gene_cancer_freq_table.py`

- [x] Write a failing test asserting `_annotate_callability()` emits `cancer_saturation_status`,
  `lawrence2014_required_n`, `n_total_samples_in_cancer_inclusive`, and
  `lawrence2014_saturation_fraction` from per-cancer cohort denominators.
- [x] Include one supported cancer above threshold, one supported cancer below threshold, and one
  unsupported cancer, expecting `saturated`, `undersampled`, and `no_lawrence_reference`.
- [x] Run the targeted pytest test and verify it fails on the missing columns.
- [x] Add helper functions for the explicit Lawrence reference mapping and status assignment.
- [x] Re-run targeted pytest and existing script tests.

### Task 3: Documentation And Verification

**Files:**
- Modify: `doc/guides/canonical-outputs.md`
- Optional modify: `tasks/active.md`, `tasks/done/2026-04.md`

- [x] Update the canonical output guide to list the new columns and describe
  `no_lawrence_reference`.
- [x] Run `uv run --frozen pytest code/scripts/tests/test_create_combined_gene_cancer_freq_table.py`.
- [x] Run `uv run --frozen ruff check code/scripts/create_combined_gene_cancer_freq_table.py
  code/scripts/tests/test_create_combined_gene_cancer_freq_table.py`.
