---
type: topic
title: Pan-cancer mutation landscape
status: active
created: '2026-04-13'
updated: '2026-04-13'
id: topic:pan-cancer-mutation-landscape
ontology_terms: []
source_refs: []
related:
- paper:Kandoth2013
- paper:Lawrence2014
- paper:Bailey2018
- paper:Ellrott2018
- paper:Hoadley2018
- paper:Zehir2017
- paper:Bandlamudi2026
- paper:PCAWG2020
- topic:cancer-driver-genes
- topic:pan-cancer-interpretive-frames
---

# Pan-cancer mutation landscape

## Summary

Cross-cancer somatic mutation patterns: per-gene frequency distributions, tissue-of-origin
signals, mutation-burden ranges, co-occurrence / mutual exclusivity, and the long-tail of
low-frequency drivers. This topic frames the interpretation of `summary/mut/matrix/gene_cancer.feather`
and the gene/cancer clustering outputs of this pipeline.

## Key Concepts

- **Mutation-burden range across cancer types is huge.** Kandoth 2013 reports ~30× dynamic range
  (LUSC 8.15 mut/Mb → AML 0.28 mut/Mb across 12 TCGA cancer types). PCAWG 2020 confirms similar
  patterns at WGS resolution. Per-cancer-type baselines are essential for interpreting any
  per-gene ratio.
- **Driver-gene catalog grows with cohort size.** Kandoth 2013 (3,281 tumors) → 127 SMGs.
  Lawrence 2014 (4,742) → 224 SMGs. Bailey 2018 (9,423) → 299 consensus drivers. Lawrence 2014's
  saturation analysis quantifies the cohort-size requirement per cancer type.
- **TP53 dominates pan-cancer.** ~41% of all tumors (Zehir 2017 MSK-IMPACT 10k); 95% in HGSOC,
  89% in serous endometrial. Significant in 27/33 cancer types (Bailey 2018).
- **Long-tail vs canonical drivers.** Bailey 2018: 142 of 299 consensus drivers are
  tumor-type-specific (single cancer); 87 are multi-cancer; 29 are detectable only in the
  pooled pan-cancer run.
- **Tissue-borrowed driver phenomenon.** Bailey 2018 reports 19% of driver mutations occur in
  genes that are drivers in a *different* cancer than the patient's primary site. Bandlamudi 2026
  independently reports ~1/3 of detected drivers in "non-canonical" tissue contexts behave
  differently (more subclonal, later in tumor evolution).

## Current State of Knowledge

The field has converged on:
1. **A consensus driver-gene catalog** (Bailey 2018 Table S1) used as the reference list across
   pan-cancer studies.
2. **Per-cancer-type baselines for mutation rate** as the unit of comparison (not raw counts).
3. **WES + WGS + targeted-panel as complementary sources.** WES (TCGA / MC3) gives saturation
   coverage of coding regions for ~10k tumors; targeted panels (MSK-IMPACT, GENIE) give 50-100k
   tumors at much narrower coverage; WGS (PCAWG ~2,658) adds non-coding / structural drivers.

Open frontiers include non-canonical-context drivers (Bandlamudi 2026), tissue-of-origin
clustering complement (Hoadley 2018), and the still-unsaturated long tail in rarer cancers
(Lawrence 2014's per-cancer-type required-N estimates remain unmet for many tumor types).

## Controversies & Open Questions

- **How much of the long tail is real signal vs background-rate inflation?** Lawrence 2014's
  saturation curves give per-cancer-type expected SMG counts; outputs claiming many more drivers
  for low-mutation-rate cancers are likely false-positive-laden.
- **Is "tissue-of-origin dominates" or "alteration-type dominates"?** Hoadley 2018 (integrated
  multi-omics) says lineage; Ciriello 2013 (genomic events alone) says alteration-type. Neither
  ran mutations-only clustering as comparison. See `topic:pan-cancer-interpretive-frames`.

## Relevance to This Project

Our pipeline aggregates across cBioPortal cancer studies into a single
`summary/mut/matrix/gene_cancer.feather`. This topic is the interpretive frame: what counts as
"a gene driver" for a cancer, how to compare per-cancer rates fairly, and how to read the
long tail of our outputs against published reference catalogs.

Concrete sanity checks: (i) does TP53 appear in 27+ cancer types in our outputs (matches Bailey
2018)? (ii) do per-cancer mutation-burden medians span ~30× and match Kandoth 2013 / PCAWG
ranges? (iii) does our gene-frequency long tail per cancer type stay within Lawrence 2014's
saturation-predicted range, or is it inflated?

## Key References

Kandoth2013 / Lawrence2014 / Bailey2018 (driver catalog evolution); Ellrott2018 (MC3 reference
WES MAF); Zehir2017 / Bandlamudi2026 (panel-cohort landscapes); Hoadley2018 (cell-of-origin
clustering frame); PCAWG2020 (WGS complement).
