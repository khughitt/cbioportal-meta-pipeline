# science:code
# status: library
# science:end
"""Unit tests for select_lib helpers."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
import pytest

import select_lib as lib


# ---- composite_sample_id ----


def test_composite_sample_id_format():
    assert lib.composite_sample_id("brca_tcga", "TCGA-A1") == "brca_tcga|TCGA-A1"


def test_composite_sample_id_pipe_in_input_raises():
    with pytest.raises(ValueError, match="pipe"):
        lib.composite_sample_id("brca|tcga", "s1")


# ---- build_sample_class ----


def test_build_sample_class_default_uses_study_only():
    samples = pd.DataFrame(
        {
            "composite_sample_id": ["s|1", "s|2"],
            "study": ["a", "b"],
            "age_tertile": ["1", "2"],
        }
    )
    out = lib.build_sample_class(samples, components=["study"])
    assert out.tolist() == ["a", "b"]
    assert out.index.tolist() == ["s|1", "s|2"]


def test_build_sample_class_compound():
    samples = pd.DataFrame(
        {
            "composite_sample_id": ["s|1", "s|2"],
            "study": ["a", "b"],
            "age_tertile": ["1", "2"],
        }
    )
    out = lib.build_sample_class(samples, components=["study", "age_tertile"])
    assert out.tolist() == ["a|1", "b|2"]


def test_build_sample_class_missing_component_raises():
    samples = pd.DataFrame({"composite_sample_id": ["x"], "study": ["a"]})
    with pytest.raises(KeyError, match="age_tertile"):
        lib.build_sample_class(samples, components=["study", "age_tertile"])


# ---- bh_fdr_within_groups ----


def test_bh_fdr_within_groups_recovers_known_q_values():
    """Two groups, each with [0.001, 0.5, 0.5] -> BH q [0.003, 0.5, 0.5]."""
    df = pd.DataFrame(
        {
            "g": ["A", "A", "A", "B", "B", "B"],
            "p": [0.001, 0.5, 0.5, 0.01, 0.5, 0.5],
        }
    )
    df["q"] = lib.bh_fdr_within_groups(df, group_cols=["g"], pvalue_col="p")
    a_qs = df[df["g"] == "A"]["q"].sort_values().tolist()
    np.testing.assert_allclose(a_qs, [0.003, 0.5, 0.5], rtol=1e-6)


def test_bh_fdr_within_groups_handles_nan():
    df = pd.DataFrame({"g": ["A"] * 4, "p": [0.001, 0.5, np.nan, 0.5]})
    df["q"] = lib.bh_fdr_within_groups(df, group_cols=["g"], pvalue_col="p")
    nan_q = df[df["p"].isna()]["q"].iloc[0]
    assert math.isnan(nan_q)


# ---- signed_stouffer ----


def test_signed_stouffer_all_positive_amplifies():
    """Three studies all CO with p=0.05 should give a stronger combined p."""
    z, p, n_used = lib.signed_stouffer(
        pvalues=np.array([0.05, 0.05, 0.05]),
        signs=np.array([+1, +1, +1]),
        weights=np.array([1.0, 1.0, 1.0]),
    )
    assert z > 0
    assert p < 0.05
    assert n_used == 3


def test_signed_stouffer_opposing_signs_cancel():
    """Three studies, half CO and half ME at the same p -- combined Z near zero."""
    z, p, n_used = lib.signed_stouffer(
        pvalues=np.array([0.01, 0.01, 0.01]),
        signs=np.array([+1, -1, +1]),
        weights=np.array([1.0, 1.0, 1.0]),
    )
    # 2 positive + 1 negative -- partial cancellation, z still small relative to all-aligned
    assert abs(z) < 2.0
    z2, _, _ = lib.signed_stouffer(
        pvalues=np.array([0.01, 0.01, 0.01]),
        signs=np.array([+1, +1, +1]),
        weights=np.array([1.0, 1.0, 1.0]),
    )
    assert abs(z) < z2


def test_signed_stouffer_zero_sign_contributes_zero_z():
    """A study with direction=='none' gets sign 0 and contributes 0 weighted z."""
    z_with_none, _, _ = lib.signed_stouffer(
        pvalues=np.array([0.05, 0.5]),
        signs=np.array([+1, 0]),
        weights=np.array([1.0, 1.0]),
    )
    z_alone, _, _ = lib.signed_stouffer(
        pvalues=np.array([0.05]),
        signs=np.array([+1]),
        weights=np.array([1.0]),
    )
    # Adding a sign=0 study reduces the weighted-z (denominator grows).
    assert abs(z_with_none) < abs(z_alone)


def test_signed_stouffer_drops_nan_pvalues():
    z, _, n_used = lib.signed_stouffer(
        pvalues=np.array([0.05, np.nan]),
        signs=np.array([+1, +1]),
        weights=np.array([1.0, 1.0]),
    )
    assert n_used == 1


# ---- direction_consensus_frac ----


def test_direction_consensus_frac():
    assert lib.direction_consensus_frac(["CO", "CO", "ME"]) == pytest.approx(2 / 3)
    assert lib.direction_consensus_frac(["CO", "CO", "CO"]) == 1.0
    assert lib.direction_consensus_frac(["CO", "ME"]) == 0.5
    # 'none' rows are excluded from the denominator (they carry no direction info).
    assert lib.direction_consensus_frac(["CO", "none", "none"]) == 1.0
    assert math.isnan(lib.direction_consensus_frac([]))
    assert math.isnan(lib.direction_consensus_frac(["none", "none"]))
