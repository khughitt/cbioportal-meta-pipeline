---
type: paper
title: Cancer cells co-opt an inter-organ neuroimmune circuit to escape immune surveillance
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: paper:Zhang2025
ontology_terms:
- cancer neuroscience
- neuro-immune crosstalk
- nociceptive neuron
- CGRP
- SLIT2
- tumor-draining lymph node
- immune checkpoint blockade
- head and neck squamous cell carcinoma
datasets: []
source_refs:
- cite:Zhang2025
related:
- paper:Kizil2024
- paper:Pu2025
- paper:Cortese2020
- paper:Fan2024
- paper:Lu2026
- paper:Wang2025b
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- topic:neuro-immune-crosstalk-cancer
- topic:perineural-invasion-axon-guidance-genes
---

# Cancer cells co-opt an inter-organ neuroimmune circuit to escape immune surveillance

- **Authors:** Yu Zhang, Yibo Guo, Zheqi Liu, Yiting Sun, Xi Yang, Mingtao Chen, Guanying Feng, Chengzhong Lin, Yang Wang, Zhen Zhang, Yun Zhu, Jinhai Ye, Jiajia Liu, Jun Shi, Xiaomeng Zhou, Qingjian Han, Yu Liu, Qian Jiang, Youcheng Yu, Xu Wang, Chenping Zhang, Yunfan Sun, Jian Zhou, Jia Fan, Tong Ji
- **Year:** 2025
- **Journal:** Cell 188(24):6754–6773.e29 (Epub 2025-10-24; print 2025-11-26)
- **DOI/URL:** https://doi.org/10.1016/j.cell.2025.09.029
- **BibTeX key:** Zhang2025
- **Source:** abstract (PubMed) — full text inaccessible (paywalled); details beyond the
  abstract are marked `[INACCESSIBLE]`.

## Key Contribution

A primary study (HNSCC clinical data + three murine oral cancer models, with melanoma
referenced) defining an **inter-organ neuroimmune circuit** that tumors co-opt for immune
escape: under immune pressure, cancer cells secrete **SLIT2** via an **ATF4**-dependent
pathway, activating tumor-innervating **nociceptive neurons**; this propagates to
tumor-draining-lymph-node (TDLN)-innervating nociceptive neurons, raising **CGRP** (CALCA) and
remodeling the TDLN into an immunosuppressed state that blunts immune checkpoint blockade (ICB).

## Methods

- Clinical HNSCC cohort data + three murine oral cancer models; melanoma as an additional
  context (per keywords). `[UNVERIFIED]` exact cohort sizes / model identities — not in abstract.
- Causal dissection of the ATF4→SLIT2→nociceptor→TDLN→CGRP→CCL5→TAM axis via secretion,
  neuronal activation, and intervention (targeting nociceptive neurons or the ATF4–SLIT2–CGRP
  axis). Specific genetic/pharmacologic tools, denervation methods, and readouts: `[INACCESSIBLE]`
  (full text paywalled).

## Key Findings

- **ATF4-dependent SLIT2 secretion under immune pressure** is the tumor-cell-intrinsic trigger —
  i.e. SLIT2 acts here through **regulated secretion / expression**, not somatic mutation.
- SLIT2 activates **tumor-innervating nociceptive neurons** and aggravates cancer-induced pain.
- The signal reaches **TDLN-innervating nociceptive neurons**, increasing **CGRP** secretion and
  remodeling the TDLN into an immune-suppressed state.
- Immune-suppressed TDLNs show **decreased CCL5**, driving **M2-like polarization of
  tumor-associated macrophages (TAMs)**, promoting tumor growth and reducing ICB efficacy.
- **Targeting nociceptive neurons or the ATF4–SLIT2–CGRP axis** restores immune activity,
  alleviates pain, and improves ICB responses — a therapeutic handle.
- Named molecules: **SLIT2, ATF4, CALCA (CGRP), CCL5**; TAM M2 program. `[INACCESSIBLE]`:
  receptor on nociceptors (ROBO? RAMP1/CALCRL downstream), quantitative effect sizes.

## Relevance

- **H2 (neural signal via immune modulation): strong, mechanistic, causal support.** This is the
  clearest primary demonstration in the batch of nerves mediating tumor **immune escape** —
  and it does so as a multi-organ circuit (tumor → tumor nerves → TDLN nerves → TDLN immunity →
  TAMs), echoing the brain-body framing of `paper:Wang2025b` but grounded in HNSCC.
- **Reinforces `hypothesis:0012`'s central claim.** SLIT2 is one of the large **axon-guidance**
  genes in our perineural / candidate-adjacent set
  (`topic:perineural-invasion-axon-guidance-genes`). This paper shows it acts via **ATF4-driven
  secretion/expression**, *not* via somatic mutation in the tumor genome — the exact
  "expression-not-mutation" pattern that argues against reading neural-gene **mutation**
  enrichment as active hijacking. SLIT2 here is a *secreted ligand under transcriptional
  control*, not a recurrently mutated driver.
- **Weakens H4 (CNS-artifact).** HNSCC is a peripheral cancer; the circuit is non-CNS.
- **CGRP (CALCA) convergence.** Independently corroborates `paper:Kizil2024` / `paper:Pu2025` /
  `paper:Cortese2020` on CGRP→nociceptor→immune suppression, now extended to an inter-organ
  (tumor↔TDLN) scale.

## Project Framework Mapping

| Paper concept | Project concept | Notes |
|---|---|---|
| ATF4→SLIT2 secretion | gene **expression**, not mutation | central to why mutation-frequency tables miss this biology (h12) |
| SLIT2 (axon-guidance ligand) | candidate-adjacent large gene | `topic:perineural-invasion-axon-guidance-genes`; expression-driven, not mutated |
| CGRP / nociceptor → TDLN immunosuppression | neuro-immune axis | `topic:neuro-immune-crosstalk-cancer`; H2 |
| ICB response modulation | treatment / clinical covariate | potential expression-axis covariate; not a mutation feature |

## Limitations

- `[INACCESSIBLE]`: full Methods/Results (cohort sizes, model details, effect sizes, the
  nociceptor receptor for SLIT2, statistics) — summary is abstract-based.
- Mechanism is expression/neuronal-circuit; provides **no** somatic-mutation evidence and does
  not speak to gene-length confounding.
- Generalization beyond HNSCC/oral models (e.g. to the melanoma context) not assessable from the
  abstract alone (`[UNVERIFIED]`).

## Model / Tool Availability

`[INACCESSIBLE]` — model systems, reagents, and any deposited data not determinable from the
abstract. Revisit if full text is obtained (institutional access / author copy).

## Follow-up

- If full text becomes available, extract: the SLIT2 nociceptor receptor, quantitative
  ICB-response effects, and whether SLIT2/ATF4/CALCA show any genomic alteration (vs purely
  transcriptional) in the HNSCC cohort — a direct check against `hypothesis:0012` / `question:0037`.
- Adds a concrete, citable example to `topic:neuro-immune-crosstalk-cancer` and the
  "expression-not-mutation" argument in `synthesis:0015-cancer-neuroscience-literature-batch-21-papers-does-it-explain-a-neural`.
