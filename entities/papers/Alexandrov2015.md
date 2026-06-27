---
type: paper
title: A mutational signature in gastric cancer suggests therapeutic strategies
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Alexandrov2015
ontology_terms:
- mutational signatures
- somatic mutation
- homologous recombination deficiency
- gastric cancer
- BRCA1
- BRCA2
- platinum therapy
- PARP inhibitors
datasets: []
source_refs:
- cite:Alexandrov2015
related: []
---

# A mutational signature in gastric cancer suggests therapeutic strategies

- **Authors:** Ludmil B. Alexandrov, Serena Nik-Zainal, Hoi Cheong Siu, Suet Yi Leung, Michael R. Stratton
- **Year:** 2015
- **Journal:** Nature Communications (6:8683)
- **DOI/URL:** https://doi.org/10.1038/ncomms9683
- **BibTeX key:** Alexandrov2015
- **Source:** PDF

## Key Contribution

This paper conducts the first comprehensive large-scale survey of mutational signature 3 (SBS3 — the homologous-recombination-deficiency signature) across 10,250 cancer genomes spanning 36 cancer types. The principal finding is that signature 3, previously established in breast, ovarian, and pancreatic cancers via BRCA1/2 mutations, is also present in 7–12% of gastric cancers. This implies a clinically actionable subset of gastric cancers that may respond to platinum-based chemotherapy or PARP inhibitors without necessarily carrying BRCA1/2 mutations.

## Methods

- **Data:** 10,250 matched cancer-normal genome pairs (607 WGS + 9,643 WES) from 36 cancer types, sourced from TCGA, ICGC, and peer-reviewed publications. Gastric cancer data came from four independent studies listed by the paper: 372 WES + 100 WGS samples.
- **Mutation filtering:** Germline variants removed using dbSNP, 1000 Genomes, NHLBI GO ESP, and 69 Complete Genomics panel. Technology/institute artefacts removed by a panel-of-normals approach (>250 normal WGS + >500 normal WES BAM files); any mutation in ≥2 reads in ≥2 normals discarded.
- **Signature decomposition:** Two-step MATLAB NMF framework (Alexandrov et al. Cell Rep. 2013): (1) de novo extraction per cancer type to derive consensus signatures; (2) constrained linear decomposition per sample using the Frobenius norm with non-negativity and sum-to-total constraints. Exome-derived signatures normalized from exome to whole-genome trinucleotide frequencies.
- **Statistical tests:** Mann-Whitney U-test for indel and structural variant counts; Fisher's exact test for histological associations.
- **Supplementary:** 20 gastric cell lines (WES) examined for signature 3; none identified positive (attributed to absent matched-normal controls).

## Key Findings

1. **Signature 3 prevalence in gastric cancer:** Detected in 27/372 WES samples (~7.3%) and 12/100 WGS samples (12.0%). Among the 36 cancer types surveyed, only gastric cancer joined breast (~27–29%), ovarian (~31%), and pancreatic (~7–40% depending on cohort enrichment) as types exhibiting signature 3.

2. **Independent of BRCA1/2 mutations:** Gastric samples with BRCA1/2 somatic mutations showed no enrichment for signature 3; those mutations were predominantly heterozygous and likely passengers in hypermutated (MMR-deficient) backgrounds.

3. **Corroborating indel pattern:** WGS gastric cancers with signature 3 had a median 715 large indels (>3 bp) with overlapping microhomologies at breakpoints, versus 172 in signature-3-negative samples (P = 1.07 × 10⁻⁵). WES samples showed the same elevation (P = 5.87 × 10⁻⁴). This microhomology-mediated indel pattern is a hallmark of NHEJ compensating for defective HR.

4. **Elevated structural variants:** Signature-3-positive gastric WGS samples averaged 244 structural variants versus 111 in negative samples (P = 1.24 × 10⁻³).

5. **Histological association:** Signature 3 is enriched in the intestinal subtype by Lauren's classification (P = 0.0058) and is nearly absent from diffuse-type gastric cancer (P = 0.0015). A distinctive "compact discohesive growth pattern" (solid nests of roundish cells with marked loss of cell-to-cell adhesion) co-occurs strongly with signature 3 in the WGS cohort (P = 0.0003; 54.5% of compact-discohesive cases vs 6.7% of others).

6. **Therapeutic implication:** The ~7–12% of gastric cancers with HR-deficiency-related signature 3 are candidates for platinum therapy or PARP inhibitors, analogous to established practice in BRCA1/2-mutant breast, ovarian, and pancreatic cancers — even without BRCA mutations.

## Relevance

**Direct relevance to hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and (agnostic covariate-to-signature association):**

- Signature 3 (SBS3) is one of the key cancer-biology-grounded signatures the cbioportal cross-study pipeline would encounter. This paper establishes that SBS3 is active in gastric cancer at detectable prevalence in both WES (~7%) and WGS (~12%) — relevant to the hypothesis:0007 positive-control arm's coverage of known signatures.
- More directly, this paper illustrates the core hypothesis:0007 logic in miniature: a mutational signature is associated with a clinical/molecular covariate (BRCA1/2 status, histological subtype, indel pattern) that implies an aetiology (HR deficiency). The finding that signature 3 occurs even *without* BRCA1/2 mutations is a canonical example of why agnostic association is needed — the genetic marker (BRCA1/2) is not the only upstream cause.
- The histological co-variables (Lauren type, growth pattern) in Table 1 are exactly the kind of structured clinical covariates hypothesis:0007 proposes to associate agnostically against signature exposures. This paper provides a ground-truth association (intestinal-type gastric cancer → SBS3) that could serve as a validation point for a hypothesis:0007 implementation covering gastric studies in cBioPortal.
- **Positive-control scope:** UV↔SBS7, smoking↔SBS4, and APOBEC↔SBS2/13 are the three confirmatory arms in the pre-registered design. SBS3 is not among them, but the framework here — systematic cross-cancer-type prevalence survey — parallels what hypothesis:0007 would do per-signature for all structured covariates.

**Cross-study aggregation context:** The paper's 10,250-sample, 36-cancer-type sweep is methodologically analogous to what the cbioportal pipeline does. The gastric cohort draws from TCGA and three published studies — cBioPortal hosts most of these, making the gastric cancer signature-3 finding directly replicable within the pipeline's existing study universe.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Mutational signature 3 (SBS3) | SBS3 in COSMIC reference | Same signature, current COSMIC v3.4 name |
| "Contribution" / "exposure" of a signature | H-matrix column per sample (NMF) | Direct analogue; paper uses constrained Frobenius decomposition, pipeline uses SigProfiler restricted assignment |
| 96-channel substitution context | 96-channel SBS profile | Identical classification; trinucleotide context around pyrimidine |
| De novo extraction per cancer type | `run_restricted_sigprofiler_assignment.py` | Pipeline currently uses restricted assignment (known signatures), not de novo per cancer type |
| Large indels with microhomology | Not currently tracked | Pipeline focuses on SNV/small indels in mutation frequency tables; structural variant calling is out of scope |
| Lauren histological classification | `cancer_type_detailed` or `primary_site` clinical field | Would need to be a clinical covariate loaded via `convert_to_feather.py` |
| Compact discohesive growth pattern | Not currently represented | Specialized pathology label; unlikely in cBioPortal clinical tables |

## Limitations

- Most samples (94%) are WES, not WGS; WES will miss signature 3 in cases where the signature generates few exonic mutations, likely underestimating true prevalence.
- No cell line with signature 3 was found among the 20 gastric lines examined — limits functional follow-up on drug sensitivity. Authors attribute this to absent matched-normal controls.
- Clinical data for the examined gastric cancers were very limited; no outcome data were available to correlate signature 3 with actual treatment response.
- Gastric BRCA1/2 mutations were not validated functionally; zygosity and passenger status inferred from context (high indel/MSI background), not functional assay.
- The pancreatic WGS cohort was deliberately enriched for BRCA1/2 mutations (40% signature-3 prevalence), making pan-cancer prevalence comparisons difficult.
- No analysis of signatures 15, 20, 26 (MMR-related) relative to signature 3 co-occurrence in gastric cancer — relevant because MMR-deficient gastric cancers could confound signature 3 detection.

## Model / Tool Availability

- **MATLAB NMF framework** referenced: http://www.mathworks.com/matlabcentral/fileexchange/38724 (Alexandrov et al. 2013 Cell Reports framework).
- Somatic mutation data freely retrievable from TCGA and ICGC portals per Supplementary Data 1 of the paper.
- Signature 3 characterisation and COSMIC catalogue: http://cancer.sanger.ac.uk/cosmic/signatures (now at https://cancer.sanger.ac.uk/signatures/).

## Follow-up

- **Waddell et al. 2015 (Nature 518):** The pancreatic cancer platinum-therapy study showing all responders had signature 3, cited as the clinical motivation here. Directly relevant to hypothesis:0007 positive-control and to translational use of signature-exposure associations.
- **Alexandrov et al. 2020 (Nature):** The comprehensive PCAWG signature atlas — an order-of-magnitude larger version of what this paper does; the primary reference for hypothesis:0007.
- **Does signature 3 prevalence in gastric studies within cBioPortal replicate the 7–12% figure?** Would be a straightforward validation task once per-sample SigProfiler assignment is integrated downstream of the cross-study aggregation (see question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross).
- **What are the gastric cancer studies in cBioPortal with matched-normal sequencing?** Matched-normal status is needed to reliably detect signature 3 (the paper requires it for the cell-line analysis and it is central to the pipeline's `matched_normal_studies` config list).
- **Could the Lauren-type/histology association be reproduced within cBioPortal gastric studies?** This would require that the relevant TCGA gastric STAD and other gastric studies expose Lauren type as a clinical variable — worth checking.
