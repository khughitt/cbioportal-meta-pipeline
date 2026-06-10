---
type: question
title: What is the distribution of cancer-type breadth across drivers in our own aggregated
  cohort, and does it reproduce IntOGen's restricted-vs-pan-cancer split?
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: question:0043-driver-cancer-type-breadth-distribution
ontology_terms:
- driver gene
- pan-cancer
- cancer-type breadth
- cross-study replication
- tissue specificity
datasets:
- "gene_cancer_study.feather (raw per-(gene, cancer, study) counts \u2014 the un-broadcast\
  \ substrate)"
- 'gene_cancer_pooled.feather (t077 pooled per-(cancer, gene): k_studies, status,
  pooled ratios)'
- data/bailey2018_table_s1.tsv (PanCanAtlas 299-driver consensus + per-cancer rosters;
  PANCAN rows separable)
- "data/cosmic_cgc.tsv (COSMIC CGC v100 \u2014 Role in Cancer, Tumour Types(Somatic))"
- IntOGen / Martinez-Jimenez 2020 per-cancer-type driver compendium (external reference
  roster)
- data/uniprotkb_hsapiens_protein_lengths.tsv.gz (length control)
source_refs:
- paper:MartinezJimenez2020
- paper:Hoadley2018
related:
- question:0042-driver-normal-expression-tissue-cell-type-specificity
- question:0041-driver-complexity-vs-median-age-at-diagnosis
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- hypothesis:0003-gene-length-confounds-literature-attention
- question:0013-cross-study-replication-rate
- question:0016-panel-induced-ascertainment
- question:0017-cross-study-saturation-curve
- topic:lineage-addiction-and-cell-of-origin-driver-specificity
- topic:cancer-driver-genes
- theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the
- interpretation:0037-q043-driver-breadth-distribution
- interpretation:0036-panel-tmb-denominator-stale-artifact-fix
---

# What is the distribution of cancer-type breadth across drivers in our own aggregated cohort, and does it reproduce IntOGen's restricted-vs-pan-cancer split?

## First-pass result (2026-06-07, poc-2026-04-17 cohort)

**Supported, qualitatively robust; restricted fraction is threshold-defined.** On the 4-study POC
(13,006 samples, 410 panel-covered genes), breadth is heavy-tailed: TP53 broadest (33/57 types), the
hub set TSG-dominated, oncogenes in the restricted tail (TSG median breadth > oncogene at every
threshold) — the structure q042 predicts. **8 of IntOGen's 12 cancer-wide drivers** are panel-covered
and all sit at the top. The fraction "restricted to 1–2 types" is **strongly threshold-dependent**
(8%→19%→52% at 1/2/5%; **→68% with hypermutators excluded** on corrected post-TMB-fix flags), so it
**brackets** IntOGen's 63% at the ≥5% grade (inclusive below, hypermutator-excluded above) — i.e.
"restricted vs pan-cancer" is a recurrence-bar + hypermutator-handling choice, not a constant. The
roster feather q042 needs now exists. See
`interpretation:0037-q043-driver-breadth-distribution` and
`interpretation:0036-panel-tmb-denominator-stale-artifact-fix`;
`code/notebooks/q043_driver_breadth_distribution.py`.

## Summary

We repeatedly invoke "**restricted vs pan-cancer**" drivers — q042 needs it to define its
specificity contrast, q041 needs a driver-count per cancer type, the temporal theme needs to know
which events are shared — but the project has **never measured the distribution itself**: across the
driver set, in *how many distinct cancer types* does each driver recur at above-background frequency
**in our own aggregated cBioPortal/GENIE/MC3 cohort**? The descriptive object is a single
distribution — driver → cancer-type-breadth count — and two derived questions:

1. **Shape.** Is breadth heavy-tailed (a few cancer-wide hubs — TP53/KRAS/PIK3CA — and a long tail
   of 1–2-type drivers), matching IntOGen's compendium (`paper:MartinezJimenez2020`: 360/568 = 63%
   restricted to 1–2 tumor types; only 12 cancer-wide)?
2. **Replication.** Does *our* cohort reproduce that split, or does its specific study composition
   (panel-heavy GENIE, TCGA via MC3, per-cancer-type study counts) shift it? Breadth measured on our
   composition is itself a cross-study replication test (`hypothesis:0002`, `question:0013`).

This is the **roster-counting backbone** that q042 lists as an *unmet prerequisite* and q041 needs
for its driver-count axis — and it is computable **today**, with no external expression ingest.

## Why It Matters

- **It de-risks two open questions at once.** q042's restricted-vs-pan-cancer split and q041's
  per-cancer driver count both depend on this exact roster. Building it once unblocks both, and
  surfaces the breadth threshold choices (frequency cutoff, min studies) before they silently bias a
  downstream Tau or age test.
- **It is a clean, cheap cross-study replication play** — exactly the project's wheelhouse — that
  tests whether our aggregate reproduces an external gold standard (IntOGen) or diverges in a
  structured, composition-driven way (`h02`).
- **The risk if left unmeasured:** every "restricted driver" claim downstream rides on an *assumed*
  breadth distribution we have never looked at, and on whichever roster source happens to be wired
  in — with no calibration against IntOGen.

## What we can compute (substrate already on disk — but NOT from the annotated feathers)

- **Driver set + mode of action:** `data/cosmic_cgc.tsv` (`Role in Cancer` oncogene/TSG/fusion),
  `data/bailey2018_table_s1.tsv` (PanCanAtlas roster), IntOGen (`paper:MartinezJimenez2020`).
- **Breadth must be counted from raw per-cancer recurrence, NOT the `bailey2018_driver` flag.**
  `annotate_lib.py` ORs Bailey **PANCAN** drivers into *every* cancer-type row (documented in
  `doc/guides/canonical-outputs.md`), so a gene's apparent per-cancer breadth in
  `gene_cancer_study_annotated.feather` is contaminated by pan-cancer broadcast. The breadth count
  must come from the **un-broadcast** tables: `gene_cancer_study.feather` (raw per-(gene, cancer,
  study) counts) and/or `gene_cancer_pooled.feather` (t077 pooled per-(cancer, gene) with `k_studies`
  and `status`), thresholded into a per-gene "in how many cancer types is this gene recurrently
  mutated above background" count.
- **Three roster lenses, cross-checked:** (a) our cohort's empirical breadth (recurrence-defined);
  (b) Bailey per-cancer rosters with `PANCAN` rows **excluded or separately encoded**; (c) IntOGen's
  per-tumor-type calls. Agreement/divergence between (a) and (b)/(c) is the replication result.

## Confounds that decide interpretability

- **Ascertainment / composition (`q016`).** "Restricted" partly reflects *which cohorts exist* and
  *which panels were run*. A gene can look restricted because only one cancer type has deep coverage
  of it. Report breadth alongside per-cancer sample counts and panel-callability; cross-check against
  IntOGen's WES-based calls.
- **Frequency threshold sensitivity.** The breadth count depends on the recurrence cutoff and the
  min-studies rule. Sweep the threshold; report the distribution's stability, not a single cut.
- **Gene length (`h03`).** Long genes are over-called as recurrently mutated and inflate apparent
  breadth (passenger accumulation across many cancer types). Length-aware background needed before
  calling a long gene "broadly driving."
- **Hypermutators inflate breadth** (passenger recurrence in MMR/POLE-high cancers) — couple to
  `question:0047`; consider an `is_hypermutator`-excluded breadth as a parallel view.
- **Pan-cancer ≠ PANCAN-broadcast.** The whole point: do not let the annotation flag's broadcast
  semantics define the variable.

## Predictions

- Breadth is heavy-tailed: a small cancer-wide hub set (≈ the IntOGen 12 — TP53, KRAS, PIK3CA, PTEN,
  KMT2D, KMT2C, LRP1B, ARID1A, RB1, FAT4, NF1, CDKN2A) and a long restricted tail (~60% at 1–2 types).
- The hub set is **TSG/genome-guardian-enriched**; the restricted tail is **oncogene/lineage-factor-
  enriched** — the q042 prior, now measurable directly.
- Our composition shifts the tail (panel-restricted GENIE over-represents the genes its panels target),
  a structured divergence from IntOGen consistent with `h02`.

## Stop / null conditions

- If our empirical breadth distribution is **uncorrelated** with IntOGen's after composition
  adjustment, the cohort cannot define "restricted vs pan-cancer" reliably → q042/q041 must adopt the
  **external** roster (IntOGen/Bailey) rather than our recurrence-defined one, and say so.
- If breadth is dominated by threshold choice (no stable shape across cutoffs), report it as
  ascertainment-limited rather than a biological distribution.

## Connections to Project

- **Directly feeds:** `q042` (restricted-vs-pan-cancer specificity contrast — this *is* its missing
  roster step) and `q041` (per-cancer driver count).
- **Replication frame:** `h02` (structured cross-study ranking divergence), `q013` (replication rate),
  `q016` (panel ascertainment), `q017` (saturation).
- **Confounds:** `h03` (length), `q047` (hypermutation inflation).
- **Priority:** **P2** — computable today, no external ingest, unblocks two P3 questions. The natural
  first build of this batch.
