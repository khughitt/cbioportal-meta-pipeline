---
id: "method:length-aware-geneset-enrichment"
type: "method"
title: "Length- and histology-aware gene-set enrichment guard for mutation-count rankings"
status: "proposed"
created: "2026-06-07"
updated: "2026-06-07"
related:
  - "hypothesis:h12-neural-gene-enrichment-length-histology-artifact"
  - "hypothesis:h03-gene-length-confounds-literature-attention"
  - "hypothesis:h02-cross-study-ranking-divergence-is-structured"
  - "question:q038-length-correlated-geneset-spurious-enrichment"
  - "question:q031-residual-gene-length-signal-mechanism"
  - "question:q032-neural-gene-length-null"
  - "theme:cancer-neuroscience-in-a-mutation-only-pipeline"
---

# Length- and histology-aware gene-set enrichment guard for mutation-count rankings

A reusable guard that answers one question for **any** functionally-defined gene set `S`:
*is `S` over-represented among top-mutated genes beyond what gene length and cohort histology
predict?* The "neural gene" episode (`hypothesis:h12`) is one instance; the same machinery
applies to adhesion, ECM, synaptic, large-gene-family, or any annotation-defined set.

## Why a dedicated method

Raw mutation-count rankings inherit a strong length bias (Lawrence 2014; project `h03`). Any
gene set that correlates with gene length will *appear* enriched among top-mutated genes with no
biological selection. Ad-hoc "is my set enriched?" checks repeatedly re-derive the same
length/histology corrections. This method packages them once, with explicit negative controls,
so future gene-set claims (neural, immune, DNA-repair, etc.) are tested consistently.

## Estimand

For a gene set `S`, the target is the **partial enrichment** of `S` in the top-mutated tier
*after* conditioning on `log(gene length)` (CDS / callable length) and cohort histology
composition. Operationally, a logistic/Poisson model:

```
top_mutated_membership_g  ~  in_set_g  +  log(length_g)  +  histology_mix_covariates  +  offset(callable)
```

The coefficient on `in_set_g` (not the marginal overlap) is the enrichment estimate. Equivalent
framings: length-matched permutation null (sample background genes matched on length deciles),
and a dN/dS-based ranking where length is already in the background model.

## Inputs

- Per-gene mutation counts / sample-ratios from the annotated feathers
  (`gene_cancer_study(_ratio)_annotated.feather`).
- Gene length: `data/uniprotkb_hsapiens_protein_lengths.tsv.gz` + Ensembl CDS length.
- dN/dS background: the project's dndscv path (length already modeled).
- Histology composition: `cancer_type` / `oncotree_code`; CNS and neuroendocrine flags
  (see `question:q033`, `question:q034`).
- The candidate gene set `S` (e.g. a data-driven neural-enrichment score thresholded — `q035`).

## Negative-control gene-set battery (required)

Every run reports `S` **alongside** control sets so the reader can calibrate:

- **Known length artifacts (should score ~null after correction):** large-gene family TTN, MUC16,
  CSMD1/2/3, FAT1-4, RYR2, NEB, large mucins — high raw counts, length-driven.
- **Olfactory receptors** (numerous, biologically inert for most cancers) — null expectation.
- **Established drivers (positive control):** Bailey 2018 / CGC set — should stay enriched after
  length correction.
- **Random length-matched draws** — empirical null band.

A real enrichment is one where `S` separates from the length-artifact controls and behaves like
the driver control, not the TTN/olfactory controls.

## Outputs

- Per-set enrichment coefficient + CI + permutation p, raw vs length-adjusted vs histology-adjusted.
- Waterfall of how `S`'s enrichment moves across corrections (the `h12` decision tree, generalized).
- Reusable across hypotheses; first consumer is the neural-gene program (t215–t221).

## Guardrails

- Never report raw-count enrichment without the length-adjusted and control-set columns beside it.
- Histology adjustment is **not** a substitute for the explicit CNS/NET exclusion sensitivities
  (q033/q034) — report both.
- Enrichment of a *label-defined* set is reported only alongside the *data-driven* set (q035) to
  avoid annotation circularity.
