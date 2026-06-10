---
type: topic
title: Multi-omics cancer analysis
status: active
created: '2026-04-13'
updated: '2026-04-13'
id: topic:multi-omics-cancer-analysis
ontology_terms: []
source_refs: []
related:
- paper:Hoadley2018
- paper:Jee2024
- paper:PCAWG2020
- paper:SanchezVega2018
- topic:pan-cancer-interpretive-frames
---

# Multi-omics cancer analysis

## Summary

Integrating somatic mutations with other modalities — copy-number alterations (CNA), gene
expression (mRNA), DNA methylation, miRNA, protein abundance (RPPA), structural variants,
clinical outcomes. Currently out-of-scope for this pipeline (mutation-only), but the intended
extension path noted in the project README.

## Key Concepts

- **Per-platform vs joint integration.** Two main approaches:
  - *Per-platform clusterings → consensus* (COCA: cluster-of-cluster-assignments) — easier,
    avoids platform-specific weighting questions.
  - *Joint multivariate latent-variable models* (iCluster, MOFA, JIVE) — harder, but exposes
    cross-platform patterns. Hoadley 2018 uses iCluster across CNA + methylation + mRNA + miRNA
    on 9,759 TCGA tumors.
- **Variance contributions.** Hoadley 2018: CNA ~47%, transcriptome (mRNA + miRNA) ~42%,
  methylation ~11% in their iCluster decomposition. CNA dominates the multi-omic signal.
- **Mutations are typically excluded from multi-omic clustering due to sparsity** (Hoadley 2018
  excluded mutations from iCluster input for this reason). Mutations are usually overlaid post-
  hoc rather than used to drive integration.
- **Mutation + outcome integration.** Jee 2024 (MSK-CHORD) integrates MSK-IMPACT mutation calls
  with EHR-derived clinical outcomes via automated extraction; bridges mutation data to
  treatment / response / survival without manual chart review.
- **Pathway-level integration** (Sanchez-Vega 2018) collapses mutation + CNA + fusion + methylation
  per gene onto pathway membership. Different from sample-level multi-omic clustering.

## Current State of Knowledge

The PanCanAtlas suite (2018) is the most thorough pan-cancer multi-omic benchmark on TCGA.
Hoadley 2018's 28-cluster iCluster taxonomy + Sanchez-Vega 2018's pathway view + Bailey 2018's
driver-gene catalog form a complementary tri-axis on the same ~10,000 tumor cohort.

For non-TCGA / panel-based cohorts, multi-omic integration is much sparser. MSK-CHORD (Jee 2024)
adds clinical outcomes; Bandlamudi 2026 adds CCF / clonality / HLA LOH per sample.

## Controversies & Open Questions

- **Which modalities to add first?** For a mutation-centric pipeline like ours, the obvious next
  axis is CNA (enables M/C-class hyperbola, Hoadley-style integrated clustering, Sanchez-Vega
  pathway membership). Expression / methylation are larger lifts.
- **Per-study vs per-patient integration.** Most cBioPortal studies bundle modalities at sample
  level; some have multiple samples per patient (primary + metastatic, or longitudinal). Our
  pipeline's `summary/mut/matrix/gene_patient.feather` already collapses to patient level for
  mutation; multi-omic extension needs to decide on a consistent abstraction.
- **Batch effects across modalities** (especially methylation array versions, RPPA antibody
  panels) — non-trivial and not yet addressed.

## Relevance to This Project

Roadmap topic. Concrete near-term extensions surfaced from cross-batch reading:
1. **CNA ingestion** as the simplest first multi-omic axis. Enables `topic:pan-cancer-interpretive-frames`
   M/C-class descriptor and Hoadley-style cluster comparison.
2. **Pathway-level overlay** (Sanchez-Vega 2018 Tables S2/S3) — pathway memberships for 10
   canonical signaling pathways. Already queued as task t049.
3. **Outcome integration** (MSK-CHORD-style) — much further out; requires clinical-data
   harmonization across cohorts.

## Key References

Hoadley2018 (PanCanAtlas multi-omic flagship), SanchezVega2018 (pathway-level integration),
Jee2024 (MSK-CHORD outcome integration), PCAWG2020 (WGS-based multi-omic complement). See
`topic:pan-cancer-interpretive-frames` for the comparative-framework synthesis.
