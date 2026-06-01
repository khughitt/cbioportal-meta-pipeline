# science:code
# status: library
# science:end

import numpy as np
import pandas as pd

from diagnose_h08_within_tissue import (
    CANONICAL_PROLIFERATION_GENES,
    VENET_META_PCNA_GENES,
    compute_contrast_summary,
    derive_smoking_operationalizations,
    fit_diag,
    score_gene_set_expression,
)


def test_derive_smoking_operationalizations_maps_text_labels_and_zeroes_never_smokers() -> (
    None
):
    cov = pd.DataFrame(
        {
            "sample_barcode15": [
                "TCGA-AA-0001-01",
                "TCGA-AA-0002-01",
                "TCGA-AA-0003-01",
            ],
            "patient12": ["TCGA-AA-0001", "TCGA-AA-0002", "TCGA-AA-0003"],
            "arm": ["LUAD", "LUAD", "LUSC"],
            "pack_years": [np.nan, 12.0, np.nan],
        }
    )
    smoking = pd.DataFrame(
        {
            "bcr_patient_barcode": ["TCGA-AA-0001", "TCGA-AA-0002", "TCGA-AA-0003"],
            "tobacco_smoking_history": [
                "Lifelong Non-smoker",
                "Current smoker",
                "[Unknown]",
            ],
            "number_pack_years_smoked": ["[Not Available]", "12", "[Not Available]"],
        }
    )

    out, label_counts = derive_smoking_operationalizations(cov, smoking)

    assert out["ever_smoker_derived"].tolist()[:2] == [0.0, 1.0]
    assert pd.isna(out.loc[2, "ever_smoker_derived"])
    assert out["pack_years_zero_never"].tolist()[:2] == [0.0, 12.0]
    assert pd.isna(out.loc[2, "pack_years_zero_never"])
    assert (
        label_counts.loc[
            label_counts["tobacco_smoking_history"] == "Lifelong Non-smoker",
            "mapped_value",
        ].item()
        == 0.0
    )


def test_fit_diag_uses_all_column_dropna_and_numeric_adjustments() -> None:
    df = pd.DataFrame(
        {
            "y": [1.0, 2.0, 3.0, 4.0, 5.0],
            "x": [1.0, 2.0, 3.0, 4.0, 5.0],
            "burden": [5.0, 4.0, np.nan, 2.0, 1.0],
            "arm": ["A", "A", "B", "B", "B"],
        }
    )

    fit = fit_diag(
        df,
        "y",
        "x",
        categorical_adjust=["arm"],
        numeric_adjust=["burden"],
    )

    assert fit is not None
    assert fit["n"] == 4
    assert fit["coef_std"] > 0
    assert fit["condition_number"] > 0
    assert fit["formula"] == "_y ~ _z + _num_burden + C(arm)"


def test_fit_diag_skips_zero_variance_numeric_controls_after_dropna() -> None:
    df = pd.DataFrame(
        {
            "y": [1.0, 2.0, 3.0, 4.0],
            "x": [1.0, 2.0, 3.0, 4.0],
            "constant": [7.0, 7.0, 7.0, 7.0],
        }
    )

    fit = fit_diag(df, "y", "x", categorical_adjust=[], numeric_adjust=["constant"])

    assert fit is None


def test_compute_contrast_summary_uses_explicit_range_restriction_column_names() -> (
    None
):
    frame = pd.DataFrame(
        {
            "arm": ["LUAD", "LUAD", "LUSC", "LUSC"],
            "pack_years": [0.0, 20.0, 45.0, 55.0],
        }
    )

    out = compute_contrast_summary(
        frame,
        covariate="pack_years",
        stratum_col="arm",
        strata=["LUAD", "LUSC"],
    )

    expected = {
        "sd_raw_fit_frame",
        "iqr_raw_fit_frame",
        "sd_tissue_centered_fit_frame",
        "pooled_sd_tissue_centered_fit_frame",
        "range_restriction_ratio_tissue_centered",
    }
    assert expected.issubset(out.columns)
    assert set(out["stratum"]) == {"LUAD", "LUSC"}


def test_score_gene_set_expression_logs_requested_and_realized_genes() -> None:
    expr = pd.DataFrame(
        {
            "S1": [10.0, 4.0, 0.0],
            "S2": [20.0, 8.0, 0.0],
        },
        index=["MKI67", "PCNA", "NOT_A_MARKER"],
    )

    score, meta = score_gene_set_expression(
        expr,
        requested_genes=["MKI67", "PCNA", "TOP2A"],
        set_name="test_set",
    )

    assert len(VENET_META_PCNA_GENES) > 0
    assert len(CANONICAL_PROLIFERATION_GENES) > 0
    assert meta["requested_genes"] == ["MKI67", "PCNA", "TOP2A"]
    assert meta["realized_genes"] == ["MKI67", "PCNA"]
    assert meta["n_realized_genes"] == 2
    assert score.index.tolist() == ["S1", "S2"]
