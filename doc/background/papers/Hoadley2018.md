---
id: paper:Hoadley2018
type: paper
title: Cell-of-Origin Patterns Dominate the Molecular Classification of 10,000 Tumors
  from 33 Types of Cancer
status: read
ontology_terms: []
source_refs:
- article:Hoadley2018
related:
- paper:Bailey2018
- paper:Ellrott2018
- paper:Ciriello2013
- topic:pan-cancer-mutation-landscape
created: '2026-04-13'
updated: '2026-04-12'
dataset_usage:
- ref: dataset:tcga-pancanatlas
  role: analyzed
  overlap: unknown
---

# Cell-of-Origin Patterns Dominate the Molecular Classification of 10,000 Tumors from 33 Types of Cancer

- **Authors:** Hoadley KA, et al.
- **Year:** 2018
- **Journal:** Cell 173(2):291-304.e6
- **PMID:** 29625048
- **PMCID:** PMC5957518
- **DOI:** 10.1016/j.cell.2018.03.022
- **BibTeX key:** Hoadley2018

## Key Contribution

Capstone PanCanAtlas paper that asks whether a multi-platform molecular taxonomy of
~10,000 TCGA tumors across 33 cancer types reorganizes cancer beyond its current
organ/histology-based classification. The headline finding is the negative-positive
result: cell-of-origin (tissue lineage / developmental program) dominates the integrated
molecular classification, but a meaningful fraction of tumors regroup into cross-tissue
clusters (pan-squamous, pan-gastrointestinal, pan-gynecologic, pan-kidney) that the
authors argue could change clinical management for ~1 in 10 patients. Extends a 2014
interim Pan-Cancer-12 analysis of 3,527 tumors / 12 cancer types up to the full 33-type
PanCanAtlas cohort.

## Methods

**Cohort.** ~10,000 TCGA primary tumor specimens spanning 33 cancer types
(hematologic/lymphatic, gynecologic, urologic, endocrine, GI, head/neck, thoracic,
CNS, soft tissue, neural-crest/melanoma). Platform-specific sample counts:
mRNA n=10,165; miRNA n=10,170; RPPA n=7,858 (216 proteins); methylation reduced
to 1,035 informative CpG sites; CNA at chromosome-arm level. 9,759 tumors had
complete data on the four platforms used for joint clustering.

**Integrative clustering (iCluster).** Joint multivariate latent-variable model
integrating four platforms simultaneously: CNA, DNA methylation, mRNA, and miRNA.
Variance contributions: CNA ~47%, transcriptome (mRNA+miRNA) ~42%, methylation ~11%.
Yielded a **28-cluster taxonomy** ("C1"-"C28") spanning the 33 tumor types.

**COCA (Cluster-Of-Cluster-Assignments).** Orthogonal approach: run platform-specific
clustering separately, then cluster tumors by the vector of their per-platform cluster
labels. Used to assess concordance across platforms and against iCluster.

**Mutation data treatment.** Critically, **somatic mutations were *not* used as input
to iCluster** "due to sparsity of mutations." Instead, mutational burden and mutational
signatures were overlaid post-hoc to characterize the clusters. PARADIGM was used for
pathway-level integration.

**Pan-organ deep dives.** Pan-GI, pan-gyn, pan-kidney, and pan-squamous groupings
identified here were the basis for separate companion PanCanAtlas reports.

## Key Findings

- **Cell-of-origin dominates, but not absolutely.** For **16 of 33** tumor types,
  >80% of samples landed in a single iCluster; for **6 of 33** tumor types, <50%
  landed in any one cluster (BLCA, UCS, HNSC, ESCA, STAD, CHOL exhibit substantial
  intra-histology molecular heterogeneity).
- **28 integrated clusters** from 33 tumor types - the molecular taxonomy is *coarser*
  than the histologic one in places and *finer* in others.
- **Cross-tissue ("pan-organ") clusters that cut across histology:**
  - **Pan-squamous (C10, C25, C27):** unifies LUSC, HNSC, CESC (cervical), and
    squamous ESCA; shared chromosome 3q amplification.
  - **Pan-gastrointestinal (C1, C4, C18):** COAD/READ/STAD separated by methylation
    state (EBV-CIMP, MSI, CIN).
  - **Pan-kidney (C28):** KIRC + KIRP grouped robustly.
  - **Pan-gynecologic** is *not* a clean single cluster - cervical cancer aligns
    with the squamous group rather than with other gyn tumors, fragmenting the
    "gynecologic" category.
- **C20 = mixed stromal/immune cluster:** the largest and most heterogeneous
  iCluster, containing **25 of 33 tumor types**, defined by highest median stromal
  fraction and elevated leukocyte fraction rather than by lineage - a candidate
  immunotherapy-responsive grouping that crosses tissue boundaries entirely.
- **Mutation patterns were overlaid, not used to cluster.** Post-hoc, mutational
  burden and signatures align with expected biology (UVB in SKCM/C15, smoking in
  LUAD/C14, POLE in hypermutated endometrial, MSI in pan-GI). The paper does **not**
  perform a head-to-head mutations-only-clustering vs integrated-clustering comparison.
- **Clinical implication:** authors estimate ~1 in 10 patients might be re-classified
  (and potentially re-treated) under a molecular rather than tissue-of-origin taxonomy;
  particularly relevant for cancer of unknown primary (1-3% of new diagnoses).

## Relevance

PanCanAtlas flagship arguing that tissue-of-origin / cell-of-origin dominates molecular
classification across 10,000 TCGA tumors. Direct competing frame to mutation-driven clustering:
when our pipeline clusters cancers by gene-mutation patterns, we should be aware that the
dominant axis of variation across cancers is *not* somatic mutations but tissue lineage.
Critical interpretation lens for `summary/mut/clusters/cancer.feather`.

**Important nuance from the paper itself:** Hoadley et al. *did not include somatic
mutations as a clustering input* (sparsity argument) and *did not* run a mutations-only
clustering for comparison. So while the paper establishes that lineage dominates the
*integrated multi-omic* signal (CNA + methylation + mRNA + miRNA), it does **not**
directly demonstrate that mutations-only clustering would recapitulate lineage. Our
mutation-only clustering output is therefore complementary, not redundant, and could
plausibly produce a clustering more aligned with mutational-process / driver-gene
biology than with tissue. Clusters like the pan-squamous 3q-amp group and the
hypermutator/MSI-driven pan-GI subgroups are the natural points of comparison.

## Limitations

- **TCGA-only cohort:** treatment-naive primary tumors with TCGA's known biases
  (predominantly resected, US-centric, fixed tissue protocols, age/access skew);
  metastatic and post-treatment biology underrepresented. <!-- UNVERIFIED: paper does
  not foreground treatment-naive selection bias as a stated limitation, but it is an
  inherent property of the TCGA cohort. -->
- **Mutations excluded from clustering input** due to sparsity - the iCluster
  taxonomy is by construction a CNA/methylation/expression taxonomy, not a
  mutation taxonomy.
- **Aneuploidy/CNA platform discordance:** ~one-third of samples had few arm-level
  events, reducing CNA's discriminative power for those tumors.
- **Method dependence:** iCluster (joint model) and COCA (consensus of per-platform
  clusterings) give related but non-identical taxonomies; the "28 clusters" number
  is contingent on iCluster's model-selection choices.
- **C20 catch-all:** a single cluster absorbs 25 tumor types via stromal/immune
  signal, suggesting either a real shared biology or a residual unmodeled axis.
- **Histology heterogeneity within types:** 6 cancer types fragment across many
  clusters, so "tissue-of-origin dominates" is a population-level claim, not a
  per-tumor guarantee.

## Follow-up

- Companion PanCanAtlas pan-organ deep-dives (pan-GI, pan-gyn, pan-kidney,
  pan-squamous) elaborate on the cross-tissue groupings identified here.
- Bailey et al. 2018 (driver-gene catalog) and Ellrott et al. 2018 (MC3 mutation
  calls) provide the mutation-centric companions not used as clustering input here.
- Open methodological question relevant to our work: **mutation-only clustering
  vs Hoadley's multi-omic clustering** - to what extent do they agree, and where
  do they diverge? Hoadley2018 does not answer this; our pipeline can.
- Application to cancer of unknown primary (CUP) classification is flagged by the
  authors as a concrete clinical follow-up.
