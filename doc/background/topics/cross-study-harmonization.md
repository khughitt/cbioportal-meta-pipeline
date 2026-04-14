---
id: "topic:cross-study-harmonization"
type: "topic"
title: "Cross-study harmonization in panel-based cancer genomics (synthesis)"
status: "active"
ontology_terms: []
source_refs: []
related:
  - "topic:targeted-panel-sequencing-bias"
  - "topic:clonal-hematopoiesis-contamination"
  - "topic:cohort-selection-bias-representativeness"
  - "topic:variant-interpretation-oncokb-vus"
  - "topic:mutation-rate-normalization"
  - "article:Pugh2022"
  - "article:Bandlamudi2026"
  - "article:Bolton2020"
  - "article:Ellrott2018"
  - "article:Chakravarty2017"
created: "2026-04-13"
updated: "2026-04-13"
---

# Cross-study harmonization in panel-based cancer genomics (synthesis)

## Summary

This is a synthesis topic that pulls together the cross-cutting interpretive concerns
across our reading queue. **Cancer-genomics consortia document panel and cohort biases
extensively but do not publish ready-to-use harmonization recipes.** Any pipeline
aggregating across heterogeneous cBioPortal studies inherits four bias axes that compound
multiplicatively: (1) panel content, (2) matched-vs-unmatched normal calling,
(3) cohort selection, and (4) annotation version drift. Naive aggregation is therefore not
just noisy — it is *systematically biased* in ways that the literature lets us partially
correct.

This topic is the master interpretive frame for our pipeline outputs.

## Key Concepts

### The Four Compounding Bias Axes

### 1. Panel content
- 91 distinct GENIE assays at v9.1 (Pugh 2022); MSK-IMPACT spans 4 panel versions.
- 44-gene core across all 12 launch GENIE panels; smaller intersection at 91 panels.
- Per-gene callable region length differs ~10× across panels (APC example, AACR GENIE
  2017).
- **Fix**: per-(study, gene) callability mask from per-assay BEDs.
  *See*: `topic:targeted-panel-sequencing-bias`.

### 2. Matched-vs-unmatched normal calling
- MSK-IMPACT: 98% matched-buffy-coat; CH variants correctly subtracted.
- Pugh 2022 GENIE: 52% tumor-only; centralized artifact / population-frequency filtering
  applied centrally but is not equivalent to per-patient matched-normal subtraction.
- 7 priority CH-driver genes systematically inflated in tumor-only cohorts: DNMT3A,
  PPM1D, TET2, TP53, ASXL1, CHEK2, PRPF8.
- **Fix**: CH-aware filter / flag for these 7 genes; per-study matched-normal annotation.
  *See*: `topic:clonal-hematopoiesis-contamination`.

### 3. Cohort selection
- Clinical-sequencing cohorts (GENIE, MSK-IMPACT) are dominated by advanced / metastatic /
  pre-treated disease. TCGA is treatment-naive primary.
- Quantitative example: AR mutations 18% in MSK-IMPACT metastatic prostate vs 1% in TCGA;
  ESR1 11% in MSK-IMPACT metastatic breast vs 4% in TCGA (Zehir 2017).
- EGFR T790M 11.3% of GENIE EGFR mutations vs 2.2% of TCGA EGFR mutations — clean
  quantification of post-TKI / advanced-disease bias.
- **Fix**: per-study cohort-stage descriptor (primary-naive / metastatic / pre-treated)
  ingested from study metadata; stratified analyses where stage matters.
  *See*: `topic:cohort-selection-bias-representativeness`.

### 4. Annotation version drift
- OncoKB Level 1/2A actionability rate rose from **8.9% (2017) → 31.6% (2022)** on the
  *same* MSK-IMPACT cohort (Suehnholz 2024 follow-up).
- GENIE Level 1/2A independently rose from **7.3% → 17.0%** in the same period.
- Implication: any "% functional" / "% actionable" / driver-list-overlap statistic must be
  pinned to a specific OncoKB / Bailey / CGC version, not floating against the current
  release.
- **Fix**: stamp every annotated output with the catalog version used; version-pin
  catalogs in the pipeline manifest.
  *See*: `topic:variant-interpretation-oncokb-vus`.

## Current State of Knowledge

### Recurring Pattern: Acknowledgement Without Correction

Across Batches 1–6 we hit this pattern repeatedly:

| Paper | Acknowledged bias | Published correction? |
|---|---|---|
| AACR GENIE 2017 | 12 panels with only 44-gene core | No (BEDs in Synapse, no usable correction recipe) |
| Pugh 2022 | 91 panels, 52% tumor-only | TMB harmonization model mentioned, never quantified |
| Zehir 2017 | Advanced-disease selection inflates AR/ESR1/TP53 | No (stratified analyses, no correction) |
| Bandlamudi 2026 | ~1/3 drivers in non-canonical contexts | No correction, but Zenodo data lets us re-analyze |
| Bolton 2020 | CH inflates DDR-gene counts | Matched-normal VAF-ratio rule (only works with matched normal) |
| Chakravarty Solit 2021 | Cross-vendor panel heterogeneity | No (review focuses on clinical utility) |
| Ellrott 2018 | TCGA per-study calling heterogeneity | **Yes — MC3 unified MAF** |

**Ellrott 2018 (MC3) is the exception that proves the rule.** It actually solves the
problem by re-calling all TCGA exomes uniformly. Most consortia document the issue and
move on.

## Relevance to This Project

### What This Means for Our Pipeline

Our `gene_cancer.feather` and downstream cluster outputs aggregate naively across all
four bias axes. Three immediately tractable corrections are available without new
research:

1. **MC3 ingestion for the TCGA portion of our cohort** — solves Axis 1 (heterogeneous
   per-study TCGA MAFs) for free. Single Synapse download, ~25% more calls, uniform
   filter vocabulary.
2. **GENIE per-assay callability mask** — solves Axis 1 partially for the GENIE portion.
   Per-(study, gene) callable-fraction column on every output. Wired in pipeline already
   (`process_genie_panel_coverage.py`).
3. **CH-priority-gene flag + per-study matched-normal flag** — solves Axis 2. Two-line
   addition to per-gene outputs; downstream consumers can choose to filter.

Three additional fixes that need design work:

4. **Per-study cohort-stage descriptor** — solves Axis 3. Requires per-study metadata
   ingestion from cBioPortal study definitions (primary vs metastatic; treatment-naive vs
   pre-treated). cBioPortal exposes this via clinical sample tables but needs unified
   interpretation across studies.
5. **Catalog version stamping** — solves Axis 4. Every Bailey / CGC / OncoKB annotation
   in our outputs should carry the catalog version (date, release tag) the annotation was
   computed against.
6. **Tissue-conditional driver flag** — partial fix for the "non-canonical context"
   finding (Bandlamudi 2026 + Bailey 2018 19% tissue-borrowed). Each (gene, cancer)
   annotation should distinguish "Bailey driver in this cancer" vs "Bailey driver in
   any cancer."

## Open Questions for This Project

- **What's the right unit of cross-study evidence aggregation?** Currently we aggregate
  raw counts. Better candidates: per-study per-gene effect sizes (rate / ratio), then
  combine via meta-analytic methods (random-effects, SumZ, fixed-effects with study-level
  covariates).
- **Should we report a single cross-study ratio per (gene, cancer), or always report
  the matched-normal vs tumor-only stratified pair?** The discordance between the two is
  itself an informative output.
- **At what point does panel-aware analysis become panel-restrictive?** If we restrict
  to the 44-gene core, we lose most of the data. If we keep everything with per-(study,
  gene) callability weighting, the math gets non-trivial. No consortium has solved this.

## Key References

- Pugh2022 — GENIE 91-panel current state; 52% tumor-only; per-assay BEDs in Synapse.
- Bandlamudi2026 — non-canonical-context driver finding; published Zenodo dataset.
- Bolton2020 — CH-priority gene list and therapy-selectivity quantification.
- Ellrott2018 — MC3 unified TCGA MAF; the one published harmonization recipe.
- Chakravarty2017 + Suehnholz2024 — OncoKB version-drift quantification (8.9% → 31.6%).
- See also: `topic:targeted-panel-sequencing-bias`,
  `topic:clonal-hematopoiesis-contamination`,
  `topic:cohort-selection-bias-representativeness`,
  `topic:variant-interpretation-oncokb-vus`.
