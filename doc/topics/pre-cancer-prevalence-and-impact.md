---
id: "topic:pre-cancer-prevalence-and-impact"
type: "topic"
title: "Pre-cancer prevalence and impact: pre-malignant lesions as a continuous, characterizable population"
status: "active"
ontology_terms:
  - pre-cancer
  - dysplasia
  - field cancerization
  - clonal expansion
  - subclonal resistance
datasets:
  - "cBioPortal pre-malignant subsets (Barrett's, MGUS/SMM, MDS, IPMN, prostate ASAP/HGPIN)"
  - "HTAN (NCI Human Tumor Atlas Network) pre-cancer cohorts"
  - "Cancer registries (population incidence)"
  - "MGUS / SMM / MDS / Barrett's epidemiological cohorts"
source_refs:
  - "paper:Martincorena2018"
  - "paper:LeeSix2018"
related:
  - "hypothesis:h06-pre-malignant-n-minus-1-driver-carriage"
  - "hypothesis:h04-mhn-pathway-ordering"
  - "task:t156"
  - "task:t157"
  - "topic:normal-tissue-mutation-atlas"
  - "topic:co-occurrence-and-mutual-exclusivity"
  - "question:q012-mutation-ordering-cross-sectional-inference"
created: "2026-04-27"
updated: "2026-04-28"
---

# Pre-cancer prevalence and impact

## Summary

Pre-cancers — pre-malignant clonal lesions like MGUS, Barrett's esophagus, MDS, IPMN, ASAP /
HGPIN, dysplastic adenomas, cervical CIN — are conventionally treated as clinically
"asymptomatic precursor" categories whose value lies in their predictive relationship to
the downstream invasive cancer. This topic frames the broader research direction that
**pre-cancers are themselves a substantive object**: collectively they affect a much larger
fraction of the population than invasive cancers, they may have under-recognized
physiological costs (immune dysfunction in MGUS, surveillance burden in BE), and they offer
a privileged observational window on the order of driver acquisition that informs both the
ordering work (`h04`, `q012`) and the n-1-poised-population subclonal-resistance frame.

The framing is that current cancer treatment "waits until the very final stages of a long
gradual process" — by which time cell populations have accumulated many mutations and an
n-1 sub-clone may already be poised to re-emerge after targeted therapy. Pre-cancer-stage
intervention is the strategic alternative, but it depends on a quantitative
characterization of pre-cancer prevalence and progression risk that does not yet exist in
unified form.

## Key Concepts

- **Pre-malignant lesion / pre-cancer.** A clonal cellular population with histological
  features intermediate between normal tissue and invasive cancer, often with a
  characteristic subset of the canonical drivers of the downstream cancer.
- **Field cancerization.** The phenomenon (Slaughter 1953) that a tissue exposed to a
  carcinogenic process develops multiple independent pre-malignant clones, only some of
  which progress to invasive cancer.
- **N-1 poised population.** A sub-clone that carries n-1 of n canonical driver mutations
  and re-emerges as fully transformed after targeted therapy eliminates the dominant clone.
  The clinical consequence of slow, stepwise driver acquisition under positive selection.
- **Subclonal resistance.** Pre-existing minor sub-clones (in some cases at sub-1% VAF) that
  are selected for after targeted treatment and drive recurrence (Sottoriva 2015, Turajlic
  2019 TRACERx).
- **Surveillance vs intervention regime.** The clinical decision of whether to actively
  treat a pre-malignant lesion or surveil-and-wait. Currently dominated by surveillance
  for most pre-cancers; pre-emptive intervention requires risk-stratification not yet
  available at the molecular level.

## Current State of Knowledge

**Well-established:**
- Specific pre-cancer ↔ cancer pairs are well-characterized clinically (Barrett's → EAC,
  MGUS → MM, MDS → AML, IPMN → PDAC, prostate HGPIN → PRAD, cervical CIN → cervical
  carcinoma, dysplastic nevi → melanoma, atypical hyperplasia → DCIS → IDC).
- MGUS prevalence is ~3% over age 50 (Rajkumar 2022 reviews); progression rate to MM is
  ~1%/year for standard-risk MGUS.
- Barrett's esophagus prevalence is ~1–2% in adults; progression to EAC is ~0.1–0.3%/year.
- The general population carries pre-malignant clones at much higher rates than the
  clinical-incidence rates of corresponding cancers.

**Emerging / less established:**
- The **cumulative impact** of pre-malignant lesions on health outside the
  cancer-progression pathway is under-studied. MGUS is associated with bone loss, peripheral
  neuropathy in some subtypes, kidney damage, and infection risk — these are clinical
  observations not always reflected in the "asymptomatic precursor" framing.
- The **molecular driver landscape** of pre-cancers vs invasive cancers across the spectrum
  of cancer types has not been systematically catalogued. HTAN is closing this gap.
- The **n-1 poised population** is documented in select cancer types (Sottoriva 2015 in
  glioma, Turajlic 2019 in renal) but not systematically across the pre-cancer ↔ cancer
  spectrum.

## Controversies & Open Questions

- **Are "indolent" pre-cancers actually indolent?** MGUS is statistically indolent for the
  majority of patients, but the assumption that the clonal IgG-secreting population has
  *zero* impact is at odds with the basic biology — clonal expansion of an immune cell
  type carries metabolic and immunological cost.
- **Should pre-cancers be the primary target of cancer-prevention interventions?** Strategic
  argument: by the time invasive cancer is detected, the population is mutationally
  diverse enough that targeted therapy faces n-1 resistance. Counter-argument: most
  pre-cancers do not progress, so widespread intervention would have a poor risk-benefit
  ratio at the population level. Risk-stratification at the molecular level could
  resolve this.
- **What is the right population denominator for pre-cancer prevalence?** The
  surveillance-detected vs autopsy-detected vs population-screening-detected rates differ
  by orders of magnitude; reported prevalence depends heavily on the detection regime.
- **Is the n-1 framing literally correct?** The number of "drivers" required for invasive
  transformation is itself debated; multi-hit Knudson-style models suggest 5–8 drivers,
  but the per-cancer-type threshold varies and the pre-malignant cohorts in cBioPortal
  often carry many more than n-1.

## Relevance to This Project

- **Direct support for `hypothesis:h06`** (pre-malignant n-1 driver carriage).
- **Complementary frame for `hypothesis:h04`** (MHN ordering — pre-malignant samples
  provide *observed* ordering against which MHN-inferred ordering can be calibrated).
- **Connects to `topic:normal-tissue-mutation-atlas`** (normal → pre-malignant → invasive
  is a continuum; the pre-cancer phase is the middle term).
- **Out-of-scope but framing-relevant** for direct cBioPortal work: the population-prevalence
  and clinical-impact claims require external data (cancer registries, MGUS / BE
  epidemiological cohorts). The project's contribution can plausibly be the *molecular*
  characterization where cBioPortal samples exist; the *clinical* and *epidemiological*
  claims require collaboration or external-data ingestion.
- **Strategic implication for the project's framing:** if the pre-cancer driver landscape
  is n-1 of the invasive landscape, then cBioPortal's pan-cancer ranking is partly a
  measure of the *pre-cancer* driver set with the late-stage residual layered on top.
  This re-frames the project's headline claim: "associations that recur across studies"
  is partly a recovery of the pre-cancer-stage molecular landscape, not exclusively the
  invasive-stage one.

## Key References

- **Sottoriva 2015** *Nature Genetics* — Big Bang model of glioma; subclonal pre-existence
  of resistance.
- **Turajlic 2019** TRACERx Renal — pre-existing subclones explain post-treatment
  resistance in renal cancer.
- **Maley & Greaves 2014** "Frontiers in cancer research" — cancer as evolutionary process
  framework.
- **Rajkumar 2022** review on MGUS / SMM / MM clinical progression.
- **HTAN** (NCI Human Tumor Atlas Network) — active research program with explicit
  pre-cancer focus; provides the external data anchor for any project pre-cancer work.
- **Slaughter 1953** *Cancer* — original field cancerization paper.
