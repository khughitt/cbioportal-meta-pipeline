---
type: interpretation
title: t207 H10 treatment impact full-config exposure-label pass
status: active
created: '2026-06-01'
updated: '2026-06-28'
id: interpretation:0030-t207-h10-treatment-impact-full-config
source_refs: &id001
- code/config/config-full.yml
- code/workflows/Snakefile
- code/scripts/annotate_treatment_exposure.py
- code/scripts/create_h10_treatment_freq_tables.py
- code/scripts/create_h10_treatment_impact_table.py
- doc/plans/2026-06-01-t207-h10-treatment-denominator-schema.md
- doc/interpretations/2026-06-01-t206-treatment-exposure-audit.md
- /data/packages/cbioportal/full/metadata/samples_treatment_exposure_counts.tsv
- /data/packages/cbioportal/full/summary/mut/table/gene_cancer_h10_treatment_impact.datapackage.json
- /data/packages/cbioportal/full/summary/mut/table/gene_cancer_h10_treatment_impact_ratio.feather
related:
- hypothesis:0009-treatment-induced-signature-frequency-contamination
- question:0024-treatment-exposed-cohort-chemotherapy-signature
- question:0027-does-excluding-treatment-signature-high-samples
- task:t207
input: *id001
prior_interpretations:
- interpretation:0029-t206-treatment-exposure-audit
- interpretation:0031-t207-h10-treatment-impact-target-blocked-by-missing-full-config-raw
relations:
- predicate: sci:supersedes
  target: interpretation:0031-t207-h10-treatment-impact-target-blocked-by-missing-full-config-raw
---

# Interpretation: t207 `H10` treatment impact full-config exposure-label pass

This is the `task:t207` full-config exposure-label pass.

## Verdict

**Verdict:** [?] Non-arbitrating for the biological `H10` impact claim, but successful as a full-config exposure-label plumbing and denominator-sensitivity pass.

The full `all_h10_treatment_impact` target now runs on `code/config/config-full.yml` and emits the planned impact feathers plus datapackage manifest.
The result should not be read as the `q027` therapy-signature-high answer, because this pass excludes samples by curated treatment-exposure labels rather than by measured SBS11/SBS31/SBS35/SBS87 exposure.

The strongest conclusion is methodological.
The `H10` treatment-denominator layer is executable on the full configured substrate, and the output shows where treatment labels can move gene-cancer means and ranks.
It does not yet adjudicate whether DNA-damaging therapy signatures materially contaminate the headline frequency deliverable, because the primary mutagenic-treatment contrast is still label-thin and mostly a single-study bladder contrast.

## Findings Summary

The completed command was:

```bash
uv run --frozen --project ~/d/cancer/data-sources/cbioportal snakemake -s code/workflows/Snakefile -j1 all_h10_treatment_impact --configfile code/config/config-full.yml
```

The target produced:

| Output | Status |
|---|---|
| `/data/packages/cbioportal/full/summary/mut/table/gene_cancer_h10_treatment_impact.feather` | produced |
| `/data/packages/cbioportal/full/summary/mut/table/gene_cancer_h10_treatment_impact_ratio.feather` | produced |
| `/data/packages/cbioportal/full/summary/mut/table/gene_cancer_h10_treatment_impact.datapackage.json` | produced |

The ratio table at `/data/packages/cbioportal/full/summary/mut/table/gene_cancer_h10_treatment_impact_ratio.feather` has 776,686 gene-cancer rows and 51 columns.
The impact table has the same row count and 32 columns.
The manifest records the two summary resources under the `H10` treatment-denominator diagnostic dataset.

The sample-treatment annotation sidecar at `/data/packages/cbioportal/full/metadata/samples_treatment_exposure_counts.tsv` covers 198 configured studies and 383,477 samples.
It labels 1,232 samples as broad treatment-exposed, 50 as primary mutagenic-treatment signal, 281 as mutagenic-treatment sensitivity-only, 831 as positive naive or pretreatment, 55,218 as treatment-metadata-unknown, and 326,746 as no-detected-treatment-signal.

In the same treatment-count sidecar at `/data/packages/cbioportal/full/metadata/samples_treatment_exposure_counts.tsv`, the primary mutagenic-treatment study-level label is still only `blca_dfarber_mskcc_2014` with 50 labeled samples.
The PDX sensitivity-only labels are `pptc_2019` with 261 samples and `sclc_cancercell_gardner_2017` with 20 samples.
The confirmed naive or pretreatment studies are `lung_nci_2022`, `lusc_cptac_2021`, and `mbl_dkfz_2017`.
The two previously missing raw studies, `aml_stjude_2024` and `msk_impact_50k_2026`, now build but remain treatment-metadata-unknown in the label layer.

## Power And Contrast Read

The output separates four contrast families.
This separation is essential because the broad and no-detected contrasts have real table coverage, while the primary mutagenic and confirmed-naive contrasts are much thinner.

| Contrast | Interpretable rows | No-contrast rows | Underpowered rows | Read |
|---|---:|---:|---:|---|
| `delta_no_detected_contrast` | 92,990 | 662,382 | 21,314 | broadest comparator read, but comparator means no detected signal rather than confirmed naive |
| `delta_confirmed_naive_contrast` | 0 | 770,242 | 6,444 | cleanest negative-control idea, but not interpretable because confirmed-naive support never reaches two contributing studies |
| `delta_broad` | 60,752 | 710,764 | 5,170 | cohort-composition sensitivity, not DNA-damaging-therapy-specific |
| `delta_mutagenic_primary` | 8,834 | 766,441 | 1,411 | primary label-based mutagenic contrast, but concentrated in bladder because only one whole-study primary label is present |

In the ratio impact output at `/data/packages/cbioportal/full/summary/mut/table/gene_cancer_h10_treatment_impact_ratio.feather`, absolute changes among interpretable rows are usually small but not uniformly zero.
For `delta_no_detected_contrast`, 26,040 rows have absolute delta at least 0.01, 6,240 at least 0.05, and 2,948 at least 0.10; the median absolute delta is 0.0043 and the 95th percentile is 0.0709.
For `delta_broad`, 13,073 rows have absolute delta at least 0.01, 2,017 at least 0.05, and 866 at least 0.10; the median absolute delta is 0.0035 and the 95th percentile is 0.0325.
For `delta_mutagenic_primary`, 2,427 rows have absolute delta at least 0.01, 663 at least 0.05, and 176 at least 0.10; the median absolute delta is 0.0041 and the 95th percentile is 0.0774.

The largest interpretable primary mutagenic deltas in `/data/packages/cbioportal/full/summary/mut/table/gene_cancer_h10_treatment_impact_ratio.feather` are all bladder-cancer rows.
This is expected from the current label schema rather than surprising biological localization, because `blca_dfarber_mskcc_2014` is the only primary mutagenic whole-study label.
The top rows include genes such as `INPP5F`, `FOXB1`, `CAMKMT`, `PCSK6`, `CUL2`, `LONP2`, `ULK2`, and `SCAI`, each with `delta_mutagenic_primary` near -0.16 after removing 50 labeled samples.
These rows show that the denominator can move materially in a specific cancer type, but they are not by themselves evidence that a therapy-signature-shaped mutational process is driving driver-ranking contamination.

## Evidence Quality

Evidence type: `empirical_data_evidence` for the local full-config cBioPortal/GENIE pipeline output, plus `benchmark_evidence` for workflow and manifest production.

The evidence is strong for these propositions:

- the t207 schema is runnable on the full configured substrate;
- treatment-exposure labels are joined into per-study frequency views without changing the canonical hypermutator-inclusive/exclusive output contract;
- the final impact table reports the planned contrast-specific means, deltas, ranks, power statuses, and count audit fields;
- the previous missing-raw-data blocker has been resolved.

The evidence is weak or non-arbitrating for the biological `H10` impact claim.
The primary DNA-damaging-therapy label set is too thin to treat the primary mutagenic contrast as a pan-cancer `H10` test.
The no-detected-treatment comparator is useful but is not a confirmed treatment-naive baseline.
The confirmed-naive contrast is conceptually clean but empirically underpowered in this table because the positively naive studies do not provide at least two contributing studies for any gene-cancer row.

## Data Quality And Pipeline Robustness

The run surfaced and fixed an important sample-identity assumption before the final target completed.
Several TMB, hypermutator, and `H10` treatment-frequency paths were assuming that `sample_id` was globally unique.
That assumption fails for recurring cBioPortal sample IDs across studies, especially in large MSK substrates.
The implementation now carries `study_id` through the TMB/hotspot/GMM/hypermutator path and joins `H10` treatment annotations on `(study_id, sample_id)` where available.

This is a workflow robustness finding, not an `H10` biological result.
It increases confidence that the final treatment-impact table is keyed to the intended per-study samples rather than cross-study sample-name collisions.

The full run also required Feather-safe coercion of mixed object clinical metadata columns and missing-`hgvsp_short` handling in hotspot detection.
Those are ingestion hardening changes discovered by exercising the full configured substrate.

## Proposition-Level Updates

The result supports a methodological proposition: treatment-denominator sensitivity can be computed reproducibly as a separate opt-in output surface for the full project config.

The result modestly supports the concern that treatment-related cohort labels can perturb gene-cancer frequency summaries in some settings.
The support is modest because the observed deltas mix label ascertainment, cancer-type composition, panel coverage, and treatment-class specificity.

The result leaves the main `H10` causal proposition unresolved.
It does not show that therapy-induced signatures inflate mutation frequencies through SBS11/SBS31/SBS35/SBS87 context-specific burden.
It also does not show that excluding therapy-signature-high samples changes the canonical pooled frequency table beyond noise.

The result disputes only a narrow operational concern from the superseded blocker note: the full-config WP4 target is no longer blocked by missing local raw studies.

## Evidence vs. Open Questions

`question:0024-treatment-exposed-cohort-chemotherapy-signature` advances from audit-only to executable exposure-label substrate.
The project now has a full-config treatment-label annotation, per-study treatment-aware frequency views, and cross-study impact summaries.
However, the `q024` answer remains partial because the current label layer has high unknown metadata and unmeasured false-negative recall.

`question:0027-does-excluding-treatment-signature-high-samples` remains active and unanswered.
The `q027` exclusion set should be derived from per-sample SBS11/SBS31/SBS35/SBS87 exposures, not from clinical treatment labels alone.
This t207 pass should be cited as the exposure-label arm or denominator-plumbing precursor to `q027`, not as the `q027` result.

## Hypothesis-Level Implications

`hypothesis:0009-treatment-induced-signature-frequency-contamination` remains proposed and unresolved.
The denominator machinery now exists, and the first full-config exposure-label output makes the hypothesis testable.
The current evidence does not justify promoting, rejecting, or retiring the hypothesis.

The most defensible reading is that `H10` has passed an infrastructure gate, not an empirical confirmation gate.
The project can now ask sharper `H10` questions with deterministic label sets, measured signature exposures, and contrast-specific power flags.

## Limitations & Residual Uncertainty

The primary mutagenic-treatment layer has only one whole-study label and no sample-level rules in this run.
The highest-priority mixed mutagenic cohorts from the t206 audit, including `difg_glass_2019` and `blca_cornell_2016`, are not yet represented as deterministic sample-level mutagenic labels in this first impact table.

In the t206 audit source `doc/interpretations/2026-06-01-t206-treatment-exposure-audit.md`, `no_detected_treatment_signal` is not the same as confirmed treatment-naive.
It includes samples from studies where the `task:t207` audit found no treatment signal, plus positive-naive samples, but audit recall over the 109 no-metadata-signal studies remains unmeasured.

The output summarizes frequency-table sensitivity to treatment labels.
It does not condition on measured therapy-signature exposure, trinucleotide-context compatibility, treatment timing, cancer-stage differences, or panel ascertainment beyond the existing per-study frequency machinery.

PDX cohorts remain sensitivity-only.
They should not be folded into the primary patient denominator without a separate handling rule for passaging-acquired variants and mouse-read artifacts.

## Updated Priorities

The next `H10` step should add deterministic sample-level mutagenic-treatment labels for the high-priority mixed cohorts already identified in the t206 audit.
The clearest candidates are `difg_glass_2019` for temozolomide exposure and `blca_cornell_2016` for post-chemotherapy/platinum-containing exposure.
Those rules should be tested against raw `SAMPLE_ID` joins and rerun through the same WP4 impact target.

In parallel or immediately after that, implement the `q027` signature-high arm using measured SBS11/SBS31/SBS35/SBS87 exposures.
That arm should produce a separate interpretation because it asks a different question from the exposure-label denominator pass.

The current tables should be retained as the full-config baseline for exposure-label denominator sensitivity.
They should not be promoted into canonical frequency-table outputs until the project decides whether `H10` treatment handling is a core deliverable or an opt-in diagnostic layer.
