---
type: question
title: "Does clock-like mutational-signature exposure predict age at diagnosis better\
  \ than driver count \u2014 and does it absorb the driver-count signal q041 looks\
  \ for?"
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: question:0046-clocklike-signature-vs-driver-count-age-at-diagnosis
ontology_terms:
- clock-like signature
- mutational signature
- age of onset
- tumor mutational burden
- multistage carcinogenesis
datasets:
- "per-sample SBS signature exposures (run_restricted_sigprofiler_assignment.py \u2014\
  \ SBS1/SBS5/SBS40)"
- metadata/samples_annotated.feather (per-sample TMB, is_hypermutator, cancer type)
- patient metadata `age` (ordinal/binned via convert_to_feather.py; AGE_AT_SEQ_REPORT
  for GENIE)
- gene_cancer_study.feather (driver-count per sample, via q043 roster)
source_refs:
- paper:Alexandrov2015
- paper:Belikov2017
- paper:MoolgavkarKnudson1981
related:
- question:0041-driver-complexity-vs-median-age-at-diagnosis
- question:0023-sbs40-vs-sbs5-clocklike-expression-module
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the
- topic:multistage-carcinogenesis-and-age-of-onset
- question:0043-driver-cancer-type-breadth-distribution
---

# Does clock-like signature exposure predict age at diagnosis better than driver count — and does it absorb the driver-count signal q041 looks for?

## Summary

q041 asks whether **driver count** (the multistage "number of rate-limiting hits") tracks age at
diagnosis across cancer types. This question wires in the **competing predictor q041 never modeled**:
**clock-like mutational-signature exposure** — SBS1 (deamination, mitotic-clock-like) and SBS5/SBS40
(broad clock-like) accumulate roughly with age (`paper:Alexandrov2015`). The bridge between the
project's two most recent threads (temporal/age-of-onset and signatures):

1. Does clock-like signature burden predict **age at diagnosis** within and across cancer types?
2. Does it **absorb** the driver-count→age association q041 looks for (i.e. is "more drivers →
   older" partly just "more accumulated time → more clock mutations *and* more drivers")?
3. Net: is age-at-diagnosis better read as **elapsed mutational time** (signature exposure) than as
   **number of required events** (driver count) — or do the two carry independent information?

## Why It Matters

- It makes q041's multistage reading **testable against a rival**: clock-like burden is a direct
  molecular proxy for *elapsed time / total mutation supply*, which is exactly the
  Tomasetti-Vogelstein "replicative supply" axis the temporal theme pits against the
  number-of-events (Belikov k) axis. Separating them is the theme's core open problem.
- It leverages the project's **deepest infrastructure** (the h08 covariate-association scan +
  `run_restricted_sigprofiler_assignment`) on a new target (age), nearly for free.
- Risk if unasked: q041 could report a driver-count↔age correlation that is really a **clock-exposure
  confound** (older patients accumulate both more clock mutations and more detectable drivers),
  mis-attributing a time effect to a number-of-events effect.

## What we can compute (substrate on disk)

- **Have:** per-sample SBS exposures including SBS1/SBS5/SBS40 (the t178/t179-hardened
  `run_restricted_sigprofiler_assignment` path); per-sample TMB and `is_hypermutator`
  (`samples_annotated.feather`); per-sample driver count (via the `q043` roster); patient `age`.
- **Model:** age ~ clock-signature exposure + driver-count + TMB, within cancer type, with the rival
  nested-model comparison (does driver-count add predictive value over clock exposure, and vice
  versa?).

## Confounds that decide interpretability (inherits q041's, plus signature-specific ones)

- **Age is ordinal/binned, and age-at-sequencing ≠ age-at-onset (GENIE).** This is the *first-order*
  caveat (q041): `AGE_AT_SEQ_REPORT` is reporting time, not onset; our ingest bins age. Any "age"
  result is age-at-sampling at coarse resolution — state it, do not smooth over it.
- **Age→mutation-detection circularity.** Older tumors have had more time to accumulate *and* are
  often sampled later in disease — clock-burden↔age is partly mechanical. The interesting claim is
  whether driver count adds information *beyond* this mechanical clock.
- **Clock-signature calling quality.** SBS1/SBS5 are hard to separate from SBS40 and from
  panel-limited counts; the t179 per-sample count floor (default 383 WES) gates reliability — sub-floor
  samples flagged, not silently used. Panel data may not support reliable clock decomposition.
- **Hypermutators distort both axes** (`q047`): MMR/POLE samples inflate TMB and clock-independent
  signatures; stratify or exclude.
- **Cancer-type composition / Simpson** — always within-type, then pooled with care.

## Predictions

- Clock-like exposure predicts age-at-diagnosis **more strongly** than driver count (it is the more
  direct time proxy).
- Driver count retains **some independent** association with age across cancer types (the genuine
  multistage signal q041 seeks), concentrated where Belikov's k is large — but **weaker** than the raw
  q041 correlation once clock exposure is partialled out.
- In a subset (CNA-heavy / low-SBS cancers — prostate, myeloma), clock exposure is uninformative and
  the question is under-identified — the same modality-mismatch cases q041 flagged.

## Stop / null conditions

- If clock exposure **fully absorbs** driver-count's age association, q041's multistage reading is not
  separable from elapsed-time in our data → report age-at-diagnosis as a clock/time phenomenon, not a
  number-of-events one, at this resolution.
- If neither predicts binned age once composition is controlled, the age axis is too coarse
  (binned, age-at-seq) to carry the test → bounded by the q041 age-artifact, document and stop.

## Connections to Project

- **Bridges:** `q041` (driver-count↔age) ↔ the signature stack (`q023` clock-like SBS40/SBS5,
  `h08` covariate scan, `paper:Alexandrov2015`).
- **Theme:** `theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the` — this is the replicative-supply (clock)
  vs number-of-events (k) discriminator the theme names as its open problem
  (`topic:multistage-carcinogenesis-and-age-of-onset`).
- **Substrate:** `q043` (driver-count roster).
- **Priority:** **P3** — substrate on disk; gated on q041's age-normalization prerequisite (binned,
  age-at-seq) and reliable clock decomposition (count floor / panel limits).
