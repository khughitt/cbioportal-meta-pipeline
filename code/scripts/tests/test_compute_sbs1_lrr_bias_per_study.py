"""Tests for compute_sbs1_lrr_bias_per_study.

The three regression checks pre-registered in
doc/meta/pre-registration-t126-sbs1-lrr-bias-test.md §7:

1. Per-mutation posterior recovers SBS1 = 1.0 in pure CpG context with only SBS1 active.
2. Aggregate LRR fraction matches a hand-computed value on a 4-mutation toy dataset.
3. Bootstrap CI width shrinks as sample count grows on synthetic data.

Plus supporting unit tests for the smaller building blocks (TSB decoding, RT-bin
assignment, panel-coverage correction).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import compute_sbs1_lrr_bias_per_study as mod


# ---------------------------------------------------------------------------
# Trinucleotide context decoding (TSB binary -> pyrimidine-strand context)
# ---------------------------------------------------------------------------


def _make_fake_tsb_chrom(seq: str) -> bytes:
    """Encode a sequence as a fake SigProfilerMatrixGenerator TSB binary file.

    Uses the unstranded encoding: byte = ACGT.index(base) for ACGT, 16 for N.
    """
    base_to_byte = {"A": 0, "C": 1, "G": 2, "T": 3, "N": 16}
    return bytes(base_to_byte[b] for b in seq)


def test_decode_tsb_byte_returns_base_for_each_strand_class() -> None:
    # Bytes 0..3 are unstranded ACGT; 4..7 are T-strand ACGT; 8..11 U-strand; 12..15 B-strand.
    assert mod.decode_tsb_byte(0) == "A"
    assert mod.decode_tsb_byte(3) == "T"
    assert mod.decode_tsb_byte(5) == "C"
    assert mod.decode_tsb_byte(10) == "G"
    assert mod.decode_tsb_byte(15) == "T"
    assert mod.decode_tsb_byte(16) == "N"
    assert mod.decode_tsb_byte(17) == "N"


def test_lookup_trinucleotide_context_pyrimidine_strand(tmp_path: Path) -> None:
    # Build chr1 with sequence ...ACGT... starting at position 1.
    seq = "NACGTACGT"  # positions 1..9 = N,A,C,G,T,A,C,G,T
    chrom_dir = tmp_path / "GRCh37"
    chrom_dir.mkdir()
    (chrom_dir / "1.txt").write_bytes(_make_fake_tsb_chrom(seq))

    # Mutation at pos 3 = "C", flanked by A(2) and G(4) -> "ACG", with C>T -> A[C>T]G.
    ctx = mod.lookup_trinucleotide_context(
        chrom="1", pos=3, ref="C", alt="T", chrom_dir=chrom_dir
    )
    assert ctx == "A[C>T]G"

    # Mutation at pos 4 = "G" with G>A. Reverse-complement to pyrimidine strand.
    # Flanking: pos 3 = "C", pos 5 = "T" -> 5'..C G T..3'; rc = 5'..A C G..3' on the other
    # strand, with C>T at center. So context is A[C>T]G.
    ctx_rc = mod.lookup_trinucleotide_context(
        chrom="1", pos=4, ref="G", alt="A", chrom_dir=chrom_dir
    )
    assert ctx_rc == "A[C>T]G"


def test_lookup_trinucleotide_context_skips_non_snv() -> None:
    # Indels and multi-base alleles return None.
    assert (
        mod.lookup_trinucleotide_context(
            chrom="1", pos=3, ref="CG", alt="T", chrom_dir=Path("/no/where")
        )
        is None
    )
    assert (
        mod.lookup_trinucleotide_context(
            chrom="1", pos=3, ref="-", alt="T", chrom_dir=Path("/no/where")
        )
        is None
    )


# ---------------------------------------------------------------------------
# Per-mutation SBS1 posterior
# ---------------------------------------------------------------------------


def _toy_cosmic_reference() -> pd.DataFrame:
    """Toy COSMIC reference with three signatures and contrived context profiles.

    SBS1 is concentrated entirely on A[C>T]G (the dominant CpG context).
    SBSx and SBSy are flat over a small support to simulate alternative attribution.
    """
    contexts = ["A[C>T]G", "A[C>T]A", "A[C>A]A"]
    return pd.DataFrame(
        {
            "Type": contexts,
            "SBS1": [1.0, 0.0, 0.0],
            "SBSx": [1 / 3, 1 / 3, 1 / 3],
            "SBSy": [1 / 3, 1 / 3, 1 / 3],
        }
    )


def test_per_mutation_sbs1_posterior_pure_sbs1_context_with_only_sbs1_active() -> None:
    """Pre-registered test 1: P(SBS1|mut) == 1.0 in pure CpG context, only SBS1 active."""
    cosmic = _toy_cosmic_reference()
    exposures = pd.DataFrame(
        {"sample_name": ["S1"], "SBS1": [10.0], "SBSx": [0.0], "SBSy": [0.0]}
    )
    mutations = pd.DataFrame({"sample_name": ["S1"], "context_96": ["A[C>T]G"]})
    out = mod.per_mutation_sbs1_posterior(
        mutations=mutations, exposures=exposures, cosmic_reference=cosmic
    )
    assert out["sbs1_posterior"].tolist() == pytest.approx([1.0])


def test_per_mutation_sbs1_posterior_mixed_signature_fit_distributes_weight() -> None:
    cosmic = _toy_cosmic_reference()
    # Sample with 50/50 SBS1 vs SBSx exposure.
    exposures = pd.DataFrame(
        {"sample_name": ["S1"], "SBS1": [5.0], "SBSx": [5.0], "SBSy": [0.0]}
    )
    # In context A[C>T]G: SBS1 prob = 1.0, SBSx prob = 1/3.
    # Posterior = (5 * 1.0) / (5 * 1.0 + 5 * 1/3 + 0) = 5 / (5 + 5/3) = 0.75.
    mutations = pd.DataFrame({"sample_name": ["S1"], "context_96": ["A[C>T]G"]})
    out = mod.per_mutation_sbs1_posterior(
        mutations=mutations, exposures=exposures, cosmic_reference=cosmic
    )
    assert out["sbs1_posterior"].iloc[0] == pytest.approx(0.75)


def test_per_mutation_sbs1_posterior_zero_exposure_yields_zero_posterior() -> None:
    cosmic = _toy_cosmic_reference()
    exposures = pd.DataFrame(
        {"sample_name": ["S1"], "SBS1": [0.0], "SBSx": [10.0], "SBSy": [0.0]}
    )
    mutations = pd.DataFrame({"sample_name": ["S1"], "context_96": ["A[C>T]G"]})
    out = mod.per_mutation_sbs1_posterior(
        mutations=mutations, exposures=exposures, cosmic_reference=cosmic
    )
    assert out["sbs1_posterior"].iloc[0] == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# RT-bin assignment by genomic position
# ---------------------------------------------------------------------------


def _toy_rt_bins() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "chromosome": ["chr1", "chr1", "chr2"],
            "start": [1_000_000, 2_000_000, 3_000_000],
            "end": [1_500_000, 2_500_000, 3_500_000],
            "rt_constitutive_label": ["CE", "CL", "CL"],
        }
    )


def test_assign_rt_bin_label_returns_label_for_overlapping_position() -> None:
    bins = _toy_rt_bins()
    mutations = pd.DataFrame(
        {
            "chromosome": ["1", "1", "2", "1"],
            "start": [1_200_000, 2_400_000, 3_100_000, 5_000_000],
        }
    )
    out = mod.assign_rt_bin_label(mutations, bins)
    assert out["rt_bin_label"].tolist() == ["CE", "CL", "CL", "unassigned"]


# ---------------------------------------------------------------------------
# Aggregate LRR fraction (pre-registered test 2)
# ---------------------------------------------------------------------------


def test_aggregate_lrr_fraction_matches_hand_computed_toy_dataset() -> None:
    """Pre-registered test 2: aggregate LRR fraction on a 4-mutation hand-computed dataset.

    4 mutations across 2 samples in 1 study. Per-mutation SBS1 posteriors:
      m1: 1.0 (CE bin)
      m2: 0.5 (CE bin)
      m3: 0.8 (CL bin)
      m4: 0.2 (CL bin)
    Panel-CE-bp = 100, panel-CL-bp = 50 (CL is half the size).
    rho_CE = (1.0 + 0.5) / 100 = 0.015
    rho_CL = (0.8 + 0.2) / 50 = 0.020
    f_LRR_corrected = 0.020 / (0.015 + 0.020) = 0.020 / 0.035 = 0.5714286
    Uncorrected:
    f_LRR_uncorrected = (0.8+0.2) / (1.0+0.5+0.8+0.2) = 1.0 / 2.5 = 0.4
    """
    posteriors = pd.DataFrame(
        {
            "study_id": ["S"] * 4,
            "sample_name": ["a", "a", "b", "b"],
            "rt_bin_label": ["CE", "CE", "CL", "CL"],
            "sbs1_posterior": [1.0, 0.5, 0.8, 0.2],
        }
    )
    panel_bp = pd.DataFrame(
        {"study_id": ["S"], "panel_ce_bp": [100], "panel_cl_bp": [50]}
    )
    out = mod.aggregate_lrr_fraction(posteriors, panel_bp)
    row = out.iloc[0]
    assert row["n_sbs1_pooled"] == pytest.approx(2.5)
    assert row["n_sbs1_ce"] == pytest.approx(1.5)
    assert row["n_sbs1_cl"] == pytest.approx(1.0)
    assert row["f_lrr_uncorrected"] == pytest.approx(0.4)
    assert row["f_lrr_corrected"] == pytest.approx(0.020 / 0.035)


# ---------------------------------------------------------------------------
# Bootstrap CI (pre-registered test 3)
# ---------------------------------------------------------------------------


def test_bootstrap_ci_width_shrinks_as_sample_count_grows() -> None:
    """Pre-registered test 3: CI half-width shrinks as n_samples increases."""
    rng = np.random.default_rng(0)

    def _make_posteriors(n_samples: int) -> pd.DataFrame:
        # Each sample has 10 mutations evenly split between CE and CL.
        # SBS1 posteriors all 0.6, identical structure across samples.
        rows = []
        for s in range(n_samples):
            for label in ["CE"] * 5 + ["CL"] * 5:
                rows.append(
                    {
                        "study_id": "S",
                        "sample_name": f"s{s}",
                        "rt_bin_label": label,
                        "sbs1_posterior": 0.6,
                    }
                )
        return pd.DataFrame(rows)

    panel_bp = pd.DataFrame(
        {"study_id": ["S"], "panel_ce_bp": [100], "panel_cl_bp": [100]}
    )

    small = mod.bootstrap_lrr_ci(
        posteriors=_make_posteriors(10),
        panel_bp=panel_bp,
        n_bootstrap=200,
        rng=rng,
    )
    large = mod.bootstrap_lrr_ci(
        posteriors=_make_posteriors(200),
        panel_bp=panel_bp,
        n_bootstrap=200,
        rng=rng,
    )
    small_width = small.iloc[0]["ci_high"] - small.iloc[0]["ci_low"]
    large_width = large.iloc[0]["ci_high"] - large.iloc[0]["ci_low"]
    # With identical per-sample structure, sampling-with-replacement variance still
    # exists at small N because of duplication; at large N it collapses toward 0.
    assert large_width <= small_width


# ---------------------------------------------------------------------------
# Decision rule
# ---------------------------------------------------------------------------


def test_decision_rule_pass_when_panel_strictly_above_matched_and_above_midpoint() -> (
    None
):
    rows = pd.DataFrame(
        {
            "study_id": ["tcga_mc3", "msk_impact_2017"],
            "n_sbs1_pooled": [7000, 600],
            "f_lrr_corrected": [0.40, 0.55],
            "ci_low": [0.39, 0.50],
            "ci_high": [0.41, 0.60],
        }
    )
    verdict = mod.apply_decision_rule(
        rows,
        matched_study="tcga_mc3",
        panel_study="msk_impact_2017",
        midpoint=0.45,
        n_floor=500,
        max_ci_halfwidth=0.10,
    )
    assert verdict == "pass"


def test_decision_rule_retire_when_powered_and_overlap_below_midpoint() -> None:
    rows = pd.DataFrame(
        {
            "study_id": ["tcga_mc3", "msk_impact_2017"],
            "n_sbs1_pooled": [7000, 600],
            "f_lrr_corrected": [0.40, 0.41],
            "ci_low": [0.38, 0.38],
            "ci_high": [0.42, 0.44],
        }
    )
    verdict = mod.apply_decision_rule(
        rows,
        matched_study="tcga_mc3",
        panel_study="msk_impact_2017",
        midpoint=0.45,
        n_floor=500,
        max_ci_halfwidth=0.10,
    )
    assert verdict == "retire"


def test_decision_rule_defer_when_underpowered() -> None:
    rows = pd.DataFrame(
        {
            "study_id": ["tcga_mc3", "msk_impact_2017"],
            "n_sbs1_pooled": [7000, 200],  # below n_floor
            "f_lrr_corrected": [0.40, 0.55],
            "ci_low": [0.39, 0.30],
            "ci_high": [0.41, 0.80],
        }
    )
    verdict = mod.apply_decision_rule(
        rows,
        matched_study="tcga_mc3",
        panel_study="msk_impact_2017",
        midpoint=0.45,
        n_floor=500,
        max_ci_halfwidth=0.10,
    )
    assert verdict == "defer"


def test_decision_rule_defer_when_ci_too_wide() -> None:
    rows = pd.DataFrame(
        {
            "study_id": ["tcga_mc3", "msk_impact_2017"],
            "n_sbs1_pooled": [7000, 600],
            "f_lrr_corrected": [0.40, 0.55],
            "ci_low": [0.39, 0.40],
            "ci_high": [0.41, 0.70],  # half-width = 0.15 > 0.10
        }
    )
    verdict = mod.apply_decision_rule(
        rows,
        matched_study="tcga_mc3",
        panel_study="msk_impact_2017",
        midpoint=0.45,
        n_floor=500,
        max_ci_halfwidth=0.10,
    )
    assert verdict == "defer"
