---
id: "paper:Maura2019"
type: "paper"
title: "A practical guide for mutational signature analysis in hematological malignancies"
status: "active"
ontology_terms:
  - mutational signatures
  - hematological malignancies
  - multiple myeloma
  - chronic lymphocytic leukemia
  - acute myeloid leukemia
  - NNMF
  - signature extraction
  - signature fitting
  - inter-sample bleeding
  - AID activity
datasets:
  - "143 CLL WGS (EGAS00000000092)"
  - "30 MM WGS (EGAD00001003309)"
  - "50 AML WGS (phs000178.v1.p1 + 2 unpublished t-AML)"
source_refs:
  - "cite:Maura2019"
related: []
created: "2026-05-31"
updated: "2026-05-31"
---

# A practical guide for mutational signature analysis in hematological malignancies

- **Authors:** Francesco Maura, Andrea Degasperi, Ferran Nadeu, Daniel Leongamornlert, Helen Davies, Luiza Moore, Romina Royo, Bachisio Ziccheddu, Xose S. Puente, Herve Avet-Loiseau, Peter J. Campbell, Serena Nik-Zainal, Elias Campo, Nikhil Munshi, Niccolo Bolli
- **Year:** 2019
- **Journal:** Nature Communications
- **DOI/URL:** https://doi.org/10.1038/s41467-019-11037-8
- **BibTeX key:** Maura2019
- **Source:** PDF

## Key Contribution

This paper provides a systematic evaluation of de novo signature extraction vs. reference-based fitting approaches applied to three hematological malignancies (MM, CLL, AML), exposing three major failure modes — ambiguous signature assignment, missed localized hypermutation, and inter-sample bleeding — and proposing a multi-step workflow that combines NNMF-based de novo extraction, COSMIC assignment, and fitting only on the extracted shortlist to produce accurate, reproducible results. It demonstrates that the previously reported BRCA1/BRCA2-mediated homologous recombination deficiency (HRD) signal in MM is a fitting artefact driven by the inclusion of flat signatures (SBS3), and surfaces genuine biological insights including c-AID activity in unmutated CLL and APOBEC-mediated kataegis in MM and a therapy-related AML.

## Methods

- **Cohorts:** 143 CLL WGS, 30 MM WGS, 50 AML WGS (2 unpublished therapy-related + 48 from TCGA). All WGS aligned with BWAmem at Wellcome Sanger Institute; SNVs called with a multi-caller approach (mutect2, caveman, muse for SNVs; BRASS/Pindel for SVs/indels).
- **De novo extraction:** Alexandrov et al. NNMF framework and mutationalPatterns R package. 96-trinucleotide-context SNV catalogue as input.
- **Fitting:** deconstructSigs (fitting all 30 COSMIC signatures) and mutationalPatterns fitting approach, both with and without prior NNMF shortlisting.
- **Localized hypermutation:** Separate 96-class catalogues built from all SNVs within IGH/IGK/IGL loci; kataegis defined as ≥6 consecutive mutations with average intermutation distance ≤1 kb.
- **HRD validation:** HRDetect classifier applied with Signature 8 only, Signatures 3+8, and Signature 3 only; structural feature contributions (microhomology deletions, rearrangement signatures, HRD-LOH) inspected as orthogonal validation.
- **Inter-sample bleeding correction:** two strategies — (1) fit using only NNMF-extracted shortlist signatures; (2) split cohorts by prior biological knowledge (e.g. M-CLL vs U-CLL IGHV status) and run independent NNMF runs per subgroup.
- **c-AID quantification:** Dirichlet process for both CLL and MM; three additional SNV callers (mutect2, caveman, muse) combined with published Sidron catalog; mutations required to be called by ≥2 of 4 callers.
- **AML platinum signature:** Cohort includes 2 therapy-related AMLs; re-running NNMF after excluding t-AML samples eliminates the platinum signature from primary AML extractions, confirming inter-sample bleeding.

## Key Findings

1. **Fitting without prior knowledge inflates false positives.** Running deconstructSigs against all 30 COSMIC signatures forces spurious contributions from biologically implausible signatures (tobacco-smoking SBS4, liver-specific SBS16) into MM samples. The flat clock-like signatures (SBS3, SBS5) are particularly prone to erroneous assignment because they can substitute for each other.

2. **BRCA1/BRCA2-mediated HRD is absent in MM.** SBS3, widely used as an HRD marker, is extracted by de novo approaches as a minor flat signature but is not necessary to explain the MM mutation catalogs. HRDetect scores drop to near zero when SBS8 alone (without SBS3) is used. MM lacks the hallmark structural features of BRCA-null cancers (low microhomology-mediated deletions, low HRD-LOH, limited 1–100 kb tandem duplications). One sample with a slightly elevated HRDetect score has complex chromosomal events consistent with chromothripsis rather than HRD.

3. **c-AID activity is detectable in unmutated CLL (U-CLL).** Using a localized IGH/IGK/IGL analysis, c-AID mutations are found in both M-CLL and U-CLL, with U-CLL showing predominantly non-VDJ (non-canonical) targets — consistent with a GC-independent pathogenesis. In MM and M-CLL, c-AID activity involves mostly coding regions of the VDJ locus. BCL6 is identified as a key localized AID target across lymphoproliferative diseases.

4. **APOBEC-mediated kataegis occurs in MM and a therapy-related AML.** APOBEC kataegis events cluster around complex structural rearrangements (chromothripsis), consistent with APOBEC activity being co-localised with structural instability. This is the first reported case of APOBEC-mediated kataegis in a therapy-related AML sample.

5. **Inter-sample bleeding is a systematic problem in de novo extraction.** When biologically distinct subgroups are pooled (e.g. M-CLL and U-CLL), NNMF assigns nc-AID (Signature 9) to U-CLL samples — a biologically impossible assignment. Splitting cohorts by prior biological knowledge or using NNMF-shortlist fitting corrects this.

6. **Two novel AML signatures not in COSMIC are discovered.** A platinum exposure signature (contributing >30% to t-AML mutations) and an HSPC (hematopoietic stem/progenitor cell) signature are extracted. Both disappear from primary AML when t-AML samples are removed, showing they represent inter-sample bleeding from treatment-exposed outliers.

7. **Proposed three-step analysis framework:** (1) de novo NNMF extraction to identify active signatures; (2) assignment of extracted signatures to COSMIC/PCAWG reference; (3) fitting restricted to the identified shortlist. Applied separately to genome-wide and localized (IGH/IGK/IGL) SNV catalogues (Fig. 8 workflow diagram).

## Relevance

**Direct relevance to h08 (agnostic covariate–signature-exposure association):**

- The paper is a methodological cornerstone for the H08a positive-control arm. Its characterization of inter-sample bleeding is the primary reason why fitting approaches must be run within biologically homogeneous strata — exactly what H08a's within-tissue conditioning is designed to enforce (H08 hypothesis, Prediction 4 / Alternative R1-R4).
- The paper explicitly demonstrates that SBS3 (BRCA/HRD) is a false positive in MM attributable to flat-signature confusion, directly motivating the need in H08 to validate signature assignments with orthogonal evidence before treating them as candidate aetiologies.
- The NNMF-shortlist fitting approach recommended here is a concrete implementation of the "restricted assignment" logic already partially present in the cbioportal pipeline (`run_restricted_sigprofiler_assignment.py`), providing authoritative methodological backing.
- The c-AID and APOBEC kataegis findings are relevant benchmarks for the H08a positive-control design: APOBEC (SBS2/13) recovery within MM/CLL WGS is a confirmatory arm if MM/CLL data are included in the cross-study analysis.
- The AML inter-sample bleeding case (platinum signature disappearing after t-AML removal) is the hematological analogue of the confounding described in H08 hypothesis Alternative R4 (batch/assay artifact), illustrating that study composition — not just tissue type — confounds naive signature attribution.
- For the cross-study meta-analysis more broadly: the paper validates that a subset of cBioPortal MM/CLL studies using WGS carry interpretable signatures (SBS1, SBS2, SBS5, SBS8, SBS9, SBS13, MM1), and establishes that WES may miss localized processes (c-AID) that WGS detects — a relevant caveat when pooling mixed-assay cBioPortal studies.

## Project Framework Mapping

| Paper Concept | Project Concept / Term | Notes |
|---|---|---|
| De novo NNMF extraction | `run_sigprofiler_extraction` (planned) / `run_restricted_sigprofiler_assignment.py` | Paper distinguishes extraction from fitting; pipeline currently focuses on fitting |
| Fitting all 30 COSMIC signatures (deconstructSigs default) | Unconstrained fitting — explicitly flagged as problematic | Motivates the restricted-assignment approach already in pipeline |
| NNMF shortlist fitting | `run_restricted_sigprofiler_assignment.py` | Direct implementation of paper's recommended step 3 |
| Inter-sample bleeding | Cross-study confounding (R4 in h08 alternative explanations) | Bleeding across cancer types = tissue collinearity risk |
| Localized hypermutation / kataegis | Not currently in scope | Requires genome-wide mutation positions; cBioPortal MAFs may lack positional granularity |
| HRDetect | Not currently implemented | Structural variant data required; not uniformly available in cBioPortal |
| Biological subgroup stratification (M-CLL vs U-CLL) | Within-tissue strata (h08 design) | Paper's solution to bleeding is the analogue of h08's within-tissue conditioning |

## Limitations

- The MM cohort is small (n=30), limiting power to detect rare signatures and making the HRD-absence conclusion probabilistic rather than definitive. The authors acknowledge a larger cohort could reveal a subset with true BRCA-mediated HRD.
- The recommended workflow requires prior biological knowledge of which signatures to expect — a circularity that the paper acknowledges but does not fully resolve for novel cancer types or for fully agnostic discovery settings (the exact gap that h08 aims to fill).
- Localized hypermutation analysis depends on accurate positional mapping to immunoglobulin loci, which is not uniformly available across cBioPortal study MAFs and requires specialized SNV callers to achieve high sensitivity.
- AML findings (platinum and HSPC signatures) are partially based on only 2 unpublished t-AML cases; the t-AML bleeding conclusion is robust, but the HSPC signature characterization requires independent replication.
- The paper uses COSMIC v2 (30 signatures); the framework has since expanded to COSMIC v3+ with >60 SBS signatures, potentially altering some assignments.

## Model / Tool Availability

- R code for mutationalPatterns-based analyses provided as Supplementary Software Files 1–3.
- HRDetect algorithm: Davies et al. 2017 (separate publication); used here as-is.
- deconstructSigs: Rosenthal et al. (separate R package).
- No dedicated software package released by this paper; workflow is described procedurally and implemented in standard R packages.

## Follow-up

- The recommended three-step framework (Fig. 8) should be reviewed against the current pipeline implementation in `run_restricted_sigprofiler_assignment.py` to assess whether the de novo extraction step is present or assumed.
- For H08a positive-control design: the APOBEC-kataegis and c-AID findings in MM/CLL confirm that localized processes can be missed by genome-wide extraction — the cross-study analysis should be treated as genome-wide only, with explicit acknowledgment that localized signatures (c-AID) are likely diluted below detection.
- The AML platinum-signature bleeding case motivates adding study composition (proportion of therapy-related samples) as a nuisance covariate in the h08 association scan.
- Relevant adjacent papers: Degasperi et al. 2022 (SigProfiler v3+ catalogue, already summarized), Davies et al. 2017 (HRDetect original), Alexandrov et al. 2020 (COSMIC v3).
