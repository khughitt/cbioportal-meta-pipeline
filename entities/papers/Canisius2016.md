---
type: paper
title: A novel independence test for somatic alterations in cancer shows that biology
  drives mutual exclusivity but chance explains most co-occurrence
status: active
created: '2026-04-13'
updated: '2026-04-13'
id: paper:Canisius2016
tags:
- mutual-exclusivity
- co-occurrence
- statistical-method
- null-model
- pan-cancer
ontology_terms:
- MeSH:D009154
- MeSH:D015972
source_refs:
- paper:Canisius2016
related:
- paper:Ciriello2012
- paper:Leiserson2015
- paper:Kim2017
- paper:Mina2020
- paper:VanDeHaar2019
dataset_usage:
- ref: dataset:tcga
  role: analyzed
  overlap: unknown
---

# A novel independence test for somatic alterations in cancer shows that biology drives mutual exclusivity but chance explains most co-occurrence

- **Authors:** Sander Canisius, John W.M. Martens, Lodewyk F.A. Wessels
- **Year:** 2016
- **Journal:** Genome Biology 17:261
- **DOI/URL:** https://doi.org/10.1186/s13059-016-1114-x
- **PMID:** 27986087
- **OpenAlex ID:** W2949363897
- **BibTeX key:** Canisius2016
- **Source:** OpenAlex + PubMed (verified 2026-04-13)
- **Method name:** **DISCOVER**
- **Software:** https://github.com/NKI-CCB/DISCOVER

## Key Contribution

Introduces **DISCOVER** (Discrete Independence Statistic Controlling for Observations with
Varying Event Rates), an independence test for somatic alterations that uses
**per-tumor (sample-specific) background mutation probabilities** instead of a single
cohort-level rate. This fixes a systematic bias in earlier methods (Fisher's exact,
permutation on the full matrix) that conflates mutual exclusivity with heterogeneity of
tumor mutation burden. The pan-cancer analysis finds substantial genuine exclusivity driven
by cell-cycle, growth-factor-signaling, and Hedgehog-pathway genes, but concludes that
**most previously reported co-occurrences are explained by chance** once TMB variation is
controlled for.

## Methods

- **Null model:** Poisson-binomial distribution of gene pair overlaps where each tumor has
  its own alteration probabilities (estimated from gene- and tumor-specific marginal rates
  via an iterative proportional fitting / matrix factorization step).
- **Test:** analytic one-sided tail test against the Poisson-binomial null (no permutation
  required at pair level).
- **Group test:** extension for testing whether a gene *set* shows more exclusivity than
  expected under the same null.
- **Application:** 12 TCGA cancer types; 3,386 tumors.
- **Comparison:** benchmarks vs. Fisher's exact, MEMo, MEGSA, muex, CoMEt.

## Key Findings

- Once per-tumor background rates are controlled for, **no evidence for widespread co-occurrence
  beyond chance** is observed in TCGA pan-cancer data.
- Genuine mutual exclusivity is concentrated in functionally coherent modules (p53/MDM2,
  RTK/RAS/MAPK, PI3K, cell-cycle).
- Many "cooccurring" pairs reported by prior methods are artifacts of TMB heterogeneity across
  hypermutator subgroups.

## Relevance

Directly motivates the design of any cross-study co-occurrence layer added to the cbioportal
pipeline. The Poisson-binomial null is a natural fit for the per-study gene-coverage-filtered
matrices the pipeline already produces, and the finding that naive co-occurrence tests are
dominated by burden-heterogeneity artifacts is a critical caveat for any gene-gene correlation
matrix aggregated across heterogeneous studies (different panels, different cohort compositions).

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Per-tumor alteration probability | Per-sample gene-coverage × per-gene study frequency | Pipeline already has both inputs in `gene_patient_mutation_count_matrix.py` outputs. |
| Marginal-preserving permutation reference | Analogue to what `create_correlation_matrices.py` would need | Current correlation script has no null model. |
| Cohort-level vs per-tumor rate | Study-level vs sample-level ratio (the "_ratio" tables) | Directly maps to the two-table convention documented in AGENTS.md. |

## Limitations

- Poisson-binomial null assumes independence of alteration events across genes within a
  tumor — not exactly true in hypermutator contexts.
- Requires a reasonably large per-cancer-type sample size; degrades for rare cancer types
  with small *n*.
- Does **not** address clonal-hematopoiesis contamination — CH genes (DNMT3A, TET2, ASXL1 ...)
  may still appear as spurious co-mutations with tumor-intrinsic genes if panel-based calls
  contain CH variants.

## Model / Tool Availability

- **R package:** `discover` (Bioconductor / NKI-CCB GitHub).
- **Python port:** `discover-ccb` / derivative reimplementations exist.
- **License:** BSD-style (R package).
- No heavy compute requirements.

## Follow-up

- Read Mina 2020 (SELECT) next for the covariate-aware extension.
- Read van de Haar 2019 for the caution story on naive epistasis detection.
- Decide between DISCOVER (closed-form) and WeSME (sampling-based) as the project's primary
  null model before implementing the cross-study co-occurrence rule.
