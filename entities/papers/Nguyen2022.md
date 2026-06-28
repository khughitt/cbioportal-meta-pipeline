---
type: paper
title: Genomic characterization of metastatic patterns from prospective clinical sequencing
  of 25,000 patients
status: read
created: '2026-04-13'
updated: '2026-06-28'
id: paper:Nguyen2022
ontology_terms: []
source_refs:
- article:Nguyen2022
- cite:Nguyen2022
related:
- paper:Zehir2017
- topic:pan-cancer-mutation-landscape
dataset_usage:
- ref: dataset:msk-met
  role: analyzed
  overlap: full
---

# Genomic characterization of metastatic patterns from prospective clinical sequencing of 25,000 patients

- **Authors:** Nguyen B, et al.
- **Year:** 2022
- **Journal:** Cell
- **PMID:** 35120664
- **BibTeX key:** Nguyen2022

## Key Contribution

This metastatic-pattern sequencing note links paper:Zehir2017 and topic:pan-cancer-mutation-landscape.

Assembles MSK-MET, a pan-cancer cohort of 25,775 patients (50 tumor types) sequenced
prospectively with MSK-IMPACT and uniformly annotated for metastatic events across 21
anatomic sites. The paper systematically links somatic alterations to overall metastatic
burden and to organ-specific tropism, establishing one of the largest clinically-annotated
genomic resources for studying cancer dissemination [@Nguyen2022].

## Methods

The cohort extends the prospective MSK-IMPACT clinical-sequencing program initiated by
Zehir et al. 2017, with longer follow-up and richer annotation (15,632 primary and 10,143
metastatic samples; one sample per patient; 341–468-gene targeted panel). Metastatic
events were extracted at the patient level by combining (a) free-text pathology reports
from sequenced specimens, (b) ICD billing codes from the electronic health record, and
(c) manual chart review of 4,859 patients (~22%) used to validate the EHR pipeline
(median sensitivity ~77% across tumor types). Twenty-one anatomic metastatic sites were
mapped per patient. Associations between somatic alterations and metastatic burden /
organotropism were tested in two stages: (1) univariate Mann-Whitney U (continuous) or
Fisher's exact (categorical) with q < 0.05, then (2) multivariable logistic regression
adjusting for sample type (primary vs. metastatic biopsy), metastatic burden, fraction
genome altered (FGA), and tumor mutational burden (TMB), requiring p < 0.05. Analyses
were stratified by tumor type to control for cohort heterogeneity. Data are released
through cBioPortal and Zenodo with supplementary tables enumerating per-tumor-type and
per-site results [@Nguyen2022].

## Key Findings

Chromosomal instability correlates with metastatic burden in a cancer-type-dependent
manner: strong positive correlation in prostate (rho = 0.33, q = 7.0e-45), lung
adenocarcinoma, and HR+/HER2- breast, but absent in MSS colorectal and high-grade
serous ovarian, suggesting CNA patterns are fixed early in those lineages. Whole-genome
doubling was significantly enriched in metastases vs. primaries in 7 tumor types
(e.g., uterine endometrioid rising from 0% to 14%). No single somatic alteration was
pan-cancer organotropic; all robust gene-site associations were tumor-type-specific.
Examples include: prostate -> bone enriched for AR amplification (5% vs. 21%) and PTEN
deletion (9% vs. 19%); prostate -> liver enriched for PTEN loss (11% vs. 30%) and RB1
loss (3% vs. 10%); HR+ breast -> liver enriched for ESR1 mutations (58% vs. 79%);
lobular breast -> ovary enriched for RHOA mutations (3% vs. 36%); MSS colorectal ->
lung enriched for KRAS (39% vs. 52%); cutaneous melanoma -> brain enriched for PTEN
(7% vs. 14%); lung adenocarcinoma -> brain enriched for TP53, TERT amplification, and
EGFR. The most heavily sampled metastatic sites were lymph node (2,305), liver
(2,289), lung (982), and bone (726) [@Nguyen2022].

## Relevance

Matches the archived `archive/msk_met_2021/` dataset in this repo. Relevant for extending the
pipeline to primary-vs-metastatic comparisons and organotropism-aware clustering.

## Limitations

- Targeted 341–468-gene panel misses signals visible to WES/WGS (e.g., genome-wide
  structural variation, non-coding drivers, mutational signatures requiring full coverage).
- Metastatic-event ascertainment relies on ICD codes plus pathology free-text, with
  median sensitivity ~77% per tumor type — under-counting of asymptomatic or
  non-biopsied sites is expected.
- Single-institution cohort (MSKCC) with referral, treatment, and ascertainment biases;
  metastatic samples are over-represented for pre-treated disease (39% vs. 15% for
  primaries), confounding mutation-vs-therapy interpretation.
- One specimen per patient: no longitudinal or multi-site sampling to resolve clonal
  timing of metastasis-associated alterations.
- Tumor-type sample sizes vary widely; rarer histologies have limited power for
  organ-specific tests.

## Follow-up

- Zehir2017 — IMPACT panel basis and the upstream cohort that MSK-MET extends.
