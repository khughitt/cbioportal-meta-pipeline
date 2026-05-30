---
id: paper:Vocht2026
type: paper
title: 'mhn: a Python package for analyzing cancer progression with Mutual Hazard
  Networks'
status: active
ontology_terms: []
source_refs:
- cite:Vocht2026
related:
- paper:Schill2024
- question:q012-mutation-ordering-cross-sectional-inference
- topic:co-occurrence-and-mutual-exclusivity
- discussion:2026-04-24-mutation-ordering-and-path-dependency
created: '2026-04-27'
updated: '2026-04-27'
dataset_usage:
- ref: dataset:aacr-genie
  role: analyzed
  overlap: unknown
---

# mhn: a Python package for analyzing cancer progression with Mutual Hazard Networks

- **Authors:** Stefan Vocht, Yanren Linda Hu, Andreas Lösch, Kevin Rupp, Tilo Wettig, Lars Grasedyck, Niko Beerenwinkel, Rainer Spang, Rudolf Schill
- **Year:** 2026
- **Journal:** Bioinformatics Advances, 6(1), vbaf283
- **DOI:** 10.1093/bioadv/vbaf283
- **BibTeX key:** Vocht2026
- **License:** CC-BY 4.0
- **Source:** PDF (local copy at papers/pdfs/vbaf283.pdf); all content extracted directly from the full text

## Key Contribution

`mhn` is a Python package implementing Mutual Hazard Networks (MHNs) for cancer progression modeling from cross-sectional tumor genotype data. The package addresses the primary computational bottleneck of earlier MHN implementations: because the state space of an n-event MHN grows as 2^n, training on more than ~25 events was previously infeasible. `mhn` introduces *state space restriction* — restricting each sample's computation to the submatrix of the transition rate matrix covering only states reachable from that sample's observed active events — combined with optional CUDA GPU acceleration. This reduces the per-sample runtime from O(n^2 * 2^n) (for the naive full-matrix approach) to O(n * m * 2^m) where m is the number of active events in a given sample, lifting the practical ceiling to **>100 events** provided no single sample has more than ~32 active events simultaneously.

Critically, the package implements the updated MHN formulation introduced in Schill et al. 2024, which resolves a pervasive **collider bias** inherent in prior cross-sectional progression models. The earlier approach (Schill et al. 2020) treated observation time as a nuisance variable marginalized uniformly; in the updated formulation, *tumor detection itself is modeled as an additional event* whose rate depends on the tumor's current genotype. This means that high-visibility genotypes (those causing earlier clinical detection) are no longer conflated with genotypes that have simply had more time to accumulate events. Without this correction, cross-sectional data — where all samples are observed at a single snapshot — produces collider-biased estimates: mutations that increase tumor observability appear falsely correlated with other late events. Schill et al. 2024 is the mathematical foundation; `mhn` is its production implementation.

The demo analysis, which directly aligns with this project, applies the package to **3,662 primary lung adenocarcinomas (LUADs) from AACR GENIE** (targeted clinical sequencing, Memorial Sloan Kettering cohort), modeling 12 driver gene SNVs.

## Methods

**Model structure:** An MHN is a continuous-time Markov chain over all 2^n binary event states, parametrized by an (n+1) × n matrix. Diagonal entries encode base rates (spontaneous event accumulation). Off-diagonal entries encode rate multipliers: how the presence of event j scales the rate of event i. An additional row encodes observation rates — how each event affects the rate at which the tumor is clinically detected. This observation-event addition (relative to the 2020 formulation) is what resolves the collider bias.

**Training:** Maximum marginal log-likelihood, where the observation time is marginalized out. With state space restriction, the log-likelihood for dataset D is:

    l_D = (1/|D|) * sum_{x in D} l_x

where l_x is computed on a 2^m × 2^m submatrix restricted to states reachable from observation x (m = active events in x). GPU (CUDA) acceleration handles samples with larger m.

**Regularization options:** L1 (sparsity), L2 (shrinkage), symmetric (encourages reciprocal interaction magnitudes), or user-defined callable penalties. Cross-validation for penalty strength selection.

**Backwards compatibility:** The package can also train the 2020-era MHN (without explicit observation event modeling), enabling direct comparison of the old and new formulations on the same data.

**Input format:** Binary patient × event matrix (CSV, NumPy array, or pandas DataFrame). Each row = one patient/sample; each column = one event (gene, copy number change, etc.).

## Key Findings

### LUAD demo (3,662 AACR GENIE samples, 12 driver genes)

The trained MHN parameter matrix (Fig. 2A in the paper) reveals several biologically interpretable patterns:

- **EGFR increases observation rate by a factor of 10.91** — EGFR-mutant LUADs are detected earlier (EGFR mutations cause characteristic symptoms and are clinically actionable, driving earlier sequencing). This is precisely the kind of detection bias the observation-event formulation corrects for: without it, EGFR would appear falsely enriched among early-stage events.
- **EGFR and TP53 show mutual synergy** — each promotes the other's accumulation rate.
- **EGFR and KRAS show mutual suppression** — consistent with the known mutual exclusivity of EGFR and KRAS mutations in LUAD, which the MHN captures as a negative rate multiplier.
- **Reconstructed progression trajectories (Fig. 2B):** Most common LUAD histories begin with either TP53 or KRAS as the initiating event; EGFR frequently appears as a later event. The tree visualization displays only cancer states present in at least 3 patients; edge/symbol size scales with patient count.

### Scalability benchmark (Fig. 1)

Training benchmarked on the same 3,661-sample LUAD dataset, repeated 10 times per configuration, on a Linux server with 512 GB RAM, 30 AMD EPYC 7453 cores, and an NVIDIA A100 80 GB GPU:

- For 5–15 events: `mhn` CPU and the prior R implementation have similar run times.
- For 20–25 events: `mhn` CPU is substantially faster than R; `mhn` GPU is faster still.
- For 25 events: only `mhn`'s GPU implementation is feasible (R times out or becomes impractical).
- For 50 events: only `mhn` GPU is shown as feasible.

The paper states that in practice, analysis of datasets with **>100 events** is achievable as long as no individual sample has more than ~25 active events simultaneously (hard technical limit: 32 active events per observation).

## Relevance

This paper is directly relevant to the cbioportal project across three dimensions:

**1. Methodological alternative to frequency-based co-occurrence analysis**

The pipeline currently characterizes gene-cancer associations via mutation frequency tables and per-study correlation matrices (gene × gene co-occurrence / mutual exclusivity within studies). MHN offers a principled causal-progression alternative: instead of pairwise co-occurrence statistics, it fits a continuous-time model of event ordering and rate modification. The MHN parameter matrix explicitly separates "event A promotes event B" from "events A and B co-occur at diagnosis because they are both late-stage." This distinction is relevant to the project's interest in distinguishing clonal hematopoiesis contamination signals (early, background events) from tumor-specific driver co-occurrence patterns.

**2. Demo dataset is 3,662 AACR GENIE LUADs — our data**

The demo analysis uses the exact same data source the pipeline ingests (AACR GENIE targeted clinical sequencing). LUAD is a cancer type well-represented in cBioPortal studies and a primary target of the pipeline's cross-study aggregation. The 12-gene LUAD MHN provides a reference progression model for the gene-cancer outputs: expected interaction signs (EGFR↔KRAS mutual exclusivity, EGFR↔TP53 synergy) can be cross-validated against the pipeline's co-occurrence correlation matrices.

**3. Scalability ceiling now exceeds our panel gene count**

The pipeline's gene lists run up to ~10,000 genes (config-10k-genes.yml), but in practice meaningful MHN modeling requires pre-selecting driver events — the demo uses 12. The state space restriction means that for a focused driver set of 50–100 genes (a reasonable cancer-type-specific panel), `mhn` with GPU access is now feasible. This opens a potential downstream analysis: fitting per-cancer-type MHNs on the pipeline's most frequently mutated driver genes to extract progression ordering structure that frequency tables cannot capture.

**4. Collider-bias correction is essential for cross-sectional cBioPortal data**

All cBioPortal studies are cross-sectional: patients are sequenced at a single clinical time point, not longitudinally. The collider bias described in Schill et al. 2024 and corrected by the observation-event addition applies directly. Genes like EGFR that are clinically actionable and drive earlier tumor detection will appear in cross-sectional datasets at apparent frequencies inflated relative to their true progression-time base rates. Any naive co-occurrence or mutual exclusivity analysis on cBioPortal data inherits this bias; MHN's explicit observation model corrects it.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| MHN rate multiplier matrix | Gene-gene co-occurrence / mutual exclusivity tables | MHN is a causal-progression alternative; the pipeline computes descriptive correlations |
| Observation-event (detection rate per genotype) | Ascertainment bias in cBioPortal studies | EGFR example (10.91× detection rate) directly relevant to LUAD; other genes similarly affected |
| State space restriction (>100 events, 32 active/sample) | Pipeline gene lists (10k genes, driver subsets) | GPU-accelerated `mhn` is feasible for 50–100 driver genes per cancer type |
| EGFR–KRAS mutual suppression | Mutual exclusivity signals in gene×cancer matrices | MHN quantifies this as a directed rate multiplier, not just a co-occurrence statistic |
| AACR GENIE LUAD 3,662 samples | AACR GENIE input data | Same data source; MHN results provide a reference progression model |
| Schill 2024 collider-bias correction | Cross-sectional sampling in cBioPortal | All cBioPortal studies are cross-sectional; the bias is universal |
| Backwards-compatible 2020-era cMHN training | Reproducibility of prior analyses | Allows apples-to-apples comparison if we replicate published results |

## Limitations

- **Application note format (4 pages):** The paper is primarily a software announcement. Biological interpretation of the LUAD demo is illustrative rather than an exhaustive analysis; the 12-gene selection is for demonstration, not for maximal driver coverage.
- **32 active events per sample hard limit:** Samples with >32 simultaneous active events cannot be processed even with GPU. In practice this constrains which datasets/gene sets are tractable — hypermutator samples (high TMB) may exceed this limit if many driver genes are hit simultaneously. Pre-filtering hypermutators (already done by the pipeline's TMB annotation) would mitigate this.
- **GPU required for large event sets:** Beyond ~25 events, the CPU implementation becomes infeasible. This is a computational infrastructure dependency; the pipeline currently runs on CPU only.
- **Binary event representation:** The model as implemented treats events as binary (present/absent). Copy number variation, multi-hit events, or allele-specific information require collapsing to a binary call, potentially losing information about event dosage.
- **Cross-sectional data only:** MHNs infer temporal ordering from co-occurrence statistics across patients; they do not use within-patient longitudinal data. The resulting ordering is a population-average inference, not validated against individual patient tumor evolution.
- **No explicit correction for panel size variation:** Different GENIE panels capture different gene subsets. Genes absent from a given panel are not observed as zero-events; they are simply missing. Whether `mhn` accounts for panel-specific missingness is not discussed in this application note (see Schill et al. 2024 for details).

## Model / Tool Availability

- **Package:** `mhn`, available on PyPI; install in this project with `uv add mhn`. MIT
  License.
- **GitHub:** https://github.com/spang-lab/LearnMHN
- **Documentation:** https://learnmhn.readthedocs.io/en/latest/index.html
- **Tutorial:** Jupyter notebook available on GitHub for guided exploration.
- **Demo data:** AACR GENIE LUAD dataset underlying the figures is available at the GitHub repository.
- **Predecessor R implementation:** Schill et al. 2020 R package (slower; superseded for large event sets).

## Follow-up

- Read **Schill et al. 2024** (the mathematical companion) to understand the full observation-event formulation and its collider-bias derivation — this is the theoretical foundation that `mhn` implements. The paper is cited as: Schill R, Klever M, Lösch A et al. "Overcoming Observation Bias for Cancer Progression Modeling." Springer Nature, 2024, 217–34. DOI: 10.1007/978-1-0716-3989-4_14.
- Assess whether fitting a per-cancer-type MHN on the top-N driver genes from the pipeline's `gene_cancer_study_ratio_annotated.feather` is computationally feasible and scientifically valuable. Start with LUAD (the demo cancer type) using the pipeline's GENIE-derived gene×sample matrix.
- Consider whether the pipeline's existing mutual-exclusivity correlation outputs (gene×gene per-study correlation matrices) can be used as a first-pass sanity check against MHN interaction signs: negative rate multipliers should correspond to negative co-occurrence correlations, positive rate multipliers to positive correlations.
- Evaluate whether pre-filtering hypermutator samples (already flagged by the `is_hypermutator` column from the TMB annotation pipeline) before MHN training would make the 32-active-events-per-sample limit non-binding for the cBioPortal data.
- Check whether AACR GENIE v9.1 (which the pipeline uses) differs substantially from the GENIE release used in this paper (AACR-GENIE-Consortium Release 13.1-public, 2023) and whether the LUAD sample count (3,662) is specific to that later release.
