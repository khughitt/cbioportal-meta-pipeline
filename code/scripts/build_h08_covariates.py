# science:code
# status: workflow-owned
# science:end
"""Assemble + FREEZE the h08 covariate table and the rank-gate denominator manifest (t199 WP1).

WP1 of `plan:2026-05-31-t199-h08-association-core`. This builds one per-sample covariate table
across the 7 MC3 arm strata and writes the **frozen denominator manifest BEFORE any association
rank is computed** (pre-reg §Metric Selection Rationale — the top-3 threshold is meaningless
without a frozen denominator). It does NOT run any model; WP2 consumes these two artifacts.

Frozen-before-ranks decisions recorded in the manifest (all delegated to run time by the pre-reg;
none is an amendment):

- **Covariate split (makes the F4 rank statistic well-defined).** The pre-reg covariate universe is
  split into (a) ADJUSTMENT covariates — conditioned on, never ranked: ancestry, race, treatment,
  plus the tissue stratifier and the (constant) MC3 study/assay; and (b) RANKED scalar candidate
  covariates — continuous / binary / ordinal, each with a single signed standardized coefficient.
  Multi-level nominal fields (oncotree_code, cancer_type_detailed) have no scalar effect and are
  carried as context only. The per-stratum rank-gate denominator = count of ranked covariates that
  are *testable* (>=2 distinct non-missing values) in that stratum (F10 degeneracy drop).
- **Two denominators (F1).** The per-tissue arms (A/B) include the K NMF expression modules in the
  ranked set; the pooled Arm-C model EXCLUDES modules (the per-tissue NMF bases are
  non-commensurable — different latent factors, different K) — modules enter Arm C only as
  tissue-nested nuisance. Both denominators are written here.
- **F4 rank statistic.** Per (covariate, signature, stratum): one adjusted within-tissue model with
  the CLR coordinate of the target signature as outcome; ranking statistic = the signed
  standardized coefficient of the covariate of interest. Recorded here; applied in WP2.
- **UV proxy (KD4).** SKCM `TUMOR_TISSUE_SITE` (pipe-delimited multi-site) → frozen sun-exposure
  ordinal (max tier over the sample's body-site tokens); `SAMPLE_TYPE` carried separately.
- **Active-signature rule.** A signature enters a stratum's denominator iff it has exposure > 0 in
  >= 5% of that stratum's samples (COSMIC v3.4). Computed from the t197 H table.

LEAKAGE FIREWALL: no covariate is a function of the signature exposures `H`. TMB is taken from the
independent clinical `TMB_NONSYNONYMOUS` field (not from H burden); the H table is not read except to
compute the active-signature set + the per-stratum sample spine.
"""

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
from detect_polymerase_hotspots import detect_hotspots_per_sample  # noqa: E402

console = Console()
logger = logging.getLogger("build_h08_covariates")
if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s %(name)s: %(message)s"
    )

# --- frozen constants (written into the manifest) ---
ACTIVE_SIGNATURE_MIN_FRAC = 0.05
MSI_SENSOR_H_THRESHOLD = 10.0  # MSISensor score >= 10 → MSI-H (cBioPortal convention)
HYPERMUTATOR_TMB_THRESHOLD = 10.0  # mut/Mb, Campbell 2017 absolute view
MAX_MODULE_K = 10  # widest arm (BRCA); narrower arms leave module_06..10 NaN

# cBioPortal / TCGA missing-value sentinels → NaN
MISSING = {
    "",
    "NA",
    "N/A",
    "[Not Available]",
    "[Unknown]",
    "[Not Applicable]",
    "[Not Evaluated]",
    "[Discrepancy]",
    "[Pending]",
    "Not Available",
    "Unknown",
    "[Completed]",
    "[Not Reported]",
}

# Frozen UV sun-exposure ordinal (KD4): max tier over a sample's pipe-delimited TUMOR_TISSUE_SITE.
UV_SITE_TIER = {
    "Head and Neck": 2,  # high sun
    "Extremities": 2,
    "Regional Cutaneous or Subcutaneous Tissue": 2,
    "Trunk": 1,  # intermediate
    "Regional Lymph Node": 0,  # sun-shielded / non-cutaneous
    "Distant Metastasis": 0,
    "Other": 0,
    # "Primary" / "NA" tokens are non-anatomical qualifiers → ignored (no tier)
}

# Ranked scalar candidate covariates (each has a single signed standardized coefficient).
# arm scope: "all" | "skcm" | "lung". Modules are added dynamically per arm.
RANKED_SCALAR = [
    ("age", "all", "continuous"),
    ("sex_male", "all", "binary"),
    ("stage_ordinal", "all", "ordinal"),
    ("sample_type_met", "all", "binary"),
    ("msi_sensor_score", "all", "continuous"),
    ("is_msi_h", "all", "binary"),
    ("tmb_nonsynonymous", "all", "continuous"),
    ("is_hypermutator", "all", "binary"),
    ("pole_hotspot", "all", "binary"),
    ("pold1_hotspot", "all", "binary"),
    (
        "apobec3ab_joint",
        "all",
        "continuous",
    ),  # Arm-C covariate of interest (t180 joint score)
    ("uv_sun_exposure_ordinal", "skcm", "ordinal"),  # Arm-A covariate of interest
    ("pack_years", "lung", "continuous"),  # Arm-B covariate of interest
]
# Conditioned on, never ranked.
ADJUSTMENT_COVARIATES = [
    "ancestry",
    "race",
    "treatment_exposed",
    "tissue(stratifier)",
    "study(MC3 constant)",
]
# In the table for context / exploratory use, not in the ranked denominator.
CONTEXT_COVARIATES = [
    "oncotree_code",
    "cancer_type_detailed",
    "apobec3a",
    "apobec3b",
    "ever_smoker",
]

ARM_C_STRATA = ["BLCA", "BRCA", "CESC", "HNSC", "LUAD", "LUSC"]


def _clean(series: pd.Series) -> pd.Series:
    s = series.astype("string").str.strip()
    return s.where(~s.isin(MISSING), other=pd.NA)


def _to_num(series: pd.Series) -> pd.Series:
    return pd.to_numeric(_clean(series), errors="coerce")


def _read_clinical(path: Path) -> pd.DataFrame:
    # cBioPortal clinical: 4 comment rows, row 5 = header.
    return pd.read_csv(path, sep="\t", skiprows=4, dtype=str)


def _stage_ordinal(series: pd.Series) -> pd.Series:
    s = _clean(series).str.upper().str.replace("STAGE", "", regex=False).str.strip()
    out = pd.Series(np.nan, index=series.index, dtype=float)
    # longest-prefix first so IV/III beat I/II
    for token, val in [("IV", 4), ("III", 3), ("II", 2), ("I", 1)]:
        hit = s.str.startswith(token, na=False) & out.isna()
        out[hit] = val
    return out


def _uv_ordinal(series: pd.Series) -> pd.Series:
    def tier(val: object) -> float:
        if pd.isna(val):
            return np.nan
        tiers = [
            UV_SITE_TIER[t.strip()]
            for t in str(val).split("|")
            if t.strip() in UV_SITE_TIER
        ]
        return float(max(tiers)) if tiers else np.nan

    return series.map(tier)


def _load_rsem_apobec(path: Path) -> pd.DataFrame:
    """Return APOBEC3A / APOBEC3B log2(RSEM+1), indexed by 15-char sample barcode."""
    df = pd.read_csv(path, sep="\t", dtype={"Hugo_Symbol": str})
    df = df[df["Hugo_Symbol"].isin(["APOBEC3A", "APOBEC3B"])].drop(
        columns=[c for c in ("Entrez_Gene_Id",) if c in df.columns]
    )
    df = (
        df.groupby("Hugo_Symbol", sort=False).max(numeric_only=True).T
    )  # samples × {A3A,A3B}
    df.index = df.index.str.slice(0, 15)
    df = df[~df.index.duplicated(keep="first")]
    log = np.log2(df.clip(lower=0) + 1.0)
    out = pd.DataFrame(index=df.index)
    out["apobec3a"] = log.get("APOBEC3A")
    out["apobec3b"] = log.get("APOBEC3B")
    out["apobec3ab_joint"] = np.log2(
        df.get("APOBEC3A", 0.0).clip(lower=0)
        + df.get("APOBEC3B", 0.0).clip(lower=0)
        + 1.0
    )
    return out


def build_arm(
    arm: str, study: str, spine15: list[str], data_dir: Path, out_dir: Path
) -> pd.DataFrame:
    study_dir = data_dir / study
    sample = _read_clinical(study_dir / "data_clinical_sample.txt")
    patient = _read_clinical(study_dir / "data_clinical_patient.txt")
    sample = sample.assign(b15=sample["SAMPLE_ID"].str.slice(0, 15)).set_index("b15")
    sample = sample[~sample.index.duplicated(keep="first")]
    patient = patient.set_index("PATIENT_ID")
    patient = patient[~patient.index.duplicated(keep="first")]

    df = pd.DataFrame(index=pd.Index(spine15, name="sample_barcode15"))
    df["arm"] = arm
    df["patient12"] = df.index.str.slice(0, 12)

    # sample-level clinical
    df["oncotree_code"] = sample["ONCOTREE_CODE"].reindex(df.index).pipe(_clean)
    df["cancer_type_detailed"] = (
        sample["CANCER_TYPE_DETAILED"].reindex(df.index).pipe(_clean)
    )
    st = _clean(sample["SAMPLE_TYPE"].reindex(df.index))
    df["sample_type_met"] = (
        st.str.contains("Metasta", case=False, na=False)
        .where(st.notna(), other=pd.NA)
        .astype("float")
    )
    df["msi_sensor_score"] = _to_num(sample["MSI_SENSOR_SCORE"].reindex(df.index))
    df["is_msi_h"] = (df["msi_sensor_score"] >= MSI_SENSOR_H_THRESHOLD).where(
        df["msi_sensor_score"].notna(), other=np.nan
    )
    df["tmb_nonsynonymous"] = _to_num(sample["TMB_NONSYNONYMOUS"].reindex(df.index))
    df["is_hypermutator"] = (
        df["tmb_nonsynonymous"] >= HYPERMUTATOR_TMB_THRESHOLD
    ).where(df["tmb_nonsynonymous"].notna(), other=np.nan)
    df["uv_sun_exposure_ordinal"] = (
        _uv_ordinal(sample["TUMOR_TISSUE_SITE"].reindex(df.index))
        if arm == "SKCM"
        else np.nan
    )

    # patient-level clinical (broadcast on 12-char barcode)
    pat = patient.reindex(df["patient12"])
    pat.index = df.index
    df["age"] = _to_num(pat["AGE"])
    sex = _clean(pat["SEX"]).str.upper()
    df["sex_male"] = sex.eq("MALE").where(sex.notna(), other=pd.NA).astype("float")
    df["race"] = _clean(pat["RACE"])
    df["ancestry"] = _clean(pat["GENETIC_ANCESTRY_LABEL"])
    df["stage_ordinal"] = _stage_ordinal(pat["AJCC_PATHOLOGIC_TUMOR_STAGE"])
    neoadj = _clean(pat["HISTORY_NEOADJUVANT_TRTYN"]).str.upper()
    df["treatment_exposed"] = (
        neoadj.eq("YES").where(neoadj.notna(), other=pd.NA).astype("float")
    )

    # expression: APOBEC3A/B + modules
    apobec = _load_rsem_apobec(study_dir / "data_mrna_seq_v2_rsem.txt")
    for c in ("apobec3a", "apobec3b", "apobec3ab_joint"):
        df[c] = apobec[c].reindex(df.index)
    loadings = pd.read_feather(
        out_dir / "expression_modules" / arm / "nmf_sample_loadings.feather"
    )
    loadings = loadings.assign(
        b15=loadings["sample_id"].astype(str).str.slice(0, 15)
    ).set_index("b15")
    mod_cols = [c for c in loadings.columns if c.startswith("module_")]
    for i in range(1, MAX_MODULE_K + 1):
        col = f"module_{i:02d}"
        df[col] = loadings[col].reindex(df.index) if col in mod_cols else np.nan
    return df


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
    data_dir = Path(cfg["data_dir"])
    out_dir = Path(cfg["out_dir"])
    arm_studies: dict[str, str] = cfg["h08_arm_studies"]
    assoc_dir = out_dir / "association"
    assoc_dir.mkdir(parents=True, exist_ok=True)

    # --- spine: 15-char barcodes per arm from the t197 H table; assert 1 sample / case (F7) ---
    h = pd.read_feather(
        out_dir
        / "studies"
        / "tcga_mc3"
        / "mut"
        / "signatures"
        / "restricted_assignment_per_sample.feather"
    )
    h = h.assign(
        b15=h["sample_name"].str.slice(0, 15), b12=h["sample_name"].str.slice(0, 12)
    )
    spine: dict[str, list[str]] = {}
    for arm in arm_studies:
        rows = h[h["cancer_type"] == arm].drop_duplicates("b15")
        if rows["b12"].duplicated().any():
            raise SystemExit(f"F7 violated: arm {arm} has >1 MC3 sample for some case")
        spine[arm] = sorted(rows["b15"])
        logger.info("spine %s: n=%d (1 sample/case asserted)", arm, len(spine[arm]))

    # --- per-arm covariate assembly ---
    frames = [
        build_arm(arm, study, spine[arm], data_dir, out_dir)
        for arm, study in arm_studies.items()
    ]
    cov = pd.concat(frames).reset_index()

    # --- POLE/POLD1 hotspots from the MC3 MAF (left-join, absent = False) ---
    mut = pd.read_feather(
        out_dir / "studies" / "tcga_mc3" / "mut" / "table" / "mut.feather"
    )
    hot = detect_hotspots_per_sample(mut)
    hot = hot.assign(b15=hot["sample_id_tumor"].astype(str).str.slice(0, 15)).set_index(
        "b15"
    )
    cov["pole_hotspot"] = (
        cov["sample_barcode15"]
        .map(hot["pole_hotspot_detected"])
        .fillna(False)
        .astype(float)
    )
    cov["pold1_hotspot"] = (
        cov["sample_barcode15"]
        .map(hot["pold1_hotspot_detected"])
        .fillna(False)
        .astype(float)
    )

    # --- smoking (Arm-B): patient-level join on 12-char barcode (latin-1 TCGA biotab) ---
    sm = pd.read_csv(smoking, sep="\t", dtype=str, low_memory=False, encoding="latin-1")
    sm = sm.assign(
        b12=sm["bcr_patient_barcode"].astype(str).str.slice(0, 12)
    ).set_index("b12")
    sm = sm[~sm.index.duplicated(keep="first")]
    cov["pack_years"] = _to_num(cov["patient12"].map(sm["number_pack_years_smoked"]))
    hist = _to_num(cov["patient12"].map(sm["tobacco_smoking_history"]))
    cov["ever_smoker"] = (hist >= 2).where(
        hist.notna(), other=np.nan
    )  # 1=never; 2-5=ever
    # pack-years/ever only meaningful in lung; null elsewhere so they don't enter other strata's denominator
    nonlung = ~cov["arm"].isin(["LUAD", "LUSC"])
    cov.loc[nonlung, ["pack_years", "ever_smoker"]] = np.nan

    # --- active-signature set per stratum (>=5% of stratum samples with exposure>0) ---
    active: dict[str, list[str]] = {}
    for arm in arm_studies:
        sub = h[h["cancer_type"] == arm]
        n = sub["b15"].nunique()
        frac = sub.assign(pos=sub["exposure"] > 0).groupby("signature")["pos"].sum() / n
        active[arm] = sorted(frac[frac >= ACTIVE_SIGNATURE_MIN_FRAC].index)
    # Arm-C pooled active set: exposure>0 in >=5% of the pooled APOBEC-six samples
    poolc = h[h["cancer_type"].isin(ARM_C_STRATA)]
    npool = poolc["b15"].nunique()
    fracc = (
        poolc.assign(pos=poolc["exposure"] > 0).groupby("signature")["pos"].sum()
        / npool
    )
    active_pooled = sorted(fracc[fracc >= ACTIVE_SIGNATURE_MIN_FRAC].index)

    # --- realized ranked denominator per stratum (testable = >=2 distinct non-missing) ---
    def testable(frame: pd.DataFrame, col: str) -> bool:
        return col in frame.columns and frame[col].dropna().nunique() >= 2

    ranked_all = [name for name, _, _ in RANKED_SCALAR]
    module_cols = [f"module_{i:02d}" for i in range(1, MAX_MODULE_K + 1)]
    per_stratum: dict[str, dict] = {}
    for arm in arm_studies:
        f = cov[cov["arm"] == arm]
        scalar_ok = [c for c in ranked_all if testable(f, c)]
        mods_ok = [c for c in module_cols if testable(f, c)]
        ranked = scalar_ok + mods_ok  # per-tissue: modules INCLUDED (F1)
        per_stratum[arm] = {
            "n_samples": int(len(f)),
            "ranked_covariates": ranked,
            "n_ranked_covariates": len(ranked),
            "modules_K": len(mods_ok),
            "active_signatures": active[arm],
            "n_active_signatures": len(active[arm]),
        }

    # Arm-C pooled denominator: modules EXCLUDED (F1)
    fc = cov[cov["arm"].isin(ARM_C_STRATA)]
    c_scalar = [c for c in ranked_all if testable(fc, c)]
    arm_c = {
        "strata": ARM_C_STRATA,
        "n_samples": int(len(fc)),
        "ranked_covariates": c_scalar,
        "n_ranked_covariates": len(c_scalar),
        "modules_excluded": True,
        "active_signatures": active_pooled,
        "n_active_signatures": len(active_pooled),
    }

    manifest = {
        "frozen_at": "2026-05-31",
        "task": "t199",
        "plan": "plan:2026-05-31-t199-h08-association-core",
        "leakage_firewall": "no covariate is a function of H; TMB from clinical TMB_NONSYNONYMOUS (independent of exposures)",
        "rank_statistic": {
            "model": "one adjusted within-tissue model per (covariate, signature, stratum)",
            "outcome": "CLR coordinate of the target signature exposure",
            "statistic": "signed standardized coefficient of the covariate of interest (sign read directly)",
            "fdr": "BH across the full covariate×signature×stratum grid; q<0.05",
            "note": "WP2 applies this; frozen here before any rank (F4).",
        },
        "covariate_split": {
            "ranked_scalar": [
                {"name": n, "scope": s, "encoding": e} for n, s, e in RANKED_SCALAR
            ],
            "ranked_modules": module_cols,
            "adjustment_covariates": ADJUSTMENT_COVARIATES,
            "context_covariates": CONTEXT_COVARIATES,
            "rationale": "ranked covariates are scalar so the signed standardized coefficient (F4) is well-defined; multi-level nominal fields are adjustment/context only.",
        },
        "frozen_rules": {
            "active_signature_min_frac": ACTIVE_SIGNATURE_MIN_FRAC,
            "cosmic_version": cfg.get("signature_assignment_cosmic_version"),
            "msi_sensor_h_threshold": MSI_SENSOR_H_THRESHOLD,
            "hypermutator_tmb_threshold": HYPERMUTATOR_TMB_THRESHOLD,
            "uv_site_tier_map": UV_SITE_TIER,
            "uv_rule": "max sun-exposure tier over pipe-delimited TUMOR_TISSUE_SITE tokens (KD4)",
            "clr_pseudocount": cfg.get("signature_ratio_pseudocount", 0.5),
            "arm_c_modules_excluded": True,
        },
        "denominators": {
            "per_tissue_arms": {
                arm: per_stratum[arm]["n_ranked_covariates"] for arm in arm_studies
            },
            "pooled_arm_c": arm_c["n_ranked_covariates"],
        },
        "per_stratum": per_stratum,
        "arm_c_pooled": arm_c,
    }

    cov_out = assoc_dir / "h08_covariates.feather"
    man_out = assoc_dir / "covariate_denominator.json"
    cov.to_feather(cov_out)
    man_out.write_text(json.dumps(manifest, indent=2, default=str))

    # --- report ---
    console.print(
        f"[green]wrote[/] {cov_out}  ({cov.shape[0]} samples × {cov.shape[1]} cols)"
    )
    console.print(f"[green]wrote[/] {man_out}")
    for arm in arm_studies:
        s = per_stratum[arm]
        console.print(
            f"  [bold]{arm}[/] n={s['n_samples']}  ranked_covars={s['n_ranked_covariates']} "
            f"(modules_K={s['modules_K']})  active_sigs={s['n_active_signatures']}"
        )
    console.print(
        f"  [bold]Arm-C pooled[/] n={arm_c['n_samples']}  ranked_covars={arm_c['n_ranked_covariates']} "
        f"(modules excluded)  active_sigs={arm_c['n_active_signatures']}"
    )
    # loud missingness for the three confirmatory covariates of interest
    for arm, col in [
        ("SKCM", "uv_sun_exposure_ordinal"),
        ("LUAD", "pack_years"),
        ("LUSC", "pack_years"),
    ]:
        f = cov[cov["arm"] == arm]
        comp = f[col].notna().mean()
        console.print(f"  completeness {arm}.{col}: {comp:.0%}")


if __name__ == "__main__":
    main()
