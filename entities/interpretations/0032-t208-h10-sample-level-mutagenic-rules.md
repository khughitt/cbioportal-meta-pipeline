---
type: interpretation
title: t208 H10 sample-level mutagenic-treatment rule impact
status: active
created: '2026-06-01'
updated: '2026-06-28'
id: interpretation:0032-t208-h10-sample-level-mutagenic-rules
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
- hypothesis:0009-treatment-induced-signature-frequency-contamination
- question:0024-treatment-exposed-cohort-chemotherapy-signature
- question:0027-does-excluding-treatment-signature-high-samples
- task:t206
- task:t207
- task:t208
input: *id001
prior_interpretations:
- interpretation:0029-t206-treatment-exposure-audit
- interpretation:0030-t207-h10-treatment-impact-full-config
---

# Interpretation: t208 `H10` sample-level mutagenic-treatment rule impact

Project links: this interpretation contributes to
`hypothesis:0009-treatment-induced-signature-frequency-contamination` and follows `task:t206`,
`task:t207`, and `task:t208`.

## Verdict

**Verdict:** [?] Improved exposure-label substrate, still non-arbitrating for the biological `H10` claim.

The t208 follow-up adds deterministic sample-level primary mutagenic-treatment rules for the two clearest mixed cohorts from the t206 audit:
`difg_glass_2019` via `TMZ_TREATMENT == "Yes"` and `blca_cornell_2016` via `SPECIMEN_COLLECTION_PRE_OR_POST_CHEMO == "post-chemotherapy"`.
The full `all_h10_treatment_impact` target reruns with those rules and produces updated impact outputs.

This materially improves the primary mutagenic-treatment contrast, but it also exposes a comparator-definition gap.
It increases labeled primary mutagenic samples from 50 to 280 and expands interpretable `delta_mutagenic_primary` rows from 8,834 to 29,377.
For DIFG/GLASS, the residual comparator is not cleanly untreated: 161 of the 265 non-TMZ-positive samples have blank `TMZ_TREATMENT`, so they are unknown-not-confirmed-naive rather than explicit TMZ-negative controls.
The result still does not answer `q027`, because `q027` requires measured therapy-signature-high samples from SBS11/SBS31/SBS35/SBS87 exposure rather than clinical treatment labels.

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

The DIFG/GLASS residual no-detected bucket is mixed.
Among 444 samples, `TMZ_TREATMENT` is `Yes` for 179 samples, explicit `No` for 104 samples, and blank for 161 samples.
The current sample-level rule mechanism only marks positives; it has no sample-level `treatment_metadata_unknown` target.
As a result, the 161 blank-TMZ samples remain in `no_detected_treatment_signal`.
That label should be read as "no positive sample-level TMZ label detected" for this cohort, not as confirmed absence of relevant therapy.

BLCA Cornell has the opposite missed opportunity.
Its 21 `pre-chemotherapy` samples are genuine pretreatment-at-collection comparators within the same study, but the current sample-level target vocabulary cannot mark `positive_naive_or_pretreatment`.
Those samples also enter the generic no-detected bucket instead of contributing to the confirmed-naive contrast.

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

The glioma read also has a specific longitudinal confound.
GLASS is a longitudinal glioma study, and `TMZ_TREATMENT` is entangled with surgical episode and recurrence/progression.
In the raw clinical table, sample types include 215 primary tumors and 229 recurrence samples.
The non-`Yes` group is not simply pretreatment primary glioma: among the 161 blank-TMZ samples, 125 are recurrence samples and 36 are primary samples; among the 104 explicit `No` samples, 50 are recurrence samples and 54 are primary samples.
Therefore the glioma `delta_mutagenic_primary` contrast can mix temozolomide exposure, recurrence/progression biology, sampling time, and clinical ascertainment.
It should not be interpreted as a clean TMZ causal contrast.

## Evidence Quality

Evidence type: `empirical_data_evidence` for the local full-config cBioPortal/GENIE pipeline output, plus workflow-validation evidence from the forced Snakemake target.

The evidence is strong that deterministic sample-level treatment labels can be joined and propagated through the `H10` denominator machinery on the full configured substrate.
The label counts match the raw-clinical expectations from the t206 audit: 179 TMZ-positive DIFG samples and 51 post-chemotherapy BLCA Cornell samples.

The evidence is weaker for the `H10` biological proposition.
The output shows that treatment labels can change gene-cancer frequency summaries in bladder and glioma, but it does not establish that therapy-induced SBS11/SBS31/SBS35/SBS87 processes are causing the changes.
Clinical treatment labels, cancer-type composition, panel coverage, treatment timing, recurrence/progression, and mutation burden remain entangled.
The DIFG/GLASS comparator specifically includes 161 blank-TMZ samples, so the current implementation still has a silent-negative behavior for sample-level unknown treatment status.

## Open Questions

`question:0024-treatment-exposed-cohort-chemotherapy-signature` advances again.
The project now has both whole-study and deterministic sample-level exposure-label handling for the strongest available mixed mutagenic cohorts.
`q024` remains partial because treatment-metadata-unknown remains large, sample-level unknowns cannot yet be marked, and audit false-negative recall is still unmeasured.

The most immediate schema follow-up is to extend sample-level rules beyond positive treatment labels.
The rule target vocabulary should support at least sample-level `treatment_metadata_unknown` and `positive_naive_or_pretreatment`.
That would keep blank DIFG TMZ labels out of an overconfident no-detected comparator and would let the 21 BLCA Cornell pre-chemotherapy samples feed the confirmed-naive sensitivity arm.

`question:0027-does-excluding-treatment-signature-high-samples` remains active and unanswered.
The next `q027` pass should define high-exposure samples from measured SBS11/SBS31/SBS35/SBS87 assignments, then reuse the `H10` denominator machinery to ask whether signature-high exclusion changes pooled frequencies and ranks.

## Implications

`H10` remains proposed and unresolved.
The infrastructure is now stronger than it was in t207, and the primary mutagenic label arm is no longer a single-study bladder-only contrast.
However, this still reads as an exposure-label sensitivity analysis rather than a therapy-signature causal test.

The next useful `H10` implementation step is not yet `q027`.
First, the sample-level `H10` schema should support unknown and confirmed-naive targets so the exposure-label comparator is not silently overconfident.
After that repair, the `q027` signature-high arm should be filed separately, use measured SBS11/SBS31/SBS35/SBS87 exposure, and write a separate interpretation so clinical-label and signature-outcome evidence do not collapse into one verdict.
