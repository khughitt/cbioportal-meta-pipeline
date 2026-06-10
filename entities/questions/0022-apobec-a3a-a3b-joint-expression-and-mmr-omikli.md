---
type: question
title: Does a joint APOBEC3A+APOBEC3B expression score (and intact-MMR expression
  in MSS tumors) predict SBS2/SBS13 burden better than single covariates?
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: question:0022-apobec-a3a-a3b-joint-expression-and-mmr-omikli
ontology_terms: []
datasets: []
source_refs:
- paper:Carpenter2023
- paper:MasPonte2020
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- method:h08-agnostic-association-model
- topic:apobec-mutagenesis
---

# Does a joint APOBEC3A+APOBEC3B expression score (and intact-MMR expression in MSS tumors) predict SBS2/SBS13 burden better than single covariates?

## Summary

h08 Arm C tests APOBEC mRNA -> SBS2/13. The batch evidence refines this: both A3A and A3B contribute via distinct sub-signatures (YTCA vs RTCA), so a joint score may outperform either paralog; and counterintuitively, intact MMR may *promote* the dominant diffuse (omikli) APOBEC mode, predicting a positive MMR-expression -> SBS2/13 association within MSS tumors.

## Why It Matters

- Decision affected: the exact APOBEC covariate specification in the h08 model (single gene vs joint score) and whether MMR expression is a confounder or a co-cause for Arm C.
- Risk if unanswered: using A3B alone (the historical default) may under-detect A3A-driven cases; ignoring the MMR-omikli coupling could misattribute an MMR-expression effect.

## Current Evidence

- `paper:Carpenter2023` (cell-line WGS) shows A3A and A3B both generate SBS2/SBS13 with distinct tetranucleotide preferences (YTCW ~70% vs RTCW ~53%), supporting combinatorial contributions.
- `paper:MasPonte2020` shows MMR activity generates the ssDNA that fuels diffuse APOBEC3 (omikli) hypermutation — MMR promotes, not suppresses, the dominant mode.
- Panel/WES studies overrepresent APOBEC-context coding mutations relative to WGS (assay-type confound).

## Thoughts

- Best current interpretation: specify a joint A3A+A3B expression score as the Arm C covariate; test MMR expression as a positive co-predictor within MSS-restricted strata.
- Major uncertainty: whether cBioPortal expression exports resolve A3A vs A3B reliably (paralog mapping), and the magnitude of the WES/panel coding-context inflation.

## Connections to Project

- Related hypotheses: `hypothesis:h08-...` (Arm C).
- Required data or analyses: paralog-resolved APOBEC3 expression extraction; MSS-restricted MMR-expression vs SBS2/13 test; assay-type stratification.
- Priority level: P2.

## Related

- Topic notes: `topic:apobec-mutagenesis`
- Article notes: `paper:Carpenter2023`, `paper:MasPonte2020`
- Methods/Datasets: `method:h08-agnostic-association-model`
