---
id: "paper:Bandlamudi2026"
type: "paper"
title: "Cancer type-specific variation in patterns of driver alterations across 50,000 tumors"
status: "abstract-read"
ontology_terms: []
datasets: ["msk-impact", "msk-impact-50k-2026"]
source_refs: ["cite:Bandlamudi2026"]
related: ["paper:Zehir2017", "paper:Bailey2018", "paper:Chakravarty2017", "topic:cancer-driver-genes", "topic:pan-cancer-mutation-landscape"]
created: "2026-04-13"
updated: "2026-04-13"
---

# Cancer type-specific variation in patterns of driver alterations across 50,000 tumors

- **Authors:** Bandlamudi C, et al. (co-corresponding: Bandlamudi C, Berger MF)
- **Year:** 2026
- **Journal:** Cancer Cell
- **PMID:** 41895280
- **DOI:** 10.1016/j.ccell.2026.03.003
- **Published online:** 2026-03-26
- **BibTeX key:** Bandlamudi2026

## Key Contribution

A 5x scale-up of the Zehir2017 MSK-IMPACT cohort (10,945 -> 54,331 tumors) with new
methodological emphasis on *tissue context* of driver alterations. The headline argument is
that a driver mutation's behavior — clonality, timing, zygosity, and immunogenicity — depends
on which cancer type it occurs in, not just on the gene/position itself. The authors
formalize a "canonical vs non-canonical context" distinction and show that ~1/3 of all
detected drivers fall into non-canonical contexts with measurably different biology
(later emergence, increased subclonality). They also publish 164 newly significant
hotspots after rigorous control for gene/position/sample-specific mutation rates.

## Methods

- **Cohort:** 54,331 tumor specimens from 48,179 patients spanning 448 histological cancer
  subtypes, prospectively sequenced at MSK.
- **Assay:** MSK-IMPACT targeted panel, profiling **up to 505 cancer genes** (panel grew over
  time across the 341 / 410 / 468 / 505-gene versions; the 50k cohort spans all versions).
- **Tumor-normal:** patient-matched blood specimens used for germline subtraction.
- **Data types deposited:** point mutations with cancer cell fraction (CCF), copy-number
  alterations, gene fusions, structural variants, FACETS gene- and arm-level CN,
  HLA class I genotypes, somatic HLA class I LOH, and mutation signature assignments.
- **Hotspot discovery:** mutation-rate-adjusted significance test correcting for gene,
  position, and sample-specific background rates plus biological/technical false-positive
  sources; yielded 164 newly significant hotspots.
- **What's new vs Zehir2017:** (i) ~5x sample size and broader histology coverage (448 vs
  ~340 subtypes); (ii) explicit canonical/non-canonical context framework; (iii) integrated
  CCF/clonality, HLA LOH, and ancestry-stratified neoantigen analysis layered on top of the
  driver catalog rather than a pure mutation frequency landscape. <!-- ABSTRACT-ONLY: comparison
  drawn from abstract + commentary, not from a methods-section read -->

## Key Findings

- **Non-canonical drivers behave differently.** ~1/3 of detected driver mutations occur in
  cancer-type contexts where that gene is not a "canonical" driver. These show increased
  subclonality, later emergence in tumor evolution, and divergent biological properties
  compared to the same mutation in its canonical tissue context.
- **164 new hotspots** identified after stringent multi-factor false-positive control.
- **Gene fusions and co-occurring driver patterns** correlate with earlier age of disease
  onset within specific cancer types.
- **Ancestry-specific HLA-restricted driver neoantigens.** Differences in HLA-restricted
  presentation of driver-derived neoantigens vary by genetic ancestry, with implications
  for TCR-based therapy eligibility.
- **Cancer-type-specific HLA loss patterns** confer intrinsic immune-evasion / resistance
  in a tissue-dependent manner.
- Driver clonality, zygosity, age-of-onset associations, and HLA-dependent immunogenicity
  all vary systematically by tissue context — the central methodological claim is that
  pan-cancer driver tables that ignore tissue context are systematically misleading.

<!-- ABSTRACT-ONLY: full-text Methods/Results section was paywalled; findings above
synthesized from the PubMed abstract, the MSK press release, and the EurekAlert summary. -->

## Relevance

Most direct methodological peer of this pipeline's outputs. Treat its driver-gene x cancer-type
patterns as an external reference to compare against our clustering and frequency tables.

The paper's "canonical vs non-canonical context" framing is directly applicable: our gene x
cancer heatmaps and clustering outputs implicitly assume drivers are drivers regardless of
tissue, which Bandlamudi2026 argues is wrong for ~1/3 of events. The 164 new hotspots and
the published per-sample CCF MAF (620 MB) on Zenodo are concrete external benchmarks our
gene x cancer outputs should be cross-referenced against.

## Limitations

- **Single-center cohort** (MSK only) — patient population, referral patterns, and sequencing
  protocol all introduce institutional bias.
- **Advanced-disease selection** — MSK-IMPACT is ordered for therapy matching, so the cohort
  is enriched for metastatic / recurrent / treatment-refractory disease and underrepresents
  early-stage tumors.
- **Targeted panel (<=505 genes)** — cannot detect drivers outside the panel; non-coding,
  whole-genome, and many fusion partners are out of scope.
- **Histology imbalance** — 448 subtypes is wide, but per-subtype power varies enormously;
  rare subtypes have limited statistical resolution for the context-specific claims.
- **Ancestry analyses** depend on imputed/inferred ancestry from a clinical sequencing
  cohort, with known representation gaps.
<!-- ABSTRACT-ONLY: limitations are inferred from cohort design rather than read from the
paper's own Discussion section. -->

## Follow-up

- **Zehir2017** — predecessor 10k paper; Bandlamudi2026 is its direct 5x successor.
- **Bailey2018** — TCGA PanCanAtlas driver consensus for comparison; useful contrast because
  TCGA is treatment-naive primary tumors vs MSK-IMPACT advanced/metastatic.
- **Chakravarty2017 (OncoKB)** — actionability layer; the 164 new hotspots feed directly
  into OncoKB-style annotation pipelines.
- **Data we can pull:**
  - cBioPortal study `msk_impact_50k_2026` (https://www.cbioportal.org/study?id=msk_impact_50k_2026)
  - Zenodo deposit `10.5281/zenodo.18445440` (4.4 GB; CC-BY-NC-ND 4.0; commercial use
    requires contacting datarequests@mskcc.org). Includes mutations+CCF, CNA, fusions, SVs,
    FACETS gene/arm-level CN, HLA genotypes, HLA LOH, mutation signatures, and clinical
    sample/patient tables.
