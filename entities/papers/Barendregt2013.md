---
type: paper
title: Meta-analysis of prevalence
status: active
created: '2026-04-21'
updated: '2026-06-28'
id: paper:Barendregt2013
ontology_terms: []
source_refs:
- paper:Barendregt2013
related:
- paper:Nyaga2014
- paper:LinXu2020
- topic:cross-study-meta-analysis-cancer-genomics
---

# Meta-analysis of prevalence

- **Authors:** Barendregt JJ, Doi SA, Lee YY, Norman RE, Vos T
- **Year:** 2013
- **Journal:** Journal of Epidemiology and Community Health 67(11):974-978
- **DOI:** 10.1136/jech-2013-203104
- **PMID:** 23963506
- **BibTeX key:** Barendregt2013
- **Source:** `papers/references.bib`

## Key Contribution

This prevalence-meta-analysis note links paper:Nyaga2014 and topic:cross-study-meta-analysis-cancer-genomics.

Popularizes the Freeman-Tukey double-arcsine workflow for meta-analysis of single proportions.

## Methods

- Focuses on meta-analysis of prevalence and other single-proportion outcomes.
- Emphasizes variance-stabilizing transformation before pooling.
- Presents back-transformation to the original prevalence scale after pooling.

## Key Findings

- Freeman-Tukey became a widely used operational recipe for prevalence synthesis.
- The paper is best treated here as historical context because later work in this repo argues
  that logit/GLMM approaches behave better near extreme proportions.

## Relevance

This is a context citation, not the project's preferred default. It matters because later reads
in this repo, especially `paper:LinXu2020`, explicitly argue against making arcsine transforms
the default for mutation-frequency pooling.
