---
type: paper
title: Lineage dependency and lineage-survival oncogenes in human cancer
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: paper:Garraway2006
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
- cite:Garraway2006
related:
- topic:lineage-addiction-and-cell-of-origin-driver-specificity
- question:0042-driver-normal-expression-tissue-cell-type-specificity
- discussion:0008-tissue-cell-type-specificity-of-cancer-drivers
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- topic:oncofetal-developmental-reprogramming
---

# Lineage dependency and lineage-survival oncogenes in human cancer

- **Authors:** Levi A. Garraway, William R. Sellers
- **Year:** 2006
- **Journal:** Nature Reviews Cancer, 6(8):593-602
- **DOI/URL:** https://doi.org/10.1038/nrc1947
- **PMID:** 16862190
- **BibTeX key:** Garraway2006
- **Source:** PDF (papers/pdfs/2006_Garraway_Lineage-dependency-and-lineage-survival-oncogenes-in-human-cancer.pdf)

## Key Contribution

This review introduces and formalizes two related concepts: **lineage dependency** (equivalently, **lineage addiction**) and the narrower **lineage-survival oncogene**. The paper synthesizes evidence from melanoma, prostate, lung, and breast cancer to argue that this class of oncogenes occupies a distinctive mechanistic niche: they are neither classic "gatekeeper" or "caretaker" tumor suppressors nor broadly expressed proliferation drivers, but rather genes whose oncogenic role is inseparable from the tissue or cell type in which the cancer arises.

The review constitutes the founding conceptual framework for what is now called "lineage addiction" in the cancer biology literature, and it explicitly distinguishes this mechanism from classical oncogene addiction (gain of a new tumour-specific function) by invoking instead the *persistence and deregulation* of survival mechanisms that were already operating in the normal lineage precursor.

## Methods

This is a review / perspective article; it presents no original experimental data. The argument is constructed by:

- Surveying published gene amplification and mutation studies across major cancer types (data drawn from the literature and the COSMIC database, as stated in the paper's Figure 2 legend).
- Drawing on functional RNAi and overexpression experiments from multiple laboratories.
- Synthesizing patterns across canonical examples (MITF/melanoma, AR/prostate, TITF1/lung, ESR1/breast, CCND1/mammary, FLT3/myeloid) to derive the unifying framework.
- Contrasting lineage-survival oncogenes with broadly expressed oncogenes (KRAS, EGFR, PIK3CA, BRAF, TP53, CDKN2A) to define the conceptual boundary of the category (Figure 2 in the paper).

## Key Findings

### Exact definitions (from the paper's "At a glance" and body text)

**Lineage dependency (= lineage addiction):** A model in which tumour cells depend crucially on survival mechanisms that are programmed into lineage precursor cells during development. These mechanisms may be affected by acquired genetic alterations. Unlike oncogene addiction — which invokes a dependency on a tumour-specific gain-of-function event — *lineage addiction involves the persistence and/or deregulation of crucial lineage-survival mechanisms during carcinogenesis or tumour progression.*

**Lineage-survival oncogene:** A gene whose lineage-dependency mechanisms promote tumour progression. These are *master regulatory genes that also exert key developmental survival roles.* The paper (Box 3) lists five predicted properties:

1. Crucial role(s) in normal lineage proliferation and/or survival during development.
2. Persistent or deregulated expression in cancers of the associated lineage.
3. Affected by somatic genetic alterations in tumour subsets.
4. Required for tumour survival and/or progression.
5. More likely to be lineage-associated transcription factors than signalling proteins.

**Key contrast with oncogene addiction:** Classical oncogene addiction uses growth-promoting genes (often tyrosine kinases) that have undergone activating somatic mutations conferring a transformed phenotype in standard assays. Lineage addiction instead involves deregulated expression of *master genes that mediate normal developmental lineage functions* — a distinct class of cancer genes.

### Canonical examples (Table 2 in the paper — verified from PDF)

| Gene | Lineage | Function | Genetic alterations confirmed? | Noted therapeutics |
|------|---------|----------|-------------------------------|-------------------|
| MITF | Melanocytic | Transcription factor | Yes | Antisense BCL2 |
| AR | Prostate | Transcription factor | Yes | Hormone therapy |
| CCND1 | Mammary | Cell-cycle regulator / transcription factor | Yes | CDK inhibitors |
| FLT3 | Myeloid | Receptor tyrosine kinase | Yes | FLT3 inhibitors |
| ESR1 | Mammary | Transcription factor | Yes, in co-activators | Hormone therapy |
| TITF1 (NKX2-1) | Lung | Transcription factor | No (as of 2006) | ? |
| CDX1 | Intestine | Transcription factor | No (as of 2006) | ? |
| Ets oncogenes | Prostate, mammary, other | Transcription factors | Yes (prostate) | ? |

Note: The paper uses the name **TITF1** (thyroid transcription factor 1 homeodomain protein), not NKX2-1, throughout. It notes TITF1 is highly expressed in small-cell lung cancers and lung adenocarcinomas and is a useful histological marker for primary pulmonary neoplasms, but states explicitly that no genetic alterations had been confirmed at time of writing.

### MITF as the prototype lineage-survival oncogene (detailed mechanism from the paper)

MITF is a master transcriptional regulator required for both differentiation and survival of the melanocyte lineage; the success of the melanocyte lineage depends crucially on proliferative and survival signals converging on MITF. The paper's evidence (citing Garraway et al. 2005, Nature):

- MITF undergoes amplification in **15–20% of metastatic melanomas**.
- MITF cooperates with activated BRAF^V600E to transform immortalized human melanocytes.
- This transforming capacity is only manifest in the context of aberrant MAPK pathway activation (BRAF^V600E co-expression) AND cell-cycle deregulation via the **p16–CDK4–RB pathway**.

MITF has two separable functions in melanocyte development: (1) regulation of the differentiation programme (associated with growth arrest via p16/RB); and (2) melanocyte lineage survival (proliferative via CDK2; anti-apoptotic via BCL2). In MITF-dependent melanomas, the differentiation/growth-arrest function is dispensable — indeed detrimental — so these tumours require co-occurring CDKN2A deletion and constitutive MAPK activation (via NRAS or BRAF mutations) to allow oncogenic MITF function to emerge. This explains why these specific genetic alterations are so much more frequent in melanoma than in other tumour types: the lineage dependency *conditions* the genetic landscape.

### AR as the prototype in prostate cancer

Like MITF, AR is required for development and survival of the prostate epithelial lineage. Prostate luminal differentiation requires AR and leads to growth arrest after a defined period of epithelial proliferation. Ectopic AR expression in prostate epithelial cells with inactivated RB and p53 checkpoints makes those cells able to form tumours after orthotopic injection and androgen stimulation. Thus both MITF and AR are master transcriptional regulators of their respective lineages that can acquire oncogenic roles in specific genetic contexts.

### ESR1 nuance

The paper treats ESR1 differently from AR: ESR1 has not been shown convincingly to undergo somatic genetic alterations in breast cancer. Instead, gene amplification of ER transcriptional co-factors has been observed in breast and ovarian cancer, suggesting that other cellular means suffice to deregulate ER in oestrogen-sensitive tumours. This gender discrepancy (AR mutated/amplified in prostate vs. ESR1 not mutated in breast) is explicitly noted in the paper.

### Lineage conditioning of somatic genetics

The paper argues that lineage exerts a substantial effect on the distribution of genetic alterations across tumours (Figure 2). Even activating mutations within a gene can vary markedly by lineage (e.g., Ras family mutations). Clustering of SNP array copy-number data from cancer cell lines and tumour samples by tissue of origin (cited from Garraway et al., own group's work) is consistent with lineage-driven genetic perturbations. Conversely, gatekeeper tumour suppressors such as TP53 and CDKN2A tend to show lineage-independent inactivation patterns, though the *mechanism* of inactivation varies (e.g., TP53 point mutations rare in melanoma; INK4a/ARF deletion serves the same purpose there).

### Lineage-independent paths and scope limits

The paper explicitly acknowledges that lineage addiction is not universal:
- Some melanomas show MITF downregulation in advanced disease — MITF is dispensable in these tumours.
- ~1% of prostate cancers are PSA-negative, suggesting AR-independent biology.
- Poorly differentiated cancers might largely lack the lineage programming characteristic of their lineage, though lineage "memory" might persist in microRNA expression profiles even when invisible in mRNA profiles.

### Typology / classification used in the paper

Rather than a formal multi-type taxonomy, the paper frames a dichotomy:

1. **Oncogene addiction** — dependency on a tumour-specific gain-of-function event; the factor is absent in normal tissue, present in tumour; therapeutically addressed by direct inhibition of the mutated oncoprotein (Figure 4a).
2. **Lineage addiction** — dependency on persistence/deregulation of a normal developmental survival mechanism; the factor is *present in normal cells and deregulated in tumour cells*; lineage conditions which genetic alterations arise (Figure 4b).

The paper also distinguishes lineage-survival oncogenes from classical oncogenes by their likely identity as transcription factors / master developmental regulators rather than tyrosine kinases.

### Therapeutic implications

Because lineage-survival oncogenes are present in both normal lineage cells and tumour cells, direct targeting can have increased toxic side effects. The paper proposes that the optimal tumour-specific targets may therefore lie *outside* the lineage-survival pathway itself — relying on **synthetic dosage lethality**: identifying a distinct buffering factor B that becomes essential when both the deregulated lineage-survival gene and its enabling genetic alterations are simultaneously present. Examples cited: BCL2 antisense in MITF-dependent melanoma (combined with MAPK and CDK inhibitors); FLT3 inhibitors; AR/ER hormone therapy.

## Relevance

This paper is the primary reference for the "lineage-survival oncogene" concept, which is directly relevant to this project's investigation of whether cancer-type-specific drivers are systematically genes with strong tissue/cell-type-restricted normal expression.

**Connection to the driver specificity thread (question:0042, discussion:2026-06-07):**

The Garraway & Sellers framework provides the clearest mechanistic case for the hypothesis that cancer-type-specific drivers are not a structurally heterogeneous collection, but have a definable subset — lineage-survival oncogenes — where the tissue specificity is *causal* rather than coincidental. In our pipeline's language:

- A gene like MITF appearing as a melanoma-enriched driver in the cross-study gene × cancer frequency table is not surprising given its restricted expression — the cancer carries the dependency because the normal melanocyte carried the dependency.
- Conversely, a broadly expressed driver (e.g., TP53, KRAS) appearing enriched in a particular cancer type is a different kind of finding: it reflects selective pressure or cooperative context, not expression restriction.

The paper's own Figure 2 makes this contrast explicit: BRAF, KRAS, PIK3CA, EGFR mutations are lineage-restricted in distribution (high in a few types), while TP53 and CDKN2A inactivations are broadly distributed — but the reason for each class differs.

**Distinction from context-dependent drivers (paper:Haigis2019):**

The Garraway & Sellers mechanism (normal lineage program retained and deregulated) is distinct from the context-dependent driver mechanism in Haigis et al. 2019, where a broadly expressed oncogene (e.g., oncogenic RAS) has different output depending on the tissue chromatin landscape. In the Garraway model, the tissue specificity is *intrinsic* to the gene's restricted normal expression and its developmental survival function. In the Haigis model, the gene is not tissue-restricted by expression but its downstream consequences are filtered differently in each tissue context. The two mechanisms can coexist in different driver genes but should not be conflated.

**Connection to hypothesis:0012-neural-gene-enrichment-length-histology-artifact (neural gene enrichment / length-histology artifact):**

If some of the apparent neural-gene enrichment in nervous system tumors reflects genuine lineage-survival oncogenes (master regulators of neural identity: SOX2, OLIG2, and related TFs), then the signal is biologically real and distinct from a length/expression artifact. The two explanations — artifact vs. lineage survival — generate different predictions about which specific genes drive the enrichment.

**Driver vs. oncogene/TSG framing:**

The review's conceptual framing maps onto our project's distinction between:
- **Driver (cancer-type-specific):** a gene whose recurrent mutation defines a cancer subtype — could be a lineage-survival oncogene *or* a broadly expressed driver acting in a specific context.
- **Lineage-survival oncogene (subset of drivers):** a driver whose cancer-type specificity is explained primarily by restricted normal expression, which creates the dependency that the cancer then co-opts.

This is the clearest known class of "driver whose specificity is explained by normal tissue/cell-type expression," making it the natural anchor for the broader project thread on lineage-restricted drivers.

**Connection to topic:oncofetal-developmental-reprogramming:**

Lineage-survival oncogenes as defined here operate through retained normal lineage circuitry (not reprogramming to a different state). This is mechanistically complementary to oncofetal reprogramming, where the cancer reactivates a fetal/embryonic program. The two mechanisms are not mutually exclusive — some cancers may both retain adult lineage dependency and activate fetal programs — but distinguishing them empirically requires knowing which transcription factors are activated in the cancer vs. which are retained from normal adult identity.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Lineage-survival oncogene | Cancer-type-specific driver gene (subset) | The paper's category is more specific: requires restricted normal expression AND recurrent amplification/activation in the derived cancer |
| Lineage dependency / lineage addiction | Cell-of-origin driver specificity | Broader term: any retention of normal lineage program as a cancer vulnerability |
| Master lineage transcription factor | Tissue-restricted normal expressed gene | In our pipeline: genes with high tissue-specificity scores (GTEx τ or similar) that also appear as cancer-type-enriched drivers |
| MITF amplification (15–20% metastatic melanoma) | Copy-number alteration (out of scope for current pipeline) | Current pipeline focuses on somatic point mutations; amplification data from cBioPortal would require separate module |
| Lineage-specific survival dependency | Gene × cancer enrichment (high mutation ratio in one cancer type) | The pipeline's gene × cancer frequency matrix captures recurrence signal, though not functional dependency directly |
| "Conditioning" of genetic alterations by lineage | Enrichment patterns in gene × cancer frequency table | The paper predicts that lineage-conditioned genes should show concentrated hits in few cancer types (vs. uniformly distributed gatekeeper TSGs) |
| Oncogene addiction (contrast) | Context-dependent driver (paper:Haigis2019) | Broadly expressed oncogene acting differently by tissue context — mechanistically distinct from lineage-survival |

## Limitations

- **2006 snapshot:** Written before systematic pan-cancer sequencing (TCGA, ICGC, PCAWG). The paper explicitly notes that several candidate lineage-survival oncogenes (TITF1, CDX1) lacked confirmed genetic alterations at time of writing; subsequent sequencing confirmed TITF1/NKX2-1 amplification at 14q13.3 in lung adenocarcinoma.
- **Amplification focus:** The framework emphasizes gene amplification as the primary oncogenic mechanism. Subsequent work has shown that activating point mutations, epigenetic de-repression, and translocation can serve the same role.
- **Transcription-factor centric:** The review focuses on transcription factors as the canonical lineage-survival oncogenes (Box 3 explicitly states these genes are "more likely to be lineage-associated transcription factors than signalling proteins"). Lineage-restricted cell-surface receptors, signaling kinases, and metabolic enzymes satisfying analogous logic receive less emphasis.
- **No quantitative definition:** The concepts are defined qualitatively. There is no threshold for "how restricted" normal expression must be, or how specifically the cancer must arise from the expressing lineage. This makes the framework hard to operationalize systematically across a large gene × cancer matrix.
- **Lineage addiction not universal:** The paper itself acknowledges it applies only to a subset of tumours from each lineage (advanced/poorly differentiated tumours may escape lineage dependency).

## Model / Tool Availability

Review article — no software, dataset, or model released. The conceptual framework is the primary output.

## Follow-up

- **Garraway et al. 2005 (Nature)** — the companion empirical paper identifying MITF amplification in 15–20% of metastatic melanomas and demonstrating the melanocyte lineage-survival mechanism directly; this review is in large part a synthesis built on that prior work.
- **TITF1/NKX2-1 amplification confirmation** — the paper explicitly predicted this; subsequent sequencing studies confirmed 14q13.3 amplification in lung adenocarcinoma.
- **GTEx / FANTOM5 tissue specificity** — to operationalize "lineage-restricted normal expression" in the pipeline, a tissue-specificity score (e.g., τ from GTEx) for each gene, paired with our gene × cancer frequency enrichment scores, would identify which enriched drivers are candidates for the lineage-survival mechanism.
- **SOX2, OLIG2, and neural lineage-survival oncogenes in glioma/neuroblastoma** — directly relevant to hypothesis:0012. These TFs are both neural lineage specifiers and recurrently amplified/overexpressed in neural tumors; examining their position in our gene × cancer frequency matrix would test whether the hypothesis:0012 neural enrichment signal is partly lineage-survival biology.
- **Bailey et al. 2018 Table S1** — the PanCanAtlas driver list already in this pipeline's annotation layer. Cross-referencing Bailey drivers against tissue-specificity scores would partition them into lineage-survival vs. broadly-expressed driver categories — a concrete analysis enabled by existing pipeline outputs.
