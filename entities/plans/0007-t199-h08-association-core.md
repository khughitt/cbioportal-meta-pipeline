---
type: plan
title: "Within-tissue covariate\u2194H association core (H08a scan)"
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: plan:0007-t199-h08-association-core
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- method:h08-agnostic-association-model
- pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature
- question:0025-causal-direction-guard-for-expression-signature
- task:t199
- task:t180
- task:t181
- task:t195
- dataset:tcga-mc3
- dataset:tcga-pancanatlas
---

# Within-tissue covariate↔H association core (H08a scan)

> **Pre-registration-already-exists mode.** Every verdict-bearing criterion — the three
> confirmatory arms, top-3 rank / positive sign / q<0.05, the 2-of-3 gate, the frozen Arm-C
> tissue set + pooled-rank rule, COSMIC v3.4, the active-signature ≥5% rule, the compositional
> + permutation pre-acceptance checks, and the `[+]/[?]/[-]` mapping onto H08a — is **locked**
> in `pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature` (committed 2026-05-30, amendment-001 2026-05-31).
> This plan **does not re-derive any of them.** It covers only the execution gates the pre-reg
> left to implementation: covariate provenance, the join materialization, covariate construction
> (where it is a researcher degree-of-freedom that must be frozen *before* ranks), the leakage
> guard, the compositional/permutation precision checks, and the §1b activation-table fill. Any
> belief that a locked criterion is wrong is an **amendment** question
> (`statistics-prereg-amendment-vs-fresh`), routed there — not re-planned here.

## Purpose

Build the H08a positive-control scan: the within-tissue association between each candidate
covariate and each per-sample COSMIC signature exposure `H`, over the 7 MC3 arm strata, reading
the committed 2-of-3 rank gate. This is the last of the four `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and` run-blocking checks
(`plan:0005-h08-positive-control-scan-analysis-plan` check 4); checks 1–3 (`question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross` / t197 refit / t198 NMF
modules) are done. No association-layer script exists today — the pre-reg's own "binding
constraint."

**Guiding principle:** the grid is **one statistical family** (a single BH-FDR denominator over
covariate × active-signature × stratum). The covariate universe and active-signature set that
*fix that denominator* must be frozen and written to disk **before any rank is computed** — the
top-3 threshold is meaningless otherwise (pre-reg §Metric Selection Rationale). The orchestration
is shaped around that ordering, and around a strict leakage firewall already established upstream
(t198 NMF never saw `H`).

## Scope decomposition

**In scope (this plan / t199):**
- Acquire the one missing public covariate source (PanCanAtlas smoking) and assemble the full
  covariate table joined to the t197 exposures `H` and t198 module loadings.
- The association scan, the frozen-denominator manifest, the leakage guard, the permutation null,
  the compositional-basis re-run, and the K±5 / lung-pooling / frozen-APOBEC sensitivity variants.
- The §1b activation-table fill, the H08a verdict read, and the run `datapackage.json`.

**Out of scope (deferred, with reason):**
- **H08b discovery scan** — gated behind a passing H08a verdict; separate pre-registration
  (pre-reg §Null Result Plan).
- **The EHR-covariate track** (GENIE BPC / MSK-CHORD) — gated data, separate registration; also
  excluded by the standing no-gated-access constraint.
- **t180 MMR-omikli co-predictor and assay-stratification** — exploratory; MC3 is single-assay
  (all WES), so assay stratification is moot here. The confirmatory Arm-C covariate is the joint
  APOBEC3A/B score only; MMR-omikli enters the exploratory grid, not the gate.
- **Full `annotate_hypermutators` composite** for tcga_mc3 — see Key Decision 2; molecular
  covariates are sourced directly rather than by running that heavier pipeline.

## Architecture

```
code/
  scripts/
    fetch_pancanatlas_clinical.py          NEW   WP0 — download public PanCanAtlas clinical-with-followup (smoking)
    build_h08_covariates.py                NEW   WP1 — assemble + freeze covariate table & denominator manifest
    run_h08_association_scan.py            NEW   WP2/3 — CLR transform, within-tissue grid, FDR, leakage guard,
                                                  permutation null, compositional + K±5 + lung sensitivity re-runs
    detect_polymerase_hotspots.py          UNCHANGED   reused for POLE/POLD1 covariate (already exists)
    write_datapackage.py                   UNCHANGED   reused for run datapackage
    build_expression_nmf_modules.py        UNCHANGED   t198 — produces module loadings consumed here
    run_restricted_sigprofiler_assignment.py UNCHANGED t197 — produces H exposures consumed here
  workflows/
    Snakefile                              MODIFY  WP5 — add 3 rules + all_h08_association target (after line ~1116)
  config/
    config-signature-h08-arms.yml          MODIFY  WP5 — add covariate-source + scan params (frozen seeds, thresholds)
data/
    pancanatlas_clinical_with_followup.tsv NEW   WP0 — public GDC PanCanAtlas clinical (smoking); gitignored if large
results/signature-h08-arms-2026-05-31/
    association/
      h08_covariates.feather               NEW   WP1 — per-sample covariate table (frozen, pre-association)
      covariate_denominator.json           NEW   WP1 — frozen covariate universe + per-stratum counts (pre-association)
      h08_association_grid.feather          NEW   WP2 — effect, sign, rank, BH-q per (covariate,signature,stratum)
      h08_permutation_null.feather           NEW   WP3 — within-stratum permutation ranks for flagged cells
      h08_sensitivity.feather               NEW   WP3 — K±5 / lung-pooling / absolute-burden re-run ranks
      h08_section1b_activation.feather       NEW   WP4 — filled post-join n / completeness / base-rate table
      h08_verdict.json                       NEW   WP4 — arm A/B/C pass + 2-of-3 → H08a [+]/[?]/[-]
    datapackage.json                       MODIFY  WP4 — add association resources + task t199
doc/interpretations/
    2026-05-31-t199-h08-association-verdict.md NEW WP4 — verdict + §1b table + provenance note
```

## Key decisions

### Key decision 1: one association script driving the full grid, wired as ≤3 Snakemake rules
- **Chosen approach:** a single `run_h08_association_scan.py` computes the entire
  covariate×signature×stratum grid in one process (covariate freeze → CLR → per-cell within-tissue
  model → one BH-FDR pass → ranks → leakage/permutation/sensitivity), wired as a small number of
  coarse Snakemake rules (covariate-build, scan, datapackage).
- **Rejected alternative:** fine-grained per-arm or per-covariate Snakemake rules.
- **Reason:** the BH-FDR family and the frozen denominator are global; fragmenting the grid across
  rules would split the family and make the "freeze denominator before any rank" ordering
  un-enforceable across rule boundaries.

### Key decision 2: source molecular covariates directly, not via the full hypermutator composite
- **Chosen approach:** TMB from the t197 exposure table (`total_mutations` / `total_sbs_count`,
  already per-sample) and per-study clinical `TMB_NONSYNONYMOUS`; MSI from clinical
  `MSI_SENSOR_SCORE` / `MSI_SCORE_MANTIS`; POLE/POLD1 hotspot from the existing
  `detect_polymerase_hotspots.py` on the MC3 MAF; a hypermutator flag from a documented TMB
  threshold (Campbell et al. [@Campbell2017Hypermutation] ≥10 mut/Mb, the absolute view already defined in the pipeline).
- **Rejected alternative:** run `annotate_hypermutators` (the canonical composite) for the
  tcga_mc3 `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and` config to emit `samples_annotated.feather`.
- **Reason:** the composite pulls in MSI normalization, per-cancer GMM, and panel-callable-size
  machinery that targets the cross-study aggregation pipeline; for 7 WES strata it is
  disproportionate, and the four molecular covariates are individually available with clearer
  provenance. The composite remains the right path **if this association scan becomes recurring** (then wire per
  t175) — recorded as the recurring-path alternative, not built now.

### Key decision 3: smoking covariate from the GDC open-access PanCanAtlas clinical-with-followup file
- **Chosen approach:** download `clinical_PANCAN_patient_with_followup.tsv` directly from the
  **GDC open-access data endpoint** —
  `https://api.gdc.cancer.gov/data/0fc78496-818b-4896-bd83-52db1f533c5c` (file UUID
  `0fc78496-818b-4896-bd83-52db1f533c5c`, ~18,633,685 bytes) — and join `tobacco_smoking_history`
  + `number_pack_years_smoked` on the 12-char TCGA patient barcode.
- **Rejected alternatives:** (a) the per-study cBioPortal PanCanAtlas clinical already on disk
  (smoking field absent); (b) GDC BCR Biotab per-tumor clinical / the GerkeLab GitHub mirror
  (kept as fallbacks only).
- **Reason:** **both facts verified during plan review (2026-05-31).** The cBioPortal LUAD/LUSC
  `data_clinical_patient.txt` carries no smoking/pack-years field (only stage/sex/race/ancestry/
  survival) — the covariate the pre-reg names for Arm B is *only* in the clinical-with-followup
  file. That file is served **open-access, no authentication** from the GDC `/data` endpoint
  (a `curl` range request returned the TSV header with `tobacco_smoking_history` at column 78 and
  `number_pack_years_smoked` at column 79; 232 columns, pan-cancer). It is therefore **ungated**
  and consistent with the standing no-gated-access constraint — an *un-built*, not *inaccessible*,
  input. (An earlier review draft mis-stated this as Synapse-gated; the GDC `/files` *metadata*
  index does not carry this legacy supplement object, but the `/data` *download* route does serve
  it without auth — corrected.) Data-access gate: PASS (origin external, open-access; verify on
  download per WP0). Fallbacks (BCR Biotab / GerkeLab mirror) are used **only** if the GDC direct
  file becomes unavailable.

### Key decision 4: UV proxy = frozen sun-exposure ordinal from `TUMOR_TISSUE_SITE`, with sample-type carried
- **Chosen approach:** map SKCM `TUMOR_TISSUE_SITE` body-site labels to a **frozen** sun-exposure
  ordinal (high: Head and Neck / Extremities / Regional Cutaneous-Subcutaneous; intermediate:
  Trunk; low/unknown: Regional Lymph Node / Distant Metastasis without a cutaneous component),
  and carry `SAMPLE_TYPE` (Primary vs Metastasis) as a covariate. The mapping table is written
  into `covariate_denominator.json` **before** any rank.
- **Rejected alternative:** a binary sun-exposed/not flag.
- **Reason:** the on-disk labels are pipe-delimited multi-site and the cohort is **82% metastatic**
  (367 Met / 81 Primary) — exactly the pre-reg's stated unknown ("coarse anatomic-site
  granularity"; "metastatic dilution"). A binary collapse discards resolvable structure and bakes
  in an arbitrary cut. The pre-reg names "sun-exposed anatomic site" as *the* proxy and lists its
  coarseness as a Known Limitation, so operationalizing the ordinal is implementation, not a
  criterion change — but because the mapping is a researcher degree-of-freedom it is **frozen and
  written before ranks** (same firewall discipline as the K-selection).

### Key decision 5: CLR primary, absolute-burden as the registered sensitivity basis
- **Chosen approach:** model the centered-log-ratio (CLR) transform of per-sample exposures `H`
  as the primary outcome; re-run the arm contrasts on absolute per-signature burden as the
  pre-acceptance compositional-basis check. Zero handling is frozen: **structural zeros**
  (signatures below the ≥5% active-signature threshold for a stratum) are excluded from that
  stratum's composition entirely; **sampling zeros** (active signature, zero in a sample) take a
  frozen pseudocount (0.5, matching `signature_ratio_pseudocount`).
- **Rejected alternative:** ILR, or modeling closed proportions directly.
- **Reason:** the pre-reg mandates "absolute per-signature burden **or** a CLR/ILR transform, not
  closed proportions." CLR is symmetric and keeps a per-signature coordinate so the rank readout
  is interpretable per signature; ILR forces an arbitrary basis that obscures the per-signature
  rank. Modeling closed proportions is the artifact the pre-reg's suspicious-result plan warns
  against. Distinguishing structural from sampling zeros is the documented numerical-precision
  gate, not a criterion.

### Key decision 6: APOBEC3-locus leakage guard as an explicit exclusion + sensitivity re-run
- **Chosen approach:** (a) confirm no SBS2/13-attributed variant used in the refit falls within
  the APOBEC3 gene cluster (chr22q13, APOBEC3A–H) that also drives the mRNA proxy; (b) flag
  samples carrying an APOBEC3-locus coding mutation and re-run Arm C without them, requiring the
  rank to survive.
- **Rejected alternative:** trust that mRNA and SBS2/13 are independent measurements.
- **Reason:** the pre-reg explicitly names the leakage mode (a locus event that both inflates
  APOBEC3 mRNA and is itself an SBS2/13 call) and requires a guard so the covariate and outcome
  are not two reads of one event.

## Work packages

### WP0 — acquire the PanCanAtlas smoking covariate (hard data-access gate, sequenced first)
- **Depends on:** nothing. **Sequenced first and treated as blocking** — see the F3 coupling below.
- **Entry point:** `code/scripts/fetch_pancanatlas_clinical.py` →
  `data/pancanatlas_clinical_with_followup.tsv` (downloads the GDC `/data` UUID from KD3).
- **Verification (all required before WP1 may consume the file; fail loudly, do not proceed on a
  partial download — the PDF-acquisition-verify discipline):**
  1. **stat** the downloaded file and assert size ≈ **18,633,685 bytes** (not an HTTP-200 stub).
  2. **md5** the file and check it against the GDC-published checksum for the UUID (record the
     value in the log; do not invent one).
  3. confirm `tobacco_smoking_history` + `number_pack_years_smoked` columns are present.
  4. confirm **LUAD + LUSC** rows are present and report per-histology non-missingness of
     `number_pack_years_smoked` / `tobacco_smoking_history` (this is the realized Arm-B covariate
     completeness — feeds the §1b table; loud if either histology is largely missing).
- **F3 coupling (identifiability).** Arm B is the only arm with a reasonably direct covariate; if
  smoking cannot be obtained, the 2-of-3 gate degenerates to "A **and** C must both pass," pinning a
  `[+]` on the by-design weakest arm. So a WP0 failure is a **`not-runnable` escalation**, never a
  silent drop to a two-arm gate. Fallback order on unavailability: GDC BCR Biotab per-tumor clinical
  → GerkeLab mirror (both ungated); only then escalate.
- **Definition of done:** file present + all four verifications logged; a
  `dataset:tcga-pancanatlas-clinical` entity recorded via `/science:find-datasets` with
  `access.verified: true`, `verification_method`, `source_url`, and a `consumed_by` backlink to
  this plan entity.

### WP1 — assemble & freeze the covariate table + denominator (pre-association)
- **Depends on:** WP0; t197 exposures; t198 module loadings; per-study cBioPortal clinical (on disk).
- **Entry point:** `code/scripts/build_h08_covariates.py`.
- **Builds, per sample (15-char barcode join to `H`; 12-char patient join for smoking/ancestry):**
  clinical (age, sex, race/`GENETIC_ANCESTRY_LABEL`, stage, MSI, primary_site, oncotree_code),
  the frozen UV ordinal + `SAMPLE_TYPE` (KD4), smoking pack-years/history (WP0), joint APOBEC3A/B
  score from the t198 RSEM matrices (t180 confirmatory covariate; log2(RSEM+1) sum, with A3A/A3B
  also retained separately for exploratory use), molecular TMB/hypermutator/POLE/MSI (KD2),
  treatment-exposed flag from `HISTORY_NEOADJUVANT_TRTYN`/`PRIOR_DX`/`RADIATION_THERAPY` (t181 —
  expected near-vacuous on MC3 treatment-naive primaries; logged as such), and the K expression
  modules.
- **Join discipline (F7).** The exposure key is the **28-char MC3 aliquot**
  (`TCGA-..-....-01A-..-..-..`); modules + clinical use the **15-char** sample barcode. Slice the
  exposure key to 15 char (sample-type code 01/06 retained, so the join aligns to the *actual
  MC3-sequenced* sample — critical for SKCM, 82% metastatic). Assert **one MC3 sample per case**
  after the collapse and **fail loudly** if any case retains >1 sample, for **all 7 arms** (SKCM
  verified 1:1 at review: 466 rows = 466 b15 = 466 cases). Smoking + ancestry join on the 12-char
  patient barcode.
- **Arm-C module-commensurability rule (F1, frozen before ranks).** The K NMF modules are an
  **independent per-tissue basis with arm-specific K** (six arms K=5, BRCA K=10); `module_01` in
  SKCM is not `module_01` in LUAD. They are therefore **well-defined covariates only within a single
  tissue.** Frozen rule: in the **pooled Arm-C model**, expression modules enter only as
  **tissue-nested nuisance terms and are excluded from the ranked covariate denominator**; the
  Arm-C ranked set is the **commensurable** covariates (clinical + molecular + the joint APOBEC3A/B
  expression score). Consequence — **two distinct denominators**: the per-tissue arms (A/B, modules
  included) and the pooled Arm C (modules excluded). Both are written to
  `covariate_denominator.json` before any rank. Per-tissue Arm-C runs that *do* carry their tissue's
  modules remain **sensitivity-only, never a pass route** (pre-reg rule). This is a run-time
  denominator rule the pre-reg delegated — **not an amendment** — but it is verdict-bearing, so the
  reasoning is recorded in the verdict note.
- **Per-arm adjustment realization (F10).** The adjustment set {tissue, treatment, study/assay,
  ancestry} is realized **per arm with constant columns dropped**: Arm A (single SKCM tissue, single
  MC3 study) collapses to {ancestry, treatment, sample_type}; tissue + study/assay are constant.
  This avoids rank-deficient design matrices and is mechanical, not a criterion change.
- **Definition of done:** `h08_covariates.feather` written; `covariate_denominator.json` written
  with the frozen covariate universe, the frozen UV-ordinal mapping table, the per-stratum
  active-signature set (≥5% rule, COSMIC v3.4), the **two denominators** (per-tissue / pooled-C),
  **the frozen rank-statistic definition (F4, see WP2)**, and the realized per-stratum
  covariate/signature counts — **before** any association is run. Leakage firewall preserved (no
  covariate is a function of `H`). Loud missingness for any covariate with low completeness (no
  silent fill).

### WP2 — the within-tissue association grid
- **Depends on:** WP1.
- **Entry point:** `run_h08_association_scan.py` (grid stage).
- **Frozen rank statistic (F4).** For each (covariate, active-signature, stratum) cell, fit **one
  adjusted within-tissue model** with the **CLR coordinate of the target signature** as the outcome
  and {covariate of interest + realized adjustment set (F10)} as predictors. The **ranking statistic
  is the signed standardized coefficient** of the covariate of interest (magnitude = |standardized
  β| / Wald |z|; **sign read directly** from β); the cell's BH-q is from that covariate's p-value.
  One model per covariate (not a single all-covariate multivariable fit) so the rank is interpretable
  and not distorted by inter-covariate collinearity. This estimator is frozen in
  `covariate_denominator.json` (WP1) before any rank.
- **CLR sign reading (F5).** The confirmatory "positive sign" is read on the CLR coordinate, which
  is *relative* to the per-sample geometric mean of active signatures — usually concordant with
  "more of the signature" but not guaranteed. It is **corroborated by the absolute-burden
  sensitivity re-run** (WP3, KD5); a CLR-vs-absolute **sign discordance downgrades that arm to
  `[?]`**.
- **Does:** CLR transform of `H` (KD5); the per-cell frozen-statistic model above; **Arm C as a
  single pooled within-tissue model** across {BLCA,BRCA,CESC,HNSC,LUAD,LUSC} yielding one APOBEC3A/B
  rank against the modules-excluded Arm-C denominator (F1); one BH-FDR pass over the full grid;
  effect, signed-standardized β, rank, q per cell; the unconditioned (tissue-pooled) contrast
  computed alongside for the R1 exploratory readout (Prediction 4). APOBEC3-locus leakage guard
  applied (KD6).
- **Definition of done:** `h08_association_grid.feather` with per-cell rank + sign + q and the
  per-stratum covariate-count denominators echoed from WP1; arm A/B/C target cells identified;
  the realized FDR family size logged.

### WP3 — pre-acceptance + registered sensitivity variants
- **Depends on:** WP2.
- **Entry point:** `run_h08_association_scan.py` (validation stage).
- **Reproducibility (F8).** Permutation null uses a frozen `h08_permutation_seed` (derived from
  `random_seed`) and a fixed **n_permutations = 1000**; the association model library
  (**statsmodels**) is pinned via `uv.lock`. Seed, permutation count, and library versions are
  recorded in the datapackage.
- **Does:** within-stratum **permutation null** (shuffle covariate within tissue, frozen seed,
  refit the association — not the signatures — confirm observed rank exceeds the null) for any arm
  cell landing rank-1 / q≈0; the **absolute-burden compositional re-run** (KD5); **K±5** module
  re-run (a verdict that flips → arm downgraded to `[?]`); **lung pooling** variant (LUAD+LUSC vs
  per-histology) for Arm B; the **frozen APOBEC tissue set** (six only; no expansion). All are
  implement-don't-invent — pre-committed in the pre-reg.
- **Definition of done:** `h08_permutation_null.feather` + `h08_sensitivity.feather`; each arm
  annotated with whether it survives permutation and whether it is stable under K±5 / lung pooling.

### WP4 — §1b activation fill, verdict read, datapackage, interpretation
- **Depends on:** WP1 (n / completeness), WP2 (ranks), WP3 (stability).
- **Entry point:** scan finalize stage + `write_datapackage.py` + interpretation note.
- **§1b column typing (F9).** "Base rate" is reported **per covariate type**: prevalence for binary
  covariates (treatment flag, hypermutator, MSI-H); completeness + a distribution summary
  (median/IQR, % non-zero) for continuous covariates (pack-years, APOBEC3A/B mRNA, UV ordinal).
- **Does:** fill the §1b table (post-join n, covariate completeness, per-type base rate per arm) —
  **the gate is not read until this is filled**; then read each arm (rank≤3, positive, q<0.05) and the
  2-of-3 gate → H08a `[+]`/`[?]`/`[-]`; report the frozen covariate-count denominator alongside
  each verdict; secondary controls (MMR/MSI→SBS6/15/26, POLE→SBS10) as corroboration only;
  emit/extend `datapackage.json` with the association resources + task t199; write the
  interpretation note (light-header convention, per the t197/t198 notes, to avoid graph-ref
  breakage).
- **Definition of done:** `h08_section1b_activation.feather`, `h08_verdict.json`, updated
  datapackage, and `doc/interpretations/2026-05-31-t199-h08-association-verdict.md` committed;
  `science validate` clean.

### WP5 — Snakemake wiring + config
- **Depends on:** WP1–WP4 scripts settled.
- **Entry point:** `code/workflows/Snakefile` (after line ~1116, following `all_h08_expression_modules`)
  + `config-signature-h08-arms.yml`.
- **Does:** add `fetch_pancanatlas_clinical`, `build_h08_covariates`, `run_h08_association_scan`
  rules + an `all_h08_association` aggregate target; add config params (smoking source path, frozen
  permutation seed, UV-ordinal mapping reference, CLR pseudocount = `signature_ratio_pseudocount`,
  hypermutator TMB threshold, APOBEC3-locus coordinates).
- **Definition of done:** `snakemake --lint` clean; a dry-run (`-n`) over `all_h08_association`
  fires exactly the new rules and resolves all inputs. **CLI gotcha:** `--configfile` is greedy
  (`nargs='+'`) — put the target **before** `--configfile`, or separate with `-n`.

## Open questions

- **UV-ordinal mapping precision.** The frozen body-site→sun-exposure mapping (KD4) is the main
  remaining researcher degree-of-freedom. Lock the exact table in WP1 with a one-line literature
  rationale per tier; if no defensible tier ordering exists for an ambiguous label (e.g. "Other"),
  assign it to `unknown` rather than guessing. Flagged for review at implementation.
- **Hypermutator flag definition (KD2).** Use the absolute Campbell-2017 ≥10 mut/Mb view (already
  defined in the pipeline) as the single frozen hypermutator covariate, or also carry the
  per-histology relative view? Default: absolute only (one covariate, smaller denominator);
  confirm at WP1.
- **Treatment flag near-vacuity (t181).** If the treatment-exposed fraction on MC3 is ~0 (expected,
  TCGA primaries), the flag is a near-constant covariate. Keep it in the universe for completeness
  but log the degeneracy; do not drop silently.

## Non-goals

- No new signature refit (t197 `H` is the frozen input) and no new NMF (t198 modules are frozen).
- No de-novo signature extraction (the pre-reg scan is refit/assignment-based).
- No criterion re-derivation, threshold tuning, or denominator change after ranks are seen.
- No gated-data track.

## Acceptance criteria

- [ ] Covariate universe + UV-ordinal mapping + **both denominators (per-tissue / modules-excluded
      pooled Arm C, F1)** + **the frozen rank-statistic definition (F4)** written to disk **before**
      any rank (firewall + frozen-denominator discipline verified).
- [ ] Smoking covariate sourced from the **GDC open-access** clinical-with-followup file (UUID
      `0fc78496-…`), download verified (size ≈18,633,685 B + md5 + smoking columns + LUAD/LUSC
      non-missingness); dataset entity + `consumed_by` backlink recorded.
- [ ] Full grid scanned under one BH-FDR family with the frozen per-cell statistic; Arm C is a
      single pooled within-tissue rank against the modules-excluded denominator (per-stratum ranks
      sensitivity-only, never a pass route); CLR sign corroborated by the absolute-burden re-run.
- [ ] Exposure→covariate join asserts one MC3 sample per case across all 7 arms (F7).
- [ ] APOBEC3-locus leakage guard applied; permutation null + absolute-burden re-run run for any
      "too good" arm cell as pre-acceptance.
- [ ] K±5 / lung-pooling / frozen-APOBEC sensitivity executed; flips downgrade the arm to `[?]`.
- [ ] §1b activation table filled (post-join n, completeness, base rate) — and only then the gate
      read: arm A/B/C → 2-of-3 → H08a `[+]`/`[?]`/`[-]`, denominator reported per arm.
- [ ] `datapackage.json` updated (task t199); interpretation note committed; `science validate`
      clean; `snakemake --lint` clean.

## Reusable infrastructure

`build_h08_covariates.py` produces a per-sample MC3 covariate table (clinical + molecular +
expression-module) that is reusable by the future **H08b discovery** scan and by any downstream
MC3 covariate analysis — flag `reusable: true`. The within-tissue CLR association grid in
`run_h08_association_scan.py` is likewise the engine H08b will reuse over the non-textbook cells.
