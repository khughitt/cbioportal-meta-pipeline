---
id: "paper:Zhang2026"
type: "paper"
title: "SigFormer: an Attention-Based Framework for Robust Single-Sample Mutational Signature Decomposition"
status: "active"
ontology_terms:
  - mutational signatures
  - signature decomposition
  - transformer
  - attention mechanism
  - COSMIC
  - single-sample inference
datasets: []
source_refs:
  - "cite:Zhang2026"
related: []
created: "2026-05-31"
updated: "2026-05-31"
---

# SigFormer: an Attention-Based Framework for Robust Single-Sample Mutational Signature Decomposition

- **Authors:** Yang Zhang, Muchun Niu, Chenghang Zong
- **Year:** 2026
- **Journal:** bioRxiv (preprint, posted January 21 2026)
- **DOI/URL:** https://doi.org/10.64898/2026.01.20.700228
- **BibTeX key:** Zhang2026
- **Source:** PDF

## Key Contribution

SigFormer is a set-conditioned transformer framework for single-sample mutational signature decomposition. It treats the reference signature catalogue as an explicit input set and uses cross-attention between a sample's observed 96-channel trinucleotide mutation profile (query tokens) and the reference signatures (key/value tokens) to produce per-signature exposure estimates without requiring tumor-type-specific gating or cohort-scale discovery. In systematic benchmarks across simulated profiles spanning wide ranges of mutation burden, noise level, and catalogue size, SigFormer improves sensitivity and F1 relative to MuSiCal (likelihood-driven refitting) while maintaining comparable specificity, with the largest gains in high-noise and overcomplete catalogue settings. It also introduces an explicit "unattributed" residual channel that absorbs out-of-catalogue signal instead of forcing it into flat catch-all signatures, providing a principled flag for catalogue incompleteness.

## Methods

**Architecture.** Each sample's 96-channel mutation spectrum is encoded as a set of sample tokens (one per trinucleotide feature or aggregated context), and each reference signature is encoded as a reference token. In a cross-attention block, sample tokens act as queries and reference tokens supply keys and values, producing a weighted combination of candidate signature representations for every observed context. Multiple stacked attention blocks refine early coarse assignments through competition among similar signatures. The reference set is treated as an unordered set, so variable-size and study-specific catalogues (masked or augmented) are natively supported without retraining. An "unattributed" output channel collects probability mass that cannot be explained by any catalogue element.

**Training data.** Simulated 96-channel profiles generated from COSMIC v3.4 SBS signatures plus mock de-novo signatures designed to span COSMIC-like entropy and sparsity statistics. Sampling noise was applied via depth-controlled Dirichlet-multinomial models across a grid of mutation burdens, noise levels, and reference set sizes. 19,200 simulated samples (3,000 batches of 64) were averaged per condition.

**Evaluation.** (1) Simulated benchmark: F1 for binary detection, R² for quantitative exposure concordance across 180 distinct noise × catalogue-size conditions, compared against MuSiCal. (2) Spike-in benchmark: individual signatures titrated from 0 to 100% activity to assess recovery at low exposure levels. (3) PCAWG real-data benchmark: cosine similarity of reconstruction, UMAP geometry of exposure space versus raw spectra, and cluster-level analysis of five biologically annotated tumour clusters (UV/melanoma, smoking/lung, lymphoid CLL/BNHL, POLE-driven MMR, heterogeneous MSI). (4) Normal-tissue benchmark: six published clonal expansion and microdissection datasets across blood, bone marrow, breast, colon, intestine, liver, spleen, and tonsil; evaluation is structural concordance of UMAP and Leiden cluster signatures with expected tissue biology.

**Comparison baseline.** MuSiCal (Jin et al. 2024, Nature Genetics) with its PCAWG reanalysis assignments used as reference exposures.

## Key Findings

**Simulated benchmarks.**
- SigFormer achieved higher F1 than MuSiCal in 157 of 180 conditions and higher R² in 162 of 180 conditions; the exceptions were near-deterministic low-noise regimes with small catalogues where linear refitting approaches the ceiling.
- Mean R² across spike-in benchmark: SigFormer 0.9228, MuSiCal 0.8856.
- The largest relative gains were for flat, weakly distinctive signatures (SBS3, SBS5, SBS40a), where SigFormer's set-conditioned attention most consistently outperformed MuSiCal's fixed linear basis.

**PCAWG real-data.**
- SigFormer achieved cosine similarity > 0.9 across retained samples (SBS count ≥ 200) and slightly exceeded MuSiCal overall.
- SigFormer's UMAP embedding of exposures recapitulated the geometry of raw trinucleotide spectra (anchored to data); MuSiCal's exposures produced a more discretized embedding consistent with tissue-conditioned prior shaping.
- UV/melanoma cluster (C13): both tools recovered SBS7a/SBS7b; SigFormer additionally recovered SBS7c/SBS7d (minor UV components, validated by replacement-aware bootstrap necessity test, Spearman ρ = 0.84 and 0.96) and reduced spurious SBS5 allocation that MuSiCal showed.
- Smoking/lung cluster (C14): SigFormer recovered SBS4 + SBS92 (both tobacco-associated); detected divergent T>A/C>G spectral deviations (SBS25 + SBS39 vs MuSiCal's SBS22 + SBS100), flagged as possibly reflecting a recurrent unrepresented mutational process in a subset of lung adenocarcinomas.
- Lymphoid (CLL/BNHL) cluster (C9): SigFormer consistently detected SBS9 (polymerase-eta hypermutation; 20–50% per sample vs MuSiCal 39%) and SBS85 (AID-related); bootstrap necessity test supported SBS9 as reproducible signal (Spearman ρ = 0.96, p = 1.1×10⁻⁴³).
- POLE-driven cluster (C10): SigFormer assigned SBS15/SBS21 (MSI-associated) to the POLE residual rather than MuSiCal's SBS5; necessity test confirmed these components (ρ = 0.96 and 0.83), while MuSiCal's SBS5 showed predominantly negative per-mutation evidence gain (ρ = −0.52), consistent with SBS5 acting as a catch-all rather than a genuine process.
- Heterogeneous MSI cluster (C11): recovered shared MSI core (SBS6, SBS20, SBS26, SBS44) plus subsets of SBS14/SBS15/SBS21; SBS97 used by MuSiCal confirmed to be largely synonymous with COSMIC SBS44 (cosine similarity 0.85, rising to 0.95 for C>T channels).

**Normal-tissue results.**
- Across six clonal expansion and microdissection datasets, SigFormer recovered tissue-structured UMAP organization concordant with raw 96-channel space.
- Identified endogenous continuum: colon-enriched clusters balanced SBS1 (CpG deamination) + SBS5 + SBS40a; blood-enriched clusters shifted toward SBS19/SBS8 (hematopoietic-lineage damage); liver-enriched clusters showed markedly reduced SBS1 (<10%).
- Detected expected exogenous exposures without tissue-specific gating: SBS4/SBS92 (tobacco) in donors with documented smoking history; SBS88/SBS89 (colibactin) in colorectal clones; SBS22a/b (aristolochic acid) in exposed donors.
- Residual patterns in a lymphoma donor (combination chemotherapy) flagged an out-of-catalogue process; replacing four catalogue components with a de-novo SBSD signature (cosine similarity 0.928 to the composite) improved mean reconstruction cosine similarity from 0.943 to 0.978.

## Relevance

**Direct support for H08a (positive-control recovery).** SigFormer demonstrates that a prior-free, single-sample inference procedure can recover known exposure→signature links — UV↔SBS7 in melanoma, smoking↔SBS4/SBS92 in lung, MMR-loss↔SBS6/SBS15/SBS20/SBS26 in MSI cancers, POLE↔SBS10a/b/SBS28 — *without* tumor-type-specific gating. This is the same positive-control recovery that h08 requires before trusting novel covariate hits. SigFormer's demonstration that catalogue-anchored decomposition naturally clusters by tissue biology (even without conditioning) reduces concern that our pipeline's cross-study aggregation will conflate tissue collinearity with true exposure signal (h08 rival R1).

**Residual channel as a discovery signal.** The explicit unattributed channel in SigFormer is a concrete implementation of the idea h08 encodes for novel signature discovery: rather than forcing unresolved structure into SBS5-like catch-alls, flag it. This is directly relevant to h08b, where we want to identify signatures with unknown or clock-like labels that may have upstream covariates.

**Flat-signature identifiability.** The finding that SBS3, SBS5, and SBS40a are the hardest to recover (reduced R², largest MuSiCal catch-all effect) is a direct caution for the h08 association scan: these signatures may receive spurious mass from any unmodelled signal, inflating their covariate associations. The pipeline should treat SBS5/SBS40 associations with additional scrutiny.

**Tool option for the h08 per-sample refit step.** For q018 (feasibility of per-sample signature extraction downstream of the cross-study pipeline), SigFormer is a candidate tool alongside SigProfilerSingleSample and MuSiCal; its set-conditioned design supports study-specific catalogue pruning/augmentation, which could be valuable for the within-tissue stratification the h08 positive-control design requires. However, the code repository was private at preprint time and not yet peer-reviewed.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Prior-free single-sample inference | Within-tissue agnostic association (h08) | Both avoid tumor-type gating |
| Reference catalogue as input set | COSMIC v3.4 catalogue used in restricted SigProfiler assignment | SigFormer supports custom/pruned sets |
| Unattributed residual channel | Out-of-catalogue signal; novel signature flag | Relevant to h08b discovery |
| Bootstrap necessity test | Validation of minor signature calls | Complements FDR association controls in h08 |
| SBS5/SBS40a catch-all inflation | Flat-signature confounding rival (h08 R4) | Key caution for association scan |
| Tissue-stratified UMAP of exposures | Within-tissue stratification in h08 design | Confirms tissue partitions without explicit conditioning |

## Limitations

- SigFormer is trained on COSMIC + synthetic simulated profiles; generalization depends on how well these capture real sequencing artifacts and biological departures from multinomial sampling (e.g., context-dependent calling errors, strand-bias artifacts).
- Improved sensitivity comes with modestly reduced specificity: minor "leakage" into correlated candidates when predictions are thresholded.
- Coverage limited to 96-channel SBS spectra; indels, DBS, transcriptional strand, and genomic covariate extensions are not yet implemented.
- Bootstrap necessity tests add computational overhead and rely on parametric bootstrap assumptions that may be imperfect in low-count regimes.
- Code repository was private at preprint posting (GitHub: https://github.com/Yang-Zhang-717/SigFormer); release scheduled before journal publication.

## Model / Tool Availability

- **Repository:** https://github.com/Yang-Zhang-717/SigFormer (private at preprint, public release planned)
- **Training data:** reconstructable from instructions in the repository; PCAWG data from ICGC Data Portal; normal-tissue datasets from publications cited in the paper
- **Status:** preprint (bioRxiv, not peer-reviewed as of 2026-01-21)
- **License:** not stated in preprint

## Follow-up

- Check whether SigFormer code has been made public after the preprint date and evaluate as an alternative/complement to SigProfilerSingleSample for the h08 per-sample refit step (q018).
- The replacement-aware bootstrap necessity test (Supplementary Note 4) is a useful complement to exposure-frequency thresholding — consider adapting the approach for validating minor signature hits in the h08 association scan.
- SigFormer's handling of the smoking/lung divergence (SBS25+SBS39 vs SBS22+SBS100) flags a recurrent poorly-represented process in lung adenocarcinomas; relevant to h08b discovery if expression modules correlate with this subcluster.
- The SBS3/SBS5/SBS40a flat-signature finding should inform the specificity-vs-sensitivity trade-off discussion when SigProfiler-assigned exposures for these signatures enter the h08 association model.
