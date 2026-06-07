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
- **Source:** LLM knowledge (full text inaccessible — Science Perspective, paywalled, no OA copy via Unpaywall or Europe PMC)

## Key Contribution

This short Science Perspective argues that tissue-specificity in cancer driver gene behavior is the *rule*, not the exception: the same somatic mutation in the same gene can be strongly oncogenic in one tissue and neutral or even tumor-suppressive in another. The central thesis is that driver status is a joint property of the mutation *and* the tissue context in which it occurs, not of the gene alone. The authors synthesize evidence across multiple oncogenes and tumor suppressors to show that tissue-specific gene-expression programs, signaling network wiring, and selective pressures all determine whether a given mutation is "actionable" as a driver.

## Methods

This is a Perspective / opinion piece, not an empirical study. The authors [INACCESSIBLE — full text not retrieved] draw on published literature to illustrate context-dependent oncogenesis with named examples, propose mechanistic explanations for tissue-specificity, and argue for a conceptual reframing of how driver genes should be understood. No new experimental data or computational analyses are presented.

## Key Findings

The following summarizes the paper's thesis and illustrative examples based on LLM knowledge of this Perspective; specific page-level citations and any figures should be treated as [INACCESSIBLE].

### Central thesis

Cancer driver genes exhibit remarkable tissue-specificity. The mutation spectrum of individual cancer types is not simply a random draw from all possible driver genes — particular genes dominate in particular tissues in a non-random way that reflects the biology of the normal cell type, not merely which genes are mutated most frequently genome-wide.

### Context-dependent driver behavior: the same gene, different tissues

- **KRAS** is the paradigm case [UNVERIFIED detail beyond abstract-level claim]: activating KRAS mutations (especially G12D/G12V) are among the most frequent drivers in pancreatic ductal adenocarcinoma, colorectal cancer, and lung adenocarcinoma, yet rare in many other tumor types despite KRAS being broadly expressed. This tissue-restricted driver frequency cannot be explained by tissue-specific expression of KRAS itself (it is ubiquitous), implying the *functional consequence* of the mutation is tissue-dependent.
- **BRAF V600E** drives melanoma and papillary thyroid carcinoma but is rare in many carcinomas where RAS is the dominant driver. In some contexts (e.g. normal melanocytes) BRAF V600E induces senescence rather than proliferation, demonstrating that the same allele can be growth-suppressive in one cell state and oncogenic in another. [UNVERIFIED specific cell-state details]
- **NF1** (neurofibromin) loss is a dominant driver in nerve-sheath tumors (neurofibromas, MPNSTs) and glioma, but NF1 mutations are underrepresented as drivers in many epithelial cancers despite NF1 being broadly expressed — consistent with tissue-specific selective pressure on RAS pathway activation.
- **PIK3CA** and **PTEN** mutations occur frequently in endometrial, breast, and prostate cancers, but the same PI3K pathway genes are only infrequently the primary driver in, e.g., pancreatic cancer, where KRAS dominates the same downstream effectors. [UNVERIFIED cross-tissue frequency comparison]

### Proposed explanations for tissue-specificity

The authors propose two non-mutually-exclusive classes of mechanism [INACCESSIBLE — precise framing from full text not available; reconstruction from LLM knowledge]:

1. **Tissue-specific regulatory/expression context.** Even broadly-expressed genes operate within tissue-specific transcriptional programs and chromatin states. The downstream targets available for a given oncogenic signal, the availability of co-activators or co-repressors, and which growth checkpoints are active all depend on the differentiation state of the cell of origin. A mutation that hyperactivates a pathway may produce a growth advantage only if the relevant effectors are expressed and the relevant checkpoints are absent.

2. **Tissue-specific selective pressures.** Different tissues impose different evolutionary constraints on emerging cancer clones. In one tissue, a given mutation may confer a strong growth advantage; in another, it may be growth-neutral, require additional cooperating mutations to be selected, or actually reduce fitness (e.g., by triggering differentiation or senescence). Oncogene-induced senescence responses and the presence or absence of specific tumor-suppressor axes (e.g., p16/RB, ARF/p53) interact with the mutated gene in a tissue-dependent way. [UNVERIFIED specific pathway details]

3. **Cell-of-origin lineage programs (lineage addiction).** Some oncogenes are "lineage survival factors" — they are required for the survival or identity of the normal cell type from which the tumor arises, making them preferentially selected in that lineage. This is conceptually related to but distinct from the above: here, the gene itself has a tissue-restricted *normal* function, making it a tissue-specific dependency even without a mutation. [SPECULATION — this synthesis of lineage addiction into Haigis2019's framing extends beyond what the Perspective explicitly argues; see paper:Garraway2006 for the original lineage-addiction framing]

### Implications for driver discovery

By framing tissue-specificity as the norm, the Perspective argues that pan-cancer driver analysis should not be the primary mode of discovery — instead, tissue-stratified analyses are essential. Methods that aggregate mutation frequencies across all tumor types will undercount context-dependent drivers and overcount genes that happen to be broadly mutated due to high background rates. [INACCESSIBLE — whether the authors make this specific methodological prescription is not confirmed from full text]

## Relevance

This Perspective is directly relevant to the project's cross-study mutation-frequency meta-analysis and to question:q042-driver-normal-expression-tissue-cell-type-specificity.

**Mechanism 2 in the two-mechanism framework.** The Haigis2019 thesis describes a *distinct* route to tissue-specific driver behavior compared to lineage-addiction oncogenes (paper:Garraway2006). Garraway2006 explains tissue-specific drivers via tissue-restricted *expression* of the oncogene in normal tissue (the gene is only expressed — and thus only a dependency — in that lineage). Haigis2019 explains tissue-specific drivers via context-dependent *functional consequences*: the gene is broadly expressed, but whether the mutation drives cancer depends on the regulatory wiring, available effectors, and selective pressures of each tissue. This is a clean conceptual separation:

| Route | Mechanism | Example |
|---|---|---|
| Lineage addiction (Garraway2006) | Gene is tissue-restricted in normal expression → tissue-restricted dependency after amplification/mutation | MITF in melanoma, AR in prostate |
| Context-dependent driver (Haigis2019) | Gene is broadly expressed, but driver fitness effect is tissue-specific | KRAS in pancreas vs. other tissues |

**For q042:** Any attempt to predict driver-ness from normal-tissue expression profiles will successfully capture lineage-addiction oncogenes (Garraway2006 route) but will *miss* context-dependent drivers (Haigis2019 route), because the latter are broadly expressed. The project's q042 must decide which route it is asking about, or build separate classifiers for each.

**For cross-study frequency tables:** The pipeline's gene × cancer mutation-frequency matrices implicitly capture the empirical outcome of tissue-specificity without resolving its mechanism. High-frequency hits in a single cancer type could reflect either route. The Haigis2019 framing motivates using cancer-type-specific frequency thresholds rather than pan-cancer averages when calling recurrent drivers.

**For Bailey2018 driver overlay:** The Bailey2018 pan-cancer driver list used in the pipeline's `annotate_drivers.py` was derived in part from pan-cancer and per-cancer analyses; it already partly encodes tissue-specific driver designations. Haigis2019 provides the conceptual justification for why per-cancer driver annotations should be preferred over the pan-cancer binary flag for most downstream uses.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Context-dependent driver | Per-cancer driver frequency (gene_cancer_study tables) | Empirically captures outcome; Haigis2019 explains the mechanism |
| Tissue-specific selective pressure | Cancer-type stratification in frequency tables | Motivates per-cancer thresholds over pan-cancer aggregation |
| Tissue-restricted driver via broadly-expressed gene | Non-lineage-addiction mechanism in q042 | Distinct from lineage-survival oncogenes (Garraway2006) |
| Pan-cancer driver vs. tissue-specific driver | bailey2018_driver flag vs. per-cancer driver roster | Bailey2018 overlay partially encodes this distinction |
| Oncogene-induced senescence as tissue checkpoint | Not currently modeled | Relevant to interpreting low-frequency mutations in some cancer types |

## Limitations

- As a short Perspective (2 pages), the paper provides illustrative examples rather than a systematic analysis; the claim that tissue-specificity is "the rule" is argued from selected cases rather than a comprehensive statistical survey. [INACCESSIBLE — the full evidentiary structure of the argument is not accessible]
- The paper does not provide a mechanistic model that could be operationalized to *predict* which tissues will show driver behavior for a given gene — it is a framing paper, not a predictive tool.
- The distinction between the two routes to tissue-specific driver behavior (Garraway2006's lineage addiction vs. Haigis2019's context-dependent fitness) is not explicitly formalized; a reader synthesizing both papers must construct this distinction.
- The Perspective does not address the role of clonal selection dynamics, tumor microenvironment, or epigenetic reprogramming in modulating driver fitness — all of which are tissue-specific but not discussed.
- Citation count is ~176 (Crossref, 2026-06-07), below the 500-citation threshold typically associated with landmark status; this is a targeted conceptual piece rather than a high-citation review.

## Model / Tool Availability

No computational tools, datasets, or models are released. This is a Perspective article.

## Follow-up

- **paper:Garraway2006** (Garraway & Sellers 2006, Nature Reviews Cancer) — the original lineage-addiction / lineage-survival oncogene framing; complements Haigis2019's distinct mechanism and is essential for q042.
- **question:q042-driver-normal-expression-tissue-cell-type-specificity** — the project question this Perspective directly motivates; the two-mechanism framework (lineage addiction vs. context-dependent driver) should be formalized there.
- **Bailey et al. 2018** (Cell, PMID 30096302) — pan-cancer driver census; Haigis2019's framing provides conceptual justification for why per-cancer driver rosters matter more than the binary pan-cancer flag.
- Systematic follow-up: Martincorena et al. 2018 (Science) — quantifies positive selection per gene per cancer type; provides empirical support for the tissue-specific selection-pressure mechanism proposed by Haigis2019. Already in project (paper:Martincorena2018).
- **Sanchez-Vega et al. 2018** (Cell) — TCGA PanCanAtlas oncogenic signaling pathway analysis; empirically shows that pathway activation varies by cancer type even when the same pathway member is mutated, supporting Haigis2019's context-dependent fitness claim. [UNVERIFIED whether this citation appears in Haigis2019]
- Project question: Can the pipeline's per-cancer mutation-frequency tables be used to empirically score "tissue-specificity index" for known driver genes, and does that index separate lineage-addiction oncogenes from context-dependent drivers?
