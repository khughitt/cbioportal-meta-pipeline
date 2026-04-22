---
id: "interpretation:2026-04-22-t122-rt-brca-pilot"
type: "interpretation"
mode: "research"
title: "t122: BRCA gene-level replication-timing pilot"
status: "active"
source_refs:
  - "paper:Yaacov2023"
related:
  - "task:t121"
  - "question:q003-replication-timing-as-gene-level-mutation-rate-confounder"
  - "question:q009-sbs1-lrr-bias-as-normal-contamination-flag"
  - "interpretation:2026-04-22-t110-sbs1-sbs5-brca-comparison"
created: "2026-04-22"
updated: "2026-04-22"
input: "BRCA pair: tcga_mc3 vs msk_impact_2017"
workflow_run: "t122-2026-04-22-brca-rt-pilot"
prior_interpretations:
  - "interpretation:2026-04-22-t110-sbs1-sbs5-brca-comparison"
---

# Interpretation: BRCA gene-level replication-timing pilot

## Verdict

**Verdict:** [~] The first gene-level `CL/CE` pilot shows relative late-replication enrichment in unmatched BRCA, but absolute mutation burden is still dominated by assay coverage, so the result is suggestive rather than decisive.

## Run Surface

- Gene RT map: `data/gene_replication_timing.feather`
- Matched cohort: `tcga_mc3` BRCA samples selected by `restricted_assignment_per_sample.feather`
- Unmatched cohort: `msk_impact_2017` Breast Cancer samples selected by `restricted_assignment_per_sample.feather`
- Outputs:
  - `results/signature-brca-2026-04-22/summary/signatures/rt_gene_burden_per_sample.feather`
  - `results/signature-brca-2026-04-22/summary/signatures/rt_gene_burden_comparison.feather`

## Main Result

Summary row for `lookup_key = breast`:

| matched | unmatched | matched median CE | unmatched median CE | matched median CL | unmatched median CL | matched median log10((CL+0.5)/(CE+0.5)) | unmatched median log10-ratio | one-sided p: unmatched>CL | one-sided p: unmatched>ratio |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `tcga_mc3` | `msk_impact_2017` | 13.0 | 1.0 | 2.0 | 0.0 | -0.7725 | -0.4771 | 1.0 | 3.86e-41 |

Derived directions:

- `median_ce_shift = -12.0` (`matched_higher`)
- `median_cl_shift = -2.0` (`matched_higher`)
- `median_log10_cl_ce_ratio_shift = +0.2954` (`unmatched_higher`)

## Interpretation

Two things are true at once:

1. **Absolute burden is lower in the unmatched panel cohort.**
   `msk_impact_2017` has lower per-sample counts in both `CE` and `CL` genes than MC3, which is expected because this is still a panel-vs-WES comparison.

2. **Relative late-replication burden is higher in the unmatched cohort.**
   The `CL/CE` ratio is shifted upward in `msk_impact_2017`, and the one-sided Mann-Whitney test for higher unmatched `log10(CL/CE)` is strongly significant.

So the coarse gene-level RT signal is not dead the way the SBS1/SBS5 proxy was, but it is also not clean enough to serve as a standalone contamination flag yet. The dominant confounder is still assay regime.

## Why This Matters

This pilot changes the branch priority:

- The simple SBS1/SBS5 proxy failed outright in `t110`.
- The gene-level RT proxy shows **some** directional separation, but only in the relative ratio, not in the raw counts.

That means the next useful step is not "add more coarse burden summaries." It is to make the RT comparison more SBS1-specific, so the statistic tracks the Yaacov 2023 mechanism rather than generic WES-vs-panel sparsity.

## Decision

The result is strong enough to justify a follow-up, but not strong enough to treat `CL/CE` on all mutations as an operational QC flag.

Recommended next step:

- rerun the BRCA pilot with an SBS1-enriched mutation subset or mutation-level attribution, then test whether the `CL/CE` enrichment remains after restricting to the putative SBS1 signal.
