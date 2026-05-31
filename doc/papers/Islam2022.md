---
id: "paper:Islam2022"
type: "paper"
title: "Uncovering novel mutational signatures by de novo extraction with SigProfilerExtractor"
status: "active"
ontology_terms:
  - mutational signatures
  - de novo extraction
  - nonnegative matrix factorization
  - SigProfilerExtractor
  - COSMIC signatures
  - benchmarking
datasets:
  - "PCAWG WGS cohort (4,643 whole-genome-sequenced cancers)"
  - "Extended WES cohort (19,184 whole-exome-sequenced cancers)"
  - "Synthetic benchmarking corpus (>80,000 simulated cancer samples)"
source_refs:
  - "cite:Islam2022"
related: []
created: "2026-05-31"
updated: "2026-05-31"
---

# Uncovering novel mutational signatures by de novo extraction with SigProfilerExtractor

- **Authors:** S.M. Ashiqul Islam, Marcos Diaz-Gay, Yang Wu, Mark Barnes, Raviteja Vangara, Erik N. Bergstrom, Yudou He, Mike Vella, Jingwei Wang, Jon W. Teague, Peter Clapham, Sarah Moody, Sergey Senkin, Yun Rose Li, Laura Riva, Tongwu Zhang, Andreas J. Gruber, Christopher D. Steele, Burçak Otlu, Azhar Khandekar, Ammal Abbasi, Laura Humphreys, Natalia Syulyukina, Samuel W. Brady, Boian S. Alexandrov, Nischalan Pillay, Jinghui Zhang, David J. Adams, Iñigo Martincorena, David C. Wedge, Maria Teresa Landi, Paul Brennan, Michael R. Stratton, Steven G. Rozen, Ludmil B. Alexandrov
- **Year:** 2022
- **Journal:** Cell Genomics, 2(11), 100179
- **DOI/URL:** https://doi.org/10.1016/j.xgen.2022.100179
- **BibTeX key:** Islam2022
- **Source:** PDF

## Key Contribution

SigProfilerExtractor is a Python/R tool for automated de novo extraction of mutational signatures via NMF with a custom multiplicative update algorithm, automatic rank selection using NMFk, and Hungarian-algorithm-based stability clustering. The paper presents the largest benchmarking of de novo extraction tools to date (14 tools, 34 scenarios, >80,000 synthetic cancer samples), showing SigProfilerExtractor outperforms all 13 competitors on noisy data by recovering 20–50% more true-positive signatures with 5-fold fewer false positives. Applied to 23,827 sequenced cancers, it identifies four novel mutational signatures, including SBS92, a tobacco-smoking-associated signature in bladder cancer.

## Methods

**Tool architecture:** SigProfilerExtractor decomposes a mutation-count matrix M into signatures S and activities A via NMF. It performs 100 independent factorizations per rank (Poisson resampling + normalization before each), evaluates stability via silhouette scores using the Hungarian algorithm for clustering, and selects the optimal rank using a modified NMFk approach. A Kullback-Leibler divergence objective function is used. Extracted de novo signatures are matched to COSMIC reference signatures using cosine similarity. GPU acceleration (PyTorch) is supported. Inputs accepted: matrix, VCF, MAF, custom formats.

**Benchmarking design:** 34 distinct scenarios spanning "easy" (3–5 signatures, ~7.4% of cancer types), "medium" (11–21 signatures, ~15.9%), and "hard" (≥25 signatures, ~59.5%) complexity levels were evaluated. Scenarios included 32 noiseless SBS-96 WGS cases plus noise scenarios (0–10% noise), plus 12 extended-channel matrix scenarios. Ground-truth signatures were drawn from COSMICv3, SignatureAnalyzer (SA), or randomly generated; synthetic samples ranged from 200 to 2,700 per scenario. Evaluation metrics: precision (TP/(TP+FP)), sensitivity (TP/(TP+FN)), F1 score. A de novo signature is TP if cosine similarity ≥ 0.90 to a ground-truth signature.

**Real-data application:** SigProfilerExtractor was applied within-cancer-type and pan-cancer to 2,778 PCAWG WGS cancers (the PCAWG public dataset) plus an extended cohort of 1,865 WGS and 19,184 WES cancers (TCGA + 261 ICGC projects). De novo extraction was run separately within each cancer type and across all samples.

**Normalization / initialization sensitivity:** Gaussian mixture model (GMM), 100X, and log2 input normalizations were compared; all yielded comparable results. KL-divergence updates outperformed Euclidean and Itakura-Saito. Random and NNDSVD initialization gave similar results under the best hyperparameter settings.

## Key Findings

**Benchmarking:**
- On noiseless hard WGS scenarios (≥25 signatures, ~60% of human cancer types), SigProfilerExtractor outperformed all other tools: 10–37% more TP signatures, 2.7–16-fold fewer FP signatures compared to the next seven best tools.
- At 5% noise (reflecting real high-quality datasets with ~95% sensitivity and 95% precision for SBS-96): SigProfilerExtractor identified 20–50% more TP signatures with >5-fold fewer FP signatures than the next seven best-performing tools (WGS).
- For WES with 5% noise, performance drops substantially for all tools; average F1 = 0.61 (WGS) vs 0.46 (WES) across tools, but SigProfilerExtractor was the only tool with average F1 >0.60 — no other tool exceeded 0.53 on WES noise scenarios.
- SigProfilerExtractor and SignatureAnalyzer are the only two tools supporting extended mutational channel matrices (DBS, ID, CN, SV) and GPU acceleration. SigProfilerExtractor's automatic rank selection performs near-identically to forced (known-N) selection (rF1 ≈ 1.0 on medium and hard scenarios), indicating robust model selection.
- Tools using the NMF R package (Maftools, MutationalPatterns, MutSpec, SignatureToolsLib, SigMiner, SomaticSignatures) behave similarly, as expected from a shared factorization engine. SignatureAnalyzer (ARD-based) and SigNeR (BIC-based) are susceptible to noise — at 10% noise, SA's F1 drops from 0.76 to 0.07; SignatureAnalyzer's average FP count increases from 4.40 to 90.95 at 10% noise.

**Novel biological signatures (real-data application):**
- **SBS92** (bladder cancer): characterized by T>C mutations with transcriptional strand asymmetry consistent with damage on purines — mechanistically consistent with tobacco smoke's complex mixture of chemicals that damage purines. Found to be 9-fold elevated in bladder cancers of ever-smokers vs never-smokers (p = 7.6 × 10⁻³, Wilcoxon). Confirmed in an independent WGS cohort of 88 normal urothelial microbiopsies (cosine similarity 0.98, p < 10⁻³²); 3-fold elevated in normal urothelium of ever-smokers vs never-smokers (p = 8.3 × 10⁻³).
- **SBS93** (stomach cancers): T>C and T>G mutations with strand asymmetry consistent with damage on pyrimidines in TpTpA contexts; confirmed in an independent WGS set of esophageal squamous cell carcinomas (cosine similarity 0.88). Aetiology unknown.
- **SBS94** (predominantly colorectal, smaller contributions to 8 other cancers): C>A mutations with strand asymmetry indicative of damage on purines. Aetiology unknown.
- **SBS95** (liver hepatocellular carcinomas only, extended cohort): C>A mutations biased toward genic regions; found as predominant in 5 ICGC LINC-JP samples, modest contributions in 24 others. Classified as a possible artifact, as no independent validation was obtained.
- SBS92 and SBS93 were confirmed in independent cohorts; SBS94 and SBS95 were not.

**Why WES misses SBS92:** SBS92's profile is predominantly in intergenic regions, so exome sequencing captures too few mutations per sample (typically <15 from SBS92) to detect it. Downsampling of WGS bladder urothelial genomes to exome confirmed this.

## Relevance

**Direct relevance to h08 (agnostic covariate↔signature-exposure association):**

1. **SBS92 as a smoking positive control.** H08a requires recovery of the smoking→signature link without being told it. SBS92 is a textbook example of exactly this — an environment-exposure (tobacco) signature in a specific tissue (bladder). The paper demonstrates that without prior knowledge of tobacco etiology, de novo extraction of SBS92 followed by statistical association of per-sample SBS92 exposure with self-reported smoking status (never vs ever) reproduces the known link at p < 0.001. This validates the agnostic-association paradigm and serves as a model for the H08a positive-control arm design.

2. **Tool selection for the pipeline.** For h08's signature-decomposition step (see `question:q019`), SigProfilerExtractor is the best-evidenced open-source tool for de novo extraction — it outperforms 13 alternatives on the benchmarking scenarios most representative of real cancer genomics (5% noise, hard multi-signature settings). Its automatic rank selection removes an analyst-dependent hyperparameter, important for reproducibility in the cbioportal pipeline.

3. **SBS92 is WGS-only.** The paper explicitly shows SBS92 is undetectable by WES because of its intergenic distribution. This is a binding constraint for h08: the smoking↔SBS92 positive control can only be tested on WGS cohorts (PCAWG, MC3 where WGS is available). Panel-sequenced studies in cBioPortal will miss it. This informs the per-study stratification and the Q018 panel-adequacy question.

4. **Within-tissue stratification.** The paper's de novo extraction ran within-cancer-type, matching h08's design requirement that associations be conditioned on tissue of origin (Prediction 4 of h08). Cross-tissue pooling inflates both false positives and confounders; SigProfilerExtractor's per-cancer-type runs are the model for the h08 pipeline architecture.

5. **NMFk rank-selection robustness.** The near-identity of suggested vs forced model-selection F1 (rF1 ≈ 1.0) confirms that SigProfilerExtractor's automatic rank selection is not a material source of error. For h08, this means the extracted exposures H used as outcome variables carry limited model-selection uncertainty.

6. **Cross-study aggregation relevance.** The paper's multi-study aggregation (PCAWG + TCGA + 261 ICGC studies) mirrors the cbioportal pipeline's core cross-study design. Four signatures that were missed in single-study analyses emerge only in the larger pooled cohort — consistent with the project's hypothesis that cross-study aggregation surfaces signal invisible within individual studies.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| De novo NMF extraction (M ≈ S × A) | Upstream of `run_restricted_sigprofiler_assignment.py` | Paper provides the extraction step; project currently uses restricted assignment |
| Activities matrix A (per-sample signature exposures) | Outcome variable for h08 association scan | H columns = signature exposures = h08's dependent variables |
| SBS-96 mutational classification | cBioPortal mutation counts (6-channel or 96-channel) | Pipeline currently aggregates counts; 96-channel matrix requires per-sample SBS context |
| Within-cancer-type extraction | Within-tissue conditioning (h08 Prediction 4) | Required to avoid tissue collinearity (h08 Alternative R1) |
| COSMICv3 reference signatures | COSMIC catalog used in `annotate_drivers.py` context | Same reference catalog; driver annotation uses genes not signatures |
| Noise robustness (5% noise benchmark) | WES vs WGS heterogeneity across cBioPortal studies | Panel / WES studies → higher noise; WGS studies → best extraction |
| SBS92 (tobacco / bladder) | h08a positive control: smoking→signature | Key validation target for h08a's smoking arm |
| SBS4 (lung / smoking) | h08a positive control: smoking→SBS4 | SBS4 not re-extracted here but is the canonical lung control |

## Limitations

- **Linear independence assumption.** The model assumes mutational signatures accumulate independently and linearly across a tumour's genome. This is violated when copy-number alterations amplify certain genomic regions (affecting context frequencies) or when whole-genome duplication events co-occur. Copy-number signatures are handled separately as a different classification.
- **WES underpowers multi-signature cancers.** Average F1 drops from 0.61 (WGS noise) to 0.46 (WES noise); SigProfilerExtractor remains the best WES tool but WES performance is substantially degraded. Implications: de novo extraction of rare/weak signatures will be unreliable for panel or WES-only cBioPortal studies.
- **Single-sample assignment not evaluated.** Benchmarking focuses on cohort-level de novo extraction. The assignment of signatures to individual cancer genomes (refitting) requires a separate validation not covered here.
- **SBS95 may be an artifact.** No independent validation cohort confirmed SBS95; the authors classify it as a possible sequencing or bioinformatics artifact. Demonstrates the need for replication before biological interpretation.
- **No ground-truth for novel signatures.** Validation of SBS92–SBS95 relies on epidemiological correlation, not experimental mutagenesis — causality is inferred not proven.
- **Benchmarked on SBS-96 primarily.** Extended channel matrices (DBS, ID, CN, SV) were tested in only 12 of 34 scenarios and in a smaller comparison; the advantage may differ for non-SBS signatures.

## Model / Tool Availability

- **Package:** SigProfilerExtractor (Python, with R wrapper)
- **GitHub:** https://github.com/AlexandrovLab/SigProfilerExtractor
- **Install:** `pip install SigProfilerExtractor` (or `uv add SigProfilerExtractor`)
- **License:** BSD-2-Clause
- **GPU support:** Yes (PyTorch backend for matrix factorization)
- **Input formats:** matrix, VCF, MAF, custom
- **Mutational catalogs supported:** SBS-96, DBS-78, ID-83, CN-48, SV-32, and any user-defined channel set
- **Reference signatures:** COSMICv3 (and any user-supplied reference)
- **Hardware requirements:** CPU sufficient for small datasets; GPU recommended for extended-channel scenarios or large cohorts
- **Note:** SigProfilerMatrixGenerator (a companion tool, ref 15 in paper) is required to generate the mutation matrix from VCF/MAF inputs

## Follow-up

- **Read next:** Degasperi et al. 2022 (already summarized: `paper:Degasperi2022`) for comparison of signature extraction methodology using a Bayesian framework (SignatureAnalyzer). DiazGay et al. 2023 (`paper:DiazGay2023`) for downstream restricted assignment in multi-cancer contexts.
- **h08 design questions:** Can SigProfilerExtractor's per-sample activity outputs be used directly as outcome variables in the h08 association scan, or must activities first be refitted per-sample using `run_restricted_sigprofiler_assignment.py`? (See `question:q018`.)
- **Cross-study aggregation:** Does pooling across cBioPortal studies before extraction (pan-cancer) vs within-study extraction change the signatures recovered? The paper suggests within-cancer-type extraction first, then pan-cancer as a supplement — consistent with h08's within-tissue conditioning requirement.
- **SBS92 positive control:** For h08a's smoking arm, which cBioPortal/MC3 WGS bladder cancer studies have self-reported smoking status to replicate the SBS92 elevation analysis?
