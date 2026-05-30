---
id: paper:ChakravartySolit2021
type: paper
title: Clinical cancer genomic profiling
status: abstract-read
ontology_terms: []
source_refs:
- article:ChakravartySolit2021
related:
- paper:Zehir2017
- paper:AACRGENIEConsortium2017
- paper:Pugh2022
- topic:targeted-panel-sequencing-bias
- topic:cohort-selection-bias-representativeness
created: '2026-04-13'
updated: '2026-04-13'
---

# Clinical cancer genomic profiling

- **Authors:** Chakravarty D, Solit DB
- **Year:** 2021
- **Journal:** Nature Reviews Genetics (22:483–501)
- **PMID:** 33762738
- **DOI:** 10.1038/s41576-021-00338-8
- **BibTeX key:** ChakravartySolit2021

## Key Contribution

A Nature Reviews Genetics synthesis framing clinical tumour genomic profiling as a
mature, multi-platform methodology class rather than a single assay. Chakravarty
and Solit (both MSK / OncoKB) argue that the next phase of clinical utility hinges
on integrating tumour with germline calling, interpreting allelic/zygosity context,
and moving beyond simple variant lists to mutational-signature- and cfDNA-based
readouts. <!-- UNVERIFIED: framing inferred from abstract; full-text confirmation
of the "methodology class" framing not obtained -->

## Methods

Narrative review (not systematic). Full-text access was paywalled; this summary is
built from the published abstract plus the review's advertised scope.

Scope as declared in the abstract:

- Routine-care tumour profiling panels covering "hundreds of cancer-associated
  genes".
- Integration of tumour and germline analyses.
- Allelic / zygosity context of somatic variants.
- Mutational signatures as therapy-response biomarkers.
- Whole-genome and whole-transcriptome sequencing as comprehensive extensions.
- Ultra-sensitive cell-free DNA (cfDNA) profiling for minimally invasive,
  serial analysis.

<!-- UNVERIFIED: the specific set of commercial panels compared
(MSK-IMPACT, FoundationOne CDx, FoundationOne Heme, Tempus xT, Caris MI,
Guardant360, Personalis) and whether the review contains a side-by-side
gene-content table could not be confirmed from the abstract alone. Given the
authorship (MSK / OncoKB) and journal scope, MSK-IMPACT and FoundationOne CDx
are near-certain to be discussed; the others are likely but unverified. -->

## Key Findings

Verified themes (from abstract):

1. **Clinical utility beyond variant calling.** Tumour genomic profiling is
   framed as clinically useful for (a) refining cancer subtype classification,
   (b) selecting patients for systemic (typically targeted) therapies, and
   (c) screening for heritable cancer-risk germline variants uncovered by
   tumour sequencing.
2. **Paired tumour+germline is emphasised.** The review explicitly calls out
   integration of tumour and germline analyses as a direction for enhancing
   clinical utility — consistent with the matched-normal design used by
   MSK-IMPACT and increasingly by other platforms.
3. **Allelic / zygosity context matters.** The abstract calls out
   "characterizing allelic context" as a next-generation requirement —
   i.e. LOH, biallelic inactivation, mutant-allele fraction in the context of
   ploidy and purity.
4. **Mutational signatures as biomarkers.** Signatures (e.g. MMRd, HRD, APOBEC,
   tobacco, UV) are framed as therapy-response predictors, not just
   mechanistic labels.
5. **cfDNA as a serial complement.** Ultra-sensitive cfDNA profiling is
   positioned as enabling minimally invasive, longitudinal surveillance —
   relevant for MRD, resistance emergence, and serial TMB/MSI tracking.
6. **WGS/WTS as the comprehensive ceiling.** Whole-genome and
   whole-transcriptome sequencing are discussed as the comprehensive endpoint
   toward which clinical panels are evolving.

<!-- UNVERIFIED: the following project-relevant specifics could NOT be verified
from the abstract. They are likely covered given the review's scope but should
be checked against the full text before being cited:
- Explicit gene-content overlap numbers across commercial panels
  (e.g. "~150 genes are shared across all major panels").
- Quantitative comparison of TMB calls across platforms
  (MSK-IMPACT vs F1CDx vs Guardant vs WES).
- Explicit treatment of clonal-hematopoiesis (CH) filtering as a
  panel-design problem and the role of matched buffy-coat sequencing.
- Explicit discussion of cohort-selection biases across commercial
  vs academic platforms (late-stage enrichment, referral bias,
  over-representation of advanced/metastatic disease).
- Per-use-case recommendations (e.g. "panel X appropriate for solid
  tumours stage IV; inappropriate for hematologic malignancies without
  heme-specific panel"). -->

## Relevance

Frames panel-based clinical sequencing (MSK-IMPACT, FoundationOne, GENIE, etc.) as a single
methodology class. Useful synthesis layer for our cross-study work because it explicitly compares
panel content, calling pipelines, and cohort biases across the major commercial / academic
platforms — the dimensions our pipeline implicitly aggregates over.

<!-- UNVERIFIED: the specific claim "explicitly compares panel content, calling
pipelines, and cohort biases" in the Relevance paragraph reflects the expected
scope of a 2021 NRG review on this topic, but could not be confirmed against
the full text. If the full text turns out to emphasise cfDNA / WGS / signatures
more than cross-platform panel comparison, the Relevance framing should be
narrowed. -->

## Limitations

- **Narrative review, not systematic.** No declared search strategy or
  inclusion/exclusion criteria (expected for a Nature Reviews commission).
- **2021 cutoff.** Pre-dates several key developments relevant to our pipeline:
  expanded GENIE releases (v13+), maturation of liquid-biopsy MRD assays
  (Signatera, etc.), large-cohort CH-aware calling studies, and newer
  pan-cancer signature frameworks. Anything post-early-2021 is out of scope.
- **Clinical-utility framing, not meta-analysis methodology.** The review is
  oriented toward the oncologist/clinician reader, not toward downstream
  meta-analysts harmonising heterogeneous cohorts. Do not expect formal
  cross-panel normalisation recipes. <!-- UNVERIFIED -->
- **Likely MSK-centric perspective.** Both authors are MSK faculty and
  OncoKB co-developers; the review's panel comparison should be read with
  that institutional frame of reference in mind. <!-- UNVERIFIED but
  structurally likely. -->

## Follow-up

Natural next-reads for our pipeline, based on the review's declared scope:

- **Zehir et al. 2017** (MSK-IMPACT 10,000 cohort) — concrete instance of the
  matched-normal, panel-based paradigm the review advocates.
- **AACR GENIE Consortium 2017 (and subsequent releases)** — multi-institution
  aggregation of the panel class the review describes.
- **Pugh et al. 2022** (AACR GENIE Biopharma Collaborative / analytical
  comparability work) — the harmonisation layer the review implies is needed
  but does not itself provide.
- **Priestley et al. 2019** (Hartwig WGS pan-cancer) — the WGS endpoint the
  review points toward.
- **cfDNA / MSK-ACCESS, Guardant360, FoundationOne Liquid CDx** primary
  papers — concrete realisations of the "ultra-sensitive cfDNA" category the
  abstract highlights.
- **Clonal-hematopoiesis / panel-filtering work** (e.g. Ptashkin 2018,
  Razavi 2019) — fill the CH-filtering gap if the review itself treats it
  only at a high level.

<!-- UNVERIFIED: the specific reference set the review forward-cites could not
be extracted from the abstract; the list above is our best guess at the
natural next reads given the declared scope. -->
