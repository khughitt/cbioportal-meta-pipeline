---
id: "paper:Belikov2017"
type: "paper"
title: "The number of key carcinogenic events can be predicted from cancer incidence"
status: "active"
ontology_terms:
  - multistage carcinogenesis
  - age-incidence curves
  - Erlang distribution
  - gamma distribution
  - carcinogenesis stages
  - driver mutations
  - cancer epidemiology
  - SEER incidence
datasets: []
source_refs:
  - "cite:Belikov2017"
related:
  - topic:multistage-carcinogenesis-and-age-of-onset
  - question:q041-driver-complexity-vs-median-age-at-diagnosis
  - paper:ArmitageDoll1954
  - theme:temporal-structure-of-carcinogenesis
created: "2026-06-07"
updated: "2026-06-07"
---

# The number of key carcinogenic events can be predicted from cancer incidence

- **Authors:** Aleksey V. Belikov
- **Year:** 2017
- **Journal:** Scientific Reports 7:12170
- **DOI/URL:** https://doi.org/10.1038/s41598-017-12448-7
- **PMC:** PMC5610194
- **BibTeX key:** Belikov2017
- **Source:** Europe PMC full-text XML

## Key Contribution

Belikov fits the Erlang probability distribution to age-incidence curves for the 20 most prevalent US cancer types (CDC WONDER data, ~20 million cases, 1999–2012) and extracts three interpretable parameters per cancer type: k (number of key carcinogenic events), b (average time in years between events), and A/1000 (maximal populational susceptibility as a percentage). The Erlang distribution — which describes the waiting time for k independent Poisson-process events — provides excellent fits across all 20 cancer types (R² = 0.9734–0.9999, mean 0.9953), and the framework extends the classical Armitage-Doll/Nordling multistage model by replacing the power-law approximation with an exact probability distribution, which additionally accounts for the empirically observed decline in cancer incidence at advanced age.

## Methods

**Data.** US Cancer Statistics crude incidence rates by 5-year age group (15–84 years; "85+" excluded due to undefined interval) from CDC WONDER, pooled 1999–2012. Twenty most prevalent cancer types analyzed.

**Statistical fitting.** Sixteen continuous probability distributions were evaluated using least-squares nonlinear regression (GraphPad Prism 5). The Erlang distribution (integer-k special case of the gamma distribution) was selected based on consistently superior goodness of fit, particularly for gender-specific cancers analyzed per observation year, and on its mechanistic interpretability as a sum of k exponentially distributed waiting times.

**Parameter extraction procedure.** For each cancer type the gamma distribution was fit first to obtain a precise (non-integer) k estimate; that value was then rounded to the nearest integer and held fixed ("Erlang k") in a second-pass gamma fit to obtain final b and A estimates with standard errors.

**Robustness check.** Prostate cancer was refit separately for each of the 14 observation years (1999–2012) using the gamma distribution to verify parameter stability across years with markedly different screening behavior.

## Key Findings

**Per-cancer-type k estimates (number of carcinogenic events):**

| Cancer type | k (events) | b (years between events) | Max. susceptibility (%) |
|---|---|---|---|
| Prostate | 41 ± 1 | 1.83 | 26.4 |
| Lung and bronchus | 30 ± 2 | 2.75 | 16.4 |
| Bladder | 21 ± 1 | 4.59 | 9.9 |
| Uterus | 20 ± 1 | 3.67 | 3.8 |
| Oesophagus | 20 ± 0 | 4.25 | 1.3 |
| Larynx | 24 ± 1 | 3.15 | 0.7 |
| Myeloma | 16 ± 1 | 6.14 | 2.7 |
| Pancreas | 15 ± 1 | 7.07 | 7.2 |
| Kidney | 15 ± 1 | 5.75 | 3.7 |
| Colon and rectum | 10 ± 1 | 13.75 | 66.9 |
| Stomach | 11 ± 1 | 11.51 | 7.3 |
| Oral cavity | 13 ± 1 | 6.32 | 2.3 |
| Liver | 13 ± 2 | 6.67 | 1.5 |
| Breast | 9 ± 1 | 10.71 | 20.4 |
| Non-Hodgkin lymphomas | 8 ± 1 | 19.26 | 31.2 |
| Leukaemias | 8 ± 2 | 23.56 | 49.6 |
| Ovary | 8 ± 1 | 13.66 | 5.4 |
| Thyroid | 5 ± 0 | 14.67 | 1.5 |
| Brain | 4 ± 1 | 76.69 | 26.3 |
| Melanoma | 4 ± 1 | 81.01 | 100 |

**Range and heterogeneity.** k spans 4 (melanoma, brain) to 41 (prostate), b spans ~2 years (prostate) to ~81 years (melanoma). This reveals high heterogeneity in carcinogenesis requirements across types. Low-k cancers (melanoma, brain) have very long inter-event intervals suggesting rate-limiting steps occur rarely but require few of them; high-k cancers (prostate, lung) require many events each occurring more rapidly.

**Robustness of k.** For prostate cancer fit year-by-year (1999–2012), k varied only 38–45 (±8%) despite a 47% drop in diagnosed incidence following 2008/2011 screening recommendation changes. Pre-2008, variation was ±3.8%. This stability is interpreted as reflecting a biologically fundamental parameter.

**Mechanistic interpretation.** The author argues that k reflects total driver alterations (not just driver genes), including point mutations, indels, CNVs, inversions, translocations, gene fusions, and epimutations. He notes that the range 0–40 alterations per tumour reported by large omics studies (e.g., TCGA pan-cancer) corresponds to the Erlang k range, and that k should be interpreted as driver mutations (individual allele-level events) rather than driver genes.

**Model fit versus prior frameworks.** The Erlang distribution outperforms the power-law (Armitage-Doll) by naturally capturing the decline in incidence at advanced age, without requiring additional assumptions about senescence or population depletion.

## Relevance

This paper is the external calibration target for question:q041-driver-complexity-vs-median-age-at-diagnosis. Belikov's k estimates represent an incidence-curve-derived, population-level measure of "how many rate-limiting carcinogenic events each cancer type requires." In our project, we estimate driver complexity from somatic mutation prevalence data in diagnosed tumor cohorts (cBioPortal studies). These are fundamentally different quantities:

- Belikov uses population incidence (undiagnosed + diagnosed) over lifetime, fitting an age distribution.
- Our data reflect point-in-time mutation catalogs from patients who have already been diagnosed (prevalent cases in sequencing studies), with all the attendant ascertainment biases.

As a comparison reference: if our driver-count proxy (e.g., number of recurrently mutated genes per cancer type) correlates with Belikov's k, that would support the idea that incidence-curve shape and somatic mutation landscape both reflect underlying carcinogenic complexity. A mismatch could reveal that sequencing studies systematically under- or over-represent high-k cancers, or that k and driver gene count are genuinely orthogonal. Belikov's table provides a numerical anchor for each cancer type that we can join to our gene x cancer frequency outputs.

Note that the paper uses cancer-type-level incidence aggregates (e.g., "Leukaemias" pooled), whereas our data has finer subtype resolution — direct comparison requires careful cancer-type harmonization.

## Project Framework Mapping

| Paper concept | Project concept | Notes |
|---|---|---|
| k (Erlang shape parameter) | Driver complexity per cancer type | Incidence-derived; compare to count of recurrently mutated driver genes per cancer in our gene×cancer matrix |
| b (average inter-event interval, years) | — | No direct analog in our pipeline; related to mutation rate per gene per year |
| A/1000 (maximal populational susceptibility, %) | — | Lifetime penetrance estimate; not captured by somatic mutation cohort data |
| "Key carcinogenic event" | Driver mutation/alteration | Belikov explicitly includes point mutations, indels, CNVs, epimutations — broader than our somatic SNV/indel focus |
| 20 cancer types (CDC WONDER groupings) | Cancer types in `gene_cancer_study.feather` | Harmonization needed; Belikov uses coarse groupings (e.g., "Leukaemias" combined) |

## Limitations

- **Coarse cancer-type groupings.** Belikov pools subtypes (e.g., all leukaemias, all NHL), so k estimates are averages across heterogeneous subtype mixtures; the author acknowledges this and recommends subtype-specific analyses where data allow.
- **Diagnosis-stage dependency.** The estimated k reflects events accumulated to diagnosis time, not to the appearance of the first malignant cell or full cancer development. Improved screening (earlier diagnosis) will yield lower k; abandonment of screening yields higher k (the prostate PSA case demonstrates this empirically).
- **Single mutation-rate assumption.** The model assumes key carcinogenic events occur at a constant average rate throughout adult life (the Poisson process assumption). This is explicitly stated as an assumption, not derived from data; the excellent fit is cited as post-hoc support.
- **US population only.** CDC WONDER 1999–2012 data; generalizability to other populations with different carcinogen exposures or genetic backgrounds is not assessed.
- **k is integers-only.** The Erlang distribution constrains k to positive integers; real mechanistic k could be non-integer if events have variable weights.
- **No mechanistic validation.** The paper does not independently validate k against genomic driver counts from sequencing studies — it remains a predictive claim. Comparison with TCGA per-tumour alteration counts (cited from ref. 38 in the paper) is qualitative.
- **Epimutations and non-SNV events.** While Belikov argues k includes all alteration types, the parameters are estimated purely from incidence curves with no genomic data input; the mechanistic assignment to specific alteration categories is interpretive.

## Model / Tool Availability

No software or model released with this paper. The GraphPad Prism 5 project files (pzfx format) and raw CDC WONDER downloads are available as Supplementary Data. The Erlang/gamma fitting equations are provided in the Methods section and are straightforward to implement in any nonlinear regression framework.

## Follow-up

- **ArmitageDoll1954** — original multistage carcinogenesis model using the power-law; Belikov explicitly extends/replaces this framework.
- **Nordling 1953** — companion early multistage paper.
- Compare Belikov's k values to driver-gene counts from Bailey 2018 (Table S1 already in this project) to test whether incidence-derived k and consensus driver counts per cancer type are correlated.
- Investigate whether cancer types with low k (melanoma k=4, brain k=4) indeed have fewer driver mutations on average in our cBioPortal data versus high-k types (prostate k=41, lung k=30).
- Examine whether Belikov's b (inter-event interval) correlates with median age at diagnosis — this is a direct test of the model's implied relationship between b, k, and peak incidence age.
- Consider whether the "maximal populational susceptibility" parameter (A/1000) could serve as a baseline cancer-type prevalence prior for our cross-study meta-analysis.
