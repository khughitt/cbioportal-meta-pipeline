---
id: "paper:Haigis2019"
type: "paper"
title: "Tissue-specificity in cancer: The rule, not the exception"
status: "active"
ontology_terms:
  - tissue specificity
  - cancer driver genes
  - oncogene
  - tumor suppressor
  - cell-of-origin
  - lineage addiction
  - RAS signaling
  - context-dependent oncogenesis
  - tissue context
  - driver gene
  - epigenetic landscape
  - chromatin state
source_refs:
  - "cite:Haigis2019"
related:
  - "topic:lineage-addiction-and-cell-of-origin-driver-specificity"
  - "question:q042-driver-normal-expression-tissue-cell-type-specificity"
  - "discussion:2026-06-07-tissue-cell-type-specificity-of-cancer-drivers"
created: "2026-06-07"
updated: "2026-06-07"
---

# Tissue-specificity in cancer: The rule, not the exception

- **Authors:** Kevin M. Haigis, Karen Cichowski, Stephen J. Elledge
- **Year:** 2019
- **Journal:** Science, 363(6432): 1150–1151
- **DOI/URL:** https://doi.org/10.1126/science.aaw3472
- **BibTeX key:** Haigis2019
- **Source:** PDF (papers/pdfs/2019_Haigis_Tissue-specificity-in-cancer-the-rule-not-the-exception.pdf)

## Key Contribution

This two-page Science Perspective argues that tissue-specificity in cancer driver gene behavior
is the *rule*, not the exception: the same somatic mutation in the same gene can be strongly
oncogenic in one tissue and neutral or detrimental in another. The central thesis is that driver
status is a joint property of the mutation *and* the tissue context in which it occurs — not of
the gene alone. The authors' proposed unifying explanation is the **preexisting epigenetic
landscape**: oncogenes and tumor suppressors cannot exert their effects unless the chromatin and
proteomic state of a cell permits it to respond to that particular oncogenic signal. The
Perspective synthesizes named examples across oncogenes and tumor suppressors, cites a genetic
screen showing 80–90% of proliferation-promoting genes differ across cell types, and closes by
prescribing a comparative approach (permissive vs. nonpermissive tissues) for mechanistic driver
discovery.

## Methods

This is a Perspective / opinion piece. No new experimental data or computational analyses are
presented. The authors draw on published literature (12 cited references) to illustrate
context-dependent oncogenesis, support the epigenetic-landscape hypothesis, and argue for a
conceptual reframing of how driver genes should be understood.

## Key Findings

### Central thesis

Only a handful of drivers — TERT, TP53, CDKN2A, MYC — show a broad tissue spectrum. Almost all
others are tissue-restricted. This tissue-specificity of oncogene and tumor suppressor usage is
rooted in the underlying biology of tissues rather than in differences in expression or
mutability per se.

### Illustrative examples: where the mechanism *is* known

The authors open by noting three classes where an explanation is in hand:

1. **Tissue-specific expression.** ESR1 (estrogen receptor) is highly expressed and controls
   proliferation in estrogen-responsive tissues, explaining its role in ovarian, endometrial, and
   breast cancer.
2. **Tissue-specific exposure.** Xeroderma pigmentosum proteins (ERCC3, XPC) perform excision
   repair of UV-induced DNA damage; their loss primarily causes skin cancers because skin is
   uniquely exposed to UV radiation.
3. **Tissue-specific differentiation program.** GATA3 regulates breast ductal differentiation;
   its loss is enriched in breast cancers because it participates in a lineage-specific
   regulatory circuit that limits stem cell expansion.

### Illustrative examples: where the mechanism is *not* understood

These cases are the paper's argumentative core — broadly expressed essential genes with
tissue-restricted driver patterns that cannot be explained by the three classes above:

- **BRCA1 / BRCA2** — ubiquitously expressed, function in homologous recombination. Inherited
  inactivating mutations predispose largely to breast and ovarian cancer. Two candidate
  explanations: (a) complete BRCA loss of function can only be tolerated in these tissues; (b)
  the cyclical estrogen response in these tissues generates a greater demand for homologous
  recombination.
- **VHL** — broad expression; loss drives renal cancer specifically.
- **APC** — broad expression; loss drives colorectal cancer.
- **KRAS** — broad expression; activating mutations are drivers in cancers of the pancreas,
  colon, and lung, but not across all epithelial cancers despite ubiquitous expression.

### Empirical support for tissue-specificity as the rule

Genetic screens examining cell proliferation across different cell types (Sack et al. 2018, Cell
173:499, ref. 5 in the paper) showed that while core cell-cycle regulators (D-type cyclins, CDK
inhibitors) universally affected proliferation, **80–90% of proliferation-promoting genes
differed between cell types**. Tissue-specific oncogenes and tumor suppressors identified
through cancer genomics appropriately affected proliferation only in their cognate tissue types
in this analysis.

### The unifying hypothesis: the preexisting epigenetic landscape

The authors propose that in many cases tissue-specificity is driven by the preexisting epigenetic
landscape, which has two coupled layers:

- **Chromatin configuration** — determines which genes are expressed and which can be activated
  or repressed in response to stimuli.
- **Epi-proteome / proteomic circuitry** — determines which signals can be sensed and how the
  cell responds.

Both are established by developmental lineage and the microenvironment (paracrine signaling,
cell-cell contact). Because different cells of origin have distinct developmental histories, the
same oncogenic mutation can produce a pro-tumorigenic phenotype, no phenotype, or even a
detrimental phenotype depending on the cell type.

Two examples given for this chromatin-state-dependent output:

- **Glucocorticoid receptor** activation produces a different transcriptional readout in
  different cell types because the accessible chromatin differs (John et al. 2011, Nat. Genet.
  43:264).
- **TGF-β** is oncogenic in some settings and tumor-suppressive in others.

### EZH2 as the paradigm of context-dependent gain-of-function vs. loss-of-function

EZH2 (catalytic component of PRC2, deposits H3K27me3) illustrates how the *same gene* can be
oncogenic in opposite directions depending on lineage:

- **Gain-of-function** EZH2 mutations are oncogenic in **lymphomas and melanomas**; EZH2 is
  also broadly overexpressed in solid tumors.
- **Loss-of-function** defects in EZH2 and other PRC2 components (SUZ12, EED) drive **T-ALL,
  MPNSTs, and myeloproliferative disorders**.

This is offered as direct evidence that each tissue lineage has a distinct preexisting epigenetic
state, and that different tissues are susceptible to different oncogenic and/or epigenetic
insults.

### Therapy response as a readout of tissue-specific permissivity

The same logic extends to therapeutic response, providing clinical evidence for the epigenetic
permissivity model:

- **BRAF V600E + RAF inhibition** — effective in melanoma; minimal single-agent efficacy in
  colorectal cancer expressing the *same* mutant. The mechanism in CRC is EGFR-mediated feedback
  reactivation of the MAPK pathway, which does not occur in melanoma due to absent EGFR
  expression.
- **IDH inhibition** — effective in IDH1/IDH2-mutant AML; not effective in IDH-mutant glioma.
- **EGFR inhibition** — effective in EGFR-mutant NSCLC; not effective in EGFR-mutant glioma.
- **Pan-HER (ERBB2) inhibition** — clinical trials showed strong efficacy in ERBB2-mutant
  breast, biliary tract, and cervical cancers; poorer responses in lung, bladder, and colorectal
  cancer with the same mutation (Hyman et al. 2018, Nature 554:189). The authors flag this as
  evidence that genotype-alone trials must be powered to detect tissue-to-tissue variation.

### Epigenetic plasticity and therapeutic resistance

Epigenetic states are fluid: NSCLC cancers expressing mutant EGFR can become resistant to EGFR
inhibition by transforming into small-cell lung cancer — downregulating EGFR expression and
acquiring RB1 mutations (which are common in neuroendocrine cancers). This is offered as
evidence that epigenetic states define genetic permissivity and that this permissivity can shift
during treatment.

### Prescription for driver discovery

The authors argue that tissue-specificity remains phenomenological and call for mechanistic
investigation by comparing effects of cancer genes in **permissive versus nonpermissive
tissues**. A thorough deconstruction of the transcriptional, epigenetic, proteomic, and
biological responses to different cancer-causing alterations across tissues should reveal both
developmental insights and therapeutic vulnerabilities.

## Relevance

This Perspective is directly relevant to question:q042-driver-normal-expression-tissue-cell-type-
specificity and to the project's cross-study mutation-frequency meta-analysis.

**Route-2 anchor for q042.** The Haigis2019 thesis describes a mechanistically *distinct* route
to tissue-specific driver behavior compared to lineage-addiction oncogenes (paper:Garraway2006).
Garraway2006 explains tissue-specific drivers via tissue-restricted *expression* of the oncogene
in normal tissue (the gene is only expressed — and thus only a dependency — in that lineage).
Haigis2019 explains tissue-specific drivers via **context-dependent functional consequences of
the mutation**: the gene is broadly expressed, but whether the mutation drives cancer depends on
the epigenetic and proteomic wiring of each tissue. This is a clean conceptual separation:

| Route | Mechanism | Canonical examples |
|---|---|---|
| Lineage addiction (Garraway2006) | Gene is tissue-restricted in normal expression → tissue-restricted dependency after amplification/mutation | MITF in melanoma, AR in prostate |
| Context-dependent driver (Haigis2019) | Gene is broadly expressed; driver fitness effect is tissue-specific via epigenetic permissivity | KRAS in pancreas/colon/lung vs. other tissues; BRAF V600E in melanoma vs. CRC |

**For q042 null condition.** Any attempt to predict driver-ness from normal-tissue expression
profiles will capture lineage-addiction oncogenes (Garraway2006 route) but will *miss*
context-dependent drivers (Haigis2019 route), because the latter are broadly expressed. A
vanishing restricted-vs-pan-cancer Tau difference in the pipeline's frequency tables may reflect
route-2 dominance — not artifact — because route-2 drivers would not be picked up by an
expression-based classifier. The project's q042 must either distinguish the two routes or accept
that expression-based signal will only partially explain driver tissue-specificity.

**For cross-study frequency tables.** The pipeline's gene × cancer mutation-frequency matrices
capture the empirical outcome of tissue-specific permissivity without resolving mechanism.
High-frequency hits in a single cancer type could reflect either route. The Haigis2019 framing
motivates using cancer-type-specific frequency thresholds rather than pan-cancer averages when
calling recurrent drivers.

**For Bailey2018 driver overlay.** The Bailey2018 pan-cancer driver list used in
`annotate_drivers.py` partially encodes per-cancer driver designations. Haigis2019 provides the
conceptual justification for why per-cancer driver annotations should be preferred over the
binary pan-cancer flag for most downstream uses.

**For therapy-response interpretation.** The BRAF V600E / EGFR feedback example (melanoma vs.
CRC) directly connects tissue-specific epigenetic state to differential signaling pathway
architecture — relevant if the pipeline is extended to incorporate pathway-level context.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Preexisting epigenetic landscape as permissivity filter | Not currently modeled | Explains why same mutation → different driver outcome; not captured by mutation-frequency tables |
| Context-dependent driver (broadly expressed gene) | Per-cancer driver frequency (gene_cancer_study tables) | Empirically captures outcome; Haigis2019 explains the mechanism |
| Tissue-specific selective pressure via proteomic circuitry | Cancer-type stratification in frequency tables | Motivates per-cancer thresholds over pan-cancer aggregation |
| Route-2 (broadly expressed, tissue-restricted driver effect) | Non-lineage-addiction mechanism in q042 | Distinct from lineage-survival oncogenes (Garraway2006) |
| Pan-cancer driver vs. tissue-specific driver | bailey2018_driver flag vs. per-cancer driver roster | Bailey2018 overlay partially encodes this distinction |
| EZH2 gain-of-function vs. loss-of-function across lineages | Not modeled | Demonstrates same gene can have opposite driver direction by tissue |
| Permissive vs. nonpermissive tissue comparison | Not currently implemented | Authors' prescribed research design for mechanistic driver discovery |

## Limitations

- As a two-page Perspective, the paper provides illustrative examples rather than a systematic
  analysis. The claim that tissue-specificity is "the rule" is supported by the Sack et al. 2018
  screen data (80–90% figure) and selected genomic examples, not a comprehensive statistical
  survey across all known drivers.
- The paper does not provide an operationalizable model for predicting which tissues will be
  permissive for a given gene's driver activity — it is a framing piece, not a predictive tool.
- The distinction between lineage-addiction (Garraway2006) and context-dependent epigenetic
  permissivity (Haigis2019) is not explicitly formalized in the paper; both phenomena are real
  but the clean two-route taxonomy is a synthesis constructed by a reader comparing the two
  papers.
- Mechanistic explanations remain incomplete for several named examples (BRCA1/2, VHL, APC,
  KRAS tissue restriction) — the paper candidly acknowledges this and frames it as motivation
  for future work.
- Epigenetic reprogramming, tumor microenvironment signaling, and clonal selection dynamics are
  acknowledged implicitly but not elaborated as distinct mechanisms.

## Model / Tool Availability

No computational tools, datasets, or models are released. This is a Perspective article.

## Follow-up

- **paper:Garraway2006** — lineage addiction / lineage-survival oncogene framing; the
  complementary route-1 to Haigis2019's route-2, essential for q042.
- **question:q042-driver-normal-expression-tissue-cell-type-specificity** — the project
  question this Perspective directly motivates; the two-mechanism framework should be formalized
  there.
- **Sack et al. 2018** (Cell 173:499, ref. 5) — the genetic screen showing 80–90% of
  proliferation genes differ by cell type; this is the strongest empirical anchor in the paper
  and merits its own summary if the project explores tissue-specific proliferation programs.
- **Hyman et al. 2018** (Nature 554:189, ref. 11) — pan-HER inhibitor clinical trial showing
  tissue-to-tissue variation in response despite shared ERBB2 mutation; direct clinical evidence
  for epigenetic permissivity.
- **Bailey et al. 2018** (Cell, PMID 30096302) — pan-cancer driver census; per-cancer rosters
  are the project annotation anchor.
- **Martincorena et al. 2018** (Science) — quantifies positive selection per gene per cancer
  type; empirical support for tissue-specific selection pressure. Already in project
  (paper:Martincorena2018).
- Project question: Can the pipeline's per-cancer mutation-frequency tables be used to
  empirically score a "tissue-specificity index" for known driver genes, and does that index
  separate lineage-addiction oncogenes from context-dependent (route-2) drivers?
