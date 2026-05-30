# science:code
# status: library
# science:end
from __future__ import annotations

from pathlib import Path

from build_dndscv_loso_manifest import build_loso_manifest

# Arbitrary out_root for the path-string assertions below; relative so it does
# not trip the hardcoded-absolute-path check (no real I/O happens at this path).
OUT_ROOT = Path("pkg/pan-cancer-dndscv-loso")


def test_build_loso_manifest_excludes_one_study_per_row() -> None:
    manifest = build_loso_manifest(
        studies=["a", "b", "c"],
        config_path=Path("code/config/config-pan-cancer-dndscv.yml"),
        out_root=OUT_ROOT,
    )

    assert list(manifest["excluded_study_id"]) == ["a", "b", "c"]
    assert manifest.loc[0, "included_studies_json"] == '["b","c"]'
    assert manifest.loc[1, "included_studies_json"] == '["a","c"]'
    assert manifest.loc[2, "out_dir"] == str(OUT_ROOT / "exclude_c")


def test_build_loso_manifest_pilot_limits_to_requested_holdout() -> None:
    manifest = build_loso_manifest(
        studies=["a", "genie", "c"],
        config_path=Path("code/config/config-pan-cancer-dndscv.yml"),
        out_root=OUT_ROOT,
        pilot_study="genie",
    )

    assert list(manifest["excluded_study_id"]) == ["genie"]
    assert manifest.loc[0, "included_studies_json"] == '["a","c"]'


def test_build_loso_manifest_command_isolated_and_dry_run_ready() -> None:
    manifest = build_loso_manifest(
        studies=["a", "genie"],
        config_path=Path("code/config/config-pan-cancer-dndscv.yml"),
        out_root=OUT_ROOT,
        pilot_study="genie",
        jobs=4,
    )

    command = manifest.loc[0, "command"]
    dry_run_command = manifest.loc[0, "dry_run_command"]

    assert "uv run --frozen snakemake" in command
    assert "--configfile code/config/config-pan-cancer-dndscv.yml" in command
    assert f"out_dir={OUT_ROOT}/exclude_genie" in command
    assert """studies='["a"]'""" in command
    assert "/pan-cancer-dndscv " not in command
    assert "aggregate_dndscv_per_gene" in command
    assert "all_with_dndscv" not in command
    assert command.index("aggregate_dndscv_per_gene") < command.index(" --config ")
    assert dry_run_command.index("-n") < dry_run_command.index(
        "aggregate_dndscv_per_gene"
    )
    assert dry_run_command.index("aggregate_dndscv_per_gene") < dry_run_command.index(
        " --config "
    )
