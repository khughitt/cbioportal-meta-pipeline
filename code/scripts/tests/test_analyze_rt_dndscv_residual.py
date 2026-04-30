import pandas as pd

from analyze_rt_dndscv_residual import (
    add_rt_adjusted_signal,
    bootstrap_rt_effect,
    build_rt_dndscv_table,
    fit_rt_model,
)


def test_build_rt_dndscv_table_merges_rt_and_computes_signal() -> None:
    dndscv = pd.DataFrame(
        [
            {
                "symbol": "TTN",
                "min_qglobal": 0.0,
                "n_cancers_significant_q05": 48,
                "rank_dndscv": 4,
                "length": 34350.0,
            },
            {
                "symbol": "TP53",
                "min_qglobal": 1e-8,
                "n_cancers_significant_q05": 64,
                "rank_dndscv": 1,
                "length": 393.0,
            },
        ]
    )
    rt = pd.DataFrame(
        [
            {
                "symbol": "TTN",
                "rt_constitutive_label": "CL",
                "rt_ce_fraction": 0.1,
                "rt_cl_fraction": 0.9,
            },
            {
                "symbol": "TP53",
                "rt_constitutive_label": "CE",
                "rt_ce_fraction": 0.8,
                "rt_cl_fraction": 0.2,
            },
        ]
    )

    out = build_rt_dndscv_table(dndscv, rt, q_floor=1e-300)

    by_symbol = out.set_index("symbol")
    assert by_symbol.loc["TTN", "dndscv_signal"] == 300.0
    assert by_symbol.loc["TTN", "rt_late_score"] == 0.8
    assert by_symbol.loc["TP53", "rt_late_score"] == -0.6000000000000001


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
    model = {
        "intercept": 1.0,
        "beta_rt_late_score": 10.0,
        "beta_log_length": 0.0,
        "beta_n_cancers_significant_q05": 0.0,
    }

    out = add_rt_adjusted_signal(table, model)

    assert {"rt_adjusted_signal", "rt_adjusted_rank"}.issubset(out.columns)
    assert out.loc[out["symbol"] == "TTN", "rt_adjusted_signal"].iloc[0] < 300.0
