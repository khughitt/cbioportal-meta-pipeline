"""Tests for ``build_panel_callable_sizes.compute_callable_mb_table``.

Specification is task 1 of the t081 hypermutator / TMB annotation plan at
``doc/plans/2026-04-13-t081-hypermutator-annotation-pipeline-plan.md``.
"""

import logging

import pandas as pd
import pytest

from build_panel_callable_sizes import compute_callable_mb_table


_COVERAGE_COLUMNS = [
    "panel_id",
    "gene",
    "chromosome",
    "start",
    "end",
    "length_bp",
    "feature_type",
    "included",
]


def _make_coverage(rows: list[tuple]) -> pd.DataFrame:
    return pd.DataFrame.from_records(rows, columns=_COVERAGE_COLUMNS)


def test_bed_sum_three_exons_each_1000bp_gives_0_003_mb() -> None:
    cov = _make_coverage(
        [
            ("TEST-PANEL", "G1", "1", 0, 1_000, 1_000, "exon", True),
            ("TEST-PANEL", "G2", "1", 2_000, 3_000, 1_000, "exon", True),
            ("TEST-PANEL", "G3", "1", 4_000, 5_000, 1_000, "exon", True),
        ]
    )
    result = compute_callable_mb_table(
        cov,
        override_map={},
        wes_default_mb=30.0,
        required_panel_ids=["TEST-PANEL"],
    )
    row = result.loc[result["panel_id"] == "TEST-PANEL"].iloc[0]
    assert row["callable_mb"] == pytest.approx(0.003)
    assert row["source"] == "bed_sum"


def test_override_wins_regardless_of_bed() -> None:
    # BED suggests ~2 Mb, but the override map dictates 1.446 Mb. The override must win
    # with source == "config_override".
    cov = _make_coverage(
        [
            ("MSK-IMPACT-468", "G1", "1", 0, 2_000_000, 2_000_000, "exon", True),
        ]
    )
    result = compute_callable_mb_table(
        cov,
        override_map={"MSK-IMPACT-468": 1.446},
        wes_default_mb=30.0,
        required_panel_ids=["MSK-IMPACT-468"],
    )
    row = result.loc[result["panel_id"] == "MSK-IMPACT-468"].iloc[0]
    assert row["callable_mb"] == pytest.approx(1.446)
    assert row["source"] == "config_override"


def test_unknown_panel_gets_wes_default() -> None:
    cov = _make_coverage([])
    result = compute_callable_mb_table(
        cov,
        override_map={},
        wes_default_mb=30.0,
        required_panel_ids=["UNKNOWN-PANEL"],
    )
    row = result.loc[result["panel_id"] == "UNKNOWN-PANEL"].iloc[0]
    assert row["callable_mb"] == pytest.approx(30.0)
    assert row["source"] == "wes_default"


def test_bed_within_tolerance_of_override_uses_override_without_warning(
    caplog: pytest.LogCaptureFixture,
) -> None:
    # BED-derived 1.42 Mb is within ±5% of the 1.446 Mb override — no warning expected.
    cov = _make_coverage(
        [
            ("MSK-IMPACT-468", "G1", "1", 0, 1_420_000, 1_420_000, "exon", True),
        ]
    )
    with caplog.at_level(logging.WARNING, logger="build_panel_callable_sizes"):
        result = compute_callable_mb_table(
            cov,
            override_map={"MSK-IMPACT-468": 1.446},
            wes_default_mb=30.0,
            tolerance=0.05,
            required_panel_ids=["MSK-IMPACT-468"],
        )
    row = result.loc[result["panel_id"] == "MSK-IMPACT-468"].iloc[0]
    assert row["source"] == "config_override"
    assert row["callable_mb"] == pytest.approx(1.446)
    assert not any("tolerance" in record.message.lower() for record in caplog.records)


def test_bed_outside_tolerance_of_override_warns_but_override_still_wins(
    caplog: pytest.LogCaptureFixture,
) -> None:
    # BED-derived 1.30 Mb differs from the 1.446 Mb override by ~10% — outside the 5%
    # tolerance. Override still wins, but a warning must be emitted so the operator
    # can reconcile.
    cov = _make_coverage(
        [
            ("MSK-IMPACT-468", "G1", "1", 0, 1_300_000, 1_300_000, "exon", True),
        ]
    )
    with caplog.at_level(logging.WARNING, logger="build_panel_callable_sizes"):
        result = compute_callable_mb_table(
            cov,
            override_map={"MSK-IMPACT-468": 1.446},
            wes_default_mb=30.0,
            tolerance=0.05,
            required_panel_ids=["MSK-IMPACT-468"],
        )
    row = result.loc[result["panel_id"] == "MSK-IMPACT-468"].iloc[0]
    assert row["source"] == "config_override"
    assert row["callable_mb"] == pytest.approx(1.446)
    assert any(
        "MSK-IMPACT-468" in record.message and "tolerance" in record.message.lower()
        for record in caplog.records
    )


def test_output_has_row_for_every_required_panel_id() -> None:
    cov = _make_coverage(
        [
            ("A", "G1", "1", 0, 500_000, 500_000, "exon", True),
        ]
    )
    result = compute_callable_mb_table(
        cov,
        override_map={"B": 2.0},
        wes_default_mb=30.0,
        required_panel_ids=["A", "B", "C"],
    )
    assert set(result["panel_id"]) == {"A", "B", "C"}
    sources = dict(zip(result["panel_id"], result["source"]))
    assert sources == {"A": "bed_sum", "B": "config_override", "C": "wes_default"}


def test_non_exon_features_excluded_from_bed_sum() -> None:
    # Only ``feature_type == "exon"`` rows should contribute to the bed sum — introns
    # and other feature types must be ignored, per the plan's summation rule.
    cov = _make_coverage(
        [
            ("MIXED-PANEL", "G1", "1", 0, 1_000, 1_000, "exon", True),
            ("MIXED-PANEL", "G1", "1", 2_000, 10_000, 8_000, "intron", True),
        ]
    )
    result = compute_callable_mb_table(
        cov,
        override_map={},
        wes_default_mb=30.0,
        required_panel_ids=["MIXED-PANEL"],
    )
    row = result.loc[result["panel_id"] == "MIXED-PANEL"].iloc[0]
    assert row["callable_mb"] == pytest.approx(0.001)
    assert row["source"] == "bed_sum"


def test_output_column_order_is_stable() -> None:
    cov = _make_coverage([])
    result = compute_callable_mb_table(
        cov,
        override_map={"X": 1.0},
        wes_default_mb=30.0,
        required_panel_ids=["X"],
    )
    assert list(result.columns) == ["panel_id", "callable_mb", "source"]
