---
type: question
title: "If any neural-gene enrichment survives length+histology correction, is it\
  \ fetal/developmental (oncofetal, H3) rather than adult-neural \u2014 and non-selective\
  \ rather than positively selected?"
status: active
created: '2026-06-06'
updated: '2026-06-06'
id: question:0036-oncofetal-fetal-vs-adult-neural-expression
ontology_terms:
- oncofetal reprogramming
- developmental expression
- BrainSpan
- positive selection
- neural genes
datasets: []
source_refs:
- paper:Cao2023
- paper:Huang2023a
- paper:Hanahan2023
related:
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- question:0035-label-free-neural-gene-definition
- question:0037-canonical-neural-gene-dnds-selection
- topic:oncofetal-developmental-reprogramming
---

# Is any residual neural-gene enrichment fetal/developmental (oncofetal, H3) rather than adult-neural and selected?

## Summary

`paper:Cao2023` argues tumors broadly de-repress the fetal transcriptome via SOX2/MYCN/Wnt/
Hedgehog reprogramming. Neural developmental genes are the largest class of developmentally-
regulated genes, so oncofetal de-repression could produce apparent "neural-gene" signal as a
diffuse byproduct (H3) — distinct from active, selected neural hijacking (H1). This asks
whether residual enrichment (after length + CNS + NET correction) carries the H3 signature:
fetal-brain expression bias and stemness correlation, with non-recurrent, non-selected mutation.

## Why It Matters

- Distinguishes the two surviving biological readings (H1 vs H3), which make opposite empirical
  predictions: H1 → recurrent/clustered/dN/dS>1 in specific effectors; H3 → diffuse, length-
  scaled, fetal-enriched, non-recurrent.
- Tells us whether the signal (if any) is "selection for neural function" or "a side effect of
  dedifferentiation."

## Current Evidence

- `paper:Cao2023`: oncofetal reprogramming reactivates SOX2/OLIG2/BMI1 (neural-developmental
  TFs); HCC reconstitutes a fetal-like TME (label-free, developmental-stage-defined).
- `paper:Huang2023a`: cancer stem cells transdifferentiate toward neurons via EGR2/SOX2/HOX.
- `paper:Hanahan2023`: neural co-option is non-mutational/epigenetic.

## Thoughts

- Best current interpretation: residual signal, if present, is developmental byproduct (H3),
  not selection (H1).
- Major uncertainty: whether matched expression data are available for enough cBioPortal
  studies to compute fetal-vs-adult and stemness scores per sample.

## Connections to Project

- Related hypotheses: h12 (P4)
- Required data or analyses: BrainSpan fetal-vs-adult expression ratio per gene; intersect
  with residual enriched set; correlate residual-gene mutation with stemness/oncofetal score
  (e.g. AFP/GPC3, Wnt/Hh activity) in studies with matched expression; recurrence/clustering
  check on residual genes.
- Priority level: P3 (after P1–P3 corrections)

## Related

- Topic notes: topic:oncofetal-developmental-reprogramming
- Article notes: paper:Cao2023, paper:Huang2023a, paper:Hanahan2023
- Methods/Datasets: BrainSpan, Allen Developing Human Brain Atlas, Human Cell Atlas fetal
