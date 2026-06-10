---
type: theme
title: "Temporal structure of carcinogenesis \u2014 order, count, and timing of the\
  \ events of cancer"
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the
theme_kind: conceptual
theme_scope: project
related:
- question:0012-mutation-ordering-cross-sectional-inference
- question:0041-driver-complexity-vs-median-age-at-diagnosis
- question:0043-driver-cancer-type-breadth-distribution
- question:0045-pathway-grain-convergence-vs-gene-grain-divergence
- question:0046-clocklike-signature-vs-driver-count-age-at-diagnosis
- hypothesis:0004-mhn-pathway-ordering
- hypothesis:0006-pre-malignant-n-minus-1-driver-carriage
- topic:multistage-carcinogenesis-and-age-of-onset
- discussion:0002-mutation-ordering-and-path-dependency
- discussion:0007-hallmark-ordering-and-data-driven-modules
- discussion:0006-age-of-onset-and-multistage-mutation-requirement
- topic:co-occurrence-and-mutual-exclusivity
- task:t078
source_refs: []
evidence_refs: []
---

# Theme: Temporal structure of carcinogenesis — order, count, and timing of the events of cancer

## Definition

A cross-cutting frame for the project's work on **when, in what order, and how many** somatic
events occur during carcinogenesis — as distinct from the project's other axes (signature
aetiology, contamination/QC, gene-length confounding). Three coupled sub-questions live here:

- **Order** — in what *sequence* are drivers/pathways acquired? (`question:0012`, `hypothesis:0004`
  MHN ordering; `hypothesis:0006` pre-malignant n-1 carriage as the paired-data route; the
  hallmark-grain echo in `discussion:0007-hallmark-ordering-and-data-driven-modules`).
- **Count** — *how many* rate-limiting events does a cancer type require, and how does that set its
  age of onset? (`topic:multistage-carcinogenesis-and-age-of-onset`, `question:0041`).
- **Timing / rate** — what governs *how fast* the process runs (replicative supply vs
  selection-landscape shifts)? (the Tomasetti-Vogelstein vs Rozhok-DeGregori axis in the topic).

## Why It Matters

- These entities share a **single hard constraint**: cBioPortal/GENIE are nearly all
  single-biopsy snapshots at diagnosis, so *temporal* claims (order, rate, number-of-required-
  hits) are **under-identified** from the data and ride on the same confounds — collider/
  ascertainment bias, age->mutation-detection inflation, CH and normal-tissue contamination,
  panel callability, and per-histology pooling (Simpson). Grouping them keeps those shared
  confounds and their mitigations in one place.
- It marks the project's **epistemic boundary** on temporal questions: the rigorous versions
  (true k, true order) live in **incidence-vs-age** or **longitudinal/clonal (VAF/CCF)** data;
  the prevalent cohort yields *suggestive, confound-controlled correlations and inferred*
  structure, not identification. Every entity here must state which side of that line it is on.

## Boundaries

- **Inside:** mutation/pathway ordering (q012/h04); paired-stage driver carriage (h06);
  multistage number-of-hits and age-of-onset (topic + q041); hallmark-acquisition ordering
  (hallmark discussion); the replicative-supply-vs-selection mechanism debate.
- **Outside (own concepts/work):** the co-occurrence / mutual-exclusivity *association substrate*
  itself (`topic:co-occurrence-and-mutual-exclusivity`, `t078`) is machinery this theme *consumes*
  to infer order/modules — it is association, not time; signature aetiology and contamination/QC
  themes (technical, not temporal); gene-length confounding (`theme` via h03) except where it
  enters as a confound on a temporal statistic.

## Current Project Links

- Questions: `q012` (ordering inferability), `q041` (driver-count vs age of onset).
- Hypotheses: `h04` (MHN-inferred order), `h06` (observed paired-stage carriage / n-1).
- Topic: `topic:multistage-carcinogenesis-and-age-of-onset`.
- Discussions: `2026-04-24-mutation-ordering-and-path-dependency`,
  `2026-06-07-hallmark-ordering-and-data-driven-modules`,
  `2026-06-07-age-of-onset-and-multistage-mutation-requirement`.
- Substrate consumed: `topic:co-occurrence-and-mutual-exclusivity`, `task:t078` (and t137 wiring).

## Guardrails

- Never present a temporal claim (order, rate, number-of-hits) from prevalent cross-sectional
  data without naming the identifiability gap and the specific confound controls applied.
- Distinguish **intrinsic mutators** (MMR/POLE/POLD1 — accelerate acquisition) from **checkpoint /
  expansion-permissive** genes (TP53/RB1 — often *late* despite the naive "repair-first" reading).
- For age/onset work, treat **age at sequencing != age at onset** (GENIE) and the
  **age->mutation-detection circularity** as first-order, not footnotes.
- Keep **association** (co-occurrence/exclusivity) separate from **order** (MHN) separate from
  **modules** (a distinct inference step) — do not let one stand in for another.
- Calibrate against external truth where it exists: PCAWG chronology (order), Belikov 2017 / SEER
  (count), before claiming any novel temporal result.

## Open Questions

- Can directed order be recovered at all from our cohort (simulation calibration gate, `q012`)?
- Does driver complexity track age of onset once detection confounds are removed (`q041`)?
- Do data-driven modules map onto hallmark sets, and do hallmarks show an acquisition order
  (hallmark discussion)?

## Update Triggers

- Any MHN/ordering result from `h04`/`q012` (changes what "order" claims the theme can host).
- VAF/CCF availability audit landing (opens the longitudinal/clonal route).
- New external benchmark adopted (PCAWG, SEER/Belikov, Gerstung chronology).
