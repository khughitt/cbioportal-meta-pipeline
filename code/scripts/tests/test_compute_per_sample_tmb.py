# science:code
# status: library
# science:end
"""Tests for ``compute_per_sample_tmb.compute_tmb_for_study``.

Specification is task 2 of the t081 hypermutator / TMB annotation plan at
``doc/plans/2026-04-13-t081-hypermutator-annotation-pipeline-plan.md`` (plus
Assumption 3 for the protein-altering variant-class set).
"""

import math

import pandas as pd
import pytest

from compute_per_sample_tmb import (
    PROTEIN_ALTERING_VARIANT_CLASSES,
    _check_no_duplicate_sample_ids,
    compute_tmb_for_study,
    resolve_panel_for_sample,
)


_MUT_COLS = ["sample_id_tumor", "variant_class"]
_SAMPLE_COLS = ["sample_id", "cancer_type"]


def _make_muts(rows: list[tuple[str, str]]) -> pd.DataFrame:
    return pd.DataFrame.from_records(rows, columns=_MUT_COLS)


def _make_samples(sample_ids: list[str]) -> pd.DataFrame:
    return pd.DataFrame.from_records(
        [(sid, "Test Cancer") for sid in sample_ids], columns=_SAMPLE_COLS
    )


def test_mutation_count_counts_only_protein_altering_classes() -> None:
    # 3 protein-altering + 4 non-protein-altering for the same sample → count == 3.
    muts = _make_muts(
        [
            ("S1", "Missense_Mutation"),
            ("S1", "Nonsense_Mutation"),
            ("S1", "Frame_Shift_Del"),
            ("S1", "Silent"),
            ("S1", "Intron"),
            ("S1", "3'UTR"),
            ("S1", "5'UTR"),
        ]
    )
    samples = _make_samples(["S1"])
    out = compute_tmb_for_study(
        muts,
        samples,
        study_id="study_x",
        panel_callable_mb=1.0,
        panel_source="bed_sum",
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert row["mutation_count"] == 3


def test_full_protein_altering_set_all_counted() -> None:
    # Every element of the canonical protein-altering set contributes exactly once.
    sample_rows = [("S1", vc) for vc in sorted(PROTEIN_ALTERING_VARIANT_CLASSES)]
    muts = _make_muts(sample_rows)
    samples = _make_samples(["S1"])
    out = compute_tmb_for_study(
        muts, samples, study_id="s", panel_callable_mb=1.0, panel_source="bed_sum"
    )
    assert out.loc[out["sample_id"] == "S1", "mutation_count"].iloc[0] == len(
        PROTEIN_ALTERING_VARIANT_CLASSES
    )


def test_non_protein_altering_set_excluded() -> None:
    for excluded in ["Silent", "Intron", "3'UTR", "5'UTR", "RNA", "IGR"]:
        muts = _make_muts([("S1", excluded)])
        samples = _make_samples(["S1"])
        out = compute_tmb_for_study(
            muts, samples, study_id="s", panel_callable_mb=1.0, panel_source="bed_sum"
        )
        assert out.loc[out["sample_id"] == "S1", "mutation_count"].iloc[0] == 0, (
            f"variant_class {excluded!r} should be excluded from the TMB numerator"
        )


def test_tmb_is_mutation_count_divided_by_panel_callable_mb() -> None:
    muts = _make_muts(
        [
            ("S1", "Missense_Mutation"),
            ("S1", "Missense_Mutation"),
            ("S1", "Missense_Mutation"),
            ("S1", "Missense_Mutation"),
        ]
    )
    samples = _make_samples(["S1"])
    out = compute_tmb_for_study(
        muts, samples, study_id="s", panel_callable_mb=2.0, panel_source="bed_sum"
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert row["tmb"] == pytest.approx(2.0)  # 4 muts / 2 Mb


def test_tmb_log10_is_log10_of_tmb_plus_one() -> None:
    muts = _make_muts(
        [("S1", "Missense_Mutation")] * 9
    )  # 9 muts / 1 Mb → tmb 9, log10(10) == 1.0
    samples = _make_samples(["S1"])
    out = compute_tmb_for_study(
        muts, samples, study_id="s", panel_callable_mb=1.0, panel_source="bed_sum"
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert row["tmb_log10"] == pytest.approx(1.0)


def test_zero_mutation_samples_preserved_via_left_join() -> None:
    # S2 has no mutation rows at all — it must still appear in the output with
    # mutation_count = 0, tmb = 0, tmb_log10 = log10(1) = 0.
    muts = _make_muts([("S1", "Missense_Mutation")])
    samples = _make_samples(["S1", "S2"])
    out = compute_tmb_for_study(
        muts, samples, study_id="s", panel_callable_mb=1.0, panel_source="bed_sum"
    )
    assert set(out["sample_id"]) == {"S1", "S2"}
    row_s2 = out.loc[out["sample_id"] == "S2"].iloc[0]
    assert row_s2["mutation_count"] == 0
    assert row_s2["tmb"] == 0.0
    assert row_s2["tmb_log10"] == pytest.approx(0.0)


def test_study_id_column_present_on_every_row() -> None:
    muts = _make_muts([("S1", "Missense_Mutation")])
    samples = _make_samples(["S1", "S2", "S3"])
    out = compute_tmb_for_study(
        muts,
        samples,
        study_id="msk_impact_2017",
        panel_callable_mb=1.0,
        panel_source="bed_sum",
    )
    assert (out["study_id"] == "msk_impact_2017").all()
    assert out["study_id"].notna().all()


def test_tmb_source_column_records_panel_source() -> None:
    samples = _make_samples(["S1"])
    muts = _make_muts([("S1", "Missense_Mutation")])
    out = compute_tmb_for_study(
        muts,
        samples,
        study_id="s",
        panel_callable_mb=30.0,
        panel_source="wes_default",
    )
    assert out.loc[out["sample_id"] == "S1", "tmb_source"].iloc[0] == "wes_default"


def test_panel_callable_mb_column_propagates_into_output() -> None:
    samples = _make_samples(["S1"])
    muts = _make_muts([("S1", "Missense_Mutation")])
    out = compute_tmb_for_study(
        muts,
        samples,
        study_id="s",
        panel_callable_mb=1.446,
        panel_source="config_override",
    )
    assert out.loc[out["sample_id"] == "S1", "panel_callable_mb"].iloc[
        0
    ] == pytest.approx(1.446)


def test_mutation_not_in_samples_table_is_dropped() -> None:
    # A mutation attached to a sample_id_tumor that isn't in samples.feather should NOT
    # silently create a phantom row in the output. The samples table is authoritative.
    muts = _make_muts([("S1", "Missense_Mutation"), ("S_PHANTOM", "Missense_Mutation")])
    samples = _make_samples(["S1"])
    out = compute_tmb_for_study(
        muts, samples, study_id="s", panel_callable_mb=1.0, panel_source="bed_sum"
    )
    assert set(out["sample_id"]) == {"S1"}


def test_huge_tmb_sample_still_computed_correctly() -> None:
    # A deliberately ultra-hypermutated synthetic sample (5000 missense mutations in 1
    # Mb) should compute without error and carry the expected log10 value.
    muts = _make_muts([("S1", "Missense_Mutation")] * 5000)
    samples = _make_samples(["S1"])
    out = compute_tmb_for_study(
        muts, samples, study_id="s", panel_callable_mb=1.0, panel_source="bed_sum"
    )
    row = out.loc[out["sample_id"] == "S1"].iloc[0]
    assert row["mutation_count"] == 5000
    assert row["tmb"] == pytest.approx(5000.0)
    assert row["tmb_log10"] == pytest.approx(math.log10(5001.0))


# ---------------------------------------------------------------------------
# t070: per-sample Series path tests
# ---------------------------------------------------------------------------


def test_per_sample_panel_mb_drives_per_sample_tmb() -> None:
    """t070: when panel_callable_mb is a Series, each sample's TMB uses its own value."""
    muts = _make_muts(
        [
            ("S1", "Missense_Mutation"),
            ("S1", "Missense_Mutation"),
            ("S2", "Missense_Mutation"),
        ]
    )
    samples = _make_samples(["S1", "S2"])
    panel_mb = pd.Series([0.89, 1.22], index=["S1", "S2"], name="panel_callable_mb")
    panel_source = pd.Series(
        ["config_override", "config_override"], index=["S1", "S2"], name="tmb_source"
    )

    out = compute_tmb_for_study(
        muts,
        samples,
        study_id="msk_impact_2017",
        panel_callable_mb=panel_mb,
        panel_source=panel_source,
    )

    s1 = out.loc[out["sample_id"] == "S1"].iloc[0]
    s2 = out.loc[out["sample_id"] == "S2"].iloc[0]
    assert s1["panel_callable_mb"] == pytest.approx(0.89)
    assert s2["panel_callable_mb"] == pytest.approx(1.22)
    assert s1["tmb"] == pytest.approx(2 / 0.89)
    assert s2["tmb"] == pytest.approx(1 / 1.22)


def test_resolve_panel_for_sample_uses_panel_id_when_present() -> None:
    panel_registry = pd.DataFrame(
        {
            "panel_id": ["MSK-IMPACT-341", "MSK-IMPACT-468"],
            "callable_mb": [0.89, 1.22],
            "source": ["config_override", "config_override"],
        }
    )
    mb, source = resolve_panel_for_sample(
        sample_panel_id="MSK-IMPACT-468",
        study_id="msk_impact_2017",
        study_panel_map={},
        panel_registry=panel_registry,
        wes_default_callable_mb=30.0,
    )
    assert mb == pytest.approx(1.22)
    assert source == "config_override"


def test_resolve_panel_for_sample_falls_back_to_study_when_panel_id_missing() -> None:
    panel_registry = pd.DataFrame(
        {
            "panel_id": ["MSK-IMPACT-468"],
            "callable_mb": [1.22],
            "source": ["config_override"],
        }
    )
    mb, source = resolve_panel_for_sample(
        sample_panel_id=None,
        study_id="msk_impact_2017",
        study_panel_map={"msk_impact_2017": "MSK-IMPACT-468"},
        panel_registry=panel_registry,
        wes_default_callable_mb=30.0,
    )
    assert mb == pytest.approx(1.22)


def test_resolve_panel_for_sample_raises_for_unknown_panel_id() -> None:
    panel_registry = pd.DataFrame(
        {
            "panel_id": ["MSK-IMPACT-341"],
            "callable_mb": [0.89],
            "source": ["config_override"],
        }
    )
    with pytest.raises(ValueError, match="MSK-IMPACT-505"):
        resolve_panel_for_sample(
            sample_panel_id="MSK-IMPACT-505",
            study_id="msk_impact_2017",
            study_panel_map={},
            panel_registry=panel_registry,
            wes_default_callable_mb=30.0,
        )


# ---------------------------------------------------------------------------
# t070: duplicate sample_id guard
# ---------------------------------------------------------------------------


def test_check_no_duplicate_sample_ids_passes_when_unique() -> None:
    """t070: unique sample_ids should not raise."""
    samples = _make_samples(["S1", "S2", "S3"])
    _check_no_duplicate_sample_ids(samples, "test_study")  # no raise


def test_check_no_duplicate_sample_ids_raises_with_context() -> None:
    """t070: duplicate sample_ids must fail loud with the study_id and offending ids."""
    samples = _make_samples(["S1", "S1", "S2"])
    with pytest.raises(ValueError, match="test_study.*duplicate sample_id.*S1"):
        _check_no_duplicate_sample_ids(samples, "test_study")
