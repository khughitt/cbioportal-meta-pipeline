---
type: paper
title: Genomic and immune signatures predict clinical outcome in newly diagnosed multiple
  myeloma treated with immunotherapy regimens
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Maura2023
ontology_terms:
- multiple myeloma
- mutational signatures
- APOBEC
- whole genome sequencing
- tumor microenvironment
- single-cell RNA sequencing
- minimal residual disease
- immunotherapy
datasets: []
source_refs:
- cite:Maura2023
related: []
---

# Genomic and immune signatures predict clinical outcome in newly diagnosed multiple myeloma treated with immunotherapy regimens

- **Authors:** Francesco Maura, Eileen M. Boyle, David Coffey, Kylee Maclachlan, et al. (Ola Landgren, Gareth J. Morgan co-senior authors)
- **Year:** 2023
- **Journal:** Nature Cancer, 4(12): 1660-1674
- **DOI/URL:** https://doi.org/10.1038/s43018-023-00657-1
- **BibTeX key:** Maura2023
- **Source:** PDF

## Key Contribution

Integrating whole genome sequencing (WGS) of tumor plasma cells and single-cell RNA sequencing (scRNA) of bone marrow microenvironment cells in 49 newly diagnosed multiple myeloma (NDMM) patients treated with daratumumab-carfilzomib-lenalidomide-dexamethasone (DKRd), the authors demonstrate that both tumor-intrinsic genomic features and immune microenvironment composition jointly predict sustained minimal residual disease (MRD) negativity and progression-free survival. High APOBEC mutational activity (SBS2/SBS13) independently predicts worse clinical outcomes even in the modern daratumumab era, while pre-treatment NK-cell numbers, T-cell receptor diversity, and post-treatment monocyte expansion collectively define a favorable immune microenvironment associated with deep, durable responses.

## Methods

- **Cohort:** 49 NDMM patients enrolled in the MANHATTAN phase-II trial (NCT03290950), treated with DKRd; 46/49 completed 8 cycles. Median follow-up 3.4 years. 33/49 (67%) achieved MRD-negativity; 24/49 (49%) sustained MRD-negativity.
- **WGS:** Matched tumor (CD138+) / normal (peripheral blood) WGS at 80x/40x coverage on NovaSeq 6000 (GRCh37 reference). SNVs called by integrating CaVEMan, Mutect, and Strelka; CNVs by Battenberg; SVs by BRASS.
- **Mutational signatures:** Three-step de novo extraction (SigProfiler), COSMIC catalogue matching, and fitting via mmsig. Seven SBS signatures identified: SBS1, SBS5 (clock), SBS2, SBS13 (APOBEC), SBS9 (germinal center polymerase eta), SBS8 (oxidative damage), SBS18 (reactive oxygen species).
- **Genomic driver catalogue:** Evaluated 73 recurrent SV hotspots, 159 aneuploidies (GISTIC2.0 peaks), and point mutations/indels in 80 MM driver genes across all 44 sequenced patients. Validated findings in CoMMpass (n=752 WGS with clinical data).
- **scRNA-seq:** 5-prime scRNA-seq on 22 paired bone marrow samples (CD138-negative mononuclear fraction): 17 at diagnosis (T1; 71,811 cells), 20 after 8 cycles (T2; 76,082 cells). 16 paired samples available. TCR sequencing performed concurrently. Cell type annotation using Seurat against Azimuth human bone marrow reference.
- **Statistical comparisons:** Kruskal-Wallis / Wilcoxon tests for immune cell proportions; log-rank test for PFS; partition around medoids (PAM) clustering for immune microenvironment classification.

## Key Findings

### Mutational Signatures and Outcome
- Seven SBS signatures detected; median WGS tumor mutation burden 5,178 (range 1,157-14,471). Overall SBS burden was higher in progressors (p=0.028).
- **High APOBEC activity (SBS2/SBS13) associated with significantly higher progression rate (p=0.05) and shorter PFS (p=0.01, log-rank).** Crucially, DKRd combination therapy did not override this adverse signal, consistent with prior work showing APOBEC as a pan-treatment adverse feature.
- Low SBS9 (germinal center polymerase eta) contribution also associated with shorter PFS (p=0.039).

### Genomic Drivers and Resistance
- Historically adverse features including t(4;14), 1q gain, chromothripsis did not significantly impact MRD-negativity or progression in this DKRd-treated cohort — immunotherapy partially neutralizes classical high-risk cytogenetics.
- Novel adverse genomic features identified:
  - **del(1p22) / RPL5 loss:** poor PFS (p=0.00059); validated in CoMMpass.
  - **XBP1 deletion:** all 5 patients with XBP1 loss failed sustained MRD-negativity (p=0.018); XBP1 loss reduces CD38 expression, impairing daratumumab activity.
  - **IKZF3 loss (SV/focal deletion):** 4/4 patients failed sustained MRD-negativity, 3/4 progressed early (p=0.0001). IKZF3 loss prevalent in 1.6% of CoMMpass NDMM; 66.6% of those underwent early progression. Links to lenalidomide (IMiD) resistance.
  - **SV involving KLF2:** all 4 patients progressed (p<0.0001).
  - **SVs at MYC locus (NSMCE2 del/PVT1 events):** p=0.022 for shorter PFS.
  - **18q+ and 8q+:** associated with low sustained MRD-negativity. **4q+** associated with higher sustained MRD-negativity; **17q+** with early progression.
  - **CYLD (16q12.1) loss:** trend toward shorter PFS (p=0.056).
  - **CCSER1 (4q22.1) SV:** 4/6 patients progressed (p=0.0028); biological function unclear.

### Tumor Microenvironment and Immune Predictors
- **Pre-treatment NK-cells:** Higher NK-cell proportion at T1 was the only immune population significantly associated with sustained MRD-negativity (4% vs 0.7%, p=0.04).
  - NK subpopulation analysis identified IFNgamma-secreting regulatory NK cells (NK Cluster #0) favoring good response; activated NK cells (XCL1+, NK Cluster #2) favoring poor response.
- **Post-treatment (T2) immune changes in non-responders:**
  - More B-cells (1.7% vs 0.3%, p=0.01), more NK cells (0.1% vs 0.01%, p=0.03), more T-cells (19% vs 4%, p=0.008), and fewer monocytes/DCs (33% vs 54%, p=0.01) compared to sustained MRD-negative cases.
  - Persistent activated T/B/NK populations at T2 suggest ongoing antigen stimulation by residual tumor cells.
- **CD14+ monocyte expansion at T2** was a hallmark of sustained MRD-negativity (19% vs 47%, p=0.01). PIM1 enriched in monocytes of good responders; IFN response (IFITM3) enriched in non-responders.
- **TCR diversity:** Higher T-cell receptor diversity at baseline predicted sustained MRD-negativity.
- **PAM immune clustering** identified Immune-Cluster #4 (high CD14+, low T-cells) as "favorable" (58% sustained MRD-negative at T2), and Immune-Cluster #3 (all T1 samples, 0% sustained MRD-negative) as "high-risk."

### Genomic-Immune Crosstalk
- In the 15 patients with both WGS and scRNA at T1, 8q24.21 amplification associated with higher T-cell CD8 effectors (p=0.02); 6p amplification associated with T-cell CD8 effectors (p=0.003); 16q deletion associated with lower B-cells (p=0.01) and lower CD56bright NK cells (p=0.04); SVs at MYC associated with high CD8 memory T-cells and low naïve B-cells (p<0.05).

## Relevance

**Direct relevance to h08 (agnostic covariate-signature-exposure association):**

This paper provides a strong, clinically validated positive control for the APOBEC signature axis. Specifically:
- **APOBEC (SBS2/SBS13) as an adverse outcome predictor in myeloma** is demonstrated here using the same SigProfiler / COSMIC / mmsig pipeline the cbioportal meta-analysis would use for restricted assignment. The survival impact survives a modern immunotherapy regimen, suggesting APOBEC exposure is a durable adverse signal across treatment eras, making it a reliable ground-truth anchor for H08a positive-control recovery.
- The study uses **SigProfiler + mmsig** (the mmsig tool, from the same UM-Myeloma-Genomics group, is a fitting algorithm). The three-step de novo → COSMIC match → restricted fitting approach mirrors the approach being considered for the cbioportal pipeline (q018).
- The finding that **high APOBEC does NOT convey adverse prognosis in a classical cytogenetics sense** (t(4;14), 1q gain were not adverse here) but through a signature-exposure-to-clinical-outcome channel is conceptually important for h08's design: it underscores that signature exposures carry information independent of cytogenetic risk annotation, justifying a separate agnostic association arm.
- For **h08b (novel discovery):** the germinal-center signature (SBS9, hypermutation via polymerase eta) emerges as a prognostic marker in MM — low SBS9 predicts poor PFS. This is a myeloma-specific, biology-grounded novel association that a cross-cancer agnostic scan would need to recover or extend, demonstrating the concept of immune/biology-linked process discovery.
- The integration of scRNA immune profiling with mutational signatures illustrates the concept discussed in the h08 hypothesis: expression modules (here, single-cell immune populations) associate with specific mutational events and clinical outcomes. While this paper does not run a phenome-wide signature-covariate scan, it validates the biological plausibility that immune expression features co-vary with signature exposures.

**Relevance to the cross-study meta-analysis:**
- APOBEC signature (SBS2/13) is a major recurring signal in myeloma; this paper confirms it persists as a clinically actionable variable even in daratumumab-era NDMM. The cbioportal cross-study aggregation likely captures this signal across multiple cBioPortal MM studies and CoMMpass, making APOBEC a candidate for cross-study stability testing.
- RPL5 (1p22) and XBP1 deletion frequencies in CoMMpass (n=752) are reported here as prevalence anchors; these validated driver genes could be added to the pipeline's driver annotation overlay.
- The CoMMpass validation cohort used here overlaps with data that may be included in the cBioPortal meta-analysis; if so, independence checks are needed.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| SigProfiler + COSMIC SBS catalogue + mmsig fitting | `run_restricted_sigprofiler_assignment.py` | Same toolchain; mmsig is the MM-specific restricted fitter described here |
| APOBEC activity (SBS2+SBS13) → short PFS | H08a APOBEC positive-control axis (APOBEC3 expression ↔ SBS2/13) | Direct ground-truth case for h08 recovery; paper validates outcome correlation |
| SBS9 (germinal center polymerase eta, low = worse PFS) | Novel candidate for h08b scan | MM-specific; not a standard "known" COSMIC exposure–aetiology pair |
| WGS matched tumor/normal | `matched_normal_studies` config list | MANHATTAN is a matched-normal WGS study; analogous to tcga_mc3 |
| CoMMpass (IA15, n=752, WGS) | Candidate external validation cohort | CoMMpass may partially overlap with cBioPortal MM studies |
| Immune microenvironment (NK, T, monocyte) ↔ treatment response | h08 expression-module covariate axis | Demonstrates single-cell immune expression covariates predict signature-outcome axes |
| XBP1/IKZF3/RPL5 driver annotation | Bailey 2018 driver overlay + custom annotations | These myeloma-specific drivers could extend the pipeline's annotate_drivers overlay |

## Limitations

- Small discovery cohort (n=44 WGS, n=17-22 scRNA); statistical power limited for rare genomic events (e.g., CCSER1 SVs, n=6). Most findings require external validation — CoMMpass validation is conducted but is observational/retrospective.
- Single treatment arm (DKRd); findings may not generalize to other immunotherapy backbones (e.g., BCMA-targeted agents, CAR-T).
- scRNA paired analysis limited to 16 pairs; cross-timepoint analyses further constrained by sample availability.
- Immune-genomic co-analysis restricted to 15 patients with both WGS and scRNA at T1 — underpowered for definitive genomic-immune crosstalk conclusions.
- No germline-only WGS arm; APOBEC and other signature contributions are inferred entirely from somatic mutations in tumor cells. Confounding from clonal hematopoiesis (CH) is not explicitly discussed in the mutational signature section, though the pipeline used matched normal samples which should reduce false-positive somatic calls.
- IKZF3 and XBP1 findings, while statistically striking, are based on n=4 and n=5 patients respectively in the discovery cohort.
- Biological role of CCSER1 (4q22.1) remains unknown; the association may be driven by a nearby gene or a fragile site artifact.

## Model / Tool Availability

- WGS analysis code: https://github.com/UM-Myeloma-Genomics
- scRNA analysis code: https://github.com/Eileen-Boyle/CITE-DKRD
- mmsig (mutational signature fitting for MM): https://github.com/UM-Myeloma-Genomics/mmsig

## Follow-up

- **mmsig tool:** Examine for compatibility with the cbioportal pipeline's restricted signature assignment step (q018). The mmsig fitting algorithm is validated here on MM WGS and available on GitHub.
- **APOBEC validation in cBioPortal MM studies:** Check whether APOBEC signal is reproducibly detected across cBioPortal MM studies in the cross-study aggregation. This would validate the H08a positive-control recovery in a cross-study (rather than single-trial) setting.
- **RPL5 / XBP1 / IKZF3 as driver annotations:** Consider adding these to the pipeline's driver gene list (currently anchored to Bailey 2018), especially for myeloma-focused analyses.
- **SBS9 in other cancer types:** The germinal center hypermutation signature is active primarily in B-cell neoplasms. In a cross-cancer scan, it provides a B-cell lineage specificity test for h08b discovery.
- **Immune-signature crosstalk:** The paper hints but does not fully execute a joint immune-expression / mutational-signature association scan. This is precisely the H08b design gap.
- Papers to consider next: the referenced mmsig paper (ref 46), the CoMMpass WGS paper (ref 16, Maura et al. 2022 NEJM Evid or similar), and the Kydar scRNA study (ref 28).
