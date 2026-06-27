---
type: paper
title: 'Toward an evolutionary model of cancer: Considering the mechanisms that govern
  the fate of somatic mutations'
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: paper:RozhokDeGregori2015
ontology_terms:
- somatic evolution
- fitness landscape
- age-dependent carcinogenesis
- tissue microenvironment
- multistage carcinogenesis
- clonal dynamics
- stem cell biology
- Peto's paradox
datasets: []
source_refs:
- cite:RozhokDeGregori2015
related:
- topic:multistage-carcinogenesis-and-age-of-onset
- question:0041-driver-complexity-vs-median-age-at-diagnosis
- paper:TomasettiVogelstein2015
- paper:ArmitageDoll1954
- theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the
---

# Toward an evolutionary model of cancer: Considering the mechanisms that govern the fate of somatic mutations

- **Authors:** Andrii I. Rozhok, James DeGregori
- **Year:** 2015
- **Journal:** Proceedings of the National Academy of Sciences, 112(29):8914-8921
- **DOI/URL:** https://doi.org/10.1073/pnas.1501713112
- **PMC:** PMC4517250
- **BibTeX key:** RozhokDeGregori2015
- **Source:** full text via Europe PMC (PMC4517250); abstract confirmed via Crossref/Europe PMC API

> **Title note:** The user's request cited the subtitle as "...rate of carcinogenesis"; the published title uses "...fate of somatic mutations." The PMC and Crossref records are consistent on the correct title. Content confirmed from full-text PMC fetch.

## Key Contribution

Rozhok and DeGregori argue that the classical multistage carcinogenesis model — which attributes age-dependent cancer incidence primarily to the accumulation of oncogenic mutations over time — cannot explain several fundamental empirical puzzles. In its place they develop a fitness-landscape framework in which the selective value of an oncogenic mutation is not fixed but is dynamically determined by the tissue microenvironment, and that environment itself changes with age. Young, healthy tissue imposes stabilizing selection that suppresses somatic evolution; aging tissue rewires the microenvironment in ways that convert previously neutral or deleterious mutations into selectively advantageous ones. The paper proposes that the late-life surge in cancer incidence is therefore primarily driven by age-dependent shifts in the selection landscape, not by the raw pace of mutation accumulation.

## Methods

This is a perspective/theoretical review paper, not a primary data study. The argument proceeds in three analytical layers:

1. **Empirical anomalies compilation.** The authors survey published data on mutation accumulation kinetics, stem cell (SC) division profiles, cancer incidence curves, and interspecies comparisons (Peto's paradox) to document observations that are quantitatively inconsistent with a simple mutation-count model.

2. **Formal probabilistic argument.** A model is presented for the probability of acquiring multiple driver mutations as a function of clonal dynamics:

   > P_d1…dn(t) = D(t) × ∫₀ᵗ (∏ pᵢ)(t) dt

   where D(t) is the total number of cell divisions within a clonal context and pᵢ are per-division mutation probabilities. This formalism shows that selection-driven proliferation (affecting D(t)) has an exponentially greater impact on multi-driver cancer probability than mutation rate itself.

3. **Evolutionary biology import.** The authors ground their framework in established evolutionary genetics — Shelford's Law of Tolerance (fitness is a bell-curve function of environmental conditions, not a fixed property), population-size effects on selection efficacy, and stabilizing vs. directional selection theory — and map these directly onto somatic tissue ecology.

## Key Findings

**The mutation-accumulation paradox.** Approximately 40–50% of somatic mutations accumulate before body maturation stops, yet most cancers manifest decades later. Hematopoietic stem cell (HSC) division rates slow dramatically before body maturation, yet cancer incidence continues to rise exponentially afterward. These temporal dissociations are inconsistent with a model in which cumulative mutation count is the dominant driver of incidence timing.

**Universal incidence curve despite tissue heterogeneity.** Cancers arising from stem/progenitor pools that differ drastically in size, compartmentalization, and cell-division profile all exhibit a similar age-dependent exponential rise in incidence. Cancers requiring different numbers of oncogenic mutations show this common pattern. A pure mutation-accumulation model would predict incidence curves that diverge systematically across these tissue types; they do not.

**CML as a falsifying case.** Chronic myeloid leukemia (CML) arises from a single oncogenic mutation (BCR-ABL) yet shows a late-life exponential increase in incidence, not an early-life plateau. This directly contradicts the prediction that fewer required mutations should substantially shift onset to younger ages.

**Fitness is dynamic and environment-dependent.** Drawing on Shelford's Law of Tolerance, the paper argues that the selective advantage conferred by an oncogenic mutation is a function of the tissue microenvironment, not an intrinsic property of the mutation. A mutation conferring hypoxia resistance is neutral in normally oxygenated young tissue but advantageous in an aging microenvironment with deteriorating oxygen homeostasis. The authors review experimental evidence that mutant clones respond differently to inflammatory conditions, irradiation, and age-related tissue decline.

**Age-dependent shift in selection regime.** During the reproductive period, coevolution of stem cells and their supporting microenvironments maintains "stabilizing selection" — the niche actively suppresses variants deviating from the optimized stem cell phenotype, so most oncogenic mutations remain neutral or deleterious. Post-reproductively, age-related microenvironmental degradation (inflammation, stromal remodeling, loss of niche signaling fidelity) perturbs this equilibrium, progressively rewarding previously suppressed mutant phenotypes. This produces a temporal shift from stabilizing selection to positive selection for proto-oncogenic variants, driving the late-life incidence surge.

**Tissue architecture governs selection efficacy.** Large, well-mixed SC pools (e.g., hematopoietic) enable efficient Darwinian selection and exponential clonal expansion of advantaged variants. Small, fragmented SC pools (e.g., intestinal crypts) are governed predominantly by genetic drift rather than selection, limiting the speed of somatic evolution. This architectural difference is proposed as a key determinant of tissue-specific cancer kinetics, independent of mutation rate differences.

**Selection amplifies multi-driver probability more than mutation rate does.** The quantitative model shows that fitness-driven proliferation (the D(t) term) contributes exponentially to the probability of acquiring multiple driver mutations, whereas per-division mutation probability (the ∏pᵢ term) contributes only linearly. Therefore, modulating selection has a disproportionately greater effect on carcinogenesis kinetics than modulating mutation rate.

**Peto's paradox.** Larger mammals with proportionally larger stem cell pools are not proportionally more prone to cancer. The fitness-landscape model is compatible with this: inter-species differences in microenvironmental control mechanisms and life-history optimization of stabilizing selection can cancel out the expected larger-target effect.

**Therapeutic implication.** The authors argue that targeting tumor cell fitness via microenvironmental modulation — particularly anti-inflammatory interventions that restore stabilizing selection — may be more effective than mutation-targeted therapies, because the latter create selective pressure for resistance while the former alter the landscape that rewards any mutation.

## Relevance

This paper is the essential modern counterweight to a naive "fewer required hits = earlier onset" interpretation of the Armitage-Doll multistage framework and the Tomasetti-Vogelstein lifetime stem-cell-division (lscd) correlation. The lscd correlation observes that tissues with more cumulative stem cell divisions have higher lifetime cancer risk, which Tomasetti and Vogelstein attributed primarily to "bad luck" replication errors. Rozhok and DeGregori provide a mechanistic argument for why the lscd correlation, even if real, should not be interpreted causally: the timing and rate of carcinogenesis are governed not only by mutation supply (which is proportional to divisions) but critically by the selection landscape — and that landscape shifts with age in ways that are largely independent of division count. A tissue could accumulate mutations rapidly via frequent divisions yet suppress carcinogenesis efficiently through robust stabilizing selection; conversely, infrequently dividing tissue in an aged microenvironment could rapidly promote clonal expansion once the selection balance tips.

For this project's question about what governs differential median age of cancer onset (question:0041-driver-complexity-vs-median-age-at-diagnosis), the Rozhok-DeGregori framework demands that any multi-study analysis of driver-complexity vs. age-at-diagnosis distinguish the mutation-supply channel (hits accumulated per unit time, related to lscd) from the selection-landscape channel (when those accumulated hits begin conferring a fitness advantage). The steep late-life incidence surge in some tissues — even those requiring many driver events — is more readily explained by a late-shifting selection regime than by the final mutation event being delayed to old age by sheer probability. The model also provides a principled explanation for CML's late-life incidence despite its single-hit origin, a paradox that purely hit-counting models cannot resolve.

## Project Framework Mapping

| Paper Concept | Project Framework Concept | Notes |
|---|---|---|
| Stabilizing selection in young tissue | Pre-malignant suppression regime | Connects to hypothesis:0006-pre-malignant-n-minus-1-driver-carriage; suppressed clones may carry subsets of required drivers without expanding |
| Age-dependent microenvironmental shift | Temporal structure of carcinogenesis | The primary driver of incidence timing in the theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the thread |
| Fitness is dynamic / environment-dependent | Selection landscape modulation | The key departure from the Armitage-Doll fixed-probability-per-stage assumption |
| Tissue architecture (pool size, fragmentation) | Cancer-type-specific mutation dynamics | Could inform why some cancer types show sharper driver-complexity vs. age correlations than others in our gene x cancer matrices |
| D(t) clonal expansion factor | Mutation frequency metric (cross-study) | Our cross-study mutation frequencies reflect fixed-time snapshots; this framework implies the snapshot captures post-selection state, not raw mutation supply |
| CML single-hit late-life paradox | Counter-example for hit-count models | Directly relevant to interpreting outlier cancer types in question:0041 |

## Limitations

- The fitness-landscape framework is largely qualitative and conceptual. While the probabilistic model (P_d1…dn formula) is presented, no quantitative predictions of cancer incidence curves are derived and tested against epidemiological data.
- The paper does not directly measure or model the specific microenvironmental changes that shift the selection regime, beyond citing supporting studies; the mechanistic link between age-related inflammation/stromal remodeling and fitness reversal is described but not formalized.
- Tomasetti-Vogelstein (2015) is not directly addressed or cited (the paper was published in the same year); the implicit rebuttal of lscd-based causal reasoning is present but the engagement is indirect.
- The model is organism-wide and does not make tissue-specific quantitative predictions that could be tested using the kind of cross-study mutation frequency data this project generates.
- The "stabilizing selection" argument draws heavily on evolutionary theory in sexual populations; whether the same dynamics operate faithfully in somatic tissues with their specific niche architectures requires further empirical validation.

## Model / Tool Availability

No software, dataset, or quantitative model is released with this paper. It is a theoretical perspective article.

## Follow-up

- **TomasettiVogelstein2015** — the primary interlocutor for the lscd correlation interpretation; this project has a summary forthcoming or pending.
- **ArmitageDoll1954** — the foundational multi-stage model this paper critiques; summary exists at `doc/papers/ArmitageDoll1954.md`.
- DeGregori and collaborators subsequently developed the "adaptive oncogenesis" framework more formally in follow-up work; those papers extend the fitness-landscape concept with experimental data from hematopoietic systems.
- Wu et al. and other experimental studies on aged HSC niches may provide empirical grounding for the microenvironmental shift mechanism.
- Questions for this project: Does the driver-complexity vs. median-age-at-diagnosis correlation in our cross-study data show a different slope for tissue types with large well-mixed SC pools vs. small fragmented pools (hematopoietic vs. epithelial)? Does the CML outlier pattern (single-driver, late onset) appear in our cross-study gene x cancer matrix?
