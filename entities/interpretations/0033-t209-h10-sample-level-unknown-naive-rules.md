---
type: interpretation
title: t209 H10 sample-level unknown and confirmed-naive rule impact
status: active
created: '2026-06-01'
updated: '2026-06-01'
id: interpretation:0033-t209-h10-sample-level-unknown-naive-rules
source_refs: &id001
- code/config/config-full.yml
- code/scripts/annotate_treatment_exposure.py
- code/scripts/create_h10_treatment_freq_tables.py
- code/scripts/create_h10_treatment_impact_table.py
- doc/interpretations/2026-06-01-t206-treatment-exposure-audit.md
- doc/interpretations/2026-06-01-t207-h10-treatment-impact-full-config.md
- doc/interpretations/2026-06-01-t208-h10-sample-level-mutagenic-rules.md
- /data/packages/cbioportal/full/metadata/samples_treatment_exposure_counts.tsv
- /data/packages/cbioportal/full/summary/mut/table/gene_cancer_h10_treatment_impact.datapackage.json
- /data/packages/cbioportal/full/summary/mut/table/gene_cancer_h10_treatment_impact_ratio.feather
related:
- hypothesis:0009-treatment-induced-signature-frequency-contamination
- question:0024-treatment-exposed-cohort-chemotherapy-signature
- question:0027-does-excluding-treatment-signature-high-samples
- task:t206
- task:t207
- task:t208
- task:t209
input: *id001
prior_interpretations:
- interpretation:0029-t206-treatment-exposure-audit
- interpretation:0030-t207-h10-treatment-impact-full-config
- interpretation:0032-t208-h10-sample-level-mutagenic-rules
---

# Interpretation: t209 H10 sample-level unknown and confirmed-naive rule impact

## Verdict

**Verdict:** [?] Comparator semantics repaired for the exposure-label arm; H10 remains non-arbitrating and q027 remains unanswered.

The t209 follow-up extends `h10_treatment_denominator.sample_level_rules` so sample-level rules can now target `treatment_metadata_unknown` and `positive_naive_or_pretreatment`, not only positive treatment labels.
The full `all_h10_treatment_impact` target reruns on `code/config/config-full.yml` with the repaired label vocabulary and produces an up-to-date impact table plus datapackage.

The important change is semantic rather than broad power improvement.
The 161 DIFG/GLASS samples with blank `TMZ_TREATMENT` now leave `no_detected_treatment_signal` and enter `treatment_metadata_unknown`.
The 21 BLCA Cornell `pre-chemotherapy` samples now enter `positive_naive_or_pretreatment` while remaining in the retained no-detected comparator.
This closes the silent-negative behavior identified after t208.

The result still does not adjudicate H10.
The exposure-label denominator pass is now cleaner, but q027 requires a separate measured SBS11/SBS31/SBS35/SBS87 signature-high exclusion arm.

## What Changed

The implementation adds two real-data sample-level rules.

| Rule | Study | Clinical column | Positive value | Target | Labeled samples |
|---|---|---|---|---|---:|
| `difg_glass_2019_tmz_unknown` | `difg_glass_2019` | `TMZ_TREATMENT` | blank | `treatment_metadata_unknown` | 161 |
| `blca_cornell_2016_pre_chemo` | `blca_cornell_2016` | `SPECIMEN_COLLECTION_PRE_OR_POST_CHEMO` | `pre-chemotherapy` | `positive_naive_or_pretreatment` | 21 |

The existing sample-level positive-treatment rules remain unchanged.

| Rule | Study | Clinical column | Positive value | Target | Labeled samples |
|---|---|---|---|---|---:|
| `difg_glass_2019_tmz` | `difg_glass_2019` | `TMZ_TREATMENT` | `Yes` | `mutagenic_treatment_signal` | 179 |
| `blca_cornell_2016_post_chemo` | `blca_cornell_2016` | `SPECIMEN_COLLECTION_PRE_OR_POST_CHEMO` | `post-chemotherapy` | `mutagenic_treatment_signal` | 51 |

The regenerated sidecar covers 383,477 samples.

| Label | Count |
|---|---:|
| `treatment_exposed_broad` | 1,462 |
| `mutagenic_treatment_signal` | 280 |
| `mutagenic_treatment_signal_sensitivity_only` | 281 |
| `positive_naive_or_pretreatment` | 852 |
| `treatment_metadata_unknown` | 55,379 |
| `no_detected_treatment_signal` | 326,355 |

For the two mixed cohorts, the repaired labels now read as intended.

| Study | Samples | Primary mutagenic | Confirmed pretreatment | Unknown metadata | No-detected comparator |
|---|---:|---:|---:|---:|---:|
| `blca_cornell_2016` | 72 | 51 | 21 | 0 | 21 |
| `difg_glass_2019` | 444 | 179 | 0 | 161 | 104 |

The DIFG/GLASS comparator is therefore no longer contaminated by blank TMZ metadata.
For that study, `no_detected_treatment_signal` now means explicit `TMZ_TREATMENT == "No"` under the available TMZ field, not "blank or not Yes."
This does not prove absence of radiation or other treatment exposure; it only fixes the TMZ-specific silent fallback.

This remedy is per-cohort, not structural.
The silent-negative pattern is closed only for the two studies that now carry explicit sample-level unknown/naive rules.
Any future mixed cohort with partial sample-level treatment metadata will again route blank values into `no_detected_treatment_signal` unless a matching unknown rule is hand-authored.
The fix is therefore a manual per-cohort remedy reusing the t209 schema, not a structural guarantee against silent negatives.

## Impact Read

The refreshed ratio impact table still has 776,686 rows and 51 columns.
Power status is essentially unchanged for the primary mutagenic label contrast and improves semantically for the retained comparator.

| Contrast | Interpretable rows | No-contrast rows | Underpowered rows | Read |
|---|---:|---:|---:|---|
| `delta_no_detected_contrast` | 106,185 | 646,046 | 24,455 | comparator no longer treats blank DIFG TMZ as no-detected |
| `delta_broad` | 80,394 | 687,981 | 8,311 | broad cohort-composition sensitivity unchanged in scope |
| `delta_mutagenic_primary` | 29,377 | 742,757 | 4,552 | still bladder plus glioma exposure-label contrast |
| `delta_confirmed_naive_contrast` | 0 | 762,633 | 14,053 | now has BLCA sample-level support but remains underpowered |

The `delta_no_detected_contrast` power-status counts (106,185 / 646,046 / 24,455) are identical to t208, but the underlying glioma frequencies did shift.
The glioma `no_detected` denominator dropped from 265 to 104 samples once the 161 blank-TMZ samples moved to `treatment_metadata_unknown`, so glioma no-detected ratios changed; no gene-cancer row's power classification flipped.
Read this as "row counts unchanged, glioma no-detected values shifted," not "nothing changed."

The primary mutagenic interpretable rows remain 17,894 glioma rows and 11,483 bladder-cancer rows.
Among interpretable bladder rows, mean `delta_mutagenic_primary` is -0.008166, with a minimum of -0.166894 and a maximum of 0.063492.
Among interpretable glioma rows, mean `delta_mutagenic_primary` is 0.000484, with a minimum of -0.010522 and a maximum of 0.015834.

The confirmed-naive arm is no longer empty because the schema cannot express sample-level pretreatment labels; it is empty because confirmed-naive support remains too thin by the two-study rule.
The underpowered confirmed-naive rows are concentrated in bladder cancer, non-small cell lung cancer, and embryonal tumor.
BLCA Cornell contributes useful pretreatment samples, but one bladder study is not enough for an interpretable cross-study confirmed-naive contrast.

## Evidence Quality

Evidence type: `empirical_data_evidence` for the local full-config cBioPortal/GENIE pipeline output, plus workflow-validation evidence from the forced Snakemake run.

The evidence is strong that the t209 schema fix behaves as intended.
Focused tests prove the new sample-level targets, the config wiring pins the two real rules, and the full workflow regenerated the annotation sidecar, per-study views, impact tables, and datapackage.

The evidence remains weak for the biological H10 proposition.
The analysis still excludes by clinical labels rather than measured therapy-signature exposure.
Clinical treatment, recurrence/progression, cancer subtype, panel coverage, and mutation burden remain entangled.
In GLASS specifically, the glioma contrast remains a longitudinal treatment/timing/progression mixture rather than a clean TMZ causal contrast.

## Open Questions

`question:0024-treatment-exposed-cohort-chemotherapy-signature` advances from a schema standpoint.
The known sample-level positive, unknown, and pretreatment labels for DIFG/GLASS and BLCA Cornell are now expressible and propagated through the H10 denominator outputs.
q024 remains partial because audit recall is still unmeasured and many no-signal studies are not confirmed naive.

`question:0027-does-excluding-treatment-signature-high-samples` remains active and unanswered.
The next task should define therapy-signature-high samples from measured SBS11/SBS31/SBS35/SBS87 exposure, then reuse the H10 denominator machinery to compare all-sample frequencies against signature-high-excluded frequencies.
That task should be planned separately so clinical-label and signature-outcome evidence remain distinct.

## Implications

The H10 exposure-label substrate is now ready for the next branch.
It should remain a denominator-sensitivity layer, not the final biological H10 test.

The next step is to file and plan the q027 therapy-signature-high exclusion arm.
That plan should use measured signature exposures, define high-exposure thresholds before running, state how SBS11/SBS31/SBS35/SBS87 are handled when absent or under count floor, and emit a separate interpretation rather than overwriting the t207-t209 exposure-label notes.
