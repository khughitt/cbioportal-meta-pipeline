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
