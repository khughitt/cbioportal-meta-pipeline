---
type: paper
title: Insertions and Deletions Target Lineage-Defining Genes in Human Cancers
status: active
created: '2026-04-13'
updated: '2026-06-28'
id: paper:Imielinski2017
tags:
- background-mutation-rate
- driver-detection
- covariate-regression
- indel
- lineage
ontology_terms:
- MeSH:D009154
source_refs:
- paper:Imielinski2017
related:
- paper:Lawrence2014
- paper:Martincorena2017
- paper:Bailey2018
- paper:Canisius2016
dataset_usage:
- ref: dataset:tcga
  role: analyzed
  overlap: full
---

# Insertions and Deletions Target Lineage-Defining Genes in Human Cancers

- **Authors:** Marcin Imielinski, Guangwu Guo, Matthew Meyerson
- **Year:** 2017
- **Journal:** Cell 168(3):460-472.e14
- **DOI/URL:** https://doi.org/10.1016/j.cell.2016.12.025
- **PMID:** 28089356
- **OpenAlex ID:** W2573077199
- **BibTeX key:** Imielinski2017
- **Source:** OpenAlex + PubMed (verified 2026-04-13)
- **Method name:** **FishHook**
- **Software:** https://github.com/mskilab-org/fishHook

## Key Contribution

This indel-driver note links paper:Lawrence2014, paper:Martincorena2017, paper:Bailey2018, and paper:Canisius2016.

Introduces the **FishHook** statistical framework — a **Gamma-Poisson regression** on
somatic mutation counts along the genome that **corrects for known covariates of neutral
mutation** (chromatin state, replication timing, local nucleotide composition, gene length,
GC content). Applied to indel density in 702 tumor WGS/WES samples, the authors identify
lineage-defining transcription factors as a previously under-appreciated class of
indel-targeted drivers. The FishHook framework itself is now a widely-reused tool for
background-rate-corrected recurrence testing in both coding and non-coding regions.

## Methods

- **Model:** per-region mutation counts ~ Negative Binomial with mean modeled by Gamma-Poisson
  GLM on a set of continuous/categorical covariates of neutral mutation rate.
- **Output:** per-region significance of enrichment/depletion of observed counts vs. the
  covariate-adjusted expected rate.
- Accepts arbitrary genomic region definitions (genes, exons, tiles, regulatory elements).
- Handles coverage variation explicitly via offsets.

## Key Findings

- Indels show distinct mutational hotspots from SNVs; clustering on transcription factors
  like GATA3, RUNX1, FOXA1, PAX5 in lineage-appropriate cancers.
- The **FishHook framework** generalizes beyond this paper and is the reference
  implementation for covariate-aware background-rate correction in cancer genomics.

## Relevance

Complementary to the mutual-exclusivity axis: FishHook addresses the *gene-level
significance* problem (is this gene mutated more than expected under the background model?)
while DISCOVER/SELECT/WeSME address the *pair-level interaction* problem. The cbioportal
pipeline currently applies only a coarse per-study gene-coverage filter and raw counts +
sample-level ratios; FishHook-style covariate regression is the principled replacement if
we want to move from coverage to proper background normalization. Especially relevant when
pooling across panel assays with very different genomic targets (MSK-IMPACT vs
FoundationOne vs GENIE assays).

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Gamma-Poisson regression on covariates | Replacement for raw-count gene ranking | Covariates would include panel coverage, gene length, perhaps sample-level TMB. |
| Region-tile offset | Panel coverage encoding | Direct mapping: per-study panel BED → per-gene offset. |
| Per-region significance | Per-gene per-study *p*-value | Natural input to meta-analytic aggregation. |

## Limitations

- R-based; heavier than the pipeline's current Python-first stack.
- Requires covariate tables (chromatin, replication timing) not currently stored in `data/`.
- Originally applied to WGS/WES — adapting to panel-based cBioPortal + GENIE studies
  requires thoughtful encoding of panel coverage as an offset.

## Model / Tool Availability

- **R package:** https://github.com/mskilab-org/fishHook
- Tutorial: https://mskilab.com/fishHook/tutorial.html
- License: check current repo.
- Depends on GenomicRanges / rtracklayer / data.table.

## Follow-up

- Investigate whether FishHook's R backend can be invoked via a Snakemake rule
  (analogous to the existing `run_dndscv.R`).
- Compare FishHook-style per-gene background correction to the simpler
  UniProt-protein-length normalization the pipeline currently uses.
- Cross-reference Lawrence 2014 [@Lawrence2014] (MutSigCV) for the conceptual predecessor of covariate-
  aware background modeling.
