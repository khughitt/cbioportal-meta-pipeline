---
type: topic
title: Sex-biased somatic mutation burden and driver landscape across cancer types
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: topic:sex-biased-somatic-mutation-landscape
ontology_terms:
- sex differences
- tumor mutational burden
- X-linked tumor suppressor
- loss of Y
- escape from X-inactivation
source_refs: []
related:
- question:0044-sex-biased-mutation-burden-and-driver-landscape
- topic:tumor-mutational-burden
- topic:cancer-driver-genes
- hypothesis:0003-gene-length-confounds-literature-attention
- question:0016-panel-induced-ascertainment
---

# Sex-biased somatic mutation burden and driver landscape across cancer types

## Scope

An orthogonal axis the project has **never touched**: do somatic **mutation burden** and the
**driver landscape** differ between male and female patients, across cancer types, beyond what
cancer-type composition and assay differences explain? The `sex` field is ingested into patient
metadata (`convert_to_feather.py`), so the substrate exists; the literature target is well
established but not yet in the project library.

## Why sex is a real, mechanistic axis (not just a covariate)

The established (external, not-yet-in-library) findings this topic organizes:

- **Higher TMB in male tumors** across most non-reproductive cancer types, only partly explained by
  carcinogen exposure (smoking, UV) — a residual after exposure adjustment is reported pan-cancer.
- **X-linked tumor suppressors that escape X-inactivation (EXITS genes).** Genes such as **KDM6A,
  KDM5C, ATRX, DDX3X, CNKSR2, MAGEC3** carry a second active X-allele in females, giving females a
  buffer against biallelic loss — predicting **male-biased loss-of-function** in these specific TSGs.
  This is a clean, gene-resolved, falsifiable prediction (not a diffuse "men get more cancer").
- **Mosaic loss of chromosome Y (LOY / mLOY)** in male tumors and in clonal hematopoiesis — a
  male-only somatic event class with prognostic associations; whether it is callable from
  panel/targeted data is an open question (most panels under-cover ChrY).
- **Sex-biased driver frequencies** beyond the X — e.g. reported BAP1, TP53 pathway, and signature
  (APOBEC vs smoking) differences — many of which dissolve into cancer-type composition and must be
  tested *within* cancer type.

## What this project can compute vs what it can't

- **Have:** `sex` (patient metadata), per-sample TMB (`compute_per_sample_tmb`, the t081 pipeline),
  `is_hypermutator`, gene×cancer mutation counts, COSMIC CGC role/location labels. So: sex-stratified
  TMB *within cancer type*; per-gene male/female mutation odds ratios; the EXITS-gene male-bias test;
  signature-exposure-by-sex (h08 substrate).
- **Cannot (or only weakly):** **LOY** — ChrY copy-state is poorly callable from the targeted panels
  that dominate GENIE; treat as a flagged-not-computed sub-question. Germline/ancestry interactions —
  out of scope for a mutation-only pipeline.
- **First-order confounds:** cancer-type composition (always stratify within type; Simpson risk),
  panel callability and ChrY coverage (`q016`), carcinogen-exposure signatures (smoking/UV — adjust
  via h08 covariates), and the age×sex interaction in incidence.

## Connections

- **Question:** `q044` (the falsifiable sex-bias tests).
- **Shared machinery:** `topic:tumor-mutational-burden` (the TMB denominator + hypermutator flags),
  `hypothesis:h08-...` (signature-by-covariate scan — sex is a covariate it can carry),
  `topic:cancer-driver-genes` (the driver roster), `q043` (breadth, for per-gene tests).
- **Confounds:** `q016` (panel/ChrY ascertainment), `h03` (length null on any per-gene enrichment).
- **External / not-yet-in-library:** the EXITS-gene paper (male-biased X-linked TSG LoF), pan-cancer
  sex-TMB analyses, and the LOY/mLOY clonal-mosaicism literature — candidates for a future
  `/science:research-papers` pass *if* a pilot shows the axis is worth formalizing here.

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
