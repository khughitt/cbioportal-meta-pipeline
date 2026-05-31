---
id: "paper:Drummond2023"
type: "paper"
title: "Relating mutational signature exposures to clinical data in cancers via signeR 2.0"
status: "active"
ontology_terms:
  - mutational signatures
  - NMF
  - Bayesian inference
  - clinical covariates
  - survival analysis
  - microsatellite instability
datasets:
  - "TCGA-STAD (stomach adenocarcinoma, 439 samples)"
source_refs:
  - "cite:Drummond2023"
related:
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
  - "paper:Rosales2017"
created: "2026-05-31"
updated: "2026-05-31"
---

# Relating mutational signature exposures to clinical data in cancers via signeR 2.0

- **Authors:** Rodrigo D. Drummond, Alexandre Defelicibus, Mathilde Meyenberg, Renan Valieris, Emmanuel Dias-Neto, Rafael A. Rosales, Israel Tojal da Silva
- **Year:** 2023
- **Journal:** BMC Bioinformatics
- **DOI/URL:** https://doi.org/10.1186/s12859-023-05550-3
- **BibTeX key:** Drummond2023
- **Source:** PDF

## Key Contribution

signeR 2.0 extends the original Bayesian NMF framework for mutational-signature discovery (signeR 1.x) with a downstream covariate-analysis toolkit: after sampling the posterior distribution of signature exposure matrices, it applies the same statistical test to every posterior draw and summarises results across draws, giving uncertainty-aware associations between signature exposures and clinical/molecular features (categorical, continuous, or survival). A companion R-Shiny app, signeRFlow, makes the entire pipeline accessible without programming expertise by embedding TCGA clinical data and COSMIC SBS v3.2 signatures directly, enabling point-and-click de novo extraction or fitting followed by covariate analysis.

## Methods

**Framework.** signeR models mutation count matrices M ≈ P × E (signatures × exposures) via Gibbs sampling, yielding R posterior realizations E^(1), …, E^(R) of the exposure matrix. All downstream analyses are applied to each E^(r) and results are summarised (typically by taking medians of p-values or test statistics) across all R draws, propagating estimation uncertainty into every association test.

**Covariate analysis modes:**
- *Categorical features* (e.g., molecular subtype, MSI status): Wilcoxon–Mann–Whitney (two groups) or Kruskal–Wallis (K groups) tests per signature per draw; inverted log-transformed p-values form the Differential Exposure Score (DES). Classification algorithms (k-NN, LDA, logistic regression, lasso, naive Bayes, SVM, random forests, linear vector quantisation) can additionally predict sample labels from exposure profiles.
- *Continuous features* (e.g., gene expression): Pearson/Spearman correlation per draw, plus linear regression treating all exposures jointly as predictors.
- *Survival data*: log-rank test after stratifying samples by exposure level (cutoff optimised by maxstat); Cox proportional-hazards regression for continuous exposure.

**Clustering.** When no external labels are available, hierarchical and fuzzy C-means clustering are applied to each E^(r), with the final dendrogram or membership matrix averaged across draws.

**Computational improvements over v1:** parallel computation support; pre-computed hyperparameter initialisation (avoiding expensive estimation), cutting runtime substantially (benchmarks in Supplementary file 1).

**Data.** Demonstration uses TCGA-STAD (stomach adenocarcinoma, 439 samples), fitting 19 COSMIC SBS signatures selected by literature review. Results compared to known molecular subtypes (EBV+, MSI, GS, CIN) from the TCGA STAD comprehensive characterisation study.

**Software.** Bioconductor R package (≥ R 4.3); GPL v3 licence. signeRFlow built with R Shiny. Available at https://doi.org/10.18129/B9.bioc.signeR.

## Key Findings

1. **Fuzzy clustering on exposures recovers molecular subtypes.** Six fuzzy clusters emerged from the STAD cohort; clusters 1, 4, and 5 were predominantly MSI-High samples, consistent with prior TCGA classification.

2. **DES recovers biology-consistent signature–subtype links.** Thirteen of the 19 fitted COSMIC signatures showed significantly different exposures across molecular subtypes (Kruskal–Wallis, FDR-controlled). Signatures elevated in MSI samples include SBS1 (clock-like / age), SBS15, SBS20, SBS21, SBS26, and SBS44 — all associated with defective DNA mismatch repair or microsatellite instability per COSMIC. This is a clean positive-control demonstration: known MMR-deficiency signatures are recovered agnostically from exposure data alone.

3. **Exposure profiles classify MSI-H with AUC = 0.983.** Using 8-fold cross-validation with a classifier ensemble, signeR 2.0 assigned MSI-H vs other labels with AUC = 0.983 on the 439-sample STAD set. A small fraction of samples (< 0.69%) was left *undefined* because their classification was inconsistent across posterior draws — the uncertainty-propagation mechanism actively prevents overconfident labelling.

4. **Survival associations.** SBS1, SBS5, SBS15, SBS21, and SBS26 showed significant associations with overall survival in STAD (log-rank, p < 0.05). Kaplan–Meier curves for SBS26 illustrate the stratification (p = 0.007). SBS1 and SBS5 are clock-like; the latter three are MMR-related — the survival link mirrors and extends prior prognostic literature on MSI status.

## Relevance

This paper is directly relevant to **hypothesis h08 (agnostic covariate↔signature-exposure association)** as a methodological reference implementation of exactly the analysis h08 proposes:

- **H08a positive control (recovery):** The STAD demonstration is a worked example of agnostic DES recovering textbook MMR/MSI-signature links (SBS15/20/21/26/44) without curating which signatures to examine. The same logic applies to UV→SBS7 (skin) and smoking→SBS4 (lung) in other tissue strata — signeR 2.0 provides the test statistics for those arms.
- **H08b discovery:** The continuous-feature correlation mode (expression → exposure) and survival analyses are the machinery needed for the expression-module↔signature associations h08 predicts will reveal novel upstream causes.
- **Uncertainty propagation:** The core algorithmic novelty — running every test on each posterior draw E^(r) and summarising across R — directly addresses the concern (noted in h08) that NMF solutions are non-unique and that single-point exposure estimates understate uncertainty. This is a principled answer to the multiple-solutions problem that bootstrap resampling only partially solves.
- **Classifier as optional label for cross-study transfer:** The ExposureClassify function could label new samples from an external study using a model trained on a reference cohort — relevant to the cross-study aggregation pipeline if per-sample signature profiles are ever compared across cBioPortal studies.
- **Positive-control design alignment:** The MSI/MMR recovery here (agnostically, from exposures alone, AUC 0.983) is the template for the h08 pre-registration design: a 2-of-3 gate requiring UV, smoking, and APOBEC arms to recover their known covariates. signeR 2.0 is one of the candidate tools for running those association arms.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Signature exposure matrix E | Per-sample signature weights H (NMF H matrix) | Same object; signeR uses Bayesian posterior, SigProfiler uses maximum-likelihood |
| Differential Exposure Score (DES) | Covariate↔signature association | DES is the per-draw inverted log p-value for group-difference tests |
| signeRFlow TCGA Explorer | cBioPortal study ingestion | signeRFlow works on TCGA; project pipeline uses cBioPortal + MC3 |
| k-fold ExposureClassify | Cross-study label transfer | Could label cBioPortal samples if trained on TCGA reference |
| Posterior realizations E^(r) | Replicate NMF runs / bootstrap | signeR's Bayesian draws are more principled than bootstrap for uncertainty |

## Limitations

- **R-only, Bioconductor ecosystem.** The project pipeline uses Python/Snakemake; integrating signeR requires an R subprocess or conda-env. The NMF backend is not interchangeable with SigProfilerExtractor or sklearn NMF without re-fitting.
- **Single-tissue demonstration.** The paper only validates on TCGA-STAD. Cross-tissue and cross-study behaviour (as in the cBioPortal pipeline) are not evaluated; confounding by tissue-of-origin is not addressed.
- **Sample size ceiling.** The Gibbs sampler scales polynomially; the authors note the paper covers a 439-sample cohort. Large pan-cancer cohorts (MC3: ~9,000 WES samples) may be prohibitively slow without further parallelisation.
- **No FDR correction reported explicitly for the STAD DES results.** The significance threshold of 0.05 is applied per-signature without explicit correction for testing all 19 signatures simultaneously, so the 13/19 figure may be conservative.
- **Survival cutoff optimisation (maxstat) inflates p-values.** Searching over all cutoff values introduces a look-elsewhere effect; results should be treated as hypothesis-generating, not confirmatory.
- **Undefined samples in classification.** While the ability to leave ambiguous samples unlabelled is presented as a feature, the paper does not discuss what drives a sample to be unlabelled or how to handle them downstream.

## Model / Tool Availability

- **Package:** Bioconductor `signeR` (https://doi.org/10.18129/B9.bioc.signeR), version 2.0+
- **Language:** R (≥ 4.3)
- **UI:** signeRFlow (Shiny app, bundled with package)
- **License:** GNU General Public License v3.0
- **Embedded data:** TCGA clinical data + COSMIC SBS v3.2 signatures (pre-loaded in signeRFlow)
- **Hardware:** No GPU required; parallel CPU computation supported
- **Restrictions:** Non-academic use requires a commercial licence

## Follow-up

- Compare DES (Kruskal–Wallis on posterior draws) to standard association tests (logistic regression, mixed model) on the same data to understand power/FDR properties in the cBioPortal context.
- The paper cites the original signeR (Rosales 2017, `paper:Rosales2017`) — worth reading for the full Bayesian derivation underlying the Gibbs sampler.
- Check whether the signeR Bioconductor package accepts pre-computed exposure matrices from SigProfilerExtractor as input (allowing the association layer to be reused without re-running extraction).
- The MSI-H classification result (AUC 0.983) with SBS26 as a key driver is directly relevant to the MMR arm of the h08 pre-registration positive control — consider replicating on MC3 STAD samples as a pilot.
