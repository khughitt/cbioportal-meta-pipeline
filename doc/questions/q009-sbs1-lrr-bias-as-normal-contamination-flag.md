---
id: "question:q009-sbs1-lrr-bias-as-normal-contamination-flag"
type: "question"
title: "Can the SBS1 late-replicating-region bias (present in normal tissue, absent in cancer) serve as a practical contamination quality flag for cBioPortal studies?"
status: "active"
ontology_terms:
  - mutational signatures
  - replication timing
  - SBS1
  - normal tissue contamination
  - tumor purity
datasets:
  - PCAWG
  - SomaMutDB
source_refs:
  - "cite:Yaacov2023"
related:
  - "topic:signature-decomposition-unmatched-normal"
  - "article:Yaacov2023"
  - "question:q003-replication-timing-as-gene-level-mutation-rate-confounder"
  - "question:q008-signature-decomposition-tissue-background-subtraction"
created: "2026-04-18"
updated: "2026-04-18"
---

# Can the SBS1 late-replicating-region bias (present in normal tissue, absent in cancer) serve as a practical contamination quality flag for cBioPortal studies?

## Summary

Yaacov et al. 2023 (Scientific Reports) demonstrated that SBS1 mutations accumulate preferentially in late-replicating regions (LRR) of the genome in normal tissue, but lose this LRR bias in matched cancer samples. This represents a potential topographic fingerprint: a cBioPortal study showing SBS1 with a detectable LRR enrichment — assessed by mapping SBS1-attributed mutations to constitutive RT regions — would carry an excess of normal-tissue-origin SBS1 relative to tumor-origin SBS1. The question is whether this diagnostic is practically computable from panel/WES-based mutation calls and, if so, whether it provides a usable contamination flag.

## Why It Matters

- If operable, it would provide a direct (not proxy) indicator of normal-tissue contamination in individual studies, independent of assumptions about tumor purity or cohort composition.
- It would complement the SBS1/SBS5 ratio proxy (Intervention 2 in `topic:signature-decomposition-unmatched-normal`) with a mechanistically grounded signal.
- For WGS-based studies in the pipeline (e.g., if the MC3 TCGA WGS data is incorporated), this diagnostic is immediately applicable.

## Current Evidence

- Yaacov 2023: SBS1 LRR bias in normal tissue is highly reproducible (R = 0.967 between two independent cohorts) and statistically significant (Wilcoxon P < 2.2×10⁻¹⁶). The change between normal and cancer contexts is consistent across all four matched tissue pairs examined.
- The signal requires aligning mutations to constitutive RT regions (~40% of the genome) and comparing early vs. late enrichment. For WGS, this is feasible with SigProfilerTopography or equivalent tools.
- For panel/WES data (typical of cBioPortal): per-gene replication timing annotations exist (ENCODE RT data, mapped to RefSeq genes). A coarser version of the test — compare SBS1 mutation density across ERR-annotated vs LRR-annotated genes — is possible but has lower power due to fewer mutations per sample.

## Thoughts

- The main practical constraint is statistical power. Detecting an LRR enrichment of SBS1 requires enough SBS1-attributed mutations to compare regional distributions. For panel-sequenced studies with 50–200 mutations per sample, this test is unlikely to be powered per-sample; it might be powered at the per-study aggregate level (pooling all samples of the same study).
- A simpler proxy: at the gene level, LRR-resident genes should show higher per-sample SBS1 mutation counts in studies with normal contamination. This can be tested with existing pipeline outputs by crossing gene positions with LRR/ERR annotations.
- The Yaacov 2023 paper does not provide a standalone computational tool for this analysis; the methods use SigProfilerMatrixGenerator + custom RT-region annotation. SigProfilerTopography (a companion tool from the Alexandrov lab) is designed to compute topographic biases and would be the most accessible implementation pathway.

## Connections to Project

- Related hypotheses: none filed.
- Required data or analyses:
  1. Obtain constitutive replication-timing region annotations from the Yaacov 2023 / ENCODE RT data.
  2. Annotate pipeline genes with ERR/LRR designation.
  3. For a test subset of matched-normal vs unmatched-normal studies, compute per-study SBS1 mutation density in ERR vs LRR genes; compare distributions.
  4. For WGS-level studies: apply SigProfilerTopography to compute formal LRR bias delta values and compare with expected cancer vs normal tissue values.
- Priority level: medium for WGS studies; low for panel-only studies in the current pipeline. Becomes high if WGS inputs are added.

## Related

- Topic notes: `topic:signature-decomposition-unmatched-normal`
- Article notes: `article:Yaacov2023`
- Related questions: `question:q003` (RT as gene-level mutation-rate confounder), `question:q008` (SBS1/SBS5 contamination magnitude)
- Methods/Datasets: SigProfilerTopography; ENCODE replication timing data (constitutive ERR/LRR regions); Yaacov 2023 code (see Yaacov et al. 2022, the companion cancer-RT paper for RT region construction)
