---
type: question
title: Are common-fragile-site (CFS) loci a distinct gene-level confounder class,
  separable from broad replication-timing effects?
status: active
created: '2026-04-27'
updated: '2026-04-28'
id: question:0014-cfs-as-distinct-confounder-class
ontology_terms:
- common fragile sites
- replication stress
- structural instability
datasets:
- cBioPortal gene_cancer_study_ratio_annotated.feather
- Published CFS catalogues (FRA3B/FHIT, FRA16D/WWOX, FRA6E/PARK2, FRA4F/GRID2, etc.)
source_refs: []
related:
- question:0003-replication-timing-as-gene-level-mutation-rate-confounder
- interpretation:0009-t131-full-pan-cancer-dndscv-run
- hypothesis:0001-non-tumor-signal-contamination
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- task:t153
---

# Are CFS loci a distinct confounder class from broad replication-timing effects?

## Summary

The t131 full pan-cancer dNdScv run + t145 mean_inclusive fix surfaced a residual cluster of
common-fragile-site (CFS)-overlapping genes — FHIT (FRA3B), WWOX (FRA16D), MACROD2, IMMP2L,
GRID2 (FRA4F), CNTNAP2, LSAMP, NKAIN3, KCNIP4, SGCZ, LRRTM4 — at the head of the raw
mutation-frequency distribution even after the methodological fix. CFS biology is real
(replication-stress-driven structural instability at characteristic chromosomal regions) but
the project's SNV-only pipeline consumes this signal as point-mutation frequency rather
than as structural variation, producing inflated apparent SNV rates at CFS loci.

The question is whether CFS loci constitute a **distinct confounder class** from the broader
replication-timing (RT) covariate already framed in `q003`. They overlap (CFS regions are
typically late-replicating) but are not identical: CFS regions have specific structural
features (R-loops, large genes, fragile-site motifs) that drive replication-stress-induced
DSBs and elevated structural variation, with consequences for SNV rate that may exceed
the RT-only expectation.

## Why It Matters

- Decides whether `q003` (RT confounder) captures CFS loci as a special case, or whether
  CFS needs separate treatment in the project's correction stack.
- Directly affects the residual top-N in `h02` — whether the surviving large-gene signal
  in dNdScv (TTN, AHNAK, AHNAK2, ABCA13) is "RT-late residual" or "CFS-overlap residual"
  changes the next correction step.
- Informs `h01` channel partition (P2) — CFS is the "channel (c)" claim; without
  separating it, the contamination correction may misattribute CFS signal to CH or
  normal-clone channels.

## Current Evidence

- t131 + t145 surfaced the CFS-cluster pile-up empirically; FHIT, MACROD2, IMMP2L, GRID2,
  CNTNAP2, LSAMP appear at 22–26% in their best cancer-type after the t145 fix (down from
  65–84% before, but still prominent).
- Published CFS catalogues exist (Le Tallec 2013; Glover 2017 reviews); a per-gene CFS-
  overlap annotation is straightforward to build.
- RT data exists in the pipeline (`t121` gene-level RT map from the
  `question:0009-sbs1-lrr-bias-as-normal-contamination-flag` work); the
  RT-vs-CFS comparison can be done on the existing artifacts.

## Thoughts

- The cleanest test: regress per-gene mutation rate on `(RT-late-fraction, CFS-overlap)`
  with both as covariates. If `CFS-overlap` carries a non-zero coefficient after controlling
  for RT, CFS is a distinct confounder class.
- The structural-variation point matters: if the project ever ingests CNA / SV data
  (currently out of scope, `t055` deferred), CFS loci should be the first place to look —
  large structural events at CFS may explain SNV-call inflation indirectly (calling
  artifacts in highly-rearranged regions).
- A per-CFS-region rate inflation factor, derived from this question, becomes a candidate
  correction column in the annotated feathers.

## Connections to Project

- Related hypotheses: `h01` (channel partition), `h02` (residual confounder identification),
  candidate `h05` (cross-tissue background — CFS rate may itself be tissue-specific).
- Required data or analyses: per-gene CFS-overlap annotation (straightforward join);
  RT-vs-CFS regression on existing pipeline outputs.
- Tracking task: `t153`.
- Priority level: P3. Specialization of `q003`; depends on the broader RT framing being
  done first.

## Related

- Topic notes: `topic:mutation-rate-normalization` (CFS as covariate).
- Article notes: Le Tallec 2013 (CFS catalogue); Glover 2017 (CFS reviews); [@Lawrence2014]
  (gene-length confounder, partially overlapping); [@Yaacov2023] (RT bias on SBS1).
- Methods/Datasets: per-gene CFS overlap (manual curation from published lists); existing
  `t121` RT map; pipeline gene-frequency tables.
