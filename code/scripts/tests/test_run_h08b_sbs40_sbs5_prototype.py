# science:code
# status: workflow-owned
# science:end

from __future__ import annotations

import numpy as np
import pandas as pd

from run_h08b_sbs40_sbs5_prototype import (
    apply_bh,
    build_clr_outcomes,
    build_target_expression,
    fit_adjusted_cell,
)


def test_sbs40_collapse_uses_only_active_manifest_parts() -> None:
    expo = pd.DataFrame(
        {
            "SBS5": [1.0],
            "SBS40a": [2.0],
            "SBS40b": [100.0],
            "SBS40c": [3.0],
            "SBS1": [4.0],
        },
        index=["s1"],
    )

    out = build_clr_outcomes(expo, active=["SBS1", "SBS5", "SBS40a", "SBS40c"])

    expected = np.log(2.0 + 3.0 + 0.5) - np.log(1.0 + 0.5)
    assert out.loc["s1", "sbs40_active_parts"] == "SBS40a|SBS40c"
    assert np.isclose(out.loc["s1", "clr_SBS40_minus_SBS5"], expected)


def test_primary_contrast_equals_clr_sbs40_minus_clr_sbs5() -> None:
    expo = pd.DataFrame(
        {"SBS5": [9.0, 3.0], "SBS40a": [1.0, 7.0], "SBS1": [5.0, 5.0]},
        index=["s1", "s2"],
    )

    out = build_clr_outcomes(expo, active=["SBS1", "SBS5", "SBS40a"])

    assert np.allclose(out["clr_SBS40_minus_SBS5"], out["clr_SBS40"] - out["clr_SBS5"])


def test_fit_adjusted_cell_uses_age_as_numeric_adjustment_after_all_column_dropna() -> (
    None
):
    df = pd.DataFrame(
        {
            "y": [0.0, 1.0, 2.0, 3.0],
            "module_01": [0.0, 1.0, 2.0, 3.0],
            "age": [50.0, 60.0, np.nan, 80.0],
            "ancestry": ["A", "A", "B", "B"],
            "treatment": [0.0, 1.0, 0.0, 1.0],
        }
    )

    fit = fit_adjusted_cell(
        df,
        "y",
        "module_01",
        categorical_adjust=["ancestry"],
        numeric_adjust=["age"],
        min_n=3,
    )

    assert fit is not None
    assert fit["n"] == 3
    assert fit["numeric_adjust"] == "age"


def test_missing_polz_returns_not_evaluable_target_row() -> None:
    rsem = pd.DataFrame(
        {"TCGA-01-0001-01A": [10.0], "TCGA-01-0002-01A": [20.0]},
        index=pd.Index(["REV3L"], name="Hugo_Symbol"),
    )

    expr, status = build_target_expression(
        rsem,
        sample_ids=["TCGA-01-0001-01A", "TCGA-01-0002-01A"],
        genes=["REV3L", "POLZ"],
    )

    assert "REV3L" in expr.columns
    polz = status[status["gene"] == "POLZ"].iloc[0]
    assert polz["status"] == "not_evaluable_missing_expression_row"
    assert polz["n_expression_samples"] == 0


def test_apply_bh_uses_monotone_adjustment() -> None:
    grid = pd.DataFrame(
        {
            "family": ["a", "a", "a", "a"],
            "pvalue": [0.04, 0.001, 0.03, 0.02],
        }
    )

    out = apply_bh(grid, family_cols=["family"]).sort_values("pvalue")

    assert out["q_bh"].is_monotonic_increasing
    assert np.isclose(out.iloc[0]["q_bh"], 0.004)
