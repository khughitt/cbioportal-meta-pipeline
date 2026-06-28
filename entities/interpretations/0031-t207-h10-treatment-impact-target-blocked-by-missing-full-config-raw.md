---
type: interpretation
title: t207 H10 treatment impact target blocked by missing full-config raw studies
status: superseded
created: '2026-06-01'
updated: '2026-06-28'
id: interpretation:0031-t207-h10-treatment-impact-target-blocked-by-missing-full-config-raw
source_refs: &id001
- code/config/config-full.yml
- code/workflows/Snakefile
- doc/plans/2026-06-01-t207-h10-treatment-denominator-schema.md
- doc/interpretations/2026-06-01-t206-treatment-exposure-audit.md
related:
- hypothesis:0009-treatment-induced-signature-frequency-contamination
- question:0024-treatment-exposed-cohort-chemotherapy-signature
- question:0027-does-excluding-treatment-signature-high-samples
- task:t207
input: *id001
prior_interpretations:
- interpretation:0029-t206-treatment-exposure-audit
relations: []
---
<!--
Conclusion chains:
- Use `relations:` with `predicate: "sci:amends"` when this interpretation revises,
  narrows, qualifies, or extends an older conclusion.
- Use `relations:` with `predicate: "sci:supersedes"` when this interpretation
  replaces an older conclusion as the current canonical reading.
- Keep `prior_interpretations` only as a narrative breadcrumb. The graph relation
  is the machine-readable source of truth.
-->

# Interpretation: t207 `H10` treatment impact target blocked by missing full-config raw studies

Superseded by `interpretation:0030-t207-h10-treatment-impact-full-config`.
The missing raw studies were restored, the full `all_h10_treatment_impact` target completed, and the current full-config interpretation is now recorded there.
This superseded blocker was part of `task:t207`.

## Verdict

**Verdict:** [?] Inconclusive - the full-config WP4 `H10` treatment-impact target did not reach the impact-table stage because two configured raw study directories are absent from the local substrate.

## Findings Summary

The attempted command was:

```bash
uv run --frozen --project ~/d/cancer/data-sources/cbioportal snakemake -s code/workflows/Snakefile -j1 all_h10_treatment_impact --configfile code/config/config-full.yml
```

Snakemake stopped in `rule convert_to_feather` before `H10` treatment annotation or WP4 aggregation.
The missing inputs were the canonical cBioPortal raw files for `aml_stjude_2024`:

```text
/data/raw/cbioportal/aml_stjude_2024/data_mutations.txt
/data/raw/cbioportal/aml_stjude_2024/data_clinical_sample.txt
/data/raw/cbioportal/aml_stjude_2024/data_clinical_patient.txt
```

A direct raw-substrate audit found 198 configured studies and 2 studies with missing required raw files.
`aml_stjude_2024` lacks `data_mutations.txt`, `data_clinical_sample.txt`, and `data_clinical_patient.txt`.
`msk_impact_50k_2026` lacks those three files plus `data_gene_panel_matrix.txt`, which is required because it is listed in `panel_bearing_studies`.

No `gene_cancer_h10_treatment_impact.feather`, `gene_cancer_h10_treatment_impact_ratio.feather`, or `gene_cancer_h10_treatment_impact.datapackage.json` was produced for the full configured substrate.
This is a methodological/blocking finding, not an empirical `H10` result.

The t206 audit had already identified these same two studies as missing local metadata.
The t207 run attempt shows that the missingness is not only an audit caveat; it is currently a build blocker for the full-config `H10` impact target.

## Evidence Quality

Evidence type: workflow execution evidence and local raw-substrate audit.
The finding is strong for substrate readiness because the failure is deterministic and occurs before any stochastic analysis step.

This result is not confirmatory evidence for or against `hypothesis:0009-treatment-induced-signature-frequency-contamination`.
It does not test treatment-exposed versus no-detected-treatment frequencies, does not test SBS11/SBS31/SBS35/SBS87-high samples, and does not evaluate rank shifts.

Two cBioPortal DataHub tarball checks for the absent study IDs returned S3 `403 Forbidden`.
That matches the workflow's own caution that cBioPortal re-requests can be blocked, so resolving the substrate probably requires a local/manual raw-data restoration path rather than assuming the downloader can repair the run.

## Data Quality Checks

Methodological finding: the configured full run expects 198 studies, but the local raw substrate currently satisfies the required file contract for only 196 of them.

The missing files are not downstream `H10` outputs and not optional QA sidecars.
They are upstream raw inputs required to build `metadata/samples_annotated.feather` and the per-study mutation feathers that the `H10` views consume.

Control uniqueness, row conservation, treatment-view denominator nesting, and impact-table dimensionality were not evaluated because the pipeline did not reach those stages.

## Proposition-Level Updates

The proposition that the t207 WP4 implementation is wired into Snakemake remains supported by the earlier synthetic/fixture verification, but that is software evidence only.
This run disputes the narrower operational proposition that `all_h10_treatment_impact` is currently runnable end-to-end on the local `config-full.yml` substrate.

The `H10` empirical propositions remain unresolved:

- whether broad treatment-exposed cohort composition changes the public mutation-frequency deliverable;
- whether primary mutagenic-treatment labels change SBS-sensitive gene-cancer rankings;
- whether no-detected-treatment comparators differ from all-sample ratios;
- whether therapy-signature-high sample exclusion, the `q027` arm, changes pooled frequencies or rankings.

No support or dispute edge should be added to the biological `H10` impact claim from this run.

## Hypothesis-Level Implications

`hypothesis:0009-treatment-induced-signature-frequency-contamination` remains proposed and empirically unresolved.
The executable schema exists, but the full-config substrate is not yet ready to arbitrate the hypothesis.

This interpretation should not be read as a null `H10` result.
It is a substrate-readiness failure before any treatment-aware frequency contrast was computed.

## Evidence vs. Open Questions

`question:0024-treatment-exposed-cohort-chemotherapy-signature` is partially affected.
The earlier t206 audit remains the current substantive answer for treatment-exposure labels, and this run confirms that the two missing-metadata studies must be resolved before full-config execution can proceed.

`question:0027-does-excluding-treatment-signature-high-samples` is unchanged.
The `q027` signature-high arm was not run and is still a distinct follow-up that should consume measured SBS11/SBS31/SBS35/SBS87 exposures rather than clinical treatment labels.

The t207 exposure-label arm was attempted but not completed on the full configured substrate.
No impact-table interpretation exists yet.

## New Questions Raised

Priority P1, methodological: how should the project restore or replace raw inputs for `aml_stjude_2024` and `msk_impact_50k_2026` so `config-full.yml` is runnable again?
The fastest evidence is a local file-presence check after manual restoration, followed by a Snakemake dry run and then the targeted WP4 run.

Priority P2, workflow robustness: should `download_study` or a preflight rule explicitly report missing raw studies before Snakemake reaches `convert_to_feather`?
The current failure is loud, but it occurs as a generic missing-input error rather than as a project-level substrate-readiness report.

Priority P2, scientific scope: if raw restoration is not immediately possible, should a deliberately named available-substrate sensitivity config exclude the two absent studies?
That would be useful for plumbing, but it should not be represented as the full-config `H10` impact answer.

## Limitations & Residual Uncertainty

The run did not reach `H10` annotation, per-study treatment views, cross-study aggregation, or manifest generation.
Therefore it cannot evaluate denominator dilution, no-detected-treatment contrasts, confirmed-naive sensitivity, broad-treatment sensitivity, PDX sensitivity, rank shifts, or contrast-specific power statuses.

The missing-study audit checked required raw file presence, not whether all present studies have semantically complete treatment metadata.
The t206 recall caveat still stands: `no_detected_treatment_signal` is not a confirmed treatment-naive baseline.

## Updated Priorities

The immediate next step is substrate repair, not `H10` interpretation.
Restore or otherwise resolve the raw inputs for `aml_stjude_2024` and `msk_impact_50k_2026`, then rerun:

```bash
uv run --frozen --project ~/d/cancer/data-sources/cbioportal snakemake -s code/workflows/Snakefile -j1 all_h10_treatment_impact --configfile code/config/config-full.yml
```

After the target produces `gene_cancer_h10_treatment_impact_ratio.feather` and its datapackage, write the substantive t207 impact note.
That later note should keep the exposure-label arm separate from `q027`, report primary mutagenic exclusion separately from broad-treatment sensitivity, and treat no-contrast or underpowered rows as plumbing signals unless deterministic sample-level mutagenic-treatment rules have been added.
