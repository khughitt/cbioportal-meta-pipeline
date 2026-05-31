---
id: hypothesis:h09-cross-study-signature-exposure-reproducibility
type: hypothesis
title: Per-cancer-type mutational-signature exposures reproduce across independent cBioPortal studies, and divergences are explained by technical batch (caller/panel/treatment), not biology
status: proposed
phase: active
ontology_terms:
  - mutational signatures
  - somatic mutation
  - batch effect
  - reproducibility
datasets:
  - dataset:tcga-mc3
  - dataset:cbioportal
  - dataset:aacr-genie
source_refs:
  - paper:Jiang2025
  - paper:Medo2024
  - paper:Battuello2024
  - paper:Wu2023
related:
  - hypothesis:h02-cross-study-ranking-divergence-is-structured
  - hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and
  - topic:signature-extraction-fitting-methods
  - topic:aetiology-covariate-association
  - question:q020-minimum-sample-size-and-caller-provenance-for
  - question:q021-how-should-single-caller-cbioportal-studies-be-flagged-and-handled-in-signature-analysis
---

# Hypothesis: Per-cancer-type mutational-signature exposures reproduce across independent cBioPortal studies, and divergences are explained by technical batch

## Summary

The project's defining strength is having *many independent studies of the same cancer types*. This
hypothesis asks the signature analog of `hypothesis:h02` (which concerns mutation-frequency ranking
divergence): **do per-cancer-type signature exposure profiles replicate across independent
cBioPortal/MC3/GENIE studies of the same tissue, and — where they diverge — is the divergence
explained by technical batch (variant-caller provenance, panel vs WES vs WGS, treatment exposure)
rather than by real biological difference?** A clean answer is a prerequisite for trusting any
cross-study pooled signature claim, including the h08 positive control.

## Rationale

- The literature batch shows signature *estimates* are tool- and reference-dependent
  (`paper:Battuello2024`, `paper:Medo2024`, `paper:Wu2023`) and that single-caller provenance injects
  reproducible artefactual signatures (`paper:Jiang2025`). These are exactly the cross-study nuisances
  the project is positioned to measure, because it holds the same tissue sequenced under different
  pipelines.
- `hypothesis:h02` already establishes that cross-study *ranking* divergence is structured (not
  noise); signatures are a second readout where the same logic should hold and is independently
  testable.
- If exposures replicate after batch adjustment, cross-study pooling (the project's core move) is
  validated for signatures; if they do not, it bounds what h08 and any pooled-signature deliverable
  can claim.

## Predictions

1. Within a cancer type, the *rank order* of dominant signatures (e.g. SBS1/SBS5/SBS40 clock-like,
   plus the tissue-canonical exposure) is concordant across independent studies (rank correlation
   clearly above a permutation null).
2. Residual cross-study exposure variance is predicted by technical covariates — caller consensus
   (`paper:Jiang2025`), assay class (panel/WES/WGS), and treatment-exposed fraction — more strongly
   than by any biological study covariate.
3. Consensus-called substrates (MC3) show tighter cross-replicate agreement than heterogeneous
   per-study cBioPortal TCGA MAFs of the same cancer types (a built-in positive control for the
   batch claim).
4. Artefact-prone flat signatures (SBS5/SBS40) and known sequencing-artefact signatures
   (SBS27/43/45–60) account for a disproportionate share of cross-study disagreement.

## Falsifiability

- **Refuted** if within-cancer-type signature profiles are no more concordant across studies than
  across randomly shuffled study labels — i.e. signatures do not carry a reproducible cross-study
  signal at cBioPortal scale.
- **Refuted (batch claim)** if divergence is *not* explained by technical covariates — i.e. studies
  with identical caller/assay/treatment profiles diverge as much as discordant ones, implying the
  variation is biological or irreducible.

## Alternative Explanations

- **True biological heterogeneity** — same-tissue cohorts differ by ancestry, subtype mix, or stage,
  producing real exposure differences (adjudicate by conditioning on available biological covariates
  before attributing residual to batch).
- **Reference-version skew** — studies fit against different COSMIC versions (`question:q021` heme
  variant); harmonise before comparing.
- **Power artefact** — small studies have noisier exposures; concordance must be assessed at matched
  effective sample size.

## Status & Next Steps

- **status: proposed.** Naturally downstream of the h08 signature-decomposition layer (shares
  `task:t178`/`t179` infrastructure: caller-provenance flag + per-sample fitting). Could run as its
  own analysis once per-sample/refit exposures exist for ≥2 independent studies per cancer type.
- Next: enumerate cancer types with ≥2 independent cBioPortal/MC3 studies; reuse the
  caller-consensus + assay + treatment flags (`task:t178`, `task:t181`) as the batch covariates.

## Related

- Hypotheses: `hypothesis:h02-cross-study-ranking-divergence-is-structured` (mutation-frequency
  analog), `hypothesis:h08-...` (consumes reproducible exposures)
- Topics: `topic:signature-extraction-fitting-methods`, `topic:aetiology-covariate-association`
- Questions: `question:q020-...`, `question:q021-...` (heme COSMIC-version harmonisation)
- Tasks: `task:t178`, `task:t179`, `task:t181`
