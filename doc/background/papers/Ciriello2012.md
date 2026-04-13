---
id: "article:Ciriello2012"
type: "article"
title: "Mutual exclusivity analysis identifies oncogenic network modules"
status: "active"
tags:
  - mutual-exclusivity
  - network-module
  - oncogenic-module
  - seminal
ontology_terms:
  - "MeSH:D015972"
datasets:
  - "TCGA"
source_refs:
  - "cite:Ciriello2012"
related:
  - "article:Ciriello2013"
  - "article:Canisius2016"
  - "article:Leiserson2015"
  - "article:Babur2015"
created: "2026-04-13"
updated: "2026-04-13"
---

# Mutual exclusivity analysis identifies oncogenic network modules

- **Authors:** Giovanni Ciriello, Ethan Cerami, Chris Sander, Nikolaus Schultz
- **Year:** 2012 (OpenAlex records publication year 2011; Genome Research issue Feb 2012)
- **Journal:** Genome Research 22(2):398-406
- **DOI/URL:** https://doi.org/10.1101/gr.125567.111
- **PMID:** 21908773
- **OpenAlex ID:** W2144940507
- **BibTeX key:** Ciriello2012
- **Source:** OpenAlex + PubMed (verified 2026-04-13)
- **Method name:** **MEMo** (Mutual Exclusivity Modules in cancer)
- **Citations:** 743

## Key Contribution

The **seminal** method for systematic mutual-exclusivity-driven discovery of oncogenic
network modules in cancer genomics. Combines a mutual-exclusivity test with a
protein-protein / functional interaction network prior to identify gene modules whose
alterations (a) tend to be mutually exclusive within tumors and (b) participate in the
same functional neighborhood. Establishes the MEMo framework that essentially every later
method (Dendrix, CoMEt, MEGSA, TiMEx, WeSME, SELECT) either builds on or benchmarks against.

## Methods

- **Step 1:** build a functional-interaction network (HPRD, Reactome, etc.).
- **Step 2:** identify candidate gene groups that form connected subnetworks.
- **Step 3:** test each subnetwork for mutual exclusivity via a permutation null.
- **Step 4:** report significant modules with supporting network evidence.

## Key Findings

- Recovers canonical oncogenic modules (p53/MDM2/MDM4; RB/CDK4/CDKN2A; RTK/RAS/PI3K) across
  TCGA glioblastoma, breast, ovarian, and other cohorts.
- Demonstrates that network constraints substantially improve precision over unconstrained
  mutual-exclusivity testing.

## Relevance

- The foundational reference whenever the project claims to "detect co-mutation / exclusivity
  modules across studies". Any method choice (DISCOVER, WeSME, SELECT) should cite MEMo as
  the conceptual origin.
- The **network-prior** design pattern (use pathway / PPI edges as a filter on the search
  space) is a natural extension for the cbioportal pipeline, because `process_sanchez_vega_pathways.py`
  already produces pathway-gene mappings.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Functional-interaction network prior | Sanchez-Vega 2018 pathway mappings | Already in pipeline as `process_sanchez_vega_pathways.py`. |
| Subnetwork-level ME test | Module-level extension of the pair-level layer | Future work. |
| Permutation null | Replaced / supplemented by DISCOVER / WeSME | Method has since been superseded in precision but not in framing. |

## Limitations

- Permutation null does not account for per-sample burden heterogeneity (corrected by
  DISCOVER in 2016).
- Depends heavily on the quality of the functional-interaction network used.
- No per-cancer-type subtype conditioning.

## Model / Tool Availability

- Historical MEMo implementation (Java) hosted by cBioPortal; see supplement of the paper.
- Subsequent protocol paper (Ciriello et al. 2013, PMID 23504936) gives a step-by-step
  guide.

## Follow-up

- Read Babur 2015 (Mutex) for the next-generation network-aware variant.
- Read Leiserson 2015 (CoMEt) for the set-level extension.
- Use MEMo primarily as the *conceptual citation* in any project write-up, and DISCOVER /
  SELECT as the operational methods.
