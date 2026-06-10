---
type: paper
title: Reconstructing the lifelong history of cells and tissues via somatic mutation
  analysis
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Faienza2025
ontology_terms: []
datasets: []
source_refs:
- cite:Faienza2025
related: []
---

# Reconstructing the lifelong history of cells and tissues via somatic mutation analysis

- **Authors:** Sipontina Faienza, Jean Piero Margaria, Irene Franco
- **Year:** 2025
- **Journal:** Cellular and Molecular Life Sciences
- **DOI/URL:** https://doi.org/10.1007/s00018-025-05946-9
- **BibTeX key:** Faienza2025
- **Source:** PDF

## Key Contribution

This review argues that somatic mutations — non-reversible, cumulative records embedded in each cell's genome — constitute a uniquely powerful window into the lifelong history of cells and tissues, distinct from and complementary to transcriptomic or proteomic snapshots. The authors survey how somatic variants are exploited as natural barcodes for lineage tracing, clonal dynamics monitoring, mutagen exposure assessment, microbial infection detection, tissue-of-origin classification, and DNA-repair system characterisation. The review positions mutational signature analysis as a maturing experimental tool for physiology and aging biology, not just cancer genomics.

## Methods

This is a narrative review. The authors survey the literature across five thematic areas:

1. **Somatic variants as natural barcodes** — phylogenetic reconstruction of embryonic development and lineage tracing via shared SNVs across tissues.
2. **Clonal composition assessment** — hematopoietic clonal dynamics (including clonal haematopoiesis, VEXAS, and post-transplant evolution) and solid-tissue clonal expansion in liver, esophagus, and brain.
3. **Mutagen exposure tracking** — tobacco (SBS4), chemotherapy drugs (cisplatin footprint), dietary factors (red meat / colonic KRAS/PI3K mutation), aristolochic acid (SBS22), and bacterial toxins (colibactin from *pks*+ *E. coli*; SBS88).
4. **Tissue-of-origin / cell-residency inference** — UV signature (SBS7a) in circulating memory T cells as proof of skin residency; colibactin signature in metastases to infer primary site.
5. **DNA-repair system activity** — CRISPR knock-out of DNA-repair genes in organoids / cell lines to map specific signatures to enzymatic components; "mutational phenotypes" defined by composite SBS + indel + structural variant patterns; familial cancer predisposition contexts.

No original data analysis is presented; the review synthesises published findings primarily from WGS of single cells and bulk tissue biopsies.

## Key Findings

- **Somatic mutations accumulate at 10–80 SNVs and 1–10 indels per genome per year** across normal tissues; the rate and spectrum are tissue-specific.
- **Embryonic lineage reconstruction** using SNVs showed the first two cells of the embryo contribute asymmetrically to adult tissues, and cell fate specification in the brain is established as early as the 9th–17th cell division.
- **Clonal diversity in the blood declines after age 70**, with clones expanding to generate >30% of blood-forming progenitors; this loss of diversity corresponds to ~12 years of physiological aging when observed after haematopoietic transplantation.
- **Tobacco SBS4** is dose-dependent, tissue-specific (lung), and non-reversible — it persists in former smokers' genomes decades after cessation. SBS4 exemplifies the general properties of all mutational signatures.
- **Chemotherapy footprints (cisplatin)** are detectable in normal blood, colon, and liver stem cells of cancer survivors, and in de novo germline variants in children born from treated fathers, underscoring off-target mutagenicity.
- **Colibactin (SBS88)**, from *pks*+ *E. coli*, is found in 12% of colon cancers; cancer patients carrying this signature have earlier cancer onset and its geographic prevalence correlates with colorectal cancer incidence.
- **UV signature SBS7a in circulating memory T cells** (which cannot be UV-exposed directly) proves their skin residency, illustrating how mutational signatures can establish tissue-of-origin of migrating cells.
- **Mutational phenotypes** — composite signatures including SBS, indels, and structural variants — can identify novel DNA-repair defects, including mTOR signalling as an unexpected regulator of mismatch repair fidelity and TP53/RB loss causing chromatin reorganisation that elevates mutation burden.
- **The COSMIC SBS classification** (96-trinucleotide class framework) and COSMIC catalogue are positioned as the primary reference for signature cataloguing; COSMIC numbers (SBS4, SBS7a, SBS17, SBS22, SBS88, etc.) are used throughout.

## Relevance

**Hypothesis h08** (agnostic covariate–signature-exposure association; positive-control recovery of UV/smoking/APOBEC/MMR): This review is directly relevant as a conceptual anchor. It articulates why the known aetiology of canonical signatures (UV→SBS7a, tobacco→SBS4, MMR defects→SBS6/15/20/26, aristolochic acid→SBS22) can serve as ground-truth positive controls for any agnostic association pipeline. The review explicitly lists the properties a validated signature must have: tissue-specificity of the exposed tissue, dose-dependence, and non-reversibility. These criteria translate directly into testable expectations for h08: a covariate such as tobacco exposure should recover SBS4 preferentially in lung, scaled by pack-year equivalents.

**Cross-study meta-analysis (cbioportal pipeline)**: The paper underscores that bulk tumour WGS/WES data from cBioPortal studies is the dominant data source for signature discovery in cancer. The review of mutational phenotypes (composite SBS+indel+CNA patterns) is relevant to understanding confounders in cross-study aggregation: samples with MMR deficiency or POLE/POLD1 mutations will show hypermutator phenotypes that need to be stratified (aligning with the pipeline's `is_hypermutator` annotation layer and the t081 plan). The colibactin and chemotherapy signature findings highlight that somatic mutation rate in cBioPortal studies can be elevated by prior treatment or infection, which is a confound for frequency-ranking analysis.

The review's framing that somatic mutations are "non-reversible, cumulative" while transcriptomics is "snapshot" data is useful background justification for why somatic mutation frequency tables (the pipeline's primary output) carry integrative information about lifetime exposures rather than current cellular state.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| COSMIC SBS catalogue | Canonical signature reference | Pipeline uses COSMIC SBS numbers via Bailey 2018 driver overlay and CH annotation |
| Mutational signature tissue-specificity | Cross-cancer mutation frequency matrix | Tissue-of-origin patterns visible in gene x cancer tables |
| Hypermutator / high-TMB phenotypes | `is_hypermutator` annotation (t081) | Review confirms POLE/POLD1 and MMR defects as major hypermutator sources |
| Clonal haematopoiesis | CH-aware annotation (`ch_priority_gene`) | Bolton 2020 gene list captures DNMT3A, TET2, ASXL1, etc. mentioned in review |
| Prior chemotherapy (cisplatin) as mutagen | Treatment-related signal in cBioPortal studies | A confound in cross-study mutation frequency comparisons |
| Colibactin / SBS88 in colon cancer | Not currently tracked | Could be relevant if stratifying GI cancers by infection exposure |

## Limitations

- **No original data or quantitative analysis** — the review's claims rest on the cited primary literature; individual studies have heterogeneous sample sizes and sequencing depths.
- **Coverage is selective** — the review focuses on illustrative examples; it does not attempt a systematic or exhaustive survey of all published normal-tissue somatic mutation studies.
- **APOBEC signatures (SBS2/13) are absent** — the review does not cover APOBEC mutagenesis, a major endogenous mutational process and important positive-control candidate for h08.
- **SBS-centric** — indels and structural variants are mentioned in the context of DNA-repair phenotypes but are not covered as systematically as SBS.
- **Tissue culture / organoid generalizability** — several mechanistic claims about DNA-repair signatures derive from in vitro CRISPR screens whose translation to primary tissue is noted by the authors themselves as uncertain.
- **Clinical applications are aspirational** — the review presents cisplatin germline mutagenicity and tissue-of-origin inference as proof-of-concept; clinical adoption is not yet established.

## Model / Tool Availability

No new computational tools or models are released with this review. References are made to:
- **COSMIC** catalogue (https://cancer.sanger.ac.uk/signatures) — public, continuously updated
- **MOSAICS** platform for in vivo CRISPR fitness screens in mouse liver [ref 51 in paper]
- **GO-TEN** (Genotyping Of Transcriptomes Enhanced with Nanopore sequencing) for cell-type-informed mosaic variant genotyping [ref 9 / Bizzotto 2025]

## Follow-up

- **Boysen2025** (already in doc/papers/) — covers origins of mutational signatures, complementary mechanistic depth.
- **LeeSix2018** (already in doc/papers/) — the colibactin landscape paper is reviewed here as a primary source.
- **Koh2021** (already in doc/papers/) — COSMIC signature clinical applications review cited extensively.
- Consider reading Senkin 2024 (ref 71) on geographic variation of mutagenic exposures in kidney cancers, which is directly relevant to h08 covariate-geographic variables.
- Consider reading Vali-Pour 2022 (ref 105) on rare germline variants and somatic mutation phenotypes, relevant to familial cancer predisposition contexts in the pipeline.
- The Mutograph project (ref 69, Perdomo 2024) — correlating regional cancer incidence with mutational signature data epidemiologically — is a real-world implementation of h08-style covariate association at population scale.
