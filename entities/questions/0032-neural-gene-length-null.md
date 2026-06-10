---
type: question
title: Does the apparent neural-gene enrichment in top-mutated genes survive gene-length
  normalization, or is it a length artifact?
status: active
created: '2026-06-06'
updated: '2026-06-06'
id: question:0032-neural-gene-length-null
ontology_terms:
- gene length
- somatic mutation
- passenger mutation
- neural genes
datasets: []
source_refs:
- paper:Lu2026
- paper:Mancusi2023
related:
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- hypothesis:0003-gene-length-confounds-literature-attention
- question:0031-residual-gene-length-signal-mechanism
---

# Does the apparent neural-gene enrichment in top-mutated genes survive gene-length normalization, or is it a length artifact?

## Summary

The candidate neural genes (NKAIN2, KCNIP4, TAFA2/FAM19A2, RIT2, CALN1, RBFOX1, LSAMP, SGCZ,
OPCML) are unusually large adhesion / axon-guidance / ion-channel / splicing-regulator genes.
This asks whether their high raw mutation counts are explained entirely by gene length — the
project's known passenger-mutation confound — or whether a neural-label enrichment persists
after normalizing to mutations-per-callable-kb and to a dN/dS-style background model.

## Why It Matters

- Decides whether there is *anything to explain*. If the enrichment is pure length, H1/H3
  interpretation is moot and the observation is a known artifact (`hypothesis:0003`).
- Cheapest, most decisive test in the whole program; gates all downstream neural-biology work.
- Risk if unanswered: building a neural-hijacking narrative on a length artifact.

## Current Evidence

- The 21-paper cancer-neuroscience batch names *none* of the candidate genes; canonical
  effectors (NLGN3, ADRB2, NTRK1/2) are shorter and absent from our list.
- `paper:Lu2026` notes the candidate IgCAM/axon-guidance overlap is "expected under
  length-proportional background mutation without any selection."
- Project already has dndscv output and `data/uniprotkb_hsapiens_protein_lengths.tsv.gz`.

## Thoughts

- Best current interpretation: most of the signal is length (P1 of `hypothesis:0012`).
- Major uncertainty: whether a small residual survives, and in which cancer types.

## Connections to Project

- Related hypotheses: h12 (P1), h03, h01
- Required data or analyses: top-N raw-count list vs length-normalized list; neural-label
  enrichment statistic on both; reuse dndscv per-gene q-values; UniProt protein lengths +
  Ensembl CDS length.
- Priority level: P1 (do first)

## Related

- Topic notes: topic:perineural-invasion-axon-guidance-genes
- Article notes: paper:Lu2026, paper:Mancusi2023
- Methods/Datasets: dndscv path; data/uniprotkb_hsapiens_protein_lengths.tsv.gz
