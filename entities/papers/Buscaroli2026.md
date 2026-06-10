---
type: paper
title: 'BASCULE: bayesian inference and clustering of mutational signatures leveraging
  biological priors'
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Buscaroli2026
ontology_terms:
- mutational signatures
- Bayesian non-negative matrix factorization
- signature deconvolution
- patient clustering
- de novo signature discovery
- COSMIC
datasets: []
source_refs:
- cite:Buscaroli2026
related: []
---

# BASCULE: bayesian inference and clustering of mutational signatures leveraging biological priors

- **Authors:** Elena Buscaroli, Azad Sadr, Riccardo Bergamin, Salvatore Milite, Edith Natalia Villegas Garcia, Arianna Tasciotti, Alessio Ansuini, Daniele Ramazzotti, Nicola Calonaci, Giulio Caravagna
- **Year:** 2026
- **Journal:** Genome Biology (2026) 27:15
- **DOI/URL:** https://doi.org/10.1186/s13059-025-03835-9
- **BibTeX key:** Buscaroli2026
- **Source:** PDF

## Key Contribution

BASCULE is a Bayesian framework that unifies de novo mutational signature discovery with known-catalogue deconvolution: it simultaneously extracts catalogue-constrained exposures and statistically distinct de novo signatures via Bayesian NMF (bNMF), then clusters patients across multiple signature types (SBS, DBS, ID, CN) using a nonparametric Dirichlet Process Mixture model. The key advance is that it can expand existing signature catalogues in a principled way — ensuring new signatures differ probabilistically from known ones — while also stratifying patients into molecular subtypes whose exposures span all signature modalities jointly. Applied to ~7000 WGS cancer samples across three tumour types, BASCULE recovers established subtypes (TNBC, HER2+, MSS/MSI colorectal) and reveals DBS-informed sub-clusters that SBS alone could not resolve.

## Methods

**Model architecture — two coupled modules:**

1. **Bayesian NMF (bNMF) for signature deconvolution.** The mutation count matrix X (N samples × F features, where F = 96 for SBS, 78 for DBS, etc.) is factorised as X ≈ α̂β, with α (N×K exposure matrix) and β (K×F signature matrix) split into a fixed catalogue component β^c and learnable de novo component β^d. Priors are Dirichlet; the likelihood is Poisson. The number of de novo signatures K^d is selected by minimising BIC. A post-fit heuristic drops de novo signatures that are linear combinations of other signatures (catalogue or de novo), improving sparsity. Implemented in Pyro (stochastic variational inference, MAP estimates), with GPU support.

2. **Bayesian Dirichlet Process Mixture (tensor clustering).** After running bNMF independently per signature type, the V exposure matrices (one per modality: SBS, DBS…) are stacked into a V×N×K' tensor A (zero-padded to the widest modality). A Dirichlet Process DP(η, H) defines a mixture over G≥1 latent patient groups; each group has a centroid θ_{v,g} drawn from Dirichlet. Inference again uses SVI in Pyro; the stick-breaking construction automatically determines G. After inference, clusters with similar centroids are merged via cosine similarity.

**Two-step inference to reduce catalogue noise:** first run bNMF with K^d = 0 to identify which catalogue signatures are active (exposure > 0.2 threshold); then re-run including only those "reduced catalogue" signatures plus the de novo search.

**Benchmarking:** Compared against SigProfiler (historical COSMIC method), SparseSignatures (LASSO), and FitMS (bootstrap NMF). Evaluated on synthetic data from BASCULE's own generative model and from the independent SigFitTest tool (draws from real data). Clustering compared to K-means, KL-KMeans, and JS-Spectral methods (evaluated by NMI against ground truth).

**Cancer datasets:**
- Breast (n=2682), lung (n=1396), colorectal (n=2845) WGS samples from Degasperi et al. (Genomics England / ICGC / Hartwig) using a minimal curated starting catalogue.
- ICGC subsets with matched clinical data: skin (n=259), pancreatic (n=343), esophageal (n=315) for survival analysis (Kaplan–Meier + multivariate Cox proportional hazards).

## Key Findings

**Simulation benchmarks:**
- BASCULE matches or outperforms competitors on recall (proportion of true signatures correctly identified) and on exposure cosine similarity (CS=0.87 vs SigProfiler CS=0.79, SparseSignatures CS=0.81, FitMS_E CS=0.75).
- Reconstruction error (MSE) is comparable across BASCULE, SigProfiler, and SparseSignatures.
- Clustering NMI: BASCULE Dirichlet Process NMI=0.96 vs JS-Spectral 0.83, KMeans 0.73, KL-KMeans 0.62.
- Runtime on GPU (1000 samples): 6 min BASCULE vs 30 min SigProfiler, 194 min FitMS_E, 559 min SparseSignatures.

**Breast cancer (n=2682):** 5 clusters identified by joint SBS+DBS exposure. Cluster G1 (n=2058): HRD (SBS3/SBS13) + DBS13 — triple-negative breast cancer. Cluster G0 (n=272): APOBEC activity (SBS2/13) + DBS2/11/13 — HER2+ breast cancer. Clusters G10/G11/G13 share similar SBS patterns but differ in DBS profiles (DBS2/11, DBS14, DBS13/DBS20), allowing sub-classification that SBS alone could not resolve.

**Lung cancer (n=1396):** 7 clusters, 21 signatures (9 de novo). Cluster G1 (n=1204): heavy smokers (SBS4 + DBS2). Cluster G3 (n=31): chemotherapy (SBS31 + DBS5). Cluster G0/G12/G8 differ by DBS signatures related to HRD, HRD-related, and unknown aetiology.

**Colorectal cancer (n=2845):** 8 clusters, 32 signatures. Recovered canonical MSS/MSI split. Cluster G10 (n=412): MSI (SBS44/SBS57 via BASCULE de novo signatures SBSD12/SBSD7 + hyper-DBS14). Cluster G9 (n=28): POLE ultra-hypermutator (SBS10a + DBS3).

**Survival analysis:**
- Skin (n=259, 2 SBS clusters): Kaplan–Meier log-rank p=0.033; UV-enriched cluster G11 shows better survival; Cox HR for cluster G11 vs G1: 0.63 (95% CI: 0.39–1.02, p=0.059, borderline).
- Pancreatic (n=343, 3 clusters): log-rank p<0.0001; APOBEC-enriched G2 has HR=0.17 (0.08–0.35, p<0.001) vs G0; MMR-enriched G4 has HR=0.51 (0.29–0.90, p=0.02) vs G0.
- Esophageal (n=315): no significant survival differences detected.

## Relevance

**Direct relevance to h08 (agnostic covariate-signature association; positive-control recovery):**

BASCULE is a methodological alternative or complement to the restricted SigProfiler assignment currently planned for h08. Several connections:

1. **Catalogue-aware de novo extraction addresses the same problem as h08's positive-control design.** BASCULE's bNMF ensures de novo signatures are statistically distinct from known ones, which is precisely the concern behind h08's use of restricted assignment (SBS4, SBS7, SBS2/13) as positive controls — if those signals exist, they should appear whether you fit or discover them. BASCULE provides a framework that could run both steps simultaneously rather than sequentially.

2. **SBS+DBS joint clustering is a concrete instantiation of h08's "cross-decomposition concordance" idea.** H08 proposes that concordance between a latent mutation factor and a latent expression module is stronger evidence of shared upstream biology; BASCULE demonstrates that concordance between SBS and DBS factors already resolves subtypes invisible to SBS alone. This validates the cross-modality principle and suggests that adding expression as a third modality (BASCULE's conclusions section explicitly mentions this as future work) is a natural extension.

3. **Positive-control recovery (h08a) demonstrated implicitly.** BASCULE's breast and lung results recover UV (SBS7 family), smoking (SBS4+DBS2), APOBEC (SBS2/13+DBS2/11), MMR deficiency (SBS44/MSI), and HRD (SBS3/SBS13) without being explicitly told to — precisely the positive controls h08a pre-registers. The Pancreatic survival finding (APOBEC cluster G2 has 83% lower hazard than G0) is particularly relevant: it shows that APOBEC-exposure stratification has independent prognostic value even after adjusting for age and gender.

4. **Tool option for h08 implementation.** BASCULE's Nextflow / Singularity packaging and GPU backend make it a feasible drop-in for the pipeline's signature-extraction step, as an alternative to `run_restricted_sigprofiler_assignment.py`. The BIC-based model selection sidesteps the manual K-selection problem.

5. **Catalogue standardisation as a confound to be aware of.** The Discussion notes that heterogeneous catalogues from different groups require harmonisation (currently done by cosine similarity and human oversight). This is directly relevant to the cross-study aggregation context, where studies may be processed by different tools.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| bNMF catalogue component β^c | `run_restricted_sigprofiler_assignment.py` | Functionally equivalent: fix known signatures, infer exposures |
| bNMF de novo component β^d | `run_sigprofiler_extraction.py` (unrestricted NMF) | BASCULE does both simultaneously with separation prior |
| Dirichlet Process patient clustering on α tensor | Planned h08 association layer | BASCULE clusters; h08 regresses exposures against covariates — complementary goals |
| BIC-based K^d selection | Manual K selection in current pipeline | BASCULE automates this step |
| Post-fit linear-combination heuristic | Not currently implemented | Useful heuristic for dropping artefactual de novo signatures |
| Pyro / SVI inference | scikit-learn NMF (current) | Different inference paradigm; Bayesian approach propagates uncertainty |

## Limitations

- Benchmarking on SigFitTest (more realistic synthetic data) shows lower overall performance than on BASCULE's own generative model — particularly sensitive to datasets with low mutation counts, which is a concern for WES and panel-sequenced cBioPortal studies.
- The clustering module works on exposures α after bNMF; if bNMF mis-attributes exposures, clustering inherits those errors — no joint end-to-end uncertainty propagation.
- Survival analysis restricted to ICGC subsets with matched clinical data; esophageal cancer showed no significant differences, suggesting the approach is not universally prognostic.
- The Dirichlet Process requires a user-specified maximum G; results may be sensitive to this upper bound and to the concentration η.
- DBS signals were sparse (>98% zero entry) in several ICGC datasets — DBS was therefore excluded from survival analyses. This is a practical limitation for datasets dominated by WES.
- No joint multi-region or longitudinal formulation yet; the authors note this as future work.
- Comparisons to SigProfiler/SparseSignatures/FitMS represent only the bNMF step; no competing tool was evaluated on the combined deconvolution + clustering task.

## Model / Tool Availability

- **Repository:** available as a Nextflow module with Singularity image (details in paper; GitHub link not explicitly shown in pages read).
- **Language:** Python (Pyro probabilistic programming).
- **Hardware:** GPU-compatible; benchmarked on GPU for cohorts of ≥500 samples; CPU mode available.
- **License:** open access (CC-BY-NC-ND 4.0 for article; tool license not stated in read pages).
- **Input:** mutation count matrix (any signature type: SBS 96-channel, DBS 78-channel, ID, CN); optional known catalogue.
- **Output:** signature profiles β, exposures α, cluster assignments, BIC curves.

## Follow-up

- The authors suggest extending BASCULE to include methylation and gene expression signals as additional modalities — this is exactly the h08b discovery prong. Worth tracking for a follow-up implementation using BASCULE rather than a bespoke association model.
- The pancreatic cancer result (APOBEC cluster, HR=0.17) warrants checking against cBioPortal pancreatic studies in the pipeline — is APOBEC exposure recoverable at WES depth, and does it stratify survival there?
- The DBS-resolved sub-clusters in breast cancer (G10/G11/G13) would be invisible to SBS-only analysis; this motivates including DBS signature extraction as a parallel pipeline step.
- Degasperi et al. 2022 (already summarised in `paper:Degasperi2022`) is the source catalogue and data used here — BASCULE's results extend and validate that catalogue.
