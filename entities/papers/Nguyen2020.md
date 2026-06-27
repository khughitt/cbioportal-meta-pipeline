---
type: paper
title: Pan-cancer landscape of homologous recombination deficiency
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Nguyen2020
ontology_terms:
- homologous recombination deficiency
- mutational signatures
- somatic mutation
- whole-genome sequencing
- BRCA1
- BRCA2
- pan-cancer
datasets: []
source_refs:
- cite:Nguyen2020
related: []
---

# Pan-cancer landscape of homologous recombination deficiency

- **Authors:** Luan Nguyen, John W. M. Martens, Arne Van Hoeck, Edwin Cuppen
- **Year:** 2020
- **Journal:** Nature Communications
- **DOI/URL:** https://doi.org/10.1038/s41467-020-19406-4
- **BibTeX key:** Nguyen2020
- **Source:** PDF (corrupted local copy; text extracted via Europe PMC XML, PMC7643118)

## Key Contribution

CHORD (Classifier of HOmologous Recombination Deficiency) is a random forest model trained
on whole-genome somatic mutation contexts (SNV, indel, and SV features; not pre-extracted
COSMIC signatures) that detects HRD pan-cancer with high accuracy (AUROC > 0.98) and
additionally distinguishes BRCA1-type from BRCA2-type HRD. Applied to ~5,100 primary and
metastatic tumors spanning multiple cancer types, the study reveals the pan-cancer prevalence
of HRD, identifies the genetic causes per cancer type, and argues that genome-wide
mutational-scar testing is superior to germline BRCA1/2 testing alone for patient stratification
towards PARP inhibitor therapy.

A key methodological finding is that **accurate HRD detection does not require an intermediate
mutational signature decomposition step**: CHORD using raw mutation contexts matches the
performance of a signature-based variant (CHORD-signature) and of HRDetect, while simplifying
the pipeline and avoiding complications of signature-fitting.

## Methods

- **Training data:** 2,026 solid metastatic tumor WGS samples from the Hartwig Medical
  Foundation (HMF) pan-cancer cohort; samples selected for high-confidence BRCA1 (n=35) or
  BRCA2 (n=89) biallelic loss, or BRCA1/2-proficient status (n=1,902).
- **Features:** Relative counts of 29 mutation context features — six base-substitution classes
  (SNV), 30 indel contexts (stratified by microhomology, repeat, or neither, and further by
  length), and 16 SV contexts (type × length bins). The 96-trinucleotide contexts were collapsed
  to 6 for CHORD; microhomology deletions were split into ≥2 bp vs 1 bp bins.
- **Model:** Random forest with nested 10-fold cross-validation; feature selection and class
  resampling to handle class imbalance; outputs BRCA1-type HRD probability, BRCA2-type HRD
  probability; HRD classification threshold = 0.5 (sum of the two).
- **Validation:** (1) 10-fold CV on HMF training set; (2) BRCA-EU dataset (543 primary breast
  tumors, including 365 used by HRDetect); (3) PCAWG pan-cancer dataset (1,854 primary tumors).
- **Biallelic status determination:** 781 cancer/HR genes screened using copy number (deep
  deletion < 0.3 copies), LOH (minor allele < 0.2), and pathogenicity-scored SNV/indels
  (ClinVar P-scores; SnpEff fallback). BP-score = sum of two event P-scores; threshold of 10
  defines high-confidence biallelic inactivation.
- **Application:** CHORD applied to full HMF (3,504 patients) and PCAWG (1,618 patients) cohorts
  after QC filtering (MSI exclusion: ≥14,000 repeat indels; minimum variant counts).
- **Tool availability:** R package at https://github.com/UMCUGenetics/CHORD;
  mutation context extraction via https://github.com/UMCUGenetics/mutSigExtractor.

## Key Findings

1. **Performance:** CHORD achieves AUROC ≥ 0.98 and AUPRC ≥ 0.87 on training CV; AUROC > 0.98
   and AUPRC > 0.93 on both independent validation datasets. F1 ≈ 0.88 at threshold 0.5.
   Performance is comparable to HRDetect on BRCA-EU, and 99% concordant with HRDetect on PCAWG.

2. **Key predictive features:** Deletions with ≥2 bp flanking microhomology (del.mh.bimh.2.5)
   are the single most important HRD feature. 1–10 kb and 10–100 kb structural duplications
   distinguish BRCA1-type from BRCA2-type HRD (only BRCA1 deficiency generates these).

3. **HRD landscape:** 310/5,122 patients (6%) classified HRD across both cohorts: 118 BRCA1-type,
   192 BRCA2-type. HRD is most prevalent in ovarian (52% primary, 30% metastatic), breast
   (24% primary, 12% metastatic), prostate (~13% metastatic), and pancreatic (~13% metastatic)
   cancer; the latter two have substantially higher HRD rates in metastatic vs. primary disease.

4. **Genetic causes:** Biallelic inactivation of BRCA1, BRCA2, RAD51C, or PALB2 explains ~60%
   (184/310) of CHORD-HRD patients. RAD51C and PALB2 deficiency produce BRCA2-type HRD (absence
   of tandem duplications). LOH is the dominant second hit, followed by deep deletion. Germline
   pathogenic variants account for only ~30% of CHORD-HRD — a major limitation of germline-only
   testing. Somatic-only biallelic inactivation explains 35% pan-cancer, rising to 54% in
   prostate cancer due to frequent BRCA2 deep deletions.

5. **Cancer-type specificity:** The relative frequency of BRCA1-type vs BRCA2-type HRD differs
   by tissue: ovarian/breast favor BRCA1-type; pancreatic/prostate favor BRCA2-type. Cancer-type
   composition of the training set does not bias predictions (HRD mutational footprint is
   tissue-type-agnostic; false positive < 2%, false negative < 6% in held-out cancer types).

6. **Treatment effects:** Radiotherapy can induce microhomology deletions, but splitting del.mh
   into 1 bp vs ≥2 bp bins largely mitigates this; the overall impact on HRD classification
   is minimal when using all somatic variants (clonal + subclonal). Subclonal-only CHORD
   predictions should be interpreted with caution.

7. **Signatures not needed:** CHORD using raw mutation contexts matches a signature-based variant
   (CHORD-signature using fitted COSMIC SBS + SV signatures), demonstrating that detecting HRD
   does not require the intermediate signature-fitting step. This bypasses current ambiguities
   in per-sample signature decomposition.

## Relevance

**Relevance to h08 (agnostic covariate↔signature-exposure association):**

- HRD/BRCA-deficiency is the underlying aetiology for SBS3 (homologous recombination deficiency)
  and ID6/ID8 (microhomology-mediated end-joining deletions). This paper defines how to
  operationalize HRD ground-truth status — a prerequisite for any aetiology-assignment
  benchmark, including h08a's positive-control recovery.
- The paper's central methodological claim — that HRD can be detected from raw mutation contexts
  *without* fitting COSMIC signatures — is directly relevant to h08's design choice of using
  per-sample mutation spectra (or exposures) as outcomes. It validates that the raw-context
  representation retains sufficient information.
- HRD status is a strong candidate covariate in the h08 agnostic scan: BRCA1/2-deficient tumors
  have markedly elevated SBS3 and indel-microhomology exposures, so a properly calibrated scan
  should recover HRD→SBS3 as a strong positive-control association alongside UV→SBS7 and
  smoking→SBS4.
- The finding that germline-only BRCA testing misses ~70% of HRD patients is a concrete example
  of how phenotypic covariates (clinical HER2/ER/PR status, germline panel results) will give
  incomplete signal; WGS-derived functional HRD status (like CHORD outputs) would be more
  informative but is not routinely available in cBioPortal study metadata.

**Cross-study / pipeline relevance:**

- In the cbioportal cross-study meta-analysis context, BRCA1/2 mutation frequency is a tracked
  gene-level output. CHORD provides the conceptual link between those counts and the functional
  HRD phenotype: not all biallelically inactivated BRCA2 tumors are in the mutation table (deep
  deletions are missed by SNV-only pipelines), and not all BRCA1/2-mutant tumors have HRD
  (monoallelic events without LOH don't produce the scar). This is relevant when interpreting
  gene-cancer frequency tables that include BRCA1/2.
- RAD51C and PALB2 emerge as important HRD drivers not captured by BRCA1/2-centric clinical
  testing — these are genes worth tracking in the cross-study aggregation for contexts where
  HRD interpretation is relevant.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| CHORD HRD probability | Potential covariate in h08 agnostic scan | Not in cBioPortal metadata; would need external join |
| Biallelic BRCA1/BRCA2 status | Gene-cancer mutation frequency (gene_cancer_study.feather) | cBioPortal captures SNV/indels but frequently misses deep deletions and CNV-mediated LOH |
| BRCA1-type vs BRCA2-type HRD | Signature-subtype discrimination | Analogous to distinguishing SBS2 vs SBS13 (APOBEC sub-activities) |
| Mutation contexts (SNV/indel/SV relative fractions) | Input features for signature decomposition | CHORD uses these directly; h08 uses COSMIC-fitted exposures as outcomes |
| HRD mutational scar | SBS3 / ID6 / ID8 COSMIC signatures | Paper demonstrates the scar is tissue-agnostic |
| MSI exclusion (≥14,000 repeat indels) | Hypermutator exclusion | Analogue to the project's GMM-based hypermutator annotation; MSI masks microhomology signal |

## Limitations

- WGS required: CHORD relies on indel microhomology and SV features that are poorly captured
  by targeted panels or WES; direct application to cBioPortal panel-sequenced cohorts is not
  feasible without re-architecture.
- Training cancer-type imbalance: BRCA1/2-deficient training samples were predominantly ovarian,
  breast, and prostate; false-negative rate in under-represented cancer types (biliary, lung) may
  be underestimated.
- Variant-calling pipeline sensitivity: Indel and SV calling quality affects predictions;
  the authors note that different pipelines alter HRD probabilities, particularly for BRCA1-
  deficient samples; threshold re-calibration is recommended for new pipelines.
- Methylation data absence: ~40% of CHORD-HRD patients lack clear biallelic genetic inactivation;
  BRCA1/RAD51C promoter methylation is the likely explanation but could not be confirmed in HMF
  or PCAWG due to lack of methylation data.
- Mutational scars represent history not current status: reversion mutations (secondary
  frameshifts) can restore HRD; recent acquisition of HRD may not yet accumulate enough scar.
- Cohort differences: metastatic vs. primary cancer rates may reflect patient selection bias
  rather than true biological stage-dependent HRD frequency.

## Model / Tool Availability

- **CHORD R package:** https://github.com/UMCUGenetics/CHORD
- **mutSigExtractor R package:** https://github.com/UMCUGenetics/mutSigExtractor (context
  extraction from VCF/TSV mutation data)
- License: not explicitly stated in the paper text; check the repositories before reuse
- Input: somatic VCF files (SNV/indel + SV) processed through the HMF pipeline or equivalent;
  relative mutation context fractions computed per sample
- Output: BRCA1-type HRD probability, BRCA2-type HRD probability, HRD classification (≥0.5)
- Hardware requirements: standard desktop; random forest inference is lightweight

## Follow-up

- HRDetect (Davies et al. 2017, *Nature Medicine*) — the breast-cancer-specific predecessor;
  uses COSMIC signatures as input features rather than raw contexts.
- Priestley et al. 2019 — the full HMF metastatic pan-cancer cohort paper underlying the
  training data.
- Ellrott et al. 2018 (MC3 TCGA MAF) — the cBioPortal pipeline's TCGA equivalent; CHORD
  applied to MC3 would require SV calls, which MC3 does not include.
- PCAWG consortium papers — provide the validation cohort.
- For h08: connecting HRD status to SBS3 exposure in the within-tissue association model —
  whether cBioPortal panel data yields enough microhomology indels to proxy HRD probability
  (likely no; this is a concrete limitation for the h08 positive-control design where SBS3
  is not one of the three pre-registered arms).
