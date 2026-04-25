"""Tests for ``create_freq_tables.compute_freq_tables``.

Specification is task 7a of the t081 hypermutator / TMB annotation plan at
``doc/plans/2026-04-13-t081-hypermutator-annotation-pipeline-plan.md``. The
per-study freq-table step must emit inclusive/exclusive paired columns once
the cross-study samples_annotated feather carries ``is_hypermutator``.
"""

import pandas as pd
import pytest

from create_freq_tables import compute_freq_tables


def _muts(rows: list[tuple[str, str]]) -> pd.DataFrame:
    """Rows are ``(symbol, sample_id_tumor)`` tuples."""
    return pd.DataFrame.from_records(rows, columns=["symbol", "sample_id_tumor"])


def _samples(rows: list[tuple[str, str, str]]) -> pd.DataFrame:
    """Rows are ``(sample_id, cancer_type, cancer_type_detailed)``."""
    return pd.DataFrame.from_records(
        rows, columns=["sample_id", "cancer_type", "cancer_type_detailed"]
    )


def _hypermutator_flags(rows: list[tuple[str, bool]]) -> pd.DataFrame:
    return pd.DataFrame.from_records(rows, columns=["sample_id", "is_hypermutator"])


def test_no_hypermutators_inclusive_equals_exclusive() -> None:
    muts = _muts(
        [
            ("GENE1", "S1"),
            ("GENE1", "S2"),
            ("GENE2", "S3"),
        ]
    )
    samples = _samples(
        [
            ("S1", "Cancer A", "A detailed"),
            ("S2", "Cancer A", "A detailed"),
            ("S3", "Cancer B", "B detailed"),
        ]
    )
    flags = _hypermutator_flags([("S1", False), ("S2", False), ("S3", False)])

    _, _, gene_df, gene_cancer_df = compute_freq_tables(muts, samples, flags)

    assert (gene_df["num_inclusive"] == gene_df["num_exclusive"]).all()
    assert (gene_df["ratio_inclusive"] == gene_df["ratio_exclusive"]).all()
    assert (gene_cancer_df["num_inclusive"] == gene_cancer_df["num_exclusive"]).all()
    assert (
        gene_cancer_df["ratio_inclusive"] == gene_cancer_df["ratio_exclusive"]
    ).all()


def test_gene_mutated_only_in_hypermutator_has_zero_exclusive() -> None:
    muts = _muts(
        [
            ("HYPGENE", "HYP1"),
            ("NORMAL", "N1"),
            ("NORMAL", "N2"),
        ]
    )
    samples = _samples(
        [
            ("HYP1", "Cancer A", "A"),
            ("N1", "Cancer A", "A"),
            ("N2", "Cancer A", "A"),
        ]
    )
    flags = _hypermutator_flags([("HYP1", True), ("N1", False), ("N2", False)])
    _, _, gene_df, _ = compute_freq_tables(muts, samples, flags)
    hyp_row = gene_df.loc[gene_df["symbol"] == "HYPGENE"].iloc[0]
    assert hyp_row["num_inclusive"] == 1
    assert hyp_row["num_exclusive"] == 0
    assert hyp_row["ratio_exclusive"] == 0.0

    # Ratio_inclusive: 1 mutated / 3 samples = 1/3.
    assert hyp_row["ratio_inclusive"] == pd.Series([1 / 3]).iloc[0]


def test_denominators_reflect_inclusive_and_exclusive_sample_counts() -> None:
    muts = _muts(
        [
            ("NORMAL", "N1"),
            ("NORMAL", "N2"),
            ("NORMAL", "HYP1"),  # HYP1 also has NORMAL
        ]
    )
    samples = _samples(
        [
            ("N1", "Cancer A", "A"),
            ("N2", "Cancer A", "A"),
            ("N3", "Cancer A", "A"),  # N3 has no mutations but is in the cohort
            ("HYP1", "Cancer A", "A"),
        ]
    )
    flags = _hypermutator_flags(
        [("N1", False), ("N2", False), ("N3", False), ("HYP1", True)]
    )
    _, _, gene_df, _ = compute_freq_tables(muts, samples, flags)
    row = gene_df.loc[gene_df["symbol"] == "NORMAL"].iloc[0]
    # Inclusive: 3 mutated samples / 4 total = 0.75
    assert row["num_inclusive"] == 3
    assert row["ratio_inclusive"] == 0.75
    # Exclusive (HYP1 dropped from numerator AND denominator): 2 mutated / 3 non-hyp = 2/3
    assert row["num_exclusive"] == 2
    assert row["ratio_exclusive"] == pd.Series([2 / 3]).iloc[0]


def test_per_cancer_denominators_correct() -> None:
    muts = _muts(
        [
            ("GENE", "CA1"),
            ("GENE", "CA2"),
            ("GENE", "CB1"),
            ("GENE", "HYPB"),  # hypermutator in Cancer B
        ]
    )
    samples = _samples(
        [
            ("CA1", "Cancer A", "A"),
            ("CA2", "Cancer A", "A"),
            ("CA3", "Cancer A", "A"),
            ("CB1", "Cancer B", "B"),
            ("CB2", "Cancer B", "B"),
            ("HYPB", "Cancer B", "B"),
        ]
    )
    flags = _hypermutator_flags(
        [
            ("CA1", False),
            ("CA2", False),
            ("CA3", False),
            ("CB1", False),
            ("CB2", False),
            ("HYPB", True),
        ]
    )
    _, _, _, gene_cancer_df = compute_freq_tables(muts, samples, flags)

    # Cancer A: 2 mutated / 3 total (no hypermutators so inclusive == exclusive).
    row_a = gene_cancer_df.loc[
        (gene_cancer_df["cancer_type"] == "Cancer A")
        & (gene_cancer_df["symbol"] == "GENE")
    ].iloc[0]
    assert row_a["num_inclusive"] == 2
    assert row_a["num_exclusive"] == 2
    assert row_a["ratio_inclusive"] == pd.Series([2 / 3]).iloc[0]
    assert row_a["ratio_exclusive"] == pd.Series([2 / 3]).iloc[0]

    # Cancer B: inclusive 2 mutated / 3 total; exclusive 1 mutated / 2 non-hyp.
    row_b = gene_cancer_df.loc[
        (gene_cancer_df["cancer_type"] == "Cancer B")
        & (gene_cancer_df["symbol"] == "GENE")
    ].iloc[0]
    assert row_b["num_inclusive"] == 2
    assert row_b["ratio_inclusive"] == pd.Series([2 / 3]).iloc[0]
    assert row_b["num_exclusive"] == 1
    assert row_b["ratio_exclusive"] == 0.5


def test_n_samples_columns_emitted() -> None:
    muts = _muts([("G", "N1")])
    samples = _samples([("N1", "A", "A"), ("N2", "A", "A"), ("H1", "A", "A")])
    flags = _hypermutator_flags([("N1", False), ("N2", False), ("H1", True)])
    _, _, _, gene_cancer_df = compute_freq_tables(muts, samples, flags)
    row = gene_cancer_df.iloc[0]
    assert row["n_samples_inclusive"] == 3
    assert row["n_samples_exclusive"] == 2


def test_legacy_num_ratio_aliases_match_inclusive() -> None:
    muts = _muts([("G", "S1"), ("G", "S2")])
    samples = _samples([("S1", "A", "A"), ("S2", "A", "A"), ("H1", "A", "A")])
    flags = _hypermutator_flags([("S1", False), ("S2", False), ("H1", True)])
    cancer_df, cancer_detailed_df, gene_df, gene_cancer_df = compute_freq_tables(
        muts, samples, flags
    )
    for df in (cancer_df, cancer_detailed_df, gene_df, gene_cancer_df):
        assert (df["num"] == df["num_inclusive"]).all()
        assert (df["ratio"] == df["ratio_inclusive"]).all()


def test_sample_not_in_flags_defaults_to_not_hypermutator() -> None:
    # Absence from samples_annotated means we assume not-a-hypermutator.
    muts = _muts([("G", "S1")])
    samples = _samples([("S1", "A", "A"), ("S2", "A", "A")])
    flags = _hypermutator_flags([])  # empty — no flag info at all
    _, _, gene_df, _ = compute_freq_tables(muts, samples, flags)
    row = gene_df.iloc[0]
    assert row["num_inclusive"] == row["num_exclusive"]
    assert row["ratio_inclusive"] == row["ratio_exclusive"]


def test_all_hypermutators_exclusive_sample_count_is_zero_and_no_crash() -> None:
    # Edge case: every sample in a cancer type is a hypermutator → exclusive
    # denominator is zero; the output must not crash and should emit NaN or 0 for
    # the exclusive ratio (we pick NaN — undefined rate).
    muts = _muts([("G", "H1"), ("G", "H2")])
    samples = _samples([("H1", "A", "A"), ("H2", "A", "A")])
    flags = _hypermutator_flags([("H1", True), ("H2", True)])
    _, _, _, gene_cancer_df = compute_freq_tables(muts, samples, flags)
    row = gene_cancer_df.iloc[0]
    assert row["n_samples_exclusive"] == 0
    # ratio_exclusive should be NaN (undefined) when denominator is zero.
    assert pd.isna(row["ratio_exclusive"])


def test_output_feather_shapes_unchanged() -> None:
    # Regression: the four output DataFrames still key on cancer_type /
    # cancer_type_detailed / symbol / (cancer_type, symbol).
    muts = _muts([("G", "S1"), ("G", "S2")])
    samples = _samples([("S1", "A", "A1"), ("S2", "A", "A2")])
    flags = _hypermutator_flags([("S1", False), ("S2", False)])
    cancer_df, cancer_detailed_df, gene_df, gene_cancer_df = compute_freq_tables(
        muts, samples, flags
    )
    assert "cancer_type" in cancer_df.columns
    assert "cancer_type_detailed" in cancer_detailed_df.columns
    assert "symbol" in gene_df.columns
    assert {"cancer_type", "symbol"} <= set(gene_cancer_df.columns)


def test_panel_aware_gene_cancer_denominator() -> None:
    """t070: when samples are panel-mixed and panel_coverage is supplied, the
    denominator for a gene off the smaller panel must be reduced by the count
    of samples on that smaller panel."""
    muts = _muts(
        [
            ("GENE_A", "S1"),  # GENE_A on both panels, mutated in 1 sample
            ("GENE_B", "S2"),  # GENE_B only on PANEL_BIG, mutated in 1 sample
        ]
    )
    samples = pd.DataFrame(
        {
            "sample_id": ["S1", "S2", "S3", "S4"],
            "cancer_type": ["Cancer A"] * 4,
            "cancer_type_detailed": ["A detailed"] * 4,
            "panel_id": ["PANEL_BIG", "PANEL_BIG", "PANEL_SMALL", "PANEL_SMALL"],
        }
    )
    flags = _hypermutator_flags([(s, False) for s in ["S1", "S2", "S3", "S4"]])
    panel_coverage = pd.DataFrame(
        {
            "panel_id": ["PANEL_BIG", "PANEL_BIG", "PANEL_SMALL"],
            "gene": ["GENE_A", "GENE_B", "GENE_A"],
        }
    )

    _, _, _, gene_cancer = compute_freq_tables(
        muts, samples, flags, panel_coverage=panel_coverage
    )
    row_a = gene_cancer.loc[
        (gene_cancer["cancer_type"] == "Cancer A") & (gene_cancer["symbol"] == "GENE_A")
    ].iloc[0]
    row_b = gene_cancer.loc[
        (gene_cancer["cancer_type"] == "Cancer A") & (gene_cancer["symbol"] == "GENE_B")
    ].iloc[0]
    assert row_a["n_samples_inclusive"] == 4  # all panels cover GENE_A
    assert row_b["n_samples_inclusive"] == 2  # only PANEL_BIG covers GENE_B
    assert row_a["num_inclusive"] == 1
    assert row_b["num_inclusive"] == 1
    assert row_a["ratio_inclusive"] == pytest.approx(1 / 4)
    assert row_b["ratio_inclusive"] == pytest.approx(1 / 2)


def test_panel_coverage_none_preserves_cohort_denominator() -> None:
    """t070: when panel_coverage=None (WES study), behavior is unchanged."""
    muts = _muts([("GENE_A", "S1")])
    samples = pd.DataFrame(
        {
            "sample_id": ["S1", "S2"],
            "cancer_type": ["Cancer A", "Cancer A"],
            "cancer_type_detailed": ["A detailed", "A detailed"],
        }
    )
    flags = _hypermutator_flags([("S1", False), ("S2", False)])
    _, _, _, gene_cancer = compute_freq_tables(
        muts, samples, flags, panel_coverage=None
    )
    row = gene_cancer.iloc[0]
    assert row["n_samples_inclusive"] == 2


def test_panel_aware_gene_table_uses_per_gene_denominator() -> None:
    """t070: gene-keyed table denominator for an off-panel gene is reduced.

    PANEL_SMALL covers GENE_A but not GENE_B; PANEL_BIG covers both.
    Only PANEL_BIG samples should count toward the GENE_B denominator.
    """
    muts = _muts([("GENE_B", "S2")])  # GENE_B only on PANEL_BIG
    samples = pd.DataFrame(
        {
            "sample_id": ["S1", "S2", "S3", "S4"],
            "cancer_type": ["Cancer A"] * 4,
            "cancer_type_detailed": ["A detailed"] * 4,
            "panel_id": ["PANEL_BIG", "PANEL_BIG", "PANEL_SMALL", "PANEL_SMALL"],
        }
    )
    flags = _hypermutator_flags([(s, False) for s in ["S1", "S2", "S3", "S4"]])
    # PANEL_SMALL appears in coverage (covers GENE_A), but not GENE_B.
    panel_coverage = pd.DataFrame(
        {"panel_id": ["PANEL_BIG", "PANEL_SMALL"], "gene": ["GENE_B", "GENE_A"]}
    )

    _, _, gene_df, _ = compute_freq_tables(
        muts, samples, flags, panel_coverage=panel_coverage
    )
    row = gene_df.loc[gene_df["symbol"] == "GENE_B"].iloc[0]
    assert row["n_samples_inclusive"] == 2  # only the 2 PANEL_BIG samples
    assert row["num_inclusive"] == 1
    assert row["ratio_inclusive"] == pytest.approx(1 / 2)


def test_missing_panel_coverage_raises() -> None:
    """t070 prereq check: a panel_id used in samples but absent from panel_coverage
    must fail loud."""
    muts = _muts([("GENE_A", "S1")])
    samples = pd.DataFrame(
        {
            "sample_id": ["S1"],
            "cancer_type": ["Cancer A"],
            "cancer_type_detailed": ["A detailed"],
            "panel_id": ["PANEL_UNKNOWN"],
        }
    )
    flags = _hypermutator_flags([("S1", False)])
    panel_coverage = pd.DataFrame({"panel_id": ["PANEL_BIG"], "gene": ["GENE_A"]})
    with pytest.raises(ValueError, match="PANEL_UNKNOWN"):
        compute_freq_tables(muts, samples, flags, panel_coverage=panel_coverage)


def test_off_panel_gene_in_mut_dropped_with_warning(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """t070 spec error handling #6: gene in mut but on no panel → drop + WARNING.

    Use 200 on-panel genes + 1 off-panel gene so the off-panel fraction (0.5%) is
    below the 1% raise threshold, exercising the warn-and-drop path.
    """
    # 200 on-panel genes + 1 off-panel gene → 1/201 ≈ 0.5% < 1% threshold.
    on_panel_muts = [(f"GENE_{i}", "S1") for i in range(200)]
    muts = _muts(on_panel_muts + [("GENE_OFF_PANEL", "S2")])
    samples = pd.DataFrame(
        {
            "sample_id": ["S1", "S2", "S3", "S4"],
            "cancer_type": ["Cancer A"] * 4,
            "cancer_type_detailed": ["A detailed"] * 4,
            "panel_id": ["PANEL_BIG"] * 4,
        }
    )
    flags = _hypermutator_flags([(s, False) for s in ["S1", "S2", "S3", "S4"]])
    panel_coverage = pd.DataFrame(
        {
            "panel_id": ["PANEL_BIG"] * 200,
            "gene": [f"GENE_{i}" for i in range(200)],
        }
    )

    import logging

    with caplog.at_level(logging.WARNING):
        _, _, _, gene_cancer = compute_freq_tables(
            muts, samples, flags, panel_coverage=panel_coverage
        )

    # Off-panel gene must be absent from output (not present with NaN ratio).
    assert "GENE_OFF_PANEL" not in gene_cancer["symbol"].values
    # Warning must mention the dropped pair.
    assert any("GENE_OFF_PANEL" in msg for msg in caplog.text.splitlines())


def test_off_panel_gene_above_threshold_raises() -> None:
    """t070 spec: if >1% of mutated pairs have no panel coverage → ValueError."""
    # 99 off-panel mutations + 1 on-panel = 99% off-panel, way above 1% threshold.
    muts = _muts([("GENE_A", "S1")] + [(f"OFF_GENE_{i}", "S2") for i in range(99)])
    samples = pd.DataFrame(
        {
            "sample_id": ["S1", "S2"],
            "cancer_type": ["Cancer A", "Cancer A"],
            "cancer_type_detailed": ["A detailed", "A detailed"],
            "panel_id": ["PANEL_BIG", "PANEL_BIG"],
        }
    )
    flags = _hypermutator_flags([("S1", False), ("S2", False)])
    panel_coverage = pd.DataFrame({"panel_id": ["PANEL_BIG"], "gene": ["GENE_A"]})
    with pytest.raises(ValueError, match="no panel coverage"):
        compute_freq_tables(muts, samples, flags, panel_coverage=panel_coverage)


# --- Regression: mixed sample_id dtypes across study sources --------------- #
#
# Caught in the t131 full pan-cancer-dndscv run 2026-04-25: pog570_bcgsc_2020
# stores sample_id as int64 in samples.feather and sample_id_tumor as int64
# in mut.feather, while the cross-study samples_annotated.feather (built by
# combine_samples_tmb) carries str-typed sample_id post-concat. The merge
# `mut.merge(samples_meta).merge(flags)` failed with
#   ValueError: You are trying to merge on int64 and str columns for key 'sample_id'.
# Fix: cast every sample_id column to str at compute_freq_tables entry.

def test_int_sample_ids_in_mut_and_samples_with_str_flags() -> None:
    """Reproduces the pog570_bcgsc_2020 cross-study merge failure from
    full-run-#5 (2026-04-25)."""
    muts = pd.DataFrame.from_records(
        [("GENE1", 100), ("GENE1", 200), ("GENE2", 300)],
        columns=["symbol", "sample_id_tumor"],
    )
    # int sample_id (matches what pog570's samples.feather stores natively).
    samples = pd.DataFrame.from_records(
        [
            (100, "Cancer A", "A detailed"),
            (200, "Cancer A", "A detailed"),
            (300, "Cancer B", "B detailed"),
        ],
        columns=["sample_id", "cancer_type", "cancer_type_detailed"],
    )
    # str sample_id (matches what samples_annotated.feather carries post-concat
    # across mixed-dtype studies).
    flags = pd.DataFrame.from_records(
        [("100", False), ("200", False), ("300", False)],
        columns=["sample_id", "is_hypermutator"],
    )

    _, _, gene_df, gene_cancer_df = compute_freq_tables(muts, samples, flags)

    # Did not crash; produced expected per-gene rows.
    assert set(gene_df["symbol"]) == {"GENE1", "GENE2"}
    assert int(gene_df.loc[gene_df["symbol"] == "GENE1", "num_inclusive"].iloc[0]) == 2
    assert int(gene_df.loc[gene_df["symbol"] == "GENE2", "num_inclusive"].iloc[0]) == 1
