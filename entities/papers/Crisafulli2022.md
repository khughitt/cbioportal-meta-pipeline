---
type: paper
title: Temozolomide Treatment Alters Mismatch Repair and Boosts Mutational Burden
  in Tumor and Blood of Colorectal Cancer Patients
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Crisafulli2022
ontology_terms: []
datasets: []
source_refs:
- cite:Crisafulli2022
related: []
---

# Temozolomide Treatment Alters Mismatch Repair and Boosts Mutational Burden in Tumor and Blood of Colorectal Cancer Patients

- **Authors:** Giovanni Crisafulli, Andrea Sartore-Bianchi, Luca Lazzari, Filippo Pietrantonio, et al.
- **Year:** 2022
- **Journal:** Cancer Discovery
- **DOI/URL:** https://doi.org/10.1158/2159-8290.CD-21-1434
- **BibTeX key:** Crisafulli2022
- **Source:** PDF

## Key Contribution

The ARETHUSA proof-of-concept clinical trial demonstrates that temozolomide (TMZ), an alkylating chemotherapy agent, can pharmacologically inactivate mismatch repair (MMR) genes in MMR-proficient (MMRp) metastatic colorectal cancer (mCRC), producing a distinct COSMIC mutational signature 11 (SBS11) and substantially increasing tumor mutational burden (TMB) in both tumor biopsies and circulating tumor DNA (ctDNA). This provides clinical proof-of-concept that a treatment-induced mutational signature can be detected longitudinally in tissue and liquid biopsy, and that the resulting hypermutation state — combined with acquired MMR-gene mutations — can sensitize otherwise immunotherapy-resistant tumors to anti-PD-1 pembrolizumab.

## Methods

**Trial design (ARETHUSA; NCT03519412):** Two-step phase II clinical trial in MGMT-deficient (IHC-negative and MGMT-promoter-methylated by methyl-BEAMing), RAS-mutant, MMRp/MSS mCRC patients. Step 1 (priming phase): oral TMZ 150 mg/m² days 1–5 every 28 days until progressive disease (PD). Step 2 (immunotherapy phase): pembrolizumab 200 mg every 3 weeks in patients achieving post-TMZ TMB ≥20 mut/Mb.

**Cohort:** 473 patients screened for MGMT status; 33 of 69 MGMT-methylated patients enrolled; 21 biopsied at PD for the translational analyses presented here. Tissue biopsies obtained pre- and post-TMZ (mandatory post-TMZ, optional pre-TMZ). Longitudinal liquid biopsies (pre/post-TMZ, pre/post-pembrolizumab) collected for most patients.

**Sequencing:** Whole exome sequencing (WES) at high depth (median 376×, PhredScore ≥30, coverage ≥96.82% at 100×) using Nextera DNA Flex Library Prep + IDT xGen Exome Enrichment. PBMC used as germline-matched normal. For liquid biopsy: GuardantOMNI research-use-only NGS assay across 2.145 Mb panel; bTMB reported as mut/Mb.

**Mutational signature analysis:** MuSiCa and Mutational Patterns R packages; fitting against COSMIC signature databases (v2.0, v3.0, v3.2). Clonal analysis: VAF ≥10%; subclonal analysis: VAF ≥1%. Cosine similarity threshold ≥0.9 for quality control. Patient stratification into subtypes A (no TMZ molecular evidence), B1 (subclonal TMZ signature), B2 (clonal TMZ signature) based on SBS11 score and mutation abundance.

**TMB calculation:** WES-derived TMB from somatic SNVs/indels at 5% Fisher-test significance, minimum 4 supporting reads, VAF ≥10% (clonal) or ≥1% (subclonal), filtered against dbSNP (v147). Copy-number normalization applied. Intratumor heterogeneity (ITH) studied by multi-region biopsies from same lesion (three corings of one liver metastasis in patient AR02005).

**Clinical efficacy metric:** Growth modulation index (GMI) = PFS on current therapy / PFS on immediately prior therapy; GMI >1.33 considered clinically meaningful.

## Key Findings

**TMZ mutational signature:**
- COSMIC SBS11 (alkylating-agent signature, C>T enrichment in TCN context) detected in post-TMZ tumor biopsies. Three patient subtypes: Subtype A (n=4, no SBS11, received few TMZ cycles), Subtype B1 (n=15, SBS11 subclonal), Subtype B2 (n=2, SBS11 clonal with highest TMB).
- TMB increases significantly with number of TMZ cycles: Spearman R=0.7847, P=2.535e−5.

**TMB elevation in tissue and blood:**
- Subtype A mCRC patients: mean subclonal post-TMZ bTMB 24 mut/Mb; Subtype B patients: significantly higher subclonal bTMB (P<0.0007). Subtype B2 patients (AR02007, AR01052): post-TMZ bTMB of 2,276 and 196 mut/Mb respectively.
- Wilcoxon rank-sum test: priming phase significantly increases bTMB (P=0.002443).
- TMZ increases SNVs predominantly (indel count remains similar across groups), consistent with alkylating-agent mechanism (elevated SNVs, not indels).

**MMR gene mutations:**
- MSH6 mutations recur across patients post-TMZ; p.T1219I variant detected in tissue and/or ctDNA of 16/17 (94%) patients who benefited from TMZ treatment (Subtype B). The p.T1219I variant was absent in all pre-TMZ samples and in Subtype A patients.
- All MSH6 SNVs (100%) lie in nucleotide contexts favored by SBS11, confirming TMZ as the causal agent, not germline or spontaneous mutation.
- Additional recurrent MSH6 variants: p.G557D (n=2), p.T1008I (n=2), premature stop at glutamine 1122 (n=2), plus multiple stop-codon acquisitions.

**Intratumor heterogeneity:**
- Multi-coring of a single liver lesion showed differential TMZ molecular impact: one coring had high clonal and subclonal TMZ signature, others had only subclonal or no detectable effect. At least 25–30% TMZ-resistant cells required for clonal threshold detection, as few as 2–6% for subclonal detection.

**Pembrolizumab clinical response (first 6 patients):**
- Disease control rate (DCR) 4/6 (67%) with sustained SD lasting >2 years, 6.5 months, and 5.5 months in three patients (AR02007, AR01015, AR03047).
- Longitudinal bTMB monitoring in long-SD patient (AR02007) showed bTMB decline and disappearance of MSH6 p.T1219I ctDNA variant during pembrolizumab treatment, consistent with immune clearance of MMRd tumor fraction.
- All 6 patients had GMI >1.33, suggesting clinical benefit beyond natural tumor kinetics.

**Liquid biopsy as monitoring tool:**
- Longitudinal ctDNA (including MSH6 p.T1219I VAF) tracked immune response dynamics. In AR02007 (longest responder, 24.7 months SD on pembrolizumab), MSH6 variant emerged with TMZ, declined during immunotherapy, and disappeared, while KRAS p.G12V and TP53 trunk driver mutations remained stable.

## Relevance

**Direct connection to hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and (agnostic covariate–signature–exposure association):**

This paper is a critical positive-control reference for hypothesis:0007's goal of recovering known treatment-induced signatures alongside endogenous etiological signatures. COSMIC SBS11 (alkylating-agent signature) is a canonical treatment-induced signature with a defined nucleotide-context profile (C>T in TCN triplets favored by TMZ). The paper demonstrates:

1. **Signature detection from treatment exposure:** SBS11 can be quantitatively detected in tumor tissue and ctDNA and correlates dose-dependently with number of TMZ cycles — precisely the kind of covariate–signature–exposure relationship that hypothesis:0007 aims to recover. In a cross-study meta-analysis context, samples from patients treated with TMZ-based regimens (e.g., glioblastoma, some colorectal trials) would be expected to carry elevated SBS11 and should ideally be flagged as treatment-exposed confounders or positive controls.

2. **MMR deficiency as a secondary signature generator:** TMZ-induced MMR gene inactivation (primarily MSH6) converts an MMRp tumor into an acquired MMRd tumor, thereby amplifying overall TMB and inducing indel accumulation over time. This illustrates how a treatment exposure can generate a secondary, biologically downstream signature (MMRd-like) distinguishable from the primary alkylating-agent SBS11. For hypothesis:0007's aetiology inference, this is a concrete example of a confounder chain: treatment → SBS11 → acquired MMRd → elevated indels.

3. **Clonal vs. subclonal decomposition of signatures:** The subtype A/B1/B2 stratification, and the ITH multi-coring experiment, underscore that the same COSMIC signature can appear at clonal or subclonal VAF levels depending on the proportion of affected cells. For the cbioportal cross-study pipeline, this is relevant to how per-study mutation call VAF thresholds interact with signature detection sensitivity — if a study uses higher VAF cutoffs, subclonal treatment-induced signatures will be systematically missed.

4. **Liquid biopsy as longitudinal signature tracker:** ctDNA-based bTMB tracks the SBS11-associated tumor fraction over time, providing a dynamic view of signature exposure. This is conceptually analogous to tracking signature exposures as clinical/treatment covariates in an agnostic association scan — a key component of hypothesis:0007.

**Cross-study meta-analysis relevance:**
- cBioPortal mCRC studies may include patients enrolled in or treated analogously to ARETHUSA. Patients receiving TMZ-based regimens could exhibit elevated SBS11 in their somatic mutation profiles, inflating the TMB estimates and potentially confounding cancer-type-level mutation frequency comparisons. The pipeline's hypermutator annotation (task t081) would ideally flag such patients.
- The paper's demonstration that MMRp tumors can become hypermutated pharmacologically (bTMB up to 2,276 mut/Mb in two patients) is directly relevant to pipeline decisions about hypermutator thresholds (the 10 mut/Mb Campbell threshold [@Campbell2017Hypermutation] and 100 mut/Mb ultra-hypermutator categories) and the GMM-based per-cancer-type TMB fitting.
- The MSH6 p.T1219I variant's high recurrence (94% of TMZ-responding patients) across studies could create a spurious "hotspot" signal in cross-study aggregation if samples from TMZ-treated patients are included without annotation.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| COSMIC SBS11 (alkylating-agent signature) | Mutational signature (treatment-induced) | Positive-control signature for hypothesis:0007; should be recoverable in TMZ-treated study arms |
| Subtype A / B1 / B2 patient stratification | Hypermutator annotation categories | B2 patients exceed 100 mut/Mb ultra-hypermutator threshold |
| bTMB (blood TMB from ctDNA) | Per-sample TMB | Pipeline computes tissue TMB; ctDNA-derived TMB is analogous but requires separate panel-size normalization |
| MGMT methylation status | Matched-normal / annotation covariate | Not currently in pipeline schema; relevant as a treatment-selection biomarker |
| GMI (growth modulation index) | Clinical endpoint | Not in pipeline; relevant for linking mutational phenotype to outcome |
| MSH6 p.T1219I recurrent variant | Resistance/functional mutation | Could appear as spurious hotspot in cross-study aggregation; flag in post-hoc annotation |
| Clonal vs. subclonal TMZ signature | VAF-stratified mutation calling | Pipeline VAF ≥10% threshold matches clonal analysis; subclonal (VAF ≥1%) detection requires lower cutoff |

## Limitations

- Small translational cohort (21 tissue biopsies; only 6 patients reached pembrolizumab phase at data lock due to COVID-19 disruption); no statistical power for efficacy conclusions about pembrolizumab.
- Post-TMZ tissue biopsy was mandatory but pre-TMZ biopsy only available in 5/21 patients, limiting paired before/after signature analysis to a subset.
- WES was used only for TMB; PD-L1 expression, TIL quantification, and neoantigen analysis could not be co-performed on the same samples due to tissue quantity limitations.
- Tissue biopsy captures a spatial snapshot; ITH experiments show that different tumor regions respond differently to TMZ, so a single biopsy may over- or under-estimate the TMZ effect.
- bTMB (ctDNA) is influenced by metastatic site: lung/peritoneal lesions have lower ctDNA allele frequencies than liver lesions, potentially underestimating bTMB in some patients.
- No randomized control arm for pembrolizumab efficacy; GMI used as intra-patient comparison but inherits assumptions about growth kinetics.
- ARETHUSA selects for MGMT-methylated tumors (IHC-negative + promoter methylation); generalizability to MGMT-proficient MMRp mCRC is not established.

## Model / Tool Availability

- Bioinformatic pipeline code: https://bitbucket.org/irccit/idea/src/master/
- Human sequencing data: EGA study EGAS00001002694; ENA accessions PRJEB33045 and PRJEB46380
- Statistical analysis performed in R v3.6.3 and v4.0.3
- Mutational signature tools: MuSiCa (web application), Mutational Patterns R package; COSMIC v2.0, v3.0, v3.2 reference databases

## Follow-up

- Compare with Poon2021 (COSMIC signature landscape) and LeeSix2018 (treatment-associated signatures) for the expected profile of SBS11 in population-scale datasets and how to distinguish it from endogenous signatures.
- The MSH6 p.T1219I recurrent mutation raises a specific question: does this variant appear at anomalously high frequency in cBioPortal mCRC studies that may have included TMZ-treated patients? Worth a targeted query in the cross-study aggregation output.
- For hypothesis:0007 positive-control recovery: SBS11 should be recoverable in glioma/glioblastoma cBioPortal studies (TMZ is standard of care there) and could serve as a benchmark alongside UV (SBS7), smoking (SBS4), APOBEC (SBS2/13), and MMR (SBS6/15/21/26) signatures.
- Connection to hypermutator pipeline (t081): patients like AR02007 (bTMB 2,276 mut/Mb) would be extreme hypermutators requiring correct annotation as treatment-induced rather than intrinsic hypermutators (POLE/MSI); the `hypermutator_reason` taxonomy should consider a `treatment_alkylating` category.
- The MAYA trial (Morano et al., Ann Oncol 2022) extended ARETHUSA's design with TMZ + low-dose ipilimumab + nivolumab and reached the primary endpoint (8-month PFS 36%); reading alongside Crisafulli2022 would round out the clinical picture.
