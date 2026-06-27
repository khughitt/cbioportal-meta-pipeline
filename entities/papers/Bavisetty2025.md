---
type: paper
title: 'Attractors are less stable than their basins: Canalization creates a coherence
  gap in gene regulatory networks'
status: active
created: '2026-04-25'
updated: '2026-04-25'
id: paper:Bavisetty2025
ontology_terms: []
source_refs:
- cite:Bavisetty2025
related: []
---

# Attractors are less stable than their basins: Canalization creates a coherence gap in gene regulatory networks

- **Authors:** Venkata Sai Narayana Bavisetty, Matthew Wheeler, Claus Kadelka
- **Year:** 2025
- **Journal:** bioRxiv (preprint; posted November 8, 2025)
- **DOI/URL:** https://doi.org/10.1101/2025.11.06.687062
- **BibTeX key:** Bavisetty2025
- **Source:** PDF

## Key Contribution

This paper formalizes and empirically validates *attractor coherence* — the probability that a single-gene perturbation of a mature cell-type state (attractor) does not cause phenotype switching — and distinguishes it from the previously used *basin coherence* (average stability of all states leading to an attractor). Analyzing 122 expert-curated biological Boolean network (BN) models, the authors demonstrate a striking paradox: attractors representing mature cell types are consistently *less* stable than the transient states along the developmental trajectories that approach them (AUC:BC = 0.853 vs AUC:AC = 0.825 across 95 biological BN models with N ≤ 64). Large-scale random-network simulations (10,000 networks each ensemble) show this "coherence gap" is mechanistically driven by canalization — individual regulatory inputs that can override others — which disproportionately stabilizes transient states and positions attractors closer to basin boundaries. The gap magnitude is almost perfectly predicted by network bias (Spearman's ρ = −0.997).

## Methods

- **Data:** 122 published, expert-curated biological Boolean network models (from a meta-analysis by Park et al. 2023), spanning 5–342 nodes; two analysis tiers: N ≤ 20 (exact, n = 42) and N ≤ 64 (sampled, n = 95).
- **Coherence definition:** Per-state coherence ψ_x = fraction of single-bit-flip neighbors that remain in the same basin of attraction. Basin coherence ψ_B = mean over all states in basin B. Attractor coherence ψ_A = mean over attractor states only.
- **Coherence gap:** ΔAUC = AUC:BC − AUC:AC, integrated over basin sizes with a uniform weighting to remove confounding from basin size distribution; random baseline = 0.5 for both measures.
- **Random ensembles:** 10,000 random 12-node BNs per ensemble; varied degree (3–7) and canalizing depth (non-canalizing k=0, canalizing k=1, nested canalizing k=n). Used BoolForge Python package for generation and exact analysis; for large biological BNs, 1000 random samples from state space for unbiased basin/attractor estimates.
- **Canalization metrics:** Canalizing depth, canalizing strength, input redundancy — all highly correlated; results robust to metric choice.
- **Null models:** For each biological BN, 100 random null models preserving wiring diagram but randomizing update rules; confirmed biological networks exhibit significantly higher coherence than topology-matched nulls (p = 9×10⁻⁶, n = 42).

## Key Findings

1. **Attractors are less stable than their basins in biological networks.** Across 597 attractors in the 42 small biological BN models, attractor coherence was significantly lower than basin coherence (sign test p = 2×10⁻¹¹). This holds even for large models (AUC:BC = 0.853 vs AUC:AC = 0.825).

2. **Canalization creates the coherence gap.** Without canalization, non-canalizing networks show ΔAUC ≈ −0.005 to −0.008 (essentially no gap). Canalizing networks show ΔAUC = 0.031–0.034; nested canalizing networks show ΔAUC = 0.059–0.061. Biological BNs — dominated by nested canalizing functions — inherit this gap.

3. **Bias is the proximal predictor.** Basin coherence is primarily governed by sensitivity (Spearman's ρ = −0.629 with AUC:BC); attractor coherence is governed by bias (ρ = 0.983 with AUC:AC). The coherence gap is almost perfectly predicted by standardized bias p(1−p): Spearman's ρ = −0.997 (Fig. 10F). Higher bias → larger coherence gap.

4. **Mechanistic explanation.** In highly biased and canalized networks, many nodes are "frozen" (always 0 or always 1) across attractors, clustering attractors in similar regions of state space. This reduces mean Hamming distance between attractors, flattening the ridges separating basins *near attractor locations* while maintaining high absolute coherence in mid-basin transient states. Small perturbations at attractors can therefore more easily push across basin boundaries.

5. **Revised Waddington landscape.** Canalization carves deep protective valleys (robust developmental trajectories) but simultaneously flattens ridges near valley floors (attractors), making mature phenotypes more responsive to switching signals when multiple fates coexist. The landscape is not simply deepest at the floor; it is deepest mid-trajectory.

6. **Cancer implications.** In normal tissues, one dominant attractor minimizes the functional relevance of the coherence gap. In cancer, where mutations can create multiple partially stable attractors (epithelial, mesenchymal, hybrid intermediates), the coherence gap predicts enhanced phenotypic plasticity: cancer cells more readily undergo EMT, dedifferentiation, or therapy-induced state switching.

7. **Reprogramming implications.** Differentiated cells near basin boundaries may be more efficiently reprogrammed than cells mid-differentiation — a counterintuitive prediction consistent with transcription-factor cocktail reprogramming (Yamanaka-type).

## Relevance

This paper is primarily a conceptual/mechanistic contribution to gene regulatory network theory, but it offers a precise formal lens for the cbioportal project's interest in canalization:

- **spec:research-question:** The project asks which gene-cancer associations recur robustly across independent studies. The coherence gap framework suggests that driver genes operating in *canalized* regulatory contexts (those with high bias and canalizing depth) govern attractors that are, paradoxically, the most susceptible to perturbation-driven phenotype switching. This implies that the most recurrently mutated cancer drivers may be those whose mutations efficiently breach attractor boundaries in canalized networks — connecting observed cross-study mutation frequency to an underlying network-topological mechanism.

- **Hypermutator and driver-gene context (AGENTS.md):** The pipeline's hypermutator annotation distinguishes high-TMB samples (POLE/POLD1 hotspots, MSI-H, GMM upper mode). The coherence gap concept suggests a complementary biological framing: hypermutators accumulate many perturbations across the genome, increasing the probability of breaching attractor boundaries regardless of which specific gene is hit. This could explain why hypermutators tend to activate non-canonical pathways, not just classical drivers.

- **Cross-study recurrence:** Gene-cancer associations that recur across many independent cBioPortal studies likely represent perturbations at the most influential nodes of canalized networks — those with the highest basin-boundary proximity at the attractor. The paper's finding that bias nearly perfectly predicts the coherence gap (ρ = −0.997) suggests that genes regulating highly biased (asymmetrically expressed) regulatory circuits will be disproportionately represented among recurrent drivers.

- **EMT / cancer plasticity (AGENTS.md mention of epithelial-mesenchymal transition):** The authors explicitly invoke EMT as a paradigm case where the multi-attractor landscape makes the coherence gap biologically relevant — directly applicable to interpreting cancer-type clusters in the pipeline's gene × cancer frequency matrices.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Attractor (Boolean network) | Stable cancer phenotype / cell type | Each cancer type in cBioPortal corresponds loosely to one attractor |
| Basin of attraction | Developmental / evolutionary trajectory toward a cancer phenotype | All genomic states that converge to a given cancer phenotype |
| Attractor coherence (ψ_A) | Driver-gene perturbability of a mature tumor cell type | Low attractor coherence → single-gene mutation more likely to cause phenotype switch |
| Coherence gap (ΔAUC) | Differential plasticity of mature vs. intermediate tumor states | Relevant to hypermutator vs. low-TMB tumor behavior |
| Canalization | Regulatory buffering (see topic:clonal-hematopoiesis-contamination for CH context) | Canalized genes override others — maps to dominant oncogenic regulators |
| Network bias | Output asymmetry of regulatory logic | High-bias circuits → clustered attractors → larger coherence gap |
| Nested canalizing function (NCF) | Dominant regulatory logic in curated biological BN models | Most biological update rules are NCFs; relevant to driver-gene hierarchy |

## Limitations

- Model is Boolean (binary gene states); quantitative gene expression dynamics, post-translational modifications, and metabolic constraints are abstracted away. Extensions to continuous or multi-state models could reveal additional nuances.
- Synchronous update scheme used throughout; asynchronous update could alter stability gradients within basins.
- The ΔAUC metric removes basin-size confounding but may overestimate the coherence gap in highly ordered networks where mid-sized basins (which show the largest gaps) are rare.
- No rigorous mathematical proof connecting bias to attractor boundary proximity; the empirical finding (ρ = −0.997) is compelling but a theoretical derivation is lacking.
- The 122 biological BN models, while expert-curated, represent a biased sample of well-studied signaling pathways (e.g., cell cycle, apoptosis, EMT) and may not generalize to all cancer regulatory contexts.
- The paper is a preprint (bioRxiv, November 2025) and has not yet undergone peer review.

## Model / Tool Availability

- All code freely available: https://github.com/ckadelka/AttractorCoherence
- Python package BoolForge used for BN generation and exact analysis.

## Follow-up

- Read the Park et al. (2023) meta-analysis of 122 biological BN models cited as reference [10] — this is the dataset underlying the key empirical claims.
- Consider whether the canalizing depth / bias framing maps onto Bailey 2018 [@Bailey2018] driver gene classes: do Bailey drivers tend to regulate high-bias, nested-canalizing circuits?
- The Huang et al. (2005) paper on cell fates as high-dimensional attractor states (Phys Rev Lett 94:128701) is foundational context cited here.
- Compare with other canalization papers in this batch for synthesis.
