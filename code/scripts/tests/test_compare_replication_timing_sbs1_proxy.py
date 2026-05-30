# science:code
# status: library
# science:end
from pathlib import Path

import pandas as pd

import compare_replication_timing_sbs1_proxy as rt_sbs1


def test_is_sbs1_proxy_mutation_requires_cpg_context() -> None:
    assert rt_sbs1.is_sbs1_proxy_mutation("C", "T", "aCg/aTg")
    assert rt_sbs1.is_sbs1_proxy_mutation("G", "A", "cGc/cAc")

    assert not rt_sbs1.is_sbs1_proxy_mutation("C", "T", "aCa/aTa")
    assert not rt_sbs1.is_sbs1_proxy_mutation("G", "A", "tGc/tAc")
    assert not rt_sbs1.is_sbs1_proxy_mutation("C", "A", "aCg/aAg")
    assert not rt_sbs1.is_sbs1_proxy_mutation("C", "T", ".")
    assert not rt_sbs1.is_sbs1_proxy_mutation("C", "T", None)


def test_build_sample_rt_burden_table_keeps_only_sbs1_proxy_mutations() -> None:
    symbol_rt = pd.DataFrame(
        {
            "symbol": ["CE1", "CL1"],
            "rt_ce_bp": [100, 0],
            "rt_cl_bp": [0, 120],
            "rt_constitutive_label": ["CE", "CL"],
        }
    )
    mutations = pd.DataFrame(
        {
            "symbol": ["CE1", "CE1", "CL1", "CL1", "CL1"],
            "sample_id_tumor": ["S1", "S1", "S1", "S2", "S2"],
            "reference_allele": ["C", "C", "G", "G", "G"],
            "tumor_seq_allele2": ["T", "T", "A", "A", "A"],
            "codons": ["aCg/aTg", "aCa/aTa", "cGc/cAc", "cGc/cAc", "tGc/tAc"],
        }
    )
    assignments = pd.DataFrame(
        {
            "study_id": ["tcga_mc3", "tcga_mc3", "tcga_mc3"],
            "lookup_key": ["breast", "breast", "breast"],
            "sample_name": ["S1", "S2", "S3"],
        }
    )

    out = rt_sbs1.build_sample_rt_burden_table(
        study_id="tcga_mc3",
        mutations=mutations,
        assignments=assignments,
        symbol_rt=symbol_rt,
        ratio_pseudocount=0.5,
    )

    assert out[["study_id", "lookup_key", "sample_name", "CE", "CL"]].to_dict(orient="records") == [
        {"study_id": "tcga_mc3", "lookup_key": "breast", "sample_name": "S1", "CE": 1, "CL": 1},
        {"study_id": "tcga_mc3", "lookup_key": "breast", "sample_name": "S2", "CE": 0, "CL": 1},
        {"study_id": "tcga_mc3", "lookup_key": "breast", "sample_name": "S3", "CE": 0, "CL": 0},
    ]


def test_load_assignment_inputs_filters_non_proxy_rows(tmp_path: Path) -> None:
    first_mut = tmp_path / "first_mut.feather"
    first_assign = tmp_path / "first_assign.feather"
    second_mut = tmp_path / "second_mut.feather"
    second_assign = tmp_path / "second_assign.feather"

    pd.DataFrame(
        {
            "symbol": ["CE1", "CE1"],
            "sample_id_tumor": ["S1", "S1"],
            "reference_allele": ["C", "C"],
            "tumor_seq_allele2": ["T", "T"],
            "codons": ["aCg/aTg", "aCa/aTa"],
        }
    ).to_feather(first_mut)
    pd.DataFrame({"study_id": ["a"], "lookup_key": ["breast"], "sample_name": ["S1"]}).to_feather(first_assign)
    pd.DataFrame(
        {
            "symbol": ["CL1"],
            "sample_id_tumor": ["S2"],
            "reference_allele": ["G"],
            "tumor_seq_allele2": ["A"],
            "codons": ["cGc/cAc"],
        }
    ).to_feather(second_mut)
    pd.DataFrame({"study_id": ["b"], "lookup_key": ["breast"], "sample_name": ["S2"]}).to_feather(second_assign)

    out = rt_sbs1.load_assignment_inputs(
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
    assert out["CE"].tolist() == [1, 0]
    assert out["CL"].tolist() == [0, 1]


def test_filter_to_sbs1_proxy_mutations_tolerates_missing_codon_annotations() -> None:
    mutations = pd.DataFrame(
        {
            "symbol": ["CE1", "CL1", "CL1"],
            "sample_id_tumor": ["S1", "S1", "S2"],
            "reference_allele": ["C", "G", "G"],
            "tumor_seq_allele2": ["T", "A", "A"],
            "codons": [None, "cGc/cAc", "."],
        }
    )

    out = rt_sbs1.filter_to_sbs1_proxy_mutations(mutations)

    assert out[["symbol", "sample_id_tumor", "codons"]].to_dict(orient="records") == [
        {"symbol": "CL1", "sample_id_tumor": "S1", "codons": "cGc/cAc"},
    ]
