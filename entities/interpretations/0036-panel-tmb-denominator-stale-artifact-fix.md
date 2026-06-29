---
type: interpretation
title: Panel TMB denominator was WES-default for all panel samples in poc-2026-04-17
  (stale pre-t070 artifact); fixed + guarded
status: active
created: '2026-06-07'
updated: '2026-06-28'
id: interpretation:0036-panel-tmb-denominator-stale-artifact-fix
source_refs: []
related:
- question:0047-hypermutation-confound-on-driver-tissue-specificity
- question:0043-driver-cancer-type-breadth-distribution
- topic:tumor-mutational-burden
- interpretation:0038-q047-hypermutation-specificity-confound
- interpretation:0037-q043-driver-breadth-distribution
---

# Interpretation: panel TMB denominator was WES-default in poc-2026-04-17 — stale artifact, fixed + guarded

Project links: this interpretation updates `topic:tumor-mutational-burden` and supports the
downstream reads in `interpretation:0037-q043-driver-breadth-distribution` and
`interpretation:0038-q047-hypermutation-specificity-confound`.

## What was wrong

The `question:0047-hypermutation-confound-on-driver-tissue-specificity` first pass surfaced an anomaly: only Melanoma and Endometrial (the two TCGA WES studies)
had any hypermutators; **Colorectal — the canonical MSI-hypermutator type — had 7/1007**, with a
median TMB of **0.2 mut/Mb** (impossible; MSS CRC is ~3–5, MSI-H ~30–50). Root-causing it:

- `samples_annotated.feather` carried `tmb_source = wes_default` and `panel_callable_mb = 30.0` for
  **all 13,006 samples — including the 10,945 MSK-IMPACT panel samples**. The IMPACT panel covers
  ~0.9–1.2 Mb, so dividing panel mutation counts by a 30 Mb WES denominator made panel TMB **~25×
  too small**, which silently disabled hypermutator detection for the entire panel majority of the
  cohort (the GMM/relative/absolute flags all key on TMB).

## Root cause: stale artifact, not a code bug

The materialized `poc-2026-04-17` run (mtime 2026-04-17 18:07) **predates the t070 per-sample
panel-version-resolution machinery** (designed 2026-04-18). The current pipeline is correct:
`convert_to_feather` attaches per-sample `panel_id` from `data_gene_panel_matrix.txt`
(`resolve_panel_ids`), and `compute_per_sample_tmb` then takes the per-sample path against the
`panel_callable_mb` registry. The 04-17 artifact simply has no `panel_id` column, so every sample
fell through to the legacy study-level path → empty `study_panel_map` → `wes_default`.

## Fix

1. **Re-ran the TMB → hypermutator sub-DAG** (`convert_to_feather` → `compute_per_sample_tmb` →
   `combine_samples_tmb` → `fit_per_cancer_tmb_gmm` → `annotate_hypermutators`) plus the freq-table
   summary, on the current code/config. Verified result:

   | | stale (04-17) | fixed |
   |---|---:|---:|
   | `tmb_source` | wes_default ×13,006 | config_override ×10,945 (0.89–1.01 Mb) + wes_default ×2,061 (TCGA WES) |
   | CRC median TMB | 0.2 | **6.7** mut/Mb |
   | CRC hypermutators | 7 | **88** (81 MSI/GMM-upper + 7 POLE) |
| testable cancer types (`question:0047-hypermutation-confound-on-driver-tissue-specificity`) | 2 | **8** (CRC, NSCLC, Bladder, Esophagogastric, Hepatobiliary, Endometrial, Melanoma, cSCC) |

   In `interpretation:0036-panel-tmb-denominator-stale-artifact-fix` for `question:0047-hypermutation-confound-on-driver-tissue-specificity`,
   panel cancers now flag sensibly: NSCLC 6.3%, CRC 8.7%, Bladder 7.6%, Hepatobiliary 5.4% (all
   previously 0%); low-TMB types stay ≈0% (Glioma, Pancreatic, RCC, Prostate).

2. **Durable fail-loud guard** (`assert_panel_bearing_resolved` in `compute_per_sample_tmb.py`, with
   tests): a study declared in `config['panel_bearing_studies']` that reaches TMB computation
   without a usable per-sample `panel_id` now **raises** instead of silently applying the WES
   default. This implements the project's "fail early / avoid silent fallbacks" rule for exactly the
   failure mode that produced this artifact — a ~25×-wrong-but-plausible TMB would otherwise pass
   unnoticed.

## Downstream impact (corrected)

- **`question:0043-driver-cancer-type-breadth-distribution`:** the hypermutator-exclusive restricted-driver fraction at ≥5% rises from 52.1%
  (inclusive) to **68.1%** (was 60.4% on stale flags) — IntOGen's 63% is now *bracketed*. Breadth
  inflation by hypermutators is larger than the stale run implied (253 drivers lose breadth at ≥2%,
  186 at ≥5%).
- **`question:0047-hypermutation-confound-on-driver-tissue-specificity`:** the per-sample driver-share dilution — previously "under-identified on panel data" — is
  **now clearly detectable** across the 8 testable cancer types (driver share of load drops 0.10–0.22
  in hypermutators; CRC 0.89→0.76, NSCLC 0.93→0.78, cSCC 1.00→0.78). The "CRC under-flagging"
  follow-up is resolved here (it *was* this TMB bug).

## Not-yet-refreshed (follow-up)

Any other artifact in `poc-2026-04-17` that consumed the old `samples_annotated` hypermutator flags
(e.g. `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and` covariate tables, signature `_exclusive` views, QA reports) may still be stale. The freq
tables (`gene_cancer_study*`) were regenerated; a broader `snakemake` target sweep on the POC out_dir
would refresh the rest. Flagged, not silently assumed clean.
