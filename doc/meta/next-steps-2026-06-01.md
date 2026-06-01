---
id: "meta:next-steps-2026-06-01"
type: "meta"
title: "Next Steps — 2026-06-01"
created: "2026-06-01"
updated: "2026-06-01"
prior: "meta:next-steps-2026-05-31"
related:
  [
    "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and",
    "task:t195",
    "task:t199",
    "task:t200",
    "task:t201",
    "task:t202",
    "task:t205",
    "task:t206",
    "task:t207",
    "discussion:2026-06-01-h08b-gate-handling",
  ]
---

# Next Steps — 2026-06-01

## Recent Progress

The major 2026-05-31 recommendation shipped: the h08 positive-control association scan ran, was wired into Snakemake, and produced an interpretation.
The locked H08a verdict is `[?]`: Arm C APOBEC passed strongly, while the registered UV-site and pack-years arms failed.

The follow-up t200 diagnostic probe also shipped.
It reproduced the frozen t199 baseline coefficients exactly, attributed Arm A mostly to weak UV proxy plus SBS7 saturation, attributed Arm B to a smoking operationalization problem rather than simple range restriction, and found the APOBEC pass proliferation-robust in this substrate.

Workflow provenance improved for the h08 run bundle: `results/signature-h08-arms-2026-05-31/datapackage.json` now exists.
The health check still reports validation debt, including two dataset-access verification errors introduced by the new h08 plan references.

## Current State

The h08 result is no longer "built but unrun."
The new decision is whether to repair and re-register the environmental positive-control arms, or treat H08a as inconclusive and proceed only to narrowly scoped H08b exploration.

Task state has drifted:

| Task | Current tracker state | Evidence | Suggested update |
|---|---|---|---|
| `t195` | active / proposed | `t199` completed the H08a scan and wrote `doc/interpretations/2026-05-31-t199-h08-association-verdict.md` | mark done or retire as superseded by `t199` |
| `t200` | active / proposed | commit `db24409` added diagnostics script, Snakemake rule, tests, and `doc/interpretations/2026-06-01-h08-within-tissue-diagnostics.md` | mark done, completed `2026-06-01` |

No P0 tasks are present.
The still-relevant P1/P2 work clusters are dataset acquisition (`t166`, `t169`, `t170`, `t171`), h08 follow-up (`t180`, `t181`, `t182`, `t183`), and hygiene/provenance debt (`t128`, dataset verification, graph update).

## Coverage Gaps

| Area | Coverage | Direction | Key Gap |
|---|---|---|---|
| H08a positive-control scan | Partial | improving | The scan is now executed, but only 1/3 arms passed and the failed arms are proxy-limited. |
| H08 diagnostic attribution | Strong | new | t200 explains the misses well enough to guide repair without changing the locked verdict. |
| Smoking positive control | Partial | new | Derived `ever_smoker` and zero-filled never-smoker pack-years recover SBS4 better than frozen `pack_years`, but this is not pre-registered. |
| UV positive control | Weak | stable | SKCM SBS7 is nearly saturated and the anatomic-site ordinal is too coarse for residual recovery. |
| APOBEC positive control | Strong | improving | APOBEC survives burden/proliferation controls, but BRCA remains a per-tissue caveat. |
| Task-state fidelity | Partial | regressing | `t195` and `t200` no longer reflect shipped work. |
| Dataset/access validation | Partial | regressing | `science health` now flags `dataset:tcga-mc3` and `dataset:tcga-pancanatlas` as consumed but access-unverified. |

## Strategic Decision Point

The fork is now between **repairing H08a** and **opening H08b**.

Repairing H08a would mean a new pre-registered positive-control repair, not a reinterpretation of the frozen result.
The strongest candidate is Arm B: fix production `ever_smoker`, decide whether the registered smoking proxy should be binary ever-smoker, zero-filled pack-years, or a smoking-signature-derived biomarker, then rerun only under a new amendment.
Arm A looks less attractive because the t200 non-saturated SKCM subset is only n = 9–10 across thresholds; a credible UV repair likely needs a better UV exposure substrate, not just a code fix.

Opening H08b now is tempting because APOBEC passed robustly, but the pre-registered gate did not promote H08a.
The safer path is a narrow H08b prototype framed as exploratory and explicitly not a hypothesis-promotion step.

## Recommended Next Actions

| Priority | Action | Rationale | Command |
|---|---|---|---|
| P1 | Fix task drift for `t195` and `t200` | The shipped h08 scan and diagnostic probe are still represented as active/proposed work. | `science tasks complete t200` and decide whether `t195` is done or superseded |
| P1 | File a new follow-up for the latent production `ever_smoker` bug | t200 worked around the frozen artifact; production `build_h08_covariates.py` still has the textual-label-to-numeric coercion bug. | `science tasks add` for the smoking covariate repair |
| P1 | Repair dataset verification metadata for `tcga-mc3` and `tcga-pancanatlas` | `science health` reports them as consumed by the h08 plan while `access.verified` is false. | edit `doc/datasets/tcga-mc3.md` and `doc/datasets/tcga-pancanatlas.md`, then `uv run --frozen science validate --verbose` |
| P2 | Decide whether to pre-register a smoking-arm repair | The diagnostic result supports a repairable Arm-B miss, but it must not be folded into the locked H08a read. | `science-pre-register` for an H08a smoking-repair amendment |
| P2 | Defer UV repair unless a better exposure substrate is identified | The current SKCM arm is saturated and proxy-limited; a quick rerun is unlikely to be informative. | add a low-priority task only if a better UV covariate/source is available |
| P2 | Start a tightly labeled exploratory H08b prototype | APOBEC is robust, but H08a stayed `[?]`; discovery work should remain exploratory until a repaired gate exists. | implement `t182` only with explicit exploratory framing |
| P2 | Run cross-project sync | Sync is 7 days stale and cancer-meta may carry relevant updates. | `science-sync` |

## Session Summary

The h08 program crossed from infrastructure into evidence.
The result did not promote H08a, but it also did not collapse the method: the molecular APOBEC arm behaved as intended, while the two failed environmental arms now have concrete proxy-level explanations.
The next useful move is housekeeping plus one explicit choice: repair smoking under a new pre-registration, or proceed to H08b as exploratory work with the `[?]` gate preserved.

## Update — 07:17 EDT

Three recommendations from the morning note have now shipped.

| Prior recommendation | Current status | Evidence |
|---|---|---|
| Fix task drift for `t195` and `t200` | Done | Both tasks are closed in `tasks/done/2026-06.md`; `t195` is recorded as completed by the t196–t199 work package chain, and `t200` by commit `db24409`. |
| File and handle the production `ever_smoker` bug | Done | `task:t201` was filed, completed, and merged in commit `22a87e2`; production `build_h08_covariates.py` now maps raw PanCanAtlas smoking labels explicitly and emits `pack_years_zero_never`. |
| Repair dataset verification metadata for `tcga-mc3` and `tcga-pancanatlas` | Done | The dataset notes now carry public-access verification metadata and validation no longer reports those access-verification errors. |

The remaining h08 fork is therefore narrower than it was earlier today.
The housekeeping and production bug fix are no longer blockers.
The next decision is not whether the frozen H08a verdict changes — it does not — but whether to author a new smoking-arm repair commitment before running any repaired Arm-B scan.

Recommended next move: pre-register a **H08a smoking-arm repair** as a new, forward-looking pre-registration.
It should explicitly treat the repaired analysis as non-identical to the locked 2026-05-31 H08a read, use the repaired production covariates, and decide up front whether the primary smoking proxy is `ever_smoker`, `pack_years_zero_never`, or both in a fixed primary/sensitivity order.
The t200 diagnostic supports `ever_smoker` as the primary candidate, with `pack_years_zero_never` as sensitivity; neither should be folded back into the locked `[?]` verdict.

Lower-priority items remain stable:
UV repair should stay deferred unless a better exposure substrate appears, and H08b should remain exploratory until a repaired gate or a deliberate gate-bypass decision is on record.

**Follow-through:** `task:t202` tracks and closes the smoking-arm repair pre-registration.
The repair document is `pre-registration:h08-smoking-repair`; the next executable step is a small implementation plan for the repaired Arm-B production rerun, not a broad H08b scan.

## Update — 08:12 EDT

The next executable step is now also tracked and closed.

| Prior recommendation | Current status | Evidence |
|---|---|---|
| Plan the repaired Arm-B production rerun | Done | `task:t203` wrote `doc/plans/2026-06-01-h08-smoking-repair-rerun.md`. |

The repaired rerun plan keeps the new Arm-B read separate from the locked t199 artifacts.
It defines a repair-specific output surface under `association/repairs/smoking_arm/`, derives the repaired denominator from the original manifest without overwriting it, and locks `ever_smoker` as the only primary pass route.
`pack_years_zero_never`, original `pack_years`, LUAD-only, and LUSC-only remain sensitivity/localization reads.

Recommended next move: implement `run_h08_smoking_repair.py` and the opt-in Snakemake target `all_h08_smoking_repair`, then write the repair interpretation note.
This is still a repaired positive-control read with limited epistemic weight; it does not change H08a `[?]` and does not make H08b confirmatory.

## Update — 08:44 EDT

The repaired Arm-B production rerun has now shipped as `task:t204`.

| Prior recommendation | Current status | Evidence |
|---|---|---|
| Implement the repaired smoking-arm rerun | Done | `code/scripts/run_h08_smoking_repair.py`, `all_h08_smoking_repair`, and `doc/interpretations/2026-06-01-h08-smoking-repair.md`. |

The repaired production result is informative but not a pass.
`ever_smoker` is positive and significant against SBS4 in LUAD+LUSC (n = 839, coef = +0.267, BH-q = 5.10e-04), but it ranks 5 / 8 in the repaired primary family.
Under `pre-registration:h08-smoking-repair`, the local repaired Arm-B verdict is therefore `[?]`, because the rank <= 3 criterion fails.

The strongest current read is now stable:
the frozen Arm-B miss was partly an exposure-operationalization artifact, but the repaired binary smoking proxy still does not produce a clean top-3 positive control on this substrate.
H08a remains `[?]`, and H08b remains exploratory unless a later gate-bypass decision is explicitly recorded.

## Update — 09:02 EDT

The H08b gate-handling decision is now explicit.

| Prior recommendation | Current status | Evidence |
|---|---|---|
| Decide whether H08b can proceed after the repaired smoking result | Done | `discussion:2026-06-01-h08b-gate-handling` records that no confirmatory H08b gate is open; any `task:t182` work is exploratory/prototype only. |

This is intentionally **not** a gate bypass.
The locked H08a verdict remains `[?]`, the repaired smoking-arm result remains `[?]`, and H08b cannot be used for hypothesis promotion without a future pre-registered gate that passes.

Recommended next move: if staying on H08, run only a narrow exploratory t182 feasibility prototype for SBS40/SBS5 expression-module separation, with the causal-direction guard up front.
Otherwise, shift out of H08 and address broader active-project debt: treatment-exposed cohort flags (`task:t181` / H10), the commons-validation hygiene tasks, or cross-project sync.

## Update — t182 Prototype

The narrow exploratory H08b prototype has now run.

| Prior recommendation | Current status | Evidence |
|---|---|---|
| Run only a narrow exploratory t182 feasibility prototype | Done | `doc/interpretations/2026-06-01-t182-h08b-sbs40-sbs5-prototype.md` and `code/scripts/run_h08b_sbs40_sbs5_prototype.py`. |

The result is candidate-bearing but not mechanism-bearing.
SKCM `module_04` is associated with the SBS40-vs-SBS5 contrast after age conditioning (n = 363, coef = +0.154, BH-q = 0.0348), but the secondary read suggests the contrast is driven mostly by lower SBS5 rather than a strong separate SBS40 increase.
CESC `module_02` is weaker and points toward higher SBS5 relative to SBS40.
LUAD `REV3L` is null, and `POLZ` is not evaluable from the LUAD RSEM matrix.

H08b remains exploratory and unpromoted.
The next H08-specific refinement would be formal module labeling/enrichment, but the broader project may get more value from `task:t181` treatment-exposed cohort flags because those feed H10, H09, and any future signature scan.

## Update — t181 Treatment Exposure

The treatment-exposure stratum has now landed for the H08 MC3 substrate.

| Prior recommendation | Current status | Evidence |
|---|---|---|
| Build treatment-exposed cohort flags (`task:t181`) | H08-facing piece done | `code/scripts/build_h08_covariates.py`, `code/config/config-signature-h08-arms.yml`, and `doc/interpretations/2026-06-01-t181-treatment-exposure-stratum.md`. |

The implementation separates patient-level neoadjuvant labels from study-level cohort exposure:
`treatment_exposed_clinical`, `treatment_exposed_study`, `treatment_exposed_fraction`, and combined `treatment_exposed`.
For the current MC3-only H08 substrate, `tcga_mc3` is explicitly audited as study-level unexposed (`treatment_exposed_study = 0`, `treatment_exposed_fraction = 0.0`), while 55 samples retain a patient-level neoadjuvant positive label.

This closes the H08 confound-stratum gap but does not yet test H10.
The next broader H10 step is `task:t206`: a non-TCGA cBioPortal treatment-exposed cohort audit plus a frequency-table impact pass.

## Update — t206 H10 Treatment-Exposure Audit

The first t206 slice is now planned and scaffolded.

| Prior recommendation | Current status | Evidence |
|---|---|---|
| Start the non-TCGA treatment-exposed cohort audit | In progress | `doc/plans/2026-06-01-t206-h10-treatment-exposure-audit-analysis-plan.md` and `code/scripts/audit_treatment_exposed_studies.py`. |

The audit scaffold is deliberately metadata-first.
It scans `config-full.yml` studies against local cBioPortal `meta_study.txt` and clinical-column names, skips TCGA studies, and separates `flag_exposed` from `review_for_fraction` so metastatic-only cohorts do not automatically become treatment-exposed.

The current regenerated local table has 167 non-TCGA studies: 11 `flag_exposed`, 42 `review_for_fraction`, 2 `needs_manual_review`, and 112 `do_not_flag`.
This is not yet the final H10 label set.
The next step is manual confirmation of the 11 explicit candidates and clinical-field review of the 42 review candidates before writing `treatment_exposed_studies` or building paired treatment-inclusive/exclusive frequency tables.

## Update — t206 Manual Review

The manual-review note for the scaffolded audit has now landed at `doc/interpretations/2026-06-01-t206-treatment-exposure-audit.md`.

The review confirms the 11 `flag_exposed` studies as broad treatment-exposed cohort candidates, but it separates broad treatment history from direct DNA-damaging-therapy expectation and keeps PDX cohorts sensitivity-only.
Several confirmed studies are ICB, endocrine, targeted, or castration-resistant cohorts; they are useful nuisance strata but should not be overread as expected SBS11/SBS31/SBS35/SBS87 carriers.

The stronger mutagenic-treatment candidates are partly in the mixed/fraction-review bucket:
`blca_cornell_2016` has 51 / 72 post-chemotherapy samples with platinum-containing labels, and `difg_glass_2019` has explicit TMZ fields.
`coadread_mskcc`, `coadread_cass_2020`, `brca_mbcproject_wagle_2017`, `mpcproject_broad_2021`, OHSU AML, and `brain_cptac_2020` need sample-level or fraction handling rather than whole-study promotion.
`pptc_2019` and `sclc_cancercell_gardner_2017` should stay out of the primary patient denominator unless PDX-specific mutation-call handling is modeled.

The review also names the control-arm limitation: only `lung_nci_2022`, `lusc_cptac_2021`, and `mbl_dkfz_2017` were positively classified as treatment-naive or pretreatment.
The other no-signal studies are `no_detected_treatment_signal`, not confirmed naive, so audit recall remains unmeasured.

Recommended next move: write the small config/schema plan for H10 denominator handling.
The design should keep a broad `treatment_exposed_studies` layer separate from a narrower `mutagenic_treatment_signal` study/fraction layer, then implement paired treatment-inclusive/exclusive frequency-table outputs parallel to the existing hypermutator-inclusive/exclusive columns.

## Update — t207 H10 Denominator Schema

The H10 denominator schema is now planned and split from the audit task.

| Prior recommendation | Current status | Evidence |
|---|---|---|
| Write the H10 treatment-denominator config/schema plan | Done | `doc/plans/2026-06-01-t207-h10-treatment-denominator-schema.md`. |
| Separate audit from implementation | Done | `task:t206` is closed as the audit/manual-review slice; `task:t207` is active for executable schema and impact-pass work. |

The design preserves the t206 review's central distinction:
broad treatment-exposed cohorts are a cohort-composition sensitivity, while primary H10 treatment-signature impact uses a narrower mutagenic-treatment layer.
It also keeps PDX cohorts sensitivity-only, names the comparator `no_detected_treatment_signal` rather than treatment-naive, and avoids overloading the existing `_exclusive` suffix because canonical frequency tables already use that suffix for hypermutator exclusion.

Recommended next move: implement `t207` WP1-WP2 first.
That means adding the `h10_treatment_denominator` config schema and `annotate_treatment_exposure.py` with tests before touching frequency-table aggregation.

## Update — t207 Plan Review

The t207 schema plan review landed at `doc/plans/2026-06-01-t207-h10-treatment-denominator-schema-review.md` and the blocking points have been patched into the plan.

The plan now states that this pass is the H10 exposure-label arm, not the full q027 therapy-signature-high exclusion answer.
It also defines `no_detected_treatment_signal` as the retained comparator cohort, pins raw clinical `SAMPLE_ID` joins to canonical `samples_annotated.feather`, maps H10 hypermutator companion columns back to canonical `*_inclusive` / `*_exclusive` fields, and requires a datapackage manifest for the new summary outputs.

Recommended next move is unchanged but sharper: implement WP1-WP2 only.
Do not start the frequency impact pass until the config parser and treatment sample annotation can prove the label schema, raw-clinical joins, and no-detected-signal comparator semantics on tests.

## Update — t207 Second-Order Review Fixes

The second-order issues from the t207 review response are now folded into the plan.
The impact table now uses contrast-specific power statuses rather than one ambiguous `h10_power_status`.
It also makes `mean_no_detected_treatment_signal` verdict-bearing through `delta_no_detected_contrast`, adds a `confirmed_naive_or_pretreatment` sensitivity/QA view for the three positively clean studies, and fixes status precedence so `no_contrast` wins when both no-contrast and underpowered conditions apply.

Recommended implementation order remains WP1-WP2 first.
The annotation tests should specifically prove that positive-naive samples are folded into `no_detected_treatment_signal` and also exposed through the confirmed-naive sensitivity view.

## Update — t207 Annotation Substrate

WP1-WP2 are now implemented as the executable H10 treatment-label substrate.
`code/config/config-full.yml` carries the curated `h10_treatment_denominator` schema from the t206 audit, and `code/scripts/annotate_treatment_exposure.py` produces `metadata/samples_treatment_exposure.feather` plus `metadata/samples_treatment_exposure_counts.tsv`.
The Snakemake surface is opt-in through `all_h10_treatment_annotations`, so the canonical mutation-frequency tables remain unchanged.

The tests cover the label semantics that mattered in the plan review:
primary mutagenic conflicts with positive-naive and sensitivity-only labels hard-fail; positive-naive samples are folded into `no_detected_treatment_signal`; unknown metadata is not silently treated as unexposed; sample-level raw `SAMPLE_ID` joins hard-fail on missing clinical columns or unmatched raw IDs; and the counts sidecar reports per-study label totals.

Recommended next move: implement WP3, the per-study treatment-aware frequency views.
This should consume `samples_treatment_exposure.feather`, emit a long `cohort_view` table, and keep the hypermutator companion columns explicitly named rather than overloading the existing `_exclusive` suffix.

## Update — t207 Treatment Frequency Views

WP3 is now implemented as the per-study H10 treatment-frequency substrate.

| Prior recommendation | Current status | Evidence |
|---|---|---|
| Implement WP3 per-study treatment-aware frequency views | Done | `code/scripts/create_h10_treatment_freq_tables.py`, `code/scripts/tests/test_create_h10_treatment_freq_tables.py`, and opt-in `all_h10_treatment_freq_tables`. |

The new per-study table is long on `cohort_view` and preserves the canonical hypermutator contract by naming the companion columns explicitly:
`num_hypermutator_excluded`, `n_samples_hypermutator_excluded`, and `ratio_hypermutator_excluded`.
The `all_samples` view reproduces the mapped canonical `gene_cancer_study` inclusive/exclusive columns, while the treatment views use the planned denominator semantics for `no_detected_treatment_signal`, `confirmed_naive_or_pretreatment`, broad-treatment exclusion, primary mutagenic-treatment exclusion, and PDX sensitivity exclusion.

Recommended next move: implement WP4, the cross-study H10 treatment impact table.
That pass should aggregate the per-study view tables, compute `delta_no_detected_contrast` separately from denominator-dilution deltas, and emit contrast-specific power statuses before any interpretation note is written.

## Update — t207 Treatment Impact Table

WP4 is now implemented as the cross-study H10 treatment-impact aggregation layer.

| Prior recommendation | Current status | Evidence |
|---|---|---|
| Implement WP4 cross-study treatment impact table | Done | `code/scripts/create_h10_treatment_impact_table.py`, `code/scripts/tests/test_create_h10_treatment_impact_table.py`, and opt-in `all_h10_treatment_impact`. |

The impact table keeps the plan's two effect-size questions separate.
`delta_no_detected_contrast` compares the all-sample deliverable against the retained no-detected-treatment comparator, while `delta_mutagenic_primary` measures denominator dilution after primary mutagenic-treatment exclusion.
The output also carries `delta_confirmed_naive_contrast`, broad-treatment sensitivity, within-cancer ranks, rank deltas, contrast-specific power statuses, and count/audit fields for numerator-vs-denominator changes.
The opt-in target emits both summary feathers and `gene_cancer_h10_treatment_impact.datapackage.json`.

Recommended next move: run the `all_h10_treatment_impact` target on the configured substrate and write the t207 interpretation note.
That note should keep the exposure-label pass separate from the q027 therapy-signature-high arm and should treat no-contrast or underpowered rows as a plumbing checkpoint unless deterministic sample-level mutagenic-treatment rules have been added.

## Update - t207 Full-Config Impact Run Attempt

The configured WP4 impact target was attempted against `code/config/config-full.yml`, but it did not reach H10 aggregation.
Snakemake stopped before `samples_treatment_exposure` or the impact tables because local raw cBioPortal inputs are absent for two configured studies.

| Prior recommendation | Current status | Evidence |
|---|---|---|
| Run `all_h10_treatment_impact` on the configured substrate | Blocked | `aml_stjude_2024` is missing the three canonical raw files; `msk_impact_50k_2026` is missing those plus its required panel matrix. |
| Write the t207 interpretation note | Done as substrate-readiness note | `doc/interpretations/2026-06-01-t207-h10-treatment-impact-target-blocked-by-missing-full-config-raw.md`. |

This is not a null H10 result.
No `gene_cancer_h10_treatment_impact_ratio.feather` or datapackage was produced for the full configured substrate, so the exposure-label arm remains unadjudicated and q027 remains deferred.

Recommended next move: repair or explicitly resolve the two missing raw study substrates, then rerun `all_h10_treatment_impact`.
If a temporary available-substrate run is useful for plumbing, label it as partial and do not use it as the full-config H10 impact answer.

## Update - t207 Full-Config Impact Complete

The missing raw substrates were restored locally and the configured WP4 target now completes on `code/config/config-full.yml`.

| Prior recommendation | Current status | Evidence |
|---|---|---|
| Restore missing raw studies and rerun `all_h10_treatment_impact` | Done | `/data/packages/cbioportal/full/summary/mut/table/gene_cancer_h10_treatment_impact.feather`, `gene_cancer_h10_treatment_impact_ratio.feather`, and `gene_cancer_h10_treatment_impact.datapackage.json` now exist. |
| Write the substantive t207 interpretation note | Done | `doc/interpretations/2026-06-01-t207-h10-treatment-impact-full-config.md` supersedes the missing-raw blocker note. |

The full-config output is a successful exposure-label denominator pass, not the q027 therapy-signature-high answer.
The ratio table has 776,686 gene-cancer rows.
Power remains the limiting feature: `delta_no_detected_contrast` has 92,990 interpretable rows, `delta_broad` has 60,752, `delta_mutagenic_primary` has 8,834, and `delta_confirmed_naive_contrast` has none.
The primary mutagenic contrast is almost entirely a bladder-cancer contrast because only `blca_dfarber_mskcc_2014` is in the current whole-study primary mutagenic label set.

The biological H10 claim therefore remains unresolved.
The useful result is that the H10 denominator machinery now runs on the full configured substrate, emits a manifest, and reports contrast-specific power so thin contrasts are not overread as null effects.

Recommended next move: start a follow-up that adds deterministic sample-level mutagenic-treatment rules for the mixed cohorts already identified in t206, especially `difg_glass_2019` and `blca_cornell_2016`.
The separate q027 arm should use measured SBS11/SBS31/SBS35/SBS87 exposure and should not be collapsed into the exposure-label pass.

## Update - t208 Sample-Level Mutagenic Rules

The recommended sample-level H10 follow-up has now shipped as `task:t208`.

| Prior recommendation | Current status | Evidence |
|---|---|---|
| Add deterministic sample-level rules for `difg_glass_2019` and `blca_cornell_2016` | Done | `config-full.yml` now defines `difg_glass_2019_tmz` and `blca_cornell_2016_post_chemo` under `h10_treatment_denominator.sample_level_rules`. |
| Rerun the H10 impact target with those labels | Done | `all_h10_treatment_impact` was forced from `annotate_treatment_exposure`, then the final target check reported all files up to date. |
| Write the t208 interpretation | Done | `doc/interpretations/2026-06-01-t208-h10-sample-level-mutagenic-rules.md`. |

The new rules add 230 primary mutagenic-treatment samples: 179 TMZ-positive DIFG samples and 51 post-chemotherapy BLCA Cornell samples.
Primary mutagenic signal rises from 50 to 280 samples, and `delta_mutagenic_primary` interpretable rows rise from 8,834 to 29,377.
The contrast now covers both glioma and bladder cancer instead of being effectively bladder-only.

This improves the exposure-label substrate but also surfaces a sharper schema gap.
For DIFG/GLASS, 161 samples have blank `TMZ_TREATMENT` and currently remain in `no_detected_treatment_signal`; they are unknown-not-confirmed-naive, not explicit untreated controls.
For BLCA Cornell, 21 `pre-chemotherapy` samples are clean pretreatment-at-collection comparators, but the current sample-level target vocabulary cannot mark `positive_naive_or_pretreatment`.

The biological H10 claim remains unresolved because the current pass excludes by clinical treatment labels, not by measured SBS11/SBS31/SBS35/SBS87 exposure, and because the sample-level comparator still overclaims in mixed cohorts.

Recommended next move: handle `task:t209` before q027.
Extend sample-level rules to support sample-level `treatment_metadata_unknown` and `positive_naive_or_pretreatment`, rerun the H10 impact target, and only then file the distinct q027 therapy-signature-high arm.
