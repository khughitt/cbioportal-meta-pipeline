---
type: question
title: Which cBioPortal studies carry treatment-induced signatures (SBS11/SBS31/SBS35/SBS87)
  that must be flagged as a confound stratum before the positive-control scan?
status: partial
created: '2026-05-31'
updated: '2026-06-01'
id: question:0024-treatment-exposed-cohort-chemotherapy-signature
ontology_terms: []
datasets: []
source_refs:
- paper:Diamond2023
- paper:Crisafulli2022
- paper:Pleasance2020
- paper:Maura2023
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- method:h08-agnostic-association-model
- topic:clinical-translational-signatures
- topic:signatures-hematologic-malignancies
---

# Which cBioPortal studies carry treatment-induced signatures (SBS11/SBS31/SBS35/SBS87) that must be flagged as a confound stratum before the positive-control scan?

## Summary

Treatment-induced and prior-exposure signatures (temozolomide/SBS11, platinum/SBS31-35, thiopurine/SBS87) appear in pre-treated and relapsed cohorts and will bleed into agnostic covariate associations as batch-like confounders. Before H08a runs, treatment-exposed studies need to be identified and flagged as a confound stratum.

## Why It Matters

- Decision affected: study-level eligibility/stratification for the
  `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and` scan; the `treatment history` confounder in the method's adjustment set becomes operational only if exposed cohorts are labelled.
- Risk if unanswered: iatrogenic signatures masquerade as novel covariate->signature associations, or contaminate de novo estimates in pooled cancer types.

## Current Evidence

- `paper:Diamond2023` (chemotherapy signatures as temporal barcodes in tMN) and `paper:Crisafulli2022` (TMZ induces SBS11 in CRC) show treatment signatures are strong and specific.
- `paper:Pleasance2020` (advanced/treated tumors) and `paper:Maura2023` (treated myeloma) are exemplars of cohorts where these signatures dominate.
- The pipeline already has a `matched_normal_studies` config list; a parallel treatment-exposed flag is the natural mechanism.
- 2026-06-01 t181 operationalized this for the
  `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and` MC3 substrate: `tcga_mc3` is explicitly marked
  study-level unexposed (`treatment_exposed_study = 0`, `treatment_exposed_fraction = 0.0`) while
  patient-level neoadjuvant labels remain available as `treatment_exposed_clinical`.

## Thoughts

- Best current interpretation: build a treatment-exposed study flag (and a per-study fraction-treated field) as a nuisance covariate / exclusion stratum before the positive-control scan.
- Major uncertainty: completeness of treatment metadata across cBioPortal studies; many lack reliable prior-therapy annotation.
- `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`-facing status: implemented for the MC3-only positive-control substrate.
- Broader `hypothesis:0009-treatment-induced-signature-frequency-contamination` status: `task:t206` has produced a non-TCGA metadata scaffold and manual review.
  The review confirms 11 broad treatment-exposed study candidates, but separates them from narrower
  DNA-damaging-therapy expectations because several are ICB, endocrine, targeted, or
  castration-resistant cohorts.
  The next unresolved piece is config/schema handling for mixed cohorts with sample-level fractions
  before the frequency-table impact pass.

## Connections to Project

- Related hypotheses: `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`
  (treatment is a named confounder).
- Required data or analyses: cBioPortal study-metadata audit for treatment exposure; config field addition; stratification rule.
- Priority level: P2.

## Related

- Topic notes: `topic:clinical-translational-signatures`, `topic:signatures-hematologic-malignancies`
- Article notes: `paper:Diamond2023`, `paper:Crisafulli2022`, `paper:Pleasance2020`, `paper:Maura2023`
- Methods/Datasets: `method:h08-agnostic-association-model`
