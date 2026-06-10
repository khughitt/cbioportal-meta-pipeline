---
type: question
title: Does the high normal-tissue mCA burden in esophagus mucosa produce detectable
  clone-signal in cBioPortal esophageal study CNA outputs?
status: active
created: '2026-04-18'
updated: '2026-04-18'
id: question:0004-mca-burden-in-esophageal-vs-other-study-tissues
ontology_terms: []
datasets: []
source_refs:
- paper:Gao2023
- paper:Yoshida2026
related:
- topic:clonal-hematopoiesis-contamination
- paper:Gao2023
- paper:Yoshida2026
- question:0001-normal-epithelial-clone-contamination-in-esophageal-studies
---

# Does the high normal-tissue mCA burden in esophagus mucosa produce detectable clone-signal in cBioPortal esophageal study CNA outputs?

## Summary

Gao2023 finds that 10% of normal esophagus mucosa samples carry detectable mCAs, predominantly chr9q CNLoH events (137 of 147 esophageal mCAs). These chr9q events likely represent second hits to NOTCH1 (9q34) in normal esophageal clones that are positively selected in morphologically normal tissue without obligate progression to cancer. If any cBioPortal esophageal studies sequenced biopsy specimens with variable tumor purity (or enrolled subjects with high normal-tissue clone burden), chr9q LOH/CNLoH events would appear inflated in aggregate CNA frequency tables relative to their true tumor-intrinsic frequency. The question is whether this is detectable or practically significant in this pipeline's outputs.

## Why It Matters

- The pipeline currently focuses on SNV frequencies (gene×cancer mutation counts and ratios). CNA/LOH data are outside current scope per science.yaml.
- However, if CNA data are ever incorporated, or if this project is extended to include LOH-based driver calls, normal-tissue chr9q CNLoH contamination would be a significant background source specific to esophageal samples.
- Understanding the magnitude of normal-tissue mCA burden establishes what a plausible contamination effect size would be: 10% sample-level prevalence in esophagus mucosa is high enough that it could move population-level CNA frequency estimates by several percentage points in unmatched-normal studies.
- Adjacent question (q001): NOTCH1 SNV contamination from normal esophageal clones — Gao2023 provides the CNA complement to that SNV-level concern.

## Current Evidence

- Gao2023 establishes 10% mCA prevalence in esophagus mucosa (GTEx v8, n=1,473 samples from 947 donors aged 20-70), with chr9q CNLoH as the dominant event (93% of esophageal mCAs).
- Normal adrenal (6.7%) and pituitary (2.8%) mCA prevalences are also notable but less directly relevant to cBioPortal's cancer study mix.
- Most tissues have <2% mCA prevalence — esophagus mucosa is a clear high-burden outlier among solid tissues.
- No mCA analysis has been performed on the cBioPortal studies in this pipeline; the current pipeline ingests SNV/indel MAF files and does not process CNA segment data.
- The normal-tissue mCA prevalence far exceeds malignant cancer incidence for adrenal (0.0001-0.04%) and pituitary (0.0005-0.5%), confirming most mCAs are non-progressive — but they are still present in biopsied tissue.

## Thoughts

- The current pipeline does not incorporate CNA/LOH data, so this contamination does not affect current gene×cancer SNV frequency outputs.
- If CNA data is later added: flag esophageal studies with <100% estimated purity or without matched-normal sequencing for elevated chr9q CNLoH background. The ~10% background prevalence in normal esophagus mucosa is the relevant null to test against.
- For adrenal and pituitary cancer studies: if these are in the cBioPortal study list, their chr3 loss frequencies may be partially influenced by normal-tissue clone background (though this is less of a concern than for esophagus, given the lower sample numbers for these tumor types in cBioPortal).
- Priority: low for the current pipeline (SNV-only). Re-elevate if CNA integration is planned.

## Connections to Project

- Related hypotheses: none filed; could inform a future hypothesis about tissue-specific CNA background inflation if CNA data are incorporated.
- Required data or analyses: list of esophageal studies in the cBioPortal pipeline input; their tumor purity metadata (if available); whether matched-normal sequencing is annotated for those studies.
- Priority level: low (current pipeline is SNV-only; CNA contamination is out of current scope).

## Related

- Topic notes: `topic:clonal-hematopoiesis-contamination` (SNV-level CH; same family of problems)
- Article notes: `paper:Gao2023`, `paper:Yoshida2026`
- Related question: `question:0001-normal-epithelial-clone-contamination-in-esophageal-studies` (NOTCH1 SNV analog)
- Methods/Datasets: GTEx v8 (Gao2023); cBioPortal esophageal study list; matched-normal annotation from `matched_normal_studies` config key
