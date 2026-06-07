---
id: "topic:neuro-immune-crosstalk-cancer"
type: "topic"
title: "Neuro-immune crosstalk in cancer (neural control of tumor immunity)"
status: "active"
ontology_terms:
  - neuro-immune crosstalk
  - tumor immunity
  - adrenergic signaling
  - cholinergic anti-inflammatory pathway
  - neuropeptides
  - stress and cancer
source_refs:
  - "paper:Kizil2024"
  - "paper:Pu2025"
  - "paper:Cortese2020"
  - "paper:Mravec2008"
related:
  - "hypothesis:h12-neural-gene-enrichment-length-histology-artifact"
  - "hypothesis:h01-non-tumor-signal-contamination"
  - "question:q035-label-free-neural-gene-definition"
  - "synthesis:2026-06-06-cancer-neuroscience"
  - "topic:cancer-neuroscience-neural-regulation"
created: "2026-06-06"
updated: "2026-06-06"
---

# Neuro-immune crosstalk in cancer (neural control of tumor immunity)

## Scope

How nerves and neural signals regulate the tumor immune microenvironment — the user's "does it
help by disrupting the immune system?" thread. Review-of-record: `paper:Kizil2024` (neural
control of tumor immunity); comprehensive mechanism+therapy: `paper:Pu2025`; peripheral-nervous-
system focus: `paper:Cortese2020`; historical nervous–endocrine–immune triad (stress, HPA):
`paper:Mravec2008`.

## Core mechanisms (effector genes act on immune cells, not via mutation)

- **Sympathetic/adrenergic:** NE → ADRB1/2/3 on CD8 T cells (exhaustion), MDSCs (Arg1/PD-L1),
  TAMs (M2), Tregs. Chronic stress amplifies this (HPA + SAM axes).
- **Sensory/nociceptor:** CGRP (CALCA) → RAMP1 on CD8 T cells → exhaustion; TRPV1+ neuron
  ablation increases anti-tumor immunity.
- **Cholinergic anti-inflammatory pathway:** ACh → CHRNA7 on macrophages suppresses NF-κB.
- **Metabolite/neurotransmitter:** GABA (from B cells/macrophages) suppresses CD8; serotonin
  → PD-L1 (histone serotonylation, TGM2); circadian clock (BMAL1) in myeloid cells.
- **NF1 in neurons** → Midkine→CCL4→microglia→CCL5 circuit supporting glioma stem cells
  (a rare case of a *neural-gene mutation* with immune consequence — but in NF1, an established
  driver, not in the candidate list).

## Relevance to this project

Supports the user's H2 (neural signal acts via immune modulation) as **biology**, but again at
the **expression/receptor** level — the neuro-immune effector genes (ADRB2, CHRM1, CALCA, RAMP1,
GAD1) are not the project's candidate list and are not predicted to be mutation-enriched. Useful
contributions: (i) a positive-control neuro-immune gene set for the label-free definition
(`question:q035`); (ii) the prediction that, in studies with immune deconvolution, neural-signal
gene *expression* (not mutation) should track immune composition — a future expression-axis test.
Clock genes (BMAL1/PER/CRY) and stress/HPA framing connect to the user's hormone/neuroendocrine
questions (see `topic:neuroendocrine-neoplasm-lineage-confound`).
