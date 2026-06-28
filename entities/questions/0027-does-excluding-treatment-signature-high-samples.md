---
type: question
title: Does excluding therapy-signature-high samples measurably change the pooled
  gene-by-cancer mutation-frequency tables and any cross-study driver ranking?
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: question:0027-does-excluding-treatment-signature-high-samples
ontology_terms: []
datasets: []
source_refs:
- paper:Diamond2023
- paper:Pleasance2020
related:
- hypothesis:0009-treatment-induced-signature-frequency-contamination
- topic:clinical-translational-signatures
- question:0024-treatment-exposed-cohort-chemotherapy-signature
---

# Does excluding therapy-signature-high samples measurably change the pooled gene-by-cancer mutation-frequency tables and any cross-study driver ranking?

## Summary

The impact test for `hypothesis:0009`. After flagging therapy-signature-high samples (SBS11/31/35/87), re-run the pooled gene × cancer frequency tables with and without them and measure whether the deliverable — and any cross-study driver ranking — changes beyond noise.

## Why It Matters

- Decision: whether the primary frequency-table output needs a treatment-exposed exclusion/down-weight step.
- Risk: the headline tables silently carry iatrogenic burden inflation.

## Current Evidence

- `paper:Diamond2023`/`paper:Pleasance2020` show therapy signatures are strong in treated cohorts.
- `create_freq_tables.py` already emits inclusive/exclusive columns keyed on hypermutator status — a treatment-exposed parallel is a small extension.

## Thoughts

- Effect likely concentrated in types with both treated and naive cohorts (CRC, myeloma, lung).
- Uncertainty: completeness of treatment metadata to define the exclusion set.

## Connections to Project

- Hypotheses: `hypothesis:0009-treatment-induced-signature-frequency-contamination`.
- Analyses: treatment-exposed flag (`question:0024-treatment-exposed-cohort-chemotherapy-signature` / `task:t181`); paired freq-table diff.
- Priority: P2.

## Related

- Hypotheses: `hypothesis:0009-treatment-induced-signature-frequency-contamination`
- Topics: `topic:clinical-translational-signatures`
- Questions: `question:0024-treatment-exposed-cohort-chemotherapy-signature`
- Code: `code/scripts/create_freq_tables.py`
