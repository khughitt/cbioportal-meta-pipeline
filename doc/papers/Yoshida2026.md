---
id: "article:Yoshida2026"
type: "article"
title: "Somatic mutations and clonal evolution in normal tissues and cancer development"
status: "active"
ontology_terms: []
datasets: []
source_refs:
  - "cite:Yoshida2026"
related:
  - "topic:clonal-hematopoiesis-contamination"
  - "article:Bolton2020"
  - "article:Martincorena2017"
  - "topic:pan-cancer-mutation-landscape"
  - "topic:mutation-rate-normalization"
created: "2026-04-18"
updated: "2026-04-18"
---

# Somatic mutations and clonal evolution in normal tissues and cancer development

- **Authors:** Kenichi Yoshida
- **Year:** 2026 (published April 8, 2026; submitted 2025)
- **Journal:** Experimental & Molecular Medicine (Nature/Springer)
- **PMID:** 41331092
- **DOI:** 10.1038/s12276-025-01592-0
- **BibTeX key:** Yoshida2026
- **Source:** web search + PubMed metadata + LLM knowledge (full text paywalled; key facts cross-checked via PubMed, related PMC articles, and the author's institutional profile)

## Key Contribution

A solo-authored review by Yoshida (Division of Cancer Evolution, National Cancer Center Research Institute, Tokyo) synthesizing the current state of knowledge on somatic mutation accumulation, clonal selection, and clonal evolution in morphologically normal human tissues across multiple organ types. The central argument is that carcinogenesis is a multi-decade process: driver mutations are often acquired in early life, positively selected clones colonize normal tissue progressively with age, and malignant transformation represents a late exception rather than the rule for most driver-mutant clones. The review also highlights epimutations (non-genomic epigenetic alterations) as an under-explored contributor to clonal expansion without overt genomic driver mutations.

## Methods

This is a narrative review, not a primary research article. Yoshida synthesizes work from multiple large-scale sequencing projects — whole-genome sequencing of single-cell-derived colonies, micro-dissection WGS of tissue units (crypts, glands, bronchial cells), and population-scale cohort studies — spanning at least the following tissues: esophagus, bronchial epithelium, stomach, colon, skin, blood/hematopoietic system, liver, endometrium, mammary glands, bladder, prostate, kidney, and brain. The review draws on duplex sequencing, single-cell culture, and spatial approaches as complementary methodological strategies. [UNVERIFIED: exact section structure and section-level citations not accessible without full text]

## Key Findings

### Somatic mutation accumulation rates

- Normal tissues accumulate somatic mutations at a roughly constant rate of **13–44 single-nucleotide variants per genome per year**, with variation across organ types. [UNVERIFIED: exact per-tissue rates in this review; range sourced from closely related PMC literature that this review likely cites]
- **Gastric epithelium** (from Yoshida's own primary work, 2025 *Nature*): ~28 SNVs per year per gland; by age 60, driver-mutant clones occupy ~8% of the gastric epithelial lining; rate is accelerated by chronic inflammation (H. pylori).
- **Bronchial epithelium**: tobacco smoking substantially increases mutational burden and driver mutation frequency; smoking cessation is followed by replenishment of the epithelium with near-normal clones (Yoshida et al. 2020, *Nature*).
- **Esophageal epithelium**: despite a 10-fold lower mutation rate than sun-exposed skin, positive selection is exceptionally strong; clones bearing mutations in at least 14 cancer-associated genes colonize the majority of the esophagus by middle age.
- **Skin**: UV-driven mutation burden is the highest; ~25% of cells in normal sun-exposed skin carry cancer driver mutations.

### Driver gene differences: normal tissue vs. tumor

A striking theme across tissues is that the driver gene repertoire in positively-selected normal clones is often **discordant** with that of the corresponding tumor type:

| Tissue | Normal epithelium | Corresponding cancer |
|--------|------------------|---------------------|
| Esophagus | NOTCH1 ~66% of clones | NOTCH1 ~15% of tumors |
| Esophagus | TP53 ~30% of clones | TP53 ~95% of tumors |
| Stomach | ARID1A, ARID1B, ARID2, KDM6A, CTNNB1 | Different ranking |

NOTCH1-mutant clones in normal esophageal epithelium appear to competitively suppress early tumor cell expansion — a possible tissue-protective phenotype. The review frames this "antagonistic epistasis" between NOTCH1 and canonical tumor suppressors (TP53, RB1) as evidence that clonal remodeling of normal tissue does not straightforwardly predict malignancy.

### Clonal hematopoiesis (CHIP)

- CH is reviewed as the hematopoietic exemplar of age-related clonal evolution: **DNMT3A, TET2, ASXL1** are the dominant age-driven drivers; DDR-pathway genes (PPM1D, TP53, CHEK2) are enriched by prior cytotoxic therapy and radiation.
- Annual risk of progression to hematologic malignancy in CH carriers: ~**0.5–1.0%** per year. [UNVERIFIED: whether this exact figure appears in Yoshida2026 or is from cited Bolton/Jaiswal literature]
- ~30–60% of older adults harbor clonal expansions; the majority of clones initiated expansion before age 40; only ~22% carry a canonical driver mutation — the remainder are "driver-negative" clones, possibly driven by epimutations or sub-threshold variants.
- CH is **not** discussed solely as a hematology topic: the review contextualizes it alongside epithelial clonal evolution as part of a unified framework for pre-malignant tissue remodeling. [UNVERIFIED: exact framing in text]
- VEXAS syndrome (somatic UBA1 mutations causing systemic autoimmune disease) is cited as an example of non-malignant disease arising from clonal hematopoiesis.

### Epimutations and clonal expansion without genomic drivers

The review explicitly flags epigenetic alterations (DNA methylation changes, chromatin accessibility shifts) — termed "epimutations" — as a likely partial explanation for the large fraction of clonal expansions that carry no recognizable genomic driver. This is presented as a significant open research frontier. [UNVERIFIED: depth of treatment; confirmed by secondary sources and bioengineer.org summary]

### Environmental modulation

- Smoking: increases bronchial and esophageal driver mutation load; cessation reverses clonal composition.
- UV: primary driver of skin mutational burden.
- H. pylori infection + chronic gastric inflammation: accelerates driver mutation prevalence in gastric epithelium (confirmed in Yoshida 2025 *Nature* gastric paper).
- Alcohol: associated with signature mutations in esophageal epithelium.
- Postmenopausal estrogen decline: reduces mammary epithelial mutation rate (~19.5 → ~8.1 SNVs/year); associated with regression of proliferative pre-malignant lesions.
- Prior cytotoxic therapy / radiation: specifically enriches DDR-pathway CH clones (PPM1D, TP53, CHEK2), not age-driven DNMT3A/TET2.

### Natural history and multi-decade timelines

- For breast cancer with der(1;16): average driver mutation acquired at age ~10.6; widespread clone expansion (~62 mm) precedes malignant transformation by decades.
- Carcinogenic process from first driver mutation to overt cancer often spans **several decades**, with the first driver typically acquired in early life or early adulthood.
- Critically, only a tiny fraction of driver-mutant clones progress: <1 in 375,000 driver-mutant colorectal crypts progress to adenoma; <1 in 3 million to carcinoma.

## Relevance

This review is highly relevant to this project across three dimensions:

**1. CH contamination in cross-study aggregation (direct pipeline relevance)**
The treatment of CH as a predictable consequence of age and therapy directly supports the CH-aware stratification already implemented in the pipeline (see `topic:clonal-hematopoiesis-contamination`, `article:Bolton2020`). Yoshida's framework reinforces the mechanistic basis for our matched-normal stratification: unmatched-normal cohorts will inflate mutation rates for DNMT3A, TET2, ASXL1 in older/pretreated populations because these are positively selected normal-tissue clones, not tumor mutations.

**2. Driver gene interpretation — normal-tissue discordance**
The NOTCH1/TP53 esophageal inversion (NOTCH1 high in normal, low in tumor; TP53 reversed) is a direct caution for pipeline outputs: elevated NOTCH1 mutation rates in a cBioPortal esophageal study could partially reflect normal-epithelial clone contamination rather than true tumor biology. This applies to any study where tumor purity is variable or where tissue is difficult to dissect (e.g., endoscopic biopsies).

**3. Age as a confound in cross-cancer comparisons**
The review frames mutation burden and clonal expansion as monotonically age-dependent across all tissue types. In our cross-cancer gene×cancer matrices, cohorts with older median patient age will systematically show higher mutation frequencies — not because the cancer is more mutagenic but because the normal-epithelial background has more clonal remodeling. This intersects with the hypermutator TMB annotation work (t081/t092–t099) and the cohort-selection-bias topic.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Driver-mutant clones in normal epithelium | CH-priority gene contamination | Extends CH concept to epithelial tissues beyond blood |
| Age-driven mutation accumulation | Per-cohort age confound | Relevant to cross-cancer ratio normalization |
| CHIP (DNMT3A/TET2/ASXL1) as age-selected clones | `ch_priority_gene` flag (Bolton 7-gene list) | Yoshida provides mechanistic framing |
| Normal-tissue driver gene ≠ tumor driver gene | CH/normal contamination filter logic | NOTCH1 example: caution for esophageal outputs |
| Therapy-selected DDR-CH (PPM1D/TP53/CHEK2) | Matched vs unmatched normal stratification | Supports per-cancer matched-normal subgroup split |
| Epimutations driving driver-negative clones | Not yet in pipeline | Future annotation dimension |
| Multi-decade carcinogenesis timeline | Somatic mutation background model | Background prior for driver gene recurrence |

## Limitations

- Solo-authored narrative review without systematic search criteria; selection of cited studies may reflect the author's own primary work disproportionately. [UNVERIFIED: no methods section for literature selection]
- Quantitative thresholds discussed (VAF, clone-size cutoffs, mutation rates per tissue) are aggregated from heterogeneous primary studies using different sequencing platforms, calling pipelines, and tissue-preparation methods — cross-tissue comparisons should be interpreted cautiously.
- The review likely does not propose specific filter thresholds for computational pipelines distinguishing normal-tissue clonal mutations from tumor somatic mutations; it describes the biology but the operational translation is left to the reader.
- Epimutation characterization remains largely pre-quantitative; the claim that epimutations explain driver-negative clonal expansion is mechanistically plausible but not yet numerically characterized in most tissue types.

## Model / Tool Availability

Not applicable — this is a review article; no software, datasets, or models are released alongside it.

## Follow-up

- Read Yoshida et al. 2020 (*Nature*) — tobacco smoking and bronchial epithelial mutations — the primary study most directly relevant to lung cancer cohorts in the pipeline.
- Read Yoshida et al. 2025 (*Nature*) — gastric epithelium somatic mutation landscape — directly relevant to stomach cancer studies in cBioPortal.
- Revisit Martincorena 2017 (*Science*) on dN/dS ≈ 1 in normal tissues, which Yoshida's review likely synthesizes.
- Consider: does the normal-tissue driver discordance (NOTCH1 in esophagus) produce detectable signal in our esophageal squamous vs adenocarcinoma frequency outputs? A spot-check comparing NOTCH1 ranks across esophageal study types would test this.
- Track forthcoming quantitative epimutation studies; if tissue-specific epimutation rates become available, they could improve the background-model for driver-negative clonal contamination.
