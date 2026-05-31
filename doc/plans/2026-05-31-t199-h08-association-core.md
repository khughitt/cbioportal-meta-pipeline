---
id: "plan:2026-05-31-t199-h08-association-core"
type: "plan"
title: "h08 within-tissue covariate↔H association core (H08a scan)"
status: "active"
created: "2026-05-31"
updated: "2026-05-31"
related:
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
  - "method:h08-agnostic-association-model"
  - "pre-registration:h08-positive-control"
  - "question:q025-causal-direction-guard-for-expression-signature"
  - "task:t199"
  - "task:t180"
  - "task:t181"
  - "task:t195"
  - "dataset:tcga-mc3"
  - "dataset:tcga-pancanatlas"
---

# h08 within-tissue covariate↔H association core (H08a scan)

> **Pre-registration-already-exists mode.** Every verdict-bearing criterion — the three
> confirmatory arms, top-3 rank / positive sign / q<0.05, the 2-of-3 gate, the frozen Arm-C
> tissue set + pooled-rank rule, COSMIC v3.4, the active-signature ≥5% rule, the compositional
> + permutation pre-acceptance checks, and the `[+]/[?]/[-]` mapping onto H08a — is **locked**
> in `pre-registration:h08-positive-control` (committed 2026-05-30, amendment-001 2026-05-31).
> This plan **does not re-derive any of them.** It covers only the execution gates the pre-reg
> left to implementation: covariate provenance, the join materialization, covariate construction
> (where it is a researcher degree-of-freedom that must be frozen *before* ranks), the leakage
> guard, the compositional/permutation precision checks, and the §1b activation-table fill. Any
> belief that a locked criterion is wrong is an **amendment** question
> (`statistics-prereg-amendment-vs-fresh`), routed there — not re-planned here.

## Purpose

Build the H08a positive-control scan: the within-tissue association between each candidate
covariate and each per-sample COSMIC signature exposure `H`, over the 7 MC3 arm strata, reading
the committed 2-of-3 rank gate. This is the last of the four h08-run blocking checks
(`analysis-plan:h08-positive-control-scan` check 4); checks 1–3 (q018 / t197 refit / t198 NMF
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
  threshold (Campbell 2017 ≥10 mut/Mb, the absolute view already defined in the pipeline).
- **Rejected alternative:** run `annotate_hypermutators` (the canonical composite) for the
  tcga_mc3 h08 config to emit `samples_annotated.feather`.
- **Reason:** the composite pulls in MSI normalization, per-cancer GMM, and panel-callable-size
  machinery that targets the cross-study aggregation pipeline; for 7 WES strata it is
  disproportionate, and the four molecular covariates are individually available with clearer
  provenance. The composite remains the right path **if h08 becomes recurring** (then wire per
  t175) — recorded as the recurring-path alternative, not built now.

### Key decision 3: smoking covariate comes from the public PanCanAtlas clinical-with-followup file
- **Chosen approach:** fetch `clinical_PANCAN_patient_with_followup.tsv` from the public GDC
  PanCanAtlas publications page, join `tobacco_smoking_history` + `number_pack_years_smoked` on
  the 12-char TCGA patient barcode.
- **Rejected alternative:** the per-study cBioPortal PanCanAtlas clinical already on disk.
- **Reason:** **verified absent** — the cBioPortal LUAD/LUSC `data_clinical_patient.txt` carries
  no smoking/pack-years field at all (confirmed: only stage/sex/race/ancestry/survival). The
  covariate the pre-reg names for Arm B is *only* in the PanCanAtlas clinical-with-followup file.
  **It is public and ungated** (GDC PanCanAtlas supplement), so it is consistent with the standing
  no-gated-access constraint — this is an *un-built*, not an *inaccessible*, input. Data-access
  gate: PASS (origin external, public; verify on download).

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

### WP0 — acquire the PanCanAtlas smoking covariate (data-access gate)
- **Depends on:** nothing.
- **Entry point:** `code/scripts/fetch_pancanatlas_clinical.py` → `data/pancanatlas_clinical_with_followup.tsv`.
- **Definition of done:** file present and stat-verified (per the PDF-acquisition-verify discipline:
  verify the actual download, not the HTTP 200); `tobacco_smoking_history` +
  `number_pack_years_smoked` columns present for LUAD/LUSC patients; row count logged; a
  `dataset:tcga-pancanatlas-clinical` entity (or an `access.exception`/log note) recorded via
  `/science:find-datasets` if a fresh entity is warranted. Public/ungated confirmed in the log.

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
- **Definition of done:** `h08_covariates.feather` written; `covariate_denominator.json` written
  with the frozen covariate universe, the frozen UV-ordinal mapping table, the per-stratum
  active-signature set (≥5% rule, COSMIC v3.4), and the realized per-stratum covariate/signature
  counts — **before** any association is run. Leakage firewall preserved (no covariate is a
  function of `H`). Loud missingness for any covariate with low completeness (no silent fill).

### WP2 — the within-tissue association grid
- **Depends on:** WP1.
- **Entry point:** `run_h08_association_scan.py` (grid stage).
- **Does:** CLR transform of `H` (KD5); per (covariate, active-signature, stratum) within-tissue
  model with adjustment set {tissue, treatment, study/assay, ancestry} — tissue as fixed-effect
  stratifier; **Arm C as a single pooled within-tissue model** across {BLCA,BRCA,CESC,HNSC,LUAD,
  LUSC} yielding one APOBEC3A/B rank; one BH-FDR pass over the full grid; effect, sign, rank, q
  per cell; the unconditioned (tissue-pooled) contrast computed alongside for the R1 exploratory
  readout (Prediction 4). APOBEC3-locus leakage guard applied (KD6).
- **Definition of done:** `h08_association_grid.feather` with per-cell rank + sign + q and the
  per-stratum covariate-count denominators echoed from WP1; arm A/B/C target cells identified;
  the realized FDR family size logged.

### WP3 — pre-acceptance + registered sensitivity variants
- **Depends on:** WP2.
- **Entry point:** `run_h08_association_scan.py` (validation stage).
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
- **Does:** fill the §1b table (post-join n, covariate completeness, base rate per arm) — **the
  gate is not read until this is filled**; then read each arm (rank≤3, positive, q<0.05) and the
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

- [ ] Covariate universe + per-stratum denominator + UV-ordinal mapping written to disk **before**
      any rank (firewall + frozen-denominator discipline verified).
- [ ] Smoking covariate sourced from the public PanCanAtlas clinical, download stat-verified.
- [ ] Full grid scanned under one BH-FDR family; Arm C is a single pooled within-tissue rank
      (per-stratum ranks reported sensitivity-only, never a pass route).
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
