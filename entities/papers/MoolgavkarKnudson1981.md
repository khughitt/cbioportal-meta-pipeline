---
type: paper
title: 'Mutation and cancer: a model for human carcinogenesis'
status: active
created: '2026-06-07'
updated: '2026-06-28'
id: paper:MoolgavkarKnudson1981
ontology_terms:
- multistage carcinogenesis
- two-stage clonal expansion
- cancer incidence
- age-of-onset
- retinoblastoma
- tumor suppressor
- cell proliferation
- mathematical modeling
source_refs:
- cite:MoolgavkarKnudson1981
related:
- topic:multistage-carcinogenesis-and-age-of-onset
- question:0041-driver-complexity-vs-median-age-at-diagnosis
- paper:ArmitageDoll1954
- paper:Knudson1971
- theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the
---

# Mutation and cancer: a model for human carcinogenesis

- **Authors:** Suresh H. Moolgavkar, Alfred G. Knudson Jr.
- **Year:** 1981
- **Journal:** Journal of the National Cancer Institute, 66(6):1037–1052
- **DOI/URL:** https://doi.org/10.1093/jnci/66.6.1037
- **PMID:** 6941039
- **BibTeX key:** MoolgavkarKnudson1981
- **Source:** Full text read from PDF (`~/downloads/moolgavkar1981.pdf`, 16 pp., scanned + OCR, extracted cleanly via `pdftotext`). Affiliation confirmed as The Institute for Cancer Research, Fox Chase Cancer Center, Philadelphia.

## Key Contribution

This multistage carcinogenesis model note links theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the.

This paper introduces the two-stage clonal-expansion model of carcinogenesis — often called the MVK model (Moolgavkar–Venzon–Knudson) or TSCE model (two-stage clonal expansion). The paper's central claim, stated explicitly in the abstract and conclusion, is that *two* heritable events (not five to seven, as Armitage–Doll multistage fits suggested) are sufficient to account for the full spectrum of human cancer incidence curves — from embryonal/childhood-peak tumors through adult log-log carcinomas through the complex hormone-modulated shape of breast cancer — provided that the **intermediate cell (IC) compartment is allowed to grow and die**. The proliferative dynamics of ICs (parameterised by birth rate α₂ and death/differentiation rate β₂) bend the incidence curve in ways that no fixed-stage mutation-counting model can reproduce. The paper also embeds Knudson's two-hit retinoblastoma hypothesis formally within this stochastic framework and gives a precise mechanistic interpretation of tumor promotion: promoters raise α₂ − β₂ for ICs, not mutation rates.

## Methods

### Biological formulation

The model posits three cell classes and five parameters:

| Symbol | Role |
|--------|------|
| X(t) | Number of susceptible normal stem cells (NC) at time t — treated deterministically; grows with tissue via a Gompertz (lung, colon) or logistic (breast) or gamma-density (childhood) growth curve |
| μ₁ | Rate per cell per year: NC → IC (first heritable event) |
| α₂ | Birth rate of IC per cell per year |
| β₂ | Death/differentiation rate of IC per cell per year |
| μ₂ | Rate per cell per year: IC → malignant cell (MC) (second heritable event) |

Key biological assumptions stated in the paper:
- A single MC gives rise to a tumor with probability 1 (i.e., detection latency is treated as a constant offset, not stochastic — the authors note this simplification explicitly).
- Each heritable event occurs in a single cell division and is irreversible.
- Cells transform independently; NC divisions generate IC via a Poisson process with expectation ∫₀ᵗ μ₁ X(s) ds.
- IC undergo a birth–death–mutation branching process: in interval dt, an IC divides into two ICs with probability α₂dt, dies or differentiates with probability β₂dt, or yields one IC + one MC with probability μ₂dt.

The paper explicitly notes (in the "Mathematical Formulation" section) that the reference for the full derivation is its 1979 mathematical-biology predecessor (Math Biosci 47:55–77), and provides only an appendix sketch here.

### The key incidence equation

For small μ₂, the age-specific incidence rate I(t) (per individual) is given exactly in the paper as:

> **I(t) ≈ μ₁μ₂ ∫₀ᵗ X(s) · exp[(α₂ − β₂)(t − s)] ds**

with the age-specific incidence per 100,000 being I(t) × 10⁵ [@MoolgavkarKnudson1981].

The appendix gives the exact hazard function derivation via generating functions. Let ψ(z,w,t) be the generating function for the number of ICs and MCs at time t from all NC lineages, and φ(z,w,t) the corresponding function for descendants of a single IC. Then:

> ψ(z,w,t) = exp[ μ₁ ∫₀ᵗ X(s){ φ(z,w,t−s) − 1 } ds ]

and the hazard is:

> I(t) = −ψ'(1,0,t) / ψ(1,0,t)

which simplifies (for small μ₂) to I(t) = μ₂ · E[Z(t) | W(t) = 0], where Z(t) is the number of ICs and W(t) is the number of MCs.

Two structural consequences follow immediately from the approximate expression:
1. The transition rates μ₁ and μ₂ enter only as a product (μ₁μ₂), so they cannot be separately identified from population incidence data. Separate estimation of μ₂ requires hereditary-cancer incidence data (where all target cells start as ICs).
2. The **shape** of the incidence curve is determined entirely by X(s) (tissue growth) and (α₂ − β₂) (IC net growth advantage). The **level** of the curve is set by μ₁μ₂.

### Relationship to Armitage–Doll

The paper proves explicitly that when (a) NC count is constant and (b) α₂ > β₂, the model recovers the Armitage–Doll (1957) two-stage deterministic exponential-growth model. That earlier model generates incidence ∝ t^k for appropriate k; the present model shows that k is determined by α₂ − β₂, not by the number of mutation stages.

When α₂ < β₂ (IC growth disadvantage), the incidence curve peaks and declines — the childhood-tumor pattern. Text-figure 3 in the paper demonstrates this explicitly using X(s) proportional to s·exp(−s) (a gamma density) to simulate tissues where dividing target cells peak early then disappear (e.g., retinoblasts).

### Fitting strategy

- **Free parameters estimated from data:** Usually only α₂ − β₂ is estimated by maximum likelihood; μ₁μ₂ and the scale of X(s) are fixed at preassigned values.
- Text-figure 4A shows a maximum-likelihood fit to Doll's lung cancer in nonsmokers data (ages 40–80), yielding **α₂ − β₂ = 0.067 per year** with μ₁μ₂ = 3 × 10⁻¹⁴ and 10⁷ target cells (5% present at birth, Gompertz growth complete by age 20).
- Text-figure 5 shows fits to breast cancer incidence across six populations (Connecticut, Denmark, Finland, Slovenia, Iceland, Osaka), normalised so total rates sum equally, with all curves generated by adjusting only μ₁ and μ₂ (the shape driven by tissue kinetics is shared).
- Text-figure 2 shows the sensitivity: for μ₁μ₂ = 3 × 10⁻¹⁴ and 10⁷ adult target cells, varying α₂ − β₂ across 0, 0.04, 0.06, 0.08, 0.09 changes incidence at age 70 by roughly an order of magnitude — "incidence is very sensitive to small changes in α₂ − β₂."

## Which cancer types are treated in this paper

Confirmed from the PDF — the paper explicitly models and fits data for the following:

| Cancer | Treatment |
|--------|-----------|
| **Lung cancer (nonsmokers)** | Quantitative fit (text-fig. 4A/4B); α₂ − β₂ = 0.067 estimated by ML from Doll (1971) data; log-log plot confirms log-linear fit on double logarithm scale |
| **Breast cancer (female)** | Quantitative fit across 6 populations (text-fig. 5 and 6); hormonal modulation via growth curve; first-birth protective effect modelled; radiation risk predictions; hereditary breast cancer interpretation |
| **Retinoblastoma** | Qualitative/conceptual treatment — cited to prior papers by Knudson, Hethcote & Knudson (refs 12, 13); referenced as confirming that the model "provides an excellent description of the data" |
| **Colon cancer / familial polyposis** | Qualitative — adenomatous polyps as intermediate lesions; familial polyposis as germline first hit; Table 1 includes colon carcinoma |
| **Other childhood tumors** | Qualitative — neuroblastoma, Wilms' tumour, acute lymphocytic leukemia mentioned; text-fig. 3 shows the generic IC-growth-disadvantage curve |

**Retinoblastoma is not fitted quantitatively in this 1981 paper** — that work is in refs 12–13, covering earlier retinoblastoma modeling papers. Lung cancer (nonsmokers) and breast cancer are the two fully fitted examples here.

## Key Findings

### 1. Two mutations with IC proliferation reproduce all human incidence curve shapes

The paper demonstrates (text-figs 2 and 3) that the three empirical patterns of human cancer incidence — (1) log-log power-law increase, (2) increase with a mid-life deceleration (breast), (3) childhood peak then decline — all arise from one model structure with different tissue growth curves and signs of α₂ − β₂. No ad hoc multi-stage extension is needed.

### 2. The incidence-curve slope (power of age) is set by IC kinetics, not by mutation count

For the log-log cancers (colon, stomach), the slope of log(incidence) vs. log(age) is between 5 and 7 in population data. Armitage–Doll interpreted this as requiring 6–8 stages. The MVK model shows that the same slope is generated by α₂ − β₂ > 0 within a two-stage framework; "the power of age [is] being determined by the kinetics of growth of the IC." (Direct quote, p. 1043.)

### 3. Promotion = raising α₂ − β₂, not raising mutation rates

The paper provides a precise mechanistic definition: initiators perform the first mutation event; promoters "act on the IC to increase α₂ − β₂." This leads to proliferation of preneoplastic lesions (papillomas). Regression on promoter withdrawal occurs because α₂ − β₂ returns to baseline. The model predicts that agents affecting IC kinetics are disproportionately efficient ("small changes in α₂ − β₂ lead to large changes in incidence") compared to agents affecting transition rates.

A key distinction for environmental agents:
- Agents that raise μ₁ or μ₂ → relative risk (RR) vs. unexposed remains *constant* with duration of exposure
- Agents that raise α₂ − β₂ → RR *increases* with duration of exposure ("duration of exposure is an effect modifier")
The data on ex-smokers (extra risk stays approximately constant after cessation, not reverting to baseline) are interpreted as indicating smoking primarily raises α₂ − β₂ (IC proliferation), not μ₁.

### 4. Hereditary cancers: germline first hit → all target cells are ICs at birth

For dominant hereditary cancers (retinoblastoma, familial polyposis, hereditary breast cancer), the model proposes the first event is germline, so every target cell is born as an IC. Risk is then governed by μ₂ alone (not μ₁μ₂). This explains: earlier onset, higher penetrance, bilateral/multifocal presentation. The paper states the gene proposed for familial breast cancer (cited as chromosome #10, linked to glutamate pyruvate transaminase — a 1980 finding that was later revised) would make women "born with all the cells of the breast epithelium in the intermediate stage," and predicts 80% lifetime penetrance consistent with that report [@MoolgavkarKnudson1981].

### 5. Intermediate lesions are clonal in sporadic cases, multicellular in hereditary cases

Table 1 lists putative intermediate lesions and predicts their clonal origin. For sporadic cases (somatic first hit after X-inactivation), IC clones express a single X-linked allele. For hereditary cases (germline first hit before X-inactivation), IC lesions express both alleles. The paper lists tested examples: sporadic neurofibromas (confirmed clonal), neurofibromas in neurofibromatosis (confirmed multicellular), colonic adenomas, lobular carcinoma in situ, C-cell hyperplasia of thyroid, neuroblastoma IV-S.

### 6. Radiation risk predictions confirmed

The model predicts that a single high-dose radiation exposure will generate ICs (first hits) and directly promote some ICs to MCs. It then predicts that RR will decline with age at irradiation (fewer remaining IC-doubling years), while excess risk per year will increase. The paper works through a numerical example: for a hypothetical tumor with age-specific incidence 1,500/million at age 60 and 94/million at age 30, 100 rads gives RR 3.02 at age 30 vs. 1.62 at age 60, but excess risk 366 vs. 1,310 per million per year. This pattern was confirmed in atomic bomb survivor data (Beebe et al. 1978, cited as ref 20) and radiation-induced breast cancer studies [@MoolgavkarKnudson1981].

### 7. No support for linear dose-extrapolation as a universal rule

The model implies that appropriate dose-extrapolation form depends entirely on whether the agent acts on μ₁/μ₂ (linear extrapolation may be appropriate) or on α₂ − β₂ (incidence is a far-from-linear function of dose at fixed age). "Sensible extrapolations can be made only when the mode of action of the environmental agent is known."

## Tissue Growth / Developmental Considerations

The paper classifies tissues into three growth patterns, and maps each to a cancer incidence pattern:

1. **Gompertz growth** (lung, colon): steady increase through childhood, adult plateau with ongoing cell turnover → log-log incidence pattern (adult carcinomas). Fit: 10⁷ target cells at adult size, 5% present at birth, growth complete by age 20.
2. **Logistic growth** (breast, sex organs): puberty growth spurt, hormonal modulation → incidence with mid-life "hook" at menopause. Breast involution after menopause decreases α₂ − β₂, attenuating the incidence slope.
3. **Gamma-density / rapid early peak then decline** (lymphoid, neural, retina): target cells peak in early life, then disappear (retinoblasts gone by age 5) → childhood peak incidence. The model predicts α₂ < β₂ for these tissues (IC growth disadvantage), so IC clones shrink, and malignant transformation requires catching the brief window of dividing target cells.

The developmental structure of tissue growth is thus the direct determinant of the **age-of-onset distribution shape**, independent of mutation rates. This is the paper's most fundamental claim for understanding differential onset across cancer types.

## Relevance to the cbioportal Project

This paper is foundational to the project's age-of-onset thread (question:0041-driver-complexity-vs-median-age-at-diagnosis; topic:multistage-carcinogenesis-and-age-of-onset).

**Why the MVK model matters for cross-study mutation-frequency analyses:**

- **The incidence equation is multiplicative in three separable factors:** I(t) ≈ μ₁μ₂ × ∫X(s)ds (target cell availability, governed by tissue growth) × exp[(α₂−β₂)(t−s)] (IC proliferative fitness). In the pipeline's language: per-gene mutation frequency captures a partial proxy for μ₁ and μ₂, but the model shows that cancer type differences in *age-specific* incidence reflect **all three factors multiplicatively**. Comparing raw mutation frequencies across cancer types conflates mutation rates with tissue-specific cell dynamics.

- **Driver count alone does not determine age of onset.** The paper explicitly shows that log-log incidence slopes of 5–7 (historically interpreted as "5–7 stages") arise from α₂ − β₂ > 0 in a two-stage model. A cancer type with a high required driver count but slow IC proliferation may present at similar ages to a two-driver cancer with vigorous IC expansion.

- **Clonal expansion is the missing layer.** The pipeline counts driver mutations but carries no representation of intermediate-clone dynamics. For cancers where promotion (raised α₂ − β₂) dominates — colorectal adenoma→carcinoma, cervical dysplasia, Barrett's oesophagus — cross-study mutation frequency comparisons may be misleading if not conditioned on lesion stage.

- **Connects to the Bailey driver overlay.** Bailey et al. [@Bailey2018] identify approved cancer drivers; the MVK model provides the theoretical basis for interpreting *why* different cancer types require different numbers of drivers, and for understanding why those counts must be placed in the context of tissue-specific proliferative background to predict onset age.

- **Caution about the pipeline's scope:** The MVK model generates predictions about *incidence-vs-age curves* in population-level registries. The cbioportal pipeline aggregates *prevalent somatic mutations* in clinical cohorts, which are shaped by age at diagnosis, sampling bias, sequencing panels, and study design. Clean MVK predictions live in population incidence, not in the pipeline's mutation-frequency tables — this limits direct quantitative translation, though the qualitative inference (target-cell counts and division rates matter as much as mutation rates) remains valid.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Number of target cells X(t) | Not represented | Pipeline counts mutations per sample; no normalisation for tissue-specific stem-cell pool size |
| IC birth rate α₂, death rate β₂ | Not represented | Clonal expansion dynamics are outside current pipeline scope |
| First mutation rate μ₁ | Per-gene mutation frequency (partial proxy) | Frequency tables aggregate somatic events but do not estimate per-cell-per-generation rates |
| Second mutation rate μ₂ | Per-gene mutation frequency for second hit | TSG loss-of-heterozygosity / second-hit calls not currently tracked |
| Two-hit requirement | Driver annotation (Bailey et al. [@Bailey2018] overlay) | Known TSGs implicitly included; two-hit structure not explicitly modelled |
| Promotion (increased α₂ − β₂) | Not represented | No analog for intermediate-clone fitness in current pipeline |
| Age-specific incidence λ(t) | Not computed | Pipeline aggregates across ages; per-age-group mutation frequency not currently a target output |
| Familial vs. sporadic first hit | Not represented | Germline variant calls are out of scope for the somatic MAF pipeline |
| Tissue growth pattern (Gompertz/logistic/gamma) | Not represented | No tissue-development normalisation |

## Limitations

From the paper itself:

- The model treats detection latency (MC → clinically apparent tumor) as a constant — the authors acknowledge this explicitly as a simplification. A stochastic formulation is deferred as adding parameters without present value.
- Parameters μ₁, μ₂, α₂, β₂ cannot all be independently estimated from general-population incidence data: only μ₁μ₂ and α₂ − β₂ are identifiable from such data. Separate estimation requires hereditary-cancer cohorts.
- Only μ₁ and μ₂ enter as a product in I(t), so their relative magnitudes are not individually constrained by population data.
- The two-event assumption is a model choice; the authors state: "A two-stage model is biologically reasonable because no more than two distinct stages have been experimentally demonstrated." They do not claim it is universal.
- The paper was written before the molecular identity of most proto-oncogenes and tumor suppressors was established. The mapping of "first event" and "second event" to specific gene alterations is left open.
- The model predicts that every cancer should also occur in a heritable autosomal dominant form (if germline first hits are non-lethal). The authors acknowledge the proportion of cancers clearly attributable to such predisposition is likely small.

## Model / Tool Availability

The MVK model is a mathematical framework derived in the authors' earlier mathematical-biology work and applied here. No software tools were associated with this 1981 JNCI paper. Subsequent implementations appear in TSCE2 and multi-stage extensions by later Moolgavkar-group work. The key equations are all reproduced in the paper's appendix and text.

## Follow-up

- **Armitage and Doll [@ArmitageDoll1954]** (paper:ArmitageDoll1954) — the multistage power-law predecessor model; the 1981 paper explicitly discusses how MVK subsumes it.
- **Knudson [@Knudson1971]** (paper:Knudson1971) — the two-hit retinoblastoma analysis whose genetic model MVK formalises stochastically.
- **The 1979 Math Biosci predecessor** — the immediate predecessor developing the full mathematical derivation; cited here as ref 15. Full citation confirmed from PDF reference list.
- **Moolgavkar, Day & Stevens 1980** (JNCI 65:559–569) — the quantitative breast cancer application referenced extensively as ref 16; confirmed from PDF.
- **Later TSCE extensions** — later multi-stage TSCE work fits colorectal adenoma→carcinoma progression.
- **Do the cross-study mutation-frequency differences in the cbioportal pipeline correlate with tissue-specific stem-cell division rates?** The MVK model predicts they should, and publicly available tissue stem-cell division rate estimates [@TomasettiVogelstein2015] could be used to test this.
- **Is there a way to infer net clonal expansion rates from multi-study VAF distributions in the pipeline outputs?** VAF distributions in cBioPortal MAFs might carry partial signal for this, though panel-sequencing data are noisy and clonal-expansion inference would require careful modelling of sampling depth and tumour purity.

## Relevance

This paper informs the linked topic and question context in the frontmatter. No additional interpretation is added here beyond the summary above.
