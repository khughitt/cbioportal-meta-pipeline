---
type: paper
title: Collateral mutagenesis funnels multiple sources of DNA damage into a ubiquitous
  mutational signature
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Spisak2025
ontology_terms:
- mutational signatures
- SBS5
- collateral mutagenesis
- translesion synthesis
- DNA repair
- DNA damage
- somatic mutation
datasets: []
source_refs:
- cite:Spisak2025
related: []
---

# Collateral mutagenesis funnels multiple sources of DNA damage into a ubiquitous mutational signature

- **Authors:** Natanael Spisak, Marc de Manuel, Molly Przeworski
- **Year:** 2025
- **Journal:** bioRxiv preprint (posted 2025-08-28 / September 1, 2025)
- **DOI/URL:** https://doi.org/10.1101/2025.08.28.672844
- **BibTeX key:** Spisak2025
- **Source:** PDF

## Key Contribution

This paper proposes and provides empirical support for a mechanistic explanation for SBS5, the
most ubiquitous and age-correlated mutational signature across human tissues. The authors argue
that SBS5 is the footprint of "collateral mutagenesis" — errors introduced by error-prone
polymerases at sites *neighboring* a DNA lesion (not at the lesion itself) during either
translesion synthesis (TLS) or DNA repair gap-filling (NER). Because multiple damage types
recruit the same funneling polymerase, diverse sources of DNA damage all converge on the same
trinucleotide-context spectrum, explaining why SBS5 is seen in contexts ranging from
post-mitotic neurons to male germline cells exposed to no known exogenous mutagen. The key
empirical finding is that SBS5 mutation counts co-vary with damage-specific signature burdens
(SBS4/smoking, SBS7/UV, SBS18/oxidative damage) across tumors and non-cancerous cells, and that
SBS5 mutation rates correlate with NER repair rates along the genome in a manner consistent with
collateral errors rather than simple replication infidelity.

## Methods

**Mathematical model.** The authors extended a prior stochastic model of mutagenesis (Gao et al.
2016; Spisak et al. 2024) to include limited repair-enzyme resources and bursty damage
occurrence. The model distinguishes two mutation-producing modes: (1) replication across
unrepaired lesions (TLS-type, dominant when cell divisions are frequent and damage is high) and
(2) errors made by polymerases during the repair process itself at any cell-cycle phase
(repair-error mode, dominant in slowly dividing or post-mitotic cells). Both modes can
produce a "collateral" spectrum shaped by the error profile of the recruited polymerase rather
than by the chemistry of the lesion.

**Empirical analyses — tumors.** Signature attributions from PCAWG (N = 2,658 whole-genome
tumors, 14 cancer types) were computed per cell using Signet and an alternative deep-learning
decomposition (Colome et al.). Semipartial R² was used to quantify the unique variance in SBS5
attributable to each damage-specific signature after controlling for age, SBS1 (a proxy for
cell divisions), tumor ploidy, and purity. 27 well-powered comparisons were considered; 20
(74%) were statistically significant after Bonferroni correction.

**Empirical analyses — non-cancerous cells.** Datasets from single-cell-derived neurons, glia,
bronchial epithelial cells (smokers vs non-smokers), skin microbiopsies (UV-exposed), colonic
epithelium, and three-generation germline pedigrees were analyzed. Linear mixed-effects models
with individual as a random effect were used throughout to control for inter-individual
confounding. Signature attributions used sigprofilerreassignment (Diaz-Gay et al.).

**Genomic distribution.** NER rates (r_NER) along the genome were estimated in 5 Mb windows by
fitting the exponential decay of UV-induced BPDE lesions measured at multiple time points in a
human cell line (Hu et al. 2017). SBS4 and SBS5 mutation rates were regressed against r_NER
windows; SBS5 rates were compared between smokers and non-smokers to dissect TLS vs repair-error
contributions.

**Clustered mutations.** Mutation clusters (pairs of point mutations separated by <100 bp) in
lung and liver of smokers were identified and their composition (SBS4 vs SBS5+SBS40) was
quantified. The positional asymmetry of SBS5 mutations relative to C:G→A:T anchor mutations
was used to infer directionality consistent with TLS extension errors.

## Key Findings

1. **SBS5 increases with damage-specific signatures across tissues (the "funneling" result).**
   In PCAWG, SBS5 burden is significantly correlated with tobacco-smoke signatures (SBS4, DBS2,
   ID3) in lung and liver cancers, UV signatures (SBS7b/d, DBS1, ID13) in melanoma, and oxidative
   damage signatures (SBS18) in adenocarcinomas, even after controlling for age and SBS1. In
   lung and liver cells of smokers (non-cancerous), SBS4 explains ~65% of the variance in SBS5
   counts; ~58% in liver cells. These correlations are not explained by shared age effects and
   persist in linear mixed models with individual as a random effect.

2. **Mutation clusters provide direct evidence of TLS as one SBS5 source.** Approximately 0.5%
   of point mutations in lung and liver of smokers occur in clusters of nearby mutations
   consistent with TLS extension errors (spacing <100 bp). Within these clusters, SBS4 accounts
   for 10–12% of mutations and SBS5+SBS40 for 22–64%. The positional asymmetry of SBS5 cluster
   members relative to SBS4 anchor mutations is consistent with replication direction, supporting
   a model in which TLS polymerases bypass a BPDE lesion and then introduce a collateral error
   downstream.

3. **SBS5 also arises from repair errors, and the relative contribution is cell-type dependent.**
   SBS5 mutation rates across genomic windows correlate inversely with NER repair rates (r_NER)
   in smokers — as predicted if TLS (which depends on unrepaired lesions) is a major source —
   but a non-zero baseline B~0 remains even in high-repair regions. In non-smokers and in
   post-mitotic neurons, the inverse correlation with r_NER is very weak (R² = 1–38%), and the
   non-zero intercept is relatively larger, indicating repair errors dominate. In colonic
   epithelial cells (rapidly dividing), both TLS and repair errors each contribute roughly half.

4. **Consistent model predictions across the cell-type spectrum.** Neurons (post-mitotic, low
   cumulative damage) are predicted and observed to accumulate SBS5 mainly through repair errors.
   Germline cells show a similarly weak r_NER dependence. Glia and colonic epithelia, with
   moderate to high division rates, show a stronger r_NER dependence, consistent with a TLS
   component. Overall, the rate-of-accumulation of SBS5 mutations with age ranges from ~0.3
   (maternal germline) to ~15 (glia) per haploid genome per year, a ~50-fold spread compatible
   with the model.

5. **SBS5 behaves as a single process, not a superposition.** Across cell types, SBS5 does not
   decompose into linear sub-components (unlike SBS40), accumulates at varying age-rates without
   the tight co-synchronization that a superposition would require, and shows tissue-specific
   genomic distributions (neurons: enriched in open/transcribed; glia: reversed) consistent with
   a single polymerase whose recruitment probability varies by chromatin context.

6. **Candidate funneling polymerase.** The authors propose that polymerase zeta (Polζ), known
   to participate in TLS extension and in NER gap-filling, is the most plausible candidate, given
   its diffuse error spectrum, weak strand asymmetry consistent with SBS5, and prior evidence
   that it accounts for a substantial fraction of spontaneous mutations in human cell lines.

## Relevance

**Direct relevance to h08 (agnostic covariate ↔ signature-exposure association).**

- **Positive-control framing (H08a):** This paper provides the mechanistic justification for
  why smoking→SBS4 and UV→SBS7 should correlate with SBS5 burden, not merely with their own
  damage-specific signatures. The SBS5 funneling model predicts that any cross-study association
  analysis will find SBS5 co-varying with SBS4 in lung/liver and SBS7 in skin — a weaker but
  real positive-control signal on top of the primary SBS4/SBS7 recovery tests. This is directly
  useful when designing the H08a positive control: correlations between SBS5 and known-exposure
  signatures are now expected and mechanistically interpretable, not noise to be filtered.

- **H08b (discovery / novel SBS5 aetiology):** The paper explicitly notes that SBS5's aetiology
  is partially explained by cumulative damage from known exposures but that a substantial
  age-dependent fraction remains in non-exposed cell types (neurons, germline). The repair-error
  mode means SBS5 may associate with expression of repair genes (NER pathway members) or
  with inflammation/DNA-damage-response modules even in cancer — precisely the kind of
  expression-covariate association that H08b seeks to surface. The authors' Figure 3A showing
  SBS18 (oxidative damage) associations with SBS5 in adenocarcinomas, independent of cell
  division proxies, is an example of a novel aetiology link recoverable by agnostic covariate
  association.

- **Cross-study aggregation context:** In the cbioportal pipeline, SBS5 will be a major
  component of per-study mutation spectra across nearly all cancer types. The "funneling" result
  means that cross-study variance in SBS5 burden reflects heterogeneity in cumulative DNA damage
  from multiple distinct exogenous and endogenous sources — not just replication errors. This
  implies that SBS5 burden in the aggregated gene×cancer matrix is a noisy composite of many
  upstream inputs, which should be modeled (or conditioned on) explicitly when interpreting
  mutation-frequency patterns, particularly for comparisons between slow- and fast-dividing
  tumor subtypes.

- **Signature decomposition:** The paper validates the robustness of SBS5 as a COSMIC signature
  (cosine similarity 0.94–0.99 in cells where it dominates), supporting its use in restricted
  COSMIC-based decomposition (as in `run_restricted_sigprofiler_assignment.py`) while cautioning
  that in contexts with low mutation counts or co-occurring flat signatures (e.g., SBS40), the
  attribution is more ambiguous.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| SBS5 "funneling" signature | COSMIC SBS5 (restricted assignment output) | Directly the same; SBS5 attribution from pipeline will carry this interpretation |
| Damage-specific signatures (SBS4, SBS7, SBS18…) | COSMIC signatures used in H08a positive controls | SBS4 (smoking→lung), SBS7 (UV→skin) are pre-registered H08a arms |
| Semipartial R² of damage-specific sig on SBS5 | Signature exposure association statistic | Analogous to h08's per-sample regression of signature exposures on covariates |
| NER repair rate r_NER as genomic covariate | Not currently in pipeline | Would require external NER rate maps |
| TLS vs repair-error mode by cell type | Not modeled in pipeline | Relevant when interpreting inter-study SBS5 variance |
| Polζ as funneling polymerase | Not currently used | Downstream mechanistic interpretation only |

## Limitations

- **Preprint.** Not yet peer-reviewed at time of writing; main findings are quantitative
  and the methods are detailed, but some conclusions (particularly about the identity of the
  funneling polymerase) rest on indirect inference.
- **Bulk sequencing for tumor analyses.** The PCAWG data capture high-frequency clonal
  mutations; pre-malignant cells may have different relative SBS5 contributions. The authors
  acknowledge this limitation explicitly.
- **Signature attribution uncertainty.** SBS5 has a relatively flat trinucleotide profile,
  making attribution more susceptible to contamination by other flat signatures (SBS3, SBS40).
  The authors handle this carefully with sensitivity analyses but acknowledge residual uncertainty
  in contexts with low mutation counts.
- **Repair rate proxies.** NER rates are estimated from a single human cell line (HCT116);
  applicability to other tissues is assumed but not directly demonstrated.
- **Causality.** The correlations between damage-specific signatures and SBS5 are consistent
  with collateral mutagenesis but could in principle reflect shared upstream processes (e.g.,
  inflammation driving both SBS5 and SBS4/18) rather than a direct mechanistic link. The authors
  note this and present the mouse DMBA model as partial causal evidence.
- **Alternative flat signatures.** SBS40, which also accumulates with age, is hard to
  distinguish from SBS5 in low-mutation-count contexts; the paper treats SBS5+SBS40 jointly in
  some analyses and does not fully resolve whether SBS40 has a distinct aetiology.

## Model / Tool Availability

No software tool released. The mathematical model is described in full in Methods (Table 1;
stochastic differential equation framework). Simulation code and analysis scripts are not
explicitly linked in the preprint.

## Follow-up

- **Papers to read next:**
  - Ganz et al. (2024) — contrasting somatic mutation patterns in aging neurons and
    oligodendrocytes (provides the neuronal SBS5 age-rate data used here).
  - Colome et al. (2023 bioRxiv) — the neural-network signature decomposition used as
    sensitivity analysis; relevant because it was specifically designed to handle flat
    signatures like SBS5.
  - Anderson et al. (2024, Nature) — strand-resolved mutagenicity of DNA damage and repair;
    provides the cluster mutation evidence cited here.
  - Yoshida et al. (2020, Nature) — tobacco smoking and somatic mutations in human bronchial
    epithelium; the non-cancerous lung dataset used in Figures 3B and 4.

- **Questions this raises for the project:**
  - If SBS5 accumulates from repair errors in non-dividing cells but from TLS in rapidly
    dividing cells, how should we interpret cross-cancer-type differences in SBS5 burden in
    the cbioportal aggregated matrix? Should SBS5 exposure estimates be normalized differently
    by cancer type's typical cell division rate?
  - The paper shows that SBS5 co-varies with SBS4 even after controlling for SBS1 (a proxy for
    cell divisions). Does this mean that within-cancer-type association tests in H08a should
    include SBS1 as a nuisance covariate when testing SBS4 → SBS5 (not just SBS4 → itself)?
  - The funneling model implies that expression of NER pathway genes or Polζ (POLZ) could
    associate with SBS5 — a directly testable H08b candidate. POLZ expression vs SBS5 burden
    within lung adenocarcinoma is a concrete first test.
