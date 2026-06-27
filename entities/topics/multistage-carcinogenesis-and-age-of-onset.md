---
type: topic
title: Multistage carcinogenesis and the determinants of differential age of cancer
  onset
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: topic:multistage-carcinogenesis-and-age-of-onset
ontology_terms:
- multistage carcinogenesis
- age of onset
- number of driver mutations
- stem cell divisions
- clonal expansion
- adaptive oncogenesis
source_refs:
- paper:ArmitageDoll1954
- paper:Knudson1971
- paper:MoolgavkarKnudson1981
- paper:TomasettiVogelstein2015
- paper:Belikov2017
- paper:RozhokDeGregori2015
related:
- theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the
- question:0041-driver-complexity-vs-median-age-at-diagnosis
- hypothesis:0006-pre-malignant-n-minus-1-driver-carriage
- hypothesis:0004-mhn-pathway-ordering
- question:0012-mutation-ordering-cross-sectional-inference
- question:0046-clocklike-signature-vs-driver-count-age-at-diagnosis
- discussion:0006-age-of-onset-and-multistage-mutation-requirement
---

# Multistage carcinogenesis and the determinants of differential age of cancer onset

## Scope

Why does the **median age of onset differ across cancer types**, and what governs it? This topic
collects the classical and modern theory for three candidate determinants — (1) the **number of
rate-limiting mutations** a type requires, (2) **cell-division rate**, (3) **target-cell /
stem-cell number** — plus the evolutionary counterweight that timing is set by **selection**, not
mutation supply alone. It is the background for `question:0041` (the prevalent-cohort test) and a
node in `theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the`.

## The multistage scaffold (factor 1: number of required hits)

- **`paper:ArmitageDoll1954`** — the foundational result: for most adult carcinomas, incidence
  rises as roughly the **(k-1)th power of age**; a log-log incidence-vs-age slope of ~5-6 implies
  **~6-7 rate-limiting stages**. The number of required events sets *how steeply* incidence
  climbs and *when* a cancer becomes common. (Nordling 1953 is the predecessor.)
- **`paper:Knudson1971`** — the cleanest single demonstration that **fewer required hits ->
  earlier onset**: hereditary retinoblastoma (one germline + one somatic hit) is **early and
  bilateral**; sporadic (two somatic hits) is **later and unilateral**. Germline pre-loading of a
  hit is the mechanism behind early-onset hereditary syndromes (Li-Fraumeni *TP53*, Lynch, *BRCA*,
  FAP *APC*). This is the conceptual root of `hypothesis:0006` (n-1 driver carriage).
- **`paper:MoolgavkarKnudson1981`** — the **two-stage clonal-expansion (MVK) model**: adds
  proliferation of *intermediate* (initiated) cells to the raw stage count, explaining why real
  incidence curves **bend** rather than being pure power laws, and providing the formal slot where
  division-rate and target-cell-number enter multiplicatively.
- **`paper:Belikov2017`** — the modern re-fit: estimates a **per-cancer-type number of key
  carcinogenic events** by fitting models to SEER age-incidence curves. This is the most direct
  external quantity to (loosely) compare against mutation-derived driver counts in `q041`.
- Convergent modern estimates of *how many drivers* per tumor: Tomasetti-Vogelstein-Nowak 2015
  (PNAS) "~3 drivers" for lung/colorectal; Martincorena 2017 dN/dS "~4 drivers/tumor" average,
  ranging 1-10 by type. *(These two are cited as context; not yet summarized in the library —
  candidate follow-up papers.)*

## Replicative supply (factors 2 and 3: division rate x target-cell number)

- **`paper:TomasettiVogelstein2015`** — the "bad luck" paper: lifetime cancer **risk** across
  tissues correlates with the **total number of stem-cell divisions** (lscd; ~65% of variation).
  Mutation supply ~ (stem-cell number) x (division rate) x (mutations/division) — this is factors
  2 and 3 combined in one term. **Two crucial caveats:** it explains lifetime **risk**, not
  age-of-**onset** directly; and it is **heavily contested** (Wu et al. 2016 *Nature*: extrinsic
  factors dominate; correlation != causation).
- **Target-cell number alone fails across species** — *Peto's paradox*: whales have ~1000x more
  cells than mice yet do not get proportionally more cancer (large/long-lived organisms evolved
  extra suppression, e.g. elephant *TP53* copies). Target-cell number is a real *within-tissue*
  term but not a clean cross-organism predictor.

## The evolutionary counterweight (timing = selection, not just supply)

- **`paper:RozhokDeGregori2015`** — argues age-dependent cancer risk is shaped less by raw
  mutation accumulation than by **age-dependent shifts in selection**: the aged-tissue
  microenvironment changes the fitness landscape so that clones neutral/deleterious in young
  tissue become advantageous in old tissue (**adaptive oncogenesis**). Better explains the
  late-life incidence surge in some tissues and the single-hit-looking onset of others, and warns
  against over-reading the lscd correlation as causal. The essential nuance for any "fewer hits =
  earlier onset" claim: *onset depends on when tissue ecology starts rewarding the hits.*

## Special cases any general model must excuse

- **Pediatric / embryonal tumors** — ~10x fewer somatic mutations (Gröbner/Ma 2018), often a
  **single fusion or CNV** rather than an SNV burden; arise from developmental cells. They break
  the adult multistage curve by *mechanism*, not just count.
- **Testicular (germ-cell)** — a young-adult incidence peak that mutation-count models do not
  explain.
- **Hormonal windows** (breast, prostate) and **heavy extrinsic exposure** (lung/smoking,
  skin/UV, liver/HBV) can dominate the intrinsic terms and advance onset.

## What this project's data can and cannot do

- **Can (correlational only):** relate per-cancer-type median age at diagnosis to a
  mutation-derived driver-complexity proxy (`question:0041`), as a sanity check against
  `paper:Belikov2017`.
- **Cannot:** estimate the true number of required hits k — that needs **incidence-vs-age**
  curves (Armitage-Doll / Belikov), not prevalent diagnostic mutation cohorts; and cannot supply
  stem-cell-division counts, so factors 2/3 stay interpretive context.
- **Central confound** carried into `q041`: older patients accumulate more *detectable* mutations
  regardless of how many were rate-limiting — a mutation-derived complexity proxy can manufacture
  an age correlation. See `q041` for the controls.

## Connections

- **Theme:** `theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the` (order + count + hallmark-timing).
- **Hypotheses:** `h06` (count axis — drivers carried per stage), `h04` (order axis).
- **Questions:** `q041` (the test here), `q012` (ordering, shares confounds).
- **Discussion:** `discussion:0006-age-of-onset-and-multistage-mutation-requirement`.
- **External / not-yet-in-library:** Nordling 1953; Tomasetti-Vogelstein-Nowak 2015 PNAS
  (3-drivers); Martincorena 2017 (dN/dS driver counts); Wu et al. 2016 *Nature* (extrinsic
  rebuttal); Gröbner 2018 / Ma 2018 (pan-pediatric).

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
