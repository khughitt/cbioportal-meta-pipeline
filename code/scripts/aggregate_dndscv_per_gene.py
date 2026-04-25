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

snek = snakemake  # type: ignore[name-defined]  # noqa: F821

paths = list(snek.input)
print(f"aggregate_dndscv_per_gene: reading {len(paths):,} per-cancer outputs")

frames = []
for path in paths:
    df = pd.read_feather(path)
    if df.empty:
        continue
    frames.append(df)

if not frames:
    print("aggregate_dndscv_per_gene: no inputs; writing empty pooled feather")
    pd.DataFrame(
        columns=pd.Index(
            [
                "symbol",
                "min_qglobal",
                "n_cancers_significant_q05",
                "n_cancers_significant_q01",
                "n_cancers_tested",
                "best_cancer_type",
            ]
        )
    ).to_feather(snek.output[0])
    raise SystemExit(0)

stacked = pd.concat(frames, ignore_index=True)
# Drop rows with no symbol (placeholder rows from cancer types with no
# real per-gene results).
stacked = stacked[stacked["symbol"].notna()].copy()
stacked["symbol"] = stacked["symbol"].astype(str)
print(f"aggregate_dndscv_per_gene: {len(stacked):,} (gene, cancer_type) rows total")

if stacked.empty:
    # All per-cancer outputs were sentinel-only (every cancer cohort hit
    # failed_qc or below_threshold). Emit an empty pooled feather with the
    # canonical schema so downstream rules see a valid file.
    print("aggregate_dndscv_per_gene: no real (symbol, cancer_type) rows after filter; writing empty pooled feather")
    pd.DataFrame(
        columns=pd.Index(
            [
                "symbol",
                "min_qglobal",
                "n_cancers_significant_q05",
                "n_cancers_significant_q01",
                "n_cancers_tested",
                "best_cancer_type",
            ]
        )
    ).to_feather(snek.output[0])
    raise SystemExit(0)


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


rows = [_per_gene(str(sym), grp) for sym, grp in stacked.groupby("symbol", sort=True)]
pooled = pd.DataFrame(rows)

# `groupby(...).apply` flattens to long-format with `symbol` carried via the
# as_index=False; double-check shape.
if "symbol" not in pooled.columns:
    raise RuntimeError(
        "aggregate_dndscv_per_gene: groupby+apply produced unexpected schema "
        f"({list(pooled.columns)})"
    )

pooled = pooled[
    [
        "symbol",
        "min_qglobal",
        "n_cancers_significant_q05",
        "n_cancers_significant_q01",
        "n_cancers_tested",
        "best_cancer_type",
    ]
].sort_values(by="min_qglobal", na_position="last").reset_index(drop=True)

pooled.to_feather(snek.output[0])
print(
    f"aggregate_dndscv_per_gene: wrote {len(pooled):,} genes "
    f"({int(pooled['min_qglobal'].notna().sum()):,} with non-null min_qglobal) "
    f"to {snek.output[0]}"
)
