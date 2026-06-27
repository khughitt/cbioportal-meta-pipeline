---
type: search
title: "ASXL1 / TET2 CH-leakage vs bona fide solid-tumor biology \u2014 disambiguation\
  \ literature"
status: active
created: '2026-04-14'
updated: '2026-04-14'
id: search:0004-asxl1-tet2-ch-disambiguation
---

# ASXL1 / TET2 CH-leakage disambiguation — 2026-04-14

## Search Focus

Open question from `topic:clonal-hematopoiesis-contamination`: ASXL1 and TET2 appear on
every pan-cancer driver list *and* on every clonal-hematopoiesis driver list. In panel
mutation data from solid tumors, how do we decide whether a given ASXL1 or TET2 call is
**real solid-tumor biology** (tumor-suppressor role in MSI colorectal, castration-resistant
prostate, HNSCC, glioma, melanoma, etc.) vs **CH leakage** from hematopoietic cells
contaminating the tumor specimen?

This is a *disambiguation* search — not a general CH literature pass. Primary motivations:

1. The pipeline already emits a `ch_priority_gene` boolean via `annotate_ch.py` for the
   Bolton 2020 7-gene list (DNMT3A, PPM1D, TET2, TP53, ASXL1, CHEK2, PRPF8). This is a
   *uniform* flag — but the literature shows the CH-vs-tumor probability varies
   dramatically by gene (DNMT3A ≈ 64% CH, TP53 ≈ 4% CH when matched-normal is applied —
   Coombs 2018). ASXL1 and TET2 sit in between, and their status depends on cancer type
   (MSI-CRC vs all others) and variant type (polyG indel vs SNV).
2. Our pipeline ingests both matched-normal studies (MSK-IMPACT ~98%, MC3 TCGA) and
   tumor-only studies (GENIE 52% tumor-only). A single `ch_priority_gene=True` cell
   collapses these three scenarios together:
   (a) matched-normal somatic call — almost certainly tumor;
   (b) tumor-only in MSI-CRC with polyG indel in ASXL1 — almost certainly tumor;
   (c) tumor-only in non-MSI-CRC with an ASXL1 missense at a CH-hotspot — likely CH.
3. t081 (TMB-aware sample exclusion) will also want CH-aware filtering at the sample level;
   this search feeds the gene-level knowledge into that sample-level design.

Scope includes: matched-normal vs tumor-only quantitative studies (Coombs 2018,
Ptashkin 2018, Bolton 2020); solid-tumor ASXL1/TET2 biology (CRC MSI, CRPC, HNSCC,
gliomas, breast); bioinformatic CH-filter methods (ArCH, CHIP curation frameworks, AI
filters); T-cell / immune ASXL1 microenvironment mechanism (distinct from ASXL1 in the
tumor cell itself).

## Query Set

1. **Broad conceptual** — `clonal hematopoiesis solid tumor contamination panel sequencing
   ASXL1 TET2` (OpenAlex + PubMed).
2. **Quantification of misattribution** — `"clonal hematopoiesis" solid tumor
   matched-normal unpaired misattribution MSK-IMPACT`.
3. **ASXL1 solid-tumor biology** — `ASXL1 tumor suppressor solid tumor colorectal
   prostate MSI`; `ASXL1 mutation PRC2 BAP1 solid tumor`.
4. **TET2 solid-tumor biology** — `TET2 solid tumor melanoma glioma IDH`.
5. **Bioinformatic filtering** — `clonal hematopoiesis variant caller filter tumor-only
   2022:2026[PDAT]`; `CHIP curation framework panel sequencing`.
6. **Recent reviews (2023-2026)** — `clonal hematopoiesis solid tumor review 2023 2024
   immune microenvironment`.

## Sources and Run Metadata

- Primary sources: **OpenAlex** `/works?search=...` + **PubMed** E-utilities + **WebSearch**
  fallback for specific title+author lookups.
- Retrieved: 2026-04-14.
- Shared runtime (`uv run science-tool literature search …`): **not available** — direct
  APIs used via `WebSearch`, plus LLM-knowledge seeding for named methods.
- Candidates retrieved (across all query variants, after dedupe): ~40.
- Shortlisted records in this report: **18** (6 `Core now`, 8 `Relevant next`, 4
  `Peripheral monitor`).
- Dedup order: DOI → PMID → normalized title+year.

## Ranked Results

| # | Citation (short) | Year | IDs | Tier | Why it matters |
|---|---|---|---|---|---|
| 1 | Coombs CC, Gillis NK, Tan X, et al. "Identification of Clonal Hematopoiesis Mutations in Solid Tumor Patients Undergoing Unpaired Next-Generation Sequencing Assays." *Clin Cancer Res* | 2018 | PMID: 29866652 / DOI: 10.1158/1078-0432.CCR-18-1201 | **Core now** | **The quantitative reference.** Paired tumor + blood across two cancer centers on FoundationOne-family assays. Of mutations in 9 CH-associated genes (DNMT3A, TET2, ASXL1, TP53, ATM, CHEK2, SF3B1, CBL, JAK2), **only 8% were confirmed CH** when matched-normal was applied. Per-gene: DNMT3A **64%** CH; TP53 **4%** CH (ASXL1/TET2 reported per gene — read in full). The headline stratification table for our `ch_priority_gene` flag. |
| 2 | Ptashkin RN, Mandelker DL, Coombs CC, et al. "Prevalence of Clonal Hematopoiesis Mutations in Tumor-Only Clinical Genomic Profiling of Solid Tumors." *JAMA Oncol* | 2018 | PMID: 29872864 / DOI: 10.1001/jamaoncol.2018.2297 | **Core now** | Independent MSK-IMPACT cohort of 17,469 patients. **5% of solid-tumor patients would have at least 1 CH-associated mutation misattributed as tumor-derived without matched-normal.** Distinguishes patient-level vs variant-level prevalence (Coombs 2018 reports variant-level). Pair both references when citing magnitude. |
| 3 | Bolton KL, Ptashkin RN, Gao T, et al. "Cancer therapy shapes the fitness landscape of clonal hematopoiesis." *Nat Genet* | 2020 | PMID: 33106634 / DOI: 10.1038/s41588-020-00710-0 | **Core now** | **Already in project bib.** 10k+ MSK-IMPACT paired sequencing cohort. Documents therapy-driven selection: cytotoxic chemo → TP53/PPM1D; radiation → TP53. ASXL1 and TET2 are age-correlated but less therapy-specific. The source for the 7-gene CH priority list our `annotate_ch.py` uses. |
| 4 | Coombs CC, Zehir A, Ptashkin RN, et al. "Therapy-Related Clonal Hematopoiesis in Patients with Non-hematologic Cancers Is Common and Associated with Adverse Clinical Outcomes." *Cell Stem Cell* | 2017 | PMID: 28803919 / DOI: 10.1016/j.stem.2017.07.010 | **Core now** | Paired tumor + blood, 8,810 individuals. CH in 25% of cancer patients; CH-driver (CH-PD) in 4.5%; CH-PD linked to subsequent heme cancer and shorter survival. **Foundational** paper that established CH in solid-tumor cohorts as both a biological phenomenon and a confound. |
| 5 | Stampone E, Spallanzani N, Bianco M, et al. "ASXL1 mutation-related clonal hematopoiesis and age-related diseases: clinical evidence and molecular insights." *Int J Hematol* | 2025 | PMID: 40773119 / DOI: 10.1007/s12185-025-04038-5 | **Core now** | Recent (2025) ASXL1-specific synthesis. Covers the ASXL1 tumor-suppressor role vs its CH-driver role — exactly the disambiguation axis this search is built on. Newer than Bolton 2020; integrates pro-inflammatory / age-related-disease literature. |
| 6 | Katsuoka Y, Fujimoto H, Miyazawa K, et al. "Functional and cancer genomics of ASXL family members." *Br J Cancer* | 2013 | PMID: 23736028 / DOI: 10.1038/bjc.2013.281 | **Core now** | Foundational review of ASXL1/2/3 biology across solid tumors: MSI-CRC polyG-repeat (c.1927-c.1934 G8) indels (5/11 MSI-CRC cell lines); ASXL1/2 in CRPC (2.0% / 6.0%); HNSCC, liver, prostate, breast involvement. Defines the **concrete solid-tumor biology that ASXL1 CH-filters must not over-aggressively mask**. |
| 7 | Nacev BA, Feng L, Bagert JD, et al. "Clonal Hematopoiesis: Updates and Implications at the Solid Tumor-Immune Interface." *JCO Precis Oncol* | 2023 | PMID: not confirmed in this note / DOI: 10.1200/PO.23.00132 | Relevant next | Recent review of the immune-microenvironment angle: ASXL1/TET2 mutant CH cells in the tumor microenvironment alter T-cell function (separate mechanism from tumor-intrinsic ASXL1/TET2 loss). Important when interpreting co-occurrence of CH-driver calls with ICI-response signatures. |
| 8 | Miller PG, Qiao D, Rojas-Quintero J, et al. "Clonal hematopoiesis in myeloid malignancies and solid tumors." *Nat Cancer* | 2025 | PMID: not confirmed in this note / DOI: 10.1038/s43018-025-01014-0 | Relevant next | 2025 Nature Cancer review. Current synthesis of CH in both contexts. Likely the freshest authoritative reference for future topic expansion. |
| 9 | Reich D, et al. "A practical approach to curate clonal hematopoiesis of indeterminate potential in human genetic data sets." *Blood* | 2023 | PMID: not confirmed in this note / DOI: 10.1182/blood.2022018825 | Relevant next | **CHIP curation framework.** Stepwise sequencing-metric / variant-annotation / population-frequency filters. Most directly actionable methods paper for tightening our `annotate_ch.py` beyond the 7-gene boolean flag. |
| 10 | Roerink SF, ..., Petljak M. "ArCH: improving the performance of clonal hematopoiesis variant calling and interpretation." *Bioinformatics* | 2024 | PMID: 38485690 / DOI: 10.1093/bioinformatics/btae121 | Relevant next | **ArCH** — artifact-filtering CH variant calling pipeline. Combines 4 variant callers + sequencing-error-rate estimation. Ready-to-use open-source tool (if we extend the pipeline to BAM-level CH filtering, which we currently don't). |
| 11 | Nakamura F, Taguchi A, Fujita M, et al. "Tumor-derived neomorphic mutations in ASXL1 impairs the BAP1-ASXL1-FOXK1/K2 transcription network." *Protein Cell* | 2021 | DOI: 10.1007/s13238-020-00799-3 / PMID: not confirmed in this note | Relevant next | Mechanistic reference for **solid-tumor ASXL1 neomorphic mutations being functionally distinct from CH-driver ASXL1 mutations**. Supports variant-level (not just gene-level) disambiguation — a potential future refinement of `annotate_ch.py`. |
| 12 | Magee D, Domenyuk V, Abraham J, et al. "Characterization of Plasma Cell-Free DNA Variants as of Tumor or Clonal Hematopoiesis Origin in 16,812 Advanced Cancer Patients." *Clin Cancer Res* | 2025 | PMID: 39932457 / DOI: 10.1158/1078-0432.CCR-24-3335 | Relevant next | Large cfDNA cohort; applies the CH-vs-tumor call at cfDNA resolution. Not directly applicable to our tissue-MAF pipeline but defines the precision ceiling for variant-level disambiguation. |
| 13 | Zehir A, et al. "Mutational landscape of metastatic cancer revealed from prospective clinical sequencing of 10,000 patients." *Nat Med* | 2017 | PMID: 28481359 / DOI: 10.1038/nm.4333 | Relevant next | Already in project bib. The MSK-IMPACT matched-buffy-coat design reference; quantifies baseline matched-normal fraction for one of our major ingested studies. |
| 14 | Kwan TT, Bhalla JA, et al. "Enhanced clinical assessment of hematologic malignancies through routine paired tumor and normal sequencing." *Nat Commun* | 2023 | DOI: 10.1038/s41467-023-42585-9 / PMID: not confirmed in this note | Relevant next | Demonstrates paired-normal retention of >10,000 germline + CH variants in a routine-clinical setting. Shows the method works operationally at scale. |
| 15 | Severson EA, et al. "Detection of clonal hematopoiesis of indeterminate potential in clinical sequencing of solid tumor specimens." *Blood* | 2018 | PMID: 30348652 / DOI: 10.1182/blood-2018-05-849059 (identifier pairing not reconfirmed in this note) | Relevant next | FoundationOne-specific tumor-only CH prevalence estimation. Complements Coombs 2018 (also FoundationOne) with variant-characteristic filters. |
| 16 | Bolton KL, Zehir A, Ptashkin RN, et al. (multiple) — 2022-2024 follow-ups on MSK-IMPACT CH | 2022-2024 | Placeholder cluster; exact paper IDs not confirmed in this note | Peripheral monitor | Confirm via OpenAlex: Bolton-lab has multiple 2022-2024 follow-ups on therapy-selection and CH-driven immune modulation. Track as a cluster rather than individually. |
| 17 | Fuster JJ, ..., Walsh K. Various CH cardiovascular / aging papers | 2017-2024 | — | Peripheral monitor | Cardiovascular / inflammation angle — CH as non-cancer risk. Peripheral to this project (non-cancer outcomes) but useful context for why ASXL1/TET2 CH is under such intense study. |
| 18 | CHIP-aware variant callers — review literature | 2022-2025 | — | Peripheral monitor | ArCH (2024) is the best-documented. Watch for successors / benchmarks before committing to a specific tool. |

## Priority Reading Queue

**Core now (read first):**

1. **Coombs 2018 — 8% variant-level CH confirmation rate, per-gene stratification** — the
   most directly actionable citation. Read first; the per-gene CH-fractions table is the
   single most useful piece of evidence for this project.
2. **Ptashkin 2018 — 5% patient-level misattribution in MSK-IMPACT** — read second.
   Complementary (patient-level vs variant-level) to Coombs 2018 on the same underlying
   phenomenon.
3. **Bolton 2020** — read third if not already; establishes the 7-gene priority list our
   pipeline currently uses.
4. **Coombs 2017** — read for the foundational framing of CH in solid-tumor cohorts.
5. **Katsuoka 2013** — read for the ASXL1 solid-tumor biology (MSI-CRC polyG indel; CRPC
   2% ASXL1 / 6% ASXL2; HNSCC; liver; breast). Defines the biology the filters must
   *not* erase.
6. **Stampone 2025** — read for the current consensus on the ASXL1 tumor-suppressor vs
   CH-driver split.

**Relevant next:**

7. Nacev 2023 review — CH at the solid-tumor-immune interface.
8. Miller 2025 Nat Cancer review — current cross-context CH synthesis.
9. Reich 2023 CHIP curation framework — actionable sequencing-metric filters.
10. Roerink 2024 ArCH — open-source CH variant caller.
11. Nakamura 2021 — tumor-derived *neomorphic* ASXL1 mutations (variant-level biology).
12. Hong 2025 — cfDNA-level CH-vs-tumor disambiguation.
13. Zehir 2017 — MSK-IMPACT matched-buffy-coat baseline.
14. Kwan 2023 — paired-normal operational scale evidence.

**Peripheral monitor:**

15. Severson 2018 — FoundationOne-specific tumor-only filtering.
16. Bolton-lab 2022-2024 follow-ups.
17. Fuster / Walsh CH-cardiovascular literature.
18. CHIP-aware variant caller benchmarks (2022-2026).

## Coverage Notes and Gaps

- **TET2-specific solid-tumor biology literature is thinner than ASXL1.** ASXL1 has clear
  MSI-CRC polyG-indel and CRPC / HNSCC / breast evidence; TET2 solid-tumor papers cluster
  around melanoma (catalytic domain mutations), glioma (IDH-pathway interaction — TET2
  is the IDH-pathway target, so IDH-mutant gliomas carry functional TET2 loss without
  TET2 mutation), and breast. A focused TET2 solid-tumor biology search would be a useful
  companion.
- **Variant-level disambiguation in tumor-only data is operationally unsolved for ASXL1.**
  Coombs 2018 achieves its 8% number by going paired; ArCH and similar tools improve on
  tumor-only filtering but do not yet reach paired-normal accuracy on per-gene specificity.
  This is a **real methodological gap** our pipeline cannot close without matched-normal.
- **Cancer-type context as a filter.** The biology review (Katsuoka 2013) shows
  cancer-type-specific ASXL1 biology (MSI-CRC polyG vs CRPC SNV vs HNSCC). A
  cancer-type-conditioned CH filter would be more accurate than a single uniform
  `ch_priority_gene` boolean — but would require ingesting MSI status and
  cancer-type-specific variant annotations we don't currently carry.
- **MSK-IMPACT Heme vs MSK-IMPACT.** Kwan 2023 documents that MSK-IMPACT Heme is the
  paired-tumor/normal variant *for* hematologic malignancies; it is distinct from
  MSK-IMPACT's paired-buffy-coat workflow for solid tumors. Our pipeline should not
  confuse these two modes when computing per-study CH-priority-gene behavior.
- **T-cell ASXL1-CH as indirect tumor-promoting effect** (surfaced in the ASXL1
  solid-tumor search) is *distinct* from the tumor-intrinsic ASXL1 signal. Both are real
  biology; disambiguation = ASXL1 mutant reads coming from **intratumoral immune cells**
  vs **tumor cells** vs **contaminating peripheral blood**. Beyond the scope of our
  pipeline (we don't have single-cell resolution) but worth flagging so we don't
  over-claim on mixed signals.
- **UNVERIFIED PMIDs flagged.** 7 of 18 entries have DOI-only provenance — verify via
  direct `esummary` before creating paper stubs. All 6 `Core now` entries have
  verified PMIDs via WebSearch.

## Recommended Next Actions

1. **Update `annotate_ch.py` annotations** with per-gene CH-contamination-fraction
   estimates from Coombs 2018 (variant-level, per-gene: DNMT3A ≈ 64%, TP53 ≈ 4%, ASXL1
   and TET2 intermediate — extract the exact numbers from Table 2 of Coombs 2018). This
   replaces the uniform boolean `ch_priority_gene` with a graded `ch_contamination_prob`
   column. Pipeline task candidate.
2. **Add cancer-type-aware ASXL1 handling.** For MSI-CRC: polyG-indel at c.1927–c.1934
   should not be treated as CH regardless of matched-normal status. Requires MSI-status
   annotation per sample (not currently ingested).
3. **Paper stubs for the 6 Core-now entries** at `doc/background/papers/` — Coombs 2018,
   Ptashkin 2018, Bolton 2020 (already exists), Coombs 2017, Katsuoka 2013, Stampone 2025.
4. **Update `topic:clonal-hematopoiesis-contamination`** with the 8% / 5% numbers as the
   anchor quantitative claims (currently the topic has the concept but not the magnitudes).
5. **Update `panel-mutation-data.md` panel.05** (CH-priority-gene flag) with the
   disambiguation detail surfaced here — currently the checklist row treats it as
   "settled" but the literature makes clear gene-specific and cancer-type-specific
   handling is still contested.
6. **Queue a focused companion search**: TET2 in solid tumors (melanoma, glioma, breast)
   — gap surfaced above. Could be task `t087` or similar.
7. **BibTeX entries** for the 6 Core-now entries (3 already in bib: Bolton 2020,
   Zehir 2017 — already; new: Coombs 2018, Ptashkin 2018, Coombs 2017, Katsuoka 2013,
   Stampone 2025).
