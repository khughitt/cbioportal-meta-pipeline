# t077 GLMM-Logit Pooled Gene x Cancer Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement the pre-registered GLMM-logit random-effects meta-analysis pipeline for per-(gene, cancer) mutation rates and emit a consumer-facing pooled output with heterogeneity diagnostics.

**Architecture:** Build a long-format pooled-input table directly from the per-study `gene_cancer_study.feather` artifacts so zero-count cells retain their true denominators. Fit the confirmatory model in an isolated R environment via `metafor::rma.glmm`, emit a pooled feather plus diagnostics, then join the pooled metrics back into the annotated cross-study output surface.

**Tech Stack:** Python, pandas, Snakemake, R (`metafor`, `arrow`, `optparse`), pytest

---

### Task 1: Build the pooled-input adapter table

**Files:**
- Create: `code/scripts/build_pooled_gene_cancer_input.py`
- Modify: `code/workflows/Snakefile`
- Test: `code/scripts/tests/test_build_pooled_gene_cancer_input.py`

**Scope:**
- Read per-study `studies/{id}/mut/table/gene_cancer_study.feather`
- Emit one long row per `(study_id, cancer_type, symbol)` with:
  - `y_inclusive`, `y_exclusive`
  - `n_inclusive`, `n_exclusive`
  - `k_studies`-relevant identifiers
  - study-level covariates derived from config/runtime (`panel_class`, `matched_normal`)
- Treat the post-`t076` per-study tables as the source of truth for zero-event denominators

### Task 2: Add the isolated R meta-analysis environment and runner skeleton

**Files:**
- Create: `code/envs/r-meta.yml`
- Create: `code/scripts/run_gene_cancer_meta_analysis.R`
- Test: `code/scripts/tests/test_run_gene_cancer_meta_analysis_cli.py`

**Scope:**
- Define the Snakemake env for R meta-analysis
- Add an R CLI entrypoint that reads the pooled-input feather and writes a schema-valid output feather
- Keep the first green pass to argument parsing + round-trip output schema only

### Task 3: Implement the confirmatory GLMM fit and fallback status logic

**Files:**
- Modify: `code/scripts/run_gene_cancer_meta_analysis.R`
- Test: `code/scripts/tests/test_run_gene_cancer_meta_analysis_cli.py`

**Scope:**
- Filter cells per the pre-registration thresholds
- Fit `metafor::rma.glmm(measure = "PLO", ...)`
- Emit:
  - `pooled_logit`, `pooled_rate`
  - `pooled_ci_lo`, `pooled_ci_hi`
  - `tau2`, `i2`
  - `pi_lo`, `pi_hi`
  - `k_studies`, `n_total`, `y_total`
  - `converged`, `status`
- Implement the pre-registered REML-logit escape hatch for non-converged cells

### Task 4: Add sensitivity and diagnostic outputs

**Files:**
- Modify: `code/scripts/run_gene_cancer_meta_analysis.R`
- Modify: `code/workflows/Snakefile`
- Test: `code/scripts/tests/test_run_gene_cancer_meta_analysis_cli.py`

**Scope:**
- Emit a diagnostics feather for convergence/fallback reasons
- Add leave-one-out or hold-out-ready output tables required by the pre-registration
- Ensure high-I2 / skipped-cell cases are explicit in schema, not implicit `NaN`s

### Task 5: Wire the Snakemake rule and consumer-facing join

**Files:**
- Modify: `code/workflows/Snakefile`
- Modify: `code/scripts/annotate.py` or a new dedicated join script if clearer
- Test: `code/scripts/tests/test_gene_cancer_meta_join.py`

**Scope:**
- Add the workflow rule(s) that build the long input and run the R model
- Write `summary/mut/table/gene_cancer_pooled.feather`
- Join pooled metrics onto the canonical annotated output surface without mutating existing per-study semantics

### Task 6: Documentation and verification pass

**Files:**
- Modify: `doc/meta/pre-registration-t077-glmm-logit-pooling.md` only if deviations are required
- Modify: `AGENTS.md` only if canonical-output guidance changes
- Add/modify task notes on completion

**Scope:**
- Verify the implementation matches the pre-registration
- If any confirmatory-path deviation is necessary, document it before reporting results
- Run targeted tests, lint, and at least one workflow-level sanity check on `config-poc.yml`
