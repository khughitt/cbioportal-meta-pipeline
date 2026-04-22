from pathlib import Path

import pandas as pd

import prepare_replication_timing_annotations as rt


def test_clean_constitutive_rt_bins_filters_to_ce_and_cl() -> None:
    raw = pd.DataFrame(
        {
            "CHR": ["chr1", "chr1", "chr2", "chr2"],
            "Start": [0, 50_000, 0, 50_000],
            "End": [50_000, 100_000, 50_000, 100_000],
            "RTlabel": ["CE", "D", "CL", "N/a"],
            "GM12878_seq.RT": [0.8, 0.1, -0.7, -0.1],
        }
    )

    out = rt.clean_constitutive_rt_bins(raw)

    assert out.columns.tolist() == rt.RT_BINS_COLUMNS
    assert out.to_dict(orient="records") == [
        {
            "chromosome": "chr1",
            "start": 0,
            "end": 50_000,
            "rt_constitutive_label": "CE",
            "source": rt.RT_SOURCE,
        },
        {
            "chromosome": "chr2",
            "start": 0,
            "end": 50_000,
            "rt_constitutive_label": "CL",
            "source": rt.RT_SOURCE,
        },
    ]


def test_annotate_genes_with_constitutive_rt_uses_majority_overlap() -> None:
    bins = pd.DataFrame(
        {
            "chromosome": ["chr1", "chr1", "chr1"],
            "start": [0, 50, 100],
            "end": [50, 100, 150],
            "rt_constitutive_label": ["CE", "CL", "CL"],
            "source": [rt.RT_SOURCE] * 3,
        }
    )
    genes = pd.DataFrame(
        {
            "ensgene": ["E1", "E2", "E3", "E4"],
            "entrez": [1, 2, 3, 4],
            "symbol": ["G1", "G2", "G3", "G4"],
            "chr": ["1", "1", "1", "2"],
            "start": [0, 25, 0, 0],
            "end": [50, 125, 100, 40],
            "strand": [1, 1, 1, 1],
            "biotype": ["protein_coding"] * 4,
            "description": ["a", "b", "c", "d"],
        }
    )

    out = rt.annotate_genes_with_constitutive_rt(genes, bins)

    assert out.columns.tolist() == rt.GENE_RT_COLUMNS

    by_symbol = out.set_index("symbol")

    assert by_symbol.loc["G1", "rt_constitutive_label"] == "CE"
    assert by_symbol.loc["G1", "rt_ce_bp"] == 50
    assert by_symbol.loc["G1", "rt_cl_bp"] == 0
    assert by_symbol.loc["G1", "rt_ce_fraction"] == 1.0
    assert by_symbol.loc["G1", "rt_cl_fraction"] == 0.0
    assert by_symbol.loc["G1", "rt_assignment_method"] == "majority_constitutive_bp"

    assert by_symbol.loc["G2", "rt_constitutive_label"] == "CL"
    assert by_symbol.loc["G2", "rt_ce_bp"] == 25
    assert by_symbol.loc["G2", "rt_cl_bp"] == 75
    assert by_symbol.loc["G2", "rt_ce_fraction"] == 0.25
    assert by_symbol.loc["G2", "rt_cl_fraction"] == 0.75

    assert by_symbol.loc["G3", "rt_constitutive_label"] == "mixed"
    assert by_symbol.loc["G3", "rt_ce_bp"] == 50
    assert by_symbol.loc["G3", "rt_cl_bp"] == 50
    assert by_symbol.loc["G3", "rt_ce_fraction"] == 0.5
    assert by_symbol.loc["G3", "rt_cl_fraction"] == 0.5

    assert by_symbol.loc["G4", "rt_constitutive_label"] == "unassigned"
    assert by_symbol.loc["G4", "rt_constitutive_bp"] == 0
    assert pd.isna(by_symbol.loc["G4", "rt_ce_fraction"])
    assert pd.isna(by_symbol.loc["G4", "rt_cl_fraction"])
    assert by_symbol.loc["G4", "rt_assignment_method"] == "no_constitutive_overlap"


def test_read_rt_bins_xlsx_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "rt.xlsx"
    pd.DataFrame(
        {
            "CHR": ["chr1", "chr1"],
            "Start": [0, 50_000],
            "End": [50_000, 100_000],
            "RTlabel": ["CE", "CL"],
        }
    ).to_excel(path, index=False)

    out = rt.read_rt_bins(path)

    assert out["RTlabel"].tolist() == ["CE", "CL"]
