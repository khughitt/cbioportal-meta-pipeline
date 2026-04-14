---
id: "article:Ellrott2018"
type: "article"
title: "Scalable Open Science Approach for Mutation Calling of Tumor Exomes Using Multiple Genomic Pipelines"
status: "summarized"
ontology_terms: []
datasets: ["tcga-mc3"]
source_refs: ["cite:Ellrott2018"]
related: ["article:Bailey2018", "topic:targeted-panel-sequencing-bias"]
created: "2026-04-13"
updated: "2026-04-12"
---

# Scalable Open Science Approach for Mutation Calling of Tumor Exomes Using Multiple Genomic Pipelines

- **Authors:** Ellrott K, et al.
- **Year:** 2018
- **Journal:** Cell Systems
- **PMID:** 29596782
- **BibTeX key:** Ellrott2018

## Key Contribution

MC3 (Multi-Center Mutation Calling in Multiple Cancers) — the canonical TCGA pan-cancer
somatic MAF produced by combining seven variant callers across ~10,000 tumor/normal exome
pairs from 33 cancer types. It is the reference call-set that subsequent pan-cancer driver
and signature analyses (e.g., Bailey2018, PCAWG companion work) compare against.

## Methods

**Cohort.** 10,510 tumor/normal exome pairs from 33 TCGA cancer types (final whitelist
11,069 pairs across 10,486 participants), with >400 TB of raw input.

**Seven callers, run in parallel.**
- SNV callers (5): MuTect, MuSE, SomaticSniper, RADIA, VarScan2.
- Indel callers (3): Pindel, Indelocator, VarScan2.

Each caller was run with author-recommended parameters; per-caller VCFs were merged and
re-annotated with VEP via `vcf2maf`.

**Consensus / filtering.** Rather than a strict N-of-7 vote, MC3 merges all caller output
and applies eight uniform post-hoc filters: `broad_PoN_v2`, `Common_in_ExAC`, `OxoG`,
`ContEst`, `StrandBias`, `NormalDepth` (`ndp`), `CaptureKit` (`bitgt`), and `NonExonic`.
A two-caller-agreement requirement is layered on for the public release; analysis showed
the two-caller rule outperforms any specific pairwise combination on validated sites
(stronger for SNVs than indels, where it inflates false negatives).

**Reproducibility infrastructure.** The full pipeline is described in Common Workflow
Language (CWL) with each tool wrapped in Docker. Compute was distributed across
DNANexus (primary calling, ~1.8M core-hours), Broad Firehose (MuTect, Indelocator),
ISB Cancer Genomics Cloud (OxoG), and the UCSC NCI cluster (GATK co-cleaning). Code at
`github.com/OpenGenomics/mc3`.

**MAF harmonization.** Two release tiers — controlled-access MAF (all calls + filter
flags, suitable for re-filtering) and open-access MAF (filtered: PASS-equivalent, exonic,
≥2 callers, no PoN/contest/wga/ndp/bitgt artifacts).

## Key Findings

- **Open-access MAF: 3,600,963 variants** from 10,295 tumors (3,427,680 SNVs +
  173,283 indels).
- **Per-caller behavior.** MuTect and MuSE have the highest pairwise agreement and the
  largest number of unique calls; SomaticSniper has the lowest FPR but the highest FNR;
  Pindel dominates indel volume but with sample-skewed artifacts (>130K calls from two
  samples).
- **Vs. PanCan12 single-caller MAFs (12 overlapping cancer types):**
  MC3 = 1,079,216 calls vs PanCan12 = 804,571; intersection = 717,326 (~89.5%
  concordance on PanCan12 sites). Net **~25% increase** in call set. Recovery >90% for
  HNSC/SKCM/BRCA/BLCA/COADREAD/UCEC, but only 33% for PAAD (low purity) and 44% for
  LAML (normal-contamination issues).
- **Validation.** Orthogonal data from 3,128 targeted deep-sequenced samples and 1,059
  WGS samples; the two-caller consensus had the highest TP rate. Authors caveat that the
  validation set is enriched for high-confidence sites and is not a true benchmarking
  cohort.

## Relevance

Reference WES-based call-set for contrasting against panel-based GENIE/MSK-IMPACT calls. Useful
when quantifying panel vs. WES differences for a given gene.

## Limitations

- **Tumor exomes only** — no WGS, no RNA-seq, no structural variants or copy number.
- **TCGA-only** cohort, with all attendant batch effects (capture kit heterogeneity, FFPE
  artifacts in some cohorts, variable normal quality — notably LAML peripheral blood).
- Validation set is biased toward high-confidence sites; quoted TP rates are not
  random-sample sensitivity/specificity.
- Two-caller rule under-calls indels relative to SNVs.
- Low-purity tumors (e.g., PAAD) systematically lose calls.

## Follow-up

- Bailey2018 — downstream driver-gene analysis built on MC3.
