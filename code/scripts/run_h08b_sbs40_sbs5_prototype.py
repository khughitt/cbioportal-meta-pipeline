# science:code
# status: workflow-owned
# science:end
"""Exploratory H08b SBS40-vs-SBS5 expression-module prototype (t182).

This script is intentionally exploratory. It does not re-read H08a, does not promote H08b, and
does not make upstream-cause claims. It asks whether the existing H08 expression-module substrate
can separate SBS40 from SBS5 after age conditioning.
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Any

import click
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import yaml
from rich.console import Console

console = Console()
logger = logging.getLogger("run_h08b_sbs40_sbs5_prototype")
if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s %(name)s: %(message)s"
    )

CLR_PSEUDOCOUNT = 0.5
MIN_MODEL_N = 100
SBS40_PARTS = ("SBS40a", "SBS40b", "SBS40c")
TARGET_GENES = ("REV3L", "POLZ")
PRIMARY_OUTCOME = "clr_SBS40_minus_SBS5"
SECONDARY_OUTCOMES = ("clr_SBS40", "clr_SBS5")
SIG_GROUP = {
    "SBS7a": "SBS7",
    "SBS7b": "SBS7",
    "SBS7c": "SBS7",
    "SBS7d": "SBS7",
    "SBS2": "SBS2_13",
    "SBS13": "SBS2_13",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def active_sbs40_parts(active: list[str]) -> list[str]:
    return [part for part in SBS40_PARTS if part in set(active)]


def build_clr_outcomes(expo: pd.DataFrame, active: list[str]) -> pd.DataFrame:
    """Build CLR outcomes with active-manifest SBS40 parts collapsed to one SBS40 component."""
    parts = active_sbs40_parts(active)
    if "SBS5" not in active:
        raise ValueError("SBS5 is not active in this stratum")
    if not parts:
        raise ValueError("No SBS40 component is active in this stratum")

    grouped = pd.DataFrame(index=expo.index)
    grouped["SBS40"] = sum(
        expo[part] if part in expo.columns else 0.0 for part in parts
    )
    for sig in active:
        if sig in SBS40_PARTS:
            continue
        target = SIG_GROUP.get(sig, sig)
        values = expo[sig] if sig in expo.columns else 0.0
        if target in grouped.columns:
            grouped[target] = grouped[target] + values
        else:
            grouped[target] = values

    vals = grouped.astype(float).to_numpy() + CLR_PSEUDOCOUNT
    logv = np.log(vals)
    clr = logv - logv.mean(axis=1, keepdims=True)
    out = pd.DataFrame(
        clr, index=grouped.index, columns=[f"clr_{c}" for c in grouped.columns]
    )
    out[PRIMARY_OUTCOME] = out["clr_SBS40"] - out["clr_SBS5"]
    out["sbs40_active_parts"] = "|".join(parts)
    return out


def fit_adjusted_cell(
    df: pd.DataFrame,
    ycol: str,
    cov: str,
    *,
    categorical_adjust: list[str],
    numeric_adjust: list[str],
    min_n: int = MIN_MODEL_N,
) -> dict[str, Any] | None:
    columns = [ycol, cov, *categorical_adjust, *numeric_adjust]
    sub = df[columns].replace([np.inf, -np.inf], np.nan).dropna().copy()
    if len(sub) < min_n or sub[cov].nunique(dropna=True) < 2:
        return None

    cov_std = sub[cov].std(ddof=0)
    if not np.isfinite(cov_std) or cov_std == 0:
        return None
    sub["_z_cov"] = (sub[cov] - sub[cov].mean()) / cov_std

    terms = ["_z_cov"]
    used_numeric = []
    used_categorical = []
    for col in numeric_adjust:
        if sub[col].nunique(dropna=True) < 2:
            continue
        std = sub[col].std(ddof=0)
        if not np.isfinite(std) or std == 0:
            continue
        zcol = f"_z_{col}"
        sub[zcol] = (sub[col] - sub[col].mean()) / std
        terms.append(zcol)
        used_numeric.append(col)

    for col in categorical_adjust:
        if sub[col].nunique(dropna=True) >= 2:
            terms.append(f"C({col})")
            used_categorical.append(col)

    sub = sub.rename(columns={ycol: "_y"})
    try:
        res = smf.ols("_y ~ " + " + ".join(terms), data=sub).fit()
    except Exception as exc:  # noqa: BLE001
        logger.warning("fit failed (%s vs %s): %s", cov, ycol, exc)
        return None

    if "_z_cov" not in res.params.index:
        return None
    return {
        "n": int(len(sub)),
        "coef_std": float(res.params["_z_cov"]),
        "pvalue": float(res.pvalues["_z_cov"]),
        "sign": "+" if float(res.params["_z_cov"]) > 0 else "-",
        "numeric_adjust": "|".join(used_numeric),
        "categorical_adjust": "|".join(used_categorical),
    }


def apply_bh(grid: pd.DataFrame, *, family_cols: list[str]) -> pd.DataFrame:
    if grid.empty:
        return grid.assign(q_bh=pd.Series(dtype=float))

    out = grid.copy()
    out["q_bh"] = np.nan
    grouped = (
        out.groupby(family_cols, dropna=False, sort=False)
        if family_cols
        else [((), out)]
    )
    for _, group in grouped:
        estimable = group[group["pvalue"].notna()].sort_values("pvalue")
        if estimable.empty:
            continue
        m = len(estimable)
        raw = estimable["pvalue"].to_numpy(dtype=float) * m / np.arange(1, m + 1)
        q = np.minimum.accumulate(raw[::-1])[::-1].clip(max=1.0)
        out.loc[estimable.index, "q_bh"] = q
    return out


def build_target_expression(
    rsem: pd.DataFrame, *, sample_ids: list[str], genes: list[str]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return log2(RSEM+1) target gene expression and per-gene evaluability rows."""
    col_by_b15: dict[str, str] = {}
    for col in rsem.columns:
        col_by_b15.setdefault(str(col)[:15], str(col))
    index = pd.Index([sample[:15] for sample in sample_ids], name="sample_barcode15")
    expr = pd.DataFrame(index=index)
    rows = []

    for gene in genes:
        if gene not in rsem.index:
            rows.append(
                {
                    "gene": gene,
                    "status": "not_evaluable_missing_expression_row",
                    "n_expression_samples": 0,
                }
            )
            continue
        mapped = [col_by_b15.get(sample[:15]) for sample in sample_ids]
        values = pd.Series(np.nan, index=index, dtype=float)
        for sample, col in zip(index, mapped, strict=True):
            if col is not None:
                values.loc[sample] = float(rsem.loc[gene, col])
        expr[gene] = np.log2(values.clip(lower=0) + 1.0)
        rows.append(
            {
                "gene": gene,
                "status": "evaluable"
                if expr[gene].notna().any()
                else "not_evaluable_no_overlap",
                "n_expression_samples": int(expr[gene].notna().sum()),
            }
        )
    return expr, pd.DataFrame(rows)


def load_rsem_gene_matrix(path: Path, genes: tuple[str, ...]) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t", dtype={"Hugo_Symbol": str})
    df = df[df["Hugo_Symbol"].isin(genes)].drop(
        columns=[c for c in ("Entrez_Gene_Id",) if c in df.columns]
    )
    if df.empty:
        return pd.DataFrame(index=pd.Index([], name="Hugo_Symbol"))
    df = df.groupby("Hugo_Symbol", sort=False).max(numeric_only=True)
    return df.apply(pd.to_numeric, errors="coerce")


def _module_columns(ranked: list[str]) -> list[str]:
    return [cov for cov in ranked if cov.startswith("module_")]


def _fit_or_status(
    frame: pd.DataFrame,
    outcome: str,
    covariate: str,
    *,
    family: str,
    stratum: str,
    covariate_class: str,
) -> dict[str, Any]:
    fit = fit_adjusted_cell(
        frame,
        outcome,
        covariate,
        categorical_adjust=["ancestry"],
        numeric_adjust=["age", "treatment"],
        min_n=MIN_MODEL_N,
    )
    row: dict[str, Any] = {
        "stratum": stratum,
        "family": family,
        "outcome": outcome,
        "covariate": covariate,
        "covariate_class": covariate_class,
    }
    if fit is None:
        row.update(
            {
                "status": "not_evaluable_model",
                "n": 0,
                "coef_std": np.nan,
                "pvalue": np.nan,
                "sign": "",
            }
        )
    else:
        row.update({"status": "evaluable", **fit})
    return row


def build_model_frame(
    cov: pd.DataFrame,
    expo_wide: pd.DataFrame,
    *,
    samples: list[str],
    active: list[str],
) -> pd.DataFrame:
    base = cov.set_index("sample_barcode15").reindex(samples).copy()
    base["treatment"] = base["treatment_exposed"].fillna(0.0)
    base["ancestry"] = base["ancestry"].fillna("Unknown")
    outcomes = build_clr_outcomes(expo_wide.reindex(samples).fillna(0.0), active)
    return base.join(outcomes)


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
    output_dir = assoc / "exploratory" / "h08b_sbs40_sbs5"
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = assoc / "covariate_denominator.json"
    cov_path = assoc / "h08_covariates.feather"
    h_path = (
        out_dir
        / "studies"
        / "tcga_mc3"
        / "mut"
        / "signatures"
        / "restricted_assignment_per_sample.feather"
    )
    for path in (manifest_path, cov_path, h_path):
        if not path.exists():
            raise SystemExit(f"missing required H08 artifact: {path}")

    manifest = json.loads(manifest_path.read_text())
    cov = pd.read_feather(cov_path)
    h = pd.read_feather(h_path).assign(
        b15=lambda df: df["sample_name"].astype(str).str.slice(0, 15)
    )
    passing = h[h["passes_count_floor"]]
    expo_wide = passing.pivot_table(
        index="b15", columns="signature", values="exposure", aggfunc="first"
    ).fillna(0.0)
    pass_b15 = set(expo_wide.index)

    module_rows = []
    inspection = []
    for arm, meta in manifest["per_stratum"].items():
        arm_samples = cov.loc[cov["arm"] == arm, "sample_barcode15"].tolist()
        samples = [sample for sample in arm_samples if sample in pass_b15]
        active = meta["active_signatures"]
        sbs40_parts = active_sbs40_parts(active)
        inspection.append(
            {
                "stratum": arm,
                "total_covariate_samples": len(arm_samples),
                "count_floor_passing_samples": len(samples),
                "sbs5_active": "SBS5" in active,
                "sbs40_active_parts": "|".join(sbs40_parts),
                "n_ranked_modules": len(_module_columns(meta["ranked_covariates"])),
            }
        )
        if "SBS5" not in active or not sbs40_parts:
            continue
        frame = build_model_frame(cov, expo_wide, samples=samples, active=active)
        for module in _module_columns(meta["ranked_covariates"]):
            module_rows.append(
                _fit_or_status(
                    frame,
                    PRIMARY_OUTCOME,
                    module,
                    family="module_primary_contrast",
                    stratum=arm,
                    covariate_class="nmf_module",
                )
            )
            for outcome in SECONDARY_OUTCOMES:
                module_rows.append(
                    _fit_or_status(
                        frame,
                        outcome,
                        module,
                        family="module_secondary_single_signature",
                        stratum=arm,
                        covariate_class="nmf_module",
                    )
                )

    module_grid = apply_bh(pd.DataFrame(module_rows), family_cols=["family"])
    module_grid["rank_in_family"] = (
        module_grid[module_grid["q_bh"].notna()]
        .groupby("family")["q_bh"]
        .rank(method="min")
        .reindex(module_grid.index)
    )

    target_rows = []
    target_status_rows = []
    luad_meta = manifest["per_stratum"]["LUAD"]
    luad_samples = [
        sample
        for sample in cov.loc[cov["arm"] == "LUAD", "sample_barcode15"]
        if sample in pass_b15
    ]
    luad_frame = build_model_frame(
        cov, expo_wide, samples=luad_samples, active=luad_meta["active_signatures"]
    )
    rsem_path = (
        Path(cfg["data_dir"])
        / cfg["h08_arm_studies"]["LUAD"]
        / "data_mrna_seq_v2_rsem.txt"
    )
    rsem = load_rsem_gene_matrix(rsem_path, TARGET_GENES)
    target_expr, target_status = build_target_expression(
        rsem, sample_ids=luad_samples, genes=list(TARGET_GENES)
    )
    target_status_rows.extend(target_status.to_dict("records"))
    luad_frame = luad_frame.join(target_expr)
    for status in target_status_rows:
        gene = status["gene"]
        if status["status"] != "evaluable":
            for outcome in (PRIMARY_OUTCOME, "clr_SBS5"):
                target_rows.append(
                    {
                        "stratum": "LUAD",
                        "family": "target_gene",
                        "outcome": outcome,
                        "covariate": gene,
                        "covariate_class": "target_gene",
                        "status": status["status"],
                        "n": 0,
                        "coef_std": np.nan,
                        "pvalue": np.nan,
                        "sign": "",
                    }
                )
            continue
        for outcome in (PRIMARY_OUTCOME, "clr_SBS5"):
            target_rows.append(
                _fit_or_status(
                    luad_frame,
                    outcome,
                    gene,
                    family="target_gene",
                    stratum="LUAD",
                    covariate_class="target_gene",
                )
            )
    target_grid = apply_bh(pd.DataFrame(target_rows), family_cols=["family"])

    module_out = output_dir / "h08b_sbs40_sbs5_module_contrast.feather"
    target_out = output_dir / "h08b_sbs40_sbs5_target_genes.feather"
    meta_out = output_dir / "h08b_sbs40_sbs5.meta.json"
    module_grid.to_feather(module_out)
    target_grid.to_feather(target_out)
    meta = {
        "task": "t182",
        "status": "exploratory_only",
        "plan": "plan:2026-06-01-t182-h08b-sbs40-sbs5-exploratory",
        "gate_note": "H08a remains [?]; this output cannot promote H08b.",
        "inputs": {
            "covariates": str(cov_path),
            "exposures": str(h_path),
            "denominator_manifest": str(manifest_path),
            "denominator_manifest_sha256": sha256(manifest_path),
            "luad_rsem": str(rsem_path),
        },
        "primary_outcome": PRIMARY_OUTCOME,
        "secondary_outcomes": list(SECONDARY_OUTCOMES),
        "min_model_n": MIN_MODEL_N,
        "clr_pseudocount": CLR_PSEUDOCOUNT,
        "inspection": inspection,
        "target_gene_status": target_status_rows,
    }
    meta_out.write_text(json.dumps(meta, indent=2, default=str))

    console.print(f"[green]wrote[/] {module_out} ({len(module_grid)} rows)")
    console.print(f"[green]wrote[/] {target_out} ({len(target_grid)} rows)")
    top = module_grid[
        (module_grid["family"] == "module_primary_contrast")
        & module_grid["q_bh"].notna()
    ].sort_values(["q_bh", "pvalue"])
    if not top.empty:
        r = top.iloc[0]
        console.print(
            f"  top exploratory contrast: {r['stratum']} {r['covariate']} "
            f"coef={r['coef_std']:.3g} q={r['q_bh']:.3g} n={int(r['n'])}"
        )
    console.print(
        "[yellow]exploratory only — no H08a/H08b promotion verdict is read.[/]"
    )


if __name__ == "__main__":
    main()
