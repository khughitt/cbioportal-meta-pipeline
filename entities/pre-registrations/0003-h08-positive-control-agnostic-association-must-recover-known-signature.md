---
type: pre-registration
title: "h08 positive control \u2014 agnostic association must recover known signature\
  \ aetiologies unprompted"
status: committed
created: '2026-05-30'
updated: '2026-06-28'
id: pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature
committed: '2026-05-30'
spec: doc/methods/h08-agnostic-association-model.md
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- method:h08-agnostic-association-model
- question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross
- question:0019-does-de-novo-extraction-on-the-aggregated-cohort-surface-factors-not-in
- task:t177
- dataset:tcga-mc3
- dataset:tcga-pancanatlas
- discussion:0004-common-mutational-signatures-known-vs-learned-immune-causes-and
commits_to:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
amendments:
- id: amendment-001
  date: '2026-05-31'
  label: amendment_before_results
  summary: Expression-substrate unit clarification (t198). The frozen NMF rule named
    log2(TPM+1) on TCGA PanCanAtlas RNA-seq, but TCGA PanCanAtlas distributes RSEM
    (no native TPM). Realized substrate = per-study cBioPortal PanCanAtlas RSEM (data_mrna_seq_v2_rsem.txt)
    for the 7 arm tissues; realized unit = log2(RSEM_V2 + 1). Per-arm NMF makes cross-tissue
    batch correction moot. No change to hypothesis, arms, cohort, adjustment set,
    rank gate, 2-of-3 rule, K-selection procedure, MAD/<10%-expressed filters, or
    active-signature rule. Recorded before any association run (no parent verdict
    known).
---

# Pre-registration: positive control — agnostic association must recover known signature aetiologies unprompted

**Target class (§0): mixed.**

- **Operational portion** — refit per-sample COSMIC signature exposures `H` on the MC3 WES
  substrate (`tcga_mc3`) and run the within-tissue covariate↔`H` association exactly as specified
  in `method:h08-agnostic-association-model`. This portion is an amendment-gate: any deviation from
  the committed adjustment set, stratification, or substrate requires an `amendments:` record. It
  produces no `bears_on` edge.
- **Epistemic portion** — interpret the recovery result as evidence about **H08a** (the
  positive-control prong of `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`): does the agnostic method recover textbook
  exposure→signature links *without being told them*? `commits_to:` is scoped to `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`
  only; the other `related:` entries (`question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross`, `question:0019-does-de-novo-extraction-on-the-aggregated-cohort-surface-factors-not-in`, `task:t177`, datasets, discussion) are navigation context
  and do **not** receive derived `bears_on` edges.

**Execution timing (§0 sub-axis): runnable-now, engineering-gated — NOT data-gated.** The qualifying
vehicle exists and is adequately powered (MC3 WES, ~9–10k samples / 32–33 cancer types, already
ingested as `dataset:tcga-mc3`; co-measured mRNA from `dataset:tcga-pancanatlas`). The binding constraint is *building the
association layer + the per-sample signature refit*, not data availability, so this pre-reg is
authored in normal (runnable) mode, not data-gated mode. Activation is nonetheless conditioned on
two open gates that do **not** change the registered criteria:

1. `task:t177` — literature scan of prior agnostic / PheWAS-style signature-aetiology work (so we do
   not re-derive a published method and so the discovery prong's novelty bar is calibrated).
2. `question:0018` — feasibility verdict on downstream per-sample signature extraction + panel
   adequacy (confirms the refit is sound on MC3 before the association runs).

The conceptual background for known-versus-learned signature causes is
`discussion:0004-common-mutational-signatures-known-vs-learned-immune-causes-and`.

## Hypotheses Under Test

- **H08a (positive control / recovery)** of
  `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`.

This pre-reg covers **only the positive-control prong**. H08b (discovery) is explicitly **not**
pre-registered here — it remains exploratory and is *gated behind* a passing H08a verdict (see
§ Null Result Plan). A separate pre-registration should be authored for H08b once H08a passes and
t177 has fixed the novelty bar.

## Feasibility (§1b — support sets)

Raw per-arm support counted as **distinct TCGA cases per project** from
`data/tcga_case_to_project.tsv` (deduplicated; **11,428** distinct cases across **33** projects) on
2026-05-30. This map defines the `tcga_mc3` WES substrate's case identity and is the honest
computable-today **upper bound** on each arm's n. It is deliberately *not* counted from
`results/poc-2026-04-17/metadata/samples_annotated.feather` — that POC table is dominated by
`msk_impact_2017` panel samples, which `method:h08-agnostic-association-model` excludes from per-sample signatures, so it is the wrong
substrate for this table.

**Two computable-today bounds are recorded.** *Raw distinct cases* is the upper bound from the
case→project map. *PASS-bearing MC3 samples* is the closer pre-refit floor: distinct
`Tumor_Sample_Barcode` carrying ≥1 `FILTER == PASS` variant in `data/mc3.v0.2.8.PUBLIC.maf.gz`
(3,600,962 data rows), mapped to project via the case map — i.e. the samples that actually hold
callable somatic variants and so can receive a per-sample signature refit. This is materially lower
than the case count (e.g. BRCA 1,098 cases → 791 PASS-bearing samples; APOBEC-six 3,434 → 2,991) and
is the honest lower bound on each arm's pre-join n. Counted 2026-05-30; an independent reviewer count
agreed on **every arm** (SKCM 466, LUAD 513, LUSC 480, BLCA 411, BRCA 791, CESC 289, HNSC 507,
APOBEC-six total 2,991). The realized per-arm n sits between these two bounds and shrinks further at
the covariate join (clinical / RNA-seq); it is recorded at activation.

| Arm | Stratum (TCGA project) | Raw distinct cases | PASS-bearing MC3 samples | Post-join n | Covariate completeness | Base rate |
|---|---|---|---|---|---|---|
| A | SKCM | **470** | **466** | **391** (count-floor ∩ arm; fit n 370) | `uv_sun_exposure_ordinal` 370/391 = **94.6%** | site tiers high(2):211 / mid(1):119 / low(0):40 |
| B | LUAD + LUSC | **1,089** (585 + 504) | **993** (513 + 480) | **859** (count-floor ∩ arm; fit n 703) | `pack_years` 703/859 = **81.8%** | mean 48.2, median 42 pack-years |
| C | BLCA·BRCA·CESC·HNSC·LUAD·LUSC | **3,434** (412·1098·307·528·585·504) | **2,991** (411·791·289·507·513·480) | **1,934** (count-floor ∩ arm; fit n 1,883) | `apobec3ab_joint` 1,883/1,934 = **97.4%** | mean 9.04, median 9.19 (log2 mRNA) |

The **post-join n** (signature exposure × covariate, after the signature refit and the MC3∩clinical /
MC3∩RNA-seq intersections), **covariate completeness**, and **base rates** cannot be computed today:
the per-sample signature refit, the clinical-covariate join, and the expression export are not yet
materialized as a single joined table on the MC3 substrate. Recording these three numbers per arm
against the realized join is an **activation precondition** (alongside `task:t177` / `question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross`) — the gate is
**not read until they are filled into this table**. Raw n is comfortably powered for arms A and B
(textbook effects at n ≈ 470–1,089); arm C's effective n is the one most likely eroded by the
RNA-seq intersection, consistent with it being the tolerated miss under the 2-of-3 rule.

**Activation satisfied (2026-05-31, task:t199 WP4).** The three TBC columns are now filled against the
realized MC3 ∩ signature-refit ∩ covariate join (count-floor-passing primary grid), so the gate is
read. All three arms cleared their power floor; arm C's RNA-seq intersection eroded less than feared
(post-join n 1,934, 97.4% complete) and it is in fact the *only* primary pass — the tolerated miss
under 2-of-3 turned out to be the two environmental-exposure arms (A, B), not arm C. See
`doc/interpretations/2026-05-31-t199-h08-association-verdict.md` for the gate read (1/3 → H08a
`[?]`).

## Expected Outcomes

The agnostic within-tissue scan, given no aetiology labels, will rank each textbook covariate at or
near the top of all covariates tested against its matching signature, with the literature-expected
sign:

- **UV proxy → SBS7** within cutaneous melanoma (SKCM). SBS7 is the dominant signature of sun-exposed
  melanoma; the effect is expected to be large and unambiguous.
- **Smoking → SBS4** within lung (LUAD + LUSC). SBS4 is the canonical tobacco signature; expected
  strong in smokers, with never-smoker LUAD diluting the pooled estimate.
- **APOBEC3A/B expression → SBS2/13** within tissue (bladder / breast / cervix / head-and-neck /
  lung, where APOBEC signatures are prevalent). Expected positive but more modest and noisier than
  the two exogenous arms — this is the arm most likely to miss, by design tolerated under the
  2-of-3 rule.

For `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`,
two further textbook links — **MMR/MSI → SBS6/15/26** and **POLE → SBS10** — are tracked as
**exploratory secondary positive controls** (not part of the 2-of-3 gate), because their covariates
(MSI status, POLE hotspot flag) are already pipeline-derived annotations and a hit there is
corroborating but not load-bearing.

We also expect (Prediction 4 of `method:h08-agnostic-association-model`) that the **unconditioned** (tissue-pooled) version of each arm
will show inflated or sign-distorted associations relative to the within-tissue version — quantifying
how much of the naive exposure→signature story is tissue collinearity (rival **R1**).

## Expectations

For `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`, the interpretive numerical commitment is a **rank-position gate**: within the relevant tissue
stratum, the known covariate must rank in the **top 3** of all tested covariates by adjusted effect
size against its matching signature, with the expected sign, at **FDR q < 0.05**. These rank
expectations are **literature-backed only** (no prior own-analysis of this exact agnostic pipeline
exists), so every block below is `hint` tier → **soft gate** with a deliberately wide acceptance
band (top-3, not rank-1; 2-of-3, not 3-of-3). The registered gate is reported in the verdict
regardless of outcome; any post-data tightening requires an amendment and forfeits confirmatory
status for the retightened arm.

```yaml
- parameter: "rank of UV proxy (sun-exposed anatomic site) among covariates tested vs SBS7 exposure, within SKCM"
  scope: confirmatory
  expected:
    central: "rank 1"
    range:   "rank [1, 3]"
    direction: positive   # sun-exposed site -> higher SBS7 exposure
  evidence_tier: hint
  provenance:
    - source: "Alexandrov2020"
      calibration_source: literature
      estimate: "SBS7a-d dominate cutaneous melanoma spectra (UV C>T at dipyrimidines)"
      ref: "paper:Alexandrov2020"
      notes: "Establishes SBS7 as THE melanoma signature; does not establish rank vs an agnostic covariate scan on MC3."
  unknowns:
    - "TCGA SKCM anatomic-site granularity is coarse; 'sun-exposed vs not' may be weakly resolved or partly missing"
    - "metastatic SKCM samples (a large fraction of the cohort) may dilute the primary-site sun-exposure contrast"
  gate_use: "Anchors the §Decision Criteria top-3 rank gate for arm A; soft gate (literature-only), wide band [1,3]."

- parameter: "rank of smoking exposure (pack-years / smoking-history) among covariates tested vs SBS4 exposure, within LUAD+LUSC"
  scope: confirmatory
  expected:
    central: "rank 1"
    range:   "rank [1, 3]"
    direction: positive
  evidence_tier: hint
  provenance:
    - source: "Alexandrov2020"
      calibration_source: literature
      estimate: "SBS4 = tobacco-smoking signature in lung (C>A transversions)"
      ref: "paper:Alexandrov2020"
      notes: "Establishes the aetiology; rank vs agnostic covariate scan on MC3 unvalidated."
  unknowns:
    - "never-smoker LUAD dilutes the pooled within-lung estimate; pack-years completeness in TCGA clinical varies"
    - "whether to pool LUAD+LUSC or stratify — pooling within 'lung' vs per-histology may shift the rank"
  gate_use: "Anchors the §Decision Criteria top-3 rank gate for arm B; soft gate, wide band [1,3]."

- parameter: "rank of APOBEC3A/B mRNA among covariates tested vs SBS2/13 exposure, within tissue (APOBEC-prevalent strata)"
  scope: confirmatory
  expected:
    central: "rank [1, 3]"          # best guess
    range:   "rank [1, 5]"          # plausible expectation band — NOT the gate (gate is rank<=3)
    direction: positive
  evidence_tier: hint
  provenance:
    - source: "Alexandrov2020"
      calibration_source: literature
      estimate: "SBS2/13 attributed to APOBEC3 cytidine-deaminase activity"
      ref: "paper:Alexandrov2020"
      notes: "Aetiology established; steady-state APOBEC3 mRNA is an imperfect proxy for episodic deaminase activity."
  unknowns:
    - "MC3 mutation samples ∩ PanCanAtlas RNA-seq samples is <100%; effective n per stratum is smaller than raw cohort n"
    - "APOBEC mutagenesis is episodic (kataegis); steady-state mRNA may decorrelate from accumulated SBS2/13 burden"
    - "APOBEC3A vs APOBEC3B contribution differs by tissue; which transcript(s) to use is a design choice"
  gate_use: "Anchors the §Decision Criteria rank gate for arm C. Expected plausible band: top-5 (this is the noisiest arm, the likely tolerated miss under 2-of-3). Confirmatory PASS threshold: top-3 — the [1,5] band is the honest pre-data expectation, the gate is rank<=3 per §Decision Criteria; the two are deliberately distinct. Soft gate (literature-only)."
  gate_limitations:
    - alternative: "R2 reverse causation — SBS2/13-causing driver events remodel APOBEC3 expression, so high expr is a consequence not a cause"
      region: "any positive APOBEC3-expr↔SBS2/13 association in the top-3 band"
      verdict_if_unresolved: "[?] inconclusive"
      # A top-3 positive rank confirms the method RECOVERS the known association (the H08a question)
      # but does NOT establish expression is upstream; that is an H08b-discovery claim requiring mediation/temporality.
```

## Decision Criteria

For `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`,
three pre-specified **confirmatory arms**. An arm **passes** iff, within its tissue stratum, the
known covariate ranks **top-3** among all tested covariates by adjusted effect against its matching
signature, with the **expected (positive) sign**, at **FDR q < 0.05**.

| Arm | Covariate | Signature | Stratum | Pass condition |
|---|---|---|---|---|
| A | UV proxy = sun-exposed anatomic site | SBS7 | SKCM | rank ≤ 3, positive, q < 0.05 |
| B | smoking (pack-years / history) | SBS4 | LUAD+LUSC | rank ≤ 3, positive, q < 0.05 |
| C | APOBEC3A/B mRNA | SBS2/13 | BLCA·BRCA·CESC·HNSC·LUAD·LUSC (pooled, within-tissue) | pooled rank ≤ 3, positive, q < 0.05 |

**Gate (user-committed): 2 of 3 arms must pass.**

**Arm C aggregation rule (frozen).** The eligible APOBEC-prevalent strata are exactly
**{BLCA, BRCA, CESC, HNSC, LUAD, LUSC}** — the canonical APOBEC-enriched TCGA tissues (Alexandrov
2020 [@Alexandrov2020]; Roberts et al. [@Roberts2013]) — frozen here and not expanded or substituted post-hoc. Arm C is evaluated as a
**single pooled within-tissue model** across these six strata (tissue entered as a fixed-effect
stratifier so the estimand stays within-tissue per `method:h08-agnostic-association-model`), yielding
**one** rank for APOBEC3A/B mRNA against SBS2/13. The arm passes iff that **pooled** rank ≤ 3 with
positive sign at q < 0.05. Per-stratum ranks are reported as **sensitivity / exploratory only** and
do **not** constitute an alternative pass route — in particular, "APOBEC3 ranks top-3 in *some*
eligible tissue" is explicitly **not** a pass, removing tissue-cherry-picking flexibility.

Mapped to the canonical verdict vocabulary on **H08a**:

- **`[+]` supports** — **≥ 2 of 3** arms pass. The method recovers the known map unprompted; H08a is
  supported and the H08b discovery prong is **unlocked** for separate pre-registration. (3/3 is
  strong support; 2/3 meets the committed gate.)
- **`[?]` inconclusive** — **exactly 1 of 3** arms passes. Recovery is partial and below the gate;
  no H08a support, discovery stays locked, but the failure is plausibly a power/proxy problem in the
  missing arms rather than a method failure (see Null Result Plan). Triggers diagnosis, not abandonment.
- **`[-]` refutes** — **0 of 3** arms pass. The agnostic scan cannot reproduce *any* textbook link
  within tissue at a reasonable FDR — the method is underpowered or confounded beyond rescue on
  MC3-scale data, and **the H08b discovery prong is void** (per `method:h08-agnostic-association-model`
  § Positive control).

Secondary controls (MMR/MSI→SBS6/15/26, POLE→SBS10) are reported as `[+]/[~]` corroboration only and
**do not change the H08a verdict**.

## Null Result Plan

A null here is **evidence about the method, not (yet) about biology**. Because H08a is a
positive-control gate over phenomena with overwhelming prior literature support, the diagnostic
ordering on a `[?]` or `[-]` result is:

1. **Power / proxy adequacy first.** A miss on arm A or C is more likely a *proxy* failure
   (coarse TCGA anatomic-site labels for UV; steady-state mRNA vs episodic APOBEC activity) or a
   *cohort-overlap* shortfall (MC3 ∩ RNA-seq) than a true method failure. Re-examine effective n and
   covariate completeness per stratum **before** any belief update on `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`.
2. **Stratification check.** Re-run the failing arm under the alternative lung pooling (per-histology
   vs LUAD+LUSC) and the alternative APOBEC tissue set, as registered sensitivity variants — these
   are not threshold moves, the rank gate is unchanged.
3. **Only then** read the verdict against H08a. A genuine `[-]` (0/3, with adequate power and clean
   proxies) is a real refutation that voids the discovery prong; a `[?]` (1/3) recommends repairing
   proxies / adding the EHR-covariate track (BPC/MSK-CHORD) and re-running, not abandoning `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`.

This is not a pilot — MC3 is full-scale — so a clean null carries real evidential weight, subject to
the proxy/power triage above.

## Suspicious/Unexpected Result Plan

"Too good to be true" for an agnostic association scan looks like **everything associating with
everything**:

- **Universal significance** — if a large fraction of *all* covariate×signature cells clear q < 0.05,
  suspect (a) **compositional artifact**: signature exposures `H` are sum-constrained per sample, so
  raw exposures induce spurious negative correlations — guard by modeling absolute per-signature
  burden or a CLR/ILR transform, not closed proportions; (b) **insufficient tissue conditioning** —
  if the within-tissue and unconditioned results are nearly identical, tissue was not actually held
  fixed (Prediction 4 should show a *difference*).
- **Rank-1, q ≈ 0 on all three arms simultaneously** — plausible for SBS7/SKCM, suspicious for the
  APOBEC arm; check for **leakage** where the covariate and the signature are two measurements of the
  same event (e.g. an APOBEC3-locus mutation that both inflates mRNA and is itself an SBS2/13 call).
- **Required pre-acceptance checks**: a within-stratum **permutation null** (shuffle the covariate
  across samples within tissue, refit, confirm the observed rank/effect exceeds the null), and the
  compositional-transform sensitivity re-run. An unexpectedly strong result is not accepted until
  both pass.

## Known Limitations

- **Proxy quality is the dominant limitation.** TCGA anatomic-site granularity (UV) and steady-state
  APOBEC3 mRNA (APOBEC) are imperfect stand-ins for the true exposures; only the smoking arm has a
  reasonably direct covariate. The 2-of-3 + top-3 design exists precisely to tolerate this.
- **Cohort overlap.** The signature outcome (MC3 mutations) and the expression covariate (PanCanAtlas
  RNA-seq) are co-measured on overlapping but not identical sample sets; effective n per stratum is
  set by the intersection.
- **Recovery ≠ causation.** Even a full 3/3 pass establishes only that the agnostic method
  *recovers* known associations — it does not establish that any covariate (especially expression) is
  *upstream*. Causal/upstream claims are H08b territory and require the mediation/temporality logic in
  `method:h08-agnostic-association-model` (R2 guard).
- **Single substrate.** This pre-reg is MC3-only (the signature-grade track). The EHR-covariate track
  (GENIE BPC / MSK-CHORD, cohort-pooled) is out of scope here and would be a separate registration.

## Metric Selection Rationale

**Primary metric: rank position** of the known covariate among all tested covariates for its
signature, within tissue stratum (with sign and FDR q-value as qualifiers). Rank is chosen over a raw
effect-size threshold because the question H08a asks is comparative — "does the *agnostic* scan
surface the right covariate *near the top* without being told to?" — not "is the effect of a given
magnitude?". A magnitude gate would require a `calibrated`-tier effect-size prior this project does
not yet have; a rank gate is the honest instrument for a hint-tier, literature-only expectation.
Known limitation: rank is sensitive to the size/composition of the covariate set, so the realized
covariate-count denominator is reported alongside each arm's verdict — and the covariate universe and
active-signature inclusion rule that *determine* that denominator are frozen in § Total Comparison
Count before any rank is computed, so the top-3 threshold cannot be moved by post-hoc denominator
changes.

## Exploratory vs. Confirmatory

Per-block `scope:` is authoritative (see § Expectations).

- **Confirmatory:** arms A, B, C (the three Expectations blocks above).
- **Exploratory:** secondary positive controls (MMR/MSI→SBS6/15/26, POLE→SBS10); the
  unconditioned-vs-within-tissue R1 contrast (Prediction 4); and the entire H08b discovery scan over
  non-textbook covariate↔signature cells. Exploratory results carry no confirmatory weight and feed
  hypothesis generation only.

## Total Comparison Count

The agnostic scan is the full grid: (covariates) × (active COSMIC SBS signatures) × (tissue strata).
For a rank-position gate the denominator must be **fixed by rule before any rank is computed**, even
though its realized integer is only known at run time. The following are **frozen here**:

- **Covariate universe** — the union of (a) the structured clinical fields enumerated in
  `method:h08-agnostic-association-model` (age, sex, race, stage, MSI, primary_site / anatomic-site,
  oncotree_code, treatment history where available); (b) the derived molecular features already in
  the pipeline (TMB, hypermutator class / flags, POLE/POLD1 hotspot, MSI status); and (c) K
  expression modules. No covariate outside this enumerated union enters the denominator.
- **Expression-module count K — frozen rule (inlined; no external plan dependency).** Modules are
  derived by **non-negative matrix factorization (NMF)** on the log2(TPM+1) expression matrix
  (genes × samples) of the signature-grade substrate (TCGA PanCanAtlas RNA-seq, restricted to the
  MC3-overlapping samples per arm), after standard filtering: drop genes expressed in < 10% of
  samples, retain the top 2,000 most-variable genes by median-absolute-deviation. K is selected by
  the **cophenetic-correlation criterion** of Brunet et al. 2004 — run NMF for K ∈ {5, 10, 15, …, 50}
  with 50 random restarts each, and choose the **largest K before the cophenetic correlation
  coefficient drops below 0.90** (ties broken toward the smaller K). This selection runs on the
  **expression matrix alone** — it never sees signature exposures, mutation data, or the covariate↔H
  association — so K cannot be tuned against the gate. The selected K and the per-K cophenetic curve
  are written to the run's output and recorded **before** any covariate↔signature rank is computed.
  *Sensitivity (exploratory):* the full scan is re-run at K±5 to confirm the H08a arm verdicts are
  not artifacts of the exact module count; a verdict that flips under K±5 is downgraded to `[?]`.
- **Active-signature inclusion rule** — COSMIC v3.4 SBS reference; a signature enters a stratum's
  denominator iff it receives non-zero assigned exposure in **≥ 5%** of that stratum's samples
  (frozen threshold). The reference version and the 5% rule are fixed here.

Under these frozen rules the realized integer denominator (and per-stratum covariate / signature
counts) is **reported at run time as an output, not a free parameter** — with ~tens of covariates ×
~30–50 active SBS × ~32 strata, the exploratory grid is in the **thousands** of cells.

| Category | Count | Correction |
|---|---|---|
| Confirmatory tests | 3 (arms A/B/C) | FDR (Benjamini–Hochberg) within the full grid; arm verdicts read at q < 0.05 |
| Exploratory tests | full grid minus 3 (≈ thousands; exact count reported at run time) | FDR (BH) across the full covariate×signature×stratum family; grid size reported |
| **Total** | **full grid (reported at run time)** | **BH-FDR, family = full grid; per-stratum rank denominators reported** |

## Amendments

### Amendment 001 — expression-substrate unit clarification (2026-05-31)

**Label:** `amendment_before_results`. Recorded while building the expression-module substrate
(`task:t198`), **before** any covariate↔`H` association has been run — no parent verdict is known.

**Trigger.** The frozen rule in *Total Comparison Count* specified NMF on the **`log2(TPM+1)`**
expression matrix of "TCGA PanCanAtlas RNA-seq." TCGA PanCanAtlas RNA-seq is distributed as
**RSEM-V2**, not TPM — neither the per-study cBioPortal matrices nor the EBPlusPlus batch-corrected
pan-cancer matrix carry native TPM. The literal wording is therefore unsatisfiable against the
named substrate.

**Resolution.** Realized substrate = the per-study cBioPortal PanCanAtlas matrices
(`data_mrna_seq_v2_rsem.txt`) for the seven arm tissues, restricted to MC3-overlapping samples per
arm; realized unit = **`log2(RSEM_V2 + 1)`**. Because the K-selection NMF runs **per arm** (one
tissue stratum at a time), the cross-tissue batch correction of the single EBPlusPlus file confers
no benefit here, so the per-study (per-arm) RSEM matrices are the faithful and lower-cost substrate.

| Parent section | Status | Notes |
|---|---|---|
| Scope / hypothesis / arms (A/B/C) | inherited | unchanged |
| Cohort (7 MC3 arm strata; MC3-overlapping samples) | inherited | unchanged; realized expression∩MC3 n reported at run time |
| Estimand / contrast (within-tissue covariate↔`H`) | inherited | unchanged |
| Model / adjustment set | inherited | unchanged |
| Metric (rank ≤3, positive, q<0.05; 2-of-3 gate) | inherited | unchanged |
| Active-signature rule (≥5%), COSMIC v3.4 | inherited | unchanged |
| K-selection (NMF K∈{5..50}×50 restarts, cophenetic≥0.90, ties→smaller; leakage firewall) | inherited | unchanged |
| Gene filters (drop <10% expressed, top-2,000 MAD) | inherited | unchanged |
| **Expression substrate + unit** | **revised** | `log2(TPM+1)` on "PanCanAtlas RNA-seq" → `log2(RSEM_V2+1)` on per-study cBioPortal PanCanAtlas RSEM (the form PanCanAtlas actually distributes) |
| Sensitivity panel (K±5, lung pooling, frozen APOBEC set, permutation null) | inherited | unchanged |
| Verdict rule / output artifacts | inherited | unchanged |

**Power.** No power-floor change: the amendment does not alter any arm's sample size, the
contrast, or the estimator — only the expression unit label and the per-arm sharding of an
otherwise-identical RSEM matrix.

**Scope of override.** This amendment only *contextualizes* the substrate; it cannot narrow or
override any verdict-bearing decision. All decision criteria remain locked.
