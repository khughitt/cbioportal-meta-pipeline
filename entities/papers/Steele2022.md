---
type: paper
title: An overview of mutational and copy number signatures in human cancer
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Steele2022
ontology_terms:
- mutational signatures
- copy number signatures
- somatic mutation
- NMF
- homologous recombination deficiency
- chromothripsis
- cancer genomics
datasets: []
source_refs:
- cite:Steele2022
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
---

# An overview of mutational and copy number signatures in human cancer

- **Authors:** Christopher D Steele, Nischalan Pillay, Ludmik B Alexandrov
- **Year:** 2022
- **Journal:** Journal of Pathology (J Pathol), 257: 454–465
- **DOI/URL:** https://doi.org/10.1002/path.5912
- **BibTeX key:** Steele2022
- **Source:** PDF

## Key Contribution

An invited review from the Alexandrov lab that provides a dual overview: (1) a concise synthetic
survey of the well-established SBS/DBS/ID (small mutational event) signature framework, covering
biological underpinnings, computational extraction (NMF), and practical utilities in basic
science, treatment, and prevention; and (2) a deeper focus on the emerging field of copy number
(CN) signatures — their profiling technology, the competing feature-design philosophies
(mechanism-designed vs. mechanism-agnostic), published methods, biological associations, and
future directions toward event-level and combined CN+rearrangement signatures. The review
positions CN signatures as complementary to, and in some ways biologically richer than, small
mutational event signatures because CNAs are subject to strong positive/negative selection.

## Methods

This is an invited narrative review. Primary sources surveyed include:

- **SBS/DBS/ID landscape:** TCGA, ICGC, Alexandrov et al. [@Alexandrov2013Nature; @Alexandrov2020] flagship papers, NMF-based
  COSMIC catalogues, experimental in-vitro signature libraries.
- **CN profiling techniques:** karyotyping, CGH arrays, SNP arrays, WGS/WES-derived logR +
  B-allele frequency (BAF) copy-number profiles, allele-specific callers (ascatNGS, Sequenza,
  CHISEL).
- **CN signature methods surveyed:** Macintyre et al. 2018 (ovarian; designed, NMF, 7 sigs);
  Wang et al. 2021 (prostate; designed, NMF, 5 sigs); Maclachlan et al. 2021 (multiple myeloma;
  hybrid/HDP, 5 sigs); Steele et al. 2019 (USARCs; agnostic, NMF, 7 sigs); Steele et al. 2021
  (pan-cancer, 11 210 samples; agnostic, NMF, 21 sigs, SigProfiler).
- **Decomposition methods:** NMF, latent Dirichlet allocation, hierarchical Dirichlet processes,
  and SigProfiler as software.

No original data analysis is presented; all quantitative results cited are from the reviewed
primary literature.

## Key Findings

### Small mutational event signatures (SBS, DBS, ID)

- Mutational patterns arise from the superposition of all mutagenic processes active across a
  tumour's lifetime; NMF (and related methods) deconvolves them into individual signatures and
  per-sample exposures.
- Established aetiological links: UV → SBS7 (CC>TT at dipyrimidines, CPDs); tobacco smoking
  → SBS4 (C>A transversions); APOBEC3A/B deamination → SBS2/13; aflatoxin, aristolochic acid,
  colibactin (E. coli) as confirmed environmental carcinogens identified via signatures;
  mismatch repair deficiency (MSI) → SBS6/15/26; POLE/POLD1 exonuclease mutations → SBS10.
- Signatures serve as multi-tumour phenotypes for germline predisposition screening (NTHL1
  example) and as predictive biomarkers: BRCA1/2 HR-deficiency signatures predict PARP inhibitor
  and platinum response; APOBEC-signature presence predicts tamoxifen resistance; others indicate
  iatrogenic mutagenesis (temozolomide, azathioprine, platinum).

### Copy number (CN) signatures

- CN profiles are derived from a combination of logR (total CN) and BAF (allele-specific CN)
  across the genome — together termed the "CN profile." Shallow WGS and SNP arrays are practical
  input platforms; allele-specific resolution requires phased data.
- **Feature-design philosophies:**
  - *Mechanism-designed*: features encode biologically suspected CN-generating processes
    (chromothripsis breakpoints, segment counts, LOH, ploidy). Captures known processes reliably
    but rarely reveals new mechanisms.
  - *Mechanism-agnostic*: CN profiles are summarised by LOH status × total CN × segment size
    categories (a "CN summary vector"), then NMF-decomposed. Post-hoc linkage to biological
    processes via driver mutations, WGD status, or transcriptomic data. Can reveal novel processes
    but may not capture all known biology.
- **Pan-cancer CN signature catalogue:** 21 CN signatures from 11 210 cancers
  across multiple sequencing platforms. New signatures linked to HRD, extrachromosomal circular
  DNA, and haploidisation.
- **Genomic mapping of CN signatures** (post-hoc): signature attributions can be projected back
  onto individual genomic segments, revealing which chromosomal regions are shaped by which CN
  process. Illustrated with a dedifferentiated liposarcoma (DDLPS) case: MDM2 chr12 amplification
  linked to the chromothripsis-amplification signature (CN8).
- **Clinical utility:** CN signatures predict prognosis in ovarian cancer,
  prostate cancer, and multiple myeloma studies; HRD-associated CN
  signatures underpin genomic scar assays (myChoice CDx) for PARP inhibitor patient selection.
- **Selection bias caveat:** unlike SBS passenger mutations (largely neutral), CN changes are
  under strong positive/negative selection. This means CN signatures are not a purely unbiased
  window onto mutational processes — selection shapes the observable CN landscape.
- **Future directions:** combining CN and rearrangement data into joint "event-level" signatures;
  sub-clonal CN reconstruction to map events onto tumour evolutionary trees; moving from
  "end-state" to "event-level" CN signature interpretation.

## Relevance

### Connection to hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and

The review is directly background-constituting for **hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and (agnostic covariate↔signature-exposure
association)**:

- **Positive-control grounding:** The aetiological map this review synthesises — UV→SBS7,
  smoking→SBS4, APOBEC3→SBS2/13, MMR-loss→SBS6/15/26, POLE→SBS10 — is exactly the positive
  control panel that the hypothesis's pre-registration commits to recovering before trusting any novel
  associations. The review's authoritative summary (from the Alexandrov group) provides citation
  support for each anchor link.
- **NMF framework orientation:** The review clarifies the distinction between NMF-derived
  signature weights (W) and per-sample exposures (H); the hypothesis targets H as the outcome of a
  phenome-wide association against clinical/expression covariates.
- **CN signatures as a potential extension:** The discovery prong could, in principle, be
  extended to CN signature exposures as outcomes, providing an orthogonal mutation-mode view.
  The review identifies which CN signatures have known biological interpretations (HRD,
  chromothripsis, WGD) that could serve as positive controls analogous to the SBS positive-
  control suite.
- **Signature prediction of treatment response:** The review's treatment-stratification examples
  (PARP inhibitor, platinum, tamoxifen) are concrete precedents that clinical covariate→signature
  associations can have translational utility — motivation for the discovery arm.
- **Selection-pressure caveat for CN signatures:** The observation that CN landscapes are under
  positive/negative selection (unlike most SBS passengers) is relevant to R3 (selection/
  immunoediting on burden) in the hypothesis's alternative-explanations inventory: for CN signatures the
  selection confound is more severe than for SBS.

### Connection to the cbioportal cross-study meta-analysis

- The review's description of mechanism-agnostic CN signature extraction (LOH × CN × segment
  size features → NMF) parallels the pipeline's cross-study aggregation philosophy: agnostic
  feature construction followed by unsupervised decomposition.
- The emphasis on platform heterogeneity (WGS vs. WES vs. shallow WGS vs. SNP arrays) and
  allele-specific resolution requirements is a practical caution for any future plan to extend
  the pipeline to CN-level signatures: cBioPortal studies vary widely in available CN data
  granularity.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| SBS/DBS/ID mutational signatures | Signature exposures targeted by hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and | Positive-control aetiologies directly used |
| Per-sample signature exposure (H matrix) | hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and outcome variable | NMF H column = per-sample activity |
| CN summary vector (LOH × CN × segment size) | Potential future CN feature | Not in current pipeline scope |
| Mechanism-agnostic CN signature | Parallel to cross-study agnostic aggregation | Philosophy alignment |
| Positive/negative selection on CNAs | R3 alternative (selection on burden) | More severe for CN than SBS |
| HRD signatures (BRCA1/2) | Not explicitly in pipeline | Relevant to matched-normal study stratification |

## Limitations

- As a review, presents no new data; quantitative claims are sourced from primary literature and
  should be verified there.
- Coverage of CN signatures is weighted toward methods from the Steele/Alexandrov/Macintyre
  lineage; other CN approaches (e.g. GISTIC-based) are mentioned but not deeply compared.
- The review predates (by one year) the Steele et al. 2021 pan-cancer 21-signature CN catalogue
  full peer-reviewed publication, which was a preprint (bioRxiv 2021.2004.2030.441940) at time
  of writing — that catalogue is cited as "not peer reviewed." [UNVERIFIED: peer-review status
  as of current date.]
- The distinction between "end-state" and "event-level" CN signatures is raised as a conceptual
  direction but no implemented method is described.
- Selection pressure on CNAs is acknowledged but not quantitatively treated — the magnitude of
  the bias introduced into CN signature aetiological inference is unclear.

## Model / Tool Availability

- **SigProfiler** (Alexandrov lab): used for the cited pan-cancer CN signature extraction;
  software cited for decomposition.
- **myChoice CDx** (Myriad Genetics): commercial HRD assay incorporating CN-based genomic scars;
  mentioned as a clinical implementation.
- **ascatNGS, Sequenza, CHISEL, Control-FREEC, Favero et al. Sequenza R package:** CN calling
  tools cited; not released by this review.
- No new tools or datasets are released by this review itself.

## Follow-up

- The cited pan-cancer 21 CN signature preprint (bioRxiv 2021.2004.2030.441940, not peer reviewed at time of writing) —
  the pan-cancer 21 CN signature paper; check peer-review status and read for the full catalogue.
- The founding ovarian CN signature paper cited by this review is already a
  source in the current project's hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and framing.
- Degasperi et al. 2022 — already summarised as `paper:Degasperi2022`; complements this review
  with COSMIC v3.3 SBS/DBS/ID catalogue update.
- Alexandrov et al. [@Alexandrov2020] — primary citation for the pan-cancer SBS landscape; check
  that `paper:Alexandrov2020` summary covers the full PCAWG catalogue adequately for the hypothesis context.
- For a CN extension to the hypothesis: the multiple myeloma CN
  signatures using hierarchical Dirichlet processes — methodologically distinct from NMF.
