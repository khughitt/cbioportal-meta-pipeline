---
id: "paper:Wang2025a"
type: "paper"
title: "Data-driven universal insights into tumorigenesis via hallmark networks"
status: "active"
ontology_terms:
  - hallmarks of cancer
  - gene regulatory network
  - coarse-graining
  - stochastic differential equations
  - dynamic network biomarker
  - critical transition
  - tumorigenesis dynamics
  - pan-cancer analysis
  - tissue invasion and metastasis
  - reprogramming energy metabolism
  - GRAND database
  - PANDA algorithm
datasets:
  - GRAND (gene regulatory networks, normal and cancer tissues)
  - GTEx (normal tissue expression, used for model initialization)
  - TCGA/GEO (cancer expression, used for model initialization)
source_refs:
  - "cite:Wang2025a"
related:
  - "discussion:2026-06-07-hallmark-ordering-and-data-driven-modules"
  - "topic:co-occurrence-and-mutual-exclusivity"
created: "2026-06-07"
updated: "2026-06-07"
---

# Data-driven universal insights into tumorigenesis via hallmark networks

<!-- Authors: Jiahe Wang, Yan Wu, Yuke Hou, Yang Li, Dachuan Xu, Changjing Zhuge, Yue Han -->
<!-- DOI: https://doi.org/10.1038/s41540-025-00602-1 -->
<!-- BibTeX key: Wang2025a -->
<!-- Source: PDF -->

- **Authors:** Jiahe Wang, Yan Wu, Yuke Hou, Yang Li, Dachuan Xu, Changjing Zhuge, Yue Han
- **Year:** 2025
- **Journal:** npj Systems Biology and Applications
- **Volume/Issue/Pages:** 11:131
- **DOI/URL:** https://doi.org/10.1038/s41540-025-00602-1
- **BibTeX key:** Wang2025a
- **Source:** PDF

## Key Contribution

This paper proposes a whole-genome, data-driven systems biology framework for studying cancer evolution at the level of hallmarks rather than individual genes. The core idea is to coarse-grain the high-dimensional gene regulatory network (GRN) of a cell into a 10-node "hallmark network" — one node per canonical hallmark — and then simulate the dynamics of that network using stochastic differential equations (SDEs) incorporating Ornstein-Uhlenbeck noise. Applied across 15 cancer types from the GRAND database, the framework produces two main results: (1) hallmark-level probability distributions shift significantly between normal and cancerous states (all 10 hallmarks elevated in cancer, p < 0.001 for gastric adenocarcinoma as the representative example), with "Tissue Invasion and Metastasis" showing the largest normal-vs-cancer divergence (Jensen-Shannon divergence 0.692) and "Reprogramming Energy Metabolism" the smallest (JS divergence 0.385); and (2) network topology — specifically inter-hallmark regulatory connectivity as captured by the Dynamic Network Biomarker (DNB) score — undergoes significant reconfiguration **before** overt shifts in individual hallmark levels, providing an early-warning signal of the malignant transition. The topological early-warning lead time is statistically significant for all 10 hallmarks across all 15 cancer types (one-sample Wilcoxon signed-rank test, p < 0.001).

## Methods

### Data sources and GRN construction

Gene regulatory networks are drawn from the publicly available GRAND database (grand.networkmedicine.org), which contains computationally-inferred aggregate TF regulatory networks for 36 normal human tissues and 28 cancer types, constructed using the PANDA algorithm from expression profiles in GTEx (normal) and TCGA/GEO (cancer). The study restricts to **aggregate TF (Transcription Factor) Networks** built with PANDA for methodological consistency; miRNA and single-sample networks are excluded. Only cancer types with a paired normal tissue counterpart in GTEx are retained. A completeness check on normal tissue expression profiles (needed for model initialization) further narrows the cohort. The final dataset comprises **15 cancer types**: STAD, KIRP, KIRC, LUAD, LUSC, PCPG, SKCM, THCA, UVM, LAML, ACC, LGG, ESCA, HNSC, and KICH (14 solid tumors + 1 hematological).

### Hallmark gene set construction

The 10 canonical hallmarks (H1 Evading Apoptosis, H2 Evading Immune Destruction, H3 Genome Instability and Mutation, H4 Insensitivity to Anti-Growth Signals, H5 Limitless Replicative Potential, H6 Reprogramming Energy Metabolism, H7 Self-Sufficiency in Growth Signals, H8 Sustained Angiogenesis, H9 Tissue Invasion and Metastasis, H10 Tumor-Promoting Inflammation) are operationalized as gene sets through the following pipeline:

1. Start from the **Plaisier et al. (2012)** published mapping of hallmarks of cancer to Gene Ontology (GO) terms (reference 62 in the paper).
2. Retrieve the current GO term IDs from geneontology.org; remove any officially deprecated IDs (two removed, documented in Supplementary Table S2).
3. Use the **AmiGO tool** to retrieve genes annotated under each GO ID.
4. Intersect with genes present in the selected GRAND network datasets.
5. Retain only rows and columns corresponding to genes in at least one hallmark gene set, yielding hallmark-only sub-networks for analysis.

The final hallmark gene sets are provided in Supplementary Data 1.

### Coarse-graining and hallmark network construction

The inter-hallmark regulatory interaction matrix **V** is computed by summing all regulatory edge weights between each pair of hallmark gene sets within the paired normal and cancer sub-networks:

$$V_{ij} = \sum_{g_a \in G_i} \sum_{g_b \in G_j} w_{g_b \to g_a}$$

where $w_{g_b \to g_a}$ is the PANDA-inferred regulatory weight of gene $g_b$ on gene $g_a$. This is computed separately to yield a constant normal matrix $V_n = [V_{ij,n}]$ and a constant cancer matrix $V_c = [V_{ij,c}]$.

### Stochastic dynamical model

The state of the system at time $t$ is the vector $\mathbf{x}(t) = (x_1, \ldots, x_{10})$ where $x_i$ is the "level" of hallmark $H_i$. The regulatory input to hallmark $i$ is:

$$w_i(\mathbf{x}, t) = \alpha \sum_{j=1}^{M} V_{ij}(t) x_j$$

with scaling constant $\alpha = 10^{-4}$. This is passed through a nonlinear activation function, and the full SDE dynamics per hallmark are:

$$\frac{\mathrm{d}x_i}{\mathrm{d}t} = \lambda_i F(w_i(\mathbf{x}, t)) - e^{\eta_i(t) - \frac{\sigma^2}{2}} x_i$$

where $\lambda_i = 3.8$ is the maximum production rate, $\eta_i(t)$ is an Ornstein-Uhlenbeck noise process with noise intensity $\sigma = 0.1$ and correlation time $\tau = 1.0$, and the stochastic part is integrated by an Euler-Maruyama scheme.

The time-dependent interaction matrix $V(t)$ interpolates linearly between $V_n$ and $V_c$ via a transition function $f(t)$ randomly selected for each simulation run from four candidates (linear, sigmoidal, exponential, $1 - e^{-at}$), making the ensemble robust to the specific assumed transition shape. Simulation runs from $t = 0$ to $t = 100$: $t = 0$–30 is the normal network phase, $t = 30$–70 is the transition phase, and $t = 70$–100 is the cancer network phase. 10,000 trajectories are generated per cancer type.

Initial conditions $x_i(0)$ are set at the stationary state of the normal network, obtained by numerically solving the model with $V(t) = V_n$. The stationary value is the average expression level of genes in hallmark $i$ in normal tissue data.

### Early-warning signal detection (DNB theory)

The Dynamic Network Biomarker (DNB) method is applied to detect the critical transition tipping point. Fifty independent "virtual patient" samples are generated by resampling and aggregating 1,000 trajectories each. The **DIND (Direct Interaction Network-based Divergence) score** — a topology-sensitive variant of the DNB score based on symmetric KL divergence between distributions of adjacent time points — is computed per hallmark node and globally. The tipping point $t_1$ is defined as the first peak in the global DIND score; $t_2$ is the moment the average hallmark level first exceeds 1.2× the normal stationary state. The lead time $\Delta t = t_2 - t_1$ quantifies how far in advance network reconfiguration precedes phenotypic shift.

### Divergence quantification

Jensen-Shannon (JS) divergence is used to compare normal vs. cancer hallmark level distributions. Kernel Density Estimation with a common bandwidth (Silverman's rule applied to pooled data) ensures all PDFs are comparably smoothed.

### Statistical tests

- Mann-Whitney U test for pairwise normal vs. cancer hallmark level comparisons.
- One-sample Wilcoxon signed-rank test on $\Delta t$ distributions (null: median = 0).
- Friedman test on rank matrices across 15 cancer types.

### Potential energy landscape

A potential energy landscape is constructed by projecting the 10,000 × 100 trajectory matrix into 2D PCA space and estimating the density via 2D KDE; $U(x,y) = -\ln(P(x,y))$. This reveals two attractor basins (normal, cancer) and a most probable transition path (Fig. 7).

## Key Findings

### Hallmark dynamics (gastric adenocarcinoma as representative example)

- All 10 hallmark levels are significantly elevated in the cancerous stationary state vs. the normal stationary state (Mann-Whitney U, p < 0.001; Fig. 3c).
- JS divergences range from 0.295 (H6, Reprogramming Energy Metabolism) to 0.683 (H9, Tissue Invasion and Metastasis; Fig. 3d).
- Hallmarks with the largest distributional shifts: H9 Tissue Invasion and Metastasis (0.683), H8 Sustained Angiogenesis (0.669), H10 Tumor-Promoting Inflammation (0.668), H7 Self-Sufficiency in Growth Signals (0.667). Hallmarks with the smallest shifts: H6 Reprogramming Energy Metabolism (0.295), H4 Insensitivity to Anti-Growth Signals (0.218), H5 Limitless Replicative Potential (0.373; Fig. 3d).
- The smaller divergence of H6/H4/H5 is interpreted as reflecting overlap with normal proliferative physiology (e.g., Warburg effect is active in normal embryonic/immune cells; H4/H5 processes overlap with normal proliferative mechanisms).

### Network reconfiguration precedes hallmark shifts — across all 15 cancer types

- The DIND score shows a sharp peak at $t_1 = 37$ (gastric example), before $t_2$ (the overt hallmark shift), giving a positive lead time $\Delta t$ for all hallmarks.
- For H9 (Tissue Invasion and Metastasis), network reconfiguration preceded hallmark-level change by approximately 3 time units on average.
- Lead time $\Delta t$ is significantly greater than zero for all 10 hallmarks across 15 cancer types (one-sample Wilcoxon signed-rank, p < 0.001 for all; Fig. 5b).
- This precedence of network topology over node-level changes is the central mechanistic claim: the structure of hallmark interactions is a more sensitive malignancy indicator than hallmark activity levels per se.

### Pan-cancer universality (15 cancer types)

- "Tissue Invasion and Metastasis" (H9) is the **top-ranked hallmark by JS divergence** in 12 of 15 cancer types (average rank 1.00 across the cohort; Fig. 6c). H1 Evading Apoptosis and H7 Self-Sufficiency in Growth Signals are also consistently highly ranked.
- "Reprogramming Energy Metabolism" (H6) and "Limitless Replicative Potential" (H5) and "Genome Instability and Mutation" (H3) consistently show lower divergence ranks (Fig. 6a,c). Notably, H6 has average rank ~5.6 and H3 has average rank ~8.4 (lower rank = larger divergence in their convention).
- The consistent ranking pattern across the 15 cancers is highly statistically significant (Friedman test, p < 2.55 × 10^{-23}).
- H7 (Self-Sufficiency in Growth Signals) has the earliest early-warning lead time on average (average rank 1.00 in the lead-time ranking; Fig. 6d); H2 (Evading Immune Destruction) has the latest (average rank 9.73). The ranking of lead times is also highly significant (Friedman test, p < 1.08 × 10^{-19}).
- Hierarchical clustering of hallmark levels (Fig. 6e) identifies one major cluster of solid tumors: STAD, KIRP, KIRC, LUAD, THCA. LUSC is separated; hematological LAML is distinct.

### Cancer-type-specific patterns

- LUAD frequently harbors EGFR/KRAS mutations, activating PI3K/AKT/mTOR and MAPK/ERK, reflected in the H4/H7 dynamics.
- LUSC is driven by smoking-related CDKN2A mutations disrupting cell cycle and apoptosis, and "CEP55" co-expresses with cell cycle and DNA replication genes in LUAD but not LUSC.

### Potential energy landscape

- Two clear attractor basins (normal, cancer) are visible in the potential landscape (Fig. 7a,b).
- The normal-state basin is deeper than the cancer-state basin, indicating normal is a more stable attractor.
- The most probable transition path shows H9 (Tissue Invasion and Metastasis), H1 (Evading Apoptosis), and H7 (Self-Sufficiency in Growth Signals) exhibit the most pronounced hallmark increases along the transition path (Fig. 7c).

## Relevance

**Modality mismatch — be explicit.** This paper operates entirely on **gene-expression-derived regulatory network dynamics** (GRN edge weights from PANDA + SDE simulation). It does not use somatic mutation data, mutation frequencies, or cross-sectional genomic cohorts. The "hallmark levels" in this framework are aggregated expression activity of hallmark gene sets, not mutation burdens. The critical-transition signal is a property of inter-hallmark TF regulatory connectivity, not of somatic alteration ordering. Consequently, **this paper is adjacent to, not directly applicable to, the cBioPortal/GENIE somatic-mutation meta-analysis**. The specific experimental logic — compute TMB, build gene × cancer mutation matrices, infer ordering via MHN — has no equivalent in Wang2025a.

**What does transfer to the project:**

1. **Coarse-grained hallmark module framing.** Wang2025a provides a concrete, peer-reviewed implementation of precisely the "hallmarks as coarse-grained modules" conceptualization that `discussion:2026-06-07-hallmark-ordering-and-data-driven-modules` is exploring. Their coarse-graining procedure (GO-term gene sets aggregated via the Plaisier 2012 mapping → GRAND network sub-matrices → 10-node interaction network) is a specific, reproducible recipe. The project's analogous task is to treat hallmarks as gene-set partitions of the mutation matrix, then test whether mutual-exclusivity patterns within sets and co-occurrence patterns across sets match the expected GRN-level structure. Wang2025a demonstrates the framing is biologically productive at the expression level; the mutation-level version remains untested.

2. **Gene-to-hallmark assignment source.** The paper uses the **Plaisier et al. (2012, Genome Research)** hallmark-to-GO mapping as its canonical gene assignment step, intersected against the current GO database and the GRAND network genes. This is a specific, citable, reproducible assignment procedure that the project could adopt for the mutation-data version (assign each driver gene to a hallmark via its GO annotations, validate against the Plaisier mapping). The Plaisier reference (ref 62) is the load-bearing gene-assignment cite; the supplementary data (Supplementary Data 1, Table S2) provide the exact final gene sets.

3. **Critical-transition / early-indicator idea at the hallmark level.** The finding that network topology (inter-hallmark connectivity) changes before hallmark-level activity shifts is conceptually related to the project's mutation-ordering question: do mutations in some hallmarks systematically precede mutations in others? Wang2025a's result is at the regulatory level (topology precedes activity) and ours would be at the somatic level (driver mutations in enabling hallmarks precede mutations in executing hallmarks), but the logical structure is parallel. This makes the paper useful as **conceptual prior art and framing**, not a methodological blueprint.

4. **Pan-cancer hallmark ranking as a calibration target.** Wang2025a's finding that "Tissue Invasion and Metastasis" has the largest normal-vs-cancer divergence and "Reprogramming Energy Metabolism" the smallest, consistently across 15 cancer types, provides an expression-level reference expectation. If the project's mutation-ordering analysis recovers a different ordering (e.g., if H3 Genome Instability ranks first in the mutation-frequency domain, consistent with its enabling-characteristic role), the divergence between the two orderings would be interpretively interesting — mutation selection and expression dysregulation measure different aspects of hallmark activation.

5. **What does NOT transfer:**
   - The SDE model and DNB/DIND scores are not applicable to cross-sectional snapshot mutation data. Mutation data lack the time-series trajectory structure that the DNB method requires.
   - The "hallmark level" variable is defined as aggregated expression activity; there is no mutation-frequency analogue defined or validated.
   - The GRAND/PANDA networks are TF regulatory networks inferred from expression; they are not directly connected to the somatic alteration landscape.
   - The 15-cancer cohort overlaps substantially with TCGA-origin cBioPortal studies but the exact study composition differs.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Coarse-grained hallmark network (10-node GRN) | Hallmark-level aggregation of mutation modules | Wang2025a demonstrates feasibility of the framing; project needs the somatic-mutation analogue |
| Plaisier 2012 GO-based hallmark gene sets | Gene-to-hallmark assignment for mutual-exclusivity module analysis | Cite Plaisier 2012 (not Wang2025a) as the assignment source; Wang2025a validates the sets work at expression level |
| Network topology precedes hallmark activity shift (DNB/DIND early-warning) | Mutation-ordering inference (h04 / MHN) | Conceptual parallel: both ask whether some hallmark-level change is "earlier"; different data modalities and methods |
| JS divergence ranking (H9 highest, H6 lowest) | Pan-cancer hallmark ordering calibration | Expression-level ranking ≠ mutation-frequency ranking; the difference is interpretively informative |
| H9 Tissue Invasion and Metastasis: most different normal-vs-cancer | Late/executing hallmark in ordering | Consistent with `discussion:2026-06-07-hallmark-ordering-and-data-driven-modules` expectation that invasion/metastasis is a late hallmark |
| H3 Genome Instability and Mutation: smaller JS divergence | Genome instability as early/enabling hallmark | Expression level of H3 genes does not differentiate sharply — consistent with its role as an early mutational enabler, not a late expression program |
| H7 Self-Sufficiency in Growth Signals: earliest early-warning lead time | MHN early events | GRN-level early-warning order (H7 first, H2 last) may partially calibrate mutation-ordering expectations |
| Potential landscape with two attractor basins (normal, cancer) | Cancer as a distinct genomic attractor state | Conceptual support for treating tumorigenesis as a discontinuous transition rather than a continuum |
| 15 cancer types from GRAND (STAD, KIRP, KIRC, LUAD, etc.) | Overlapping cBioPortal study cancer types | Good overlap with the cBioPortal pipeline cohort; mutation-level analysis could be run on the same 15 types for direct comparison |
| GRAND database (publicly available) | Potential secondary input for expression-level validation | If project adds expression data, GRAND provides pre-built TF networks for paired normal/cancer comparisons |

## Limitations

- **Expression-only, no mutation data.** The entire framework is built on GRN (expression-based TF regulatory weights) and does not engage with somatic mutation frequency, driver mutation status, or clonal dynamics. The connection to the somatic mutation domain is entirely conceptual, not empirical. Claims about hallmark ordering made here cannot be directly compared to MHN-based ordering from mutation data without an explicit bridging analysis.
- **Curated hallmark labels as input, not output.** The coarse-graining starts from the Plaisier 2012 hallmark-to-GO mapping — a human-curated partition. The paper does not test whether data-driven coarse-graining would recover the same 10-node structure, nor whether a different partition would yield a more informative model. The hallmarks are an assumption, not an inference. This is the key gap relative to the project's "label-free module" aspiration described in `discussion:2026-06-07-hallmark-ordering-and-data-driven-modules`.
- **Simulation circularity.** The SDE model is initialized from the normal GRN and transitions to the cancer GRN as boundary conditions. The "transition" is therefore a mathematical interpolation between two observed endpoint states, not an independent prediction. The DNB early-warning signal is a property of the model's transition dynamics, which are themselves engineered to go from normal to cancer. The claim that "topology changes before levels" is internally consistent within the model but may not be independently falsifiable from the input data.
- **No patient-level data.** All "virtual patient" trajectories are synthetic: generated by resampling simulation runs. No actual longitudinal patient data are used to validate the predicted ordering or lead times.
- **PANDA networks are aggregate, not single-sample.** The GRAND/PANDA networks represent tissue-level averages; single-cell or single-patient heterogeneity is not captured. This limits the model's relevance to within-tumor clonal evolution.
- **15-cancer scope.** The cohort is restricted by data availability in GRAND (PANDA algorithm, paired normal). Cancers without a well-defined normal tissue counterpart (e.g., LAML is included but is hematological) or without PANDA-based GRAND networks are excluded. Generalizability beyond these 15 is untested.
- **DNB/DIND method assumptions.** DNB theory assumes that the critical-transition module shows enhanced within-module variance and cross-module correlation near the tipping point. These assumptions are derived from equilibrium statistical physics (Hopf bifurcation analogy) and may not hold for all cancer trajectories, particularly those driven by strong positive selection rather than a phase transition.
- **No external validation dataset.** The findings are not validated on an independent cohort or a held-out cancer type. The consistency across 15 cancer types is encouraging but all come from the same GRAND database with the same normalization pipeline.

## Model / Tool Availability

- The GRAND database is publicly available at grand.networkmedicine.org.
- Analysis pipelines and simulation codes are maintained at https://github.com/zhuge-c/Hallmark_dynamics (cited in the paper).
- Hallmark gene sets are provided in Supplementary Data 1; GO term-to-hallmark mappings in Supplementary Table S2.
- The paper is open-access under CC BY-NC-ND 4.0.

## Follow-up

- **Adopt the Plaisier 2012 hallmark-to-GO gene assignment as the project's canonical label-free-to-labeled bridge.** Wang2025a uses this mapping to go from data-available gene sets to hallmark labels, and provides the cleaned/updated gene sets in its supplementary data. For the project's post-hoc hallmark annotation of data-driven mutual-exclusivity modules (step 3 in the `discussion:2026-06-07` pipeline), this is a citable, reproducible starting point. Supplement with the Iorio 2018 / SLAPenrich pathway-hallmark mapping for cross-validation.

- **Compare hallmark ordering between modalities.** Wang2025a reports two hallmark rankings: (a) JS divergence rank (H9 first, H6 last — which hallmark's activity shifts most between normal and cancer) and (b) early-warning lead time rank (H7 first, H2 last — which hallmark's network reconfigures earliest). If the project's MHN-based mutation ordering recovers a third ranking (e.g., H3 Genome Instability first per the enabling-characteristic hypothesis), the three rankings can be compared in a table. Agreement and disagreement would each be interpretively informative: agreement would suggest the three modalities measure the same underlying biology; disagreement would suggest mutation selection, expression dysregulation, and regulatory network reconfiguration are partially decoupled processes.

- **Use the 15-cancer cohort as a benchmark set.** Wang2025a's results hold across STAD, KIRP, KIRC, LUAD, LUSC, PCPG, SKCM, THCA, UVM, LAML, ACC, LGG, ESCA, HNSC, and KICH — all of which have cBioPortal studies. Running the project's mutual-exclusivity and MHN analysis on the same cancer types enables a direct head-to-head comparison at the hallmark level.

- **Probe the "coarse-grained modules from data" gap.** The paper's most important limitation for the project is that it starts from curated hallmark labels. The natural extension — running the same stochastic network model on data-driven modules discovered by mutual exclusivity (à la `paper:RaphaelVandin2015`) rather than on hallmark-labeled gene sets — is not done here and would be a genuine novelty. Cite Wang2025a as motivation for the coarse-grained-module approach, then extend it by replacing curated hallmarks with data-driven modules as the node set.

- **Access Supplementary Data 1 (hallmark gene sets).** The paper's final gene sets (GO-based, intersected with GRAND genes) are in Supplementary Data 1 at https://doi.org/10.1038/s41540-025-00602-1. These are the most directly usable output for the project: a ready-made, up-to-date, curated-but-reproducible hallmark gene set that can be applied to annotate the project's data-driven modules.
