---
id: "question:q001-normal-epithelial-clone-contamination-in-esophageal-studies"
type: "question"
title: "Do elevated NOTCH1 rates in cBioPortal esophageal studies reflect normal-epithelial clone contamination rather than tumor biology?"
status: "active"
ontology_terms: []
datasets: []
source_refs:
  - "cite:Yoshida2026"
related:
  - "topic:clonal-hematopoiesis-contamination"
  - "article:Yoshida2026"
  - "article:Bolton2020"
  - "topic:cohort-selection-bias-representativeness"
created: "2026-04-18"
updated: "2026-04-18"
---

# Do elevated NOTCH1 rates in cBioPortal esophageal studies reflect normal-epithelial clone contamination rather than tumor biology?

## Summary

Yoshida 2026 (and the primary studies it synthesizes) documents a striking inversion in esophageal tissue: NOTCH1 mutations are present in ~66% of normal esophageal epithelial clones but only ~15% of esophageal squamous cell carcinomas, while TP53 shows the reverse pattern (~30% normal vs ~95% tumor). Normal-epithelial NOTCH1-mutant clones may even suppress tumor cell expansion via antagonistic epistasis with TP53/RB1. If cBioPortal esophageal studies include samples with variable tumor purity or normal-tissue contamination (e.g., endoscopic biopsies), NOTCH1 mutation frequencies in our pipeline could be inflated by normal-clone signal rather than tumor-cell signal.

## Why It Matters

- Incorrect inflation of NOTCH1 mutation rates would misrank it as a cancer driver in esophageal gene×cancer outputs.
- Cluster outputs grouping esophageal studies may be distorted if some studies have systematically lower tumor purity.
- If we produce a cancer driver overlay for esophageal carcinoma, NOTCH1's rank should be interpreted with explicit tumor-purity caveats.
- Analogous contamination could occur in other sites with known normal-tissue driver enrichment (skin NOTCH2/NOTCH3, gastric ARID1A, bronchial NOTCH1/TP53 with inverted ratios).

## Current Evidence

- Yoshida 2026 review synthesizes esophageal data establishing the NOTCH1 inversion as a robust observation across multiple cohorts.
- Primary evidence: Martincorena et al. 2018 (*Nature*) — age-related colonization of normal esophagus by mutant clones; Yokoyama et al. 2019 (*Science*) — somatic mutant clones colonize esophagus.
- No pipeline-level analysis has been done in this project to flag this as a potential artifact.
- Tumor purity metadata is not uniformly available across cBioPortal studies, making direct correction difficult.

## Thoughts

- The simplest first-pass check: compare NOTCH1 mutation rates across esophageal studies in our pipeline, stratified by study type (endoscopic biopsy cohort vs surgical resection cohort) — biopsy cohorts are more likely to have lower tumor purity.
- A second check: cross-reference NOTCH1 ranking in esophageal studies that use matched-normal sequencing (where normal-clone variants are subtracted) vs tumor-only studies.
- The effect may be small enough to be lost in the noise for cross-study aggregation, but it is worth flagging in any esophageal-specific output.

## Connections to Project

- Related hypotheses: none yet filed; could inform a future hypothesis about tissue-type-specific contamination patterns.
- Required data or analyses: tumor purity metadata (if available in cBioPortal clinical data for esophageal studies); NOTCH1 mutation rate distribution across esophageal studies; matched vs unmatched normal stratification for esophageal subset.
- Priority level: medium — the CH contamination issue (DNMT3A/TET2/ASXL1) is a higher-priority and more quantitatively grounded concern; this is a secondary contamination risk specific to esophageal outputs.

## Related

- Topic notes: `topic:clonal-hematopoiesis-contamination` (CH in blood, same conceptual family)
- Article notes: `article:Yoshida2026`, `article:Bolton2020`, `article:Martincorena2017`
- Methods/Datasets: cBioPortal esophageal study list; MSK-IMPACT esophageal cohort (matched normal, should be clean)
