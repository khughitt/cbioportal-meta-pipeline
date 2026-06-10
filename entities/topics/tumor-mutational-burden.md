---
type: topic
title: "Tumor mutational burden (TMB) \u2014 definition, measurement, harmonization"
status: active
created: '2026-04-13'
updated: '2026-04-14'
id: topic:tumor-mutational-burden
ontology_terms: []
source_refs: []
related:
- paper:Zehir2017
- paper:Pugh2022
- paper:Bandlamudi2026
- paper:Suehnholz2024
- topic:targeted-panel-sequencing-bias
---

# Tumor mutational burden (TMB) — definition, measurement, harmonization

## Summary

TMB (mutations per megabase of coding sequence) is a clinically-used summary statistic — TMB-H
(typically ≥10 mut/Mb) is an FDA-recognized pan-cancer biomarker for pembrolizumab eligibility
(Suehnholz 2024 confirms +9.2 pp pan-cancer Level 1 contribution). Its definition and
measurement vary substantially between panels and WES, and naive panel-derived TMB is not
directly comparable to WES-derived TMB without per-panel calibration.

## Key Concepts

- **TMB definition.** Mutations per megabase of *callable* coding sequence. Variants typically
  count: synonymous + non-synonymous, or non-synonymous only (pipeline-dependent). Key choice
  point: include indels, fusions, structural variants? (Most TMB definitions: SNV + small indels
  only.)
- **Panel TMB.** Computed per-panel using the panel's own callable-coding length as denominator.
  Zehir 2017: MSK-IMPACT panel-TMB correlates R²=0.76 with WES on matched samples. Reasonable
  but not perfect.
- **TMB-H thresholds vary by setting.** FDA pembrolizumab indication uses 10 mut/Mb; some
  research / clinical-trial protocols use 16 mut/Mb. Threshold choice affects classification of
  ~5-15% of tumors.
- **Hypermutation phenotypes** drive TMB-H: MSI (MMR deficiency), POLE / POLD1 mutator, UV-
  driven (melanoma), tobacco (lung). These are biologically distinct mechanisms with different
  immunotherapy implications.

## Current State of Knowledge

- **Friends-of-Cancer-Research / Buchhalter** TMB harmonization work proposes a calibration
  framework for panel-vs-WES TMB. Not yet adopted as a published correction in cBioPortal.
- **Pugh 2022** mentions a TMB harmonization model for GENIE but does not quantify it; per-
  assay TMB values across the 91 GENIE panels remain uncorrected.
- **Bandlamudi 2026** uses the standard MSK-IMPACT TMB and reports it as a per-sample annotation,
  not as a cross-panel-comparable value.
- Consensus emerging: report panel-TMB with an explicit panel-version flag; don't aggregate
  across panels without per-panel calibration.

## Controversies & Open Questions

- **Should our pipeline define a TMB axis at all?** If yes, with what definition and on what
  callable-coding denominator?
- **Per-panel calibration to WES** — feasible only if we have matched panel + WES samples
  (rare); otherwise rely on Friends-of-Cancer-Research published calibration tables.
- **TMB-H under CH contamination.** Tumor-only-called samples can have inflated TMB from CH
  variants; matched-normal cohorts should report lower TMB for older patients than unmatched
  cohorts. See `topic:clonal-hematopoiesis-contamination`.

## Relevance to This Project

**Implemented** as of t081 (plan: `doc/plans/2026-04-13-t081-hypermutator-annotation-pipeline-
plan.md`; subtasks t092–t099). The pipeline emits `metadata/samples_annotated.feather` as a
per-sample annotation feather carrying TMB + hypermutator status + audit trail:

| Column | Type | Source |
|---|---|---|
| `study_id`, `sample_id`, `cancer_type`, `cancer_type_detailed` | | carried from per-study samples |
| `tmb`, `tmb_log10`, `mutation_count` | float / int | `compute_per_sample_tmb` (protein-altering variant_class filter per Chalmers 2017 / FMI convention) |
| `panel_callable_mb`, `tmb_source` | float / str | `build_panel_callable_sizes` (sources: `bed_sum` / `config_override` / `wes_default`) |
| `msi_type`, `msi_score` | str / float | `msi_normalization.normalize_msi_columns` (parsed from `MSI_TYPE` / `MSI_STATUS` / `MSI_SCORE` / `MSI_SENSOR_SCORE`; normalized to `{MSI-H, MSI-L, MSS, Indeterminate}`) |
| `pole_hotspot_detected`, `pold1_hotspot_detected` | bool | `detect_polymerase_hotspots` (canonical 8-site POLE + 6-site POLD1 literature sets) |
| `tmb_zscore_within_cancer`, `gmm_posterior_upper` | float | `fit_per_cancer_tmb_gmm` (pinned `random_seed` for reproducibility; Hartigan dip test + ΔBIC selection) |
| `hypermutation_score`, `is_hypermutator`, `hypermutator_reason` | float / bool / str | `annotate_hypermutators` canonical 8-row decision table (plan finding #4) |
| `is_hypermutator_absolute` (≥10 mut/Mb Campbell 2017), `is_hypermutator_ultra` (≥100 mut/Mb), `is_hypermutator_relative` (per-histology top-20% Samstein 2019) | bool | `annotate_hypermutators` parallel flags per t089 dual-view recommendation |

The cross-study `gene_cancer_study*.feather` outputs carry paired
`num_inclusive` / `num_exclusive` / `ratio_inclusive` / `ratio_exclusive` per-study columns
plus pooled `mean_inclusive` / `mean_exclusive` (t098). Downstream consumers (e.g.
`summary.Rmd`) can select which view to report per audit-checklist item
`agg.15`. Default shipping behavior: both are emitted; primary displayed column is
`mean_inclusive` unless t079 pre-registration explicitly overrides.

**Residual follow-ups** not part of t081:
1. Panel-vs-WES FoCR Phase II calibration (Vega 2021) not yet applied to our computed TMB
   values — the pipeline reports raw per-panel TMB with a panel-source provenance column;
   cross-panel calibration is a future task (see `topic:cross-panel-normalization-methods`).
2. Downstream aggregations using `mean_inclusive` implicitly INCLUDE hypermutators — be wary
   when interpreting driver-rate differences for MSI-CRC / UCEC / melanoma cancers where the
   hypermutator tail is dominant.

## Key References

Zehir2017 (panel-TMB ~ WES-TMB R² calibration); Pugh2022 (acknowledges panel-TMB harmonization
need without solving it); Bandlamudi2026 (current MSK-IMPACT TMB usage); Suehnholz2024 (TMB-H as
Level 1 pan-cancer biomarker contribution to actionability landscape). Follow-up search t025 for
Friends-of-Cancer-Research / Buchhalter TMB harmonization paper still queued.
