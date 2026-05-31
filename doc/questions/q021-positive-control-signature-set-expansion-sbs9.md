---
id: question:q021-positive-control-signature-set-expansion-sbs9
type: question
title: Should the h08 positive-control signature set be expanded to include SBS9 (germinal-centre)
  and SBS54, and which MMR signatures are the canonical MSI discriminators?
status: active
ontology_terms: []
datasets: []
source_refs:
- paper:Ji2023
- paper:Machado2022
- paper:Owusu2025
related:
- hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- method:h08-agnostic-association-model
- topic:aetiology-covariate-association
- topic:signatures-normal-tissue-germline
created: '2026-05-31'
updated: '2026-05-31'
---

# Should the h08 positive-control signature set be expanded to include SBS9 (germinal-centre) and SBS54, and which MMR signatures are the canonical MSI discriminators?

## Summary

The h08 method note currently lists the positive-control map as UV/SBS7, smoking/SBS4, APOBEC/SBS2-13, MMR/SBS6-15-26, POLE/SBS10. The batch literature suggests two additions: SBS9 (AID/germinal-centre, a tissue-of-origin positive control in lymphoid studies) and SBS54, reported to discriminate MSI from MSS better than established dMMR signatures.

## Why It Matters

- Decision affected: the frozen positive-control signature set against which H08a pass/fail is judged, and the restricted-assignment reference used in the pipeline.
- Risk if unanswered: omitting a real, recoverable aetiology (SBS9 in lymphoid tissue) understates positive-control power; including a flagged/germline-confounded signature (SBS54) without scrutiny weakens the gate.

## Current Evidence

- `paper:Machado2022` grounds SBS9/SBS7a as tissue-of-origin processes in normal lymphocytes — SBS9 should be an expected positive in DLBCL/lymphoid strata, not a novel hit.
- `paper:Ji2023` reports SBS54 outperforming established dMMR signatures at MSI-vs-MSS discrimination; however SBS54 has historically been flagged as possible germline contamination in some COSMIC notes [UNVERIFIED].
- `paper:Owusu2025` experimentally resolves the seven COSMIC MMRd signatures and flags SBS57 as an SNP-indel alignment artefact — informs which MMR signatures are real discriminators.

## Thoughts

- Best current interpretation: add SBS9 as a tissue-restricted positive control (lymphoid only); treat SBS54 as a candidate MSI discriminator to evaluate, not auto-include, pending a germline-artefact check.
- Major uncertainty: SBS54's provenance status in the COSMIC version the pipeline loads (see `question:q020`).

## Connections to Project

- Related hypotheses: `hypothesis:h08-...` (defines the positive-control gate).
- Required data or analyses: confirm SBS9/SBS54 presence in the restricted reference; lymphoid-stratum check; SBS54 germline-artefact adjudication.
- Priority level: P2 (freezes before H08a runs).

## Related

- Topic notes: `topic:aetiology-covariate-association`, `topic:signatures-normal-tissue-germline`
- Article notes: `paper:Ji2023`, `paper:Machado2022`, `paper:Owusu2025`
- Methods/Datasets: `method:h08-agnostic-association-model`
