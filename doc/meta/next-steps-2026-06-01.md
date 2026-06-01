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
