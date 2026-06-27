---
type: paper
title: Unsupervised Identification of Cancer Attractor States through the Lens of
  Embryonic Origin and Cancer Hallmarks
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: paper:Deshpande2026
ontology_terms:
- hallmarks of cancer
- embryological origin
- attractor states
- unsupervised clustering
- somatic mutation
- metastasis
datasets:
- dataset:msk-met
source_refs:
- cite:Deshpande2026
related:
- discussion:0007-hallmark-ordering-and-data-driven-modules
- hypothesis:0004-mhn-pathway-ordering
- topic:co-occurrence-and-mutual-exclusivity
dataset_usage:
- ref: dataset:msk-met
  role: analyzed
  overlap: partial
---

# Unsupervised Identification of Cancer Attractor States through the Lens of Embryonic Origin and Cancer Hallmarks

- **Authors:** Prashant Deshpande, Prabal Deb, Ibrahim Al Haddabi, Boris Itkin
- **Year:** 2026
- **Venue:** bioRxiv preprint (posted January 14, 2026)
- **DOI:** 10.64898/2026.01.13.699215
- **Institution:** Department of Clinical Laboratories, Sultan Qaboos Comprehensive Cancer Care and Research Center, University Medical City, Muscat, Oman
- **BibTeX key:** Deshpande2026
- **Source:** Full text PDF (local); all methods and results verified from primary text.

## Key Contribution

This paper introduces an **EO/HRM framework** that integrates **embryological origin (EO)** — a coarse five-group proxy (ectoderm, mesoderm, endoderm [foregut/midgut/hindgut/urogenital], neural crest, yolk sac) for the inherent cellular gene-regulatory network — with **hallmark-related mutations (HRM)** — binary per-hallmark involvement flags derived from COSMIC-annotated somatic variants — to perform unsupervised clustering across 25,775 pan-cancer tumor samples in the MSK-MET database. The clustering (Jaccard-distanced t-SNE + K-means; optimal K selected by the elbow method) identifies **11 stable pan-cancer "attractor states"** (EO/HRM model) that are interpreted as stable functional basins in the Waddington epigenetic landscape. The central claim is that adding embryological origin as a feature — even at this coarse organ-level grain — significantly enhances cluster stability (ARI: 0.74 vs. 0.70 for HRM-only) and prognostic performance (C-index: 0.59 vs. 0.56 for HRM-only) relative to using HRM profiles alone.

## Methods

### Dataset

The **MSK-MET database** (Nguyen et al. 2022, *Cell* 185:563) was downloaded from cBioPortal. It contains mutation profiles for 25,775 primary and metastatic tumors sequenced with the MSK-IMPACT targeted panel. SNVs, indels, and fusion-generating structural variants (both partner genes included) were retained. Non-fusion structural variants and copy number variations were excluded.

### Hallmark annotation (HRM construction)

Fifteen hallmarks from the 2022 *Cancer Discovery* hallmarks update were used:
invasion/metastasis, evading growth suppressors (growth suppression), proliferative signaling, angiogenesis, dysdifferentiation, genomic regulation, energetics, genomic instability, escaping cell death, cell division control, inflammation, replicative immortality, senescence, escaping immune response, and pathogen response.

Genes associated with each hallmark were extracted from the **COSMIC** database (Catalogue of Somatic Mutations in Cancer; last accessed July 2025). Because TP53 maps to 13/15 hallmarks in COSMIC, TP53 variants were separated into a standalone 16th binary feature (total feature space: 16 HRM indicators). A hallmark was flagged as "involved" if at least one variant fell in any hallmark-associated gene for that sample. This is a **binary per-sample, per-hallmark indicator** — no mutation-count or burden component. The full gene-to-hallmark mapping is in supplementary table S1.

### Embryological origin (EO) encoding

Each cancer type was assigned an embryological origin (supplementary table S2). The subgroups are: ectoderm, mesoderm, endoderm (foregut, midgut, hindgut, urogenital sinus), neural crest, and yolk sac. EO was one-hot encoded as binary indicator columns, concatenated to the HRM feature vector for the EO/HRM model.

### Clustering pipeline

1. **Input feature matrix:** binary HRM (16 features) ± one-hot EO columns.
2. **Dimensionality reduction:** Jaccard-distanced t-SNE to 2D. Jaccard distance was chosen over Euclidean because it focuses on shared positive features in sparse binary vectors, avoiding distortion from joint absences.
3. **Clustering:** K-means on the 2D t-SNE coordinates; optimal K determined by the elbow method (Within-Cluster Sum of Squares) plus qualitative separation assessment.
4. **Cluster assignment for new samples:** Random Forest classifiers trained on the training subset (n=16,496); validated on validation set (n=4,124); applied to test set (n=5,155). Classifier accuracy and recall exceeded 99% in validation.
5. **Robustness:** bootstrap resampling (100 iterations) and 5-fold stratified cross-validation; metrics included ARI, sample stability, Silhouette score, Davies-Bouldin index, Calinski-Harabasz index, C-index, AIC, log-rank p-value.
6. **Generalizability test:** re-clustering cross-validation — clusters re-derived in each training fold; new samples assigned by nearest-centroid.

### Survival analysis

Kaplan-Meier overall survival (OS) curves; log-rank test; Cox proportional hazards regression (univariate and multivariate). Software: SPSS v29.0.0.0 and Python 3 (scikit-learn, Matlab, SciPy).

### Metastasis analysis

Organ-specific metastasis rates modeled with logistic regression; cluster vs. histological subtype compared at AUC; multivariate logistic regression controlling for cancer subtype.

## Key Findings

### HRM prevalence

HRMs were detected in 24,615/25,775 (95.5%) of tumors. Most ubiquitous pan-cancer HRMs: invasion/metastasis (88.1%), escaping cell death (87.8%), dysdifferentiation (84.4%), and signaling (83%). Least common: pathogen response (14.6%) and immune response (47.4%). TP53 variants present in 48.1% of tumors.

HRM patterns varied strongly by histology — different tumors from the same organ can have divergent HRM landscapes (e.g., pancreatic adenocarcinoma vs. pancreatic neuroendocrine neoplasms have similar TMB [3.45 vs. 2.5 mut/Mb] but divergent HRM profiles). Tumors sharing etiology (HPV-related anal vs. cervical SCC) showed similar HRM profiles across 15/16 hallmarks.

### Prognostic significance of individual HRMs

Univariate Cox regression: 14/16 HRMs showed significant associations with OS (not significant: cell division control and escaping immune response). Nearly all HRMs associated with inferior survival, except pathogen response (HR: 0.804, p<0.001 — improved survival, possibly reflecting MSI-H-like immune responsiveness). Patients with no HRM had significantly longer OS than those with HRM (median OS: 58.97 vs. 40.08 months; log-rank p<0.001; HR: 0.827, 95%CI: 0.764–0.895). Leave-one-out analysis confirmed that most hallmark groups retained prognostic value even after removing their dominant gene (e.g., KRAS in angiogenesis, energetics, inflammation).

### Model comparison: EO/HRM vs. HRM-only

| Metric | EO/HRM | HRM-only |
|---|---|---|
| Clusters identified | 11 | 12 |
| ARI (bootstrap stability) | 0.7426 | 0.7011 |
| Sample stability | 0.1989 | 0.1798 |
| Silhouette score | -0.0262 | 0.18 |
| Calinski-Harabasz index | 1306.86 | 3158.63 |
| C-index (full dataset) | 0.5917 | 0.5649 |
| AIC | 192,719.17 | 193,165.76 |
| Clusters with significant OS | 11/11 | 8/12 |
| Mean C-index (5-fold CV) | 0.5907 ± 0.0080 | 0.5640 ± 0.0054 |
| Mean C-index (re-clustering CV) | 0.5742 ± 0.0079 | 0.5628 ± 0.0047 |

Interpretation: HRM-only had tighter geometric clusters (higher Silhouette, higher Calinski-Harabasz); EO/HRM had superior cluster stability and prognostic performance. All 11 EO/HRM clusters showed statistically significant survival associations vs. only 8/12 for HRM-only.

### Biological characteristics of selected clusters

- **C5 (genomically quiescent):** Lowest TMB (median: 2 mut/Mb; TMB-High: 0%), lowest FGA (0.024). Composed of LUAD, PAAD, IHCA, GIST subgroups — identified the quiescent subset within each of these histologies. Predominantly foregut embryological origin (86.8%).
- **C10 (hyper-unstable):** Highest TMB (median: 9 mut/Mb; TMB-High: 22.5%), highest FGA (0.267). Composed of cutaneous melanoma and GIST subgroups. 99.9% neural crest embryological origin. GIST tumors in C10 had the highest TMB among all GIST clusters (median 2.9 mut/Mb vs. 0–2.6 in other clusters; p<0.001).
- **C6 (TP53-minimalist attractor):** Dominated by TP53 alterations (41.0%) with near-complete absence of other HRMs (<4% in 15/16 categories). Lowest TMB (median: 0 mut/Mb; TMB-High: 0%) and lowest MSI-H frequency (0.1%). Histologically: high-grade serous ovarian carcinoma (HGSOC), prostate carcinoma (PRCA), breast invasive ductal carcinoma (IDC), and colon adenocarcinoma (COAD). Favorable prognosis in PRCA and trend toward improved survival in HGSOC and IDC.
- **C1 and C3:** Highest MSI-H frequencies (10.4% each), high TMB-H (11.2% and 14.7%), moderate FGA (0.158 and 0.115).

### Metastatic patterns

Among 15 major cancer types (≥400 patients each), cluster C1 had the highest global metastatic disease prevalence (90.9%); C3 the lowest (71.9%). Cluster assignments predicted metastatic status with AUC 0.68 vs. 0.67 for histology alone; multivariate models showed C10, C7, C5, C4 retained independent predictive capacity (OR: 2.1, 1.7, 0.78, 1.6; p<0.05). Specific organ-site models: C10 was independently associated with lung, liver, and bone metastases (OR: 1.7, 2.0, 1.8; p<0.05); C4 with brain metastases (OR: 1.3; p=0.002); C5 and C8 with reduced risk of lymph node, brain, and liver metastases.

**Prognostic inversions across histologies:** Cluster C0 was associated with favorable prognosis in LUAD, PAAD, and IHCA but poorest outcomes in prostate carcinoma (median OS: 29.6 months). Cluster C6 showed significantly superior outcomes in prostate carcinoma (median OS not reached vs. 29.6 months for C0). Cluster C7 conferred high metastasis risk in HGSOC and GIST but was protective in renal clear cell carcinoma (metastatic prevalence 73% vs. 89% in C3). These context-dependent inversions are interpreted as evidence that attractor state behavior is gated by the embryological landscape.

## Relevance

### 1. Label-free vs. semi-supervised — the key epistemological point for this project

This paper occupies an intermediate position between fully label-free and fully supervised. The **clustering step is genuinely unsupervised** (t-SNE + K-means with no class labels), but the **input features are not label-free**: every sample is first projected into a 16-dimensional HRM binary vector using a human-curated hallmark-to-gene mapping from COSMIC. The hallmark labels therefore enter at feature-construction time, not at the clustering step.

For the project's stated goal of inferring hallmark-like structure "from data, not labels" (`discussion:0007-hallmark-ordering-and-data-driven-modules`), this paper provides an important contrast: the clustering recovers "attractor states" that are guaranteed to be expressible in terms of the 16 input hallmarks — it cannot discover a structure that cuts across those hallmarks or that groups genes in a biologically different way. In the language of the discussion, the human labels are an *input*, not a *post-hoc annotation*. The paper explicitly does not answer the question "do data-driven modules recapitulate the canonical hallmark partition or carve the space differently?" — that would require a fully label-free module-discovery step (as in RaphaelVandin2015 or the project's t078/WeSME approach) followed by post-hoc annotation against hallmark gene sets.

That said, the paper does provide something genuinely useful for the project: a demonstration that **binary hallmark-involvement vectors on cBioPortal-adjacent panel data (MSK-IMPACT) yield stable, prognostically meaningful pan-cancer clusters** — validating the feature engineering approach for the project's own data, even if the label-free question remains open.

### 2. EO integration and the per-histology framing

The EO component is the paper's most original methodological contribution. Rather than using raw histological labels (which would trivially separate cancer types), the authors use **embryological germ-layer origin** as a proxy for the underlying GRN "topography." The five-group EO encoding is coarser than histology but captures a conserved developmental constraint shared across organ systems — the claim being that tumors sharing a germ-layer origin share latent GRN structure that modulates how somatic mutations are selected.

For the project, this is directly relevant to the **mandatory per-histology framing** as a principled justification. The prognostic inversions (C0 favorable in lung/pancreas/liver but unfavorable in prostate; C6 favorable in prostate) demonstrate that the same genomic attractor state has opposite clinical consequences depending on the cell-of-origin context — exactly the Simpson's-paradox-type problem the project must address by conditioning all analyses on histology. The paper shows that even a coarse EO proxy (5 groups) is enough to qualitatively improve cluster stability and prognostic utility over HRM alone (EO/HRM ARI 0.74 vs. HRM-only 0.70; C-index 0.59 vs. 0.56 across 5-fold CV). **EO/HRM beats HRM-alone on stability and survival concordance** in all reported comparisons — the advantage is modest but consistent across bootstrap (100 iterations) and 5-fold CV.

For the project's potential oncofetal/embryonic-origin extension, the specific EO subgroups used (foregut-dominated C5, neural-crest-dominated C10) are directly interpretable and suggest that germ-layer partitioning could be incorporated as a stratification covariate in the project's per-histology analyses.

### 3. Attractor states — structure, not temporal ordering

The "attractor states" in this paper are **static phenotypic clusters**, not a temporal or progression model. The paper does not claim or infer any ordering among C0–C10. No method (MHN, PLPM, pseudotime, or otherwise) is applied to order the clusters along a progression axis. The attractors are identified as stable regions of the joint EO/HRM feature space — basins in the Waddington landscape — but no direction of travel between basins is specified.

This is a direct answer to the project's interest in ordering (`hypothesis:0004`, `discussion:2026-06-07`): **this paper is about structure/states, not about temporal order**. Its contribution is complementary to — not overlapping with — the MHN progression-ordering goal. The clusters could in principle serve as inputs to a subsequent ordering analysis (e.g., are certain attractor states enriched in early-stage vs. late-stage disease, or do MHN hazard edges preferentially lead toward the hyper-unstable C10 attractor?), but the paper itself does not pursue this.

### 4. MSK-MET specifics

- **n=25,775** tumors; both primary and metastatic (MSK-MET is the metastatic-focused cohort from MSK-IMPACT).
- **Panel:** MSK-IMPACT targeted panel (cBioPortal-downloadable); not WGS/WES. CNVs and non-fusion structural variants excluded.
- **84 cancer subtypes** represented; metastasis analysis restricted to 15 major types (≥400 patients each).
- **Hallmark annotation source:** COSMIC database (gene-to-hallmark mapping, last accessed July 2025); the specific COSMIC version or gene census version is not stated [UNVERIFIED from text — supplementary table S1 lists the final gene set].
- **Metastasis focus:** The MSK-MET cohort was specifically designed to characterize metastatic patterns (Nguyen et al. 2022 Cell); this means the dataset is enriched for advanced/metastatic disease and **not representative of early-stage tumors** — a limitation the authors acknowledge, noting that survival models could not be adjusted for age, performance status, or treatment.
- **TP53 handling:** Because TP53 maps to 13/15 hallmarks in COSMIC, it was broken out as a standalone 16th feature. This is an important design choice — TP53 involvement at any hallmark would inflate 13 binary features simultaneously, confounding the distance calculation.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| HRM binary feature vector (16 dim) | Per-sample hallmark-level summarization | Directly applicable to project's MSK-IMPACT/cBioPortal data; COSMIC gene-hallmark map is the annotation source |
| Jaccard-distanced t-SNE + K-means | Unsupervised cancer-type clustering | Blueprint for a pan-cancer attractor-state analysis on this project's gene×cancer matrix |
| EO (5 germ-layer groups) as one-hot feature | Per-histology framing; oncofetal/cell-of-origin stratification | Provides principled rationale for why histology conditioning is necessary; EO is a coarser but transferable proxy |
| EO/HRM beats HRM-alone (ARI, C-index) | EO/lineage improves over mutation-only models | Supports adding EO or lineage metadata as a covariate in the project's cross-histology analyses |
| 11 attractor states (EO/HRM model) | Data-driven cancer subgroups beyond histology | These are states, not a progression order; contrast with the hypothesis:0004 MHN ordering goal |
| C6 (TP53-minimalist) attractor | TP53 as a standalone feature / driver class | Supports separating TP53 from other hallmarks in feature construction — relevant to project's annotation pipeline |
| C10 (neural-crest hyper-unstable) | Hypermutator / genomic instability cluster | C10 aligns with the project's hypermutator stratification (t081): neural-crest-derived, high TMB, high FGA |
| C5 (genomically quiescent) | Low-TMB / low-FGA subtype | Low-burden subgroup potentially contaminated by CH or panel under-coverage — relevant to t081 / t087 |
| Prognostic inversions (C0 in LUAD vs. PRCA) | Mandatory per-histology framing | Direct empirical demonstration of Simpson's-paradox-type context-dependence; justifies per-histology conditioning |
| Metastasis site prediction (AUC 0.68 vs. 0.67) | Cross-study aggregation of metastasis metadata | MSK-MET's metastasis site data is richer than typical cBioPortal studies; not directly replicated in project pipeline |
| Random Forest cluster assignment (>99% accuracy) | Cluster assignment for held-out samples | Practical template: train RF on training folds, assign test samples by classifier rather than re-running t-SNE |
| Bootstrap + 5-fold CV robustness evaluation | Leave-one-study-out stability for hypothesis:0004 | Directly adoptable validation protocol for any clustering step in the project |
| Semi-supervised nature of HRM features | Label-free vs. label-guided (discussion:2026-06-07) | Hallmark labels enter at feature construction, not clustering — the "from data, not labels" question is NOT answered here |
| No progression ordering claimed | hypothesis:0004-mhn-pathway-ordering | Paper is about states/structure; ordering is an open question that this paper neither addresses nor contradicts |

## Limitations

- **HRM features are hallmark-label-dependent.** The COSMIC gene-to-hallmark mapping is used as a fixed annotation; any errors, omissions, or boundary choices in COSMIC propagate directly into the features. The paper cannot discover structure that crosses or contradicts the COSMIC hallmark assignments. The "from data" claim applies only to the clustering step, not the feature engineering.
- **Binary HRM encoding loses mutation burden.** Each hallmark is binary (involved/not), ignoring the number of mutations per hallmark, their functional weight, or the distinction between activating and loss-of-function variants. This flattens biologically meaningful distinctions (e.g., a single KRAS G12D vs. many low-impact variants in the same hallmark category both receive the same binary flag).
- **CNVs and non-fusion structural variants excluded.** Copy number alterations are a major driver of many cancer types (e.g., ERBB2 amplification, CDKN2A deletion). Exclusion means HRM profiles represent only sequence-variant-accessible hallmarks.
- **MSK-IMPACT panel bias.** All data come from a single panel. Panel-specific gene coverage means absence = not tested, not wild-type — the same callability confounder the project's t078 addresses. No callability correction is applied; between-cancer-type differences in HRM prevalence may partly reflect differences in which hallmark-associated genes are on the panel.
- **MSK-MET is advanced/metastatic-enriched.** Survival models cannot be generalized to early-stage disease. Models were not adjusted for age, performance status, or treatment — major confounders for OS in a mixed cohort.
- **TP53 handling is post-hoc.** Separating TP53 into a 16th feature is biologically motivated but was decided based on observing its COSMIC representation, not specified a priori. Other highly pleiotropic genes (e.g., KRAS, which dominates several hallmarks per the leave-one-out analysis) were not given the same treatment.
- **EO is organ-level, not cell-type-level.** Embryological origin was inferred from organ-level cancer type classification (supplementary table S2), not from single-cell or lineage tracing. Intra-organ heterogeneity in cell-of-origin (e.g., luminal vs. basal breast; acinar vs. ductal pancreatic) is not captured.
- **No external validation cohort.** All robustness assessment (bootstrap, 5-fold CV) is internal to MSK-MET. No independent cohort (e.g., TCGA, AACR GENIE) was used to confirm cluster reproducibility.
- **No clonal hematopoiesis correction.** CH-contaminated alleles (DNMT3A, TET2, TP53, ASXL1 — all present in COSMIC with hallmark associations) in non-matched-normal studies would inflate apparent HRM involvement. MSK-IMPACT uses paired normal sequencing for most samples [UNVERIFIED — matched-normal status per sample not stated in text], which would mitigate but not eliminate this concern.
- **No accounting for hypermutators / MSI-H separately.** C10 and C1/C3 are retrospectively described as TMB-High and/or MSI-H-enriched clusters, but hypermutator status is not used as a feature or confounder in the clustering. The project's t081 hypermutator stratification would be a necessary preprocessing step before applying this framework to project data.

## Model / Tool Availability

No software package or code repository is reported. Analysis was performed with Python (scikit-learn, SciPy), Matlab, and SPSS v29.0.0.0. The pipeline components (Jaccard t-SNE, K-means, Random Forest classifier) are all standard scikit-learn primitives — the method is readily re-implementable. Supplementary tables S1 (hallmark-gene mapping) and S2 (cancer-type to EO mapping) are the critical annotation assets; they are described but not hosted at a URL in the preprint.

## Follow-up

- **Replicate HRM feature construction on project data.** The COSMIC gene-hallmark mapping used here (supplementary table S1) is directly applicable to the project's MSK-IMPACT-derived mutation tables. As a concrete pilot: extract the 16-dimensional HRM binary vector per sample from the project's `gene_cancer_study_annotated.feather` (after filtering against the COSMIC hallmark gene sets) and run the same Jaccard t-SNE + K-means pipeline. Compare resulting clusters to the 11 EO/HRM states described here.
- **Assess whether EO adds discriminative power in the project's data.** The paper shows EO improves ARI and C-index modestly but consistently over HRM-alone. In the project's data (which spans more cancer types but with fewer samples per type), test whether adding the five germ-layer EO one-hot encoding as features shifts cluster stability, and whether it resolves the prognostic inversions the paper demonstrates.
- **Use C10 (neural-crest, TMB-high) as a hypermutator label validation.** C10 is retrospectively characterized as the hyper-unstable cluster dominated by cutaneous melanoma and GIST with high TMB. Compare C10 cluster membership against the project's t081 `is_hypermutator` flag — this serves as a cross-method validation of the hypermutator annotation.
- **Treat attractor states as inputs to MHN ordering.** The 11 attractor states defined here are cross-sectional structure, not temporal order. A natural extension (not attempted in the paper) is to treat cluster membership as a categorical covariate in a progression-ordering analysis: do transitions between attractor states show a directional bias analogous to the genome-instability-first → immune-evasion-last hallmark ordering from the 2024 temporal-evolution paper? This would connect this paper's structure to the project's hypothesis:0004 ordering goal.
- **Incorporate EO/HRM attractor states as a post-hoc annotation overlay for hypothesis:0004.** After per-histology MHN fits, annotate each gene with its most-common HRM assignment and check whether the MHN-inferred progression order mirrors the hallmark co-occurrence structure of the EO/HRM clusters — i.e., do genes from the same attractor-state cluster tend to be co-ordered in MHN, or to occupy the same position in the inferred progression?
- **Obtain supplementary tables S1 and S2** (COSMIC hallmark gene list; cancer-type to EO mapping) to enable direct replication of the HRM feature construction. These are the load-bearing annotation assets and are not reproduced in the main text.
- **Note for `discussion:0007-hallmark-ordering-and-data-driven-modules`:** This paper validates the HRM feature-construction approach on cBioPortal-adjacent panel data, confirms that binary hallmark vectors carry stable clustering signal, and confirms that EO/lineage context modulates the clinical meaning of genomic states — but it does not answer the "hallmark-like modules from data" question because hallmark labels are inputs to the feature construction, not discovered from the data. The label-free question remains open and best addressed by the t078/WeSME + MHN route described in that discussion.
