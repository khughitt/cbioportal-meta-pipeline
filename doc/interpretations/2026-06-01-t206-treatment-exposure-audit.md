# t206 — H10 treatment-exposure audit manual review

Date: 2026-06-01

## Question

Which non-TCGA cBioPortal studies in `config-full.yml` are ready to be treated as treatment-exposed strata for `hypothesis:h10`, and which need sample-level fraction review before they can affect the frequency-table denominator?

This is a manual-review note for the metadata scaffold in `code/scripts/audit_treatment_exposed_studies.py`.
It does not estimate H10 support and does not yet change the frequency tables.

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
| `sclc_cancercell_gardner_2017` | propose broad flag | chemosensitive/chemoresistant SCLC PDX cohort | chemotherapy-resistance signal, but PDX denominator caveat |
| `skcm_mskcc_2014` | propose broad flag | pretreated ipilimumab/tremelimumab melanoma | treated cohort; ICB is not the therapy-signature endpoint |

Recommended broad config proposal, pending the config-edit step:

```yaml
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
  - sclc_cancercell_gardner_2017
  - skcm_mskcc_2014
```

For the H10 impact pass, this broad list should be paired with a narrower `mutagenic_treatment_signal` or equivalent reporting field.
The broad flag answers "could cohort composition differ by treatment history?"
The narrower field answers "should SBS11/SBS31/SBS35/SBS87 be expected a priori?"

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
| `pptc_2019` | `TX_CISPLATIN` is nonblank for 47 / 261 PDX samples | review before use; PDX and coded-count semantics are not yet resolved |

The advanced/metastatic-only studies without direct treatment columns should remain out of the primary H10 label set.
They may still be useful as a stage-enriched sensitivity, but treating metastatic status as treatment exposure would confound treatment history with disease stage.

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
For H10, the clean next design is a two-layer label:

- broad `treatment_exposed_studies` for cohort-composition sensitivity;
- a narrower therapy-class or sample-fraction layer for DNA-damaging therapies expected to generate SBS11/SBS31/SBS35/SBS87.

This keeps `question:q024` from collapsing exposure ascertainment into signature outcomes.
It also prevents the frequency-table impact pass from overclaiming that an ICB-treated or endocrine-treated cohort is direct evidence for chemotherapy-signature contamination.

## Next Step

The next executable step is a small config/schema plan for H10 denominator handling:

- add broad confirmed study-level flags only after deciding where `config-full.yml` should carry them;
- add fraction fields for `blca_cornell_2016`, `difg_glass_2019`, `coadread_mskcc`, and other manually adjudicated mixed cohorts;
- keep stage-only metastatic cohorts out of the primary treatment-exposed exclusion;
- then implement the paired treatment-inclusive/exclusive frequency-table impact pass, parallel to the hypermutator-inclusive/exclusive output.
