---
type: paper
title: Mutational processes of tobacco smoking and APOBEC activity generate protein-truncating
  mutations in cancer genomes
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Adler2023
ontology_terms:
- mutational signatures
- stop-gain mutations
- APOBEC
- tobacco smoking
- protein truncation
- tumor suppressor genes
- pan-cancer
datasets: []
source_refs:
- cite:Adler2023
related: []
---

# Mutational processes of tobacco smoking and APOBEC activity generate protein-truncating mutations in cancer genomes

- **Authors:** Nina Adler, Alexander T. Bahcheli, Kevin C. L. Cheng, Khalid N. Al-Zahrani, Mykhaylo Slobodyanyuk, Diogo Pellegrina, Daniel Schramek, Juri Reimand
- **Year:** 2023
- **Journal:** Science Advances, Vol. 9, No. 44, eadh3083
- **DOI/URL:** https://doi.org/10.1126/sciadv.adh3083
- **BibTeX key:** Adler2023
- **Source:** PDF

## Key Contribution

This study characterizes the protein-coding impact of single-base substitution (SBS) mutational signatures across 12,341 cancer genomes from 18 cancer types. The central finding is that stop-gain mutations (SGMs; nonsense mutations) are strongly and consistently enriched in the SBS signatures of tobacco smoking (SBS4/SBS29), APOBEC cytidine deaminases (SBS13), and reactive oxygen species (SBS18), while other SBS classes (missense, silent) are not. This enrichment is mechanistically explained by the trinucleotide preferences of these mutational processes: their preferred substitution contexts happen to convert specific serine and glutamic acid codons into stop codons at high frequency. The study thereby provides direct evidence that specific exogenous and endogenous mutational processes cause protein loss-of-function at scale, connecting mutational process aetiology to functional genomic consequences.

## Methods

**Cohorts.** Three independent pan-cancer genomic datasets were analysed:
- PCAWG (n = 2,360 WGS, primary cancers from ICGC/TCGA)
- HMF (n = 3,472 WGS, metastatic cancers from Hartwig Medical Foundation)
- TCGA PanCanAtlas (n = 6,509 WES, primary cancers)

Hypermutated samples were excluded (>90,000 SNVs in WGS; >1,800 SNVs/Mbp in WES). After QC, a total of 1.75 million exonic SNVs were annotated by protein-coding consequence (missense 67.4 %, silent 27.7 %, SGM 4.6 %, stop-loss 0.1 %, start-loss 0.1 %) using ANNOVAR.

**Signature assignment.** SBS signatures from the COSMIC v3 catalog were used. For PCAWG, consensus signature exposures from the PCAWG working group were used. For TCGA and HMF, per-sample signature assignment was performed with SigProfilerSingleSample (v0.0.0.27). Each SNV was assigned to the most probable SBS signature per sample.

**Enrichment analysis.** A Fisher's exact test framework tested whether each SNV functional class was enriched in specific SBS signatures compared to the exome-wide distribution, across cancer types and cohorts separately. FDR correction was applied (Benjamini-Hochberg). Probabilistic reassignment over 100 iterations was used to account for annotation uncertainty.

**Gene-level analysis.** Genes with significantly enriched SGMs from the three major signatures (SBS4, SBS13, SBS18) were identified via one-tailed Fisher's exact tests comparing SGM distributions per gene against all SGMs in all genes. Brown's method merged p-values across datasets.

**Pathway enrichment.** ActivePathways (integrative pathway enrichment) was applied to the gene-level enrichment p-values across cancer types.

**Amino-acid and genetic code analysis.** The proportions of amino acids substituted to stop codons were computed; trinucleotide profiles of SGMs were compared to COSMIC reference profiles using cosine similarity (COS). Genetic code diagrams illustrate how specific mutational contexts create stop codons from serine (TCA/TCG codons → C>G/C>A transversions, SBS13) and glutamic acid (GAA/GAG codons → T[C>A]N transversions, SBS4/SBS18) residues.

**Copy number and biallelic inactivation.** For the 56 SGM-enriched genes, co-occurring genomic copy number losses in the same tumour samples were assessed.

**Clinical/molecular correlates.** Associations of SGM burden with smoking history (TCGA), cancer subtype, APOBEC3 gene expression (RNA-seq, median-dichotomised), and DNA motif context (YTCA vs RTCA) were tested. APOBEC3A/B knockout cell line data (BT-474 breast cancer) from external WGS experiments were also analysed.

## Key Findings

1. **SGMs are disproportionately driven by three mutational processes.** Tobacco smoking (SBS4), APOBEC (SBS13), and reactive oxygen species (SBS18/SBS36) are robustly enriched in SGMs across all three cohorts and multiple cancer types, while other signatures (including clock-like SBS1/SBS5) are not.

2. **Mechanistic explanation via genetic code.** The enrichment is not random: the trinucleotide preferences of SBS13 (C>G and C>A in TCN context) convert serine and glutamic acid codons to stop codons (TGA, TAA, TAG). SBS4's T[C>A]N transversions convert adjacent glutamic acid codon pairs into stop codons. This explains why serine and glutamic acid are disproportionately replaced by stops in APOBEC and tobacco smoking signatures respectively.

3. **SGMs converge on core tumour suppressor genes and hallmark pathways.** 56 genes with significantly enriched signature-associated SGMs were identified across six cancer types. These include TP53 (SBS4/SBS13 in lung, head/neck), FAT1 (SBS13 in head/neck, 21 APOBEC-associated SGMs), APC (SBS18 in colorectal), STK11, RB1, NF1, CDH1, CDKN2A, TGFBR2, ARID1A, and MGA. About 43 % are known cancer genes in the COSMIC Cancer Gene Census, far more than expected by chance.

4. **Biallelic inactivation evidence.** The SGM-enriched genes carry both SGMs and copy number losses in 58.9 % or more of relevant cancer samples (e.g. TP53: 67.1 %, FAT1: 73.3 %), consistent with classic two-hit tumour suppressor inactivation.

5. **Smoking-history dose-response.** Lung cancer patients with greater tobacco exposure have significantly higher SBS4-associated SGM burden; lifelong nonsmokers have the fewest SGMs, and the gradient is statistically significant across smoking history categories (FDR < 0.01).

6. **APOBEC3A expression correlates with SGM burden.** Breast cancer samples with higher APOBEC3A expression carry significantly more SBS13-associated SGMs (P = 1.3 × 10⁻⁶). APOBEC3A knockout in BT-474 cells significantly reduces SGM burden; APOBEC3B knockout does not, implicating APOBEC3A as the dominant enzymatic driver of SBS13-associated SGMs. YTCA motif enrichment of SBS13 SGMs (consistent with APOBEC3A preference) was confirmed across cohorts.

7. **HER2+ breast cancer has 3× more APOBEC-driven SGMs.** This is consistent with higher reported APOBEC activity in HER2-amplified tumours.

8. **ROS signature enrichment in metastatic colorectal cancers.** SBS18 (ROS) SGMs are enriched in metastatic CRC in HMF, and APC is the most enriched gene, consistent with Wnt pathway disruption by oxidative stress.

9. **SGM expansion as a mechanism of tumour heterogeneity.** Because SGMs arise stochastically from ongoing mutational processes, they increase tumour heterogeneity, offer targets for synthetic lethality, and may serve as biomarkers for mutational-process activity.

## Relevance

**Direct support for hypothesis:0007 positive controls.** This paper is highly relevant to hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and because it provides detailed, independently validated ground-truth links between exposures/covariates and specific SBS signatures that the hypothesis:0007 positive-control prong must recover:

- **Smoking→SBS4:** Smoking history (a clinical covariate already present in cBioPortal) associates with SBS4 SGM burden in lung adenocarcinoma, providing the exact within-tissue positive-control arm specified for hypothesis:0007.
- **APOBEC3A expression→SBS13:** APOBEC3A mRNA level (available via `export_study_expression.py`) associates with SBS13 SGM burden in breast cancer, a second arm of the hypothesis:0007 positive control.
- **The mechanistic specificity (trinucleotide context → genetic code → stop codons) shows that SBS13 and SBS4 have functionally distinct consequences,** strengthening the rationale for treating them as separable signals in signature-exposure association analyses.

**Additional relevance for the cross-study pipeline:**
- The paper confirms that APOBEC enrichment is predominantly driven by SBS13 (not SBS2), with SBS2 more often enriched in silent mutations — this distinction matters for how signature exposures are interpreted when the pipeline aggregates across studies using SigProfilerSingleSample assignments.
- The three-cohort validation design (TCGA WES + PCAWG WGS + HMF WGS metastatic) closely mirrors the pipeline's use of heterogeneous data sources; the finding that SGM enrichments replicate across all three supports the cross-study aggregation strategy.
- The YTCA motif specificity of SBS13 provides a mechanistic fingerprint that could distinguish APOBEC3A- vs APOBEC3B-associated signature contributions in cohorts where expression data is unavailable.
- Loss-of-function enrichment in core driver genes (TP53, APC, STK11, NF1) is consistent with the pipeline's existing Bailey driver overlay [@Bailey2018] and the CH-annotation framework (noting TP53 is in the Bolton 7-gene CH priority list [@Bolton2020]).

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| SBS signatures (COSMIC v3) | `SBS4`, `SBS13`, `SBS18` in signature decomposition | Consistent with COSMIC v3 used in SigProfilerSingleSample |
| Stop-gain mutations (SGMs) | Functional annotation layer (ANNOVAR `stopgain`) | `convert_to_feather.py` ingests mutation consequence; SGMs are a subset of exonic SNVs |
| Tobacco smoking signature (SBS4) | Positive-control arm: smoking→SBS4 (hypothesis:0007) | Smoking history clinical variable available in cBioPortal studies |
| APOBEC3A expression ↔ SBS13 | Positive-control arm: APOBEC3-expr→SBS2/13 (hypothesis:0007) | mRNA accessible via `export_study_expression.py` |
| TCGA / PCAWG / HMF cohorts | `studies` list in pipeline configs; `tcga_mc3` pseudo-study | Cross-cohort replication mirrors pipeline's multi-study aggregation |
| Bailey driver genes (CGC overlap) [@Bailey2018] | `annotate_drivers.py` → `bailey2018_driver` flag | 43% of SGM-enriched genes are known cancer genes |
| TP53 (CH priority gene) | `ch_priority_gene` flag (Bolton list [@Bolton2020]) | SBS4- and SBS13-driven SGMs converge on TP53 |
| Hypermutator exclusion thresholds | `is_hypermutator` flag / GMM pipeline (t081) | Paper excludes >90k SNVs WGS / >1800 SNV/Mb WES; comparable to pipeline thresholds |

## Limitations

- The study examines SGMs (nonsense mutations) only — the functionally equivalent protein-truncating contributions from indels and splice-site mutations are not analysed, which may underestimate total loss-of-function burden from each signature.
- Signature assignment at the per-SNV level via SigProfilerSingleSample introduces annotation uncertainty; the authors address this with probabilistic reassignment but cannot fully eliminate assignment noise, particularly in samples with low mutation counts or co-occurring signatures with overlapping trinucleotide preferences (SBS2 and SBS13 share TCN context; SBS4 and SBS29 both reflect tobacco).
- Most analyses focus on three leading signatures (SBS4, SBS13, SBS18); other signatures with moderate SGM enrichment receive less characterisation.
- APOBEC expression–SGM associations are correlational in patient data (reverse causation guard required per hypothesis:0007 pre-registration): APOBEC3A upregulation could be downstream of tumour evolution (e.g., increased replication stress), not solely upstream.
- HMF is a metastatic cohort; enrichment of SBS13 and SBS18 in that setting may reflect selection during progression, not just mutagenic exposure at tumour initiation.
- The study does not directly test within-tissue vs across-tissue confounding; tissue collinearity may inflate some signature–SGM associations (cf. hypothesis:0007 alternative explanation R1).
- Cell-line APOBEC3A/B KO experiments use a single breast cancer line (BT-474), limiting generalisation.

## Model / Tool Availability

No new software tool released. Analyses use:
- SigProfilerSingleSample v0.0.0.27 (signature assignment)
- ANNOVAR v24 October 2019 (functional SNV annotation)
- ActivePathways (pathway enrichment, R/Bioconductor)
- COSMIC SBS catalog v3
- g:Profiler (gene set enrichment)

All three genomic datasets used are publicly available (TCGA PanCanAtlas via GDC, PCAWG via ICGC Data Portal, HMF via material transfer agreement).

## Follow-up

- The paper's APOBEC3A expression→SBS13 association is the direct mechanistic grounding for the hypothesis:0007 recovery arm "APOBEC3 expression ↔ SBS2/13". When implementing the positive-control analysis, use APOBEC3A (not APOBEC3B) expression and YTCA motif-enriched SBS13 mutations as the strongest signal.
- The smoking-history categorical variable used here (lifelong nonsmoker / current reformed ≤15y / current reformed >15y / current smoker) is more granular than a binary smoker/nonsmoker clinical label; verify which granularity is available across cBioPortal studies.
- The 56-gene SGM-enriched list (Table S1 referenced in the paper) provides a functional validation layer for genes flagged as high-frequency in the pipeline's cross-study mutation-frequency tables.
- ROS signature (SBS18) enrichment in colorectal cancer with APC is a possible third positive-control arm for hypothesis:0007 if dietary/oxidative-stress clinical covariates are available.
- The paper discusses SGM expansion as a source of tumour heterogeneity — this connects to the pipeline's interest in how mutation patterns vary across studies, and to hypothesis:0006-pre-malignant-n-minus-1-driver-carriage.
