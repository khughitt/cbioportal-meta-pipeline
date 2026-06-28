---
type: question
title: What is the magnitude of normal-tissue SBS1/SBS5 contamination in unmatched-normal
  cBioPortal studies, and can per-tissue background subtraction reduce it?
status: active
created: '2026-04-18'
updated: '2026-04-18'
id: question:0008-signature-decomposition-tissue-background-subtraction
ontology_terms:
- mutational signatures
- unmatched normal
- tissue-of-origin
- SBS1
- SBS5
datasets: []
source_refs:
- paper:Alexandrov2020
- paper:Li2021
- paper:Xu2025
related:
- topic:signature-decomposition-unmatched-normal
- paper:Li2021
- paper:Xu2025
- paper:Yaacov2023
- question:0001-normal-epithelial-clone-contamination-in-esophageal-studies
- question:0007-cross-tissue-somatic-mutation-rate-variation-as-null-model
---

# What is the magnitude of normal-tissue SBS1/SBS5 contamination in unmatched-normal cBioPortal studies, and can per-tissue background subtraction reduce it?

## Summary

When cBioPortal studies lack patient-matched germline sequencing, normal cells contaminating the tumor biopsy contribute their own somatic mutations — predominantly SBS1 (clock-like CpG deamination) and SBS5 (clock-like, unknown mechanism) — to the observed mutation spectrum. Standard signature decomposition cannot distinguish the tumor's own SBS1/SBS5 signal from the normal-tissue contribution. The question is: how large is this contamination effect quantitatively (as a fraction of apparent SBS1/SBS5 exposure), and would subtracting a per-tissue normal-spectrum prior before decomposition reduce it to a negligible level?

## Why It Matters

- Overestimated SBS1/SBS5 exposures in unmatched-normal studies will make those studies appear to have more "aging-associated" mutation burden than matched-normal studies of the same cancer type, introducing a systematic batch effect in cross-study comparisons.
- Genes in late-replicating regions (LRR-enriched for SBS1) will have spuriously elevated apparent mutation rates in unmatched-normal studies — a direct gene-frequency confound in the `gene_cancer_study.feather` outputs.
- If quantifiable, the effect size informs whether it is worth implementing a background-subtraction Snakemake rule vs accepting the contamination as a tolerable noise floor.

## Current Evidence

- Li 2021: normal-tissue somatic burden varies from ~10 (pancreas) to ~69 (liver) mutations/exome across 9 organs; SBS1/SBS5 dominant in all.
- Xu 2025: GTEx pan-tissue coding mutation rates 0.21–2.49 mut/Mb; SBS18 universal; spectra available.
- Yaacov et al. report that SBS1 is LRR-biased in normal tissue but loses this bias in cancer, providing a potential diagnostic that is only applicable with WGS [@Yaacov2023].
- No published quantification of the per-study contamination effect size in unmatched-normal cBioPortal cohorts exists (as of April 2026).

## Thoughts

- The effect size likely scales with (1–tumor purity) × (normal-tissue SBS1/SBS5 burden per cell). For a 70% pure tumor biopsy with 100 total observed mutations, the normal-cell contribution is ~30 mutations, all SBS1/SBS5 dominated — possibly 20–30% of the apparent SBS1 exposure.
- A computationally tractable first test: compare SBS1/SBS5 ratios between matched-normal and unmatched-normal cBioPortal studies for the same cancer type (e.g., breast: TCGA BRCA matched-normal vs HER2-amplified panel-sequenced studies). A systematic elevation of SBS1 in unmatched studies would support the contamination hypothesis.
- Per-tissue background subtraction (Intervention 3 in `topic:signature-decomposition-unmatched-normal`) requires reference spectra from Li 2021 / Xu 2025 and is tractable but untested on this pipeline.

## Connections to Project

- Related hypotheses: none filed; this question could motivate a formal hypothesis about SBS1 excess as a contamination indicator.
- Required data or analyses:
  1. Run SigProfilerAssignment or MuSiCal on a subset of matched-normal vs unmatched-normal studies for the same cancer type; compare SBS1/SBS5 exposure distributions.
  2. Extract per-tissue reference spectra from Li 2021 or Xu 2025 supplemental tables.
  3. Implement background subtraction as a Snakemake rule and compare decomposition outputs before/after.
- Priority level: high — this directly affects the reliability of any signature-level analysis added to the pipeline.

## Related

- Topic notes: `topic:signature-decomposition-unmatched-normal`
- Article notes: `paper:Li2021`, `paper:Xu2025`, `paper:Yaacov2023`
- Related questions: `question:0001` (esophageal NOTCH1 contamination), `question:0007` (null model for normal-tissue background)
- Methods/Datasets: SigProfilerAssignment (Alexandrov lab), MuSiCal (Park lab); Li 2021 EGA data; Xu 2025 dbGaP data
