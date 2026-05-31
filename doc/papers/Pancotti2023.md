---
id: "paper:Pancotti2023"
type: "paper"
title: "Unravelling the instability of mutational signatures extraction via archetypal analysis"
status: "active"
ontology_terms:
  - mutational signatures
  - COSMIC
  - NMF
  - archetypal analysis
  - de novo extraction
  - signature stability
datasets:
  - "COSMIC SBS v3.3 (60 non-artefactual signatures)"
source_refs:
  - "cite:Pancotti2023"
related:
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
created: "2026-05-31"
updated: "2026-05-31"
---

# Unravelling the instability of mutational signatures extraction via archetypal analysis

- **Authors:** Corrado Pancotti, Cesare Rollo, Giovanni Birolo, Silvia Benevenuta, Piero Fariselli, Tiziana Sanavia
- **Year:** 2023
- **Journal:** Frontiers in Genetics
- **DOI/URL:** https://doi.org/10.3389/fgene.2022.1049501
- **BibTeX key:** Pancotti2023
- **Source:** PDF

## Key Contribution

This paper provides a systematic evaluation of the instability of NMF-based de novo mutational signature extraction applied to COSMIC SBS v3.3 (79 signatures; 60 non-artefactual). Through simulation studies it shows that high inter-signature cosine similarity and "flatness" (featureless profiles) severely degrade SigProfilerExtractor's ability to recover the correct number and identity of latent signatures, even at sample sizes in the thousands. As a novel complement, the authors apply Archetypal Analysis (AA) to the COSMIC catalogue itself and find that 29 archetypes suffice to reconstruct all 60 profiles with cosine similarity > 0.8 while revealing which signatures are redundant mathematical blends of others.

## Methods

**Data:** COSMIC SBS v3.3 catalogue; 60 of 79 signatures retained after removing 19 designated sequencing artefacts by the COSMIC curators.

**Similarity analysis:** Pairwise cosine similarity matrix over all 60 profiles, then hierarchical clustering (average linkage) to identify highly correlated groups.

**Flatness metric:** Defined quantitatively as the cosine similarity of a signature profile with the uniform distribution over 96 trinucleotide contexts (Eq. 2). Ranges 0–1; SBS3, SBS5, SBS40, SBS8 identified as high-flatness signatures.

**Simulation (de novo extraction benchmarks):** Five scenarios differing in number of latent signatures (6–20), median pairwise cosine similarity (0.22–0.83), median flatness (0.34–0.76), and sample size (200–10,000). Synthetic catalogues generated via SigsPack (10 replicate catalogues per scenario); SigProfilerExtractor used as gold-standard NMF extractor (30 NMF repetitions per run). Metrics: frequency F of runs correctly identifying all signatures, MSE, average cluster stability C_mean, minimum stability C_min.

**Archetypal Analysis (AA):** Applied directly to the 60×96 COSMIC signature matrix M. AA finds convex combinations of extremal data points (archetypes z_k) such that all observations can be expressed as convex mixtures of archetypes. Number of archetypes set to explain 95% of variance (yielding 29); implemented via Python *Archetypal Analysis Package* (Motevalli Soumehsaraei and Barnard, 2019). Code at https://github.com/compbiomed-unito/archetypal-analysis-cosmic.

## Key Findings

**Similarity and flatness profiling of COSMIC v3.3:**
- Several distinct clusters show pairwise cosine similarity > 0.8, including a six-signature flat cluster (SBS3, SBS5, SBS8, SBS40, SBS25, SBS89) and a polymerase-deficiency cluster (SBS36, SBS18, SBS10a/b/c/d; median similarity 0.83).
- Flatness ranges from 0.15 (SBS1) to 0.87 (SBS3); the bimodal distribution indicates a meaningful continuum.

**De novo extraction benchmarks:**
- Scenarios 1 and 2 (few signatures, moderate–high similarity): SigProfilerExtractor succeeds at 200–500 samples (F ≈ 0.9–1.0).
- Scenario 3 (11 signatures combining both highly similar flat and non-flat groups): F = 0.0 at all sample sizes up to 5,000; only 80% success at 10,000 samples. C_min collapses even though C_mean stays high — minimum stability is the sensitive diagnostic.
- Scenario 4 (11 lower-similarity signatures): correct identification restored at ≥ 1,000 samples (F = 0.9–1.0).
- Scenario 5 (20 signatures, pairwise similarity ≥ 0.8 for each): always fails at ≤ 5,000 samples; 10% success at 10,000.
- Implication: obtaining 10,000 matched tumour samples (the failure point for scenario 5) far exceeds the 2,780 PCAWG genomes that anchored COSMIC v3.3, casting doubt on the uniqueness of some signatures.

**Archetypal analysis of COSMIC v3.3:**
- 29 archetypes reconstruct all 60 COSMIC profiles at cosine similarity > 0.8 (26/29 archetypes correspond to at least one COSMIC signature at similarity ≥ 0.97).
- 19 archetypes have a one-to-one correspondence with a single COSMIC signature; 10 archetypes reconstruct multiple signatures, grouping them by shared aetiology or similar biological processes.
- Biologically coherent clusters recovered: Yellow (SBS7b UV + SBS30 BER); Green (SBS4 tobacco + SBS8 HR/NER + SBS36 BER/ROS); Salmon (SBS18 ROS + SBS24 aflatoxin + SBS29 tobacco chewing); Silver Blue + Pink + Blue (seven MMR-deficiency signatures separated into mechanistically distinct subgroups); Orange (SBS11 temozolomide + SBS32 azathioprine); Grey (SBS31 + SBS35 platinum chemotherapy); Light Grey (SBS3 + SBS5 + SBS25 + SBS39 + SBS40 + SBS93 — predominantly high-flatness, uncertain aetiology).
- The Light Grey archetype (A26) reconstructs multiple flat, aetiologically uncertain signatures, reinforcing that these profiles may be mathematical artefacts rather than distinct biological processes.

## Relevance

**h08 (agnostic covariate↔signature-exposure association; positive-control recovery of UV/smoking/APOBEC/MMR):**

This paper is directly relevant to h08 in several ways:

1. **Positive-control signatures:** The AA clustering confirms that canonical positive-control exposures (UV: SBS7b in Yellow; tobacco smoking: SBS4 in Green; MMR deficiency: Silver Blue/Pink/Blue groups) are represented by stable, low-flatness, well-separated archetypes. These are precisely the signatures most likely to pass as reliable positive controls in an h08 covariate-association sweep.

2. **Flat/ambiguous signatures as confounders:** High-flatness signatures (SBS3, SBS5, SBS40, SBS93 in Light Grey) group together under a single archetype whose own profile is nearly uniform. In an h08 association pipeline these would generate noisy, diffuse exposure estimates; prior filtering on flatness score (or restricting analysis to signatures with low AA reconstruction ambiguity) is advisable.

3. **NMF instability warning for cross-study de novo extraction:** The cbioportal pipeline aggregates many studies with heterogeneous sample sizes. The simulation results indicate that when fewer than ~3,000–5,000 samples are available and signatures are highly similar (APOBEC-related SBS2/SBS13, multiple MMR signatures), NMF extraction is unreliable. This argues for using the pre-computed COSMIC v3.3 reference for refitting rather than attempting per-study de novo extraction (consistent with the SigProfilerSingleSample / NNLS refitting approach contemplated in q018/q019).

4. **Dimensionality reduction perspective:** AA provides a compact 29-archetype basis for the 60-dimensional COSMIC space. In a downstream regression or association test (h08), projecting exposure vectors onto this basis could reduce collinearity among highly similar signature pairs (e.g., SBS6/SBS15/SBS21/SBS26 MMR cluster) while preserving biological interpretability — an alternative to ad-hoc signature merging.

5. **Signature redundancy as a design constraint:** The paper's finding that several COSMIC v3.3 signatures have no experimentally validated aetiology and may be blends of others implies that any h08 association result implicating such signatures (e.g., SBS39, SBS40) should be treated with lower confidence until validated by orthogonal evidence.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Flatness score (cosine sim to uniform) | Signature quality filter | Could gate which COSMIC signatures are included in h08 refitting |
| AA archetypes (29) | Dimensionality-reduced signature basis | Alternative to NMF components for covariate association |
| SigProfilerExtractor F / C_min | Extraction reliability metrics | C_min more sensitive than C_mean for detecting instability |
| Scenario 3 failure (11 mixed sigs) | Cross-study aggregation risk | Pipeline cohorts rarely reach 10,000 samples per cancer type |
| Light Grey archetype group | Flat/artefact signature cluster | Candidates for exclusion from h08 association tests |

## Limitations

- Simulated catalogues use random uniform exposures (each signature equally likely to contribute), which does not match real tumour biology where a small number of processes dominate per cancer type. This may underestimate extraction performance in biologically structured cohorts.
- The COSMIC v3.3 catalogue used as input; since then COSMIC v3.4 has been released [UNVERIFIED], potentially altering the similarity landscape.
- AA is applied to the COSMIC signature matrix directly (60 signatures × 96 contexts), not to a patient × mutation catalogue. Thus archetypes describe the geometry of the signature space rather than patient subpopulations.
- Archetypal profiles need not be biologically interpretable on their own (they are extremal convex combinations of observed signatures); the authors note archetypes should complement rather than replace COSMIC.
- The 29-archetype representation explains 95% of variance but loses 5%; individual low-frequency signatures may be poorly represented.
- No APOBEC (SBS2/SBS13) scenario is explicitly tested, despite these being highly similar and clinically important.

## Model / Tool Availability

- **Code and archetypal profiles:** https://github.com/compbiomed-unito/archetypal-analysis-cosmic
- **Synthetic catalogue generation:** SigsPack R package (https://github.com/bihealth/SigsPack)
- **AA implementation:** Python Archetypal Analysis Package (https://data.csiro.au/collection/csiro:40600v1)
- **License:** Not specified in paper [UNVERIFIED]; code repository is public

## Follow-up

- Examine COSMIC v3.4 pairwise similarity matrix to see whether the number of high-flatness or highly similar signatures has changed.
- For h08 pipeline design: evaluate whether pre-filtering COSMIC signatures by flatness < 0.5 and AA archetype membership improves covariate-association specificity.
- Check whether SBS2/SBS13 (APOBEC) form a stable pair that warrants merging before h08 testing — the AA grouping (not explicitly discussed for APOBEC in this paper) would clarify this.
- Schill2024 (also in doc/papers/) addresses NMF stability from a different angle; compare recommendations.
- The companion question q018 (de novo extraction on the aggregated cohort) should incorporate the sample-size thresholds from Table 2: scenario 3 requires 10,000 samples for 80% success — an important feasibility constraint for per-cancer-type extraction.
