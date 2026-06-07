---
id: "topic:cancer-neuroscience-neural-regulation"
type: "topic"
title: "Cancer neuroscience: nervous-system regulation of tumors (foundations)"
status: "active"
ontology_terms:
  - cancer neuroscience
  - neural regulation of cancer
  - synaptic signaling
  - autonomic nervous system
  - brain-body circuit
  - tumor innervation
source_refs:
  - "paper:Mancusi2023"
  - "paper:Keough2022"
  - "paper:Magnon2023"
  - "paper:Hanahan2023"
  - "paper:Venkatesh2019"
  - "paper:Hwang2025a"
  - "paper:Huang2023"
  - "paper:Huang2025"
  - "paper:Wang2025"
  - "paper:Wu2025a"
  - "paper:Xiong2023"
related:
  - "hypothesis:h12-neural-gene-enrichment-length-histology-artifact"
  - "question:q033-neural-enrichment-cns-exclusion"
  - "question:q035-label-free-neural-gene-definition"
  - "question:q037-canonical-neural-gene-dnds-selection"
  - "synthesis:2026-06-06-cancer-neuroscience"
  - "topic:neuro-immune-crosstalk-cancer"
  - "topic:oncofetal-developmental-reprogramming"
created: "2026-06-06"
updated: "2026-06-06"
---

# Cancer neuroscience: nervous-system regulation of tumors (foundations)

## Scope

The foundational reviews establishing that the nervous system regulates cancer initiation,
growth, and metastasis — and that tumors reciprocally remodel nerves. Flagship: `paper:Mancusi2023`
(Nature). Field consensus / hallmarks framing: `paper:Hanahan2023` (neural co-option as an
emerging enabling characteristic). Mechanistic depth: `paper:Keough2022`. Systemic brain-body
framing: `paper:Wang2025`, `paper:Magnon2023` ("neural addiction"). Roadmap/priorities:
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
(`paper:Wang2025`, `paper:Xiong2023`), so a mutation-frequency table is not the expected readout.
None of the project's candidate genes (NKAIN2, KCNIP4, LSAMP, OPCML, RBFOX1, …) appear in this
literature; the canonical effectors above are a disjoint, shorter set. This motivates the
null-first `hypothesis:h12` and the canonical-effector dN/dS test (`question:q037`).

## Open leads

- Label-free neural-gene definition from glioma OPC/NPC state signatures (Neftel2019/Filbin2018)
  and brain atlases (`question:q035`).
- Whether enrichment survives CNS-study removal (`question:q033`) — peripheral-cancer biology is
  real (see `topic:perineural-invasion-axon-guidance-genes`) but still non-mutational.
