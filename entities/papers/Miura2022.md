---
type: paper
title: A phylogenetic approach to study the evolution of somatic mutational processes
  in cancer
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Miura2022
ontology_terms:
- mutational signatures
- clone phylogeny
- tumor evolution
- COSMIC signatures
- somatic mutation
datasets: []
source_refs:
- cite:Miura2022
related: []
---

# A phylogenetic approach to study the evolution of somatic mutational processes in cancer

- **Authors:** Sayaka Miura, Tracy Vu, Jiyeong Choi, Jeffrey P. Townsend, Sajjad Karim, Sudhir Kumar
- **Year:** 2022
- **Journal:** Communications Biology (Nature Portfolio), vol. 5, article 617
- **DOI/URL:** https://doi.org/10.1038/s42003-022-03560-0
- **BibTeX key:** Miura2022
- **Source:** PDF

## Key Contribution

PhyloSignare (PS) is a phylogeny-aware wrapper around existing refitting methods (QP, deconstructSigs, MutationalPatterns) that reduces false-positive branch-specific signature detection and recovers faint signatures by pooling variants from proximate branches before applying standard refitting. Applied to 61 non-small cell lung cancer (NSCLC) clone phylogenies, PS recovers the known smoking→COSMIC-S4 and APOBEC→S2/S13 dynamics across tumor evolution: S4 dominates trunks and declines toward tips, while APOBEC signatures rise over time.

## Methods

**Input:** A reconstructed cancer cell clone phylogeny with variant counts mapped to each branch (96-trinucleotide SBS spectrum per branch).

**PhyloSignare algorithm (three stages):**
1. *Candidate pooling.* For a target branch, PS pools its variants with those of neighbouring branches (sibling, parent, children) at four levels of proximity. Each pooled collection is fed to a user-chosen refitting method (here: quadratic programming / QP) to identify candidate COSMIC signatures.
2. *Importance score (iS) filtering.* For each candidate signature S, iS is computed as `(f_{S−} − f) / f`, where f is the residual fit of the full model and f_{S−} is the fit when S is excluded. A small iS (~0) indicates the signature adds little explanatory power and is likely spurious; the threshold is iS > 0.02.
3. *Neighbour-activity test.* In the final step, the selected candidate signatures are evaluated only for branches where they are detected in immediate neighbours, minimising gain/loss artifacts from signature bleeding.

**Benchmarking:** 180 simulated multi-clone phylogenies (5–7 branches, 20–205 mutations/branch) generated from PhySigs datasets; COSMIC v2 signatures randomly drawn via Dirichlet; Gaussian noise (SD = 0.1/0.2/0.3). Refitting methods compared: QP, deconstructSigs, MutationalPatterns, PhySigs, plus PS coupled to each.

**Empirical data:** 61 NSCLC clone phylogenies from TRACERx (100 non-small cell + 32 squamous samples; filtered to ≥100 variants total and ≥2 tip branches). COSMIC v2 signatures known to be active in lung adenocarcinoma (S1, S2, S4, S5, S6, S13, S17) and squamous cell carcinoma (S1, S2, S4, S5, S6, S13) were provided as the candidate set.

## Key Findings

**Simulated data:**
- PS + QP achieves precision 93% vs 66% for QP alone (on branches with <50 variants), reducing spurious detections.
- PS improves recall (true positive rate) for branches with >100 variants while matching or exceeding precision.
- PS detects faint signatures (<10% relative activity) that the 5% activity filter cannot.
- Overall iS is reduced 2%–56% when incorrect signatures detected by QP alone are included, confirming that spurious signatures degrade model fit.
- PS + QP outperforms a bootstrap resampling approach (QP + BS, 1,000 replicates) on F1 score.
- PhySigs (direct phylogeny-aware method) shows slightly better relative activity estimates but PS + QP better handles low-mutation branches.

**Lung cancer empirical data (TRACERx):**
- COSMIC S4 (tobacco/smoking, C→A) dominates the trunk in >72% of patients (44/61), but its relative activity declines progressively toward tip branches — consistent with a cessation-like reduction in smoking mutagenesis during clonal evolution.
- APOBEC signatures S2 and/or S13 are active in >86% of patients; their relative activity rises in tip branches relative to trunks — APOBEC mutagenesis increases as tumour evolution progresses.
- Age-related S1 activity is present in most branches but is often masked by the dominant S4 signal in trunks.
- APOBEC signature S13 (C→G at TCA/TCT contexts) appears only in late tip branches (e.g. branches E and F in patient CRUK0025), indicating punctuated acquisition.
- More than half of clone phylogenies have at least one tip-tip branch pair with different signature compositions (Fig. 8 top), and >50% have trunk-tip pairs that differ, quantifying intratumour mutational heterogeneity.

**Global (whole-tumour) detection:**
- PS + QP-Global (pooling across all branches) achieves higher F1 than QP-ALL (naive pooling) and intermediate recall compared with PhySigs-Global.

## Relevance

**Direct connection to h08 (agnostic covariate ↔ signature-exposure association):**

- **Positive-control recovery (H08a):** This paper confirms at branch resolution the three canonical exposure→signature links that H08a must recover: smoking→SBS4, APOBEC activity→SBS2/SBS13 (with the further observation that APOBEC3 deaminases are cited as the mechanism), and age-related→SBS1. These are exactly the "must-pass" positive controls in the pre-registered H08a design (UV→SBS7 / smoking→SBS4 / APOBEC3-expression→SBS2/SBS13). The lung cancer dynamics here provide quantitative priors: SBS4 should be the dominant trunk signal in any lung cohort, and SBS2/13 should rise toward tips / later evolution.
- **Signature bleeding / false positives:** PS's core problem (spurious signatures from naive per-branch refitting) is directly analogous to the false-positive risk in h08's per-sample refit step. The iS statistic and candidate-pooling strategy are reusable concepts for a within-tissue, per-sample association: pooling samples from the same tissue/study before refitting reduces spurious detections in low-mutation-count samples (the same mechanism as low-variant branches).
- **APOBEC dynamics and expression:** The paper cites APOBEC3 deaminases as the mutagenic mechanism for S2/S13, which aligns with h08's prediction 2 (APOBEC3A/B mRNA expression should be the strongest APOBEC signature correlate). The temporal rise of APOBEC signatures in tips implies that expression-level APOBEC activity increases during clonal evolution, a feature measurable in the TRACERx expression dataset and recoverable within tissue using the h08 association design.
- **Cross-study aggregation context:** The cBioPortal pipeline aggregates per-study mutation tables without per-patient clone phylogenies. PS is not directly applicable, but its insights calibrate expectations: (a) signature composition varies substantially within patients, so study-level pooling will average over real intratumoral heterogeneity, and (b) the dominant signatures in bulk tumour samples (S4, S2/13 in lung) should be the ones most detectable by the h08 scan.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Branch-specific variant counts (96-dim) | Per-sample mutation spectrum | PS branches ≈ project's per-sample inputs |
| COSMIC v2 restricted signature set (per cancer type) | `run_restricted_sigprofiler_assignment.py` candidate set | Both restrict to cancer-type-relevant signatures |
| iS (importance score) — excludes spurious signatures | Planned h08 association quality filter | iS is a within-fit exclusion test; h08 uses FDR across covariates |
| Pooling from neighbouring branches to raise variant count | Study-level pooling for low-sample-count cohorts | Analogous low-count remedy; PS pools genomically, h08 pools cohort-wise |
| Trunk vs tip signature dynamics | Early vs late mutation strata | Not currently modelled in cross-study pipeline (no phylogeny available) |
| COSMIC S4 (smoking), S2/S13 (APOBEC), S1 (age) | H08a positive-control signatures | Same three aetiologies the h08 pre-registration must recover |

## Limitations

- Requires a pre-computed cancer cell clone phylogeny; quality of phylogenetic inference (errors in branch variant assignment) propagates into signature errors. The paper notes that diluted signals from incorrect clone-phasing cause false negatives.
- Currently limited to SBS signatures; indel and doublet-base-substitution signatures are acknowledged as future work.
- The iS score is powerless when the number of variants is very small (chi-square assumption fails); branches with <20 variants are pooled with neighbours without independent assessment.
- Only COSMIC v2 signatures were benchmarked in simulation; v3 analysis (Supplementary) reportedly generates more spurious detections when all 30 signatures are provided rather than a curated set.
- Signature bleeding (a signature present in only some patients being "transferred" to others via pooling) is acknowledged as a limitation analogous to cohort-level signature bleeding in bulk analyses.
- Empirical validation relies on TRACERx NSCLC only; other cancer types not shown.
- Linear phylogeny methods (CloneSig) excluded from comparison because linear clone phylogenies are rare in practice.

## Model / Tool Availability

- **PhyloSignare** source code: https://github.com/SayakaMiura/PhyloSignare
- **Input data files** for the paper: https://github.com/SayakaMiura/PhyloSignare/input_files
- **Source data for figures**: https://github.com/SayakaMiura/PhyloSignare/Sourcedata
- Simulated datasets obtained from: https://github.com/elkebir-group/PhySigs (PhySigs repo, downloaded 2019)
- License: not stated in the paper; check the repository before reuse
- Language: not stated in the paper; infer from repository metadata before implementation work
- Hardware: standard laptop/workstation; no GPU requirement implied

## Follow-up

- The iS score formula (Eqs 1–3) could be adapted as a signature-retention criterion during the h08 per-sample restricted refit: retain a COSMIC component only if its exclusion degrades fit by iS > some threshold.
- The TRACERx lung dataset analysed here overlaps with datasets accessible via cBioPortal; cross-referencing study IDs could extend the cross-study aggregation with clone-level resolution for a subset of patients.
- Comparison with PhySigs (Christensen et al. 2020) deserves attention: PhySigs directly models signature evolution along the phylogeny via a parsimony framework; PS is a pre-filter wrapper. For h08's purposes (bulk cross-study refitting, no phylogenies available), PS's pooling heuristic is more directly transferable.
- The convergent smoking→APOBEC signature shift observed here is consistent with an immune-pressure / selection mechanism discussed in `discussion:0004-common-mutational-signatures-known-vs-learned-immune-causes-and` (immune editing removing high-TMB clones, leaving APOBEC-diversified clones). Explicit testing of this hypothesis requires immune cell abundance data alongside the signature dynamics.
