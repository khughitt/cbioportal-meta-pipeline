---
type: dataset
title: Kucab 2019 environmental-mutagen reference signature compendium (iPSC)
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: dataset:kucab2019-mutagen-compendium
source_class: reference
origin: external
tier: evaluate-next
license: CC-BY-4.0
update_cadence: static
ontology_terms: []
accessions:
- Kucab 2019 Cell supplementary signatures (DOI 10.1016/j.cell.2019.03.001)
access:
  level: public
  availability: available
  available_after: ''
  verified: false
  verification_method: ''
  last_reviewed: '2026-05-31'
  verified_by: ''
  source_url: https://doi.org/10.1016/j.cell.2019.03.001
  credentials_required: ''
  exception:
    mode: ''
    decision_date: ''
    followup_task: ''
    superseded_by_dataset: ''
    rationale: ''
siblings: []
consumed_by: []
source_refs:
- paper:Kucab2019
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- topic:pan-cancer-signature-catalogs
- topic:dna-damage-repair-signature-mechanisms
- dataset:cosmic-signatures
- dataset:normal-tissue-spectra
---

# Kucab 2019 environmental-mutagen reference signature compendium (iPSC)

## Summary

Whole-genome sequencing of 324 isogenic iPSC subclones each exposed to one of **79 known or
suspected environmental mutagens**, yielding **41 substitution, 6 doublet, and 8 indel reference
signatures** with *experimentally controlled* aetiology. Because each signature has a known causal
exposure, this is a ground-truth reference for aetiology anchoring — distinct from COSMIC's
observational, post-hoc-labelled catalogue.

## Why it matters for the project

- **Aetiology ground truth for `hypothesis:0007`.** When the agnostic scan produces a candidate
  spectrum, matching it against experimentally-caused Kucab signatures is stronger evidence than a
  COSMIC cosine match alone — a spectrum-level corroboration layer for any h08b discovery hit.
- **Positive-control spectra.** Provides clean reference spectra for known exposures (e.g. specific
  carcinogens) that the positive-control arms can be benchmarked against.
- **Complements `dataset:cosmic-signatures`** (observational reference) and
  `dataset:normal-tissue-spectra` (tissue background) as the *controlled-exposure* reference corner.

## Access and Scope

- Access: **public** — signatures available as Cell supplementary material (CC-BY); the underlying
  WGS is deposited (ENA, version-dependent).
- Modality: WGS of exposed iPSC subclones; derived reference signatures (SBS/DBS/ID).
- Source: https://doi.org/10.1016/j.cell.2019.03.001

## Evaluation Notes

- **Tier: evaluate-next.** Low acquisition cost (public signatures), high value as a reference table;
  the main work is integrating the spectra as a matchable reference alongside COSMIC.
- Caveat: iPSC in-vitro spectra may differ from in-vivo tissue context — use as corroboration, not
  sole arbiter.

## Related

- Hypotheses: `hypothesis:h08-...`
- Topics: `topic:pan-cancer-signature-catalogs`, `topic:dna-damage-repair-signature-mechanisms`
- Datasets: `dataset:cosmic-signatures`, `dataset:normal-tissue-spectra`
- Papers: `paper:Kucab2019`
