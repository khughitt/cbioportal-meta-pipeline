---
id: "paper:Leiserson2013"
type: "paper"
title: "Simultaneous Identification of Multiple Driver Pathways in Cancer"
status: "active"
ontology_terms: []
datasets: []
source_refs:
  - "paper:Leiserson2013"
related:
  - "paper:Vandin2012"
  - "paper:Leiserson2015"
  - "topic:co-occurrence-and-mutual-exclusivity"
created: "2026-04-21"
updated: "2026-04-21"
---

# Simultaneous Identification of Multiple Driver Pathways in Cancer

- **Authors:** Leiserson MDM, Blokh D, Sharan R, Raphael BJ
- **Year:** 2013
- **Journal:** PLoS Computational Biology 9(5):e1003054
- **DOI:** 10.1371/journal.pcbi.1003054
- **BibTeX key:** Leiserson2013
- **Source:** `papers/references.bib`

## Key Contribution

Introduces Multi-Dendrix, extending coverage-exclusivity pathway discovery from one pathway at a
time to multiple pathways jointly.

## Methods

- Coverage-exclusivity objective over altered-gene sets.
- Joint optimization to recover multiple driver pathways instead of a single best set.
- Network/pathway discovery setting rather than pairwise exclusivity alone.

## Key Findings

- Multiple mutually exclusive pathways can be identified simultaneously without collapsing them
  into one mixed signal.
- This matters when distinct cancer programs would otherwise be conflated in pan-cancer data.

## Relevance

This is a direct background reference for the mutual-exclusivity cluster in the project, where
the transition from pairwise tests to pathway/module discovery matters.
