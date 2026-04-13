---
id: "article:Vandin2012"
type: "article"
title: "De novo discovery of mutated driver pathways in cancer"
status: "active"
tags:
  - driver-pathway
  - mutual-exclusivity
  - coverage
  - combinatorial-optimization
ontology_terms:
  - "MeSH:D015972"
datasets:
  - "TCGA"
source_refs:
  - "cite:Vandin2012"
related:
  - "article:Ciriello2012"
  - "article:Leiserson2013"
  - "article:Leiserson2015"
created: "2026-04-13"
updated: "2026-04-13"
---

# De novo discovery of mutated driver pathways in cancer

- **Authors:** Fabio Vandin, Eli Upfal, Benjamin J. Raphael
- **Year:** 2012 (OpenAlex records 2011; Genome Research issue Feb 2012)
- **Journal:** Genome Research 22(2):375-385
- **DOI/URL:** https://doi.org/10.1101/gr.120477.111
- **PMID:** 21653252
- **OpenAlex ID:** W2121443461
- **BibTeX key:** Vandin2012
- **Source:** OpenAlex + PubMed (verified 2026-04-13)
- **Method name:** **Dendrix** (De novo Driver Exclusivity)

## Key Contribution

Introduces **Dendrix**, a combinatorial optimization framework for discovering driver
pathways **without any prior pathway database** — gene groups are scored purely on the
joint criterion of (a) high patient **coverage** (many samples have at least one alteration
in the group) and (b) **exclusivity** (most altered samples have only one alteration in
the group). The `W(M) = |coverage(M)| - |overlap(M)|` weight function and the Markov-chain
Monte Carlo search over gene sets define the original "coverage-exclusivity" design pattern
used by the entire Raphael-group lineage (Multi-Dendrix, CoMEt, WExT).

## Methods

- **Weight function:** W(M) = Γ(M) - ω(M), where Γ(M) = number of samples with ≥ 1 gene in M
  altered, and ω(M) = number of samples with > 1 gene in M altered.
- **MCMC search** over gene sets of fixed size *k*.
- **Significance:** permutation test on the weight statistic.

## Key Findings

- Recovers known RTK-signaling and TP53 modules in GBM and lung cancer without pathway
  priors.
- Demonstrates that combinatorial exclusivity alone is sufficient signal to recover
  biologically coherent modules — a foundational observation.

## Relevance

- Conceptual origin of every later "coverage × exclusivity" driver-module method.
- Useful reference whenever the project wants to justify designing a module-level score
  that does not depend on external pathway databases.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Coverage Γ(M) | Sum of sample-level mutation ratios over module | Directly computable from existing `_ratio` tables. |
| Exclusivity ω(M) | Joint-mutation overlap per module | Computable from gene × sample matrices. |
| W(M) weight | Candidate cross-study scoring statistic | Could be aggregated across studies with sample-size weights. |

## Limitations

- Fixed module size *k* (user-specified) — sensitive to choice.
- No per-sample burden correction (addressed later by DISCOVER).
- No statistical guarantees beyond permutation.

## Model / Tool Availability

- Original Python implementation: https://github.com/raphael-group/dendrix
- Later re-implementations in CoMEt / Multi-Dendrix supersede standalone use.

## Follow-up

- Read Leiserson 2013 (Multi-Dendrix) for the joint-multi-pathway extension.
- Read Leiserson 2015 (CoMEt) for the exact-test replacement of the permutation step.
