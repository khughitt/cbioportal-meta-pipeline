---
type: interpretation
title: "t149 leave-one-study-out replication-rate analysis \u2014 pooled_rate top-N\
  \ is unstable; instability concentrates in small / specialty studies and is not\
  \ rescued by Bailey restriction"
status: active
created: '2026-04-28'
updated: '2026-06-28'
id: interpretation:0013-t149-loso-replication
source_refs:
- task:t149
date: '2026-04-28'
related:
- task:t149
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- question:0013-cross-study-replication-rate
- question:0015-pan-cancer-aggregator-choice
- interpretation:0009-t131-full-pan-cancer-dndscv-run
- interpretation:0010-t144-tiebreaker-fix-rerun
- interpretation:0011-t145-mean-inclusive-inflation-diagnostic
prior_interpretations:
- 2026-04-27-t144-tiebreaker-fix-rerun
- 2026-04-27-t145-mean-inclusive-inflation-diagnostic
---

# t149 LOSO replication-rate analysis

Project links: this interpretation records `task:t149` for
`question:0013-cross-study-replication-rate`, building on
`interpretation:0009-t131-full-pan-cancer-dndscv-run`,
`interpretation:0010-t144-tiebreaker-fix-rerun`, and
`interpretation:0011-t145-mean-inclusive-inflation-diagnostic`.

## Question

Task `t149` asked: how stable is the top-N gene-cancer ranking under leave-one-study-out (LOSO)? This is the decisive test of `hypothesis:0002-cross-study-ranking-divergence-is-structured` proposition P1 ("canonical drivers replicate strongly across LOSO iterations") and P2 ("specialty / small-cohort studies cause more LOSO disruption than large general-purpose studies").

## Method

`code/scripts/analyze_loso_replication.py` operates on the existing t077 outputs:

- Base ranking: `gene_cancer_pooled.feather`, top-K by `pooled_rate` desc, restricted to `status == "ok"`.
- LOSO ranking: `gene_cancer_pooled_leave_one_out.feather`, top-K by `holdout_pooled_rate` desc, restricted to `holdout_status == "ok"` for each `excluded_study_id`.
- Both views (`inclusive`, `exclusive`) and both gene cohorts (`all`, `bailey_only`) are computed for K ∈ {10, 25, 50, 100, 250, 500, 1000}.
- Metrics: per (cohort, view, excluded_study, K) Jaccard and recovery (∣base ∩ hold∣ / ∣base∣).
- Aggregate: median, IQR, min across the 10 LOSO iterations.

Outputs (`/data/packages/cbioportal/pan-cancer/summary/loso/`):

- `loso_topn_overlap.feather` — full grid (560 rows: 2 cohorts × 2 views × 7 K values × 10 studies).
- `loso_summary.feather` — per (cohort, view, K) summary.

## Findings

### F1 — pooled_rate top-N is highly unstable under LOSO

For K=100 inclusive view, **all-cohort median recovery = 0.185** (IQR 0.023–0.495). Min recovery = 0.0; max = 0.86. Spread is 86 percentage points across 10 LOSO iterations.

Restricting to Bailey et al. [@Bailey2018] drivers does not rescue the instability: **bailey_only K=100 inclusive median recovery = 0.21** (IQR 0.028–0.58, min 0.0, max 0.90). The Bailey restriction modestly improves the upper tail (third quartile 0.58 vs 0.49) but median and min are essentially unchanged.

This is a **negative result for `hypothesis:0002-cross-study-ranking-divergence-is-structured` P1 as currently framed**. The pooled_rate top-N ranking is not stable under LOSO even when restricted to the canonical-driver consensus.

### F2 — instability concentrates in small / specialty / pediatric studies

Per-study breakdown at K=100 inclusive (all cohort):

| excluded_study | recovery | jaccard | hold_size |
|---|---:|---:|---:|
| msk_met_2021 | 0.00 | 0.000 | 0 |
| mixed_pipseq_2017 | 0.01 | 0.005 | 100 |
| pediatric_dkfz_2017 | 0.02 | 0.010 | 100 |
| acc_2019 | 0.03 | 0.015 | 100 |
| pptc_2019 | 0.08 | 0.042 | 100 |
| mixed_allen_2018 | 0.29 | 0.170 | 100 |
| genie | 0.48 | 0.316 | 100 |
| pancan_pcawg_2020 | 0.50 | 0.333 | 100 |
| pog570_bcgsc_2020 | 0.74 | 0.587 | 100 |
| metastatic_solid_tumors_mich_2017 | 0.86 | 0.754 | 100 |

The pattern partially supports `hypothesis:0002-cross-study-ranking-divergence-is-structured` P2 — pediatric (`pediatric_dkfz_2017`, `pptc_2019`) and rare-cancer (`acc_2019` adrenocortical) studies cause large disruption, while general-purpose metastatic studies cause smaller disruption. But two findings break the simple story:

- **`msk_met_2021` is structurally load-bearing**: dropping it produces zero `holdout_status == "ok"` rows in the inclusive top-100. The meta-analysis convergence threshold requires k_studies coverage that msk_met_2021 alone provides for the pairs that occupy the top-100.
- **GENIE produces only 48% recovery** despite contributing the largest sample count; this is not "low disruption from large general study" as P2 predicts.

### F3 — the instability is mostly a sample-size-naive ranking artifact

The top-15 by `pooled_rate` is dominated by rare-cancer × frequent-driver pairs whose ratio is high because the cancer-type cohort is small:

```
Small Cell Lung Cancer / TP53     0.872  k=5
Colorectal Cancer / APC           0.753  k=6
Ovarian Cancer / TP53             0.745  k=5
GIST / KIT                        0.743  k=4
Pancreatic / KRAS                 0.710  k=5
```

`pooled_rate` is the meta-analyzed proportion only; it has no significance weighting and no large-cohort prior. When a study is dropped, the convergence boundary at k_studies ≥ 3 shifts unpredictably and the membership of the convergence-eligible pool churns. This is a **methodological finding, not a refutation of `hypothesis:0002-cross-study-ranking-divergence-is-structured`**: the structured-divergence claim refers to ranking schemes (raw, length-adjusted, dNdScv) at scale, but the LOSO test was inadvertently run against a fourth ranking scheme (pooled_rate) which the project has not endorsed as a primary ranking metric.

### F4 — the right next test uses dNdScv-rank-based stability

`gene_cancer_study_ratio_annotated_dndscv.feather` carries `dndscv_q` per (cancer, gene). A LOSO test against the dNdScv ranking would be the cleaner P1 / P2 test, but requires re-running dNdScv per LOO iteration (R, multi-hour). That is filed as a follow-up.

## Verdict

**Partial.** The LOSO test as run produces a sample-size-naive instability number (median recovery 0.18–0.21 at K=100) that does not directly support or refute `hypothesis:0002-cross-study-ranking-divergence-is-structured` P1. The per-study breakdown is consistent with `hypothesis:0002-cross-study-ranking-divergence-is-structured` P2 for specialty studies but inconsistent for the largest general-purpose study (GENIE). The decisive test of P1 / P2 requires a dNdScv-ranking LOSO, which is more expensive but eliminates the rate-based-ranking confound surfaced here.

The `pooled_rate` top-K is not the project's primary ranking metric, but the fact that it is this unstable is itself relevant to `question:0015-pan-cancer-aggregator-choice`: any aggregator that effectively reduces to "rank by point estimate" inherits this instability.

## Follow-up

- File `task:t173` (LOSO against dNdScv ranking, P1 / P2 decisive test).
- The msk_met_2021 zero-convergence finding suggests t077's `k_studies ≥ 3` floor is too tight when the study contributing the largest k drops out. Consider a `k_min ≥ 2` sensitivity panel.
- The GENIE 48% recovery is interesting independent of `hypothesis:0002-cross-study-ranking-divergence-is-structured` — GENIE is the largest cohort by sample count but its disproportionate panel composition (vs WES studies) means it contributes asymmetric `n_total` to the meta. Worth a closer look.
- Cross-reference to `task:t155` (aggregator comparison): any aggregator that uses point-estimate ranking should be expected to inherit this instability; only an aggregator that combines effect-size with significance / sample-size weighting will produce a more stable top-N.

## Outputs

- `code/scripts/analyze_loso_replication.py`
- `/data/packages/cbioportal/pan-cancer/summary/loso/loso_topn_overlap.feather` (560 rows)
- `/data/packages/cbioportal/pan-cancer/summary/loso/loso_summary.feather` (28 rows)
