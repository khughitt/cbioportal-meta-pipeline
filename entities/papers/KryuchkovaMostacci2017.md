---
type: paper
title: A benchmark of gene expression tissue-specificity metrics
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: paper:KryuchkovaMostacci2017
ontology_terms:
- tissue specificity
- gene expression
- RNA-seq
- Tau
- housekeeping genes
- tissue-specific genes
- benchmarking
datasets: []
source_refs:
- cite:KryuchkovaMostacci2017
related:
- question:0042-driver-normal-expression-tissue-cell-type-specificity
- topic:lineage-addiction-and-cell-of-origin-driver-specificity
- discussion:0008-tissue-cell-type-specificity-of-cancer-drivers
- hypothesis:0003-gene-length-confounds-literature-attention
---

# A benchmark of gene expression tissue-specificity metrics

- **Authors:** Nadezda Kryuchkova-Mostacci and Marc Robinson-Rechavi
- **Year:** 2017
- **Journal:** Briefings in Bioinformatics, 18(2):205-214
- **DOI/URL:** https://doi.org/10.1093/bib/bbw008
- **PMID:** 26891983 ; **PMCID:** PMC5444245
- **BibTeX key:** KryuchkovaMostacci2017
- **Source:** Full text (Europe PMC XML, PMC5444245)

## Key Contribution

This paper is the primary benchmark for gene-expression tissue-specificity metrics. It compares nine
metrics — Tau, Gini, TSI, Counts, Hg (Shannon entropy-based), z-score, SPM, EE, and PEM — across
RNA-seq and microarray data in human and mouse, evaluating robustness to tissue-set size,
cross-species conservation, and ability to separate biologically known tissue-specific from
housekeeping gene categories. The central conclusion is that **Tau is the most robust overall
metric** and should be the default choice when a single scalar tissue-specificity score is needed.
Gini and simple Counts (with a well-chosen threshold) are acceptable alternatives; z-score performs
poorly and should not be used.

## Methods

**Data.** Four expression datasets were benchmarked:
- Human RNA-seq: 27 tissues (Fagerberg et al., E-MTAB-1733)
- Mouse RNA-seq: 22 tissues (ENCODE, GSE36025)
- Human microarray: 32 tissues (GSE2361)
- Mouse microarray: 19 tissues (GSE9954)

Additionally, a 6-tissue human + 8-tissue mouse RNA-seq dataset from Brawand et al. (Bgee) was
used for cross-species comparisons. All RNA-seq values < 1 RPKM were set to not expressed; data
were log-transformed before metric calculation. Values are averaged across replicates per tissue;
genes not expressed in at least one tissue were removed.

**Metrics evaluated.** Nine metrics spanning two classes:

*Global specificity scores (one number per gene):*
- **Tau:** τ = Σ(1 − x̂_i) / (n−1), where x̂_i = x_i / max(x_i). Range 0 (ubiquitous) to 1 (specific).
- **Gini:** inequality coefficient adapted from economics; range 0–(n−1)/n, rescaled to 0–1.
- **TSI** (tissue specificity index): max(x_i) / Σx_i.
- **Counts:** number of tissues where the gene exceeds an expression threshold (RPKM ≥ 1).
- **Hg:** Shannon entropy −Σ p_i · log₂(p_i), where p_i = x_i / Σx_i; inverted so high = specific.

*Per-tissue scores (maximum assigned as global score):*
- **z-score:** (x_i − μ) / σ; only over-expression arm used for comparability.
- **SPM:** x_i² / Σx_i².
- **EE** (expression enrichment): x_i / (Σx_i · s_i / Σs_i), normalized by tissue-wide expression.
- **PEM** (preferential expression measure): log₁₀(EE).

**Evaluation criteria.**
1. *Robustness to tissue-set size:* correlation between scores computed on all tissues vs. random
   subsets of 5 tissues (1000 permutations).
2. *Cross-species conservation:* Pearson r between human and mouse orthologous gene scores on
   16 common tissues.
3. *Biological signal:* ability to separate gene sets with known tissue-specific (spermatogenesis,
   neurological process, xenobiotic metabolism) or housekeeping (protein folding, membrane
   organization, RNA splicing) GO annotations.
4. *Normalization sensitivity:* comparison of log-transformed RPKM vs. raw RPKM vs. log +
   quantile-normalized RPKM.

## Key Findings

1. **Tau is the best overall metric.** It shows the highest robustness to tissue-set sampling
   (mean r > 0.4 on 5-tissue subsets), high cross-species conservation (r > 0.69 on 16 tissues),
   and the best separation of GO-annotated tissue-specific from housekeeping gene sets. Among
   methods tested, Tau uniquely detects tissue-specific genes missed by all other metrics, and GO
   enrichment confirms those additional genes have biologically coherent tissue functions.

2. **Gini and Counts are acceptable alternatives.** Gini shows performance comparable to Tau on
   most tests. Counts works well if the expression threshold (RPKM ≥ 1 for RNA-seq) is chosen
   appropriately, though it tends to under-call tissue-specific genes.

3. **z-score is the worst metric.** It shows negative correlation between full and 5-tissue subset
   scores, meaning it cannot be used reliably when tissue sampling is limited.

4. **Distribution shape matters.** Most metrics produce strongly bimodal distributions skewed
   toward ubiquitous. Tau provides the least skewed distribution with the most intermediate-scoring
   genes, indicating it captures more variance in expression pattern.

5. **All metrics show strong negative correlation with mean expression level** (r = −0.69 to
   −0.93 for RNA-seq). Tissue-specific genes tend to be more lowly expressed — a key confound
   for downstream interpretation.

6. **Log-transformation is critical.** Without log-transformation, raw RPKM data inflate
   tissue-specificity scores for all metrics, particularly Tau, and substantially reduce
   cross-subset and cross-species correlations. Quantile normalization across tissues has
   negligible effect on the metric rankings.

7. **RNA-seq outperforms microarrays.** RNA-seq detects nearly twice as many expressed genes,
   especially in the lowly expressed, tissue-specific category that microarrays miss. Cross-subset
   correlations are consistently higher for RNA-seq than microarray; past microarray-based
   evolutionary analyses should be treated cautiously.

8. **Testis is the dominant outlier tissue.** Including testis in any 5-tissue subset dramatically
   improves robustness correlations because testis contains the largest number of tissue-specific
   genes. Brain is the second most influential tissue. This has direct implications for designing
   reference expression atlases: omitting testis inflates apparent sensitivity to tissue sampling.

9. **Per-tissue scores: PEM is the best per-tissue metric**, performing most similarly to Tau when
   a tissue-level assignment is needed; alternatively, Tau can be combined with the tissue of
   highest expression to get tissue-of-specificity assignments.

## Relevance

This paper is the methods anchor for **question:0042-driver-normal-expression-tissue-cell-type-specificity** (are cancer drivers biased toward tissue/cell-type-
restricted normal expression?). It provides a citable, benchmarked recommendation — **use Tau** —
with a clear formula and known failure modes, so any specificity score computed for the question's
analysis rests on a defensible methodological choice rather than an ad-hoc selection.

**Specific implications for question:0042-driver-normal-expression-tissue-cell-type-specificity and the cbioportal pipeline:**

- **Metric choice:** Tau should be the default specificity score computed on normal reference
  expression data. Gini is an acceptable secondary check. z-score should be avoided.

- **Reference data grain:** The metric must be applied to a chosen normal-expression reference.
  For *tissue grain* (matching the cancer-type labels in cBioPortal), compute Tau on bulk GTEx
  or BrainSpan. For *cell-type grain* (finer resolution relevant to lineage addiction), compute
  Tau on Human Protein Atlas single-cell RNA-seq or Tabula Sapiens; these are distinct analyses
  with different biological interpretations.

- **Interaction with hypothesis:0003-gene-length-confounds-literature-attention.** Finding #5 above — all metrics
  negatively correlate with mean expression level (r up to −0.93) — is a critical confound.
  Lowly expressed genes score as more tissue-specific by construction, which directly interacts
  with the gene-length / detection-bias confound in the hypothesis: short/lowly-expressed genes may
  appear both tissue-specific AND under-represented in mutation literature, making it difficult
  to separate true tissue restriction from detection artifact. Any question:0042-driver-normal-expression-tissue-cell-type-specificity analysis should therefore
  stratify or residualize on mean expression level when using Tau scores.

- **Tissue-set composition:** Including testis in the reference panel will dominate the
  tissue-specific tail (finding #8). The cBioPortal pipeline has limited testis-specific cancer
  types, so Tau computed on a GTEx panel that includes testis may classify many testis-specific
  genes as highly specific even though they are irrelevant to the cancers in the analysis. Either
  exclude testis from the Tau computation or report results with and without.

- **Log-transformation requirement (finding #6):** GTEx TPM / FPKM values must be
  log-transformed before computing Tau (set values < 1 to not expressed). Failing to
  log-transform will inflate specificity scores for highly expressed tissue-restricted genes.

- **Cross-platform note:** If the reference expression data spans multiple technologies (e.g.,
  bulk RNA-seq GTEx + single-cell HPA), Tau should be computed separately per platform; the
  paper shows RNA-seq and microarray produce different absolute Tau distributions and cannot
  be directly merged.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Tau metric (0 = ubiquitous, 1 = specific) | question:0042-driver-normal-expression-tissue-cell-type-specificity specificity score | Canonical recommended metric |
| Normal reference expression atlas | GTEx (tissue grain) / HPA / Tabula Sapiens (cell-type grain) | Must choose grain appropriate to research question |
| Housekeeping genes (Tau ≈ 0) | Broadly expressed reference set | Contrast class for question:0042-driver-normal-expression-tissue-cell-type-specificity enrichment analysis |
| Tissue-specific genes (Tau ≈ 1) | Lineage-restricted driver candidates | Test set for question:0042-driver-normal-expression-tissue-cell-type-specificity |
| Negative correlation: specificity ↔ mean expression | Gene-length / expression confound in hypothesis:0003-gene-length-confounds-literature-attention | Must residualize or stratify in question:0042-driver-normal-expression-tissue-cell-type-specificity analysis |
| Testis-specific genes dominating high-Tau tail | Testis cancer type (TGCT) in cBioPortal | Consider excluding testis from Tau reference panel or analysing separately |
| Log-transform before Tau calculation | Pre-processing step for any GTEx / HPA input | Set values < 1 TPM/RPKM to 0 or not-expressed |

## Limitations

- The benchmark uses only bulk tissue expression (RNA-seq or microarray). Cell-type-level
  specificity — which is arguably more relevant for lineage addiction — is not addressed.
  Tau can be applied to single-cell pseudobulk or cell-type-level data, but this paper provides
  no evaluation of its performance in that setting.

- The RNA-seq datasets tested span 27 (human) and 22 (mouse) tissues. Many cancer-relevant
  cell types (e.g., specific haematopoietic progenitor types, neural crest derivatives) are not
  represented as distinct tissues in the tested panels, so Tau computed on these panels will
  miss cell-type-restricted expression.

- The paper does not address the situation where a gene is lowly expressed everywhere but
  slightly higher in one tissue — such genes can score high Tau purely because of the ratio
  structure, even if absolute expression differences are negligible. There is no minimum
  expression or minimum fold-change filter built into Tau.

- Human and mouse data were evaluated; no other species. For cross-species evolutionary
  analyses, this is fine; for single-species biomedical use (cancer), the mouse validation is
  supportive but not the primary concern.

- The benchmark predates large single-cell RNA-seq atlases (Tabula Sapiens, HCA). Performance
  of Tau at single-cell resolution, where dropout and sparsity are major issues, is not evaluated.

## Model / Tool Availability

The R script implementing all nine metrics and producing all benchmark figures is provided in the
Supplementary Materials of the paper (available via PMC5444245). No standalone package was
released, but Tau's formula is simple enough to implement in two lines of Python/R (see Methods
section formula above). The Bgee database (https://www.bgee.org/) provides pre-computed
tissue-specificity scores based on Tau for human and mouse genes across multiple expression atlases.

## Follow-up

- **Compute Tau for question:0042-driver-normal-expression-tissue-cell-type-specificity:** Apply Tau to GTEx v8 bulk RNA-seq (54 tissues) and/or Human Protein
  Atlas cell-type-resolved data. Cross-reference the resulting per-gene Tau scores against the
  pipeline's `gene_cancer_study_ratio_annotated.feather` to ask whether high-Tau (tissue-specific)
  genes are over-represented among Bailey et al. [@Bailey2018] drivers.
- **Residualize on expression level:** Because Tau correlates strongly (negatively) with mean
  expression, regress out log mean expression before testing for driver enrichment among
  high-Tau genes — otherwise the test conflates tissue restriction with low overall expression.
- **Testis sensitivity analysis:** Run question:0042-driver-normal-expression-tissue-cell-type-specificity analysis with and without testis in the Tau reference
  panel; report whether conclusions change (expected to affect TGCT-relevant genes most).
- **Single-cell Tau:** Explore Tau computed on Tabula Sapiens or HCA cell-type pseudobulks to ask
  the same question at cell-type grain — this may be a more mechanistically appropriate level for
  lineage addiction hypotheses.
- **Bgee pre-computed scores:** Check whether Bgee's pre-computed Tau scores (which use a curated
  multi-study RNA-seq compilation including GTEx) can serve as an off-the-shelf input for question:0042-driver-normal-expression-tissue-cell-type-specificity,
  avoiding the need to recompute from raw GTEx.
- Read next: Yanai et al. 2005 (original Tau paper), the GTEx v8 tissue eQTL/expression
  atlas used as Tau input), and any papers benchmarking Tau on single-cell data.
