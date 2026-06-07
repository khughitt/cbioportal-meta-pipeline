---
id: theme:cancer-neuroscience-in-a-mutation-only-pipeline
type: theme
title: Cancer neuroscience in a mutation-only pipeline — expression-not-mutation, and the confound-first stance
status: active
theme_kind: substantive
theme_scope: project
related:
- hypothesis:h12-neural-gene-enrichment-length-histology-artifact
- hypothesis:h03-gene-length-confounds-literature-attention
- topic:cancer-neuroscience-neural-regulation
- topic:neuro-immune-crosstalk-cancer
- topic:perineural-invasion-axon-guidance-genes
- topic:neuroendocrine-neoplasm-lineage-confound
- topic:oncofetal-developmental-reprogramming
- question:q032-neural-gene-length-null
- question:q033-neural-enrichment-cns-exclusion
- question:q034-neuroendocrine-histology-confound
- question:q035-label-free-neural-gene-definition
- question:q036-oncofetal-fetal-vs-adult-neural-expression
- question:q037-canonical-neural-gene-dnds-selection
- question:q038-length-correlated-geneset-spurious-enrichment
- question:q039-stress-hpa-adrenergic-mutational-footprint
- question:q040-neuroactive-drug-exposure-treatment-signature
- method:length-aware-geneset-enrichment
- synthesis:2026-06-06-cancer-neuroscience
source_refs: []
evidence_refs: []
created: '2026-06-07'
updated: '2026-06-07'
---
# Theme: Cancer neuroscience in a mutation-only pipeline — expression-not-mutation, and the confound-first stance

## Definition

A cross-cutting frame for how the project relates to the cancer-neuroscience literature
(21-paper batch, `synthesis:2026-06-06-cancer-neuroscience`). The field's biology — neural
regulation of tumor growth, neuro-immune control, perineural invasion — is real but operates
through **expression, innervation, paracrine signaling, and epigenetic reprogramming, not
somatic mutation** of neural genes in tumor DNA. The project measures somatic mutation. This
theme organizes the resulting stance: treat an apparent "neural gene" mutation signal as a
**confound to disprove (length + histology) before it is biology**, and be explicit about what a
mutation-only pipeline can and cannot say about neuro-oncology.

## Why It Matters

- Prevents an attractive but likely-spurious narrative ("neural genes are top-mutated → tumors
  hijack neural programs") from being adopted without the length/histology nulls.
- Clarifies the project's epistemic boundary: the genuine neuro-cancer signal lives on an
  **expression axis the pipeline does not currently measure**; mutation-layer contributions are
  limited to (a) confound control and (b) a few narrow, testable footprints (stress/repair,
  neuro-active-drug exposure, canonical-effector dN/dS).
- Gives the five new topic notes and h12 a shared home and a consistent reading.

## Boundaries

- **Inside:** the neural-gene mutation-enrichment question and its confounds (length, CNS, NET);
  label-free neural-gene definition; oncofetal (H3) vs selection (H1) discrimination;
  neuro→mutation footprints (stress/HPA, drug exposure); the generalized length-aware enrichment guard.
- **Outside (remains its own concept/work):** building an expression modality (a scope decision
  for the project, not this theme); clinical neuro-oncology; the assay-regime confound
  (`theme:assay-regime-confounding`) which is technical, not biological.

## Current Project Links

- Hypothesis: `hypothesis:h12` (null-first); builds on `hypothesis:h03`.
- Topics: the five `topic:` notes in `related`.
- Questions: q032–q040.
- Method: `method:length-aware-geneset-enrichment`.
- Plan / tasks: `doc/plans/2026-06-06-neural-gene-enrichment-meta-analysis-plan.md`; group
  `neural-gene-meta-analysis` (t215–t221) + search tasks for label-free neural datasets.

## Guardrails

- Never present raw-count neural enrichment as biology without the length-adjusted statistic and
  negative-control gene sets beside it.
- Do not equate "neuroendocrine neoplasm" (a tumor lineage) with "neural regulation of cancer" (a
  mechanism) — they enter the project as different things (confound vs biology).
- Mutation-layer absence of signal is **not** evidence against the cancer-neuroscience field; it
  is evidence the signal is on a different (expression) axis.
- Keep neural-gene definitions data-driven (expression/developmental enrichment); GO labels are a
  sensitivity comparator only.

## Downstream Work

- The neural-gene meta-analysis program (t215–t221) and the generalized enrichment guard (q038).
- Substrate-gated leads connecting neuro-biology to the mutation/signature core (q039, q040).
- Possible future: a scoped decision on whether the project adds an expression modality, which is
  where the field's real signal would be visible.

## Open Questions

- Does any neural enrichment survive length + CNS + NET correction at all? (q032–q034)
- If so, is it oncofetal byproduct (H3) or selection (H1)? (q036/q037)
- Is there a real stress/repair or drug-exposure mutational footprint? (q039/q040)

## Update Triggers

- Completion of t215 (does the observation even reproduce).
- Any decision to add an expression/RNA modality to the pipeline.
- New cancer-neuroscience papers with primary **somatic-mutation** (not expression) evidence.
