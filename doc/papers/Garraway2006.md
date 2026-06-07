---
id: "paper:Garraway2006"
type: "paper"
title: "Lineage dependency and lineage-survival oncogenes in human cancer"
status: "active"
ontology_terms:
  - lineage addiction
  - lineage-survival oncogene
  - cancer driver
  - tissue-specific transcription factor
  - cell-of-origin
  - melanoma
  - MITF
  - androgen receptor
  - NKX2-1
  - ESR1
  - oncogene amplification
  - cancer type specificity
datasets: []
source_refs:
  - "cite:Garraway2006"
related:
  - topic:lineage-addiction-and-cell-of-origin-driver-specificity
  - question:q042-driver-normal-expression-tissue-cell-type-specificity
  - discussion:2026-06-07-tissue-cell-type-specificity-of-cancer-drivers
  - hypothesis:h12-neural-gene-enrichment-length-histology-artifact
  - topic:oncofetal-developmental-reprogramming
created: "2026-06-07"
updated: "2026-06-07"
---

# Lineage dependency and lineage-survival oncogenes in human cancer

- **Authors:** Levi A. Garraway, William R. Sellers
- **Year:** 2006
- **Journal:** Nature Reviews Cancer, 6(8):593-602
- **DOI/URL:** https://doi.org/10.1038/nrc1947
- **PMID:** 16862190
- **BibTeX key:** Garraway2006
- **Source:** LLM knowledge (paywalled; Crossref 313 citations, Europe PMC 271-273; classic-exception applied: foundational 2006 NRC review, conceptual synthesis, comprehensively covered in LLM training)

## Key Contribution

This review introduces and formalizes two related concepts: **lineage dependency** (the general observation that cancers often remain dependent on the master transcriptional regulators of their cell of origin) and the narrower **lineage-survival oncogene** (a gene that is both a master regulator of normal lineage identity and is recurrently amplified or activated in the cancer derived from that lineage, providing a direct survival advantage) [UNVERIFIED: exact definitions may differ at margins from paper]. The authors synthesize evidence from melanoma, prostate, lung, and breast cancer to argue that this class of oncogenes occupies a distinctive mechanistic niche: they are neither classic "gatekeeper" or "caretaker" tumor suppressors nor broadly expressed proliferation drivers, but rather genes whose oncogenic role is inseparable from the tissue or cell type in which the cancer arises. The review constitutes the founding conceptual framework for what has since been called "lineage addiction" in the cancer biology literature.

## Methods

This is a review / perspective article; it presents no original experimental data. The argument is constructed by [UNVERIFIED]:

- Surveying published gene amplification and mutation studies across major cancer types.
- Drawing on functional RNAi and overexpression experiments from multiple laboratories.
- Synthesizing patterns across canonical examples (MITF/melanoma, AR/prostate, NKX2-1/lung, ESR1/breast) to derive the unifying framework.
- Contrasting lineage-survival oncogenes with oncogenes that have broad expression profiles (e.g., KRAS, MYC) to define the conceptual boundary of the category.

## Key Findings

### Definitions introduced [UNVERIFIED: paraphrased from LLM knowledge]

**Lineage dependency:** Cancers frequently retain dependence on transcription factors and signaling programs that govern the differentiation state of the normal cell from which the cancer arose. This dependence persists even as the cancer acquires many additional genetic alterations — the lineage program is not discarded but is co-opted.

**Lineage-survival oncogene:** A specialized subset of oncogenes defined by three converging properties:
1. The gene encodes a master regulator of normal cell-type identity (a lineage-specifying transcription factor or closely associated effector).
2. The gene is recurrently amplified, mutated, or otherwise activated in the cancer derived from that same lineage.
3. Knockdown or inhibition of the gene selectively impairs survival of the cancer cells, not (or much less so) cells from other lineages.

### Canonical examples [UNVERIFIED: details from LLM knowledge]

| Gene | Cancer type | Normal lineage role | Oncogenic event |
|------|-------------|---------------------|-----------------|
| MITF | Melanoma | Master regulator of melanocyte identity and differentiation | Amplification at 3p14; activating mutation in MITF itself; also activated downstream of BRAF→MAPK |
| AR (androgen receptor) | Prostate adenocarcinoma | Core regulator of prostatic epithelial identity | Amplification; ligand-binding domain mutations; transcriptional co-activator amplification |
| NKX2-1 (TTF-1) | Lung adenocarcinoma | Specifies lung alveolar epithelial identity; regulates surfactant gene expression | Amplification at 14q13.3 |
| ESR1 (ERα) | Luminal breast carcinoma | Specifies luminal mammary epithelial fate | Amplification; activating mutations (mostly acquired/treatment-selected) |

The review argues that in each case the oncogenic activity of the lineage-survival oncogene is directly continuous with its normal developmental function — it does not acquire a wholly new biochemical activity but instead drives an existing transcriptional program constitutively and at elevated levels.

### Mechanistic framework [UNVERIFIED]

The authors propose that lineage-survival oncogenes occupy a specific position in the cancer genome: they are typically found at the apex (or near-apex) of the transcriptional hierarchy governing the cell of origin. Their amplification/activation has two separable effects:

1. **Survival:** Direct transcriptional activation of anti-apoptotic programs and repression of pro-apoptotic or differentiation programs. Because these survival circuits were already wired into the lineage during normal development, cancer cells inherit the wiring and amplify it.
2. **Identity maintenance / differentiation block:** Sustained activity of the lineage factor prevents terminal differentiation or alternative-fate acquisition, keeping the cell in a proliferation-permissive state.

### Distinction from broadly expressed drivers [UNVERIFIED]

The paper explicitly distinguishes lineage-survival oncogenes from oncogenes like RAS, MYC, or PI3K-pathway components that: (a) are expressed across many cell types, (b) drive proliferation/survival through generic downstream effectors, and (c) whose cancer-type specificity (when present) arises from contextual pathway wiring rather than from the gene's own restricted expression. A broadly expressed oncogene can be cancer-type-enriched because cooperating mutations, chromatin context, or selective pressure differ between tissues — but that is distinct from a gene that is intrinsically tissue-restricted at the expression level.

### Implications for therapeutic targeting [UNVERIFIED]

Because lineage-survival oncogenes are required for survival of the cancer but not of most normal adult tissues (whose lineage programs are no longer driven by high-level expression of the same factor), they represent potentially selective therapeutic targets. The paper frames this as one rationale for prioritizing lineage-survival oncogenes as drug targets — a line of reasoning that subsequently motivated direct targeting efforts for MITF, AR, and NKX2-1.

## Relevance

This paper is the primary reference for the "lineage-survival oncogene" concept, which is directly relevant to this project's investigation of whether cancer-type-specific drivers are systematically genes with strong tissue/cell-type-restricted normal expression.

**Connection to the driver specificity thread (question:q042, discussion:2026-06-07):**

The Garraway & Sellers framework provides the clearest mechanistic case for the hypothesis that cancer-type-specific drivers are not a structurally heterogeneous collection, but have a definable subset — lineage-survival oncogenes — where the tissue specificity is *causal* rather than coincidental. In our pipeline's language:

- A gene like MITF appearing as a melanoma-enriched driver in the cross-study gene × cancer frequency table is not surprising given its restricted expression — the cancer carries the dependency because the normal melanocyte carried the dependency.
- Conversely, a broadly expressed driver (e.g., TP53, KRAS) appearing enriched in a particular cancer type is a different kind of finding: it reflects selective pressure or cooperative context, not expression restriction.

This distinction is load-bearing for hypothesis h12 (neural gene enrichment / length-histology artifact): if some of the apparent neural-gene enrichment in nervous system tumors reflects genuine lineage-survival oncogenes (master regulators of neural identity: SOX2, OLIG2, and related TFs), then the signal is biologically real and distinct from a length/expression artifact. The two explanations — artifact vs. lineage survival — generate different predictions about which specific genes drive the enrichment.

**Driver vs. oncogene/TSG framing:**

The review's conceptual framing maps onto our project's distinction between:
- **Driver (cancer-type-specific):** a gene whose recurrent mutation defines a cancer subtype — could be a lineage-survival oncogene *or* a broadly expressed driver acting in a specific context.
- **Lineage-survival oncogene (subset of drivers):** a driver whose cancer-type specificity is explained primarily by restricted normal expression, which creates the dependency that the cancer then co-opts.

This is the clearest known class of "driver whose specificity is explained by normal tissue/cell-type expression," making it the natural anchor for the broader project thread on lineage-restricted drivers.

**Connection to topic:oncofetal-developmental-reprogramming:**

Lineage-survival oncogenes as defined here operate through retained normal lineage circuitry (not reprogram to a different state). This is mechanistically complementary to oncofetal reprogramming, where the cancer reactivates a fetal/embryonic program. The two mechanisms are not mutually exclusive — some cancers may both retain adult lineage dependency and activate fetal programs — but distinguishing them empirically requires knowing which transcription factors are activated in the cancer vs. which are retained from normal adult identity.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Lineage-survival oncogene | Cancer-type-specific driver gene (subset) | The paper's category is more specific: requires restricted normal expression AND recurrent amplification/activation in the derived cancer |
| Lineage dependency | Cell-of-origin driver specificity | Broader term: any retention of normal lineage program as a cancer vulnerability |
| Master lineage transcription factor | Tissue-restricted normal expressed gene | In our pipeline: genes with high tissue-specificity scores (GTEx τ or similar) that also appear as cancer-type-enriched drivers |
| Amplification as oncogenic mechanism | Copy-number alteration (out of scope for current pipeline) | Current pipeline focuses on somatic point mutations; amplification data from cBioPortal would require separate module |
| Lineage-specific survival dependency | Gene × cancer enrichment (high mutation ratio in one cancer type) | The pipeline's gene × cancer frequency matrix captures the recurrence signal, though not the functional dependency directly |
| "Context-dependent" broadly expressed driver | Context-specific driver (e.g., KRAS in pancreatic) | The paper's mechanism (contextual wiring) is distinct from expression restriction — a nuance the frequency table alone cannot resolve |

## Limitations

- **2006 snapshot:** The paper was written before the systematic pan-cancer sequencing era (TCGA, ICGC, PCAWG). The canonical examples it discusses were well-established by 2006, but the subsequent decade of comprehensive genomic data has revealed many additional lineage-related drivers and some cases that complicate the clean framework [UNVERIFIED: specific complications not enumerated].
- **Amplification focus:** The original framework emphasizes gene amplification as the primary oncogenic mechanism for lineage-survival oncogenes. Subsequent work has shown that activating point mutations, epigenetic de-repression, and translocation can serve the same role — the paper may underweight these mechanisms.
- **Transcription-factor centric:** The review focuses on transcription factors as the canonical lineage-survival oncogenes. Lineage-restricted cell-surface receptors, signaling kinases, and metabolic enzymes can also satisfy analogous logic but are less prominent in this framework.
- **No quantitative definition:** The concepts are defined qualitatively. There is no threshold for "how restricted" normal expression must be, or how specifically the cancer must arise from the expressing lineage. This makes the framework hard to operationalize systematically across a large gene × cancer matrix [UNVERIFIED: later literature has partially addressed this operationally].
- **Full text inaccessible:** Specific section-level claims, exact examples cited per section, quantitative claims about expression thresholds or amplification frequencies, and the precise language of definitions are `[INACCESSIBLE]` — this summary is based on LLM knowledge of the paper's conceptual content and must be verified against the PDF before any claims are treated as direct quotations.

## Model / Tool Availability

Review article — no software, dataset, or model released. The conceptual framework is the primary output.

## Follow-up

- **Garraway et al. 2005 (Nature)** — the companion empirical paper identifying MITF amplification and demonstrating the melanocyte lineage-survival mechanism directly, which this review builds on. Read to get the original experimental evidence for the flagship example [UNVERIFIED: check DOI].
- **Chiang & Bhatt et al. (lineage oncogene operationalization)** — subsequent papers that attempt to score genes genome-wide for lineage-survival properties using expression specificity + cancer amplification concordance. Would provide the quantitative bridge from this review's qualitative framework to systematic analysis in our pipeline.
- **GTEx / FANTOM5 tissue specificity** — to operationalize "lineage-restricted normal expression" in the pipeline, we need a tissue-specificity score (e.g., τ from GTEx) for each gene. Pairing this with our gene × cancer frequency enrichment scores would identify which enriched drivers are candidates for the lineage-survival mechanism.
- **SOX2, OLIG2, and neural lineage-survival oncogenes in glioma/neuroblastoma** — directly relevant to h12. These TFs are both neural lineage specifiers and recurrently amplified/overexpressed in neural tumors; examining their position in our gene × cancer frequency matrix would test whether h12's neural enrichment signal is partly lineage-survival biology.
- **Bailey et al. 2018 Table S1** — the PanCanAtlas driver list already in this pipeline's annotation layer. Cross-referencing Bailey drivers against tissue-specificity scores would partition them into lineage-survival vs. broadly-expressed driver categories — a concrete analysis enabled by existing pipeline outputs.
