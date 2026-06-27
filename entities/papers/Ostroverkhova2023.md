---
type: paper
title: 'Cancer driver mutations: predictions and reality'
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Ostroverkhova2023
ontology_terms: []
datasets: []
source_refs:
- cite:Ostroverkhova2023
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
---

# Cancer driver mutations: predictions and reality

- **Authors:** Daria Ostroverkhova, Teresa M. Przytycka, Anna R. Panchenko
- **Year:** 2023
- **Journal:** Trends in Molecular Medicine, Vol. 29, No. 7, pp. 554–566
- **DOI/URL:** https://doi.org/10.1016/j.molmed.2023.03.007
- **BibTeX key:** Ostroverkhova2023
- **Source:** PDF

## Key Contribution

This review systematically surveys computational methods for identifying cancer driver mutations,
distinguishing four major families — (i) mutation-occurrence statistics / probabilistic
background models, (ii) functional-impact decoders, (iii) supervised machine-learning classifiers,
and (iv) mutational-process / signature-based approaches — and critically evaluates their
performance and limitations against experimental ground-truth. A central finding is that the
field lacks an objective gold-standard benchmark, because most supervised methods actually learn
to distinguish driver *genes* from non-driver genes rather than driver *variants* from passenger
variants, inflating apparent accuracy by ~28 pp when negative (passenger) examples are omitted
from driver-gene contexts. The review also documents how mutational signatures are exploited
both to model the background mutation rate (enabling better driver detection) and as direct
clinical biomarkers predicting drug sensitivity and immunotherapy response.

## Methods

Narrative review drawing on primary literature; no new dataset or computational experiment is
presented. Coverage spans:

- **Background mutation rate modelling:** dN/dS, heptanucleotide context models, epigenomic
  covariates (replication timing, chromatin accessibility, histone marks) explaining up to 86%
  of megabase-scale mutation rate variance.
- **Mutational signature frameworks:** NMF-based de-novo extraction (COSMIC SBS catalogue) and
  motif-based approaches; signature-exposure inference methods (SigProfiler, sigLASSO,
  MutationalPatterns).
- **Driver prediction methods surveyed:** MutaGene, PROVEAN, PrimateAI, DEOGEN2, CHASM/
  CHASMPlus, CADD, CanDrA, DEOGEN2, Dig, CTAT-cancer, TVA, and others.
- **Experimental validation datasets:** xenograft formation, drug sensitivity assays, base-editor
  proliferation screens (Ba/F3 and MCF10A cells, 1049 mutations in two growth factor-dependent
  lines).
- **Comparative benchmarks:** MCC-based evaluation across CHASMplus, MutaGene, and CanDrAplus
  (MCC = 0.64, 0.61, 0.58 respectively); PROVEAN best by in vivo AUC (0.72).

## Key Findings

1. **Driver counts per tumour are low and cancer-type-specific.** Bladder, endometrial, and
   colorectal cancers average ~4 driver mutations per patient; sarcomas, thyroid, and testicular
   cancers average ~1. Early clonal drivers cluster in just nine genes; subclonal drivers are
   spread across 35 genes.

2. **Mutational signatures link mutagenic processes to specific driver hotspots.** Established
   examples reviewed: KRAS G12C (CCA>CAA) linked to smoking-related signatures in lung
   adenocarcinoma; TP53 R249S (GCC>GAC) linked to aflatoxin; BRAF V600E in melanoma linked to
   UV (SBS7); PIK3CA hotspot driven by APOBEC across many cancers; POLE/POLD1 mutations
   generate a distinct ultra-mutator signature (SBS10). Bidirectionality is stressed — driver
   mutations can *cause* signature shifts, and mutagenic processes *cause* specific driver
   hotspots.

3. **Probabilistic background-rate methods are robust but imprecise at single-nucleotide scale.**
   Epigenomic-covariate models correct most megabase-scale variation; residual single-nucleotide
   variation is captured by heptanucleotide context (explains ~80%). Hotspot mutations at highly
   mutable sites can still be neutral, requiring additional confounding checks.

4. **Supervised ML methods suffer from training-set design flaws and overfitting.** The most
   common flaw: methods classify driver *genes* vs. non-driver genes rather than driver
   *variants* vs. passengers, producing inflated performance metrics (~28 pp drop when
   corrected). Negative examples (passengers) are inconsistently defined (SNPs, germline
   deleterious variants, or random sampling), making cross-method comparison unreliable.
   Deep-learning models (CNN, Dig) show promise but require large, unbiased labelled sets that
   do not yet exist for cancer drivers.

5. **Mutational signatures as clinical biomarkers.** APOBEC signatures (SBS2/SBS13) are
   predictive of immunotherapy response in multiple cancers, partly via high TMB and partly via
   APOBEC3B upregulation. HRD-associated signatures (SBS3) guide PARP inhibitor use (synthetic
   lethality). POLE deficiency (SBS10) predicts immunotherapy sensitivity and is now used in
   pretreatment triage. H3K27M mutations in histone `H3` define a WHO tumour category (diffuse
   midline glioma) with OS < 1 year vs. >4 years for wild-type.

6. **Liquid biopsy (ctDNA) extends biomarker reach.** CancerSEEK achieved 70% correct detection
   across 8 cancer types; EGFR-sensitising mutations detected in 11% of a TARGET cohort from
   blood. False positives from clonal haematopoiesis remain a key limitation; computational
   approaches to distinguish somatic CH mutations from tumour-derived mutations are emerging.

7. **Lack of gold-standard benchmark is the central bottleneck.** Databases (ClinVar, OncoKB)
   mix experimentally validated and computationally predicted variants, risking circularity in
   method evaluation. Cancer- and patient-specific predictions lag behind general pathogenicity
   predictors.

## Relevance

**hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and (agnostic covariate–signature-exposure association; positive-control recovery of
UV/smoking/APOBEC/MMR):**

- Section "Driver mutations and mutational signatures" + Box 1 directly enumerate the canonical
  exposure→driver-hotspot links that form the positive-control arm:
  UV→SBS7→BRAF V600E (melanoma), smoking→SBS4→KRAS G12C (lung), APOBEC→PIK3CA hotspot (pan-cancer),
  POLE→SBS10 (ultra-mutator), aflatoxin→TP53 R249S. These pairings are textbook confirmations
  that the hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and agnostic scan should recover unprompted.
- The paper emphasises that the signature–driver relationship is **bidirectional**: signatures
  cause specific driver hotspots *and* driver mutations alter the signature landscape. This
  bidirectionality is precisely the reverse-causation concern flagged in the hypothesis's alternative
  explanation R2. The review provides no resolution strategy beyond noting the conceptual
  complexity — mediation logic (as stipulated in the hypothesis) is the appropriate guard.
- The APOBEC3B upregulation → APOBEC signatures (SBS2/13) link explicitly validates the hypothesis's
  Prediction 2: *APOBEC3A/B expression* should be the strongest correlate of SBS2/13, outranking
  clinical labels.
- The clinical-biomarker section establishes that signature exposures are already
  well-powered enough to separate patient groups (immunotherapy responders, HRD patients) —
  supporting the hypothesis that within-tissue association of signature exposures against
  clinical and expression covariates is feasible on cBioPortal/MC3 sample sizes.

**Cross-study mutation meta-analysis:**
- The background-mutability section (epigenomic covariates, heptanucleotide context) is relevant
  to understanding why cross-study pooling of per-gene mutation counts needs TMB and hypermutator
  filters — high background mutability mimics positive selection and inflates apparent driver
  frequency. The pipeline's existing `_inclusive`/`_exclusive` columns and the hypermutator
  annotation pipeline address exactly this concern.
- Driver counts per cancer type (Figure 1C in paper) provide external calibration for the
  pipeline's gene×cancer frequency tables: cancer types with ~1 driver (sarcoma) vs. ~4
  (endometrial) differ in how many rows of the frequency table should carry high signal vs. noise.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Mutational signatures (COSMIC SBS) | `topic:signature-decomposition-unmatched-normal`; hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and exposure matrix H | Paper reviews NMF/COSMIC approach used in cBioPortal studies |
| Background mutation rate / mutability model | Hypermutator annotation pipeline; TMB denominators | The paper's probabilistic methods are conceptually equivalent to the pipeline's hypermutator score |
| Driver vs. passenger mutation | `bailey2018_driver` flag; annotate_drivers.py overlay | Bailey et al. [@Bailey2018] is the pipeline's canonical driver list |
| Signature-linked driver hotspots (Box 1) | Positive-control set (UV→SBS7, smoking→SBS4, APOBEC→SBS2/13, POLE→SBS10) | Direct mapping; these hotspots are the hypothesis's ground truth |
| ctDNA / liquid biopsy | Out of scope for current pipeline | Flagged as future avenue in the review |
| Clonal haematopoiesis contamination | `ch_priority_gene` flag; Bolton et al. [@Bolton2020] list; `annotate_ch.py` | The pipeline's CH-aware annotation directly addresses the ctDNA false-positive problem |

## Limitations

- As a review, the paper presents no new data; all performance numbers are drawn from cited
  primary studies and may not transfer to cBioPortal's study mix (panel vs. WES, varied tumour
  purities, no matched-normal for many studies).
- The "benchmark" section covers only a limited subset of driver prediction tools; newer
  methods published after mid-2022 are not included.
- The gold-standard problem the paper identifies (Section "Constructing experimental datasets")
  applies equally to the cBioPortal pipeline: our annotation relies on Bailey et al. [@Bailey2018] (a
  consensus-based, not purely experimental, list) and COSMIC reference signatures — both
  acknowledged as imperfect benchmarks in this review.
- Liquid-biopsy / ctDNA discussion is surface-level for our purposes; primary ctDNA literature
  should be consulted for any pipeline extension.
- The review focuses almost entirely on single-nucleotide substitutions; structural variants,
  indels, and copy-number drivers receive minimal coverage.

## Model / Tool Availability

This is a review; no new tool is released. Tools surveyed and cited that are relevant to the
pipeline:

- **MutaGene** (NCBI): probabilistic driver scoring using context-corrected background models.
- **PROVEAN / PrimateAI / DEOGEN2 / CHASMPlus / CADD / CanDrA:** variant-effect predictors
  benchmarked in the paper; none are currently used by the cBioPortal pipeline.
- **Dig:** combines kilobase- and single-nucleotide-scale background modelling (positive
  selection scan); open-source.
- **CTAT-cancer / TVA / MutaGene:** pan-cancer integrative driver predictors.

## Follow-up

- **Immediate:** Box 1 and the signature-driver section provide a compact literature basis for
  the hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and positive-control pre-registration (already committed 2026-05-30). No new reading
  is required on the positive-control set from this review alone.
- **Questions raised:**
  - The paper notes that dN/dS estimation is confounded by multiple gene copies and recessive
    deleterious mutations (citing a paper in this review's reference list). Does our pipeline's use of per-sample allele
    frequency implicitly inherit this bias?
  - The benchmark failure mode (learning gene-level rather than variant-level discrimination,
    ~28 pp inflation) is directly relevant to any future attempt to score individual variants in
    our frequency tables. Worth pre-registering the distinction before building such a layer.
  - APOBEC3B upregulation as a predictor of immunotherapy response (refs 98–99 in paper):
    since the pipeline has expression data for some studies, testing APOBEC3A/B expression vs.
    SBS2/13 exposure would be a concrete hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and positive-control experiment.
- **Papers to read next (from this review's reference list):**
  - Robinson et al. 2019 (ref 28) — clinical/molecular covariates of mutational process activity
    (direct hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and precedent — a PheWAS-style association of covariates with signature exposures).
  - Brown et al. 2019 (ref 12) — background mutability and driver identification in cancer;
    dN/dS role of background processes.
  - Landrum et al. 2022 (ref 108) — current driver mutation predictors learn driver genes not
    functional variants; the 28 pp drop finding.
  - Choi et al. 2012 (ref 86) — PROVEAN; best AUC comparator in the review.
