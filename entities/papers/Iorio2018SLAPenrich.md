---
type: paper
title: Pathway-based dissection of the genomic heterogeneity of cancer hallmarks'
  acquisition with SLAPenrich
status: active
created: '2026-06-07'
updated: '2026-06-27'
id: paper:Iorio2018SLAPenrich
ontology_terms:
- cancer hallmarks
- somatic mutation
- pathway enrichment
- genomic heterogeneity
- Poisson-binomial distribution
- cancer evolution
- mutual exclusivity
- pan-cancer analysis
- pathway alteration
- hallmark acquisition
dataset_usage:
- ref: dataset:tcga
  role: analyzed
  overlap: full
source_refs:
- cite:Iorio2018SLAPenrich
related:
- hypothesis:0004-mhn-pathway-ordering
- discussion:0007-hallmark-ordering-and-data-driven-modules
- topic:co-occurrence-and-mutual-exclusivity
---

# Pathway-based dissection of the genomic heterogeneity of cancer hallmarks' acquisition with SLAPenrich

<!-- Authors: Francesco Iorio, Luz Garcia-Alonso, Jonathan S. Brammeld, Iñigo Martincorena, David R. Wille, Ultan McDermott, Julio Saez-Rodriguez -->
<!-- DOI: https://doi.org/10.1038/s41598-018-25076-6 -->
<!-- BibTeX key: Iorio2018SLAPenrich -->
<!-- Source: Full text (PMC open access) -->

- **Authors:** Francesco Iorio, Luz Garcia-Alonso, Jonathan S. Brammeld, Iñigo Martincorena, David R. Wille, Ultan McDermott, Julio Saez-Rodriguez
- **Year:** 2018
- **Journal:** Scientific Reports
- **Volume/Issue:** 8:6713
- **DOI/URL:** https://doi.org/10.1038/s41598-018-25076-6
- **BibTeX key:** Iorio2018SLAPenrich
- **Source:** Full text (PMC open access, PMC5928049)

## Key Contribution

This paper introduces SLAPenrich (Sample-population Level Analysis of Pathway enrichments), a population-level statistical enrichment method that identifies pathways significantly altered across a population of cancer samples — distinguishing it from per-sample enrichment tools.
The central application is systematic characterisation of the genomic heterogeneity of cancer hallmark acquisition: across 4,415 TCGA patients and 10 cancer types, the authors map somatic mutation pathway enrichments onto the 10 canonical Hanahan-Weinberg hallmarks, demonstrating that different cancer lineages acquire the same hallmarks through distinct and heterogeneous pathway alterations ("hallmark heterogeneity signatures").
A secondary finding is that enrichments are substantially preserved even after removing known high-confidence cancer driver genes, suggesting that infrequent mutations in hallmark-associated pathways collectively constitute a genuine signal beyond established drivers [@Iorio2018SLAPenrich].

For this project, SLAPenrich is relevant primarily as the curated pathway→hallmark bridge: its manually curated mapping of 374 Pathway Commons gene-sets onto the 10 canonical hallmarks is the resource one would use to post hoc annotate data-driven mutual-exclusivity modules with hallmark labels — i.e. to ask whether the data's own partition aligns with the canonical human hallmark schema (the label-free module question in `discussion:0007-hallmark-ordering-and-data-driven-modules`).

## Methods

### Dataset

TCGA somatic mutation data (PANCAN dataset, MAF files) from 10 cancer types: breast invasive carcinoma (BRCA, n=1,132), colon/rectum adenocarcinoma (COREAD, n=489), glioblastoma multiforme (GBM, n=365), head and neck squamous cell carcinoma (HNSC, n=375), kidney renal clear cell carcinoma (KIRC, n=417), lung adenocarcinoma (LUAD, n=388), ovarian serous cystadenocarcinoma (OV, n=316), prostate adenocarcinoma (PRAD, n=242), skin cutaneous melanoma (SKCM, n=369), thyroid carcinoma (THCA, n=322).
Total: 4,415 samples [@Iorio2018SLAPenrich].

### Pathway gene-sets

374 curated pathway gene-sets sourced from Pathway Commons v8 (2016), encompassing 3,915 unique genes.
These were manually curated via a computer-aided keyword-matching process and assigned to 10 canonical cancer hallmarks.
Of the 374 pathways, 298 (80%) map to exactly one hallmark; the remainder map to 1–2 hallmarks; 99% map to at most 2.
The resulting hallmark-tagged collection is referred to as the Hallmark-Mapped Alteration (HMA) pathway set [@Iorio2018SLAPenrich].

### Statistical model (SLAPenrich)

The core question is: does the observed number of samples harbouring at least one mutation in pathway P exceed what is expected by chance, accounting for each sample's individual mutation burden and each gene's exonic content?

**Per-sample pathway alteration probability (primary model — Bernoulli/Poisson):**

For sample j and pathway P, the probability that sample j contains at least one mutated gene in P is:

> p_j(P) = 1 − exp(−ρ_j · k'(P))

where ρ_j is the background somatic mutation rate for sample j (total non-synonymous mutations divided by total callable exonic bases), and k'(P) is the total exonic content (in bp) of pathway P. This per-sample Bernoulli probability incorporates both mutation burden and gene-set size in a biologically motivated way: larger pathways and more hypermutated samples yield higher expected probabilities.

An alternative hypergeometric model (equation 2 in the paper) treats the genome as N′ = Σλ(g) total exonic bases and k′(P) as the pathway's portion, sampling n_j mutated bases per sample; results were consistent with the Bernoulli model.

**Expected vs. observed:**

The expected number of samples with ≥1 mutation in P across the cohort is E[P] = Σ_j p_j(P). The observed count is O[P] = |{j : pathway P is mutated in j}|.

The enrichment effect size is the Pathway Alteration Index: Δ(P) = log₁₀(O[P] / E[P]).

**Significance — Poisson-binomial p-value:**

Because samples have heterogeneous per-sample probabilities p_j, the distribution of the sum of n independent Bernoulli(p_j) variables is a Poisson-binomial distribution (not a standard Poisson or binomial). The p-value for pathway P is Pr(X ≥ O[P]) under the Poisson-binomial with parameters {p_j}. Multiple-hypothesis correction uses Benjamini-Hochberg FDR; enrichments reported at FDR < 5%.

An additional constraint, exclusive coverage > 50%, requires that the majority of the mutated samples in P be "exclusively" covered — i.e. the pathway alteration is not entirely explained by a single dominant driver gene. This mutual-exclusivity-aware filter suppresses enrichments driven by a single gene with high frequency that would trivially explain the pathway result.

### Hallmark heterogeneity scoring

Two summary metrics quantify heterogeneity:

- **Pathway Heterogeneity Score (PHS):** For a given enriched pathway, the number of cancer types in which it is significantly enriched divided by the total tested. High PHS = pathway altered in many cancer types; low PHS = cancer-type-specific.
- **Cumulative Heterogeneity Score (CHS):** For a given hallmark and cancer type, the proportion of that hallmark's HMA-pathways that are significantly enriched. CHS summarises how broadly a hallmark's associated pathways are altered in that cancer type.

### Driver-gene filtering sensitivity analysis

To test whether enrichments reflect genuine hallmark biology beyond established cancer genes, the authors re-ran SLAPenrich after removing mutations in high-confidence cancer genes (HCGs — a combined driver list from multiple selection-based methods, analogous to a Bailey-type driver census).
On average, 21% of original enrichments were retained after HCG removal (range: 2.1% in GBM to 56.2% in COREAD).
The preserved hallmark heterogeneity structure was assessed by comparing CHS-based hallmark signatures with vs. without HCGs via correlation [@Iorio2018SLAPenrich].

### Robustness

SLAPenrich was tested against simulated noise (mutation call sensitivity perturbed from 95% to 50%, false-negative rates varied): median AUROC > 0.995 under sensitivity perturbation and > 0.99 under false-negative variation, indicating robustness to sequencing noise [@Iorio2018SLAPenrich].

## Key Findings

### Hallmark heterogeneity signatures are cancer-type-specific

The HMA analysis produced a 10-cancer × 10-hallmark CHS matrix ("hallmark heterogeneity signatures") showing which hallmarks are most heavily altered in each cancer type, and by which pathways. Key observations:

- **Sustaining proliferative signaling / evading growth suppressors** are broadly altered across most cancer types, consistent with their pan-cancer driver status.
- **Genome instability and mutation:** BRCA and OV show enrichment in homologous recombination deficiency pathways; COREAD shows microsatellite instability-related pathways; SKCM shows unique miRNA-mediated DNA-damage response pathways.
- **Avoiding immune destruction:** Extensive pathway enrichment in COREAD; minimal enrichment in most other cancers — making this a highly lineage-specific hallmark enrichment pattern.
- **Tumor-promoting inflammation:** Predominantly enriched in COREAD; SKCM shows exclusive enrichment of IRF3-related (innate immune) pathways not found elsewhere.
- **Deregulating cellular energetics (Warburg effect):** Enriched pathway detected only in GBM (not other cancer types), consistent with GBM's distinctive metabolic dependencies.

### Enrichment is not simply a function of mutation burden or sample size

CHS per cancer type (median enriched HMA-pathways: range 55 for PRAD to ~200 for BRCA and COREAD) showed only a weak correlation with sample size (R = 0.53, p = 0.11) and was essentially uncorrelated with average mutations per sample (R = 0.16, p = 0.65).
SKCM, which has the highest average point mutation count per sample (387.63), has fewer enriched HMA-pathways than half the cancer types — because its high background rate inflates individual p_j values, reducing the signal-to-expected ratio.
THCA has the lowest average mutations per sample (15.03) but still yields more enriched pathways than four other cancer types.
This decoupling validates that SLAPenrich's per-sample probability normalisation is doing meaningful work [@Iorio2018SLAPenrich].

### Driver removal preserves hallmark structure

After removing HCG mutations, hallmark heterogeneity signatures are largely conserved (high correlation between original and filtered CHS matrices), but with reduced magnitude. Examples of specific enrichments surviving HCG removal:

- **Activation of matrix metalloproteinases** (invasion and metastasis hallmark) in COREAD (FDR = 0.002%), driven by Plasminogen (PLG) mutations — not a canonical CRC driver.
- **IL-6 type cytokine receptor ligand interactions** (tumor-promoting inflammation) in SKCM (FDR = 4.6%), featuring OSMR.
- **PDGF receptor signaling** (angiogenesis) in SKCM (FDR = 2.7%).
- **RAC1 activity regulation** (invasion/metastasis) in COREAD, detected through mutual exclusivity patterns.

These results suggest the HMA framework can identify non-obvious functional alterations in sparsely mutated genes that collectively contribute to hallmark acquisition.

### Novel candidate genes/pathways identified

The mutual-exclusivity-aware pathway enrichment, combined with HCG filtering, flags candidates such as PLG (plasminogen) in CRC invasion pathways and OSMR in melanoma inflammation pathways — neither is a well-established cancer gene, but each appears in the context of a pathway that is enriched at the population level.

## Relevance

### (a) Pathway→hallmark bridge for post hoc annotation of data-driven modules

SLAPenrich's curated HMA gene-set collection (374 Pathway Commons pathways mapped to 10 canonical hallmarks) is the most direct available resource for answering the project's label-free module question: after inferring mutual-exclusivity modules from the cBioPortal mutation data (via DISCOVER/WeSME or `paper:RaphaelVandin2015`'s ILP), one would enrich each data-driven module against the HMA gene-sets to ask whether the module's genes map predominantly to one hallmark or span several.
This is the annotate-post-hoc step described in `discussion:0007-hallmark-ordering-and-data-driven-modules`.
The mapping is curated by domain experts (computer-aided manual curation), making it a principled reference; however, it is also the human-label dependency the project wants to test (see next point) [@Iorio2018SLAPenrich].

### (b) The curated hallmark→gene mapping is a dependency, not a ground truth

The hallmark heterogeneity findings in this paper are entirely downstream of the human-assigned pathway→hallmark labels.
The 374 pathway→hallmark associations were made by the authors through keyword matching and manual review; they reflect the current expert consensus on which pathways "belong to" which hallmark, which is exactly the partitioning the project wants to validate or challenge from data [@Iorio2018SLAPenrich].
If one uses SLAPenrich's HMA labels to annotate data-driven modules, the test of "do the inferred modules recapitulate hallmarks?" is partially circular — the modules can only recapitulate hallmark labels if the gene-to-hallmark mapping is correct.
The project should treat the HMA labelling as a testable prior, not as a gold standard: enrich data-driven modules against HMA gene-sets, compute overlap statistics, but also allow modules to span or split hallmarks.
A module that perfectly matches one hallmark is evidence the partition is real; a module that straddles two hallmarks is evidence either the module boundary or the hallmark boundary is wrong.

### (c) Relation to Sanchez-Vega pathways already in the pipeline

The pipeline already implements the Sanchez-Vega ten-pathway annotation (`process_sanchez_vega_pathways.py`) [@SanchezVega2018]. The Sanchez-Vega pathways are a different set (10 signalling pathways rather than 374 hallmark-grouped pathways), oriented around recurrently altered oncogenic signalling axes (RTK/RAS, Wnt, PI3K, etc.) rather than hallmark capabilities. The SLAPenrich HMA gene-sets are orthogonal: they provide hallmark-level semantic labels (e.g., "enabling replicative immortality", "avoiding immune destruction") rather than signalling-pathway functional labels. The relationship is: Sanchez-Vega pathways feed into hypothesis:0004-mhn-pathway-ordering at the signalling-pathway grain; SLAPenrich HMA gene-sets would serve as a second annotation layer to map inferred modules or Sanchez-Vega pathway alterations onto hallmark-level biology. One could, for example, ask whether hypothesis:0004's ordering of Sanchez-Vega pathways recapitulates the hallmark acquisition order implied by this paper's CHS results.

### (d) Population-level method is well-matched to the pipeline's cross-study design

Because SLAPenrich tests enrichment across a population of samples rather than per-sample, it is conceptually aligned with the pipeline's aggregation design. The per-sample mutation rate normalisation accounts for the same TMB heterogeneity that motivates the pipeline's `is_hypermutator` flag and inclusive/exclusive count pairs. For application to the pipeline's gene × cancer matrix, the SLAPenrich statistics (expected vs. observed pathway alteration) could be computed per cancer type using the pipeline's ratio table rather than raw mutation calls.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| 374 HMA pathway gene-sets (Pathway Commons → 10 hallmarks) | Post hoc hallmark annotation of data-driven modules | The curated bridge for the label-free module question in `discussion:2026-06-07` |
| Hallmark heterogeneity signatures (CHS matrix) | Hallmark-level ordering / enrichment results | Would be one output of the hypothesis:0004 aggregation-to-hallmark layer |
| Poisson-binomial population enrichment | Cross-study gene/pathway mutation rate enrichment | Method analogous in spirit to the pipeline's per-cancer-type ratio tables; normalises for per-sample TMB |
| Exclusive coverage filter (mutual-exclusivity-aware) | `topic:co-occurrence-and-mutual-exclusivity` | Direct overlap; suppresses single-gene-driven enrichments analogous to the callability null in t078 |
| Sanchez-Vega pathways (referenced implicitly via TCGA PANCAN data) | `process_sanchez_vega_pathways.py` annotation | SLAPenrich uses broader Pathway Commons set; Sanchez-Vega is the pipeline's current pathway vocabulary for hypothesis:0004 |
| HCG driver removal → enrichment persists | Bailey driver overlay (`annotate_drivers.py`) [@Bailey2018] | Same logic: are enrichments beyond the canonical driver list meaningful? The pipeline flags drivers; this paper tests what survives their removal |
| Cancer-type-specific hallmark patterns (e.g. Warburg in GBM only) | Per-cancer-type mutation frequency matrix | Validates the cross-study aggregation approach; cancer-type specificity aligns with per-histology fitting in hypothesis:0004 |
| Pathway Alteration Index Δ(P) = log₁₀(O/E) | Gene/pathway mutation ratio (enrichment over background) | Conceptual analogue; the pipeline computes sample ratios, SLAPenrich computes cohort-level expected vs. observed |
| 10 TCGA cancer types (BRCA, COREAD, GBM, HNSC, KIRC, LUAD, OV, PRAD, SKCM, THCA) | cBioPortal study universe | These cancer types are all represented in the pipeline's cBioPortal studies |

## Limitations

- The pathway→hallmark mapping is human-curated and reflects current expert consensus, not an empirically derived partition. It can be seen as a prior that encodes existing beliefs; the paper's findings cannot independently validate the hallmark schema because the schema is an input.
- Pathway Commons v8 (2016) is the gene-set source; some pathways may be incomplete, misannotated, or have since been revised. The mapping is not updated automatically.
- The exclusive coverage filter (>50%) is a heuristic to suppress single-gene-dominated enrichments. It does not fully model mutual exclusivity — it only requires that the pathway's signal is not entirely explained by the most common alteration. A rigorous mutual exclusivity test (as in `paper:RaphaelVandin2015` or the DISCOVER framework) would be more principled.
- The Bernoulli model for per-sample pathway alteration probability assumes a uniform background somatic mutation rate across the genome (per-sample calibrated but not positionally varying). Regional mutation rate variation (e.g., late-replicating domains, transcription-coupled repair) is not modelled, which may inflate expected alteration counts for large pathways in genomically hypermutable regions.
- Sample sizes for some cancer types (PRAD n=242, OV n=316) are modest for pathway-level tests after conditioning on hallmark-specific pathway subsets.
- The analysis is limited to somatic point mutations and small indels; copy number alterations, structural variants, and gene expression changes are not incorporated, potentially missing a substantial fraction of hallmark-relevant alterations.
- The 10 TCGA cancer types do not include some important lineages (e.g., leukemia, hepatocellular, bladder, cervical), limiting the generalisability of the hallmark heterogeneity findings.
- The paper does not address statistical power formally; it is unclear whether the absence of significant enrichment for a hallmark in a cancer type reflects true biological absence or insufficient sample size.

## Model / Tool Availability

**SLAPenrich R package:** Available on GitHub at https://github.com/saezlab/SLAPenrich.
The package includes mutation data preprocessing, pathway curation routines, core enrichment analysis (Poisson-binomial statistics), mutual exclusivity filtering, core-component gene identification, and a visualisation/report framework for exploring enriched pathways.
The package is not on Bioconductor (as of the time of publication it was a standalone GitHub repository).
The curated 374 HMA pathway gene-sets and hallmark assignments are distributed as part of the package [@Iorio2018SLAPenrich].

## Follow-up

- **Immediate use: HMA gene-set extraction.** The SLAPenrich R package's curated HMA pathway collection (374 gene-sets → 10 hallmarks) should be extracted as a static gene-set table for use in the pipeline's post hoc hallmark annotation layer. This would allow enrichment of any data-driven module (from DISCOVER/WeSME/RaphaelVandin2015) against hallmark gene-sets without re-running the full SLAPenrich method.

- **Apply to pipeline's gene × cancer matrix.** Compute a SLAPenrich-style expected-vs-observed enrichment using the pipeline's per-cancer-type mutation ratio table: for each HMA pathway, sum the gene-level mutation ratios as a proxy for E[P], compare to O[P] (fraction of studies/samples with ≥1 pathway gene mutated). This would reproduce the paper's hallmark heterogeneity signature across the pipeline's broader study universe (including non-TCGA cBioPortal studies and GENIE).

- **Cross-validate against Sanchez-Vega pathway ordering.** If hypothesis:0004's per-histology MHN recovers an ordering of Sanchez-Vega pathways, one can ask whether that ordering is consistent with the hallmark acquisition order implied by the SLAPenrich CHS matrix — i.e., hallmarks with high CHS early in the recovered order should correspond to early-acquired biological capabilities (proliferation, genome instability), and those with low CHS or cancer-type-restricted enrichment should map to late events (immune evasion).

- **Test whether data-driven modules recapitulate hallmark partition.** Use the HMA gene-sets as the annotation overlay for the label-free module pipeline (`discussion:2026-06-07`): enrich each mutual-exclusivity module against all 374 HMA gene-sets, record the top hallmark annotations, and measure how cleanly each module maps to a single hallmark vs. spanning multiple. Clean single-hallmark modules support the canonical partition; diffuse or multi-hallmark modules suggest the partition is imprecise or that the module captures a functional unit not well-described by a single hallmark.

- **Warburg effect / GBM specificity.** The paper's finding that Warburg-effect pathway enrichment appears only in GBM (not other cancer types) is an operationally testable claim in the pipeline: compute mutation rates in the metabolic gene-sets (LDHA, PKM, HIF1A, etc.) across all cBioPortal cancer types and test whether GBM shows elevated rates relative to the population-level background. This would serve as a pipeline validation check.

- **COREAD immune evasion signal.** The strong immune evasion pathway enrichment in COREAD (but not other cancer types) is consistent with MSI-high CRC's distinctive immunogenic phenotype and response to checkpoint inhibitors. Within the pipeline, COREAD studies with matched hypermutator annotation (`is_hypermutator`) could be stratified to test whether the immune-evasion enrichment is entirely driven by MSI-H samples.

- **Identify which HMA pathways overlap the Sanchez-Vega 10-pathway gene universe.** A gene-set overlap table between SLAPenrich HMA gene-sets and Sanchez-Vega pathway genes would clarify which Sanchez-Vega pathways (RTK/RAS, Wnt, etc.) are represented within which hallmarks in the SLAPenrich framework, enabling a direct semantic bridge between hypothesis:0004's pathway-level MHN results and the hallmark-level annotation.
