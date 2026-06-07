---
id: "question:q038-length-correlated-geneset-spurious-enrichment"
type: "question"
title: "Do length-correlated functional gene categories generically produce spurious raw-count enrichment, and should the pipeline ship a length-aware gene-set enrichment guard?"
status: "active"
ontology_terms:
  - gene length
  - gene set enrichment
  - passenger mutation
  - methodology
datasets: []
source_refs:
  - "paper:Lu2026"
related:
  - "method:length-aware-geneset-enrichment"
  - "hypothesis:h12-neural-gene-enrichment-length-histology-artifact"
  - "hypothesis:h03-gene-length-confounds-literature-attention"
  - "question:q032-neural-gene-length-null"
  - "question:q031-residual-gene-length-signal-mechanism"
created: "2026-06-07"
updated: "2026-06-07"
---

# Do length-correlated functional gene categories generically produce spurious raw-count enrichment, and should the pipeline ship a length-aware gene-set enrichment guard?

## Summary

The neural-gene observation (`hypothesis:h12`) is likely an instance of a general failure mode:
**any** functionally-defined gene set whose members are systematically long (neural/synaptic,
cell-adhesion, ECM, ion channels, large gene families) will appear enriched among top-mutated
genes purely from length-proportional passenger mutation. This asks whether that genericity is
real and whether the pipeline should ship a reusable length-/histology-aware gene-set enrichment
guard (`method:length-aware-geneset-enrichment`) rather than re-deriving the correction per claim.

## Why It Matters

- Turns a one-off neural-gene correction into reusable infrastructure for h02/h03/q031 and any
  future gene-set claim.
- A negative-control battery (TTN/MUC/CSMD-class large genes, olfactory receptors) calibrates
  *every* enrichment statement, preventing the next "category X is highly mutated" artifact.
- Risk if unanswered: repeated false-positive gene-set enrichment narratives across the project.

## Current Evidence

- `hypothesis:h03` establishes the length bias on mutation counts and literature attention.
- `paper:Lu2026` flags the neural/IgCAM overlap as length-expected without selection.
- The project already corrects length for individual rankings (dndscv) but has no gene-**set**
  guard with built-in negative controls.

## Thoughts

- Best current interpretation: the failure mode is generic; a guard with a control-set battery
  is the right abstraction.
- Major uncertainty: best estimand (logistic partial-enrichment vs length-matched permutation vs
  dN/dS-ranked) and how to fold histology in without double-counting q033/q034.

## Connections to Project

- Related hypotheses: h12, h03, h02
- Required data or analyses: implement `method:length-aware-geneset-enrichment`; validate on the
  neural set + control battery (first consumer = t217/t221).
- Priority level: P2 (reusable; do alongside the neural program)

## Related

- Topic notes: theme:cancer-neuroscience-in-a-mutation-only-pipeline
- Article notes: paper:Lu2026
- Methods/Datasets: method:length-aware-geneset-enrichment; dndscv path; UniProt lengths
