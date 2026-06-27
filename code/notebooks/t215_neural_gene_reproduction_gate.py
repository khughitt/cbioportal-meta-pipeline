# science:code
# status: exploratory
# science:end
"""t215 — neural-gene mutation-enrichment reproduction gate.

Question: q032 / hypothesis h12-neural-gene-enrichment-length-histology-artifact.
Plan: doc/plans/2026-06-06-neural-gene-enrichment-meta-analysis-plan.md (step 1, gate).

The motivating observation — neural genes (NKAIN2, KCNIP4, TAFA2/FAM19A2, RIT2, CALN1,
RBFOX1, LSAMP, SGCZ, OPCML) topping a mutation-frequency view — comes from UNRELIABLE NOTES.
Before any neural-biology work, reproduce it from the pipeline:

  - On which metric do the 9 candidates rank highly (raw count vs sample-ratio)?
  - In which config (full / pan-cancer / 10k)?
  - From which studies / cancer types?
  - Is the candidate set's rank distribution enriched vs random (Mann-Whitney + hypergeometric)?

DECISION RULE (from the plan):
  reproduce (candidates rank highly / set is enriched)  -> proceed to t217 length-null.
  does NOT reproduce                                    -> record notes as spurious; close program.

This script only REPRODUCES + characterizes; the decisive length test is t217 (q032). The
candidate protein lengths are reported descriptively here to foreshadow that test, not to run it.

Run:  uv run --frozen python code/notebooks/t215_neural_gene_reproduction_gate.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

PACKAGE_ROOT = Path("/") / "data" / "packages" / "cbioportal"

# --- candidate set (TAFA2 is the HGNC alias of FAM19A2; the pipeline carries FAM19A2) ---
CANDIDATES = [
    "NKAIN2",
    "KCNIP4",
    "FAM19A2",
    "RIT2",
    "CALN1",
    "RBFOX1",
    "LSAMP",
    "SGCZ",
    "OPCML",
]
CANDIDATE_ALIASES = {"FAM19A2": "TAFA2"}

# --- canonical neural EFFECTORS (positive control: short, known cancer-neuroscience genes) ---
EFFECTORS = [
    "NLGN3",
    "ADRB2",
    "NTRK1",
    "NTRK2",
    "CHRM3",
    "GRIN2A",
    "GRIN2B",
    "NGF",
    "BDNF",
]

META = ["cancer_type", "symbol"]
MIN_STRATA = 20  # min non-null (cancer,study) cells for the mean-ratio metric (kills tiny-cohort lincRNA noise)
TOPN = 50

# Non-study columns that ride along in the aggregate tables and must NOT be summed/ranked as studies.
# `full`/`10k` carry pooled summaries (mean, mean_adj); the pan-cancer annotated layout additionally
# carries per-study hypermutator-`_exclusive` twins plus pooled/metadata columns (mean_inclusive,
# n_*_studies, n_panel_covered_samples_*, callable_*). We keep only the bare inclusive `{study}` columns.
_NONSTUDY_EXACT = {"mean", "mean_adj"}
_NONSTUDY_PREFIXES = ("mean_", "n_", "callable_")


def study_columns(df: pd.DataFrame) -> list[str]:
    """Inclusive per-study columns only — drop meta, pooled summaries, `_exclusive` twins, and metadata."""
    out = []
    for c in df.columns:
        if c in META or c in _NONSTUDY_EXACT or c.endswith("_exclusive"):
            continue
        if c.startswith(_NONSTUDY_PREFIXES):
            continue
        out.append(c)
    return out


CONFIGS = {
    "full": PACKAGE_ROOT / "full/summary/mut/table",
    "pan-cancer": PACKAGE_ROOT / "pan-cancer/summary/mut/table",
    "10k": PACKAGE_ROOT / "10k/summary/mut/table",
}

OUT = Path("results/neural-gene-reproduction-2026-06-08")


def load_driver_symbols() -> set[str]:
    """Bailey 2018 consensus drivers ∪ COSMIC CGC — used for the non-driver ranking."""
    bailey = set(
        pd.read_csv("data/bailey2018_table_s1.tsv", sep="\t")["Gene"]
        .dropna()
        .astype(str)
    )
    cgc = set(
        pd.read_csv("data/cosmic_cgc.tsv", sep="\t")["Gene Symbol"].dropna().astype(str)
    )
    return {g.strip() for g in (bailey | cgc)}


def load_gene_lengths() -> tuple[pd.Series, dict[str, float]]:
    """Return (primary-symbol -> length) for the genome distribution, and a synonym-aware lookup.

    UniProt 'Gene Names' is space-separated synonyms; the primary symbol is the first token, but the
    pipeline may carry a gene under any synonym (e.g. FAM19A2 is the HGNC alias of primary TAFA2). The
    primary series defines the percentile denominator; the synonym map resolves targeted lookups so all
    candidates/effectors are found regardless of which alias is canonical.
    """
    u = pd.read_csv("data/uniprotkb_hsapiens_protein_lengths.tsv.gz", sep="\t")
    u = u.dropna(subset=["Gene Names", "Length"]).copy()
    tokens = u["Gene Names"].astype(str).str.split()
    u["primary"] = tokens.str[0]
    primary_len = u.groupby("primary")["Length"].max()
    syn_len: dict[str, float] = {}
    for toks, length in zip(tokens, u["Length"]):
        for t in toks:
            if length > syn_len.get(t, 0):
                syn_len[t] = float(length)
    return primary_len, syn_len


def per_gene_metrics(count_path: Path, ratio_path: Path) -> tuple[pd.DataFrame, int]:
    """Aggregate the long (cancer_type, symbol) x study tables to per-gene mutation-frequency metrics.

    Returns (per-gene metrics, n_study_columns). Only inclusive per-study columns are summed; pooled
    summary / `_exclusive` / metadata columns are excluded via ``study_columns``.
    """
    cnt = pd.read_feather(count_path)
    rat = pd.read_feather(ratio_path)
    cstudies = study_columns(cnt)
    rstudies = study_columns(rat)

    total_count = cnt.groupby("symbol")[cstudies].sum(min_count=1).sum(axis=1)

    rstack = rat.set_index(META)[rstudies].stack()
    mean_ratio = rstack.groupby(level="symbol").mean()
    n_strata = rstack.groupby(level="symbol").size()

    out = pd.DataFrame(
        {"total_count": total_count, "mean_ratio": mean_ratio, "n_strata": n_strata}
    )
    # mean-ratio is only meaningful for genes seen in enough strata
    out["mean_ratio_filtered"] = out["mean_ratio"].where(out["n_strata"] >= MIN_STRATA)
    return out, len(cstudies)


def rank_pct(series: pd.Series) -> pd.DataFrame:
    s = series.dropna()
    rk = s.rank(ascending=False, method="min")
    return pd.DataFrame(
        {
            "value": s,
            "rank": rk.astype(int),
            "pct": 100.0 * rk / len(s),
            "n_total": len(s),
        }
    )


def enrichment(metric: pd.Series, gene_set: list[str]) -> dict:
    """Mann-Whitney (candidate ranks better than rest, one-sided) + top-100 hypergeometric."""
    s = metric.dropna()
    present = [g for g in gene_set if g in s.index]
    in_set = s.index.isin(present)
    set_vals = s[in_set].to_numpy()
    rest_vals = s[~in_set].to_numpy()
    # one-sided: candidate metric values are GREATER (rank higher) than the rest
    _u, p = stats.mannwhitneyu(set_vals, rest_vals, alternative="greater")
    median_pct = float(
        100.0 * s.rank(ascending=False, method="min")[present].median() / len(s)
    )
    # hypergeometric: how many of the set fall in the top-100
    rk = s.rank(ascending=False, method="min")
    top100 = int((rk[present] <= 100).sum())
    exp_top100 = len(present) * 100 / len(s)
    hyp_p = float(stats.hypergeom.sf(top100 - 1, len(s), 100, len(present)))
    return {
        "n_in_set": len(present),
        "median_pct": round(median_pct, 3),
        "mwu_p_greater": float(p),
        "n_in_top100": top100,
        "exp_in_top100": round(exp_top100, 3),
        "hypergeom_top100_p": hyp_p,
    }


def top_contributors(count_path: Path, gene: str, by: str) -> list[tuple[str, int]]:
    cnt = pd.read_feather(count_path)
    studies = study_columns(cnt)
    if by == "cancer_type":
        s = cnt[cnt.symbol == gene].set_index("cancer_type")[studies].sum(axis=1)
    else:  # study
        s = cnt[cnt.symbol == gene][studies].sum()
    return [
        (str(k), int(round(v)))
        for k, v in s.sort_values(ascending=False).head(5).items()
        if v > 0
    ]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    drivers = load_driver_symbols()
    primary_len, syn_len = load_gene_lengths()

    metrics = {
        "total_count": "raw mutation count",
        "mean_ratio_filtered": f"mean sample-ratio (>={MIN_STRATA} strata)",
    }

    rank_rows: list[dict] = []
    enrich_rows: list[dict] = []
    top_rows: list[pd.DataFrame] = []
    study_counts: dict[str, int] = {}

    for cfg, base in CONFIGS.items():
        base = Path(base)
        cpath, rpath = (
            base / "gene_cancer_study.feather",
            base / "gene_cancer_study_ratio.feather",
        )
        if not cpath.exists():
            print(f"[skip] {cfg}: {cpath} absent")
            continue
        print(f"[{cfg}] loading ...")
        m, n_studies = per_gene_metrics(cpath, rpath)
        study_counts[cfg] = n_studies
        print(f"[{cfg}] {n_studies} inclusive study columns")

        # non-driver variant of raw count (the most likely source of the eyeballed observation)
        m["total_count_nondriver"] = m["total_count"].where(~m.index.isin(drivers))
        metric_cols = {
            **metrics,
            "total_count_nondriver": "raw count, non-driver genes only",
        }

        for col, label in metric_cols.items():
            rp = rank_pct(m[col])
            for g in CANDIDATES + EFFECTORS:
                role = "candidate" if g in CANDIDATES else "effector"
                if g in rp.index:
                    rank_rows.append(
                        {
                            "config": cfg,
                            "metric": col,
                            "metric_label": label,
                            "gene": g,
                            "role": role,
                            "value": float(rp.loc[g, "value"]),
                            "rank": int(rp.loc[g, "rank"]),
                            "pct": round(float(rp.loc[g, "pct"]), 3),
                            "n_total": int(rp.loc[g, "n_total"]),
                        }
                    )
                else:
                    rank_rows.append(
                        {
                            "config": cfg,
                            "metric": col,
                            "metric_label": label,
                            "gene": g,
                            "role": role,
                            "value": np.nan,
                            "rank": -1,
                            "pct": np.nan,
                            "n_total": int(rp["n_total"].iloc[0]) if len(rp) else 0,
                        }
                    )
            # enrichment of candidate set + effector set
            for setname, gs in [("candidates", CANDIDATES), ("effectors", EFFECTORS)]:
                e = enrichment(m[col], gs)
                enrich_rows.append(
                    {
                        "config": cfg,
                        "metric": col,
                        "metric_label": label,
                        "gene_set": setname,
                        **e,
                    }
                )
            # top-N table for context
            tn = (
                rp.sort_values("rank")
                .head(TOPN)
                .reset_index()
                .rename(columns={"index": "symbol"})
            )
            tn["config"], tn["metric"] = cfg, col
            tn["is_driver"] = tn["symbol"].isin(drivers)
            tn["is_candidate"] = tn["symbol"].isin(CANDIDATES)
            top_rows.append(tn)

        # per-candidate top contributing cancer types + studies (raw count), full config only for brevity
        if cfg == "full":
            for g in CANDIDATES:
                top_rows_ct = top_contributors(cpath, g, "cancer_type")
                top_rows_st = top_contributors(cpath, g, "study")
                top_rows.append(
                    pd.DataFrame(
                        [
                            {
                                "config": cfg,
                                "metric": "contributors",
                                "symbol": g,
                                "top_cancer_types": "; ".join(
                                    f"{k}:{v}" for k, v in top_rows_ct
                                ),
                                "top_studies": "; ".join(
                                    f"{k}:{v}" for k, v in top_rows_st
                                ),
                            }
                        ]
                    )
                )

    ranks = pd.DataFrame(rank_rows)
    enrich = pd.DataFrame(enrich_rows)
    tops = pd.concat([t for t in top_rows if "rank" in t.columns], ignore_index=True)
    contribs = pd.concat(
        [t for t in top_rows if "top_cancer_types" in t.columns], ignore_index=True
    )

    # length foreshadow (descriptive only; decisive test = t217). Percentile is vs the primary-symbol
    # protein-length distribution; the candidate length is resolved alias-aware (FAM19A2 <- TAFA2 etc).
    genome_median_len = float(primary_len.median())
    len_rows = []
    for g in CANDIDATES + EFFECTORS:
        resolved = g if g in syn_len else CANDIDATE_ALIASES.get(g, g)
        L = float(syn_len.get(resolved, np.nan))
        len_pct = float(100.0 * (primary_len < L).mean()) if not np.isnan(L) else np.nan
        len_rows.append(
            {
                "gene": g,
                "resolved_symbol": resolved if not np.isnan(L) else "",
                "role": "candidate" if g in CANDIDATES else "effector",
                "protein_length_aa": L,
                "length_pctile": round(len_pct, 1) if not np.isnan(L) else np.nan,
            }
        )
    length_df = pd.DataFrame(len_rows)

    # --- write artifacts ---
    ranks.to_feather(OUT / "candidate_ranks.feather")
    enrich.to_csv(OUT / "enrichment_stats.tsv", sep="\t", index=False)
    tops.to_feather(OUT / "top_genes_by_metric.feather")
    contribs.to_csv(OUT / "candidate_contributors.tsv", sep="\t", index=False)
    length_df.to_csv(OUT / "candidate_lengths.tsv", sep="\t", index=False)

    datapackage = {
        "name": "neural-gene-reproduction-2026-06-08",
        "title": "t215 neural-gene mutation-enrichment reproduction gate",
        "description": "Reproduction gate for hypothesis:h12 / question:q032. Characterizes where the "
        "9 candidate neural genes rank in pipeline mutation-frequency views across configs/metrics, "
        "with set-level enrichment statistics. Reproduces from gene_cancer_study(_ratio).feather.",
        "created": "2026-06-08",
        "sources": [
            {"config": cfg, "path": f"{base}/gene_cancer_study{{,_ratio}}.feather"}
            for cfg, base in CONFIGS.items()
        ],
        "tasks": ["t215"],
        "related": [
            "hypothesis:h12-neural-gene-enrichment-length-histology-artifact",
            "question:q032-neural-gene-length-null",
        ],
        "resources": [
            {"name": "candidate_ranks", "path": "candidate_ranks.feather"},
            {"name": "enrichment_stats", "path": "enrichment_stats.tsv"},
            {"name": "top_genes_by_metric", "path": "top_genes_by_metric.feather"},
            {"name": "candidate_contributors", "path": "candidate_contributors.tsv"},
            {"name": "candidate_lengths", "path": "candidate_lengths.tsv"},
        ],
        "parameters": {
            "min_strata": MIN_STRATA,
            "topn": TOPN,
            "candidates": CANDIDATES,
            "effectors": EFFECTORS,
            "inclusive_study_counts": study_counts,
            "note": "unannotated gene_cancer_study(_ratio) aggregates used; annotated full/10k feathers "
            "are not present under the package root (annotation adds overlay columns, not counts).",
        },
    }
    (OUT / "datapackage.json").write_text(json.dumps(datapackage, indent=2))

    # --- console summary ---
    pd.set_option("display.width", 200, "display.max_columns", 30)
    print(
        f"\n================ INCLUSIVE STUDY COLUMNS PER CONFIG ================\n  {study_counts}"
    )
    print("\n================ CANDIDATE RANKS (full config) ================")
    print(
        ranks[(ranks.config == "full") & (ranks.role == "candidate")]
        .pivot(index="gene", columns="metric", values="rank")
        .to_string()
    )
    print("\n================ ENRICHMENT (candidate set vs all genes) ================")
    print(
        enrich[enrich.gene_set == "candidates"][
            [
                "config",
                "metric",
                "n_in_set",
                "median_pct",
                "mwu_p_greater",
                "n_in_top100",
                "exp_in_top100",
                "hypergeom_top100_p",
            ]
        ].to_string(index=False)
    )
    print("\n================ EFFECTOR (positive-control) ENRICHMENT ================")
    print(
        enrich[enrich.gene_set == "effectors"][
            [
                "config",
                "metric",
                "n_in_set",
                "median_pct",
                "mwu_p_greater",
                "n_in_top100",
            ]
        ].to_string(index=False)
    )
    print(
        f"\n================ LENGTH FORESHADOW (genome median = {genome_median_len:.0f} aa) ================"
    )
    print(length_df.to_string(index=False))
    print(
        "\n================ PER-CANDIDATE CONTRIBUTORS (full, raw count) ================"
    )
    for _, r in contribs.iterrows():
        print(f"  {r['symbol']:9s} cancers: {r['top_cancer_types']}")

    print(f"\nArtifacts written to {OUT}/")


if __name__ == "__main__":
    main()
