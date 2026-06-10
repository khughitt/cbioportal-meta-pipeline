---
type: topic
title: 'Mutational-signature topography: association with replication timing, chromatin,
  and local genomic features'
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: topic:signature-topography-genomic-features
ontology_terms: []
datasets:
- dataset:replication-timing-constitutive-regions
- dataset:pcawg
source_refs: []
related:
- paper:Otlu2023
- paper:GonzalezPerez2019
- paper:Yaacov2023
- paper:Spisak2025
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- hypothesis:0003-gene-length-confounds-literature-attention
- question:0003-replication-timing-as-gene-level-mutation-rate-confounder
- topic:dna-damage-repair-signature-mechanisms
---

# Mutational-signature topography: association with replication timing, chromatin, and local genomic features

## Summary

Mutational signatures are not uniformly distributed across the genome: their density covaries with
**replication timing (RT), chromatin accessibility, nucleosome positioning, transcription, and
nucleotide context**. This topic collects the topography literature and connects it to two existing
project threads — the gene-level mutation-rate confounders behind `hypothesis:0003` /
`question:0003`, and the agnostic aetiology association of `hypothesis:0007`.

## What the literature establishes

- **Comprehensive topography map.** `paper:Otlu2023` maps 76 signatures against 516 genomic features
  across 5,120 WGS tumors / 40 cancer types — the reference atlas for which signatures are early- vs
  late-replicating, transcribed- vs untranscribed-strand biased, etc.
- **Local determinants are damage × repair, not damage alone.** `paper:GonzalezPerez2019` shows
  nucleosomes, TF-binding sites, and transcription modulate mutation rate by differentially gating
  damage and repair — the mechanistic basis for signature spatial structure.
- **RT bias is largely conserved into cancer.** `paper:Yaacov2023` (already a project paper) shows
  most processes keep their RT bias from normal tissue into tumor, with SBS1 (clock-like CpG
  deamination) the key exception (late-RT-enriched in normal, bias lost in cancer).
- **Flat clock-like signatures funnel.** `paper:Spisak2025` argues SBS5 aggregates polymerase/TLS
  errors from diverse damage — relevant because flat signatures are the hardest to localise and the
  most artefact-prone in topography analysis.

## Why it matters for the project

- **Confounder control (h03/q003).** Replication timing is already on record as a candidate
  gene-level mutation-rate confounder (`question:0003`); the topography literature says signature
  *composition*, not just total rate, varies with RT — so any gene × signature claim must condition
  on RT/chromatin, not only on tissue. The `dataset:replication-timing-constitutive-regions` entity
  is the existing substrate for this.
- **h08 discovery guard.** A covariate↔signature association that is really an RT/chromatin artefact
  is rival R4 (batch/structural) in `method:h08-agnostic-association-model`; the `paper:Otlu2023`
  feature atlas is a ready negative-control feature set.
- **Bounds for SBS40-vs-SBS5 (q023).** Topographic features may help separate the two flat
  clock-like signatures that expression modules alone may not resolve.

## Open questions / gaps

- The project operates mostly on panel/WES coding regions, where genome-wide topography is largely
  invisible — topography analysis is realistic only on WGS substrates (`dataset:pcawg`, MC3 with
  caution). This bounds how far the project can exploit topography directly vs. cite it as a
  confounder caveat.
- Whether RT conditioning materially changes the h08 positive-control recovery is untested.

## Related

- Papers: `paper:Otlu2023`, `paper:GonzalezPerez2019`, `paper:Yaacov2023`, `paper:Spisak2025`
- Hypotheses: `hypothesis:h08-...`, `hypothesis:h03-...`
- Questions: `question:0003-replication-timing-as-gene-level-mutation-rate-confounder`
- Topics: `topic:dna-damage-repair-signature-mechanisms`
- Datasets: `dataset:replication-timing-constitutive-regions`, `dataset:pcawg`
