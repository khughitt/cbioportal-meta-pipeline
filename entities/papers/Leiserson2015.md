---
type: paper
title: 'CoMEt: a statistical approach to identify combinations of mutually exclusive
  alterations in cancer'
status: active
created: '2026-04-13'
updated: '2026-06-28'
id: paper:Leiserson2015
tags:
- mutual-exclusivity
- set-level-testing
- combinatorial
- exact-test
ontology_terms:
- MeSH:D015972
source_refs:
- paper:Leiserson2015
related:
- paper:Vandin2012
- paper:Leiserson2013
- paper:Leiserson2016
- paper:Ciriello2012
dataset_usage:
- ref: dataset:tcga
  role: analyzed
  overlap: full
---

# CoMEt: a statistical approach to identify combinations of mutually exclusive alterations in cancer

- **Authors:** Mark D.M. Leiserson, Hsin-Ta Wu, Fabio Vandin, Benjamin J. Raphael
- **Year:** 2015
- **Journal:** Genome Biology 16:160
- **DOI/URL:** https://doi.org/10.1186/s13059-015-0700-7
- **PMID:** 26253137
- **OpenAlex ID:** W1911343030
- **BibTeX key:** Leiserson2015
- **Source:** OpenAlex + PubMed (verified 2026-04-13)
- **Method name:** **CoMEt** (Combinations of Mutually Exclusive alterations test)

## Key Contribution

This CoMEt mutual-exclusivity note links paper:Vandin2012, paper:Leiserson2013, paper:Leiserson2016, and paper:Ciriello2012.

Introduces **CoMEt**, an exact-tail-enumeration statistical test for **sets of mutually
exclusive alterations** (arbitrary size *k*, not just pairs). Provides principled Bonferroni-
/ FDR-corrected *p*-values via exact enumeration rather than permutation. Extends to
subtype-specific mutual-exclusivity testing. Benchmarks favorably against Dendrix,
Multi-Dendrix, MEMo, and muex on both simulated and real data.

## Methods

- **Exact test:** enumerates the tail of the hypergeometric-like distribution of coverage
  with exclusive support for set sizes *k* ≥ 2.
- **MCMC search** over gene sets with Metropolis-Hastings proposals.
- **Subtype extension:** conditional testing within pre-defined subtypes to avoid
  confounding by lineage.

## Key Findings

- Recovers known mutually-exclusive driver modules across 5 TCGA cancer types.
- Identifies novel putative driver sets with *k* > 2 that pair-only methods (MEMo, Dendrix)
  miss.
- Outperforms competitors in precision/recall on simulated data at multiple effect sizes.

## Relevance

The reference design for moving **beyond pairwise gene-gene matrices** (the current level of
`create_correlation_matrices.py`) into *module* / *set-level* mutual-exclusivity detection.
If the project ever wants to test e.g. "do any 3-gene subsets of the PI3K pathway show
exclusivity across studies?" CoMEt's exact-test machinery is the template.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Set-level exclusivity test | Extension of per-pair correlation matrices | Would require new Snakemake rule consuming gene × sample matrices per study. |
| Subtype-conditional test | cancer / cancer_detailed stratification | Maps directly to existing stratification columns. |
| MCMC gene-set search | Future "module" discovery rule | Heavier compute; defer until pairwise layer is stable. |

## Limitations

- Exact enumeration cost grows quickly with *k*; CoMEt limits practical *k* ≤ 5–6.
- Assumes the same gene set would be tested across all samples in a study — requires
  gene-coverage uniformity (same argument for the pipeline's gene-coverage filter).
- Does not handle cross-study meta-analysis directly.

## Model / Tool Availability

- **Python implementation:** https://github.com/raphael-group/CoMEt
- License: check current repo (historically MIT-style).

## Follow-up

- Review Leiserson 2016 [@Leiserson2016] (WExT) for the weighted variant that bridges CoMEt and WeSME.
- Defer CoMEt adoption until the pair-level DISCOVER/WeSME layer is in place.
