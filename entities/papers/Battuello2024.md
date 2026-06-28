---
type: paper
title: Mutational signatures of colorectal cancers according to distinct computational
  workflows
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Battuello2024
ontology_terms: []
datasets: []
source_refs:
- cite:Battuello2024
related: []
---

# Mutational signatures of colorectal cancers according to distinct computational workflows

- **Authors:** Paolo Battuello, Giorgio Corti, Alice Bartolini, Annalisa Lorenzato, Alberto Sogari, Mariangela Russo, Federica Di Nicolantonio, Alberto Bardelli, Giovanni Crisafulli
- **Year:** 2024
- **Journal:** Briefings in Bioinformatics, 25(4), bbae249
- **DOI/URL:** https://doi.org/10.1093/bib/bbae249
- **BibTeX key:** Battuello2024
- **Source:** PDF

## Key Contribution

Arbitrary choices in the mutational signature analysis pipeline — NGS workflow (WGS vs. WES vs. targeted panel), fitting algorithm, and COSMIC reference catalogue version — produce statistically different signature exposures in the same samples. Using colorectal cancer (CRC) as a model system (230 cell lines + 152 patients, validated in three independent cohorts), the authors quantify how each variable shifts both mathematical goodness-of-fit and biological utility for stratifying MSI-MMRd vs. MSS-MMRp and POLE-mutant tumours. They also release CoMSCER, an open-source R/Shiny bioinformatics tool that runs multiple algorithms and references in parallel to help researchers identify the most appropriate workflow, and they establish minimum somatic variant thresholds required for reliable signature assignment [@Battuello2024].

## Methods

**Datasets:**
- Preclinical: 230 CRC cell lines (WES, WGS, and TSO-500 targeted panel on the same samples; MSS-MMRp 145/230, MSI-MMRd 78/230, POLE-mutant 7/230).
- Clinical: 152 TCGA-COAD patients (downloaded from GDC).
- Validation: TCGA-UCEC (483 endometrial cancer, MMR-stratified), TCGA-LUAD/LUSC (35 lung cancer, smoking-stratified), 12 CRC patient-derived organoids (PDOs) treated with colibactin-producing E. coli.

**NGS workflow comparison:** TSO-500 pan-cancer targeted gene panel (523 genes, in silico from WGS), WES, and WGS applied to the same samples; mutational matrices generated with SigProfilerMatrixGenerator v1.1.31 [@Battuello2024].

**Algorithm comparison:** Systematic PMC literature review (831 entries → 70 with available installable tools); top 5 most referenced: MutationalPatterns (MP), deconstructSigs (DS), signature.tools.lib (STL), SigProfilerAssignment (SPA), SignatureAnalyzer (SA). All run with standard/author-recommended settings [@Battuello2024].

**Reference catalogue comparison:** COSMIC v2 (30 SBS signatures), COSMIC v3.2 (79 SBS signatures), and a CRC tissue-specific (TS) reference.

**Readouts:**
- Mathematical: cosine similarity between original and reconstructed mutational profiles (threshold 0.9).
- Biological: ΔMMR (median difference in MMR-deficiency signature contribution between MSI-MMRd and MSS-MMRp) and ΔPOLE (median difference in POLE-associated signature contribution between POLE-mutant and wild-type).

**Minimum mutation threshold:** Random sampling (5–95% of mutations per sample, 19 subgroups) to derive the minimum number of somatic variants for reliable cosine similarity [@Battuello2024].

**Genomic region analysis:** Mutational signatures decomposed separately for exonic, intronic, and extragenic regions from WGS.

**Metanormal:** Constructed from 21 peripheral blood mononuclear cells (PBMCs) of CRC patients to assess germline and artefact filtering.

**CoMSCER tool:** Freely available at https://github.com/pbattuello/CoMSCER; integrates multiple tools and references, supports coding vs. extragenic region comparison, and metanormal-based artefact filtering.

## Key Findings

**NGS workflow:**
- All three data types (WGS, WES, TSO-500) achieve cosine similarity ≥ 0.9 (mathematical reliability), but differences across workflows are statistically significant (Wilcoxon, p < 2.2e-16) [@Battuello2024].
- Biological utility (ΔMMR) is significantly positive with all three workflows, supporting MSI-MMRd vs. MSS-MMRp stratification. However, ΔMMR is unexpectedly lower with WGS (0.11 WGS < 0.26 WES < 0.32 TSO-500).
- The WGS deficit is explained by dilution from "flat signatures" (SBS 3-5-8-40-89, uniformly distributed across trinucleotide contexts) enriched in intronic and extragenic regions (flat-signature contribution: ~0% exonic, ~12% intronic, ~36% extragenic in MSI-MMRd lines).
- Clinical implication: large pan-cancer targeted panels like TSO-500 are feasible for CRC subtype stratification and may outperform WGS for this task.

**Algorithm choice:**
- 4 of 5 tools (MP, DS, STL, SPA) achieve median cosine similarity ≥ 0.9 in the preclinical dataset; SignatureAnalyzer (SA) fails for 94.3% of samples (217/230 not assigned).
- SPA provides highest ΔMMR (median 0.67 vs. MP 0.34, DS 0.28, STL 0.31, SA 0.28) and highest ΔPOLE across algorithms, making it the best discriminator of biologically relevant CRC subtypes.
- MP is the best overall choice for CRC cell lines balancing mathematical and biological performance.
- Tool choice can leave >30% of samples unassigned and shifts individual MMR signature contributions substantially (e.g., SBS6 contribution: 46% in C2, 13% in C3, 24% in TS with SPA; 9% in C2, 19% in C3, 25% in TS with SA).

**Reference catalogue:**
- Larger catalogues (COSMIC v3.2, 79 signatures) yield higher cosine similarity but worsen biological stratification compared to smaller catalogues (COSMIC v2 or tissue-specific), because individual disease-relevant signatures are diluted.
- All three references support significant ΔMMR and ΔPOLE stratification; COSMIC v2 or TS references recommended when investigating MMR- or POLE-specific biology.
- Individual MMR signature contributions (SBS6, SBS15, SBS20, SBS21, SBS26, SBS44) vary substantially across reference catalogues.

**Minimum mutation threshold:**
- CRC cell lines: ≥ 323 mutations required to reach cosine similarity ≥ 0.9.
- Clinical dataset (matched normal): ≥ 64 mutations (threshold substantially lower with matched normal control).
- With metanormal, threshold drops from 323 to 145 mutations in cell lines, confirming metanormal utility.
- Artefact-associated SBS contributions drop from ~0.30 to ~0.15 with metanormal vs. hg38 reference (p < 0.0001).

**Validation:**
- Findings replicated in endometrial cancer (TCGA-UCEC), lung cancer (smoking status), and CRC PDOs (colibactin), confirming generalisability beyond CRC.

## Relevance

This paper is directly relevant to hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and (agnostic covariate ↔ signature-exposure association; positive-control recovery of biologically meaningful signatures). Key connections:

1. **Positive-control recovery:** The paper operationalises exactly the kind of positive-control test that hypothesis:0007 envisions — it asks whether known biological covariates (MMR status, POLE mutation, smoking, colibactin) are recoverable from fitted signature exposures, and shows that the answer depends strongly on pipeline choices. This provides a concrete benchmark design for hypothesis:0007 validation experiments.

2. **Pipeline standardisation for cross-study meta-analysis:** The cbioportal pipeline aggregates somatic mutations across heterogeneous cBioPortal studies that differ in sequencing platform (WGS, WES, targeted panels) and calling workflows. The finding that NGS workflow choice produces statistically different signature exposures — even when cosine similarity is similar — is a direct warning about cross-study signature comparisons without workflow harmonisation.

3. **Algorithm and reference choice:** The dramatic spread in SBS6/SBS15/SBS26 contributions across reference catalogues and algorithms (e.g., SBS6 ranging 5–46%) is relevant when interpreting the cbioportal meta-analysis outputs for MMR-related signatures. MutationalPatterns (MP) emerges as a reasonable default for coding-region data.

4. **Targeted panel feasibility:** The result that TSO-500 (a 523-gene panel) can reliably stratify MMR and POLE subtypes — often better than WGS — implies that the heterogeneous panel-sequenced studies in cBioPortal are not necessarily worse for signature inference than WES/WGS studies, provided mutation counts are adequate.

5. **Minimum mutation count:** The ≥ 64–323 mutation threshold (depending on matched-normal availability) provides a concrete filter for excluding low-mutation-burden samples from signature analysis in the cross-study pipeline.

6. **Flat signatures / extragenic dilution:** The finding that intronic and extragenic regions inflate "flat signature" contributions in WGS data suggests the cbioportal pipeline (which operates on coding-region calls from cBioPortal MAFs) is partially protected from this confound; this is a useful note for interpreting pan-cancer signature results.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| ΔMMR (biological readout) | Positive-control signature recovery | hypothesis:0007 validation metric |
| ΔPOLE (biological readout) | Positive-control signature recovery | POLE as a known hypermutator aetiology |
| NGS workflow (WGS/WES/panel) | Study-level sequencing heterogeneity | Relevant to cross-study aggregation in cbioportal |
| Reference catalogue (COSMIC v2/v3/TS) | Signature reference choice | Affects pooled meta-analysis results |
| Minimum mutation threshold | Sample-level TMB filter | Links to t081/t092–t099 hypermutator pipeline |
| Flat signatures (extragenic dilution) | Confounding signatures | Less problematic for coding-region MAFs |
| CoMSCER tool | Potential benchmarking resource | GitHub: pbattuello/CoMSCER |
| Metanormal | Matched-normal proxy | Relevant to CH contamination / artefact filtering |

## Limitations

- Study focuses on five algorithms selected by PubMed citation frequency as of July 2023; >30 tools exist. SignatureAnalyzer (SA, Bayesian NMF) performs poorly here but may be superior in other contexts.
- CRC is a well-characterised model; generalisability to cancer types with fewer known molecular subtypes is assumed but not fully demonstrated.
- The TSO-500 data were generated in silico from WGS, not independently sequenced; real-world TSO-500 library prep introduces additional technical variation not captured here.
- Metanormal constructed from 21 PBMCs may not represent all germline backgrounds; the method was validated only in the CRC cell line context.
- COSMIC catalogues are version-locked to mid-2023; v3.3+ signatures (released later) are not evaluated.
- The study does not assess de novo signature extraction workflows (e.g., NMF-based discovery) — only refitting against known catalogues.
- Cross-study heterogeneity (different tumour purities, sequencing depths, variant callers) is not directly modelled; this is a major concern for the cbioportal meta-analysis use case.

## Model / Tool Availability

- **CoMSCER** (COmparative Mutational Signature analysis on Coding and Extragenic Regions): https://github.com/pbattuello/CoMSCER
  - R/Shiny tool; freely available, open source.
  - Supports multiple algorithms (MP, DS, STL, SPA, SA) and reference datasets (COSMIC v2, v3.2, tissue-specific).
  - Evaluates coding vs. intronic vs. extragenic region signature contributions.
  - Includes metanormal filtering for artefact reduction.
- All data and code: https://github.com/pbattuello/MutationalSignatures
- NGS data deposited in ENA under accessions PRJEB33045, PRJEB33640, PRJEB57691, PRJEB61897.

## Follow-up

- Evaluate whether the cbioportal cross-study pipeline should apply a minimum mutation-count filter before signature fitting (threshold: 64–323 depending on normal matching).
- Test whether MutationalPatterns with COSMIC v2 or a pan-cancer tissue-specific reference improves positive-control signature recovery in the cross-study meta-analysis.
- Examine CoMSCER as a benchmarking tool to compare signature outputs across the heterogeneous sequencing platforms present in cBioPortal studies.
- Consider whether the ΔMMR / ΔPOLE framework could serve as a hypothesis:0007 positive-control metric: if fitted exposures in MMR-deficient tumours do not elevate MMR-associated signatures, the pipeline is miscalibrated.
- Read: Alexandrov et al. 2020 (Nature, SBS repertoire); Maura et al. 2019 (Nat Commun, practical guide for haematological malignancies); Blokzijl et al. 2018 (Genome Biol, MutationalPatterns); Rosenthal et al. 2016 (Genome Biol, deconstructSigs).
