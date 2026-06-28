---
type: interpretation
title: 't110: BRCA SBS1/SBS5 matched-vs-unmatched comparison'
status: active
created: '2026-04-22'
updated: '2026-04-22'
id: interpretation:0004-t110-sbs1-sbs5-brca-comparison
mode: research
source_refs:
- paper:Yaacov2023
- paper:Xu2025
related:
- task:t110
- task:t109
- topic:signature-decomposition-unmatched-normal
- question:0008-signature-decomposition-tissue-background-subtraction
- question:0009-sbs1-lrr-bias-as-normal-contamination-flag
input: "task:t110 \u2014 commits 1580255..working tree"
workflow_run: t110-2026-04-22-brca
prior_interpretations:
- interpretation:0003-t111-normal-tissue-spectra-pipeline
---

# Interpretation: t110 BRCA SBS1/SBS5 comparison

## Verdict

**Verdict:** [-] The first matched-vs-unmatched BRCA comparison does not support SBS1 excess in the unmatched cohort, so the SBS1/SBS5 ratio is not an operational contamination flag on this pair.

## Run Surface

- Config: `code/config/config-signature-brca-poc.yml`
- Matched-normal cohort: `tcga_mc3` (`BRCA`, n=791 samples)
- Unmatched-normal cohort: `msk_impact_2017` (`Breast Cancer`, n=1,210 samples)
- Per-sample exposures: `results/signature-brca-2026-04-22/studies/{study}/mut/signatures/restricted_assignment_per_sample.feather`
- Comparison table: `results/signature-brca-2026-04-22/summary/signatures/sbs1_sbs5_proxy_comparison.feather`

## Main Result

The BRCA comparison row is:

| lookup_key | matched | unmatched | matched median SBS1 | unmatched median SBS1 | matched median log10((SBS1+0.5)/(SBS5+0.5)) | unmatched median log10-ratio | one-sided p: unmatched>SBS1 | one-sided p: unmatched>ratio |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| breast | `tcga_mc3` | `msk_impact_2017` | 7.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.99975 |

Additional comparison fields:

- `median_sbs1_shift = -7.0` (`matched_higher`)
- `median_log10_ratio_shift = 0.0` (`tie`)
- `sbs1_two_sided_pvalue = 1.93e-132`
- `log10_ratio_two_sided_pvalue = 5.00e-4`

Interpretation:

- The unmatched cohort is **not** shifted upward on SBS1. The observed direction is the opposite of the contamination-proxy hypothesis.
- The pseudocount-stabilized SBS1/SBS5 ratio has identical medians (`log10 ratio = 0`) in both cohorts, so the proposed threshold surface is degenerate at the median.
- The two-sided tests show the cohorts differ, but not in the hypothesized way that would justify a simple "unmatched-normal contamination" flag.

## Why This Is Not Enough For A Proxy

This task asked whether a simple SBS1 excess or SBS1/SBS5 ratio shift could serve as an operational contamination signal before investing in the more mechanistic `question:0009-sbs1-lrr-bias-as-normal-contamination-flag` path.

On this first required pair (`>=1` overlapping cancer type), the answer is no:

- `tcga_mc3` has materially higher SBS1 exposures than the unmatched MSK panel cohort.
- The ratio median is flat because both cohorts have `median SBS5 = 0`, so the pseudocount dominates the center of the distribution.
- The comparison is confounded by assay regime as well as matched-normal status: `tcga_mc3` is WES-scale while `msk_impact_2017` is panel-restricted, producing a far sparser exposure surface in the panel cohort.

So the SBS1/SBS5 ratio may still be descriptively interesting, but it is **not supported here as a thresholdable QC flag** for `question:0009-sbs1-lrr-bias-as-normal-contamination-flag`.

## Methodological Outcome

t110 also surfaced two implementation requirements that are now fixed in the code:

1. Per-sample restricted assignment needed its own workflow branch; pooled per-study exposures from t109 were not sufficient for the task question.
2. The mutation inputs use plain chromosome labels (`1`, `2`, `X`) rather than `chr1` form, so the SigProfiler-prep path had to normalize chromosome names before filtering callable SNVs.

Without that normalization fix, both study outputs were silently empty and the comparison would have been uninterpretable.

## Updated Priority Signal

- **t110:** complete as a negative-result validation task.
- **`question:0009-sbs1-lrr-bias-as-normal-contamination-flag`:** still open, and now relatively more important. The Yaacov replication-timing signal [@Yaacov2023] remains the better-motivated path because this coarse SBS1/SBS5 proxy did not separate the first matched-vs-unmatched pair.
- **`question:0008-signature-decomposition-tissue-background-subtraction`:** any future background-subtraction work should treat the SBS1/SBS5 ratio as exploratory, not as a pre-validated contamination threshold.
