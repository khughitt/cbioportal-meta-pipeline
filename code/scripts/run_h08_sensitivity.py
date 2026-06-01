# science:code
# status: workflow-owned
# science:end
"""h08 pre-acceptance + registered sensitivity variants (t199 WP3).

Runs the pre-registered checks that gate the FINAL H08a verdict (read in WP4), keeping the
primary-gate vs diagnostic-sensitivity distinction the pre-reg mandates:

1. **Permutation null** (pre-acceptance for a "too good" result, pre-reg §Suspicious-Result).
   For each confirmatory target, shuffle the covariate WITHIN tissue (frozen seed, n=1000),
   refit, and compare the observed signed standardized coefficient to the null. Most load-bearing
   for Arm C (rank-1, q≈0): if its effect does not exceed the null, the only primary-pass arm is
   unstable and the whole read weakens.

2. **Absolute-burden re-run** (compositional sensitivity / DIAGNOSTIC ONLY, pre-reg §Suspicious-
   Result). Re-ranks the target covariates using log(absolute per-signature burden) instead of the
   CLR coordinate. This is NOT a path to a primary PASS: CLR was frozen before ranks as the primary
   read (plan WP2). If absolute burden recovers A/B while CLR fails, that is reported as
   **basis-dependent recovery → pushes the interpretation toward [?]**, never converted to a primary
   pass. Recorded with `is_primary_gate=False`.

3. **Lung-pooling variant** (Arm B): per-histology (LUAD-only, LUSC-only) ranks vs the pooled
   primary — read directly from the WP2 grid (those per-tissue cells already exist).

4. **K±5 modules**: analytically moot here and documented rather than re-run — the two pooled
   confirmatory arms (B, C) EXCLUDE modules from their denominators, so module count cannot move
   their ranks; and Arm A's UV proxy sits at rank ~10/14 with coef≈0, far from top-3 regardless of
   ±5 module covariates. (Recorded in meta with the reasoning.)

FREEZE GUARD: re-reads `covariate_denominator.json` read-only and re-logs its SHA256 (must match
WP2's), so the sensitivity outputs are tied to the same frozen denominator.
"""

import hashlib
import json
import logging
import sys
from pathlib import Path

import click
import numpy as np
import pandas as pd
import yaml
from rich.console import Console

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_h08_association_scan import (  # noqa: E402
    ARM_B_STRATA,
    ARM_C_STRATA,
    CLR_PSEUDOCOUNT,
    TARGETS,
    _collapse,
    fit_cell,
)

console = Console()
logger = logging.getLogger("run_h08_sensitivity")
if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s %(name)s: %(message)s"
    )

N_PERMUTATIONS = 1000
PERMUTATION_SEED = 0  # frozen (= config random_seed); documented in meta


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def grouped_exposure(expo: pd.DataFrame, active: list[str]) -> pd.DataFrame:
    """Collapsed active-signature exposures (sample × parts) — shared basis for CLR and absolute."""
    cols = [s for s in active if s in expo.columns]
    sub = expo[cols].copy()
    sub.columns = [_collapse(c) for c in cols]
    return sub.T.groupby(level=0).sum().T


def transform_outcomes(grouped: pd.DataFrame, kind: str) -> pd.DataFrame:
    """`kind` = 'clr' (primary) or 'abs' (diagnostic log absolute burden)."""
    logv = np.log(grouped.to_numpy(dtype=float) + CLR_PSEUDOCOUNT)
    if kind == "clr":
        logv = logv - logv.mean(axis=1, keepdims=True)
    return pd.DataFrame(logv, index=grouped.index, columns=grouped.columns)


def build_frame(
    cov: pd.DataFrame,
    expo: pd.DataFrame,
    samples: list[str],
    active: list[str],
    kind: str,
) -> pd.DataFrame:
    out = transform_outcomes(grouped_exposure(expo.reindex(samples), active), kind)
    base = cov.set_index("sample_barcode15").reindex(samples).copy()
    base["treatment"] = base["treatment_exposed"].fillna(0.0)
    base["ancestry"] = base["ancestry"].fillna("Unknown")
    return base.join(out.add_prefix("y_"))


def rank_target(
    frame: pd.DataFrame, sig: str, ranked: list[str], adjust: list[str], target_cov: str
) -> dict:
    """Re-rank `ranked` covariates by |coef| against outcome y_<sig>; return the target's rank."""
    rows = []
    for c in ranked:
        ft = fit_cell(frame, f"y_{sig}", c, adjust)
        if ft is not None:
            rows.append(
                {
                    "covariate": c,
                    "abs_coef": abs(ft[1]),
                    "coef": ft[1],
                    "p": ft[2],
                    "n": ft[0],
                }
            )
    rdf = (
        pd.DataFrame(rows)
        .sort_values("abs_coef", ascending=False)
        .reset_index(drop=True)
    )
    if target_cov not in set(rdf["covariate"]):
        return {"rank": None, "denominator": len(rdf)}
    i = int(rdf.index[rdf["covariate"] == target_cov][0])
    r = rdf.iloc[i]
    return {
        "rank": i + 1,
        "denominator": len(rdf),
        "coef": round(float(r["coef"]), 4),
        "sign": "+" if r["coef"] > 0 else "-",
        "n": int(r["n"]),
        "pvalue": round(float(r["p"]), 6),
    }


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
    man_path = assoc / "covariate_denominator.json"
    manifest = json.loads(man_path.read_text())
    manifest_sha = _sha256(man_path)
    logger.info("frozen denominator manifest sha256=%s", manifest_sha)

    # FREEZE GUARD: WP3 consumes the WP2 grid, so the sensitivity results MUST be tied to the
    # exact frozen denominator WP2 ranked under. Fail loudly rather than silently mixing a grid
    # built on one denominator with sensitivity runs built on another (review finding #1).
    grid_meta_path = assoc / "h08_association_grid.meta.json"
    if not grid_meta_path.exists():
        logger.error(
            "WP2 meta %s missing — run the association scan first", grid_meta_path
        )
        sys.exit(2)
    wp2_sha = json.loads(grid_meta_path.read_text())["frozen_denominator_manifest"][
        "sha256"
    ]
    if wp2_sha != manifest_sha:
        logger.error(
            "denominator SHA mismatch: WP2 grid ranked under %s but current manifest is %s — "
            "the frozen denominator changed between WP2 and WP3; refusing to mix bases",
            wp2_sha,
            manifest_sha,
        )
        sys.exit(2)
    logger.info("denominator SHA matches WP2 grid (%s)", wp2_sha[:16])

    cov = pd.read_feather(assoc / "h08_covariates.feather")
    grid = pd.read_feather(assoc / "h08_association_grid.feather")
    h = pd.read_feather(
        out_dir
        / "studies"
        / "tcga_mc3"
        / "mut"
        / "signatures"
        / "restricted_assignment_per_sample.feather"
    )
    h = h.assign(b15=h["sample_name"].str.slice(0, 15))
    passing = h[h["passes_count_floor"]]
    expo = passing.pivot_table(
        index="b15", columns="signature", values="exposure", aggfunc="first"
    ).fillna(0.0)
    pass_b15 = set(expo.index)

    def stratum_samples(skey: str) -> tuple[list[str], list[str], list[str], list[str]]:
        """Return (samples, ranked_covariates, active_signatures, adjust) for a target stratum key."""
        if skey == "ARM_B_POOLED":
            strata, block, adjust = (
                ARM_B_STRATA,
                manifest["arm_b_pooled"],
                ["arm", "ancestry", "treatment"],
            )
        elif skey == "ARM_C_POOLED":
            strata, block, adjust = (
                ARM_C_STRATA,
                manifest["arm_c_pooled"],
                ["arm", "ancestry", "treatment"],
            )
        else:
            strata, block, adjust = (
                [skey],
                manifest["per_stratum"][skey],
                ["ancestry", "treatment"],
            )
        samples = [
            b for b in cov[cov["arm"].isin(strata)]["sample_barcode15"] if b in pass_b15
        ]
        return samples, block["ranked_covariates"], block["active_signatures"], adjust

    rng = np.random.default_rng(PERMUTATION_SEED)

    # ---------- (1) absolute-burden diagnostic + (2) permutation null, per target ----------
    sens_rows = []
    perm_rows = []
    for arm, (covar, sig, skey) in TARGETS.items():
        samples, ranked, active, adjust = stratum_samples(skey)
        # primary (CLR) target read from the WP2 grid
        cell = grid[
            (grid.stratum == skey) & (grid.signature == sig) & (grid.covariate == covar)
        ]
        clr_rank = int(cell["rank"].iloc[0]) if not cell.empty else None

        # (1) absolute-burden re-rank (DIAGNOSTIC ONLY)
        frame_abs = build_frame(cov, expo, samples, active, "abs")
        abs_res = rank_target(frame_abs, sig, ranked, adjust, covar)
        sens_rows.append(
            {
                "arm": arm,
                "covariate": covar,
                "signature": sig,
                "stratum": skey,
                "basis": "absolute_burden",
                "is_primary_gate": False,
                "clr_primary_rank": clr_rank,
                **abs_res,
            }
        )

        # (2) permutation null on the PRIMARY (CLR) effect: shuffle covariate within tissue
        frame_clr = build_frame(cov, expo, samples, active, "clr")
        obs = fit_cell(frame_clr, f"y_{sig}", covar, adjust)
        obs_coef = obs[1] if obs else np.nan
        df = (
            frame_clr[[f"y_{sig}", covar, *adjust]]
            .dropna(subset=[f"y_{sig}", covar])
            .copy()
        )
        null_abs = []
        arm_key = "arm" if skey in ("ARM_B_POOLED", "ARM_C_POOLED") else None
        for _ in range(N_PERMUTATIONS):
            shuffled = df.copy()
            if arm_key:  # shuffle covariate WITHIN tissue
                shuffled[covar] = shuffled.groupby(arm_key)[covar].transform(
                    lambda x: rng.permutation(x.to_numpy())
                )
            else:
                shuffled[covar] = rng.permutation(shuffled[covar].to_numpy())
            ft = fit_cell(shuffled, f"y_{sig}", covar, adjust)
            if ft is not None:
                null_abs.append(abs(ft[1]))
        null_abs = np.array(null_abs)
        # Unbiased permutation p-value: (#exceedances + 1) / (n + 1). Never reports a literal 0.0
        # for a finite null — a "too good" effect that no permutation reaches still floors at
        # 1/(n+1) ≈ 0.001, which is honest about the resolution of an n=1000 null (review finding #3).
        if len(null_abs) and np.isfinite(obs_coef):
            n_exceed = int((null_abs >= abs(obs_coef)).sum())
            p_perm = (n_exceed + 1) / (len(null_abs) + 1)
        else:
            n_exceed, p_perm = None, np.nan
        perm_rows.append(
            {
                "arm": arm,
                "covariate": covar,
                "signature": sig,
                "stratum": skey,
                "obs_coef": round(float(obs_coef), 4)
                if np.isfinite(obs_coef)
                else None,
                "null_p95_abs_coef": round(float(np.percentile(null_abs, 95)), 4)
                if len(null_abs)
                else None,
                "n_exceedances": n_exceed,
                "p_permutation": round(p_perm, 5) if np.isfinite(p_perm) else None,
                "n_permutations": int(len(null_abs)),
                "exceeds_null": bool(np.isfinite(p_perm) and p_perm < 0.05),
            }
        )

    # ---------- (3) lung-pooling variant: per-histology pack_years→SBS4 from the WP2 grid ----------
    lung_rows = []
    for st in ("ARM_B_POOLED", "LUAD", "LUSC"):
        c = grid[
            (grid.stratum == st)
            & (grid.signature == "SBS4")
            & (grid.covariate == "pack_years")
        ]
        if not c.empty:
            r = c.iloc[0]
            lung_rows.append(
                {
                    "variant": st,
                    "rank": int(r["rank"]),
                    "denominator": int(r["denominator_used"]),
                    "sign": r["sign"],
                    "coef_std": round(float(r["coef_std"]), 4),
                    "q_bh": round(float(r["q_bh"]), 5),
                    "pass": bool(
                        r["rank"] <= 3 and r["sign"] == "+" and r["q_bh"] < 0.05
                    ),
                }
            )

    pd.DataFrame(sens_rows).to_feather(assoc / "h08_sensitivity.feather")
    pd.DataFrame(perm_rows).to_feather(assoc / "h08_permutation_null.feather")
    pd.DataFrame(lung_rows).to_feather(assoc / "h08_lung_pooling.feather")

    meta = {
        "task": "t199",
        "stage": "WP3",
        "frozen_denominator_manifest_sha256": manifest_sha,
        "permutation": {
            "n": N_PERMUTATIONS,
            "seed": PERMUTATION_SEED,
            "within_tissue_shuffle": True,
        },
        "arbitration": "CLR is the frozen PRIMARY gate (WP2); absolute burden is a DIAGNOSTIC sensitivity "
        "check and cannot promote an arm to a primary PASS. Basis-dependent recovery (abs "
        "passes, CLR fails) pushes interpretation toward [?], not [+].",
        "k_plus_minus_5": {
            "rerun": False,
            "reasoning": "Moot here: arms B/C exclude NMF modules from their pooled denominators, so module "
            "count cannot change their ranks; Arm A's UV proxy is rank~10/14 with coef≈0, far "
            "from top-3 regardless of ±5 module covariates. No NMF re-fit performed.",
        },
        "absolute_burden_diagnostic": sens_rows,
        "permutation_null": perm_rows,
        "lung_pooling_variant": lung_rows,
        "frozen_apobec_set": {"strata": ARM_C_STRATA, "expanded_or_substituted": False},
    }
    (assoc / "h08_sensitivity.meta.json").write_text(
        json.dumps(meta, indent=2, default=str)
    )

    # ---------- report ----------
    console.print(f"  manifest sha256={manifest_sha[:16]}…  (must match WP2)")
    console.print("[bold]Permutation null (within-tissue shuffle, n=1000):[/]")
    for r in perm_rows:
        console.print(
            f"  Arm cov={r['covariate']}→{r['signature']}: obs_coef={r['obs_coef']} "
            f"n_exceed={r['n_exceedances']}/{r['n_permutations']} p_perm={r['p_permutation']} "
            f"exceeds_null={r['exceeds_null']}"
        )
    console.print("[bold]Absolute-burden DIAGNOSTIC (not a primary pass):[/]")
    for r in sens_rows:
        console.print(
            f"  Arm {r['arm']} {r['covariate']}→{r['signature']}: CLR_rank={r['clr_primary_rank']} "
            f"→ abs_rank={r['rank']}/{r['denominator']} sign={r.get('sign')}"
        )
    console.print("[bold]Lung-pooling variant (Arm B):[/]")
    for r in lung_rows:
        console.print(
            f"  {r['variant']}: rank {r['rank']}/{r['denominator']} sign {r['sign']} q={r['q_bh']} pass={r['pass']}"
        )


if __name__ == "__main__":
    main()
