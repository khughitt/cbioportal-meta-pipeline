---
id: "discussion:2026-06-07-age-of-onset-and-multistage-mutation-requirement"
type: "discussion"
title: "Why does median age of cancer onset differ across types? Number-of-hits vs division rate vs target-cell number"
status: "active"
focus_type: "approach"
mode: "standard"
source_refs:
  - "paper:ArmitageDoll1954"
  - "paper:Knudson1971"
  - "paper:MoolgavkarKnudson1981"
  - "paper:TomasettiVogelstein2015"
  - "paper:Belikov2017"
  - "paper:RozhokDeGregori2015"
related:
  - "theme:temporal-structure-of-carcinogenesis"
  - "topic:multistage-carcinogenesis-and-age-of-onset"
  - "question:q041-driver-complexity-vs-median-age-at-diagnosis"
  - "question:q012-mutation-ordering-cross-sectional-inference"
  - "hypothesis:h06-pre-malignant-n-minus-1-driver-carriage"
  - "hypothesis:h04-mhn-pathway-ordering"
  - "discussion:2026-06-07-hallmark-ordering-and-data-driven-modules"
created: "2026-06-07"
updated: "2026-06-07"
---

# Why does median age of cancer onset differ across types?

## Focus

Does the **median age of disease onset** for different cancer types vary with respect to (1) the
**number of mutations a type requires** to become malignant/metastatic, (2) **cell-type
properties** (e.g. baseline division rate), (3) **how numerous the cell type is** in the body, or
(4) something else — and what is already known or hypothesized about the causes? This is the
**count/timing** sibling of the project's **order** work (`question:q012`, `hypothesis:h04`,
`hypothesis:h06`) and `discussion:2026-06-07-hallmark-ordering-and-data-driven-modules`.

## Current Position

**This is one of the oldest quantitative results in cancer biology, not green field — the *what
governs it* is well-theorized; the *measure it in our data* is sharply confound-limited.** The
user's three factors map onto the three terms of the classical multistage / two-stage
clonal-expansion (MVK) model:

1. **Number of required hits — strongest, best-evidenced factor.** `paper:ArmitageDoll1954`:
   incidence ~ (k-1)th power of age => ~6-7 rate-limiting stages for adult carcinomas; the number
   of required events sets the slope of incidence-vs-age. `paper:Knudson1971` is the cleanest
   confirmation that **fewer required hits => earlier onset** (hereditary vs sporadic
   retinoblastoma), and the mechanism behind early-onset hereditary syndromes (germline
   pre-loading). `paper:Belikov2017` gives a modern per-cancer-type estimate of the number of key
   events from incidence curves. Pediatric/embryonal tumors are the extreme low-hit, early-onset
   class — but by a *different mechanism* (fusion/CNV, not SNV burden).

2. **Cell-division rate** and 3. **target-cell / stem-cell number** — `paper:TomasettiVogelstein2015`
   folds both into one term: mutation supply ~ stem-cell-number x division-rate x mutations/
   division, and lifetime **risk** across tissues tracks total stem-cell divisions (~65% of
   variation). But this is about **risk, not age-of-onset**, and is heavily contested; target-cell
   number alone fails across species (Peto's paradox).

4. **Something else — the decisive nuance.** `paper:RozhokDeGregori2015`: age-dependent
   **selection shifts** (adaptive oncogenesis) in aged tissue, not raw mutation supply, may set
   carcinogenesis rate — onset depends on *when tissue ecology starts rewarding* the hits.
   Plus extrinsic exposure, hormonal windows, and germline predisposition.

The full background and citations live in `topic:multistage-carcinogenesis-and-age-of-onset`.

## Critical Analysis

- **The honest framing: the rigorous version lives in incidence data, not ours.** Armitage-Doll
  and Belikov estimate k from **population age-incidence curves**. Our cBioPortal/GENIE data is a
  **prevalent cohort of diagnostic snapshots** — we observe *which* mutations are present at
  diagnosis, in a *screening/referral-selected* sample, not the population incidence-vs-age curve.
  We can do a **suggestive cross-type correlation**, not an identification of the number of
  required hits.
- **The killer confound is age -> mutation-detection circularity.** Older patients carry more
  passengers *and* more incidentally detectable drivers regardless of how many were rate-limiting.
  A mutation-derived "driver complexity" proxy can therefore **manufacture** an age correlation.
  Any test must use recurrent/known drivers only, work within age bands, or regress out TMB —
  and report whether the signal survives (`question:q041`).
- **"Age of onset" is not what we have.** GENIE's `AGE_AT_SEQ_REPORT` is age at *sequencing*,
  often well after onset; ascertainment/screening (PSA, mammography, colonoscopy) shifts apparent
  onset; subtype pooling induces Simpson's paradox. Per-histology only.
- **Different mechanisms break a single regression.** Pediatric/embryonal (few SNV drivers,
  fusion/CNV-driven) and germline-syndrome (pre-loaded hit) early-onset classes, and testicular
  (germ-cell) young-adult onset, must be **flagged and modeled separately**, not pooled.
- **Correlation cannot adjudicate mechanism.** Even a clean age/complexity relationship does not
  decide *supply* (Tomasetti-Vogelstein) vs *selection* (Rozhok-DeGregori) — our data describes,
  it does not mechanistically arbitrate.
- **Initiation != metastatic competence.** The user's "to become cancer-like *or metastatic*"
  spans two different counts; the multistage age curve is about initiation/diagnosis, while
  metastatic progression is the `h04`/`q012` ordering regime. Keep them separate.

## Relationship to existing entities

- **`hypothesis:h06` (pre-malignant n-1 driver carriage)** is the closest existing home: it is
  literally about *how many of the n required drivers* are present at a stage — the count axis of
  this discussion, with paired pre-malignant/invasive data as the cleaner route.
- **`question:q012` / `hypothesis:h04`** are the *order* axis; this discussion is the *count/timing*
  axis. Same cohort, same confounds (collider, CH, callability, Simpson).
- **`discussion:2026-06-07-hallmark-ordering-and-data-driven-modules`** is the hallmark-grain echo
  of the same temporal question; all three now sit under
  `theme:temporal-structure-of-carcinogenesis`.

## Prioritized Follow-Ups

| Priority | Item | Where |
|---|---|---|
| **P3** | `question:q041` — driver-complexity vs median age at diagnosis, with the age->detection confound controls; calibrate against Belikov 2017. Descriptive, low-cost, gated on a clean per-histology age table + driver annotations. | `question:q041`, needs `gene_cancer_study_annotated.feather` + clinical `AGE` |
| **P4** | Candidate methodological question: **age as a covariate inflating mutation/driver burden** project-wide (touches TMB, SBS1/SBS5 clock signatures `q023`). File only if the confound recurs beyond this thread. | not yet filed |
| **P4** | Add context papers to the library if the thread advances: Tomasetti-Vogelstein-Nowak 2015 PNAS (3-drivers), Martincorena 2017 (dN/dS driver counts), Wu 2016 *Nature* (extrinsic rebuttal), Gröbner/Ma 2018 (pan-pediatric). | `topic:multistage-carcinogenesis-and-age-of-onset` |
| **done** | `paper:MoolgavkarKnudson1981` summary is now **full-text from the PDF** (user-provided 2026-06-07): two-stage model fitted to lung-in-nonsmokers + breast, with exact parameters and the incidence formula confirmed. | `doc/papers/MoolgavkarKnudson1981.md` |

## Synthesis

The user's instinct is correct and quantified: **cancer types that require fewer rate-limiting
changes do present earlier** (`paper:Knudson1971`, `paper:Belikov2017`), and division-rate x
target-cell-number sets mutation *supply* (`paper:TomasettiVogelstein2015`) — but with two
load-bearing qualifications: (i) the clean, identifiable version of "number of required hits"
lives in **incidence-vs-age** data we do not have, so our prevalent cohort can only offer a
**confound-controlled correlation** (`question:q041`); and (ii) timing may be governed by
age-dependent **selection** as much as by mutation supply (`paper:RozhokDeGregori2015`), so even a
positive correlation describes rather than explains. The defensible project claim is: *we can test
whether mutation-derived driver complexity tracks age of onset across types, as a sanity check
against the incidence-curve literature — not estimate how many hits each cancer requires.*
