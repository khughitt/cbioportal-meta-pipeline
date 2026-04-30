# t163 RT-dNdScv Residual Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Test whether gene-level replication timing explains residual full-scale pan-cancer dNdScv signal, especially TTN's top-rank persistence.

**Architecture:** Add one standalone, tested analysis script over existing artifacts. The script joins post-fix dNdScv per-gene ranks to `data/gene_replication_timing.feather`, builds RT features, fits simple rank/signal regressions, bootstraps coefficients, computes RT-adjusted dNdScv ranks, and writes feather outputs plus an interpretation.

**Tech Stack:** Python, pandas, numpy, click, pyarrow feather, pytest, ruff, pyright.

---

### Task 1: Join And Signal Helpers

**Files:**
- Create: `code/scripts/tests/test_analyze_rt_dndscv_residual.py`
- Create: `code/scripts/analyze_rt_dndscv_residual.py`

- [ ] **Step 1: Write failing tests for RT join and q-value signal**

```python
import pandas as pd

from analyze_rt_dndscv_residual import build_rt_dndscv_table


def test_build_rt_dndscv_table_merges_rt_and_computes_signal() -> None:
    dndscv = pd.DataFrame(
        [
            {"symbol": "TTN", "min_qglobal": 0.0, "n_cancers_significant_q05": 48, "rank_dndscv": 4},
            {"symbol": "TP53", "min_qglobal": 1e-8, "n_cancers_significant_q05": 64, "rank_dndscv": 1},
        ]
    )
    rt = pd.DataFrame(
        [
            {"symbol": "TTN", "rt_constitutive_label": "CL", "rt_ce_fraction": 0.1, "rt_cl_fraction": 0.9},
            {"symbol": "TP53", "rt_constitutive_label": "CE", "rt_ce_fraction": 0.8, "rt_cl_fraction": 0.2},
        ]
    )

    out = build_rt_dndscv_table(dndscv, rt, q_floor=1e-300)

    by_symbol = out.set_index("symbol")
    assert by_symbol.loc["TTN", "dndscv_signal"] == 300.0
    assert by_symbol.loc["TTN", "rt_late_score"] == 0.8
    assert by_symbol.loc["TP53", "rt_late_score"] == -0.6000000000000001
```

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=code/scripts uv run --frozen pytest code/scripts/tests/test_analyze_rt_dndscv_residual.py -q`

Expected: import failure because `analyze_rt_dndscv_residual.py` does not exist.

- [ ] **Step 3: Implement minimal join helper**

Create `build_rt_dndscv_table()` and `dndscv_signal = -log10(max(min_qglobal, q_floor))`.

- [ ] **Step 4: Verify GREEN**

Run: `PYTHONPATH=code/scripts uv run --frozen pytest code/scripts/tests/test_analyze_rt_dndscv_residual.py -q`

Expected: tests pass.

### Task 2: Regression And Bootstrap

**Files:**
- Modify: `code/scripts/tests/test_analyze_rt_dndscv_residual.py`
- Modify: `code/scripts/analyze_rt_dndscv_residual.py`

- [ ] **Step 1: Write failing tests for coefficient and bootstrap output**

```python
from analyze_rt_dndscv_residual import bootstrap_rt_effect, fit_rt_model


def test_fit_rt_model_reports_late_score_coefficient() -> None:
    table = pd.DataFrame(
        {
            "symbol": ["A", "B", "C", "D"],
            "dndscv_signal": [1.0, 2.0, 3.0, 4.0],
            "rt_late_score": [0.0, 0.25, 0.5, 0.75],
            "log_length": [2.0, 2.0, 2.0, 2.0],
            "n_cancers_significant_q05": [1, 1, 1, 1],
        }
    )

    out = fit_rt_model(table)

    assert out["n_genes"] == 4
    assert out["beta_rt_late_score"] > 0


def test_bootstrap_rt_effect_is_deterministic() -> None:
    table = pd.DataFrame(
        {
            "symbol": ["A", "B", "C", "D"],
            "dndscv_signal": [1.0, 2.0, 3.0, 4.0],
            "rt_late_score": [0.0, 0.25, 0.5, 0.75],
            "log_length": [2.0, 2.0, 2.0, 2.0],
            "n_cancers_significant_q05": [1, 1, 1, 1],
        }
    )

    out = bootstrap_rt_effect(table, n_boot=25, seed=0)

    assert out["n_boot"] == 25
    assert out["beta_rt_late_score_ci_low"] <= out["beta_rt_late_score_ci_high"]
```

- [ ] **Step 2: Verify RED**

Run each new test by name and confirm missing-function import failure.

- [ ] **Step 3: Implement `fit_rt_model()` and `bootstrap_rt_effect()`**

Use numpy least squares with columns: intercept, `rt_late_score`, `log_length`.
Do not include `n_cancers_significant_q05` in the adjusted-rank model because it is part of the
dNdScv ranking definition; including it makes the residual rank a breadth-adjusted diagnostic
rather than an RT residual.

- [ ] **Step 4: Verify GREEN**

Run the full t163 test file.

### Task 3: Adjusted Ranks, CLI, And Interpretation

**Files:**
- Modify: `code/scripts/tests/test_analyze_rt_dndscv_residual.py`
- Modify: `code/scripts/analyze_rt_dndscv_residual.py`
- Create: `doc/interpretations/2026-04-29-q003-rt-residual-regression.md`

- [ ] **Step 1: Write failing test for adjusted rank output**

```python
from analyze_rt_dndscv_residual import add_rt_adjusted_signal


def test_add_rt_adjusted_signal_keeps_rank_columns() -> None:
    table = pd.DataFrame(
        {
            "symbol": ["TTN", "TP53"],
            "dndscv_signal": [300.0, 300.0],
            "rt_late_score": [0.8, -0.6],
            "log_length": [3.0, 2.5],
            "n_cancers_significant_q05": [48, 64],
        }
    )
    model = {"intercept": 1.0, "beta_rt_late_score": 10.0, "beta_log_length": 0.0}

    out = add_rt_adjusted_signal(table, model)

    assert {"rt_adjusted_signal", "rt_adjusted_rank"}.issubset(out.columns)
    assert out.loc[out["symbol"] == "TTN", "rt_adjusted_signal"].iloc[0] < 300.0
```

- [ ] **Step 2: Implement adjusted ranks and CLI**

CLI inputs:

```bash
PYTHONPATH=code/scripts uv run --frozen python code/scripts/analyze_rt_dndscv_residual.py \
  --dndscv /data/packages/cbioportal/pan-cancer/summary/mut/table/three_way_ranking_comparison.feather \
  --rt data/gene_replication_timing.feather \
  --out-dir /data/packages/cbioportal/pan-cancer/summary/rt_residual \
  --n-boot 1000 \
  --seed 0
```

Outputs: `rt_dndscv_table.feather`, `rt_model_summary.feather`, `rt_bootstrap.feather`, `ttn_rank_check.feather`.

- [ ] **Step 3: Run analysis and write interpretation**

Interpret coefficient sign, bootstrap CI, RT-adjusted TTN rank, and whether TTN survives RT adjustment.

### Task 4: Workflow-Integration Follow-Up

**Files:**
- Modify: `tasks/active.md`

- [ ] **Step 1: File follow-up task**

Add a task for integrating standalone analysis scripts (`t154`, `t163`, and similar) into Snakemake if they become recurring outputs.

- [ ] **Step 2: Final verification**

Run:

```bash
PYTHONPATH=code/scripts uv run --frozen pytest code/scripts/tests/test_analyze_rt_dndscv_residual.py -q
uv run --frozen ruff check code/scripts/analyze_rt_dndscv_residual.py code/scripts/tests/test_analyze_rt_dndscv_residual.py
uv run --frozen ruff format --check code/scripts/analyze_rt_dndscv_residual.py code/scripts/tests/test_analyze_rt_dndscv_residual.py
uv run --frozen pyright code/scripts/analyze_rt_dndscv_residual.py
```

Expected: all pass.
