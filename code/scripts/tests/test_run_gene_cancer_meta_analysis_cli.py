"""CLI tests for the t077 R meta-analysis runner skeleton."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "code" / "scripts" / "run_gene_cancer_meta_analysis.R"
ENV_FILE = ROOT / "code" / "envs" / "r-meta.yml"


def _rscript_ready() -> bool:
    rscript = shutil.which("Rscript")
    if rscript is None:
        return False
    probe = subprocess.run(
        [rscript, "-e", 'suppressPackageStartupMessages(library(arrow)); cat("ok\\n")'],
        capture_output=True,
        text=True,
        check=False,
    )
    return probe.returncode == 0


def _metafor_ready() -> bool:
    rscript = shutil.which("Rscript")
    if rscript is None:
        return False
    probe = subprocess.run(
        [
            rscript,
            "-e",
            (
                'suppressPackageStartupMessages({library(arrow); library(metafor)}); '
                'cat("ok\\n")'
            ),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return probe.returncode == 0


def test_r_meta_env_declares_expected_packages() -> None:
    text = ENV_FILE.read_text()
    for expected in (
        "r-base>=4.3",
        "r-metafor",
        "r-arrow",
        "r-optparse",
        "r-matrix",
        "r-lme4",
    ):
        assert expected in text


@pytest.mark.skipif(not _rscript_ready(), reason="Rscript with arrow is unavailable")
def test_cli_writes_schema_valid_output_for_underpowered_cell(tmp_path: Path) -> None:
    pooled_input = pd.DataFrame(
        {
            "study_id": ["study_a", "study_b"],
            "cancer_type": ["BRCA", "BRCA"],
            "symbol": ["TP53", "TP53"],
            "y_inclusive": [10, 5],
            "y_exclusive": [8, 4],
            "n_inclusive": [100, 50],
            "n_exclusive": [80, 50],
            "panel_class": ["WES", "large_hybrid_capture"],
            "matched_normal": [True, False],
        }
    )
    input_path = tmp_path / "gene_cancer_pooled_input.feather"
    output_path = tmp_path / "gene_cancer_pooled.feather"
    pooled_input.to_feather(input_path)

    result = subprocess.run(
        [
            "Rscript",
            str(SCRIPT),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert output_path.exists()

    out = pd.read_feather(output_path)
    assert list(out.columns) == [
        "cancer_type",
        "symbol",
        "analysis_view",
        "pooled_logit",
        "pooled_rate",
        "pooled_ci_lo",
        "pooled_ci_hi",
        "tau2",
        "i2",
        "pi_lo",
        "pi_hi",
        "k_studies",
        "n_total",
        "y_total",
        "converged",
        "status",
    ]
    assert out["analysis_view"].tolist() == ["exclusive", "inclusive"]

    inclusive = out.loc[out["analysis_view"] == "inclusive"].iloc[0]
    exclusive = out.loc[out["analysis_view"] == "exclusive"].iloc[0]

    assert inclusive["k_studies"] == 2
    assert inclusive["n_total"] == 150
    assert inclusive["y_total"] == 15
    assert exclusive["n_total"] == 130
    assert exclusive["y_total"] == 12
    assert bool(inclusive["converged"]) is False
    assert bool(exclusive["converged"]) is False
    assert inclusive["status"] == "skipped_k"
    assert exclusive["status"] == "skipped_k"


@pytest.mark.skipif(not _rscript_ready(), reason="Rscript with arrow is unavailable")
def test_cli_requires_input_and_output_args(tmp_path: Path) -> None:
    pooled_input = pd.DataFrame(
        {
            "study_id": ["study_a"],
            "cancer_type": ["BRCA"],
            "symbol": ["TP53"],
            "y_inclusive": [10],
            "y_exclusive": [8],
            "n_inclusive": [100],
            "n_exclusive": [80],
            "panel_class": ["WES"],
            "matched_normal": [True],
        }
    )
    input_path = tmp_path / "gene_cancer_pooled_input.feather"
    pooled_input.to_feather(input_path)

    result = subprocess.run(
        ["Rscript", str(SCRIPT), "--input", str(input_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "--output" in result.stderr


@pytest.mark.skipif(not _metafor_ready(), reason="Rscript with arrow+metafor is unavailable")
def test_cli_fits_valid_cell_and_emits_ok_status(tmp_path: Path) -> None:
    pooled_input = pd.DataFrame(
        {
            "study_id": ["s1", "s2", "s3"],
            "cancer_type": ["BRCA", "BRCA", "BRCA"],
            "symbol": ["TP53", "TP53", "TP53"],
            "y_inclusive": [20, 15, 12],
            "y_exclusive": [18, 14, 10],
            "n_inclusive": [100, 80, 60],
            "n_exclusive": [90, 70, 55],
            "panel_class": ["WES", "large_hybrid_capture", "WES"],
            "matched_normal": [True, False, True],
        }
    )
    input_path = tmp_path / "gene_cancer_pooled_input.feather"
    output_path = tmp_path / "gene_cancer_pooled.feather"
    pooled_input.to_feather(input_path)

    result = subprocess.run(
        [
            "Rscript",
            str(SCRIPT),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    out = pd.read_feather(output_path)
    assert out["status"].tolist() == ["ok", "ok"]
    assert out["converged"].tolist() == [True, True]

    inclusive = out.loc[out["analysis_view"] == "inclusive"].iloc[0]
    assert inclusive["k_studies"] == 3
    assert inclusive["n_total"] == 240
    assert inclusive["y_total"] == 47
    assert inclusive["pooled_rate"] > 0
    assert inclusive["pooled_ci_lo"] <= inclusive["pooled_rate"] <= inclusive["pooled_ci_hi"]


@pytest.mark.skipif(not _metafor_ready(), reason="Rscript with arrow+metafor is unavailable")
def test_cli_marks_threshold_failures_with_registered_statuses(tmp_path: Path) -> None:
    pooled_input = pd.DataFrame(
        {
            "study_id": ["s1", "s2", "s1", "s2", "s3", "s1", "s2", "s3"],
            "cancer_type": [
                "BRCA",
                "BRCA",
                "LUAD",
                "LUAD",
                "LUAD",
                "COAD",
                "COAD",
                "COAD",
            ],
            "symbol": [
                "GENE_K",
                "GENE_K",
                "GENE_N",
                "GENE_N",
                "GENE_N",
                "GENE_Y",
                "GENE_Y",
                "GENE_Y",
            ],
            "y_inclusive": [10, 5, 1, 1, 1, 0, 0, 0],
            "y_exclusive": [8, 4, 1, 1, 1, 0, 0, 0],
            "n_inclusive": [100, 90, 60, 60, 60, 100, 100, 100],
            "n_exclusive": [90, 80, 55, 55, 55, 90, 90, 90],
            "panel_class": [
                "WES",
                "WES",
                "WES",
                "WES",
                "large_hybrid_capture",
                "WES",
                "large_hybrid_capture",
                "WES",
            ],
            "matched_normal": [True, False, True, False, True, True, False, True],
        }
    )
    input_path = tmp_path / "gene_cancer_pooled_input.feather"
    output_path = tmp_path / "gene_cancer_pooled.feather"
    pooled_input.to_feather(input_path)

    result = subprocess.run(
        [
            "Rscript",
            str(SCRIPT),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    out = pd.read_feather(output_path)

    status_map = {
        (row["cancer_type"], row["symbol"], row["analysis_view"]): row["status"]
        for _, row in out.iterrows()
    }
    assert status_map[("BRCA", "GENE_K", "inclusive")] == "skipped_k"
    assert status_map[("LUAD", "GENE_N", "inclusive")] == "skipped_n"
    assert status_map[("COAD", "GENE_Y", "inclusive")] == "skipped_y"


@pytest.mark.skipif(not _metafor_ready(), reason="Rscript with arrow+metafor is unavailable")
def test_cli_falls_back_to_reml_when_glmm_is_forced_to_fail(tmp_path: Path) -> None:
    pooled_input = pd.DataFrame(
        {
            "study_id": ["s1", "s2", "s3"],
            "cancer_type": ["BRCA", "BRCA", "BRCA"],
            "symbol": ["TP53", "TP53", "TP53"],
            "y_inclusive": [20, 15, 12],
            "y_exclusive": [18, 14, 10],
            "n_inclusive": [100, 80, 60],
            "n_exclusive": [90, 70, 55],
            "panel_class": ["WES", "large_hybrid_capture", "WES"],
            "matched_normal": [True, False, True],
        }
    )
    input_path = tmp_path / "gene_cancer_pooled_input.feather"
    output_path = tmp_path / "gene_cancer_pooled.feather"
    pooled_input.to_feather(input_path)

    result = subprocess.run(
        [
            "Rscript",
            str(SCRIPT),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--force-glmm-failure",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    out = pd.read_feather(output_path)
    assert "REML fallback" in result.stderr
    assert out["status"].tolist() == ["ok", "ok"]
    assert out["converged"].tolist() == [True, True]


@pytest.mark.skipif(not _metafor_ready(), reason="Rscript with arrow+metafor is unavailable")
def test_cli_writes_diagnostics_sidecar_and_empty_leave_one_out_when_not_ready(
    tmp_path: Path,
) -> None:
    pooled_input = pd.DataFrame(
        {
            "study_id": ["s1", "s2", "s3"],
            "cancer_type": ["BRCA", "BRCA", "BRCA"],
            "symbol": ["TP53", "TP53", "TP53"],
            "y_inclusive": [20, 15, 12],
            "y_exclusive": [18, 14, 10],
            "n_inclusive": [100, 80, 60],
            "n_exclusive": [90, 70, 55],
            "panel_class": ["WES", "large_hybrid_capture", "WES"],
            "matched_normal": [True, False, True],
        }
    )
    input_path = tmp_path / "gene_cancer_pooled_input.feather"
    output_path = tmp_path / "gene_cancer_pooled.feather"
    diagnostics_path = tmp_path / "gene_cancer_pooled_diagnostics.feather"
    leave_one_out_path = tmp_path / "gene_cancer_pooled_leave_one_out.feather"
    pooled_input.to_feather(input_path)

    result = subprocess.run(
        [
            "Rscript",
            str(SCRIPT),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--diagnostics-output",
            str(diagnostics_path),
            "--leave-one-out-output",
            str(leave_one_out_path),
            "--force-glmm-failure",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    diagnostics = pd.read_feather(diagnostics_path)
    assert list(diagnostics.columns) == [
        "cancer_type",
        "symbol",
        "analysis_view",
        "status",
        "method_used",
        "fallback_used",
        "glmm_error",
        "reml_error",
        "heterogeneity_state",
        "high_i2_threshold",
        "leave_one_out_candidate",
        "k_studies",
        "n_total",
        "y_total",
    ]
    assert diagnostics["method_used"].tolist() == ["reml_fallback", "reml_fallback"]
    assert diagnostics["fallback_used"].tolist() == [True, True]
    assert diagnostics["glmm_error"].notna().all()
    assert diagnostics["heterogeneity_state"].isin(
        ["high_i2", "not_high_i2", "not_evaluable"]
    ).all()
    assert diagnostics["leave_one_out_candidate"].tolist() == [False, False]

    leave_one_out = pd.read_feather(leave_one_out_path)
    assert list(leave_one_out.columns) == [
        "cancer_type",
        "symbol",
        "analysis_view",
        "excluded_study_id",
        "base_status",
        "holdout_status",
        "holdout_method_used",
        "holdout_k_studies",
        "holdout_n_total",
        "holdout_y_total",
        "holdout_pooled_rate",
        "holdout_ci_lo",
        "holdout_ci_hi",
        "holdout_i2",
    ]
    assert leave_one_out.empty


@pytest.mark.skipif(not _metafor_ready(), reason="Rscript with arrow+metafor is unavailable")
def test_cli_writes_leave_one_out_refits_for_holdout_ready_cells(tmp_path: Path) -> None:
    pooled_input = pd.DataFrame(
        {
            "study_id": ["s1", "s2", "s3", "s4"],
            "cancer_type": ["BRCA", "BRCA", "BRCA", "BRCA"],
            "symbol": ["TP53", "TP53", "TP53", "TP53"],
            "y_inclusive": [20, 15, 12, 18],
            "y_exclusive": [18, 14, 10, 16],
            "n_inclusive": [100, 80, 60, 90],
            "n_exclusive": [90, 70, 55, 85],
            "panel_class": ["WES", "large_hybrid_capture", "WES", "MC3"],
            "matched_normal": [True, False, True, True],
        }
    )
    input_path = tmp_path / "gene_cancer_pooled_input.feather"
    output_path = tmp_path / "gene_cancer_pooled.feather"
    diagnostics_path = tmp_path / "gene_cancer_pooled_diagnostics.feather"
    leave_one_out_path = tmp_path / "gene_cancer_pooled_leave_one_out.feather"
    pooled_input.to_feather(input_path)

    result = subprocess.run(
        [
            "Rscript",
            str(SCRIPT),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--diagnostics-output",
            str(diagnostics_path),
            "--leave-one-out-output",
            str(leave_one_out_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr

    diagnostics = pd.read_feather(diagnostics_path)
    assert diagnostics["leave_one_out_candidate"].tolist() == [True, True]

    leave_one_out = pd.read_feather(leave_one_out_path)
    assert len(leave_one_out) == 8
    assert set(leave_one_out["excluded_study_id"]) == {"s1", "s2", "s3", "s4"}
    assert set(leave_one_out["analysis_view"]) == {"inclusive", "exclusive"}
    assert set(leave_one_out["base_status"]) == {"ok"}
    assert set(leave_one_out["holdout_status"]) <= {"ok", "nonconverged"}
    assert (leave_one_out["holdout_k_studies"] == 3).all()


@pytest.mark.skipif(not _metafor_ready(), reason="Rscript with arrow+metafor is unavailable")
def test_cli_pooled_output_depends_on_study_covariate_assignment(tmp_path: Path) -> None:
    base = pd.DataFrame(
        {
            "study_id": ["s1", "s2", "s3", "s4", "s5", "s6"],
            "cancer_type": ["BRCA"] * 6,
            "symbol": ["TP53"] * 6,
            "y_inclusive": [4, 6, 26, 29, 12, 14],
            "y_exclusive": [4, 5, 24, 27, 11, 13],
            "n_inclusive": [100, 100, 100, 100, 100, 100],
            "n_exclusive": [100, 100, 100, 100, 100, 100],
            "panel_class": [
                "WES",
                "WES",
                "MC3",
                "MC3",
                "large_hybrid_capture",
                "large_hybrid_capture",
            ],
            "matched_normal": [True, False, True, False, True, False],
        }
    )
    shuffled = base.copy()
    shuffled["panel_class"] = [
        "MC3",
        "large_hybrid_capture",
        "WES",
        "MC3",
        "WES",
        "large_hybrid_capture",
    ]
    shuffled["matched_normal"] = [False, True, False, True, True, False]

    base_input = tmp_path / "base_input.feather"
    shuffled_input = tmp_path / "shuffled_input.feather"
    base_output = tmp_path / "base_output.feather"
    shuffled_output = tmp_path / "shuffled_output.feather"
    base.to_feather(base_input)
    shuffled.to_feather(shuffled_input)

    base_result = subprocess.run(
        [
            "Rscript",
            str(SCRIPT),
            "--input",
            str(base_input),
            "--output",
            str(base_output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    shuffled_result = subprocess.run(
        [
            "Rscript",
            str(SCRIPT),
            "--input",
            str(shuffled_input),
            "--output",
            str(shuffled_output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert base_result.returncode == 0, base_result.stderr
    assert shuffled_result.returncode == 0, shuffled_result.stderr

    base_out = pd.read_feather(base_output)
    shuffled_out = pd.read_feather(shuffled_output)
    merged = base_out.merge(
        shuffled_out,
        on=["cancer_type", "symbol", "analysis_view"],
        suffixes=("_base", "_shuffled"),
    )

    assert (merged["status_base"] == "ok").all()
    assert (merged["status_shuffled"] == "ok").all()
    assert (
        (merged["pooled_rate_base"] - merged["pooled_rate_shuffled"]).abs() > 1e-6
    ).any()
