---
id: "paper:DeVito2025"
type: "paper"
title: "Analysis of mutational signatures in multiple cancer studies: Recent Bayesian tools"
status: active
ontology_terms:
  - mutational signatures
  - nonnegative matrix factorization
  - Bayesian statistics
  - multi-study analysis
  - somatic mutations
datasets: []
source_refs:
  - "cite:DeVito2025"
related:
  - hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and
  - question:q018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross
  - question:q019-does-de-novo-extraction-on-the-aggregated-cohort-surface-factors-not-in
created: "2026-05-31"
updated: "2026-05-31"
---

# Analysis of mutational signatures in multiple cancer studies: Recent Bayesian tools

- **Authors:** Roberta De Vito, Blake Hansen, Isabella N. Grabski, Lorenzo Trippa, Giovanni Parmigiani
- **Year:** 2025
- **Journal:** Journal of Cancer Biology
- **Volume/Issue/Pages:** 6(2):108–114
- **DOI/URL:** [UNVERIFIED] (no DOI given in PDF; published by ProBiologists, open-access)
- **BibTeX key:** DeVito2025
- **Source:** PDF

## Key Contribution

This mini-review presents and contextualises two recent Bayesian NMF frameworks for multi-study mutational signature analysis: (1) **Multi-Study NMF** (Grabski et al. 2025, Genome Biology), which decomposes mutation count matrices across S studies with a shared signature matrix and study-specific binary inclusion indicators, plus a semi-supervised recovery–discovery mode that simultaneously refits COSMIC-catalogue signatures and discovers novel ones; and (2) **Bayesian Probit Multi-Study NMF (BaP Multi-NMF)** (Hansen et al. 2025, arXiv:2502.01468), which encodes exposure sparsity via a probit mixture prior and incorporates sample-level covariates directly into the exposure model. Together, the two models address the growing need for integrative, multi-cohort signature analyses that go beyond single-dataset NMF or ad hoc meta-analyses.

## Methods

**Data model.** Both methods build on the standard 96-motif SBS representation (I=96; six substitution classes × flanking nucleotides). For S studies each contributing a count matrix M_s (I × J_s), the joint generative model is:

```
M_s ~ Poisson(P A_s E_s)
```

where P (I×K) is the shared signature matrix, A_s is a study-specific diagonal binary indicator matrix selecting which of the K signatures are active in study s, and E_s (K×J_s) is the study-specific exposure matrix.

**Grabski 2025 (Multi-Study NMF):**
- Gamma priors with hierarchical hyperpriors on signature and exposure entries; Bernoulli(q) prior on each A_{sk} entry, inducing sparsity in cross-study signature sharing.
- Semi-supervised recovery–discovery extension: the Poisson mean is split into P^R A_s^R E_s^R (known COSMIC signatures, with strong but not rigid priors) plus P^D A_s^D E_s^D (novel signatures inferred de novo).
- Applied to breast-cancer samples from TCGA and PCAWG across age groups 20–29, 30–39, 40–49.

**Hansen 2025 (BaP Multi-NMF):**
- Columns of P and E_s normalised to sum-to-one; Dirichlet priors on signatures (p_k ~ Dirichlet(α^p)) and on exposures conditioned on a latent binary activity indicator a_{sjk}.
- The binary indicator is modelled via probit regression on sample-level covariates x_{sj}: a*_{sjk} ~ N(β_{sk}^T x_{sj}, 1), with hierarchical normal priors on β_{sk} and Gamma priors on precision τ_{sk}.
- This yields a bi-clustering of patients and signatures; covariate effects on signature activity are estimated jointly with the NMF.
- Applied to tumor DNA from 7 cancer types to recover signature clusters and patient clusters.

**Inference:** Both models rely on MCMC or variational Bayes (implementation details deferred to the primary papers); posterior uncertainty on signatures and exposures is explicitly quantified. Software is available in the GitHub repositories cited in each primary paper.

## Key Findings

1. **Multi-study borrowing improves signal recovery.** Integrating multiple small cohorts allows the model to detect signatures that would be undetectable in any single study, demonstrated by recovering meaningful signals from a TCGA 20–29-year-old breast cancer group with only 7 tumors.

2. **Early-onset breast cancer (20–29) shows a distinct signature profile.** The youngest age group lacked SBS3 (homologous recombination deficiency) and other canonical breast cancer signatures but instead carried SBS4 (tobacco smoking) and other environmental-exposure signatures — suggesting lifestyle/environmental mutagenesis predominates over germline HR-pathway deficiency in this rare group. (Caution warranted given tiny sample size.)

3. **BaP Multi-NMF recovers biologically coherent signature clusters across 7 cancer types.** Across breast, head, colorectal, stomach, esophagus, lung adenocarcinoma, and lung squamous cell carcinoma:
   - Tobacco-related signatures (SBS4, SBS2, SBS92, SBS22a, SBS45) form a cohesive cluster active in lung cancers.
   - SBS93 (unknown etiology) co-clusters with SBS3 (HRD) and other DNA-repair signatures.
   - Cancer types form three main patient clusters (breast+head; stomach+colorectal+esophagus; lung adenoCA+SCC), with notable inter-cancer border cases (some breast cancers resembling head cancers; some stomach cancers resembling esophageal).

4. **Three novel signatures (D1, D2, D3) were discovered** by the recovery–discovery framework in the 7-cancer-type analysis, in addition to the known COSMIC catalogue signatures.

5. **Covariate integration improves both signature estimation and biological interpretation.** Incorporating sex, smoking status, or inherited susceptibility as covariates into the probit model improves exposure estimates relative to treating covariates as post-hoc annotations.

## Relevance

This review is directly relevant to **hypothesis h08** (agnostic covariate–signature-exposure association; positive-control recovery of UV/smoking/APOBEC/MMR).

- **H08a (positive-control recovery):** BaP Multi-NMF's built-in probit covariate model is the closest published analog to the association design in H08a. It demonstrates that smoking status and sex can be linked to signature activity within a joint Bayesian NMF — i.e. the recovery of known aetiology links (smoking→SBS4) is achievable without post-hoc correlation. This supports the feasibility of the H08a design and provides a benchmark architecture.

- **H08b (discovery):** The recovery–discovery split (P^R for known, P^D for novel) is directly applicable to our multi-study aggregation: we can anchor COSMIC catalogue signatures and simultaneously discover study- or cancer-type-specific novel processes. The cross-study sharing structure (study-specific A_s matrices) maps onto our scenario of ~300 heterogeneous cBioPortal studies.

- **Multi-study integration design:** The paper distinguishes multi-study analysis (shared variable labels across matrices) from multimodal integration (shared subject labels across matrices). Our pipeline occupies the multi-study regime for mutation count data, and the multimodal regime when expression and mutation are co-measured on the same samples — a distinction the framework makes explicit and useful.

- **Software gap:** The review notes R implementations in separate GitHub repositories (Grabski 2025, Hansen 2025). For integration into the Python/Snakemake pipeline, a wrapper or port would be needed. SigProfilerExtractor (Python) and bayesNMF (Python, arXiv:2502.18674) are listed as alternatives in Table 1 for those preferring Python-native tools.

- **Cross-study aggregation connection:** The project's `gene_cancer_study_ratio_annotated.feather` aggregates across cBioPortal studies in a meta-analytic manner. If per-sample mutation spectra were retained (rather than aggregated mutation ratios), the Grabski/Hansen models could be applied directly — this maps to the feasibility question raised in q018.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Study-specific count matrix M_s | Per-study mutation table (studies/{id}/mut/) | Each study is a cBioPortal cohort; counts would be 96-motif SBS |
| Shared signature matrix P | COSMIC SBS catalogue / de-novo factors W | The pipeline currently uses SigProfilerAssignment for refitting |
| Study-specific binary indicator A_s | Study-level signature-activity flags | Not currently tracked in feather outputs |
| Exposure matrix E_s | Per-sample signature attribution (H) | Not in current pipeline outputs; feasibility question = q018 |
| Sample-level covariates x_{sj} | Clinical fields in samples_annotated.feather | age, sex, MSI, TMB, oncotree_code etc. already ingested |
| Recovery component P^R | Restricted COSMIC catalogue assignment | run_restricted_sigprofiler_assignment.py |
| Discovery component P^D | De-novo NMF factors (q019 scope) | Currently unimplemented; q019 asks about feasibility |

## Limitations

- **Mini-review scope:** The paper does not introduce new methodology but summarises two primary papers (Grabski 2025, Hansen 2025). Quantitative performance comparisons (sensitivity, specificity, computational cost) are not presented; readers must consult the primary papers.
- **W_s limitation in BaP Multi-NMF:** The per-sample scaling matrix W_s = diag(w_{s1}, ..., w_{sJ_s}) is fixed at observed total mutation counts, which may be informative of signature activity in hypermutator tumors (extreme genomic instability) — a limitation the authors acknowledge.
- **R implementations only:** Both primary tools are implemented in R; integration into Python-based pipelines requires additional work.
- **Small early-onset breast cancer cohorts:** The TCGA 20–29 group (n=7) result is intriguing but statistically fragile; the authors appropriately note caution.
- **No direct comparison to single-study Bayesian NMF baselines** in terms of precision/recall curves; the claim of improved learning efficiency relative to single-dataset analysis is supported by logic and application examples but not by a formal simulation benchmark in this review.

## Model / Tool Availability

- **Grabski 2025 (Multi-Study NMF):** R code; GitHub repository referenced in Genome Biology paper (Genome Biol. 2025 Apr 16;26(1):98). [UNVERIFIED exact repo URL]
- **Hansen 2025 (BaP Multi-NMF):** R code; GitHub repository referenced in arXiv:2502.01468. [UNVERIFIED exact repo URL]
- Table 1 in the review provides a comprehensive taxonomy of 30+ signature analysis tools organised by topic (Dirichlet mixture specs, regularization, ensembling, multi-study, covariates, etc.)

## Follow-up

- Read the two primary papers in full: Grabski IN et al., Genome Biol. 2025;26(1):98 (Multi-Study NMF) and Hansen B et al., arXiv:2502.01468 (BaP Multi-NMF).
- Assess whether BaP Multi-NMF's probit covariate model can serve as the within-study association layer for H08a, or whether a lighter post-hoc regression on SigProfilerAssignment outputs is preferable.
- Check Table 1's "Covariates and spatial variation" row: Robinson 2019, Grabski 2025, Hansen 2025, SigProfilerTopography — at least one of these may provide a direct Python-compatible implementation of covariate-aware signature analysis for H08.
- q018 feasibility: the paper implicitly confirms that per-sample WES/WGS spectra are the appropriate substrate (not aggregated ratios); panel data require refit, not de-novo extraction.
