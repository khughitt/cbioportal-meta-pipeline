---
id: "interpretation:2026-06-07-q047-hypermutation-specificity-confound"
type: "interpretation"
title: "q047 first pass: hypermutation inflates breadth (confirmed) but per-sample dilution is under-identified on panel data"
status: "active"
source_refs:
  - "paper:MartinezJimenez2020"
related:
  - "question:q047-hypermutation-confound-on-driver-tissue-specificity"
  - "question:q043-driver-cancer-type-breadth-distribution"
  - "question:q042-driver-normal-expression-tissue-cell-type-specificity"
  - "topic:lineage-addiction-and-cell-of-origin-driver-specificity"
created: "2026-06-07"
updated: "2026-06-07"
---

# Interpretation: q047 — hypermutation as a driver-specificity confound (first pass)

## Verdict

**Partial.** One of q047's two claims is **confirmed and actionable**: hypermutators inflate apparent
cancer-type **breadth** (the q043↔q047 link), so q042/q043 must stratify on `is_hypermutator`. The
other claim — a clean *per-sample dilution of the restricted-lineage-oncogene signal* — is **not
identifiable on this targeted-panel-dominated cohort**, for structural reasons that themselves refine
the question's null condition.

## Cohort + method

- **Cohort:** `results/poc-2026-04-17/` — 542/13,006 samples flagged `is_hypermutator` (4.2%).
- Per-sample coding-nonsynonymous gene calls from per-study `mut_filtered.feather` (100% sample-meta
  join), joined to `is_hypermutator` + `cancer_type` from `samples_annotated.feather`.
- Gene classes reuse the q043 breadth feather (restricted_oncogene = CGC oncogene, breadth ≤2;
  broad_oncogene = breadth >10; tsg; oncogene_and_tsg; background = non-CGC panel genes).
- Script: `code/notebooks/q047_hypermutation_specificity_confound.py`.

## Key results

**1. Hypermutators concentrate in two cancer types — and CRC is under-flagged.** Of 542
hypermutators, 281 are Melanoma (35% of 813 — UV) and 190 Endometrial (25% of 747 — MSI/POLE). Only
these two cancer types cleared the testability floor (≥15 hyper & ≥30 non-hyper). **Colorectal — the
canonical MSI-hypermutator type — was *not* sufficiently flagged**, which points at the composite
`is_hypermutator` flag under-calling CRC MSI in this POC (a flagging-audit follow-up, not a q047
result).

**2. Breadth inflation confirmed (the actionable finding).** Excluding hypermutators raises the
restricted-driver fraction 52%→60% (q043, ≥5%) and **232 drivers lose ≥1 cancer-type of breadth**.
Hypermutator passenger recurrence does inflate apparent breadth — so any restricted-vs-pan-cancer
count (q042/q043) must be computed with hypermutators excluded *or* explicitly stratified.

**3. Per-sample passenger dilution is WEAK on panel data (a limitation, not a biology result).**
Within cancer type, hypermutators carry far more panel mutations (Endometrial median 7→93.5;
Melanoma 9→50), but the **driver share of load barely moves** (UCEC 0.941→0.882; Melanoma
0.900→0.895). Reason: the MSK-IMPACT panel is **driver-enriched by design** — off-panel passengers
are not even measured, so "driver share" is mechanically ≈0.9 regardless of hypermutation. The
passenger-dilution test needs WES.

**4. The prevalence-ratio metric is baseline-confounded — counter to the naive prediction.** Median
log2(prev_hyper / prev_non) by class: restricted_oncogene 4.40 and cgc_other 4.48 (highest),
background 3.22, **broad_oncogene 2.47 (lowest)**. Naively this looks like restricted oncogenes
inflate *most* — the opposite of the dilution hypothesis. But it is a **ceiling/baseline artifact**:
broad oncogenes (KRAS, PIK3CA, BRAF) are already highly prevalent in non-hypermutators, so their
ratio is compressed; rare restricted genes start near zero and yield mechanically large ratios. The
ratio metric does not isolate selection-vs-passenger; the one robust read is that **broad oncogenes
(the q043 hubs) are the most stable to hypermutation**.

## Limitations → refinements to q047's design

- **Panel driver-enrichment** caps the driver-share dilution test → rerun on a **WES cohort** where
  off-panel passengers are counted.
- **Baseline-prevalence confound** in the per-gene ratio → use a **prevalence-matched** comparison
  (or the composition of the *excess* mutations: of the extra mutations hypermutators carry, what
  fraction land on restricted oncogenes vs their non-hypermutator share) rather than a raw log-ratio.
- **Only two testable cancer types** + **CRC under-flagging** → audit the composite `is_hypermutator`
  flag (does it under-call CRC MSI?) before a pan-cancer rerun; raise the cohort beyond the 4-study POC.

## Implications for the questions

- **`q042` / `q043`:** confirmed — compute breadth / restricted-vs-pan-cancer with hypermutators
  excluded or stratified; the effect is material (232 drivers shift breadth).
- **`q047`:** the breadth-inflation arm is closed-positive; the per-sample dilution arm is **deferred
  to WES** with a baseline-matched metric and a hypermutator-flag audit (CRC). The null is sharpened:
  on panel data the dilution test is structurally under-identified, so a "no dilution" reading here is
  *not* evidence against the mechanism.
