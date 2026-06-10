---
type: paper
title: Simultaneous Inference of Cancer Pathways and Tumor Progression from Cross-Sectional
  Mutation Data
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: paper:RaphaelVandin2015
ontology_terms: []
datasets:
- dataset:tcga
source_refs:
- cite:RaphaelVandin2015
related:
- hypothesis:0004-mhn-pathway-ordering
- question:0012-mutation-ordering-cross-sectional-inference
- discussion:0007-hallmark-ordering-and-data-driven-modules
- topic:co-occurrence-and-mutual-exclusivity
- paper:Vocht2026
- paper:Schill2024
dataset_usage:
- ref: dataset:tcga
  role: analyzed
  overlap: unknown
---

# Simultaneous Inference of Cancer Pathways and Tumor Progression from Cross-Sectional Mutation Data

- **Authors:** Benjamin J. Raphael, Fabio Vandin
- **Year:** 2015
- **Journal:** Journal of Computational Biology
- **Volume/Issue:** 22(6):510–527
- **DOI:** 10.1089/cmb.2014.0161
- **PMC:** PMC4449706
- **Conference version:** RECOMB 2014
- **BibTeX key:** RaphaelVandin2015
- **Source:** Full text via PMC open access (PMC4449706); all methods and results verified from primary text.

## Key Contribution

This paper introduces the **Pathway Linear Progression Model (PLPM)** — a unified probabilistic-combinatorial framework that **simultaneously infers** (a) which genes belong to the same "pathway" (i.e., mutually exclusive cancer driver modules) **and** (b) the ordered temporal sequence in which those modules are acquired during tumor progression, using only cross-sectional binary mutation matrices. No pathway labels are required as input; both the partition and the ordering emerge from the data.

The core insight is that two known empirical regularities — *within-pathway mutual exclusivity* (one hit per cell is sufficient to perturb a functional module) and *across-pathway progression order* (later modules tend not to be mutated unless earlier ones already are) — impose jointly testable constraints on a binary mutation matrix. The authors cast recovery of the optimal partition-plus-ordering as a minimum-edit ILP (integer linear program), prove NP-hardness of the exact problem (Theorem 2.1), derive sample-complexity bounds for identifiability under noise-free (Theorem 2.2) and noisy (Theorem 2.3) conditions, and demonstrate feasibility on three real cancer datasets using CPLEX.

## Methods

### Model definition

A **PLPM** with K ordered pathways is a partition of n driver genes into K ordered sets S_1, S_2, ..., S_K with two properties:

1. **Exclusivity constraint:** Within each set S_k, at most one gene is mutated per tumor sample (one-hit mutual exclusivity).
2. **Progression constraint:** If any gene in S_k is mutated in sample i, then at least one gene in every earlier set S_1, ..., S_{k-1} is also mutated in sample i (linear ordering of module acquisition).

Given an m × n binary mutation matrix M (m samples, n genes), the **Pathway Linear Progression Reconstruction Problem** seeks the K-set partition that minimizes the number of matrix entries ("flips") that must be changed to make M exactly consistent with a valid PLPM — i.e., the edit distance between M and the nearest exactly-PLPM-consistent matrix.

### ILP formulation

Binary indicator variables:
- **p_{j,k}**: gene j is assigned to pathway k.
- **a_{i,k}**: pathway k is "active" (mutated) in sample i.
- **f_{i,k}**: a flip is needed in pathway k for sample i.

Constraints enforce that each gene belongs to exactly one pathway, each pathway contains at least one gene, the progression ordering is maintained (a_{i,k} = 1 implies a_{i,k'} = 1 for all k' < k), pathway activity is consistent with gene assignment, and flip indicators are correctly set. The objective minimizes ∑_{i,k} f_{i,k}.

### Complexity and identifiability

**Theorem 2.1 (NP-hardness):** The reconstruction problem is NP-hard even when gene-to-pathway assignment is fixed (only ordering varies), establishing that there is no polynomial algorithm unless P = NP.

**Theorem 2.2 (error-free sample complexity):** With no data noise and at least m* samples, where m* depends on K, n, and the gene frequencies, the ILP optimal solution uniquely recovers the true partition with high probability.

**Theorem 2.3 (noisy sample complexity):** When each entry in M is independently flipped with probability q (false-positive/negative error rate), unique recovery remains possible, but the required sample size m* increases — specifically, the required m grows with q/(1-2q)^2 scaling. This provides a closed-form condition on sample count, number of pathways, and noise rate under which PLPM is identifiable.

### Algorithm

The ILP is solved with CPLEX v12.3 (default parameters, single CPU). Pathway count K is treated as a user-supplied parameter; model selection across K is done by inspecting the progression score (total flips / mn) as K increases. A bootstrap stability analysis assigns each gene to the pathway it is most frequently assigned to across 100 bootstrap resamples; genes assigned to the same pathway ≥50% of resamples are considered robustly co-assigned.

### Implementation note

No public software package was released with this paper. The ILP is described fully in the text; implementations would depend on an external MILP solver (CPLEX or open-source equivalents such as Gurobi, CBC, or SCIP).

## Key Findings

### Simulated data

- With K = 5 pathways, 5 genes each, and noise probability p ≤ 0.01, the ILP recovers the correct partition 100% of the time with m = 500 samples.
- At higher noise (p = 0.05), m = 1000 samples achieves 95% correct recovery.
- Adding 25 irrelevant (non-driver) genes does not degrade recovery at p = 0.001, m = 500.

### Colorectal cancer — Wood et al. 2007 dataset (95 samples, 8 genes)

The inferred 3-stage PLPM places APC in the earliest stage, TP53 and PIK3CA in the middle stage (significantly mutually exclusive; p < 0.008), and KRAS late — consistent with the established APC → TP53/PIK3CA → KRAS colorectal progression model. This is recovered without supplying pathway labels.

### TCGA colorectal cancer (224 samples, 14 genes)

The 5-stage PLPM reproduces the same APC → TP53/PIK3CA → KRAS core ordering. Extended analysis on 43 genes additionally places ATM (a known TP53 interactor) in the TP53/PIK3CA module; Ras/Raf pathway genes (BRAF, KRAS, NRAS) co-cluster (p < 0.05 for SMAD2/SMAD4 co-assignment); SMAD2 and SMAD4 are significantly co-assigned, reflecting their known interaction. Running time: 86 seconds (5 stages, 14 genes, 224 samples); 13,763 seconds for the 43-gene extended model.

### TCGA glioblastoma multiforme (251 samples, 27 genes, 6 stages)

A six-stage PLPM assigns:
- Stage 2: Rb1 pathway genes predominate (≥50% of genes assigned here by bootstrap).
- Stage 3: PI3K pathway dominates.
- Stage 4: p53 pathway concentrated.

Bootstrap analysis shows >50% assignment stability for pathway-paired genes, indicating that the ILP solution is not an artifact of the optimization landscape. Running time: 2,488 seconds.

## Relevance

### Module discovery and mutual exclusivity (topic:co-occurrence-and-mutual-exclusivity / t078)

The PLPM's module-discovery component is directly related to what the project's co-occurrence and mutual-exclusivity pipeline (t078; DISCOVER / SELECT / WeSME) seeks to detect. Both exploit the same signal: within-pathway mutual exclusivity implies negative co-occurrence of driver genes that perturb the same functional unit. The difference is in approach: t078 tests for pairwise (or gene-set) mutual exclusivity against a callability-corrected null, while the PLPM solves for the optimal *partition* that is globally consistent with mutual exclusivity across all K pathways simultaneously.

The ILP formulation is therefore a natural upstream complement to t078: instead of testing whether a pre-specified gene set is mutually exclusive, it discovers which gene sets are mutually exclusive. The recovered modules are data-driven analogs of the "hallmark-like units" discussed in `discussion:0007-hallmark-ordering-and-data-driven-modules` — and, because the partition is label-free, they do not presuppose the canonical hallmark boundary assignments.

**Practical implication for t078:** Results from the PLPM (or any mutual-exclusivity module-discovery step) could *define* the input modules for pathway-level MHN analysis (h04), rather than using the Sanchez-Vega 2018 10-pathway annotation. This creates a fully data-driven pipeline: discover modules (PLPM/WeSME) → order modules (MHN) → annotate post hoc against hallmark gene sets.

### Progression inference and MHN (h04)

The PLPM's progression-ordering component occupies a similar niche to MHN (Schill 2020; Schill 2024; Vocht 2026), but the two methods differ substantially:

| Dimension | PLPM (this paper) | MHN (Schill/Vocht) |
|---|---|---|
| Model type | Combinatorial edit-distance / ILP | Continuous-time Markov chain |
| Simultaneity | Jointly infers partition AND order | Assumes genes are pre-defined events; infers hazard matrix |
| Module discovery | Yes — partition is a free variable | No — each gene is a separate event |
| Temporal model | Discrete linear order (S_1 < S_2 < ... < S_K) | Directed graph of hazard promotions/inhibitions |
| Observation bias | Not modeled — no observation-event equivalent | Explicit observation-event correction (Schill 2024) |
| Noise model | Edit-distance / flip model | Likelihood under exponential holding times |
| Output | Partition + total ordering of modules | Continuous hazard rates + pairwise edge directions |

The PLPM is more interpretable at the module level and does not require a pre-specified gene list, but it sacrifices the continuous-time generative story, the diagnostic-cohort observation-event correction, and the ability to infer partial orderings or cycles. For the project's h04 goal of ordered pathway-level inference, the PLPM and MHN are therefore best treated as **complementary**: the PLPM discovers the modules (label-free partition), and MHN then orders them with the observation-event correction that prevents collider bias.

### Identifiability assumptions and confounders relative to q012

The paper's Theorems 2.2 and 2.3 establish identifiability conditions for the PLPM. In the context of q012 and the project's cross-sectional cBioPortal data, several important gaps apply:

1. **Cross-sectional under-identification (q012 core concern).** The PLPM, like all cross-sectional methods, cannot distinguish true temporal progression from pure fitness asymmetry. The identifiability theorems assume the PLPM generative model is correct — i.e., that early-module mutations are genuinely prerequisite. This is an assumption about biology, not a statistical test.

2. **No observation-event / collider-bias correction.** The PLPM has no analog of Schill 2024's observation-event model. Diagnostic-cohort selection means that a sample enters the dataset partly because of its genomic state; genes that raise detectability (EGFR in LUAD, TP53 in CRC) will appear anti-correlated with co-occurring drivers in naive mutual-exclusivity analysis, potentially mislabeling biologically co-occurring genes as same-module (mutually exclusive). The project would need to apply an observation-event correction *before* running the PLPM, or separately validate PLPM module assignments against an observation-corrected model.

3. **No error model for panel callability.** The Theorem 2.3 noise model treats each entry as independently flipped with a constant probability q. Real panel sequencing introduces structured missingness: a gene not on the panel is always 0, and different samples in the same study may have different callable gene sets. This is a form of non-random, non-i.i.d. "noise" that violates the theorem's assumptions and can create spurious mutual exclusivity (two genes that are both absent from some panels look exclusive). The same callability correction required for t078 would be required before applying the PLPM.

4. **Per-histology pooling.** The paper applies the PLPM to individual cancer types (CRC, GBM) rather than pooling across histologies. Simpson's-paradox artifacts from pan-cancer pooling (a recurring confound in q012) are avoided by design in these experiments, but would need to be explicitly gated in any pipeline application.

5. **Hypermutator tumors.** Hypermutator / MMR-deficient tumors violate the progression assumption (they saturate multiple pathway sets simultaneously), making them likely to appear as high-flip-count outliers. The project's t081 hypermutator filter should be applied before running the PLPM.

6. **ILP runtime scalability.** The 43-gene extended CRC model required ~3.8 hours; the 27-gene GBM model ~41 minutes on a single CPU. The project's 10k-gene universe requires pre-filtering to a driver gene set (~100-500 genes) before ILP is feasible; even then, per-cancer-type analysis with >50 genes and >500 samples will push runtime substantially beyond what was demonstrated.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Pathway Linear Progression Model (PLPM) | Data-driven mutation module discovery | Blueprint for label-free hallmark analog inference (discussion:2026-06-07) |
| Mutually exclusive gene module (pathway set S_k) | Co-occurrence-null gene cluster (t078 output) | Same signal; PLPM global optimization vs. t078 pairwise/set tests |
| Linear ordered sequence S_1 < ... < S_K | Pathway-level MHN progression order (h04) | PLPM gives discrete total order; MHN gives continuous directed graph |
| Edit distance / flip count | Fit quality metric | Analogous to MHN log-likelihood; PLPM minimizes flips, MHN maximizes likelihood |
| NP-hardness (Theorem 2.1) | Computational constraint | Practical implication: pre-filter to ≤50-100 driver genes before ILP |
| Noisy identifiability (Theorem 2.3) | Cross-sectional under-identification (q012) | Theory gives closed-form m* requirement; project cohort sizes may meet this for pathway-level K |
| ILP (CPLEX) | External solver dependency | No published package; project would need CPLEX/Gurobi or open-source MILP solver |
| APC → TP53/PIK3CA → KRAS (CRC result) | Known CRC progression benchmark (h04 calibration) | Matches Gerstung 2020 PCAWG ordering; useful as a validation baseline |
| Rb1 → PI3K → p53 (GBM result) | GBM pathway ordering (not in current h04 scope) | Six-stage model with bootstrap-stable pathway assignments |
| Bootstrap stability analysis | Robustness / leave-one-study-out (h04 falsifiability) | PLPM uses 100 bootstrap resamples; project would analogously fold-validate |
| K (number of stages) as user parameter | Number of pathway-level modules | Must be selected by model-comparison (score vs. K); not estimated from data |
| No observation-event model | Missing collider-bias correction vs. Schill2024 | This is the most important gap relative to the MHN family for cBioPortal diagnostic cohorts |

## Limitations

- **No observation-event correction.** The PLPM does not model diagnostic-cohort selection bias. Genes that affect clinical detectability will create spurious mutual-exclusivity or progression signals in the recovered partition (see Schill 2024 for the correction that the MHN family provides). This is the single most important gap for applying PLPM to cBioPortal data.
- **Strictly linear progression.** The PLPM requires a total order (each pathway is either before or after every other). Branching evolutionary trajectories — parallel routes that are common in cancer (e.g., the KRAS/BRAF alternative route in CRC) — are not representable. MHN-family methods support partial orders and inhibitory edges.
- **ILP scalability.** Runtime grows rapidly with the number of genes and stages: 43 genes at 5 stages took ~3.8 hours; even 100 genes would likely be intractable. Pre-filtering to a small driver gene set is mandatory. The project's 10k-gene universe cannot be used directly.
- **K is exogenous.** The number of pathway stages K is supplied by the user and selected informally (inspection of flip-count vs. K curves). There is no formal model-selection criterion analogous to BIC or cross-validation built into the method.
- **Constant flip rate assumption.** Theorem 2.3's noise model assumes i.i.d. flip probability q. Panel-specific gene missingness and hypermutator-driven excess mutations are structured violations of this assumption. The theoretical guarantees therefore do not directly translate to real panel sequencing data without additional preprocessing.
- **No software package released.** The paper describes the ILP in full but does not release a standalone tool. Re-implementation requires writing the ILP from scratch and linking to a solver. This is a practical barrier compared to the ready-to-use `mhn` Python package (Vocht 2026).
- **No accounting for clonal hematopoiesis.** CH-contaminated alleles (DNMT3A, TET2, TP53, ASXL1 in non-matched-normal studies) would appear as ubiquitous "early" mutations — not because they precede lineage drivers biologically, but because they are somatic noise from blood leukocytes.

## Model / Tool Availability

No published software package. The ILP formulation is fully described in the paper (equations and variable definitions in Section 2); a re-implementation would use a standard MILP solver:

- **CPLEX** (IBM, commercial) — used in the paper; v12.3, default settings.
- **Gurobi** (commercial, free academic license) — direct drop-in alternative.
- **PuLP / OR-Tools / SCIP** (open source) — viable for smaller instances.

The `mhn` Python package (Vocht 2026; https://github.com/spang-lab/LearnMHN) provides the MHN-family progression ordering but not the PLPM's joint module discovery.

## Follow-up

- **Evaluate as a module-discovery front-end for h04.** The principled pipeline is: (1) discover mutually exclusive modules via PLPM (or WeSME / SELECT from t078) on per-histology driver gene sets; (2) order the modules with observation-event MHN (Vocht 2026 / Schill 2024); (3) annotate modules post hoc against Sanchez-Vega 2018 / hallmark gene sets. Assess whether PLPM modules or Sanchez-Vega pathway labels give more stable MHN-level ordering.
- **Re-implement the ILP using an open-source solver** (OR-Tools or PuLP + CBC/SCIP) for a small proof-of-concept: apply to CRC from GENIE (matched to Wood et al. 8-gene set) and verify that APC → TP53/PIK3CA → KRAS is recovered — this doubles as a pipeline validation against known biology.
- **Apply Theorem 2.3 to the project's cohort sizes.** Compute the theoretical sample-size lower bound m* for K ∈ {3, 5, 10} stages and n ∈ {14, 27, 50} driver genes at realistic noise rates (q ≈ 0.05) to confirm that per-histology GENIE cohort sizes (e.g., ~3,600 LUAD samples) satisfy identifiability requirements.
- **Check q012 for update.** Add a note that the PLPM is relevant to the module-discovery sub-question raised in `discussion:0007-hallmark-ordering-and-data-driven-modules`: specifically, that it is a single-method alternative to the "t078 pairwise exclusivity → post hoc partition" approach, and that it lacks the observation-event correction required before deployment on diagnostic cohorts.
- **Read Beerenwinkel 2007 (CBN)** for the continuous-time antecedent of both PLPM and MHN; and Caravagna 2016 (CAPRI / TRONCO) for the CAPRESE/CAPRI formulation that also jointly infers topology and selects a model from cross-sectional data — comparisons across these methods are part of the t132 literature search scope.
- **Consider runtime alternatives.** If exact ILP is too slow for the project's driver gene sets, the WeSME algorithm (weighted set-cover based mutual-exclusivity module discovery) or the PathoLogic relaxation of the PLPM are approximate polynomial alternatives that scale better; include in t132 scope.
