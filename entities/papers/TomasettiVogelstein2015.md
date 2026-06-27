---
type: paper
title: Variation in cancer risk among tissues can be explained by the number of stem
  cell divisions
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: paper:TomasettiVogelstein2015
ontology_terms:
- cancer etiology
- stem cells
- somatic mutation
- cancer risk
- stochastic mutation
- replicative mutations
- carcinogenesis
- tissue-type differences
datasets: []
source_refs:
- cite:TomasettiVogelstein2015
related:
- topic:multistage-carcinogenesis-and-age-of-onset
- question:0041-driver-complexity-vs-median-age-at-diagnosis
- theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the
---

# Variation in cancer risk among tissues can be explained by the number of stem cell divisions

- **Authors:** Cristian Tomasetti, Bert Vogelstein
- **Year:** 2015
- **Journal:** Science, 347(6217): 78–81
- **DOI/URL:** https://doi.org/10.1126/science.1260825
- **BibTeX key:** TomasettiVogelstein2015
- **Source:** PMC full-text (PMC4446723) + LLM knowledge

## Key Contribution

Tomasetti and Vogelstein demonstrate that lifetime cancer risk across 31 tissue types correlates strongly with the total number of lifetime stem cell divisions in that tissue (Spearman rho = 0.81, p < 3.5 × 10⁻⁸; Pearson r = 0.804, 95% CI 0.63–0.90), explaining approximately 65% (95% CI 39–81%) of the variance in cancer risk across tissue types. The paper introduces the "extra risk score" (ERS, also called lscd — lifetime stem cell divisions) as the baseline replicative mutation supply per tissue, and uses it to classify cancers as either replication-driven ("R-tumors," risk tracks ERS closely) or deterministic/environmentally-driven ("D-tumors," risk substantially exceeds the ERS baseline). The central argument — immediately contentious — is that most cancers arise predominantly from stochastic replication errors ("bad luck") rather than inherited or environmental factors, which are additive contributors rather than primary drivers of cross-tissue variation.

## Methods

- **Data sources:** Published literature compiled for 31 tissue types that had both (a) quantitative estimates of tissue-specific stem cell numbers and stem cell division rates and (b) corresponding lifetime cancer incidence data. Data points ranged over ~five orders of magnitude on both axes.
- **Stem-cell-division estimates:** Lifetime stem cell divisions (lscd) computed as: estimated number of stem cells in the tissue × average number of divisions per stem cell per lifetime. Values drawn from published cell biology and physiology literature; not uniformly measured across tissues.
- **Cancer risk data:** Age-standardized lifetime risk estimates from SEER (US) databases.
- **Statistical analysis:** Spearman rank and Pearson linear correlation on log-transformed (lscd, lifetime cancer risk) pairs. Confidence intervals for variance explained estimated by bootstrap.
- **Clustering / ERS:** An "extra risk score" (ERS) was computed as the residual of observed cancer risk above the regression line. An unsupervised machine-learning clustering (k-means or hierarchical, not described in detail in the main text) of tissues on ERS identified two classes — R-tumors (ERS near zero) and D-tumors (high ERS, interpreted as having substantial environmental or hereditary contributions on top of replication).
- **Scope:** 31 tissue types — notably **excluding** several high-incidence cancer types where stem-cell-division estimates were unavailable or unreliable (breast, prostate). This exclusion was later a focal point of criticism.

## Key Findings

1. **Strong cross-tissue correlation:** Log(lifetime stem cell divisions) vs. log(lifetime cancer risk) yields Spearman rho = 0.81 (p < 3.5 × 10⁻⁸), spanning roughly five orders of magnitude. This is the paper's headline result and the basis for the "bad luck" framing.

2. **65% variance explained:** The lscd variable alone accounts for ~65% (95% CI 39–81%) of the cross-tissue variation in lifetime cancer risk. The remaining ~35% is consistent with environmental, hereditary, and additional stochastic contributions.

3. **R-tumor vs. D-tumor classification:** 22 of 31 cancer types were classified as D-tumors (deterministic — environmental and/or hereditary factors add substantially to the replicative baseline; examples: lung, colorectal with strong lifestyle associations, familial forms). 9 were classified as R-tumors (replication-dominated; examples: osteosarcoma, certain brain tumors, pancreatic cancer, thyroid cancer). The D/R distinction operationalizes whether prevention via lifestyle/environment is plausible for a given cancer type.

4. **Hereditary contribution bounded:** The authors estimated that inherited mutations contribute to only ~5–10% of all cancers, consistent with prior literature. The lscd correlation holds independent of this heritable fraction.

5. **Implications for prevention:** R-tumor cancers, where ERS tracks risk, may be less amenable to primary prevention (lifestyle change) and more appropriately targeted by early detection. D-tumor cancers have substantial preventable fractions.

## Relevance

**(a) Risk across tissues, not age-of-onset per se.** This paper explains cross-tissue *variation in lifetime cancer risk* (i.e., why some tissues are 1,000× more likely than others to develop cancer), not the age-of-onset trajectory within a tissue type. The x-axis is cumulative stem cell divisions over an entire lifetime, not a time-series. Multistage models of carcinogenesis (Armitage–Doll, Knudson two-hit) address why risk rises as a power of age within a tissue — this paper does not directly model that intra-tissue dynamics. The two questions are related: more divisions supply more mutations, but the specific timing/ordering of hits required for transformation is a separate, stage-dependent question. Both the lscd framework and multistage onset models are needed to fully describe the temporal structure of carcinogenesis (see `theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the`).

**(b) Factors 2 and 3 are background context for this project, not directly testable data.** The lscd framework decomposes mutation supply across tissues as: stem-cell count × division rate × mutations per division. This project's cBioPortal data contains somatic mutation catalogs per sample and cancer type — it has NO direct measurements of stem-cell-division counts or tissue-specific stem cell numbers. Factors 2 (division rate) and 3 (stem-cell count) are biological parameters not represented in cBioPortal study tables. Consequently, the lscd correlation itself cannot be reproduced or tested within this pipeline. However, the framework is valuable interpretive context: when this project observes that mutation frequency varies across cancer types, the Tomasetti–Vogelstein finding suggests the baseline of that variation is substantially set by division rate × stem-cell number — not purely by environmental exposure heterogeneity. See `question:0041-driver-complexity-vs-median-age-at-diagnosis` for where this background intersects with project-testable questions.

**(c) "Bad luck" vs. extrinsic factors debate.** This paper is the anchor of the "bad luck" position. Wu et al. 2016 (Nature) later argued — using different analytical approaches and including breast and prostate cancer — that extrinsic factors dominate cancer risk in most tissues (~70–90% of risk attributable to extrinsic factors), directly contradicting the 65% intrinsic-replication interpretation. The contradiction is partly definitional: Tomasetti–Vogelstein measure what explains cross-tissue *differences* in risk (relative), while Wu et al. examine what fraction of absolute incidence would disappear with zero environmental exposure. Both framings are coherent but ask different questions.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Lifetime stem cell divisions (lscd / ERS) | No direct equivalent | Background context; not measurable from cBioPortal mutation tables |
| Replication-driven mutation supply | Per-sample mutation burden (TMB) | TMB partially reflects replication fidelity but also environmental exposures; not the same as lscd |
| R-tumor / D-tumor classification | Cancer type (oncotree_code, cancer_type) | D/R labels could be linked to cancer types as metadata, but are not currently in the pipeline |
| Cross-tissue variation in cancer risk | Cross-cancer-type variation in mutation frequency | The pipeline observes this variation; lscd is one causal explanation for it |
| Extra Risk Score (ERS) | Not represented | A residual measure above lscd baseline; would require external lscd estimates to compute |
| Environmental + hereditary "added risk" | Signature exposures (SBS4 = smoking, etc.) | Partial overlap: specific mutational signatures encode some environmental etiology |

## Limitations

**Paper-internal limitations:**

- **Excluded high-incidence cancers.** Breast and prostate cancer — two of the most common cancers in Western populations — were excluded because reliable stem-cell-division estimates were unavailable. Critics (notably Wu et al. 2016) showed that including them materially changes the inference about the relative importance of intrinsic vs. extrinsic factors.
- **Stem-cell-division estimates are uncertain.** Published estimates for stem cell numbers and division rates vary widely and are often indirect. The lscd values carry large, unquantified uncertainty; the correlation analysis does not propagate this uncertainty.
- **Correlation is not causation.** The correlation between lscd and cancer risk is consistent with replication error as a driver, but is also consistent with confounding: tissues with high division rates may also have higher environmental exposure (gut epithelium exposed to dietary carcinogens, lung epithelium exposed to inhaled carcinogens). The correlation does not isolate the replication-error mechanism from co-varying exposure. Rozhok and DeGregori (2015, Science) raised this specific confound.
- **R-tumor/D-tumor boundary is data-driven without a mechanistic threshold.** The ERS cutoff separating R from D tumors is derived from an unsupervised clustering on 31 points; it is not a principled mechanistic boundary.
- **No age-of-onset modeling.** The paper treats cancer risk as a single lifetime probability, not as an age-specific hazard function. How lscd connects to the observed power-law rise of incidence with age (the Armitage–Doll pattern) is not addressed.

**Conceptual and methodological critiques (post-publication):**

- **Wu et al. 2016 (Nature):** Reanalysis using a different decomposition (extrinsic risk = incidence reduction if environmental exposures were zero) found ~70–90% of cancer risk attributable to extrinsic factors in most tissues. The discrepancy arises because Tomasetti–Vogelstein ask "what accounts for the *difference* between tissue types?" while Wu et al. ask "what is the absolute preventable fraction?"
- **Rozhok and DeGregori 2015 [@RozhokDeGregori2015] (Science):** Argued that the correlation is confounded by evolutionary biology: tissues with higher division rates evolved tight tissue homeostasis and selection against transformed cells; the correlation may reflect selective pressures rather than mutation supply per se.
- **Gotay et al. and others:** The "bad luck" framing was seen as scientifically misleading for public health messaging — it could be misread as implying cancer is largely unavoidable, potentially undermining prevention campaigns for D-tumors (lung, colorectal) where lifestyle interventions have substantial effect.
- **Small N concern:** 31 tissue types is a modest sample for a correlation analysis, especially with heterogeneous data quality across the lscd estimates.

## Model / Tool Availability

No software, model, or dataset is released with this paper. The lscd estimates are derived from published literature values (cited in supplementary table), not a reusable computational tool. The SEER lifetime risk data are publicly available from the National Cancer Institute (https://seer.cancer.gov).

## Follow-up

- **Wu et al. 2016 (Nature, 529:43–47):** "Substantial contribution of extrinsic risk factors to cancer development" — the direct rebuttal, arguing extrinsic factors dominate in most tissues. Should be read alongside this paper to understand the debate.
- **Tomasetti et al. 2017 (Science, 355:1330–1334):** The authors' follow-up expanding to 32 cancer types across 69 countries, including cross-national comparisons that strengthen the lscd argument while addressing the environmental confound critique.
- **Rozhok & DeGregori 2015 [@RozhokDeGregori2015] (Science, 347:938–939):** Short commentary directly critiquing the correlation-causation leap; introduces evolutionary/selective arguments.
- **Armitage & Doll 1954 [@ArmitageDoll1954]:** The foundational paper establishing the power-law rise of cancer incidence with age — the intra-tissue temporal dynamics that Tomasetti–Vogelstein do not address. Needed alongside this paper for `theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the`.
- **Project-facing question:** Given that lscd explains ~65% of cross-tissue risk variation, what fraction of the cross-cancer-type variation in somatic mutation frequency observed in the cBioPortal pipeline is explained by the replicative baseline vs. environmental exposures encoded in mutational signatures? This is background context rather than a directly testable hypothesis with available data, but it motivates the interpretation of cross-cancer mutation frequency tables. See `question:0041-driver-complexity-vs-median-age-at-diagnosis`.
