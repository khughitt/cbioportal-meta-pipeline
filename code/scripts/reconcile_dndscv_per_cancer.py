# science:code
# status: workflow-owned
# science:end
#
# reconcile_dndscv_per_cancer.py (t131)
#
# Combine per-build dNdScv outputs back to a single per-cancer-type result.
# For mono-build cancer types this is essentially a pass-through; for the
# rare case where one cancer type spans both hg19 and hg38 sub-cohorts,
# emits a single row per gene with min(qglobal_cv) across builds plus a
# `dndscv_split_build = True` flag warning consumers that the underlying
# cohort was not actually pooled.
#
# Inputs (snek.input):
#   genes_inputs — list of paths to
#                  summary/mut/dndscv/per_cancer_per_build/{slug}/genes.feather
#                  for ALL slugs whose cancer_type matches snek.wildcards.cancer_slug
#   run_inputs   — matching list of summary/.../run.feather (one per slug)
#
# Outputs:
#   summary/mut/dndscv/per_cancer/{cancer_slug}/genes.feather
#   summary/mut/dndscv/per_cancer/{cancer_slug}/run.feather
#
# Output schema (per-gene):
#   symbol, cancer_type, dndscv_qglobal_cv, dndscv_significant_q05,
#   dndscv_input_status, dndscv_input_modality, dndscv_panel_only,
#   dndscv_n_samples, dndscv_n_variants, dndscv_split_build,
#   dndscv_refdb, dndscv_package_version, dndscv_git_sha
#
import pandas as pd

snek = snakemake  # type: ignore[name-defined]  # noqa: F821

genes_paths = list(snek.input.genes_inputs)
run_paths = list(snek.input.run_inputs)
cancer_slug = snek.wildcards["cancer_slug"]

if len(genes_paths) != len(run_paths):
    raise ValueError(
        f"reconcile_dndscv ({cancer_slug}): genes_inputs ({len(genes_paths)}) and "
        f"run_inputs ({len(run_paths)}) must have the same length"
    )


def _load_pair(genes_path: str, run_path: str) -> tuple[pd.DataFrame, pd.Series]:
    genes = pd.read_feather(genes_path)
    run = pd.read_feather(run_path).iloc[0]
    # dndscv may emit either `qglobal_cv` (when both subs + indels are tested,
    # outp=3) or `qallsubs_cv` (subs-only, our case since prepare_dndscv_input
    # restricts to SNVs). Normalize to a single internal name `qglobal_cv`.
    if "qglobal_cv" not in genes.columns and "qallsubs_cv" in genes.columns:
        genes = genes.rename(columns={"qallsubs_cv": "qglobal_cv"})
    return genes, run


# ---------------------------------------------------------------------------
# Load all per-build outputs.
# ---------------------------------------------------------------------------
pairs = [_load_pair(g, r) for g, r in zip(genes_paths, run_paths)]

# Sanity: cancer_type should be the same across all pairs (they're all sub-cohorts
# of one cancer type).
cancer_types = sorted({str(run["cancer_type"]) for _, run in pairs})
if len(cancer_types) != 1:
    raise ValueError(
        f"reconcile_dndscv ({cancer_slug}): per-build runs disagree on cancer_type: "
        f"{cancer_types}"
    )
cancer_type = cancer_types[0]

split_build = len(pairs) > 1
print(
    f"reconcile_dndscv_per_cancer ({cancer_slug}): {len(pairs)} build sub-cohort(s), "
    f"split_build={split_build}, cancer_type={cancer_type!r}"
)

# ---------------------------------------------------------------------------
# Per-build → per-gene rows, keyed on gene_name.
# ---------------------------------------------------------------------------
per_build_rows = []
for genes, run in pairs:
    if genes.empty:
        # The cohort ran but produced no rows (failed_qc / below_threshold).
        # Emit a sentinel row so downstream sees the cohort metadata.
        per_build_rows.append(
            pd.DataFrame(
                [
                    {
                        "symbol": pd.NA,
                        "qglobal_cv": pd.NA,
                        "build": str(run["build"]),
                        "refdb": str(run["refdb"]),
                        "modality": str(run["modality"]),
                        "panel_only": bool(run["panel_only"]),
                        "n_samples": int(run["n_samples"]),
                        "n_variants": int(run["n_variants_used"]),
                        "status": str(run["status"]),
                        "package_version": str(run["package_version"]),
                        "git_sha": str(run["git_sha"]),
                    }
                ]
            )
        )
        continue

    df = genes.rename(columns={"gene_name": "symbol"})[["symbol", "qglobal_cv"]].copy()
    df["build"] = str(run["build"])
    df["refdb"] = str(run["refdb"])
    df["modality"] = str(run["modality"])
    df["panel_only"] = bool(run["panel_only"])
    df["n_samples"] = int(run["n_samples"])
    df["n_variants"] = int(run["n_variants_used"])
    df["status"] = str(run["status"])
    df["package_version"] = str(run["package_version"])
    df["git_sha"] = str(run["git_sha"])
    per_build_rows.append(df)

stacked = pd.concat(per_build_rows, ignore_index=True)

# Drop sentinel rows (symbol is NA) when there's at least one real per-gene row
# for the cancer type. They're only there to carry cohort metadata when ALL
# sub-cohorts produced empty outputs.
has_real_rows = stacked["symbol"].notna().any()
if has_real_rows:
    stacked = stacked[stacked["symbol"].notna()].copy()

# ---------------------------------------------------------------------------
# Per-gene rollup: take min qglobal_cv across builds; carry forward the
# refdb/modality/sample-counts of the lower-q sub-cohort (or the only sub-cohort).
# ---------------------------------------------------------------------------
def _row_for_gene(symbol: str, grp: pd.DataFrame) -> dict:
    grp_with_q = grp.dropna(subset=["qglobal_cv"])
    if grp_with_q.empty:
        # All sub-cohorts produced no result for this gene.
        winner = grp.iloc[0]
        qglobal: object = pd.NA
    else:
        winner = grp_with_q.loc[grp_with_q["qglobal_cv"].astype(float).idxmin()]
        qglobal = float(winner["qglobal_cv"])

    # Cohort-aggregate: if multiple builds contributed for this cancer_type,
    # sum n_samples / n_variants and union modality.
    n_samples_total = int(grp["n_samples"].sum())
    n_variants_total = int(grp["n_variants"].sum())
    modalities = set(grp["modality"].astype(str).unique())
    if modalities <= {"wes"}:
        modality = "wes"
    elif modalities <= {"panel"}:
        modality = "panel"
    else:
        modality = "mixed"

    return {
        "symbol": symbol,
        "cancer_type": cancer_type,
        "dndscv_qglobal_cv": qglobal,
        "dndscv_input_modality": modality,
        "dndscv_panel_only": modality == "panel",
        "dndscv_n_samples": n_samples_total,
        "dndscv_n_variants": n_variants_total,
        "dndscv_split_build": split_build,
        "dndscv_refdb": str(winner["refdb"]),
        "dndscv_package_version": str(winner["package_version"]),
        "dndscv_git_sha": str(winner["git_sha"]),
        "_winner_status": str(winner["status"]),
    }


if has_real_rows:
    rows = [
        _row_for_gene(str(sym), grp)
        for sym, grp in stacked.groupby("symbol", sort=False)
    ]
    out = pd.DataFrame(rows)
else:
    # No real per-gene rows from any sub-cohort. Emit a single placeholder row
    # capturing the worst-case status across builds so downstream knows the
    # cancer type was attempted.
    statuses = list(stacked["status"].astype(str))
    # Status precedence: failed_qc > below_threshold > ok > anything_else.
    if "failed_qc" in statuses:
        winner_status = "failed_qc"
    elif "below_threshold" in statuses:
        winner_status = "below_threshold"
    else:
        winner_status = statuses[0]
    out = pd.DataFrame(
        [
            {
                "symbol": pd.NA,
                "cancer_type": cancer_type,
                "dndscv_qglobal_cv": pd.NA,
                "dndscv_input_modality": str(stacked["modality"].iloc[0]),
                "dndscv_panel_only": bool(stacked["panel_only"].iloc[0]),
                "dndscv_n_samples": int(stacked["n_samples"].sum()),
                "dndscv_n_variants": int(stacked["n_variants"].sum()),
                "dndscv_split_build": split_build,
                "dndscv_refdb": str(stacked["refdb"].iloc[0]),
                "dndscv_package_version": str(stacked["package_version"].iloc[0]),
                "dndscv_git_sha": str(stacked["git_sha"].iloc[0]),
                "_winner_status": winner_status,
            }
        ]
    )

# ---------------------------------------------------------------------------
# Compute dndscv_input_status and dndscv_significant_q05.
# Status precedence:
#   not_run                -> never set here (set by join step when whole cancer absent)
#   below_threshold        -> winner_status was "below_threshold" AND no q
#   failed_qc              -> winner_status was "failed_qc"   AND no q
#   tested_significant     -> qglobal_cv < 0.05
#   tested_not_significant -> qglobal_cv >= 0.05
# ---------------------------------------------------------------------------
def _classify_status(row: pd.Series) -> str:
    q = row["dndscv_qglobal_cv"]
    if pd.isna(q):
        ws = row.get("_winner_status", "failed_qc")
        if ws == "below_threshold":
            return "below_threshold"
        return "failed_qc"
    return "tested_significant" if float(q) < 0.05 else "tested_not_significant"


out["dndscv_input_status"] = out.apply(_classify_status, axis=1)
out["dndscv_significant_q05"] = out["dndscv_qglobal_cv"].apply(
    lambda q: pd.NA if pd.isna(q) else (float(q) < 0.05)
)

out = out.drop(columns=["_winner_status"])

# Final column order matches §"Schema contract on canonical feather" in the
# t131 design plan.
out = out[
    [
        "symbol",
        "cancer_type",
        "dndscv_qglobal_cv",
        "dndscv_significant_q05",
        "dndscv_input_status",
        "dndscv_input_modality",
        "dndscv_panel_only",
        "dndscv_n_samples",
        "dndscv_n_variants",
        "dndscv_split_build",
        "dndscv_refdb",
        "dndscv_package_version",
        "dndscv_git_sha",
    ]
]
out = out.reset_index(drop=True)
out.to_feather(snek.output.genes)

# Also propagate a per-cancer run summary.
run_summary = pd.DataFrame(
    [
        {
            "cancer_type": cancer_type,
            "n_builds": len(pairs),
            "split_build": split_build,
            "n_genes_emitted": int(out["symbol"].notna().sum()),
            "n_genes_significant_q05": int(
                ((~out["dndscv_significant_q05"].isna())
                 & out["dndscv_significant_q05"].fillna(False).astype(bool)).sum()
            ),
        }
    ]
)
run_summary.to_feather(snek.output.run)

print(
    f"reconcile_dndscv_per_cancer ({cancer_slug}): wrote {len(out)} rows "
    f"({int(out['symbol'].notna().sum())} with valid symbol)"
)
