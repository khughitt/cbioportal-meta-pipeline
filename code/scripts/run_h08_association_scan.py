# science:code
# status: workflow-owned
# science:end
"""h08 within-tissue covariate↔H association grid (t199 WP2).

Computes the H08a scan: for each (ranked covariate, signature, stratum), an adjusted within-tissue
model of the covariate against the CLR coordinate of the signature's per-sample exposure, then a
single BH-FDR pass over the full grid and a per-(stratum, signature) rank of every covariate. The
three confirmatory arms (A: UV→SBS7 in SKCM; B: smoking→SBS4 in LUAD+LUSC pooled; C: APOBEC3A/B→
SBS2/13 in the APOBEC-six pooled) are read at rank≤3 / positive / q<0.05 — but the FINAL verdict is
deferred to WP4 (after the WP3 permutation null + sensitivity re-runs); this stage records the raw
reads only.

FREEZE GUARD (per review + user instruction): `covariate_denominator.json` is treated as a READ-ONLY
input. This script never regenerates or infers it; it fails if absent and logs its SHA256 into the
WP2 meta sidecar, so the gitignored freeze artifact gets a durable fingerprint in the committed
record. The ranked covariate set + per-stratum/pooled denominators are taken verbatim from it.

Frozen rules applied (all from the manifest / pre-reg; none re-decided here):
- CLR (KD5): composition over the stratum's active signatures (collapsed to the pre-reg targets —
  SBS7 = ΣSBS7a-d, SBS2_13 = SBS2+SBS13), pseudocount 0.5 on active-signature zeros (sampling
  zeros); signatures below the 5% active rule are structural zeros excluded from the composition.
- Count floor (t179): the primary grid uses only `passes_count_floor` samples (trusted exposures);
  sub-floor counts are reported loudly per stratum, not silently dropped.
- Rank statistic (F4): signed standardized coefficient of the covariate of interest.
- Two/three denominators (F1): per-tissue arms include modules; pooled arms B/C exclude them.

Outputs:
- association/h08_association_grid.feather  — one row per (stratum, signature, covariate)
- association/h08_association_grid.meta.json — manifest sha256, target reads (pre-WP3), leakage
  guard, R1 unconditioned contrast, count-floor drops, provenance.
"""

import hashlib
import json
import logging
from pathlib import Path

import click
import numpy as np
import pandas as pd
import statsmodels
import statsmodels.formula.api as smf
from rich.console import Console

console = Console()
logger = logging.getLogger("run_h08_association_scan")
if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s %(name)s: %(message)s"
    )

CLR_PSEUDOCOUNT = 0.5
APOBEC3_GENES = (
    "APOBEC3A",
    "APOBEC3B",
    "APOBEC3C",
    "APOBEC3D",
    "APOBEC3F",
    "APOBEC3G",
    "APOBEC3H",
)

# signature sub-signature collapse → pre-reg-named targets (KD/WP1 frozen)
SIG_GROUP = {
    "SBS7a": "SBS7",
    "SBS7b": "SBS7",
    "SBS7c": "SBS7",
    "SBS7d": "SBS7",
    "SBS2": "SBS2_13",
    "SBS13": "SBS2_13",
}

# confirmatory targets: arm -> (covariate, target signature part, stratum key)
TARGETS = {
    "A": ("uv_sun_exposure_ordinal", "SBS7", "SKCM"),
    "B": ("pack_years", "SBS4", "ARM_B_POOLED"),
    "C": ("apobec3ab_joint", "SBS2_13", "ARM_C_POOLED"),
}
ARM_B_STRATA = ["LUAD", "LUSC"]
ARM_C_STRATA = ["BLCA", "BRCA", "CESC", "HNSC", "LUAD", "LUSC"]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _collapse(sig: str) -> str:
    return SIG_GROUP.get(sig, sig)


def clr_matrix(expo: pd.DataFrame, active: list[str]) -> pd.DataFrame:
    """CLR coordinates over the collapsed active-signature composition. `expo` is sample×signature."""
    cols = [s for s in active if s in expo.columns]
    sub = expo[cols].copy()
    # collapse sub-signatures to targets, summing exposures (column-wise group; pandas-2 safe)
    sub.columns = [_collapse(c) for c in cols]
    grouped = sub.T.groupby(level=0).sum().T
    vals = (
        grouped.to_numpy(dtype=float) + CLR_PSEUDOCOUNT
    )  # pseudocount on sampling zeros
    logv = np.log(vals)
    clr = logv - logv.mean(axis=1, keepdims=True)
    return pd.DataFrame(clr, index=grouped.index, columns=grouped.columns)


def fit_cell(
    df: pd.DataFrame, ycol: str, cov: str, adjust: list[str]
) -> tuple[int, float, float] | None:
    """One adjusted OLS. Returns (n, signed_standardized_coef, pvalue) or None if not estimable."""
    sub = df[[ycol, cov, *adjust]].dropna(subset=[ycol, cov]).copy()
    if sub[cov].nunique() < 2 or len(sub) < 20:
        return None
    sub["_z"] = (sub[cov] - sub[cov].mean()) / sub[cov].std(ddof=0)
    if not np.isfinite(sub["_z"]).all():
        return None
    terms = ["_z"]
    for a in adjust:
        s = sub[a]
        if a == "treatment":
            if s.fillna(0).nunique() >= 2:
                terms.append("treatment")
        elif s.nunique(dropna=True) >= 2:
            terms.append(f"C({a})")
    sub = sub.rename(columns={ycol: "_y"})
    formula = "_y ~ " + " + ".join(terms)
    try:
        res = smf.ols(formula, data=sub).fit()
    except Exception as exc:  # noqa: BLE001 — loud, then skip this cell
        logger.warning("fit failed (%s vs %s): %s", cov, ycol, exc)
        return None
    if "_z" not in res.params.index:
        return None
    return int(len(sub)), float(res.params["_z"]), float(res.pvalues["_z"])


def build_stratum(
    cov: pd.DataFrame, expo_wide: pd.DataFrame, samples: list[str], active: list[str]
) -> pd.DataFrame:
    """Modeling frame: covariates + adjustment + CLR outcomes, indexed by sample, for one stratum."""
    clr = clr_matrix(expo_wide.reindex(samples), active)
    base = cov.set_index("sample_barcode15").reindex(samples).copy()
    base["treatment"] = base["treatment_exposed"].fillna(0.0)
    base["ancestry"] = base["ancestry"].fillna("Unknown")
    frame = base.join(clr.add_prefix("clr_"))
    return frame


@click.command()
@click.option(
    "--config",
    "config_path",
    type=click.Path(path_type=Path, exists=True),
    required=True,
)
def main(config_path: Path) -> None:
    import yaml

    cfg = yaml.safe_load(config_path.read_text())
    out_dir = Path(cfg["out_dir"])
    assoc = out_dir / "association"
    man_path = assoc / "covariate_denominator.json"
    cov_path = assoc / "h08_covariates.feather"
    h_path = (
        out_dir
        / "studies"
        / "tcga_mc3"
        / "mut"
        / "signatures"
        / "restricted_assignment_per_sample.feather"
    )

    # --- FREEZE GUARD: manifest is read-only; fail if missing; fingerprint it ---
    for p in (man_path, cov_path, h_path):
        if not p.exists():
            raise SystemExit(
                f"WP2 requires WP1 artifact (read-only input) — missing: {p}"
            )
    manifest = json.loads(man_path.read_text())
    manifest_sha = _sha256(man_path)
    logger.info("frozen denominator manifest sha256=%s", manifest_sha)

    cov = pd.read_feather(cov_path)
    h = pd.read_feather(h_path)
    h = h.assign(b15=h["sample_name"].str.slice(0, 15))

    # count floor (t179): primary grid uses trusted (passing) exposures only
    floor_drop = {}
    passing = h[h["passes_count_floor"]]
    expo_wide = passing.pivot_table(
        index="b15", columns="signature", values="exposure", aggfunc="first"
    ).fillna(0.0)
    pass_b15 = set(expo_wide.index)
    for arm in cfg["h08_arm_studies"]:
        arm15 = set(h[h["cancer_type"] == arm]["b15"])
        floor_drop[arm] = {"total": len(arm15), "passing": len(arm15 & pass_b15)}

    # --- modeling strata: 7 per-tissue (modules incl) + arm-B pooled + arm-C pooled (modules excl) ---
    strata: list[dict] = []
    for arm, meta in manifest["per_stratum"].items():
        s = [b for b in cov[cov["arm"] == arm]["sample_barcode15"] if b in pass_b15]
        strata.append(
            {
                "key": arm,
                "kind": "per_tissue",
                "samples": s,
                "ranked": meta["ranked_covariates"],
                "active": meta["active_signatures"],
                "adjust": ["ancestry", "treatment"],
            }
        )
    for key, mblock, mstrata in [
        ("ARM_B_POOLED", manifest["arm_b_pooled"], ARM_B_STRATA),
        ("ARM_C_POOLED", manifest["arm_c_pooled"], ARM_C_STRATA),
    ]:
        s = [
            b
            for b in cov[cov["arm"].isin(mstrata)]["sample_barcode15"]
            if b in pass_b15
        ]
        strata.append(
            {
                "key": key,
                "kind": "pooled",
                "samples": s,
                "ranked": mblock["ranked_covariates"],
                "active": mblock["active_signatures"],
                "adjust": ["arm", "ancestry", "treatment"],
            }
        )

    # --- the grid ---
    rows = []
    for st in strata:
        frame = build_stratum(cov, expo_wide, st["samples"], st["active"])
        sig_parts = [c[4:] for c in frame.columns if c.startswith("clr_")]
        for sig in sig_parts:
            for c in st["ranked"]:
                fit = fit_cell(frame, f"clr_{sig}", c, st["adjust"])
                if fit is None:
                    continue
                n, coef, p = fit
                rows.append(
                    {
                        "stratum": st["key"],
                        "stratum_kind": st["kind"],
                        "signature": sig,
                        "covariate": c,
                        "n": n,
                        "coef_std": coef,
                        "sign": "+" if coef > 0 else "-",
                        "abs_coef": abs(coef),
                        "pvalue": p,
                    }
                )
    grid = pd.DataFrame(rows)

    # BH-FDR over the full family
    m = len(grid)
    order = grid["pvalue"].rank(method="first").astype(int)
    grid = grid.assign(_rank_p=order)
    grid["q_bh"] = (grid["pvalue"] * m / grid["_rank_p"]).clip(upper=1.0)
    grid["q_bh"] = (
        grid.sort_values("pvalue", ascending=False)["q_bh"].cummin().reindex(grid.index)
    )
    grid = grid.drop(columns="_rank_p")

    # per-(stratum, signature) rank by |coef|
    grid["rank"] = (
        grid.groupby(["stratum", "signature"])["abs_coef"]
        .rank(ascending=False, method="min")
        .astype(int)
    )
    grid["denominator_used"] = grid.groupby(["stratum", "signature"])[
        "covariate"
    ].transform("size")

    # --- confirmatory target reads (PRE-WP3: not the final verdict) ---
    targets_out = {}
    for arm, (covar, sig, skey) in TARGETS.items():
        cell = grid[
            (grid["stratum"] == skey)
            & (grid["signature"] == sig)
            & (grid["covariate"] == covar)
        ]
        if cell.empty:
            targets_out[arm] = {
                "covariate": covar,
                "signature": sig,
                "stratum": skey,
                "status": "no cell (covariate not estimable?)",
            }
            continue
        r = cell.iloc[0]
        targets_out[arm] = {
            "covariate": covar,
            "signature": sig,
            "stratum": skey,
            "n": int(r["n"]),
            "rank": int(r["rank"]),
            "denominator": int(r["denominator_used"]),
            "sign": r["sign"],
            "coef_std": round(float(r["coef_std"]), 4),
            "q_bh": round(float(r["q_bh"]), 5),
            "raw_pass": bool(r["rank"] <= 3 and r["sign"] == "+" and r["q_bh"] < 0.05),
        }

    # --- APOBEC3-locus leakage guard (KD6): re-run Arm-C target excluding APOBEC3-mutated samples ---
    mut = pd.read_feather(
        out_dir / "studies" / "tcga_mc3" / "mut" / "table" / "mut.feather",
        columns=["symbol", "sample_id_tumor"],
    )
    apo_samples = set(
        mut[mut["symbol"].astype(str).isin(APOBEC3_GENES)]["sample_id_tumor"]
        .astype(str)
        .str.slice(0, 15)
    )
    c_samples = [
        b
        for b in cov[cov["arm"].isin(ARM_C_STRATA)]["sample_barcode15"]
        if b in pass_b15
    ]
    c_clean = [b for b in c_samples if b not in apo_samples]
    frame_c = build_stratum(
        cov, expo_wide, c_clean, manifest["arm_c_pooled"]["active_signatures"]
    )
    leak: dict[str, object] = {
        "n_apobec3_mutated_in_arm_c": len(set(c_samples) & apo_samples),
        "n_arm_c_total": len(c_samples),
    }
    fit_clean = fit_cell(
        frame_c, "clr_SBS2_13", "apobec3ab_joint", ["arm", "ancestry", "treatment"]
    )
    if fit_clean is not None:
        # rank apobec among arm-C ranked covariates on the cleaned set
        clean_rows = []
        for c in manifest["arm_c_pooled"]["ranked_covariates"]:
            ft = fit_cell(frame_c, "clr_SBS2_13", c, ["arm", "ancestry", "treatment"])
            if ft is not None:
                clean_rows.append(
                    {"covariate": c, "abs_coef": abs(ft[1]), "coef": ft[1]}
                )
        cdf = (
            pd.DataFrame(clean_rows)
            .sort_values("abs_coef", ascending=False)
            .reset_index(drop=True)
        )
        rk = (
            int(cdf.index[cdf["covariate"] == "apobec3ab_joint"][0]) + 1
            if "apobec3ab_joint" in set(cdf["covariate"])
            else None
        )
        leak.update(
            {
                "arm_c_rank_excluding_apobec3_mutated": rk,
                "arm_c_sign_excluding": "+" if fit_clean[1] > 0 else "-",
                "arm_c_rank_full": targets_out["C"].get("rank"),
                "survives": bool(rk is not None and rk <= 3 and fit_clean[1] > 0),
            }
        )

    # --- R1 unconditioned contrast (exploratory): within-tissue vs tissue-pooled (no tissue term) ---
    r1 = {}
    full_pass = [b for b in cov["sample_barcode15"] if b in pass_b15]
    # unconditioned active set = union across all arms' active sets
    union_active = sorted(
        {
            s
            for meta in manifest["per_stratum"].values()
            for s in meta["active_signatures"]
        }
    )
    frame_uncond = build_stratum(cov, expo_wide, full_pass, union_active)
    for arm, (covar, sig, _stratum_key) in TARGETS.items():
        ft = fit_cell(
            frame_uncond, f"clr_{sig}", covar, ["ancestry", "treatment"]
        )  # NO tissue term
        within = targets_out[arm].get("coef_std")
        r1[arm] = {
            "within_tissue_coef": within,
            "unconditioned_coef": round(ft[1], 4) if ft else None,
        }

    # --- write ---
    grid_out = assoc / "h08_association_grid.feather"
    grid.drop(columns="abs_coef").to_feather(grid_out)
    meta = {
        "task": "t199",
        "stage": "WP2",
        "frozen_denominator_manifest": {"path": str(man_path), "sha256": manifest_sha},
        "fdr_family_size": int(m),
        "count_floor_note": "primary grid restricted to passes_count_floor (t179 trusted exposures)",
        "count_floor_per_arm": floor_drop,
        "confirmatory_targets_pre_wp3": targets_out,
        "leakage_guard_apobec3_locus": leak,
        "r1_unconditioned_contrast": r1,
        "statsmodels_version": statsmodels.__version__,
        "clr_pseudocount": CLR_PSEUDOCOUNT,
        "note": "Target reads are PRE-permutation/PRE-sensitivity; the final H08a verdict is read in WP4.",
    }
    (assoc / "h08_association_grid.meta.json").write_text(
        json.dumps(meta, indent=2, default=str)
    )

    # --- report ---
    console.print(f"[green]wrote[/] {grid_out}  ({len(grid)} cells; FDR family={m})")
    console.print(
        f"  manifest sha256={manifest_sha[:16]}…  statsmodels {statsmodels.__version__}"
    )
    for arm in ("A", "B", "C"):
        t = targets_out[arm]
        if "rank" in t:
            console.print(
                f"  [bold]Arm {arm}[/] {t['covariate']}→{t['signature']} @{t['stratum']} "
                f"(n={t['n']}): rank {t['rank']}/{t['denominator']} sign {t['sign']} "
                f"coef={t['coef_std']} q={t['q_bh']} → raw_pass={t['raw_pass']}"
            )
    if "survives" in leak:
        console.print(
            f"  leakage guard: arm-C rank full={leak.get('arm_c_rank_full')} → "
            f"excl {leak['n_apobec3_mutated_in_arm_c']} APOBEC3-mutated = rank "
            f"{leak['arm_c_rank_excluding_apobec3_mutated']} (survives={leak['survives']})"
        )
    console.print(
        "  [yellow]PRE-WP3 reads — final verdict gated on WP3 permutation+sensitivity (WP4).[/]"
    )


if __name__ == "__main__":
    main()
