# Pipeline Review: h08 within-tissue covariate↔H association core (t199)

- **Plan:** `plan:2026-05-31-t199-h08-association-core`
- **Task:** t199 (analysis-plan check 4; pre-reg-already-exists mode)
- **Date:** 2026-05-31
- **Overall:** **WARN** — structurally sound and correctly avoids relitigating locked criteria, but
  carries **one FAIL-level implementation defect** (Arm-C module commensurability) and **one
  undefined verdict-bearing quantity** (the rank statistic) that must be fixed/frozen *before* WP1
  ranks. Neither requires a pre-reg amendment — both are run-time specifications the pre-reg
  explicitly delegated. **Update (2026-05-31, post-review correction):** the original F2 finding
  (smoking source "Synapse-gated") was **overclaimed and is retracted** — the file is served
  open-access from the GDC `/data` endpoint with no auth (verified). F2 is reframed as a
  plan-precision fix (name the concrete endpoint + verification), and all findings are now patched
  into the plan (commits below).

> Sub-plan handling: this plan sits under `pre-registration:h08-positive-control` +
> `plan:2026-05-31-h08-positive-control-scan`, which already passed methodological review.
> Dimension 1 (Evidence Coverage) and Dimension 7 (Scope) are **inherited from the parent** and
> spot-checked only. Review effort is concentrated on Dimensions 2, 3, 4, 6, 8.

## Summary

The plan is the right shape (design-mode, pre-reg-already-exists) and its standout strength is that
it surfaced three real provenance facts at plan time (smoking absent from cBioPortal clinical, UV
proxy coarse + 82% metastatic, no `samples_annotated` for this run). But three issues survived,
verified against the on-disk artifacts during this review: the **pooled Arm-C model cannot carry the
NMF expression modules** (they are tissue-specific, non-commensurable, and differ in K — SKCM=5,
BRCA=10) and the **rank statistic itself is never defined**. Because the rank-gate denominator and
the rank are verdict-bearing, both must be resolved and frozen before WP1. A third drafted finding
(smoking source "Synapse-gated") was **wrong and is retracted** — the GDC `/data` endpoint serves
the file open-access; the residual is a plan-precision fix (concrete endpoint + verification step).

## Rubric Results

| Dimension | Score | Issues |
|---|---|---|
| Evidence coverage | PASS (inherited) | Parent pre-reg sources the gate params; new construction choices (UV ordinal, hypermutator threshold) flagged as open, Campbell-2017 sourced |
| Assumption audit | **WARN** | CLR sign ≠ unconditional "more signature" (F5); per-arm adjustment-set degeneracy unstated (F10) |
| Data availability | **WARN** | F2 retracted — smoking file IS GDC open-access (verified); residual: name concrete endpoint + verify (F2′); no dataset backlinks / no smoking entity (F6) |
| Identifiability | **WARN** | Arm-B miss collapses the 2-of-3 tolerance to "A∧C", hinging `[+]` on the by-design weakest arm (F3) |
| Reproducibility | WARN | Permutation seed key, n_permutations, and stats library/version unspecified (F8) |
| Validation criteria | **WARN** | Rank statistic undefined (F4); "base rate" column ill-defined for continuous covariates (F9) |
| Scope check | PASS (inherited) | In scope; no gated data **provided the smoking route is switched** (couples to F2) |
| Integration boundaries | **FAIL** | Arm-C cannot carry per-tissue NMF modules — non-commensurable, different K (F1); join dedup rule unstated but verified low-risk (F7) |
| Manifest completeness | PASS | datapackage.json update + resources covered in WP4 |

## Detailed Findings

### F1 — [CRITICAL, Dim 8] The pooled Arm-C model cannot include the NMF expression modules

**Verified on disk.** Each arm's module loadings are an independent NMF basis: columns are
`module_01..module_K` with **arm-specific K** (SKCM/LUAD/LUSC/BLCA/CESC/HNSC = 5, BRCA = 10), and
`module_01` in SKCM is a *different latent factor* than `module_01` in LUAD. The pre-reg's Arm C is a
**single pooled within-tissue model across {BLCA,BRCA,CESC,HNSC,LUAD,LUSC}** yielding *one* APOBEC3A/B
rank. There is no shared "module_01" across those six tissues — the modules are non-commensurable and
not even equal in count — so expression modules **cannot enter the pooled Arm-C covariate set** as
ranked covariates.

Why it is verdict-bearing: the rank gate is "rank ≤ 3 among all covariates tested vs SBS2/13." The
covariate-count denominator therefore differs between Arm C (pooled, modules excluded from the ranked
set) and Arms A/B (single-tissue, modules included). The pre-reg froze the denominator "by rule,
realized at run time" — but it did *not* resolve this pooled-vs-stratified module question, and the
plan inherited the ambiguity.

**Recommendation.** In WP1, freeze an explicit rule (before any rank) and write it into
`covariate_denominator.json`: for the pooled Arm-C model, expression modules enter only as
**tissue-nested nuisance terms** (or are omitted) and are **excluded from the ranked covariate
denominator**; the commensurable covariates (clinical, molecular, the joint APOBEC3A/B expression
score) form the Arm-C ranked set. Per-tissue Arm-C runs (which *can* carry that tissue's modules)
remain sensitivity-only, never a pass route — already the pre-reg rule. State the resulting two
distinct denominators (per-tissue arms vs pooled Arm C) in the plan and report both at run time.
Confirm this does not need an amendment (it does not — it is a run-time denominator rule the pre-reg
delegated), but record the reasoning in the verdict note.

### F2′ — [RETRACTED → MINOR, Dim 3] Smoking source is GDC open-access; name the endpoint + verify

**Original finding RETRACTED.** A review draft claimed `clinical_PANCAN_patient_with_followup.tsv`
was Synapse-gated. That was **wrong** — it conflated the GDC `/files` *metadata* index (which does
not carry this legacy supplement object) with the `/data` *download* route (which **does** serve it
open-access, no auth). **Re-verified this turn:** a `curl` range request to
`https://api.gdc.cancer.gov/data/0fc78496-818b-4896-bd83-52db1f533c5c` returned the TSV header with
`tobacco_smoking_history` (col 78) and `number_pack_years_smoked` (col 79), 232 columns, pan-cancer.
The file is **ungated** and consistent with the no-gated-access constraint.

**What survives as a real (minor) finding.** The plan's *prose* mis-described the route ("public GDC
publications page" browsing) and gave no concrete endpoint or download verification. KD3/WP0 are
patched to: target the exact GDC `/data` UUID; treat WP0 as a **hard, first-sequenced gate** (F3
still holds); verify size ≈18,633,685 B + md5 + smoking columns + LUAD/LUSC non-missingness before
WP1 consumes it; register a `dataset:tcga-pancanatlas-clinical` entity with the backlink. BCR Biotab
/ GerkeLab mirror are demoted to **fallbacks** used only if the GDC direct file becomes unavailable.

### F3 — [CRITICAL, Dim 4] An Arm-B miss collapses the 2-of-3 tolerance

The 2-of-3 gate was designed so the noisiest arm (C, APOBEC) can miss. But Arms A and C are the two
*proxy-weak* arms (coarse UV labels; steady-state mRNA vs episodic kataegis), and Arm B (smoking) is
the only arm with a reasonably direct covariate. If WP0 fails to deliver smoking ungated, Arm B
becomes untestable and the gate degenerates to **"A and C must both pass"** — forcing a `[+]` to hinge
on the by-design weakest arm and removing the slack the 2-of-3 rule exists to provide. This makes WP0
a **hard sequencing gate**, not a parallel nicety.

**Recommendation.** Sequence WP0 first and treat smoking acquisition as blocking. The covariate **is**
obtainable ungated (GDC `/data`, verified — F2′), so the expected path is fine; but if the file ever
becomes unavailable, that is a `not-runnable` condition to escalate, *not* a silent drop to a two-arm
gate. **Patched** into WP0's definition-of-done.

### F4 — [MAJOR, Dim 6] The rank statistic is undefined

The plan never specifies *how* each covariate's "effect against a signature" is computed for ranking:
separate adjusted within-tissue regressions per covariate (rank by signed standardized coefficient),
or one multivariable model (rank by coefficient within it). These produce different ranks and, with a
multivariable model, collinear covariates distort each other's coefficients. This is the single most
verdict-bearing undefined quantity.

**Recommendation.** Freeze in WP1 (before ranks): per covariate, an adjusted within-tissue model with
the **CLR coordinate of the target signature** as outcome and the adjustment set as covariates;
ranking statistic = the **signed standardized coefficient** of the covariate (sign read directly,
magnitude = |standardized coef| or the Wald |z|); BH-q from that model's covariate p-value. One model
per (covariate, signature, stratum) cell keeps the rank interpretable and avoids collinearity
artifacts. Write the chosen estimator into `covariate_denominator.json` alongside the frozen
denominator.

### F5 — [MAJOR, Dim 2] CLR sign is relative, not absolute

A positive association on the CLR coordinate of SBS7 means "more SBS7 *relative to the per-sample
geometric mean of active signatures*," not unconditionally "more SBS7." This is usually concordant
with the pre-reg's "positive sign" expectation, but can diverge when the covariate also shifts the
compositional mean.

**Recommendation.** State that the confirmatory sign is read on the CLR coordinate and **corroborated
by the absolute-burden sensitivity re-run** (already in WP3); flag any CLR-vs-absolute sign discordance
as a `[?]`-triggering condition for that arm. No criterion change — this is the documented
compositional precision gate.

### F6 — [MAJOR, Dim 3/9] Dataset backlinks (plan-pipeline Step 4.5) were skipped

No `consumed_by: plan:2026-05-31-t199-h08-association-core` was appended to `dataset:tcga-mc3` /
`dataset:tcga-pancanatlas`, and no entity exists for the smoking source.

**Recommendation.** Add the `consumed_by` backlink to the two existing dataset entities and create
the smoking-source entity (F2) via `/science:find-datasets`, with a verification-log line.

### F7 — [MINOR, Dim 8] Exposure→covariate join dedup rule unstated (verified low-risk)

The exposure key is the **28-char MC3 aliquot** (`TCGA-2F-A9KO-01A-11D-A38G-08`); modules + clinical
use the **15-char** sample barcode. The join requires slicing to 15 char. **Verified:** SKCM has
466 exposure rows per signature = 466 distinct 15-char = 466 distinct cases (no collision), and the
sample-type code (01/06) is *inside* the 15-char key, so the 82%-metastatic clinical aligns correctly
to the MC3-sequenced sample. Risk is low but the rule is implicit.

**Recommendation.** Assert "one MC3 sample per case, sample-type-aware 15-char key" in WP1 and
fail loudly if any case retains >1 sample after the collapse (check all 7 arms, not just SKCM).

### F8 — [MINOR, Dim 5] Reproducibility specifics missing

Permutation null: no seed key, no permutation count. Modeling library/version unnamed.

**Recommendation.** Name `h08_permutation_seed` (derive from `random_seed`), fix n_permutations
(e.g. 1000), and pin the stats library (statsmodels) via uv.lock; record both in the datapackage.

### F9 — [MINOR, Dim 6] "Base rate" is ill-defined for continuous covariates

The §1b table's "base rate" column is meaningful for binary covariates (treatment flag, hypermutator,
MSI-H) but not for continuous ones (pack-years, APOBEC3A/B mRNA, UV ordinal).

**Recommendation.** Define per covariate type: base rate (prevalence) for binary; completeness +
a distribution summary (median/IQR, % non-zero) for continuous.

### F10 — [MINOR, Dim 2] Per-arm adjustment-set degeneracy

Arm A (SKCM) is a single tissue within a single MC3 study, so {tissue, study/assay} are constant and
drop out, leaving {ancestry, treatment, sample_type}. Entering constant terms yields a rank-deficient
design.

**Recommendation.** Note in the plan that the adjustment set is *realized per arm* — constant columns
dropped — to avoid singular design matrices; this is mechanical, not a criterion change.

## Recommendations (priority order) — all patched into the plan this turn

1. **F1** — freeze the Arm-C module-exclusion / tissue-nesting rule and the two distinct denominators
   in WP1, before any rank. (Verdict-bearing; no amendment needed but must be documented.) **Done.**
2. **F2′ + F3** — target the concrete GDC `/data` UUID, sequence WP0 as a hard first gate, verify on
   disk (size + md5 + columns + LUAD/LUSC non-missingness), register the entity; BCR Biotab/GerkeLab
   as fallbacks only. **Done.**
3. **F4** — freeze the rank statistic (per-covariate adjusted CLR-coordinate model, signed
   standardized coefficient) in WP1/WP2. **Done.**
4. **F5, F6** — read confirmatory sign on CLR + corroborate with absolute burden (sign discordance →
   `[?]`); add dataset backlinks. **F5 done; F6 folded into WP0/WP1 entity registration.**
5. **F7–F10** — assert the one-sample-per-case dedup, pin permutation seed/count + stats version,
   type the §1b columns per covariate, realize the adjustment set per arm. **Done.**

## Strengths

- Correctly operates in pre-reg-already-exists mode — re-derives **no** locked criterion and routes
  any criterion doubt to amendment.
- The leakage firewall is already enforced upstream (t198 NMF never saw `H`), and the
  frozen-denominator-before-ranks discipline is baked into WP1.
- The three provenance findings (smoking absence, UV coarseness + metastatic dominance, missing
  `samples_annotated`) were caught at plan time, not at run time.
- Sensitivity variants are implement-don't-invent (K±5, lung pooling, frozen APOBEC set, permutation
  null, absolute-burden basis); datapackage + interpretation note are scoped.
- Reusable infrastructure (covariate table + CLR grid engine) correctly flagged for H08b reuse.

## Sources

- GDC open-access download endpoint (verified, no auth):
  `https://api.gdc.cancer.gov/data/0fc78496-818b-4896-bd83-52db1f533c5c` — header carries
  `tobacco_smoking_history` (col 78) + `number_pack_years_smoked` (col 79), 232 cols, pan-cancer.
- [GDC PanCanAtlas Publications](https://gdc.cancer.gov/about-data/publications/pancanatlas) — lists
  the clinical-with-followup file under Supplemental Data with open-access instructions.
- [GerkeLab/TCGAclinical](https://github.com/GerkeLab/TCGAclinical) — public mirror of the same GDC
  PanCanAtlas clinical file (fallback route).
- Retraction note: an earlier draft cited [Synapse syn7343873](https://www.synapse.org/Synapse:syn7343873)
  as the *required* route; that was incorrect — Synapse hosts a copy, but the GDC `/data` route is
  open-access and is the primary source.
