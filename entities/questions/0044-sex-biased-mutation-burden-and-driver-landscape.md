---
type: question
title: "Do somatic mutation burden and the driver landscape differ by patient sex\
  \ within cancer type \u2014 and are X-linked escape-from-inactivation tumor suppressors\
  \ male-biased for loss, beyond chance?"
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: question:0044-sex-biased-mutation-burden-and-driver-landscape
ontology_terms:
- sex differences
- tumor mutational burden
- X-linked tumor suppressor
- escape from X-inactivation
- loss of Y
datasets:
- metadata/samples_annotated.feather (per-sample TMB, is_hypermutator, cancer type)
- patient metadata `sex` (ingested via convert_to_feather.py SEX->sex)
- gene_cancer_study.feather (per-gene per-cancer mutation counts for OR tests)
- data/cosmic_cgc.tsv (Role in Cancer + genomic location for EXITS / ChrX/ChrY genes)
- data/uniprotkb_hsapiens_protein_lengths.tsv.gz (length control)
source_refs: []
related:
- topic:sex-biased-somatic-mutation-landscape
- topic:tumor-mutational-burden
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- hypothesis:0003-gene-length-confounds-literature-attention
- question:0016-panel-induced-ascertainment
- question:0043-driver-cancer-type-breadth-distribution
---

# Do somatic mutation burden and the driver landscape differ by patient sex within cancer type — and are X-linked escape-from-inactivation tumor suppressors male-biased for loss, beyond chance?

## Summary

Sex is a known, mechanistic axis of somatic cancer biology that this **mutation-only meta-analysis
has never examined**, despite `sex` being ingested into patient metadata. Three nested, increasingly
specific tests:

1. **Burden.** Is per-sample TMB higher in male tumors **within cancer type**, after adjusting for
   carcinogen-exposure signatures (smoking/UV) and panel callability?
2. **Per-gene driver bias.** Which drivers carry a male/female mutation odds-ratio skew within cancer
   type, beyond composition?
3. **The sharp, falsifiable one — EXITS genes.** A specific set of **X-linked tumor suppressors that
   escape X-inactivation** (KDM6A, KDM5C, ATRX, DDX3X, CNKSR2, MAGEC3, …) should show **male-biased
   loss-of-function**, because females retain a second active allele as a buffer. This is a
   gene-resolved prediction, not a diffuse "men get more cancer."

## Why It Matters

- A whole orthogonal axis the project can address with data already on disk, and a clean
  confound-rigor problem (does a sex-TMB gap survive cancer-type, exposure, and callability
  adjustment?) — the project's core competency applied somewhere new.
- The EXITS test is **mechanistically pre-specified and falsifiable**: a named gene set with a
  directional prediction grounded in X-inactivation biology, separable from generic burden effects.
- Risk if left unasked: any pan-cancer driver/burden claim we make is implicitly sex-pooled, hiding a
  structured biological axis (and a Simpson trap when cancer types have skewed sex ratios).

## What we can compute (substrate on disk)

- **Burden:** `samples_annotated.feather` TMB + `is_hypermutator`, stratified by `sex` **within
  cancer type**; exposure adjustment via the h08 signature covariates (smoking/UV/APOBEC).
- **Per-gene OR:** male/female mutation odds ratios from `gene_cancer_study.feather`, within cancer
  type, length-matched background (`h03`).
- **EXITS test:** restrict to the X-linked escape-TSG set (location + role from `data/cosmic_cgc.tsv`),
  test male-biased LoF-class mutations vs a matched autosomal-TSG and matched-length background.
- **Cannot / weak:** **loss of Y (LOY)** — ChrY copy-state is poorly callable from the targeted panels
  that dominate GENIE (most under-cover ChrY); flag as not-computed, not silently absent.

## Confounds that decide interpretability

- **Cancer-type composition (first-order).** Always stratify within cancer type; a pooled sex-TMB gap
  is mostly composition (sex-skewed cancer types). Simpson risk is the headline confound.
- **Carcinogen exposure.** Smoking (lung/head-neck) and UV (melanoma) are sex-skewed and inflate male
  TMB; adjust via h08 exposure-signature covariates before claiming an intrinsic sex effect.
- **Panel callability / ChrY coverage (`q016`).** Panel composition differs; ChrX/ChrY coverage is
  uneven. Sex-bias in a gene can be a coverage artifact.
- **Gene length (`h03`).** Any per-gene enrichment needs a length-matched null.
- **Age×sex.** Incidence age structure differs by sex; couple to `q041`/age handling (age is ordinal
  in our ingest).

## Predictions

- Male-biased TMB **within** several non-reproductive cancer types, **shrinking but not vanishing**
  after exposure adjustment (an intrinsic residual is the interesting, contestable claim).
- The **EXITS gene set** shows male-biased LoF beyond matched autosomal-TSG and length-matched
  background; a generic autosomal TSG set does **not** — the cleanest positive result.
- Most diffuse "sex-biased driver" signals **dissolve into composition**; the EXITS subset survives.

## Stop / null conditions

- If the EXITS male-bias **vanishes** under length + callability + composition adjustment, report no
  sex-resolved selection signal at our cohort's resolution (panel ascertainment dominates) — a clean
  negative, not a forced positive.
- LOY is **blocked** at the calling step for panel-dominated data; document, do not approximate from
  ChrY mutation counts.

## Connections to Project

- **Topic:** `topic:sex-biased-somatic-mutation-landscape` (background + external lit).
- **Shared machinery:** `topic:tumor-mutational-burden` (TMB denominator, hypermutator flags),
  `h08` (sex as a covariate in the signature-association scan), `q043` (breadth roster for per-gene
  tests).
- **Confounds:** `q016` (panel/ChrY), `h03` (length).
- **Priority:** **P3** — substrate on disk; gated on a one-pass `sex`-completeness audit (coverage
  varies by study/source) and the EXITS gene-set definition. A hypothesis ("EXITS genes are
  male-biased for LoF beyond matched background") can be promoted once a pilot shows direction.
