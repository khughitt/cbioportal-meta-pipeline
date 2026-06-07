---
id: "question:q041-driver-complexity-vs-median-age-at-diagnosis"
type: "question"
title: "Does per-cancer-type driver complexity track median age at diagnosis in the aggregated cohort, once the age->mutation-detection confound is controlled?"
status: "active"
ontology_terms:
  - multistage carcinogenesis
  - age at diagnosis
  - driver gene count
  - cancer type
datasets:
  - "cBioPortal clinical AGE field (age at diagnosis, per study)"
  - "AACR GENIE AGE_AT_SEQ_REPORT (age at sequencing, NOT onset)"
  - "gene_cancer_study_annotated.feather (Bailey 2018 driver overlay)"
  - "studies/{id}/mut/dndscv/genes.feather (per-study dN/dS driver calls, opt-in)"
  - "metadata/samples_annotated.feather (per-sample TMB / hypermutator class)"
  - "Belikov 2017 per-cancer-type key-event estimates (external calibration)"
  - "SEER age-incidence curves (external benchmark, not in project)"
source_refs:
  - "paper:Belikov2017"
  - "paper:ArmitageDoll1954"
  - "paper:Knudson1971"
  - "paper:TomasettiVogelstein2015"
  - "paper:RozhokDeGregori2015"
related:
  - "topic:multistage-carcinogenesis-and-age-of-onset"
  - "theme:temporal-structure-of-carcinogenesis"
  - "hypothesis:h06-pre-malignant-n-minus-1-driver-carriage"
  - "hypothesis:h04-mhn-pathway-ordering"
  - "question:q012-mutation-ordering-cross-sectional-inference"
  - "discussion:2026-06-07-age-of-onset-and-multistage-mutation-requirement"
created: "2026-06-07"
updated: "2026-06-07"
---

# Does per-cancer-type driver complexity track median age at diagnosis, once the age->detection confound is controlled?

## Summary

The multistage model (`paper:ArmitageDoll1954`, `paper:Knudson1971`, MVK) predicts that cancer
types requiring **more rate-limiting driver events** should, all else equal, reach diagnosis
**later** (older median age), and types requiring **fewer** (pediatric, germline-pre-loaded,
developmental) should present **earlier**. `paper:Belikov2017` estimates a per-cancer-type number
of "key carcinogenic events" directly from population age-incidence curves. The question here is
the **prevalent-cohort echo** of that result: across the cancer types in our aggregated cBioPortal
/ GENIE cohort, does a *mutation-derived* proxy for **driver complexity** correlate with **median
age at diagnosis**, in a way that survives the confounds — most importantly the circularity that
older patients accumulate more detectable mutations (drivers included) regardless of how many were
*rate-limiting*?

This is explicitly a **correlational, suggestive** test. The rigorous estimate of "number of
required hits" lives in **incidence-vs-age** data (Armitage-Doll / Belikov), which we do not have.
Our prevalent mutation cohort can offer a cross-type scatter and a sanity check against Belikov,
not an identification of k.

## Why It Matters

- It is the **count/timing sibling** of the project's ordering work (`q012`, `h04`) and the
  driver-carriage work (`h06`): ordering asks *in what sequence*; this asks *how many* and
  *how early*. Same cohort, same callability mask, same driver annotations.
- It turns the user's three candidate explanations of differential age-of-onset (number of
  required mutations; cell-division rate; target-cell number) into the *one* that is even
  partially testable in mutation data — factors 2 and 3 need stem-cell-division counts we do not
  have (`paper:TomasettiVogelstein2015`), so they remain interpretive background only.
- A clean *negative* (no correlation, or a correlation fully explained by age->detection) is
  itself informative: it would say our prevalent cohort cannot see the multistage signal, and the
  question must be deferred to incidence data.

## What we can compute

- **Median age at diagnosis per cancer type** (per histology, to avoid Simpson's paradox).
  **Prerequisite — there is no age-normalized artifact in the pipeline yet, so this is not
  computable today.** The `samples_annotated.feather` QA contract requires only
  study/sample/cancer_type/TMB/hypermutator fields, *not* age
  (`validate_mutation_pipeline_artifacts.py::validate_samples_annotated`), and the only existing
  AGE extraction is TCGA/PanCanAtlas-specific — keyed on the 12-char TCGA barcode in
  `build_h08_covariates.py`. q041 is therefore **gated on a precursor task** that audits the
  per-study clinical age fields (heterogeneous keys: `AGE`, `AGE_AT_DIAGNOSIS`, GENIE
  `AGE_AT_SEQ_REPORT`, …), normalizes units and redaction conventions (e.g. the ">89" cap), and
  emits a canonical per-sample/per-study **q041 age table**. Without that artifact the question is
  not executable.
  **GENIE caveat:** `AGE_AT_SEQ_REPORT` is age at *sequencing*, often well after onset; GENIE
  studies must be handled separately or excluded from the onset proxy.
- **Driver-complexity proxy** (prefer *driver-set size*, never raw TMB):
  - (a) count of recurrent `paper:Bailey2018` drivers reaching a frequency threshold per type
    (`gene_cancer_study_annotated.feather`);
  - (b) count of dN/dS-significant genes per type (`run_dndscv.R` output, opt-in);
  - (c) MHN path length / number of high-hazard edges per histology from `h04`, once available.
  **Demotion — this is a weak, biased proxy for Belikov's k, not a measurement of it.**
  `paper:Belikov2017`'s k counts *all* key carcinogenic events — SNVs, indels, **CNVs, fusions,
  and epimutations** (`doc/papers/Belikov2017.md`) — whereas (a)/(b) are **mutation-observable
  gene rosters** only, and even (c) rides on the same SNV/indel substrate. Cancer types whose
  required events are dominated by **non-SNV modalities** will be systematic under-counts and are
  **expected calibration failures** — not only the pediatric/fusion cases, but adult
  modality-mismatch types: **prostate** (CNA- and *ETS*-fusion-driven), **multiple myeloma** (IgH
  translocations, hyperdiploidy), and **CNA-heavy** tumors generally. Name, and either exclude or
  annotate, these before reading any cross-type correlation.
- **External calibration:** `paper:Belikov2017` per-type key-event counts; SEER incidence slopes.

## The confounds that decide whether this is interpretable

- **Age -> mutation-detection circularity (the killer).** Older patients carry more passengers
  *and* more incidentally detectable drivers. If the complexity proxy is mutation-count-derived,
  a positive age/complexity correlation can be **mechanically induced** rather than biological.
  **Mind the level-of-analysis mismatch:** the primary proxy is a *per-cancer-type* driver-set
  size built from already-aggregated outputs, so a per-sample TMB regression **cannot be bolted on
  post hoc** to deconfound it. Deconfounding requires rebuilding the driver-counting step at
  **sample level**: count drivers within narrow **age (and/or TMB) strata** per histology and
  compare strata, or use age/TMB-stratified driver calls, or restrict to *recurrent/known* drivers
  whose detection is least age-sensitive. If the age/complexity relationship survives stratified
  re-counting it is structure; if it appears only in the pooled aggregate, it was detection.
- **Age at sequencing != age at onset** (GENIE especially); screening/ascertainment shifts
  apparent onset (e.g. PSA, mammography, colonoscopy).
- **Panel vs WES** asymmetry changes how many drivers are *callable* per sample — condition on
  callability (same mask as `t078`/`q012`).
- **Subtype pooling** (Simpson): per-histology, not per-broad-type.
- **Mechanistically different early-onset classes**: pediatric/embryonal tumors are
  fusion/CNV-driven with few SNV drivers (`paper:Knudson1971` two-hit; Gröbner/Ma 2018), and
  germline-syndrome cases pre-load a hit (Li-Fraumeni, Lynch, BRCA). These must be **flagged and
  modeled separately**, not pooled into the SNV-driver-count regression.
- **Selection-landscape counterweight** (`paper:RozhokDeGregori2015`): even a clean age/complexity
  relationship does not establish that mutation *supply* sets timing — aged-tissue selection may.
  This question can describe a correlation; it cannot adjudicate the supply-vs-selection mechanism.

## Predictions (loose, directional)

- A weak-to-moderate **positive** rank correlation between driver-set size and median age at
  diagnosis across adult solid types, *if* it survives detection-confound controls.
- Pediatric/embryonal and germline-syndrome-enriched types sit as **low-driver, early-onset**
  outliers; testicular (germ-cell) is an early-onset outlier the SNV-count model will not explain.
- The ranking should correlate (loosely) with `paper:Belikov2017`'s key-event estimates; large
  disagreements localize where prevalent-cohort detection diverges from incidence-curve fitting.

## What would make this uninformative (stop conditions)

- The age/complexity correlation is fully accounted for by age->TMB detection (vanishes within
  age bands / after TMB regression) — then the prevalent cohort cannot see multistage structure.
- Per-histology sample sizes are too small for a stable median-age + driver-count estimate across
  enough types to support a cross-type correlation.

## Connections to Project

- **Hypotheses:** `h06` (how many of the n drivers are carried at a stage — the count axis),
  `h04` (the order axis).
- **Sibling question:** `q012` (can order be inferred at all from cross-sectional data — shares
  every confound here).
- **Topic / theme:** `topic:multistage-carcinogenesis-and-age-of-onset` (background),
  `theme:temporal-structure-of-carcinogenesis` (organizing frame).
- **Priority:** P3 — a scoped, low-cost descriptive analysis once driver annotations + a clean
  per-histology age table exist; not ahead of `t078`/`q012` infrastructure.
- **Candidate follow-up (not yet filed):** a methodological question on **age as a covariate
  inflating mutation/driver burden** project-wide (touches TMB, the SBS1/SBS5 clock signatures of
  `q023`) — flag if this confound recurs outside the age-of-onset thread.
