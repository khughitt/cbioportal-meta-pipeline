---
id: plan:2026-06-01-t210-q027-therapy-signature-high-exclusion
type: plan
title: t210 q027 therapy-signature-high exclusion impact arm
status: proposed
created: "2026-06-01"
updated: "2026-06-01"
related:
  - hypothesis:h10-treatment-induced-signature-frequency-contamination
  - question:q027-does-excluding-treatment-signature-high-samples
  - question:q024-treatment-exposed-cohort-chemotherapy-signature
  - task:t207
  - task:t208
  - task:t209
  - task:t210
---

# t210 q027 therapy-signature-high exclusion impact arm

## Goal

Implement the q027 arm of H10 as a measured-signature exclusion test:
flag samples with high measured SBS11/SBS31/SBS35/SBS87 exposure, rerun gene-cancer frequency summaries with those samples excluded, and report how pooled frequencies and ranks change.

This is deliberately separate from the t207-t209 exposure-label arm.
Clinical treatment labels answer "known or suspected treatment exposure."
q027 asks whether samples carrying therapy-associated mutational signatures measurably affect the frequency deliverable.

## Background

t207-t209 built the H10 denominator machinery and repaired the known clinical-label comparator leak.
That substrate now produces exposure-label cohort views, impact tables, and a datapackage on `code/config/config-full.yml`.

The q027 input is different.
The current H10 full-config output has no SBS signature exposure table, and the existing H08 signature run is MC3-only and does not include SBS11/SBS31/SBS35/SBS87 in its assigned signature set.
The q027 plan therefore starts by creating a therapy-signature exposure substrate rather than reusing t207 labels as if they were signature outcomes.

## Scope

Primary scope is a **probe-sized q027 implementation** over studies with plausible therapy-signature signal and enough mutation counts to make per-sample assignment meaningful.
The initial candidate set should include the H10 clinical-label positives from t206-t209:

| Study | Rationale | Expected therapy signature |
|---|---|---|
| `difg_glass_2019` | TMZ field with 179 Yes / 104 No / 161 blank | SBS11 |
| `blca_cornell_2016` | 51 post-chemotherapy and 21 pre-chemotherapy samples | SBS31/SBS35 plausible |
| `blca_dfarber_mskcc_2014` | cisplatin-treated bladder cohort | SBS31/SBS35 plausible |
| `sclc_cancercell_gardner_2017` | treatment-derived PDX caveat | sensitivity-only, not primary patient denominator |
| `pptc_2019` | PDX caveat | sensitivity-only, not primary patient denominator |

Add other studies only if an explicit feasibility audit shows enough SBS-count-passing samples and a therapy-signature expectation from the t206 audit or raw metadata.
Do not run a full 198-study signature assignment as the first pass.

## Inputs

- `code/config/config-full.yml` for study IDs, raw data directory, and H10 clinical treatment labels.
- Per-study mutation and sample tables under `/data/packages/cbioportal/full/studies/{study}/`.
- Raw cBioPortal clinical sample files under `/data/raw/cbioportal/{study}/data_clinical_sample.txt`.
- `data/cosmic_cancer_type_signatures.tsv` for the baseline cancer-type restricted signature lookup.
- Existing signature assignment code: `code/scripts/run_restricted_sigprofiler_assignment.py`.
- Existing H10 impact code: `code/scripts/create_h10_treatment_freq_tables.py` and `code/scripts/create_h10_treatment_impact_table.py`.

## Approach

### WP1: Feasibility audit

Create `code/scripts/audit_q027_therapy_signature_substrate.py`.
For each candidate study, compute:

- total samples;
- per-sample SBS mutation counts after the same mutation-context filter used by the signature assignment script;
- number and fraction passing the configured count floor;
- clinical-label strata from `samples_treatment_exposure.feather`;
- whether the target therapy signatures are available in the requested COSMIC catalog;
- whether the candidate study has enough samples for a contrast.

The audit output should be a TSV and short markdown note under `results/q027-therapy-signature-high-2026-06-01/`.
If no candidate study has adequate count-floor-passing samples, stop and write a non-arbitrating interpretation rather than forcing an impact table.

Decision rule for continuing to WP2:
at least one primary patient study must have `>=25` count-floor-passing samples in a plausible therapy-signature target family and at least one retained comparator stratum.

### WP2: Therapy-signature assignment substrate

Add a q027-specific config, for example `code/config/config-q027-therapy-signature-high.yml`, with:

- `studies`: the WP1-passing candidate studies;
- `signature_assignment_lookup_keys`: the corresponding cancer-family keys;
- `signature_assignment_extra_signatures`: `SBS11`, `SBS31`, `SBS35`, and `SBS87`;
- the existing t178/t179 provenance and count-floor settings;
- an explicit `q027_therapy_signature_targets` block mapping study/cancer-family to target signatures.

Modify `run_restricted_sigprofiler_assignment.py` only if needed to support `signature_assignment_extra_signatures`.
The extra signatures must be appended to the cancer-family restricted set before assignment and recorded in the signature audit sidecar.
There must be no silent fallback if a requested therapy signature is absent from the installed COSMIC reference.

### WP3: Signature-high labels

Create `code/scripts/annotate_q027_signature_high.py`.
Input is one or more `restricted_assignment_per_sample.feather` files.
Output is `metadata/samples_q027_signature_high.feather` with at least:

- `study_id`;
- `sample_id`;
- `cancer_type`;
- `passes_count_floor`;
- `therapy_signature_exposure`;
- `therapy_signature_fraction`;
- per-signature exposure and fraction columns for `SBS11`, `SBS31`, `SBS35`, `SBS87`;
- `therapy_signature_high`;
- `therapy_signature_label_reason`.

Primary high rule:
`therapy_signature_high = passes_count_floor AND therapy_signature_exposure >= 50 SBS`.

Sensitivity rules:

- exposure >= 20 SBS;
- therapy-signature fraction >= 0.10 among assigned SBS;
- any non-zero target signature exposure.

The primary rule prioritizes absolute treatment-mutagenesis burden rather than small fractional fits in low-count samples.
Rows failing the count floor are not called negative; they must be labeled unevaluable.

### WP4: Frequency and impact outputs

Implement q027 frequency views parallel to H10 treatment views, without overloading the t207 label names.
Preferred outputs:

- `studies/{id}/mut/table/gene_cancer_q027_signature_high_views.feather`;
- `summary/mut/table/gene_cancer_q027_signature_high_impact.feather`;
- `summary/mut/table/gene_cancer_q027_signature_high_impact_ratio.feather`;
- `summary/mut/table/gene_cancer_q027_signature_high_impact.datapackage.json`.

Required cohort views:

- `all_samples`;
- `signature_evaluable`;
- `therapy_signature_high`;
- `therapy_signature_high_excluded_primary`;
- `therapy_signature_high_excluded_sensitivity_20`;
- `therapy_signature_high_excluded_sensitivity_fraction_10`.

Required deltas:

- `delta_signature_high_excluded_primary = mean_all_samples - mean_therapy_signature_high_excluded_primary`;
- sensitivity deltas for the 20-SBS and 10%-fraction rules;
- ranks and rank deltas within cancer type;
- count audit fields showing removed samples and removed mutated samples.

Power statuses should follow t207 precedence:
`no_contrast` wins when zero signature-high samples are removed; otherwise `<2 contributing studies` is `underpowered_non_arbitrating`.

### WP5: Interpretation

Write `doc/interpretations/2026-06-01-t210-q027-therapy-signature-high-exclusion.md`.
The note must state whether q027 is:

- interpretable for at least one cancer type;
- non-arbitrating because no samples are therapy-signature-high;
- non-arbitrating because signature assignment is underpowered or count-floor limited.

The note should compare, but not conflate, the q027 signature-high labels with t207-t209 clinical treatment labels.

## Key Decisions

### Use measured signatures, not treatment labels

Chosen: define the q027 exclusion set from SBS11/SBS31/SBS35/SBS87 exposure.
Rejected: reuse `mutagenic_treatment_signal` from t207-t209.
Reason: q027 specifically asks whether signature-high samples alter frequency tables; treatment labels and signature-high samples are different sets.

### Probe first, not full-config signature assignment

Chosen: run a scoped candidate-study feasibility pass before any full-config q027 workflow.
Rejected: run per-sample SigProfiler assignment across all 198 configured studies immediately.
Reason: panel samples often have low SBS counts, and the existing full-config H10 run has no signature substrate; a broad run could consume substantial time while producing mostly unevaluable samples.

### Absolute exposure threshold as primary

Chosen: primary high rule is at least 50 SBS assigned to the target therapy signatures, with count-floor passing required.
Rejected: use any non-zero exposure as primary.
Reason: tiny non-zero refit weights can reflect assignment bleed, especially in low-count samples; the primary rule should privilege materially burdened samples.

### Keep q027 outputs separate from H10 treatment views

Chosen: write `q027_signature_high_*` files and cohort views.
Rejected: add more columns to `gene_cancer_h10_treatment_impact_ratio.feather`.
Reason: t207-t209 is an exposure-label denominator layer; q027 is an outcome-signature layer and needs independent provenance.

## Validation

Tests:

- config parsing accepts `signature_assignment_extra_signatures`;
- signature audit sidecar records all requested therapy signatures and hard-fails absent requested signatures unless explicitly marked unavailable;
- `annotate_q027_signature_high.py` labels high, low, and unevaluable samples correctly on synthetic exposures;
- frequency views reproduce canonical `all_samples` counts and remove exactly the `therapy_signature_high` samples in primary and sensitivity views;
- impact table reports `no_contrast` before `underpowered_non_arbitrating`;
- datapackage is produced for the q027 impact outputs.

Workflow checks:

```bash
uv run --frozen pytest code/scripts/tests/test_annotate_q027_signature_high.py
uv run --frozen pytest code/scripts/tests/test_create_q027_signature_high_freq_tables.py
uv run --frozen pytest code/scripts/tests/test_create_q027_signature_high_impact_table.py
uv run --frozen ruff check code/scripts/ code/workflows/Snakefile
uv run --frozen ruff format --check code/scripts/
uv run --frozen snakemake -s code/workflows/Snakefile -j8 all_q027_signature_high_impact --configfile code/config/config-q027-therapy-signature-high.yml
uv run --frozen science validate --verbose
```

## Out Of Scope

- Treating clinical treatment labels as signature-high labels.
- De-novo extraction of a new therapy signature.
- Driver causality claims from a frequency-table delta alone.
- PDX primary-denominator interpretation.
- Full 198-study per-sample signature assignment before the candidate-study feasibility gate.

## Acceptance Criteria

- `task:t210` has a q027-specific config, scripts, tests, Snakemake target, outputs, datapackage, and interpretation.
- The q027 interpretation explicitly separates measured signature-high exclusion from t207-t209 clinical-label exclusion.
- If the run is non-arbitrating, the reason is named as no signal, low count-floor support, no comparator, or underpowered cross-study support.
- H10 remains proposed unless q027 produces an interpretable effect that materially changes frequency/rank outputs and survives the pre-specified sensitivity checks.
