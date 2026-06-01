---
id: "plan:2026-06-01-t207-h10-treatment-denominator-schema"
type: "plan"
title: "H10 treatment-denominator schema and impact pass"
status: "active"
created: "2026-06-01"
updated: "2026-06-01"
related:
  - "hypothesis:h10-treatment-induced-signature-frequency-contamination"
  - "question:q024-treatment-exposed-cohort-chemotherapy-signature"
  - "question:q027-does-excluding-treatment-signature-high-samples"
  - "task:t181"
  - "task:t206"
  - "task:t207"
---

# H10 treatment-denominator schema and impact pass

## Purpose

Implement the H10 denominator layer without collapsing broad treatment history into the narrower DNA-damaging-therapy prediction.
The output should answer two different questions separately:

- does any broad treatment-exposed cohort composition change the public mutation-frequency deliverable?
- do cohorts with an a priori mutagenic-treatment expectation change SBS11/SBS31/SBS35/SBS87-sensitive gene-cancer rankings?

This is a design plan for `task:t207`.
It follows the t206 audit scaffold and manual-review note, and it should not reinterpret the t206 audit as an H10 result.
The upstream analysis-readiness artifact is `doc/plans/2026-06-01-t206-h10-treatment-exposure-audit-analysis-plan.md`.

## Scope Decomposition

`task:t206` owns the audit and manual review.
It produced `doc/interpretations/2026-06-01-t206-treatment-exposure-audit.md`, which confirmed broad treatment-exposed candidates, separated mutagenic-treatment candidates from broad exposure, and flagged PDX cohorts as sensitivity-only.

`task:t207` owns the executable schema and impact pass.
It should encode the curated labels, annotate samples or studies deterministically, recompute treatment-aware denominator views, and write an impact note.

The existing hypermutator-inclusive/exclusive contract remains unchanged.
In current frequency tables, `_exclusive` means hypermutator-excluded.
Treatment-aware outputs should use explicit H10 names rather than reusing `_exclusive` alone.

## Architecture

```text
code/config/config-full.yml                                      MODIFY
  add h10_treatment_denominator schema under a named top-level key

code/scripts/annotate_treatment_exposure.py                      NEW
  config + per-study sample metadata -> metadata/samples_treatment_exposure.feather

code/scripts/create_h10_treatment_freq_tables.py                 NEW
  mutations + samples + treatment annotations + panel coverage -> long per-study cohort-view table

code/scripts/create_h10_treatment_impact_table.py                NEW
  per-study cohort-view tables -> gene-cancer H10 impact summary

code/workflows/Snakefile                                         MODIFY
  add opt-in H10 treatment-denominator rules and all_h10_treatment_impact target

code/scripts/tests/test_annotate_treatment_exposure.py            NEW
code/scripts/tests/test_create_h10_treatment_freq_tables.py       NEW
code/scripts/tests/test_create_h10_treatment_impact_table.py      NEW
  synthetic checks for schema, sample labels, denominator conservation, and rank shifts

doc/interpretations/YYYY-MM-DD-t207-h10-treatment-impact.md       NEW
  result interpretation; not part of this design plan
```

Proposed output surface:

```text
metadata/samples_treatment_exposure.feather
studies/{id}/mut/table/gene_cancer_h10_treatment_views.feather
summary/mut/table/gene_cancer_h10_treatment_impact.feather
summary/mut/table/gene_cancer_h10_treatment_impact_ratio.feather
```

The long per-study table should carry `cohort_view` rather than adding multiple ambiguous suffixes.
Required cohort views:

| Cohort view | Meaning |
|---|---|
| `all_samples` | all callable samples; the treatment-inclusive baseline |
| `no_detected_treatment_signal` | excludes primary mutagenic-treatment labels; comparator is not confirmed naive |
| `broad_treatment_excluded` | excludes broad confirmed treatment-exposed cohorts; cohort-composition sensitivity |
| `mutagenic_treatment_excluded_primary` | excludes primary DNA-damaging-therapy labels; primary H10 treatment denominator |
| `mutagenic_treatment_excluded_with_pdx_sensitivity` | additionally excludes PDX sensitivity-only labels; sensitivity only |

## Key Decisions

### Key decision: layered labels instead of a flat treatment list

Chosen approach: encode broad treatment exposure, mutagenic-treatment expectation, sample-level rules, positive naive/pre-treatment evidence, missing metadata, and PDX sensitivity as separate config fields.
Rejected alternative: a single `treatment_exposed_studies` list used for the primary H10 test.
Reason: the t206 manual review showed that ICB, endocrine, targeted, and castration-resistant cohorts are broad treatment-history signals but not direct SBS11/SBS31/SBS35/SBS87 expectations.

### Key decision: sample-level labels when evidence is sample-level

Chosen approach: derive sample-level treatment annotations for mixed cohorts when the raw clinical column identifies treated versus untreated samples.
Rejected alternative: storing only study-level fractions and applying fractional denominators.
Reason: fractional denominators cannot identify which mutated samples should be excluded, so they can distort numerator and denominator in different directions.

Initial sample-level rule targets:

| Study | Source column evidence | Primary handling |
|---|---|---|
| `blca_cornell_2016` | `SPECIMEN_COLLECTION_PRE_OR_POST_CHEMO`: 51 / 72 post-chemotherapy | sample-level mutagenic-treatment candidate |
| `difg_glass_2019` | `TMZ_TREATMENT`: 179 Yes / 104 No / 161 blank; `CONCURRENT_TMZ`: 108 Yes / 25 No / 311 blank | sample-level mutagenic-treatment candidate with missingness report |
| `brain_cptac_2020` | `TREATMENT_STATUS`: 36 post-treatment / 182 treatment naive | sensitivity until pediatric brain subtype and timing semantics are reviewed |
| `pptc_2019` | `TX_CISPLATIN` nonblank in PDX samples | PDX sensitivity-only, excluded from primary patient denominator |

Fraction-only or semantics-heavy cohorts should remain reported but not primary-excluded until a deterministic sample rule is written.
This includes `coadread_mskcc`, `coadread_cass_2020`, `brca_mbcproject_wagle_2017`, `mpcproject_broad_2021`, and OHSU AML.

### Key decision: PDX cohorts are sensitivity-only

Chosen approach: exclude PDX cohorts from the primary patient denominator and include them only in a named sensitivity view.
Rejected alternative: treating PDX treatment fields as ordinary patient sample labels.
Reason: passaging-acquired mutation calls and mouse-read artifacts can alter the mutation table independently of patient treatment history.

### Key decision: no-detected-signal baseline, not confirmed naive

Chosen approach: name the default comparator `no_detected_treatment_signal` and separately report positive naive/pre-treatment studies.
Rejected alternative: calling all unflagged studies treatment-naive.
Reason: the audit recall is unmeasured for the 109 no-metadata-signal studies, and only `lung_nci_2022`, `lusc_cptac_2021`, and `mbl_dkfz_2017` are positively clean.

### Key decision: opt-in H10 impact tables first

Chosen approach: build an opt-in H10 impact target that writes separate H10 treatment tables.
Rejected alternative: immediately extending canonical `gene_cancer_study_ratio_annotated.feather`.
Reason: the canonical table already uses inclusive/exclusive terminology for hypermutator handling; adding treatment exclusion there before the semantics are tested would invite consumer confusion.

## Work Packages

### WP1: Config schema and validation

Depends on: t206 manual-review note.
Entry point: `code/config/config-full.yml`.

Add a top-level `h10_treatment_denominator` block:

```yaml
h10_treatment_denominator:
  broad_treatment_exposed_studies:
    - blca_dfarber_mskcc_2014
    - brca_dfci_2020
    - brca_fuscc_2020
    - brca_mskcc_2019
    - mel_ucla_2016
    - mixed_allen_2018
    - nepc_wcm_2016
    - nsclc_mskcc_2018
    - prad_su2c_2019
    - skcm_mskcc_2014
  mutagenic_treatment_signal_studies:
    - blca_dfarber_mskcc_2014
  mutagenic_treatment_signal_sensitivity_only_studies:
    - sclc_cancercell_gardner_2017
    - pptc_2019
  positive_naive_or_pretreatment_studies:
    - lung_nci_2022
    - lusc_cptac_2021
    - mbl_dkfz_2017
  unknown_treatment_metadata_studies:
    - aml_stjude_2024
    - msk_impact_50k_2026
  sample_level_rules: {}
```

`sample_level_rules` should be filled with exact clinical-column rules during implementation after re-reading the raw labels.
The empty map is intentional at schema introduction time; it prevents implicit fractional exclusion before sample IDs are available.

Definition of done:

- config parser hard-fails if a study appears in both primary mutagenic and positive-naive fields;
- config parser hard-fails if a sensitivity-only PDX study is also in the primary mutagenic field;
- unknown metadata studies are reported, never silently treated as unexposed;
- tests cover empty config, conflicting labels, and the provisional t206 label set.

### WP2: Treatment exposure sample annotation

Depends on: WP1.
Entry point: `code/scripts/annotate_treatment_exposure.py`.

Produce `metadata/samples_treatment_exposure.feather` from per-study `samples.feather`, config labels, and optional raw clinical sample files.
Required columns:

| Column | Type | Meaning |
|---|---|---|
| `sample_id` | string | sample ID as used downstream |
| `study_id` | string | source study |
| `treatment_exposed_broad` | bool | broad treatment-history cohort label |
| `mutagenic_treatment_signal` | bool | primary H10 DNA-damaging-treatment label |
| `mutagenic_treatment_signal_sensitivity_only` | bool | PDX or other sensitivity-only mutagenic label |
| `positive_naive_or_pretreatment` | bool | positively classified clean baseline |
| `treatment_metadata_unknown` | bool | study metadata unavailable or unresolved |
| `treatment_label_source` | string | study-level, sample-level, sensitivity-only, positive-naive, unknown, or no-detected-signal |
| `treatment_rule_id` | string | config rule or study-level label that assigned the row |

Definition of done:

- every sample in configured studies appears once;
- study-level labels are applied to all samples from that study;
- sample-level rules override broad study-level absence but not PDX sensitivity-only status;
- label counts by study are written to a small TSV sidecar;
- missing clinical columns named by a rule hard-fail.

### WP3: Treatment-aware per-study frequency views

Depends on: WP2.
Entry point: `code/scripts/create_h10_treatment_freq_tables.py`.

Compute per-study `(cancer_type, symbol, cohort_view)` rows using the same panel-aware denominator rules as `create_freq_tables.py`.
Do not mutate the existing hypermutator columns.
The treatment-aware script may reuse helper functions from `create_freq_tables.py` if the extraction is small and test-covered.

Required numeric columns:

```text
num
n_samples
ratio
n_samples_hypermutator_excluded
num_hypermutator_excluded
ratio_hypermutator_excluded
```

The hypermutator-excluded companion columns are required because H10 needs to know whether treatment effects persist after the existing hypermutator layer.
They should be explicitly named and should not replace the existing canonical `ratio_exclusive`.

Definition of done:

- panel-aware callable denominators match `create_freq_tables.py` for `all_samples` on synthetic inputs;
- excluding treatment-positive samples removes those sample IDs from both numerator and denominator;
- zero-denominator rows emit `NaN` ratios, not zero;
- PDX sensitivity-only samples are excluded only in the PDX sensitivity view.

### WP4: Cross-study H10 impact aggregation

Depends on: WP3.
Entry point: `code/scripts/create_h10_treatment_impact_table.py`.

Aggregate the per-study treatment views into `summary/mut/table/gene_cancer_h10_treatment_impact_ratio.feather`.
The table should report per-row changes rather than overwrite canonical means.

Required summary fields:

| Field | Meaning |
|---|---|
| `mean_all_samples` | mean ratio across studies in `all_samples` view |
| `mean_no_detected_treatment_signal` | mean ratio after primary mutagenic-treatment exclusion |
| `mean_broad_treatment_excluded` | broad treatment-history sensitivity mean |
| `mean_mutagenic_treatment_excluded_primary` | primary H10 treatment-excluded mean |
| `mean_mutagenic_treatment_excluded_with_pdx_sensitivity` | PDX sensitivity mean |
| `delta_mutagenic_primary` | `mean_all_samples - mean_mutagenic_treatment_excluded_primary` |
| `rank_all_samples` | within-cancer rank by `mean_all_samples` |
| `rank_mutagenic_primary` | within-cancer rank after primary exclusion |
| `rank_delta_mutagenic_primary` | `rank_all_samples - rank_mutagenic_primary` |
| `h10_power_status` | `interpretable`, `underpowered_non_arbitrating`, or `no_contrast` |

Definition of done:

- rank shifts are computed within cancer type;
- rows with fewer than two contributing non-excluded studies are `underpowered_non_arbitrating`;
- rows with zero excluded samples are `no_contrast`;
- output includes enough counts to audit whether a change is numerator-driven or denominator-driven.

### WP5: Snakemake integration and interpretation

Depends on: WP1-WP4.
Entry point: `code/workflows/Snakefile`.

Add an opt-in target:

```text
all_h10_treatment_impact
```

The target should build the annotation, per-study treatment views, aggregate impact tables, and a QA report.
It should stay outside the default all-target until the interpretation note decides whether the output is ready for canonical annotation.

Definition of done:

- dry-run resolves under `code/config/config-full.yml`;
- targeted unit tests pass;
- `doc/interpretations/YYYY-MM-DD-t207-h10-treatment-impact.md` reports primary mutagenic exclusion separately from broad-treatment sensitivity;
- the interpretation states that `no_detected_treatment_signal` is not confirmed treatment-naive.

## QA Checkpoints

Input assertions:

- all study IDs in the H10 config block exist in `studies`;
- all configured sample-level rule columns exist in the raw clinical sample file;
- every output sample has exactly one `study_id` and one `sample_id`;
- no primary label is assigned by a mutational-signature outcome.

Inter-stage invariants:

- `all_samples` view reproduces existing `create_freq_tables.py` counts on synthetic and small real fixtures;
- for every `(study, cancer_type, symbol)`, each treatment-excluded denominator is less than or equal to `all_samples`;
- numerator counts are less than or equal to denominators for every cohort view;
- PDX sensitivity-only exclusions do not affect the primary view.

Sanity checks:

- `blca_dfarber_mskcc_2014` is primary mutagenic-treatment at study level;
- `sclc_cancercell_gardner_2017` and `pptc_2019` are sensitivity-only;
- `lung_nci_2022`, `lusc_cptac_2021`, and `mbl_dkfz_2017` are positive naive/pre-treatment;
- missing metadata studies are surfaced in the annotation summary.

Failure mode:

- structural schema, missing-column, and impossible-label conflicts hard-fail;
- distribution warnings such as high missingness in `TMZ_TREATMENT` are reported in the QA sidecar and interpretation, not silently ignored.

## Open Questions

- Whether `brain_cptac_2020` should enter the primary sample-level rule set or remain sensitivity-only after subtype and timing review.
- Whether AML relapse/treatment fields should be modeled in the same H10 pass or deferred to a hematologic-specific treatment semantics pass.
- Whether the first impact note should promote any H10 output into canonical annotated frequency tables or keep it as an opt-in diagnostic artifact.

## Non-Goals

- Estimating the causal effect of treatment on mutation frequency.
- Defining treatment exposure from SBS11/SBS31/SBS35/SBS87 outcomes.
- Reclassifying all 109 no-metadata-signal studies as confirmed treatment-naive.
- Changing the existing hypermutator-inclusive/exclusive output contract.
- Making PDX mutation calls part of the primary patient denominator.

## Acceptance Criteria

- The H10 config schema encodes broad treatment, mutagenic-treatment, PDX sensitivity-only, positive-naive, and unknown-metadata labels separately.
- Sample-level mixed-cohort labels are applied only when a deterministic clinical rule maps to sample IDs.
- Treatment-aware per-study frequency views preserve panel-aware callable denominators.
- The cross-study impact table reports primary mutagenic exclusion, broad treatment sensitivity, PDX sensitivity, rank shifts, and power status.
- The final interpretation does not call `no_detected_treatment_signal` a confirmed naive baseline.
- Verification includes targeted pytest, ruff, Snakemake dry-run for `all_h10_treatment_impact`, and `uv run --frozen science validate --verbose`.
