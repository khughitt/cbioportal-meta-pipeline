#
# aggregate_dndscv_per_gene.py (t131)
#
# Per-gene pan-cancer rollup across the per-cancer reconciled outputs.
# Used by `compare_three_way_rankings.py` to build the per-gene three-way
# ranking comparison feather.
#
# Inputs (snek.input):
#   list of summary/mut/dndscv/per_cancer/{cancer_slug}/genes.feather
#
# Output (snek.output[0]):
#   summary/mut/table/dndscv_pooled.feather
#
# Per-gene rollup rule (min-q across cancer types):
#   min_qglobal              = min(dndscv_qglobal_cv) across cancer types
#                              where the gene has a non-null q
#   n_cancers_significant_q05 = count of cancer types with q < 0.05
#   n_cancers_significant_q01 = count of cancer types with q < 0.01
#   n_cancers_tested          = count of cancer types where the gene appeared
#                              in any per-cancer dndscv output (any status)
#   best_cancer_type          = cancer type achieving the min q (NaN if all q NaN)
#
# Rationale: with per-cancer-type combined MAFs, cohorts are biologically
# meaningful (one cancer type's selection regime). A gene that is a strong
# driver in even one cancer type should rank high pan-cancer; this is what
# min-q captures. Stouffer would dilute strong-but-tissue-specific drivers
# (BRAF in melanoma, KRAS in pancreatic) by averaging in non-significant
# signal from unrelated cancer types.
#
import pandas as pd

POOLED_SCHEMA = [
    "symbol",
    "min_qglobal",
    "n_cancers_significant_q05",
    "n_cancers_significant_q01",
    "n_cancers_tested",
    "best_cancer_type",
]


def _empty_pooled() -> pd.DataFrame:
    return pd.DataFrame(columns=pd.Index(POOLED_SCHEMA))


def _per_gene(symbol: str, grp: pd.DataFrame) -> dict:
    q = grp["dndscv_qglobal_cv"].astype(float)
    has_q = q.notna()
    n_tested = int(grp.shape[0])
    if not has_q.any():
        return {
            "symbol": symbol,
            "min_qglobal": pd.NA,
            "n_cancers_significant_q05": 0,
            "n_cancers_significant_q01": 0,
            "n_cancers_tested": n_tested,
            "best_cancer_type": pd.NA,
        }
    qmin = float(q[has_q].min())
    best_idx = q[has_q].astype(float).idxmin()
    best_cancer = str(grp.loc[best_idx, "cancer_type"])
    return {
        "symbol": symbol,
        "min_qglobal": qmin,
        "n_cancers_significant_q05": int(((q < 0.05) & has_q).sum()),
        "n_cancers_significant_q01": int(((q < 0.01) & has_q).sum()),
        "n_cancers_tested": n_tested,
        "best_cancer_type": best_cancer,
    }


def aggregate_dndscv_per_gene(per_cancer_frames: list[pd.DataFrame]) -> pd.DataFrame:
    """Roll per-cancer dNdScv outputs into a per-gene pan-cancer summary.

    Each input frame is one per-cancer-type genes.feather as produced by
    `reconcile_dndscv_per_cancer.py`. Sentinel rows (where ``symbol`` is
    NA, indicating a cohort that hit `failed_qc` or `below_threshold`) are
    filtered before the rollup.

    Returns a DataFrame with the canonical schema (``POOLED_SCHEMA``);
    empty-but-schema-conforming when no input frame contains real per-gene
    rows.
    """
    real_frames = [df for df in per_cancer_frames if not df.empty]
    if not real_frames:
        return _empty_pooled()

    stacked = pd.concat(real_frames, ignore_index=True)
    stacked = stacked[stacked["symbol"].notna()].copy()

    if stacked.empty:
        # Every per-cancer feather was sentinel-only.
        return _empty_pooled()

    stacked["symbol"] = stacked["symbol"].astype(str)
    rows = [
        _per_gene(str(sym), grp) for sym, grp in stacked.groupby("symbol", sort=True)
    ]
    pooled = pd.DataFrame(rows)
    if "symbol" not in pooled.columns:
        raise RuntimeError(
            "aggregate_dndscv_per_gene: groupby produced unexpected schema "
            f"({list(pooled.columns)})"
        )
    return (
        pooled[POOLED_SCHEMA]
        .sort_values(by="min_qglobal", na_position="last")
        .reset_index(drop=True)
    )


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    paths = list(snek.input)
    print(f"aggregate_dndscv_per_gene: reading {len(paths):,} per-cancer outputs")
    per_cancer_frames = [pd.read_feather(p) for p in paths]
    pooled = aggregate_dndscv_per_gene(per_cancer_frames)
    pooled.to_feather(snek.output[0])
    print(
        f"aggregate_dndscv_per_gene: wrote {len(pooled):,} genes "
        f"({int(pooled['min_qglobal'].notna().sum()):,} with non-null min_qglobal) "
        f"to {snek.output[0]}"
    )


if "snakemake" in globals():
    _run_via_snakemake()
