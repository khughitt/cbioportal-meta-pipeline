---
type: paper
title: 'Identifying Epistasis in Cancer Genomes: A Delicate Affair'
status: active
created: '2026-04-13'
updated: '2026-04-13'
id: paper:VanDeHaar2019
tags:
- perspective
- methodology-critique
- epistasis
- confounding
- mutual-exclusivity
ontology_terms:
- MeSH:D015972
source_refs:
- paper:VanDeHaar2019
related:
- paper:Canisius2016
- paper:Mina2020
- paper:Ciriello2012
- paper:Leiserson2015
---

# Identifying Epistasis in Cancer Genomes: A Delicate Affair

- **Authors:** Joris van de Haar, Sander Canisius, Michael B. Yaffe, Lodewyk F.A. Wessels,
  Lewis C. Cantley, Emile E. Voest, Trey Ideker
- **Year:** 2019
- **Journal:** Cell 177(6):1375-1383 (Perspective)
- **DOI/URL:** https://doi.org/10.1016/j.cell.2019.05.005
- **PMID:** 31150618
- **OpenAlex ID:** W2947209894
- **BibTeX key:** VanDeHaar2019
- **Source:** OpenAlex + PubMed (verified 2026-04-13)

## Key Contribution

A **Perspective / methodology-critique** paper enumerating the specific statistical pitfalls
that plague mutual-exclusivity and co-occurrence testing in pan-cancer datasets. Argues
that a large fraction of published "epistasis" / "co-occurrence" claims in cancer genomics
are artifacts of cohort composition, tumor-mutation-burden heterogeneity, lineage
confounding, and selection bias — and provides a checklist of controls any new method
should implement. Essential reading before making any cross-study co-occurrence claim.

## Methods

- Literature review + formal statistical analysis of common confounders.
- Reanalyzes several published co-occurrence claims under corrected null models (DISCOVER-
  style burden-aware nulls).
- Proposes a minimum-evidence checklist:
  1. Control for per-sample mutation burden.
  2. Stratify / condition on tissue of origin (lineage).
  3. Account for cohort composition effects (hypermutator subgroups, viral-positive
     subgroups).
  4. Prefer interaction tests with explicit biological / functional priors.

## Key Findings

- Most previously published co-occurrence results do not survive burden + lineage
  correction.
- A substantial fraction of mutual-exclusivity calls are also confounded by shared lineage
  restriction (both genes are rarely altered *together* simply because each is rare in
  certain lineages).
- Cross-cohort reproducibility is rarely assessed.

## Relevance

**The required cautionary read** before the cbioportal project implements any cross-study
co-occurrence statistic. Every item on the van de Haar checklist directly applies to the
pipeline:

- Per-sample burden → the pipeline already computes sample totals; use them as covariates.
- Lineage stratification → already implicit via `cancer` / `cancer_detailed`; make explicit.
- Cohort-composition effects → the pipeline runs across **many independent studies**;
  cross-study reproducibility assessment is a natural output.
- Functional priors → Sanchez-Vega 2018 pathways already processed.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Burden confounding | Per-sample TMB normalization | Add as explicit covariate before testing. |
| Lineage confounding | `cancer` stratum | Stratify or condition. |
| Cross-cohort reproducibility | Cross-study aggregation (core project goal) | The cbioportal project is **uniquely positioned** to do this right since it already aggregates across studies. |

## Limitations

- Perspective paper — no new algorithm.
- Empirical reanalysis is limited to a handful of case studies; not a systematic benchmark.

## Model / Tool Availability

- No code artifact.

## Follow-up

- Implement the van de Haar checklist as explicit validation gates in any new
  `create_cooccurrence_matrices.py` rule.
- Pre-register the choice of null model and covariates via `/science:pre-register` before
  running the analysis.
