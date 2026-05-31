---
id: "paper:Rosales2017"
type: "paper"
title: "signeR: an empirical Bayesian approach to mutational signature discovery"
status: "active"
ontology_terms:
  - mutational signatures
  - NMF
  - empirical Bayes
  - MCMC
  - model selection
  - somatic mutation
datasets: []
source_refs:
  - "cite:Rosales2017"
related:
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
created: "2026-05-31"
updated: "2026-05-31"
---

# signeR: an empirical Bayesian approach to mutational signature discovery

- **Authors:** Rafael A. Rosales, Rodrigo D. Drummond, Renan Valieris, Emmanuel Dias-Neto, Israel T. da Silva
- **Year:** 2017 (advance access 2016)
- **Journal:** Bioinformatics, 33(1): 8–16
- **DOI/URL:** https://doi.org/10.1093/bioinformatics/btw572
- **BibTeX key:** Rosales2017
- **Source:** PDF

## Key Contribution

signeR applies an empirical Bayesian treatment of Poissonian NMF to mutational signature discovery, combining a Metropolized Gibbs sampler with an MCMC-EM outer loop to jointly estimate signatures (P), exposures (E), and hyperparameters. Model rank (number of signatures N) is selected via median BIC computed directly from MCMC samples, without any additional approximation. Beyond signature extraction, the paper introduces two clinically-oriented outputs: a **Differential Exposure Score (DES)** that tests per-signature exposure differences across sample groups (via Kruskal-Wallis over MCMC samples), and a **posterior sample classification** scheme that assigns unlabelled samples to clinical groups based on exposure profiles via k-Nearest Neighbours.

## Methods

**Model.** Mutation counts M (K × G matrix; K = 96 trinucleotide types, G = genomes) are Poisson distributed with rate P ⊙ E ⊙ W, where W is an opportunity (trinucleotide frequency) weight matrix. A data augmentation latent-variable decomposition (Mij = Σ_n Z_inj) enables Gibbs sampling. Conjugate Gamma priors are placed on entries of P and E; hyperparameters are themselves Gamma/exponential distributed and estimated from data (empirical Bayes, not fully Bayesian).

**Inference.** A Metropolized Gibbs sampler cycles over (Z, θ, ψ) conditioned on hyperprior γ; a stochastic EM step updates γ using MCMC samples. This MCMC-EM alternation converges (Theorem 1: total-variation convergence as R, U → ∞). Final MCMC samples provide the full posterior over P and E.

**Rank selection.** BIC is computed per MCMC sample at each candidate rank k; the median BIC across samples identifies N. A binary-search-like algorithm (Algorithm 2) reduces computation from O(T) to O(log T) full MCMC-EM runs for unimodal BIC curves.

**Differential Exposure Score (DES).** Kruskal-Wallis test applied to each exposure MCMC sample E^(r) over predefined sample groups; the median of −log(p-values) across samples defines DES. Signatures with DES above a threshold are deemed differentially active.

**Sample Classification.** k-NN applied to each E^(r); majority-vote (>75% agreement) assigns unlabelled samples; ambiguous samples labelled "undefined."

**Data.** 21 breast cancer WGS genomes (Nik-Zainal 2012, Sanger FTP), 183,916 somatic point mutations. 114 gastric cancer TCGA WGS genomes (Bass 2014), 38,157 curated somatic mutations, subsetted to Lauren's classification groups.

**Implementation.** R + C++ on Bioconductor (`bioconductor.org/packages/signeR`). Runs on a standard computer. Reads VCF input, produces M matrix, signatures, exposures, and graphics.

## Key Findings

**Simulation benchmarks vs LBA (Alexandrov 2013) and EMu (Fischer 2013):**
- All 500/500 signeR runs correctly estimated 4 signatures from a 4-signature synthetic dataset; only 51/500 EMu runs recovered the correct rank (449/500 found 3).
- On accuracy (sum of squared errors between true and estimated P): signeR mean SSE = 0.095 (SD 0.016) vs EMu 0.23 (SD 0.007) with opportunities (P < 2.2e-16, Wilcoxon); signeR 0.044 (SD 0.029) vs LBA 0.203 (SD 0.012) without opportunities (P < 2.2e-16).
- signeR estimates cluster at a single log-likelihood value; EMu estimates bifurcate across two modes (one for the 3- and one for the 4-signature runs), indicating sensitivity to initialization.

**Breast cancer (21 genomes):** 5 signatures recovered, matching COSMIC signatures 1, 2, 3, 13, and one unreported. DES with BRCA1/BRCA2 germline status highlights signatures S3 (HRD/BRCA-related) and S5 (APOBEC), consistent with known biology. Leave-one-out classification: 1/21 samples misclassified.

**Gastric cancer (114 genomes):** 4 signatures identified. DES reveals two signatures (COSMIC Sigs 3 and 17) enriched in intestinal-type gastric cancer (better prognosis) vs diffuse type. Posterior classification assigns 65% of samples confidently; among classified, 75% match Lauren's histological label.

## Relevance

**Directly relevant to h08 (agnostic covariate→signature-exposure association).**

1. **DES as a primitive h08 association test.** The Differential Exposure Score is conceptually the same operation h08 proposes (covariate group → signature exposure), implemented as Kruskal-Wallis over MCMC posterior samples rather than on point-estimate exposures. signeR's built-in DES can serve as a baseline or sanity-check for the h08 association layer, especially for binary/categorical clinical covariates (BRCA status, Lauren's subtype).

2. **Positive-control recovery via DES.** The breast cancer APOBEC recovery (S1/S5 = COSMIC Sigs 2/13, DES significant for BRCA+ group) and HRD recovery (S3 = COSMIC Sig 3) replicate exactly the kind of "recovery of known aetiology from agnostic association" that H08a demands. The paper effectively demonstrates a proto-positive-control for H08a's APOBEC arm (APOBEC3 expression ↔ SBS2/13) even though it uses a binary germline-mutation group rather than mRNA expression.

3. **Uncertainty-propagation in exposure estimation.** Because signeR propagates posterior uncertainty in E through the association test (applying Kruskal-Wallis to each MCMC sample), the DES is naturally calibrated against the uncertainty in exposure attribution. H08's association layer could benefit from the same principle if it relies on per-sample exposure point estimates from SigProfiler/deconstructSigs rather than a Bayesian method.

4. **Rank selection as a prerequisite for h08.** H08 requires de-novo extraction (q019) upstream of the association scan. signeR's BIC-based rank selection — robust to initialization, no extra approximation — is directly applicable for that de-novo step on the aggregated cBioPortal cohort.

5. **Sample classification for patient stratification.** The posterior classification output (kNN on MCMC exposure samples) suggests that signature-based patient groups are clinically predictive (gastric: 75% Lauren's concordance among confidently classified). This supports H08b's framing that novel covariate↔signature associations can surface actionable patient subgroups.

**Limitations for h08's scale:** signeR's computational design targets individual cohorts (21–114 samples). Its per-sample WGS assumption, MCMC cost scaling (O(K·N·G) per iteration), and R-package architecture are not designed for the thousands-of-sample, multi-study, panel-sequencing context of the cBioPortal meta-analysis. The successor tool signeR 2.0 (Drummond et al., 2023; `cite:Drummond2023`) directly extends the DES framework with survival and staging regression — more directly applicable to h08's multi-covariate design.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Mutation count matrix M (K × G) | per-sample 96-channel SBS spectrum | Project aggregates counts to cancer×study level; per-sample spectra needed for signeR |
| Signature matrix P (K × N) | COSMIC SBS reference W matrix | signeR can discover de-novo; project can refit against COSMIC |
| Exposure matrix E (N × G) | per-sample signature exposures H | What h08 treats as outcome variable in its association scan |
| Opportunity matrix W | trinucleotide frequencies per genome | Project does not currently compute this; WES panels require panel-callable BED |
| Differential Exposure Score | h08 covariate→signature association | DES is the binary/ordinal special case; h08 extends to continuous covariates and expression |
| Posterior sample classification | patient stratification by signature | h08b discovery application |
| MCMC BIC rank selection | number-of-signatures hyperparameter | Required for q019 de-novo extraction on aggregated cohort |

## Limitations

- **Scale.** MCMC is computationally expensive per sample; not designed for thousands of panel-sequenced tumors. Rank selection requires one full MCMC-EM run per candidate N.
- **Panel sequencing.** Opportunity matrix W assumes full trinucleotide frequency counts; not straightforward for targeted/panel data where many trinucleotides are uncallable. The project's panel-callable-size infrastructure (build_panel_callable_sizes) partially addresses this at cohort level.
- **Rank selection assumes unimodal BIC.** Algorithm 2 (binary search) only guarantees finding the global maximum for unimodal BIC curves; multimodal curves (e.g., ambiguous data) may yield wrong rank.
- **DES is univariate per clinical group.** It tests one grouping variable at a time via Kruskal-Wallis; not designed for multivariate, FDR-controlled, phenome-wide association across a covariate grid (what h08 proposes).
- **No continuous covariate regression.** DES requires categorical group labels; continuous covariates (age, TMB, mRNA module scores) require the signeR 2.0 extensions.
- **Identifiability.** As with all NMF methods, P and E are only jointly identifiable up to permutation and scale; results depend on the BIC-selected rank.

## Model / Tool Availability

- **Package:** `bioconductor.org/packages/signeR` (R/Bioconductor)
- **Language:** R + C++
- **Input:** VCF files or prebuilt M matrix; computes trinucleotide context internally
- **License:** Bioconductor (open source) [UNVERIFIED — exact CRAN/Bioconductor license field not checked]
- **Hardware:** Standard desktop/laptop; no GPU requirement
- **Successor:** signeR 2.0 (Drummond et al. 2023, BMC Bioinformatics) extends to survival and staging regression via DES

## Follow-up

- **signeR 2.0** (`cite:Drummond2023` already in references.bib): the direct extension with multi-covariate clinical regression — more applicable to h08's association layer.
- **deconstructSigs** (Rosenthal et al. 2016): a refitting approach (E-only estimation given fixed P, N); relevant to h08's restricted-assignment arm on cBioPortal panel data.
- **EMu** (Fischer et al. 2013): probabilistic NMF with EM; benchmark comparison target in this paper; less robust than signeR per simulations here.
- **Shiraishi et al. 2015:** independent-feature NMF parametrization; different model class from the one signeR (and COSMIC) use.
- **Questions for the project:** Does the cBioPortal aggregated cohort have sufficient WGS/WES sample counts per cancer type to run signeR de-novo extraction (q019)? What is the cost of MCMC-EM at N = 10–30 for cohorts of ~200–500 samples?
