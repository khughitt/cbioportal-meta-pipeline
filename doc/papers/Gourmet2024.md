---
id: "paper:Gourmet2024"
type: "paper"
title: "The temporal evolution of cancer hallmarks"
status: "active"
ontology_terms:
  - "cancer hallmarks"
  - "tumor evolution"
  - "variant allele frequency"
  - "dN/dS"
  - "clonal dynamics"
  - "genomic instability"
  - "immune evasion"
datasets:
  - "TCGA pan-cancer (2,626,225 mutations, 9,484 patients, 32 cancer types)"
  - "GTEx healthy tissues (999,203 mutations, 7,584 patients, 16 tissue types)"
source_refs:
  - "cite:Gourmet2024"
related:
  - "hypothesis:h04-mhn-pathway-ordering"
  - "question:q012-mutation-ordering-cross-sectional-inference"
  - "discussion:2026-06-07-hallmark-ordering-and-data-driven-modules"
  - "topic:co-occurrence-and-mutual-exclusivity"
  - "paper:RaphaelVandin2015"
created: "2026-06-07"
updated: "2026-06-07"
dataset_usage:
  - ref: "dataset:tcga-pan-cancer"
    role: "analyzed"
    overlap: "substantial — 32 cancer types, 9,484 primary tumors; overlaps cBioPortal TCGA studies"
  - ref: "dataset:gtex"
    role: "analyzed (healthy-tissue control)"
    overlap: "none — not in cBioPortal pipeline"
---

# The temporal evolution of cancer hallmarks

- **Authors:** Lucie Gourmet, Daniele Ramazzotti, Parag Mallick, Simon Walker-Samuel, Luis Zapata
- **Year:** 2024
- **Venue:** bioRxiv preprint (doi: 10.1101/2024.01.21.576566; also Research Square rs-5499335); posted January 23, 2024
- **DOI:** 10.1101/2024.01.21.576566
- **BibTeX key:** Gourmet2024
- **Source:** Full text PDF (local copy); all methods, figures, and quantitative results read directly from the paper.

## Key Contribution

This paper provides the first systematic inference of the temporal acquisition order of all ten canonical cancer hallmarks across 32 cancer types, using variant allele frequency (VAF) as a clonality proxy for timing and dN/dS as a selective-advantage proxy. The key finding is a common evolutionary trajectory in 27 of 32 cancer types: **genomic instability and replicative immortality are acquired first; inflammation and immune evasion are acquired last**. The ordering is cancer-specific (healthy GTEx tissues show no corresponding order), all hallmarks are under positive selection in cancer (dN/dS > 1) and negative selection in healthy tissues (dN/dS < 1), and patient-level clustering reveals two prognostically distinct groups defined by whether genomic instability is acquired early or late.

## Methods

### Hallmark gene-set source

Hallmark gene sets were obtained from **Zhang et al. 2020** (the CHG — Cancer Hallmark Genes — database; ref. 11 in the paper: Zhang D et al., Front Genet 2020), filtered to match HGNC gene nomenclature. Two additional gene categories were included as comparative controls: "escape" genes (immune-evasion drivers from Zapata et al. 2023) and "driver" genes (365 cancer driver genes under positive selection from Martincorena et al. 2017). The ten hallmarks with their shorthand names used in the paper are:

| Canonical hallmark | Shorthand |
|---|---|
| Sustained proliferative signalling | proliferation |
| Evading growth suppressors | growth |
| Resisting cell death | death |
| Inducing angiogenesis | angiogenesis |
| Activation of invasion and metastasis | metastasis |
| Enabling replicative immortality | immortality |
| Avoiding immune destruction | immune evasion |
| De-regulation of cellular energetics | metabolism |
| Genome instability and mutation | genome instability (GI) |
| Tumour promoting inflammation | inflammation |

Gene-set sizes: angiogenesis 478 genes; growth 522; metastasis 1,072; metabolism 429; genome instability 211. The hallmarks with the smallest unique gene sets were metabolism (59% gene sharing with others) and genome instability (41% gene sharing). Less than half (42%; 152/365) of known cancer driver genes were associated with any specific hallmark.

### Order statistic: VAF as clonality proxy

**VAF (variant allele frequency) of nonsynonymous somatic point mutations** is used as the primary timing proxy, operationalized as: higher mean VAF across a hallmark's gene set = earlier (more clonal) acquisition. This directly exploits the evolutionary logic that early mutations are present in a larger fraction of tumor cells and thus detected at higher frequency than later, subclonal mutations.

Only nonsynonymous mutations (Missense, Nonsense, Essential Splice, Stop loss) were retained. For each hallmark, mean VAF and standard error were computed across all mutations in hallmark-associated genes, aggregated per cancer type and pan-cancer. Hallmarks were ordered from high VAF (early) to low VAF (late).

The analysis does **not** use patient age as an order proxy. This is an important design choice: the paper explicitly frames VAF as a within-lineage clonality measure, not an epidemiological association.

A secondary metric — **cancer cell fraction (CCF)**, which corrects for tumor ploidy and purity using the formula CCF = (VAF/mp) × (pN + 2 × (1-p)) — was also computed and used in sensitivity analyses. When CCF replaced VAF, genomic instability shifted to a middle position while immune evasion remained last, suggesting that ploidy correction partially confounds the genomic instability signal.

### Order statistic: dN/dS as selective-advantage proxy

The **ratio of nonsynonymous to synonymous mutations (dN/dS)** was computed per hallmark using the **dNdScv R package (v0.0.1.0)**, providing the global dN/dS output from the gene list for each hallmark. Values > 1 indicate positive selection; values < 1 indicate negative (purifying) selection. Hallmarks were ranked from highest dN/dS (strongest positive selection) to lowest.

VAF and dN/dS orderings were significantly correlated pan-cancer (Spearman ρ = 0.806, p = 0.008) but not in normal tissues (ρ = 0.103, p = 0.785). Combining VAF and dN/dS into a single integrated metric produced inconsistent results (metastasis ranked first), so the paper treats them as complementary rather than combining them.

### Dataset

- **Cancer:** TCGA pan-cancer dataset via GDC portal — **2,626,225 mutations across 9,484 patients from 32 cancer types**; metastatic samples and duplicates excluded; primary tumors only.
- **Healthy tissue control:** GTEx pantissue dataset — **999,203 mutations across 7,584 patients from 16 tissue types** (adipose, adrenal, brain regions, breast, colon subtypes, coronary artery, aorta, artery tibial). TCGA data were annotated using the dNdScv annotation pipeline.

### Trajectory analysis across cancer types and patients

Inter-tumor consistency was assessed by computing the mean hallmark VAF rank for each cancer type, then computing all-vs-all Pearson correlation across tumor types (Fig. 2a). The **ASCETIC algorithm** (Fontana et al. 2023, Nat Commun — an evolutionary algorithm that infers ordering from gene-group binary matrices with CCF/VAF timing input) was applied as a complementary method to confirm the VAF-based ordering (Fig. 2b). ASCETIC uses 100 resampling iterations.

Patient-level clustering was performed by computing mean hallmark VAF ranks per patient (patients with data for at least 8 of 10 hallmarks retained), followed by PCA and k-means clustering (elbow method; optimal k = 2). Cluster prognostic value was assessed with Kaplan-Meier analysis of overall survival (OS), progression-free survival (PFS), and disease-free survival (DFS).

Smoking-status stratification was performed for LUAD and LUSC using available clinical metadata (current smoker, non-smoker, reformed smoker).

### Randomization and robustness controls

- Synonymous-only control: analysis repeated with synonymous mutations only to check for neutral drift (VAF is significantly higher for hallmark genes than for synonymous controls; Supplementary Fig. 3).
- Diploid-only control: restricts to ploidy = 2 tumors; results are similar (Supplementary Fig. 2).
- TP53 removal: hallmark gene lists re-run without TP53 — genome instability shifts to last position, suggesting early GI is predominantly driven by TP53.
- Pseudo-hallmark randomization: hallmark gene labels randomly shuffled 100× to validate that the ordering is not an artifact of gene-set sizes or mutation biases (Supplementary Fig. 19).
- Genes-under-positive-selection only: analysis restricted to genes with significant dN/dS > 1; genomic instability remains first, inflammation and immune evasion remain last (Supplementary Fig. 5).

## Key Findings

### 1. Pan-cancer hallmark ordering by VAF (clonality)

The pan-cancer ordering, from earliest (highest mean VAF) to latest (lowest mean VAF), is:

| Rank | Hallmark | Mean VAF ± SE |
|---|---|---|
| 1 | Genome instability | 0.3272 ± 0.001 |
| 2 | Replicative immortality | 0.3196 ± 0.001 |
| 3 | Metabolism | 0.3123 ± 0.0008 |
| 4 | Evading growth suppressors | 0.3081 ± 0.0007 |
| 5 | Angiogenesis | 0.3080 ± 0.0008 |
| 6 | Resisting cell death | 0.2967 ± 0.0005 |
| 7 | Metastasis | 0.2964 ± 0.0004 |
| 8 | Proliferative signalling | 0.2961 ± 0.0004 |
| 9 | Inflammation | 0.2888 ± 0.0007 |
| 10 | Immune evasion | 0.2883 ± 0.0007 |

Healthy GTEx tissues display no clear ordering: VAF estimates for 6 of 10 hallmarks overlap.

### 2. Selective advantage ordering by dN/dS

All ten hallmarks in cancer exhibit dN/dS > 1 (positive selection). The two hallmarks with the strongest positive selection are:
- Genome instability: dN/dS = 1.340, 95% CI [1.295, 1.387]
- Replicative immortality: dN/dS = 1.361, 95% CI [1.327, 1.396]

In healthy tissues, all hallmarks show dN/dS < 1 (negative/purifying selection):
- Replicative immortality: dN/dS = 0.287, 95% CI [0.275, 0.300]
- Genome instability: dN/dS = 0.456, 95% CI [0.442, 0.471]

After the top two, the dN/dS-based ordering places: metabolism, angiogenesis, growth evasion, death resistance, inflammation, proliferation, and finally metastasis.

### 3. Common trajectory across 27 of 32 cancer types

The Pearson correlation heatmap of hallmark VAF ranks shows that most cancer types share a common trajectory. Five cancer types showed deviations: **uveal melanoma, thymoma, thyroid carcinoma, skin cutaneous melanoma, and pheochromocytoma/paraganglioma**. After multiple testing correction, nine cancer types did not share the common trajectory.

When using the ASCETIC algorithm (which operates on binary hallmark presence matrices + CCF/VAF timing, applied at the gene-group level), most tumor types followed a similar acquisition order (Fig. 2b), independently confirming the VAF-based result.

### 4. Melanoma exception

Skin cutaneous melanoma and uveal melanoma consistently deviated from the common trajectory. The authors interpret this as evidence that strong environmental mutagens (UV light exposure) disrupt the common evolutionary path. Smoking-status analysis in LUAD and LUSC showed that environmental exposures modulate VAF profiles: LUAD former smokers had a significantly higher overall VAF across all hallmarks except genome instability compared to non-smokers and current smokers (Fig. 2d), suggesting a clonal sweep driven by modification of metabolism, growth capacity, and angiogenesis. The pair with the most divergent trajectories was LUAD current smokers vs. LUSC non-smokers. LUSC overall followed a pan-cancer-similar trajectory (R_s = 0.94 vs. pan-cancer).

### 5. TP53 drives early genomic instability positioning

When TP53 is excluded from all hallmark gene lists, genome instability shifts to the **last** position in the ordering, while most other hallmarks are unaffected (Supplementary Fig. 9). This demonstrates that the early positioning of genomic instability is predominantly driven by TP53 mutations, which are clonal (high VAF) and ubiquitous across cancer types. The genes under significant positive selection within the genome instability hallmark include ATM, CASP8, TP53, and PTEN; for immune evasion, PIK3R1 and HLA genes are among the most positively selected.

### 6. Two patient clusters with differential prognosis

At the patient level, PCA of per-patient hallmark VAF ranks reveals that **genomic instability (GI), immune evasion, and inflammation** are the primary features separating patients into two clusters (Fig. 3c-d):

- **Cluster 1 (early GI):** Genomic instability acquired early → **poorer prognosis** (worse overall survival, PFS, and DFS; log-rank p = 0.00096 for OS, p < 0.0001 for PFS and DFS).
- **Cluster 2 (late GI):** Genomic instability acquired later → **better prognosis**.

The genomic instability hallmark showed a markedly dichotomous pattern: it was predominantly ranked either 1st or last in individual patients, and this bimodality depended largely on the presence/absence of TP53 mutations (Supplementary Fig. 15-16). Approximately half of patients with a ranked GI hallmark had that ranking driven by a TP53 mutation.

Patients were distributed roughly evenly across clusters pan-cancer, with notable exceptions in BRCA, HNSC, LUSC, and OV, which showed skewed cluster membership.

When ASCETIC-based clustering with 6 clusters was used (Supplementary Fig. 17), prognostic differences were also observed.

### 7. Cancer-specificity of the ordering

The temporal ordering is **absent in healthy tissues**: the ordering in cancer and healthy tissues is not significantly correlated by either dN/dS (Spearman ρ = 0.382, p = 0.279) or VAF (ρ = 0.309, p = 0.387). This cancer-specificity supports the interpretation that the ordering reflects genuine tumor-selective forces, not constitutive biology.

## Relevance

This paper is the **direct prior art and external calibration target** for hypothesis `h04-mhn-pathway-ordering` and the primary empirical reference for `discussion:2026-06-07-hallmark-ordering-and-data-driven-modules`.

**(a) External calibration for h04's predicted ordering.**
h04 predicts that per-histology MHN fits will recover an "intrinsic mutators → lineage drivers → checkpoint/immune-late" order. Gourmet et al. provide exactly that at the hallmark grain: genome instability and immortality are first, immune evasion and inflammation are last, across 27/32 cancer types. This is the hallmark-level echo of h04's pathway-level prediction: the "intrinsic-instability-early → checkpoint/immune-late" ordering is confirmed in the largest cross-cancer VAF analysis to date.

**(b) Clonality + selection as the correct order proxy, validating the discussion's pushback on age.**
The paper uses VAF (clonality) and dN/dS (selective advantage) as the order proxy — precisely the combination that `discussion:2026-06-07` advocated and that q012 adopted as the methodological standard. Patient age is not used anywhere in the analysis. This is a direct methodological parallel: the project should use clonality-based ordering (via VAF/CCF or MHN), not patient age, as the primary ordering signal.

**(c) Trajectory clustering corresponds to the project's cancer-type clustering interest.**
The inter-tumor Pearson correlation heatmap (Fig. 2a) and patient-level k-means clustering (Fig. 3b-d) correspond to the project's interest in "clusters of cancer types with coherent ordering" (discussion). The melanoma exception (environmental disruption of common path) is particularly relevant: cBioPortal TCGA skin/uveal melanoma data would be expected to show the same deviation, providing a built-in falsification check for any ordering model.

**(d) Confounders the project faces that Gourmet et al. may not fully address:**

1. **Cross-sectional under-identification.** The VAF-ordering approach inherits the same fundamental limitation as MHN: a higher mean VAF is consistent with both "acquired earlier in the lineage" and "under stronger clonal selection regardless of order." The paper does not formally test these alternatives; it interprets VAF as a timing proxy without modeling the selection-vs-timing confound. The project's use of MHN (which explicitly models hazard rates) is methodologically stronger for directed ordering claims.

2. **Clonal hematopoiesis (CH) contamination.** In non-matched-normal TCGA studies, CH-contaminated mutations in DNMT3A, TP53, TET2, ASXL1, PPM1D would inflate VAF for genome instability and related hallmarks — potentially amplifying the "genomic instability first" signal artificially. The paper does not apply a CH filter. This is a direct concern for the cBioPortal pipeline's `t087` CH-aware annotation and `matched_normal_studies` config list.

3. **Panel callability.** GTEx uses RNA-seq-derived mutation calls; TCGA uses WES. The paper does not address panel callability corrections. For the project's mixed-panel GENIE data, the same callability mask required for t078 must be applied before hallmark-level ordering.

4. **Hypermutator tumors.** Hypermutator/MSI-H/POLE-driven tumors accumulate mutations throughout the genome at elevated rates. These tumors would have genome-instability-hallmark genes mutated at high VAF simply because of elevated mutation rate, not because GI was acquired early in a causal sense. The paper does not apply a hypermutator stratification filter (analogous to the project's t081). This is the most likely source of residual confounding in their GI-first result.

5. **TP53 dominance.** The paper's own sensitivity analysis shows that removing TP53 moves genome instability to last place. This raises the question of whether the "GI first" result reflects a genuine hallmark ordering or is driven by TP53's ubiquity and high clonality as a tumor suppressor loss-of-function event — which occurs across multiple hallmark categories (TP53 is listed in 8 of 10 hallmarks). The project's analysis would need to consider this carefully.

6. **Per-histology pooling.** The pan-cancer ordering pools all 32 cancer types before computing mean VAF. Type-specific findings (melanoma, thymoma exceptions) emerge only in the correlation heatmap. The project's per-histology approach avoids the Simpson's-paradox risk of pooling.

7. **CCF vs. VAF discordance.** Using CCF (ploidy-corrected) moves GI to a middle position, while VAF places it first. This discordance suggests that the GI-first result is sensitive to copy-number/ploidy status — a known source of technical confounding. The project should replicate both metrics when VAF data are available.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| VAF of nonsynonymous mutations as timing proxy | Clonality-based ordering (q012); t133 VAF audit | Same principle; project auditing VAF retention across cBioPortal studies |
| dN/dS (dNdScv) as selective advantage | Positive-selection annotation; Bailey 2018 driver overlay | dNdScv used in both; per-hallmark vs. per-gene grain |
| Hallmark gene sets from Zhang et al. 2020 (CHG) | Sanchez-Vega 2018 10-pathway annotation (current pipeline) | Different gene-set sources; project uses pathway layer, not hallmark layer directly |
| Common ordering in 27/32 cancer types | h04 prediction of intrinsic-mutator-early ordering | Direct calibration target; project would test at pathway grain per histology |
| Melanoma exception (UV mutagenesis) | Per-histology stratification; SBS7 signature group | Signature-stratified ordering (t111) expected to show same deviation |
| 2 patient clusters (early vs. late GI) | Cancer-type or patient clustering by mutation profile | Project interest in coherent ordering clusters across cancer types |
| Dichotomous GI position (ranked 1 or last) | TP53 clonality signal; CH contamination risk | TP53 dominant role; in non-matched-normal studies CH TP53 inflates GI rank |
| dN/dS > 1 in cancer, < 1 in healthy tissue | Positive selection in cancer vs. normal tissue | Validates hallmark gene sets as under genuine positive selection |
| ASCETIC algorithm (evolutionary trajectory inference) | MHN (h04); PLPM (RaphaelVandin2015) | ASCETIC is an alternative trajectory method; paper uses it as cross-validation |
| CCF (ploidy-corrected allele frequency) | VAF in pipeline; t133 VAF/CCF availability | CCF discordance with VAF is a methodological caution for the project |
| Healthy tissue (GTEx) negative control | Normal-tissue contamination concern (q001/q005) | Paper uses GTEx as external control; project removes contaminated samples |
| No hallmark ordering in healthy tissues | Cancer-specificity of driver ordering | Supports that any ordering recovered in TCGA/GENIE is tumor-biology signal |
| Randomization (pseudo-hallmark) control | Bootstrap / leave-one-study-out (h04 falsifiability) | Paper validates ordering is not a gene-set-size artifact; project would use leave-one-study-out |

## Limitations

- **VAF as clonality is confounded with selection strength.** A mutation that is clonally fixed (high VAF) could be early, or could simply be under very strong positive selection. The paper does not formally distinguish these alternatives. dN/dS is offered as a complementary selection-strength measure, but the ordering of the two metrics is inconsistent (Spearman ρ = 0.806 pan-cancer, but breaks down per-cancer-type), and combining them yields a different order entirely. The ordering should be interpreted as "clonal + selected" rather than purely temporal.

- **TP53 dominance confounds genome instability.** Removing TP53 from the analysis moves GI from first to last. Given that TP53 is present in 8 of 10 hallmark gene sets, the genome-instability-first result may largely reflect TP53's ubiquity as a clonal, highly selected driver rather than a general property of the GI hallmark. The paper acknowledges this but does not fully resolve it.

- **No hypermutator stratification.** MSI-H, POLE/POLD1-mutant, and other hypermutator tumors accumulate hallmark-gene mutations at elevated rates throughout tumor evolution. Including these tumors without stratification can inflate VAF for multiple hallmarks simultaneously and create spurious ordering artifacts. The project's t081 hypermutator annotation would be required before applying this logic to cBioPortal data.

- **No CH contamination filter.** In non-matched-normal sequencing (a substantial fraction of TCGA studies), clonal hematopoiesis-derived mutations in TP53, DNMT3A, TET2, ASXL1, PPM1D inflate VAF of the genome instability and other hallmarks in blood-contaminated tumor samples. This is a direct confounder for the GI-first result.

- **CCF discordance.** The CCF-based analysis moves GI to a middle position; the paper does not explain or reconcile this discordance beyond noting it in supplementary materials. The project should treat the raw-VAF and CCF results as providing different signals (tumor purity-corrected clonality vs. raw allele depth), not as redundant confirmations.

- **Cross-sectional design.** The entire analysis is cross-sectional: each patient contributes a single snapshot. VAF-based ordering assumes that high-VAF = early event, but this holds cleanly only under a simple linear progression model with no parallel evolution or subclonal sweeps. The paper does not formally test this assumption against within-patient longitudinal data.

- **Hallmark gene-set label dependency.** Results depend on the Zhang et al. 2020 (CHG) gene-set assignments. The paper notes that AKT, Ras, PIK3, and MAPK gene families appear in 9 of 10 hallmarks; BRAF in 7/10; TP53 in 8/10. Such multi-membership means that the VAF for different hallmarks is not independent — the ordering partly reflects shared gene membership, not independent biological processes. The 41% gene sharing for genome instability (87/211 genes shared with other hallmarks) is the lowest of any hallmark, making GI somewhat more separable.

- **Preprint status.** This is a bioRxiv preprint (January 2024); it has not been peer-reviewed. Quantitative findings should be treated with appropriate uncertainty until publication.

- **No code or data repository linked.** The methods describe use of standard R packages (dNdScv, ggplot2, pheatmap, UpSetR, cluster, factorextra) but no analysis code repository or processed data repository is referenced in the paper.

## Model / Tool Availability

The paper does not release a standalone software tool. All analyses use existing R packages:

- **dNdScv** (v0.0.1.0) — dN/dS calculation; CRAN/Bioconductor, open source
- **ASCETIC** — evolutionary trajectory algorithm from Fontana et al. 2023 (Nat Commun); available via GitHub (caravagnalab/ASCETIC)
- **CHG database** (Zhang et al. 2020, Front Genet) — hallmark gene sets; publicly available
- Standard R: ggplot2, pheatmap, UpSetR, prcomp, kmeans, silhouette (cluster package), fviz_nbclust (factorextra)

No processed VAF tables, hallmark gene-assignment matrices, or cluster membership files are deposited in a public repository in the preprint.

## Follow-up

- **Use as calibration for h04.** When the project's per-histology MHN pathway ordering is computed (task t135), compare the recovered pathway-level ordering against the Gourmet et al. hallmark ordering by mapping Sanchez-Vega pathways to their corresponding hallmarks. The expected calibration check: MMR/POLE (genome instability pathway) orders early; immune checkpoint pathways order late. Deviation from this in ≥ 5 of the common cancer types would argue against h04 or flag a confound.

- **Replicate TP53 sensitivity analysis.** Before treating h04's predicted "intrinsic-instability-first" result as confirmed, replicate the paper's TP53-removal sensitivity test using cBioPortal data: does the GI pathway (or TP53 specifically) dominate the early ordering, and if so, does the ordering collapse when TP53 is excluded? This directly tests whether the GI-first result is a TP53-driven artifact vs. a genuine hallmark signal.

- **Apply hypermutator filter before any hallmark-level VAF analysis.** The project's t081 hypermutator annotation should be applied before any VAF-based hallmark ordering replication; the paper's omission of this filter is the most likely single confounder to address.

- **CH filter for non-matched-normal studies.** The project's `ch_priority_gene` flag (Bolton 2020 7-gene list) and `matched_normal_studies` config should be used to flag or exclude CH-contaminated mutations before hallmark-level VAF calculations, especially for TP53 (in GI) and DNMT3A/TET2 (which appear in metabolism/epigenetic hallmarks).

- **Obtain CHG gene sets (Zhang et al. 2020).** For a direct comparison between the paper's hallmark-level result and the project's Sanchez-Vega 10-pathway result, download the CHG database gene sets and cross-map them to the Sanchez-Vega pathways. This defines the hallmark-to-pathway bridge for calibration.

- **Examine ASCETIC as an alternative to MHN.** The ASCETIC algorithm (Fontana et al. 2023, Nat Commun 14:5982) is used in the paper as a cross-validation trajectory method operating on binary hallmark-presence matrices with CCF/VAF timing. It is an alternative to MHN for ordered progression inference and may be worth comparing against MHN for the project's module-ordering step (h04/q012). The ASCETIC GitHub is caravagnalab/ASCETIC.

- **Assess the 2-cluster patient stratification in cBioPortal data.** The paper's finding that early vs. late GI acquisition predicts prognosis is clinically actionable and directly testable in cBioPortal data. If VAF is available (t133 audit), compute per-patient hallmark VAF ranks and reproduce the 2-cluster PCA. A concordance check against the Gourmet et al. cluster assignments (using TCGA overlap samples) would validate both the method and the prognostic signal.

- **Read Fontana et al. 2023 (ASCETIC).** This is reference 24 in the paper (Nat Commun 14:5982, doi: 10.1038/s41467-023-41507-1) — the ASCETIC evolutionary-trajectory algorithm used as a cross-validation tool. It is directly relevant to q012's "which ordering method" question and complements MHN in the trajectory inference landscape.

- **Read Zhang et al. 2020 (CHG database).** Reference 11 (Front Genet 2020 Feb 5;11) — the source of the hallmark gene sets. Comparing CHG against Sanchez-Vega 2018 and against COSMIC cancer gene census would establish which curated gene-set framework is most appropriate for the project's hallmark-level annotation layer.
