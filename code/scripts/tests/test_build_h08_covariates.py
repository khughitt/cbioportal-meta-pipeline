# science:code
# status: library
# science:end

import pandas as pd

from build_h08_covariates import _derive_smoking_covariates


def test_derive_smoking_covariates_maps_pancanatlas_text_labels() -> None:
    cov = pd.DataFrame(
        {
            "patient12": [
                "TCGA-AA-0001",
                "TCGA-AA-0002",
                "TCGA-AA-0003",
                "TCGA-AA-0004",
            ],
            "arm": ["LUAD", "LUAD", "LUSC", "LUAD"],
        }
    )
    smoking = pd.DataFrame(
        {
            "bcr_patient_barcode": [
                "TCGA-AA-0001",
                "TCGA-AA-0002",
                "TCGA-AA-0003",
                "TCGA-AA-0004",
            ],
            "tobacco_smoking_history": [
                "Lifelong Non-smoker",
                "Current smoker",
                "Current reformed smoker for > 15 years",
                "[Unknown]",
            ],
            "number_pack_years_smoked": [
                "[Not Available]",
                "12",
                "30",
                "[Not Available]",
            ],
        }
    )

    out = _derive_smoking_covariates(cov, smoking)

    assert pd.isna(out.loc[0, "pack_years"])
    assert out["pack_years"].tolist()[1:3] == [12.0, 30.0]
    assert out["ever_smoker"].tolist()[:3] == [0.0, 1.0, 1.0]
    assert out["pack_years_zero_never"].tolist()[:3] == [0.0, 12.0, 30.0]
    assert pd.isna(out.loc[3, "ever_smoker"])
    assert pd.isna(out.loc[3, "pack_years_zero_never"])


def test_derive_smoking_covariates_nulls_nonlung_rows() -> None:
    cov = pd.DataFrame(
        {
            "patient12": ["TCGA-AA-0001", "TCGA-AA-0002"],
            "arm": ["LUAD", "BRCA"],
        }
    )
    smoking = pd.DataFrame(
        {
            "bcr_patient_barcode": ["TCGA-AA-0001", "TCGA-AA-0002"],
            "tobacco_smoking_history": ["Current smoker", "Current smoker"],
            "number_pack_years_smoked": ["12", "40"],
        }
    )

    out = _derive_smoking_covariates(cov, smoking)

    assert out.loc[
        0, ["pack_years", "ever_smoker", "pack_years_zero_never"]
    ].tolist() == [
        12.0,
        1.0,
        12.0,
    ]
    assert (
        out.loc[1, ["pack_years", "ever_smoker", "pack_years_zero_never"]].isna().all()
    )
