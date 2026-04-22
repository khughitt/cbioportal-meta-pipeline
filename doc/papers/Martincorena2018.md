---
id: "paper:Martincorena2018"
type: "paper"
title: "Somatic mutant clones colonize the human esophagus with age"
status: "active"
ontology_terms: []
datasets: []
source_refs:
  - "paper:Martincorena2018"
related:
  - "paper:Yoshida2026"
  - "paper:Poon2021"
  - "paper:Li2021"
  - "paper:Gao2023"
  - "topic:clonal-hematopoiesis-contamination"
  - "topic:pan-cancer-mutation-landscape"
  - "question:q001-normal-epithelial-clone-contamination-in-esophageal-studies"
created: "2026-04-18"
updated: "2026-04-18"
---

# Somatic mutant clones colonize the human esophagus with age

- **Authors:** Inigo Martincorena, Joanna C. Fowler, Agnieszka Wabik, Andrew R. J. Lawson, Federico Abascal, Michael W. J. Hall, Alex Cagan, Kasumi Murai, Krishnaa Mahbubani, Michael R. Stratton, Rebecca C. Fitzgerald, Penny A. Handford, Peter J. Campbell, Kourosh Saeb-Parsy, Philip H. Jones
- **Year:** 2018
- **Journal:** Science, vol. 362, issue 6417
- **DOI:** 10.1126/science.aau3879
- **PMCID:** PMC6298579
- **BibTeX key:** Martincorena2018
- **Source:** Full text via PMC (PMC6298579), confirmed OA copy; all quantitative values extracted directly from PMC full text. Metadata confirmed via Crossref/Unpaywall. No paywalled content needed.

## Key Contribution

Martincorena et al. (Wellcome Sanger Institute / MRC Laboratory, Cambridge) present the founding primary-data study on age-related somatic clone colonization of normal human esophageal epithelium. Using deep targeted sequencing of 74 cancer genes across 844 contiguous 2 mm² biopsy samples from nine organ donors aged 20–75 years, they show that normal esophageal epithelium accumulates hundreds to thousands of somatic mutations per cell with age, and that 14 cancer genes — led by NOTCH1 and TP53 — are under strong positive selection. By middle age, NOTCH1-mutant clones cover 30–80% of the esophageal epithelium; TP53-mutant clones cover 5–37%. Critically, NOTCH1 mutation prevalence in normal esophagus is several-fold *higher* than in esophageal squamous cell carcinoma (ESCC), while TP53 shows the opposite pattern — establishing the central "NOTCH1 paradox" that defines the normal-tissue-vs-cancer driver inversion framework.

## Methods

### Cohort

- **Donors:** 9 deceased organ transplant donors (no known esophageal disease or chronic disease history).
- **Age range:** 20–75 years.
- **Smoking status:** 4 of 9 donors had a history of cigarette smoking; 2 were heavy smokers.
- **Anatomical sampling:** Upper and mid-esophageal epithelium dissected into contiguous ~2 mm² grid samples. Total tissue area sequenced: ~17 cm². Biopsies were taken across the full epithelial surface, not from endoscopically identified lesions.

### Sequencing

- **Panel:** 74 cancer genes selected for known roles in esophageal or other squamous cancers. Panel includes NOTCH1, NOTCH2, NOTCH3, TP53, FAT1, CCND1, PIK3CA, TP63, NFE2L2, ARID1A, ARID2, KMT2D, CUL3, AJUBA, and others.
- **Depth:** Median on-target coverage 870× after duplicate removal.
- **Total samples:** 844 biopsy samples; 21 samples with large clones subsequently received whole-genome sequencing (37× median).
- **Variant calling:** ShearwaterML algorithm, designed for detecting low-allele-frequency somatic variants in a panel sequencing context (fits a beta-binomial model to control overdispersion from sequencing artifacts).
- **Median VAF of detected mutations:** 1.6%; one-third of mutations were below 1% allele frequency.

### Clone-size estimation

Clone boundaries were inferred from contiguous samples sharing the same variant at similar allele frequencies. The spatial extent of a clone was defined as the contiguous patch of samples in which a given mutation was detectable. Detectable clone sizes ranged from 0.01 mm² (smallest detectable, limited by sample grid resolution) to >8.5 mm². For phylogenetic analysis of large clones, WGS data were used to reconstruct subclonal structure and branching histories. NOTCH1 copy-neutral loss of heterozygosity (CN-LOH) was detected by statistical phasing of heterozygous SNPs.

### Selection quantification

dN/dS analysis via dNdScv (Martincorena 2017, Cell) was applied to all detected somatic mutations. The tool estimates gene-level selection coefficients as dN/dS ratios using a negative-binomial regression framework that corrects for gene length and trinucleotide mutation rates.

## Key Findings

### Mutation burden per cell with age

- Normal esophageal cells accumulate at least several hundred somatic mutations per cell in individuals in their twenties, rising to over 2,000 mutations per cell by late life.
- Linear regression of mutation count versus donor age: P = 0.0068, R² = 0.67.
- Mutation burden is significantly higher in the two heavy smokers than expected for their age.

### Mutational processes

- Dominant signatures are COSMIC Sig 1 (CpG deamination, age-related) and Sig 5 (broad aging-related), consistent with intrinsic mutational processes.
- A transcription-strand asymmetric T>C component (strongly resembling COSMIC Sig 16) is also present — associated with transcription-coupled repair.
- **No evidence of COSMIC Sig 2 or Sig 13 (APOBEC)** in normal esophagus, despite APOBEC signatures being frequent in ESCC. This absence is a key distinction between normal tissue and cancer.
- C>A/G>T changes present at a considerable rate with modest transcription-strand bias.

### Positive selection: 14 driver genes

dNdScv analysis identified 14 genes under significant positive selection in normal esophageal epithelium:

**NOTCH1, TP53, NOTCH2, FAT1, NOTCH3, ARID1A, KMT2D, CUL3, AJUBA, PIK3CA, ARID2, TP63, NFE2L2, CCND1**

**Selection coefficients (dN/dS ratios):**

| Gene / Mutation class | dN/dS |
|---|---|
| Global missense (all genes) | ~2.2 |
| Global protein-truncating (all genes) | ~8.6 |
| NOTCH1 truncating mutations | >50 |
| TP53 missense mutations | ~50 |
| TP53 truncating mutations | ~150 |

The very high truncating dN/dS for NOTCH1 (>50) indicates near-neutral background for truncating mutations across the panel, but an extreme >50-fold excess in NOTCH1 — confirming it as the most strongly selected gene. TP53 missense dN/dS of ~50 is also exceptionally high for a missense category.

### Driver mutation density across the epithelium

- Total positively selected driver mutations estimated in the ~17 cm² of sequenced normal esophageal epithelium: **3,915 (95% CI: 3,829–3,988)**.
- NOTCH1 accounts for ~48% of all driver mutations; 52% of drivers are in genes other than NOTCH1.
- NOTCH1 mutation density: approximately **120 different mutations per cm²**.
- TP53 mutation density: approximately **35 mutations per cm²**.

### Clone sizes and coverage by age

**NOTCH1:**
- Young donors (<40 years): 1–6% of esophageal epithelium covered by NOTCH1-mutant clones.
- Middle-aged and elderly donors (5 of 6 donors 40+): 30–80% of epithelium covered.
- Average across all 9 donors: 25–42% of cells carry a NOTCH1 mutation.

**TP53:**
- Overall prevalence: ~5–10% of epithelium across donors.
- Oldest donor (72–75 years): 20–37% of cells carry a TP53 mutation.

**Clone size distribution:**
- Detectable clones ranged from 0.01 mm² to >8.5 mm², with the largest clone spanning 6 contiguous biopsy samples in the oldest donor.
- Clone size increases significantly with age: mixed-effects regression P = 0.027.
- The oldest donor's largest TP53-mutant clone exhibited a complex phylogenetic history: a founder TP53 mutation expanded first, then three separate subclones each acquired a second TP53 mutation (bi-allelic TP53 inactivation), consistent with the hypothesis that TP53 biallelic loss precedes malignant transformation.

### Multi-driver clones and LOH

- NOTCH1 LOH (copy-neutral loss of heterozygosity) was detected in ~30% of samples; nearly all samples with a high-frequency NOTCH1 single-nucleotide mutation also showed NOTCH1 LOH — confirming that bi-allelic NOTCH1 inactivation is the selective endpoint.
- 14 of 25 large-clone samples showed NOTCH1 bi-allelic inactivation.
- Common driver combinations: NOTCH1+FAT1, NOTCH1+NOTCH3, PIK3CA+NOTCH3.
- Chromosome 3 gains (duplicating PIK3CA/SOX2/TP63) were detected in approximately half of WGS samples.

### NOTCH1 paradox: normal vs. cancer

A key unexpected finding is the inversion of NOTCH1 frequency between normal esophagus and ESCC:

- **Normal esophagus (middle-aged individuals):** NOTCH1 mutated in ~30–80% of the epithelium.
- **ESCC tumors:** NOTCH1 mutated in approximately ~10% of tumors (published ESCC cohort rates vary ~5–15%).

This means NOTCH1 mutations are several times more prevalent in the normal tissue from which ESCC arises than in the cancers themselves. The paper discusses two possible explanations: (1) NOTCH1-mutant clones do not efficiently progress to cancer (perhaps because NOTCH1 loss provides a fitness advantage in normal epithelium but is neutral or disadvantageous in malignant cells); or (2) cancers arising from NOTCH1-mutant clones are selectively lost or dedifferentiated such that NOTCH1 status is masked. Either interpretation implies NOTCH1 mutations in an esophageal cancer cohort may partly represent normal-tissue contamination or post-selection loss rather than tumor driver biology.

### TP53 contrast

TP53 shows the inverse pattern:
- TP53 is mutated in over **90% of ESCCs** but in only a **minority of cells** in normal esophageal epithelium.
- Cancers with TP53 mutations likely arise from the small TP53-mutant clone fraction, with TP53 inactivation representing a late-stage transition step (possibly via LOH) that enables malignant transformation.

### Normal esophagus vs. ESCC — key differences

| Feature | Normal esophagus | ESCC |
|---|---|---|
| Somatic mutation burden | Several hundred to ~2,000 SNVs/cell | ~10-fold higher than normal |
| APOBEC signatures (SBS2/13) | Absent | Present |
| Chromosomal instability | Largely absent | Prominent |
| Average driver mutations/cell | Low (1–2 per clone) | Higher |
| NOTCH1 mutation frequency | 30–80% of cells (middle-aged) | ~10% of tumors |
| TP53 mutation frequency | 5–37% of cells | >90% of tumors |

## Relevance

This paper is the primary empirical foundation for the q001 esophageal contamination concern and for multiple claims in the normal-tissue synthesis. It is directly relevant to the cbioportal project across four dimensions:

**1. Direct source for q001: NOTCH1 contamination risk in esophageal cBioPortal studies**

The quantitative finding that NOTCH1-mutant clones cover 30–80% of the normal esophageal epithelium by middle age — and that this is *higher* than the ~10% NOTCH1 rate in ESCC tumors — means that any cBioPortal esophageal study with imperfect tumor purity (endoscopic biopsies, variable dissection quality) will have NOTCH1 mutation rates inflated by normal-clone contamination. This sharpens `question:q001` with specific numbers: if a biopsy is 30% contaminated by normal cells, and 30–80% of those normal cells carry NOTCH1 mutations, the contamination contribution to apparent NOTCH1 frequency could be on the order of 10–24 percentage points. The pipeline's cross-study gene×cancer outputs for esophageal studies may therefore overestimate NOTCH1 as a driver while underestimating its cancer-specificity.

**2. Empirical backbone for the NOTCH1 inversion used in Yoshida2026, Poon2021, Li2021**

Yoshida2026 cites this study for the NOTCH1 normal-vs-cancer inversion. Poon2021 uses the 9-donor dataset from this paper as their esophageal data source (~600 synonymous variants from these 844 samples). Li2021's qualitative claim that esophagus/cardia harbor macroscopic driver clones is mechanistically grounded in this study. All three downstream summaries in the project can now be cross-referenced to primary numbers here.

**3. dNdScv as the selection quantification method**

The dNdScv algorithm used here is the Martincorena 2017 (Cell) method, which is also implemented in our pipeline's optional `run_dndscv.R` rule. The dN/dS values (NOTCH1 truncating >50; TP53 missense ~50; TP53 truncating ~150) represent strong empirical benchmarks for expected selection coefficients in normal esophageal tissue. These can be compared against dN/dS values the pipeline computes for esophageal cancer cohorts.

**4. Mutation burden calibration for the aging background model**

The finding that normal esophageal cells accumulate several hundred to 2,000 mutations per cell with age (linear with age, R² = 0.67) establishes an empirical aging clock for the esophageal normal-tissue background. This supports the hypothesis (from Li2021 and Yoshida2026) that older esophageal cancer cohorts will carry higher apparent mutation burdens partly from the normal-tissue background — relevant to the TMB annotation work (t081/t092–t099).

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| NOTCH1 30–80% in normal epithelium, ~10% in ESCC | Normal-clone contamination in esophageal studies | Direct quantitative grounding for `question:q001` |
| TP53 inversion (5–37% normal vs >90% ESCC) | Cancer-specific driver identification | TP53 remains a true ESCC driver; NOTCH1 does not |
| 14 positively selected driver genes | Normal-tissue driver gene set | Extends beyond CH-priority list to solid-tissue drivers |
| dN/dS via dNdScv | `run_dndscv.R` rule | Same tool; benchmarks available from this study |
| NOTCH1 truncating dN/dS >50 | Selection strength reference | Strongest known epithelial selection coefficient |
| Mutation rate ~hundreds to 2,000/cell with age | Aging background floor | Somatic SBS1/SBS5 accumulation in esophageal tissue |
| ShearwaterML at 870× depth | Deep targeted-panel clone detection | Ultra-deep panel necessary for sub-1% VAF clones |
| No APOBEC in normal esophagus | Signature contamination risk stratifier | APOBEC signal in esophageal study = tumor-specific, not normal-tissue |
| Clone size 0.01–8.5 mm², increases with age | Contamination magnitude vs. donor age | Larger clones in older donors → higher VAF → survive tumor-calling filters |

## Limitations

- **Very small cohort (N = 9 donors).** The per-individual dN/dS and clone-coverage estimates carry substantial uncertainty. One donor (likely the oldest) dominates the TP53 statistics; NOTCH1 coverage of 30–80% is the interdonor range, not a precise population estimate.
- **Focused on upper/mid-esophagus only.** The study does not cover esophago-gastric junction or lower esophageal adenocarcinoma precursor tissue; conclusions apply to squamous epithelium and ESCC, not EAC.
- **74-gene panel sequencing, not WGS.** The study cannot characterize mutations outside the 74-gene panel; non-panel driver genes (and genome-wide selection outside these genes) are invisible. This is explicitly acknowledged as the basis for the Poon2021 synonymous-passenger complement.
- **Clone-size lower bound limited by 2 mm² grid resolution.** Clones smaller than ~0.01 mm² are undetectable; the true number of small driver-mutant clones is underestimated.
- **Absence of matched cancer comparisons within donors.** The normal/cancer frequency comparison relies on published ESCC cohort rates rather than patient-matched normal-tumor pairs from the same individuals, introducing uncertainty from cohort differences.
- **The NOTCH1 paradox is mechanistically unresolved.** The paper describes the inversion but does not demonstrate *why* NOTCH1-mutant clones do not efficiently progress to ESCC. Subsequent work (Yokoyama 2019; mouse models cited in Yoshida2026) suggests NOTCH1 loss may actually *suppress* adjacent cancer-cell proliferation, but this remains an active research question.
- **Four smoking donors** — smoking status complicates interpretation of mutation burden age-dependence even with statistical adjustment.

## Model / Tool Availability

- **dNdScv:** R package implementing the dN/dS selection-coefficient method used in this paper. Available: `https://github.com/im3sanger/dndscv`. Our pipeline already implements this via `code/scripts/run_dndscv.R`.
- **ShearwaterML:** Part of the deepSNV/shearwater Bioconductor package, used for ultra-deep panel variant calling. Available on Bioconductor.
- **Data:** Sequencing data deposited to EGA (European Genome-phenome Archive); accession not specified in the PMC text. The Cambridge University OA repository copy is at https://doi.org/10.17863/cam.31457.
- No standalone software package for clone-size inference is described in this paper.

## Follow-up

- **Read Yokoyama et al. 2019 (Science)** — independent study of somatic clone colonization in esophagus; complements this study and resolves some of the mechanistic questions about NOTCH1's non-oncogenic role. Cited in Yoshida2026 and q001.
- **Update `question:q001`** — the specific numbers from this paper (30–80% NOTCH1 coverage in normal, ~10% in ESCC; TP53 5–37% normal vs >90% ESCC) sharpen the contamination concern substantially. The question should now include these quantitative bounds.
- **Check dNdScv pipeline output** for esophageal studies in cBioPortal: if any run has been done, compare NOTCH1 dN/dS there against the >50 benchmark for normal tissue. A cancer-tissue dN/dS much lower than 50 would confirm that the selection signal in tumors comes primarily from a different (smaller) selected clone subpopulation.
- **Synthesis update:** Add Martincorena2018 to `synthesis-2026-04-18-somatic-mutations-in-normal-tissue.md` as the primary data reference behind claims currently attributed to secondary sources.
- **Consider:** does the ~17 cm² sampling of 9 donors constitute a sufficient power base for the selection coefficients? The Poon2021 re-analysis of these data using the synonymous-passenger framework independently confirms NOTCH1 and TP53 selection, which provides orthogonal validation.
