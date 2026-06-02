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
    n_samples_hypermutator_excluded: int | None = None,
    num_hypermutator_excluded: int | None = None,
) -> dict[str, object]:
    ratio = num / n_samples if n_samples else float("nan")
    hyper_n = (
        n_samples
        if n_samples_hypermutator_excluded is None
        else n_samples_hypermutator_excluded
    )
    hyper_num = num if num_hypermutator_excluded is None else num_hypermutator_excluded
    hyper_ratio = hyper_num / hyper_n if hyper_n else float("nan")
    return {
        "cancer_type": "Glioma",
        "symbol": symbol,
        "cohort_view": cohort_view,
        "num": num,
        "n_samples": n_samples,
        "ratio": ratio,
        "n_samples_hypermutator_excluded": hyper_n,
        "num_hypermutator_excluded": hyper_num,
        "ratio_hypermutator_excluded": hyper_ratio,
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
        _view(
            symbol=symbol,
            cohort_view="signature_evaluable_high_excluded_primary",
            n_samples=2,
            num=primary_num,
        ),
        _view(
            symbol=symbol,
            cohort_view="signature_evaluable_high_excluded_sensitivity_20",
            n_samples=2,
            num=max(primary_num - 1, 0),
        ),
        _view(
            symbol=symbol,
            cohort_view="signature_evaluable_high_excluded_sensitivity_fraction_10",
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
    assert tp53["delta_signature_evaluable_high_excluded_primary"] == (2 / 3) - 0.5
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
            _view(
                symbol="TP53",
                cohort_view="signature_evaluable_high_excluded_primary",
                n_samples=4,
                num=1,
            ),
            _view(
                symbol="TP53",
                cohort_view="signature_evaluable_high_excluded_sensitivity_20",
                n_samples=4,
                num=1,
            ),
            _view(
                symbol="TP53",
                cohort_view="signature_evaluable_high_excluded_sensitivity_fraction_10",
                n_samples=4,
                num=1,
            ),
        ]
    )

    out = compute_q027_signature_high_impact_table([("study_a", no_contrast)])

    assert out.loc[0, "power_status_signature_high_excluded_primary"] == "no_contrast"


def test_q027_impact_power_status_no_comparator() -> None:
    no_comparator = pd.DataFrame(
        [
            _view(symbol="TP53", cohort_view="all_samples", n_samples=1, num=1),
            _view(symbol="TP53", cohort_view="signature_evaluable", n_samples=1, num=1),
            _view(
                symbol="TP53", cohort_view="therapy_signature_high", n_samples=1, num=1
            ),
            _view(
                symbol="TP53",
                cohort_view="therapy_signature_high_excluded_primary",
                n_samples=0,
                num=0,
            ),
            _view(
                symbol="TP53",
                cohort_view="therapy_signature_high_excluded_sensitivity_20",
                n_samples=0,
                num=0,
            ),
            _view(
                symbol="TP53",
                cohort_view="therapy_signature_high_excluded_sensitivity_fraction_10",
                n_samples=0,
                num=0,
            ),
            _view(
                symbol="TP53",
                cohort_view="signature_evaluable_high_excluded_primary",
                n_samples=0,
                num=0,
            ),
            _view(
                symbol="TP53",
                cohort_view="signature_evaluable_high_excluded_sensitivity_20",
                n_samples=0,
                num=0,
            ),
            _view(
                symbol="TP53",
                cohort_view="signature_evaluable_high_excluded_sensitivity_fraction_10",
                n_samples=0,
                num=0,
            ),
        ]
    )

    out = compute_q027_signature_high_impact_table([("study_a", no_comparator)])

    assert out.loc[0, "power_status_signature_high_excluded_primary"] == "no_comparator"


def test_q027_impact_power_status_interpretable_with_two_studies() -> None:
    study_a = pd.DataFrame(_complete_rows("TP53", 2, 1))
    study_b = pd.DataFrame(_complete_rows("TP53", 1, 1))

    out = compute_q027_signature_high_impact_table(
        [("study_a", study_a), ("study_b", study_b)]
    )

    assert out.loc[0, "power_status_signature_high_excluded_primary"] == "interpretable"
    assert (
        out.loc[0, "power_status_signature_evaluable_high_excluded_primary"]
        == "interpretable"
    )


def test_q027_impact_hypermutator_marginal_delta_can_be_no_contrast() -> None:
    rows = pd.DataFrame(
        [
            _view(
                symbol="TP53",
                cohort_view="all_samples",
                n_samples=4,
                num=2,
                n_samples_hypermutator_excluded=3,
                num_hypermutator_excluded=1,
            ),
            _view(
                symbol="TP53",
                cohort_view="signature_evaluable",
                n_samples=3,
                num=2,
                n_samples_hypermutator_excluded=2,
                num_hypermutator_excluded=1,
            ),
            _view(
                symbol="TP53",
                cohort_view="therapy_signature_high",
                n_samples=1,
                num=1,
                n_samples_hypermutator_excluded=0,
                num_hypermutator_excluded=0,
            ),
            _view(
                symbol="TP53",
                cohort_view="therapy_signature_high_excluded_primary",
                n_samples=3,
                num=1,
                n_samples_hypermutator_excluded=3,
                num_hypermutator_excluded=1,
            ),
            _view(
                symbol="TP53",
                cohort_view="therapy_signature_high_excluded_sensitivity_20",
                n_samples=3,
                num=1,
                n_samples_hypermutator_excluded=3,
                num_hypermutator_excluded=1,
            ),
            _view(
                symbol="TP53",
                cohort_view="therapy_signature_high_excluded_sensitivity_fraction_10",
                n_samples=3,
                num=1,
                n_samples_hypermutator_excluded=3,
                num_hypermutator_excluded=1,
            ),
            _view(
                symbol="TP53",
                cohort_view="signature_evaluable_high_excluded_primary",
                n_samples=2,
                num=1,
                n_samples_hypermutator_excluded=2,
                num_hypermutator_excluded=1,
            ),
            _view(
                symbol="TP53",
                cohort_view="signature_evaluable_high_excluded_sensitivity_20",
                n_samples=2,
                num=1,
                n_samples_hypermutator_excluded=2,
                num_hypermutator_excluded=1,
            ),
            _view(
                symbol="TP53",
                cohort_view="signature_evaluable_high_excluded_sensitivity_fraction_10",
                n_samples=2,
                num=1,
                n_samples_hypermutator_excluded=2,
                num_hypermutator_excluded=1,
            ),
        ]
    )

    out = compute_q027_signature_high_impact_table([("study_a", rows)])

    assert out.loc[0, "delta_signature_high_excluded_primary"] == 0.5 - (1 / 3)
    assert (
        out.loc[0, "delta_signature_high_excluded_primary_hypermutator_excluded"] == 0
    )
    assert (
        out.loc[0, "power_status_signature_high_excluded_primary_hypermutator_excluded"]
        == "no_contrast"
    )
