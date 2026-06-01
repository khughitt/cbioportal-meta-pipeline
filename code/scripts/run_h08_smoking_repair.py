# science:code
# status: workflow-owned
# science:end
"""Repaired h08 Arm-B smoking positive-control rerun.

This is the production rerun committed in `pre-registration:h08-smoking-repair`.
It derives a repair-specific denominator from the locked t199 denominator manifest
without overwriting the original H08a artifacts.
"""

from __future__ import annotations

import hashlib
import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import click
import pandas as pd
import statsmodels
import yaml
from rich.console import Console

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_h08_association_scan import (  # noqa: E402
    ARM_B_STRATA,
    build_stratum,
    fit_cell,
)

console = Console()
logger = logging.getLogger("run_h08_smoking_repair")
if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s %(name)s: %(message)s"
    )

PRIMARY_MIN_N = 700
PRIMARY_COVARIATE = "ever_smoker"
ORIGINAL_COVARIATE = "pack_years"
ZERO_NEVER_COVARIATE = "pack_years_zero_never"
TARGET_SIGNATURE = "SBS4"
PRIMARY_STRATUM = "ARM_B_POOLED"
REPAIR_SUBDIR = Path("association") / "repairs" / "smoking_arm"


@dataclass(frozen=True)
class RepairCell:
    n: int
    coef_std: float
    q_bh: float
    rank: int


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_ranked_covariate(
    ranked: list[str], *, original: str, replacement: str
) -> list[str]:
    if ranked.count(original) != 1:
        raise ValueError(f"ranked set must contain exactly one {original!r}")
    if replacement in ranked:
        raise ValueError(f"ranked set already contains replacement {replacement!r}")
    return [replacement if covariate == original else covariate for covariate in ranked]


def apply_bh(grid: pd.DataFrame) -> pd.DataFrame:
    if grid.empty:
        return grid.assign(q_bh=pd.Series(dtype=float))
    out = grid.copy()
    ordered = out.sort_values("pvalue", ascending=True).copy()
    ordered["_rank_p"] = range(1, len(ordered) + 1)
    ordered["q_bh"] = (ordered["pvalue"] * len(ordered) / ordered["_rank_p"]).clip(
        upper=1.0
    )
    ordered["q_bh"] = ordered["q_bh"][::-1].cummin()[::-1]
    return ordered.drop(columns="_rank_p").sort_index()


def repair_verdict(cell: RepairCell | None) -> str:
    if cell is None:
        return "-"
    if cell.coef_std <= 0:
        return "-"
    if cell.n < PRIMARY_MIN_N:
        return "?"
    if cell.q_bh >= 0.05 or cell.rank > 3:
        return "?"
    return "+"


def _exposure_wide(out_dir: Path) -> tuple[pd.DataFrame, set[str], dict[str, int]]:
    h_path = (
        out_dir
        / "studies"
        / "tcga_mc3"
        / "mut"
        / "signatures"
        / "restricted_assignment_per_sample.feather"
    )
    h = pd.read_feather(h_path)
    h = h.assign(b15=h["sample_name"].astype(str).str.slice(0, 15))
    passing = h[h["passes_count_floor"]]
    expo_wide = passing.pivot_table(
        index="b15", columns="signature", values="exposure", aggfunc="first"
    ).fillna(0.0)
    pass_b15 = set(expo_wide.index)
    counts = {
        arm: int(len(set(h[h["cancer_type"] == arm]["b15"]) & pass_b15))
        for arm in ARM_B_STRATA
    }
    return expo_wide, pass_b15, counts


def _fit_family(
    *,
    cov: pd.DataFrame,
    expo_wide: pd.DataFrame,
    samples: list[str],
    active_signatures: list[str],
    ranked_covariates: list[str],
    adjust: list[str],
    family: str,
    stratum: str,
) -> pd.DataFrame:
    frame = build_stratum(cov, expo_wide, samples, active_signatures)
    rows: list[dict[str, Any]] = []
    for covariate in ranked_covariates:
        fit = fit_cell(frame, f"clr_{TARGET_SIGNATURE}", covariate, adjust)
        if fit is None:
            continue
        n, coef, pvalue = fit
        rows.append(
            {
                "family": family,
                "stratum": stratum,
                "signature": TARGET_SIGNATURE,
                "covariate": covariate,
                "n": n,
                "coef_std": coef,
                "sign": "+" if coef > 0 else "-",
                "abs_coef": abs(coef),
                "pvalue": pvalue,
            }
        )
    if not rows:
        return pd.DataFrame(
            columns=[
                "family",
                "stratum",
                "signature",
                "covariate",
                "n",
                "coef_std",
                "sign",
                "abs_coef",
                "pvalue",
                "q_bh",
                "rank",
                "denominator_used",
            ]
        )
    grid = apply_bh(pd.DataFrame(rows))
    grid["rank"] = grid["abs_coef"].rank(ascending=False, method="min").astype(int)
    grid["denominator_used"] = len(grid)
    return grid


def _primary_cell(grid: pd.DataFrame, covariate: str) -> RepairCell | None:
    cell = grid[grid["covariate"] == covariate]
    if cell.empty:
        return None
    row = cell.iloc[0]
    return RepairCell(
        n=int(row["n"]),
        coef_std=float(row["coef_std"]),
        q_bh=float(row["q_bh"]),
        rank=int(row["rank"]),
    )


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


@click.command()
@click.option(
    "--config",
    "config_path",
    type=click.Path(path_type=Path, exists=True),
    required=True,
)
def main(config_path: Path) -> None:
    cfg = yaml.safe_load(config_path.read_text())
    out_dir = Path(cfg["out_dir"])
    assoc = out_dir / "association"
    repair_dir = out_dir / REPAIR_SUBDIR
    repair_dir.mkdir(parents=True, exist_ok=True)

    man_path = assoc / "covariate_denominator.json"
    cov_path = assoc / "h08_covariates.feather"
    for path in (man_path, cov_path):
        if not path.exists():
            raise SystemExit(f"smoking repair requires existing h08 artifact: {path}")

    manifest = _read_json(man_path)
    manifest_sha = sha256(man_path)
    cov = pd.read_feather(cov_path)
    expo_wide, pass_b15, count_floor_passing = _exposure_wide(out_dir)

    arm_b = manifest["arm_b_pooled"]
    primary_ranked = replace_ranked_covariate(
        list(arm_b["ranked_covariates"]),
        original=ORIGINAL_COVARIATE,
        replacement=PRIMARY_COVARIATE,
    )
    pooled_samples = [
        sample
        for sample in cov[cov["arm"].isin(ARM_B_STRATA)]["sample_barcode15"]
        if sample in pass_b15
    ]
    primary_grid = _fit_family(
        cov=cov,
        expo_wide=expo_wide,
        samples=pooled_samples,
        active_signatures=arm_b["active_signatures"],
        ranked_covariates=primary_ranked,
        adjust=["arm", "ancestry", "treatment"],
        family="primary_ever_smoker",
        stratum=PRIMARY_STRATUM,
    )

    sensitivity_frames = []
    for covariate in (ZERO_NEVER_COVARIATE, ORIGINAL_COVARIATE):
        ranked = (
            list(arm_b["ranked_covariates"])
            if covariate == ORIGINAL_COVARIATE
            else replace_ranked_covariate(
                list(arm_b["ranked_covariates"]),
                original=ORIGINAL_COVARIATE,
                replacement=covariate,
            )
        )
        sensitivity_frames.append(
            _fit_family(
                cov=cov,
                expo_wide=expo_wide,
                samples=pooled_samples,
                active_signatures=arm_b["active_signatures"],
                ranked_covariates=ranked,
                adjust=["arm", "ancestry", "treatment"],
                family=f"pooled_{covariate}",
                stratum=PRIMARY_STRATUM,
            )
        )
    for arm in ARM_B_STRATA:
        meta = manifest["per_stratum"][arm]
        ranked = replace_ranked_covariate(
            list(meta["ranked_covariates"]),
            original=ORIGINAL_COVARIATE,
            replacement=PRIMARY_COVARIATE,
        )
        samples = [
            sample
            for sample in cov[cov["arm"] == arm]["sample_barcode15"]
            if sample in pass_b15
        ]
        sensitivity_frames.append(
            _fit_family(
                cov=cov,
                expo_wide=expo_wide,
                samples=samples,
                active_signatures=meta["active_signatures"],
                ranked_covariates=ranked,
                adjust=["ancestry", "treatment"],
                family=f"{arm.lower()}_ever_smoker",
                stratum=arm,
            )
        )

    sensitivity = (
        pd.concat(sensitivity_frames, ignore_index=True)
        if sensitivity_frames
        else pd.DataFrame()
    )
    primary_cell = _primary_cell(primary_grid, PRIMARY_COVARIATE)
    verdict = repair_verdict(primary_cell)

    primary_out = primary_grid.drop(columns=["abs_coef"], errors="ignore")
    sensitivity_out = sensitivity.drop(columns=["abs_coef"], errors="ignore")
    primary_out.to_feather(repair_dir / "h08_smoking_repair_grid.feather")
    sensitivity_out.to_feather(repair_dir / "h08_smoking_repair_sensitivity.feather")

    meta = {
        "task": "t204",
        "plan": "plan:2026-06-01-h08-smoking-repair-rerun",
        "pre_registration": "pre-registration:h08-smoking-repair",
        "source_denominator_manifest": {
            "path": str(man_path),
            "sha256": manifest_sha,
        },
        "derived_primary_denominator": {
            "stratum": PRIMARY_STRATUM,
            "signature": TARGET_SIGNATURE,
            "source_ranked_covariates": arm_b["ranked_covariates"],
            "repaired_ranked_covariates": primary_ranked,
            "n_testable_covariates": int(len(primary_grid)),
        },
        "count_floor_passing_lung": count_floor_passing,
        "primary_min_n": PRIMARY_MIN_N,
        "primary_cell": None if primary_cell is None else primary_cell.__dict__,
        "repair_verdict": verdict,
        "statsmodels_version": statsmodels.__version__,
        "note": "Repair verdict is local to repaired Arm-B recovery; locked H08a remains [?].",
    }
    (repair_dir / "h08_smoking_repair.meta.json").write_text(
        json.dumps(meta, indent=2, default=str)
    )

    console.print(
        f"[green]wrote[/] {repair_dir / 'h08_smoking_repair_grid.feather'} "
        f"({len(primary_grid)} primary cells)"
    )
    if primary_cell is None:
        console.print("[red]primary ever_smoker cell was not estimable[/]")
    else:
        console.print(
            f"  [bold]ever_smoker→SBS4[/] n={primary_cell.n} "
            f"rank={primary_cell.rank}/{len(primary_grid)} "
            f"coef={primary_cell.coef_std:.4g} q={primary_cell.q_bh:.4g} "
            f"repair_verdict={verdict}"
        )
    console.print("  [yellow]Locked t199 H08a verdict remains [?].[/]")


if __name__ == "__main__":
    main()
