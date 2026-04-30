"""External validation of pan-cancer dNdScv ranking against
existing in-project driver-list overlays.

First pass for task t146; uses only the overlays already shipped in
the annotated feather (Bailey 2018, COSMIC CGC tier 1/2). Full
IntOGen 2024 + Martincorena 2017 comparisons are blocked on dataset
acquisition (task t171).

Computes per-gene aggregate dNdScv signal across cancer types,
ranks pan-cancer, and reports recovery@K + Jaccard@K + odds ratios
versus each external list.

Usage:

  uv run python code/scripts/validate_dndscv_external.py \
    --annotated /data/packages/cbioportal/pan-cancer/summary/mut/table/gene_cancer_study_ratio_annotated_dndscv.feather \
    --pooled    /data/packages/cbioportal/pan-cancer/summary/mut/table/dndscv_pooled.feather \
    --out-dir   /data/packages/cbioportal/pan-cancer/summary/external-validation
"""

from __future__ import annotations

from pathlib import Path

import click
import pandas as pd
from scipy.stats import fisher_exact

from symbol_normalization import expand_reference_symbols_to_universe

K_VALUES = (10, 25, 50, 100, 250, 500)


def odds_ratio_at_k(
    top_set: set[str], list_set: set[str], universe: set[str]
) -> tuple[float, float]:
    a = len(top_set & list_set)
    b = len(top_set - list_set)
    c = len((list_set - top_set) & universe)
    d = len(universe - top_set - list_set)
    if min(a + b, a + c, b + d, c + d) == 0:
        return float("nan"), float("nan")
    or_, p = fisher_exact([[a, b], [c, d]], alternative="greater")
    return float(or_), float(p)


def extract_reference_sets(
    annotated: pd.DataFrame, universe: set[str]
) -> dict[str, set[str]]:
    """Extract Bailey/CGC references, expanding bare symbols to dNdScv isoforms."""
    bailey = _symbols_where(annotated, "bailey2018_driver", universe)
    cgc_t1 = _symbols_where(annotated, "cgc_tier_1", universe)
    cgc_t2 = _symbols_where(annotated, "cgc_tier_2", universe)
    return {
        "bailey2018": bailey,
        "cgc_tier1": cgc_t1,
        "cgc_tier1_or_2": cgc_t1 | cgc_t2,
    }


def _symbols_where(
    annotated: pd.DataFrame, flag_col: str, universe: set[str]
) -> set[str]:
    if flag_col not in annotated.columns:
        return set()
    flags = annotated[flag_col].fillna(False).astype(bool)
    reference_symbols = annotated.loc[flags, "symbol"].dropna().astype(str)
    return expand_reference_symbols_to_universe(reference_symbols, universe)


@click.command()
@click.option("--annotated", "annotated_path", type=Path, required=True)
@click.option(
    "--pooled",
    "pooled_path",
    type=Path,
    required=True,
    help="dndscv_pooled.feather (per-gene rollup)",
)
@click.option("--out-dir", "out_dir", type=Path, required=True)
def main(annotated_path: Path, pooled_path: Path, out_dir: Path) -> None:
    annot = pd.read_feather(annotated_path)
    pooled = pd.read_feather(pooled_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"pooled cols: {list(pooled.columns)}")
    print(f"annotated rows: {len(annot)}; pooled rows: {len(pooled)}")

    pooled_ranked = pooled.sort_values(
        ["min_qglobal", "n_cancers_significant_q05"],
        ascending=[True, False],
    )
    print(
        "rank: min_qglobal asc, then n_cancers_significant_q05 desc (t144 tiebreaker)"
    )

    universe = set(pooled_ranked["symbol"].dropna().astype(str).unique())
    refs = extract_reference_sets(annot, universe)
    print(f"universe |U| = {len(universe)}")
    print(f"|Bailey ∩ U| = {len(refs['bailey2018'])}")
    print(f"|CGC tier1 ∩ U| = {len(refs['cgc_tier1'])}")
    print(f"|CGC tier1+2 ∩ U| = {len(refs['cgc_tier1_or_2'])}")

    rows: list[dict] = []
    for k in K_VALUES:
        top_genes = set(pooled_ranked.head(k)["symbol"].dropna().astype(str).unique())
        for name, ref_set in refs.items():
            inter = top_genes & ref_set
            jaccard = (
                len(inter) / len(top_genes | ref_set)
                if (top_genes | ref_set)
                else float("nan")
            )
            recovery = len(inter) / len(top_genes) if top_genes else float("nan")
            ref_recovery = len(inter) / len(ref_set) if ref_set else float("nan")
            or_, p_or = odds_ratio_at_k(top_genes, ref_set, universe)
            rows.append(
                {
                    "k": k,
                    "reference": name,
                    "ref_size": len(ref_set),
                    "top_size": len(top_genes),
                    "intersection": len(inter),
                    "recovery_in_top": recovery,
                    "recovery_of_ref": ref_recovery,
                    "jaccard": jaccard,
                    "odds_ratio_enrichment": or_,
                    "fisher_pvalue_one_sided": p_or,
                }
            )

    summary = pd.DataFrame(rows)
    summary_path = out_dir / "dndscv_external_validation.feather"
    summary.to_feather(summary_path)

    print()
    print(f"wrote: {summary_path}")
    print()
    with pd.option_context(
        "display.max_rows",
        None,
        "display.width",
        180,
        "display.float_format",
        "{:0.4f}".format,
    ):
        print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
