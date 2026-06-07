---
id: "paper:ArmitageDoll1954"
type: "paper"
title: "The Age Distribution of Cancer and a Multi-stage Theory of Carcinogenesis"
status: "active"
ontology_terms: []
datasets: []
source_refs:
  - "cite:ArmitageDoll1954"
related:
  - "topic:multistage-carcinogenesis-and-age-of-onset"
  - "question:q041-driver-complexity-vs-median-age-at-diagnosis"
  - "question:q012-mutation-ordering-cross-sectional-inference"
  - "hypothesis:h06-pre-malignant-n-minus-1-driver-carriage"
  - "theme:temporal-structure-of-carcinogenesis"
created: "2026-06-07"
updated: "2026-06-07"
---

# The Age Distribution of Cancer and a Multi-stage Theory of Carcinogenesis

- **Authors:** P. Armitage, R. Doll
- **Year:** 1954
- **Journal:** British Journal of Cancer, 8(1):1-12
- **DOI/URL:** https://doi.org/10.1038/bjc.1954.1
- **PMC:** PMC2007940
- **BibTeX key:** ArmitageDoll1954
- **Source:** full text via Europe PMC (OCR scan of original print article)

## Key Contribution

Armitage and Doll provide a formal mathematical derivation showing that, under a multi-stage model of carcinogenesis in which each of r successive cellular changes occurs at a constant (small) probability per unit time, the age-specific cancer incidence rate is proportional to t^(r-1), where t is age. Fitting England and Wales age-specific mortality data to a log-log slope of 6:1 implies r = 7 (six or seven successive rate-limiting cellular changes) for cancers of the oesophagus, stomach, colon, rectum, and pancreas. This is the foundational quantitative statement linking the slope of incidence-vs-age curves to the number of required cellular hits, predating the modern concept of driver mutations by two decades.

## Methods

**Data.** Age-specific mortality rates for 17 cancer sites (both sexes) from England and Wales Registrar-General's annual reports for 1950-1951. The analysis is restricted to five-year age groups spanning 25-74 years; rates below age 25 are noted as potentially governed by distinct mechanisms, and rates above 74 are treated as less reliable due to small numbers and possible misclassification.

**Model.** The mathematical model (detailed in a formal appendix) rests on four assumptions:
1. Carcinogenesis proceeds through exactly r discrete, ordered, irreversible cellular changes.
2. Each change occurs as a rare event at a constant probability p_i per unit time (so p_i · t << 1 across a human lifetime).
3. The changes must proceed in a unique fixed order.
4. The number of target cell lines N per person is constant.

Under these assumptions the probability that the r-th (final) change occurs in the small interval (t, t+dt) is:

    rate = N · p_1 · p_2 · ... · p_r · t^(r-1) / (r-1)!

Hence incidence ~ t^(r-1), and log(incidence) ~ (r-1) · log(t).

**Analysis.** Log-log plots of death rate vs. age were constructed for all 17 sites. Reference lines with slope 6:1 (corresponding to r = 7 stages) were drawn through each dataset. Regression coefficients of log(death rate) on log(age) were computed for sites with near-constant carcinogenic exposure. Deviations from the 6:1 law for hormonally-influenced and exposure-variable cancers were explained qualitatively using a weighted-mean extension for time-varying stage-specific probabilities (also derived in the appendix). A quantitative illustrative example was worked through for penile cancer and age at circumcision.

**Ancestry.** The paper extends and critiques earlier work by Nordling (1953) — who first noted the sixth-power relationship aggregating all sites — and by Fisher and Hollomon (1951), whose "critical colony size" alternative hypothesis is ruled out on carcinogen-dose-response grounds.

## Key Findings

**The power-law result.** For cancers of the oesophagus (M), stomach (M, F), colon (M, F), rectum (M, F), and pancreas (M, F) — collectively 9 site-sex combinations — log-log slopes cluster around 6, consistent with r = 7 ordered stages. Observed regression coefficients from Table I range from 4.97 (rectum, F) to 6.48 (pancreas, F), with a central tendency near 5.5-6.

**Two-group classification of cancer sites.** The paper explicitly divides the 17 sites into two groups:

- *Group 1* (constant-environment sites, slope ~ 6): oesophagus, stomach, colon, rectum, pancreas. These are cancers believed to be relatively independent of endocrine variation and stable environmental exposures. The power-law fit is good.

- *Group 2* (variable-environment sites, deviating from slope 6): lung, bladder, and prostate in men; lung, breast, ovary, and cervix/corpus uteri in women. Deviations are attributed to time-varying stage-specific hit rates — hormonal cycling for reproductive cancers, changing smoking cohort prevalence for lung cancer, occupational exposure timing for bladder cancer.

**Weighted-mean formula for time-varying probabilities.** When one stage probability p_s varies with time to, its contribution to incidence at age t is weighted proportionally to w(to) = to^(s-1) · (t - to)^(r-s-1). Early stages exert maximum influence early in life; late stages exert maximum influence close to the time of observation. This provides a mechanistic explanation for why childhood carcinogen exposures can produce latent tumours decades later, and why cessation of a late-stage carcinogenic exposure (e.g., endocrine changes at menopause) can cause incidence to plateau.

**Penile cancer / circumcision example.** Using r = 7, s = 1, and the circumcision-age data of Shrek and Lenowitz (1947), the model predicts relative cancer risks of approximately 0.30, 0.77, 0.98, and 1.00 for circumcision at ages 3, 11.5, 26.5, and 44.5 years (and ~0.01 if circumcised in the first days of life). The observed ratios in the clinical dataset are 0.00, 0.50, 0.71, and 0.74. The qualitative agreement supports the model's claim that the prepuce is required for the first (irreversible) cellular change.

**Carcinogen concentration prediction.** Under the multi-stage model with independent stage-specific probabilities each proportional to carcinogen concentration, the final incidence is proportional linearly to concentration — consistent with experimental dose-response data. This correctly distinguishes the multi-stage model from the Fisher-Hollomon colony-size model, which would predict a 5th-6th-power dependence on concentration.

**Authors' stated caveats (from the paper itself).** The authors explicitly warn against over-interpreting the seventh-stage count:
1. A sixth-power law could arise from fewer than 7 stages if the probability of one or more stages increases with a power of age (e.g., due to cell proliferation with age).
2. The relationship is only validated in the 25-74 year window; behaviour outside this range is uncertain.
3. Alternative mechanisms besides multi-stage mutation could produce the same power-law relationship (e.g., cerebral haemorrhage, coronary thrombosis, and gastric ulcer show similar age-incidence patterns, which the authors note is difficult to explain by the same carcinogenic mechanism).

## Relevance

This paper is the theoretical anchor for the project thread on age of cancer onset as a function of driver complexity (`topic:multistage-carcinogenesis-and-age-of-onset`). Its central quantitative result — that the log-log slope of incidence vs. age equals (r-1), where r is the number of rate-limiting cellular stages — is the framework within which `question:q041-driver-complexity-vs-median-age-at-diagnosis` is posed.

**Critical limitation for our project.** The Armitage-Doll model makes predictions about **population-level incidence curves** — specifically, the slope of incidence vs. age plotted on a log-log scale for a single cancer type measured in a population over time. The cleanest empirical test uses SEER-style longitudinal incidence registries, not prevalence-based mutation cohorts.

Our project reads **cBioPortal somatic-mutation data**, which are drawn from diagnostic/clinical sequencing cohorts. These cohorts are subject to:

- **Ascertainment bias by cancer type** — study enrollment is not random with respect to age; trial eligibility, institutional referral patterns, and sequencing protocols differ across cohorts.
- **Prevalence vs. incidence conflation** — we observe patients at diagnosis across many studies and years, not a population-level incidence series within a single age-ascertained cohort.
- **Heterogeneous driver count definitions** — the number of somatic drivers observed per tumor in cBioPortal reflects sequencing depth, panel coverage, and variant-calling thresholds, not the true number of rate-limiting cellular hits postulated by Armitage-Doll.
- **Selection for progression** — the observed tumors have all survived to clinical detection; early-stage molecular precursors are systematically underrepresented.

Therefore, **any correlation we run between median age at diagnosis and a proxy for driver-count complexity using cBioPortal data is at best a confounded cross-type correlation, not an estimate of the true number of required hits.** It can generate hypotheses consistent with or inconsistent with the Armitage-Doll framework, but it cannot confirm or refute the power-law slope. That test requires prospective population-incidence data (SEER) linked to genomic driver counts per cancer type.

This distinction is directly relevant to `hypothesis:h06-pre-malignant-n-minus-1-driver-carriage`: while Armitage-Doll provides a theoretical warrant for expecting that pre-malignant cells carry n-1 prior hits, the cBioPortal data cannot directly observe those pre-malignant states. And `question:q012-mutation-ordering-cross-sectional-inference` inherits the same limitation — cross-sectional inferences about mutation order from diagnostic cohorts face the exact selection pressures that make Armitage-Doll predictions hard to test in our data.

The `theme:temporal-structure-of-carcinogenesis` is where the Armitage-Doll conceptual vocabulary (ordered stages, stage-specific hit rates, latent periods, variable vs. constant hit-rate environments) maps most directly onto the project's interpretive framework.

## Project Framework Mapping

| Armitage-Doll Concept | Project Concept | Notes |
|---|---|---|
| r successive cellular changes | driver mutation count per cancer type | AD stages are rate-limiting functional changes; driver mutations are a molecular proxy; not necessarily the same cardinality |
| Stage-specific hit-rate p_i | per-gene somatic mutation rate in a cancer type | Observed in cBioPortal as mutation frequency; confounded by clonal selection, panel coverage, hypermutation |
| t^(r-1) incidence law | age of cancer onset vs. driver complexity | Armitage-Doll predicts slope; cBioPortal gives cross-sectional median age per histology |
| Group 1 sites (constant exposure, slope ~ 6) | GI cancers (colorectal, gastric, pancreatic) | These are the sites with cleanest power-law behaviour in the original paper |
| Group 2 sites (variable exposure, deviating slope) | Lung, breast, ovarian, cervical, prostate, bladder | Hormonal or exogenous-carcinogen variation breaks the simple power law |
| Carcinogen concentration ~ linear incidence | mutagen-driven hypermutator phenotype | High TMB cancers have a different etiology; the linearity prediction assumes low p_i |
| Weighted exposure timing by stage order | early vs. late driver acquisition in clonal evolution | Early hits (e.g., founding initiating mutations) have disproportionate influence on lifetime risk |

## Limitations

**Model assumptions that do not hold in general.**

1. **Constant hit rates.** The model requires p_i constant throughout life. This is violated for hormonally-modulated cancers and for exposures that change with time (smoking, occupation). The authors handle this with the weighted-mean extension, but that introduces additional parameters that are unidentifiable without carcinogen exposure data.

2. **Ordered stages only.** The model assumes changes must occur in a single fixed order. This conflicts with modern evidence that the same driver genes can be acquired in different orders across patients (relevant to `question:q012-mutation-ordering-cross-sectional-inference`) and that clonal selection can make equivalent evolutionary paths converge.

3. **No clonal expansion between stages.** The simplest Armitage-Doll formulation treats each cell independently and does not model the growth advantage that partially-transformed cells might have. This was the central extension added by the **Moolgavkar-Venzon-Knudson (MVK) two-stage clonal-expansion model** (Moolgavkar and Venzon 1979; Moolgavkar and Knudson 1981), which allows the intermediate-stage cell population to expand clonally, changing the age-incidence predictions substantially — especially for two-hit tumour suppressor cancers (retinoblastoma being the canonical example where Knudson's "two-hit hypothesis" was validated). The MVK model is the principal successor framework.

4. **Constant target-cell number N.** Organ growth and the turnover rate of tissue stem cells both change with age, violating this assumption.

5. **Limited age range.** The fit is restricted to ages 25-74; the model cannot account for the leveling-off of cancer incidence sometimes observed at very old ages (Horiuchi-Wilmoth phenomenon), which has been attributed to demographic heterogeneity in susceptibility, depletion of susceptible cells, or immunosenescence.

6. **Population-aggregate model.** The model does not capture between-individual variation in hit rates, susceptibility, or the number of target cell lines. Unobserved heterogeneity can produce power-law-like relationships even without a true multi-stage mechanism (frailty models).

7. **Mortality as a proxy for incidence.** The authors use death rates as a proxy for incidence rates, noting this may be acceptable if case-fatality does not vary strongly with age — an assumption that does not hold for cancer types with strongly age-dependent survival (e.g., breast cancer).

8. **Cannot distinguish r from growth-rate effects.** As the authors note, a slope of 6 on a log-log plot could arise from 5 stages if one stage probability increases linearly with age (e.g., due to age-related cell proliferation), or from 4 stages with a quadratically increasing probability. The slope constrains r-1 + (sum of age-dependent exponents), not r alone.

## Model / Tool Availability

This is a theoretical/statistical paper from 1954; no software, dataset, or computational tool was released. The mathematical derivation in the appendix is the sole formal artifact. The full text is freely available via PMC (CC BY 4.0 license) at https://pmc.ncbi.nlm.nih.gov/articles/PMC2007940/.

## Follow-up

**Immediate theoretical successors.**

- **Moolgavkar and Venzon 1979 / Moolgavkar and Knudson 1981** — the MVK two-stage clonal-expansion model; adds clonal growth of initiated cells between stages; the primary refinement of Armitage-Doll.
- **Knudson 1971** — the "two-hit hypothesis" for retinoblastoma; provided the first mechanistic (somatic + germline) instantiation of the multi-stage framework.
- **Nordling 1953** — the direct precursor; grouped all cancers together and noted the sixth-power law; Armitage and Doll extend and formalize.
- **Tomasetti and Vogelstein 2015 / 2017** (Science) — revisited the number-of-stem-cell-divisions framework as the dominant determinant of cancer risk across tissues, reigniting debate about intrinsic vs. extrinsic contributions to stage hit rates.

**Questions raised for this project.**

- If we correlate median age at first diagnosis (from cBioPortal clinical metadata) with an estimate of the number of recurrent driver genes per cancer type (from our cross-study aggregation tables), does the rank ordering across cancer types qualitatively match the Armitage-Doll expectation? Which cancer types are most outlying, and do their deviations align with the "Group 2" (variable-exposure) sites the original paper identified?
- For cancer types with very steep incidence-vs-age curves (i.e., many required hits), do we observe a longer right tail in the number of drivers per tumor in cBioPortal, as would be expected if higher-stage tumors require more accumulated mutations to reach the final stage?
- Can the Bailey 2018 driver gene census (annotated in our pipeline) serve as a proxy for r — the number of rate-limiting stages — per histology, and does it correlate with median onset age in SEER data?
