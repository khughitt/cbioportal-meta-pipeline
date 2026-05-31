---
id: question:023-sbs40-vs-sbs5-clocklike-expression-module
type: question
title: Can unsupervised co-expression modules distinguish SBS40 from SBS5 clock-like
  activity within-tissue after conditioning on age (the core h08b discovery target)?
status: active
ontology_terms: []
datasets: []
source_refs:
- paper:Hakobyan2024
- paper:Luo2023
- paper:Spisak2025
related:
- hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- method:h08-agnostic-association-model
- topic:signatures-expression-microenvironment
- topic:dna-damage-repair-signature-mechanisms
created: '2026-05-31'
updated: '2026-05-31'
---

# Can unsupervised co-expression modules distinguish SBS40 from SBS5 clock-like activity within-tissue after conditioning on age (the core h08b discovery target)?

## Summary

The t177 scan narrowed h08b's defensible novelty to unsupervised co-expression modules as the agnostic covariate set. The sharpest concrete instance: SBS40 has the broadest pan-cancer impact yet least-understood cause, and is hard to separate from SBS5. Can transcriptomic modules separate them within-tissue once age (the SBS1/SBS5 clock confounder) is conditioned out?

## Why It Matters

- Decision affected: whether SBS40-vs-SBS5 becomes the flagship named target pair for the h08b discovery prong, and whether the expression-module approach has discriminating power at all.
- Risk if unanswered: if modules cannot separate flat clock-like signatures, the h08b niche may be too weak to defend; better to know pre-registration.

## Current Evidence

- `paper:Spisak2025` argues SBS5 is a polymerase-error funnel where diverse damage converges — a hard true-negative for single exogenous covariates.
- `paper:Luo2023` finds clock-like SBS40 has the broadest TME impact but aggregates it into a single clock-like etiology group, not separating SBS40 from SBS5.
- `paper:Hakobyan2024` provides a signature-pair association framework (and CoDa methodology) usable as the analysis layer.

## Thoughts

- Best current interpretation: SBS40-vs-SBS5 separation via age-conditioned expression modules is the highest-value h08b test; SBS8/SBS40 are also testable via ATR/CHEK1/CHEK2 expression.
- Major uncertainty: identifiability of the expression->H edge (reverse causation R2 in the method DAG) — see `question:q025`.

## Connections to Project

- Related hypotheses: `hypothesis:h08-...` (h08b discovery prong).
- Required data or analyses: unsupervised NMF expression modules on co-measured RNA-seq (MC3); age-conditioned within-tissue module-vs-SBS40/SBS5 association.
- Priority level: P2 (defines the h08b headline).

## Related

- Topic notes: `topic:signatures-expression-microenvironment`, `topic:dna-damage-repair-signature-mechanisms`
- Article notes: `paper:Hakobyan2024`, `paper:Luo2023`, `paper:Spisak2025`
- Methods/Datasets: `method:h08-agnostic-association-model`; `question:q025`
