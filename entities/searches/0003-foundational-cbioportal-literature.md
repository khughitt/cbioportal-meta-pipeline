---
type: search
title: 'Foundational literature for cBioPortal meta-analysis: dataset papers + cross-cutting
  topics'
status: active
created: '2026-04-13'
updated: '2026-04-13'
id: search:0003-foundational-cbioportal-literature
---

# Foundational Literature Search — 2026-04-13

## Search Focus

Build an initial reading queue for the cbioportal meta-analysis project, covering (a) the major
dataset papers describing the cohorts used in the pipeline, and (b) cross-cutting topics whose
methodological guidance directly shapes how cross-study mutation frequencies, ratios, and clusters
should be interpreted. Priority is on verifying exact citations for the large clinical-sequencing
cohorts (AACR GENIE, MSK-IMPACT 10k / 50k, MSK-MET, MSK-CHORD).

## Query Set

1. **Broad — dataset provenance**: `AACR Project GENIE cohort`; `AACR Project GENIE Powering Precision Medicine`; `AACR GENIE Consortium Pugh Cancer Discovery`.
2. **Broad — MSK-IMPACT cohort scale**: `MSK-IMPACT clinical sequencing Nguyen Chakravarty`; `MSK-IMPACT 50000 driver alterations`.
3. **Broad — metastatic cohort**: `MSK-MET metastatic organotropism Nguyen`.
4. **Broad — clinical-outcome integration**: `MSK-CHORD automated real-world data cancer outcome`.
5. **Contrasting / confounder — clonal hematopoiesis**: `Bolton clonal hematopoiesis solid tumor Nature Genetics`.
6. **Methods — pan-cancer driver / signature catalogs**: verified seed citations for Cerami 2012, Gao 2013, Zehir 2017, Bailey 2018, Ellrott 2018 (MC3), Tate 2019 (COSMIC), ICGC/TCGA PCAWG 2020.

## Sources and Run Metadata

- Primary source: **PubMed** via E-utilities (`esearch` + `esummary`).
- Retrieved: 2026-04-13.
- NCBI API key: not used (unauthenticated).
- No existing `doc/searches/` prior to this run.
- Candidate cap: ~50 per query; final shortlist: 13 records.

## Ranked Results

| # | Citation | Year | IDs | Tier | Why it matters |
|---|---|---|---|---|---|
| 1 | AACR Project GENIE Consortium. "AACR Project GENIE: Powering Precision Medicine through an International Consortium." *Cancer Discov* | 2017 | PMID: 28572459 | Core now | Original GENIE dataset paper — cohort scope, panel heterogeneity, access model. |
| 2 | Pugh TJ, et al. "AACR Project GENIE: 100,000 Cases and Beyond." *Cancer Discov* | 2022 | PMID: 35819403 | Core now | GENIE 100k-scale cohort update — essential context for current GENIE releases used by the pipeline. |
| 3 | Zehir A, et al. "Mutational landscape of metastatic cancer revealed from prospective clinical sequencing of 10,000 patients." *Nat Med* | 2017 | PMID: 28481359 | Core now | The canonical MSK-IMPACT 10k paper. Gene content of the IMPACT panel and prospective-sequencing design. |
| 4 | Bandlamudi C, et al. "Cancer type-specific variation in patterns of driver alterations across 50,000 tumors." *Cancer Cell* | 2026 | PMID: 41895280 | Core now | The MSK-IMPACT 50k-scale follow-up — driver-alteration landscape, directly comparable to this project's gene x cancer outputs. |
| 5 | Nguyen B, et al. "Genomic characterization of metastatic patterns from prospective clinical sequencing of 25,000 patients." *Cell* | 2022 | PMID: 35120664 | Core now | MSK-MET — metastatic cohort, organotropism. Matches the archived `msk_met_2021/` artifacts in this repo. |
| 6 | Jee J, et al. "Automated real-world data integration improves cancer outcome prediction." *Nature* | 2024 | PMID: 39506116 | Relevant next | MSK-CHORD — integrates MSK-IMPACT genomics with clinical outcomes; relevant when we later extend beyond mutation-only views. |
| 7 | Bolton KL, et al. "Cancer therapy shapes the fitness landscape of clonal hematopoiesis." *Nat Genet* | 2020 | PMID: 33106634 | Core now | CH-variant contamination confounds panel-based tumor mutation calls (esp. unmatched normals). Critical read before trusting gene x cancer ratios for CH-associated genes (e.g., DNMT3A, TET2, ASXL1). |
| 8 | Cerami E, et al. "The cBio cancer genomics portal: an open platform for exploring multidimensional cancer genomics data." *Cancer Discov* | 2012 | PMID: 22588877 | Core now | Foundational cBioPortal platform paper — required citation whenever the project reports on cBioPortal-derived data. |
| 9 | Gao J, et al. "Integrative analysis of complex cancer genomics and clinical profiles using the cBioPortal." *Sci Signal* | 2013 | PMID: 23550210 | Relevant next | cBioPortal API / integrative-analysis companion paper. |
| 10 | Bailey MH, et al. "Comprehensive Characterization of Cancer Driver Genes and Mutations." *Cell* | 2018 | PMID: 30096302 | Core now | Pan-cancer driver-gene consensus from TCGA PanCanAtlas. Reference driver list and methods-comparison framework for this project's gene-prioritization outputs. |
| 11 | Ellrott K, et al. "Scalable Open Science Approach for Mutation Calling of Tumor Exomes Using Multiple Genomic Pipelines." *Cell Syst* | 2018 | PMID: 29596782 | Relevant next | MC3 — the pan-cancer reference mutation call-set. Reference point when contrasting panel-based calls to WES-based calls. |
| 12 | Tate JG, et al. "COSMIC: the Catalogue Of Somatic Mutations In Cancer." *Nucleic Acids Res* | 2019 | PMID: 30371878 | Core now | COSMIC + Cancer Gene Census — the most widely used curated cancer-gene list. Use as an external validation axis for our clustering outputs. |
| 13 | ICGC/TCGA Pan-Cancer Analysis of Whole Genomes Consortium. "Pan-cancer analysis of whole genomes." *Nature* | 2020 | PMID: 32025007 | Peripheral monitor | PCAWG whole-genome complement to panel/WES work. Useful when contextualizing panel-callable-fraction limitations. |

## Priority Reading Queue

**Core now (read first):**

1. Pugh 2022 — GENIE 100k (defines the cohort the pipeline actually ingests).
2. Bandlamudi 2026 — MSK-IMPACT 50k drivers (most direct methodological peer of this project's outputs).
3. Zehir 2017 — MSK-IMPACT 10k (panel content + prospective-sequencing framing).
4. Bolton 2020 — CH contamination (critical interpretation caveat for panel-based gene frequencies).
5. Bailey 2018 — PanCanAtlas driver consensus (comparison framework for gene prioritization).
6. AACR GENIE 2017 — original consortium paper.
7. Nguyen 2022 — MSK-MET (matches an archived dataset in this repo).
8. Cerami 2012 — cBioPortal platform (citation-hygiene foundation).
9. Tate 2019 — COSMIC CGC (external validation reference list).

**Relevant next:**

10. Jee 2024 — MSK-CHORD (for the eventual outcome-integration extension).
11. Ellrott 2018 — MC3 (when comparing panel vs. WES calls).
12. Gao 2013 — cBioPortal analysis companion.

**Peripheral monitor:**

13. ICGC/TCGA PCAWG 2020 — WGS pan-cancer complement.

## Coverage Notes and Gaps

- **MSK-CH 2023**: the archived `archive/msk_ch_2023/` directory in this repo appears to reference
  the MSK clonal-hematopoiesis cBioPortal study rather than a distinct 2023 paper; the canonical
  citation for that study remains Bolton KL, et al. (2020) *Nat Genet*.
- **AACR GENIE-BPC (Biopharma Collaborative)**: found Acebedo et al. 2025 *ESMO Real World Data
  Digit Oncol* (PMID: 41647353) — treat as peripheral until the pipeline actually consumes BPC
  cohorts.
- **COSMIC mutational-signatures reference**: not verified in this run. Add Alexandrov et al.
  (2020) *Nature* signature-catalog paper when the mutational-signatures topic is developed.
- **Targeted-panel bias / comparability across panels**: no dedicated paper pulled in this run.
  Add a dedicated search (MSK-IMPACT vs FoundationOne vs GENIE panels) before attempting
  cross-panel normalization.
- **TMB harmonization (Friends-of-Cancer-Research / Buchhalter)**: not searched this round; add if
  TMB becomes an analytical axis.
- **Cross-study meta-analysis statistical methods for cancer genomics**: no dedicated paper in
  this run; complement with a methods-focused search later.

## Recommended Next Actions

1. Convert the 13 records above into `papers/references.bib` entries and per-paper stubs under
   `doc/background/papers/`.
2. Create topic stubs under `doc/background/topics/` for the 10 topics in this project's backlog
   (see `doc/background/topics/` index).
3. Queue `tasks` entries (`science-tool tasks add --type research`) for each Core-now / Relevant-next
   reading item.
4. Follow up with a second, focused search run covering mutational signatures, TMB harmonization,
   panel-comparability / cross-panel normalization, and meta-analysis statistics in cancer genomics.
