---
id: "spec:research-question"
type: "spec"
title: "Structure of somatic mutations within and across cancer types"
status: active
created: "2025-02-21"
updated: "2026-04-12"
---

## Research Question

What is the structure of somatic mutations within and across cancer types, and which gene-cancer
associations recur across independent cBioPortal studies? Specifically, which genes are
consistently mutated at elevated rates in particular cancer types, how do mutation ratios compare
once normalized for study-level differences, and which clusters of genes and cancer types emerge
when mutation patterns are aggregated across many public studies?

## Scope

### In Scope

- Somatic mutation data from cBioPortal studies (public, downloaded programmatically)
- AACR GENIE mutation data (manual download via synapse.org)
- Per-study processing: convert `data_mutations.txt` to feather, filter by gene coverage,
  build gene x cancer and gene x patient matrices, compute correlation matrices
- Cross-study aggregation into gene x cancer / gene x cancer_detailed / gene x dataset tables
  (raw counts and sample-level ratios)
- Protein-length normalization via UniProt reference
- Clustering of genes and cancer types based on mutation patterns
- Gene coverage checks across studies

### Out of Scope (Current Phase)

- Non-mutation modalities (copy-number, expression, methylation) from cBioPortal
- Background / germline mutation modeling in healthy individuals
- Population-representativeness adjustments across cohorts
- Patient-level outcome or survival modeling
- Causal / perturbation analysis

## Hypotheses

1. Aggregating somatic mutation evidence across heterogeneous cBioPortal studies reveals
   gene-cancer associations that are more robust and more generalizable than any single study,
   and exposes clusters of cancer types with shared mutational structure.

## Assumptions

- Gene-level somatic mutation calls from cBioPortal studies, despite differing sequencing panels
  and cohort definitions, are comparable after per-study gene-coverage filtering and
  sample-normalized ratio computation.
- Protein length is an adequate first-order correction when comparing gene-level mutation counts.
- Study-level biases (panel content, cohort selection) can be partially mitigated by reporting
  both raw counts and sample-level ratios and by aggregating across many independent studies.
