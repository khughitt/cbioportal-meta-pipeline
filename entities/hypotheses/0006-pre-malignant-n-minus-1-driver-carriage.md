---
type: hypothesis
title: Pre-malignant cBioPortal cohorts already carry n-1 of the canonical invasive-cancer
  drivers; residual late-stage drivers are checkpoint-enriched
status: proposed
created: '2026-04-27'
updated: '2026-06-28'
id: hypothesis:0006-pre-malignant-n-minus-1-driver-carriage
phase: candidate
source_refs:
- paper:Martincorena2018
- paper:LeeSix2018
related:
- hypothesis:0004-mhn-pathway-ordering
- question:0012-mutation-ordering-cross-sectional-inference
- question:0041-driver-complexity-vs-median-age-at-diagnosis
- topic:multistage-carcinogenesis-and-age-of-onset
- theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the
- task:t156
- task:t157
- topic:pre-cancer-prevalence-and-impact
---

# Hypothesis: Pre-malignant cBioPortal cohorts carry n-1 of canonical drivers

Project links: this hypothesis is framed by
`question:0012-mutation-ordering-cross-sectional-inference`,
`question:0041-driver-complexity-vs-median-age-at-diagnosis`,
`topic:multistage-carcinogenesis-and-age-of-onset`, and
`theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the`.

## Organizing Conjecture

For cancer types where cBioPortal includes pre-malignant cohorts (Barrett's esophagus → EAC;
MGUS / SMM → MM; MDS → AML; IPMN → PDAC; prostate ASAP / HGPIN → PRAD; colorectal adenomas →
CRC; cervical CIN → cervical carcinoma), pre-malignant samples already carry **a substantial
fraction of the mutation-observable canonical invasive-cancer drivers** of the same lineage.
Concretely: pre-malignant cohorts carry, on average, **n-1 of the top-N mutation-observable
canonical drivers** of their downstream invasive cancer at frequencies within an O(1) factor
of the invasive rate, with a small **residual set of "late-stage drivers"** that are enriched
in invasive vs pre-malignant samples and partially overlap checkpoint genes (TP53, RB1,
cell-cycle).

This is a directly **observed-ordering** hypothesis (paired pre-malignant and invasive
cohorts give direct sequencing evidence of which drivers are present at which stage), so it
is operationally simpler than the `hypothesis:0004-mhn-pathway-ordering` MHN-inferred-ordering route. Where data is
available, this provides a *cleaner* test of the ordering biology than cross-sectional
inference. The two hypotheses are complementary: `hypothesis:0004-mhn-pathway-ordering` covers histologies where pre-malignant
samples are absent or scarce; this hypothesis covers the histologies where they exist.

This is a `phase: candidate` hypothesis. Promotion to active is gated on auditing
cBioPortal study metadata for pre-malignant sample availability.

## Proposition Bundle

### Core Propositions

- **P1 (n-1 carriage).** For each cancer type with paired pre-malignant + invasive cohorts
  in cBioPortal, the pre-malignant cohort top-25 driver-frequency list overlaps the invasive
  cohort top-25 by ≥20 genes after restricting to variants observable by both assay regimes
  and by the current mutation-only pipeline. The "n-1" framing is the median-case
  expectation, allowing some pre-malignant cohorts to lack 2–4 of the invasive drivers.
- **P2 (late-stage residual is identifiable).** The set of drivers enriched in invasive vs
  pre-malignant samples (the "late-stage" set) is small (median ≤ 5 per cancer type) and
  enriched for checkpoint and chromatin / epigenetic genes — TP53, RB1, CDKN2A, ARID1A,
  KMT2D, MLL family — at higher rates than the at-random expectation across the full driver
  list.
- **P3 (frequency calibration).** For drivers carried in both stages, pre-malignant
  frequency is within a 2x band of invasive frequency (i.e. not asymptotically low — these
  drivers are clonally established in pre-malignant samples, not residual / sub-clonal
  signals).

### Supporting Or Auxiliary Propositions

- The "n-1 poised population" framing — invasive cancers re-emerge after targeted treatment
  because n-1 sub-clones already carry n-1 drivers — is a clinical consequence of P1, not
  a separate empirical claim. It is testable separately via post-treatment cBioPortal
  cohorts (Memorial Sloan Kettering MSK-Met, Breast Cancer Met, etc.) that include
  pre-treatment baselines.
- Pre-malignant-stage signature exposures (SBS1 / SBS5 / tissue-specific) more closely
  resemble matched normal-tissue spectra than invasive-stage spectra, providing an
  independent axis on which pre-malignant cohorts are *intermediate* between healthy and
  invasive.

## Current Uncertainty

- **cBioPortal pre-malignant sample coverage is patchy** and not systematically catalogued
  in the project. The first task is enumerating which studies include pre-malignant
  samples and at what sample size. Tractable cancer types are likely a small set
  (esophagus / Barrett's; myeloma / MGUS; prostate / HGPIN; pancreas / IPMN; AML / MDS).
- **Pre-malignant samples in cBioPortal are sequenced with the same panel-vs-WES asymmetry**
  as invasive samples. Comparison must control for assay regime.
- **Modality mismatch matters.** Several clinically central pre-malignant events are CNAs,
  fusions, or translocations (e.g. IgH rearrangements in plasma-cell disorders), but the
  current pipeline is somatic-SNV/indel-first. Either exclude non-mutation events from P1
  or add a separate modality before using them as evidence.
- **Pre-malignant lesions are a heterogeneous category.** Barrett's-with-dysplasia and
  Barrett's-without-dysplasia are biologically different; MGUS and SMM differ in clonal
  burden. Aggregating "pre-malignant" without sub-stratifying may wash out the signal.

## Predictions

- For Barrett's esophagus → EAC pairs in cBioPortal, the BE cohort recovers TP53, CDKN2A,
  SMAD4, and ARID1A at frequencies within 2x of EAC; KRAS and PIK3CA may be lower
  (lineage-divergent), and a clear "late" set including possibly MYC and ERBB2 is enriched
  in invasive.
- For MGUS / SMM → MM, the pre-malignant cohorts recover IgH translocations (t(11;14),
  t(4;14)) and MYC rearrangements at near-MM rates, while TP53 and RB1 are enriched in
  later-stage MM.
- For MDS → AML, FLT3 and NPM1 are enriched in AML over MDS, while DNMT3A, ASXL1, and TET2
  are present at near-AML rates in MDS (these are the CH-overlapping AML drivers — a
  feature, not a bug, since MDS *is* a clonal hematopoietic disorder).
- The residual late-stage set across cancer types is dominated by checkpoint + chromatin
  genes (P2).

## Falsifiability

- If pre-malignant cohorts in any tested cancer type fail to recover ≥20 of the invasive
  top-25 drivers (i.e. <80% overlap), P1 is locally falsified; if this holds across the
  majority of paired cancer types, P1 is globally falsified — pre-malignant cohorts are
  *not* "n-1 driver-carriers" but earlier-stage transitional populations with substantively
  different driver profiles.
- If the late-stage residual is large (median > 10 drivers per cancer type), P2 is
  falsified — the pre-malignant-to-invasive transition is driver-rich, not driver-sparse.
- If the late-stage residual is *not* enriched for checkpoint/chromatin genes (no
  significant enrichment vs background driver list), the biology framing is wrong even if
  P1 holds.
- If pre-malignant frequency is asymptotically lower than invasive (>5x lower for shared
  drivers), P3 is falsified — pre-malignant samples are not clonally established for those
  drivers and the "poised population" framing breaks.

## Promotion criteria

Promote to `phase: active` when:

1. **Pre-malignant cohort audit completes** (new task) — enumerates cBioPortal studies that
   include pre-malignant samples, with sample size, panel/WES regime, and matched-normal
   status documented. Tracked as `task:t156`.
2. **At least 3 paired pre-malignant + invasive cohorts** are identified at sample size
   sufficient (n ≥ 30 pre-malignant per pair) for the top-25 overlap test.
3. **A scoped first analysis** is identified for at least 1 paired set (Barrett's → EAC and
   MDS → AML are the most likely candidates given documented cBioPortal coverage).

## Supporting Evidence

- **Martincorena et al. [@Martincorena2018]:** establish that normal tissue carries driver-positive
  clones at high prevalence; pre-malignant samples are the obvious next step on this
  continuum and should carry even more drivers.
- **Lee-Six 2018 (paper):** colon-crypt phylogenies show driver acquisition is gradual and
  cumulative; the n-1 framing is a direct consequence of slow stepwise acquisition over
  decades.
- **Sottoriva/Turajlic resistance literature (not yet in project library):** post-treatment
  resistance from pre-existing sub-clones — the clinical version of the "n-1 poised
  population" claim.
- **HTAN (NCI Human Tumor Atlas Network):** active research program specifically focused on
  pre-cancers; the existence of this program as an external research direction validates
  the question even where cBioPortal coverage is thin.
- **Canalization synthesis** (`papers/synthesis-2026-04-25-canalization-gene-regulatory-
  networks.md`): the conceptual framing of path-dependent driver accumulation is already in
  the project's literature.

## Disputing Evidence

- **cBioPortal is not designed for pre-malignant work.** Most studies are diagnostic-stage
  invasive samples; pre-malignant cohorts are present in select studies but are not the
  primary data type. Coverage gaps may make the n-1 claim untestable in practice for most
  cancer types.
- **Heterogeneity of "pre-malignant".** Lumping Barrett's-with-dysplasia, Barrett's-without-
  dysplasia, MGUS, SMM, MDS-with-excess-blasts, MDS-low-risk into a single "pre-malignant"
  category is biologically unjustified; per-stage analysis may dramatically reduce sample
  sizes.
- **Selection bias.** Pre-malignant samples that appear in cBioPortal are selected for
  sequencing — typically because they progressed or because the patient was enrolled in a
  surveillance program. They are unlikely to be a representative sample of the
  population-level pre-malignant pool.

## Evidence Needed To Shift Belief

- **cBioPortal pre-malignant audit (gating):** Enumerate studies that include pre-malignant
  samples; report sample sizes, sub-stages, panel/WES, matched-normal status.
- **First paired analysis:** Barrett's → EAC is the most tractable. Recover top-25 drivers
  per cohort; compute overlap; identify late-stage residual; test enrichment of residual
  for checkpoint/chromatin genes.
- **External validation:** Compare against HTAN pre-cancer ↔ invasive pairs for the same
  cancer types where cBioPortal coverage is thin.

## Related Work

- **Sibling hypothesis:** `hypothesis:0004-mhn-pathway-ordering` (MHN-inferred ordering on cross-sectional invasive data —
  this hypothesis tests the same biological claim via observed paired data where
  available; the two hypotheses validate each other where they overlap).
- **Topics:** `topic:pre-cancer-prevalence-and-impact` (frames the broader research
  direction including the population-prevalence / clinical-impact / "n-1 poised population"
  big-version claims).
- **Tasks (planned):**
  - `task:t156`: cBioPortal pre-malignant cohort audit.
  - `task:t157`: first paired driver-overlap analysis on the most tractable cancer type.
- **External:** Sottoriva *Nature Genetics* subclonal-resistance framework;
  TRACERx post-treatment resistance from pre-existing subclones; HTAN
  (NCI program); Maley/Greaves "cancer as evolution" framework.
