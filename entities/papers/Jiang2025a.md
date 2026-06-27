---
type: paper
title: The Impact of Variant Calling on Substitution Mutational Signature Inference
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Jiang2025a
ontology_terms:
- mutational signatures
- variant calling
- somatic mutation
- single base substitution
- NMF
- de novo signature extraction
datasets: []
source_refs:
- cite:Jiang2025a
related: []
---

# The Impact of Variant Calling on Substitution Mutational Signature Inference

- **Authors:** Zichen Jiang, Jessica N. Au, Mariya Kazachkova, Marcos Diaz-Gay, Raviteja Vangara, Ludmil B. Alexandrov
- **Year:** 2025
- **Journal:** bioRxiv preprint (December 2025; not peer-reviewed)
- **DOI/URL:** https://doi.org/10.64898/2025.12.09.693327
- **BibTeX key:** Jiang2025a
- **Source:** PDF

## Key Contribution

Somatic variant calling strategy is a previously underappreciated upstream determinant of de novo single-base substitution (SBS) mutational signature extraction. Using matched TCGA WES (>8,900 tumors, MC3 vs. GDC harmonized releases) and PCAWG WGS (>1,800 tumors, five independent variant callers) cohorts, the authors demonstrate that consensus calling (requiring agreement between at least two callers) yields stable, biologically interpretable signatures robust to genome build and pipeline version changes, whereas single-caller outputs introduce reproducible, algorithm-specific artifactual signatures. A minimal two-caller consensus is sufficient to eliminate these artifacts while preserving true biological signal, and this holds across multiple SBS context resolutions (SBS-96 through SBS-4608) and across three independent signature extraction frameworks.

## Methods

**Cohorts:**
- *TCGA WES:* 8,908 primary tumors common to the legacy MC3 release (GRCh37; MuTect/VarScan2/MuSE, 2+/3 consensus) and the GDC harmonized release (GRCh38; MuTect2/VarScan2/MuSE, 2+/3 consensus). Also used controlled-access per-caller VCFs for 736 TCGA-BRCA tumors.
- *PCAWG WGS:* 1,857 primary tumors (≥50 samples per cancer type) with consensus 2+/4 calls (MuTect v1.14, MuSE v1.0rc, CaVEMan v1.5.1, DKFZ pipeline v0.1.19) and additionally recalls by Hartwig Medical Foundation's SAGE caller for 2,376 samples.
- *PCAWG Breast-AdenoCA:* 185 tumors with per-caller VCFs from all five tools used as principal case study.

**Mutational matrices:** SigProfilerMatrixGenerator v1.3.3; contexts SBS-96, SBS-192, SBS-288, SBS-1536, SBS-4608.

**Signature extraction:** Primary tool SigProfilerExtractor v1.2.1 (NMF-k, Kullback-Leibler divergence minimization, Poisson resampling); validation with MuSiCal v1.0.0 and SignatureToolsLib v2.4.6.

**Decomposition to COSMIC reference:** `decompose_fit` in SigProfilerAssignment v0.1.9 against COSMICv3.4 reference set (biologically irrelevant signatures excluded prior to decomposition for breast tissue analyses).

**Profile stability assay:** 1,000 Poisson resamplings of per-sample SBS-96 profiles to quantify mutation-burden-dependent profile reliability.

**Manual validation:** BAM inspection in IGV for mutations exclusive to individual callers, focusing on characteristic trinucleotide contexts of artifactual signatures.

## Key Findings

1. **Consensus calling yields stable signatures across pipeline versions.** Despite a 21% difference in total SBS counts between MC3 (GRCh37) and GDC (GRCh38) for the same TCGA tumors, de novo signatures extracted from both consensus call sets were highly concordant (cosine similarity ≥0.95 for individual signatures across 24 of 32 cancer types tested with the same k). Mutational profiles at the sample level converged more strongly with higher tumor mutation burden (Spearman's ρ=0.833; p<0.0001).

2. **Mutation burden threshold for WES profile stability.** Poisson resampling revealed that WES samples need at least ~383 SBSs to maintain stable SBS-96 profiles (95% of resampled profiles reach cosine similarity ≥0.95 above this threshold).

3. **Individual callers introduce reproducible artifactual signatures in WES.** In TCGA-BRCA, VarScan2 and MuSE each produced a caller-exclusive de novo signature (SBS96C and SBS96D respectively) not present in the consensus baseline. Both signatures lacked COSMIC matches, affected 23-41% of mutations in their respective call sets, and localized to repeat-masked/tandem-repeat regions with sequencing strand bias and low read depth (<30×) — hallmarks of false positives.

4. **Individual callers introduce reproducible artifactual signatures in WGS.** In PCAWG Breast-AdenoCA (185 WGS tumors, five callers), the 2+/5 consensus baseline yielded nine biologically interpretable de novo signatures (clock-like aging SBS1/5, APOBEC SBS2/13, HRD SBS3/8, ROS SBS18, and signatures of unknown aetiology SBS17a/b, SBS28, SBS34, SBS37, SBS39, SBS40a). MuTect added two artifactual signatures (SBS96I — matches COSMIC artifact SBS50 at cosine 0.86; SBS96J — matches SBS51+SBS60 at cosine 0.98). SAGE added one artifactual signature (SBS96H) driven by low-VAF calls from reads spanning a single ~100 bp insert. Applying a VAF≥0.05 filter or removing calls with ≤2 alternate reads eliminated SBS96H and recovered the nine-signature consensus solution. MuTect's SBS96J was independently recapitulated by DKFZ (cosine 0.95).

5. **Two-caller consensus is sufficient to eliminate artifacts.** Any pairwise intersection of two callers, regardless of which pair, effectively eliminated the artifactual signatures, with minimum cosine similarity to the five-caller ground truth of ≥0.975. The artifactual signatures were replicated in all three extraction frameworks (SigProfilerExtractor, MuSiCal, SignatureToolsLib), confirming they originate from variant callers rather than extraction algorithms.

6. **Artifact severity worsens at higher context resolution.** Discordance between individual callers increased with the number of SBS channels (SBS-288, SBS-1536, SBS-4608), making high-resolution analyses especially susceptible. Two-caller consensus also resolved artifacts in SBS-288 analyses.

## Relevance

**Direct relevance to hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and** (agnostic covariate↔signature-exposure association; positive-control recovery of UV/smoking/APOBEC/MMR):

- The MC3 dataset ingested by this pipeline uses a consensus 2+/3 calling approach (MuTect, VarScan2, MuSE, GRCh37), which this paper validates as a robust upstream choice. The TCGA GDC harmonized release (GRCh38) is equally valid under consensus calling. This removes a major methodological concern for hypothesis:0007's positive-control recovery experiments.
- The finding that individual callers produce reproducible artifactual signatures that mimic novel biological processes is directly relevant to interpreting any signature extracted from per-study cBioPortal MAFs, which may originate from single callers. Known-signature recovery (UV, APOBEC, aging) should be more reliable from consensus-called studies; studies with single-caller provenance may surface artifactual signatures that confound covariate associations.
- The artifact signatures (SBS96C/D from VarScan2/MuSE; SBS96I/J from MuTect; SBS96H from SAGE) localize to repetitive regions, low-coverage sites, and low-VAF calls — overlapping with variant classes that may be enriched in studies without matched-normal sequencing. This is a confounder for hypothesis:0007's across-study analysis and strengthens the rationale for the CH-aware matched-normal stratification already in the pipeline.
- The minimum mutation burden threshold of ~383 SBSs for stable WES profiles has practical implications: cBioPortal studies with low per-sample mutation counts (e.g., pediatric or microsatellite-stable cancers) will be unreliable substrates for per-sample signature decomposition, and sample-level covariate association in hypothesis:0007 should exclude such low-burden samples.

**Cross-study meta-analysis angle:** This study benchmarks precisely the two TCGA processing regimes (MC3 and GDC) that the cbioportal pipeline uses. The stability result (consensus → robust signatures across genome builds) validates using pooled TCGA data as a positive-control substrate for hypothesis:0007 signature recovery, as long as only consensus-called studies are included in the pool.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Consensus 2+/3 variant calling | `matched_normal_studies` + MC3 ingest | MC3 is already flagged as matched-normal consensus in pipeline config |
| Artifactual de novo signatures from single callers | Confounders in per-study signature decomposition | Single-caller cBioPortal studies may introduce systematic false-positive signatures |
| Mutation burden threshold ≥383 SBSs (WES) | TMB / hypermutator annotation | Threshold for reliable per-sample profile; informs sample exclusion for hypothesis:0007 covariate analysis |
| Caller-exclusive mutations in repeat/low-coverage regions | CH contamination (unmatched normals) | Both sources inflate certain mutation types systematically |
| SBS50/SBS51/SBS60 (COSMIC artifact signatures) | Artifact filtering step | Known artifact signatures that should be excluded from COSMIC reference set during decomposition |

## Limitations

- Study restricted to SBS signatures; insertions/deletions and structural variants not evaluated, and caller effects there may differ.
- WES data limited to TCGA-BRCA for individual-caller comparisons (due to controlled-access requirements); generalizability across cancer types for individual-caller artifacts is inferred from the PCAWG WGS analysis.
- The minimal 2-caller consensus finding is demonstrated on five specific callers; it is unclear whether the result holds for all possible caller combinations or for less commonly used tools.
- Focuses on de novo extraction; impact of variant calling on signature refitting/decomposition (fitting to a known reference catalog) is not directly examined.
- No analysis of the impact on indel (ID) or doublet (DBS) signature classes.
- Preprint: not yet peer-reviewed as of the summary date.

## Model / Tool Availability

- Code and analysis scripts: not explicitly linked in the preprint text; data are available from cBioPortal (MC3), GDC Data Portal (GDC harmonized TCGA), ICGC Data Portal (PCAWG VCFs), and European Genome-Phenome Archive (PCAWG BRCA-EU BAMs).
- SigProfilerExtractor v1.2.1, SigProfilerAssignment v0.1.9, MuSiCal v1.0.0, SignatureToolsLib v2.4.6 are publicly available Python/R packages.

## Follow-up

- Characterize which cBioPortal studies in the pipeline use single callers vs. consensus approaches; flag single-caller studies as higher-risk for artifactual signatures when planning hypothesis:0007 covariate association.
- Evaluate whether artifact signatures (SBS50, SBS51, SBS60-like) appear when performing de novo extraction on aggregated cross-study cBioPortal mutation data; if so, trace to specific studies/callers.
- The ~383 SBS threshold for WES profile stability should be integrated as a per-sample filter in the hypothesis:0007 signature decomposition step, alongside the existing hypermutator filter.
- Consider whether the SBS-288 (transcriptional strand bias) context results in this paper motivate moving beyond SBS-96 for the cross-study aggregation; the authors show extended contexts are more sensitive to variant caller artifacts but that two-caller consensus still rescues clean extraction.
