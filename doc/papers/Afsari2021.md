---
id: "paper:Afsari2021"
type: "paper"
title: "Supervised mutational signatures for obesity and other tissue-specific etiological factors in cancer"
status: "active"
ontology_terms: []
datasets: []
source_refs:
  - "cite:Afsari2021"
related: []
created: "2026-05-31"
updated: "2026-05-31"
---

# Supervised mutational signatures for obesity and other tissue-specific etiological factors in cancer

- **Authors:** Bahman Afsari, Albert Kuo, YiFan Zhang, Lu Li, Kamel Lahouel, Ludmila Danilova, Alexander Favorov, Thomas A. Rosenquist, Arthur P. Grollman, Ken W. Kinzler, Leslie Cope, Bert Vogelstein, Cristian Tomasetti
- **Year:** 2021
- **Journal:** eLife
- **DOI/URL:** https://doi.org/10.7554/eLife.61082
- **BibTeX key:** Afsari2021
- **Source:** PDF

## Key Contribution

SuperSigs is a supervised machine-learning framework that learns mutational signatures directly from annotated clinical covariates (age, smoking, BMI, etc.), rather than applying NMF unsupervised decomposition and retrospectively correlating signatures to exposures. SuperSigs outperform Alexandrov-style NMF signatures at classifying exposed vs. unexposed patients (median AUC 0.90 vs. 0.77 across etiological factors with no prior knowledge), and notably reveal that the same etiological factor — including aging — produces tissue-specific mutational signatures rather than a single pan-cancer spectrum. The method additionally discovers a robust obesity-associated signature in kidney and uterine cancers, providing evidence that obesity contributes to mutagenesis rather than merely promoting growth.

## Methods

**Data.** Somatic exomic mutation calls from 30 TCGA cancer types (GDC Bioportal, VAF ≥ 5%), with clinical metadata (age, smoking status, BMI, viral infection, etc.) downloaded from cBioPortal. WGS data from OV and AML. External validation on ICGC PCAWG WGS (non-TCGA datasets only).

**Feature space.** 151 potential mutation features: 6 single-base substitutions (SBS), 48 dinucleotides (one flanking base), and 96 trinucleotides — all considered simultaneously. This departs from the exclusive trinucleotide-context lock used by Alexandrov NMF.

**ContextMatters (feature engineering).** A hierarchical "family tree" of mutation features is built. Observed counts are propagated down the tree to children (e.g. C>T → A[C>T] → A[C>T]G). Features with observed frequencies significantly exceeding background expectation (one-sided binomial test, Bonferroni for 150 tests) are retained as first-phase candidate features; a back-pass prunes features whose apparent signal is inherited from selected children. This produces a compact, non-redundant candidate feature set.

**FeaturesSelection.** Candidate features are ranked by AUC (area under the ROC curve) from a logistic regression classifier trained to separate exposed from unexposed patients. Five iterations of threefold cross-validation select the top features; median AUC ≥ 0.60 is required for retention. The final signature (SuperSig) is characterized by: (1) the difference in mean mutation rates (exposed minus unexposed) for each predictive feature, and (2) the logistic regression beta coefficients.

**Prediction.** A logistic regression (LR) model is trained on the full dataset using the selected features, and tested on a held-out 20% test set (80/20 split). Cross-validated AUC and apparent AUC are both reported. LDA and Random Forest comparisons are included; all yield comparable results.

**Partially supervised extension.** When annotation for some exposures is available but not others, SuperSigs for known exposures are learned first; their effects are subtracted from the mutational load of exposed patients, and NMF is applied to the residual to detect additional latent signatures. This hybrid outperforms purely unsupervised NMF.

**Unsupervised comparison baselines.** Alexandrov et al. COSMIC v2 signatures (NNLS decomposition) and randomly generated single-peak signatures (encoding only the known dominant mutation type for a given exposure — e.g. C>A for smoking, [C>T]G for aging) are both used as comparators.

**Validation.** (1) Five-fold CV repeated 5 times. (2) Label-shuffling test (AUC drops to 0.50 on shuffled data, ruling out major overfitting). (3) Robustness to 5–25% mislabeling (performance remains above unsupervised). (4) External validation on ICGC PCAWG dataset; AUC is retained or improved for nearly all SuperSigs.

**Proportion-of-mutations-attributable-to-aging estimation.** The SuperSig contribution per patient is used to estimate the fraction of the mutational load attributable to normal endogenous (aging-associated) processes, averaging 69% across 30 tissues.

## Key Findings

1. **SuperSigs outperform unsupervised NMF signatures** in classifying exposed vs. unexposed patients across a wide range of etiological factors. For aging, median cross-validated AUC = 0.73 (SuperSig) vs. 0.63 (unsupervised Signature 1). For all other annotated etiological factors, median AUC = 0.90 (SuperSig) vs. 0.77 (unsupervised).

2. **Unsupervised signatures add no information beyond the already-known dominant mutation peak.** For aging, the CpG [C>T]G peak alone (single-peak random signature) achieves median AUC = 0.63 — matching the Alexandrov Signature 1. For smoking, the C>A peak achieves AUC = 0.55; unsupervised NMF achieves 0.56. SuperSigs (AUC = 0.68) are genuinely informative beyond the dominant peak.

3. **Mutational signatures are tissue-specific, even for the same etiological factor.** Aging SuperSigs differ across cancer types (e.g. C>A transversions appear in stomach and prostate; T>C transitions in liver; C>G in colorectal, head and neck, prostate, renal, and testicular tumors — none previously described as major age-associated mutations). Smoking SuperSigs differ substantially between bladder, head and neck, and lung cancers. This contradicts the pan-cancer homogeneity assumption of COSMIC signatures.

4. **Environmental factors' mutational landscapes are often similar to the aging landscape in the same tissue**, suggesting that certain exposures may mainly accelerate cell division (inducing replication-error mutations) rather than causing direct DNA damage. This is quantified via Pearson correlation between mutational landscapes (Fig. 5 heatmap).

5. **Obesity has a detectable mutational signature in kidney (KIRP) and uterine (UCEC) cancers.** Cross-validated AUC = 0.80 (KIRP) and 0.66 (UCEC). The obesity SuperSig in KIRP features elevated C>A mutations (D[C>A], C[C>A]Y, C[C>A]A), while the UCEC signature shows a deficit in T[C>G]T. The finding that obese patients do not have more total mutations but a *different* spectrum suggests obesity alters mutational processes rather than simply increasing division rate.

6. **~69% of mutations on average can be attributed to normal endogenous aging-related processes** (range: 2% in UCEC patients with POLE mutations to 87% in smoking pancreatic cancer patients).

7. **External validation on ICGC PCAWG data** confirms generalization of SuperSigs trained on TCGA; most tissue–factor AUC values are maintained or improved (e.g. ovarian and prostate age SuperSigs gain 16–18 percentage points). The only exception was melanoma aging (AUC = 0.61 → 0.45), likely because sun exposure confounding is difficult to fully remove.

8. **The partially supervised method** (supervised removal of known factors followed by NMF on the residual) achieves higher AUC than purely unsupervised NMF for all annotated etiological factors, supporting a "peel-and-discover" strategy for unknown exposures.

## Relevance

**Direct relevance to h08 (agnostic covariate association recovers known signature aetiologies and surfaces novel upstream causes).**

SuperSigs is essentially an operationalized positive-control machine for h08a: it shows that supervised association of mutation patterns with annotated clinical covariates — age, smoking, BMI, viral infection, etc. — robustly recovers and extends known exposure→signature links. Key connections:

- **H08a positive-control recovery.** The paper demonstrates that supervised approaches recover canonical exposure→signature aetiologies (UV, smoking, MMR deficiency, APOBEC, POLE) with AUC that far exceeds unsupervised NMF. This is precisely what h08a predicts and requires before the discovery prong (h08b) can be trusted.
- **H08b discovery signal — obesity.** The discovery of an obesity mutational signature in kidney and uterine cancers is a concrete example of a novel upstream cause surfaced by treating a clinical covariate as the outcome variable, which is the spirit of h08b.
- **Tissue-specificity finding.** The observation that the same exposure produces different signatures in different tissues is a direct methodological constraint for the h08 association scan: associations must be performed within-tissue strata, not pan-cancer — consistent with h08's design (Prediction 4 / R1).
- **Partially supervised strategy vs. our agnostic scan.** The "partially supervised" extension is conceptually related to h08's plan to regress out known signatures before testing residuals, and provides a methodological template. However, our h08 approach is agnostic at the first step (no pre-specified exposures), adding a PheWAS-style sweep over all clinical covariates and expression modules.
- **Key divergence from h08.** SuperSigs requires clinical annotation as a training label; h08 begins from de-novo NMF factors (W, H) and then asks what covariates correlate with H. SuperSigs generates signatures optimized for a specific exposure; our approach evaluates signatures that were learned without any exposure in mind. These are complementary designs — SuperSigs' higher AUC reflects exposure-targeted optimization, while h08 can in principle surface unknown exposures not in the clinical annotation.
- **Relevance to cross-study meta-analysis.** The finding that unsupervised signatures (NMF) in liver cancer show Signature 4 (smoking) and Signature 6 (MMR deficiency) in virtually every patient illustrates the confounding problem in pan-cancer meta-analyses: omnipresent signatures inflate apparent mutation frequencies regardless of true etiology. The cbioportal pipeline's hypermutator flags and matched-normal study separation address related concerns.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| SuperSig (supervised, exposure-specific signature) | signature exposure (H column from NMF factorization) | SuperSigs are not NMF-derived; they are feature vectors optimized per exposure |
| Etiological factor / exposure | clinical covariate (age, smoking, BMI, etc.) | h08 treats these as outcomes to correlate against signature exposures |
| Unsupervised NMF signatures (Alexandrov) | de-novo signature extraction (SigProfiler / NMF) | pipeline's `run_restricted_sigprofiler_assignment.py` does restricted assignment |
| Tissue-specificity of signatures | within-tissue stratification (h08 design) | validates the h08 requirement for within-tissue strata |
| Partially supervised (subtract known, NMF residual) | peel-and-discover residual analysis | not yet implemented; a candidate extension for h08b |
| AUC for exposure prediction | correlation / effect size in agnostic association | h08 uses FDR-corrected effect sizes; SuperSigs use AUC from targeted classifiers |

## Limitations

- **Requires complete clinical annotation for the target exposure.** Where annotation is unavailable (or noisy), predictive power degrades. This contrasts with the agnostic h08 design, which can run on any co-measured covariate.
- **One exposure per model.** Each SuperSig is fit to classify a single clinical label (e.g. smoker vs. non-smoker). Multi-exposure interactions and unknown exposures can only be explored through the partially supervised extension.
- **Exome only (primarily).** TCGA exome data limits power for less-mutable trinucleotide contexts; WGS would increase sensitivity (OV and AML used WGS for this reason).
- **Obesity signature AUC is modest in UCEC (0.66) and unreliable in colon and esophageal cancers (AUC < 0.60 in CV).** Cross-validation failures highlight that sample size constraints limit detection.
- **Tissue-specificity means no single pan-cancer signature.** This is a finding but also a complexity: 67 SuperSigs total (≈ 2–3 per cancer), requiring tissue-stratified analyses and limiting pooled inference across studies.
- **Cannot distinguish direct mutagenesis from accelerated replication.** The observation that many environmental exposure signatures resemble aging in the same tissue is consistent with increased cell division rather than direct DNA damage — but the method cannot adjudicate between these mechanisms.
- **Clinical annotation quality.** Misclassification of exposure status (e.g. self-reported smoking, BMI measured at diagnosis vs. lifetime exposure) inflates null comparisons. The robustness tests show resilience up to 25% mislabeling, but systematic biases remain a concern.

## Model / Tool Availability

The SuperSigs methodology is implemented in R (R version 3.5.2; glm from STATS, lda from MASS, nmf from NMF package). Source code referenced as ContextMatters.R, FeatureSelection.R, and MyLDAEnvClassifier.R (internal code — no public repository cited in the paper; code may be available from the corresponding author). The Cosmic Signatures v2 table was used for unsupervised comparators.

## Follow-up

- Examine whether the "partially supervised" strategy (subtract annotated SuperSigs, apply NMF to residual) is applicable as a pre-processing step before the h08 agnostic association scan.
- The tissue-specific distance heatmap (Figure 5) is a useful reference for confirming that within-tissue stratification is necessary before running h08 associations.
- The obesity SuperSig result (especially the KIRP C>A enrichment) is an example of a novel upstream candidate (h08b class); worth revisiting if kidney cancer samples appear in the cBioPortal dataset with BMI annotation.
- Compare the 69% aging attribution estimate with the CH annotation pipeline's matched vs. unmatched stratification: clonal hematopoiesis contamination would inflate "aging" attributions in studies without matched normals.
- Tomasetti et al. 2017b (referenced for the 69% figure) should be read alongside this paper for the stem-cell division / replicative mutation rate model.
