---
id: paper:AACRGENIEConsortium2017
type: paper
title: 'AACR Project GENIE: Powering Precision Medicine through an International Consortium'
status: read
ontology_terms: []
source_refs:
- article:AACRGENIEConsortium2017
related:
- topic:pan-cancer-mutation-landscape
- topic:targeted-panel-sequencing-bias
- paper:Pugh2022
- paper:Zehir2017
- paper:ChakravartySolit2021
created: '2026-04-13'
updated: '2026-04-13'
dataset_usage:
- ref: dataset:aacr-genie
  role: analyzed
  overlap: unknown
---

# AACR Project GENIE: Powering Precision Medicine through an International Consortium

- **Authors:** AACR Project GENIE Consortium
- **Year:** 2017
- **Journal:** Cancer Discovery 7(8):818–831
- **PMID:** 28572459
- **PMCID:** PMC5611790
- **DOI:** 10.1158/2159-8290.CD-17-0151
- **BibTeX key:** AACRGENIEConsortium2017

## Key Contribution

Launches AACR Project GENIE as an international data-sharing consortium that pools
clinical-grade targeted tumor sequencing from eight academic cancer centers into a single
public registry. The inaugural release (January 5, 2017) contained 18,804 samples from
18,324 patients covering ~19,000 tumors across dozens of cancer types, distributed through
Synapse (`synapse.org/genie`) and cBioPortal (`cbioportal.org/genie/`). The paper establishes
the data-sharing framework (consents, Master Participation Agreement, Data Use Agreement)
and the technical harmonization pipeline that later releases continue to follow.

## Methods

**Founding centers (8):** Dana-Farber Cancer Institute (DFCI), Institut Gustave Roussy
(GRCC), Johns Hopkins Sidney Kimmel (JHU), MD Anderson (MDA), Memorial Sloan Kettering
(MSK), Netherlands Cancer Institute (NKI), Princess Margaret Cancer Centre / UHN, and
Vanderbilt-Ingram (VICC).

**Assays.** The initial release spans 12 distinct gene panels used in ≥50 samples.
Three centers (DFCI, MSK, VICC) contributed 14,310 samples from large hybrid-capture
panels (275–429 genes); the remaining five centers used smaller amplicon-based hotspot
panels (~50 genes). Proprietary panel names (e.g., MSK-IMPACT, OncoPanel) are not
enumerated in the main text. <!-- UNVERIFIED: specific panel-to-center mapping beyond size class -->

**Harmonization.** Centers submit variant calls in MAF or VCF format plus BED files
defining each panel's footprint; raw BAMs are not shared. A stringent germline-filtering
pipeline is applied to all mutation data to reduce re-identification risk, and HIPAA
Safe Harbor de-identification is applied before upload. Two centers performed paired
tumor/normal sequencing; the remaining six were tumor-only. Three centers contributed
CNV calls and two contributed structural rearrangements.

**Governance.** Each center holds 6 months of institutional exclusivity followed by
6 months of consortium-only access before public release. Patient consent operates
through one of three mechanisms: IRB-approved prospective consent, retrospective IRB
waivers, or IRB approval of GENIE-specific proposals. Access is governed by a Master
Participation Agreement and Data Use Agreement; de-identified data are openly
available to academia, government, and industry.

## Key Findings

**Scale.** 18,804 samples / 18,324 patients at launch; MSK (7,341) and DFCI (6,137)
dominate volume. Top tumor types include NSCLC (n=2,985), colorectal (n=2,081),
~2,200 breast, and melanoma (n=785), with 12+ additional tumor types.

**Actionability.** >30% of tumors harbored a potentially actionable alteration; OncoKB
Level 1/2A in 7.3% and Level 3A in 6.4%. Actionability ranged from ~66% in GIST to
much lower rates in renal, prostate, and pancreatic cancer.

**Pan-cancer patterns.** Mutation-rate distributions varied widely within and between
tumor types; an unexpectedly high glioma burden was attributed to prior temozolomide
exposure. Mutual-exclusivity patterns (KRAS/EGFR in lung; PIK3CA/AKT1/PTEN in breast;
KRAS/BRAF in colorectal) mirror TCGA.

**Comparison with TCGA.** Gene-level frequencies are broadly concordant, but referral
bias is visible: EGFR-mutant NSCLC is enriched (~19% vs. lower in TCGA), and EGFR
p.T790M represents 11.3% of GENIE EGFR mutations vs. 2.2% in TCGA, consistent with a
post-TKI resistance population.

**Clinical-trial matching.** Applying NCI-MATCH eligibility criteria matched 2,516
patients to 17 of 18 substudies (2,885 matches), with theoretical match rates strongly
concordant with observed NCI-MATCH accrual (P < 10⁻⁴).

## Relevance

Defines GENIE as a data source for this pipeline. Establishes panel heterogeneity as a first-order
concern for any cross-study mutation-frequency analysis. The launch paper explicitly
quantifies the gene-panel superset/intersection: a **core of 44 genes** is present on
all 12 panels, the larger hybrid-capture panels add 125 genes shared across all of
them plus 134 genes shared by ≤2 large panels, with panel-specific BED files released
alongside the variant data. Any cross-center aggregation must restrict to the relevant
panel-intersection BED and weight by per-gene coverage (the APC example in the paper
shows smaller panels cover 532–1,367 bp vs. 8,622–8,936 bp on large panels — a ~10×
difference in detection opportunity for the same gene).

## Limitations

- **Panel heterogeneity.** 12 panels with only 44 fully shared genes; rare-variant
  detection and novel-target discovery are bounded by the intersection.
- **Tumor-only calling.** Six of eight centers performed tumor-only sequencing,
  relying on germline-filtering heuristics rather than matched-normal subtraction.
- **Referral / selection bias.** All eight centers are tertiary referral institutions,
  enriching for late-stage, previously treated disease (see EGFR T790M enrichment).
- **Minimal clinical annotation at launch.** Only cancer type, primary/metastatic
  status, age, and sex/race are released; treatment, response, and outcomes are not.
- **Sparse structural-variant / CNV coverage.** Only 3 centers contributed CNVs and
  only 2 contributed rearrangements at launch.
- **Panel-name opacity in the launch paper.** The manuscript describes panels only
  by size class and gene count; identifying a sample's exact assay requires the
  per-sample panel ID and BED file from the Synapse release.

## Follow-up

- Pugh2022 — 100k-cases cohort update.
