---
id: "paper:Landy2026"
type: "paper"
title: "bayesNMF: Fast Bayesian Poisson NMF with Automatically Learned Rank Applied to Mutational Signatures"
status: "active"
ontology_terms:
  - mutational signatures
  - Bayesian NMF
  - MCMC
  - Poisson factorization
  - rank selection
  - somatic mutation
datasets:
  - "PCAWG (Pan-Cancer Analysis of Whole Genomes)"
source_refs:
  - "cite:Landy2026"
related:
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
created: "2026-05-31"
updated: "2026-05-31"
---

# bayesNMF: Fast Bayesian Poisson NMF with Automatically Learned Rank Applied to Mutational Signatures

- **Authors:** Jenna M. Landy, Nishanth Basava, Giovanni Parmigiani
- **Year:** 2026
- **Journal:** Journal of Computational and Graphical Statistics
- **DOI/URL:** https://doi.org/10.1080/10618600.2026.2657487
- **BibTeX key:** Landy2026
- **Source:** PDF

## Key Contribution

bayesNMF introduces a Metropolis-Hastings-within-Gibbs (MH-within-Gibbs) sampler for Bayesian
Poisson NMF that avoids the computationally expensive Poisson augmentation step required by
standard Gibbs samplers. Combined with a BIC-based Sparse Bayesian Factor Inclusion (SBFI)
prior, the method learns latent rank automatically within a single Bayesian run while still
reporting full posterior uncertainty — a combination no prior method achieved simultaneously.
On simulated data the Poisson+MH samplers are 3-30x faster than standard Poisson samplers, and
SBFI achieves comparable or better precision and sensitivity than SignatureAnalyzer's automatic
relevance determination while also quantifying uncertainty.

## Methods

**Model family.** Bayesian Poisson NMF: M ~ Poisson(PE) where M is the K×G mutation count
matrix (K = 96 SBS channels, G = samples), P is the K×N signatures matrix, E is the N×G
exposures matrix. Two prior variants are implemented: Truncated Normal (L2) and Exponential
(L1) on elements of P and E.

**Poisson+MH for computational efficiency.** Instead of Poisson augmentation (which introduces
NKG auxiliary variables and costs O(N(K+G+KG)) per Gibbs iteration), bayesNMF uses
Metropolis-Hastings steps. Proposals for P and E are drawn from the full conditional of a
paired Normal Bayesian NMF model with identical priors. Because Normal and Poisson Bayesian NMF
share approximately the same MAP solutions (up to scaling/permutation), these Normal-based
proposals have high overlap with the Poisson posterior near its mode. Priors cancel from the MH
acceptance ratio, leaving a ratio of Poisson to Normal likelihoods that is fast to evaluate.
This reduces cost to approximately O(N(K+G)) per iteration.

**Sparse Bayesian Factor Inclusion (SBFI) for rank learning.** A diagonal binary matrix A
(A_nn ∈ {0,1}) gates each of the N prespecified latent factors. A BIC-like sparsity penalty is
embedded in the Bernoulli prior on A_nn, with the probability of inclusion q governed by a
uniform hyperprior on expected rank R. A simulated-annealing tempering schedule (temperature γ
progressing 0→1 over burn-in) prevents premature convergence to low rank. After burn-in, the
MAP inclusion matrix (mode over posterior samples) identifies the learned rank, and P/E
posteriors are summarised conditional on that MAP structure. Posterior uncertainty on signatures
and exposures is still reported at the learned rank. SBFI is compared against: (a) minBIC —
fitting separate Poisson+MH samplers for each candidate rank and picking the one minimising BIC;
(b) SignatureAnalyzer's ARD (learns rank via L1/L2 optimization without posterior uncertainty).

**Baseline models.** Standard Gibbs samplers for Poisson Bayesian NMF (Exponential and Gamma
priors, via Poisson augmentation) and Normal Bayesian NMF (Exponential and Truncated Normal
priors) are implemented for direct comparison, with all settings except likelihood/prior held
constant.

**Inference.** Final 1000 posterior samples used for inference. Scale indeterminacy resolved by
normalizing P columns to sum to 1. Posterior means and 95% credible intervals (element-wise
2.5th/97.5th percentiles) are reported. Optional post-hoc assignment to reference signatures
(default: COSMIC SBS v3.3.1) via Hungarian algorithm with majority-vote ensemble across
posterior samples.

**Simulation study.** True latent ranks N ∈ {2,4,8,16}, sample sizes G ∈ {16,32,64,128}.
Signatures sampled from COSMIC SBS v3.3.1; exposures ~ Dirichlet; mutation counts ~
Poisson(PE). 10 datasets per (N,G) condition. Metrics: RMSE, KL-divergence for reconstruction;
worst-case cosine similarity for signature recovery; rank bias, precision (proportion of
estimated signatures with a true match), sensitivity (proportion of true signatures with an
estimated match).

**Real data application.** PCAWG SBS mutation count data (96-channel). 37 histology groups,
excluding those with ≤10 samples and benign groups, leaving 32 cancer types. Hypermutated
samples excluded using a Negative Binomial mixture model (65 samples removed total, <3% of
data). bayesNMF Poisson+MH with Truncated Normal priors and SBFI (rank ∈ [1,20]) compared
against SignatureAnalyzer with L2 priors.

## Key Findings

- **Speed.** Poisson+MH samplers are 3-30× faster than standard Poisson (Poisson augmentation)
  samplers, with the gap growing with dimensionality. Posterior uncertainty is reported at the
  cost of ~12 additional minutes over SignatureAnalyzer (4 vs 16 minutes for the MH approach at
  tested scales). minBIC takes ~2 hours with Poisson+MH, versus >20 hours with standard Poisson
  augmentation.

- **Correctness of Poisson+MH.** Normal Bayesian NMF produces point estimates nearly identical
  to Poisson Bayesian NMF (cosine similarity agreement >0.99 in ≥84% of simulation cases). MH
  steps increase effective sample sizes without substantially changing credible interval widths.

- **Rank learning.** Under Truncated Normal/L2 priors: all approaches (SBFI, minBIC,
  SignatureAnalyzer ARD) estimate rank comparably well, but with different error patterns —
  SignatureAnalyzer overestimates at low and high ranks, while SBFI and minBIC tend to
  underestimate at high ranks. SBFI and minBIC achieve higher precision and sensitivity than
  SignatureAnalyzer, meaning the signatures they do estimate are more accurate (SignatureAnalyzer
  often produces noisy or split signatures even at correct rank). Under Exponential/L1 priors:
  SBFI's sparsity penalty is too strong at high ranks; minBIC still outperforms SignatureAnalyzer.

- **PCAWG application.** bayesNMF+SBFI produces sparser solutions than SignatureAnalyzer+ARD
  (roughly half as many signatures per cancer type); SignatureAnalyzer estimated a rank of 76
  for skin melanoma. High overlap in shared signatures (SBS1, SBS5, SBS40 found in nearly every
  cancer type, consistent with Alexandrov et al. 2020). Six signatures unique to bayesNMF after
  accounting for posterior uncertainty include: SBS5 in CNS pilocytic astrocytoma/pancreatic
  adenocarcinoma, SBS1 in CLL, SBS95 in HCC, SBS36 in prostate adenocarcinoma (previously
  reported), and SBS9 in esophageal adenocarcinoma (novel, though found in esophageal small cell
  carcinoma). The authors note that bayesNMF unique signatures largely reflect posterior
  uncertainty differences rather than fundamental disagreement — 28/34 (82%) had a
  SignatureAnalyzer-derived signature among candidates receiving assignment votes.

## Relevance

**h08 — agnostic covariate-signature-exposure association.** Any downstream phenome-wide
association study (PheWAS) of signature exposures against covariates requires reliable,
calibrated exposure estimates as the outcome variable. bayesNMF directly addresses two
bottlenecks relevant to h08:

1. **Posterior uncertainty on exposures.** Standard NMF and even SignatureAnalyzer return point
   estimates. bayesNMF returns 95% credible intervals on each sample's exposure to each
   signature, which could propagate uncertainty into downstream association tests (e.g., as
   measurement-error-corrected regression inputs).

2. **Rank selection without subjectivity.** The SBFI prior learns rank within a single Bayesian
   run. For the cross-study aggregation underlying h08, where signature extraction may be run
   across many cancer types and studies independently, an automated and principled rank selection
   procedure reduces one major analyst-degree-of-freedom and makes results more reproducible
   across runs.

3. **Positive-control recovery of known aetiologies.** In the PCAWG analysis, bayesNMF
   recovers SBS1 (clock/deamination), SBS5 (clock), SBS40 (clock), UV-associated signatures
   in skin, and tobacco-associated signatures in lung — the same positive controls h08 expects
   to recover in any well-calibrated signature pipeline. The PCAWG results can serve as a
   benchmark for the cbioportal cross-study extraction.

4. **Hypermutator exclusion.** bayesNMF's own pipeline excludes hypermutated samples via
   Negative Binomial mixture modeling before extraction to avoid signature bleeding — consistent
   with the cbioportal pipeline's planned hypermutator annotation (t081/t092-t099) and
   `is_hypermutator_exclusive` column logic.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Signatures matrix P (K×N) | NMF basis / signature dictionary | 96-channel SBS; comparable to COSMIC SBS reference |
| Exposures matrix E (N×G) | Per-sample signature exposures | Used as outcomes in h08 association tests |
| SBFI learned rank N' | Number of active signatures | Eliminates manual elbow/BIC scan |
| Posterior credible intervals on E | Uncertainty on exposure estimates | Currently absent from SigProfiler/SignatureAnalyzer outputs used in pipeline |
| Hypermutator exclusion (NB mixture) | `is_hypermutator` flag + `_exclusive` ratio columns | Same rationale; bayesNMF uses per-cancer mixture models |
| COSMIC SBS v3.3.1 reference | `bailey2018_driver` overlay + COSMIC cross-ref | Reference used for cosine similarity matching |

## Limitations

- **R-only implementation.** The bayesNMF package is R-only (GitHub: jennalandy/bayesNMF),
  which adds friction to integration in the predominantly Python cbioportal pipeline.
- **Gamma prior not supported in Poisson+MH.** The Poisson+MH approach requires a prior
  (shared between target and proposal) whose full conditional in Normal Bayesian NMF is of a
  known family; Gamma priors cannot be used. This precludes direct comparison to SigProfiler
  (which uses Gamma priors via SigneR-style models).
- **SBFI with Exponential prior over-penalizes high ranks.** At large true ranks, SBFI with L1
  priors underestimates rank by a wide margin; minBIC is the safer choice in that regime.
- **Reference assignment assumes unique mapping.** The Hungarian algorithm forces a 1-to-1
  assignment between estimated and reference signatures. Multiple estimated signatures
  mapping to the same reference (e.g., split signatures) reduces apparent precision in
  simulations.
- **Simulation uses PCAWG-like data.** All simulations draw signatures from COSMIC SBS v3.3.1
  and generate exposures from symmetric Dirichlet. Performance may differ in highly asymmetric
  real-data exposure distributions or with signatures not in COSMIC.
- **No joint multi-study extraction.** bayesNMF operates study-by-study. The multi-study
  extension (Grabski et al. 2025) is cited as future work; cross-study consistency of learned
  signatures is not evaluated here.

## Model / Tool Availability

- **R package:** `bayesNMF` — GitHub: [jennalandy/bayesNMF](https://github.com/jennalandy/bayesNMF)
- **Reproducibility code:** GitHub: [jennalandy/bayesNMF_PAPER](https://github.com/jennalandy/bayesNMF_PAPER)
- **Data:** PCAWG via ICGC ARGO data portal (docs.icgc-argo.org/docs/data-access/)
- **License:** Not stated in manuscript [UNVERIFIED]
- **Hardware requirements:** No GPU required; MCMC runtime ~4-16 minutes for single-cancer
  analyses at N≤20, G≈64 on unspecified hardware [UNVERIFIED exact hardware specs]

## Follow-up

- Grabski et al. 2025 (Genome Biology 26:98) — Bayesian multi-study NMF for mutational
  signatures; builds on the same Gibbs framework, extends to joint cross-study extraction.
  Directly relevant to whether cross-study consistency of signatures can be learned jointly
  rather than by post-hoc cosine alignment.
- Zito and Miller 2024 (arXiv:2404.10974) — Compressive Bayesian NMF; an alternative
  efficiency approach that the authors suggest could be combined with Poisson+MH in future work.
- **Project question:** Can the posterior credible intervals on per-sample signature exposures
  from bayesNMF be used as error-in-variables inputs to the h08 covariate association tests,
  rather than using point estimates?
- **Project question:** For the cbioportal cross-study extraction, does applying bayesNMF
  per-cancer-type with SBFI produce more parsimonious signature sets than the current
  SigProfiler workflow, and does it recover the expected positive controls (UV, smoking,
  APOBEC, MMR) with fewer spurious components?
