---
type: plan
title: "within-tissue positive-control failure diagnostics (tests 1\u20134)"
status: active
created: '2026-05-31'
updated: '2026-06-28'
id: plan:0006-h08-within-tissue-diagnostics
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- method:h08-agnostic-association-model
- plan:0007-t199-h08-association-core
- task:t199
- task:t200
---

# Within-tissue positive-control failure diagnostics (tests 1–4)

Project links: this plan extends `method:h08-agnostic-association-model` and
`plan:0007-t199-h08-association-core`, with implementation work in `task:t199` and `task:t200`.

## Goal

Diagnose *why* two of the three `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and` positive-control arms (UV→SBS7 in SKCM; smoking→SBS4 in lung)
miss the within-tissue gate, separating three non-exclusive failure modes — covariate **measurement
noise**, within-tissue **range restriction**, and **fan-in / saturation** (signature has multiple
upstream causes or is compositionally saturated). Read-only on the committed t199 artifacts. **Does
not touch the locked verdict** (H08a stays `[?]`); this is the open diagnostic layer (the *why*),
not a re-read of the gate.

## Background

The t199 verdict (`doc/interpretations/2026-05-31-t199-h08-association-verdict.md`) read 1/3 → H08a
`[?]`. The framing there was "proxy directness." A stronger, partly-testable framing: the
within-tissue design has a structural perversity — you pick the tissue *because* the registered
cause is operative there, so the cause is often **near-constant within that tissue** (≈ all SKCM had
UV; ≈ all LUSC smoked heavily). A within-tissue regression can then only detect drivers of *residual*
signature variance, which are the causes that still vary (total burden, other processes) — exactly
why `is_hypermutator`/TMB outrank the registered exposures. APOBEC escapes this because APOBEC3A/B
mRNA genuinely *varies* within bladder/breast/etc. — it is not near-universal-on. The four tests
below try to attribute each arm's miss to measurement vs range vs fan-in/saturation, and stress-test
whether the one pass (APOBEC) is partly a shared-driver (proliferation) confound rather than a direct
mRNA→deamination link.

Two handles already point the way: (i) the `r1` contrast in the WP2 grid meta — Arm A is null *both*
within-tissue and unconditioned (uninformative proxy → measurement), while Arm C is large
unconditioned and survives conditioning; (ii) LUAD (10/13) out-ranks LUSC (13/13) for pack-years,
the fingerprint of range restriction (the histology with more never-smokers has more exposure
contrast).

## Approach

**Two fit paths.** Baseline reproduction uses the **frozen `fit_cell`** unchanged (imported from
`code/scripts/run_h08_association_scan.py`) — it z-scores the target covariate and wraps every
non-`treatment` adjustment in `C(...)`, i.e. it only supports a *categorical* adjustment set. Tests 3
and 4 add **continuous** controls (`tmb_nonsynonymous`, a proliferation score), which `fit_cell`
would explode into high-cardinality dummies — so a **diagnostic-only helper** `fit_diag(df, ycol,
cov, *, categorical_adjust, numeric_adjust)` is required: it standardizes both `cov` and each numeric
control, keeps `C(...)` only for genuine categoricals, does an **explicit `dropna` over every model
column** (ycol, cov, all adjustments), and reports n *after* that dropna (the frozen `fit_cell`
drops only on `[ycol, cov]`, which is fine for WP2's NaN-free categorical adjustments but would
overstate n once a missing-bearing numeric control enters). `fit_diag` also fails early on
zero-variance `cov` or zero-variance numeric controls after dropna, logging the skipped model rather
than returning an unstable coefficient. Every test still pins the CLR transform, the
count-floor-passing sample set, the per-arm strata, and the frozen denominators. Deterministic (no
permutation).

- **Test 1 — effective within-tissue contrast.** Compute contrast on the **exact fit frame**
  (count-floor-passing, covariate-complete, same strata as WP2), not the raw column. For each
  registered covariate report within-arm SD/IQR on that frame; UV is single-tissue (SKCM) → report
  ordinal-tier distribution + entropy. For pack_years (LUAD vs LUSC vs pooled) and apobec3ab_joint
  (each Arm-C tissue vs six-pooled), report a **range-restriction ratio** (within-tissue SD ÷ pooled
  SD) computed on **tissue-mean-centred** values — i.e. the within-tissue *usable* variation, because
  a raw pooled SD across six tissues mostly reflects between-tissue composition, not the contrast the
  within-tissue model can exploit. The output columns must make this distinction explicit:
  `sd_raw_fit_frame`, `iqr_raw_fit_frame`, `sd_tissue_centered_fit_frame`,
  `pooled_sd_tissue_centered_fit_frame`, and `range_restriction_ratio_tissue_centered`. *Readout:*
  compressed effective contrast (low ratio / low entropy) → no method, however well-measured,
  recovers a dose-response → range restriction, not method failure. Predict APOBEC wide, LUSC
  pack-years and UV-site compressed.

- **Test 2 — binary smoking vs continuous pack-years → SBS4.** **Artifact gap (verified):**
  `ever_smoker` in `h08_covariates.feather` is **all-missing for LUAD/LUSC** (0/993) — `_to_num()` was
  applied to the textual `tobacco_smoking_history` labels in `build_h08_covariates.py`, so they
  became NaN. The diagnostic therefore **derives smoking from the raw PanCanAtlas string labels**, and
  compares three operationalizations against SBS4-CLR in ARM_B_POOLED / LUAD / LUSC:
  (i) frozen `pack_years`; (ii) `pack_years_zero_never` — `pack_years` with lifelong non-smokers set
  to 0 (most never-smokers have *missing* pack-years, not 0, so the frozen continuous variable
  silently drops them and confounds the binary-vs-continuous comparison); (iii) derived `ever_smoker`
  (string map: `Lifelong Non-smoker`→0; the four `Current …`/`Current reformed …` variants→1;
  `[Not Available]`/`[Unknown]`/`[Discrepancy]`/NaN→missing). *Readout:* binary out-ranking the
  continuous indicates a **thresholded, not linear** dose-response (a "model too simple" /
  mis-specification result). Expect `ever_smoker` strongest in LUAD (never-smokers give it contrast),
  near-dead in LUSC — corroborating Test 1.

- **Test 3 — burden-mediated / proximal conditioning diagnostic.** For each arm's registered
  covariate→signature, add `tmb_nonsynonymous` (+ `is_hypermutator`) as **numeric** controls via
  `fit_diag` and report the registered covariate's partial coefficient vs its marginal coefficient;
  log the model condition number and the pairwise correlation matrix among the registered covariate,
  `tmb_nonsynonymous`, and `is_hypermutator`, then refit on the non-saturated subset (exclude
  `is_hypermutator`; for SKCM also restrict below a **pre-registered-here SBS7-fraction threshold of
  0.90** — fixed *before* running, with a reported sensitivity sweep over {0.80, 0.85, 0.90, 0.95}).
  *Caveat (carried into the readout):* TMB and `is_hypermutator` are target-proximal — plausibly
  *downstream* of the same mutational process — so conditioning on them can remove the signal **by
  construction**. This test therefore measures **burden-mediated / proximal dominance**, not clean
  measurement-vs-saturation separation; a covariate that goes to ≈ 0 under burden conditioning is
  *consistent with* saturation/fan-in but does not by itself rule out a noisy-but-real proxy. Read it
  alongside Tests 1–2, not as a standalone verdict.

- **Test 4 — proliferation-robustness of the APOBEC pass.** Tests whether the APOBEC pass is partly a
  shared proliferation driver (APOBEC3 expression tracks cell-cycle), i.e. whether "directness" is
  partly illusory. **Design wrinkle surfaced in planning:** the existing NMF modules are built on the
  top-2000 MAD genes and canonical proliferation markers are essentially absent from that universe
  (0/18 in 5 of 6 Arm-C tissues) — so an existing module *cannot* be labelled "proliferation" by
  marker lookup. Instead compute a per-sample proliferation score from the **full per-study RSEM
  matrix** (resolved via `data_dir / h08_arm_studies[arm] / "data_mrna_seq_v2_rsem.txt"` from the run
  config — *not* a literal path): z-scored mean log2(RSEM+1) over a **published proliferation
  signature as primary** (Venet meta-PCNA), with the short canonical cell-cycle marker set
  (MKI67, PCNA, TOP2A, CCNB1/2, BUB1, CDK1, AURKA, FOXM1, …) as a **sensitivity** to reduce
  hand-picked-marker fragility. The exact primary and sensitivity gene lists must be embedded as
  constants in `diagnose_h08_within_tissue.py` or loaded from a stable project file under `data/`;
  the script must log those lists verbatim in the meta sidecar, plus the realized per-tissue gene
  intersection and the per-tissue score variance. Then refit apobec3ab_joint→SBS2_13 **per Arm-C
  tissue** (scores are per-tissue and non-commensurable across the six — the same constraint that kept
  modules out of the Arm-C denominator), controlling for the proliferation score via `fit_diag`, and
  compare the APOBEC coefficient before/after. *Readout:* coefficient shrinkage binned **< 25% /
  25–50% / > 50%**, weighted by per-tissue n; large shrinkage → proliferation-mediated; small
  shrinkage → **proliferation-robust in this substrate**.

## Inputs

- `results/signature-h08-arms-2026-05-31/association/h08_covariates.feather` — frozen covariates
  (`pack_years`, `apobec3ab_joint`, `uv_sun_exposure_ordinal`, `tmb_nonsynonymous`,
  `is_hypermutator`, `module_01..10`). **Note:** the `ever_smoker` column here is unusable
  (all-missing in lung); Test 2 re-derives smoking from the raw table below.
- `data/pancanatlas_clinical_with_followup.tsv` — raw `tobacco_smoking_history` string labels +
  `number_pack_years_smoked`, keyed on `bcr_patient_barcode` (Test 2 smoking derivation).
- `.../association/covariate_denominator.json` + `.../h08_association_grid.feather` + `.meta.json`
  — frozen denominators, the WP2 ranks (baseline to compare against), and the `r1` contrast.
- `.../studies/tcga_mc3/mut/signatures/restricted_assignment_per_sample.feather` — per-sample SBS
  exposures + `passes_count_floor`.
- Full per-study RSEM (Test 4 only), resolved via `data_dir / h08_arm_studies[arm] /
  "data_mrna_seq_v2_rsem.txt"` from the run config — the proliferation-score substrate.
- Reused code: `run_h08_association_scan.py` (`fit_cell` for baseline only, `_collapse`, CLR
  transform, `TARGETS`, `ARM_B_STRATA`, `ARM_C_STRATA`, adjustment sets). New diagnostic-only
  `fit_diag` (explicit `categorical_adjust` / `numeric_adjust`, all-column dropna) lives in the
  diagnostic script.

## Tasks

1. Write `code/scripts/diagnose_h08_within_tissue.py` (click `--config`): import the frozen
   `fit_cell` (baseline only) + CLR machinery; add the `fit_diag` numeric-adjust helper and the
   smoking-label derivation (string map + `pack_years_zero_never`); embed or load the exact
   proliferation gene sets from a stable project file; one function per test; emit a tidy
   `diagnostics/*.feather` per test + a `*.meta.json` (logging the smoking map, the SBS7 threshold +
   sweep, Test 3 condition/correlation diagnostics, and the proliferation gene sets + realized
   per-tissue intersection/variance).
2. Run tests 1–3 (covariate table + raw smoking labels) and confirm each test's baseline fit
   (frozen `fit_cell`, no extra control) reproduces the WP2 coefficient/sign for the registered
   covariate (apples-to-apples guard), with n matching the WP4 §1b fit n's.
3. Run test 4 (adds the config-resolved RSEM proliferation score; per Arm-C tissue).
4. Write `doc/interpretations/2026-06-01-h08-within-tissue-diagnostics.md` — per-arm failure-mode
   attribution (measurement / range restriction / burden-mediated dominance, hedged per Test 3) +
   the APOBEC proliferation-robustness result (shrinkage bins, n-weighted); cross-link the t199
   verdict note and restate that the locked `[?]` is unchanged.
5. (Optional) wire a `diagnose_h08_within_tissue` rule + add to the run bundle; commit.

## Decision criteria

- **Per failing arm (A, B):** assign a *most-consistent* failure mode from the joint pattern (no
  single test is decisive): low effective contrast (Test 1) + null marginal under burden-mediated
  conditioning (Test 3) → range restriction / saturation; informative contrast (Test 1) but null
  even for the binary (Test 2) → measurement noise; binary ≫ continuous (Test 2) → thresholded
  dose-response (linearity mis-specification). Report the attribution as weighted evidence, not a
  proof.
- **APOBEC (C):** summarize proliferation-robustness by the n-weighted shrinkage distribution across
  the six tissues (< 25% / 25–50% / > 50% bins). Predominantly small shrinkage → the pass is
  **proliferation-robust in this substrate** (directness not explained away by a shared cell-cycle
  driver); predominantly large shrinkage → re-describe the pass as substantially
  proliferation-mediated. Either way the locked H08a `[?]` is unchanged.

## Validation

- Each test's baseline fit (frozen `fit_cell`, no extra control) reproduces the WP2 grid
  coefficient/sign for the registered covariate (≤ rounding) — proves the diagnostic shares the
  frozen basis; `fit_diag` with empty `numeric_adjust` must match `fit_cell` on the same frame.
- Per-arm baseline n's match the WP4 §1b fit n's (370 / 703 / 1,883) before any subsetting; every
  `fit_diag` call reports n *after* an all-model-column dropna (so numeric-control missingness can't
  silently overstate n).
- Test 2: log the realized smoking-label map counts (n per label → 0/1/missing) so the
  binary/continuous comparison is auditable; confirm `ever_smoker` is derived, not read from the
  unusable frozen column.
- Test 3: the SBS7 saturation threshold (0.90) is fixed in the script before the run, with the
  {0.80–0.95} sensitivity sweep reported; log the condition number and pairwise covariate/control
  correlations for each burden-conditioned fit so unstable partial coefficients are interpretable.
- Test 4: log the exact primary + sensitivity proliferation gene sets verbatim, plus realized
  per-tissue intersection size and score variance (loud if a tissue retains < ~8 genes or near-zero
  score variance — score unreliable there).
- `fit_diag`: fail early and log a skipped cell when the target covariate or any numeric control has
  zero variance after the all-column dropna.
- Deterministic: no seeds needed; re-running is bit-stable.

## Out of scope

- Re-reading or relitigating the H08a verdict (locked `[?]`).
- External / primary-tumour cohorts, smoking biomarkers, better UV dosimetry — the "repair the
  proxies" follow-up that needs data this substrate lacks.
- De-novo signature extraction; any change to the frozen denominators, CLR rule, or adjustment sets.
- **Rebuilding / re-freezing `h08_covariates.feather`.** The diagnostic derives smoking from the raw
  table rather than perturbing the frozen artifact. The broken `ever_smoker` derivation in
  `build_h08_covariates.py` (`_to_num()` on string labels) is a real latent bug but fixing the
  production script + re-freezing is a separate follow-up task, not part of this read-only probe.
- Between-tissue (pooled-across-cancers) re-estimation as a primary read — the `r1` contrast already
  in the grid meta is the only cross-tissue handle used here.

## Notes on plan scope

Probe-sized on purpose: it is a read-only, deterministic battery over already-committed artifacts
(Test 4 additionally reads on-disk RSEM), reusing the frozen fit machinery — a day's work whose
product is one diagnostic note, not a new pipeline. Methodological readiness is inherited from
`plan:0005-h08-positive-control-scan-analysis-plan` (same model, same data, conditioning variations); no fresh
analysis-readiness pass is warranted because nothing here is confirmatory.
