---
id: "plan:2026-06-01-h08-smoking-repair-rerun"
type: "plan"
title: "h08 smoking-arm repair production rerun"
status: "active"
created: "2026-06-01"
updated: "2026-06-01"
related:
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
  - "method:h08-agnostic-association-model"
  - "pre-registration:h08-smoking-repair"
  - "plan:2026-05-31-t199-h08-association-core"
  - "plan:2026-05-31-h08-within-tissue-diagnostics"
  - "task:t199"
  - "task:t200"
  - "task:t201"
  - "task:t202"
  - "task:t203"
---

# h08 smoking-arm repair production rerun

## Goal

Run the pre-registered repaired Arm-B smoking analysis as a separate production artifact:
replace the original Arm-B smoking slot with `ever_smoker`, read the repaired SBS4 result under the fixed criteria in `pre-registration:h08-smoking-repair`, and leave the locked 2026-05-31 H08a verdict unchanged.

## Background

The original t199 H08a scan used `pack_years` as the registered Arm-B covariate and read 1/3 arms passing, so H08a remains `[?]`.
The t200 diagnostic then showed that the smoking miss was likely an operationalization artifact: the frozen `ever_smoker` column was all-missing in lung, while a derived binary ever-smoker variable recovered SBS4 in LUAD+LUSC.
Task t201 fixed production covariate assembly by mapping PanCanAtlas smoking labels explicitly and emitting `pack_years_zero_never`.
Task t202 committed a forward-looking repair pre-registration that locks `ever_smoker` as primary and `pack_years_zero_never` as sensitivity.

This plan implements only that repaired Arm-B read.
It is not a reread of the original H08a gate and does not authorize H08b as confirmatory work.

## Approach

Use a repair-specific script that consumes the production t201 covariate table and the frozen h08 exposure table, then writes outputs under `association/repairs/smoking_arm/`.
Do not change `run_h08_association_scan.py`, `h08_association_grid.feather`, or the t199 denominator manifest in place.

The repaired denominator is a derived manifest, not a replacement manifest.
It copies the original Arm-B pooled ranked covariate set, replaces `pack_years` with `ever_smoker` for the primary repaired family, and records the manifest SHA256 of the t199 denominator it was derived from.
The sensitivity family repeats the same replacement logic for `pack_years_zero_never` and original `pack_years`, but only `ever_smoker` can pass the repaired primary criterion.

The model should reuse the production CLR transform and `fit_cell` machinery from `run_h08_association_scan.py`.
That keeps the repair comparable to the t199 scan.
The output should report model-frame `n`, coefficient, sign, p-value, BH q-value, rank, denominator, and repair verdict.

## Inputs

- `results/signature-h08-arms-2026-05-31/association/h08_covariates.feather` after t201 regeneration.
- `results/signature-h08-arms-2026-05-31/association/covariate_denominator.json` as the source denominator manifest.
- `results/signature-h08-arms-2026-05-31/studies/tcga_mc3/mut/signatures/restricted_assignment_per_sample.feather` as the SBS exposure table.
- `doc/meta/pre-registration-h08-smoking-repair.md` for the fixed pass criteria.
- `code/config/config-signature-h08-arms.yml` for `out_dir`, `h08_arm_studies`, and CLR/count-floor configuration.

## Tasks

1. Add `code/scripts/run_h08_smoking_repair.py`.
   The script should:
   - load the t199 manifest read-only and compute its SHA256;
   - build the LUAD+LUSC pooled model frame using count-floor-passing samples;
   - construct the repaired primary ranked set by replacing `pack_years` with `ever_smoker`;
   - run SBS4 fits for every covariate in that repaired ranked set;
   - run fixed sensitivities for `pack_years_zero_never`, original `pack_years`, LUAD-only, and LUSC-only;
   - write `h08_smoking_repair_grid.feather`, `h08_smoking_repair_sensitivity.feather`, and `h08_smoking_repair.meta.json`.
2. Add focused unit tests in `code/scripts/tests/test_run_h08_smoking_repair.py`.
   Test the denominator replacement, the repaired primary verdict mapping, and the n < 700 override.
3. Wire an opt-in Snakemake rule `run_h08_smoking_repair` and target `all_h08_smoking_repair`.
   Keep it out of `all_h08_association` so the repaired run cannot be mistaken for the locked t199 scan.
4. Run the repaired target and write `doc/interpretations/2026-06-01-h08-smoking-repair.md`.
   The interpretation must state the repaired Arm-B verdict, compare `ever_smoker` to `pack_years_zero_never` and original `pack_years`, and repeat that H08a remains `[?]`.
5. Update the run bundle metadata if a datapackage exists for `results/signature-h08-arms-2026-05-31/`.
   Add the repaired outputs as repair resources, not as replacements for the original association grid.

## Decision Criteria

A repaired Arm-B primary pass requires all of the following, exactly as committed in `pre-registration:h08-smoking-repair`:

| Criterion | Requirement |
|---|---|
| Covariate | `ever_smoker`, derived by the t201 production label map. |
| Direction | Positive standardized coefficient against SBS4. |
| Multiplicity | BH-FDR q < 0.05 within the repaired primary scan family. |
| Rank | Rank <= 3 among the LUAD+LUSC ranked scalar covariates after replacing `pack_years` with `ever_smoker`. |
| Sample support | Production model-frame n >= 700; otherwise the repair verdict is `[?]` regardless of coefficient or q-value. |

`pack_years_zero_never`, original `pack_years`, LUAD-only, and LUSC-only are sensitivity or localization reads only.
They cannot rescue a failed `ever_smoker` primary result.

## Validation

- The repaired primary ranked set contains `ever_smoker` and does not contain `pack_years`.
- The original t199 denominator manifest is never overwritten; its SHA256 is recorded in repair metadata.
- The repaired grid's FDR family size equals the number of testable covariates in the repaired LUAD+LUSC ranked set for SBS4.
- The primary output reports model-frame n after `fit_cell` dropna and applies the n < 700 override.
- `uv run --frozen pytest code/scripts/tests/test_run_h08_smoking_repair.py` passes.
- `uv run --frozen ruff check` and `uv run --frozen ruff format --check` pass on changed Python files.
- `uv run --frozen science validate --verbose` passes with only pre-existing warnings.

## Out of Scope

- Changing the locked t199 H08a association grid, sensitivity files, or verdict note.
- Replacing or re-freezing the original `covariate_denominator.json`.
- Repairing Arm A / UV.
- Opening H08b as confirmatory.
- Introducing simultaneous multi-proxy smoking models as a primary read.

## Notes on Plan Scope

Probe-sized on purpose: this is one repaired production read of one positive-control arm, using already-fixed covariates and existing h08 machinery.
Methodological readiness is inherited from the original H08a method and the committed smoking-repair pre-registration; this plan only specifies how to run the repair without contaminating the locked H08a artifacts.
