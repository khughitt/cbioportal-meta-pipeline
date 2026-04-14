"""Tests for ``create_freq_tables.compute_freq_tables``.

Specification is task 7a of the t081 hypermutator / TMB annotation plan at
``doc/plans/2026-04-13-t081-hypermutator-annotation-pipeline-plan.md``. The
per-study freq-table step must emit inclusive/exclusive paired columns once
the cross-study samples_annotated feather carries ``is_hypermutator``.
"""

import pandas as pd

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
