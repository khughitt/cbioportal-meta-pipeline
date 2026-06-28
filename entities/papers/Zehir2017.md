---
type: paper
title: Mutational landscape of metastatic cancer revealed from prospective clinical
  sequencing of 10,000 patients
status: read
created: '2026-04-13'
updated: '2026-06-28'
id: paper:Zehir2017
ontology_terms: []
source_refs:
- article:Zehir2017
related:
- topic:pan-cancer-mutation-landscape
- topic:targeted-panel-sequencing-bias
- paper:Chakravarty2017
dataset_usage:
- ref: dataset:msk-impact
  role: analyzed
  overlap: full
---

# Mutational landscape of metastatic cancer revealed from prospective clinical sequencing of 10,000 patients

- **Authors:** Zehir A, et al.
- **Year:** 2017
- **Journal:** Nature Medicine
- **PMID:** 28481359
- **BibTeX key:** Zehir2017

## Key Contribution

This MSK-IMPACT cohort note links topic:pan-cancer-mutation-landscape, topic:targeted-panel-sequencing-bias, and paper:Chakravarty2017.

Reports the canonical MSK-IMPACT prospective clinical-sequencing release: 10,945 tumors from
10,336 patients spanning 62 principal tumor types and >300 detailed subtypes, sequenced as part
of routine clinical care for advanced/metastatic disease. Establishes that 36.7% of patients
harbor at least one OncoKB-actionable somatic alteration and demonstrates that paired
tumor-normal targeted sequencing at scale can both define the metastatic mutational landscape
and route patients onto genotype-matched trials (11% enrolled within the early subset).

## Methods

MSK-IMPACT is a hybridization-capture targeted panel of cancer-associated genes deployed as a
CLIA assay. Two versions were used in this cohort: IMPACT-341 (2,809 tumors, 26%) and the
expanded IMPACT-410 (8,136 tumors, 74%), with all 341 genes retained in the larger panel; a
later IMPACT-468 version is referenced as ongoing. The panel covers all protein-coding exons of
the targeted genes plus the TERT promoter and select introns of 17 recurrently rearranged genes
for fusion detection. Every tumor is processed prospectively from FFPE or frozen tissue with
automated DNA extraction, library prep, capture, and 2x100-bp Illumina HiSeq2500 sequencing to
~718x mean unique coverage; median turnaround was <21 days. Critically, 98% of cases were
sequenced with patient-matched normal peripheral-blood DNA (buffy coat) at deep coverage,
allowing somatic calls to be made directly against the patient's own germline and dramatically
reducing both rare-germline and clonal-hematopoiesis contamination. The pipeline uses BWA-MEM,
ABRA realignment, GATK BQSR, MuTect (SNVs), Pindel and SomaticIndelDetector (indels), DELLY
(structural variants), and an in-house CNV caller, followed by manual review. All variants are
classified against OncoKB therapeutic levels (1, 2A/2B, 3A/3B, 4) for clinical reporting.

## Key Findings

- **Actionability:** 36.7% of patients (n=3,792) carried at least one OncoKB-actionable
  alteration, with the highest rates in GIST (76%), thyroid (60%), breast (57%), and melanoma
  (56%). Within an early 5,009-patient subset, 11% (527 patients) were enrolled on at least one
  of 197 genotype-matched trials.
- **Pan-cancer drivers:** TP53 was altered in 41% of all samples (98% in HGSOC, 89% esophageal
  adenocarcinoma, 85% small-cell lung; >10% in 43/62 principal tumor types), and KRAS in 15%
  (90% pancreatic, 44% colon; G12 codon = 80% of KRAS hits). PIK3CA codons 1047 and 545 plus BRAF V600
  recurred across >20 tumor types each.
- **Advanced-disease enrichment:** AR mutations occurred in 18% of metastatic prostate (vs 1% in
  TCGA) and ESR1 in 11% of metastatic breast (vs 4% in TCGA), almost exclusively in
  hormone-pretreated tumors - quantifying the metastatic/treatment-resistance bias of the cohort
  versus primary-tumor TCGA.
- **Novel associations:** 33 BRAF fusions across 11 tumor types with 18 partners (10 novel,
  including recurrent CDK5RAP2-BRAF); 7 in-frame BRAF intragenic deletions; ALK/RET/ROS1
  fusions in 11 cancer types beyond lung (268 kinase fusions total = 35% of rearrangements);
  10 additional recurrent TERT-promoter sites beyond -124/-146.
- **TMB / MSI / signatures:** 994 cases (9%) were hypermutated (threshold 13.8 mut/Mb); panel
  TMB correlated R^2=0.76 with matched WES. 102 patients across 11 tumor types had a dominant
  MMR signature plus MSIsensor-positive calls; 45% of these had not previously been MMR-tested,
  and immunotherapy responses were observed in colorectal, endometrial, gastric, prostate, and
  bladder MSI cases. Dominant signatures matched expected etiology: UV (Sig 7) in melanoma,
  smoking (Sig 4) in lung, temozolomide (Sig 11) in pretreated glioma, POLE (Sig 10) in
  colorectal/endometrial, and MMR (Sigs 6/15/20/26).

## Relevance

Establishes the MSK-IMPACT panel content and prospective-sequencing design that defines the "MSK"
studies in cBioPortal. The gene content of IMPACT (341 -> 410 -> 468) is the dominant panel-bias
driver in the pipeline's cross-study mutation-frequency estimates, and the matched-buffy-coat
design means MSK-IMPACT mutation calls are unusually clean of germline and CH artifacts compared
to unmatched panel datasets - relevant when comparing per-gene cancer frequencies across studies.
The cohort is also explicitly biased toward advanced/metastatic, often heavily pretreated disease,
which inflates the apparent frequency of resistance-associated alterations (AR, ESR1, TP53)
relative to primary-tumor cohorts like TCGA.

## Limitations

- **Advanced-disease selection bias:** the cohort is enriched for metastatic, often
  multiply-pretreated patients referred to a tertiary cancer center, inflating frequencies of
  resistance drivers (AR, ESR1) and TP53 versus primary-tumor cohorts.
- **Single-institution referral pattern:** Memorial Sloan Kettering catchment skews tumor-type
  mix and demographic representation; trial-enrollment rate (11%) is bounded by trials available
  on-site and geographical access.
- **Panel coverage:** ~341-410 cancer genes only - whole-exome/genome alterations outside the
  panel (including many DDR, chromatin, and signature-shaping passenger sites) are invisible,
  and certain mutational-signature analyses are limited compared to WES.
- **MSI/TMB undercounting:** signature-based MSI calling was restricted to the highest-TMB tail,
  likely undercounting MSI prevalence; TMB threshold (13.8 mut/Mb) was cohort-derived.
- **Specimen heterogeneity:** mix of FFPE and frozen tissue from internal and outside hospitals
  produced variable quality (3% excluded for low tumor content, 6% low DNA yield, 5% post-seq QC).
- **Cohort heterogeneity:** 62 principal tumor types with very uneven sample sizes - rare
  subtypes have limited power for novel-association discovery.

## Follow-up

- Bandlamudi2026 - 50k-scale follow-up.
- Nguyen2022 - MSK-MET metastatic extension.
- Chakravarty2017 - OncoKB precision-oncology knowledge base used for actionability tiering here.
- Cheng2015 - original MSK-IMPACT 341-gene analytical-validation paper.
