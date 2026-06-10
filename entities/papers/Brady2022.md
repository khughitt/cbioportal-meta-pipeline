---
type: paper
title: Therapeutic and prognostic insights from the analysis of cancer mutational
  signatures
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Brady2022
ontology_terms:
- mutational signatures
- cancer therapeutics
- homologous recombination deficiency
- APOBEC
- mismatch repair deficiency
- therapy-induced mutagenesis
- COSMIC signatures
- prognosis
datasets: []
source_refs:
- cite:Brady2022
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
---

# Therapeutic and prognostic insights from the analysis of cancer mutational signatures

- **Authors:** Samuel W. Brady, Alexander M. Gout, Jinghui Zhang
- **Year:** 2022
- **Journal:** Trends in Genetics, Vol. 38, No. 2, pp. 194–208
- **DOI/URL:** https://doi.org/10.1016/j.tig.2021.08.007
- **BibTeX key:** Brady2022
- **Source:** PDF

## Key Contribution

This review synthesizes how mutational signature analysis — historically used to identify cancer
aetiology — is now yielding direct clinical value: identifying predictive biomarkers of therapy
sensitivity (HR deficiency → PARPi; APOBEC → ATRi), supplying prognostic classifiers (e.g.,
myeloma SV+SNV scheme with seven subgroups), and revealing therapy-induced mutagenesis that may
contraindicate specific treatments (thiopurines inducing COSMIC SBS87 → TP53 driver mutations in
MMR-deficient ALL). The review also charts emerging technologies (cfDNA, mutREAD) that could
make routine signature-guided clinical decision-making feasible.

## Methods

Narrative review drawing on the COSMIC v3.x catalogue (>60 SNV, 11 doublet, 18 indel, 8–12 SV
signatures), with three analytical phases framing each clinical application: (1) somatic variant
calling, (2) signature extraction via NMF-based tools (SigProfiler, SignatureAnalyzer,
MutationalPatterns), and (3) signature activity assignment in individual samples. The review
synthesizes findings across WGS-based cohorts, cell-line pharmacogenomics datasets (Genomics of
Drug Sensitivity in Cancer; 930 lines, 518 drugs, 29 cancer types), and several disease-specific
studies (breast, esophageal, multiple myeloma, ALL, glioma, neuroblastoma, pediatric tMNs).

## Key Findings

**Therapy sensitivity biomarkers**

- **HR deficiency (SBS3 + indel SBS + SV5):** HRDetect and CHORD classifiers predict BRCA1/2
  deficiency, PARP inhibitor sensitivity (breast, ovarian), and response to adjuvant
  platinum-based chemotherapy. Mechanistically, PARP inhibition at single-strand breaks →
  DSBs → cell death in HR-deficient tumours.
- **APOBEC (SBS2/13):** Associated with sensitivity to ATR kinase inhibition across breast,
  ovarian, and other cancers. APOBEC enzymes act on ssDNA at replication forks; ATR stabilises
  stalled forks, so APOBEC-active cancers may accumulate lethal abasic sites when ATR is
  inhibited. Intermittent APOBEC activity means only tumours with current activity are likely
  to respond.
- **MMR deficiency (SBS6/15/26/44):** WRN helicase and WEE1/CHK1/2 are synthetic-lethal
  targets; MMR-deficient tumours are also hypersensitive to PD-1/PD-L1 blockade. Signature-
  based MMR detection is orthogonal to MSI PCR and MMR-gene sequencing, capturing promoter-
  hypermethylation and focal-deletion causes missed by exome sequencing.
- **Systematic cell-line screen (Levatić et al.):** Mutational signatures predicted global
  drug response better than oncogenic mutations, CNAs, or methylation alone in 930 cell lines;
  >500 signature–drug correlations observed, including SBS26 ↔ camptothecin in CRC and SBS36
  (ROS) ↔ cabozantinib.

**Cancer prognosis**

- **Colorectal cancer (CRC):** SBS17b (T>G-dominated, possibly acid-reflux-associated) predicts
  worse progression-free survival with EGFR-inhibitor cetuximab by enriching KRAS/NRAS/EGFR
  resistance mutations.
- **Multiple myeloma:** A joint SV + SNV scheme (Hoang et al.) defines seven prognostic
  subgroups. Cluster F (poor outcome, independent of known high-risk molecular markers) lacked
  APOBEC signatures but had COSMIC SNV9 (DNA-polymerase eta somatic hypermutation) and
  non-clustered SV signature 4.
- **Esophageal adenocarcinoma (Secrier et al.):** Three signature-defined subgroups with
  differential sensitivity hypotheses: HR-deficient (PARPi + DNA-damage), SBS17b (immune,
  WEE1/CHK1), SBS1/18 (no specific therapy yet). Signature subgroups were *orthogonal* to
  clinical features (stage, survival, smoking), providing additive predictive information.

**Therapy-induced mutagenesis and contraindications**

- **Thiopurines → SBS87 → TP53 driver mutations in ALL:** Whole-genome sequencing of relapsed
  ALL showed thiopurines induce C>T mutations at NCG trinucleotides (SBS87). In MMR-deficient
  subclones, thiopurine incorporation is 10× more mutagenic because mismatches are not repaired,
  raising TP53 (and NR3C1, NT5C2) mutation probability and driving therapy resistance at relapse.
  A randomised trial showed that high-dose thiopurine increases relapse risk, suggesting
  dose-titration may reduce mutagenesis.
- **Temozolomide → SBS11 → CDKN2A/PI3K driver mutations in glioblastoma:** Signature
  accumulates specifically in MMR-deficient cancer, suggesting temozolomide is
  contraindicated when MMR is absent.
- **Platinum → SBS31/35:** Platinum-induced driver/resistance mutations were *rare* in
  post-treatment ovarian cancer and osteosarcoma, possibly because the platinum signature
  spectrum is not well-positioned to cause recurrent driver-gene variants.
- **Radiation → indel signature + copy-number changes:** In relapsed glioma, radiation-induced
  indels enriched in recurrent disease were associated with worse survival; radiation-induced
  CDKN2A deletions were also detected.
- **Secondary malignancies:** Radiation, anthracyclines, epipodophyllotoxins, platinums, and
  thiopurines are each epidemiologically associated with secondary cancers; driver mutations in
  those secondary cancers often carry the causal treatment signature (e.g., radiation-induced
  TP53/CASP8 inversions).

**Emerging frontiers**

- cfDNA and minimal-residual-disease sequencing can detect mutational signatures from small
  DNA quantities (mutREAD reduced-representation protocol), enabling on-treatment monitoring
  and early therapy-response prediction.
- Pre-treatment testing for MMR-deficient clones in cfDNA or bone marrow could flag patients
  at highest risk of thiopurine-induced TP53 mutagenesis.
- Signature-positive cfDNA would predict therapy sensitivity; signature-negative → likely
  non-response (TPMT-low / thiopurine insensitive example).

## Relevance

**Hypothesis h08 (agnostic covariate ↔ signature-exposure association):**

This review is directly relevant to h08 in two ways.

1. **Positive-control grounding (H08a).** The review catalogues the best-established
   exposure→signature links that H08a must recover: UV light→SBS7 (melanoma), tobacco
   smoking→SBS4 (lung), APOBEC3 activity→SBS2/13 (breast, ovarian, bladder), MMR
   inactivation→SBS6/15/26/44, POLE/POLD1→SBS10, and thiopurines→SBS87. Brady et al. also
   describe the *mechanism* behind each link, which helps design the expected covariate columns
   (e.g., APOBEC3A/B expression modules, MSI status, MMR-gene mutation flags) that the
   H08 agnostic scan should rank at the top for those known associations.

2. **Clinical contraindication signatures as h08 discovery targets (H08b).** The review
   highlights therapy-induced signatures (SBS87, SBS11, radiation indels) as a class of
   clinically informative exposures detectable *purely from mutation patterns* — exactly the
   kind of orthogonal, clinically actionable information an agnostic scan can surface without
   requiring prior annotation. The observation that signature-defined subgroups are
   *orthogonal* to clinical features (Secrier esophageal study) directly supports h08's
   premise: signatures carry information not captured by the structured clinical covariates
   already held in the pipeline.

3. **Known biomarker associations inform which clinical fields to prioritise in the agnostic
   scan:** HRDetect-predicted HR deficiency → treatment-response column; MSI/MMR gene status
   → MMR signatures; APOBEC-enriched cancers → stage/grade columns (if APOBEC is associated
   with high-risk translocations in myeloma, as the Walker 2015 reference suggests). These
   provide within-tissue covariate expectations that FDR-corrected H08 associations should
   match.

The review also foregrounds the *interpretive hazard* of reverse causation: expression of ATR,
WRN, or PARP is likely *downstream* of the repair-pathway loss causing the signature, not
upstream. This aligns with the h08 reverse-causation guard (R2 alternative explanation in the
hypothesis spec) — expression↔signature concordance is a hypothesis, not a causal arrow.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| COSMIC SNV/indel/SV signatures | Signature exposures (H columns of NMF) | Pipeline uses SigProfiler COSMIC reference |
| HRDetect / CHORD classifier | Derived binary annotation column | Not currently in pipeline; would require WGS |
| MMR deficiency (SBS6/15/26/44) | `is_hypermutator` + `hypermutator_reason: msi_h` | MSI-H ingest via `msi_normalization.py` |
| Therapy-induced signatures (SBS87, SBS11) | Relapsed-sample strata (not currently separated) | Pipeline does not yet partition by treatment history |
| cfDNA / mutREAD signature detection | Out-of-scope; pipeline uses bulk tumour WES/WGS data | Future direction |
| Drug-sensitivity correlations (Levatić) | Potential external annotation for H08b hits | No current drug-response column in pipeline |

## Limitations

- Review does not cover de-novo extraction methodology in detail; biases from NMF initialisation
  or signature number selection are not discussed, which is a gap for h08 implementation
  planning.
- All therapy-sensitivity examples are largely correlative cell-line or retrospective-cohort
  data; only HRDetect for PARPi is at the clinical-trial-evidence stage. The review itself
  notes the need for prospective validation throughout.
- The review focusses on WGS-scale assays for most applications; the pipeline primarily holds
  WES and panel data. Panel adequacy for per-sample signature assignment is not addressed
  (this is the subject of q018).
- No systematic evaluation of cross-study heterogeneity in signature exposures — relevant for
  the cBioPortal meta-analysis context where study-level batch effects are a concern (h08 R4
  alternative explanation).
- Outstanding questions raised by the paper: (1) Can therapy-induced signatures be detected
  on-treatment via cfDNA for clinical guidance? (2) Why do only ~15% of thiopurine-treated
  ALL relapses acquire SBS87? (3) What are the mechanisms of cell-intrinsic signatures with
  potential therapeutic relevance (e.g., SBS18 / ROS in neuroblastoma)?

## Model / Tool Availability

No new tool released. Review references SigProfiler, SignatureAnalyzer, MutationalPatterns,
HRDetect, CHORD, and mutREAD — all previously published; see respective citations.

## Follow-up

- Brady et al. cite the Levatić (2021) systematic cell-line signature ↔ drug-response screen
  (bioRxiv doi 10.1101/2021.05.19.444811) — worth summarising as a methodological template for
  H08b discovery scan design.
- The Hoang et al. multiple myeloma SV+SNV prognostic scheme demonstrates joint multi-modal
  signature classification; relevant if the pipeline ever integrates SV-level data.
- The Secrier et al. esophageal classification (three signature subgroups orthogonal to
  clinical features) is a strong existence proof for h08's premise.
- See h08 spec for the connection to q018 (panel adequacy for per-sample refit) and q019
  (de-novo extraction on the aggregated cohort).
