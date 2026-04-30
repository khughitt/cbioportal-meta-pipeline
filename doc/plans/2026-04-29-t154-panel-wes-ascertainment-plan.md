# t154 Panel-vs-WES Ascertainment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Quantify whether panel-only, WES-only, and combined mutation rankings differ enough that downstream h03 literature-attention analyses must include assay stratum.

**Architecture:** Add one standalone, tested analysis script that consumes existing pan-cancer feathers rather than adding a Snakefile rule. The script builds stratum-specific rankings from `gene_cancer_pooled_input.feather`, compares top-K overlap and driver recovery, runs a lightweight PubTator/length/rate regression by stratum, and writes feather outputs plus a markdown interpretation.

**Tech Stack:** Python, pandas, scipy, statsmodels when available with a deterministic scipy fallback for regression slopes, pyarrow feather, click CLI, pytest.

---

### Task 1: Stratum Ranking Helpers

**Files:**
- Create: `code/scripts/tests/test_analyze_panel_wes_ascertainment.py`
- Create: `code/scripts/analyze_panel_wes_ascertainment.py`

- [ ] **Step 1: Write failing tests for assay-stratum labels and rankings**

```python
import pandas as pd

from analyze_panel_wes_ascertainment import build_gene_cancer_rankings, panel_class_to_assay_stratum


def test_panel_class_to_assay_stratum_collapses_panel_classes() -> None:
    assert panel_class_to_assay_stratum("WES") == "wes"
    assert panel_class_to_assay_stratum("MC3") == "wes"
    assert panel_class_to_assay_stratum("large_hybrid_capture") == "panel"
    assert panel_class_to_assay_stratum("small_amplicon") == "panel"


def test_build_gene_cancer_rankings_uses_callability_denominators() -> None:
    pooled_input = pd.DataFrame(
        [
            {"study_id": "wes1", "cancer_type": "A", "symbol": "TP53", "y_inclusive": 10, "n_inclusive": 100, "panel_class": "WES"},
            {"study_id": "wes2", "cancer_type": "A", "symbol": "KRAS", "y_inclusive": 20, "n_inclusive": 100, "panel_class": "WES"},
            {"study_id": "pan1", "cancer_type": "A", "symbol": "TP53", "y_inclusive": 8, "n_inclusive": 10, "panel_class": "large_hybrid_capture"},
            {"study_id": "pan1", "cancer_type": "A", "symbol": "KRAS", "y_inclusive": 1, "n_inclusive": 10, "panel_class": "large_hybrid_capture"},
        ]
    )
    annotated = pd.DataFrame(
        [
            {"cancer_type": "A", "symbol": "TP53", "bailey2018_driver": True, "cgc_tier_1": True},
            {"cancer_type": "A", "symbol": "KRAS", "bailey2018_driver": False, "cgc_tier_1": False},
        ]
    )

    rankings = build_gene_cancer_rankings(pooled_input, annotated, analysis_view="inclusive")

    wes_top = rankings[(rankings["assay_stratum"] == "wes") & (rankings["rank"] == 1)].iloc[0]
    panel_top = rankings[(rankings["assay_stratum"] == "panel") & (rankings["rank"] == 1)].iloc[0]
    combined_top = rankings[(rankings["assay_stratum"] == "combined") & (rankings["rank"] == 1)].iloc[0]

    assert wes_top["symbol"] == "KRAS"
    assert wes_top["rate"] == 0.20
    assert panel_top["symbol"] == "TP53"
    assert panel_top["rate"] == 0.80
    assert combined_top["symbol"] == "TP53"
    assert combined_top["n_total"] == 110
```

- [ ] **Step 2: Verify RED**

Run: `uv run --frozen pytest code/scripts/tests/test_analyze_panel_wes_ascertainment.py -q`

Expected: import failure because `analyze_panel_wes_ascertainment.py` does not exist.

- [ ] **Step 3: Implement the minimal helper API**

Create `panel_class_to_assay_stratum()` and `build_gene_cancer_rankings()` with explicit panel-class mapping and y/n aggregation.

- [ ] **Step 4: Verify GREEN**

Run: `uv run --frozen pytest code/scripts/tests/test_analyze_panel_wes_ascertainment.py -q`

Expected: tests pass.

### Task 2: Overlap And Driver-Recovery Summaries

**Files:**
- Modify: `code/scripts/tests/test_analyze_panel_wes_ascertainment.py`
- Modify: `code/scripts/analyze_panel_wes_ascertainment.py`

- [ ] **Step 1: Write failing tests for top-K comparison**

```python
from analyze_panel_wes_ascertainment import compare_topk_rankings


def test_compare_topk_rankings_reports_jaccard_and_driver_recovery() -> None:
    rankings = pd.DataFrame(
        [
            {"assay_stratum": "wes", "cancer_type": "A", "symbol": "TP53", "rank": 1, "bailey2018_driver": True, "cgc_tier_1": True},
            {"assay_stratum": "wes", "cancer_type": "A", "symbol": "KRAS", "rank": 2, "bailey2018_driver": False, "cgc_tier_1": False},
            {"assay_stratum": "panel", "cancer_type": "A", "symbol": "TP53", "rank": 1, "bailey2018_driver": True, "cgc_tier_1": True},
            {"assay_stratum": "panel", "cancer_type": "A", "symbol": "BRAF", "rank": 2, "bailey2018_driver": True, "cgc_tier_1": True},
        ]
    )

    summary = compare_topk_rankings(rankings, k_values=(2,))
    row = summary[(summary["left_stratum"] == "wes") & (summary["right_stratum"] == "panel")].iloc[0]

    assert row["intersection"] == 1
    assert row["jaccard"] == 1 / 3
    assert row["left_bailey_recovery"] == 0.5
    assert row["right_bailey_recovery"] == 1.0
```

- [ ] **Step 2: Verify RED**

Run: `uv run --frozen pytest code/scripts/tests/test_analyze_panel_wes_ascertainment.py::test_compare_topk_rankings_reports_jaccard_and_driver_recovery -q`

Expected: import failure for `compare_topk_rankings`.

- [ ] **Step 3: Implement comparison helpers**

Add top-K pair-set extraction, Jaccard, recovery, and per-topK Bailey/CGC fractions.

- [ ] **Step 4: Verify GREEN**

Run: `uv run --frozen pytest code/scripts/tests/test_analyze_panel_wes_ascertainment.py -q`

Expected: tests pass.

### Task 3: Literature-Attention Regression And CLI

**Files:**
- Modify: `code/scripts/tests/test_analyze_panel_wes_ascertainment.py`
- Modify: `code/scripts/analyze_panel_wes_ascertainment.py`

- [ ] **Step 1: Write failing test for stratum regression output**

```python
from analyze_panel_wes_ascertainment import build_attention_regression


def test_build_attention_regression_reports_slope_per_stratum() -> None:
    rankings = pd.DataFrame(
        [
            {"assay_stratum": "wes", "symbol": "A", "rate": 0.01},
            {"assay_stratum": "wes", "symbol": "B", "rate": 0.10},
            {"assay_stratum": "panel", "symbol": "A", "rate": 0.20},
            {"assay_stratum": "panel", "symbol": "B", "rate": 0.02},
        ]
    )
    gene_features = pd.DataFrame(
        [
            {"symbol": "A", "length": 100.0, "pubtator_mention_count": 9.0},
            {"symbol": "B", "length": 1000.0, "pubtator_mention_count": 99.0},
        ]
    )

    out = build_attention_regression(rankings, gene_features)

    assert set(out["assay_stratum"]) == {"wes", "panel"}
    assert {"beta_log_length", "beta_log_rate", "n_genes"}.issubset(out.columns)
```

- [ ] **Step 2: Verify RED**

Run: `uv run --frozen pytest code/scripts/tests/test_analyze_panel_wes_ascertainment.py::test_build_attention_regression_reports_slope_per_stratum -q`

Expected: import failure for `build_attention_regression`.

- [ ] **Step 3: Implement regression helper and CLI**

Add `build_attention_regression()` and a click CLI accepting:

```bash
uv run --frozen python code/scripts/analyze_panel_wes_ascertainment.py \
  --pooled-input /data/packages/cbioportal/pan-cancer/summary/mut/table/gene_cancer_pooled_input.feather \
  --annotated /data/packages/cbioportal/pan-cancer/summary/mut/table/gene_cancer_study_ratio_annotated.feather \
  --three-way /data/packages/cbioportal/pan-cancer/summary/mut/table/three_way_ranking_comparison.feather \
  --out-dir /data/packages/cbioportal/pan-cancer/summary/panel_wes_ascertainment
```

The CLI writes `stratum_gene_cancer_rankings.feather`, `topk_overlap.feather`, and `attention_regression.feather`.

- [ ] **Step 4: Verify GREEN**

Run: `uv run --frozen pytest code/scripts/tests/test_analyze_panel_wes_ascertainment.py -q`

Expected: tests pass.

### Task 4: Run Analysis And Write Interpretation

**Files:**
- Create: `doc/interpretations/2026-04-29-q016-panel-induced-ascertainment.md`
- Generated output: `/data/packages/cbioportal/pan-cancer/summary/panel_wes_ascertainment/*.feather`

- [ ] **Step 1: Run t154 script on canonical pan-cancer outputs**

Run the CLI from Task 3.

- [ ] **Step 2: Inspect outputs**

Use a short Python readback to report mixed cancer types, K=100 panel-vs-WES Jaccard, Bailey recovery, and regression slopes.

- [ ] **Step 3: Write interpretation**

Document method, findings, caveats, verdict, and recommendation on whether t129 must include assay stratum.

- [ ] **Step 4: Final verification**

Run:

```bash
uv run --frozen pytest code/scripts/tests/test_analyze_panel_wes_ascertainment.py -q
uv run --frozen ruff check code/scripts/analyze_panel_wes_ascertainment.py code/scripts/tests/test_analyze_panel_wes_ascertainment.py
uv run --frozen ruff format --check code/scripts/analyze_panel_wes_ascertainment.py code/scripts/tests/test_analyze_panel_wes_ascertainment.py
```

Expected: all pass.
