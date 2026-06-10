---
type: interpretation
title: 't123: BRCA SBS1-proxy replication-timing pilot'
status: active
created: '2026-04-22'
updated: '2026-04-22'
id: interpretation:0006-t123-rt-brca-sbs1-proxy-pilot
mode: research
source_refs:
- paper:Yaacov2023
related:
- task:t122
- task:t123
- question:0009-sbs1-lrr-bias-as-normal-contamination-flag
- interpretation:0005-t122-rt-brca-pilot
input: 'BRCA pair: tcga_mc3 vs msk_impact_2017, CpG C>T proxy subset'
workflow_run: t123-2026-04-22-brca-rt-sbs1-proxy
prior_interpretations:
- interpretation:0005-t122-rt-brca-pilot
---

# Interpretation: BRCA SBS1-proxy replication-timing pilot

## Verdict

**Verdict:** [-] The simple CpG `C>T` / complementary `G>A` proxy does not provide a usable SBS1-specific RT signal on the BRCA panel-vs-WES pair. Once the comparison is anchored on the full assignment sample set, the unmatched panel cohort is overwhelmingly zero-inflated.

## Run Surface

- Gene RT map: `data/gene_replication_timing.feather`
- Proxy definition: coding-SNV `codons` parsed as CpG `C>T` or complementary `G>A`
- Matched cohort: `tcga_mc3` BRCA samples from `restricted_assignment_per_sample.feather`
- Unmatched cohort: `msk_impact_2017` Breast Cancer samples from the same assignment surface
- Outputs:
  - `results/signature-brca-2026-04-22/summary/signatures/rt_gene_burden_sbs1_proxy_per_sample.feather`
  - `results/signature-brca-2026-04-22/summary/signatures/rt_gene_burden_sbs1_proxy_comparison.feather`

## Main Result

Summary row for `lookup_key = breast`:

| matched | unmatched | matched n | unmatched n | matched median CE | unmatched median CE | matched median CL | unmatched median CL | matched median log10((CL+0.5)/(CE+0.5)) | unmatched median log10-ratio | one-sided p: unmatched>CL | one-sided p: unmatched>ratio |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `tcga_mc3` | `msk_impact_2017` | 791 | 1210 | 1.0 | 0.0 | 0.0 | 0.0 | -0.2553 | 0.0 | 1.0 | 7.14e-102 |

Derived directions:

- `median_ce_shift = -1.0` (`matched_higher`)
- `median_cl_shift = 0.0` (`tie`)
- `median_log10_cl_ce_ratio_shift = +0.2553` (`unmatched_higher`)

## Why This Does Not Support The Proxy

The apparent unmatched-higher ratio is not a clean SBS1-like late-replication effect. It is driven by zero inflation:

- `msk_impact_2017`: 1,210 samples total, `CE == 0` in 1,157 and `CL == 0` in 1,205
- `tcga_mc3`: 791 samples total, `CE == 0` in 343 and `CL == 0` in 678

With the required full-sample comparison surface, most unmatched samples have **no** proxy mutations in either `CE` or `CL` genes, so the pseudocount pushes the center of the distribution to `log10(1) = 0`. That makes the ratio shift a coverage/sparsity artifact rather than a persuasive contamination signal.

The nonzero-only support set is also too thin to rescue the proxy:

- only 58 unmatched samples have any proxy-labeled `CE` or `CL` mutation at all
- only 5 unmatched samples have `CL/CE > 1`

So the first coarse SBS1-enriched branch collapses under panel sparsity rather than sharpening the Yaacov-style mechanism.

## Decision

`t123` should be treated as a negative screening result:

- the all-mutation RT pilot (`t122`) was suggestive but coverage-confounded
- the simple SBS1-like CpG proxy is too sparse on the unmatched panel cohort to disambiguate that signal

Recommended next move:

- do **not** add more pseudocount-based panel/WES burden summaries for q009
- either stage a true mutation-context / SBS1-attribution implementation or explicitly retire the panel/WES proxy route for q009
