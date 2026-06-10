---
type: paper
title: A weighted exact test for mutually exclusive mutations in cancer
status: active
created: '2026-04-21'
updated: '2026-04-21'
id: paper:Leiserson2016
ontology_terms: []
source_refs:
- paper:Leiserson2016
related:
- paper:Leiserson2015
- paper:Kim2017
- topic:co-occurrence-and-mutual-exclusivity
---

# A weighted exact test for mutually exclusive mutations in cancer

- **Authors:** Leiserson MDM, Reyna MA, Raphael BJ
- **Year:** 2016
- **Journal:** Bioinformatics 32(17):i736-i745
- **DOI:** 10.1093/bioinformatics/btw462
- **PMID:** 27587696
- **BibTeX key:** Leiserson2016
- **Source:** `papers/references.bib`

## Key Contribution

Introduces WExT, a weighted exact mutual-exclusivity test that combines exact-testing logic with
sample-specific weighting.

## Methods

- Exact test over alteration patterns with per-sample weighting.
- Designed to preserve exact-testing behavior while adjusting for sample-level mutation burden.
- Positioned as a bridge between CoMEt-style exact methods and weighted-null frameworks.

## Key Findings

- Sample-specific weighting can reduce artifacts that appear when mutation burden varies strongly
  across tumors.
- Weighted exact testing provides a more realistic null for pan-cancer exclusivity analysis than
  unweighted exact counts alone.

## Relevance

This bridges the conceptual gap between CoMEt-style exact tests and WeSME-style weighted nulls,
which is why several mutual-exclusivity notes in this repo reference it.
