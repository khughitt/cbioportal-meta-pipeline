---
type: plan
title: "Analysis plan \u2014 positive-control scan (H08a recovery gate)"
status: not-ready
created: '2026-05-31'
updated: '2026-05-31'
id: plan:0005-h08-positive-control-scan-analysis-plan
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- method:h08-agnostic-association-model
- pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature
- question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross
- task:t195
- task:t178
- task:t179
- task:t180
- task:t181
skills_loaded:
- id: data-genomics-mutational-signatures-and-selection
  reason: SBS per-sample exposure refit (H) is the outcome; opportunity model, COSMIC
    pinning, low-count + positive-control QA
- id: data-genomics-somatic-mutation-qa
  reason: MC3 MAF input-call + denominator QA is prerequisite to treating the refit
    as verdict-bearing
- id: data-expression-bulk-rnaseq-qa
  reason: PanCanAtlas RNA-seq is the substrate for the frozen NMF expression-module
    covariate set
- id: statistics-compositional-data
  reason: per-sample exposures H are sum-constrained; prereg's suspicious-result plan
    requires a CLR/ILR or absolute-burden guard
- id: statistics-power-floor-acknowledgement
  reason: "realized per-arm effective n (post MC3\u2229clinical / MC3\u2229RNA-seq\
    \ join) is unfilled and gates the read"
- id: statistics-sensitivity-arbitration
  reason: "prereg pre-commits K\xB15, lung-pooling, and APOBEC-tissue-set sensitivity\
    \ variants"
---

# Analysis Plan — Positive-control scan (H08a recovery gate)

> **This plan operates in pre-registration-already-exists mode.** The verdict surface is
> **locked** in `pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature` (committed 2026-05-30): three
> confirmatory arms, top-3 rank / positive sign / FDR q<0.05 per arm, a 2-of-3 gate, the
> frozen Arm-C tissue set + pooled-rank rule, COSMIC v3.4, the NMF expression-module K-selection
> rule, the active-signature ≥5% rule, the compositional + permutation pre-acceptance checks,
> and the canonical `[+]/[?]/[-]` mapping onto H08a. **None of those criteria are re-derived
> here.** Per the skill, this plan covers only the *implementation gates* the pre-reg did not
> enumerate: data provenance, the per-sample refit + join materialization, the expression-module
> build, leakage checks, numerical/compositional precision, and the two named activation gates.
> Any belief that a locked criterion is wrong is an **amendment** question
> (`statistics-prereg-amendment-vs-fresh`), not a planning decision.

## Analysis Question

Does the agnostic within-tissue covariate↔signature-exposure scan, run on the MC3 WES
substrate with no aetiology labels, **recover the textbook exposure→signature links unprompted**
— UV→SBS7 (SKCM), smoking→SBS4 (LUAD+LUSC), APOBEC3A/B mRNA→SBS2/13 (pooled APOBEC-prevalent
tissues) — at the pre-registered rank gate? (H08a positive control.)

## Related Hypotheses / Inquiries / Tasks

- `hypothesis:0007` (prong H08a) — `method:h08-agnostic-association-model` — `pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature`.
- Activation gates named by the pre-reg: `task:t177` (**DONE** — prior-art scan landed) and
  `question:0018` (feasibility verdict — **OPEN, empty stub**).
- Covariate-spec tasks that feed the association layer: `task:t180` (joint APOBEC3A/B + MMR-omikli),
  `task:t181` (treatment-exposed confound stratum). These are inputs, not gates on H08a's run.
- Substrate hardening already shipped: `task:t178` / `task:t179` (COSMIC v3.4 pin, count floor,
  caller-consensus flag, refit/de-novo decision).
- Umbrella task: `task:t195`.

## Data Inputs and Provenance

| Input | Role | On disk? | Access |
|---|---|---|---|
| `data/mc3.v0.2.8.PUBLIC.maf.gz` (718 MB, 3.6M rows) | SBS96 spectra → per-sample exposures `H` | **yes** | public (GDC PASS release) |
| `data/tcga_case_to_project.tsv` | case→TCGA project (stratum identity) | **yes** | public (GDC API) |
| TCGA PanCanAtlas RNA-seq (log2 TPM) for MC3-overlapping samples | NMF expression-module covariates | **NO — not materialized** | **public** (GDC/cBioPortal); not gated |
| TCGA clinical: SKCM anatomic site; lung pack-years/smoking history; stage/sex/race/age | structured covariates + UV/smoking proxies | partial (per-study cBioPortal clinical) | public |
| APOBEC3A / APOBEC3B mRNA | Arm C covariate | derived from the RNA-seq substrate above | public |

**Access verdict: nothing here is gated.** The positive-control scan is fully consistent
with the "no gated data access" constraint — the blocked WGS-tier cohorts (Hartwig t166, GTEx
t169) are irrelevant to H08a. The expression matrix is *un-built*, not *inaccessible*.

## Required Input Inspection

Prerequisite — run `data-genomics-somatic-mutation-qa` on MC3 **before** the refit is
verdict-bearing (the signatures leaf requires it):
- PASS-filter handling, duplicate `Tumor_Sample_Barcode`, genome build (GRCh37) consistency,
  trinucleotide-context recoverability for SBS96.
- Per-sample callable-territory / opportunity model for the WES exome denominator (the
  signatures leaf's halt-on: "opportunity model unknown").
- Confirm the **§1b PASS-bearing sample counts** reproduce (SKCM 466, LUAD 513, LUSC 480,
  BLCA 411, BRCA 791, CESC 289, HNSC 507) — the pre-reg's independently-verified lower bound.

Signature refit QA (`data-genomics-mutational-signatures-and-selection`):
- COSMIC **v3.4** pinned (locked by prereg §Total Comparison Count; `t178` asserts at run time —
  note the AGENTS.md / method-doc "v3.5 default" is overridden to v3.4 for this run per commit
  `6dc4270`). Store the exact catalog file / checksum.
- Reconstruction error + total mutations per spectrum; `passes_count_floor` (t179) flags, not
  drops, sub-floor samples (loud missingness).
- Positive-control / forbidden-signature sanity (SBS7 should be huge in SKCM; SBS4 absent in
  brain — a cross-check that the refit is wired correctly).

Expression-matrix QA (`data-expression-bulk-rnaseq-qa`) before NMF:
- Sample-ID harmonization MC3 `Tumor_Sample_Barcode` ↔ PanCanAtlas aliquot/sample barcodes;
  record the realized intersection per arm (this sets effective n).
- Standard bulk filters per the frozen rule: drop genes expressed in <10% of samples, retain
  top-2,000 MAD genes, log2(TPM+1). Batch/plate confounding check.

## Preprocessing / Normalization Checks

- **Opportunity normalization:** WES exome opportunity for SBS96; do not pool with any panel
  spectra (the model excludes panels from per-sample H — the binding
  `question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross` constraint).
- **Compositional transform of H** (`statistics-compositional-data`): per-sample exposures are
  sum-constrained → closure-induced spurious anti-correlation. Pre-reg's suspicious-result plan
  mandates modeling **absolute per-signature burden or a CLR/ILR transform**, not closed
  proportions. Document the **pseudocount / zero-handling rule** and distinguish structural zeros
  (signature genuinely absent) from sampling zeros (low count). Repeat the key arm contrasts under
  ≥1 alternative log-ratio basis (this is a numerical-precision gate, not a criterion change).
- **Expression modules:** NMF on the filtered log2(TPM+1) matrix per arm, K selected by Brunet
  cophenetic ≥0.90 over K∈{5,10,…,50}×50 restarts, computed on the **expression matrix alone**
  (never sees H or covariates — leakage firewall). Write K + per-K cophenetic curve **before** any
  rank.
- **Treatment stratification** (`t181`): flag iatrogenic-signature-bearing / relapse cohorts
  (SBS11/31/35/87) as a confound stratum before the scan; do not silently pool primary + treated.

## Independent Unit and Denominator

- **Independent unit:** the tumor sample (one MC3 `Tumor_Sample_Barcode` per TCGA case; dedup to
  one sample/case). No repeated-measures structure within arm.
- **Estimand denominator (rank gate):** the **covariate-count denominator** per stratum — frozen
  by rule (covariate universe ∪ K expression modules ∪ derived molecular features), realized
  integer reported at run time. The top-3 threshold is meaningless without this denominator, so it
  is computed and frozen **before** any rank (prereg §Metric Selection Rationale).
- **Compositional denominator:** total per-sample SBS burden (the closure constraint on H).

## Estimand and Primary Metric

Locked by pre-reg — restated, not re-derived: per (signature, covariate) pair, the **within-tissue
association between a covariate and a signature's per-sample exposure `H`** (burden, not spectrum
`W`). **Primary metric: rank position** of the known covariate among all tested covariates for its
matching signature within the tissue stratum, with sign and FDR q-value as qualifiers. Pass =
rank≤3, positive, q<0.05; gate = 2-of-3 arms.

## Model / Test Assumptions

- Within-tissue model (tissue as fixed-effect stratifier); Arm C is a **single pooled within-tissue
  model** across {BLCA,BRCA,CESC,HNSC,LUAD,LUSC} yielding **one** APOBEC3A/B rank (per-stratum ranks
  are sensitivity-only, explicitly **not** an alternative pass route).
- Adjustment set {tissue, treatment, study/assay, ancestry}; unconditioned version reported only to
  quantify R1 tissue collinearity (Prediction 4, exploratory).
- BH-FDR across the full covariate×signature×stratum grid; confirmatory arms read at q<0.05.
- Assumption risks to check at run: (a) APOBEC steady-state mRNA decorrelates from episodic
  kataegis; (b) coarse/missing SKCM anatomic-site labels; (c) never-smoker LUAD dilution. All three
  are pre-registered Known Limitations the 2-of-3 + top-3 band is designed to tolerate.

## Power Floor or Resolution Limit

- Raw-n is comfortably powered for arms A (SKCM ~466) and B (lung ~993) for textbook-magnitude
  effects. **Arm C's effective n is the one most eroded by the MC3∩RNA-seq intersection** — the
  pre-registered tolerated miss under 2-of-3.
- **The §1b post-join n / covariate completeness / base-rate table is an explicit activation
  precondition: "the gate is not read until [these three numbers] are filled in."** They cannot be
  computed today (no joined table exists). Materializing them is a blocking check, not a criterion.

## Bias vs Variance Risks

- **Leakage (variance→false-positive):** APOBEC3-locus mutations that both inflate APOBEC3 mRNA and
  are themselves SBS2/13 calls — pre-reg names this; implement an explicit exclusion/flag so the
  covariate and outcome are not two measurements of one event.
- **Closure bias:** addressed by the compositional transform above.
- **Batch/assay (R4):** study/assay as nuisance covariate + artifact-signature flag (SBS27/43/45–60).
- **Bias audits** (signatures leaf): stratify by hypermutator class; confirm SBS7/SKCM and SBS4/lung
  are not driven solely by a handful of ultra-hypermutators.

## Sensitivity Arbitration

Pre-committed in the pre-reg (`statistics-sensitivity-arbitration` — implement, don't invent):
- **K±5** expression-module count: re-run the full scan; an arm verdict that flips under K±5 is
  **downgraded to `[?]`**.
- **Lung pooling:** LUAD+LUSC pooled vs per-histology (registered variant for a failing Arm B).
- **APOBEC tissue set:** the frozen six only; no post-hoc expansion/substitution.
- **Pre-acceptance for a "too good" result:** within-stratum **permutation null** (shuffle covariate
  within tissue, refit, confirm observed rank exceeds null) **and** the compositional-basis re-run —
  an unexpectedly strong result is not accepted until both pass.

## Required Output Artifacts

- Per-sample exposure table `H` across the 7 arm strata (+ `*.signature_audit.feather` /
  `*.denovo_decision.feather` sidecars from t178/t179).
- Expression-module artifacts: NMF modules, selected K, per-K cophenetic curve (written pre-association).
- Association grid: effect sizes, signs, ranks, BH-q, per-stratum covariate/signature denominators.
- The **filled §1b table** (post-join n, completeness, base rate per arm).
- Compositional QA bundle (denominator, zero-handling, basis-sensitivity) + permutation-null result.
- Arm A/B/C verdicts → H08a `[+]/[?]/[-]`; secondary controls (MMR/MSI→SBS6/15/26, POLE→SBS10) as
  corroboration only; R1 unconditioned contrast (exploratory).
- A `datapackage.json` for the run directory (closes the recurring provenance gap; cf. t128).

## Aspect-contributed Sections

`computational-analysis`: the association layer is non-trivial orchestration (refit × 7 strata →
NMF module derivation → join → grid scan → permutation/K-sensitivity re-runs). After the blocking
checks below clear, route execution design to **`/science:plan-pipeline`** rather than an ad-hoc
script — and wire the run into Snakemake per `t175` if it becomes recurring.

## Readiness Decision

**not-ready** — but specifically in the pre-reg's own sense: *runnable-now, engineering-gated, NOT
data-gated, NOT methodology-gated*. The verdict surface is locked and the data is on hand or
publicly buildable; what is missing is (1) two named activation gates and (2) four unbuilt
engineering pieces. No gated-access dependency, so this is the right task to pursue under the
current affiliation constraint.

### Blocking Checks Before the Scan Can Run

1. **`question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross` feasibility verdict (activation gate).** Write the answer: per-sample SBS refit
   soundness on MC3 WES + panel-adequacy exclusion rule. Largely answerable from the t178/t179
   hardening + the existing brca-subset refit; needs the written verdict committed. *(new task)*
2. **Full-MC3 per-sample SBS refit across the 7 arm strata** (SKCM, LUAD, LUSC, BLCA, BRCA, CESC,
   HNSC) with the t178/t179-hardened script at COSMIC **v3.4**, materialized as one joined
   per-sample `H` table + sidecars. Today only the brca-2026-04-22 subset exists. *(new task)*
3. **Expression substrate + NMF module layer.** Stage public PanCanAtlas RNA-seq for MC3-overlapping
   samples per arm; build the frozen NMF-K module pipeline (log2(TPM+1), top-2,000 MAD, ≥10%
   expressed, K∈{5..50}×50 restarts, cophenetic≥0.90); write K + curve before any association.
   *(new task)*
4. **Covariate join + within-tissue association layer** (the core; no script exists). Joins clinical
   (SKCM anatomic site; lung pack-years; APOBEC3A/B mRNA via `t180`) + molecular (TMB, hypermutator,
   POLE, MSI) + treatment flag (`t181`); CLR/absolute-burden transform; BH-FDR over the full grid;
   rank + sign + q; APOBEC-locus leakage guard; permutation null; K±5 / lung-pooling sensitivity
   variants; fills the §1b activation table. Hand execution design to `/science:plan-pipeline`.
   *(new task)*

Checks 1 (`question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross`) and 2 (refit) are the near-term unblockers; 3 and 4 are the larger builds. `t180`
and `t181` are existing covariate-spec tasks that feed check 4 — not duplicated here.

## Feedback Reflection

Reported via `science feedback` (see command log): the plan-analysis "pre-registration already
exists" inversion worked well here and kept the plan from relitigating a dense locked criterion set;
one friction worth noting is that the pre-reg lived under `doc/meta/` rather than a
`specs/pre-registrations/` path, so the standard setup-step glob did not surface it — it was found
only by grepping the id.
