---
id: paper:Lawrence2014
type: paper
title: Discovery and saturation analysis of cancer genes across 21 tumour types
status: read
ontology_terms: []
source_refs:
- article:Lawrence2014
related:
- paper:Bailey2018
- paper:Kandoth2013
- topic:cancer-driver-genes
- topic:mutation-rate-normalization
created: '2026-04-13'
updated: '2026-04-13'
---

# Discovery and saturation analysis of cancer genes across 21 tumour types

- **Authors:** Lawrence MS, et al.
- **Year:** 2014
- **Journal:** Nature
- **PMID:** 24390350
- **DOI:** 10.1038/nature12912
- **BibTeX key:** Lawrence2014

## Key Contribution

Applies MutSigCV — a gene-specific background-mutation-rate model — to 4,742 tumour/normal exome pairs across 21 cancer types, producing the first unified pan-cancer significantly-mutated-gene (SMG) catalogue corrected for the ~5-orders-of-magnitude variation in background rate across genes and tumours. Introduces the companion *saturation analysis*: by down-sampling and extrapolating the rate at which new SMGs appear, the authors estimate the cohort size per tumour type required to reach near-complete driver-gene discovery. The central claim is quantitative — 600–5,000 samples per tumour type, scaling with background mutation frequency — rather than a list of new genes per se.

## Methods

MutSigCV corrects three sources of false-positive inflation that plague naive recurrence counts: (1) gene-specific background rate, modelled as a function of covariates known to track mutation rate — gene expression level, DNA replication timing, and HiC-based chromatin compartment (open vs closed chromatin) <!-- UNVERIFIED: the 2014 paper references the covariates via Lawrence2013 rather than re-listing them -->; (2) patient-specific mutation rate and spectrum (six context categories: transitions at CpG, transitions at other C:G, transversions at C:G, A:T mutations, null/indel, plus gene-specific composition); (3) gene-specific composition of these contexts. The null is built from silent and non-coding mutations in the target gene plus its covariate-space neighbourhood ("bagel"). Two orthogonal tests are combined: MutSigCL (positional clustering / hotspots) and MutSigFN (functional impact via phyloP46way conservation). Significance is called at FDR q ≤ 0.1. Cohort: 4,742 tumour-normal exome pairs, 21 cancer types (35–892 samples each), 12 TCGA + 14 non-TCGA Broad projects, ~3.08M SNVs and 77,270 indels. Saturation analysis down-samples each cohort and extrapolates the SMG discovery curve; required sample size is modelled as a function of each cancer's median background mutation frequency.

## Key Findings

224 genes reached significance in at least one tumour type (334 gene × tumour-type pairs); 114 genes were significant in the pooled pan-cancer analysis. The "Cancer5000" set contains 254 candidates and the stringent "Cancer5000-S" subset contains 219 (~40 expected false positives). Per-tumour SMG counts ranged from 1 (carcinoid, medulloblastoma, neuroblastoma) to 58 (endometrial); breast cancer yielded 32. MutSigCV recovered 60 of 82 relevant Cancer Gene Census genes; 8 needed >1,000 samples to clear the threshold. 33 newly highlighted genes span anti-proliferation (ARHGAP35, MGA, IRF6, DNER), proliferation (RHEB, RHOA, SOS1, ELF3, SGK1, MYOCD), apoptosis, genome stability (RAD21, TP53BP1), chromatin regulation (SETDB1, CHD8, EZH1), immune evasion (HLA-B, TAP1, CD1D), and RNA processing (PCBP1, QKI). Saturation analysis: genes mutated at ≥20% are near-saturated; 5–10% genes scale linearly; <5% genes accelerate. Near-saturation required ~650 samples for neuroblastoma (0.5 mut/Mb) but ~5,300 for melanoma (12.9 mut/Mb). 17 of 21 cancer types lacked power to detect 5% drivers — i.e., only 4 tumour types were close to saturated at publication.

## Relevance

The MutSigCV-driven significantly-mutated-gene method that defined the field's standard of
"controlling for background mutation rate" before claiming a gene is a driver. Methodological
peer of dNdScv (Martincorena2017) and the consensus approach of Bailey2018. The "saturation"
analysis quantifies how many cancer genes remain undiscovered as a function of cohort size —
relevant for understanding whether long-tail genes in our outputs are real or noise.

## Limitations

Scope is restricted to coding point mutations and short indels — amplifications, deletions,
translocations, non-coding drivers, and epigenomic events are not modelled, so genes driven
primarily by CNA or fusion (e.g., many paediatric drivers) are under-recovered. Low-recurrence
drivers acting in small sub-cohorts fall below FDR even with covariate correction, and 22
known CGC genes failed detection at cohort sizes available in 2014. The saturation
extrapolation assumes the mutation-rate model is well-calibrated and that the discovery curve
is smooth — mis-estimated background rates (e.g., from poor covariate coverage for a given
tumour type or lineage-specific chromatin state) would bias both the SMG list and the
required-sample-size projections. Covariate data (expression, replication timing) are drawn
from reference cell lines rather than tumour-matched measurements, so tissue-specific
background-rate biases are a known residual confounder. Authors flag ~40 expected false
positives in Cancer5000-S itself.

## Follow-up

Bailey2018 (PanCanAtlas consensus driver list) directly extends this framework by
intersecting MutSigCV with 25+ other driver callers across the full TCGA PanCanAtlas —
explicitly motivated by the finding here that MutSigCV alone misses some known drivers.
Martincorena2017 (dNdScv) proposes an alternative that relies on the dN/dS selection
signal rather than excess mutation burden over a covariate-regressed null, addressing the
covariate-accuracy limitation. The saturation curves here also motivated the
Hoadley2018 / Ellrott2018 PanCanAtlas cohort-scale efforts and framed the continuing push
for per-tumour-type cohorts >1,000 samples (e.g., GENIE, ICGC/PCAWG for non-coding).
