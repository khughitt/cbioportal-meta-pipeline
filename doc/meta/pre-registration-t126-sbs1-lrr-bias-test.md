---
id: "pre-registration:pre-registration-t126-sbs1-lrr-bias-test"
type: "pre-registration"
title: "Pre-registration: t126 — per-study aggregate SBS1 LRR-bias test"
status: "active"
committed: "2026-04-24"
spec: ""
source_refs:
  - "paper:Yaacov2023"
  - "paper:Alexandrov2020"
related:
  - "task:t126"
  - "task:t124"
  - "task:t109"
  - "task:t110"
  - "task:t121"
  - "question:q009-sbs1-lrr-bias-as-normal-contamination-flag"
  - "discussion:2026-04-24-t124-q009-fork-decision"
  - "interpretation:2026-04-22-t110-sbs1-sbs5-brca-comparison"
  - "interpretation:2026-04-22-t122-rt-brca-pilot"
  - "interpretation:2026-04-22-t123-rt-brca-sbs1-proxy-pilot"
created: "2026-04-24"
updated: "2026-04-24"
---

# Pre-registration: t126 — per-study aggregate SBS1 LRR-bias test

## Purpose

Resolve `t124` (the q009 fork) by running the per-study aggregate version of the Yaacov 2023 LRR-bias statistic — the only formulation that simultaneously matches (a) the published mechanism and (b) q009's framing as a single-study contamination flag. Three prior pilots (`t110`, `t122`, `t123`) tested per-sample approximations and each failed for a different sparsity reason; this test pools across samples within a study before evaluating LRR enrichment.

This document is written **before** any implementation begins, so that the test outcomes (pass / retire / defer) are determined by pre-registered thresholds rather than post-hoc rationalization.

## Hypotheses Under Test

- **H1:** If unmatched-normal contamination contributes detectable SBS1 signal in the
  unmatched panel cohort, then the panel cohort's panel-coverage-corrected LRR fraction
  will exceed both the matched-control cohort's interval and the pre-registered 0.45
  threshold.
- **H0:** The unmatched panel cohort's corrected LRR fraction overlaps the matched-control
  cohort and remains below 0.45 despite adequate effective SBS1 counts.
- **Power gate:** If effective post-correction SBS1 support is below the pre-registered
  floor, the test is underpowered and q009 is deferred rather than interpreted as positive
  or negative evidence.

## Pre-run power projection

Computed against the existing `t109/t110` artifacts under `results/signature-brca-2026-04-22/studies/<study>/mut/signatures/restricted_assignment_per_sample.feather`:

| Cohort | n samples | Σ total mutations | Σ SBS1 exposure | % SBS1 |
|---|---:|---:|---:|---:|
| `tcga_mc3` (BRCA) | 791 | 81,064 | **7,582** | 9.4% |
| `msk_impact_2017` (BRCA) | 1,210 | 5,041 | **553** | 11.0% |

**Projected 95% CI half-width on observed LRR fraction**, assuming the SBS1 attribution distributes across CE-covered and CL-covered panel territory in proportion to their base-pair extent (panel-coverage-corrected denominator, see §4):

- `tcga_mc3`: with n = 7,582 and an observed LRR fraction near the cancer baseline (~0.40), the binomial 95% half-width is ≈ ±1.1 percentage points.
- `msk_impact_2017`: with n = 553 and the same baseline, half-width ≈ ±4.1 percentage points.

The Yaacov 2023 normal-vs-cancer LRR delta is approximately **10–20 percentage points** (cancer ~0.40, normal ~0.55–0.65). Both cohorts therefore have nominal power to detect a clean shift; `msk_impact_2017` has uncomfortably narrow margin if the true shift is small (e.g., 5 pp from partial contamination).

**Pre-registered power gate:** if pooled SBS1 attribution per study is `n < 500` after the panel-coverage correction is applied (i.e., counts inside CE+CL panel-overlap regions only), the test is declared underpowered before any inferential statistic is computed and `q009` is deferred (revisit-condition: `WGS inputs ingested`).

## Critical caveat: per-sample fit quality in panel cohort

Per-sample SigProfilerAssignment cosine-similarity quartiles for the BRCA assignment surface:

| Cohort | median cos | Q1 | Q3 | n cos≥0.7 / total | n cos≥0.85 / total |
|---|---:|---:|---:|---:|---:|
| `tcga_mc3` | 0.796 | 0.724 | 0.880 | 633 / 791 (80%) | 268 / 791 (34%) |
| `msk_impact_2017` | 0.383 | 0.264 | 0.588 | 158 / 1,210 (13%) | 30 / 1,210 (2%) |

The MSK panel cohort is overwhelmingly poorly fit by the per-cancer-type-restricted COSMIC reference. The aggregate SBS1 count (553) is preserved by NNLS construction — sum of NNLS-decomposed per-sample exposures equals total mutations apportioned. But the *per-sample assignment of which mutations are SBS1* is unreliable for ~87% of MSK samples.

**Mitigation:** rather than treat per-sample SBS1 exposure counts as discrete labels, compute per-mutation SBS1 *posterior probability* using the per-sample exposures as a Bayesian prior and the mutation's trinucleotide context as the likelihood (see §3). The aggregate LRR fraction is then a sum of fractional weights, not a count of dichotomized labels. This downweights mutations whose attribution is ambiguous and upweights mutations whose context is strongly SBS1-like (CpG C>T).

This caveat must appear in the final interpretation document, regardless of outcome.

## Test design

### Inputs

1. `data/gene_replication_timing.feather` (from `t121`): gene-level constitutive RT labels — `CE` (11,394 genes), `CL` (3,132 genes), `unassigned` (52,452 genes). Schema: `ensgene`, `entrez`, `symbol`, `chr`, `start`, `end`, `rt_constitutive_label`, `rt_ce_bp`, `rt_cl_bp`, `rt_constitutive_bp`.
2. `results/signature-brca-2026-04-22/studies/<study>/mut/signatures/restricted_assignment_per_sample.feather`: per-sample × per-signature exposure for the breast lookup_key (10 active signatures: SBS1, SBS2, SBS3, SBS5, SBS8, SBS13, SBS18, SBS40a, SBS40b, SBS40c).
3. `results/signature-brca-2026-04-22/studies/<study>/mut/table/mut.feather`: per-mutation rows with `symbol`, `chromosome`, `start`, `end`, `reference_allele`, `tumor_seq_allele2`, `consequence`, `variant_type`, `sample_id_tumor`, `codons` (trinucleotide context source).
4. COSMIC v3.x SBS reference catalog (96-context × signature probability matrix). Source: SigProfilerAssignment's bundled COSMIC reference, accessed via the same package the t109 rule already uses.
5. (Optional, for panel-coverage correction) MSK-IMPACT panel BED file. Already present in pipeline as panel coverage data.

### Per-mutation SBS1 posterior

For each SNV `i` in sample `s`:

```
P(SBS1 | mut_i, sample_s) = (E_{s,SBS1} * π_SBS1[ctx_i]) / Σ_k (E_{s,k} * π_k[ctx_i])
```

where:
- `E_{s,k}` = exposure (mutation count) of signature `k` in sample `s`, from the restricted assignment feather
- `π_k[ctx]` = COSMIC reference probability of generating a mutation in context `ctx` under signature `k`
- `ctx_i` = 96-context bin for mutation `i` (mutation class C>A/C>G/C>T/T>A/T>C/T>G × 16 trinucleotide contexts)
- sum is over the 10 active signatures used in the per-cancer-type restricted assignment

Mutations restricted to SNVs (`variant_type == 'SNP'`); indels are not assigned by SBS signatures.

### Aggregate LRR-bias statistic

For each study, compute:

```
n_CL_SBS1 = Σ_{i ∈ CL genes}  P(SBS1 | mut_i, sample_s)
n_CE_SBS1 = Σ_{i ∈ CE genes}  P(SBS1 | mut_i, sample_s)
```

LRR fraction (uncorrected): `f_LRR = n_CL_SBS1 / (n_CL_SBS1 + n_CE_SBS1)`

### Panel-coverage correction

The Yaacov 2023 cancer baseline (`f_LRR ≈ 0.40` under the null) was derived from WGS, where CE and CL regions are sampled in proportion to their genomic extent (~40% of the genome is constitutive, split CE vs CL). For panel/WES data, the assayed CE-bp and CL-bp counts are not in genome-wide proportions.

Compute panel-coverage-corrected mutation density:

```
ρ_CE = n_CE_SBS1 / panel_CE_bp_overlap
ρ_CL = n_CL_SBS1 / panel_CL_bp_overlap
f_LRR_corrected = ρ_CL / (ρ_CE + ρ_CL)
```

For `tcga_mc3` (a WES pseudo-study), `panel_*_bp_overlap` is the exonic CE/CL bp sum (gene CDS extent intersected with RT label, summed across all CE-labelled and CL-labelled genes). For `msk_impact_2017`, it is the panel BED intersected with CE/CL gene boundaries. If panel BED coordinates are not readily available, an exonic-CDS approximation is used and noted as a deviation in the final interpretation.

**Pre-registered fallback:** if panel BED intersection adds non-trivial implementation complexity (>1 hour), use the gene-CDS approximation and note the deviation. The interpretation-level claim ("does the LRR fraction approach the normal baseline?") survives the approximation as long as both cohorts use the same approximation.

### Bootstrap 95% CI

Cluster bootstrap by sample (1,000 resamples): resample sample_ids with replacement within a study, recompute `f_LRR_corrected`. Report 95% percentile CI for the per-study estimate.

## Expected Outcomes

The analysis has three allowed outcomes: `pass`, `retire`, or `defer`. A pass would justify
promoting q009 into an operational contamination-flag follow-up. A retire outcome would close
this SBS1-LRR route as negative evidence for the current panel/WES setting. A defer outcome
would preserve the question but require WGS-scale inputs before retrying.

## Decision Criteria

The test outcome is one of three pre-registered verdicts. Each maps to a concrete next action.

| Outcome | Definition | Action |
|---|---|---|
| **pass** | For at least one panel cohort (`msk_impact_2017`), the 95% CI for `f_LRR_corrected` lies **strictly above** the matched-cohort (`tcga_mc3`) CI **and** above 0.45 (mid-point between cancer baseline 0.40 and normal baseline 0.55) | Close `t124` as resolved with positive evidence; update `q009` status to `active` with a documented operational threshold; spec the contamination flag as a downstream pipeline rule |
| **retire** | The 95% CI for `f_LRR_corrected` in the panel cohort overlaps the matched cohort's CI **and** stays below 0.45, and the projected effective `n` is ≥ 500 (i.e., the test was adequately powered) | Close `t124` as resolved with negative evidence; update `q009` status to `retired`; document the retirement reasoning in `doc/interpretations/` and stop further panel/WES SBS1 LRR work |
| **defer** | The effective `n` post-panel-correction is `< 500`, or the bootstrap CI half-width exceeds ±10 pp on the panel cohort | Close `t124` as resolved with insufficient evidence; update `q009` status to `deferred` with revisit-condition `WGS inputs ingested`; do NOT retire the question |

Outcomes are evaluated per cohort but the q009 verdict is panel-cohort-driven (`tcga_mc3` is the matched control; the contamination signal must be detectable on the unmatched panel cohort to be operationally useful).

## Null Result Plan

A powered null result maps to **retire**: close `t124` as resolved with negative evidence,
update `q009` to `retired`, and stop further panel/WES SBS1 LRR work. An underpowered or
too-wide result maps to **defer**: close `t124` as insufficient evidence, update `q009` to
`deferred`, and revisit only when WGS inputs are available.

## What this test does NOT establish

This pre-registration is conservative about scope. The following are explicitly NOT outcomes of the test:

1. **Per-sample contamination scores.** The test produces per-study aggregate estimates only. Per-sample LRR-bias scoring is underpowered at panel mutation densities and is not attempted.
2. **Calibrated probability of contamination.** A "pass" outcome establishes that SBS1 LRR bias is detectable in the panel cohort; it does not assign a probability of normal-tissue origin per study.
3. **Generalization beyond BRCA.** The test runs on the BRCA `tcga_mc3` vs `msk_impact_2017` pair only. Generalization to other cancer types or other unmatched-normal cohorts is a follow-up question.
4. **Mechanism vs proxy distinction.** SigProfilerAssignment is itself a model; its SBS1 attributions inherit any mis-fitting from the per-sample NNLS step (especially severe in MSK-IMPACT, see §2). A "pass" outcome demonstrates that the *attribution-weighted* LRR signal differs between cohorts; whether that signal traces purely to mechanism or partly to fit pathology cannot be disentangled here.

## Implementation notes

- **Single-purpose script**: `code/scripts/compute_sbs1_lrr_bias_per_study.py`. Not yet wired into the main Snakefile rule graph; opt-in target only.
- **Reuses existing artifacts**: `t109/t110` per-sample assignments + `t121` RT map. No new data acquisition.
- **Output**: `results/<run-name>/summary/signatures/sbs1_lrr_bias_per_study.feather` with per-(study, lookup_key) rows: `f_LRR_uncorrected`, `f_LRR_corrected`, `n_SBS1_pooled`, `n_CE_panel_bp`, `n_CL_panel_bp`, `ci_low`, `ci_high`, `n_bootstrap`, `power_status` (powered / underpowered), `verdict` (pass / retire / defer).
- **Tests**: at minimum, three regression tests:
  1. Per-mutation posterior recovers SBS1 = 1.0 for a synthetic mutation in pure CpG context with only SBS1 active.
  2. Aggregate LRR fraction matches a hand-computed value on a 4-mutation toy dataset.
  3. Bootstrap CI width shrinks as sample count grows on synthetic data.
- **Closure deliverable**: `doc/interpretations/2026-04-XX-t126-sbs1-lrr-bias-per-study.md` reporting the verdict and the next action per §6.

## Deviation policy

Any deviation from this pre-registration must be recorded in the closing interpretation document with:
- the deviation,
- when it was discovered,
- why it was applied,
- whether it changes the verdict.

Specifically: the verdict thresholds in §6 (the 0.45 mid-point, the ±10 pp CI cap, the n ≥ 500 power floor) must not be moved post-hoc to change the verdict.
