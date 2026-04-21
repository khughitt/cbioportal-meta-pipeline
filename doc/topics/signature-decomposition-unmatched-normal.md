---
id: "topic:signature-decomposition-unmatched-normal"
type: "topic"
title: "Cancer-specific vs tissue-specific mutational-signature decomposition in unmatched-normal study contexts"
status: "active"
ontology_terms:
  - mutational signatures
  - tissue-of-origin
  - tumor purity
  - somatic mutation
  - clonal hematopoiesis
datasets:
  - cBioPortal (~300 studies)
  - PCAWG
  - COSMIC v3.x
source_refs:
  - "cite:Alexandrov2020"
  - "cite:Li2021"
  - "cite:Xu2025"
  - "cite:Yaacov2023"
  - "cite:Yoshida2026"
  - "cite:Jin2024"
  - "cite:Degasperi2022"
  - "cite:Nguyen2022CUPLR"
related:
  - "topic:clonal-hematopoiesis-contamination"
  - "topic:mutation-rate-normalization"
  - "topic:pan-cancer-mutation-landscape"
  - "topic:tumor-mutational-burden"
  - "paper:Yaacov2023"
  - "paper:Li2021"
  - "paper:Xu2025"
  - "paper:Yoshida2026"
  - "question:q008-signature-decomposition-tissue-background-subtraction"
  - "question:q009-sbs1-lrr-bias-as-normal-contamination-flag"
  - "question:q010-cuplr-style-tof-classifier-for-suspect-normal-samples"
created: "2026-04-18"
updated: "2026-04-18"
---

# Cancer-specific vs tissue-specific mutational-signature decomposition in unmatched-normal study contexts

## Summary

When a cBioPortal somatic-mutation study lacks patient-matched germline sequencing, every sample in that study carries an unknown admixture of (a) true tumor somatic mutations, (b) germline variants that escaped panel-of-normals filtering, and (c) mutations that originated in normal tissue cells contaminating the biopsy. Standard COSMIC-signature decomposition applied to such data conflates all three layers, because the global COSMIC reference catalogue was largely derived from matched-normal-subtracted tumor whole-genome sequences. The practical consequence for this pipeline is that aggregated gene-level mutation frequencies in unmatched-normal studies may be inflated by background tissue-of-origin signatures (SBS1, SBS5, SBS18, SBS40), and standard decomposition tools will over-assign these clock-like signatures without flagging that the excess may come from normal-tissue admixture rather than from the tumor cells themselves.

This topic synthesizes: the state-of-the-art decomposition methods available, COSMIC signature provenance (which signatures are present in normal tissue and therefore liable to bleed into unmatched-normal tumor decompositions), known and suspected false-positive signals attributable to this confound, empirical correction strategies, replication-timing constraints, tissue-of-origin classifiers, and concrete proposed interventions for the cbioportal pipeline.

## Scope

This synthesis covers SBS (single-base substitution) signatures only. DBS and ID (indel) signatures exist but are downstream of SBS analysis and are not a primary source of the normal-tissue contamination problem being addressed here. CNV/mCA contamination is a related but separate concern tracked under `question:q002` and `question:q004`.

---

## Key Concepts

**Matched vs unmatched normal.** In matched-normal sequencing, the patient's own germline DNA (blood or saliva) is sequenced alongside the tumor; variants present in both are subtracted as germline. In unmatched-normal (also called tumor-only or panel-of-normals) workflows, germline subtraction uses a population database or a cohort-derived reference panel. Variants in the patient's normal cells that are not in the PoN database pass through as apparent somatic mutations.

**Tissue-of-origin background signatures.** Normal cells accumulate SBSs over a lifetime. The dominant signatures in morphologically normal tissue are SBS1 (clock-like, CpG deamination), SBS5 (clock-like, unknown mechanism), SBS18 (oxidative damage, universal), and to varying degrees SBS8 and SBS40. Exogenous exposures add tissue-specific signals (SBS4/tobacco in lung/liver, SBS22/aristolochic acid in liver, SBS88/colibactin in colon, SBS7a/b/UV in skin). When these normal cells are present in a tumor biopsy — as contaminating normal stroma, as admixed biopsy tissue, or because the PoN is imperfect — their signature contributions are indistinguishable from genuine tumor contributions at the 96-trinucleotide level.

**Signature decomposition.** Given a tumor's 96-trinucleotide mutation count vector, decomposition is the problem of expressing it as a weighted sum of reference signature vectors. This is a non-negative least-squares or probabilistic problem. The output (exposures) quantifies how many mutations are attributable to each signature. Decomposition is well-conditioned only when the reference set is restricted to signatures plausible for the cancer type — the COSMIC catalogue contains ~95 SBS signatures, most of which should be set to zero for any given tumor type.

**Per-tissue signature priors.** A well-formulated decomposition for an unmatched-normal study should constrain or down-weight the contribution of "universal normal-tissue" signatures to what is expected given the tissue type, rather than allowing them to absorb unlimited variance. This is the gap that most current tools do not fill.

---

## State of the Art: Decomposition Methods

### General-purpose refitting tools (reference catalogue)

**SigProfilerAssignment** (Díaz-Gay et al., Bioinformatics 2023; PMID 38096571) is the current Alexandrov-lab standard. It implements a forward stagewise selection algorithm and NNLS refitting against COSMIC v3.x SBS signatures, and is the first tool that also supports copy-number signatures and probabilistic per-mutation assignment. The tool accepts a "activities" constraint — the analyst can specify which signatures are admissible for a given cancer type (following COSMIC's per-cancer-type signature lists). It does not natively model a normal-tissue prior; the analyst must exclude or constrain normal-tissue signatures manually.

**MuSiCal** (Jin et al., Nature Genetics 2024; PMID 38361034) combines minimum-volume NMF for de novo discovery with hierarchical NNLS refitting for assignment. On the PCAWG cohort, MuSiCal resolves nine indel signatures absent from the prior catalogue and clarifies flat-signature ambiguities (particularly the SBS5/SBS40/SBS8 cluster). Benchmarking (Nat Commun 2024) shows MuSiCal performs best when per-sample mutation counts are high (>1000 mutations); for low-mutation-count samples (panel/WES, <1000 mutations) SigProfilerSingleSample performs better. MuSiCal has no built-in tissue-background correction.

**SigNet** (bioRxiv 2023) uses a neural network that learns the empirical prior distribution of signature co-occurrences from real tumor data, making it intrinsically aware that, for example, SBS4+SBS2+SBS13 co-occur in lung cancer more often than random. This learned prior helps avoid spurious single-signature assignments. However, SigNet's training data is matched-normal PCAWG, so its prior does not represent unmatched-normal study distributions.

**SigFormer** (bioRxiv 2026) is a set-conditioned transformer that applies cross-attention between the reference catalog and the sample profile. It outperforms MuSiCal on high-noise and overcomplete reference settings, which are exactly the conditions found in panel-sequenced unmatched-normal studies. Published too recently to be tested in this pipeline, but is architecturally the most appropriate for the use case.

**MutationalPatterns** (Blokzijl et al., Genome Medicine 2018 / updated 2022; PMID 35168570) is the main R/Bioconductor option. Version 3.x includes strict refitting that bootstraps signature uncertainty and incorporates SIGNAL tissue-specific signature matrices. The SIGNAL matrix (Degasperi et al., Nature Cancer 2020) is the closest existing resource to a tissue-of-origin prior — it provides tissue-stratified reference signature sets derived from COSMIC reference signatures, so that the refitting step only allows signatures documented in a given tissue. MutationalPatterns' `convert_to_ref_genome` pipeline can convert from tissue-specific SIGNAL assignments to pan-COSMIC reference assignments for cross-tissue comparison.

**deconstructSigs** (Rosenthal et al., Genome Biology 2016) is a legacy tool widely used in published cBioPortal studies. Benchmarking consistently places it in the lower half for accuracy, particularly for small mutation counts, because it uses a threshold-based rather than probabilistic approach. Outputs from cBioPortal studies that report deconstructSigs results should be interpreted cautiously.

**cancereffectsizeR / SIGNAL** (Cannataro et al., 2022): The `suggest_cosmic_signature_exclusions()` function in cancereffectsizeR implements COSMIC's Extended Data Figure 5 (Alexandrov 2020) per-cancer-type signature exclusion lists. It also allows treatment-associated signature exclusion for naive cohorts. This is the simplest available approach to restrict decomposition to plausible signatures.

### Normal-tissue-aware approaches

No currently published tool performs decomposition with an explicit tissue-of-origin background prior. The closest approaches are:

1. **SIGNAL tissue-stratified matrices** (in MutationalPatterns): restrict the allowed signature set to those observed in that tissue type, effectively setting a floor on how much variance can be absorbed by cancer-only signatures.

2. **Per-tissue reference cohort subtraction**: fit the normal-tissue spectrum first (using published data from Li 2021, Xu 2025, or Moore 2022), then decompose the residual tumor spectrum. This is a proposed but not yet standardized workflow.

3. **CUPLR / tissue-of-origin classifier signal consistency check**: flag samples whose global signature profile is more consistent with normal-tissue priors (SBS1+SBS5 dominant, no cancer-specific signatures) than with known cancer-type profiles. Samples flagging as "ambiguous" or "normal-like" should be investigated for tumor purity.

---

## COSMIC SBS Signatures: Normal-Tissue Provenance

The table below classifies COSMIC v3.x SBS signatures by whether they are documented in morphologically normal tissue. Evidence sources are Li 2021, Xu 2025, Yaacov 2023, and COSMIC signature pages.

### Group A: Ubiquitous in normal tissue (direct bleeding risk)

| Signature | Normal-tissue evidence | Etiology | Notes |
|---|---|---|---|
| SBS1 | All tissues (Li2021, Xu2025, Yaacov2023) | Clock-like CpG deamination | LRR-biased in normal but not cancer (Yaacov2023) — potentially a contamination fingerprint |
| SBS5 | All tissues (Li2021, Xu2025, Yaacov2023) | Clock-like, mechanism unknown | ERR-biased in both normal and cancer; less distinguishable |
| SBS18 | All 46 GTEx tissues (Xu2025) | Oxidative damage (C>A) | Most universal normal-tissue signature; always present |

### Group B: Present in normal tissue, exogenous/exposure-specific

| Signature | Normal-tissue evidence | Etiology | Tissue specificity |
|---|---|---|---|
| SBS4 | Lung, liver (Li2021, Yaacov2023) | Tobacco smoking (C>A at CpCpX) | LRR-only in lung (Yaacov2023) |
| SBS7a | Skin (Xu2025) | UV, C>T at TpC | Skin-restricted |
| SBS7b | Skin, keratinocytes (Xu2025, Yaacov2023) | UV, tandem CC>TT | ERR-biased; sun-exposed skin only |
| SBS22 | Liver, esophagus, duodenum, stomach (Li2021) | Aristolochic acid (A>T at ApTpX) | East Asian exposure; Eastern cohorts |
| SBS88 | Colorectal crypts (Yaacov2023) | Colibactin (E. coli pks+) | ERR-only; high in colon studies |

### Group C: Present in normal tissue (less certain / tissue-limited)

| Signature | Normal-tissue evidence | Etiology | Notes |
|---|---|---|---|
| SBS8 | Reported in kidney, breast normal tissue; also by Xu2025 | Unknown (late replication errors) | LRR-biased; unclear normal vs cancer split |
| SBS40 | Reported in normal tissue from several studies; related to SBS5 | Unknown | SBS40a/b split in COSMIC v3.3+; possibly endogenous replication |
| SBS9 | Blood/B-cells (Yaacov2023) | Polymerase eta error (AID) | Blood-specific; relevant to CH contamination |
| SBS84 | Bone marrow (Yaacov2023) | Activation-induced cytidine deaminase (AID) | Blood lineage only |

### Group D: Cancer-enriched or cancer-associated (low normal-tissue bleeding risk)

These are signatures primarily or exclusively observed in cancer and would not be expected to inflate apparent mutation rates from normal-tissue admixture:

- **SBS2, SBS13** (APOBEC): strongly cancer-enriched in breast, bladder, lung; present sporadically in normal tissue (Xu2025 shows rare events). A small APOBEC signal in cancer is likely genuine.
- **SBS3** (HR deficiency/BRCA1/2): cancer-specific; rare in normal tissue.
- **SBS6, SBS14, SBS15, SBS20, SBS21, SBS26** (MMR deficiency): cancer-specific; microsatellite-instable tumors only.
- **SBS10a, SBS10b** (POLE/POLD1): hypermutator; cancer-specific.
- **SBS17a, SBS17b** (5-FU): treatment-associated; unlikely in normal tissue.
- **SBS31, SBS35** (platinum chemotherapy): treatment-associated.
- **SBS44** (MMR + mismatch repair deficiency): cancer-specific.

### Summary for pipeline use

For any cBioPortal study where normal sequencing is unmatched, the decomposition output may overstate contributions from SBS1, SBS5, SBS18, SBS40, and tissue-relevant exogenous signatures (SBS4 in lung/liver, SBS22 in liver, SBS88 in colon) because these signals are present in both the tumor DNA and any admixed normal DNA. Signatures in Group D, particularly APOBEC (SBS2/SBS13) and MMR-deficiency, are less likely to be confounded.

---

## Known False-Positive Signals from Unmatched Normal Contamination

### 1. CH gene inflation in tumor-only panels (well-documented)

The best-documented case of unmatched-normal contamination in cancer cohorts is clonal hematopoiesis. Coombs et al. 2018 (CCR; PMID 29866652) and Ptashkin et al. 2018 (JAMA Oncology; PMID 29872864) both quantify this effect in MSK-IMPACT data: ~8% of apparent somatic variants in tumor-only MSK-IMPACT profiling derive from DNMT3A/TET2/ASXL1 CH clones in blood-sourced DNA used without matched normal subtraction. The contamination is asymmetric by gene: DNMT3A accounts for ~64% of CH misattributions. This is the pipeline's existing `ch_priority_gene` flag.

### 2. Normal-epithelial driver inflation (partially documented)

For solid tumors, the NOTCH1 inversion in esophageal tissue (see `question:q001`) is the clearest example: NOTCH1 mutations are present in ~60–70% of normal esophageal epithelial clones but ~15% of esophageal squamous cell carcinomas. In cBioPortal esophageal studies where biopsy dissection was incomplete, NOTCH1 apparent tumor frequency could be inflated by normal-clone contamination. A similar inversion exists for PIK3CA in endometrium (high in normal, present but not dominant in endometrial cancer) and for FGFR3 in bladder (lower in invasive cancer than in non-invasive papillary tumors and normal urothelium).

No published retraction or formal cautionary note specifically attributes a cBioPortal study's NOTCH1 frequency to normal contamination, but the mechanistic basis is established in primary literature (Martincorena et al. 2018, Nature; Yokoyama et al. 2019, Science).

### 3. Signature misattribution in tumor-only RNA-seq TMB estimates

Turcan et al. 2021 and related work on RNA-seq TMB without matched normal show that germline-origin C>T variants (especially at CpG sites, i.e., SBS1-like) inflate apparent TMB and SBS1 exposure unless explicitly filtered by population germline databases. This is not specific to cBioPortal but affects any study using tumor-only RNA-derived variants. The effect is expected to be larger for SBS1 than for any other signature because CpG C>T transitions are the single most common class of germline variation.

### 4. No known published retractions specifically attributable to normal-contamination signature artifact

A systematic search (as of April 2026) found no published retractions or formal corrections to cancer genomics papers attributed specifically to signature misdecomposition from unmatched-normal contamination. However, the methodological concern is widely acknowledged in the signature methods literature (see discussion in Alexandrov 2020 Supplementary and Jin 2024 MuSiCal paper). The absence of retractions likely reflects two realities: (a) the effect is quantitative and continuous rather than binary, making it hard to identify as a discrete error; (b) the field has largely moved toward using COSMIC per-cancer-type signature lists rather than unconstrained decomposition.

---

## Empirical Correction Strategies

### Strategy 1: Cancer-type signature restriction (current best practice)

Use `suggest_cosmic_signature_exclusions()` from cancereffectsizeR or the analogous per-cancer-type lists in MutationalPatterns/SIGNAL to restrict the active signature set to those documented for the cancer type. This is the minimal, immediately actionable step.

**Status:** Well-validated. Alexandrov 2020 (PCAWG) established the per-cancer-type expected signatures (Extended Data Figure 5). MuSiCal and SigProfilerAssignment both support this via a user-supplied allowed-signature list.

**Limitations:** Does not distinguish normal-tissue background from cancer contribution within an allowed signature. SBS1, SBS5, SBS18 are allowed for virtually every cancer type because they are genuinely present in both normal and tumor.

### Strategy 2: Per-tissue background subtraction

Fit the published normal-tissue trinucleotide spectrum for the relevant tissue (from Li 2021, Xu 2025, or Moore et al. 2022 pan-tissue WGS data) as a fixed offset before decomposing the residual cancer profile. Specifically:

1. Obtain the per-tissue average mutation spectrum for morphologically normal tissue (Li 2021 / Xu 2025 provide 96-trinucleotide spectra).
2. Scale the normal-tissue spectrum to the expected contamination fraction (estimated from tumor purity, if available, or treated as a hyperparameter).
3. Subtract the scaled spectrum from the tumor spectrum before running decomposition.

**Status:** Conceptually established but not yet a published, validated workflow. The scaling step requires either a tumor purity estimate or a prior on contamination fraction, which introduces its own uncertainty. For the cbioportal pipeline, where single-sample mutation counts are often low (panel/WES), the subtraction error could exceed the signal.

**Practical feasibility for pipeline:** Medium. Requires obtaining per-tissue reference spectra from a source like Li 2021 supplemental tables or Xu 2025 / Moore 2022. The reference spectra exist; the pipeline engineering is tractable (a new Snakemake rule taking the sample's cancer type → look up tissue reference spectrum → subtract → decompose residual).

### Strategy 3: SBS1 LRR-bias as a normal-contamination indicator

Yaacov et al. 2023 showed that SBS1 carries a late-replicating-region (LRR) enrichment bias in normal tissue but loses this bias in cancer. If per-sample replication-timing-stratified SBS1 counts are available (e.g., via SigProfilerTopography), comparing the LRR vs ERR distribution of SBS1 mutations can flag samples where SBS1 is behaving like a normal-tissue signal rather than a cancer signal.

**Status:** Conceptually validated in Yaacov 2023 but not yet operationalized as a contamination filter. Requires whole-genome sequencing data for the topography analysis; not applicable to panel/WES data. Not directly usable in the current cbioportal pipeline without WGS inputs.

**Practical feasibility for pipeline:** Low for current panel/WES inputs. Applicable in the future if WGS-based studies are added.

### Strategy 4: Tumor purity-aware decomposition

Several tools (PureCN, ABSOLUTE, Sequenza) estimate tumor purity and ploidy from panel or WES data. The purity estimate defines the expected normal-cell fraction contributing mutations to the observed profile. If tumor purity is 70%, then approximately 30% of the observed mutations come from normal cells (assuming the normal-cell contribution is dominated by low-VAF mosaic variants).

Integrating purity estimates into signature decomposition is conceptually straightforward: the normal-cell fraction's signature is expected to be dominated by SBS1/SBS5/SBS18; the tumor fraction carries the cancer-type-specific signatures. The sum of expected contributions, weighted by purity, should match the observed profile.

**Status:** Partially operationalized — PureCN produces purity-corrected VAF profiles, and SigProfilerAssignment can take purity-corrected mutation counts as input. A full integrated pipeline (purity → purity-weighted decomposition → tissue-background attribution) is not yet published as a standard workflow.

**Practical feasibility for pipeline:** Medium-high if tumor purity metadata is available (cBioPortal clinical data sometimes includes ABSOLUTE-derived purity). Adding a purity covariate to existing per-study decomposition is tractable.

### Strategy 5: Cohort-level reference-based decomposition

Rather than decomposing each sample independently, fit signatures across the entire cohort of a given cancer type simultaneously (the original Alexandrov NMF approach). Cohort-level fitting naturally identifies signatures common across samples (the tumor-type signature) vs individual-sample noise. The SBS1/SBS5 excess from normal contamination will vary across samples according to their tumor purity; treating exposure across the cohort as a mixture model allows estimating both the shared cancer component and the per-sample normal-tissue component.

This is essentially what PCAWG did: extract signatures jointly from hundreds of matched-normal whole genomes per cancer type, then assign back to samples. The problem for cBioPortal is that each study is typically analyzed in isolation, and per-study sample sizes are too small for stable de novo NMF extraction.

**Status:** Standard for large matched-normal WGS cohorts; not standard for small unmatched panel/WES cohorts. Aggregating across multiple cBioPortal studies for the same cancer type before decomposition (effectively what this pipeline's cross-study gene×cancer table does for frequencies) is a partial analog.

---

## Replication-Timing Structure as a Decomposition Constraint

From Yaacov et al. 2023 (see `paper:Yaacov2023`):

- **SBS1** is LRR-enriched in normal tissue but this bias is lost in cancer. This is the strongest published topographic fingerprint distinguishing normal-tissue from cancer-origin SBS1.
- **SBS5** is ERR-enriched in both normal and cancer — no distinguishing topographic signal.
- **SBS18** is LRR-enriched in normal tissues (consistent with its C>A oxidative damage enrichment in heterochromatic regions).
- **SBS4** is LRR-only in normal lung and liver.
- **SBS88** is ERR-only in normal colon.

These topographic constraints are directly usable for contamination diagnosis when WGS data are available. For panel/WES studies (the majority of cBioPortal), the constraints are not directly applicable because only a fraction of the genome is covered and per-gene replication-timing annotations would need to be used as a proxy.

The most actionable implication: an cBioPortal study showing high SBS1 exposure relative to SBS5 exposure — particularly in a tissue where SBS5 normally dominates (bronchial, liver) — may have excess normal-cell contamination driving SBS1 upward. This is an indirect signal, not a definitive test, but it is computable from existing pipeline outputs.

---

## Tissue-of-Origin Classifiers and Their Repurposing Potential

Tissue-of-origin (TOO) classifiers for cancers of unknown primary (CUP) are trained on the same features that distinguish normal-tissue-background signatures from cancer-type-specific signatures.

**CUPLR** (Nguyen, Van Hoeck, Cuppen; Nature Communications 2022; PMID 35817764) classifies 35 cancer subtypes with ~90% precision/recall from 511 features derived from WGS-level mutation patterns, including SBS signatures, relative mutation density (RMD), structural variant type, and driver mutation presence. The RMD feature (the per-megabase mutation density in 1 Mb bins, correlated with chromatin state and replication timing) is especially tissue-discriminative and is largely independent of specific cancer drivers.

The potential repurposing for this pipeline: a sample whose signature profile and RMD pattern are more consistent with normal-tissue background (i.e., CUPLR assigns it confidently as the expected tissue type but at a lower confidence than typical matched-normal cases, or assigns it as ambiguous) is a candidate for manual purity inspection. No published study has used CUPLR (or similar classifiers) explicitly to flag abnormal normal-tissue contamination in an existing cohort, but the conceptual path is clear.

**Important limitation:** CUPLR requires WGS-level mutation counts for reliable RMD features. For panel/WES-based cBioPortal studies, CUPLR cannot be directly applied. Signature-only classifiers (using SBS profiles alone) lose the RMD component and have lower discriminative power.

A practical alternative: compute the cosine similarity of each sample's 96-trinucleotide profile against the published normal-tissue reference spectrum for its cancer type's tissue of origin (from Li 2021 / Xu 2025). Samples with high cosine similarity to normal-tissue spectrum are candidates for purity review. This is a simple, implementable heuristic.

---

## Relevance to the cbioportal Pipeline

The pipeline aggregates mutation calls from ~300 studies, many using tumor-only or PoN-based germline filtering. The downstream consequence at the gene×cancer table level is:

1. **Systematic inflation of SBS1/SBS5-attributed mutations per study** when normal cells contaminate the input. Because SBS1/SBS5 are clock-like and drive aging-associated mutation rates, older patient cohorts will show higher background even in matched-normal studies — but in unmatched-normal studies, the background is additive: tumor aging signal + normal-cell aging signal from contaminating normal cells.

2. **Per-gene false elevation of mutation frequencies** for genes that are (a) in late-replicating regions (biased toward SBS1/SBS18) and/or (b) the targets of normal-tissue positive selection (NOTCH1, TP53, ARID1A, CH genes). The `ch_priority_gene` flag addresses category (b) for blood-lineage genes; there is no analogous flag for solid-tissue drivers.

3. **Signature composition of per-study outputs will be biased** toward universal normal-tissue signatures in low-purity or biopsy-based studies. Per-study signature comparisons (e.g., comparing lung LUAD vs LUSC studies) could conflate biological signature differences with study-specific purity/contamination differences.

4. **The `matched_normal_studies` config list is the primary existing mitigation**, routing matched-normal studies to the `mean_matched` path in `annotate_ch.py`. Expanding this list and adding a parallel "tissue-background-risk" annotation would address the broader solid-tumor contamination problem.

---

## Proposed Interventions for the cbioportal Pipeline

### Intervention 1: Cancer-type signature restriction for per-study decomposition

**Action:** When signature decomposition is added as a pipeline step, use SigProfilerAssignment or MutationalPatterns with cancer-type-specific signature exclusion lists (COSMIC Extended Data Figure 5 / Alexandrov 2020). At a minimum, exclude signatures with no documented occurrence in the cancer type being analyzed.

**Feasibility:** High. The exclusion lists are published and static. A lookup table (cancer_type → allowed_sbs_signatures) can be constructed from COSMIC documentation and stored in `data/`.

**Expected impact:** Prevents spurious high-activity assignments to cancer-type-implausible signatures. Does not directly address the SBS1/SBS5/SBS18 contamination problem (these are allowed in every cancer type), but eliminates other noise.

**Caveat:** Requires a study-to-cancer-type mapping that is often incomplete in cBioPortal metadata.

### Intervention 2: SBS1/SBS5 ratio as a per-study contamination proxy flag

**Action:** Compute the ratio of SBS1 to SBS5 exposures per study (using the decomposition outputs). Tissue types where SBS5 normally dominates (lung, liver, esophagus; see Li 2021) should show SBS5 > SBS1 in clean matched-normal tumor data. Studies where SBS1 > SBS5 in a tissue that should be SBS5-dominant are flagged for purity inspection.

**Feasibility:** Medium. Requires running signature decomposition first, then a simple comparison step. Reference values (expected SBS1/SBS5 ratios per tissue type) can be derived from Li 2021 normal-tissue data or PCAWG per-cancer-type signature catalogs.

**Expected impact:** A qualitative flag, not a correction. Surfaces studies with plausible contamination for downstream review. Does not require WGS data.

**Caveat:** SBS1/SBS5 ratio is not a clean contamination indicator — it also varies with patient age and cancer type biology. Confounded by cohort age distribution.

### Intervention 3: Per-tissue normal-spectrum cosine similarity screen

**Action:** For each study in the pipeline, compute the cosine similarity of the per-study aggregate 96-trinucleotide profile against two reference profiles: (a) the matched-cancer-type PCAWG reference spectrum and (b) the matched-normal-tissue spectrum (from Li 2021 / Xu 2025 or Moore 2022 per-tissue reference). Studies where the cosine similarity to the normal-tissue reference exceeds the similarity to the cancer-type reference are flagged as potential contamination outliers.

**Feasibility:** Medium. Per-tissue reference spectra are available from Li 2021 supplemental tables and Xu 2025. Computing cosine similarity per study from the pipeline's existing per-study mutation call files is a straightforward Python step.

**Expected impact:** Identifies studies with unusually normal-like profiles for manual review. Useful as a quality-control flag at the study-selection level before inclusion in the aggregated `gene_cancer_study.feather`.

### Intervention 4: Extend `ch_priority_gene` logic to solid-tissue driver contamination

**Action:** Create a `normal_epithelial_risk_gene` annotation analogous to `ch_priority_gene`, populated from the Li 2021 32-gene normal-tissue driver list and the NOTCH1/TP53/PIK3CA/ARID1A solid-tissue inversion evidence. For each gene in this list, annotate which tissue types carry the risk (e.g., NOTCH1 risk in esophageal and bronchial studies; PIK3CA risk in endometrial studies).

**Feasibility:** Medium. The gene-tissue risk mapping can be constructed manually from published data (Li 2021 supplemental, Martincorena 2018 esophageal data, Yokoyama 2019). Annotating the `gene_cancer_study_annotated.feather` with this flag requires a new column and a new script analogous to `annotate_ch.py`.

**Expected impact:** Surfaces the most likely false-positive driver hits in biopsy-based or low-purity studies. Highest priority: NOTCH1 in ESCA studies.

**Caveat:** The Li 2021 list is from a very small cohort (5 donors, Eastern Asian). Confidence in gene-tissue risk assignments is moderate for major drivers (NOTCH1, TP53), lower for secondary genes. Track as `question:q008`.

### Intervention 5: Per-study tumor-purity covariate import

**Action:** Import tumor purity estimates from cBioPortal clinical data files where available (ABSOLUTE or FACETS purity columns), and attach them as a per-study covariate in the pipeline's metadata tables. Use purity as a continuous covariate in downstream association analysis to control for normal-tissue admixture.

**Feasibility:** Medium-high. Tumor purity data is present in cBioPortal clinical files for some studies (particularly TCGA studies run with ABSOLUTE). Importing it requires extending the `convert_to_feather.py` logic to parse clinical files.

**Expected impact:** Enables purity-stratified analysis of mutation frequency tables. Studies with purity < 0.5 should be interpretable with explicit caveats. Highest-value for esophageal, breast, and lung biopsy-based cohorts.

---

## Controversies and Open Questions

1. **How large is the contamination effect quantitatively?** The CH literature documents a few percent false-positive rate for specific genes (DNMT3A ~64% of CH misattributions, ~8% overall variant-level rate). For solid-tissue normal-clone contamination, no analogous quantification exists at the study-aggregate level. It is plausible the effect is smaller (normal epithelial clone VAF is lower than CH clone VAF) but this is unverified.

2. **Does the SBS1 LRR loss in cancer (Yaacov 2023) hold at the low mutation counts typical of panel/WES studies?** The finding is based on WGS data with thousands of mutations per sample. At panel-level mutation counts (tens to hundreds per sample), the test has insufficient power. This limits the direct applicability of the topographic contamination indicator.

3. **Is the SIGNAL tissue-stratified signature matrix (used by MutationalPatterns) an adequate proxy for per-tissue background?** SIGNAL was constructed from cancer tissue signature profiles, not normal-tissue profiles. It stratifies signatures by tissue of origin but does not model the normal-cell contribution within a tumor biopsy. Whether SIGNAL's tissue specificity is sufficient to address unmatched-normal contamination is unclear.

4. **Do cohort-level decompositions (across all samples from the same cancer type) perform better than per-sample decompositions for contamination robustness?** Theoretically yes — the shared cancer-type signature is more stable, and per-sample noise including normal-tissue contamination averages out. But combining samples across studies introduces inter-study batch effects. The cbioportal pipeline's cross-study aggregation is implicitly a cohort-level operation, so this question bears on how to extend the pipeline to signature-level analysis.

5. **For the SBS1/SBS5 ratio diagnostic (Intervention 2 above), what is the per-tissue-type expected ratio in matched-normal-subtracted cancer data?** This reference value is needed to calibrate the flag. It can be obtained from PCAWG per-cancer-type signature catalogs but has not been systematically derived for the cancer types in cBioPortal's study collection.

---

## Links to Existing Questions

- `question:q001`: NOTCH1 inflation in esophageal studies — direct application of normal-epithelial contamination in a specific tissue. The signature-decomposition framing adds the mechanistic layer: NOTCH1-mutant normal esophageal clones will carry SBS1/SBS5-dominated spectra; their contribution will inflate the SBS1 exposure of the affected study.
- `question:q003`: Replication-timing as a gene-level mutation-rate confounder — directly relevant to interpreting LRR/ERR-differential signatures in cancer vs normal.
- `question:q007`: Can normal-tissue mutation rates serve as a null model? — intersects with Intervention 3 (per-tissue cosine similarity screen) and the need for reference spectra.

New questions filed:
- `question:q008`: See `doc/questions/q008-signature-decomposition-tissue-background-subtraction.md`
- `question:q009`: See `doc/questions/q009-sbs1-lrr-bias-as-normal-contamination-flag.md`
- `question:q010`: See `doc/questions/q010-cuplr-style-tof-classifier-for-suspect-normal-samples.md`

---

## Key References

Full BibTeX entries are in `papers/references.bib`. Key entries for this topic:

- **Alexandrov2020** — PCAWG COSMIC v3 signature catalogue; per-cancer-type expected signatures (Extended Data Figure 5).
- **Jin2024** — MuSiCal; minimum-volume NMF + NNLS refitting; resolves flat-signature ambiguities.
- **Degasperi2022** — Signal/SIGNAL tissue-stratified signature framework (MutationalPatterns integration).
- **Yaacov2023** — SBS1 LRR bias lost in cancer; topographic normal-tissue fingerprint.
- **Li2021** — Body map; 7 normal-tissue signatures; per-tissue burdens as reference spectra.
- **Xu2025** — GTEx pan-tissue exome; SBS18 universal; per-tissue coding-mutation spectra.
- **Nguyen2022CUPLR** — CUPLR tissue-of-origin classifier; RMD + SBS features; 35 cancer subtypes.
- **DíazGay2023** — SigProfilerAssignment; per-mutation probabilistic assignment; CN signatures.

---

## Follow-up Reading Queue

Papers worth queuing for `/science:research-papers` full summarization:

1. **Jin et al. 2024** (MuSiCal, Nature Genetics, PMID 38361034) — The state-of-the-art decomposition tool; needs full summary to identify how to configure it for per-cancer-type constraints and whether it has any tissue-background options. Direct pipeline tooling relevance.

2. **Degasperi et al. 2020** (Signal/SIGNAL practical framework, Nature Cancer, PMID 32908195) — Introduces tissue-stratified signature matrices; directly relevant to implementing Intervention 1. MutationalPatterns incorporates SIGNAL; a full summary would clarify how the tissue stratification works and whether it covers the normal-tissue contamination use case.

3. **Nguyen, Van Hoeck, Cuppen 2022** (CUPLR, Nature Communications, PMID 35817764) — TOO classifier based on WGS features including RMD and SBS. Summary needed to assess whether the approach can be adapted for panel/WES studies or whether a simpler cosine-similarity heuristic is more appropriate.

4. **Diaz-Gay et al. 2023** (SigProfilerAssignment, Bioinformatics, PMID 38096571) — Current Alexandrov-lab assignment tool; pipeline integration candidate. A summary would clarify the allowed-signature input interface and performance on WES/panel data.

5. **Moore et al. 2022** (Pan-tissue WGS normal-cell reference spectra, referenced in Yaacov2023 as one of the two normal-tissue cohorts) — Provides the large-N per-tissue normal-cell mutation spectra that could serve as background reference. Needed if Intervention 3 is implemented.
