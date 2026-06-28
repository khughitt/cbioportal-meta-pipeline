---
type: interpretation
title: "t199 h08 positive-control association scan (H08a verdict) \u2014 inconclusive,\
  \ 1/3 arms pass (APOBEC clean)"
status: active
created: '2026-05-31'
updated: '2026-06-28'
id: interpretation:0024-t199-h08-association-verdict
source_refs:
- task:t199
- results/signature-h08-arms-2026-05-31/association/covariate_denominator.json
- results/signature-h08-arms-2026-05-31/association/h08_association_grid.feather
- results/signature-h08-arms-2026-05-31/association/h08_association_grid.meta.json
- results/signature-h08-arms-2026-05-31/association/h08_sensitivity.feather
- results/signature-h08-arms-2026-05-31/association/h08_permutation_null.feather
- results/signature-h08-arms-2026-05-31/association/h08_lung_pooling.feather
- code/scripts/build_h08_covariates.py
- code/scripts/run_h08_association_scan.py
- code/scripts/run_h08_sensitivity.py
date: '2026-05-31'
related:
- task:t199
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross
---
# t199 — hypothesis:0007 positive-control association scan (H08a verdict)

Date: 2026-05-31

## Question

Read the pre-registered H08a positive-control verdict: does the agnostic within-tissue
covariate↔signature association model recover the three
registered known aetiology→signature pairs on the MC3 WES substrate, under the criteria locked in
`pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature` (amendment-001)? This is check 4 — the association core —
of `plan:0005-h08-positive-control-scan-analysis-plan`; checks 1–3 (t196 covariate assembly QA, t197 SBS
refit, t198 NMF expression modules) are done. The verdict surface was **locked before ranks** and
is not relitigated here.
This verdict bears on
`hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and` and
inherits the feasibility constraints from
`question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross`.

## What was frozen, and when

The primary read is the **centered-log-ratio (CLR) coordinate** of the target signature, regressed
on the (z-scored) registered covariate with the pre-registered within-tissue adjustment set, ranked
by |signed standardized coefficient| within each (stratum, signature) cell. The ranking statistic,
adjustment set, CLR transform in `results/signature-h08-arms-2026-05-31/association/covariate_denominator.json` (pseudocount 0.5; structural zeros below the 5%-active rule excluded),
BH-FDR family, and the per-arm covariate-count **denominator** were all frozen in WP1/WP2 and
written to `covariate_denominator.json` **before** any rank was computed.

Freeze fingerprint (SHA256 of `covariate_denominator.json`):
`98bf159feca376e8ecfd150cd8bc0928990644b27db377df106ec86cdfaaac32`. The WP2 grid records it in
`h08_association_grid.meta.json`; the WP3 sensitivity run asserts equality against that value and
refuses to run on a mismatch, so every number below is tied to the same frozen denominator.

A **PASS** for an arm is: the registered covariate ranks ≤ 3 among that cell's frozen covariate set,
with positive sign, at BH-q < 0.05. The pre-reg maps ≥ 2/3 arms passing → H08a `[+]`; exactly 1/3 →
`[?]` inconclusive; 0/3 → `[-]`.

## §1b activation table (filled against the realized join)

The pre-reg gate is "not read until [post-join n, covariate completeness, base rate] are filled into
this table." They are now computed against the materialized MC3 ∩ signature-refit ∩ covariate join,
restricted to the t179 count-floor-passing exposures (the trusted-exposure primary grid).

| Arm | Stratum | Raw cases | PASS-bearing MC3 | Post-join n (count-floor ∩ arm) | Covariate completeness | Base rate |
|---|---|---|---|---|---|---|
| A | SKCM | 470 | 466 | 391 | `uv_sun_exposure_ordinal` 370/391 = **94.6%** | site tiers {high(2): 211, mid(1): 119, low(0): 40} — 54% high-UV-site |
| B | LUAD + LUSC | 1,089 | 993 | 859 | `pack_years` 703/859 = **81.8%** | mean 48.2, median 42 pack-years; 99.9% > 0 |
| C | BLCA·BRCA·CESC·HNSC·LUAD·LUSC | 3,434 | 2,991 | 1,934 | `apobec3ab_joint` 1,883/1,934 = **97.4%** | mean 9.04, median 9.19 (log2 APOBEC3A/B mRNA) |

In `results/signature-h08-arms-2026-05-31/association/h08_association_grid.feather`, the fit n per arm equals the completeness numerator (370 / 703 / 1,883) — the model drops samples
with the target covariate missing. All three arms are comfortably powered for a textbook effect;
none of the misses below is a power artefact (Arm B is the smallest completeness fraction at 82%, and
its registered proxy still has n = 703).

## Primary gate (CLR, the frozen WP2 read)

| Arm | Covariate → signature | Stratum | n | Rank / denom | Sign | BH-q | PASS? |
|---|---|---|---|---|---|---|---|
| A | `uv_sun_exposure_ordinal` → SBS7 | SKCM | 370 | **10 / 14** | − | 0.596 | **no** |
| B | `pack_years` → SBS4 | LUAD+LUSC pooled | 703 | **6 / 8** | + | 0.375 | **no** |
| C | `apobec3ab_joint` → SBS2_13 | APOBEC-six pooled | 1,883 | **1 / 10** | + | ≈ 0 (4.4e-12) | **yes** |

**Net: 1 / 3 → H08a `[?]` inconclusive.**

Arm C is the single primary pass, and it is a clean one: `apobec3ab_joint` (the registered
APOBEC3A/B mRNA covariate) is the rank-1 covariate against the APOBEC signature, at q ≈ 1e-12.

## Pre-acceptance and sensitivity (WP3 — DIAGNOSTIC, not a path to PASS)

The pre-reg requires a "too good to be true" pre-acceptance check on any strong pass, and a
compositional-basis sensitivity check. These are **diagnostics**: CLR was frozen as the primary read
before ranks, so a covariate that fails CLR cannot be promoted to a primary PASS by a sensitivity
basis. Basis-dependent recovery (absolute passes, CLR fails) is reported as such and pushes the read
toward `[?]`, never to `[+]`.

**Permutation null** (`results/signature-h08-arms-2026-05-31/association/h08_permutation_null.feather`; covariate shuffled *within tissue*, frozen seed 0, n = 1,000; unbiased
`(exceedances+1)/(n+1)` p-value):

| Arm | obs coef | exceedances / n | p_perm | Exceeds null? |
|---|---|---|---|---|
| C | +0.458 | 0 / 1,000 | **0.001** | **yes** — the strong pass survives pre-acceptance |
| A | −0.046 | 400 / 1,000 | 0.401 | no (consistent with null) |
| B | +0.107 | 190 / 1,000 | 0.191 | no (consistent with null) |

In `results/signature-h08-arms-2026-05-31/association/h08_permutation_null.feather`, Arm C's effect is not reachable by any of 1,000 within-tissue permutations (p floors at the null's
resolution, 0.001), so the only primary pass is stable — the 1/3 read does **not** weaken on
pre-acceptance.

**APOBEC3-locus leakage guard** (`results/signature-h08-arms-2026-05-31/association/h08_sensitivity.feather`, Arm C): excluding the 120 / 1,934 Arm-C samples carrying an
APOBEC3A/B-locus mutation, `apobec3ab_joint` remains rank 1, positive — the mRNA→signature
association is not an artefact of cis mutations at the APOBEC3 locus.

**Absolute-burden diagnostic** (`is_primary_gate = False`; re-ranks on log absolute per-signature
burden instead of the CLR coordinate):

| Arm | CLR rank | Absolute rank | Verdict |
|---|---|---|---|
| A | 10 / 14 | **12 / 14** (−) | no recovery (worse) |
| B | 6 / 8 | 6 / 8 (+) | no recovery (unchanged) |
| C | 1 / 10 | 1 / 10 (+) | robust on both bases |

There is **no basis-dependent recovery of A or B** — the absolute-burden basis does not rescue
either failing arm, so the 1/3 read is a genuine MC3-as-implemented result, not a CLR compression
artefact.

**Lung per-histology variant** (`results/signature-h08-arms-2026-05-31/association/h08_lung_pooling.feather`, Arm B sensitivity): pooled 6/8 (q 0.37), LUAD-only 10/13 (q 0.34),
LUSC-only 13/13 (q 0.65) — splitting the lung pool does not recover the smoking proxy in either
histology.

**K ± 5 modules**: analytically moot and not re-run — per `results/signature-h08-arms-2026-05-31/association/covariate_denominator.json`, the two pooled arms (B, C) exclude NMF modules
from their denominators, and Arm A's UV proxy sits at rank 10/14 with coef ≈ 0, far from top-3
regardless of ±5 module covariates.

## Why A and B miss — proxy inadequacy, not method failure (and not aetiology recovery)

The failures are interpretable, and the interpretation is disciplined to **not** overclaim recovery.

In both failing cells the top-ranked covariates are **burden-linked** rather than the registered
exposures:

- SKCM → SBS7: rank 1 `is_hypermutator` (+, q 2e-22), rank 2 `tmb_nonsynonymous` (+, q 4e-11);
  `uv_sun_exposure_ordinal` is rank 10.
- LUAD+LUSC → SBS4: rank 1 `is_hypermutator` (+, q 1e-23), rank 2 `tmb_nonsynonymous` (+, q 4e-21);
  `pack_years` is rank 6.

This is **not** evidence that the method recovers UV or smoking aetiology. `is_hypermutator` and TMB
are target-*proximal* mutational-burden consequences, and against the CLR coordinate of an arm's
**dominant** signature (SBS7 ≈ the bulk of SKCM composition; SBS4 large in lung) a correlation with
total burden is close to mechanical. The honest reading is: **the registered exposure proxies failed
to rank, and burden-linked covariates dominated — consistent with the registered proxies being
inadequate, not with H08a recovery of the aetiology.**

The proxy inadequacy is concrete and was anticipated in the pre-reg's Null Result Plan:

- **Arm A (UV):** the only UV exposure measure computable today is an *anatomic-site ordinal*
  derived from the SKCM sample's primary/metastatic site, which is heavily metastasis-contaminated
  (the high-UV-site tier is dominated by metastatic deposits whose site reflects spread, not sun
  exposure). It is a poor surrogate for cumulative UV dose.
- **Arm B (smoking):** `pack_years` carries genuine signal (positive sign, and rank 6/8 with a
  modest coefficient) but is a noisy self-reported lifetime exposure with 18% missingness; it does
  not out-rank the burden covariates against SBS4.
- **Arm C (APOBEC):** the registered covariate is a *direct molecular measure* (APOBEC3A/B mRNA),
  not an exposure surrogate — which is exactly why it is the clean pass.

So the discriminating factor across the three arms is **proxy directness**: the molecular covariate
recovers its signature; the two environmental-exposure surrogates do not. This is a statement about
the registered proxies on the MC3 substrate, not about the agnostic association method, which
behaves as designed (it surfaces the strongest covariate per cell and FDR-controls the grid).

## Secondary controls — not evaluable on this arm panel

The pre-reg lists MMR/MSI → SBS6/15/26 and POLE → SBS10 as secondary corroboration controls. In `results/signature-h08-arms-2026-05-31/association/h08_association_grid.meta.json`, they
are **not evaluable here**: none of SBS6/15/26/10 is active (above the 5% rule) in any of the seven
arm strata, so they are absent from the restricted refit's active-signature set
(`{SBS1, SBS2_13, SBS3, SBS4, SBS5, SBS7, SBS29, SBS40a, SBS40c}`). MSI/POLE hypermutation is rare in
this panel (chosen for UV/smoking/APOBEC, none of them MMR-driven tumour types), so this is expected,
not a missing computation. A corroboration of the MMR/POLE controls would require adding MMR-rich
strata (COAD/READ/STAD/UCEC) — out of scope for the positive-control panel and deferred.

A within-Arm-C observation worth recording from `results/signature-h08-arms-2026-05-31/association/h08_association_grid.feather`: against SBS2_13, `msi_sensor_score` (rank 2, −),
`is_msi_h` (rank 3, −) and `pole_hotspot` (rank 4, −) all rank just below `apobec3ab_joint` with
*negative* sign — APOBEC composition anti-correlates with MMR/POLE hypermutation in the pooled set,
consistent with these being distinct, competing mutational processes.

## Verdict and what it licenses

**H08a = `[?]` inconclusive (1/3 registered arms pass).** The hypothesis stays at `proposed`; the
positive-control prong neither promotes nor refutes the method. The discovery prong (H08b) remains
locked pending this gate and is not opened by a `[?]`.

The actionable conclusion is **"repair the proxies," not "abandon the method"**:

- The agnostic association model recovered the one arm with a direct molecular covariate (APOBEC),
  with a result robust to permutation, leakage, and compositional basis.
- The two misses are localized to environmental-exposure surrogates that are known to be weak on
  TCGA/MC3 (metastasis-contaminated UV site; noisy self-reported pack-years). A follow-up that
  swaps in better UV (e.g. a primary-tumour-restricted SKCM subset) and smoking measures is the
  indicated next step before any H08a re-read.

This note preserves the pre-reg's required distinction: the **primary gate** result is the CLR read
(1/3), and the absolute-burden re-rank is a **diagnostic sensitivity** result that confirms the
misses are not a compositional artefact — it is not folded into the gate.

## Artifacts

Run bundle `results/signature-h08-arms-2026-05-31/association/` (gitignored; fingerprinted in
`datapackage.json`):

- `h08_covariates.feather` — frozen covariate table (3,457 samples × 34 cols)
- `covariate_denominator.json` — frozen per-arm covariate-count denominator (SHA256 above)
- `h08_association_grid.feather` + `.meta.json` — full BH-FDR grid (family size 638) and WP2 meta
- `h08_sensitivity.feather`, `h08_permutation_null.feather`, `h08_lung_pooling.feather` +
  `h08_sensitivity.meta.json` — WP3 diagnostics

Scripts: `code/scripts/build_h08_covariates.py` (WP1), `run_h08_association_scan.py` (WP2),
`run_h08_sensitivity.py` (WP3). statsmodels 0.14.6; COSMIC SBS v3.4; frozen seed 0.

Related: `hypothesis:0007`, `method:h08-agnostic-association-model`,
`pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature` (amendment-001), `plan:0005-h08-positive-control-scan-analysis-plan`,
`task:t199`, and substrates `task:t197` (SBS refit) / `task:t198` (NMF modules).
