---
id: "paper:Budczies2024"
type: "paper"
title: "Tumour mutational burden: clinical utility, challenges and emerging improvements"
status: "active"
ontology_terms:
  - tumour mutational burden
  - immune checkpoint inhibitor
  - mutational signatures
  - microsatellite instability
  - neoantigen burden
  - pembrolizumab
  - biomarker
datasets: []
source_refs:
  - "cite:Budczies2024"
related: []
created: "2026-05-31"
updated: "2026-05-31"
---

# Tumour mutational burden: clinical utility, challenges and emerging improvements

- **Authors:** Jan Budczies, Daniel Kazdal, Michael Menzel, Susanne Beck, Klaus Kluck, Christian Altbürger, Constantin Schwab, Michael Allgäuer, Aysel Ahadova, Matthias Kloor, Peter Schirmacher, Solange Peters, Alwin Krämer, Petros Christopoulos, Albrecht Stenzinger
- **Year:** 2024
- **Journal:** Nature Reviews Clinical Oncology
- **DOI/URL:** https://doi.org/10.1038/s41571-024-00932-9
- **BibTeX key:** Budczies2024
- **Source:** PDF

## Key Contribution

This review provides a comprehensive synthesis of tumour mutational burden (TMB) as a predictive biomarker for immune checkpoint inhibitor (ICI) response, covering its theoretical basis, measurement challenges, FDA-approval context (Keynote-158/pembrolizumab), and three principal directions of improvement: (1) quality control in TMB measurement (panel size, tumour purity, bioinformatic variant filtering), (2) conceptual refinements such as clonal TMB (cTMB), persistent TMB (pTMB), expressed TMB (eTMB), HLA-corrected TMB, and tumour neoantigen burden (TNB), and (3) multimodal integration of TMB with PD-L1 expression, MSI status, immune gene expression signatures, and mutational signatures. The authors argue that the 10 mut/Mb cut-off is overly broad for tumour-agnostic use and that combining TMB with complementary biomarkers — especially mutational signatures — is likely necessary to improve ICI patient selection.

## Methods

Narrative review drawing on published clinical trial data (Keynote-158, CheckMate-227, BFAST, CUPISCO, MYSTIC), retrospective cohort analyses, pan-cancer TCGA data re-analysed by the authors, and harmonisation studies from the Friends of Cancer Research / German QuIP TMB initiative. Original analyses: (a) TCGA pan-cancer scatter plots of missense mutation vs indel burden per cancer type and DNA repair subtype (Fig. 2); (b) computer simulations of the effect of tumour purity on TMB detection sensitivity (Fig. 3); (c) pan-TCGA neoantigen burden prediction using four published algorithms (NetMHC 4.0, MHCFlurry 1.2, NetMHCPan 4.1, MHCFlurry 2.0) comparing TMB-high vs TNB-high classification per cancer type (Fig. 5).

## Key Findings

**Clinical context and FDA approval**
- Pembrolizumab received FDA Accelerated Approval in 2020 for TMB-high (≥10 mut/Mb) tumour-agnostic solid tumours based on Keynote-158 single-arm data (ORRs: 6.7%, 12.5%, 37% for TMB <10, 10–13, >13 mut/Mb). The EMA rejected this application.
- Keynote-158 lacked a control arm; randomised trial evidence that ICIs improve survival in unselected TMB-high patients is still lacking for most histologies.
- TMB and PD-L1 expression are largely independent predictors of ICI benefit and do not significantly correlate across most cancer types except MSI-H and POLE-mutated tumours.

**Measurement and confounders**
- Panel size is the dominant source of stochastic variability; panels ≥1 Mb recommended, ≥2 Mb preferred. Panels covering <0.5 Mb (CDS) are substantially less predictive than WES-measured TMB.
- Tumour purity ≥60% is required for reliable TMB measurement; purity <40% causes substantial TMB underestimation (>32% reduction at 20% purity). Sensitivity for detecting high TMB approaches 100% at ≥60% purity.
- Good interlaboratory reproducibility is achievable (Pearson R = 0.97–0.99 for WES across five German centres), but systematic biases from bioinformatic germline filtering remain — particularly ancestry-related SNP database coverage leads to inflated TMB in non-white patients.
- Blood-based (ctDNA) TMB can approximate tissue TMB but concordance is ~50% at the variant level; valid scores obtained in ~81% of patients vs 63% for tissue in MYSTIC.

**Limitations of clinical use**
- Among cancers where TMB is predictive, sensitivity and specificity at 10 mut/Mb remain imperfect; top-20-percentile or cancer-type-specific cut-offs outperform fixed thresholds for several histologies.
- TMB loses predictive value when ICIs are combined with chemotherapy (Keynote-189, Keynote-407, Keynote-21).
- MSI-H tumours that fail to respond to ICIs may reflect B2M or antigen presentation machinery defects; TMB cannot detect these.

**TMB refinements**
- *Clonal TMB (cTMB)*: truncal mutations only; data mixed — outperforms total TMB in MMRd gastric/CRC but not melanoma OS; subclonal TMB separates long-term responders in NSCLC.
- *Persistent TMB (pTMB)*: mutations unlikely to be lost during evolution (single-copy or multicopy regions); outperformed TMB in melanoma, head/neck, mesothelioma, NSCLC in one study.
- *Expressed TMB (eTMB)*: requires WES + WTS; outperformed TMB for OS in melanoma; evidence for independent improvement is mixed.
- *HLA-corrected TMB*: filters mutations non-recognisable by available HLA alleles; improved PFS prediction in NSCLC/melanoma receiving ICIs.

**Tumour neoantigen burden (TNB)**
- Pan-TCGA analysis shows TNB and TMB correlate moderately to strongly (Spearman 0.65–0.79 across four algorithms). Percentage of TMB-high tumours classified as TNB-high varies markedly by cancer type (especially high in MMRd/POLE cancers where frameshift neoantigens dominate).
- Frameshift mutations produce far more immunogenic neoantigens than missense mutations; the ratio of TNB to TMB is substantially higher for frameshift variants regardless of algorithm.
- Applying a pan-cancer TNB cut-off reclassifies substantial proportions of patients relative to TMB; cancer-type-specific TNB cut-offs are needed.

**Mutational signatures and ICI**
- Mutational signatures decompose TMB into aetiology-specific components: POLE/POLD1 (PRD), MMRd (SBS6/15/21/44/ID1/2/7), UV (SBS7/ID13), tobacco smoking (SBS4/ID3), APOBEC (SBS2/13), clock-like/age-related (SBS1/5).
- APOBEC signatures (SBS2/13) associate with higher neoantigen burden and improved sensitivity to anti-PD-1 in NSCLC; further supported by studies with mixed solid tumour cohorts.
- Tobacco smoking signature (SBS4) also associated with improved anti-PD-1 response in NSCLC.
- Clock-like signature SBS5 (high activity in NSCLC) associates with inferior ICI response.
- Mutational signatures associated with dMMR are robust, approved biomarkers of ICI response across solid tumours.
- WGS is optimal for signature extraction; panel-based approaches can only detect highly abundant signatures and introduce substantial stochastic error.

**Combinations with other biomarkers**
- Community challenge (417 models, 59 teams) for NSCLC showed that models combining TMB + PD-L1 + gene expression outperformed TMB + PD-L1 alone.
- CIRCLE algorithm (TMB + BCLAF1/KRAS/BRAF/TP53 mutation status + cancer type) outperformed TMB alone across solid tumours.
- Antigen presentation machinery defects (B2M mutations, JAK1/JAK2 loss) are not captured by TMB and modulate ICI response independently.

## Relevance

This review is directly relevant to hypothesis **h08** (agnostic covariate<->signature-exposure association; positive-control recovery of known aetiologies) and the cbioportal cross-study TMB annotation pipeline:

**For h08 positive controls:** The review consolidates the canonical exposure→signature map that h08 must recover: UV↔SBS7 (melanoma), tobacco smoking↔SBS4 (NSCLC), APOBEC activation↔SBS2/13 (NSCLC), MMRd↔SBS6/15/21 (colon/gastric). Crucially, the review notes that (a) APOBEC signatures associate with *higher* ICI response even within NSCLC, independent of bulk TMB — consistent with the h08 prediction that APOBEC3 expression resolves a mediator that clinical labels alone cannot; and (b) SBS4 (smoking) similarly associates with ICI benefit — confirming that the h08 positive-control arms (UV→SBS7, smoking→SBS4, APOBEC-expr→SBS2/13) have detectable phenotypic correlates this review expects to re-emerge.

**For h08 discovery / immune signatures:** The review raises the explicit question of whether immune-process mutational signatures (immune-mediated hypermutation by AID/APOBEC in B/T cells) can be distinguished from tumour-intrinsic APOBEC signatures — directly relevant to the h08 concern that immune cells contaminate the mutational spectrum. The finding that SBS5 (clock-like) is a negative predictor of ICI response in NSCLC is a novel candidate association warranting h08b investigation.

**For the TMB annotation pipeline (t081–t099):** The review provides quantitative benchmarks for the project's hypermutator annotation plan: the 10 mut/Mb FDA cut-off, the 100 mut/Mb ultra-high threshold (Fig. 1a legend), POLE/POLD1 (PRD) and MMRd as causes of ultra-high TMB, and the tumour-purity simulation data (Fig. 3) that motivate the `purity_min` quality filter. The authors' recommendation of panel size ≥1 Mb (ideally ≥2 Mb) for clinical TMB directly informs the `build_panel_callable_sizes` rule's sensitivity expectations.

**For cross-study meta-analysis:** The review demonstrates that TMB distributions vary substantially across cancer types within TCGA (Fig. 2), and that any fixed pan-cancer cut-off is a compromise. The cbioportal pipeline's per-cancer-type GMM (`fit_per_cancer_tmb_gmm`) and parallel `is_hypermutator_absolute` / `is_hypermutator_relative` flags (Samstein 2019 top-20%) are consistent with the review's own recommendation that higher and cancer-type-specific cut-offs outperform the fixed 10 mut/Mb threshold.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| PRD (proofreading deficiency): SBS10a–d, SBS14, SBS20 | `hypermutator_reason: pole_hotspot / pold1_hotspot` | POLE/POLD1 hotspot detection is first in the composite rule ordering |
| MMRd: SBS6, SBS15, SBS21, SBS44, ID1, ID2, ID7 | `hypermutator_reason: msi_h` | MSI-H annotation from `msi_normalization.py` |
| High TMB (≥10 mut/Mb) | `is_hypermutator_absolute` (Campbell 2017 ≥10 mut/Mb) | Project implements the FDA cut-off |
| Ultra-high TMB (>100 mut/Mb) | `is_hypermutator_ultra` (≥100 mut/Mb) | Separate pipeline flag |
| Per-histology top-20% | `is_hypermutator_relative` (Samstein 2019) | Per-cancer-type relative criterion |
| Per-cancer-type GMM on log10 TMB | `fit_per_cancer_tmb_gmm` | Analogous approach; review supports rationale |
| Tumour purity ≥60% recommendation | `purity_min` config filter | Simulation data (Fig. 3) quantifies sensitivity loss below 40% |
| Panel size ≥1 Mb for TMB | `panel_callable_mb_tolerance` | `build_panel_callable_sizes` rule |
| Mutational signatures as TMB components | `run_restricted_sigprofiler_assignment.py` | Review supports adding sig-layer to cross-study pipeline |
| APOBEC (SBS2/13) ↔ ICI response | h08 positive-control arm | Confirms APOBEC3 expression as mediator variable |

## Limitations

- The review does not provide a systematic meta-analysis; effect sizes for signature↔ICI associations are drawn from heterogeneous studies with varying definitions and cohorts.
- Clinical evidence for TMB refinements (cTMB, pTMB, eTMB, HLA-corrected TMB) is mostly retrospective and single-cohort; head-to-head prospective comparisons are lacking.
- The mutational signature section relies on WGS for reliable decomposition; the authors acknowledge that panel-based approaches can only detect abundant signatures, limiting applicability in the project's panel-sequencing studies.
- The TCGA neoantigen burden analysis (Fig. 5) uses four algorithms producing correlated but non-identical rankings; all four are computational with limited experimental validation of the predicted neoantigens.
- Discussion of mutational signatures as ICI biomarkers focuses primarily on the dominant/established signatures (APOBEC, MMRd, UV, smoking); immune-process signatures (AID/APOBEC in lymphocytes) are not addressed.

## Follow-up

- The review cites Alexandrov 2020 (COSMIC v3 signatures) and Degasperi 2022 (SigProfiler pan-UK) — both already have summaries in this project.
- For h08: this review's Table/Fig. 1a (signature↔TMB-level map) should be used as the reference for which signatures are expected to be detectable in panel-sequenced cBioPortal studies (abundant/dominant only) vs requiring WGS.
- Consider reading: Samstein 2019 (Nat Genet — TMB top-20% per histology, basis for `is_hypermutator_relative`), and the QuIP/Friends of Cancer Research harmonisation papers (refs 39, 40) for panel calibration context.
- The review explicitly flags antigen presentation machinery (B2M, JAK1/JAK2) as covariates not captured by TMB — potentially relevant to h08b discovery if expression module data for these pathways is available in the co-measured RNA studies.
