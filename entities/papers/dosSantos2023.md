---
type: paper
title: Transcriptomic analysis reveals a tissue-specific loss of identity during ageing
  and cancer
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: paper:dosSantos2023
ontology_terms:
- tissue specificity
- cellular identity
- transcriptomics
- cancer dedifferentiation
- ectopic gene expression
- ageing
- tumor microenvironment
- tissue-of-origin
- tau index
- pan-cancer
datasets:
- dataset:tcga
- dataset:gtex
source_refs:
- cite:dosSantos2023
related:
- question:0042-driver-normal-expression-tissue-cell-type-specificity
- topic:lineage-addiction-and-cell-of-origin-driver-specificity
- topic:oncofetal-developmental-reprogramming
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
---

# Transcriptomic analysis reveals a tissue-specific loss of identity during ageing and cancer

<!--
- **Authors:** Gabriel Arantes dos Santos, Kasit Chatsirisupachai, Roberto A. Avelar, João Pedro de Magalhães
- **Year:** 2023
- **Journal:** BMC Genomics
- **DOI:** https://doi.org/10.1186/s12864-023-09756-w
- **BibTeX key:** dosSantos2023
- **Source:** PDF
-->

## Key Contribution

Using matched TCGA tumor vs. GTEx normal transcriptomes across 16 cancer types and 26 human
tissues, this study provides the first systematic pan-cancer demonstration that tumors undergo a
coordinated "loss of cellular identity": they downregulate genes highly specific to their tissue
of origin, while simultaneously activating genes normally unexpressed in that tissue and
upregulating genes specifically expressed in *other* tissues (ectopic expression). The same
pattern — downregulation of tissue-specific genes — was observed in 40% of normal tissues
during healthy ageing, but the cancer version is more pervasive, statistically stronger, and,
critically, fully independent of patient age. Both the downregulation of tissue-specific genes
and the activation of tissue-unexpressed genes are associated with worse patient survival.

## Methods

**Data.** TCGA harmonized RNA-seq read counts (hg38, TCGAbiolinks v2.14.1) for 16 cancer types
that had at least 10 adjacent-normal samples: BLCA, BRCA, COAD, ESCA, HNSC, KICH, KIRC, KIRP,
LIHC, LUAD, LUSC, PRAD, READ, STAD, THCA, UCEC. GTEx v8 normal tissue RNA-seq (26 tissues;
tissues with fewer than 50 complete samples excluded). Only protein-coding genes retained
(biomaRt).

**Differential expression.**
- Ageing DEGs (GTEx): linear model via limma; covariates = age (continuous), sex, death
  classification (Hardy scale), tissue region. DEG thresholds: BH-adjusted p < 0.05 and
  |log2 FC across 50 years| > log2(1.5).
- Cancer DEGs (TCGA vs. adjacent normal): DESeq2 default parameters; thresholds: FC > 2 and
  FDR < 0.01.

**Tissue-specificity classification.** Two-tier taxonomy based on the Tau index (Palmer et al.
2021, from GTEx data; tau = 1 → single-tissue specific; tau = 0 → ubiquitous):

| Category | Definition |
|---|---|
| High Tissue Specificity | tau > 0.8 (pan-tissue; 4,851 genes) |
| Low Tissue Specificity | tau < 0.2 (pan-tissue; 3,464 genes) |
| Tissue-Specific | tau > 0.95 AND average expression > 1 in the tissue of interest |
| Tissue-Unexpressed | expression = 0 in the tissue of interest |

For cancer analyses, "downregulated Tissue-Specific DEGs" and "upregulated Tissue-Unexpressed
DEGs" are the two key gene sets. Results were validated with an alternative specificity scheme
from Uhlén et al. 2015 (Human Protein Atlas).

**Overlap statistics.** Fisher's exact test with BH FDR correction; overlap significant at
FDR < 0.05.

**Survival.** Expression signatures built from the overlap genes; median-expression cutoff to
split groups; overall and disease-free survival analyzed on GEPIA2 (Mantel-Cox log-rank test,
heatmap = log2 hazard ratio; significant at FDR < 0.1).

**Age-stratified analysis.** Top and bottom 30th-percentile age groups within each of 7 cancer
types that had ≥10 normal controls per age group and no T-stage imbalance between groups
(KIRP, HNSC, COAD, LIHC, LUSC, LUAD, BRCA). DEGs compared between groups by Mann-Whitney U
test; fold changes compared to assess magnitude differences.

## Key Findings

### 1. Loss of tissue-specific gene expression in cancer (16 cancer types)

Across most of the 16 TCGA cancer types, tumors show statistically significant enrichment of
**downregulated Tissue-Specific genes** (FDR < 0.05, Fisher's exact test). Among the
statistically significant cancers, 20.5% to 51.3% of all tissue-specific genes for that
tissue are downregulated DEGs:

- Minimum: THCA (thyroid) — 20.5% of tissue-specific genes downregulated in tumor
- Maximum: KIRC (clear cell renal) — 51.3% of tissue-specific genes downregulated in tumor

Two exceptions to the general pattern: THCA and PRAD (prostate) do not show the typical
enrichment for downregulated Tissue-Specific genes.

Functional enrichment of downregulated Tissue-Specific DEGs confirms tissue-appropriate
losses: digestion genes lost in COAD and STAD, respiratory exchange genes in LUSC, organic
anion transport in the three renal cancers (KICH, KIRC, KIRP).

### 2. Ectopic / non-tissue gene activation in cancer

Simultaneously with tissue-identity loss, tumors show:

- **Upregulation of High Tissue Specificity genes** (pan-tissue category; genes highly
  specific to *some* tissue, not necessarily the tumor's tissue of origin): enriched in
  upregulated cancer DEGs across most cancers (FDR < 0.05). A follow-up analysis mapping
  these upregulated genes back to which normal GTEx tissues they are typically expressed in
  found **no obvious tissue pattern** — consistent with generalized ectopic expression rather
  than systematic reversion to a single other lineage.

- **Upregulation of Tissue-Unexpressed genes** (genes with zero expression in the normal
  tissue of origin): significant in **all cancers except THCA** (FDR < 0.05). GO enrichment
  of these upregulated tissue-unexpressed genes returned more than 140 biological process
  terms, predominantly: **cellular proliferation, DNA metabolism, immune response,
  embryogenesis, and morphogenesis**.

The co-occurrence of all three signals — downregulation of self-identity genes, upregulation
of other-tissue genes, and activation of normally-silent genes — constitutes what the authors
call "loss of cellular identity" in cancer.

### 3. Loss of tissue identity in ageing: partial, not pan-organismal

Of 26 GTEx tissues analyzed, approximately **40%** (10 tissues) show significant enrichment of
downregulated Tissue-Specific genes with age, *without* a corresponding significant result in
the opposite direction:

Tissues with age-associated tissue-identity loss: adrenal gland, brain, colon, esophagus,
lung, muscle, prostate, skin, small intestine, testis.

No significant age-associated upregulation of Tissue-Unexpressed genes was detected (Fig. 2B).
The ageing signal therefore resembles only *one arm* of the cancer pattern (loss of
self-identity genes) but lacks the robust gain of ectopic/unexpressed gene expression that
characterizes cancer.

### 4. Survival association

The loss-of-identity expression patterns predict worse patient outcomes (heatmaps, Fig. 3):

- **High expression of Tissue-Unexpressed gene signature → worse survival** (positive hazard
  ratio) across most cancers.
- **Low expression of Tissue-Specific gene signature → worse survival** (negative hazard
  ratio, i.e., high expression = better outcome) across most cancers.
- Kaplan-Meier curves of significant results (Fig. 3C + Figure S6) confirm: upregulation of
  High Tissue Specificity or Tissue-Unexpressed genes is associated with worse overall and
  disease-free survival; downregulation of Tissue-Specific genes is associated with worse
  prognosis. Partial exception: LIHC, where overexpression of Low Tissue Specificity genes
  is related to worse overall and disease-free survival.

### 5. Patient age does not drive cancer-associated identity loss

In 7 cancer types with sufficient matched-normal samples in young (bottom 30%) vs. old (top
30%) patient strata, the loss-of-identity pattern — downregulation of Tissue-Specific genes,
upregulation of Tissue-Unexpressed genes — is essentially **the same in young and old
patients** (Fig. 4). While hundreds of genes are unique to each age group (Table 2; e.g.,
KIRC: 210 old-exclusive up-DEGs, 220 down-exclusive), the overlap analysis and fold-change
comparisons between age groups show no significant difference in direction or magnitude for
the tissue-specificity signature. Only 5 individual genes show opposite expression patterns
between age groups across 7 cancers (COX4I2 in HNSC; NR4A2 and NR4A1 in COAD; CYP26A1 and
FDCSP in BRCA).

This age-independence supports the interpretation that loss of cellular identity is a
*fundamental step in carcinogenesis* rather than a consequence of pre-existing age-related
tissue changes accumulating in older patients.

## Relevance

### Critical methodological caveat for q042

This paper delivers a direct, quantitative warning for the design of
`question:0042-driver-normal-expression-tissue-cell-type-specificity`. Because tumors
systematically **downregulate the tissue-specific genes of their tissue of origin** and
simultaneously **gain expression of genes from other tissues**, any characterization of a
driver gene's "normal expression specificity" must be anchored to **normal-tissue reference
expression**, not to tumor expression profiles.

Concretely:
- If one uses TCGA tumor expression to ask "is this driver gene tissue-specifically expressed
  in the cancer in which it is mutated?", the answer will be systematically biased: the tumor
  has already lost much of the tissue-specific expression it started with, and gained
  expression of genes from unrelated tissues. The specificity signal will be washed out or
  inverted.
- The correct reference is a **normal tissue or cell-type expression atlas** — GTEx (which
  this paper itself uses), Human Protein Atlas, Tabula Sapiens, or similar. The Tau index
  applied to GTEx is exactly what q042's proposed Tau-based normal-expression specificity
  metric should be built on, and this paper validates that design choice directly.

The effect sizes reported (20.5%–51.3% of tissue-specific genes downregulated per cancer,
with strong ectopic expression of other-tissue genes) are large enough that using tumor
expression would not merely add noise — it would structurally invert the specificity
measurement for the genes that matter most.

### Substantive overlap with oncofetal-developmental reprogramming

The GO terms returned for upregulated Tissue-Unexpressed genes include **embryogenesis and
morphogenesis** prominently alongside proliferation and immune response. This connects
directly to `topic:oncofetal-developmental-reprogramming`: the "silence-then-activate"
mechanism documented here (normally-silent genes turned on in cancer) is the expression-level
complement of the oncofetal reactivation axis. Importantly, this paper shows the phenomenon
is pan-cancer and not concentrated in any specific histology, which matches the prediction
from `hypothesis:0012-neural-gene-enrichment-length-histology-artifact` (that ectopic
expression is a general cancer-biology property rather than a neural-specific one). Neural
developmental genes, being among the many categories of tissue-specific or normally-silent
genes in non-neural tissues, would be expected to appear in the "Tissue-Unexpressed
upregulated" set for a wide range of cancer types — exactly the confound h12 is concerned
about.

### Connection to lineage addiction

The tissue-of-origin downregulation finding reinforces that "lineage addiction" (the
dependence of some drivers on the transcriptional program of the cell of origin, central to
`topic:lineage-addiction-and-cell-of-origin-driver-specificity`) must be understood against
the backdrop of progressive identity loss. Lineage-addicted oncogenes likely act early —
before or as identity erosion begins — while their downstream tissue-specific targets are
being lost. This implies a temporal dimension: drivers that depend on normal-tissue TF
programs may have a narrower therapeutic window as tumor dedifferentiation progresses.

### Ageing arm: separate from cancer, but relevant to project scope

The 40%-of-tissues ageing finding is interesting context for `topic:cancer-driver-genes` but
is not a direct methodological input to q042. The key comparison is that ageing shows
downregulation of tissue-specific genes *without* the robust gain of ectopic/unexpressed gene
expression that characterizes cancer. This divergence argues against the simplest hypothesis
that "old patients just have more dedifferentiated tumors" — the cancer loss-of-identity
process is age-independent.

## Project Framework Mapping

| Paper Concept | Project Concept / Analysis Hook | Notes |
|---|---|---|
| Tau index (GTEx-based) | Normal-expression tissue-specificity metric for q042 | Direct methodological match; this paper validates Tau as the right measure |
| Downregulation of Tissue-Specific genes in tumor | Loss-of-identity baseline | Quantifies magnitude: 20.5%–51.3% of tissue-specific genes lost per cancer type |
| Upregulation of Tissue-Unexpressed genes | Ectopic activation / oncofetal reactivation | GO terms include embryogenesis — connects to oncofetal topic |
| Upregulation of High Tissue Specificity genes from other tissues | Cross-lineage contamination | No obvious single target tissue; generalized instability |
| 40% of tissues in ageing | Ageing-associated identity drift | Partial signal; lacks ectopic-activation arm present in cancer |
| Survival association of identity-loss signatures | Clinical prognostic relevance | Downregulation of tissue-specific genes = worse prognosis |
| Age-independence of cancer identity loss | Carcinogenesis-intrinsic mechanism | Not age-confounded; fundamental step in transformation |
| THCA / PRAD exceptions | Outlier cancers for identity-loss hypothesis | May reflect high differentiation state of these tumors |

## Limitations

1. **Bulk RNA-seq only.** All TCGA and GTEx data are bulk tissue, so the cell-type-level
   contributors to identity loss cannot be resolved. Admixture of stromal, immune, and
   epithelial cells in tumor samples could partly explain upregulation of "other-tissue" genes
   (e.g., immune cells bringing non-epithelial expression programs). The authors acknowledge
   this but do not quantify the stromal contribution.

2. **Adjacent-normal as cancer reference.** TCGA adjacent-normal tissue may be partially
   "field-cancerized" or inflammation-adjacent, which could attenuate the measured
   fold-changes relative to truly normal tissue. The GTEx-derived tau classification mitigates
   this partially (tau is defined on healthy GTEx tissue), but DEG detection for cancer still
   uses TCGA adjacent-normal as the normal comparator.

3. **No causal direction.** The transcriptomic analysis is cross-sectional; it cannot
   establish whether identity loss *drives* carcinogenesis or is a consequence of it.
   The age-independence result is consistent with identity loss being causal but does not
   prove it.

4. **Survival signatures not validated in independent cohorts.** Survival analysis performed
   entirely within TCGA/GEPIA2. No external validation dataset is reported.

5. **GO enrichment broadly categorized.** More than 140 GO terms for upregulated
   Tissue-Unexpressed genes suggests a diffuse signal. Without ranked effect sizes per cancer
   type, it is difficult to assess whether "embryogenesis" terms dominate or appear as
   secondary signals.

6. **No single-cell resolution for ectopic expression.** Whether the ectopic expression of
   "other-tissue" genes occurs in cancer epithelial cells, tumor-recruited stromal cells, or
   both is unresolved. Single-cell TCGA / HCA data would be needed to distinguish these.

## Model / Tool Availability

No computational tool or trained model is released. The analysis uses publicly available
packages (DESeq2, limma/edgeR, WebGestalt, GEPIA2) and publicly available data (TCGA via
TCGAbiolinks, GTEx portal). The Tau index gene lists (Palmer et al. 2021) and supplementary
DEG tables are available in the paper's supplementary files. Code is not explicitly deposited
but the pipeline is described in sufficient detail to reproduce.

## Follow-up

### Papers this paper cites that are directly relevant

- **Palmer et al. 2021** (Aging 13:3313–41) — the source of the Tau index classification used
  throughout; the ageing transcriptome meta-analysis this study extends.
- **Chatsirisupachai et al. 2019** (Aging Cell 18:e13041) — from the same lab; prior analysis
  of age/cancer/senescence transcriptomics that this paper builds on directly.
- **Chatsirisupachai et al. 2021** (Nat Commun 12:2345) — integrative age-associated
  multi-omic landscape in cancer; defines the age-stratified cancer DEG framework used here.
- **Malta et al. 2018** (Cell 173:338–354) — machine learning identifies stemness features
  in oncogenic dedifferentiation; directly supports the dedifferentiation interpretation.
- **Uhlén et al. 2015** (Science 347:1260419) — Human Protein Atlas tissue-expression
  database; used as the alternative specificity classifier in validation analysis.
- **Izgi et al. 2022** (eLife 11) — inter-tissue convergence during ageing (loss of cellular
  identity in ageing mice + GTEx); most directly comparable prior study.
- **Yuan et al. 2019** (Cancer Discov 9:837–51) — cellular plasticity in cancer; background
  for the "unlocking phenotypic plasticity" hallmark framing.
- **Haigis et al. 2019** (Science 363:1150–1) — tissue-specificity in cancer: already in
  project bibliography as `paper:Haigis2019`.

### Open questions this paper raises for the project

1. **q042 reference-expression design confirmation.** This paper provides formal justification
   to use GTEx/HPA Tau as the specificity metric for q042 rather than any tumor-derived
   expression reference. The q042 write-up should cite dosSantos2023 explicitly for this
   design choice.

2. **Ectopic expression as confounder for neural gene enrichment.** If upregulated
   Tissue-Unexpressed genes in non-neural tumors include neural developmental genes (plausible
   given the embryogenesis GO terms), this would create a systematic false-positive signal in
   any pan-cancer "neural gene" analysis that uses tumor expression rather than mutation data.
   This is a refined version of the h12 concern: even mutation-frequency analyses are not
   immune if the gene expression patterns drive selection for somatic events at ectopically
   expressed loci.

3. **Which cancer types lose identity fastest?** The range 20.5% (THCA) to 51.3% (KIRC)
   suggests substantial inter-cancer variation. Cancers with the strongest identity loss might
   be those most prone to false-positive tissue-specificity assignments in q042 if tumor
   expression were naively used.

4. **Survival signature validation.** Testing whether the Tissue-Unexpressed upregulation
   signature (with prominent embryogenesis/morphogenesis GO terms) overlaps with any of the
   driver gene sets in the cbioportal pipeline could connect expression-level identity loss
   to somatic mutation patterns.
