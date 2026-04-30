# t173 dNdScv LOSO Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the tooling needed to run and interpret leave-one-study-out dNdScv ranking stability, with a pilot run path before the full expensive fan-out.

**Architecture:** Keep canonical dNdScv outputs untouched. A manifest builder emits one command per holdout run, each targeting a separate output directory; a comparison script reads completed holdout `dndscv_pooled.feather` files and writes overlap/recovery summaries. This separates cheap protocol validation from the compute-heavy dNdScv reruns.

**Tech Stack:** Python, pandas, click, PyYAML, pytest, Snakemake 9, uv.

---

### Task 1: dNdScv LOSO Comparison

**Files:**
- Create: `code/scripts/tests/test_analyze_dndscv_loso.py`
- Create: `code/scripts/analyze_dndscv_loso.py`

- [x] **Step 1: Write failing tests for ranking and overlap metrics**

Create tests that assert:
- `rank_dndscv_genes()` sorts by `min_qglobal` ascending and `n_cancers_significant_q05` descending.
- `compare_loso_rankings()` reports Jaccard/recovery against the base top-K.
- Bailey and CGC reference recovery are computed from the annotated overlay.

- [x] **Step 2: Run tests to verify they fail**

Run:

```bash
PYTHONPATH=code/scripts uv run --frozen pytest code/scripts/tests/test_analyze_dndscv_loso.py -q
```

Expected: import failure because `analyze_dndscv_loso.py` does not exist yet.

- [x] **Step 3: Implement minimal comparison code**

Implement a focused script with pure functions for:
- ranking a dNdScv pooled table;
- extracting Bailey/CGC reference sets from `gene_cancer_study_ratio_annotated_dndscv.feather`;
- comparing base vs one or more LOO pooled tables at K values 10, 25, 50, and 100;
- writing `dndscv_loso_topk_overlap.feather` and `dndscv_loso_summary.feather`.

- [x] **Step 4: Run tests to verify they pass**

Run:

```bash
PYTHONPATH=code/scripts uv run --frozen pytest code/scripts/tests/test_analyze_dndscv_loso.py -q
```

Expected: all tests pass.

### Task 2: dNdScv LOSO Run Manifest

**Files:**
- Create: `code/scripts/tests/test_build_dndscv_loso_manifest.py`
- Create: `code/scripts/build_dndscv_loso_manifest.py`

- [x] **Step 1: Write failing tests for manifest rows and commands**

Create tests that assert:
- each row excludes exactly one requested study;
- pilot mode emits only the requested holdout;
- output directories are separate from the canonical pan-cancer dNdScv directory;
- generated commands contain `uv run --frozen snakemake`, the base config, the isolated `out_dir`, and JSON-encoded included studies.

- [x] **Step 2: Run tests to verify they fail**

Run:

```bash
PYTHONPATH=code/scripts uv run --frozen pytest code/scripts/tests/test_build_dndscv_loso_manifest.py -q
```

Expected: import failure because `build_dndscv_loso_manifest.py` does not exist yet.

- [x] **Step 3: Implement minimal manifest builder**

Implement:
- YAML config loading for the base study list;
- `build_loso_manifest()` returning a pandas DataFrame;
- a click CLI writing `dndscv_loso_run_manifest.tsv`.

- [x] **Step 4: Run tests to verify they pass**

Run:

```bash
PYTHONPATH=code/scripts uv run --frozen pytest code/scripts/tests/test_build_dndscv_loso_manifest.py -q
```

Expected: all tests pass.

### Task 3: Protocol Validation

**Files:**
- Create: `doc/interpretations/2026-04-29-t173-dndscv-loso-protocol.md`

- [x] **Step 1: Generate a pilot manifest excluding `genie`**

Run:

```bash
uv run --frozen python code/scripts/build_dndscv_loso_manifest.py \
  --config code/config/config-pan-cancer-dndscv.yml \
  --out-root /data/packages/cbioportal/pan-cancer-dndscv-loso \
  --pilot-study genie \
  --manifest-out /data/packages/cbioportal/pan-cancer/summary/dndscv_loso/dndscv_loso_run_manifest.tsv
```

- [x] **Step 2: Validate the pilot command with Snakemake dry-run**

Run the manifest command with `-n` inserted before `aggregate_dndscv_per_gene`.

Expected: Snakemake resolves the isolated holdout DAG needed for
`summary/mut/table/dndscv_pooled.feather` without modifying canonical dNdScv outputs.

- [x] **Step 3: Document the protocol status**

Write a short interpretation/protocol note stating that t173 is not scientifically closed until the pilot and full holdout dNdScv runs complete.

### Task 4: Final Verification

Run:

```bash
PYTHONPATH=code/scripts uv run --frozen pytest \
  code/scripts/tests/test_analyze_dndscv_loso.py \
  code/scripts/tests/test_build_dndscv_loso_manifest.py -q
uv run --frozen ruff check code/scripts/analyze_dndscv_loso.py code/scripts/build_dndscv_loso_manifest.py \
  code/scripts/tests/test_analyze_dndscv_loso.py code/scripts/tests/test_build_dndscv_loso_manifest.py
uv run --frozen ruff format --check code/scripts/analyze_dndscv_loso.py code/scripts/build_dndscv_loso_manifest.py \
  code/scripts/tests/test_analyze_dndscv_loso.py code/scripts/tests/test_build_dndscv_loso_manifest.py
uv run --frozen pyright code/scripts/analyze_dndscv_loso.py code/scripts/build_dndscv_loso_manifest.py
```

Expected: all checks pass.
