---
type: question
title: Does replication timing create systematic gene-level mutation rate inflation
  in cross-study aggregation?
status: active
created: '2026-04-18'
updated: '2026-04-18'
id: question:0003-replication-timing-as-gene-level-mutation-rate-confounder
ontology_terms: []
datasets:
- cBioPortal studies
- PCAWG
source_refs:
- paper:Yaacov2023
- paper:Yoshida2026
related:
- paper:Yaacov2023
- topic:mutation-rate-normalization
---

# Does replication timing create systematic gene-level mutation rate inflation in cross-study aggregation?

## Summary

Late-replicating genomic regions (LRR) accumulate more somatic mutations than early-replicating regions (ERR). Several mutational signatures are exclusively or predominantly active in LRR (e.g., SBS4/tobacco, SBS18/ROS) while others are ERR-restricted (e.g., SBS16, SBS88/colibactin). Genes physically located in LRR will therefore have higher background mutation rates independent of positive selection, and genes in ERR will have lower rates. The pipeline's gene × cancer frequency tables do not currently correct for per-gene replication timing position. The question is: how large is this effect in practice, and does it generate false positives or false negatives in cross-study driver-gene ranking?

## Why It Matters

- **False positives:** LRR-resident passenger genes could rank highly in mutation-frequency tables purely due to elevated background, not selection.
- **False negatives:** ERR-resident driver genes could appear under-mutated relative to LRR drivers, biasing comparative ranking across cancer types.
- **Cross-cancer comparability:** Cancers dominated by LRR-active signatures (e.g., tobacco-driven NSCLC with SBS4) will show globally elevated rates for LRR-resident genes — confounding signal when comparing lung vs. other cancer types.
- **Normal-cell contamination indicator:** Yaacov et al. 2023 show SBS1 is LRR-biased in normal tissues but not in cancer. Studies with residual normal-cell admixture might show a detectable SBS1 LRR signal absent from matched pure-tumor datasets — a potential data-quality flag.

## Current Evidence

- Yaacov et al. 2023 (Scientific Reports): comprehensive mapping of RT bias for 10+ signatures in normal cells; SBS4 exclusively LRR, SBS16/SBS88 exclusively ERR, SBS1 LRR only in normal cells.
- Lawrence et al. 2013 (Nature): mutation rate varies ~10-fold across the genome, strongly correlated with replication timing and transcription — foundational evidence for RT as a background rate driver.
- Iorio et al. 2018 SLAPenrich: accounts for exonic gene length and regional mutation rates in pathway enrichment but not per-signature RT stratification.
- The pipeline currently uses Bailey 2018 driver flags and CH annotation but no per-gene RT annotation.

## Thoughts

- Effect size is likely moderate but non-negligible: Lawrence et al. showed ~10-fold regional variation in background mutation rate, much of which tracks RT. In a frequency table that does not normalize for gene length (our current tables normalize per sample but not for gene length or RT), LRR genes will be structurally favored.
- Priority: medium. The most immediate gains are from CH-aware stratification (already implemented) and hypermutator exclusion (t081). RT normalization would be a third-tier refinement.
- A quick feasibility check: annotate all genes in the gene × cancer table with their ENCODE constitutive RT category (ERR/LRR) and run a correlation between per-gene mutation frequency rank and RT category. If this correlation is strong in non-driver genes (e.g., bottom 50% of frequency distribution), RT inflation is real and large enough to address.

## Connections to Project

- Related hypotheses: none formally filed yet — this question motivates a new hypothesis about background-rate confounding.
- Required data or analyses: ENCODE constitutive RT annotation (BED file), cross-reference with gene coordinates (GRCh37/GRCh38 already in data/); then per-gene ERR/LRR classification.
- Priority level: low-to-medium (behind t081/hypermutator pipeline and CH stratification in the active task backlog).

## Related

- Article notes: `paper:Yaacov2023`, `paper:Yoshida2026`
- Methods/Datasets: constitutive RT regions from Yaacov et al. 2022 (ENCODE 26-tissue RT profiles); SigProfilerExtractor for signature-level attribution; cBioPortal studies via existing pipeline
