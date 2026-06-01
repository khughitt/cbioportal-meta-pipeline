# science:code
# status: library
# science:end
"""Tests for q027 signature-high impact aggregation."""

from __future__ import annotations

import pandas as pd

from create_q027_signature_high_impact_table import (
    compute_q027_signature_high_impact_table,
    make_count_audit_table,
)


def _view(
    *,
    symbol: str,
    cohort_view: str,
    n_samples: int,
    num: int,
) -> dict[str, object]:
    ratio = num / n_samples if n_samples else float("nan")
    return {
        "cancer_type": "Glioma",
        "symbol": symbol,
        "cohort_view": cohort_view,
        "num": num,
        "n_samples": n_samples,
        "ratio": ratio,
        "n_samples_hypermutator_excluded": n_samples,
        "num_hypermutator_excluded": num,
        "ratio_hypermutator_excluded": ratio,
    }


def _complete_rows(
    symbol: str, all_num: int, primary_num: int
) -> list[dict[str, object]]:
    return [
        _view(symbol=symbol, cohort_view="all_samples", n_samples=4, num=all_num),
        _view(
            symbol=symbol, cohort_view="signature_evaluable", n_samples=3, num=all_num
        ),
        _view(
            symbol=symbol,
            cohort_view="therapy_signature_high",
            n_samples=1,
            num=all_num - primary_num,
        ),
        _view(
            symbol=symbol,
            cohort_view="therapy_signature_high_excluded_primary",
            n_samples=3,
            num=primary_num,
        ),
        _view(
            symbol=symbol,
            cohort_view="therapy_signature_high_excluded_sensitivity_20",
            n_samples=2,
            num=max(primary_num - 1, 0),
        ),
        _view(
            symbol=symbol,
            cohort_view="therapy_signature_high_excluded_sensitivity_fraction_10",
            n_samples=2,
            num=max(primary_num - 1, 0),
        ),
    ]


def test_q027_impact_table_reports_deltas_ranks_and_count_audit() -> None:
    frame = pd.DataFrame([*_complete_rows("TP53", 2, 1), *_complete_rows("BRAF", 1, 1)])

    out = compute_q027_signature_high_impact_table([("study_a", frame)])
    tp53 = out.set_index("symbol").loc["TP53"]

    assert tp53["mean_all_samples"] == 0.5
    assert tp53["mean_therapy_signature_high_excluded_primary"] == 1 / 3
    assert tp53["delta_signature_high_excluded_primary"] == 0.5 - 1 / 3
    assert tp53["n_samples_removed_signature_high_excluded_primary"] == 1
    assert tp53["num_removed_signature_high_excluded_primary"] == 1
    assert (
        tp53["power_status_signature_high_excluded_primary"]
        == "underpowered_non_arbitrating"
    )

    audit = make_count_audit_table(out)
    assert "mean_all_samples" not in audit.columns
    assert "n_samples_removed_signature_high_excluded_primary" in audit.columns


def test_q027_impact_power_status_no_contrast_wins_before_underpowered() -> None:
    no_contrast = pd.DataFrame(
        [
            _view(symbol="TP53", cohort_view="all_samples", n_samples=4, num=1),
            _view(symbol="TP53", cohort_view="signature_evaluable", n_samples=4, num=1),
            _view(
                symbol="TP53", cohort_view="therapy_signature_high", n_samples=0, num=0
            ),
            _view(
                symbol="TP53",
                cohort_view="therapy_signature_high_excluded_primary",
                n_samples=4,
                num=1,
            ),
            _view(
                symbol="TP53",
                cohort_view="therapy_signature_high_excluded_sensitivity_20",
                n_samples=4,
                num=1,
            ),
            _view(
                symbol="TP53",
                cohort_view="therapy_signature_high_excluded_sensitivity_fraction_10",
                n_samples=4,
                num=1,
            ),
        ]
    )

    out = compute_q027_signature_high_impact_table([("study_a", no_contrast)])

    assert out.loc[0, "power_status_signature_high_excluded_primary"] == "no_contrast"
