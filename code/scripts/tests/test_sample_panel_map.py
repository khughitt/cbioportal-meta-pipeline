# science:code
# status: library
# science:end
"""Tests for the sample_panel_map output of create_combined_sample_table."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

import create_combined_sample_table as mod


@pytest.fixture
def study_panels_tsv(tmp_path: Path):
    p = tmp_path / "study_panels.tsv"
    p.write_text(
        "study_id\tpanel_id\tsequencing_type\n"
        "brca_tcga\twes\twes\n"
        "msk_impact_2017\tmsk_impact_410\tpanel\n"
    )
    return p


@pytest.fixture
def per_study_samples(tmp_path: Path):
    """Two non-GENIE per-study samples feathers + one GENIE.

    Layout matches the real pipeline: studies/{id}/metadata/samples.feather.
    `study_id` is derived from the parent-of-parent directory name.
    """
    out = []
    for sid, samples in [
        ("brca_tcga", [("p1", "s1"), ("p2", "s2")]),
        ("msk_impact_2017", [("p3", "s3")]),
        ("genie_v9.1", [("g1", "GENIE-A"), ("g2", "GENIE-B")]),
    ]:
        df = pd.DataFrame(
            {
                "patient_id": [s[0] for s in samples],
                "sample_id": [s[1] for s in samples],
                "cancer_type": ["BRCA"] * len(samples),
                "cancer_type_detailed": ["BRCA"] * len(samples),
            }
        )
        d = tmp_path / "studies" / sid / "metadata"
        d.mkdir(parents=True, exist_ok=True)
        p = d / "samples.feather"
        df.to_feather(p)
        out.append(p)
    return out


@pytest.fixture
def genie_assay_table(tmp_path: Path):
    """Tiny GENIE per-sample assay map (clean schema)."""
    p = tmp_path / "genie_assay_table.tsv"
    p.write_text(
        "study_id\tsample_id\tpanel_id\n"
        "genie_v9.1\tGENIE-A\tmsk_impact_410\n"
        "genie_v9.1\tGENIE-B\tfoundation_one_cdx\n"
    )
    return p


def test_sample_panel_map_covers_all_samples_non_genie(
    tmp_path: Path, per_study_samples, study_panels_tsv, genie_assay_table
):
    out = tmp_path / "sample_panel_map.feather"
    mod.build_sample_panel_map(
        per_study_samples_paths=per_study_samples,
        study_panels_tsv=study_panels_tsv,
        genie_assay_table=genie_assay_table,
        out_path=out,
    )
    df = pd.read_feather(out)
    # 3 non-GENIE samples + 2 GENIE samples = 5 rows.
    assert len(df) == 5
    assert set(df.columns) >= {"study_id", "sample_id", "panel_id", "panel_source"}
    # WES study mapped to 'wes' with source 'wes_default'.
    brca = df[df["study_id"] == "brca_tcga"]
    assert (brca["panel_id"] == "wes").all()
    assert (brca["panel_source"] == "wes_default").all()
    # Panel study mapped from study_panels_tsv.
    msk = df[df["study_id"] == "msk_impact_2017"]
    assert (msk["panel_id"] == "msk_impact_410").all()
    assert (msk["panel_source"] == "study_panels_tsv").all()


def test_sample_panel_map_uses_genie_assay_table_for_genie_samples(
    tmp_path: Path, per_study_samples, study_panels_tsv, genie_assay_table
):
    out = tmp_path / "sample_panel_map.feather"
    mod.build_sample_panel_map(
        per_study_samples_paths=per_study_samples,
        study_panels_tsv=study_panels_tsv,
        genie_assay_table=genie_assay_table,
        out_path=out,
    )
    df = pd.read_feather(out)
    a = df[(df["study_id"] == "genie_v9.1") & (df["sample_id"] == "GENIE-A")].iloc[0]
    b = df[(df["study_id"] == "genie_v9.1") & (df["sample_id"] == "GENIE-B")].iloc[0]
    assert a["panel_id"] == "msk_impact_410"
    assert a["panel_source"] == "genie_assay_table"
    assert b["panel_id"] == "foundation_one_cdx"
    assert b["panel_source"] == "genie_assay_table"


def test_sample_panel_map_unmapped_study_raises(
    tmp_path: Path, study_panels_tsv, genie_assay_table
):
    """A non-GENIE study not in study_panels.tsv must fail."""
    rogue_df = pd.DataFrame(
        {
            "patient_id": ["p1"],
            "sample_id": ["s1"],
            "cancer_type": ["BRCA"],
            "cancer_type_detailed": ["BRCA"],
        }
    )
    rogue_dir = tmp_path / "studies" / "unknown_study" / "metadata"
    rogue_dir.mkdir(parents=True, exist_ok=True)
    rogue_path = rogue_dir / "samples.feather"
    rogue_df.to_feather(rogue_path)
    out = tmp_path / "out.feather"
    with pytest.raises(KeyError, match="unknown_study"):
        mod.build_sample_panel_map(
            per_study_samples_paths=[rogue_path],
            study_panels_tsv=study_panels_tsv,
            genie_assay_table=genie_assay_table,
            out_path=out,
        )


def test_sample_panel_map_parses_cbioportal_genie_clinical_format(
    tmp_path: Path, per_study_samples, study_panels_tsv
):
    """The GENIE clinical sample file (cBioPortal MAF-like header) is recognised.

    Real input is /data/raw/cbioportal/genie/data_clinical_sample.txt, which has
    4 metadata header rows starting with '#' before the actual data.
    """
    p = tmp_path / "data_clinical_sample.txt"
    p.write_text(
        "#Patient Identifier\tSample Identifier\tSequence Assay ID\tOncotree Code\n"
        "#desc1\tdesc2\tdesc3\tdesc4\n"
        "#STRING\tSTRING\tSTRING\tSTRING\n"
        "#1\t1\t1\t1\n"
        "PATIENT_ID\tSAMPLE_ID\tSEQ_ASSAY_ID\tONCOTREE_CODE\n"
        "GENIE-PT-A\tGENIE-A\tMSK-IMPACT410\tBRCA\n"
        "GENIE-PT-B\tGENIE-B\tDFCI-ONCOPANEL-3\tBRCA\n"
    )
    out = tmp_path / "sample_panel_map.feather"
    mod.build_sample_panel_map(
        per_study_samples_paths=per_study_samples,
        study_panels_tsv=study_panels_tsv,
        genie_assay_table=p,
        out_path=out,
    )
    df = pd.read_feather(out)
    a = df[(df["study_id"] == "genie_v9.1") & (df["sample_id"] == "GENIE-A")].iloc[0]
    assert a["panel_id"] == "MSK-IMPACT410"
    assert a["panel_source"] == "genie_assay_table"
