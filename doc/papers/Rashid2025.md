---
id: paper:Rashid2025
type: paper
title: Operating principles of interconnected feedback loops driving cell fate transitions
status: active
ontology_terms:
- gene-regulatory-network
- feedback-loop
- multistability
- cell-fate
- canalization
- epithelial-mesenchymal-transition
source_refs:
- cite:Rashid2025
related: []
created: '2026-04-25'
updated: '2026-04-25'
---

# Operating principles of interconnected feedback loops driving cell fate transitions

- **Authors:** Mubasher Rashid, Abhiram Hegade
- **Year:** 2025
- **Journal:** npj Systems Biology and Applications, 11:2
- **DOI/URL:** https://doi.org/10.1038/s41540-024-00483-w
- **PMCID:** PMC11693754
- **BibTeX key:** Rashid2025
- **Source:** PDF

## Key Contribution

The paper identifies design principles governing how interconnected positive feedback loops (PFLs) — which the authors term **high-dimensional feedback loops (HDFLs)** — shape the number and nature of stable cell states (steady-state distribution, SSD). It shows that three topological families of HDFLs (serial, hub, cyclic) differ predictably in how many stable phenotypes they support, and that autoregulation (self-activation) "liberates" network dynamics from strict topological control by shifting the SSD toward higher-order stability regardless of topology. It further demonstrates that converting inhibitory interactions to activating ones (edge sign reversal, ESR) is a more effective strategy than edge deletion (ED) for collapsing a multistable network to a monostable one — a finding with direct therapeutic implications for blocking EMT-driven phenotypic heterogeneity in carcinomas.

## Methods

- **Mathematical model:** Continuous ODE framework using shifted Hill functions for each gene interaction, implemented in the RACIPE (RAndom CIrcuit PErturbation) computational platform. Each network was sampled with 10,000 random parameter sets drawn from log-uniform distributions to capture cell-to-cell biochemical variability.
- **Boolean model:** Discrete asynchronous Boolean model used for cross-validation; continuous and Boolean SSD were shown to be concordant (Jensen-Shannon divergence near zero).
- **Networks studied:** Eleven biological and synthetic HDFLs — three serial (S3, S4, S5, based on miR200/ZEB EMT circuitry and GRHL2), two hub (H4, H5), one hybrid serial-hub (SH5), three cyclic (TT, TS, TP), and complete toggle networks (C3–C10). All grounded in published EMT and CD4+T cell lineage biology.
- **State-space analysis:** Steady-state distribution (SSD) frequencies computed across mono-, bi-, tri-, tetra-, and penta/higher-order stability classes. K-means clustering with PCA projection used to identify phenotypically distinct clusters in gene-expression space.
- **Perturbation analysis:** Edge deletion (ED) and edge sign reversal (ESR) applied systematically across all networks; bifurcation analysis performed in MATLAB for S3, S4, S5, H5, and TP using basal production rate B₁ as the control parameter.

## Key Findings

1. **Topology controls state-space dimensionality.** Serial and cyclic networks favor higher-order stability (more alternative states); hub networks favor bistability. A 10-node serial network has ~20% probability for each of mono-, bi-, tri-, and tetrastability; a 10-node hub network has ~85% probability of bistability with only ~15% monostability.

2. **Same node count, different dynamics.** Topologically distinct HDFLs with equal numbers of nodes (or equal numbers of toggle switches) operate differently — the SSD peak shifts based on topology, not just size. Cyclic networks (e.g., TS) behave more like serial than hub networks.

3. **Autoregulation overrides topology.** Adding self-activations to any network shifts the SSD toward higher-order stability irrespective of topology, "liberating" dynamics from topological control. This effect scales linearly with the number of self-activated nodes.

4. **ESR > ED for monostabilization.** Converting a positive feedback loop to a negative one (ESR) is more effective at reducing multistability than simply deleting an edge (ED). Four ESRs collapse the representative SH5 network to complete monostability; four EDs achieve ~80% monostability. In networks with autoregulated genes, perturbations involving the self-activated node are disproportionately effective.

5. **Fate transitions are hysteretic and step-wise.** Bifurcation analysis confirms that fate induction signals (modeled as increasing basal production rate B₁) drive sharp saddle-node bifurcations with hysteresis. Serial networks show multistep commitment (lineages vanish sequentially with increasing B₁); hub networks show robust bistability across a wide parameter range; cyclic networks (TP) show robust multistep commitment with restricted reversibility.

6. **Complete networks operate like serial/cyclic, not hub networks.** Fully connected toggle networks (C3–C10) show increasing higher-order stability as network size grows, mirroring serial rather than hub topology behavior. Hub connectivity restricts rather than expands attractor space.

## Relevance

This paper directly informs the **canalization** conceptual lens being applied to cBioPortal cross-study mutation patterns. Several connections:

- **spec:research-question** asks which gene-cancer associations recur across independent studies — this paper frames those associations as reflections of attractor states in gene regulatory networks (GRNs). Recurrent driver gene mutations in particular cancer types may mark perturbations that shift cells into an alternative stable state (a distinct "cancer fate"), or may mark genes whose topology (hub vs. serial centrality) constrains which stable states are accessible.

- **Canalization and robustness.** The finding that hub-topology networks are intrinsically bistable (few stable states) while serial/cyclic networks support many alternative states maps cleanly onto canalization: high-centrality hub nodes constrain the phenotypic state space, exactly as Waddington's canalization concept predicts. Genes that function as hub nodes in EMT regulatory networks should be subject to stronger purifying or directional selection pressure — and should appear as high-frequency, recurrent drivers in the pipeline's cross-study aggregation.

- **Hypermutator phenotypes.** The ESR finding (converting repression to activation breaks multistability more efficiently than edge deletion) has a somatic mutation analog: gain-of-function mutations in oncogenes (activating repressors → activators) may be more potent at locking cells into cancer-specific attractors than simple loss-of-function truncations. This could explain why the pipeline's hypermutator annotation pipeline finds certain GOF hotspots (e.g., POLE, KRAS G12) at disproportionate rates — they function as ESR-like perturbations in the underlying GRN.

- **Autoregulation and phenotypic heterogeneity.** The result that autoregulated genes "liberate" network dynamics and promote higher-order stability (more distinct cell states) connects directly to the project's paired `_inclusive`/`_exclusive` hypermutator views: genes that auto-regulate their own expression (many oncogenic transcription factors) may systematically show higher inter-study mutation rate variance, since small perturbations in their activity disproportionately expand attractor space.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Stable steady state (SSS) | Cancer-type–specific mutational attractor | Each cancer type's characteristic mutation pattern as a stable attractor |
| Serial topology (many states) | Low-centrality gene set | Genes in chains of regulation; more alternative mutation patterns possible |
| Hub topology (bistability) | High-centrality driver gene | Hub genes constrain state space; candidate recurrent cross-study drivers |
| Edge sign reversal (ESR) | Gain-of-function somatic mutation | GOF converts repressor → activator, collapsing alternative fates |
| Edge deletion (ED) | Loss-of-function somatic mutation | LOF removes a positive feedback loop; less efficient at monostabilization |
| Autoregulation | Oncogenic transcription factor auto-activation | Expands phenotypic heterogeneity; relevant to inter-study TMB variance |
| Canalization | Cross-study recurrence of gene-cancer associations | Recurrent associations = canalizing attractors stable across cohort variation |

## Limitations

- All modeling is done in a parameter-agnostic regime (random sampling); no actual transcriptomic data is fit to the models, so quantitative state-occupancy predictions are not validated against single-cell RNA-seq in specific cancer types.
- Networks are small (3–10 nodes); the authors acknowledge that these HDFLs are motifs embedded in larger "parent" networks whose complexity may substantially alter dynamics.
- Noise (stochastic dynamics) is not analyzed; all results are in the signal-driven (continuous) or asynchronous Boolean modes. Stochastic escape between attractors — directly relevant to cancer progression — is deferred to future work.
- The paper does not distinguish between germline and somatic versions of these network perturbations, which matters for the cBioPortal use case (somatic mutations only).

## Model / Tool Availability

- Raw simulation data: https://github.com/AbhiramHegade/
- MATLAB bifurcation code: https://github.com/AbhiramHegade/
- RACIPE platform (used for simulations): https://github.com/simonhb1990/RACIPE-1.0

## Follow-up

- **Kadelka & Murrugarra 2024** (ref 47 in this paper): "Canalization reduces the nonlinearity of regulation in biological networks" — *npj Syst. Biol. Appl.* 10:67. Direct treatment of canalization in GRNs; high priority read for the canalization theme.
- **Hari et al. 2022** (ref 45): EMT plasticity as emergent property of coordinated teams in regulatory networks — *eLife* 11:e76535. Connects HDFL topology to phenotypic plasticity in the EMT context.
- **Rashid et al. 2024** (ref 30 — same first author, prior work): Cooperativity in miR200-Zeb feedback network for EMT control — *Bull. Math. Biol.* 86:48.
- **Gates et al. 2021** (ref 44): "The effective graph reveals redundancy, canalization, and control pathways in biochemical regulation and signaling" — *PNAS* 118. Directly connects effective graph theory to canalization.
- Questions this raises for the project:
  - Do cross-study high-frequency driver genes (top decile of mutation ratio in the pipeline's output) preferentially occupy hub positions in known GRNs (high in-degree, high betweenness)?
  - Do gain-of-function hotspot mutations show higher cross-study recurrence than loss-of-function truncations at matched genes, consistent with the ESR > ED finding?
  - Does inter-study variance in mutation ratio correlate with whether the gene has known autoregulatory interactions (self-activation loops)?
