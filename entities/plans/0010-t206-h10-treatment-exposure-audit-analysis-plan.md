---
type: plan
title: t206 H10 treatment-exposure audit analysis plan
status: ready-with-caveats
created: '2026-06-01'
updated: '2026-06-01'
id: plan:0010-t206-h10-treatment-exposure-audit-analysis-plan
related:
- hypothesis:0009-treatment-induced-signature-frequency-contamination
- question:0024-treatment-exposed-cohort-chemotherapy-signature
- question:0027-does-excluding-treatment-signature-high-samples
- task:t181
- task:t206
skills_loaded:
- id: data-genomics-somatic-mutation-qa
  reason: H10 tests mutation-frequency table shifts across cBioPortal cohorts.
- id: data-genomics-mutational-signatures-and-selection
  reason: treatment-signature-high samples and hypermutator exclusions can drive gene
    rankings.
- id: statistics-power-floor-acknowledgement
  reason: study/cancer strata may be too sparse to interpret unchanged rankings as
    null evidence.
- id: statistics-bias-vs-variance-decomposition
  reason: cohort-treatment labels are label-biased metadata, not direct exposure measurements.
- id: statistics-sensitivity-arbitration
  reason: exposed-study, metastatic-review, and therapy-signature-high exclusions
    need fixed arbitration.
---

# t206 `H10` treatment-exposure audit analysis plan

## Analysis Question

Which non-TCGA cBioPortal studies in the project configs are sufficiently enriched for prior treatment, relapse, metastatic sampling, or therapy-specific trial ascertainment that `H10` should test whether they alter pooled gene-by-cancer mutation-frequency outputs?

The immediate analysis is an audit and readiness step, not the final `H10` verdict.
It prepares a label table and impact-test design for `hypothesis:0009-treatment-induced-signature-frequency-contamination`.

## Related Hypotheses / Inquiries / Tasks

This plan executes the first half of `task:t206` and extends the `H08`-facing treatment stratum from `task:t181`.
It directly supports `question:0024-treatment-exposed-cohort-chemotherapy-signature` and prepares the denominator/exclusion logic needed by `question:0027-does-excluding-treatment-signature-high-samples`.

## Data Inputs and Provenance

Primary inputs:

- `code/config/config-full.yml` as the broad cBioPortal study universe for the first audit pass.
- `/data/raw/cbioportal/<study_id>/meta_study.txt` as the study-level metadata source.
- `/data/raw/cbioportal/<study_id>/data_clinical_sample.txt` as the optional source for clinical columns that can refine sample-level fractions.
- Existing frequency-table scripts, especially `code/scripts/create_freq_tables.py` and `code/scripts/create_combined_gene_cancer_freq_table.py`, for the later impact pass.
- Existing hypermutator-inclusive/exclusive columns as the implementation pattern for paired denominator reporting.

The first local scaffold output is `results/h10-treatment-exposure-audit-2026-06-01.tsv`.
This generated table is not committed; it can be regenerated with:

```bash
uv run --frozen python code/scripts/audit_treatment_exposed_studies.py \
  --config code/config/config-full.yml \
  --data-dir /data/raw/cbioportal \
  --output results/h10-treatment-exposure-audit-2026-06-01.tsv
```

The current scaffold finds 167 non-TCGA studies in `config-full.yml`: 11 `flag_exposed`, 42 `review_for_fraction`, 2 `needs_manual_review`, and 112 `do_not_flag`.
The review group currently includes 20 metadata-enriched metastatic/advanced studies and 22 studies with treatment-relevant clinical columns but neutral metadata.

## Required Input Inspection

Inspect every `flag_exposed` study manually before writing it into config.
The metadata classifier is intentionally conservative but still text-based; terms like `treated`, `exposed`, and `resistant` need human review when they could refer to trial context rather than prior therapy.

Inspect every `review_for_fraction` study with clinical signal columns.
The strongest candidates are metastatic or recurrent cohorts whose `data_clinical_sample.txt` has fields such as `TUMOR_TREATED`, `CALC_TREATMENT_NAIVE`, `METASTATIC_STATUS`, or treatment-response fields.

Inspect `clinical_signal_present` studies separately from metastatic/advanced studies.
These may provide useful per-sample fractions even when study-level metadata is neutral.

Resolve missing metadata for `aml_stjude_2024` and `msk_impact_50k_2026` before any all-config label freeze.
If the raw directory is intentionally absent, record that as unavailable rather than silently excluding it.

## Preprocessing / Normalization Checks

Do not infer treatment exposure from SBS11/SBS31/SBS35/SBS87 when constructing the cohort flag.
Those signatures are outcomes or impact-test filters, and using them to define the covariate would collapse exposure and endpoint.

Normalize study labels into three audited tiers:

| Tier | Meaning | Default config action |
|---|---|---|
| `explicit_treatment_exposed` | metadata indicates prior/ongoing treatment, post-therapy, resistant/refractory, or therapy-specific exposure | eligible for `treatment_exposed_studies` after manual confirmation |
| `advanced_metastatic_enriched` | metastatic, recurrent, relapsed, or advanced cohort without explicit prior-treatment evidence | keep out of `treatment_exposed_studies`; use for sensitivity or fraction review |
| `treatment_naive_or_pretreatment` | explicitly treatment-naive, previously untreated, or pre-treatment sampling | do not flag as treatment-exposed |

When sample-level clinical fields support a fraction, write `treatment_exposed_study_fractions` rather than only a binary study flag.
Fractions should be based on documented clinical labels, not on mutation-signature burden.

## Independent Unit and Denominator

The audit unit is the study, but the impact-test unit is the study-cancer-gene cell with per-gene callable denominators.
Do not count multiple samples from the same patient as independent evidence unless the frequency pipeline already collapses or models that multiplicity.

For the frequency-table impact pass, denominators must remain panel-aware.
The treatment-excluded denominator should be parallel to the existing hypermutator-excluded denominator: `n_samples_treatment_inclusive`, `n_samples_treatment_exclusive`, and paired mutation counts/ratios should be explicit rather than replacing existing `inclusive`/`exclusive` fields.

## Estimand and Primary Metric

The primary impact estimand is the change in pooled gene-by-cancer mutation frequency after excluding confirmed treatment-exposed study strata, measured on the existing ratio scale.

Primary metrics:

- Absolute ratio shift: `mean_treatment_inclusive - mean_treatment_exclusive`.
- Rank shift among genes within cancer type, using the same ranking field used by the current consumer-facing table.
- Driver-list perturbation among Bailey/driver-overlaid rows when the annotated table is available.

The audit itself does not estimate `H10` support.
It only decides whether the `H10` impact pass is ready and which labels are allowed into that pass.

## Model / Test Assumptions

The first impact pass should be deterministic table differencing, not a regression model.
That is appropriate because the immediate decision is whether the public deliverable changes enough to justify deeper modeling.

The pass assumes that confirmed treatment-exposed cohorts are a nuisance stratum and that their exclusion answers a deliverable-sensitivity question, not a causal effect of treatment on mutation frequency.
Metastatic-only review cohorts should not be mixed into the primary treatment-exposed exclusion unless explicit prior-treatment evidence is added.

## Power Floor or Resolution Limit

Null impact is interpretable only in cancer types with both enough callable samples and enough exposed/non-exposed contrast.
If a cancer type has fewer than two contributing studies after exclusion or fewer than 100 callable non-exposed samples for a gene, label unchanged ranks as `underpowered_non_arbitrating`.

For rare cancers, the audit may still be useful for provenance but should not arbitrate `H10`.
The expected high-value strata are cancers with treated and treatment-naive comparators in the same broad cancer family, such as breast, prostate, melanoma, bladder, lung, and colorectal cohorts.

## Bias vs Variance Risks

The dominant risk is label bias, not random variance.
Metadata can say `metastatic` without documenting prior treatment, while clinical sample files can encode treatment status inconsistently across studies.

Panel bias is a second major risk.
Treated cohorts are often targeted-panel cohorts and may differ in gene territory from WES/WGS cohorts.
The impact pass must preserve panel-aware callable denominators and should report assay class alongside any rank shift.

The leakage risk is using therapy signatures to define exposure.
Avoid this in the primary cohort-label audit; signature-high filtering can be a separate sensitivity with explicit post-label status.

## Sensitivity Arbitration

Primary label set: manually confirmed `explicit_treatment_exposed` studies.

Mandatory sensitivity 1: add manually reviewed `advanced_metastatic_enriched` studies with documented treatment fractions.
If this changes the direction or top-driver perturbation while the primary set does not, report `H10` as `cohort-stage-sensitive`, not as clean treatment-signature contamination.

Mandatory sensitivity 2: therapy-signature-high exclusion among samples where signature assignment is eligible and count-floor-passing.
If signature-high exclusion changes rankings but metadata-only exclusion does not, report the effect as `signature-detectable_but_metadata-limited`.

Mandatory sensitivity 3: hypermutator-excluded baseline.
If `H10` effects disappear after existing hypermutator exclusion, report them as `hypermutator_overlapping`; if they persist, `H10` remains distinct from the current hypermutator layer.

## Required Output Artifacts

This t206 slice should produce:

- `code/scripts/audit_treatment_exposed_studies.py`, a deterministic metadata/clinical-column audit scaffold.
- `results/h10-treatment-exposure-audit-2026-06-01.tsv`, a regenerated local audit table.
- A manual-review note or interpretation document listing the confirmed config changes.
- Config additions for `treatment_exposed_studies` and `treatment_exposed_study_fractions` only after manual review.
- A separate implementation plan for the paired treatment-inclusive/exclusive frequency-table impact pass.

## Aspect-Contributed Sections

Computational-analysis requirements:
the audit script should be deterministic, test-covered, and runnable from a project config plus `data_dir`.
Generated result tables remain in `results/` and are not committed unless promoted to a small curated manifest.

Software-development requirements:
classifier behavior should stay small and explicit.
No compatibility layer is needed; future refinements should extend the audit helper or replace it with a curated manifest, not introduce a parallel legacy path.

Causal-modeling requirements:
do not describe the impact pass as estimating the causal effect of treatment.
The estimand is deliverable sensitivity to cohort composition and therapy-signature strata.
