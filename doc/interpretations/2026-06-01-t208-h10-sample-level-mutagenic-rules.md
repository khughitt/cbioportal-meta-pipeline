---
id: interpretation:2026-06-01-t208-h10-sample-level-mutagenic-rules
type: interpretation
title: t208 H10 sample-level mutagenic-treatment rule impact
status: active
source_refs: &id001
  - code/config/config-full.yml
  - code/scripts/annotate_treatment_exposure.py
  - code/scripts/create_h10_treatment_freq_tables.py
  - code/scripts/create_h10_treatment_impact_table.py
  - doc/interpretations/2026-06-01-t206-treatment-exposure-audit.md
  - doc/interpretations/2026-06-01-t207-h10-treatment-impact-full-config.md
  - /data/packages/cbioportal/full/metadata/samples_treatment_exposure_counts.tsv
  - /data/packages/cbioportal/full/summary/mut/table/gene_cancer_h10_treatment_impact.datapackage.json
  - /data/packages/cbioportal/full/summary/mut/table/gene_cancer_h10_treatment_impact_ratio.feather
related:
  - hypothesis:h10-treatment-induced-signature-frequency-contamination
  - question:q024-treatment-exposed-cohort-chemotherapy-signature
  - question:q027-does-excluding-treatment-signature-high-samples
  - task:t206
  - task:t207
  - task:t208
created: "2026-06-01"
updated: "2026-06-01"
input: *id001
prior_interpretations:
  - interpretation:2026-06-01-t206-treatment-exposure-audit
  - interpretation:2026-06-01-t207-h10-treatment-impact-full-config
---

# Interpretation: t208 H10 sample-level mutagenic-treatment rule impact

## Verdict

**Verdict:** [?] Improved exposure-label substrate, still non-arbitrating for the biological H10 claim.

The t208 follow-up adds deterministic sample-level primary mutagenic-treatment rules for the two clearest mixed cohorts from the t206 audit:
`difg_glass_2019` via `TMZ_TREATMENT == "Yes"` and `blca_cornell_2016` via `SPECIMEN_COLLECTION_PRE_OR_POST_CHEMO == "post-chemotherapy"`.
The full `all_h10_treatment_impact` target reruns with those rules and produces updated impact outputs.

This materially improves the primary mutagenic-treatment contrast.
It increases labeled primary mutagenic samples from 50 to 280 and expands interpretable `delta_mutagenic_primary` rows from 8,834 to 29,377.
The result still does not answer q027, because q027 requires measured therapy-signature-high samples from SBS11/SBS31/SBS35/SBS87 exposure rather than clinical treatment labels.

## What Changed

The config now carries two sample-level rules under `h10_treatment_denominator.sample_level_rules`.

| Rule | Study | Clinical column | Positive value | Labeled samples |
|---|---|---|---|---:|
| `difg_glass_2019_tmz` | `difg_glass_2019` | `TMZ_TREATMENT` | `Yes` | 179 |
| `blca_cornell_2016_post_chemo` | `blca_cornell_2016` | `SPECIMEN_COLLECTION_PRE_OR_POST_CHEMO` | `post-chemotherapy` | 51 |

The raw `SAMPLE_ID` joins succeeded against canonical `samples_annotated.feather`.
The per-study counts sidecar now reports:

| Study | Samples | Primary mutagenic samples | No-detected-treatment-signal samples |
|---|---:|---:|---:|
| `blca_dfarber_mskcc_2014` | 50 | 50 | 0 |
| `blca_cornell_2016` | 72 | 51 | 21 |
| `difg_glass_2019` | 444 | 179 | 265 |

Across the full annotation table, total primary mutagenic-treatment signal is now 280 samples.
Broad treatment-exposed labels rise to 1,462 samples because primary mutagenic sample-level positives are also broad treatment positives.
The no-detected-treatment-signal comparator falls from 326,746 to 326,516 samples.

## Impact Read

The refreshed ratio impact table still has 776,686 rows and 51 columns.
Power improves most in the primary mutagenic contrast:

| Contrast | Interpretable rows | No-contrast rows | Underpowered rows | Read |
|---|---:|---:|---:|---|
| `delta_no_detected_contrast` | 106,185 | 646,046 | 24,455 | broader comparator improves because sample-level positives leave the no-detected set |
| `delta_broad` | 80,394 | 687,981 | 8,311 | broad cohort-composition sensitivity gains coverage |
| `delta_mutagenic_primary` | 29,377 | 742,757 | 4,552 | now covers bladder plus glioma, not bladder alone |
| `delta_confirmed_naive_contrast` | 0 | 770,242 | 6,444 | unchanged; confirmed-naive support remains too thin |

For `delta_mutagenic_primary`, interpretable rows now occur in two cancer types:
17,894 glioma rows and 11,483 bladder-cancer rows.
This is the expected consequence of adding `difg_glass_2019` and `blca_cornell_2016`.

The largest bladder-cancer effects remain sensitive to single-study and panel-coverage structure.
Among interpretable bladder rows, the mean `delta_mutagenic_primary` is -0.0082, with a minimum of -0.1669 and a maximum of 0.0635.
Some large negative rows remove only the 50 `blca_dfarber_mskcc_2014` samples because those genes are not represented across every bladder panel view.
Rows where 101 samples are removed reflect both `blca_dfarber_mskcc_2014` and `blca_cornell_2016`.

The glioma effects are smaller.
Among interpretable glioma rows, the mean `delta_mutagenic_primary` is 0.00048, with a minimum of -0.0105 and a maximum of 0.0158.
The top positive glioma deltas include `TMEM178B`, `SLC15A5`, `PITPNC1`, and `CD38`; these should be treated as denominator-sensitivity rows, not as mechanistic treatment-signature hits.

## Evidence Quality

Evidence type: `empirical_data_evidence` for the local full-config cBioPortal/GENIE pipeline output, plus workflow-validation evidence from the forced Snakemake target.

The evidence is strong that deterministic sample-level treatment labels can be joined and propagated through the H10 denominator machinery on the full configured substrate.
The label counts match the raw-clinical expectations from the t206 audit: 179 TMZ-positive DIFG samples and 51 post-chemotherapy BLCA Cornell samples.

The evidence is weaker for the H10 biological proposition.
The output shows that treatment labels can change gene-cancer frequency summaries in bladder and glioma, but it does not establish that therapy-induced SBS11/SBS31/SBS35/SBS87 processes are causing the changes.
Clinical treatment labels, cancer-type composition, panel coverage, treatment timing, and mutation burden remain entangled.

## Open Questions

`question:q024-treatment-exposed-cohort-chemotherapy-signature` advances again.
The project now has both whole-study and deterministic sample-level exposure-label handling for the strongest available mixed mutagenic cohorts.
q024 remains partial because treatment-metadata-unknown remains large and audit false-negative recall is still unmeasured.

`question:q027-does-excluding-treatment-signature-high-samples` remains active and unanswered.
The next q027 pass should define high-exposure samples from measured SBS11/SBS31/SBS35/SBS87 assignments, then reuse the H10 denominator machinery to ask whether signature-high exclusion changes pooled frequencies and ranks.

## Implications

H10 remains proposed and unresolved.
The infrastructure is now stronger than it was in t207, and the primary mutagenic label arm is no longer a single-study bladder-only contrast.
However, this still reads as an exposure-label sensitivity analysis rather than a therapy-signature causal test.

The next useful H10 step is the q027 signature-high arm.
It should be filed separately from t208, use measured SBS11/SBS31/SBS35/SBS87 exposure, and write a separate interpretation so clinical-label and signature-outcome evidence do not collapse into one verdict.
