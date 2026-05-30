---
id: paper:Schill2024
type: paper
title: Correcting for Observation Bias in Cancer Progression Modeling
status: active
ontology_terms: []
source_refs:
- cite:Schill2024
related:
- paper:Vocht2026
- question:q012-mutation-ordering-cross-sectional-inference
- topic:co-occurrence-and-mutual-exclusivity
- discussion:2026-04-24-mutation-ordering-and-path-dependency
created: '2026-04-27'
updated: '2026-04-27'
dataset_usage:
- ref: dataset:msk-impact
  role: analyzed
  overlap: unknown
---

# Correcting for Observation Bias in Cancer Progression Modeling

- **Authors:** Rudolf Schill, Maren Klever, Andreas Lösch, Y. Linda Hu, Stefan Vocht, Kevin Rupp, Lars Grasedyck, Rainer Spang, Niko Beerenwinkel
- **Year:** 2024
- **Journal:** Journal of Computational Biology
- **Volume/Issue/Pages:** 31(10):927–945
- **DOI:** 10.1089/cmb.2024.0666
- **PMID:** 39480133
- **Conference version DOI:** 10.1007/978-1-0716-3989-4_14 (RECOMB 2024, Lecture Notes in Computer Science)
- **BibTeX key:** Schill2024
- **Source:** Paywalled (no OA copy per Unpaywall); summary based on PubMed abstract, Crossref metadata, and detailed description in the open-access Vocht et al. 2026 (PMC12776348) which was co-authored by Schill and explicitly describes the Schill 2024 model. All mechanistic claims are author-attributed to that companion paper. Quantitative results carry an inline `[UNVERIFIED: …]` caveat where not directly stated in available sources.

## Key Contribution

This paper identifies and corrects a pervasive **collider bias** that distorts cancer progression models fitted to cross-sectional diagnostic cohorts. When tumors are sampled at the time of clinical detection, the observed cohort is conditioned on the event of detection — and detection rates depend on the tumor's genomic state. Genetic alterations that increase detectability (e.g. TP53 in colorectal adenocarcinoma, EGFR in lung adenocarcinoma) therefore appear anti-correlated with other alterations in naive cross-sectional analyses, producing spurious suppressive effects while masking true promoting effects.

The solution is an **observation-event model**: an explicit (n+1)th event representing tumor detection is added to the Mutual Hazard Network (MHN) framework (Schill 2020). Each driver gene mutation is allowed to modify the rate of this observation event. Conditioning on eventual observation (the selection into the diagnostic cohort) is then handled exactly within the model rather than ignored. This extends the original MHN (Schill et al. 2020, *Bioinformatics* 36:241–249) from n events to n+1 events, where the extra event has a special role: its occurrence corresponds to clinical ascertainment rather than a biological somatic alteration.

## Methods

**Model framework:** Mutual Hazard Networks — continuous-time Markov chains over all 2^n tumor genotype states. Tumors start in the healthy (wild-type) state, accumulate events irreversibly, and are eventually observed stochastically. In the original MHN (cMHN), the observation time was treated as an exponentially distributed random variable independent of genotype. Here, the observation rate is made genotype-dependent: each mutation is given a rate multiplier on the observation event, estimated from data.

**Likelihood:** The parameter matrix grows from n×n (cMHN) to (n+1)×n — adding one row for per-event effects on observation rate. An efficient tensor formula is used to compute the exact marginal log-likelihood under the expanded model, making training tractable.

**Data:** Validated on **MSK-IMPACT** data from AACR GENIE, focusing on two tumor types:
- Colon adenocarcinoma
- Lung adenocarcinoma (LUAD; 3,662 samples [UNVERIFIED — count from Vocht 2026 LUAD demo which may use the same cohort])

**Regularization:** L1 / L2 / symmetric penalties available (per Vocht 2026 implementation description).

**Comparison:** Corrected model results compared to uncorrected cMHN fits on the same data to quantify the magnitude of collider-bias distortion.

## Key Findings

1. **Collider bias is not a corner case.** Detection factors such as tumor size, inflammation (fever, fatigue), and elevated biochemical markers are influenced by genomic alterations. Any cross-sectional cancer dataset selected at diagnosis is therefore conditioned on a collider, making collider bias structurally unavoidable without explicit modeling.

2. **TP53 increases clinical detection rate in colon adenocarcinoma.** The observation-event model recovers a strong positive effect of TP53 on the observation event rate [UNVERIFIED exact multiplier magnitude]. In the uncorrected model, TP53's detectability-boosting effect would have made it appear spuriously anti-correlated with other drivers.

3. **EGFR increases clinical detection rate in lung adenocarcinoma.** EGFR mutations have a strong positive effect on observation rate in LUAD — Vocht 2026 reports an observation rate multiplier of 10.91× for EGFR in the LUAD demo trained on the same data [specific number from Vocht 2026, may reflect a slightly different training run]. This large multiplier explains why EGFR and KRAS appear mutually exclusive in LUAD even in cross-sectional data: both are common drivers, but EGFR's high observation-boosting effect creates a spurious suppressive signal in uncorrected models.

4. **Correcting for bias uncovers promoting effects.** After correction, several gene pairs that appeared suppressive in uncorrected fits are revealed to be neutral or promoting — consistent with independent biological evidence. [UNVERIFIED: specific gene pairs beyond TP53 in CRC and EGFR in LUAD.]

5. **Model is a strict extension of cMHN.** Setting all observation rate multipliers to zero recovers the classical MHN (Schill 2020), making this a backwards-compatible generalization. The `mhn` Python package (Vocht 2026) supports both formulations for direct comparison.

## Relevance

This paper is directly relevant to **q012** and to the project's mutation co-occurrence and ordering analyses, on two levels:

**1. Co-occurrence and mutual exclusivity analysis (t078)**

The cbioportal pipeline aggregates cross-sectional data from diagnostic cohorts — exactly the setting where collider bias is unavoidable. If we apply naive co-occurrence statistics (Fisher's exact test, DISCOVER, odds-ratios), or fit CBN/MHN-style ordering models without the observation-event correction, we risk:

- **False mutual exclusivity:** Two genes that both increase detectability will appear anti-correlated even if they are biologically independent. In our MSK-IMPACT / GENIE data, EGFR and KRAS already show strong apparent mutual exclusivity in LUAD — part of this is real (oncogenic bypass through the same pathway), but part may be collider bias from EGFR's large observation-rate effect (10.91×).
- **False promoting suppression:** Drivers that are frequently early events and increase detectability (TP53 in CRC) will seem to suppress later events in uncorrected models, obscuring real promoting relationships.

**Implication:** Any mutual exclusivity finding in our pipeline that involves a highly detectable driver gene (EGFR in LUAD, TP53 in CRC, likely PIK3CA in breast) should be treated with additional skepticism until checked against an observation-event–corrected model.

**2. Mutation ordering inference (q012)**

The project's roadmap includes MHN fitting for directed ordering inference (A→B temporal sequences). Schill 2024 establishes that the *standard* MHN (Schill 2020) produces biased ordering inferences on diagnostic cohorts. The corrected model should be used if mutation ordering analysis is pursued (task: prerequisite before any MHN fit on cBioPortal data).

**3. Hypothesis h04 (if applicable)**

If the project formalizes a hypothesis about gene-cancer epistasis or ordering, the observation-event correction defines the methodological lower bar that any such hypothesis test must clear. A finding from a cMHN without correction cannot be treated as evidence for or against biological ordering.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Observation event (n+1th event) | Clinical ascertainment / diagnosis | All cBioPortal studies are diagnostic cohorts; observation event is always present |
| Observation rate multiplier per gene | Detectability bias per driver | EGFR (LUAD), TP53 (CRC) are largest known multipliers; unknown for most genes |
| Spurious anti-correlation from collider | Apparent mutual exclusivity in co-occurrence analysis | Affects t078 DISCOVER / Fisher results for high-detectability genes |
| Spurious suppressive MHN edge | False negative ordering edge | Affects any planned MHN fit on cBioPortal data |
| True promoting edge (unmasked) | Valid mutation ordering signal | Only recoverable after observation-event correction |
| n+1 × n parameter matrix | Extended MHN model | Implemented in `mhn` Python package (Vocht 2026) |
| Cross-sectional data | cBioPortal per-study MAFs + GENIE | All studies in pipeline are single-biopsy diagnostic snapshots |

## Limitations

- The observation-event model requires estimating observation rate multipliers per gene from the same dataset used for training — this adds parameters and may reduce statistical power for rare drivers or small cohorts. The regularization choice (L1, L2, symmetric) influences which observation effects survive.
- The model assumes a single constant observation rate multiplier per gene, regardless of cancer type or clinical context (e.g., a gene that increases detectability via symptom burden in one cancer type may be neutral in another). In practice, the pipeline would need per-histology models.
- All drivers are modeled with the same functional form (multiplicative hazard on the observation event). Genes that affect detection through non-additive, non-stationary, or threshold mechanisms may not be fully captured.
- The correction is only as good as the coverage of events included in the model. If a key unobserved confounder (e.g., an unsequenced detectability-driving gene) is absent from the panel, residual bias remains.
- Both the journal article and the RECOMB conference paper are paywalled; specific quantitative results (exact log-likelihood comparisons, number of edges changed by correction, simulation benchmarks) are not verifiable from publicly available sources. Claims here are based on the abstract and the Vocht 2026 companion paper.

## Model / Tool Availability

The observation-event MHN described in this paper is the default model in the **`mhn` Python package** (Vocht et al. 2026, Bioinformatics Advances, doi: 10.1093/bioadv/vbaf283):

- **GitHub:** https://github.com/spang-lab/LearnMHN
- **PyPI:** `mhn` (installable via pip; project uses `uv add`)
- **Documentation:** https://learnmhn.readthedocs.io/en/latest/
- **License:** MIT
- **Hardware:** CPU default; CUDA GPU optional (substantially faster for >25 events)
- **Practical limit:** ~25–32 active events per sample; state space restriction allows >100 events in the panel as long as no single sample carries >32 simultaneously

The classical MHN (Schill 2020, without observation-event correction) is also available in `mhn` for backwards compatibility comparisons.

## Follow-up

- **Read Schill 2020** (doi: 10.1093/bioinformatics/btz513, PMC6956791 — OA) to understand the classical MHN framework before the observation-event extension; foundational for interpreting the correction.
- **Read Rupp et al. 2024** (doi: 10.1093/bioinformatics/btae250, PMC11245855 — OA) — a closely related extension of MHN to metastatic progression, also from the Schill / Beerenwinkel group; uses cross-sectional data across primary + metastatic samples.
- **Obtain the Schill 2024 PDF** via institutional access (PMID 39480133) to verify the specific quantitative results (simulation benchmarks, exact edge counts changed by collider correction, sensitivity analysis on regularization choice).
- **Pilot in the project:** Before any t078 / q012 MHN analysis, install `mhn` and run a single-cancer-type demo (e.g. LUAD from GENIE, matching the paper's own demo) to confirm the observation-event model is estimable on our data and to benchmark runtime against sample count and panel size.
- **Assess per-gene detectability biology:** Which genes in the pipeline's 10k-gene universe are likely to have large observation rate multipliers? TP53 (CRC), EGFR (LUAD) are known; BRCA1/2 in ovarian (strong family history screening), PIK3CA in breast, VHL in RCC are plausible candidates. This list would inform which apparent mutual-exclusivity results are highest-risk for collider-bias inflation.
- **Check q012 for update:** The question file already notes MHN as the recommended tool; add a note that the observation-event correction (Schill 2024) is required — the cMHN (Schill 2020) alone is insufficient for this pipeline's diagnostic cohort data.
