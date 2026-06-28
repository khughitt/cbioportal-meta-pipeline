---
type: interpretation
title: t210 q027 therapy-signature-high exclusion impact arm
status: active
created: '2026-06-01'
updated: '2026-06-28'
id: interpretation:0034-t210-q027-therapy-signature-high-exclusion
source_refs: &id001
- code/config/config-q027-therapy-signature-high.yml
- code/scripts/audit_q027_therapy_signature_substrate.py
- code/scripts/run_restricted_sigprofiler_assignment.py
- code/scripts/annotate_q027_signature_high.py
- code/scripts/create_q027_signature_high_freq_tables.py
- code/scripts/create_q027_signature_high_impact_table.py
- code/workflows/Snakefile
- doc/plans/2026-06-01-t210-q027-therapy-signature-high-exclusion.md
- doc/reports/2026-06-01-t210-q027-therapy-signature-substrate-feasibility.md
- /data/packages/cbioportal/q027-therapy-signature-high-2026-06-01/metadata/samples_q027_signature_high.feather
- /data/packages/cbioportal/q027-therapy-signature-high-2026-06-01/summary/mut/table/gene_cancer_q027_signature_high_impact.datapackage.json
- /data/packages/cbioportal/q027-therapy-signature-high-2026-06-01/summary/mut/table/gene_cancer_q027_signature_high_impact_ratio.feather
related:
- hypothesis:0009-treatment-induced-signature-frequency-contamination
- question:0027-does-excluding-treatment-signature-high-samples
- question:0024-treatment-exposed-cohort-chemotherapy-signature
- task:t207
- task:t208
- task:t209
- task:t210
input: *id001
prior_interpretations:
- interpretation:0030-t207-h10-treatment-impact-full-config
- interpretation:0032-t208-h10-sample-level-mutagenic-rules
- interpretation:0033-t209-h10-sample-level-unknown-naive-rules
---

# Interpretation: t210 `q027` therapy-signature-high exclusion impact arm

Project links: this interpretation closes the `task:t210` measured-signature arm that follows
`task:t207`, `task:t208`, and `task:t209`.
It informs `question:0027-does-excluding-treatment-signature-high-samples`,
`question:0024-treatment-exposed-cohort-chemotherapy-signature`, and
`hypothesis:0009-treatment-induced-signature-frequency-contamination`.
It should be read after `interpretation:0030-t207-h10-treatment-impact-full-config`,
`interpretation:0032-t208-h10-sample-level-mutagenic-rules`, and
`interpretation:0033-t209-h10-sample-level-unknown-naive-rules`.

## Verdict

**Verdict:** [?] The `q027` measured-signature arm now runs end-to-end, but it is non-arbitrating for `H10` because the primary configured substrate contains one interpretable patient study.

This task implements the distinct `q027` arm that t207-t209 deliberately deferred.
The exclusion set is derived from measured SBS11/SBS31/SBS35/SBS87 exposure, not from clinical treatment labels.
For the first configured pass, WP1 selected `difg_glass_2019` as the only primary patient substrate that passed the mutation-count and comparator gate, and the downstream `q027` target ran on GLASS/SBS11.

The run finds 36 SBS11-high GLASS samples and non-trivial single-study frequency shifts when those samples are excluded.
Those shifts should not be read as cross-study `H10` evidence.
Every `q027` impact row is `underpowered_non_arbitrating` because the primary pass has only one contributing study, below the pre-specified two-study threshold.
That outcome was knowable after WP1 selected only one primary patient study; the downstream impact tables are reusable scaffolding and a single-study sensitivity check, not a late-stage discovery that `q027` was underpowered.

## Substrate

WP1 audited the five treatment-signature candidates named in the t210 plan from the `H10` exposure-label work.
It did not exhaustively scan all 198 configured cBioPortal studies for SBS11/SBS31/SBS35/SBS87-evaluable patient cohorts; the audit implementation was `code/scripts/audit_q027_therapy_signature_substrate.py`.
Therefore, "no second substrate" means no second substrate in this planned candidate set, not proof that no other configured study could support `q027` after a broader search.

| Study | Target signatures | Primary patient denominator | Count-floor-passing samples | Retained comparator support | WP1 gate |
|---|---|---:|---:|---:|---|
| `difg_glass_2019` | `SBS11` | yes | 160 / 444 | 31 | pass |
| `blca_cornell_2016` | `SBS31`, `SBS35` | yes | 14 / 72 | 5 | fail |
| `blca_dfarber_mskcc_2014` | `SBS31`, `SBS35` | yes | 15 / 50 | 0 | fail |
| `sclc_cancercell_gardner_2017` | `SBS31`, `SBS35` | no, PDX sensitivity-only | 20 / 20 | 0 | fail |
| `pptc_2019` | `SBS11`, `SBS31`, `SBS35`, `SBS87` | no, PDX sensitivity-only | 1 / 118 | 0 | fail |

The resulting `q027` config is therefore intentionally scoped to `difg_glass_2019` with CNS lookup signatures plus the explicit therapy-signature add-ons `SBS11`, `SBS31`, `SBS35`, and `SBS87`.
The COSMIC reference audit confirmed all requested therapy signatures were present for the `q027` refit.

## Signature Labels

The per-sample assignment table covers 444 GLASS samples in `/data/packages/cbioportal/q027-therapy-signature-high-2026-06-01/metadata/samples_q027_signature_high.feather`.
The t179 WES count floor is 383 SBS, so 284 samples are unevaluable rather than negative in `/data/packages/cbioportal/q027-therapy-signature-high-2026-06-01/metadata/samples_q027_signature_high.feather`.

| Label | Samples |
|---|---:|
| Below count floor / unevaluable | 284 |
| Count-floor passing | 160 |
| Count-floor passing with no target SBS11 exposure | 124 |
| Primary SBS11-high, exposure >= 50 SBS | 36 |

The pre-specified sensitivity labels did not broaden the exclusion set in this run.
The >=20 SBS, fraction >=0.10, and any non-zero SBS11 sensitivity rules all selected the same 36 samples as the primary >=50 SBS rule.

Among count-floor-passing samples, median SBS11 exposure was 0 because most evaluable samples had no assigned SBS11.
Among the 36 SBS11-high samples, median SBS11 exposure was 7,197.5 SBS and median SBS11 fraction was 1.0 in `/data/packages/cbioportal/q027-therapy-signature-high-2026-06-01/metadata/samples_q027_signature_high.feather`.
This is a strong measured-signature stratum within GLASS, not just a weak non-zero refit tail.

## Impact Read

The `q027` impact ratio table has 20,822 GLASS gene-cancer rows and 150 columns in `/data/packages/cbioportal/q027-therapy-signature-high-2026-06-01/summary/mut/table/gene_cancer_q027_signature_high_impact_ratio.feather`.
All rows are `underpowered_non_arbitrating` for the primary, sensitivity, evaluable-only, and hypermutator-excluded marginal contrasts.

| Contrast | Removed samples | Power status | Delta summary |
|---|---:|---|---|
| `delta_signature_high_excluded_primary` | 36 | 20,822 / 20,822 underpowered | mean +0.0253, max +0.0669 |
| `delta_signature_high_excluded_primary_hypermutator_excluded` | 36 | 20,822 / 20,822 underpowered | identical to primary |
| `delta_signature_evaluable_high_excluded_primary` | 36 | 20,822 / 20,822 underpowered | mean +0.0585, max +0.1738 |
| `delta_signature_evaluable_high_excluded_primary_hypermutator_excluded` | 36 | 20,822 / 20,822 underpowered | identical to evaluable-only |
| `delta_signature_high_excluded_sensitivity_20` | 36 | 20,822 / 20,822 underpowered | identical to primary |
| `delta_signature_high_excluded_sensitivity_fraction_10` | 36 | 20,822 / 20,822 underpowered | identical to primary |

The full-denominator contrast compares 444 all samples against 408 non-high samples in `/data/packages/cbioportal/q027-therapy-signature-high-2026-06-01/summary/mut/table/gene_cancer_q027_signature_high_impact_ratio.feather`.
It answers the deliverable question but dilutes the measured-signature effect because 284 below-floor samples remain in both arms.
The evaluable-only contrast compares 160 count-floor-passing samples against 124 evaluable non-high samples in `/data/packages/cbioportal/q027-therapy-signature-high-2026-06-01/summary/mut/table/gene_cancer_q027_signature_high_impact_ratio.feather` and is therefore the cleaner "what changes among samples where `q027` is measurable" read.

The largest full-denominator descriptive deltas are concentrated in genes with many mutations inside the SBS11-high GLASS subset.

| Gene | All-sample mean | SBS11-high-excluded mean | Delta | Removed mutated samples |
|---|---:|---:|---:|---:|
| `UBR4` | 0.1306 | 0.0637 | +0.0669 | 32 |
| `LRP1` | 0.1351 | 0.0686 | +0.0665 | 32 |
| `GCN1L1` | 0.1081 | 0.0417 | +0.0664 | 31 |
| `HERC2` | 0.1824 | 0.1176 | +0.0648 | 33 |
| `HERC1` | 0.1554 | 0.0907 | +0.0647 | 32 |

The largest evaluable-only deltas are larger, as expected when the below-floor denominator is removed.

| Gene | Evaluable mean | Evaluable SBS11-high-excluded mean | Delta | Removed mutated samples |
|---|---:|---:|---:|---:|
| `GCN1L1` | 0.2625 | 0.0887 | +0.1738 | 31 |
| `UBR4` | 0.2938 | 0.1210 | +0.1728 | 32 |
| `LRP1` | 0.2938 | 0.1210 | +0.1728 | 32 |
| `TNXB` | 0.1938 | 0.0242 | +0.1696 | 28 |
| `COL7A1` | 0.2063 | 0.0403 | +0.1659 | 28 |

This is useful as a deliverable-sensitivity check.
It says that a measured SBS11-high GLASS subset can materially inflate some single-study glioma gene frequencies.
It does not say that treatment-signature-high samples are a reproducible cross-study driver-frequency contaminant, because there is no second primary patient study in this `q027` substrate.

## Hypermutator Marginal Read

The existing hypermutator flag does not remove the `q027` SBS11-high GLASS samples in this run, as recorded in `/data/packages/cbioportal/q027-therapy-signature-high-2026-06-01/metadata/samples_q027_signature_high.feather`.
All 444 GLASS samples have `is_hypermutator == False`, including all 36 SBS11-high samples.
The SBS11-high samples carry `hypermutator_reason == gmm_upper_mode_below_floor`, but that reason does not set the final hypermutator flag.

Consequently, the hypermutator-excluded `q027` deltas are identical to the inclusive `q027` deltas.
This answers the marginal-value question directly for this substrate: `q027` is not redundant with the current `is_hypermutator` exclusion layer here.
The caveat is the same as above: this marginal value is demonstrated only as a one-study GLASS sensitivity check, so it remains non-arbitrating for `H10`.

## Relation To t207-t209

t207-t209 answered the clinical exposure-label arm.
Those tasks repaired the distinction between treatment-exposed, unknown, confirmed pretreatment, and no-detected-treatment metadata.

t210 answers a different question.
A sample can be clinically treatment-positive without being SBS11/SBS31/SBS35/SBS87-high, and a sample can be signature-high even when treatment metadata is incomplete.
The `q027` labels therefore should not be merged into `samples_treatment_exposure.feather` or interpreted as a replacement for the t207-t209 denominator labels.

The `q027` result strengthens one narrow point from the earlier `H10` notes: clinical labels and measured signature outcomes must stay separate.
It does not change the locked `H10` status.

## Caveats

The main limitation is power.
Only GLASS passed the first primary patient gate, so the cross-study power rule correctly marks the result as non-arbitrating.
Because only one primary patient study passed WP1, this limitation was determined before the impact stage.

The second limitation is clinical confounding inside GLASS.
SBS11-high GLASS samples are likely entangled with post-treatment recurrence/progression and sampling episode.
Measured SBS11 exposure reduces exposure-label misclassification, but it does not by itself identify a TMZ causal effect on driver-frequency ranks.

The third limitation is count-floor missingness.
The 284 below-floor samples are unevaluable, not SBS11-negative in `/data/packages/cbioportal/q027-therapy-signature-high-2026-06-01/metadata/samples_q027_signature_high.feather`.
Any future expansion of `q027` should preserve this semantics; widening the analysis by silently treating below-floor samples as negative would recreate the silent-fallback problem that t209 fixed for clinical labels.
The full-denominator contrast necessarily retains below-floor samples in the non-high arm, so it should be read alongside the evaluable-only contrast rather than as the sole effect-size estimate.

## Operational Provenance

The final `q027` workflow writes to an isolated output directory:
`/data/packages/cbioportal/q027-therapy-signature-high-2026-06-01`.
It reads source mutation/sample/hypermutator inputs from `/data/packages/cbioportal/full` through `q027_source_out_dir`, so the `q027` probe does not overwrite the full-config `H10` substrate.

An early local run used the full output directory before this isolation was added.
That was detected by checking the full `samples_annotated.feather` shape and restored by rerunning the full `all_h10_treatment_impact` target on `code/config/config-full.yml`.
The restored full substrate has 383,477 samples across 198 studies in `/data/packages/cbioportal/full/metadata/samples_annotated.feather`, and the final full `H10` target reported no work remaining before the isolated `q027` run was accepted.

Operational source refs include `code/config/config-q027-therapy-signature-high.yml`,
`code/scripts/audit_q027_therapy_signature_substrate.py`,
`code/scripts/run_restricted_sigprofiler_assignment.py`,
`code/scripts/annotate_q027_signature_high.py`,
`code/scripts/create_q027_signature_high_freq_tables.py`,
`code/scripts/create_q027_signature_high_impact_table.py`, `code/workflows/Snakefile`,
`doc/plans/2026-06-01-t210-q027-therapy-signature-high-exclusion.md`,
`doc/reports/2026-06-01-t210-q027-therapy-signature-substrate-feasibility.md`,
`/data/packages/cbioportal/q027-therapy-signature-high-2026-06-01/metadata/samples_q027_signature_high.feather`,
`/data/packages/cbioportal/q027-therapy-signature-high-2026-06-01/summary/mut/table/gene_cancer_q027_signature_high_impact.datapackage.json`,
and
`/data/packages/cbioportal/q027-therapy-signature-high-2026-06-01/summary/mut/table/gene_cancer_q027_signature_high_impact_ratio.feather`.

## Implications

`question:0027-does-excluding-treatment-signature-high-samples` is now technically answered for the currently feasible substrate but not scientifically arbitrated.
The answer is: excluding SBS11-high samples changes the GLASS glioma frequency table descriptively, but the configured `q027` evidence is too thin to adjudicate `H10`.

The most useful next step is not another broad `H10` verdict update.
If `H10` remains a priority, the next work should either identify a second primary patient substrate with enough therapy-signature-evaluable samples, or do a GLASS-specific clinical timing audit to determine whether SBS11-high status is separable from recurrence/progression in this cohort.
