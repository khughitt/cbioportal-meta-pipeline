---
type: topic
title: 'Cancer neuroscience: nervous-system regulation of tumors (foundations)'
status: active
created: '2026-06-06'
updated: '2026-06-06'
id: topic:cancer-neuroscience-neural-regulation
ontology_terms:
- cancer neuroscience
- neural regulation of cancer
- synaptic signaling
- autonomic nervous system
- brain-body circuit
- tumor innervation
source_refs:
- paper:Mancusi2023
- paper:Keough2022
- paper:Magnon2023
- paper:Hanahan2023
- paper:Venkatesh2019
- paper:Hwang2025a
- paper:Huang2023a
- paper:Huang2025a
- paper:Wang2025b
- paper:Wu2025a
- paper:Xiong2023
related:
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- question:0033-neural-enrichment-cns-exclusion
- question:0035-label-free-neural-gene-definition
- question:0037-canonical-neural-gene-dnds-selection
- synthesis:0015-cancer-neuroscience-literature-batch-21-papers-does-it-explain-a-neural
- topic:neuro-immune-crosstalk-cancer
- topic:oncofetal-developmental-reprogramming
---

# Cancer neuroscience: nervous-system regulation of tumors (foundations)

## Scope

The foundational reviews establishing that the nervous system regulates cancer initiation,
growth, and metastasis — and that tumors reciprocally remodel nerves. Flagship: `paper:Mancusi2023`
(Nature). Field consensus / hallmarks framing: `paper:Hanahan2023` (neural co-option as an
emerging enabling characteristic). Mechanistic depth: `paper:Keough2022`. Systemic brain-body
framing: `paper:Wang2025b`, `paper:Magnon2023` ("neural addiction"). Roadmap/priorities:
`paper:Hwang2025a`. Primary causal proof in a non-CNS cancer: `paper:Xiong2023` (CeM→sympathetic
circuit controls breast cancer in mice). Short prize essay: `paper:Venkatesh2019`.

## Core mechanisms (canonical effector genes)

- **Synaptic / electrical:** glioma forms functional neuron→tumor synapses; NLGN3 (shed by
  ADAM10) is the central activity-dependent mitogen → PI3K-mTOR; AMPAR (GRIA), NMDAR (GRIN2A/2B),
  gap junctions (GJA1). NLGN3 anti-correlates with GBM survival.
- **Neurotrophic:** NGF, BDNF, GDNF → NTRK1/2/3 (TrkA/B/C), RET; drive innervation + proliferation.
- **Autonomic:** sympathetic NE → ADRB1/2/3; parasympathetic ACh → CHRM1/3, CHRNA7. Direction is
  cancer-type-specific.
- **Tumor neurogenesis:** DCX+ progenitors recruited; tumor axonogenesis.

## Key point for this project

This biology operates through **expression, innervation, paracrine signaling, and epigenetic
reprogramming — not somatic mutation of neural genes in tumor DNA** (`paper:Hanahan2023` states
co-option is non-mutational). The circuitry largely lives in the **host** nervous system
(`paper:Wang2025b`, `paper:Xiong2023`), so a mutation-frequency table is not the expected readout.
None of the project's candidate genes (NKAIN2, KCNIP4, LSAMP, OPCML, RBFOX1, …) appear in this
literature; the canonical effectors above are a disjoint, shorter set. This motivates the
null-first `hypothesis:0012` and the canonical-effector dN/dS test (`question:0037`).

## Open leads

- Label-free neural-gene definition from glioma OPC/NPC state signatures (Neftel2019/Filbin2018)
  and brain atlases (`question:0035`).
- Whether enrichment survives CNS-study removal (`question:0033`) — peripheral-cancer biology is
  real (see `topic:perineural-invasion-axon-guidance-genes`) but still non-mutational.

## Summary

This topic note is currently a concise project-facing record; the existing sections above carry the substantive synthesis until a fuller rewrite is warranted.

## Key Concepts

The key concepts are defined in the existing prose above and in the linked project entities; this section is present to keep the topic aligned with the current Science topic template.

## Current State of Knowledge

The current project-facing state of knowledge is summarized in the existing prose above. No additional confidence upgrade is made by this structural section.

## Relevance to This Project

This topic is relevant through the linked questions, hypotheses, datasets, and source references in the frontmatter and in the note above.

## Key References

Key references are listed in `source_refs` and cited in the note above.
