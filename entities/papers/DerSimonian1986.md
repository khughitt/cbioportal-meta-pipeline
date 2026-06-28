---
type: paper
title: Meta-analysis in clinical trials
status: active
created: '2026-04-21'
updated: '2026-06-28'
id: paper:DerSimonian1986
ontology_terms: []
source_refs:
- paper:DerSimonian1986
related:
- paper:Viechtbauer2010
- paper:Langan2018
- topic:cross-study-meta-analysis-cancer-genomics
---

# Meta-analysis in clinical trials

- **Authors:** DerSimonian R, Laird N
- **Year:** 1986
- **Journal:** Controlled Clinical Trials 7(3):177-188
- **DOI:** 10.1016/0197-2456(86)90046-2
- **BibTeX key:** DerSimonian1986
- **Source:** `papers/references.bib`

## Key Contribution

This foundational random-effects meta-analysis note links paper:Viechtbauer2010, paper:Langan2018, and topic:cross-study-meta-analysis-cancer-genomics.

Introduces the DerSimonian-Laird random-effects estimator, the canonical historical baseline for
between-study heterogeneity in meta-analysis.

## Methods

- Random-effects pooling from study-level effect estimates and within-study variances.
- Closed-form moment estimator for between-study variance (`tau^2`).
- Normal-approximation confidence interval around the pooled effect.

## Key Findings

- Makes heterogeneity an explicit model component rather than collapsing all studies into one
  pooled dataset.
- Provides a simple baseline that later methods (REML, PM, HKSJ workflows) compare against.

## Relevance

This is the obligate anchor citation whenever the project contrasts naive pooled mutation rates
with classical random-effects pooling for per-study gene-cancer proportions.
