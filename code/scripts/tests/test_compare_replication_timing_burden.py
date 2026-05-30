# science:code
# status: library
# science:end
from pathlib import Path

import pandas as pd

import compare_replication_timing_burden as rt


def test_build_symbol_rt_map_prefers_primary_chromosomes_and_collapses_bp() -> None:
    genes = pd.DataFrame(
        {
            "symbol": ["GENE1", "GENE1", "GENE2", "GENE3", "GENE3"],
            "chr": ["1", "HG79_PATCH", "2", "3", "3"],
            "biotype": ["protein_coding"] * 5,
            "rt_ce_bp": [100, 0, 0, 40, 40],
            "rt_cl_bp": [0, 0, 120, 40, 40],
        }
    )

    out = rt.build_symbol_rt_map(genes)

    assert out.to_dict(orient="records") == [
        {
            "symbol": "GENE1",
            "rt_ce_bp": 100,
            "rt_cl_bp": 0,
            "rt_constitutive_label": "CE",
        },
        {
            "symbol": "GENE2",
            "rt_ce_bp": 0,
            "rt_cl_bp": 120,
            "rt_constitutive_label": "CL",
        },
        {
            "symbol": "GENE3",
            "rt_ce_bp": 80,
            "rt_cl_bp": 80,
            "rt_constitutive_label": "mixed",
        },
    ]


def test_build_sample_rt_burden_table_uses_assignment_samples_and_primary_labels() -> None:
    symbol_rt = pd.DataFrame(
        {
            "symbol": ["CE1", "CL1", "MIX1"],
            "rt_ce_bp": [100, 0, 50],
            "rt_cl_bp": [0, 120, 50],
            "rt_constitutive_label": ["CE", "CL", "mixed"],
        }
    )
    mutations = pd.DataFrame(
        {
            "symbol": ["CE1", "CL1", "MIX1", "CE1", "CL1", "CL1"],
            "sample_id_tumor": ["S1", "S1", "S1", "S2", "S2", "S3"],
        }
    )
    assignments = pd.DataFrame(
        {
            "study_id": ["tcga_mc3", "tcga_mc3", "tcga_mc3"],
            "lookup_key": ["breast", "breast", "lung"],
            "sample_name": ["S1", "S2", "S3"],
        }
    )

    out = rt.build_sample_rt_burden_table(
        study_id="tcga_mc3",
        mutations=mutations,
        assignments=assignments,
        symbol_rt=symbol_rt,
        ratio_pseudocount=0.5,
    )

    assert out[["study_id", "lookup_key", "sample_name", "CE", "CL"]].to_dict(orient="records") == [
        {"study_id": "tcga_mc3", "lookup_key": "breast", "sample_name": "S1", "CE": 1, "CL": 1},
        {"study_id": "tcga_mc3", "lookup_key": "breast", "sample_name": "S2", "CE": 1, "CL": 1},
        {"study_id": "tcga_mc3", "lookup_key": "lung", "sample_name": "S3", "CE": 0, "CL": 1},
    ]


def test_build_comparison_table_compares_matched_and_unmatched_rt_ratios() -> None:
    per_sample = pd.DataFrame(
        {
            "study_id": ["tcga_mc3"] * 4 + ["msk_impact_2017"] * 4,
            "lookup_key": ["breast"] * 8,
            "sample_name": ["T1", "T2", "T3", "T4", "M1", "M2", "M3", "M4"],
            "CE": [5, 4, 6, 5, 2, 2, 1, 2],
            "CL": [2, 1, 2, 1, 6, 5, 7, 6],
            "cl_ce_ratio": [0.4545, 0.3333, 0.3846, 0.2727, 2.6, 2.2, 5.0, 2.6],
            "log10_cl_ce_ratio": [-0.3424, -0.4771, -0.4150, -0.5643, 0.4150, 0.3424, 0.6990, 0.4150],
        }
    )

    comparison = rt.build_comparison_table(
        per_sample,
        matched_normal_studies={"tcga_mc3"},
        min_samples_per_group=4,
    )

    row = comparison.iloc[0]
    assert row["lookup_key"] == "breast"
    assert row["matched_study_id"] == "tcga_mc3"
    assert row["unmatched_study_id"] == "msk_impact_2017"
    assert row["median_cl_shift"] > 0
    assert row["median_log10_cl_ce_ratio_shift"] > 0
    assert row["observed_cl_direction"] == "unmatched_higher"
    assert row["observed_log10_cl_ce_ratio_direction"] == "unmatched_higher"
    assert row["unmatched_gt_matched_cl_pvalue"] < 0.05
    assert row["unmatched_gt_matched_log10_cl_ce_ratio_pvalue"] < 0.05


def test_load_assignment_inputs_concatenates_pairs(tmp_path: Path) -> None:
    first_mut = tmp_path / "first_mut.feather"
    first_assign = tmp_path / "first_assign.feather"
    second_mut = tmp_path / "second_mut.feather"
    second_assign = tmp_path / "second_assign.feather"

    pd.DataFrame({"symbol": ["CE1"], "sample_id_tumor": ["S1"]}).to_feather(first_mut)
    pd.DataFrame({"study_id": ["a"], "lookup_key": ["breast"], "sample_name": ["S1"]}).to_feather(first_assign)
    pd.DataFrame({"symbol": ["CL1"], "sample_id_tumor": ["S2"]}).to_feather(second_mut)
    pd.DataFrame({"study_id": ["b"], "lookup_key": ["breast"], "sample_name": ["S2"]}).to_feather(second_assign)

    out = rt.load_assignment_inputs(
        [
            {"study_id": "a", "mutations": first_mut, "assignments": first_assign},
            {"study_id": "b", "mutations": second_mut, "assignments": second_assign},
        ],
        symbol_rt=pd.DataFrame(
            {
                "symbol": ["CE1", "CL1"],
                "rt_ce_bp": [100, 0],
                "rt_cl_bp": [0, 100],
                "rt_constitutive_label": ["CE", "CL"],
            }
        ),
        ratio_pseudocount=0.5,
    )

    assert out["study_id"].tolist() == ["a", "b"]
