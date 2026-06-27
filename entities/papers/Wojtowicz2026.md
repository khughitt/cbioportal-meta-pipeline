---
type: paper
title: Toward identification of common DNA repair process in mutational signatures
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Wojtowicz2026
ontology_terms:
- mutational signatures
- DNA repair
- COSMIC signatures
- guilt-by-association
- NMF
datasets: []
source_refs:
- cite:Wojtowicz2026
related: []
---

# Toward identification of common DNA repair process in mutational signatures

- **Authors:** Damian Wójtowicz, Marcin Wierzbinski, Jan Hoinka, Roded Sharan, Teresa M. Przytycka
- **Year:** 2026
- **Journal:** bioRxiv preprint (submitted to XXX; posted January 30, 2026)
- **DOI/URL:** https://doi.org/10.64898/2026.01.29.702643
- **BibTeX key:** Wojtowicz2026
- **Source:** PDF

## Key Contribution

This paper introduces **RePrint**, a transformation of mutational signatures into conditional probability distributions that factor out DNA-damage context and capture the DNA-repair step in isolation. By computing pairwise RePrint similarity across a large collection of COSMIC, environmental-exposure, and CRISPR-knockout signatures, the authors show that RePrint clusters signatures by shared repair pathway better than raw signature (RMSD) similarity, and use a "guilt-by-association" principle to predict repair mechanisms for signatures of unknown or partially-known origin — with 5 of 6 predictions validated by literature evidence.

## Methods

**RePrint transformation.** A mutational signature is a probability distribution over 96 trinucleotide mutation categories L[X→Y]R. For each of the 32 trinucleotide contexts LXR, RePrint normalises the three substitution probabilities to sum to one, yielding conditional probabilities P(Y | X mutated, context). A small pseudocount ε is added before normalisation to handle contexts never mutated in a given signature. Formally:

> RePrint(L[X→Y]R) = S(L[X→Y]R) / Σ_{Y'≠X} S(L[X→Y']R)

The result is a vector of 32 × 3 = 96 independent conditional probabilities — one per context — decoupled from how frequently each context is damaged.

**Gold-standard cluster construction.** Three signature sources were merged: COSMIC v3.4 (human genome GRCh37), the Kucab et al. 2019 compendium of signatures from controlled in vitro environmental-mutagen exposures (PAHs, nitro-PAHs, aristolochic acid, platinum, temozolomide, etc.), and Zou et al. 2021 CRISPR-Cas9 knockouts of MMR genes (MSH6, PMS1, PMS2) and HR-related genes (EXO1, RNF168). Two cluster tiers were defined: (i) **Homogeneous clusters** — signatures known to arise from the same or very similar DNA damage plus same repair pathway (e.g., PAHs → NER; MMRd cluster with SBS6/14/15/20/21/26/44 plus knockout signatures); (ii) **Broad clusters** — multiple homogeneous clusters sharing a repair pathway (e.g., MMRd_broad = MMRd + Temozolomide; PAHs_broad = PAHs + NitroPAHs).

**Evaluation metrics.** Hierarchical clustering (complete linkage, Euclidean distance on RMSD distance matrices) was evaluated with three complementary scores:
1. Dasgupta's objective score — measures dendrogram quality independently of gold-standard labels (lower = better).
2. Intra-cluster compactness (pvclust p-values aggregated over the LCA subtree; lower = stronger cluster support).
3. Inter-cluster separation (edge-path length between LCA nodes of different clusters in the dendrogram; higher = better).

**Guilt-by-association prediction.** A query signature was predicted to share the repair pathway of a gold-standard cluster when it was the sole non-gold-standard signature in a subtree of ≥ 3 signatures. Predictions were validated against independent literature evidence.

## Key Findings

1. **RePrint outperforms raw-signature similarity across all three evaluation metrics.** Dasgupta's objective (lower is better) dropped from ~12,500 (signatures) to ~5,000 (RePrints). Intra-cluster compactness scores were lower (stronger) for RePrints in the large majority of individual clusters. Inter-cluster separation was higher for RePrints in most clusters (Fig. 4).

2. **Six guilt-by-association predictions made; five literature-validated:**
   - SBS8 → NER pathway (PAH cluster); confirmed by Jager et al. 2019 (ERCC2 knockout → SBS8-like) and Holcomb et al. 2016 (tobacco smoke inhibits NER).
   - SBS24 → ROS oxidative damage (ROS cluster); consistent with aflatoxin inducing ROS (Huang et al. 2020).
   - Ellipticine → DNA adducts/NER (NitroPAHs cluster); confirmed by Stiborova et al. 2004 (ellipticine forms covalent DNA adducts via CYP450).
   - SBS33 → MMRd (MMRd/MMRd_broad cluster); supported by Levatić et al. 2022.
   - SBS12 → MMRd (MMRd cluster); supported by Mas-Ponte et al. 2022 (obtainable by PMS2 knockout).
   - SBS34 → DNA adducts/NER (DrugsBA_broad); no validation found (remains unconfirmed).

3. **Mechanistically informative clustering insights:**
   - MMRd cluster unites SBS15/SBS26 (distinct GC-rich vs AT-rich damage biases) because they share the same mismatch repair deficiency; their raw signatures differ substantially but RePrints are nearly identical.
   - TMZ (temozolomide) clusters with MMRd signatures, consistent with TMZ inducing MMR activation.
   - SBS10a/b (POLE epsilon deficiency) cluster with MMRd; SBS10c (POLD1 deficiency) does not — suggesting POLE errors are predominantly cleared by MMR, while POLD1 proofreading engages a different pathway.
   - ROS cluster (SBS18, SBS36, SBS38) is successfully reconstructed; SBS24 (aflatoxin) joins via ROS induction.
   - PAHs cluster confirms the NER pathway for bulky aromatic adducts; SBS8's co-clustering supports its NER association.

4. **Visualization:** RePrint bar charts (conditional probability per context) expose repair-specific features invisible in raw signatures — e.g., in SBS4 approximately 60% of C/T mutations convert to A regardless of trinucleotide context, a repair signature of tobacco-smoke–induced bulky adducts.

5. **Raw signature similarity is less powerful.** RMSD-similarity guilt-by-association recovered repair assignments for only 2 of 7 query signatures; PhIP (heterocyclic amines) clustered with PAHs — a plausible but chemically distinct DNA adduct pathway.

## Relevance

**Direct relevance to hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and (agnostic covariate–signature-exposure association):**

- The hypothesis:0007 positive-control arm requires recovering known exposure→signature links (UV/SBS7, smoking/SBS4, APOBEC/SBS2-13, MMR-loss/SBS6-15-26). The RePrint framework confirms the mechanistic structure of several of these clusters (MMRd, PAH/NER, ROS), providing an orthogonal, repair-pathway-level rationale for why the agnostic covariate approach should work: signatures that share a repair mechanism will respond similarly to the same upstream covariate perturbations.

- **SBS8's NER assignment** is directly relevant: if an agnostic covariate scan recovers a DNA-damage proxy associated with SBS8 (currently COSMIC-annotated as unknown origin), that is precisely the kind of hypothesis:0007 discovery the hypothesis targets. RePrint here provides prior mechanistic evidence to interpret such a hit.

- **SBS12 and SBS33 → MMRd** are relevant to the MMR-loss / MSI positive control (hypothesis:0007 arm): the agnostic scan should associate MSI status with SBS6/15/26 *and* possibly SBS12/33, consistent with what RePrint predicts. A positive hit for SBS12/33 would support hypothesis:0007 discovery.

- The paper underscores that raw similarity misleads: two signatures sharing a repair pathway can have very different raw spectra (divergent damage distributions). For hypothesis:0007's covariate scan, this means a single "signature similarity" filter would miss repair-mechanism groupings — RePrint provides complementary structure.

- The **guilt-by-association** analogy maps onto hypothesis:0007's logic: just as a signature of unknown aetiology inherits a repair pathway from its cluster neighbours, a signature of unknown upstream cause would inherit candidate covariates from cluster neighbours with known exposures. RePrint could serve as a pre-stratification step before running the hypothesis:0007 association scan.

**Cross-study meta-analysis context:** The cbioportal pipeline aggregates across ~300 studies with heterogeneous exposure histories. RePrint-based grouping of signatures could reduce the effective number of independent outcome variables in the covariate scan (cluster-level aggregation), improving multiple-testing correction and interpretability.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| RePrint transformation | Signature representation layer | Could be applied to per-study or pooled signatures before covariate association |
| Homogeneous / Broad clusters | Signature aetiology groups | Maps to COSMIC aetiology labels used in hypothesis:0007 positive-control arms |
| Guilt-by-association prediction | hypothesis:0007 discovery | Same logic: unknown signature inherits aetiology from cluster neighbours |
| COSMIC v3.4 signatures | COSMIC reference used in pipeline | Pipeline uses restricted SigProfiler assignment against COSMIC |
| Kucab compendium [@Kucab2019] / cited Zou experimentally annotated signatures | Gold standard for aetiology assignment | Provide mechanistic ground truth for validating hypothesis:0007 recovery |

## Limitations

1. **Sparse contexts degrade RePrint.** When a signature rarely generates mutations in certain trinucleotide contexts, the conditional probabilities are noisy or undefined. The pseudocount treatment is a heuristic; rare-context signatures may cluster incorrectly.

2. **Gold standard is curated, not comprehensive.** The cluster construction relied on expert annotation and experimental evidence; signatures whose mechanisms are partially known or contested were excluded from the gold standard. This limits evaluation power for ambiguous cases.

3. **Only SBS (single-base substitution) signatures considered.** Indel (ID), doublet-base (DBS), and structural-variant signatures are not included. DNA repair processes also shape these other mutation classes.

4. **Prediction requires a subtree with ≥ 3 annotated signatures.** The guilt-by-association criterion is conservative: isolated or sparsely-annotated signatures cannot be predicted. SBS34 received no prediction validation (no close neighbours with sufficient annotation).

5. **Causality not established.** RePrint similarity infers shared repair pathways but cannot distinguish which damaged nucleotide triggered repair, nor assign exposures. Upstream aetiological inference (exposure → damage → repair → signature) still requires additional evidence — which is precisely what hypothesis:0007 aims to provide.

6. **No per-sample analysis.** RePrint operates at the signature (population-level) rather than per-sample exposure level. Linking to sample-level covariates (as in hypothesis:0007) requires the downstream association layer described separately.

## Model / Tool Availability

- **RePrintPy** open-source Python package: https://github.com/wojtowicz-lab/RePrintPy
- Computes RePrints from COSMIC or custom signature matrices via CLI
- Generates similarity dendrograms, heatmaps, and exports RePrint matrices for integration with downstream pipelines
- License: not stated in the preprint; check the repository before reuse
- Hardware requirements: minimal (CPU-only; operates on 96-dimensional vectors)

## Follow-up

- Run RePrintPy on the signatures extracted from the cbioportal cross-study dataset to pre-stratify by repair mechanism before running hypothesis:0007 covariate associations.
- The Wojtowicz et al. 2021 (Repairsig) paper cited by this preprint deconvolves damage vs
  repair contributions; add it to the bibliography before using it as local evidence.
- Amgalan et al. 2023 (Genome Medicine) — influence network model for relations between biological processes and signatures — cited here as additional prior work relevant to h08b.
- The SBS8 → NER assignment is a concrete hypothesis:0007 discovery test case: does the hypothesis:0007 covariate scan pick up a UV/NER-related covariate for SBS8 in skin or lung cohorts?
- Consider whether RePrint-derived clusters can serve as a multiple-testing correction grouping in the hypothesis:0007 covariate scan (test cluster-level exposure rather than per-signature).
