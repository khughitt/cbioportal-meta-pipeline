---
id: paper:Harlapur2026
type: paper
title: Hierarchical organization in sparse gene regulatory networks shapes structural
  coherence and emergent regulatory coordination
status: active
ontology_terms: []
source_refs:
- cite:Harlapur2026
related: []
created: '2026-04-25'
updated: '2026-04-25'
---

# Hierarchical organization in sparse gene regulatory networks shapes structural coherence and emergent regulatory coordination

- **Authors:** Pradyumna Harlapur, Rahul Jagadeesan, Andre Sanches Ribeiro, Claus Kadelka, Mohit Kumar Jolly
- **Year:** 2026
- **Journal:** bioRxiv (openRxiv preprint, posted 2026-02-05)
- **DOI/URL:** https://doi.org/10.64898/2026.02.04.703680
- **BibTeX key:** Harlapur2026
- **Source:** PDF

## Key Contribution

Introduces the **coherence matrix**, a topology-based framework that quantifies the consistency of regulatory influence between all gene pairs in a directed, signed gene regulatory network (GRN) by aggregating information across all direct and indirect paths (walks). From the coherence matrix a scalar **structural coherence** is derived — the mean within-team coherence — that predicts how robustly a network motif preserves coordinated gene groups (teams) as connectivity is reduced. The central finding is that hierarchical organization in biological GRNs (a sparse input layer, a dense middle layer enriched for feedback and transcription factors, and a broad effector output layer) acts as a structural buffer that limits fragmentation of regulatory coordination even at low network densities, and that this buffering is independent of the local motif's intrinsic coherence.

## Methods

- **Coherence matrix construction.** For a signed, directed adjacency matrix A ∈ {-1, 0, +1}^(N×N), the coherence C_ij between a source node j and target node i is computed as the ratio of the net signed walk influence (positive walks minus negative walks) to the total walk count, summed over all walk lengths and normalized. Values near +1 indicate exclusively activating influence; near -1 exclusively inhibitory; near 0 a balanced or disconnected pair (NaN when truly disconnected, distinguishing disconnection from regulatory conflict).
- **Synthetic Erdős–Rényi (ER) networks.** All 18 non-isomorphic 2- and 3-node motifs (with self-activation and complete directed structure) were each scaled 10x–50x per node and density swept from 10% to 100% in 5% increments; 20 replicates per condition. Mean normalized communicability (matrix-exponential of |A|, normalized against a fully connected network of equal size) used as a density-agnostic proxy for connectivity.
- **Hierarchical (HI) networks.** Artificial networks built to recapitulate the empirical three-layer architecture (5% input, 5% middle, 90% output; feed-forward block structure with middle-to-middle density fixed at 100%, middle-to-output at 85%, input-to-middle at 50%); same scale and replicate scheme as ER.
- **Whole-organism GRNs.** Six organism-level directed, signed GRNs sourced from the Abasy Atlas (meta-curated, standardized annotations). Coherence matrices computed per organism; nodes classified as input (outgoing coherence only), output (incoming coherence only), or middle (both).
- **Transcriptomic validation.** Coherence-based predictions compared against *E. coli* iModulons (ICA-derived expression modules). Sign agreement assessed via precision/recall on pairwise gene-interaction signs within modules; magnitude agreement assessed via Spearman rank correlation of pairwise coherence values against ICA weight products.

## Key Findings

1. **Motif structural coherence governs robustness to sparsification.** High-coherence motifs (e.g., all-activating 2_2_0, SC = 1.0) preserve team count across all densities and scales; low-coherence motifs (e.g., 3_6_1, SC = 0.43) fragment immediately at high densities, following convex trajectories. Intermediate motifs display concave or linear fragmentation profiles. Network scale modulates the rate but not the mode of fragmentation.
2. **Biological GRNs are organized in three coherence-defined layers.** Across six whole-organism GRNs, the coherence matrix recovers the canonical input / middle / output hierarchy: on average 4.7% ± 4.1% input genes, 8.5% ± 3.2% middle genes, and 86.8% ± 7.0% output genes. The middle layer has the highest inter-layer connection density and contains the strongly connected components; all feedback loops are confined to it.
3. **The middle layer is the functional integration core.** GO enrichment confirms functional specialization: input layer enriched for signal transduction (phosphorelay, two-component systems); middle layer enriched for DNA-binding transcription factors and regulatory integration; output layer enriched for metabolic/enzymatic effector processes.
4. **Hierarchical architecture attenuates density-driven fragmentation.** HI networks never reach negative structural coherence (indicative of total regulatory conflict) even at maximum sparsification (effective density ~8.7%), whereas ER networks routinely cross into negative regimes at low densities. HI networks exhibit significantly fewer teams and narrower coherence distributions, indicating constrained, buffered regulatory structure. Notably this stabilization occurs even for intrinsically low-coherence motifs — hierarchy compensates for local incoherence.
5. **Coherence predicts transcriptomic sign of coordinated gene pairs.** Against *E. coli* iModulons, coherence achieves high precision and recall (high F1 scores across most modules) for predicting whether gene pairs contribute concordantly (+) or antagonistically (-) to a functional module. Magnitude correlations are weaker and context-dependent: modules driven by global stress responses or gene knockouts show poor coherence–expression alignment, reflecting the limits of static topology.

## Relevance

This paper connects directly to the cbioportal project's use of **canalization** as a conceptual lens for cross-study mutation patterns (see `spec:research-question`).

**Driver-gene robustness and recurrent gene-cancer associations.** The coherence framework formalizes why certain genes are structurally resistant to perturbation: genes occupying the dense middle layer of GRNs lie at the intersection of many activating feedback loops and thus have high incoming and outgoing coherence. Mutating such genes — classic driver candidates like transcription factors and signaling hub regulators — disrupts not just one regulatory relationship but the coordinated consistency across a large regulatory neighborhood. This provides a network-topological mechanism for why driver gene mutations recur robustly across independent cBioPortal studies (hypothesis 1 of `spec:research-question`): these genes sit in positions of high structural coherence where loss of function has maximal downstream regulatory reach.

**Hypermutator phenotypes.** The paper's finding that low-coherence motifs are intrinsically fragile but that hierarchy rescues them is relevant to hypermutator interpretation. A hypermutator phenotype — with mutations distributed genome-wide — may effectively reduce the sparse connectivity of regulatory networks (by disabling many regulatory genes stochastically). The HI network result predicts that hierarchically buffered systems (normal cells) resist coordination loss under this assault; hypermutators that additionally hit middle-layer coherence hubs (e.g., TP53, DNA damage response TFs) would exhibit disproportionate loss of regulatory coherence.

**Cross-study aggregation rationale.** The team / coherence decomposition suggests that genes within the same high-coherence regulatory team should co-mutate or be mutually exclusive across cancers. This is a testable structural prediction: gene pairs with high pairwise coherence values in known cancer-relevant GRNs should show correlated mutation frequencies in the cbioportal cross-study matrices.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Structural coherence | Canalization / regulatory robustness | Formalizes canalization: high coherence = buffered against perturbation |
| Coherence team | Co-mutating gene module | Teams of mutually activating genes; predicts co-mutation patterns |
| Middle layer (dense, feedback-enriched) | Driver gene hub | Classic driver TFs occupy this structural position |
| Sparsification / density reduction | Hypermutation load | Stochastic mutation of regulatory edges maps to density reduction |
| Negative structural coherence | Regulatory conflict / synthetic lethality | Complete loss of coordinated activation |
| iModulon validation | Cross-study mutation pattern validation | Analogous logic: topology predicts functional gene groupings |

## Limitations

- The coherence matrix is derived from **static network topology** only; it cannot capture condition-specific rewiring, context-dependent edge weights, or the dynamic inactivation that occurs during global stress responses or gene knockouts. This is explicitly acknowledged as the reason for reduced iModulon alignment in stress-response contexts.
- The six whole-organism GRNs are all **bacterial** (sourced from Abasy Atlas). Generalization to eukaryotic (especially cancer) GRNs — which have more complex chromatin-level regulation, post-translational control, and far larger gene sets — is assumed but not demonstrated.
- The coherence matrix formulation uses **walks** (allowing node/edge revisits) rather than simple paths. This is computationally convenient (matrix exponentiation) but means very long walks can dominate the coherence value in a way that may not reflect biological signal propagation.
- Binary edge signs (+1 activation, -1 inhibition) ignore graded regulatory strengths and condition-dependent sign flips (e.g., context-dependent co-activators that become repressors).
- Motif analysis is limited to **2- and 3-node** motifs with complete directed graphs and mandatory self-activation. Real regulatory subgraphs are often incomplete or involve partial connectivity.

## Model / Tool Availability

Code availability is not stated in the preprint. Data sourced from Abasy Atlas (publicly available) and *E. coli* iModulons (publicly available via the iModulon database). No standalone tool or package is released.

## Follow-up

- Harlapur et al. cite Salgado et al. (Abasy Atlas) [ref 31] and the iModulon work [ref 18] — both worth reading for the underlying GRN and transcriptomic resources.
- The structural balance theory papers cited [refs 36-40] and the influence matrix work [refs 26-27] are the theoretical predecessors of the coherence matrix — relevant for understanding the formal lineage.
- **Project-specific question:** Do gene pairs with high pairwise coherence in known cancer GRNs (e.g., ENCODE TF networks, OmniPath) show correlated or mutually exclusive mutation frequency patterns in the cbioportal cross-study feather tables? This would validate coherence as a predictor of co-mutation structure.
- **Project-specific question:** Can the three-layer (input/middle/output) decomposition be applied to a cancer-specific GRN to categorize the driver genes captured in `bailey2018_table_s1.xlsx`? Prediction: Bailey drivers should be enriched in the middle layer.
