---
type: paper
title: Systematic identification of cancer driving signaling pathways based on mutual
  exclusivity of genomic alterations
status: active
created: '2026-04-21'
updated: '2026-06-28'
id: paper:Babur2015
ontology_terms: []
source_refs:
- paper:Babur2015
related:
- paper:Ciriello2012
- paper:Leiserson2015
- topic:co-occurrence-and-mutual-exclusivity
---

# Systematic identification of cancer driving signaling pathways based on mutual exclusivity of genomic alterations

- **Authors:** Babur O, Gonen M, Aksoy BA, Schultz N, Ciriello G, Sander C, Demir E
- **Year:** 2015
- **Journal:** Genome Biology 16:45
- **DOI:** 10.1186/s13059-015-0612-6
- **PMID:** 25887147
- **BibTeX key:** Babur2015
- **Source:** `papers/references.bib`

## Key Contribution

This pathway-mutual-exclusivity note links paper:Ciriello2012, paper:Leiserson2015, and topic:co-occurrence-and-mutual-exclusivity.

Introduces Mutex, a pathway-aware mutual-exclusivity method that uses curated signaling priors to
find alteration sets converging on common downstream targets.

## Methods

- Mutual-exclusivity testing constrained by curated signaling-network structure.
- Searches for alteration sets that converge on shared downstream pathway components.
- Prior-informed pathway/module discovery rather than unconstrained set enumeration.

## Key Findings

- Pathway priors can sharpen mutual-exclusivity detection by ruling out biologically implausible
  gene sets.
- The method is most relevant when the project wants mechanism-level pathway interpretation, not
  just pairwise exclusivity scores.

## Relevance

This is the network/pathway-prior branch of the mutual-exclusivity literature that complements
network-free set-based methods like CoMEt and Dendrix.
