"""Leave-one-study-out (LOSO) ranking-stability analysis for top-N
gene-cancer associations.

Closes task t149.

For each (analysis_view, excluded_study, K), compares the K-element
top set produced by the base pan-cancer pooled meta-analysis against
the K-element top set produced when one study is held out, using:

  - top-K is defined as the K (cancer, gene) pairs with the largest
    `pooled_rate` among rows with `status == "ok"`.
  - holdout top-K is defined identically against `holdout_pooled_rate`
    among rows with `holdout_status == "ok"`.

Outputs:
  summary/loso/loso_topn_overlap.feather
    Per (analysis_view, excluded_study, K): jaccard, recovery,
    base_set_size, hold_set_size, intersection_size.

  summary/loso/loso_summary.feather
    Per (analysis_view, K): median / IQR / min recovery and Jaccard
    across the 10 LOSO iterations.

Run from project root:

  uv run python code/scripts/analyze_loso_replication.py \
    --base /data/packages/cbioportal/pan-cancer/summary/mut/table/gene_cancer_pooled.feather \
    --loo /data/packages/cbioportal/pan-cancer/summary/mut/table/gene_cancer_pooled_leave_one_out.feather \
    --out-dir /data/packages/cbioportal/pan-cancer/summary/loso
"""

from __future__ import annotations

from pathlib import Path

import click
import pandas as pd

K_VALUES = (10, 25, 50, 100, 250, 500, 1000)


def topn_pairs(df: pd.DataFrame, rate_col: str, status_col: str, k: int) -> set[tuple[str, str]]:
    ok = df.loc[df[status_col] == "ok", ["cancer_type", "symbol", rate_col]].dropna(subset=[rate_col])
    top = ok.nlargest(k, rate_col)
    return set(zip(top["cancer_type"], top["symbol"], strict=True))


def overlap_row(base_set: set, hold_set: set) -> dict[str, float | int]:
    inter = base_set & hold_set
    union = base_set | hold_set
    return {
        "base_size": len(base_set),
        "hold_size": len(hold_set),
        "intersection": len(inter),
        "jaccard": len(inter) / len(union) if union else float("nan"),
        "recovery": len(inter) / len(base_set) if base_set else float("nan"),
    }


@click.command()
@click.option("--base", "base_path", type=Path, required=True, help="gene_cancer_pooled.feather")
@click.option("--loo", "loo_path", type=Path, required=True, help="gene_cancer_pooled_leave_one_out.feather")
@click.option("--annotated", "annotated_path", type=Path, required=True,
              help="gene_cancer_study_ratio_annotated.feather (for Bailey driver flag)")
@click.option("--out-dir", "out_dir", type=Path, required=True, help="output directory")
def main(base_path: Path, loo_path: Path, annotated_path: Path, out_dir: Path) -> None:
    base = pd.read_feather(base_path)
    loo = pd.read_feather(loo_path)
    annot = pd.read_feather(annotated_path)
    bailey_genes = annot.loc[annot["bailey2018_driver"], "symbol"].unique().tolist()
    base = base.assign(is_bailey=base["symbol"].isin(bailey_genes))
    loo = loo.assign(is_bailey=loo["symbol"].isin(bailey_genes))
    out_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for cohort in ("all", "bailey_only"):
        for view in sorted(base["analysis_view"].unique()):
            base_view = base.loc[base["analysis_view"] == view]
            loo_view = loo.loc[loo["analysis_view"] == view]
            if cohort == "bailey_only":
                base_view = base_view.loc[base_view["is_bailey"]]
                loo_view = loo_view.loc[loo_view["is_bailey"]]

            for k in K_VALUES:
                base_set = topn_pairs(base_view, "pooled_rate", "status", k)
                for study in sorted(loo_view["excluded_study_id"].unique()):
                    hold = loo_view.loc[loo_view["excluded_study_id"] == study]
                    hold_set = topn_pairs(hold, "holdout_pooled_rate", "holdout_status", k)
                    metrics = overlap_row(base_set, hold_set)
                    rows.append({
                        "cohort": cohort,
                        "analysis_view": view,
                        "excluded_study_id": study,
                        "k": k,
                        **metrics,
                    })

    overlap = pd.DataFrame(rows)
    overlap_path = out_dir / "loso_topn_overlap.feather"
    overlap.reset_index(drop=True).to_feather(overlap_path)

    summary = (
        overlap.groupby(["cohort", "analysis_view", "k"])
        .agg(
            n_iterations=("recovery", "size"),
            recovery_median=("recovery", "median"),
            recovery_q25=("recovery", lambda s: s.quantile(0.25)),
            recovery_q75=("recovery", lambda s: s.quantile(0.75)),
            recovery_min=("recovery", "min"),
            recovery_max=("recovery", "max"),
            jaccard_median=("jaccard", "median"),
            jaccard_q25=("jaccard", lambda s: s.quantile(0.25)),
            jaccard_q75=("jaccard", lambda s: s.quantile(0.75)),
            jaccard_min=("jaccard", "min"),
        )
        .reset_index()
    )
    summary_path = out_dir / "loso_summary.feather"
    summary.to_feather(summary_path)

    print(f"wrote: {overlap_path}")
    print(f"wrote: {summary_path}")
    print()
    print("Summary by analysis_view × K:")
    with pd.option_context("display.max_rows", None, "display.width", 160):
        print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
