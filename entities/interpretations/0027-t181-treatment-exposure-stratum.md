---
type: interpretation
title: "t181 treatment-exposure stratum for covariate-association scan \u2014 MC3/TCGA carries no study-level\
  \ treated confound; 55 patient-level neoadjuvant positives"
status: active
created: '2026-06-01'
updated: '2026-06-01'
id: interpretation:0027-t181-treatment-exposure-stratum
source_refs:
- task:t181
date: '2026-06-01'
related:
- task:t181
- hypothesis:0009-treatment-induced-signature-frequency-contamination
- question:0024-treatment-exposed-cohort-chemotherapy-signature
---
# t181 — treatment-exposure stratum for covariate-association scan

Date: 2026-06-01

## Question

Does the `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and` covariate substrate carry an explicit treatment-exposure stratum so that treatment-induced signatures can be handled as nuisance context rather than silent batch structure?

## What Changed

`code/scripts/build_h08_covariates.py` now writes four treatment-exposure fields:

- `treatment_exposed_clinical`: patient-level `HISTORY_NEOADJUVANT_TRTYN`.
- `treatment_exposed_study`: config-driven study/cohort flag, parallel to `matched_normal_studies`.
- `treatment_exposed_fraction`: audited cohort-level fraction treated.
- `treatment_exposed`: combined adjustment covariate, equal to the OR of the clinical and study-level flags.

The current covariate-association run config records `tcga_mc3` as study-level unexposed:

```yaml
treatment_exposed_studies: []
treatment_exposed_study_fractions:
  tcga_mc3: 0.0
```

This is an explicit substrate audit, not an inference from treatment-signature exposures.
The leakage firewall remains intact: SBS11/SBS31/SBS35/SBS87 exposure values are not used to define the treatment flag.

## Rebuilt Artifact

`results/signature-h08-arms-2026-05-31/association/h08_covariates.feather` was rebuilt with 3,457 samples and 38 columns.
The new treatment fields have the following realized pattern:

| Field | Realized value |
|---|---|
| `treatment_exposed_study` | 0 for all 3,457 MC3 samples |
| `treatment_exposed_fraction` | 0.0 for all 3,457 MC3 samples |
| `treatment_exposed_clinical` | 55 positives among 3,385 non-missing clinical labels |
| `treatment_exposed` | 55 positives after combining clinical + study flags |

The denominator manifest now records the treatment-exposure rule and the audited config values.

## Interpretation

This closes the `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`-facing part of `question:0024-treatment-exposed-cohort-chemotherapy-signature`: the positive-control scan substrate no longer relies on an implicit or missing treatment history field.
For MC3, there is no study-level treated-cohort confound, but a small patient-level neoadjuvant signal remains available as an adjustment covariate.

This does not yet test `hypothesis:0009`.
The next `hypothesis:0009-treatment-induced-signature-frequency-contamination` step would be a broader cohort audit for non-TCGA cBioPortal studies and a frequency-table exclusion/down-weighting pass keyed on treatment-exposed cohorts or treatment-signature-high samples.
