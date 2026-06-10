---
type: search
title: EHR-rich and clinically-annotated substrates for agnostic mutational-signature
  aetiology association
status: active
created: '2026-05-30'
updated: '2026-05-30'
id: search:0007-ehr-rich-substrates-for-agnostic-signature-association
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- topic:signature-decomposition-unmatched-normal
- question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross
- dataset:aacr-genie-bpc
- dataset:tcga-mc3
---

# EHR-rich and clinically-annotated substrates for agnostic mutational-signature aetiology association

## Scope

A scan of public oncology substrates usable as the **covariate side** of an agnostic
signature-aetiology association (`hypothesis:0007`). Selection criteria, in priority order:

1. **Co-measured somatic mutations** (so signature exposures `H` can be derived).
2. **Per-sample signature feasibility** — WES/WGS preferred; gene panels give too few mutations
   per sample and can only enter as cohort-pooled / refit (the binding constraint, `q018`).
3. **Rich clinical / EHR-like metadata** — treatment, ICD-O/ICD-10, histology, outcomes,
   vital status; ideally beyond the structured fields the pipeline already ingests.

Reconnaissance, not adoption. Adapter search (`science datasets search`) returned no relevant
hits — BPC / MSK-CHORD / MC3 live on Synapse (DUA-gated) or cBioPortal study pages, none indexed
by the zenodo/GEO adapters — so ranking is LLM-knowledge-driven, cross-referenced against existing
`doc/datasets/` notes.

## Candidate substrates

| Substrate | Mutations | Signature-grade? | Clinical / EHR richness | Access | Verdict for h08 |
|---|---|---|---|---|---|
| **GENIE BPC** (`dataset:aacr-genie-bpc`) | Panel | Pooled/refit only | **Highest public EHR-adjacency:** PRISSMM treatment, ICD-O, RECIST timelines, outcomes | Synapse + DUA | **Best EHR covariate source**; panel caps to cohort-level signatures |
| **TCGA MC3** (`dataset:tcga-mc3`) | WES consensus | **Per-sample de-novo OK** (2.9M PASS / 9,104 samples / 32 types) | Structured clinical + (via PanCanAtlas) co-measured mRNA | Public | **Best signature engine**; already ingested as `tcga_mc3` |
| **TCGA PanCanAtlas** (`dataset:tcga-pancanatlas`) | WES | Per-sample OK | Structured clinical + **co-measured expression** | Public | Co-expression covariate; pairs with MC3 |
| **MSK-CHORD** (`dataset:msk-chord`) | Panel (IMPACT) | Pooled/refit only | **NLP-extracted EHR features**, ~25k patients | Controlled | Secondary EHR candidate; verify NLP fields + license |
| **GENIE main** (`dataset:aacr-genie`) | Panel | Pooled only | Thin (OncoTree, age, sex, sample type; no treatment) | Synapse + DUA | Covariate-thin; value is panel-coverage BEDs |
| **METABRIC** (`dataset:data-brca-metabric`) | Targeted + CNA | Pooled only | Co-measured microarray expression + survival (breast) | Public | Single-tissue expression-vs-signature pilot |
| **PCAWG** (`dataset:pcawg`) | WGS | **Best per-sample** (incl. SV/CNV) | Sparse clinical | Controlled | Signature-ideal, covariate-poor |

## Key findings

- **The EHR wish is partially attainable.** Free-text symptom/bigram data is IRB-gated and not in
  public repos. The closest public substrates are **GENIE BPC** (PRISSMM phenomic timelines) and
  **MSK-CHORD** (NLP-derived EHR features) — structured *derivatives* of EHR text, not the text.
- **Fundamental tension** between the two selection axes: the EHR-richest substrates (BPC, CHORD)
  are **panel-sequenced** (weak per-sample signatures), while the best per-sample substrate (MC3
  WES + co-expression) carries only structured clinical metadata. → h08 runs on **two tracks**:
  - *Signature-grade:* MC3 (per-sample de-novo) × PanCanAtlas expression + structured clinical →
    positive-control + expression-discovery prong (H08a/b).
  - *EHR-covariate:* GENIE BPC / MSK-CHORD with **cohort-pooled** signatures × rich EHR terms →
    tests whether EHR-like covariates add aetiology signal the structured fields cannot.
- Expression as covariate is **already exported** for cBioPortal studies carrying mRNA
  (`export_study_expression.py`); no new acquisition for the signature-grade track.

## Open items

- Confirm MSK-CHORD NLP field availability + license terms.
- Confirm BPC top-level Synapse accession + which cohorts have signature-usable variant calls.
- Decide whether SV/CNV signatures (PCAWG) are in scope — currently out (CNV not ingested, `t055`).
