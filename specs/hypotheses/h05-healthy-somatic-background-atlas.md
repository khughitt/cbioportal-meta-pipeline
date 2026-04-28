---
id: "hypothesis:h05-healthy-somatic-background-atlas"
type: "hypothesis"
title: "Healthy somatic-mutation backgrounds vary >2 OoM across tissues; substituting a cross-tissue normal null shifts cBioPortal driver-frequency in calibrated, tissue-specific ways"
status: "proposed"
phase: "candidate"
source_refs:
  - "paper:Martincorena2018"
  - "paper:LeeSix2018"
  - "paper:Li2021"
  - "paper:Yaacov2023"
  - "paper:Yoshida2026"
related:
  - "hypothesis:h01-non-tumor-signal-contamination"
  - "question:q007-cross-tissue-somatic-mutation-rate-variation-as-null-model"
  - "task:t150"
  - "task:t151"
  - "topic:normal-tissue-mutation-atlas"
created: "2026-04-27"
updated: "2026-04-28"
---

# Hypothesis: Healthy somatic-mutation backgrounds, characterized cross-tissue and cross-age, are a substantively different null than the project currently uses

## Organizing Conjecture

The cancer-genomics literature has invested heavily in cataloging mutations in tumors and
relatively little in characterizing what "background" looks like in apparently-healthy
individuals across tissues and ages. Single-tissue normal-mutation studies exist
(Martincorena 2015 skin / 2018 esophagus; Yokoyama 2019 esophagus; Lee-Six 2018/2019 colon
+ blood; Moore 2020 endometrium; Brunner 2019 liver; Yoshida 2020 lung; Li 2021 multi-tissue
body-map; Cagan 2022 cross-species; Park 2024 mutation clocks), but **a consolidated
cross-tissue, age-stratified normal somatic-mutation atlas does not exist in unified form**.

This hypothesis claims that (a) when consolidated via meta-analysis, healthy somatic-mutation
backgrounds vary by **>2 orders of magnitude across tissues** and scale interpretably with
tissue cell-turnover rate; (b) the prevalence of driver-mutation-positive clones in
apparently-healthy tissue **at age 70+ exceeds the per-tissue cancer-discovery rate** for
several tissues — i.e. driver-positive clonal expansion is the population norm, not the
pathological exception; and (c) substituting this cross-tissue normal null for the current
within-pipeline null produces calibrated, tissue-specific shifts in apparent
driver-frequency in cBioPortal unmatched-normal studies, with magnitude predictable from
the pre-meta-analyzed normal mutation rate.

This is a `phase: candidate` hypothesis. It generalizes `h01` from "contamination correction
within a sample" to "background as positive cross-population knowledge." Promotion to active
is gated on a feasibility audit of the available normal-tissue WGS cohorts.

## Proposition Bundle

### Core Propositions

- **P1 (cross-tissue rate variation).** Published normal-tissue sequencing studies imply
  large cross-tissue differences in per-cell-per-year SNV rates, plausibly approaching or
  exceeding 2 orders of magnitude after age and exposure adjustment. The exact range is a
  target of the feasibility audit, not a settled project result.
- **P2 (clone prevalence).** Driver-mutation-positive clonal expansions are present in
  apparently-healthy tissue at frequencies that, by age 70, **exceed the per-tissue cancer
  discovery rate** for at least 3 tissues (esophagus, skin, colon are the strongest
  candidates from existing literature). This is the population-prevalence statement of
  "cancer is the small-N tail of a continuum."
- **P3 (project-tractable claim).** When the meta-analyzed cross-tissue normal null is
  substituted for the project's current null (length, dNdScv background, panel-callability),
  the apparent driver-frequency in unmatched-normal cBioPortal studies shifts by amounts
  that are (a) tissue-specific, (b) larger for the at-risk genes flagged by `h01` (CH +
  normal-tissue + CFS), and (c) calibrated by the underlying normal mutation rate of the
  matched tissue.

### Supporting Or Auxiliary Propositions

- The age-stratified rate (P1) follows roughly linear accumulation in cell-by-cell
  phylogenies (Lee-Six 2019), supporting a near-constant per-cell-per-year mutation rate
  across the lifespan.
- Inter-tissue rate variation correlates with stem-cell-turnover estimates (Tomasetti &
  Vogelstein 2015 lifetime stem-cell-division-count tables), giving a mechanistic anchor.
- The per-tissue normal-clone driver landscape partially overlaps the per-tissue cancer
  driver landscape, with characteristic exceptions: NOTCH1 dominates normal esophagus more
  strongly than esophageal cancer (Martincorena 2018); TP53 is rare in normal but common
  in cancer; lineage-specifying drivers (KRAS in lung, APC in colon) show modest normal-
  clone presence.

## Current Uncertainty

- **Data harmonization is the unsolved problem.** Each normal-tissue cohort uses a different
  sequencing depth, caller, dissection protocol, sample-size, and age range. A meta-analysis
  requires either accepting heterogeneity as random effect, or restricting to a uniform-ish
  subset (e.g. WGS-only, post-2018, with raw VCFs available).
- **Coverage gap.** The published cohorts cover ~10 tissues (esophagus, skin, colon, blood,
  endometrium, liver, lung, breast, prostate, brain) at varying depth; cBioPortal cancer
  types span 30+ tissues. Several major cancer-tissue contexts (kidney, thyroid, pancreas)
  have thin or no normal-mutation reference data.
- **Identifiability of "driver-positive clones at age 70 vs cancer rate".** The clone
  frequency is a function of biopsy size and detection sensitivity; cancer incidence is a
  population-level number from cancer registries. Comparing them on a common axis requires
  modeling, not just direct comparison.
- **Risk of duplicating Cagan 2022 / Park 2024.** The cross-species and aging-clock work
  has covered some of this ground; the project-specific contribution must be the
  *human-cross-tissue* atlas focused on cancer-relevant tissues with cBioPortal-aligned
  cancer-type mappings.

## Predictions

- Meta-analyzed normal mutation rate, per tissue, scales with stem-cell-turnover proxy
  (R² ≥ 0.5 across tissues with both data points).
- Esophageal NOTCH1 driver-clone frequency in apparently-healthy individuals at age 70+ is
  comparable to or exceeds the population-incidence-adjusted esophageal-cancer NOTCH1 rate.
- Colon APC and TP53 driver-clone frequencies in apparently-healthy individuals at age 70+
  exceed the colorectal-cancer incidence rate at the same age.
- Substituting the meta-analyzed normal null in `h01`'s P3 test increases the
  matched-vs-unmatched rate-gap drop by ≥30% over the current within-pipeline null on
  esophageal, breast, and colon studies.

## Falsifiability

- If the cross-tissue normal mutation rate range is <1 order of magnitude after harmonized
  meta-analysis (i.e. tissues are more uniform than expected), P1 is falsified — the
  project's tissue-specific framing of "background" is overengineered.
- If driver-clone frequency at age 70 in any tested tissue is consistently below cancer
  incidence, P2 is falsified for that tissue — the framing of "cancer as continuum tail"
  does not apply uniformly.
- If substituting the cross-tissue normal null produces *no* improvement over the current
  null on the `h01` test, P3 is falsified — the cross-tissue level of detail does not buy
  predictive power on this data.

## Promotion criteria

Promote to `phase: active` when **all three** are met:

1. **Feasibility audit completes** (new task) — enumerates available normal-tissue WGS
   cohorts (n_studies, n_samples, age range, sequencing depth, public availability), maps
   each to cBioPortal cancer-type contexts, and identifies the harmonization regime
   (uniform-subset vs random-effects-meta-analysis). Tracked as `t150`.
2. **At least 6 cBioPortal-relevant tissues** are covered by the audit at a sample size
   sufficient for per-decade age stratification.
3. **A scoped first analysis** is identified that tests P3 on at least 1 tissue (likely
   esophagus or colon, given existing data density), with a pre-registered effect-size
   target.

## Supporting Evidence

- **Martincorena 2018 (paper):** NOTCH1 in normal esophagus at >10% clonal-coverage by age
  60+; the canonical "normal tissue is full of driver-positive clones" result. Direct
  evidence for P2 in esophagus.
- **Lee-Six 2018 (paper):** colon-crypt phylogenies; per-cell-per-year SNV rate; clonal
  expansion landscape across the colon. Direct support for P1 + P2.
- **Li 2021 (paper):** body-map across 9 tissues; the closest existing cross-tissue
  reference. Identified as an under-exploited resource in `q007`. Direct support for P1.
- **Yaacov 2023 (paper):** SBS1 replication-timing bias in normal tissue, used in q009.
  Direct support for "normal-tissue mutation patterns are systematic and characterizable."
- **Yoshida 2026 / Xu 2025 (papers, project library):** project-relevant normal-tissue and
  CH analyses; methodological references.
- **Project synthesis** `papers/synthesis-2026-04-18-somatic-mutations-in-normal-tissue.md`:
  cross-paper synthesis already in the project library.

## Disputing Evidence

- The published normal-tissue cohorts are heterogeneous in design (different sequencing
  depths, callers, age ranges), and several recent attempts to harmonize them (e.g. Park
  2024 mutation clocks) have produced credible but tissue-specific results that don't
  trivially aggregate.
- For some tissues (kidney, thyroid, pancreas), normal-mutation literature is thin or
  absent — P1's >2-OoM range claim cannot be tested for tissues with no data.
- The "clone prevalence exceeds cancer rate" comparison (P2) is sensitive to how the rates
  are normalized — biopsy-level clonal coverage vs population-level incidence — and any
  apparent exceedance may collapse under more careful framing.

## Evidence Needed To Shift Belief

- **Feasibility audit (gating step):** Enumerate normal-tissue WGS cohorts and identify the
  tractable subset.
- **First-tissue test:** Esophagus is the most tractable starting point (Martincorena 2018,
  Yokoyama 2019, ample literature). Substitute meta-analyzed normal-esophagus mutation rate
  as null in the `q001` NOTCH1 contamination question; report effect on per-gene rates.
- **Cross-tissue rate variation:** Reproduce / extend Li 2021 and Cagan 2022 with the
  added cohorts surfaced by the audit; report a per-tissue per-age rate table with bootstrap
  CIs.

## Related Work

- **Sibling hypothesis:** `h01` (within-sample contamination — `h05` generalizes to
  cross-population background; `h01` is the "fix the sample" version, `h05` is the "fix the
  null" version).
- **Questions:** `q007` (Li 2021 as null model — direct precursor; this hypothesis extends
  q007 by adding the meta-analytic cross-tissue dimension).
- **Topics:** `topic:normal-tissue-mutation-atlas` (frames the broader research direction
  including the "cancer as continuum tail" big-version claim).
- **Tasks (planned):**
  - `t150`: enumerate available normal-tissue WGS cohorts; map to cBioPortal cancer types;
    identify harmonization regime.
  - `t151`: scoped normal-tissue meta-analysis pilot on esophagus or colon.
- **External:** Cagan 2022 (cross-species mutation rate scaling); Park 2024 (somatic
  mutation as biological clocks); Tomasetti & Vogelstein 2015 (stem-cell-turnover
  framework); HMF / Hartwig (potential additional normal-cohort reference).
