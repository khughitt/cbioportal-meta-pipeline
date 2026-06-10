---
type: topic
title: Targeted-panel sequencing bias in cross-study cancer genomics
status: active
created: '2026-04-13'
updated: '2026-04-13'
id: topic:targeted-panel-sequencing-bias
ontology_terms: []
source_refs: []
related:
- paper:Zehir2017
- paper:Bandlamudi2026
- paper:AACRGENIEConsortium2017
- paper:Pugh2022
- paper:Ellrott2018
- paper:Bolton2020
- paper:ChakravartySolit2021
- topic:clonal-hematopoiesis-contamination
- topic:cross-study-harmonization
---

# Targeted-panel sequencing bias in cross-study cancer genomics

## Summary

Most modern cBioPortal cohorts come from **targeted gene panels**, not whole-exome sequencing.
GENIE alone uses 91 distinct assays at v9.1; MSK-IMPACT itself spans four panel versions
(341 → 410 → 468 → 505 genes); FoundationOne, Tempus, Caris, Guardant360 use yet other panel
designs. Naively aggregating mutation counts across these cohorts **systematically over-counts
genes covered by larger panels and under-counts genes only on smaller panels** — by as much as
~10× per gene at the extremes (Bailey-relevant APC region: 532–1,367 bp on small GENIE panels
vs 8,622–8,936 bp on large hybrid-capture panels per AACR GENIE 2017).

Cross-study aggregation that ignores panel content is therefore not just noisy — it is
*biased* toward genes that big panels happen to cover.

## Key Concepts

- **Panel-content heterogeneity.** GENIE v9.1: 91 distinct panels. Per-assay BED files exist
  but are released only via Synapse (`syn24179663`); no published `study_id → panel_id →
  gene_list` table. The launch GENIE paper documents a **44-gene core** present on all 12
  initial panels; the intersection at 91 panels is even smaller.
- **Per-gene callable fraction.** Even when two panels both "cover" gene X, they cover
  different exonic regions to different depths. This is the right denominator for ratio
  computations, not "is the gene on the panel."
- **Matched-vs-unmatched normal calling.** MSK-IMPACT runs paired buffy coat for ~98% of
  cases (Zehir 2017), giving per-patient germline subtraction. GENIE is **52% tumor-only**
  (Pugh 2022), relying on centralized population-frequency / artifact filtering. Tumor-only
  pipelines also fail to subtract clonal-hematopoiesis variants (see
  `topic:clonal-hematopoiesis-contamination`).
- **Panel design choices that distinguish vendors.** MSK-IMPACT covers TERT promoter +
  selected introns of 17 recurrently rearranged genes for fusion detection; FoundationOne
  has different intronic baiting for fusions; commercial vendors generally do not publish
  their full BED.
- **Cohort selection on top of panel selection.** Clinical-sequencing cohorts are dominated
  by advanced / metastatic / pre-treated disease, biasing observed gene-frequencies for
  resistance-associated alterations. Zehir 2017 quantifies AR mutations 18% in metastatic
  prostate vs 1% in TCGA, ESR1 11% in metastatic breast vs 4% in TCGA. This is a *cohort*
  bias on top of the *panel* bias.

## Current State of Knowledge

The cancer-genomics literature **acknowledges panel bias as a first-order concern but does
not publish ready-to-use harmonization corrections**. This recurring theme spans Batches 1–6:

- AACR GENIE 2017 documents the 44-gene core + 12-panel structure but does not publish a
  weighted normalization scheme.
- Pugh 2022 reports a TCGA-vs-GENIE concordance check (median weighted RMSD 0.32) and
  mentions a TMB harmonization model — neither quantified, neither released as a tool.
- Chakravarty & Solit 2021 reviews panel platforms but emphasizes clinical utility / cfDNA /
  signatures rather than cross-platform comparability.
- Bandlamudi 2026 introduces a "non-canonical context" framework that implicitly *requires*
  panel-aware analysis (otherwise the ~1/3 non-canonical drivers are confounded with panel
  coverage), but does not publish a panel-correction recipe.
- Ellrott 2018 (MC3) re-calls all TCGA exomes uniformly — solving panel heterogeneity for
  the TCGA portion of any cross-study cohort by converting it to a single WES MAF.

## Controversies & Open Questions

- **Panel-intersection vs callability-denominator correction.** Two competing schools:
  (a) restrict cross-study comparisons to the *intersection* of panel BEDs (loses most of
  the data); (b) keep all data but compute per-(study, gene) callable-region length and use
  that as the ratio denominator. Empirical evidence on which is less biased is sparse.
- **Should multiple panel versions in a cohort (IMPACT-341/410/468/505) be treated as one
  panel or four?** The progressive addition of genes means earlier samples are missing
  callable regions for later-added genes. Current practice (cBioPortal) treats them as one
  pooled cohort.
- **Are TMB and signature calls panel-comparable at all?** Alexandrov 2020 says signature
  decomposition needs WES/WGS power (panel data needs SigMA or coarse flags); TMB needs
  per-panel calibration that no consortium has published.

## Relevance to This Project

**This is the #1 interpretive caveat for our pipeline outputs.** Our `gene_cancer.feather`
and clustering outputs aggregate across heterogeneous panels with no callability adjustment.
Concretely:

- A gene that's only on the large hybrid-capture panels will appear under-mutated in any
  cancer type dominated by small-amplicon-panel studies — even if its true mutation rate is
  identical.
- A gene on every panel still has different per-gene region length across panels (the APC
  ~10× example) — naive pooled mutation counts inflate the contribution of large-region
  panels.
- Resistance-associated alterations (AR, ESR1) will be inflated in cohorts dominated by
  clinical-sequencing studies relative to TCGA-derived cohorts.

## Pipeline Implications

Three concrete actions emerged from cross-batch reading:

1. **Build per-(study, gene) callability from GENIE BEDs.** `process_genie_panel_coverage.py`
   + Snakemake rule already wired (Batch 5+6 detour). Manual prerequisite: download GENIE
   release from Synapse `syn24179663`. Once ingested, `summary/mut/table/*` outputs should
   either restrict to a panel-intersection BED or report a callable-region-weighted ratio.
2. **Switch the TCGA portion of our cohort to MC3** (Ellrott 2018; Synapse `syn7214402` or
   GDC). One unified MAF replaces heterogeneous per-study cBioPortal TCGA MAFs (~25% more
   calls, single schema, documented filter vocabulary). **Not yet implemented.**
3. **Flag the cohort-vs-panel two-axis bias explicitly** in any cross-study output: every
   per-gene ratio should carry a per-cohort callable-fraction + a cohort-stage descriptor
   (primary vs metastatic vs treatment-resistance). Currently absent.

## Key References

- AACRGENIEConsortium2017 — 44-gene core, 12-panel launch structure, APC ~10× example.
- Pugh2022 — 91-assay v9.1 release; per-assay BEDs in Synapse syn24179663.
- Zehir2017 — MSK-IMPACT panel-version progression + matched-buffy-coat design.
- Bandlamudi2026 — 50k cohort spanning multiple IMPACT panel versions; "non-canonical
  context" finding implicitly requires panel-aware analysis.
- Ellrott2018 — MC3 unified TCGA WES MAF; eliminates panel heterogeneity for TCGA portion.
- ChakravartySolit2021 — clinical-profiling review of panel platforms (`status: abstract-read`,
  full-text not yet accessed).
- Bolton2020 — matched-vs-unmatched normal calling differential, esp. for CH-driver genes.
