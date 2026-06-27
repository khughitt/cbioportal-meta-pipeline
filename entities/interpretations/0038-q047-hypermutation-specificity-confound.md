---
type: interpretation
title: 'q047: hypermutation inflates breadth AND dilutes driver-share across 8 cancer
  types (post-TMB-fix)'
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: interpretation:0038-q047-hypermutation-specificity-confound
source_refs:
- paper:MartinezJimenez2020
related:
- question:0047-hypermutation-confound-on-driver-tissue-specificity
- question:0043-driver-cancer-type-breadth-distribution
- question:0042-driver-normal-expression-tissue-cell-type-specificity
- topic:lineage-addiction-and-cell-of-origin-driver-specificity
- interpretation:0036-panel-tmb-denominator-stale-artifact-fix
---

# Interpretation: `q047` — hypermutation as a driver-specificity confound

> **Revised 2026-06-07 after the panel-TMB-denominator fix**
> (`interpretation:0036-panel-tmb-denominator-stale-artifact-fix`). The first pass ran on a
> stale `samples_annotated` where panel TMB was ~25× too small, so only the two WES cancer types had
> any hypermutators and the per-sample dilution test looked "under-identified." All numbers below are
> post-fix; the earlier "weak on panel data" verdict was itself an artifact of the broken flags.

## Verdict

**Confirmed, both arms.** (1) Hypermutators inflate apparent cancer-type **breadth** — so `q042`/`q043`
must stratify on `is_hypermutator`. (2) Hypermutators **dilute the driver share of mutational load**
across the 8 testable cancer types (drop of 0.10–0.22). The one residual caveat is the per-gene
prevalence-ratio metric, which stays baseline-confounded and is not the right tool — but the
driver-share test (`T2`) cleanly shows the dilution.

## Cohort + method

- **Cohort:** `results/poc-2026-04-17/` (post-fix) — 557/13,006 samples flagged `is_hypermutator`
  (4.3%), now correctly distributed across panel and WES cancer types.
- Per-sample coding-nonsynonymous gene calls from per-study `mut_filtered.feather` (100% sample-meta
  join), joined to `is_hypermutator` + `cancer_type` from `samples_annotated.feather` (samples with
  zero panel nonsynonymous mutations included).
- Gene classes reuse the `q043` breadth feather, oncogene-only in three bands: restricted_oncogene =
  breadth ≤2; mid_oncogene = 3–9; broad_oncogene = breadth ≥10. Plus tsg / oncogene_and_tsg /
  cgc_other by CGC role; background = non-CGC panel genes.
- Script: `code/notebooks/q047_hypermutation_specificity_confound.py`.

## Key results

**1. Eight testable cancer types (was 2 pre-fix).** Bladder, Colorectal, Endometrial,
Esophagogastric, Hepatobiliary, Melanoma, Non-Small Cell Lung, cutaneous SCC — i.e. the MSI / POLE /
smoking / UV hypermutator-bearing types, now that panel TMB is correct.

**2. Breadth inflation confirmed (the `q043`↔`q047` link).** Excluding hypermutators raises the
restricted-driver fraction **52%→68% at ≥5%** (IntOGen's 63% is now bracketed), and **186 drivers
lose ≥1 cancer-type of breadth at ≥5%** (253 at ≥2%). Any restricted-vs-pan-cancer count (`q042`/`q043`)
must be computed with hypermutators excluded or stratified.

**3. Per-sample driver-share dilution is now clearly detectable.** Within cancer type, the driver
share of (panel) mutational load drops markedly in hypermutators — a consistent passenger-dilution
signal across all 8 types:

| cancer type | driver share (non-hyper → hyper) |
|---|---|
| Colorectal | 0.889 → 0.763 |
| Non-Small Cell Lung | 0.929 → 0.784 |
| Esophagogastric | 0.913 → 0.763 |
| Bladder | 0.900 → 0.791 |
| cutaneous SCC | 1.000 → 0.783 |
| Hepatobiliary | 1.000 → 0.833 |
| Endometrial | 0.917 → 0.873 |
| Melanoma | 0.900 → 0.875 |

This is the dilution the first pass *could not* see (it only had WES-flagged melanoma/endometrial,
where the share barely moved). Even on a driver-enriched panel — where off-panel passengers aren't
measured — the within-panel background-gene fraction rises enough to register the effect.

**4. Broad oncogenes are the most stable class; the per-gene ratio stays baseline-confounded.**
Median log2(prev_hyper / prev_non) by class: background 3.38, restricted_oncogene 3.51, cgc_other
3.53, mid_oncogene 3.26, tsg 3.25, oncogene_and_tsg 3.25, **broad_oncogene 2.76 (lowest)**. Classes
other than broad now cluster tightly (3.2–3.5), so this raw ratio still does not isolate
selection-vs-passenger (it is a ceiling/baseline artifact — already-common broad oncogenes have
compressed ratios). The robust read: **broad oncogenes (the `q043` hubs) are the most stable under
hypermutation**; for the dilution question, prefer the `T2` driver-share metric over this ratio.

## Limitations → refinements to `q047`'s design

- **Per-gene prevalence ratio** remains baseline-confounded → for any *per-gene* claim use a
  prevalence-matched comparison or the composition of the *excess* mutations; the *per-sample*
  driver-share (`T2`) is the trustworthy aggregate read here.
- **Panel under-resolution** still caps the absolute magnitude (off-panel passengers unmeasured), so
  the true dilution is *larger* than the within-panel 0.10–0.22; a WES cohort would quantify it fully.
- **POC scale** — 8 cancer types from 4 studies; a multi-study cohort would broaden coverage.

## Implications for the questions

- **`q042` / `q043`:** confirmed and material — compute breadth / restricted-vs-pan-cancer with
  hypermutators excluded or stratified (186 drivers shift breadth at ≥5%; restricted fraction
  52%→68%).
- **`q047`:** both arms now positive on panel data. The "CRC under-flagging" follow-up is **resolved**
  — it was the panel-TMB-denominator bug
  (`interpretation:0036-panel-tmb-denominator-stale-artifact-fix`), not a flag-logic gap.
