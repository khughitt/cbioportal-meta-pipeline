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
