---
type: hypothesis
title: Joint indel+SBS signature decomposition improves aetiology discrimination beyond
  SBS alone, where indel-call depth permits
status: proposed
created: '2026-05-31'
updated: '2026-05-31'
id: hypothesis:0010-joint-indel-sbs-improves-aetiology-discrimination
phase: active
ontology_terms:
- mutational signatures
- somatic mutation
- indel
- DNA repair
datasets:
- dataset:tcga-mc3
- dataset:cbioportal
- dataset:pcawg
source_refs:
- paper:Koh2025
- paper:FerrerTorres2025
- paper:Owusu2025
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- topic:signature-extraction-fitting-methods
- topic:dna-damage-repair-signature-mechanisms
- question:0020-minimum-sample-size-and-caller-provenance-for
---

# Hypothesis: Joint indel+SBS signature decomposition improves aetiology discrimination beyond SBS alone

## Summary

Most signature analysis (including the current h08 design) uses 96-channel SBS. This hypothesis
proposes that **jointly decomposing indels (ID) with SBS — using the redefined indel taxonomy
(`paper:Koh2025`) and multimodal SBS+ID catalogues (`paper:FerrerTorres2025`) — improves
discrimination of aetiologies that are ambiguous in SBS space**, notably MMR-deficiency vs
clock-like and HRD vs flat signatures. The gain is expected to be **gated by indel-call depth**:
realisable on WGS/WES consensus substrates (MC3, PCAWG) but not on most panel cBioPortal studies.

## Rationale

- `paper:Owusu2025` shows MMRd produces a 7+ signature *ensemble* better resolved with indels;
  `paper:FerrerTorres2025` shows joint SBS+ID extraction sharpens DNA-repair-deficiency prognostic
  calls; `paper:Koh2025` provides a redefined 89-channel indel taxonomy that fixes COSMIC-83 indel
  artefacts.
- The project already ingests MC3 (consensus, indel-bearing) and could add PCAWG as a WGS
  gold-standard, so the high-depth substrate exists for the discriminating arm.
- For h08, indels offer a second, partly-orthogonal outcome modality — a concordance check on any
  SBS-based aetiology hit.

## Predictions

1. On MC3/PCAWG, joint SBS+ID assignment separates MMRd (ID-rich) from clock-like SBS5/SBS40 better
   than SBS alone (higher MSI-vs-MSS or dMMR-status discrimination).
2. The redefined indel taxonomy (`paper:Koh2025`) reduces apparent indel-signature artefacts in
   unmatched-normal studies relative to COSMIC-83.
3. The SBS+ID gain collapses to ~zero on panel-sequenced studies (insufficient indel calls),
   quantifying the depth gate.

## Falsifiability

- **Refuted** if adding indels yields no measurable improvement in aetiology discrimination over SBS
  alone on the high-depth substrates where it should be strongest (MC3/PCAWG).
- **Scope-bounding (not refutation)** if the gain exists only on WGS and is absent on WES — that
  confirms Prediction 3 and delimits where the modality is worth the cost.

## Alternative Explanations

- **Redundancy** — indel signatures carry the same information as SBS for the aetiologies of
  interest, so the joint model adds parameters without discrimination (the null this tests).
- **Call-quality confound** — indel "signal" is really caller/aligner artefact (`paper:Owusu2025`
  SBS57 cautionary case); adjudicate with the redefined taxonomy and consensus-only substrates.

## Status & Next Steps

- **status: proposed.** Lower priority than h09/h10 (depends on indel-call availability across the
  corpus, which is `question:0020` territory). Belongs to the `signature-modality-expansion` task
  group.
- Next: census indel-call availability across cBioPortal studies; pilot joint SBS+ID on MC3 MMRd
  vs MSS as the cleanest discrimination test.

## Related

- Hypotheses: `hypothesis:h08-...` (indels as an orthogonal concordance modality)
- Topics: `topic:signature-extraction-fitting-methods`, `topic:dna-damage-repair-signature-mechanisms`
- Questions: `question:q020-...`
- Tasks: the `signature-modality-expansion` group (see `tasks/active.md`)
