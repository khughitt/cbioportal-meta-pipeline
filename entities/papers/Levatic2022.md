---
type: paper
title: Mutational signatures are markers of drug sensitivity of cancer cells
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Levatic2022
ontology_terms:
- mutational signatures
- drug sensitivity
- cancer cell lines
- DNA repair
- germline correction
datasets: []
source_refs:
- cite:Levatic2022
related: []
---

# Mutational signatures are markers of drug sensitivity of cancer cells

- **Authors:** Jurica Levatic, Marina Salvadores, Francisco Fuster-Tormo, Fran Supek
- **Year:** 2022
- **Journal:** Nature Communications
- **DOI/URL:** https://doi.org/10.1038/s41467-022-30582-3
- **BibTeX key:** Levatic2022
- **Source:** PDF

## Key Contribution

Mutational signatures inferred from cancer cell line exomes — after correcting for ancestry-matched germline contamination — are as numerous and predictive as established genetic markers (driver mutations, CNAs, DNA methylation) for forecasting drug sensitivity across 518 drugs and 930 cell lines in GDSC. Signatures of prior exposure to DNA-damaging agents (e.g. SBS25L: chemotherapy; SBS42L: haloalkane; SBS4/45L: tobacco) tend to predict drug *resistance*, whereas signatures of DNA-repair deficiency (MMR, BER, HR, NER) tend to predict drug *sensitivity*. Replicated associations (FDR<15%, 3-way replication across GDSC, PRISM, and CRISPR Project SCORE) number 290 for mutational signatures, matching or exceeding replicated hits for driver mutations (37) and CNAs (55) in their test.

## Methods

**Data:** WES BAM files for 1,072 cancer cell lines from GDSC, matched against TCGA normal exomes (n=6,154) for ancestry correction. Drug IC50s from GDSC (518 drugs, 930 cell lines) and PRISM (1,502 drugs, 348 overlapping cell lines). CRISPR fitness scores from Project SCORE (517 overlapping cell lines).

**Ancestry-matched germline subtraction:** Because matched normal tissue from the same individual is unavailable for cell lines, the authors clustered cell line exomes with TCGA germline exomes on 150 principal components of common germline variants (using the `tclust` algorithm) into 13 ancestry clusters. The median germline trinucleotide spectrum of the matched cluster was subtracted from each cell line's observed spectrum to recover the somatic mutation spectrum. This ancestry-matching procedure significantly reduced reconstruction error (mean absolute error 68.8 vs 124.1 for simple MAF-filtering; Wilcoxon p < 2.22e-16) and outperformed regressing out signature 1/5 or SNP-signature approaches.

**Signature extraction:** NMF on 96-trinucleotide spectra from 930 cell lines, jointly with indel features, benchmarked against known COSMIC SBS signatures by cosine similarity (≥0.85 threshold = 1.8% FDR). Yielded 30 matched SBS signatures + 22 "like" variants + 5 cell-line-specific signatures (SBS-CL). Exposure assignment tested multiple approaches (sigproSS, sigLasso, custom regularized NMF regression).

**Predictive modeling:** Random Forest (RF) regression per drug per cancer type predicting log IC50, using signature exposures as features. Cross-validated RRMSE (relative RMSE). Compared against oncogenic mutations (470 driver genes), focal CNAs (425 genes), DNA methylation at CpG islands (38 genes), and mRNA expression (1,564 genes in L1000 or drug target genes).

**Replication testing:** Randomization-based test (Cohen's d statistic, 100,000 permutations) requiring FDR<15% in both GDSC and PRISM (external replication) or in GDSC and Project SCORE (pharmacological + genetic co-replication) or across two drugs with the same molecular target (internal replication). "Silver set" required replication in ≥1 method; "golden set" required ≥3 tissues or ≥3 methods with d>0.5, p<0.005.

## Key Findings

1. **Mutational signatures outperform other marker types for drug response prediction.** Average rank for mutational signature features in RF models was 3.75 vs 4.20–4.49 for other genomic/epigenomic feature types (corrected Friedman test, p<0.05). Signatures outperformed CNAs (13/16 cancer types) and DNA methylation (10/16 cancer types).

2. **Ancestry-corrected signatures surpass prior cell-line signature methods.** The ancestry-matching approach outperformed two recently published cell-line mutational signature methods (refs 31, 32) in 22/27 and 25/27 cancer types respectively, confirming that germline contamination correction is critical before associating signatures with drug response.

3. **290 replicated signature–drug associations.** At FDR<15%, 290 associations replicated across at least two independent tests. This exceeds driver mutation hits (37) and CNA hits (55) and matches DNA-methylation hits (64). A "golden set" of 995 highest-confidence associations (including driver/CNA/methylation markers) is provided as a drug repurposing resource.

4. **DNA repair deficiency signatures predict sensitivity; prior-exposure signatures predict resistance.**
   - MMR-failure signatures (SBS6, 15, 21, 26, 44 and related) associate with sensitivity to AKT inhibitors (afuresertib, MK-2206, AZD5363, uprosertib, ipatasertib) across colorectal, ovarian, gastric, skin, and prostate cancers — replicating in CRISPR k.o. of *WRN*.
   - BER signatures (SBS36/56L) and NER-related (SBS88L/4L) associate with sensitivity to EGFR/ERBB2 inhibitors.
   - Prior-exposure signatures (SBS25L chemotherapy, SBS18/36L reactive oxygen species, SBS42L haloalkane, SBS11 DNA methylating agent, SBS22L aristolochic acid, SBS4/45L tobacco/PAH adducts) are enriched among resistance associations, consistent with selection for DNA replication/repair robustness in cells pre-exposed to mutagens.

5. **Oncogene-addiction positive controls recaptured.** The analysis re-identified ERBB2 amplification sensitivity to afatinib/osimertinib, MET amplification to crizotinib/savolitinib, BRAF mutations in skin to dabrafenib/vemurafenib, and CDKN2A-loss in brain cancer to palbociclib — validating the overall framework with established clinical biomarkers.

6. **ARID1A mutation → AKT2 inhibitor sensitivity.** *ARID1A*-mutant colorectal and ovarian cancer cell lines are more sensitive to AKT2 k.o. by CRISPR and to pan-AKT inhibitors, corroborating PI3K/AKT/MTOR inhibition as a therapeutic strategy in *ARID1A*-mutant tumors (mechanistically linked to reported MMR activity loss in ARID1A-mutant cells).

7. **TP53-mutant vulnerability to CHK inhibition.** *TP53*-mutant cells are sensitized to MK-8776 (CHK1 inhibitor) and CDK2/CDK6 across multiple cancer types (BLCA, BRCA, GBM/LGG, LUAD, SKCM), replicated by CRISPR k.o. of *CHEK2*, *CDK2*, and *CDK4*.

8. **SBS-CL5 (cell-line specific indel-rich signature) associates with sensitivity to ATR inhibitors** (AZD6738, VE-822, VE-821), PARP inhibitors (olaparib, rucaparib, niraparib), replicated in *ATR* gene knockout — demonstrating utility of indel signatures for predicting response to DNA-repair targeting drugs.

## Relevance

This paper is directly relevant to hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and:

- **Positive-control benchmark:** Levatic et al. demonstrate that DNA repair deficiency signatures (MMR SBS6/15/26, HR, NER) associate robustly and replicably with drug sensitivity phenotypes. This establishes that known signature aetiologies have detectable downstream consequences in orthogonal data — the same logic underpins the prediction that known exposure→signature links (UV↔SBS7, smoking↔SBS4, APOBEC↔SBS2/13, MMR↔SBS6/15/26) should re-emerge in an agnostic covariate scan.

- **Prior-exposure signatures as resistance markers:** The finding that SBS25L (chemotherapy), SBS42L (haloalkane), and SBS4/45L (tobacco) associate with drug *resistance* illustrates a confounding pattern relevant to our cross-study analysis: tumors from heavily pre-treated patients will carry chemotherapy-exposure signatures that correlate with poor prognosis / resistance, mimicking an exposure aetiology. In the cBioPortal context — where treatment history is inconsistently recorded — this is a concrete example of the "R4 — batch/study artifact" alternative explanation flagged in the hypothesis.

- **Ancestry-matched germline correction as methodological template:** The ancestry-matching approach (cluster cell lines with TCGA normal exomes, subtract cluster-median germline spectrum) is a systematic solution to the unmatched-normal problem. This is relevant to `topic:signature-decomposition-unmatched-normal` and question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross. The cBioPortal pipeline faces the same challenge for panel-sequenced tumors without paired normals.

- **Mutational signatures complement, rather than replace, expression for drug prediction:** Figure 2d–e shows that gene expression is the single strongest predictor but that signatures add complementary, expression-independent signal for ~50% of predictive drug-tissue pairs. This is consistent with the cross-decomposition concordance rationale: expression and mutation factors can be jointly informative about shared upstream drivers.

- **MMR signatures predict AKT inhibitor sensitivity via ARID1A:** This mechanistic link (MMR deficiency ↔ ARID1A mutation ↔ AKT2 dependency) is an example of the kind of trans-omic causal chain that the agnostic association could surface — a signature (MMR) points to an expression program (ARID1A-driven transcription) and a drug vulnerability, all recoverable from the mutation data alone.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Ancestry-matched germline subtraction (13 TCGA clusters) | `topic:signature-decomposition-unmatched-normal` | Directly applicable to cBioPortal unmatched-normal problem |
| SBS-CL (cell-line-specific signatures) | Artifact signatures (SBS27/43/45–60 in COSMIC) | Cell-line culture may generate signatures not present in tumors |
| GDSC/PRISM/PSCORE replication framework | Within-study vs cross-study replication | Three-way replication is the gold standard; our cBioPortal cross-study design is analogous |
| Prior-exposure signatures → resistance | Treatment-history confound in cBioPortal | cBioPortal studies vary in treatment status; pre-treated cohorts inflate chemotherapy-exposure signatures |
| NMF joint SBS+indel extraction | signature modality choice (SBS only vs joint) | Indel signatures added >5 SBS-CL associations; worth considering for hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and |
| Random Forest per-drug-tissue predictive models | covariate association layer | RF used here for IC50 prediction; hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and uses association/regression for exposure~covariate |

## Limitations

- **Cell lines vs tumors:** Culture conditions may introduce or deplete signatures (SBS-CL signatures, reduced APOBEC activity in culture). The drug response in vitro may not reflect clinical response, particularly for immune-related mechanisms.
- **Cross-sectional / associative:** The paper explicitly cautions that associations do not imply causality — a signature could mark a co-occurring driver mutation (e.g. ARID1A mutation ~ MMR deficiency) rather than being the functional predictor.
- **Prior-exposure confounding:** A cell line's signature of prior carcinogen exposure reflects its evolutionary history, not necessarily its current DNA repair capacity. This makes mechanistic interpretation ambiguous for exposure-type signatures.
- **Panel vs WES:** Inference was done on WES data. Extension to panel-sequenced tumors (the dominant cBioPortal data type) is not directly addressed — acknowledged by authors as a future refinement (WGS would improve indel resolution further).
- **Statistical power at tissue level:** For rare cancer types with few cell lines, associations are underpowered. The authors flag this, noting that permissive thresholds (p<0.005) may be supporting evidence rather than primary results.
- **Treatment history not controlled:** Prior drug exposure in patients or cultures could both generate exposure-type signatures and confer resistance — confounding the resistance associations.

## Model / Tool Availability

- Source code and data deposited with the paper (Supplementary Data S1–S11 provided; specific code repo not explicitly named in reviewed sections).
- The "golden set" of 3,911 silver-tier and 995 golden-tier drug–marker associations is provided as Supplementary Data S8 — a resource for drug repurposing guided by mutational signature markers.

## Follow-up

- **Methodological:** The ancestry-matching germline subtraction approach warrants review for adapting to the cBioPortal panel-sequenced context (partial exome coverage, no TCGA cluster-match available for non-TCGA cohorts). See `topic:signature-decomposition-unmatched-normal`.
- **Design input:** The replication framework (GDSC × PRISM × PSCORE) is a model for the cross-study replication design. The "golden set" criteria (≥3 tissues or ≥3 methods, d>0.5, p<0.005) could inform the effect-size thresholds and FDR regime for association reporting.
- **Prior-exposure artifact audit:** Before finalizing hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and, audit cBioPortal studies for treatment-exposed cohorts whose samples will carry chemotherapy/radiation signatures — a structured confound that should be treated as a covariate or excluded from the positive-control arm.
- **Related papers to read:** Degasperi2022 (SigProfiler, already summarized); papers on WRN synthetic lethality in MMR-deficient tumors; Ellrott et al. [@Ellrott2018] MC3 (for matched-normal TCGA baseline).
