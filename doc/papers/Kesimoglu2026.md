---
id: "paper:Kesimoglu2026"
type: "paper"
title: "Combined inference of known and novel mutational signatures with ReDeNovo"
status: "active"
ontology_terms:
  - mutational signatures
  - de novo signature discovery
  - signature refitting
  - non-negative matrix factorization
  - non-convex optimization
datasets: []
source_refs:
  - "cite:Kesimoglu2026"
related: []
created: "2026-05-31"
updated: "2026-05-31"
---

# Combined inference of known and novel mutational signatures with ReDeNovo

- **Authors:** Ziynet Nesibe Kesimoglu, Ermin Hodzic, Jan Hoinka, Bayarbaatar Amgalan, M.G. Hirsch, Teresa M. Przytycka
- **Year:** 2026
- **Journal:** bioRxiv (preprint, posted 2026-02-06)
- **DOI/URL:** https://doi.org/10.64898/2026.02.05.703798
- **BibTeX key:** Kesimoglu2026
- **Source:** PDF

## Key Contribution

ReDeNovo formalises the **Combined Mutational Signature Inference (CMSI)** problem — simultaneously fitting a catalogue of known signatures while inferring genuinely novel (de novo) ones — and solves it with a two-stage heuristic (recognition phase then de novo discovery phase) built on iterative hybrid NMF with explicit activity-support and novelty constraints. On 16 synthetic benchmarks and nine ICGC-PCAWG cancer-type cohorts, ReDeNovo outperforms SigProfilerAssignment, SigProfilerExtractor, MuSiCal, sigLASSO, and CaMuS on both signature-set precision (F1) and per-sample activity accuracy (RMSE), and is the only method that consistently recovers every injected de novo signature. Applied to PCAWG melanoma data, ReDeNovo identified a new UV-light-associated signature (dominated by TCC>TTC) not captured by existing COSMIC v3.4 entries.

## Methods

**Problem formulation.** Given observed mutation-count matrix M (n samples × m categories), a catalogue C of known signatures, and tolerance parameters δ (novelty cosine-similarity threshold), φ (minimum fraction of samples with non-trivial activity), and γ (minimum relative activity fraction), CMSI seeks matrices A (activities) and P (signatures) that minimise ‖M − A×P‖²_F + α·l′ subject to: (1) each row of P is either a catalogue member or has cosine similarity < δ to every catalogue entry; (2) each signature's activity satisfies the support constraint. The problem is non-convex (like NMF) and NP-hard in general.

**ReDeNovo algorithm.** A two-stage iterative heuristic:
- *Recognition phase*: one catalogue signature is added per iteration. Each iteration runs unconstrained hybrid NMF with fixed known rows and incrementally growing de novo rows; a catalogue entry is selected when a de novo row converges to cosine similarity ≥ δ with it and satisfies the activity-support constraint. Signatures violating the activity constraint are pruned after each addition. The phase terminates when no further catalogue signature can be added.
- *De novo discovery phase*: structurally identical but a de novo row is retained only if its cosine similarity to every catalogue member is < δ; this enforces genuine novelty.

**Benchmarks.** 16 synthetic datasets were generated from COSMIC v3.4 ground-truth mixtures with varying Gaussian noise levels (σ = 0 to 30). De novo recovery was assessed by injecting four synthetically designed signatures and by hiding individual COSMIC signatures from the catalogue. Comparators: SigProfilerAssignment v0.2.3, SigProfilerExtractor v1.2.0, MuSiCal, sigLASSO v1.1, CaMuS (run with oracle-known signature counts).

**Biological data.** WGS somatic mutation calls for nine ICGC-PCAWG cancer types (Skin-Melanoma n=107, Breast-AdenoCA n=198, Prostate-AdenoCA n=286, Pancreatic-AdenoCA n=241, Ovary-AdenoCA n=113, Lymph-BNHL n=107, Liver-HCC n=326, Kidney-RCC n=144, CNS-Medulloblastoma n=146). Reference catalogue: COSMIC v3.4 SBS signatures.

## Key Findings

**Known-signature recovery.** At low noise (σ < 10) all methods achieve comparable F1 on recovering the ground-truth signature set. At all noise levels ReDeNovo yields lower RMSE for per-sample activity estimation. At high noise (σ ≥ 5), MuSiCal and several other tools accumulate substantial false-positive catalogue signatures; ReDeNovo and SigProfilerExtractor remain resilient, with ReDeNovo producing at most one false positive even at the highest tested noise.

**Flat signatures.** SBS3, SBS5, and SBS8 (broad, "flat" spectra) are universally the hardest to estimate accurately; ReDeNovo outperforms other tools on all three at every noise level.

**De novo recovery.** ReDeNovo achieves a de novo signature detection rate (SDR) of 1.000 across all 12 test configurations (four synthetic + eight hidden-COSMIC), versus 0.742 for CaMuS (oracle), 0.750 for SigProfilerExtractor (four configurations only), and 0.175 for MuSiCal. ReDeNovo's average cosine similarity between inferred and ground-truth de novo signatures is 0.918 (vs 0.703 CaMuS, 0.164 MuSiCal). Overall activity RMSE for the de novo scenario: ReDeNovo 130.4, MuSiCal 277.9, SigProfilerExtractor 261.1, CaMuS 305.4.

**PCAWG biological validation.** 75 of 83 COSMIC signature–cancer-type assignments are literature-supported. ReDeNovo newly detected SBS39 (unknown etiology, but recently linked to HRD and NHEJ pathways) in breast and kidney cancers — in both cases co-occurring with SBS3 (HRD signature), which provides supporting coherence. MMRd SBS15 was assigned to CNS Medulloblastoma with very low activity, flagged as a potential false positive.

**Novel UV signature (Skin-Melanoma N1).** The single confirmed novel signature is dominated by TCC>TTC C>T mutations. Cross-patient activity correlates strongly with SBS7a (Pearson 0.83, Spearman 0.92) and SBS7b (Pearson 0.86, Spearman 0.93), consistent with UV DNA damage. The authors attribute its distinctness from SBS7a/7b to population heterogeneity in UV-wavelength exposure and protection mechanisms (skin pigmentation, DNA repair efficiency).

## Relevance

Directly relevant to hypothesis **h08** (agnostic covariate association recovers known signature aetiologies and surfaces novel causes). h08 proposes treating per-sample signature exposures (H matrix columns) as outcomes for phenome-wide covariate association. The quality of those exposures is the bottleneck: ReDeNovo's superior per-sample activity estimation (lower RMSE at all noise levels, especially for flat signatures like SBS3/5/8) would propagate through to cleaner phenotypic associations. The joint known+novel framing also matters: if the cross-study aggregation harbours study-level technical artefacts that manifest as coherent novel signals, ReDeNovo's de novo stage would capture them explicitly rather than smearing them into known-signature exposures.

Within the signature-method ecosystem this project tracks, ReDeNovo sits alongside SigProfilerExtractor (de novo reference), SigProfilerAssignment (refitting reference), MuSiCal (prior joint method), and sigLASSO as candidate tools for the decomposition step upstream of h08's association analysis.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Activity matrix A (n samples × l signatures) | Per-sample signature exposures (H) | Direct input to h08 covariate-association |
| Recognition phase | Refitting / known-signature attribution | Corresponds to SigProfilerAssignment role |
| De novo discovery phase | De novo extraction | Corresponds to SigProfilerExtractor role |
| CMSI constraint (2): activity support threshold φ, γ | Hypermutator / low-burden exclusion filters | Activity-support gating is analogous to the pipeline's sample-count thresholds |
| COSMIC v3.4 catalogue C | COSMIC catalogue used in annotate_drivers.py and CH annotation | Catalogue version alignment needed |
| Novel signature Skin-Melanoma N1 | Potential study-level or batch-specific signal | Worth checking whether cross-study aggregation produces analogous signals |

## Limitations

- Paper is a preprint (not peer-reviewed). Benchmark advantage may shift after review.
- De novo benchmarks focus on the single-novel-signature regime; performance with multiple simultaneous novel signatures is not evaluated.
- CaMuS is given oracle signature counts (a methodological favour not available in practice), yet ReDeNovo still outperforms it; this is noted but the oracle condition makes the comparison asymmetric.
- SigProfilerExtractor cannot be tested in the "hidden COSMIC signature as de novo" condition because it cannot treat catalogue entries as novel; its SDR denominators differ, limiting direct comparison.
- A de novo signature could theoretically be a linear combination of known ones (acknowledged as a limitation; no false positives of this type were observed in tests, but the check is not implemented).
- Biological validation relies on literature consistency as a proxy for ground truth; false negatives cannot be assessed from secondary evidence alone.
- Only SBS (trinucleotide context) signatures are evaluated; no extension to DBS, ID, or other variant classes.
- Computational cost relative to comparators is not reported in the main text. [UNVERIFIED]

## Model / Tool Availability

- **Repository:** https://github.com/ncbi/redenovo
- **License:** Not explicitly stated in paper (NIH intramural work; likely public domain or permissive) [UNVERIFIED]
- **Language / dependencies:** Not stated in main text [UNVERIFIED]
- **Input:** Mutation count matrix M (n × 96 for SBS) + COSMIC catalogue; outputs activity matrix A and signature matrix P
- **Default parameters:** δ (novelty cosine threshold), φ and γ (activity support) have defaults but are user-adjustable

## Follow-up

- Compare ReDeNovo exposures vs SigProfilerExtractor/SigProfilerAssignment exposures on the PCAWG cohort to quantify the downstream effect on h08 covariate associations.
- Examine whether the cross-study aggregation in this project surfaces study-cohort-specific signals that would be captured as novel signatures by ReDeNovo but attributed to known ones by pure refitting.
- Check computational runtime and memory footprint for the full cBioPortal cohort (potentially 10k+ samples) — not reported in paper.
- Investigate whether the activity-support constraint (φ, γ) should be tuned for smaller per-study cohorts common in cBioPortal (many studies have n < 100).
- The newly proposed Skin-Melanoma N1 signature has no COSMIC entry; track whether it appears in a future COSMIC release.
