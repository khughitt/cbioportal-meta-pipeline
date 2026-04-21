---
id: "question:q001-normal-epithelial-clone-contamination-in-esophageal-studies"
type: "question"
title: "Do elevated NOTCH1 rates in cBioPortal esophageal studies reflect normal-epithelial clone contamination rather than tumor biology?"
status: "active"
ontology_terms: []
datasets: []
source_refs:
  - "cite:Yoshida2026"
  - "cite:Martincorena2018"
  - "cite:Poon2021"
  - "cite:Li2021"
related:
  - "topic:clonal-hematopoiesis-contamination"
  - "paper:Yoshida2026"
  - "paper:Martincorena2018"
  - "paper:Poon2021"
  - "paper:Li2021"
  - "paper:Bolton2020"
  - "topic:cohort-selection-bias-representativeness"
created: "2026-04-18"
updated: "2026-04-18"
---

# Do elevated NOTCH1 rates in cBioPortal esophageal studies reflect normal-epithelial clone contamination rather than tumor biology?

## Summary

Martincorena et al. 2018 (*Science*) — the primary study on normal esophageal clone colonization — provides direct quantitative evidence for this contamination risk. Deep targeted sequencing (74 genes, 870× median depth) of 844 contiguous 2 mm² biopsy samples from 9 donors (age 20–75) shows: **NOTCH1-mutant clones cover 30–80% of the normal esophageal epithelium in middle-aged and elderly donors**, while NOTCH1 is mutated in only approximately **~10% of ESCC tumors**. TP53 shows the exact inverse pattern: **5–37% of normal cells** carry TP53 mutations, but TP53 is mutated in **>90% of ESCCs**. The dN/dS selection coefficient for NOTCH1 truncating mutations in normal esophagus exceeds 50, making it the most strongly selected gene in the dataset.

If cBioPortal esophageal studies include samples with variable tumor purity or normal-tissue contamination (e.g., endoscopic biopsies), NOTCH1 mutation frequencies in our pipeline will be inflated by normal-clone signal rather than tumor biology. Normal-epithelial NOTCH1-mutant clones may additionally suppress tumor cell expansion (mouse model evidence cited in Yoshida2026), further confounding interpretation. The Poon2021 synonymous-passenger analysis of these same 9 donors independently confirms that NOTCH1 and TP53 together account for ~60% of all genome-wide positive selection detectable in normal esophageal epithelium.

## Why It Matters

- Incorrect inflation of NOTCH1 mutation rates would misrank it as a cancer driver in esophageal gene×cancer outputs.
- Cluster outputs grouping esophageal studies may be distorted if some studies have systematically lower tumor purity.
- If we produce a cancer driver overlay for esophageal carcinoma, NOTCH1's rank should be interpreted with explicit tumor-purity caveats.
- Analogous contamination could occur in other sites with known normal-tissue driver enrichment (skin NOTCH2/NOTCH3, gastric ARID1A, bronchial NOTCH1/TP53 with inverted ratios).

## Current Evidence

**Primary study (now summarized):** Martincorena et al. 2018 (*Science*, PMC6298579; `paper:Martincorena2018`) — deep targeted sequencing of 844 normal esophageal biopsies from 9 donors (age 20–75). Key numbers:
- NOTCH1 selected with dN/dS truncating >50 (strongest signal in the panel).
- NOTCH1 covers **30–80% of normal epithelium** in 5/6 donors aged 40+ years.
- TP53 covers **5–37% of normal epithelium** (highest in oldest donor).
- NOTCH1 mutation density: ~120 different mutations per cm².
- ~3,915 total positively selected driver mutations estimated in 17 cm² of normal tissue.
- Dominant signatures: SBS1/SBS5 (aging); NO APOBEC (SBS2/13) in normal tissue (present in ESCC).
- Donor-age regression: mutation count (P = 0.0068) and clone size (P = 0.027) both increase significantly with age.

**Supporting analyses:**
- Poon2021 re-analyzes these 9 donors using a synonymous-passenger framework and confirms that NOTCH1 + TP53 together account for ~60% of all genome-wide positive selection in normal esophagus.
- Li2021 independently demonstrates macroscopic NOTCH1/TP53-driven clones in normal esophagus from 5 donors (aged 85–93), with ~73.8% of esophageal samples harboring at least one driver mutation.
- Yoshida2026 review synthesizes these findings and notes the NOTCH1 mouse-model suppression of cancer-cell growth as additional mechanistic context.

No pipeline-level analysis has been done in this project to detect or flag this as an artifact. Tumor purity metadata is not uniformly available across cBioPortal studies, making direct correction difficult.

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
- Article notes: `paper:Yoshida2026`, `paper:Bolton2020`, `paper:Martincorena2017`
- Methods/Datasets: cBioPortal esophageal study list; MSK-IMPACT esophageal cohort (matched normal, should be clean)
