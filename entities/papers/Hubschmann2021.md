---
type: paper
title: Analysis of mutational signatures with yet another package for signature analysis
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Hubschmann2021
ontology_terms:
- mutational signatures
- signature decomposition
- NMF
- COSMIC
- PCAWG
- bioinformatics
datasets: []
source_refs:
- cite:Hubschmann2021
related: []
---

# Analysis of mutational signatures with yet another package for signature analysis

- **Authors:** Daniel Hübschmann, Lea Jopp-Saile, Carolin Andresen, Stephen Krämer, Zuguang Gu, Christoph E. Heilig, Simon Kreutzfeldt, Veronica Teleanu, Stefan Fröhling, Roland Eils, Matthias Schlesner
- **Year:** 2021
- **Journal:** Genes, Chromosomes & Cancer
- **DOI/URL:** https://doi.org/10.1002/gcc.22918
- **BibTeX key:** Hubschmann2021
- **Source:** PDF

## Key Contribution

YAPSA (Yet Another Package for Signature Analysis) is an R/Bioconductor package for supervised
fitting of mutational signatures to tumor genomes. Its defining features are: (1) signature-specific
cutoffs derived from ROC analysis to increase specificity and reduce false positives, (2) 95%
profile-likelihood confidence intervals for each signature exposure, and (3) a constrained stratified
analysis (SMC — Stratification of the Mutational Catalog) that characterizes enrichment and
depletion of signatures in genomic strata defined by external criteria (e.g., mutation density,
replication timing). The package natively supports COSMIC V2 SNV, PCAWG V3 SNV, and PCAWG Indel
signature collections and can correct for WES triplet-content bias across nine common target-capture
kits.

## Methods

**Core algorithm.** Signature fitting is formulated as non-negative least squares (NNLS):
decompose the mutational catalog V (samples × 96 SNV features, or 83 Indel features) into
W (known signature matrix) × H (exposure matrix). YAPSA uses the `nnls` R package for NNLS
via the `LCD()` (linear combination decomposition) family of functions.

**Signature-specific cutoffs.** After an initial NNLS pass, signatures whose exposures fall
below their per-signature optimal cutoffs are removed, and NNLS is re-run on the remaining
subset. Cutoffs were trained by modified ROC analysis (R package ROCR) on the same COSMIC/PCAWG
data from which the signature sets were derived. The cost function balances false-positive and
false-negative attribution: the `cost_factor` (ratio of FN cost to FP cost) was optimized to
minimize total misattributions (6 for COSMIC V2, 10 for PCAWG SNV, 3 for PCAWG Indel). Clock-like
signatures (AC1/AC5, SBS1/SBS5) receive zero cutoffs since they are true positives in all samples.

**Confidence intervals.** CIs are computed via profile likelihood on ordinary differential
equations (Raue et al. 2009), implemented as `variateExp()` for SNV and
`confidence_indel_only_calculation()` for Indel signatures. A likelihood ratio test (Gauss-Newton
via `pracma::newtonsys()`) is used to approximate 95% CIs.

**Stratified analysis (SMC).** The mutational catalog is split into s exclusive strata (e.g., high /
intermediate / background mutation density) and the constrained optimization:
min ||W · H^k - V^k|| subject to non-negativity and ΣH^k = H is solved jointly. This prevents
strata-specific analysis from calling signatures absent in the overall cohort-wide analysis. The
SMC function can also start from an existing unsupervised NMF decomposition by constraining the
sum of per-stratum exposures to match the NMF output.

**WES correction.** For WES data, YAPSA computes per-feature correction factors
(q_x^{WGS,WES} = n_x^{WGS} / n_x^{WES}) to account for triplet-content differences between WGS
and each exome capture kit. Pre-computed factors for nine Agilent and Illumina kits, plus one
derived from GENCODE 19, are bundled in the package.

**Demonstration cohort.** The package was applied to an ICGC publicly available ovarian cancer
dataset (OV-AU; 70 WGS samples, ≥25 SNVs and ≥20 Indels per sample threshold), analyzed with all
three signature collections. Two precision oncology cases from the MASTER program were shown as
individual-sample examples (one BRCA2 frameshift deletion case, one neuroendocrine tumor case
without HRR pathway mutations).

## Key Findings

**Cohort-wide ovarian cancer analysis.** Aging-associated signatures (AC1/SBS1 and AC5/SBS5) and
APOBEC signatures (AC2/SBS2 and AC13/SBS13) were detected across the cohort. HRR-deficiency
signatures (AC3/SBS3 and SBS3, ID6 and ID8) were identified consistently across all three
signature collections with high confidence (SBS3: 70/70 samples high confidence, ID6: 64/70 high
confidence). MMR-deficiency (AC6/SBS1, ID1/ID2) and reactive oxygen species (SBS18) signatures
were also recovered.

**Per-sample vs. cohort-wide analysis.** Per-sample analysis recovered all cohort-wide signatures
plus additional low-frequency ones: exclusive per-sample contributions accounted for 3.35% (PCAWG
SNV), 17.17% (COSMIC V2 SNV), and 4.41% (PCAWG Indel) of total exposures — capturing biological
heterogeneity and technical noise beyond what cohort-wide decomposition resolves.

**Stratified analysis (mutation density strata).** APOBEC signatures (AC2 and SBS2) were
significantly enriched in high-mutation-density regions (Kruskal-Wallis: AC2 p_KW = 4.11×10^−9,
SBS2 p_KW = 6.16×10^−8). Aging signatures (AC1, AC5, SBS1, SBS5) were significantly depleted in
high-density regions. HRR signatures (AC3, SBS3) showed enrichment at high density. APOBEC
enrichment at dense-mutation regions is consistent with APOBEC activity concentrated at replication
stress loci.

**Precision oncology cases.** Case 1 (uterine leiomyosarcoma, germline BRCA2 frameshift deletion):
YAPSA detected AC3/SBS3 (37.8% of SNVs) and ID6 (42.4% of Indels) with high confidence, matching
the HRR-deficient phenotype and genomic instability (LOH-HRD score 23, LSTs 20). Case 2
(neuroendocrine tumor, no germline HRR mutation): AC3/SBS3, ID6, ID8 absent; LOH-HRD and LST
scores = 0, consistent with no HRR deficiency.

**Consistency.** YAPSA-identified signatures showed high overlap with signatures from the original
NMF extraction of the same datasets (Alexandrov et al. 2020), confirming that the supervised
fitting recovers the expected signals without unsupervised extraction.

## Relevance

**Direct relevance to hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and:**

YAPSA is a concrete implementation of the *supervised fitting* step (mapping a known signature
catalog W onto samples to obtain per-sample exposures H) that the hypothesis requires as its input. Key points
of contact:

1. **Positive-control recovery arm.** YAPSA's ovarian cancer analysis successfully recovers
   aging (SBS1/SBS5), APOBEC (SBS2/SBS13), HRR deficiency (SBS3/ID6/ID8), and MMR (ID1/ID2)
   signatures — exactly the known-map positive controls specified by the hypothesis (UV/SBS7 is absent here
   only because the cohort is ovarian, not skin). The agreement across COSMIC V2 and PCAWG V3
   collections (different W matrices) in detecting HRR signatures is strong evidence that the
   supervised fitting is robust.

2. **Signature-specific cutoffs vs. false positives.** The association scan will only be
   meaningful if the per-sample H values are specific (not inflated by false-positive calls).
   YAPSA's ROC-trained cutoffs directly address this; the cbioportal pipeline currently calls
   `run_restricted_sigprofiler_assignment.py` — evaluating YAPSA as an alternative or
   benchmarking tool is worth recording.

3. **Confidence intervals as weights.** In the association layer, samples with low-confidence
   signature calls should be downweighted or excluded. YAPSA's profile-likelihood CIs provide an
   operationalizable uncertainty metric for this purpose (mark a call "low confidence" if CI
   includes zero).

4. **Stratified analysis as a within-tissue design.** The SMC stratified analysis is conceptually
   analogous to the hypothesis's within-tissue conditioning: both decompose the global signal into strata to
   reveal covariate-conditional signature enrichment. SMC's result that APOBEC concentrates in
   high-mutation-density regions is a methodological proof-of-concept for the hypothesis's Prediction 3
   (expression modules may resolve APOBEC mediators more finely than clinical labels).

5. **WES correction.** The hypothesis plans to use tcga_mc3 (WGS) and potentially WES cBioPortal studies.
   YAPSA's per-kit WES triplet-content correction is a concrete reference implementation for
   handling panel/WES heterogeneity.

**Cross-study meta-analysis.** The cbioportal pipeline aggregates cBioPortal studies whose mutation
calls include WES and panel data from diverse capture kits. YAPSA's WES-correction approach is
directly applicable; however, the pipeline currently works at gene×cancer aggregation level rather
than per-sample signature decomposition, so YAPSA would be invoked downstream of the existing
pipeline outputs (as discussed in question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross).

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Mutational catalog V (samples × features) | Per-study mutation matrix (pre-aggregation) | YAPSA operates on raw per-sample catalogs; cbioportal pipeline aggregates across studies first |
| Signature matrix W (COSMIC/PCAWG) | Reference signature sets | Pipeline uses SigProfiler; YAPSA provides both COSMIC V2 and PCAWG V3 |
| Exposure matrix H | Per-sample signature exposures | hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and covariate-association outcome variable |
| Signature-specific cutoff | False-positive filter | Analogous to `is_hypermutator` flag gating in pipeline outputs |
| Profile-likelihood CI | Signature-call uncertainty | Not currently computed in the pipeline |
| SMC stratified analysis | Within-tissue covariate conditioning | hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and design analogous but at covariate-association level |
| WES triplet-content correction | Panel callable-size correction | Pipeline uses `build_panel_callable_sizes`; YAPSA corrects trinucleotide features |
| LOH-HRD score + LSTs | Genomic instability annotation | Not currently in the pipeline; relevant to hypothesis:0001-non-tumor-signal-contamination |

## Limitations

- YAPSA performs **supervised fitting only** — it cannot extract de novo signatures. The hypothesis also
  needs de novo extraction (question:0019-does-de-novo-extraction-on-the-aggregated-cohort-surface-factors-not-in); YAPSA alone does not address that prong.
- The ROC-trained cutoffs are optimized on COSMIC/PCAWG training data. Their specificity on
  small panels or heterogeneous cBioPortal studies (which have variable mutation counts and
  diverse cancer types) is not characterized.
- Per-sample analysis with Indel signatures "is only feasible if the data to be analyzed has
  enough mutations for the NNLS deconvolution to yield reliable results" — the authors
  specifically note that Indel signature ID15 could not be optimized for WGS data, and only
  WGS data is recommended for Indel signature analysis. This is a relevant constraint for any
  cBioPortal WES study.
- Profile-likelihood CI computation can fail to converge (Gauss-Newton stops at 10 outer
  iterations); in those cases, no CI is reported.
- The stratified analysis requires user-supplied, mutually exclusive strata; the enrichment
  insight depends heavily on the biological relevance of the chosen stratification variable.

## Model / Tool Availability

- **R/Bioconductor package:** YAPSA, available at http://bioconductor.org/packages/3.12/bioc/html/YAPSA.html
- **License:** Open Access (CC BY-NC-NoDerivs per journal page)
- **Vignettes:** multiple, covering WES correction, Indel signatures, stratified analysis, and
  confidence intervals
- **Input:** VCF or data frame of SNV/Indel calls; pre-built COSMIC V2, PCAWG SNV/Indel
  signature matrices bundled
- **Supplementary code:** R Markdown files for figure generation provided as supplementary data

## Follow-up

- Compare YAPSA's signature-specific cutoff strategy against SigProfiler's restricted assignment
  (`run_restricted_sigprofiler_assignment.py`) on the same cBioPortal study subset — relevant to
  choosing the supervised fitting tool for hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and.
- Evaluate YAPSA's profile-likelihood CIs as a quality filter for per-sample H values entering
  the hypothesis's covariate-association layer (low-confidence calls could be excluded or downweighted).
- Read Maura et al. 2019 (Nat Commun, cited as ref 12 in this paper) for stratified signature
  analysis in hematological malignancies — an application domain with many cBioPortal studies.
- The SMC stratified result that APOBEC is enriched in high-mutation-density regions connects
  to the hypothesis's positive-control arm: if APOBEC3 expression is the mediator, it should associate
  both with SBS2/SBS13 exposure and with local mutation density independently.
