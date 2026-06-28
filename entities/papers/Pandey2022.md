---
type: paper
title: 'MetaMutationalSigs: comparison of mutational signature refitting results made
  easy'
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Pandey2022
ontology_terms:
- mutational signatures
- signature refitting
- COSMIC
- somatic mutation
- software
datasets: []
source_refs:
- cite:Pandey2022
related: []
---

# MetaMutationalSigs: comparison of mutational signature refitting results made easy

- **Authors:** Palash Pandey, Sanjeevani Arora, Gail L. Rosen
- **Year:** 2022
- **Journal:** Bioinformatics, 38(8), 2344–2347
- **DOI/URL:** https://doi.org/10.1093/bioinformatics/btac091
- **BibTeX key:** Pandey2022
- **Source:** PDF

## Key Contribution

MetaMutationalSigs is a Docker-packaged R/Python wrapper that runs four established COSMIC
signature-refitting tools (DeconstructSigs, MutationalPatterns, Sigfit, Sigminer/Sigflow) on
the same input VCF matrix and aggregates their outputs into harmonised CSV files plus a
standardised set of comparison visualisations (RMSE box plots, cosine-similarity heatmaps,
per-sample bar charts). The core motivation is that different refitting tools with different
underlying algorithms — multiple linear regression, NNLS, Bayesian inference, simulated
annealing — can yield substantially different signature-exposure estimates for the same samples,
and no single gold standard exists; researchers therefore need to survey all tools simultaneously
before drawing biological conclusions. The paper also provides an empirical comparison of the
four tools on 188 TCGA LAML whole-exome samples using both COSMIC Legacy SBS (V2) and COSMIC V3
catalogs, showing that V3 reduces inter-tool disagreement and lowers reconstruction RMSE for two
of the four methods [@Pandey2022].

## Methods

**Pipeline overview.** Input is a VCF file that has already passed the user's preprocessing
steps (alignment → variant calling → filtering/annotation). MetaMutationalSigs converts it to
the 96-channel SBS mutation matrix using SigProfilerMatrixGenerator, then passes the matrix in a
common format to each wrapped tool.

**Wrapped tools and their algorithms:**

| Tool | Algorithm | Reference |
|---|---|---|
| DeconstructSigs | Multiple linear regression (coefficients ≥ 0) | Rosenthal et al. [@Rosenthal2016] |
| MutationalPatterns | Non-negative least squares (NNLS) | MutationalPatterns package paper |
| Sigfit | Bayesian inference | Gori & Baez-Ortega 2018 |
| Sigminer / Sigflow | Simulated annealing (SA) | Sigminer / Sigflow package paper |

**Signature catalogs supported:** COSMIC Legacy SBS (V2) and COSMIC V3 SBS, DBS, and ID
signatures.

**Evaluation.** Tools are compared on 188 TCGA LAML WES samples using [@Pandey2022]:
- RMSE between the reconstructed signature profile (refit from reference signatures) and the
  observed 96-channel mutation profile.
- Pairwise cosine similarity of per-tool signature-contribution estimates for the same patient.

**Rationale for focusing on refitting rather than de-novo extraction.** The authors note that
refitting requires no minimum sample-size threshold (works per-sample), is computationally
lighter, and uses COSMIC's well-established reference catalog. De-novo extraction has additional
caveats: cosine-similarity thresholds for assignment are not standardised, and a novel extracted
signature may resemble multiple reference signatures ambiguously.

**Implementation.** R + Python; distributed as a Docker image;
code at https://github.com/EESI/MetaMutationalSigs.

## Key Findings

1. **COSMIC V3 improves reconstruction fidelity for some tools.** RMSE drops significantly for
   MutationalPatterns and Sigflow when switching from V2 (Legacy) to COSMIC V3; it does not
   change for DeconstructSigs and Sigfit.

2. **Inter-tool agreement is higher under COSMIC V3 than V2.** The pairwise cosine-similarity
   heatmap for TCGA-AB-2804 shows the four standard tools cluster more tightly under V3,
   whereas V2 produces a more dispersed pattern — suggesting Legacy signatures conflate
   multiple contributing processes.

3. **COSMIC V3 reveals richer biology than Legacy SBS.** In the three LAML patient examples,
   Legacy SBS refitting assigns Signature 3 (homologous-recombination deficiency) as the
   dominant contributor for all three samples. V3 refitting instead identifies sample-specific
   dominant signatures: unknown aetiology for TCGA-AB-2804; unknown chemotherapy-related
   signatures and distinct MMR signatures (SBS20 and SBS26, respectively) for the other two.
   This illustrates that the V3 catalog's finer granularity can unmask sample-level
   heterogeneity invisible to Legacy refitting.

4. **Sigflow had the lowest RMSE** in the LAML evaluation and was used for the per-patient
   illustration in Figure 1D.

5. **No tool predicted DBS signatures** for the LAML WES samples used in the benchmark.

## Relevance

**Direct relevance to hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and (agnostic covariate↔signature-exposure association).**

The refitting step sits upstream of the hypothesis: before any covariate association can be run, a
per-sample signature-exposure vector H must be estimated. MetaMutationalSigs is a practical
tool for exactly that estimation step; its cross-tool comparison functionality directly
addresses a key methodological uncertainty for the hypothesis:

- **Choice-of-tool is a non-trivial variance source.** The LAML results confirm that different
  algorithms produce non-trivially different exposure estimates for the same sample. Any
  downstream covariate association (positive-control recovery of UV/smoking/APOBEC/MMR; discovery)
  will have results that are sensitive to which refitting tool was used. Running multiple tools
  and checking that a covariate↔signature association holds across all of them is a concrete
  robustness test.

- **COSMIC V3 vs Legacy is an analytic choice that matters.** The paper shows V3 provides both
  lower reconstruction error and higher inter-tool agreement, supporting the use of V3 as the
  reference catalog for the hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and workflow (already implied by the cbioportal pipeline's use of
  `run_restricted_sigprofiler_assignment.py`).

- **Positive-control recovery.** The LAML example demonstrates that different tools
  assign biologically distinct dominant signatures; this heterogeneity must be considered when
  defining "recovery" of a known exposure→signature link. A tool that incorrectly collapses to
  Signature 3 for all samples would not recover, say, the MMR/MSI↔SBS26 link.

- **Cross-study meta-analysis context.** The cbioportal pipeline aggregates many studies.
  MetaMutationalSigs operates per-study on VCF-level inputs; once per-sample refitting is run
  within each study, the tool's CSV outputs are directly consumable by the cross-study
  association layer planned for hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and.

**Broader pipeline relevance.** The tool validates the choice of SigProfilerMatrixGenerator as
the canonical input-matrix generator (already used in the pipeline). The Docker packaging is
relevant for reproducibility standards.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Refitting (reconstruct observed profile from COSMIC) | `run_restricted_sigprofiler_assignment.py` | Pipeline already implements restricted assignment; MetaMutationalSigs offers multi-tool comparison as a validation layer |
| Signature contribution matrix (per-sample) | Columns of H in NMF/refitting decomposition | Used as exposures in the hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and association scan |
| COSMIC V3 SBS/DBS/ID catalog | Reference catalog for restricted assignment | V3 reduces inter-tool disagreement; confirms pipeline catalog choice |
| RMSE between reconstructed and observed profile | Reconstruction error / goodness-of-fit diagnostic | Useful QC metric for per-study refitting quality |
| Cosine similarity between tool results | Tool-concordance check | Natural robustness check for hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and associations |

## Limitations

- **Narrow benchmark.** The empirical comparison covers only one cancer type (LAML, n=188 WES),
  so generalisation of the relative tool rankings to other histologies or sequencing modalities
  (WGS, targeted panels) is not established.

- **Applications Note format.** The paper is a short applications note (4 pages); there is no
  systematic simulation study, no ground-truth synthetic evaluation, and no power analysis. Tool
  ranking claims should be treated as preliminary.

- **No de-novo extraction.** The package deliberately omits de-novo signature extraction, which
  is an alternative (and for large cohorts, preferred) approach. For h08b discovery on the
  aggregated cBioPortal cohort, de-novo extraction may be more appropriate than refitting.

- **Maintenance uncertainty.** The COSMIC catalog evolves; the paper acknowledges the need to
  keep reference signatures updated as new versions are released. The current COSMIC version
  supported by the tool is not stated explicitly.

- **No DBS prediction on LAML WES.** No tool produced DBS contributions for the samples tested,
  which may reflect panel size / sensitivity limits of WES rather than tool limitations.

- **Refitting-only.** As the authors note, refitting methods require a priori knowledge about
  the sample set and each package; results should not be used without biological assessment.

## Model / Tool Availability

- **GitHub:** https://github.com/EESI/MetaMutationalSigs
- **Installation:** Docker (primary); R + Python dependencies
- **Input:** VCF files (post variant-calling + annotation); internally converts to 96-channel
  mutation matrix via SigProfilerMatrixGenerator
- **Output:** CSV contribution tables + SVG/HTML visualisations (heatmaps, RMSE box plots,
  per-sample bar charts) — see Table 1 of the paper
- **Signature catalogs:** COSMIC Legacy SBS (V2) and COSMIC V3 SBS, DBS, ID
- **License:** Open source (GitHub; specific license not stated in paper)

## Follow-up

- Compare MetaMutationalSigs' multi-tool output against the cbioportal pipeline's current
  `run_restricted_sigprofiler_assignment.py` (SigProfiler-based) on a shared TCGA study to
  quantify inter-tool variance in practice.
- For hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and, decide whether to run all four tools and require association replication across tools
  as a robustness gate, or to commit to a single tool (Sigflow/SigProfiler recommended by the
  RMSE results) with MetaMutationalSigs as an optional spot-check.
- Consider whether the inter-tool disagreement documented here motivates registering tool choice
  as a pre-analysis decision in the hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and pre-registration materials.
- Related papers to read: Omichessan et al. 2019 (systematic review/comparison of de-novo vs
  refitting tools, cited heavily here); Degasperi et al. 2020 (Signal tool — quadratic
  programming / SA, web-based); Maura et al. 2019 (practical guide for signature analysis in
  haematological malignancies).
