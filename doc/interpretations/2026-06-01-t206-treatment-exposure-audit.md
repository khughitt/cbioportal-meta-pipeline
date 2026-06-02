---
id: "interpretation:2026-06-01-t206-treatment-exposure-audit"
type: "interpretation"
status: "active"
source_refs:
  - "task:t206"
title: "t206 H10 treatment-exposure audit manual review — 167 non-TCGA studies; layered broad vs mutagenic-treatment label design"
date: "2026-06-01"
related:
  - "task:t206"
  - "hypothesis:h10-treatment-induced-signature-frequency-contamination"
  - "question:q024-treatment-exposed-cohort-chemotherapy-signature"
---
# t206 — H10 treatment-exposure audit manual review

Date: 2026-06-01

## Question

Which non-TCGA cBioPortal studies in `config-full.yml` are ready to be treated as treatment-exposed strata for `hypothesis:h10`, and which need sample-level fraction review before they can affect the frequency-table denominator?

This is a manual-review note for the metadata scaffold in `code/scripts/audit_treatment_exposed_studies.py`.
It does not estimate H10 support and does not yet change the frequency tables.
Related project entities: `task:t206`, `hypothesis:h10-treatment-induced-signature-frequency-contamination`, `question:q024-treatment-exposed-cohort-chemotherapy-signature`, and `question:q027-does-excluding-treatment-signature-high-samples`.

## Input

The local scaffold table was regenerated at `results/h10-treatment-exposure-audit-2026-06-01.tsv`.
It audits 167 non-TCGA studies from `code/config/config-full.yml` against local cBioPortal metadata under `/data/raw/cbioportal`.

Current tier counts:

| Candidate tier | Recommendation | Studies |
|---|---|---:|
| `explicit_treatment_exposed` | `flag_exposed` | 11 |
| `advanced_metastatic_enriched` | `review_for_fraction` | 20 |
| `clinical_signal_present` | `review_for_fraction` | 22 |
| `missing_metadata` | `needs_manual_review` | 2 |
| `no_metadata_signal` | `do_not_flag` | 109 |
| `treatment_naive_or_pretreatment` | `do_not_flag` | 3 |

## Manual Review Result

The 11 `flag_exposed` studies are confirmed as broad treatment-exposed cohort candidates.
They are suitable for a proposed `treatment_exposed_studies` label set after config update, but they should not all be interpreted as likely carriers of SBS11/SBS31/SBS35/SBS87.
Several are immunotherapy, endocrine, targeted, or castration-resistant cohorts where the label is still useful as cohort-composition nuisance context, but not a direct DNA-damaging-signature expectation.

| Study | Manual action | Treatment-exposure read | Signature expectation |
|---|---|---|---|
| `blca_dfarber_mskcc_2014` | propose broad flag | cisplatin-treated muscle-invasive bladder cancer | platinum-signature plausible |
| `brca_dfci_2020` | propose broad flag | CDK4/6i-exposed metastatic breast cancer | treated cohort, not direct mutagenic-therapy evidence |
| `brca_fuscc_2020` | propose broad flag | refractory metastatic TNBC trial cohort | prior-treatment likely; mutagenic class not resolved from metadata |
| `brca_mskcc_2019` | propose broad flag | buparlisib/alpelisib plus letrozole-treated metastatic ER+ tumors | treated cohort, not direct mutagenic-therapy evidence |
| `mel_ucla_2016` | propose broad flag | pretreated pembrolizumab/nivolumab melanoma | treated cohort; ICB is not the therapy-signature endpoint |
| `mixed_allen_2018` | propose broad flag | immune-checkpoint-inhibitor-treated mixed solid tumors | treated cohort; mixed cancer denominator caveat |
| `nepc_wcm_2016` | propose broad flag | metastatic castration-resistant prostate cohort | treatment-resistant cohort, not direct mutagenic-therapy evidence |
| `nsclc_mskcc_2018` | propose broad flag | PD-1 plus CTLA-4 blockade-treated NSCLC | treated cohort; ICB is not the therapy-signature endpoint |
| `prad_su2c_2019` | propose broad flag | castrate-resistant metastatic prostate cohort | treatment-resistant cohort, not direct mutagenic-therapy evidence |
| `sclc_cancercell_gardner_2017` | sensitivity only | chemosensitive/chemoresistant SCLC PDX cohort | chemotherapy-resistance signal, but PDX denominator exclusion |
| `skcm_mskcc_2014` | propose broad flag | pretreated ipilimumab/tremelimumab melanoma | treated cohort; ICB is not the therapy-signature endpoint |

The next config artifact should not be a single flat treatment list for H10.
A flat list would pool platinum/TMZ-like candidates with ICB/endocrine/targeted/castration-resistant cohorts, diluting the specific therapy-signature prediction in `hypothesis:h10`.
The proposed labels should instead be layered:
This is a provisional `manual-review-v0` schema for the next config/schema plan, not a final committed config contract.

```yaml
# Broad cohort-composition nuisance stratum.
# This is not the primary mutagenic-signature H10 test.
treatment_exposed_studies:
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

# Study-level candidates where the metadata supports a DNA-damaging-signature expectation.
# PDX cohorts are excluded from the primary patient denominator even when chemotherapy-related.
mutagenic_treatment_signal_studies:
  - blca_dfarber_mskcc_2014

mutagenic_treatment_signal_sensitivity_only_studies:
  - sclc_cancercell_gardner_2017
```

The broad flag answers "could cohort composition differ by treatment history?"
The narrower field answers "should SBS11/SBS31/SBS35/SBS87 be expected a priori?"
Only the narrower mutagenic layer should drive the primary H10 therapy-signature impact test.
The broad layer is a cohort-composition sensitivity.

## Fraction-Review Candidates

Several `review_for_fraction` studies carry stronger sample-level exposure information than their study-level descriptions alone.
These should not be promoted into `treatment_exposed_studies`, because the study is mixed.
They are better represented through `treatment_exposed_study_fractions` or a later per-sample treatment field.

High-priority fraction-review candidates:

| Study | Local clinical evidence | Suggested handling |
|---|---|---|
| `blca_cornell_2016` | `SPECIMEN_COLLECTION_PRE_OR_POST_CHEMO`: 51 / 72 post-chemotherapy; prior therapy includes gemcitabine/cisplatin, MVAC, docetaxel, carboplatin, BCG, and mitomycin labels | sample-level fraction candidate; platinum-signature plausible |
| `difg_glass_2019` | `TMZ_TREATMENT`: 179 Yes / 104 No / 161 blank; `CONCURRENT_TMZ`: 108 Yes / 25 No / 311 blank; recurrent glioma substrate | sample-level fraction candidate; SBS11/TMZ plausible |
| `coadread_mskcc` | `TUMOR_TREATED`: 60 chemonaive, 48 both treated, 22 metastasis treated, 6 before both resections, 2 primary treated | sample-level fraction candidate; chemotherapy class unresolved |
| `coadread_cass_2020` | `METASTATIC_STATUS` includes metastatic and non-metastatic preoperative-treatment categories | sample-level fraction candidate; derive from status labels |
| `brca_mbcproject_wagle_2017` | `CALC_TREATMENT_NAIVE`: 96 Yes, 40 No, 3 Unknown, 98 blank | fraction candidate only with missingness reported |
| `mpcproject_broad_2021` | `CALC_TREATMENT_NAIVE`: 18 No, 13 Yes, 51 abstraction pending, 41 blank | defer or report as missingness-heavy fraction |
| `aml_ohsu_2018` | treatment-regimen columns are populated for most samples; 31 samples have zero cumulative treatment type count | likely treatment-rich, but hematologic-disease and treatment-timing semantics need separate handling |
| `aml_ohsu_2022` | `IS_RELAPSE`: 62 true / 859 false / 21 unknown; treatment-regimen columns are broadly populated | sample-level treatment-rich candidate; relapse and treatment fields should be separated |
| `brain_cptac_2020` | `TREATMENT_STATUS`: 36 post-treatment / 182 treatment naive; chemotherapy agents include temozolomide and platinum-containing regimens | sample-level fraction candidate; pediatric brain mixed-substrate caveat |
| `pptc_2019` | `TX_CISPLATIN` is nonblank for 47 / 261 PDX samples | exclude from primary patient denominator; sensitivity-only if PDX handling is explicitly modeled |

The advanced/metastatic-only studies without direct treatment columns should remain out of the primary H10 label set.
They may still be useful as a stage-enriched sensitivity, but treating metastatic status as treatment exposure would confound treatment history with disease stage.

For the mutagenic-treatment layer, the highest-priority mixed-cohort fraction candidates are `blca_cornell_2016` and `difg_glass_2019`.
`brain_cptac_2020` may become a mixed-substrate sensitivity after pediatric brain subtype and treatment-timing review.
PDX cohorts should stay out of the primary patient frequency denominator because passaging and non-human read artifacts can alter mutation calls independently of patient treatment history.

## Positive Naive / Pretreatment Evidence

Only three non-TCGA studies were positively classified as `treatment_naive_or_pretreatment` by the scaffold:

| Study | Evidence tier | Local signal |
|---|---|---|
| `lung_nci_2022` | treatment-naive | negative signal: `treatment-naive` |
| `lusc_cptac_2021` | treatment-naive | negative signal: `treatment-naive` |
| `mbl_dkfz_2017` | pretreatment / untreated | negative signals: `previously untreated`; `untreated` |

This is a thin clean baseline for a treated-versus-naive contrast.
The remaining `do_not_flag` studies should be interpreted as `no_detected_treatment_signal`, not as confirmed treatment-naive controls.

## Missing Metadata

Two config studies could not be reviewed from the local raw tree:

| Study | Local status | Action |
|---|---|---|
| `aml_stjude_2024` | `/data/raw/cbioportal/aml_stjude_2024` absent | resolve raw download or mark unavailable before label freeze |
| `msk_impact_50k_2026` | `/data/raw/cbioportal/msk_impact_50k_2026` absent | resolve raw download or mark unavailable before label freeze |

Do not silently treat these as unexposed.
They are unknown for the audit.

## Interpretation

The manual review supports adding a broad treatment-exposed study stratum, but it also shows that the strongest mutagenic-treatment candidates are not identical to the 11 study-level flags.
For H10, the clean next design is a layered label:

- broad `treatment_exposed_studies` for cohort-composition sensitivity;
- a narrower study-level and sample-fraction layer for DNA-damaging therapies expected to generate SBS11/SBS31/SBS35/SBS87;
- a sensitivity-only bucket for PDX cohorts and other non-patient-denominator substrates.

This keeps `question:q024` from collapsing exposure ascertainment into signature outcomes.
It also prevents the frequency-table impact pass from overclaiming that an ICB-treated or endocrine-treated cohort is direct evidence for chemotherapy-signature contamination.

The audit recall is unmeasured.
The 109 `no_metadata_signal` studies were not individually reviewed beyond the scaffold output, and the scaffold is a keyword and clinical-column detector over local cBioPortal metadata.
A treated cohort with neutral study prose and no treatment-named clinical column could remain in the apparent control baseline.
Therefore the untreated comparator for the first H10 pass is a `no_detected_treatment_signal` baseline plus the three positively naive/pre-treatment studies, not a fully adjudicated treatment-naive baseline.

## Next Step

The next executable step is a small config/schema plan for H10 denominator handling:

- add broad confirmed study-level flags only after deciding where `config-full.yml` should carry them;
- encode `mutagenic_treatment_signal_studies` separately from the broad `treatment_exposed_studies` list;
- add fraction fields for `blca_cornell_2016`, `difg_glass_2019`, `coadread_mskcc`, and other manually adjudicated mixed cohorts;
- keep `sclc_cancercell_gardner_2017` and `pptc_2019` sensitivity-only unless PDX-specific mutation-call handling is modeled;
- report the baseline as `no_detected_treatment_signal` unless a separate negative-control review adjudicates all 109 no-signal studies;
- keep stage-only metastatic cohorts out of the primary treatment-exposed exclusion;
- then implement the paired treatment-inclusive/exclusive frequency-table impact pass, parallel to the hypermutator-inclusive/exclusive output.
