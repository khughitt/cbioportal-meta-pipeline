# science:code
# status: workflow-owned
# science:end
"""h08 within-tissue positive-control failure diagnostics (t200).

Read-only diagnostic layer over the frozen t199 H08a artifacts. The script keeps the primary
`fit_cell` machinery untouched for baseline reproduction, then runs probe-only variants to separate
effective contrast, smoking operationalization, burden-mediated/proximal dominance, and APOBEC
proliferation robustness. These outputs do not re-read or alter the locked H08a verdict.
"""

from __future__ import annotations

import hashlib
import json
import logging
import sys
from pathlib import Path
from typing import Any

import click
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import yaml
from rich.console import Console

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_h08_association_scan import (  # noqa: E402
    ARM_B_STRATA,
    ARM_C_STRATA,
    TARGETS,
    _collapse,
    build_stratum,
    fit_cell,
)

console = Console()
logger = logging.getLogger("diagnose_h08_within_tissue")
if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s %(name)s: %(message)s"
    )

SBS7_SATURATION_THRESHOLD = 0.90
SBS7_SATURATION_SWEEP = (0.80, 0.85, 0.90, 0.95)

SMOKING_LABEL_MAP = {
    "Lifelong Non-smoker": 0.0,
    "Current smoker": 1.0,
    "Current reformed smoker for < or = 15 years": 1.0,
    "Current reformed smoker for > 15 years": 1.0,
    "Current Reformed Smoker, Duration Not Specified": 1.0,
}

# Published meta-PCNA proliferation genes as used in a later TCGA pan-cancer application of the
# Venet et al. 2011 PCNA metagene concept; logged verbatim in the t200 meta sidecar.
VENET_META_PCNA_GENES = (
    "AURKA",
    "BIRC5",
    "CDC20",
    "CDCA4",
    "CKLF",
    "FEN1",
    "GINS1",
    "GTPBP2",
    "LBR",
    "LSM6",
    "MAD2L1",
    "MCM4",
    "MKI67",
    "NUSAP1",
    "PCNA",
    "PSMD9",
    "RFC3",
    "RFC4",
    "RRM2",
    "SMC4",
    "SNF8",
    "SNRPB",
    "TACC3",
    "TCF3",
    "TFDP1",
    "TROAP",
    "TYMS",
    "UBE2C",
    "VRK1",
    "ZWINT",
)

CANONICAL_PROLIFERATION_GENES = (
    "MKI67",
    "PCNA",
    "TOP2A",
    "CCNB1",
    "CCNB2",
    "BUB1",
    "CDK1",
    "AURKA",
    "FOXM1",
    "CENPF",
    "RRM2",
    "TYMS",
    "MCM2",
    "BIRC5",
    "UBE2C",
    "CDC20",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _to_num(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.replace({"[Not Available]": np.nan, "[Unknown]": np.nan}),
        errors="coerce",
    )


def _iqr(series: pd.Series) -> float:
    q75, q25 = np.nanpercentile(series.to_numpy(dtype=float), [75, 25])
    return float(q75 - q25)


def _entropy(series: pd.Series) -> float:
    counts = series.dropna().value_counts()
    if counts.empty:
        return float("nan")
    p = counts / counts.sum()
    return float(-(p * np.log2(p)).sum())


def _status_fit(
    status: str,
    reason: str,
    n: int,
    ycol: str,
    cov: str,
    categorical_adjust: list[str],
    numeric_adjust: list[str],
) -> dict[str, Any]:
    return {
        "status": status,
        "reason": reason,
        "n": int(n),
        "ycol": ycol,
        "covariate": cov,
        "categorical_adjust": categorical_adjust,
        "numeric_adjust": numeric_adjust,
    }


def fit_diag(
    df: pd.DataFrame,
    ycol: str,
    cov: str,
    *,
    categorical_adjust: list[str],
    numeric_adjust: list[str],
    min_n: int = 3,
) -> dict[str, Any] | None:
    """Adjusted OLS with explicit numeric controls and all-model-column missingness handling."""
    columns = [ycol, cov, *categorical_adjust, *numeric_adjust]
    sub = df[columns].dropna().copy()
    if len(sub) < min_n or sub[cov].nunique(dropna=True) < 2:
        logger.warning(
            "skipping fit: covariate not estimable (%s vs %s, n=%s)",
            cov,
            ycol,
            len(sub),
        )
        return None

    cov_sd = sub[cov].std(ddof=0)
    if not np.isfinite(cov_sd) or cov_sd == 0:
        logger.warning("skipping fit: zero-variance covariate after dropna (%s)", cov)
        return None
    sub["_z"] = (sub[cov] - sub[cov].mean()) / cov_sd

    terms = ["_z"]
    for col in numeric_adjust:
        sd = sub[col].std(ddof=0)
        if not np.isfinite(sd) or sd == 0:
            logger.warning(
                "skipping fit: zero-variance numeric control after dropna (%s)", col
            )
            return None
        zcol = f"_num_{col}"
        sub[zcol] = (sub[col] - sub[col].mean()) / sd
        terms.append(zcol)

    for col in categorical_adjust:
        if col == "treatment":
            if sub[col].fillna(0).nunique() >= 2:
                terms.append("treatment")
        elif sub[col].nunique(dropna=True) >= 2:
            terms.append(f"C({col})")

    sub = sub.rename(columns={ycol: "_y"})
    formula = "_y ~ " + " + ".join(terms)
    try:
        res = smf.ols(formula, data=sub).fit()
    except Exception as exc:  # noqa: BLE001
        logger.warning("fit_diag failed (%s vs %s): %s", cov, ycol, exc)
        return None
    if "_z" not in res.params.index:
        return None
    return {
        "status": "ok",
        "reason": None,
        "n": int(len(sub)),
        "coef_std": float(res.params["_z"]),
        "pvalue": float(res.pvalues["_z"]),
        "condition_number": float(res.condition_number),
        "formula": formula,
        "ycol": ycol,
        "covariate": cov,
        "categorical_adjust": categorical_adjust,
        "numeric_adjust": numeric_adjust,
    }


def derive_smoking_operationalizations(
    cov: pd.DataFrame, smoking: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Derive auditable smoking variables from raw PanCanAtlas string labels."""
    sm = smoking.assign(
        b12=smoking["bcr_patient_barcode"].astype(str).str.slice(0, 12)
    ).set_index("b12")
    sm = sm[~sm.index.duplicated(keep="first")]
    out = cov.copy()
    labels = out["patient12"].map(sm["tobacco_smoking_history"])
    out["tobacco_smoking_history_raw"] = labels
    out["ever_smoker_derived"] = labels.map(SMOKING_LABEL_MAP)
    out["pack_years_raw"] = _to_num(
        out["patient12"].map(sm["number_pack_years_smoked"])
    )
    out["pack_years_zero_never"] = out["pack_years"].copy()
    out.loc[out["ever_smoker_derived"] == 0.0, "pack_years_zero_never"] = 0.0

    label_counts = (
        labels.fillna("<NA>")
        .value_counts(dropna=False)
        .rename_axis("tobacco_smoking_history")
        .reset_index(name="n")
    )
    label_counts["mapped_value"] = label_counts["tobacco_smoking_history"].map(
        SMOKING_LABEL_MAP
    )
    label_counts.loc[
        label_counts["tobacco_smoking_history"] == "<NA>", "mapped_value"
    ] = np.nan
    return out, label_counts


def compute_contrast_summary(
    frame: pd.DataFrame,
    *,
    covariate: str,
    stratum_col: str,
    strata: list[str],
) -> pd.DataFrame:
    """Effective contrast summary with explicit raw and tissue-centered SD columns."""
    sub = (
        frame[frame[stratum_col].isin(strata)][[stratum_col, covariate]].dropna().copy()
    )
    if sub.empty:
        return pd.DataFrame()
    centered = sub[covariate] - sub.groupby(stratum_col)[covariate].transform("mean")
    sub["_centered"] = centered
    pooled_sd = float(sub["_centered"].std(ddof=0))
    rows = []
    for stratum, grp in sub.groupby(stratum_col, sort=False):
        sd_raw = float(grp[covariate].std(ddof=0))
        sd_centered = float(grp["_centered"].std(ddof=0))
        rows.append(
            {
                "covariate": covariate,
                "stratum": stratum,
                "n": int(len(grp)),
                "sd_raw_fit_frame": sd_raw,
                "iqr_raw_fit_frame": _iqr(grp[covariate]),
                "sd_tissue_centered_fit_frame": sd_centered,
                "pooled_sd_tissue_centered_fit_frame": pooled_sd,
                "range_restriction_ratio_tissue_centered": sd_centered / pooled_sd
                if pooled_sd
                else np.nan,
            }
        )
    return pd.DataFrame(rows)


def load_rsem_matrix(path: Path) -> pd.DataFrame:
    """Load cBioPortal RSEM matrix as genes x 15-char sample barcodes."""
    df = pd.read_csv(path, sep="\t", dtype={"Hugo_Symbol": str})
    df = df.drop(columns=[c for c in ("Entrez_Gene_Id",) if c in df.columns])
    df = df[df["Hugo_Symbol"].notna() & (df["Hugo_Symbol"] != "")]
    df = df.groupby("Hugo_Symbol", sort=False).max(numeric_only=True)
    df = df.apply(pd.to_numeric, errors="coerce")
    df.columns = pd.Index(df.columns).astype(str).str.slice(0, 15)
    df = df.T.groupby(level=0).max().T
    return df


def score_gene_set_expression(
    expr: pd.DataFrame, *, requested_genes: list[str], set_name: str
) -> tuple[pd.Series, dict[str, Any]]:
    """Mean z-scored log2(RSEM+1) over realized genes; `expr` is genes x samples."""
    requested = list(dict.fromkeys(requested_genes))
    realized = [g for g in requested if g in expr.index]
    meta: dict[str, Any] = {
        "set_name": set_name,
        "requested_genes": requested,
        "realized_genes": realized,
        "n_requested_genes": len(requested),
        "n_realized_genes": len(realized),
    }
    if not realized:
        score = pd.Series(np.nan, index=expr.columns, name=set_name)
        meta["score_variance"] = np.nan
        return score, meta
    logged = np.log2(expr.loc[realized].clip(lower=0) + 1.0)
    sd = logged.std(axis=1, ddof=0)
    usable = sd[sd > 0].index.tolist()
    meta["usable_genes"] = usable
    meta["n_usable_genes"] = len(usable)
    if not usable:
        score = pd.Series(np.nan, index=expr.columns, name=set_name)
        meta["score_variance"] = np.nan
        return score, meta
    z = (
        logged.loc[usable]
        .sub(logged.loc[usable].mean(axis=1), axis=0)
        .div(sd.loc[usable], axis=0)
    )
    score = z.mean(axis=0).rename(set_name)
    meta["score_variance"] = float(score.var(ddof=0))
    return score, meta


def grouped_exposure(expo: pd.DataFrame, active: list[str]) -> pd.DataFrame:
    cols = [s for s in active if s in expo.columns]
    sub = expo[cols].copy()
    sub.columns = [_collapse(c) for c in cols]
    return sub.T.groupby(level=0).sum().T


def signature_fraction(
    expo: pd.DataFrame, active: list[str], signature: str
) -> pd.Series:
    grouped = grouped_exposure(expo, active)
    total = grouped.sum(axis=1).replace(0, np.nan)
    if signature not in grouped.columns:
        return pd.Series(np.nan, index=grouped.index)
    return grouped[signature] / total


def _stratum_spec(
    cov: pd.DataFrame, manifest: dict[str, Any], pass_b15: set[str], skey: str
) -> tuple[list[str], list[str], list[str], list[str]]:
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


def _corr_json(df: pd.DataFrame, columns: list[str]) -> str:
    corr = df[columns].dropna().corr(numeric_only=True)
    return json.dumps(corr.round(6).to_dict(), sort_keys=True)


def _shrinkage_bin(baseline: float, controlled: float) -> tuple[float, str]:
    if not np.isfinite(baseline) or baseline == 0 or not np.isfinite(controlled):
        return np.nan, "not_estimable"
    shrinkage = 1.0 - (abs(controlled) / abs(baseline))
    if shrinkage < 0.25:
        label = "<25%"
    elif shrinkage < 0.50:
        label = "25-50%"
    else:
        label = ">50%"
    return float(shrinkage), label


def _target_baseline_checks(
    cov: pd.DataFrame,
    expo: pd.DataFrame,
    manifest: dict[str, Any],
    grid: pd.DataFrame,
    pass_b15: set[str],
) -> list[dict[str, Any]]:
    rows = []
    for arm, (covar, sig, skey) in TARGETS.items():
        samples, _ranked, active, adjust = _stratum_spec(cov, manifest, pass_b15, skey)
        frame = build_stratum(cov, expo, samples, active)
        ft = fit_cell(frame, f"clr_{sig}", covar, adjust)
        cell = grid[
            (grid["stratum"] == skey)
            & (grid["signature"] == sig)
            & (grid["covariate"] == covar)
        ]
        if ft is None or cell.empty:
            raise SystemExit(
                f"baseline reproduction failed for Arm {arm}: missing fit/grid cell"
            )
        grid_row = cell.iloc[0]
        coef_delta = abs(float(grid_row["coef_std"]) - ft[1])
        if int(grid_row["n"]) != ft[0] or coef_delta > 1e-9:
            raise SystemExit(
                f"baseline reproduction mismatch for Arm {arm}: "
                f"fit n/coef={ft[0]}/{ft[1]} grid n/coef={grid_row['n']}/{grid_row['coef_std']}"
            )
        rows.append(
            {
                "arm": arm,
                "covariate": covar,
                "signature": sig,
                "stratum": skey,
                "n": int(ft[0]),
                "coef_std": float(ft[1]),
                "pvalue": float(ft[2]),
                "grid_rank": int(grid_row["rank"]),
                "grid_denominator": int(grid_row["denominator_used"]),
            }
        )
    return rows


def run_test1_contrast(cov: pd.DataFrame, pass_b15: set[str]) -> pd.DataFrame:
    frame = cov[cov["sample_barcode15"].isin(pass_b15)].copy()
    rows = []
    skcm = frame[frame["arm"] == "SKCM"][["arm", "uv_sun_exposure_ordinal"]].dropna()
    if not skcm.empty:
        counts = (
            skcm["uv_sun_exposure_ordinal"]
            .value_counts(dropna=False)
            .sort_index()
            .to_dict()
        )
        rows.append(
            {
                "covariate": "uv_sun_exposure_ordinal",
                "stratum": "SKCM",
                "n": int(len(skcm)),
                "sd_raw_fit_frame": float(skcm["uv_sun_exposure_ordinal"].std(ddof=0)),
                "iqr_raw_fit_frame": _iqr(skcm["uv_sun_exposure_ordinal"]),
                "sd_tissue_centered_fit_frame": np.nan,
                "pooled_sd_tissue_centered_fit_frame": np.nan,
                "range_restriction_ratio_tissue_centered": np.nan,
                "entropy_bits": _entropy(skcm["uv_sun_exposure_ordinal"]),
                "tier_counts_json": json.dumps(
                    {str(k): int(v) for k, v in counts.items()}, sort_keys=True
                ),
            }
        )
    for df in (
        compute_contrast_summary(
            frame, covariate="pack_years", stratum_col="arm", strata=ARM_B_STRATA
        ),
        compute_contrast_summary(
            frame, covariate="apobec3ab_joint", stratum_col="arm", strata=ARM_C_STRATA
        ),
    ):
        if not df.empty:
            rows.extend(df.to_dict("records"))
    return pd.DataFrame(rows)


def run_test2_smoking(
    cov: pd.DataFrame,
    smoking: pd.DataFrame,
    expo: pd.DataFrame,
    manifest: dict[str, Any],
    pass_b15: set[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    cov_smoking, label_counts = derive_smoking_operationalizations(cov, smoking)
    rows = []
    for skey in ("ARM_B_POOLED", "LUAD", "LUSC"):
        samples, _ranked, active, adjust = _stratum_spec(
            cov_smoking, manifest, pass_b15, skey
        )
        frame = build_stratum(cov_smoking, expo, samples, active)
        fits = []
        for covar in ("pack_years", "pack_years_zero_never", "ever_smoker_derived"):
            ft = fit_diag(
                frame, "clr_SBS4", covar, categorical_adjust=adjust, numeric_adjust=[]
            )
            if ft is None:
                fits.append({"covariate": covar, "abs_coef": np.nan, "fit": None})
            else:
                fits.append(
                    {"covariate": covar, "abs_coef": abs(ft["coef_std"]), "fit": ft}
                )
        ranks = (
            pd.DataFrame([{k: v for k, v in f.items() if k != "fit"} for f in fits])
            .dropna(subset=["abs_coef"])
            .sort_values("abs_coef", ascending=False)
            .reset_index(drop=True)
        )
        rank_map = {r["covariate"]: i + 1 for i, r in ranks.iterrows()}
        for f in fits:
            ft = f["fit"]
            rows.append(
                {
                    "stratum": skey,
                    "signature": "SBS4",
                    "covariate": f["covariate"],
                    "comparison_rank": rank_map.get(f["covariate"]),
                    "comparison_denominator": int(len(ranks)),
                    **(
                        {
                            "status": "not_estimable",
                            "n": None,
                            "coef_std": None,
                            "pvalue": None,
                            "condition_number": None,
                        }
                        if ft is None
                        else {
                            "status": "ok",
                            "n": ft["n"],
                            "coef_std": ft["coef_std"],
                            "pvalue": ft["pvalue"],
                            "condition_number": ft["condition_number"],
                        }
                    ),
                }
            )
    return pd.DataFrame(rows), label_counts


def run_test3_burden(
    cov: pd.DataFrame,
    expo: pd.DataFrame,
    manifest: dict[str, Any],
    pass_b15: set[str],
) -> pd.DataFrame:
    rows = []
    for arm, (covar, sig, skey) in TARGETS.items():
        samples, _ranked, active, adjust = _stratum_spec(cov, manifest, pass_b15, skey)
        frame = build_stratum(cov, expo, samples, active)
        ycol = f"clr_{sig}"
        marginal = fit_diag(
            frame, ycol, covar, categorical_adjust=adjust, numeric_adjust=[]
        )
        partial = fit_diag(
            frame,
            ycol,
            covar,
            categorical_adjust=adjust,
            numeric_adjust=["tmb_nonsynonymous", "is_hypermutator"],
        )
        corr_cols = [covar, "tmb_nonsynonymous", "is_hypermutator"]
        rows.append(
            {
                "arm": arm,
                "stratum": skey,
                "signature": sig,
                "covariate": covar,
                "model": "burden_conditioned",
                "n_marginal": marginal["n"] if marginal else None,
                "coef_marginal": marginal["coef_std"] if marginal else None,
                "n": partial["n"] if partial else None,
                "coef_std": partial["coef_std"] if partial else None,
                "pvalue": partial["pvalue"] if partial else None,
                "condition_number": partial["condition_number"] if partial else None,
                "correlation_json": _corr_json(frame, corr_cols),
            }
        )
        grouped = grouped_exposure(expo.reindex(samples), active)
        frame["_signature_fraction"] = signature_fraction(
            expo.reindex(samples), active, sig
        ).reindex(frame.index)
        for threshold in SBS7_SATURATION_SWEEP if arm == "A" else (np.nan,):
            subset = frame[frame["is_hypermutator"] != 1.0].copy()
            threshold_label = None
            if arm == "A":
                subset = subset[subset["_signature_fraction"] < threshold]
                threshold_label = threshold
            ft = fit_diag(
                subset, ycol, covar, categorical_adjust=adjust, numeric_adjust=[]
            )
            rows.append(
                {
                    "arm": arm,
                    "stratum": skey,
                    "signature": sig,
                    "covariate": covar,
                    "model": "non_saturated_subset",
                    "sbs7_fraction_threshold": threshold_label,
                    "n": ft["n"] if ft else None,
                    "coef_std": ft["coef_std"] if ft else None,
                    "pvalue": ft["pvalue"] if ft else None,
                    "condition_number": ft["condition_number"] if ft else None,
                    "n_marginal": None,
                    "coef_marginal": None,
                    "correlation_json": json.dumps({}),
                    "active_signature_parts": ",".join(grouped.columns),
                }
            )
    return pd.DataFrame(rows)


def run_test4_proliferation(
    cfg: dict[str, Any],
    cov: pd.DataFrame,
    expo: pd.DataFrame,
    manifest: dict[str, Any],
    pass_b15: set[str],
) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    data_dir = Path(cfg["data_dir"])
    rows = []
    gene_meta = []
    for arm in ARM_C_STRATA:
        study = cfg["h08_arm_studies"][arm]
        expr = load_rsem_matrix(data_dir / study / "data_mrna_seq_v2_rsem.txt")
        samples, _ranked, active, adjust = _stratum_spec(cov, manifest, pass_b15, arm)
        frame = build_stratum(cov, expo, samples, active)
        ycol = "clr_SBS2_13"
        baseline = fit_diag(
            frame, ycol, "apobec3ab_joint", categorical_adjust=adjust, numeric_adjust=[]
        )
        for set_name, genes in (
            ("venet_meta_pcna", list(VENET_META_PCNA_GENES)),
            ("canonical_cell_cycle", list(CANONICAL_PROLIFERATION_GENES)),
        ):
            score, meta = score_gene_set_expression(
                expr.reindex(columns=frame.index),
                requested_genes=genes,
                set_name=set_name,
            )
            meta.update({"arm": arm, "study": study})
            gene_meta.append(meta)
            with_score = frame.copy()
            with_score["proliferation_score"] = score.reindex(with_score.index)
            controlled = fit_diag(
                with_score,
                ycol,
                "apobec3ab_joint",
                categorical_adjust=adjust,
                numeric_adjust=["proliferation_score"],
            )
            baseline_coef = baseline["coef_std"] if baseline else np.nan
            controlled_coef = controlled["coef_std"] if controlled else np.nan
            shrinkage, shrinkage_bin = _shrinkage_bin(baseline_coef, controlled_coef)
            rows.append(
                {
                    "arm": arm,
                    "signature": "SBS2_13",
                    "covariate": "apobec3ab_joint",
                    "gene_set": set_name,
                    "n_baseline": baseline["n"] if baseline else None,
                    "coef_baseline": baseline_coef
                    if np.isfinite(baseline_coef)
                    else None,
                    "n": controlled["n"] if controlled else None,
                    "coef_std": controlled_coef
                    if np.isfinite(controlled_coef)
                    else None,
                    "pvalue": controlled["pvalue"] if controlled else None,
                    "condition_number": controlled["condition_number"]
                    if controlled
                    else None,
                    "shrinkage": shrinkage if np.isfinite(shrinkage) else None,
                    "shrinkage_bin": shrinkage_bin,
                    "n_realized_genes": meta["n_realized_genes"],
                    "n_usable_genes": meta.get("n_usable_genes"),
                    "score_variance": meta["score_variance"],
                }
            )
    return pd.DataFrame(rows), gene_meta


@click.command()
@click.option(
    "--config",
    "config_path",
    type=click.Path(path_type=Path, exists=True),
    required=True,
)
@click.option(
    "--smoking",
    type=click.Path(path_type=Path, exists=True),
    default=Path("data/pancanatlas_clinical_with_followup.tsv"),
    show_default=True,
)
def main(config_path: Path, smoking: Path) -> None:
    cfg = yaml.safe_load(config_path.read_text())
    out_dir = Path(cfg["out_dir"])
    assoc = out_dir / "association"
    diagnostics = assoc / "diagnostics"
    diagnostics.mkdir(parents=True, exist_ok=True)

    man_path = assoc / "covariate_denominator.json"
    manifest = json.loads(man_path.read_text())
    manifest_sha = _sha256(man_path)
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

    smoking_df = pd.read_csv(
        smoking, sep="\t", dtype=str, low_memory=False, encoding="latin-1"
    )

    baseline = _target_baseline_checks(cov, expo, manifest, grid, pass_b15)
    contrast = run_test1_contrast(cov, pass_b15)
    smoking_rows, smoking_label_counts = run_test2_smoking(
        cov, smoking_df, expo, manifest, pass_b15
    )
    burden = run_test3_burden(cov, expo, manifest, pass_b15)
    proliferation, proliferation_gene_meta = run_test4_proliferation(
        cfg, cov, expo, manifest, pass_b15
    )

    pd.DataFrame(baseline).to_feather(
        diagnostics / "h08_within_tissue_baseline.feather"
    )
    contrast.to_feather(diagnostics / "h08_within_tissue_contrast.feather")
    smoking_rows.to_feather(diagnostics / "h08_smoking_operationalizations.feather")
    smoking_label_counts.to_feather(diagnostics / "h08_smoking_label_counts.feather")
    burden.to_feather(diagnostics / "h08_burden_conditioning.feather")
    proliferation.to_feather(diagnostics / "h08_apobec_proliferation.feather")

    meta = {
        "task": "t200",
        "frozen_denominator_manifest": {"path": str(man_path), "sha256": manifest_sha},
        "baseline_reproduction": baseline,
        "smoking_label_map": SMOKING_LABEL_MAP,
        "sbs7_saturation_threshold": SBS7_SATURATION_THRESHOLD,
        "sbs7_saturation_sweep": SBS7_SATURATION_SWEEP,
        "proliferation_gene_sets": {
            "venet_meta_pcna": list(VENET_META_PCNA_GENES),
            "canonical_cell_cycle": list(CANONICAL_PROLIFERATION_GENES),
        },
        "proliferation_gene_set_realization": proliferation_gene_meta,
        "notes": [
            "Diagnostic only; locked H08a verdict is unchanged.",
            "fit_diag reports n after all model columns are non-missing.",
        ],
    }
    (diagnostics / "h08_within_tissue_diagnostics.meta.json").write_text(
        json.dumps(meta, indent=2, default=str)
    )

    console.print(f"[green]wrote[/] {diagnostics}")
    console.print(f"  baseline targets reproduced: {len(baseline)}")
    console.print(f"  manifest sha256={manifest_sha[:16]}...")


if __name__ == "__main__":
    main()
