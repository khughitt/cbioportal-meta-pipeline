---
type: paper
title: Modeling clinical and molecular covariates of mutational process activity in
  cancer
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Robinson2019
ontology_terms:
- mutational signatures
- topic modeling
- Bayesian inference
- somatic mutation
- tumor covariates
- homologous recombination deficiency
datasets: []
source_refs:
- cite:Robinson2019
related: []
---

# Modeling clinical and molecular covariates of mutational process activity in cancer

- **Authors:** Welles Robinson, Roded Sharan, Mark D. M. Leiserson
- **Year:** 2019
- **Journal:** Bioinformatics, 35(14), i492–i500 (ISMB/ECCB 2019)
- **DOI/URL:** https://doi.org/10.1093/bioinformatics/btz340
- **BibTeX key:** Robinson2019
- **Source:** PDF

## Key Contribution

TCSM (Tumor Covariate Signature Model) is the first probabilistic method to directly model the effect of observed tumor-level clinical/demographic or molecular covariates on mutation signature exposures. Built on Bayesian topic modeling (specifically the Structural Topic Model with a logistic-normal prior), it modifies the prior over per-tumor signature exposure distributions conditioned on the tumor's covariates, and provides a permutation-based significance test for covariate-exposure associations. On both simulated and real data it outperforms NMF and covariate-free topic modeling, especially when disentangling exposures for spectrally similar signatures such as COSMIC SBS3 (HR deficiency) and SBS5 (aging/clock-like, cosine similarity 0.83).

## Methods

**Model.** TCSM follows the generative process of LDA / correlated topic models with a logistic-normal prior on per-tumor signature exposures θ_i, where the mean of the logistic normal is set to x_i · Γ (Γ = D × (K−1) exposure–covariate coefficient matrix). This allows covariates to shift the prior probability of exposure to each signature. Signatures β_k and covariance Σ are learned jointly. Normal(0, σ_k²) hyperpriors with Half-Cauchy(1,1) on σ_k enforce weak regularization on Γ.

**Inference.** Variational expectation-maximization (using the R `stm` package as a backend) with spectral (NMF) initialization of the mutation co-occurrence matrix.

**Model selection.** 5-fold cross-validation with the "document completion" held-out log-likelihood criterion; K chosen at the plateau.

**Covariate imputation.** For held-out or missing binary covariates, a log-likelihood ratio (LLR) comparing the model under x_id = 1 vs x_id = 0 is computed from the tumor's mutation spectrum; positive LLR → predict covariate positive.

**Significance testing.** Permutation test (10,000 samples) generating an empirical null of covariate-exposure mean differences; BH-corrected P-values reported.

**Benchmarks.** Compared against: NMF (SomaticSignatures R package) and TCSM without covariates. Metrics: cosine similarity of inferred signatures to ground truth, mean-squared error of exposures, held-out log-likelihood, AUPRC of HR-deficiency prediction via a linear SVC trained on exposures.

**Data.** Three real datasets: (1) 760 TCGA BRCA exomes with biallelic HR gene inactivation calls and large-scale state transition (LST) counts as covariates; (2) 418 TCGA SKCM and 485 TCGA LUSC exomes with cancer type, smoking history, and CC→TT dinucleotide counts (UV proxy) as covariates.

**Implementation.** Python 3; Snakemake workflow; code at https://github.com/lrgr/tcsm.

## Key Findings

1. **Simulation (breast cancer scenario, SBS3/SBS5 confusion).** With N=250 samples, TCSM with covariates identified the true K=4 in 35/50 simulated datasets vs 19/50 for NMF and 3/50 for TCSM without covariates. TCSM with covariates achieved lower exposure MSE across all sample sizes, particularly for the confounded SBS3/SBS5 pair.

2. **Breast cancer HR deficiency.** K=5 signatures were recovered, each matching a known COSMIC signature (SBS1-aging, SBS2/13-APOBEC, SBS3-HR deficiency, SBS6-MMR, SBS10-POLE). Significance test correctly identified SBS3 as the signature elevated in tumors with biallelic BRCA1/BRCA2/RAD51C inactivation (BH-corrected P<0.001). HR-deficiency prediction AUPRC on the held-out 25%: TCSM with covariates=0.64, TCSM without=0.59, NMF=0.58.

3. **Covariate selection insight.** A greedy mutual-information search (maximizing MI with LST count) identified the minimal HR gene subset {BRCA1, BRCA2, RAD51C} whose biallelic inactivations are nearly mutually exclusive (1/57 co-occurring), matching pathway biology and outperforming all-7-genes encoding on held-out likelihood.

4. **Melanoma + lung cancer.** K=4 signatures recovered: UV (SBS7), smoking (SBS4), APOBEC (SBS2/13), and an aging/MMR composite (SBS1+SBS6; cosine 0.84 between them). Cancer type as a single covariate dominated; adding smoking history and CC→TT counts yielded minimal additional held-out likelihood gain (they are collinear with cancer type in this cohort).

5. **Misclassification detection.** TCSM's LLR over the cancer-type covariate flagged exactly three LUSC tumors as having mutation spectra more consistent with SKCM (LLR>1); all three are the same cases independently identified by Campbell et al. (2016) via UV-signature exposure, and all three had ≥15 CC→TT mutations (uniquely high in the LUSC cohort). This demonstrates probabilistic cancer-type imputation from mutation spectrum alone.

6. **Key limitation: covariate collinearity.** When covariates are strongly confounded with cancer type (smoking and UV in the melanoma/lung cohort), additional covariates provide marginal improvement, underscoring the need for conditional (within-tissue) design.

## Relevance

This paper is directly relevant to **hypothesis h08** (agnostic covariate↔signature-exposure association; H08a positive-control recovery of known aetiologies):

- **Methodological prior art for h08.** TCSM is the closest existing method to the agnostic association layer proposed in h08. It conditions signature-exposure priors on observed covariates rather than running post-hoc correlation, and provides a permutation significance test — both design choices that inform h08's association layer.

- **Positive-control recovery (H08a).** Results directly demonstrate the feasibility of the h08a positive control: within a single cancer type, conditioning on HR-pathway status recovers SBS3 (not SBS5) as the elevated signature, and cancer-type conditioning in the melanoma/lung cohort cleanly separates UV (SBS7) in SKCM from smoking (SBS4) and APOBEC in LUSC — exactly the known-etiology links h08 must recover to validate its discovery prong.

- **Covariate collinearity warning (relevant to h08 design).** The finding that smoking history and UV proxy added negligible held-out likelihood improvement beyond cancer type in the melanoma/lung cohort is a concrete caution: the h08 within-tissue design is essential, not optional. Cross-tissue associations are dominated by tissue-of-origin (Alternative R1 in h08).

- **Limitation for h08 purposes.** TCSM requires covariate specification at training time — it is not a post-hoc agnostic scan of an arbitrary covariate grid. h08's phenome-wide framing (all covariates × all factors) goes beyond TCSM's one-or-few-covariate parameterization. The h08 association layer will likely need a different architectural choice (e.g., simple linear/rank-based regression on pre-computed signature exposures vs. a full generative joint model), though TCSM's statistical testing strategy (permutation of covariate labels, BH correction) is reusable.

- **Expression covariates.** TCSM supports arbitrary real-valued covariates and demonstrates LST count (a continuous assay) as a valid covariate, supporting h08's plan to incorporate expression modules as numerical covariates alongside clinical fields.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Tumor covariate x_i | Per-sample covariates in `clinical_sample.feather` / expression modules | TCSM formalizes what h08 proposes to scan |
| Signature exposure θ_i | Per-sample signature exposure H (NMF) | h08 targets these as outcomes |
| Covariate–exposure coefficient Γ | Association effect size in h08 scan | TCSM learns Γ jointly; h08 plans post-hoc regression |
| Permutation significance test | FDR-controlled association layer (h08 design) | Permutation of covariate labels is the null strategy |
| CC→TT dinucleotide count as UV proxy | Anatomic-site UV proxy in h08 pre-registration | Both use orthogonal mutation features as proxies |
| Cancer type covariate | `cancer_type` / `oncotree_code` in clinical data | Within-tissue conditioning corresponds to stratifying by these fields |

## Limitations

- **Covariate must be pre-specified.** TCSM is not a phenome-wide scan; each run requires choosing covariates upfront. This limits scalability to h08's grid-scale design.
- **No panel/targeted sequencing support.** All experiments use whole-exome data. Cross-study applicability to the heterogeneous panel data in the cBioPortal meta-analysis is unstated.
- **Computational cost.** Multiple TCSM runs are required for model selection over K; the permutation test (10,000 samples per covariate×signature pair) adds further cost. Authors note this as a limitation and suggest Dirichlet-substituted models for faster closed-form significance.
- **Logistic-normal parameterization.** Makes direct interpretation of Γ coefficients non-trivial (requires sampling), unlike a Dirichlet parameterization where concentration parameters are directly interpretable.
- **Binary covariate focus.** Statistical testing is formally described for binary covariates; extension to continuous or multi-category covariates is noted as future work.
- **Greedy covariate selection.** The mutual-information-based greedy search for the HR gene subset is data-driven but not regularized; it could overfit in small cohorts.
- **Signature collinearity unresolved.** TCSM improves SBS3/SBS5 separation but does not fully resolve the problem; the aging/MMR composite (SBS1+SBS6) found in the melanoma/lung cohort suggests that at K=4, spectrally similar pairs still merge.

## Model / Tool Availability

- **Code:** https://github.com/lrgr/tcsm (Python 3, MIT license implied by US Government authorship)
- **Dependencies:** Python 3, R `stm` package (Roberts et al. 2018), Snakemake
- **Status at time of publication:** public, with data workflow for reproducing paper experiments
- **Note:** The stm R package wraps the variational EM; users must have R installed alongside the Python wrapper.

## Follow-up

- Examine the Structural Topic Model (Roberts et al. 2016) as the upstream method; understand the variational EM implementation details for potential adaptation to the h08 association layer.
- Compare TCSM's joint-model approach to the simpler post-hoc regression strategy (regress pre-computed NMF exposures on covariates) that h08 currently favors — does the joint model yield meaningfully better power on MC3-scale data?
- Check whether any subsequent work extended TCSM to continuous covariate grids or to panel sequencing, which would be directly useful for the cBioPortal meta-analysis.
- The melanoma/lung result (collinear cancer-type + smoking/UV covariates) is a useful benchmark: the h08 within-tissue design should be validated against this same dataset to confirm the collinearity finding using the planned association method.
