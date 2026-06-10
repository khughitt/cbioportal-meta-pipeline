---
type: question
title: What operationalisable causality guard (mediation, clonal timing, cross-study
  replication) should gate h08b expression-to-signature discovery hits before any
  upstream claim?
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: question:0025-causal-direction-guard-for-expression-signature
ontology_terms: []
datasets: []
source_refs:
- paper:Robinson2019
- paper:Sorensen2023
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- method:h08-agnostic-association-model
- topic:aetiology-covariate-association
---

# What operationalisable causality guard (mediation, clonal timing, cross-study replication) should gate h08b expression-to-signature discovery hits before any upstream claim?

## Summary

The h08 method DAG marks the expression->H edge as not identified by adjustment alone (reverse causation R2: a driver can remodel its own expression module). The batch reinforces that cross-sectional association cannot establish direction. This question fixes the concrete guard an h08b hit must pass before it is reported as an upstream cause.

## Why It Matters

- Decision affected: the interpretation rule converting a ranked expression<->signature association into a defensible causal claim — central to h08b's credibility.
- Risk if unanswered: h08b reports reverse-causation or confounded edges as discoveries, exactly the failure mode the pre-registration exists to prevent.

## Current Evidence

- `paper:Robinson2019` (TCSM) and `paper:Sorensen2023` establish the association paradigm but rely on post-hoc validation, not pre-specified causal guards.
- The method note already requires within-tissue stratification (R1), spectrum-vs-burden split (R3), and nuisance/artefact flags (R4); the open piece is the direction guard for R2.
- Mediation logic and temporality (clonal timing) are named in the method note as the needed tools but not operationalised.

## Thoughts

- Best current interpretation: require at least two of {mediation consistent with covariate->H, clonal-timing temporality where MC3 multi-sample allows, independent cross-study replication} before any upstream claim; otherwise report as a ranked hypothesis only.
- Major uncertainty: feasibility of clonal-timing from single-sample MC3 data.

## Connections to Project

- Related hypotheses: `hypothesis:h08-...` (h08b discovery prong; R2 rival).
- Required data or analyses: mediation framework; cross-study replication protocol; timing feasibility check.
- Priority level: P2 (must be frozen in the h08b pre-registration).

## Related

- Topic notes: `topic:aetiology-covariate-association`
- Article notes: `paper:Robinson2019`, `paper:Sorensen2023`
- Methods/Datasets: `method:h08-agnostic-association-model`; `question:0023`
