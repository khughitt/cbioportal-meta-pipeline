---
type: paper
title: Assigning mutational signatures to individual samples and individual somatic
  mutations with SigProfilerAssignment
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:DiazGay2023
ontology_terms:
- mutational signatures
- signature refitting
- COSMIC
- nonnegative least squares
- somatic mutation
- copy number signatures
datasets: []
source_refs:
- cite:DiazGay2023
related: []
---

# Assigning mutational signatures to individual samples and individual somatic mutations with SigProfilerAssignment

- **Authors:** Marcos Diaz-Gay, Raviteja Vangara, Mark Barnes, Xi Wang, S.M. Ashiqul Islam, Ian Vermes, Stephen Duke, Nithish Bharadhwaj Narasimman, Ting Yang, Zichen Jiang, Sarah Moody, Sergey Senkin, Paul Brennan, Michael R. Stratton, Ludmil B. Alexandrov
- **Year:** 2023
- **Journal:** Bioinformatics, 39(12), btad756
- **DOI/URL:** https://doi.org/10.1093/bioinformatics/btad756
- **BibTeX key:** DiazGay2023
- **Source:** PDF

## Key Contribution

SigProfilerAssignment is a signature-refitting tool (desktop + web) that assigns COSMIC reference SBS, DBS, ID, and CN signatures to individual cancer samples and — uniquely among available tools — probabilistically assigns each known signature to every individual somatic mutation based on mutational context. Its computational core combines a custom forward stagewise algorithm for sparse selection with nonnegative least squares (NNLS, Lawson-Hanson method) for activity estimation. Benchmarking on 2700 synthetic cancer genomes (0%, 5%, and 10% noise) shows it outperforms deconstructSigs, MutationalPatterns (standard and strict), sigLASSO, and SignatureToolsLib on F1 score, with F1 > 0.90 at 10% noise — the only tool to do so [@DiazGay2023].

## Methods

**Algorithm.** Given a mutation count vector v (sample) and a matrix S of n known signatures, the tool iterates two subroutines: `removeSignatures` (drops signatures whose removal reduces relative L2 reconstruction error by ≤ 1%) and `addSignatures` (re-adds signatures from the full COSMIC set if they reduce error by ≥ 5%), converging when S is stable. Final activities are computed by NNLS using the Lawson-Hanson method; the objective is to minimise `||v − S·a||²₂ / ||v||²₂`.

**Probabilistic mutation-level assignment.** When the input is individual mutations (VCF/MAF) rather than an aggregated count vector, each mutation's trinucleotide context is used to compute a posterior probability for each active signature, yielding per-mutation "most probable signature" calls.

**Supported signature types.** SBS, DBS, ID (indels), and CN (copy-number) COSMIC reference sets, plus de-novo extracted signatures and user-supplied custom signatures.

**Input formats.** VCF, MAF, or plain-text mutation matrices.

**Benchmarking dataset.** 2700 simulated genomes (Islam et al. 2022, *Cell Genomics*): 300 tumours × 9 cancer types, generated from 21 COSMIC reference SBS signatures. The full COSMICv3.3 SBS panel (79 signatures) was used as the refitting input to emulate realistic over-complete inputs. Sensitivity, specificity, and F1 were computed at three noise levels [@DiazGay2023].

**Runtime.** 2700 samples processed in 9.6 min (0.21 s/sample). Memory usage was low and comparable to competing tools [@DiazGay2023].

## Key Findings

- SigProfilerAssignment achieved the highest F1 score at every noise level (0%, 5%, 10%) across 9 cancer types and most individual signatures.
- At 10% noise, SigProfilerAssignment was the **only** tool to achieve F1 > 0.90; all others fell below this threshold.
- The tool maintained high precision (low false-positive signatures) while improving sensitivity relative to alternatives — a balance other tools sacrificed (MutationalPatterns standard mode: high recall, poor precision; MutationalPatterns strict mode: better precision, very slow; sigLASSO and deconstructSigs: L1/post-hoc penalties improved precision at the cost of sensitivity).
- DBS, ID, and CN benchmarks (Supplementary) showed F1 > 0.85 across all noise levels.
- Probabilistic per-mutation signature assignment is a novel capability absent from all prior refitting tools, enabling attribution of specific driver mutations to their mutagenic process.
- CN signature assignment is also novel; CN signatures are predictors of clinical survival (Drews et al. 2022; Steele et al. 2022).

## Relevance

**Direct relevance to hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and (agnostic covariate–signature-exposure association).**

hypothesis:0007 proposes treating per-sample signature exposure vectors (H, the NMF coefficient matrix) as phenotypes and running a phenome-wide association against clinical and molecular covariates to recover known aetiologies (UV/SBS7, smoking/SBS4, APOBEC/SBS2+13, MMR/SBS6+15) as positive controls. SigProfilerAssignment is the natural **assignment engine** for generating per-sample H vectors from COSMIC reference signatures — the refitting step that precedes the association analysis.

Key connections:
1. **Positive-control recovery.** SigProfilerAssignment's high-precision refitting (F1 > 0.90 at 10% noise) means that the H vectors fed into the hypothesis:0007 association will have low false-positive signature activations, which is critical for specificity of the downstream covariate associations.
2. **Sparse refitting aligns with hypothesis:0007's within-tissue design.** The forward stagewise selection suppresses spurious co-activations that could generate artifactual covariate correlations — an important property when running multiplicity-corrected associations across hundreds of signatures and covariates.
3. **CN signature support.** hypothesis:0007 could extend beyond SBS to CN signatures without a different tool, enabling association of chromosomal instability exposures with clinical variables (e.g., stage, survival, treatment).
4. **Per-mutation assignment.** The probabilistic mutation-level output could enable a finer-grained variant of hypothesis:0007 where driver-gene mutation burdens are attributed to specific signatures before association, linking mutational aetiology directly to driver gene activation.
5. **Cross-study meta-analysis context.** The cbioportal pipeline aggregates heterogeneous cBioPortal studies as pseudo-cohorts; SigProfilerAssignment accepts standard VCF/MAF inputs and can be applied per-study before the cross-study aggregation step, inserting cleanly into the existing Snakemake DAG.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Signature refitting (assignment) | Downstream step after cross-study aggregation | H matrix generation for hypothesis:0007 association |
| COSMIC SBS/DBS/ID/CN reference signatures | Known signature catalogue | COSMICv3.3; 79 SBS signatures used in benchmarking |
| Per-sample activity vector a | Exposure / H column | Input to phenome-wide association in hypothesis:0007 |
| Forward stagewise sparse selection | Sparse regularisation | Prevents false-positive activations; complements NNLS |
| Probabilistic per-mutation assignment | Mutation-level attribution | Novel; could augment driver-gene aetiology analysis |
| Noise robustness (0-10%) | Study heterogeneity robustness | Relevant for cross-study aggregation where panel/WES mixing adds noise |

## Limitations

- Benchmarking uses **synthetic** data only; no real-cohort validation with known ground-truth exposures (e.g., melanoma SBS7, lung SBS4) is presented.
- The forward stagewise thresholds (1% for removal, 5% for addition) are fixed and not tunable via the published interface; sensitivity to these hyperparameters is not characterised in the main text.
- Probabilistic per-mutation assignment is only available when individual mutations (VCF/MAF) are provided, not from aggregated count vectors — relevant when working from pre-aggregated cross-study tables that have already lost per-mutation identity.
- CN signature benchmarking details are deferred to supplementary data; performance on real CN data (which is noisier than SBS) is not assessed in the main text.
- Tools comparison does not include SigFit (Robles-Espinoza et al. 2016) or more recent Bayesian methods (e.g., HDP-based).
- Runtime comparison is favourable but the 2700-sample benchmark may not reflect very large cohorts (>10,000 samples) where memory or parallelisation becomes the bottleneck.

## Model / Tool Availability

- **GitHub:** https://github.com/AlexandrovLab/SigProfilerAssignment
- **Web interface:** https://cancer.sanger.ac.uk/signatures/assignment/
- **License:** BSD 2-clause (open source)
- **Language:** Python (part of the SigProfiler ecosystem)
- **Installation:** `pip install SigProfilerAssignment` (AlexandrovLab standard)
- **Input:** VCF, MAF, or tab-delimited mutation matrix; COSMIC reference signatures bundled
- **Output:** Per-sample signature activities, per-mutation signature probabilities (when VCF/MAF input)

## Follow-up

- Islam et al. 2022 (*Cell Genomics*) — SigProfilerExtractor (de-novo extraction companion); benchmarking dataset source.
- Steele et al. 2022 (*Nature*) — CN signature compendium; motivates CN assignment support.
- Degasperi et al. 2022 (*Science*) — SignatureToolsLib + UK WGS cohort; direct competitor.
- Consider integrating SigProfilerAssignment as a Snakemake rule (e.g., `assign_signatures`) that runs per-study or on the merged MC3 pseudo-study, producing `studies/{id}/mut/signatures/activities.feather` as input for hypothesis:0007 association analysis.
- Question worth raising: does the forward stagewise tolerance (1%/5%) need tuning for the cross-study setting where mutation counts per sample vary by orders of magnitude (panel ~100 muts vs. WGS ~10,000 muts)?
