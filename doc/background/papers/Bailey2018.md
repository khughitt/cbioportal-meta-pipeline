---
id: paper:Bailey2018
type: paper
title: Comprehensive Characterization of Cancer Driver Genes and Mutations
status: read
ontology_terms: []
source_refs:
- article:Bailey2018
related:
- paper:Ellrott2018
- topic:cancer-driver-genes
- topic:pan-cancer-mutation-landscape
created: '2026-04-13'
updated: '2026-04-13'
dataset_usage:
- ref: dataset:tcga-pancanatlas
  role: analyzed
  overlap: unknown
---

# Comprehensive Characterization of Cancer Driver Genes and Mutations

- **Authors:** Bailey MH, et al.
- **Year:** 2018
- **Journal:** Cell
- **PMID:** 30096302
- **BibTeX key:** Bailey2018

## Key Contribution

Produces a PanCanAtlas consensus driver-gene catalog by combining 26 computational
driver-detection tools applied to the MC3 mutation call-set across 9,423 TCGA tumor exomes
(33 cancer types). Yields a pan-cancer list of **299 unique driver genes** plus per-cancer-type
driver rosters and ~3,400 candidate driver missense mutations, serving as a reference driver
catalog downstream analyses can benchmark against.

## Methods

**Input data.** 9,423 TCGA tumor exomes (~9,079 after filtering) across all 33 cancer types,
using the MC3 consensus mutation calls (Ellrott2018), which are themselves a 7-caller consensus.
1,457,702 somatic mutations entered the discovery set.

**26 tools, two phases.** *Phase 1 — gene discovery (8 tools):* frequency/recurrence
(MuSiC2, MutSig2CV), feature/ratiometric (20/20+, CompositeDriver, OncodriveFML), clustering
(OncodriveCLUST), and domain-based (e-Driver, ActiveDriver). *Phase 2 — mutation scoring and
validation (18 additional tools):* population-based (SIFT, PolyPhen2, VEST, MutationAssessor),
cancer-focused (CHASM, CanDrA, fathmm, transFIC), 3D-structure/hotspot (HotSpot3D, HotMAPS,
3DHotSpots.org, e-Driver3D), network/omics (DriverNet, OncoIMPACT), and clinical-annotation
(PHIAL, DEPO), plus a novel meta-tool (CTAT).

**Consensus scoring.** Genes receive a weighted sum of tool votes; tools flagged as outliers
(poor overlap with known cancer genes, deviant p-value distribution, inflated significant-gene
counts) are down-weighted to 0.5. A gene is called at score ≥ 1.5 (≥2 non-outlier tools, or 3
with penalty). Genes are assigned **Gold / Silver / Bronze confidence tiers** by consensus
strength.

**Per-cancer and pan-cancer.** Each of the 33 cancer types is analyzed independently, and a
combined PanCancer run catches signals diluted across tissues.

**Validation.** Recovery of published cancer-type gene markers (≥80% in 20 of 31 types);
Ba/F3 / MCF10A functional assays on 579 candidate missense drivers (85% of the triple-predicted
set validated).

## Key Findings

- **299 consensus driver genes** pan-cancer: 258 from systematic scoring plus 41 rescued via
  omics/network tools or literature support.
- **Per-cancer-type drivers span two orders of magnitude:** UCEC tops the list with ~55 driver
  genes; KICH has only 2. Long-tail structure across the 33 types.
- **Long-tail vs. recurrent split.** 142 driver genes are tumor-type-specific (single cancer),
  87 are shared across 2+ types, and 29 are detectable only in the pooled PanCancer run. TP53
  shows signal in 27/33 cancer types; PIK3CA, KRAS, PTEN, ARID1A each in 15+.
- **~59 novel drivers** not previously in the core literature/CGC (e.g., GNA13 in BLCA, RRAS2
  in UCEC, KIF1A in HNSC).
- **TSG vs. oncogene mechanics.** TSG/OG ratio varies widely by tissue; oncogenes enriched for
  missense hotspots, TSGs for truncating/frameshift events. CDH1 is tissue-dependent
  (truncating in BRCA, missense in STAD).
- **Mutation-level results.** ~3,400 candidate missense driver mutations identified by ≥2
  approaches. **19% of driver mutations (1,719 events in 1,431 patients)** fall in genes that
  are drivers in a *different* cancer type than the patient's — an argument for tissue-agnostic
  trial design. **57% of tumors** carry a clinically actionable event.
- **Tool agreement is modest.** The union of the 8 phase-1 tools yields 2,101 candidate genes;
  consensus filtering collapses this to 299 — individual tools produce heavily inflated lists.

## Relevance

External reference driver list for evaluating which of this pipeline's high-frequency genes are
already known drivers vs. potentially novel (or artifactual) associations.

## Limitations

- Coding mutations only — non-coding / promoter / UTR / splice-region drivers (e.g., *TERT*
  promoter) are excluded from the primary detection pipeline.
- Does not directly incorporate copy-number or structural-variant-only drivers; CNA is used
  only as supporting annotation in some tools.
- Bound by MC3 quality: tumor-only WES, matched-normal exome, no tumor-only WGS or RNA
  confirmation for most samples, inheriting MC3's caller-bias and coverage-bias issues.
- Restricted to the 33 TCGA cancer types — pediatric cancers, rare subtypes, and non-TCGA
  cohorts (e.g., MMRF myeloma, Pediatric PanCanAtlas) are not represented.
- Consensus calibrated on MC3 itself; generalization to other mutation callers or non-TCGA
  cohorts not guaranteed.
- Gene-level calls do not resolve isoform/domain-level or context-specific driverhood.

## Follow-up

- **Ellrott2018** — upstream MC3 mutation call-set consumed as input here.
- **Tate2019 (COSMIC CGC)** — independent curated driver reference for overlap/benchmarking.
- Downstream PanCanAtlas analyses use this list as the canonical driver annotation
  (pathway analyses, actionability surveys, signature association).
- For this project: use **Table S1** (pan-cancer) and per-cancer-type tables to classify the
  meta-analysis's high-frequency genes as known drivers vs. long-tail / novel candidates.
