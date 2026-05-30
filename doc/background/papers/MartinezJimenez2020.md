---
id: paper:MartinezJimenez2020
type: paper
title: A compendium of mutational cancer driver genes
status: active
ontology_terms: []
source_refs:
- paper:MartinezJimenez2020
related:
- paper:Bailey2018
- topic:cross-study-meta-analysis-cancer-genomics
- topic:cancer-driver-genes
created: '2026-04-21'
updated: '2026-04-21'
---

# A compendium of mutational cancer driver genes

- **Authors:** Martinez-Jimenez F, Muinos F, Sentis I, et al.
- **Year:** 2020
- **Journal:** Nature Reviews Cancer 20(10):555-572
- **DOI:** 10.1038/s41568-020-0290-x
- **PMID:** 32778778
- **BibTeX key:** MartinezJimenez2020
- **Source:** `papers/references.bib`

## Key Contribution

Synthesizes IntOGen-style driver-gene aggregation across many cohorts and methods, providing a
cancer-genomics-native reference point between naive pooling and fully explicit meta-analysis.

## Methods

- Review/compendium of driver-gene discovery across many cohorts and driver-calling methods.
- Uses multi-method consensus logic rather than a single statistical test.
- Organizes results by cancer type and pan-cancer recurrence.

## Key Findings

- Large-scale driver catalogs benefit from combining multiple methods and cohorts.
- Consensus-voting pipelines are a realistic baseline for cancer-genomics aggregation even when
  they do not expose explicit random-effects uncertainty.

## Relevance

This repo uses the paper as prior art for cross-study aggregation and pathway/driver consensus
workflows, especially where method ensembles are a more realistic baseline than single-study
significance calls.
