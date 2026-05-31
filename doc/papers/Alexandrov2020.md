---
id: "paper:Alexandrov2020"
type: "paper"
title: "The repertoire of mutational signatures in human cancer"
status: "active"
ontology_terms:
  - mutational signatures
  - somatic mutation
  - single-base substitution
  - doublet-base substitution
  - insertion-deletion
  - NMF
  - PCAWG
  - COSMIC
  - cancer genomics
  - DNA damage and repair
datasets: []
source_refs:
  - "cite:Alexandrov2020"
related:
  - "paper:Alexandrov2015"
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
created: "2026-05-31"
updated: "2026-05-31"
---

# The repertoire of mutational signatures in human cancer

- **Authors:** Ludmil B. Alexandrov, Jaegil Kim, Nicholas J. Haradhvala, Mi Ni Huang, Alvin Wei Tian Ng, Yang Wu, Arnoud Boot, Kyle R. Covington, Dmitry A. Gordenin, Erik N. Bergstrom, S. M. Ashiqul Islam, Nuria Lopez-Bigas, Leszek J. Klimczak, John R. McPherson, Sandro Morganella, Radhakrishnan Sabarinathan, David A. Wheeler, Ville Mustonen, PCAWG Mutational Signatures Working Group, Gad Getz, Steven G. Rozen, Michael R. Stratton, PCAWG Consortium
- **Year:** 2020
- **Journal:** Nature
- **DOI/URL:** https://doi.org/10.1038/s41586-020-1943-3
- **BibTeX key:** Alexandrov2020
- **Source:** PDF

## Key Contribution

This paper presents the most comprehensive catalogue of mutational signatures in human cancer to
date, derived from the full PCAWG dataset of 4,645 whole genomes and 19,184 exomes spanning most
cancer types. Using two complementary NMF-based tools (SigProfiler and SignatureAnalyzer), the
authors extracted 49 single-base substitution (SBS), 11 doublet-base substitution (DBS), 4
clustered-base substitution (CBS), and 17 insertion-deletion (ID) signatures — together defining
COSMIC v3 — and assigned proposed aetiologies (UV, tobacco, APOBEC, MMR deficiency, HRD, etc.)
to most, while flagging a substantial fraction as unknown. The 10-fold increase in mutation data
vs prior analyses enabled better separation of overlapping signatures and decomposition of
previously fused signatures into biologically distinct components.

## Methods

**Cohort:** The 23,829-sample PCAWG set (2,780 WGS + 19,184 exomes + 1,865 additional WGS from
other sources), yielding 79,793,266 SBSs, 814,191 DBS, and 4,122,233 small indels — roughly
10-fold more mutations than any prior signature study.

**Classification schemes:** SBSs classified into 96 trinucleotide classes (pyrimidine-centric);
extended to 1,536 pentanucleotide classes for COMPOSITE analysis. DBSs classified into 78 classes;
indels into 83 classes based on type (deletion/insertion), length, repeat context, and
microhomology.

**Extraction tools:**
- *SigProfiler:* hierarchical de novo NMF extraction (generalised Kullback-Leibler divergence);
  separate extraction from low-burden and hypermutated samples; SigProfilerAttribution for
  per-sample contribution estimation.
- *SignatureAnalyzer:* Bayesian ARD-NMF; automatic relevance determination infers the number of
  signatures; applies to 1,697-feature COMPOSITE space.
- Both tools validated on 11 sets of synthetic data (64,400 total synthetic samples) generated
  from known signatures.

**Two-step approach for hypermutators:** Step 1 extracts signatures from non-hypermutated samples
(n = 2,624, excluding POLE/MMR-deficient/skin/TMZ-exposed); Step 2 adds signatures unique to
hypermutated samples. Biological plausibility and human-guided sensitivity analyses were used to
guide final signature selection alongside mathematical extraction.

**Age correlations:** Robust linear regression (MATLAB `robustfit`) between age at diagnosis and
per-signature mutation burden, Benjamini-Hochberg FDR correction.

## Key Findings

**SBS signatures (49 total, 49 considered biologically plausible):**
- 67 candidate SBS signatures extracted; 49 considered of biological origin.
- All COSMIC v2 signatures confirmed (median cosine similarity 0.95 to new signatures), except
  SBS25 (previously found only in chemotherapy-treated Hodgkin lymphoma cell lines).
- Three previously unified signatures split: SBS7 → SBS7a/b/c/d (UV); SBS10 → SBS10a/b;
  SBS17 → SBS17a/b.
- Thirteen signatures newly identified and probably real (not in COSMIC v2): SBS31 (platinum),
  SBS32 (azathioprine), SBS35 (platinum), SBS36 (MUTYH mutation), SBS38 (indirect UV),
  SBS39 (unknown), SBS40 (flat/clock-like), SBS42 (haloalkane occupational exposure), SBS44
  (defective MMR).
- SBS signatures show substantial variation across cancer types and samples; median of ~3
  signatures per sample.

**Key aetiology assignments:**
- SBS1 (deamination of 5-methylcytosine), SBS5 (unknown/clock-like): both correlate with age.
- SBS2/13 (APOBEC3A and APOBEC3B cytidine deaminase activity): APOBEC3A accounts for more
  mutations; split attributable to distinct trinucleotide contexts at +2 and −2 positions.
- SBS4 (tobacco smoking, C>A dominant, transcriptional strand bias): lung, head-and-neck.
- SBS7a/b/c/d (UV light): malignant melanoma, transcriptional strand bias indicating NER.
- SBS6/15/26/44 (defective MMR): associated with microsatellite instability.
- SBS10a/b (POLE mutation + MMR deficiency): extreme hypermutation.
- SBS5 and SBS40 correlate with age in multiple cancer types; possibly reflective of
  replication-associated processes operating in normal cells.

**DBS signatures (11 total):**
- DBS1: UV-induced (CC>TT); found in melanoma.
- DBS2: tobacco-smoke-associated (CC>AA); lung adenocarcinoma, lung squamous.
- DBS4/9/10: defective MMR or POLE-related.
- DBS5: platinum chemotherapy.
- DBS6/10: defective MMR.
- Numbers of DBSs generally proportional to SBSs but lung cancers and melanomas have more than
  expected.

**Indel signatures (17 total):**
- ID1 (poly-T insertions) and ID2 (poly-T deletions): replication slippage; most cancer types,
  particularly colorectal, stomach, endometrial, oesophageal; correlated with SBS1/5, suggestive
  of mitotic origin. Together account for 97% of indels in hypermutated and 45% in
  non-hypermutated genomes.
- ID3 (cytosine deletions at short cytosine repeats): tobacco-smoking-associated; lung, head-
  and-neck, transcriptional strand bias consistent with NER on guanine damage.
- ID6/8: homologous recombination deficiency.
- ID13: thymine–thymine dinucleotide deletions; UV-induced; malignant melanoma skin.

**Clustered mutations:**
- Four main clustered SBS signatures identified: CBS2 and CBS3 (APOBEC activity);
  CBS4 (C>T and C>G at cytosine trinucleotides, lymphoid neoplasms — activation-induced
  cytidine deaminase); CBS5 (T>A and T>G at thymine trinucleotides, lymphoid — translesion DNA
  synthesis).

**Age correlations:**
- SBS1, SBS5, SBS40, SBS8 correlate positively with age across multiple cancer types.
- ID1, ID2, ID5 correlate with age; DBS2, DBS4 correlate with age in some tissues.
- Interpretation: multiple mutational processes operate in normal cells, accumulating during
  normal cell division throughout life.

**Unknown-aetiology signatures:**
- A substantial fraction of signatures remain unexplained (SBS5, SBS8, SBS12, SBS16, SBS17a/b,
  SBS19–21, SBS23, SBS25–26, SBS28–33, SBS36–40, many DBS and ID). The paper notes that
  common, geographically restricted, and therapeutic exposures may remain uncharacterised.

**Concordance between SigProfiler and SignatureAnalyzer:**
- Most results agreed well; key differences in flat/featureless signatures (SBS5/40-related
  attribution) and in the numbers of signatures extracted from hypermutated samples (13 vs 25
  SBS signatures from hypermutated PCAWG samples).

## Relevance

This paper is the **primary reference catalogue for hypothesis h08** (agnostic covariate↔signature
exposure association). It defines:

1. **The positive-control signature set for H08a:** The well-characterised UV→SBS7, tobacco→SBS4,
   APOBEC3→SBS2/13, MMR-loss/MSI→SBS6/15/26/44, POLE→SBS10a/b linkages are documented here with
   their cancer-type distributions and proposed aetiologies. An agnostic association scan on
   cBioPortal/MC3 data should re-discover these links to validate that the pipeline is
   sufficiently powered.

2. **The benchmark for novel discovery (H08b):** The paper explicitly catalogues signatures with
   unknown or only partial aetiologies (SBS5, SBS8, SBS16, SBS17a/b, SBS25, SBS39, SBS40 and many
   DBS/ID signatures). These are the target space for H08b — covariates (especially expression
   modules) associated with these signatures in an agnostic scan represent ranked novel candidates
   for upstream causes.

3. **The COSMIC v3 reference frame:** All downstream signature attribution in the cbioportal
   pipeline (via `run_restricted_sigprofiler_assignment.py`) uses COSMIC v3 signatures as its
   reference. This paper is the origin of those signatures and describes their profiles, cancer-type
   distributions, and attributions.

4. **Positive-control recovery check — specific predictions testable in the pipeline:**
   - SBS4 should have highest exposure in lung and head-and-neck cancers (tobacco-enriched
     cBioPortal studies).
   - SBS7a/b should dominate skin/melanoma studies.
   - SBS2/13 exposure should correlate with APOBEC3A/3B mRNA in studies with co-measured
     expression.
   - SBS6/15/26 should segregate with MSI-H samples (flagged by the MSI annotation step in
     the hypermutator pipeline).

5. **Age as a confounder:** The finding that SBS1, SBS5, SBS40 correlate with age is directly
   relevant to h08's within-tissue association design: age must be included as a nuisance covariate
   or tested separately to avoid confounding clock-like signature associations with true exposure
   signals.

6. **Methodological reference for two-step extraction and hypermutator stratification:** The
   paper's strategy of separating low-burden and hypermutated samples before extraction directly
   informs the pipeline's annotation approach (compute_per_sample_tmb + annotate_hypermutators),
   and the `matched_normal_studies` config list.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| SBS signatures (COSMIC v3) | Reference signatures for restricted SigProfiler attribution | Used in `run_restricted_sigprofiler_assignment.py` |
| Hypermutated tumours (POLE/MMR/skin/TMZ) | `is_hypermutator` / `hypermutator_reason` | Annotated via `annotate_hypermutators` rule |
| Tobacco-associated SBS4 / DBS2 / ID3 | Positive control for h08a (smoking arm) | Lung / head-and-neck enrichment |
| UV-associated SBS7a/b/c/d / DBS1 / ID13 | Positive control for h08a (UV arm) | Skin-Melanoma enrichment |
| APOBEC SBS2/13 / CBS2/3 | Positive control for h08a (APOBEC3 expression arm) | Requires co-measured expression data |
| Clock-like SBS1/5/40 (age-correlated) | Unknown-aetiology discovery targets (H08b) | Must model age as covariate |
| Signature aetiologies listed in Fig. 3 | `bailey2018_driver` and clinical overlays | Corroborates which gene mutations drive hypermutation phenotypes |
| SigProfiler / SignatureAnalyzer | `run_restricted_sigprofiler_assignment.py` | Pipeline uses SigProfiler restricted attribution |

## Limitations

- The reference signatures are derived from cancer exomes and genomes; panel-sequenced data
  (most cBioPortal studies) have far fewer mutations per sample and are not directly decomposable
  on a per-sample basis — a binding constraint noted in question:q018.
- A substantial fraction of extracted signatures remain unexplained (unknown aetiology); the paper
  does not provide a systematic association framework for identifying upstream causes.
- Signature extraction is sensitive to the number of signatures requested (NMF rank), to
  hypermutator thresholds, and to the mathematical method (SigProfiler vs SignatureAnalyzer produce
  modestly different results for flat and featureless signatures).
- Transcriptional strand bias is used as a proxy for aetiology assignment but is an indirect
  measure; direct experimental validation is available only for a subset of signatures.
- The two-step extraction strategy (low-burden first, then hypermutated) introduces an ordering
  assumption: signatures unique to hypermutated samples might be missed if the first step does not
  adequately characterise shared signatures.
- Cross-study heterogeneity (sequencing platform, calling algorithm, tumour purity, matched-normal
  availability) is not modelled within the main PCAWG dataset; the cbioportal pipeline inherits
  this limitation.

## Model / Tool Availability

- **SigProfiler (Python/MATLAB):** BSD-2 licence.
  - Python: https://github.com/AlexandrovLab/SigProfilerExtractor
  - MATLAB: https://www.mathworks.com/matlabcentral/fileexchange/38724-sigprofiler
- **SignatureAnalyzer:** MIT licence.
  - https://github.com/broadinstitute/getzlab-SignatureAnalyzer
- **COSMIC v3 signature profiles:** https://cancer.sanger.ac.uk/cosmic/signatures/
- **All derived datasets (synapse accession synXXXXXXXX):** open-access, no registration required.
  - Observed mutational spectra: syn11801889
  - SigProfiler signatures: syn11738306
  - SignatureAnalyzer signatures: syn11738307
  - Per-tumour mutation counts per signature: syn11804065
  - Per-tumour signature probabilities: syn11804068
  - Synthetic test data + extraction test results: syn18497223

## Follow-up

- Degasperi 2022 (`paper:Degasperi2022`) extends this catalogue with tissue-specific reference
  signatures (SIGNAL/SIGFIT) and provides a framework for fitting signatures to panel data —
  directly relevant to q018.
- Check whether the cBioPortal studies used in the meta-analysis have per-sample SBS attribution
  from the PCAWG pipeline (syn11804065) as an external validation reference.
- For h08 implementation: confirm which COSMIC v3 SBS signatures have well-supported,
  experimentally verified aetiologies (positive-control tier) vs only proposed aetiologies
  (the paper marks uncertain assignments with asterisks in Fig. 3).
- Age-signature correlations (SBS1, SBS5, SBS40) suggest that age stratification or age
  residualisation is necessary before any agnostic covariate scan — add as a design requirement
  for the H08a pre-registration.
