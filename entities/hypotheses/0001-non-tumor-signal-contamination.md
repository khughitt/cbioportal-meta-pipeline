---
type: hypothesis
title: Non-tumor signal contaminates cBioPortal mutation-frequency estimates in identifiable,
  partially correctable ways
status: proposed
created: '2026-04-27'
updated: '2026-04-27'
id: hypothesis:0001-non-tumor-signal-contamination
phase: active
source_refs:
- paper:Martincorena2018
- paper:Yaacov2023
- paper:Li2021
- paper:Yoshida2026
- paper:Xu2025
- paper:LeeSix2018
related:
- question:0001-normal-epithelial-clone-contamination-in-esophageal-studies
- question:0002-normal-breast-cna-background-chr1q-chr16q
- question:0004-mca-burden-in-esophageal-vs-other-study-tissues
- question:0005-gli1-normal-tissue-hotspot-inflation
- question:0006-ch-priority-gene-completeness
- question:0007-cross-tissue-somatic-mutation-rate-variation-as-null-model
- question:0008-signature-decomposition-tissue-background-subtraction
- question:0010-cuplr-style-tof-classifier-for-suspect-normal-samples
- topic:clonal-hematopoiesis-contamination
- topic:signature-decomposition-unmatched-normal
---

# Hypothesis: Non-tumor signal contaminates cBioPortal mutation-frequency estimates in identifiable, partially correctable ways

## Organizing Conjecture

A measurable fraction of high-frequency genes in cBioPortal (and AACR GENIE) cross-study
mutation tables reflects mutational processes operating in **non-tumor** cell populations —
clonal hematopoiesis (CH), normal-tissue clonal expansions, age- and tissue-specific somatic
background, and replication-stress / common-fragile-site instability. These contributions are
not random noise: they are tissue-, gene-, and study-design-specific (matched-vs-unmatched
normal calling, panel coverage), and they are partially correctable via tissue/process-specific
reference spectra and study-level overlays already built in the project.

## Proposition Bundle

### Core Propositions

- **P1 (presence).** For at least one canonical CH gene set (Bolton 2020 7-gene panel) and at
  least one tissue with documented normal-clonal expansion (esophagus, breast, skin), the
  per-gene mutation rate in unmatched-normal cBioPortal studies is significantly elevated
  relative to matched-normal studies of the same cancer-type, after stratifying on cohort
  composition and panel callability.
- **P2 (mechanism partition).** The elevation in P1 partitions into at least three
  distinguishable channels: (a) CH leakage (Coombs 2017, Bolton 2020), (b) normal-tissue
  clonal contamination (Martincorena 2018, Yokoyama 2019), and (c) replication-stress / CFS
  loci (FHIT, MACROD2, IMMP2L, GRID2, LSAMP, …). Each channel has a distinct gene-level
  signature recoverable from existing project artifacts.
- **P3 (correctability).** Per-tissue/per-process background subtraction using the project's
  reference spectra (`t111`) and CH-priority annotations (`t087`) materially reduces the
  apparent driver-frequency for at-risk genes in unmatched-normal studies, without inducing a
  symmetric over-correction in matched-normal studies. "Materially" = ≥1 percentage point
  shift on per-gene rates AND a directional rank change for ≥1 gene in the top-100.

### Supporting Or Auxiliary Propositions

- The asymmetric correction effect (large on unmatched, small on matched) is itself a
  validation that the correction is tracking the intended channel.
- The sum of corrections does not materially affect canonical drivers (TP53, KRAS, PIK3CA,
  APC, PTEN, BRAF, EGFR, NRAS, IDH1) — these survive contamination correction with rank and
  rate within tolerance, providing a positive control.
- The set of genes for which correction matters is enriched for CH genes, tissue-specific
  normal-clone genes (NOTCH1 in esophagus, GLI1 hotspot genes, etc.), and CFS loci, not for
  random gene strata.

## Current Uncertainty

- Multiple independent confounders are still entangled: panel-vs-WES sequencing depth,
  matched-vs-unmatched-normal calling, cohort composition (primary vs metastatic), and
  per-study cancer-type heterogeneity. The corrections need to be applied as a stack, not
  in isolation.
- The "expected normal background" is itself imperfect — Li 2021 covers 9 tissues, not the
  full set; matching cBioPortal cancer-types to Li 2021 tissues is itself a modeling choice.
- The CH priority gene panel (Bolton 2020 7-gene) may be incomplete (`q006`); residual CH
  leakage outside the 7 genes would be silently absorbed into apparent driver rates.

## Predictions

- For every cancer-type with both matched and unmatched cohorts in the pipeline (BRCA, COAD,
  PRAD, LUAD, etc.), the matched-vs-unmatched per-gene rate gap concentrates on a small,
  characterizable gene set (CH + tissue normal-clone + CFS) rather than spreading evenly.
- After correction, the residual matched-vs-unmatched gap on CH genes drops by ≥50% on
  average; the gap on canonical drivers stays within ±10% (no over-correction).
- Esophageal NOTCH1 rates (`q001`) drop after normal-tissue spectrum subtraction by an amount
  consistent with Martincorena 2018's reported normal-esophagus NOTCH1 burden in the same
  age range.

## Falsifiability

- If, after stratifying on cohort composition and panel callability, the matched-vs-unmatched
  per-gene rate gap is uniformly distributed across genes (no enrichment in CH / normal-clone
  / CFS sets), P2 is falsified — contamination is not the dominant explanation for the gap.
- If background subtraction shifts canonical drivers by more than the long-tail genes (i.e.
  the correction is symmetric across drivers and contamination genes), P3 is falsified — the
  correction is not specific.
- If the correction's effect size on at-risk genes is below the noise floor of bootstrap
  resampling on per-study counts, the hypothesis is operationally vacuous even if directionally
  correct.

## Supporting Evidence

- **Literature.** Martincorena 2018 — NOTCH1 in normal esophagus at rates exceeding the
  cancer rate in the same tissue. Coombs 2017 / Bolton 2020 — CH leakage signature. Yaacov
  2023 — normal-tissue replication-timing bias for SBS1. Li 2021 — body-map normal somatic
  mutation rates as null model. Lee-Six 2018 — normal-colon clonal expansions; the same
  drivers dominate normal expansions and the cancers.
- **Empirical (project).** t110 BRCA matched-vs-unmatched comparison (negative for the SBS1
  ratio specifically but established the comparison framework). t126 SBS1 LRR-bias-per-study
  (q009 retired but methodology validated). t131 full pan-cancer dNdScv run surfaced
  CFS-overlapping genes (FHIT, MACROD2, IMMP2L, …) at the head of the raw distribution after
  the t145 fix — consistent with channel (c).
- **Infrastructure built (un-exploited).** `t111` per-tissue reference spectra (built
  2026-04-19, idle); `t081` hypermutator annotation; `t087` graded CH contamination flag;
  `annotate_ch.py` 7-gene priority overlay.

## Disputing Evidence

- t110 (BRCA matched vs unmatched) found no SBS1 excess in the unmatched cohort and no
  threshold-able SBS1/SBS5 ratio shift. This is evidence *against* the SBS1-as-flag
  formulation specifically, not against the broader contamination claim — but it constrains
  which channels are detectable on this data.
- The matched-vs-unmatched contrast is confounded with assay (WES vs panel) and cohort
  (TCGA vs MSK clinical sequencing) in many cases; clean isolation of the contamination
  signal may require deliberate cohort matching beyond what the project currently does.
- For some genes (NOTCH1, TP53), normal-tissue clonal expansion is evidence of *real*
  positive selection in normal epithelium, not a "contamination" — the framing as
  contamination is correct only when the question is "what's happening in the cancer cells."

## Evidence Needed To Shift Belief

- **Decisive supporting test (P1):** Run `t127` (first q008 quantitative pass) over the 10k
  config with `t111` reference spectra, comparing per-gene rates before and after subtraction
  on `tcga_mc3` (matched) vs `msk_impact_2017` (unmatched) for breast cancer. Expectation:
  CH gene rates drop in unmatched, drivers unchanged.
- **Decisive disputing test:** A cleanly cohort-matched primary-only comparison (TCGA primary
  WES vs a primary-only MSK cohort, same cancer-type, same age range) shows no per-gene rate
  gap after panel-callability correction — meaning matched-vs-unmatched-normal status is not
  driving the apparent rate inflation.
- **Channel partition (P2):** A multi-channel decomposition (CH + normal-tissue + CFS)
  applied to the per-gene matched-vs-unmatched gap, with each channel's contribution
  separately bounded.

## Related Work

- **Topics:** `topic:clonal-hematopoiesis-contamination`,
  `topic:signature-decomposition-unmatched-normal`, `topic:mutation-rate-normalization`.
- **Questions subsumed:** q001, q002, q004, q005, q006, q007, q008, q010 (q009 retired).
- **Sibling hypotheses:** `hypothesis:0005-healthy-somatic-background-atlas` (the
  cross-individual, cross-tissue, cross-age generalization of the "normal background"
  notion); `hypothesis:0002-cross-study-ranking-divergence-is-structured` (methodological
  partner — same gene set, ranking-axis perspective).
