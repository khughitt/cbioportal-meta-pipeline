---
type: paper
title: Somatic mutations and clonal evolution in normal tissues and cancer development
status: active
created: '2026-04-18'
updated: '2026-04-18'
id: paper:Yoshida2026
ontology_terms: []
source_refs:
- paper:Yoshida2026
related:
- topic:clonal-hematopoiesis-contamination
- paper:Bolton2020
- paper:Martincorena2017
- topic:pan-cancer-mutation-landscape
- topic:mutation-rate-normalization
---

<!-- 2026-04-18: revised against full-text PDF; prior unresolved verification markers cleared, per-tissue mutation rates now sourced from Table 1, several secondary-source numbers corrected or removed. -->


# Somatic mutations and clonal evolution in normal tissues and cancer development

- **Authors:** Kenichi Yoshida
- **Year:** 2026 (published April 8, 2026; submitted 2025)
- **Journal:** Experimental & Molecular Medicine (Nature/Springer)
- **PMID:** 41331092
- **DOI:** 10.1038/s12276-025-01592-0
- **BibTeX key:** Yoshida2026
- **Source:** full-text PDF (verified 2026-04-18) + PubMed metadata. Initial draft built from web search / LLM knowledge while paywalled, subsequently verified and corrected against the full text.

## Key Contribution

A solo-authored review by Yoshida (Division of Cancer Evolution, National Cancer Center Research Institute, Tokyo) synthesizing the current state of knowledge on somatic mutation accumulation, clonal selection, and clonal evolution in morphologically normal human tissues across multiple organ types. The central argument is that carcinogenesis is a multi-decade process: driver mutations are often acquired in early life, positively selected clones colonize normal tissue progressively with age, and malignant transformation represents a late exception rather than the rule for most driver-mutant clones. The review also highlights epimutations (non-genomic epigenetic alterations) as an under-explored contributor to clonal expansion without overt genomic driver mutations.

## Methods

This is a narrative review, not a primary research article. Yoshida synthesizes work across three experimental paradigms explicitly introduced in the review's "Experimental techniques" section (Fig. 1):

1. **Laser-capture microdissection + WGS** on 100–1000 cells — enables spatial analysis but suffers polyclonality when clones are small.
2. **Single-cell-derived organoids / colonies** — enables single-cell genetic analysis but loses spatial context and is hard to establish for some organs.
3. **Duplex / nanorate sequencing (NanoSeq)** — distinguishes true mutations from sequencing errors (<5×10⁻⁹ errors per bp) without clonal expansion; usable for non-dividing cells (muscle, nervous system).

Tissues covered: blood, bladder, breast, bronchus, colon, endometrium, esophagus, heart, liver, muscle, neuron, prostate, small intestine, stomach (Table 1 of the paper).

## Key Findings

### Somatic mutation accumulation rates (Table 1 of the paper)

Per-tissue SBSs per year accumulated in normal cells:

| Tissue | SBSs/year | Clonal expansion frequency | Freq. driver genes (normal) |
|---|---|---|---|
| Blood (HSC) | 14.2–17 | High | DNMT3A, TET2, −Y |
| Blood (B lymphocyte) | 15–17 | Low | — |
| Blood (T lymphocyte) | 22–25 | Low | — |
| Breast | 19.5 | High | PIK3CA, der(1;16), +1q, del(16q) |
| Bronchus | 22 | High | NOTCH1, FAT1, TP53 |
| Colon | 43.6 | Low | — |
| Endometrium | 29 | High | PIK3CA, ARHGAP35, PIK3R1 |
| Esophagus | 41.5 | High | NOTCH1, TP53, FAT1 |
| Heart | 19 | Low | — |
| Liver | 33 | Low | — |
| Muscle | 20.7 | Low | — |
| Neuron | 17.1 | Low | — |
| Prostate | 16 | Low | — |
| Small intestine | 42–51 | Low | — |
| Stomach | 28 | High | ARID1A, CTNNB1, KDM6A |

Notable modulators reported in the text:

- **Breast**: 19.5 SNVs/year before menopause, **decreasing to 8.1/year after menopause**; a single pregnancy leads to a reduction of 54.8 mutations — attributed to reduced cell division and declined estrogen following menstrual cycle cessation.
- **Esophagus**: NOTCH1 mutations are acquired **as early as infancy**; clones with NOTCH1/TP53 drivers are larger than those without driver mutations.
- **Skin**: acquired NOTCH1 mutations found in **~20% of skin cells**; clones with driver mutations larger than clones without.
- **Intestinal crypts in polymerase-proofreading polyposis**: ~7-fold more SBSs in *POLE* germline carriers and up to 3-fold higher in *POLD1* carriers than in normals.
- **Colon**: clonal expansion is **rare (~1% driver-mutant frequency)** because the colon is composed of crypts, each derived from a single stem cell; acquired drivers rarely expand because they disrupt crypt structure.
- **Liver / prostate**: clonal expansion frequency of acquired driver mutations is low (<5% liver; prostate stem cells are physically separated).
- **BRCA1/2 normal breast**: aneuploidy frequency 3.63–3.65% vs. 2.45% in mutation-negative cases.

### Driver gene differences: normal tissue vs. tumor

Yoshida explicitly identifies a set of driver mutations that occur **frequently in normal tissues but relatively infrequently in cancer**, and vice versa:

- **High in normal, lower in cancer**: NOTCH1 in skin, esophagus, and bronchial tissues. In a mouse model, *Notch1*-mutant clones in normal esophageal epithelium **inhibited the proliferation of cancer cells**, suggesting a tumorigenesis-suppressive role.
- **Higher in cancer than normal**: TP53 across tissues, FGFR3 in bladder, PTEN in endometrium.

This normal-vs-cancer asymmetry is framed as evidence that clonal remodeling of normal tissue does not straightforwardly predict malignancy. (Specific quantitative normal-vs-cancer frequency ratios — e.g., "NOTCH1 ~66% of normal esophageal clones vs. ~15% of tumors" — are not stated in this review text; those figures belong to the cited primary literature such as Martincorena 2018 [@Martincorena2018] / Yokoyama 2019.)

### Clonal hematopoiesis (CHIP)

- In the intro, ~**0.7–1%** nonrandom X-inactivation ratios in healthy females and **mCAs in 6–9% of healthy individuals** establish the baseline prevalence of age-related clonal abnormalities in blood.
- Primary CH drivers named: **TET2, DNMT3A, ASXL1** (→ clonal hematopoiesis, associated with age-related diseases including cardiovascular and cerebrovascular disease, and — conversely — decreased risk of Alzheimer disease).
- Annual progression risk: "It is estimated that **0.5–1%** of individuals with detectable clonal hematopoiesis develop hematologic malignancies each year" (verbatim).
- Clone initiation timing: MPN analysis (JAK2 V617F) shows the **average time from the initial driver mutation to MPN onset is ~30 years**, implying several decades for a second driver mutation.
- Gene-specific progression: mutations in RNA splicing factors (*U2AF1*, *SRSF2*, *SF3B1*) are mainly observed in older adults with MDS and have higher progression risk. DNMT3A and TET2 occur at younger ages and have comparatively lower leukemia progression risk.
- **TCL1A promoter SNP** (rs2887399) suppresses expansion of *TET2*- and *ASXL1*-driven CH — a germline-by-somatic interaction mechanism.
- Aplastic-anemia / inflammation-driven CH: CN-LOH of chromosome 6p (HLA region) in aplastic anemia and NFKBIZ / TRAF3IP3 / ZC3H12A selection in ulcerative colitis are cited as **tissue-context-specific** driver repertoires that differ from age-related CH.

### Epimutations and clonal expansion without genomic drivers

The review flags epimutations (epigenetic alterations) in a single Summary-section paragraph: "changes in the epigenome (epimutations) in normal tissues, which represent one of the nongenomic abnormalities involved, require further clarification. Although the understanding of epi-mutations in normal cells is limited, these changes may partly explain the clonal evolution driven by abnormalities other than those in the genome." The treatment is high-level rather than quantitative — Yoshida flags this as an open research frontier, not a characterized phenomenon.

### Environmental modulation (Table 2 of the paper)

Comprehensive signature-to-cause mapping (Table 2):

- **Tobacco smoking**: SBS4 (lung, liver), SBS16 (esophagus, liver, lung), Sig-B (bronchus, ~nitrosamine), Sig-A (bladder, ~nitrosamine), SBS92 (bladder). Smoking cessation is followed by near-normal-clone epithelial replenishment in bronchi. *H. pylori* + germline *BRCA1/2* increases gastric cancer risk.
- **Alcohol**: SBS16 in esophageal epithelium; **faster accumulation in carriers of inactive ALDH2 (rs671)** (acetaldehyde metabolism).
- **UV**: SBS7(a/b/c/d); skin cancer incidence varies by ethnicity, with higher frequencies in Western populations. SBS7 also identified in ALL and normal B/T lymphocytes — suggesting the signature can be acquired via UV exposure while cells are in the skin.
- **Chemotherapy/antivirals**: SBS11 (temozolomide), SBS17 (5-FU, capecitabine), SBS25 (procarbazine), SBS31 (platinum), SBS32 (azathioprine), SBS35 (platinum), SBS99 (melphalan), SBS90 (duocarmycin), and a **ganciclovir-induced C>A signature**.
- **E. coli pks+ colibactin**: SBS88 in normal colorectal crypts — a potential colorectal cancer risk factor.
- **Aristolochic acid**: SBS22(a/b) in hepatocytes and normal bladder epithelial cells.
- **Ionizing radiation**: no characteristic SBS signature; causes ID-A (indel signature with microhomology), resembling IE8/NHEJ pattern. Also produces complex structural abnormalities (chromoplexy, chromothripsis).
- **Prior cytotoxic therapy**: enriches DDR-pathway CH clones (in general), consistent with therapy-related mutagenesis signatures above.

### Natural history and multi-decade timelines

- **Breast cancer with der(1;16)**: acquired "during early puberty to late adolescence, [followed by] over 10 years for the development of breast cancer through the acquisition of further driver mutations." Multiple independent cancer lesions arose from a common noncancerous der(1;16) clone — demonstrating departure from the single-founder model.
- **Endometrium**: *KRAS* and *PIK3CA* mutations commonly acquired during childhood, **before age ~10 years**.
- **Breast copy-number alterations**: der(1;16), +1q, del(16q) occur from early puberty to late adolescence.
- **Carcinogenesis as a decades-long process**: fetal-origin or early-life driver acquisition is consistent with MPN phylogenetic data (JAK2 V617F acquired in fetal state, MPN onset ~30 years later) and with the 10+ year breast cancer timeline.
- **Colon crypt structure protects against clonal expansion**: driver mutations occur but rarely expand because expansion disrupts the crypt.

## Relevance

This review is highly relevant to this project across three dimensions:

**1. CH contamination in cross-study aggregation (direct pipeline relevance)**
The treatment of CH as a predictable consequence of age and therapy directly supports the CH-aware stratification already implemented in the pipeline (see `topic:clonal-hematopoiesis-contamination`, `paper:Bolton2020`). Yoshida's framework reinforces the mechanistic basis for our matched-normal stratification: unmatched-normal cohorts will inflate mutation rates for DNMT3A, TET2, ASXL1 in older/pretreated populations because these are positively selected normal-tissue clones, not tumor mutations.

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

- Solo-authored narrative review without a systematic literature-search methods section; selection of cited studies reflects the author's own primary work (bronchial smoking 2020; gastric 2025) prominently.
- Quantitative per-tissue rates in Table 1 are aggregated from heterogeneous primary studies using different sequencing platforms (LCM-WGS, organoid WGS, duplex/NanoSeq) and tissue-preparation methods — cross-tissue comparisons should be interpreted cautiously.
- The review does **not** propose specific filter thresholds for computational pipelines distinguishing normal-tissue clonal mutations from tumor somatic mutations; it describes the biology but leaves the operational translation to the reader.
- Epimutation characterization is treated briefly (one paragraph); the claim that epimutations explain driver-negative clonal expansion is mechanistically plausible but not yet numerically characterized.
- Detailed primary-study VAF cutoffs, clone-size distributions, and dN/dS statistics are not recapitulated here — consult the cited Martincorena / Yokoyama / Coorens / Moore primary papers for those.

## Model / Tool Availability

Not applicable — this is a review article; no software, datasets, or models are released alongside it.

## Follow-up

- Read Yoshida et al. 2020 (*Nature*) — tobacco smoking and bronchial epithelial mutations — the primary study most directly relevant to lung cancer cohorts in the pipeline.
- Read Yoshida et al. 2025 (*Nature*) — gastric epithelium somatic mutation landscape — directly relevant to stomach cancer studies in cBioPortal.
- Revisit Martincorena 2017 [@Martincorena2017] (*Science*) on dN/dS ≈ 1 in normal tissues, which Yoshida's review likely synthesizes.
- Consider: does the normal-tissue driver discordance (NOTCH1 in esophagus) produce detectable signal in our esophageal squamous vs adenocarcinoma frequency outputs? A spot-check comparing NOTCH1 ranks across esophageal study types would test this.
- Track forthcoming quantitative epimutation studies; if tissue-specific epimutation rates become available, they could improve the background-model for driver-negative clonal contamination.
