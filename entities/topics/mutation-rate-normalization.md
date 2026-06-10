---
type: topic
title: Mutation-rate normalization (gene length, context, covariates)
status: active
created: '2026-04-13'
updated: '2026-04-13'
id: topic:mutation-rate-normalization
ontology_terms: []
source_refs: []
related:
- paper:Lawrence2014
- paper:Martincorena2017
- paper:Chang2016
- paper:Bailey2018
- topic:cancer-driver-genes
- topic:targeted-panel-sequencing-bias
---

# Mutation-rate normalization (gene length, context, covariates)

## Summary

Raw gene-level mutation counts are biased by gene length, sequence context (trinucleotide
substitution rates), and regional covariates (replication timing, expression, chromatin state).
Naive recurrence ranking conflates "frequently mutated because biologically selected" with
"frequently mutated because the gene is long / replication-late / heterochromatic." Background-
rate correction is the difference between a 224-driver list (Lawrence 2014's MutSigCV after
correction) and an ~17,000-gene list (genes with ≥5 mutations across the cohort, no correction).

## Key Concepts

- **Gene / protein length** is the simplest correction (mutations per kb of coding sequence).
  Necessary but not sufficient. Our pipeline already pulls UniProt protein lengths via
  `create_protein_length_mapping.py`.
- **Trinucleotide context (192 classes)** captures sequence-context-dependent substitution rates
  (e.g., C>T at CpG vs C>T at non-CpG). Used by dNdScv (Martincorena 2017), Chang 2016
  hotspot model, COSMIC mutational signatures (Alexandrov 2020).
- **Genomic-region covariates.** MutSigCV (Lawrence 2014) uses three: gene-expression level,
  DNA replication timing, and HiC-derived chromatin compartment. All three are *external to
  mutation data* — derived from RNA-seq + ENCODE reference cell-line tracks.
- **Per-codon background rate** (Chang 2016): combines trinucleotide context with gene-level
  rate and a within-gene relative codon mutability term. Used for residue-level hotspot
  detection where naive position-counting fails.

## Current State of Knowledge

Three operational approaches in use:

1. **Recurrence + covariate correction** (MutSigCV family). Strong on hotspot drivers; weak on
   long-tail truncating drivers. Requires external covariate tracks (expression, replication
   timing, chromatin) that are typically derived from non-tumor reference cell lines.
2. **Selection-based** (dNdScv, Martincorena 2017). Compares observed non-synonymous to
   synonymous rates with trinucleotide context. Catches genes under positive selection without
   needing single-position recurrence (e.g., truncating-mutation enrichment). Limitation:
   requires enough synonymous sites for stable background fit; degrades on small panels.
3. **Per-codon hotspot models** (Chang 2016). Codon-level recurrence with trinucleotide-
   adjusted background. Complementary to gene-level methods.

Field consensus per Bailey 2018: combine multiple methods rather than rely on one. Their 26-tool
consensus shrinks 2,101 candidate genes (union of 8 phase-1 tools) to 299 consensus drivers.

## Controversies & Open Questions

- **Is protein-length-only normalization (what our pipeline does) sufficient as a first pass?**
  No — it leaves regional rate variation uncorrected, especially for replication-late and
  heterochromatic genes. But it's a meaningful first correction over raw counts.
- **Can MutSigCV-style covariates be approximated from data we already have?** No. The
  expression / replication / chromatin tracks are external. A "MutSigCV-lite" without them
  misses the main signal.
- **For panel data (most of our cohort), what's the best feasible background model?** dNdScv
  works with caveats; per-cohort fits degrade as panel size shrinks. MutSigCV doesn't apply at
  panel scale. Practical answer: use panel data for *annotation* against external catalogs
  (Bailey 2018, CGC), not for *discovery* with a new background model.

## Relevance to This Project

Our pipeline ranks genes by raw cross-study mutation frequency (with optional protein-length
normalization). That puts us *below* the 2013 methodology bar (Kandoth used MuSiC's covariate-
aware test). The cleanest upgrade path is **dNdScv as a parallel pipeline rule** (already
wired — see `code/scripts/run_dndscv.R` and `topic:cancer-driver-genes`), producing per-gene
selection scores alongside our raw counts. Cross-validating both gives a more robust ranking
than either alone.

## Key References

Lawrence2014 (MutSigCV background-rate model + saturation); Martincorena2017 (dNdScv
selection-based); Chang2016 (per-codon trinucleotide background); Bailey2018 (consensus
methodology validates the multi-method approach).
