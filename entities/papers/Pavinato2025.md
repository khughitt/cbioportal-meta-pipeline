---
type: paper
title: 'Oncogenic competence: balancing mutations, cellular state, and microenvironment'
status: active
created: '2026-06-07'
updated: '2026-06-28'
id: paper:Pavinato2025
ontology_terms:
- oncogenic competence
- cell-of-origin
- cellular lineage
- differentiation state
- tumor microenvironment
- epigenetic state
- chromatin landscape
- tissue specificity
- cancer driver genes
- tumor initiation
- neural crest
- melanoma
- context-dependent oncogenesis
- lineage transcription factors
source_refs:
- cite:Pavinato2025
related:
- topic:lineage-addiction-and-cell-of-origin-driver-specificity
- question:0042-driver-normal-expression-tissue-cell-type-specificity
- discussion:0008-tissue-cell-type-specificity-of-cancer-drivers
- topic:oncofetal-developmental-reprogramming
- paper:Haigis2019
- paper:Garraway2006
---

# Oncogenic competence: balancing mutations, cellular state, and microenvironment

- **Authors:** Lisa Pavinato, Arianna Baggiolini
- **Year:** 2025
- **Journal:** Trends in Cancer, Vol. 11, No. 4 (April 2025; 10th Anniversary Special Issue)
- **DOI/URL:** https://doi.org/10.1016/j.trecan.2025.01.002
- **BibTeX key:** Pavinato2025
- **Source:** PDF (open access, CC BY-NC)

## Key Contribution

This oncogenic-competence review note links topic:lineage-addiction-and-cell-of-origin-driver-specificity, discussion:0008-tissue-cell-type-specificity-of-cancer-drivers, and topic:oncofetal-developmental-reprogramming.

This Opinion piece introduces and systematizes the concept of **oncogenic competence** — the
idea that tumor-causing mutations only trigger malignant transformation within specific cellular
contexts. The same driver mutation in the same gene can initiate cancer in one cell type/state
but be inert (or even growth-suppressive) in another, even under identical mutational load. The
authors frame oncogenic competence as a "cellular black box" shaped by three interacting
layers: (1) intrinsic cell-state determinants (transcriptional and epigenetic programs tied to
lineage and differentiation stage), (2) metabolic profile coupled to differentiation, and (3)
extrinsic microenvironmental signals. The paper argues that understanding and ultimately
targeting oncogenic-competent states — rather than the mutations themselves — represents a
new frontier for cancer prevention and treatment.

## Methods

This is an Opinion/Perspective article in the Trends in Cancer 10th anniversary special issue.
No new experimental data are presented. The authors synthesize published experimental
evidence across multiple model systems and cancer types, organized around three conceptual
pillars of oncogenic competence (lineage, differentiation state, microenvironment). Key evidence
is drawn from:

- Mouse and human melanoma models using `Tyr::CreERT2 BrafV600E Pten−/−` and related
  lines (Baggiolini et al. 2021, Science, ref [1]) — the Baggiolini lab's own foundational work.
- Human embryonic stem cell (hESC) and human pluripotent stem cell (hPSC) models of
  pediatric glioma (K27M and G34R mutations in histone 3.3; refs [28, 44]).
- COSMIC v100 data for cross-tumor driver mutation frequencies (Figure 1B).
- PIK3CA^H1047R^ studies in esophagus vs. skin epidermis (refs [25, 26]).
- Basal cell carcinoma (BCC) extracellular matrix studies (ref [46]).
- Mathematical modeling of nevus melanocyte growth arrest (ref [50]).

## Key Findings

### Definition and framing of oncogenic competence

Oncogenic competence is the property of a cell that makes it responsive to a tumor-initiating
mutation. It is not a static property of a gene or even a tissue — it is dynamic, cell-state-specific,
and modulated in time and space. Cancer is framed as not a purely genetic disease: the
tumorigenic potential of a DNA mutation depends on the overall transcriptional and epigenetic
programs active in the cell at the moment of mutation acquisition.

Crucially, healthy tissues can harbor substantial clonal expansions of cells carrying known
cancer driver mutations without tumor formation — sun-exposed skin in middle age has roughly
1 in 4 cells carrying such mutations; the esophagus shows similar selection for cancer-gene
clones. This demonstrates that mutations are necessary but not sufficient: oncogenic competence
is the additional required condition.

### Pillar 1 — Cellular lineage

Most driver mutations are tissue-specific in their oncogenic output despite being acquired in
broadly-expressed genes. Examples discussed:

- **BRCA1/BRCA2**: ubiquitously expressed; germline loss of function confers risk almost
  exclusively for breast and ovarian cancer.
- **NF1/NF2**: germline mutations cause neurofibromatosis with nerve-sheath tumor predisposition
  (neurofibroma, Schwannoma), reflecting selective oncogenic competence in Schwann cells of
  the peripheral nervous system.
- **PAX8 and VHL/HIF2A in clear-cell renal cell carcinoma (ccRCC)**: VHL loss (present in
  ~90% of ccRCCs) stabilizes HIF2A; HIF2A only drives ccRCC because it co-occupies
  chromatin with the kidney-lineage transcription factor PAX8, which directs the complex to
  the CCND1 enhancer and MYC targets. Without PAX8, the same VHL/HIF2A axis does not
  produce this oncogenic output. This is a clean mechanistic demonstration that lineage
  transcription factors are key modulators of tissue-specific oncogenic competence.
- **BRAF^V600E^ in colon**: occurs in proximal but not distal colon, reflecting distinct regional
  transcriptional programs that differentially regulate stemness and proliferation.
- **SMO (Hedgehog) in BCC**: oncogenic Smo drives BCC only in tail/ear epidermis of mice,
  not back skin, due to differences in extracellular matrix composition, collagen network, and
  stiffness.
- **PIK3CA^H1047R^ context-switch**: in esophagus, the same mutation confers a proliferative
  clonal advantage (enhanced by obesity/high-fat diet, reduced by metformin); in skin
  epidermis, PIK3CA^H1047R^ forces epidermal progenitor differentiation and *suppresses*
  epidermal growth. The same oncogenic allele is growth-promoting in one lineage and
  growth-suppressive in another.

The pre-existing chromatin profile of the cell of origin is highlighted as the strongest
determinant of the cancer mutational landscape (Polak et al. 2015, Nature), to the point that
statistical models can predict tumor-of-unknown-origin from DNA sequencing alone.

### Pillar 2 — Differentiation state within a lineage

Even within the same lineage, cells at different stages of differentiation respond differently to
the same mutation:

- **Melanoma / BRAF^V600E^**: melanoblasts (progenitors) are readily transformed by
  BRAF^V600E^; mature melanocytes in the same mouse with the same mutation load are not.
  Mature melanocytes can be rendered oncogenic-competent by acquisition of additional
  features — loss of tumor suppressors, or epigenetic rewiring (e.g., expression of ATAD2,
  which activates a progenitor signature and drives partial dedifferentiation). This is the
  Baggiolini et al. 2021 (Science) finding — the authors' own lab's foundational work on
  "developmental chromatin programs determining oncogenic competence."
- **Histone 3.3 K27M glioma**: this histone mutation induces cancer only in neural progenitor cells,
  not in differentiated somatic cells.

The differentiation-state axis is linked to **metabolism**: as cells differentiate they change their
metabolic profile, and metabolic state feeds back on epigenetic and transcriptional programs
(e.g., mitochondria controlling stem cell fate, metabolites regulating chromatin modification).
Metabolic changes during malignant transformation may be both drivers of, and consequences
of, oncogenic competence — the authors flag the "chicken-and-egg" problem.

### Pillar 3 — Microenvironment (extrinsic)

The tumor microenvironment (TME) — comprising extracellular matrix, immune cells, fibroblasts,
endothelial cells, pericytes, neurons, adipocytes, and the microbiome — also determines
oncogenic competence:

- **Tissue injury and inflammation**: cirrhosis and pancreatitis are predisposing conditions for
  liver and pancreatic cancer; tissue damage in the presence of predisposing mutations triggers
  transcriptional and chromatin changes that accelerate tumor development.
- **Neuronal microenvironment**: NF1 patients develop optic pathway gliomas; optic nerve
  neuronal activity directly contributes to tumor initiation (Pan et al. 2021, Nature). This
  illustrates how the local nervous system is a component of the oncogenic microenvironment.
- **Intraorgan microenvironmental heterogeneity**: the histone 3.3 G34R variant, ATRX, and TP53 mutations
  drive high-grade glioma only in forebrain, not hindbrain, progenitor cells — confirmed in
  hPSC-based models (Funato et al. 2021). BCC driven by oncogenic Smo affects tail/ear
  but not back skin epidermis. Cutaneous vs. acral melanoma carry entirely different driver
  profiles (BRAF/NRAS vs. CCND1/CDK4/MDM2 amplifications), partly attributable to
  anatomical location and local microenvironment rather than UV exposure differences.
- **Nevus arrest**: nevi (BRAF/NRAS mutant benign melanocytic lesions) rarely progress to
  melanoma not because of intrinsic senescence but because the microenvironment tightly
  controls clonal expansion — nevus melanocytes are not truly senescent relative to other skin
  cells; mathematical modeling attributes growth arrest to microenvironmental modulatory
  interactions.
- **Keratinocyte-melanocyte GABAergic signaling**: keratinocytes regulate melanoma initiation
  by establishing GABAergic interactions with melanocytes that modulate local electrical
  activity, promoting tumor initiation — a striking example of a non-cell-autonomous
  oncogenic competence regulator.
- **Mouse melanoma models (Tyr::CreERT2 BrafV600E Pten−/−)**: in the same genetic
  background, mature pigmented melanocytes in tail epidermis gave rise to melanoma via
  dedifferentiation, while melanocyte stem cells in hair follicles of back skin gave rise to
  melanoma in response to UVB — two distinct cells-of-origin responding to the same
  oncogenic signals depending on their local microenvironment.

### Therapeutic and prevention implications

The authors propose that targeting the mechanisms that render cells oncogenic-competent —
rather than the mutations themselves — could enable novel strategies to:

1. Transition cells from an oncogenic-competent state to a refractory one (or prevent the
   transition to competence).
2. Design context-specific cancer prevention approaches.
3. Interrogate whether a "point of no return" exists beyond which state-switching is no longer
   possible — relevant to understanding relapse and resistance.

The rising incidence of tumors in young adults, combined with cross-country variation, is noted
as underscoring the importance of environmental/epigenetic modulation of oncogenic competence.

## Relevance

This paper is the mechanistic heart of the **"route-2" context-dependent driving** framing
relevant to `question:0042-driver-normal-expression-tissue-cell-type-specificity`.

**Why drivers are tissue-specific even when broadly expressed.** The core explanatory move
in Pavinato2025 — that competence lives in the cell state, not in the gene's expression level —
directly addresses the puzzle that motivates question:0042. A gene like BRAF or PIK3CA is broadly
expressed, so its expression pattern cannot explain why its mutations drive cancer in some
tissues but not others. Pavinato2025 resolves this by pointing to the transcriptional, epigenetic,
metabolic, and microenvironmental context: these factors determine whether the same activated
gene product produces a malignant or neutral (or even suppressive) cellular outcome.

**Relationship to paper:Haigis2019.** Both papers argue that tissue-specific driver effects are
the rule, not the exception. Haigis2019 is a short perspective that names the phenomenon and
illustrates it with examples; Pavinato2025 provides the mechanistic taxonomy (lineage /
differentiation state / microenvironment) and connects each pillar to specific experimental
evidence. Pavinato2025 can be read as the mechanistic elaboration of the Haigis2019 thesis.

**Relationship to paper:Garraway2006.** Garraway2006 explains tissue-specific drivers via
tissue-restricted *expression* of the oncogene (lineage-survival oncogenes — e.g., MITF in
melanoma, AR in prostate). Pavinato2025 explains a distinct route: broadly-expressed genes
whose *functional consequence after mutation* is tissue/state-specific. The PAX8-HIF2A
example in Pavinato2025 is a hybrid: VHL is broadly expressed but its oncogenic output is
gated by PAX8 expression (a lineage TF) — this is mechanistically closer to Garraway2006's
lineage-survival logic but applied to a tumor suppressor rather than an amplified oncogene.

**For the cell-of-origin framework.** Pavinato2025 is one of the strongest current synthetic
treatments of cell-of-origin as a driver of tissue specificity. The Baggiolini lab's own melanoma
data (Baggiolini et al. 2021, ref [1] in this paper) is the foundational experimental evidence base
— the paper is partly a review of their own prior work positioned within the broader literature.

**Connection to multistage/age thread.** The authors explicitly note that oncogenic competence
is not in contradiction with the classical multistage carcinogenesis model; rather, the state of
oncogenic competence determines how many and which combinations of driver mutations are
required. This is a permissive-state framing: some cells are pre-primed (competent) and need
fewer mutational hits; others are refractory and require more. This is mechanistically relevant to
age-incidence relationships and the route-2 framing of question:0042.

**For the project's gene × cancer frequency tables.** The pipeline captures the empirical
*output* of oncogenic competence — high-frequency mutation of a given gene in a given cancer
type means that gene's mutation conferred fitness in that oncogenic-competent context. But the
pipeline cannot distinguish whether high frequency arises from lineage-survival addiction
(Garraway2006 route) vs. context-dependent competence (Haigis2025/Haigis2019 route).
Pavinato2025 motivates building a second-tier annotation layer that identifies whether
tissue-specific high-frequency drivers are (a) lineage-restricted in normal expression or
(b) broadly-expressed with state-gated oncogenic competence.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Oncogenic competence (cellular black box) | Context-dependent driver behavior | The conceptual framework explaining why gene × cancer frequency is tissue-stratified |
| Cellular lineage as competence determinant | Cancer type in gene_cancer_study tables | Each cancer type represents a lineage; high per-cancer frequency = lineage-competent driver |
| Differentiation state as competence determinant | Cell-of-origin heterogeneity within cancer type | Not currently captured in the pipeline; relevant to intra-tumor heterogeneity and study-level variability |
| Lineage transcription factor gating (PAX8 example) | Not modeled | Mechanistic explanation for why some broadly-expressed genes are tissue-specific drivers |
| Microenvironment as competence modulator | Not modeled | Extrinsic axis; relevant to TME-driven driver frequency differences across studies |
| PIK3CA^H1047R^ context-switch (growth-promoting vs. suppressive) | Non-monotonic gene × tissue relationships | Motivates checking for sign-flip patterns in gene × cancer frequency tables |
| Pre-existing chromatin profile → mutational landscape | Bailey2018 per-cancer driver rosters | Polak et al. 2015 cited: chromatin of cell of origin is strongest determinant of cancer mutations |
| Oncogenic-competent vs. refractory state as therapeutic target | Not in scope | Prevention framing; relevant to long-horizon project goals |

## Limitations

- As an Opinion piece (~10 pages), the paper synthesizes rather than tests the oncogenic
  competence framework; the three-pillar structure (lineage, differentiation, microenvironment)
  is the authors' conceptual organization, not an empirically derived taxonomy.
- The paper does not formalize how to measure or operationalize "oncogenic competence" — it
  remains a conceptual umbrella rather than a quantifiable variable. The authors acknowledge
  this in the Outstanding Questions.
- The melanoma / BRAF^V600E^ example (pillar 2) is heavily drawn from the corresponding
  author's own prior work (Baggiolini et al. 2021); the framework may be more fully elaborated
  for neural-crest-derived tumors than for others.
- The distinction between lineage-specific oncogenic competence (pillar 1) and differentiation-
  state-specific competence within a lineage (pillar 2) is conceptually clear but can be blurry
  in practice — dedifferentiation can change both the lineage identity and the differentiation
  stage simultaneously.
- The metabolic coupling to differentiation state is invoked but the mechanistic details remain
  underdeveloped; the authors flag this as an open area.
- The paper does not systematically address how to predict, from molecular features, which cells
  are oncogenic-competent for a given mutation — the Outstanding Questions acknowledge this.

## Model / Tool Availability

No computational tools, datasets, or models are released. This is an Opinion article. The
authors recommend hPSC-based model systems and human tissue organoids as experimental
platforms to interrogate oncogenic competence, but do not release these tools in this paper.

## Follow-up

- **Baggiolini et al. 2021 (Science 373, eabc1048)** — the foundational experimental paper from
  the Baggiolini lab demonstrating that BRAF^V600E^ transforms melanoblasts but not mature
  melanocytes, and that ATAD2-mediated epigenetic rewiring can restore competence. This is
  ref [1] and the empirical backbone of Pavinato2025's differentiation-state pillar. Should be
  read alongside Pavinato2025 for the full mechanistic detail.
- **Bansaccal et al. 2023 (Nature 623, 828–835)** — extracellular matrix dictates regional
  competence for tumor initiation; the BCC/skin stiffness example in Pavinato2025. Directly
  demonstrates a molecular mechanism by which microenvironment shapes competence.
- **Patel et al. 2022 (Nature 606, 999–1006)** — PAX8 lineage TF controlling HIF2A oncogenic
  signaling in ccRCC; cited as the cleanest mechanistic example of lineage-TF-gated oncogenic
  competence.
- **Polak et al. 2015 (Nature 518, 360–364)** — cell-of-origin chromatin organization shapes
  cancer mutational landscape; the empirical basis for using chromatin state to predict
  tumor-of-unknown-origin. Highly relevant to the project's per-cancer driver analysis.
- **Herms et al. 2024 (Nat. Genet. 56, 2144–2157)** — organismal metabolism regulates
  PIK3CA mutant clone expansion in esophagus (metformin / obesity angle); demonstrates
  metabolic modulation of oncogenic competence in human normal tissue.
- **paper:Haigis2019** — the complementary framing paper; Pavinato2025 is its mechanistic
  elaboration.
- **paper:Garraway2006** — lineage-survival oncogenes; contrasting mechanism to
  context-dependent competence.
- **question:0042-driver-normal-expression-tissue-cell-type-specificity** — the three-pillar
  competence framework directly informs how to build a two-route explanatory model for
  tissue-specific driver behavior: lineage-survival (Garraway2006 route) vs. competence-gated
  broadly-expressed oncogenes (Pavinato2025/Haigis2019 route).
- **Project question**: Can the pipeline's per-cancer mutation-frequency tables be used to
  detect genes that show PIK3CA-like context-switches — high frequency in one cancer type
  but absent or under-represented in closely related cancer types despite similar tissue
  expression levels? Such genes would be candidates for competence-gated rather than
  lineage-survival drivers.
