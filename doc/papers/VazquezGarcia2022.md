---
id: "paper:VazquezGarcia2022"
type: "paper"
title: "Ovarian cancer mutational processes drive site-specific immune evasion"
status: "active"
ontology_terms:
  - mutational signatures
  - homologous recombination deficiency
  - tumour microenvironment
  - immune evasion
  - high-grade serous ovarian cancer
  - single-cell RNA sequencing
  - whole-genome sequencing
datasets: []
source_refs:
  - "cite:VazquezGarcia2022"
related: []
created: "2026-05-31"
updated: "2026-05-31"
---

# Ovarian cancer mutational processes drive site-specific immune evasion

- **Authors:** Ignacio Vázquez-García, Florian Uhlitz, Nicholas Ceglia, Jamie L. P. Lim, et al. (Sohrab P. Shah lab, MSK)
- **Year:** 2022
- **Journal:** Nature
- **DOI/URL:** https://doi.org/10.1038/s41586-022-05496-1
- **BibTeX key:** VazquezGarcia2022
- **Source:** PDF (Europe PMC XML full text; local PDF corrupted/unreadable)

## Key Contribution

In a prospective multi-site biopsy study of 42 treatment-naive HGSOC patients (160 tumour sites),
WGS-derived structural-variation mutational subtypes (HRD-Dup, HRD-Del, and foldback-inversion
[FBI]) each drive a distinct tumour microenvironment (TME) and immune-evasion programme. HRD
subtypes show elevated JAK–STAT and NF-κB inflammatory signalling with HLA class I LOH and
highly dysfunctional CD8+ T cells (active immunoediting), whereas FBI tumours exhibit
TGFβ-driven immune exclusion and predominantly naive/stem-like T cells (immunological inertness).
TME composition and cellular topology further vary by anatomical site, revealing that mutational
processes and peritoneal spread together co-determine immune resistance in HGSOC.

## Methods

- **Cohort:** 42 treatment-naive HGSOC patients; 160 multi-site biopsies spanning adnexa,
  omentum, peritoneum, bowel, ascites, and other intraperitoneal sites; collected prospectively
  at MSK over 24 months.
- **Sequencing:** Whole-genome tumour–normal sequencing (WGS); MSK-IMPACT (468-gene targeted
  panel); single-cell RNA-seq (scRNA-seq) on CD45+ and CD45− sorted fractions.
- **Imaging:** H&E histopathology and multiplexed immunofluorescence (mpIF) with markers for
  T cells (CD8, PD-1, TOX), macrophages (CD68), and cancer cells (pan-CK, PD-L1).
- **Mutational signature inference:** WGS copy-number profiles used to classify tumours into
  HRD-Dup (BRCA1-like, tandem duplications), HRD-Del (BRCA2-like, interstitial deletions),
  FBI (foldback inversion, associated with CCNE1 amplification), and TD (tandem duplicator,
  CDK12-associated). 16 HRD-Dup, 6 HRD-Del, 14 FBI cases in discovery cohort.
- **Key algorithms:** SIGNALS (single-cell allele imbalance) for per-cell HLA LOH from scRNA-seq;
  GLM for anatomical site × mutational signature effects on cell-type composition.
- **Validation:** MSK-IMPACT cohort (n = 1,298) for HLA LOH frequency by BRCA1/BRCA2/CCNE1/CDK12 status.

## Key Findings

1. **Mutational subtype drives TME immunophenotype.** HRD subtypes (HRD-Dup, HRD-Del) are
   enriched for dysfunctional (CD8+PD-1+TOX+) T cells and activated JAK–STAT / NF-κB / type I
   IFN signalling in cancer cells. FBI tumours have elevated TGFβ in cancer cells and immune-excluded
   TMEs with predominantly naive/stem-like T cells.

2. **Anatomical site modulates immune composition independently.** CD45+ immune fractions vary
   significantly across sites: ascites is T-cell- and DC-enriched; adnexal lesions are lymphocyte-
   and B-cell-depleted. Non-adnexal solid sites have higher CD8+ T cell fractions than adnexa.

3. **HRD-Dup immunoediting involves early HLA class I LOH.** 6p LOH (HLA class I locus) is
   most prevalent in HRD-Dup (clonal) vs. FBI (subclonal), and co-occurs with JAK–STAT upregulation
   and T cell dysfunction. In the 1,298-patient IMPACT cohort, HLA LOH prevalence: BRCA1-mutant
   31%, BRCA2-mutant 19%, CCNE1-amplified 24%.

4. **PD-L1 spatial interactions are mutational-subtype specific.** CD8+PD-1+ T cells within
   30 µm of PD-L1+ cancer cells are common in HRD-Dup adnexa and bowel but rare/absent in FBI.

5. **FBI tumours are immunologically inert.** TGFβ-driven signalling and near-absence of
   antigen-experienced T cell–cancer cell proximity explains the therapeutic resistance of
   FBI tumours (already known to be chemotherapy-resistant).

6. **Cancer cell signalling is site × subtype specific.** JAK–STAT/NF-κB immune signalling in
   HRD-Dup is strongest at adnexal (primary) sites, suggesting early immune selection; TGFβ
   in FBI is strongest at non-adnexal (metastatic) sites.

## Relevance

**To h08 (agnostic covariate–signature-exposure association):** This paper is a direct
exemplar of the mechanistic layer underlying h08's positive-control target. The paper
demonstrates that WGS-derived structural-variation mutational signatures (HRD-Dup, HRD-Del,
FBI, TD) stratify tumours by both genomic process *and* by downstream immune phenotype,
gene-expression programme (JAK–STAT, TGFβ), and HLA LOH. In h08 terms:

- The signature exposures (HRD-Dup/Del vs. FBI) are the `H` column outcomes.
- The co-measured mRNA modules (JAK–STAT, TGFβ, NF-κB, IFN) are exactly the kind of
  **expression covariate** the agnostic association pipeline should recover — the paper
  shows these associations are strong, consistent, and biologically causal.
- HLA LOH frequency (6p LOH) is a structured clinical/genomic feature analogous to the
  MSI or POLE covariates listed as h08 positive controls.
- **APOBEC3 context:** SBS2/13 (APOBEC) is not the focus here; the relevant signatures are
  SBS3 (HRD) and rearrangement signatures. This paper shows that downstream
  covariate associations can go well beyond SNV-signature aetiologies to link structural
  rearrangement mutational processes to TME immunophenotype — an expanded scope for h08b.

**To the cross-study somatic mutation meta-analysis:** HGSOC is represented in several
cBioPortal studies. HRD status and CCNE1 amplification are well-characterised drivers that
our gene × cancer cross-study tables should capture. The mutational-subtype→immune-evasion
linkage shown here provides biological context for interpreting cross-study BRCA1/BRCA2/CDK12
mutation frequency patterns in ovarian cancer.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| HRD-Dup / HRD-Del / FBI / TD mutational subtypes | WGS structural-variation signatures; analogous to COSMIC rearrangement signatures | Paper uses SV patterns rather than SNV SBS catalogue |
| SIGNALS per-cell 6p LOH | HLA loss / immune editing covariate | Clinical covariate for h08 association |
| JAK–STAT / TGFβ / NF-κB expression modules | mRNA expression modules from export_study_expression.py | These are exactly the co-measured covariates h08 would test |
| TME immune cell composition by site | Not currently captured in cBioPortal pipeline | Would require scRNA deconvolution data |
| MSK-IMPACT 468-gene panel | cBioPortal targeted panel studies | Same platform; msk_impact studies in cBioPortal |

## Limitations

- **SNV-based mutational signatures not the primary focus.** The study uses structural variation
  (copy number rearrangement) signatures rather than the SBS/ID/DBS trinucleotide catalogues
  used by COSMIC and the cbioportal pipeline. h08's positive controls (UV/SBS7, smoking/SBS4,
  APOBEC/SBS2+13, MMR/SBS6) are not directly assessed here.
- **Small discovery cohort (n = 42).** Despite multi-site sampling, power for rare subgroups
  is limited; the larger validation relies on targeted sequencing (IMPACT) rather than WGS.
- **Single institution (MSK).** Potential referral bias toward surgically amenable disease;
  patient and tumour characteristics may not generalise.
- **Site × subtype interpretations are observational / correlative.** Causal direction of
  immune signalling (early selection vs. reaction) is inferred from subclonal structure and
  site patterns; not experimentally proven.
- **No immunotherapy outcome data.** Despite motivating improved immunotherapy, the study
  is purely biomarker-level and does not report ICB response.

## Model / Tool Availability

- **SIGNALS algorithm** for per-cell allele imbalance inference from scRNA-seq (previously
  published alongside the broader HGSOC genomic landscape paper, Shah lab).
- Data and code deposition referenced in the paper; specific repository URL [UNVERIFIED].

## Follow-up

- **Cross-study:** Examine HRD/BRCA1/BRCA2/CCNE1/CDK12 mutation frequencies across
  cBioPortal ovarian cancer studies to see whether the mutational subtype proportions
  replicate in public data.
- **h08 connection:** When implementing the covariate-association pipeline, add HRD status /
  HRD score as a candidate covariate. The strong JAK–STAT vs. TGFβ split between HRD-Dup
  and FBI tumours would serve as a positive-control test case for the expression-module
  correlation arm of h08.
- **Related papers to read:** Macintyre et al. 2018 (copy number signatures in ovarian
  cancer), Macintyre/Shah group HGSOC landscape paper (SIGNALS algorithm introduction),
  TCGA ovarian cancer analyses for comparison.
