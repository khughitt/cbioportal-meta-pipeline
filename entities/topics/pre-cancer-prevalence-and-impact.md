---
type: topic
title: Pre-cancer source fitness in cBioPortal and GENIE
status: active
created: '2026-04-27'
updated: '2026-05-02'
id: topic:pre-cancer-prevalence-and-impact
ontology_terms:
- pre-cancer
- dysplasia
- field cancerization
- clonal expansion
datasets:
- dataset:cbioportal
- dataset:aacr-genie
source_refs: []
related:
- hypothesis:0006-pre-malignant-n-minus-1-driver-carriage
- hypothesis:0004-mhn-pathway-ordering
- question:0012-mutation-ordering-cross-sectional-inference
- topic:normal-tissue-mutation-atlas
---

# Pre-cancer source fitness in cBioPortal and GENIE

## Summary

This cBioPortal topic now describes what the cBioPortal/GENIE data source can and
cannot support for pre-cancer questions. Consumer-facing synthesis about prevalence,
indolence, progression, biological cost, and prevention strategy belongs in
`conditions/pre-cancer` after that child is registered.

## What cBioPortal Can Support

- Molecular characterization of precursor or pre-malignant samples when study
  metadata identifies the precursor state.
- Comparisons between precursor-labeled and invasive-labeled samples when cancer type,
  assay, and study context are explicit.
- Source caveats for mutation-ordering hypotheses that use cBioPortal or GENIE
  cross-sectional data.
- Links from cBioPortal hypotheses and questions to the condition child after
  registration.

## What cBioPortal Does Not Support Alone

- Population prevalence of pre-cancer conditions.
- Clinical progression rates without external cohort or registry data.
- Biological-cost claims for precursor clones outside molecular source evidence.
- Intervention or surveillance strategy.
- Denominator claims that require screening, autopsy, registry, or prospective cohort
  designs.

## Split Record

The previous version of this topic mixed source-fitness material with consumer-facing
pre-cancer synthesis. Phase 5 split the ownership:

- cBioPortal retained this source-fitness note.
- `conditions/pre-cancer` owns the day-1 synthesis and questions about indolence,
  progression, prevalence, biological cost, and n-minus-1 frame evaluation.
- The previous `source_refs` to `paper:Martincorena2018` and `paper:LeeSix2018`
  traveled to the pre-cancer evidence manifest as cross-project `evidence_refs`.

## Graph-ID Rewrite Record

- `hypothesis:0006-pre-malignant-n-minus-1-driver-carriage` remains related because it
  is a cBioPortal hypothesis about pre-malignant driver carriage.
- `hypothesis:0004-mhn-pathway-ordering` remains related because it is a cBioPortal
  hypothesis about mutation ordering from cross-sectional source data.
- `question:0012-mutation-ordering-cross-sectional-inference` remains related because
  it asks what cBioPortal-like cross-sectional data can infer.
- `topic:normal-tissue-mutation-atlas` remains related as source context.
- `topic:co-occurrence-and-mutual-exclusivity` was dropped because this source-facing
  note does not discuss co-occurrence or mutual exclusivity directly.
- Task ids `task:t156` and `task:t157` were not retained as graph relations in this
  source-facing topic.

## Consumer Link

After `conditions/pre-cancer` is registered, the consumer-facing follow-up is:

- `pre-cancer:report:2026-05-02-day-1-pre-cancer-synthesis`
