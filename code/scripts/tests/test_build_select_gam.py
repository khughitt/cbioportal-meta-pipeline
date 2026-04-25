"""Unit tests for build_select_gam -- core B-tier path."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

import build_select_gam as mod
import select_lib as lib


@pytest.fixture
def fixture_studies(tmp_path: Path):
    """Two-study fixture: 60 LUAD samples (30 per study), 5 genes, single panel."""
    rows = []
    for sid, prefix in [("st1", "A"), ("st2", "B")]:
        for i in range(30):
            sample_id = f"{prefix}{i:02d}"
            rows.append(
                {
                    "study_id": sid,
                    "sample_id": sample_id,
                    "composite_sample_id": lib.composite_sample_id(sid, sample_id),
                    "cancer_type": "luad",
                    "is_hypermutator": False,
                }
            )
    samples = pd.DataFrame(rows)

    rng = pd.RangeIndex(len(samples))
    mut = pd.DataFrame(
        {
            "composite_sample_id": samples["composite_sample_id"],
            "TP53": rng.map(lambda i: i % 2 == 0),
            "KRAS": rng.map(lambda i: i % 3 == 0),
            "EGFR": rng.map(lambda i: i % 4 == 0),
            "BRAF": rng.map(lambda i: i % 5 == 0),
            # MYC kept above the prevalence floor so >=5 genes survive (the n_genes<5
            # short-circuit is exercised separately in test_b_cell_below_stratum_threshold).
            "MYC": rng.map(lambda i: i % 2 == 1),
            "ZZTOPLOWFREQ": [False] * (len(samples) - 1)
            + [True],  # mutated in 1 sample
        }
    )

    panel_map = pd.DataFrame(
        {
            "study_id": samples["study_id"],
            "sample_id": samples["sample_id"],
            "panel_id": ["panel_x"] * len(samples),
            "panel_source": ["study_panels_tsv"] * len(samples),
        }
    )
    panel_genes = pd.DataFrame(
        {
            "symbol": ["TP53", "KRAS", "EGFR", "BRAF", "MYC", "ZZTOPLOWFREQ"],
            "callable": [True] * 6,
            "panel_id": ["panel_x"] * 6,
            "source": ["bed"] * 6,
        }
    )

    return samples, mut, panel_map, panel_genes


def test_build_b_inclusive_cell_basic_shape(tmp_path: Path, fixture_studies):
    samples, mut, panel_map, panel_genes = fixture_studies
    out = tmp_path / "cell"
    mod.build_b_tier_cell(
        cancer_type="luad",
        cohort="inclusive",
        samples=samples,
        mutation_long=_to_long(mut),
        sample_panel_map=panel_map,
        panel_gene_sets={"panel_x": panel_genes},
        gene_universe=pd.DataFrame(
            {
                "symbol": [
                    "TP53",
                    "KRAS",
                    "EGFR",
                    "BRAF",
                    "MYC",
                    "ZZTOPLOWFREQ",
                    "OTHER",
                ],
                "from_bailey": [True] * 7,
                "from_cgc": [False] * 7,
                "from_sanchez_vega": [False] * 7,
                "from_custom": [False] * 7,
            }
        ),
        ch_priority_genes=set(),
        sample_class_components=["study_id"],
        thresholds=mod.Thresholds(
            min_stratum_samples=30,
            min_gene_prevalence_frac=0.03,
            min_gene_prevalence_count=3,
            study_residual_threshold_frac=0.10,
        ),
        out_dir=out,
    )

    gam = pd.read_feather(out / "gam.feather")
    sc = pd.read_feather(out / "sample_class.feather")
    ac = pd.read_feather(out / "alteration_class.feather")
    meta = json.loads((out / "cell_metadata.json").read_text())

    # Orientation: rows = samples, cols = genes (design Section 1.2).
    assert gam.shape[0] == 60  # 60 samples
    # ZZTOPLOWFREQ mutated in 1 sample (<3 absolute count) -> dropped.
    assert "ZZTOPLOWFREQ" not in gam.columns
    # 5 surviving genes.
    assert sorted(c for c in gam.columns if c != "composite_sample_id") == [
        "BRAF",
        "EGFR",
        "KRAS",
        "MYC",
        "TP53",
    ]
    assert sc.shape[0] == 60
    assert ac.shape[0] == 5
    assert meta["skip_reason"] is None
    assert meta["n_samples"] == 60
    assert meta["n_genes"] == 5


def test_b_cell_below_stratum_threshold_writes_sentinel(
    tmp_path: Path, fixture_studies
):
    samples, mut, panel_map, panel_genes = fixture_studies
    samples_small = samples.head(20)  # below 30
    mut_long = _to_long(_subset(mut, samples_small))
    out = tmp_path / "cell_small"
    mod.build_b_tier_cell(
        cancer_type="luad",
        cohort="inclusive",
        samples=samples_small,
        mutation_long=mut_long,
        sample_panel_map=panel_map,
        panel_gene_sets={"panel_x": panel_genes},
        gene_universe=pd.DataFrame(
            {
                "symbol": ["TP53"],
                "from_bailey": [True],
                "from_cgc": [False],
                "from_sanchez_vega": [False],
                "from_custom": [False],
            }
        ),
        ch_priority_genes=set(),
        sample_class_components=["study_id"],
        thresholds=mod.Thresholds(
            min_stratum_samples=30,
            min_gene_prevalence_frac=0.03,
            min_gene_prevalence_count=3,
            study_residual_threshold_frac=0.10,
        ),
        out_dir=out,
    )

    meta = json.loads((out / "cell_metadata.json").read_text())
    assert meta["skip_reason"] == "n_samples_below_threshold"
    # Empty placeholder feathers must exist for DAG safety (Section 1.5).
    for fn in ["gam.feather", "sample_class.feather", "alteration_class.feather"]:
        assert (out / fn).exists()


def _to_long(wide: pd.DataFrame) -> pd.DataFrame:
    """Convert a wide (sample x gene) bool table to (composite_sample_id, gene) long."""
    long = wide.melt(
        id_vars=["composite_sample_id"], var_name="symbol", value_name="mutated"
    )
    return long[long["mutated"]][["composite_sample_id", "symbol"]].reset_index(
        drop=True
    )


def _subset(wide: pd.DataFrame, samples: pd.DataFrame) -> pd.DataFrame:
    return wide[wide["composite_sample_id"].isin(samples["composite_sample_id"])]
