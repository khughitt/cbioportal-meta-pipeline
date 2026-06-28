---
type: question
title: Do length-correlated functional gene categories generically produce spurious
  raw-count enrichment, and should the pipeline ship a length-aware gene-set enrichment
  guard?
status: active
created: '2026-06-07'
updated: '2026-06-28'
id: question:0038-length-correlated-geneset-spurious-enrichment
ontology_terms:
- gene length
- gene set enrichment
- passenger mutation
- methodology
datasets: []
source_refs:
- paper:Lu2026
related:
- method:length-aware-geneset-enrichment
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- hypothesis:0003-gene-length-confounds-literature-attention
- question:0032-neural-gene-length-null
- question:0031-residual-gene-length-signal-mechanism
---

# Do length-correlated functional gene categories generically produce spurious raw-count enrichment, and should the pipeline ship a length-aware gene-set enrichment guard?

## Summary

The neural-gene observation (`hypothesis:0012-neural-gene-enrichment-length-histology-artifact`) is likely an instance of a general failure mode:
**any** functionally-defined gene set whose members are systematically long (neural/synaptic,
cell-adhesion, ECM, ion channels, large gene families) will appear enriched among top-mutated
genes purely from length-proportional passenger mutation. This asks whether that genericity is
real and whether the pipeline should ship a reusable length-/histology-aware gene-set enrichment
guard (`method:length-aware-geneset-enrichment`) rather than re-deriving the correction per claim.

## Why It Matters

- Turns a one-off neural-gene correction into reusable infrastructure for
  `hypothesis:0002-cross-study-ranking-divergence-is-structured`,
  `hypothesis:0003-gene-length-confounds-literature-attention`,
  `question:0031-residual-gene-length-signal-mechanism`, and any
  future gene-set claim.
- A negative-control battery (TTN/MUC/CSMD-class large genes, olfactory receptors) calibrates
  *every* enrichment statement, preventing the next "category X is highly mutated" artifact.
- Risk if unanswered: repeated false-positive gene-set enrichment narratives across the project.

## Current Evidence

- `hypothesis:0003-gene-length-confounds-literature-attention` establishes the length bias on mutation counts and literature attention.
- `paper:Lu2026` flags the neural/IgCAM overlap as length-expected without selection.
- The project already corrects length for individual rankings (dndscv) but has no gene-**set**
  guard with built-in negative controls.

## Thoughts

- Best current interpretation: the failure mode is generic; a guard with a control-set battery
  is the right abstraction.
- Major uncertainty: best estimand (logistic partial-enrichment vs length-matched permutation vs
  dN/dS-ranked) and how to fold histology in without double-counting
  `question:0033-neural-enrichment-cns-exclusion` / `question:0034-neuroendocrine-histology-confound`.

## Connections to Project

- Related hypotheses: `hypothesis:0012-neural-gene-enrichment-length-histology-artifact`,
  `hypothesis:0003-gene-length-confounds-literature-attention`,
  `hypothesis:0002-cross-study-ranking-divergence-is-structured`
- Required data or analyses: implement `method:length-aware-geneset-enrichment`; validate on the
  neural set + control battery (first consumer = `task:t217` / `task:t221`).
- Priority level: P2 (reusable; do alongside the neural program)

## Related

- Topic notes: `theme:0002-cancer-neuroscience-in-a-mutation-only-pipeline-expression-not-mutation`,
  `question:0032-neural-gene-length-null`
- Article notes: paper:Lu2026
- Methods/Datasets: method:length-aware-geneset-enrichment; dndscv path; UniProt lengths
