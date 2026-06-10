---
type: paper
title: Joint inference of mutational signatures from indels and single-nucleotide
  substitutions reveals prognostic impact of DNA repair deficiencies
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:FerrerTorres2025
ontology_terms:
- mutational signatures
- homologous recombination deficiency
- indels
- NMF
- prognostic biomarker
- ovarian cancer
- mismatch repair deficiency
datasets: []
source_refs:
- cite:FerrerTorres2025
related: []
---

# Joint inference of mutational signatures from indels and single-nucleotide substitutions reveals prognostic impact of DNA repair deficiencies

- **Authors:** Patricia Ferrer-Torres, Iván Galván-Femenía, Fran Supek
- **Year:** 2025
- **Journal:** Genome Medicine
- **DOI/URL:** https://doi.org/10.1186/s13073-025-01497-7
- **BibTeX key:** FerrerTorres2025
- **Source:** PDF

## Key Contribution

Jointly extracting mutational signatures from single-base substitution (SBS) and indel (ID) spectra using a concatenated NMF approach ("multimodal" SBS+ID) resolves the notoriously featureless COSMIC SBS3 signature into two biologically distinct sub-signatures — m-SBS3a (linked preferentially to BRCA1 deficiency, containing an ID8-like indel component) and m-SBS3b (linked to both BRCA1 and BRCA2 deficiency, containing an ID6-like microhomology-mediated deletion component). Multimodal m-SBS3b is a significantly stronger and more robust predictor of overall survival in high-grade serous ovarian cancer (HGSOC) than the standard SBS3 signature, replicating across four independent cohorts and outperforming all tested HR-deficiency classifiers (CHORD, HRDetect, GIS). The same multimodal strategy, applied to mismatch repair deficiency (MMRd) signatures in colorectal cancer, improves survival prediction and immunotherapy response prediction (AUC 0.789 vs 0.730 for SBS-only).

## Methods

**Signature extraction.** SigProfiler MatrixGenerator was used to derive SBS96 and ID83 mutation count matrices from WGS VCF files. These were concatenated into a 179-channel SBS+ID matrix and submitted to SigProfiler Extractor for NMF-based de novo signature extraction. The number of signatures k was selected by mean sample cosine distance and stability. Extracted multimodal signatures were matched to COSMIC v3.3 by decomposing the SBS and ID portions separately using SigProfiler Assignment.

**Cohorts.** Four independent HGSOC whole-genome-sequenced cohorts were used as primary discovery/validation: DECIDER (n=100), PCAWG ovarian (n=110, OV-AU and OV-US), Hartwig (n=124, metastatic), and OVCARE (n=52). Pan-HGSOC analysis pooled all 386 samples. Non-ovarian validation used Hartwig TN breast (n=78), prostate (n=165), and pancreatic (n=384) cancer samples. Colorectal cancer analyses used Hartwig (n=737, metastatic) and Uppsala University (n=1063, primary) cohorts.

**Survival analysis.** Signature exposures were binarized at multiple percentile thresholds (20th–80th). Kaplan–Meier curves and Cox proportional hazards regression (adjusting for age, stage, cohort, and co-extracted signatures via multivariate model) were used; concordance index (C-index) reported. PFS was also assessed where available (DECIDER, PCAWG, OVCARE).

**HR status annotation.** BRCA1/BRCA2 germline and somatic variants were annotated per cohort. Kruskal–Wallis + Wilcoxon rank-sum tests (Bonferroni-corrected) assessed signature activity differences across BRCA1-deficient, BRCA2-deficient, other HR gene-deficient, and HR-proficient groups.

**Refitting validation.** Both SigProfiler Assignment and MuSiCal refitting were tested as alternatives to de novo extraction to confirm practical applicability of multimodal signatures in new samples without re-running NMF.

**Replication timing (RT) aware analysis.** Mutations were split into early-RT and late-RT bins (from Repli-seq data), yielding 358-channel RT-aware matrices. This RT stratification was explored as an additional dimension to improve extraction, particularly for separating SBS3-related signatures.

**Comparison to existing HRd classifiers.** Multimodal signatures were benchmarked against CHORD (n=182 overlapping), HRDetect (n=68), CN Signature 3 (n=40), and GIS/MyChoice CDx (n=108) using C-index from Cox regressions.

## Key Findings

1. **Two mechanistically distinct SBS3 sub-signatures.** The multimodal approach robustly extracted m-SBS3a (ID8-rich; primarily BRCA1-linked; ratio of median exposures BRCA1-deficient vs HR-proficient = 6.3) and m-SBS3b (ID6-rich microhomology deletions; linked to both BRCA1 and BRCA2; ratio BRCA2-deficient vs HR-proficient = 7.6). Standard SBS-only s-SBS3 had a combined ratio of 3.87 for BRCA1/BRCA2.

2. **Superior survival prediction.** In the pan-HGSOC cohort (n=386), m-SBS3b-positive patients had a median overall survival of 31.2 months vs 27.7 months for the negative group (p=1.55e−07). The best multimodal m-SBS3b C-index was 0.648; the standard s-SBS3 consistently trailed. In all four individual cohorts, m-SBS3ab (the combined refitting signature) showed significant survival associations (best Z-scores ranging from −2.83 to −3.33 across cohorts).

3. **Outperforms established HRd classifiers.** De novo and refitted m-SBS3b outperformed CHORD, GIS, HRDetect, and CN Signature 3 in C-index comparisons on overlapping samples.

4. **SBS39 and SBS8 not HRd.** SBS39 and the co-confused SBS8 showed no consistent positive link to BRCA1/BRCA2 deficiency or to longer survival in the same analyses, supporting the multimodal approach's ability to unmix these from true HRd signatures. SBS39 was significantly associated with *shorter* survival in platinum-treated patients (p<0.05), suggesting it may reflect a non-HRd or artifact process.

5. **Pan-cancer applicability.** Multimodal m-SBS3ab was significantly associated with longer overall survival in TN breast cancer (Z=−2.78, p=0.005 platinum-treated) and showed trends in prostate and pancreatic cancer (specifically in platinum-treated patients), consistent with HRd predicting response to platinum.

6. **MMRd in colorectal cancer.** Multimodal SBS+ID extraction improved prediction of overall survival (the multimodal m-SBS44+ID7 was the only MMRd-related signature significantly associated with better survival in multivariate Cox; standard SBS signatures were not). Immunotherapy response (PR/SD vs PD in Hartwig) was better predicted by multimodal MMRd signatures (AUC=0.789) than SBS-only (AUC=0.730) or ID-only (AUC=0.710).

7. **Refitting is sufficient for clinical use.** MuSiCal refitting onto the de novo multimodal catalog recapitulated strong survival associations for both m-SBS3a (p=0.0197) and m-SBS3b (p=4.42e−06), with median survival differences of 13.9 and 23.7 months respectively. This enables applying the approach to new samples without full de novo NMF.

8. **RT-aware extraction.** Incorporating replication timing bins (192-channel or 358-channel matrices) improved extraction of m-SBS3a and m-SBS3b in some cohorts, especially when indels were sparse or in smaller cohorts, but did not substantially change results for the primary pan-HGSOC analysis.

## Relevance

**Direct relevance to h08 (agnostic covariate-to-signature association; positive-control recovery).**

- **Positive-control recovery (H08a):** This paper shows that the HRd-associated SBS3 signature can be substantially refined by multimodal extraction, yielding sub-signatures with cleaner links to BRCA1 and BRCA2 genotypes. For the h08 positive-control design (recovering UV/smoking/APOBEC/MMR links agnostically), the corollary is that SBS+ID joint inference may be necessary to recover clean HRd↔BRCA associations — a SBS-only agnostic scan on this project's mutation tables would likely conflate m-SBS3a, m-SBS3b, SBS5, SBS8, SBS39, and SBS40 into a messy factor. This is directly relevant to q018 (feasibility of downstream signature extraction on the cBioPortal aggregated cohort): if the pipeline only captures SBS, clinically important HRd sub-signatures will be inaccessible.

- **Modality gap.** The current cbioportal pipeline ingests somatic SNV/indel calls but the cross-study aggregation (`gene_cancer_study.feather`) operates at gene-mutation level, not at trinucleotide-context mutation-count level required for SBS+ID NMF. Running multimodal signature extraction would require per-sample SBS96+ID83 mutation count matrices, which exist only for WGS/WES studies in cBioPortal — not panel studies.

- **SBS39 / confounding signatures.** The paper provides strong evidence that SBS39 is *not* an HRd signature and is confounded with SBS3 in unimodal analyses. This directly informs the h08 positive-control design: any association of an SBS39-like factor with BRCA1/BRCA2 annotations should be treated as a confounding artifact rather than a true HRd link.

- **MMRd positive control (H08a arm 3).** The colorectal cancer MMRd analysis demonstrates that multimodal m-SBS44+ID7 is more cleanly associated with MMRd than standard SBS signatures. For the H08a MMR-loss/MSI↔SBS6/15/26 positive-control arm, indel information (ID signatures) may need to be incorporated to achieve reliable recovery in practice.

- **Refitting vs de novo.** The demonstration that MuSiCal refitting onto a pre-built multimodal catalog achieves comparable results to de novo extraction is practically important for the h08 implementation, where per-study sample sizes may be too small for de novo NMF but refitting onto a reference catalog is feasible.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| SBS+ID joint NMF (multimodal) | Potential extension to cross-study sig. extraction | Current pipeline does not do per-sample SBS96+ID83; would require a new rule |
| m-SBS3a / m-SBS3b sub-signatures | HRd signature sub-types | Relevant when evaluating BRCA1/BRCA2-linked studies in cBioPortal |
| Refitting with MuSiCal or SigProfiler Assignment | `run_restricted_sigprofiler_assignment.py` | Current restricted assignment is SBS-only; extending to ID83 is feasible |
| HRd classifier benchmark (CHORD, GIS, HRDetect) | Comparison benchmark for h08 positive-control | Provides expected effect sizes for BRCA1/BRCA2-linked signatures |
| SBS39 as confounded / non-HRd | Artifact/confound signatures (SBS27/43/45–60 list) | SBS39 should be treated cautiously in HRd-association analyses |
| Per-sample signature exposures as survival predictors | Signature exposure as covariate in h08 association scan | Direct methodological parallel |

## Limitations

- **WGS only.** The multimodal SBS+ID approach requires whole-genome sequencing; it does not apply to panel or WES data where indel calls are sparse. Most cBioPortal studies are panel-based, limiting direct translation.
- **HGSOC focus.** Primary validation is in four HGSOC cohorts; pan-cancer applicability is demonstrated in only three non-ovarian types (breast, prostate, pancreas from a single Hartwig cohort) and one colorectal analysis.
- **Small cohorts for individual-cohort analyses.** Individual HGSOC cohorts (n=52–124) were too small to separate m-SBS3a from m-SBS3b in de novo extraction; combined m-SBS3ab was used, losing sub-signature distinction.
- **HR status annotation heterogeneity.** BRCA1/BRCA2 germline/somatic annotation methods differed across cohorts (VEP annotations vs clinical metadata), introducing potential misclassification noise in the HR-association analyses.
- **Confounders not fully explored.** Platinum treatment (known to generate SBS31/35) and prior therapies could modulate signature activities and survival associations beyond what the Cox covariates (age, stage, cohort) capture.
- **SBS3 mechanistic origin remains unclear.** Despite improved HRd stratification, the paper does not fully resolve whether m-SBS3b mutations arise from translesion synthesis, alternative NHEJ, or other downstream processes; the mechanistic interpretation remains partially speculative.
- **MMRd analysis is preliminary.** Colorectal MMRd findings are based on two cohorts; the immunotherapy response analysis is restricted to patients in the Hartwig cohort who received immunotherapy, and sample sizes for subgroup analyses are small.

## Model / Tool Availability

- Code for multimodal (SBS+ID) signature extraction is available at: https://github.com/patriciaferrer/multimodal_mut_signs_SBSID (reference [80] in paper)
- SigProfiler tools (MatrixGenerator, Extractor, Assignment) used; COSMIC v3.3 reference signatures used for matching
- MuSiCal refitting tool used for assignment validation
- No pre-trained model weights released; the approach is a pipeline modification (concatenation of matrices before existing NMF tools)

## Follow-up

- **For h08:** Evaluate whether the cbioportal pipeline could incorporate SBS+ID joint extraction for WGS/WES studies, at minimum for the tcga_mc3 unified MAF which has matched-normal calling and would yield clean indel calls.
- **For h08 positive-control design:** Consider incorporating ID6/ID8 indel signatures alongside SBS2/13 (APOBEC) and SBS4 (smoking) arms — this paper demonstrates their value for HRd recovery.
- **Tool evaluation:** Test MuSiCal refitting onto a pan-cancer multimodal SBS+ID catalog as a complement to the current `run_restricted_sigprofiler_assignment.py` (SBS-only restricted assignment).
- Papers to read: Sorensen et al. 2023 (pan-cancer MMRd signatures, cited as [72]) for the MMRd arm of H08a; Levaticet al. 2022 (Nature Communications, cited as [12]) on mutational signatures as drug-sensitivity markers in cell lines.
