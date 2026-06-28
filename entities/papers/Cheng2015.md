---
type: paper
title: 'Memorial Sloan Kettering-Integrated Mutation Profiling of Actionable Cancer
  Targets (MSK-IMPACT): A Hybridization Capture-Based Next-Generation Sequencing Clinical
  Assay for Solid Tumor Molecular Oncology'
status: read
created: '2026-04-13'
updated: '2026-06-28'
id: paper:Cheng2015
ontology_terms: []
source_refs:
- cite:Cheng2015
- article:Cheng2015
related:
- paper:Zehir2017
- topic:targeted-panel-sequencing-bias
dataset_usage:
- ref: dataset:msk-impact
  role: analyzed
  overlap: full
---

# Memorial Sloan Kettering-Integrated Mutation Profiling of Actionable Cancer Targets (MSK-IMPACT): A Hybridization Capture-Based Next-Generation Sequencing Clinical Assay for Solid Tumor Molecular Oncology

- **Authors:** Cheng DT, et al.
- **Year:** 2015
- **Journal:** Journal of Molecular Diagnostics
- **PMID:** 25801821
- **DOI:** 10.1016/j.jmoldx.2014.12.006
- **BibTeX key:** Cheng2015

## Key Contribution

This MSK-IMPACT assay note links paper:Zehir2017 and topic:targeted-panel-sequencing-bias.

Analytical validation of the first-generation MSK-IMPACT assay (IMPACT-341), a CLIA-certified
hybridization-capture NGS panel covering 341 cancer-associated genes from FFPE tumor DNA against
patient-matched normal. The paper establishes the assay's performance envelope - limits of
detection near 2% VAF for hotspot variants and 5% for novel variants, >99.9% specificity, and
uniform deep coverage - and operationalizes a matched-normal somatic-calling workflow that
became the template for all downstream MSK-IMPACT cohort studies (Zehir2017 and later) [@Cheng2015].

## Methods

**Panel composition.** 341 genes selected as oncogenes, tumor suppressors, or members of
pathways deemed actionable by targeted therapies; COSMIC v64 was used to prioritize hotspots
but not as the sole selection criterion. The capture footprint comprises 4,976 canonical coding
exons plus 104 noncanonical-transcript exons, with additional probes tiling 33 introns of 14
recurrently rearranged genes (e.g., *ALK*, *ROS1*) for structural-variant detection. The
complete gene list is provided in a supplementary table referenced from the Methods [@Cheng2015].

**Bait design.** Custom biotinylated DNA probes synthesized with the Roche NimbleGen SeqCap EZ
custom oligo system. Probes were empirically re-tiled over multiple iterations to flatten
coverage uniformity, particularly in high-GC and repetitive regions.

**Sequencing.** Illumina HiSeq 2500 in rapid-run mode, 2x100 bp paired-end. Minimum acceptable
mean unique coverage 200x; typical operating range 500-1000x. In the validation cohort median
sample coverage was 753x, and 97% of canonical exons reached >=350x (half the mean) [@Cheng2015].

**Matched-normal design.** Every tumor was sequenced alongside a patient-matched normal control
(FFPE or blood-derived) on the same capture pool. The paper quantifies the value of matching:
tumor-matched-normal calling yields on average 6 somatic events per sample versus 15 in unmatched
mode, with approximately 9 extra spurious private germline calls per unmatched sample that
population-frequency filters cannot remove.

**Variant calling pipeline.** BWA-MEM 0.7.5a for alignment; MuTect 1.1.4 for SNVs; GATK 2.3.9
SomaticIndelDetector for short indels (<30 bp); DELLY 0.3.3 for somatic structural variants;
a custom coverage-based caller using square-root-transformed, GC-Loess-normalized read depth
with circular binary segmentation for CNVs. Filters: 1000 Genomes MAF >1% removed; a two-tier
VAF policy accepts hotspot calls at coverage >=20x, >=8 mutant reads, VAF >=2% and novel calls
at coverage >=20x, >=10 mutant reads, VAF >=5%; variants recurrent in >20% of a standard-normal
panel are flagged as artifacts [@Cheng2015].

**Validation cohort.** 284 tumor samples previously genotyped by orthogonal clinical methods
across 47 exons of 19 cancer genes (Table 1; including *BRAF*, *EGFR*, *ERBB2*, *KIT*, *KRAS*,
*NRAS*, *PDGFRA*, *PIK3CA*, *TP53*), plus 75 matched normals, 19 *ERBB2*-amplified samples,
and 4 *EML4-ALK* fusion-positive lung adenocarcinomas [@Cheng2015].

## Key Findings

- **SNV/indel sensitivity.** 393/393 previously known variants recovered across the 284 tumor
  samples (100% concordance with prior clinical genotyping).
- **Specificity.** 99.9% false-positive rejection rate; only 9 false-positive second-tier events
  after tier-1/tier-2 VAF filtering.
- **Limit of detection.** ~2% VAF for hotspot SNVs and ~5% VAF for non-hotspot SNVs under the
  two-tier calling scheme. Serial dilution series called *ERBB2* V777L down to 0.78% VAF and
  other variants down to ~3.1%.
- **Reproducibility.** Intra- and inter-run replicates of 6 samples (3 SNVs, 3 indels) showed
  VAF standard deviations of 0.01-0.025 at matched coverage.
- **CNVs.** All 19 *ERBB2*-amplified reference samples correctly flagged (median fold-change 3.4
  in breast, 4.1 in gastric).
- **Fusions.** All 4 *EML4-ALK* fusion-positive samples detected (average ~10 paired + ~13 split
  reads).
- **Coverage performance.** 97% of canonical exons covered to >=350x; 42 exons with chronic low
  coverage (<5% of sample mean) driven by homology or GC >80%.
- **Matched vs unmatched somatic calling.** Matched-normal calling yields 6 somatic events per
  sample; unmatched calling yields 15, including ~9 germline private mutations per sample that
  evade population-AF filtering - a core argument for obligate matched-normal clinical panels.

## Relevance

The original analytical-validation paper for the IMPACT-341 panel that defines all subsequent
MSK-IMPACT cohort papers (Zehir2017, Bandlamudi2026, Nguyen2022). Useful for understanding the
per-gene capture / bait-design choices that shape downstream call quality and panel-vs-panel
comparability.

## Limitations

- **Indel size.** Pipeline restricted to indels <30 bp; larger events (e.g., *FLT3*-ITD) are
  explicitly out of scope, with Pindel flagged as a future extension.
- **GC bias.** Coverage drops in regions with >70% GC; 42 canonical exons remain chronically
  under-covered and should be treated as blind spots.
- **Minimum tumor content.** Samples were pre-screened to >=10% tumor by pathology review;
  performance below that threshold is not characterized.
- **CNV/SV validation depth.** Authors explicitly acknowledge that full sensitivity/specificity
  characterization for CNVs and structural variants was ongoing at publication - the numbers
  above are demonstrative rather than comprehensive LoD curves.
- **Deferred panel content.** IMPACT-341 omits many clinically actionable genes that were added
  in later versions (IMPACT-410 in 2014, IMPACT-468 in 2017); this paper characterizes only
  the v1 gene set.
- **Head-to-head panel comparisons.** The paper references FoundationOne (287 genes),
  UW-OncoPlex (194 genes), WuCAMP (25 genes), and amplicon platforms (Ion AmpliSeq, TruSeq
  Amplicon) as contemporary options but does not benchmark IMPACT-341 performance against any
  of them.

## Follow-up

- **Panel expansions.** IMPACT-410 and IMPACT-468 are analytically validated implicitly through
  the Zehir2017 cohort paper; a standalone v2/v3 validation paper analogous to this one is
  worth locating if per-gene LoD needs to be version-matched.
- **CH-aware filtering implications.** The 2% hotspot / 5% novel VAF floors interact directly
  with clonal-hematopoiesis contamination analysis: matched buffy-coat normals should subtract
  CH signal, but any MSK-IMPACT-derived tumor-only reanalysis (or re-called public data lacking
  paired normals) inherits the ~9-extra-private-germline-calls-per-sample problem Cheng et al.
  quantify.
- **Fusion-gene coverage list.** The 14 rearrangement-targeted genes and the specific 33 introns
  are named only in supplementary material; pulling that list is useful for any downstream
  analysis that conditions on fusion-callable vs exon-only regions.
