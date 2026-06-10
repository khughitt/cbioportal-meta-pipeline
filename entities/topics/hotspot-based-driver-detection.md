---
type: topic
title: Hotspot-based driver detection (1D residue-level and 3D spatial)
status: active
created: '2026-04-13'
updated: '2026-04-13'
id: topic:hotspot-based-driver-detection
ontology_terms: []
source_refs: []
related:
- paper:Chang2016
- paper:Gao2017
- paper:Chakravarty2017
- topic:cancer-driver-genes
---

# Hotspot-based driver detection (1D residue-level and 3D spatial)

## Summary

Hotspot methods identify drivers from single-residue (1D) or 3D-spatial recurrence rather than
gene-level mutation counts. Two reference catalogs cover this space — **Chang 2016** (1D
residue-level, 470 hotspots / 275 genes, github.com/taylor-lab/hotspots) and **Gao 2017** (3D
spatial, 943 clusters / 3,404 residues / 503 genes, 3dhotspots.org). The two catalogs are
**largely complementary**: only ~3% of 3D-cluster residues are also 1D hotspots; ~97% are rare
residues that gain power from spatial neighbors. Both catalogs apply cleanly as overlays on our
gene × cancer outputs.

## Key Concepts

- **1D residue-level (Chang 2016).** Per-codon recurrence test using a trinucleotide-context-
  aware binomial model. Background rate from per-gene mutation rate × per-codon mutability ×
  trinucleotide context, with truncation of top 99th-percentile positions to prevent dominant
  hotspots from inflating their own gene's baseline.
- **3D spatial (Gao 2017).** Per-gene permutation test over clusters defined as central residue
  + neighbors within 5 Å on PDB structures. Cluster mutation count vs decoy clusters with same
  total but shuffled residue indices. Uses BioJava + RCSB PDB, requires ≥90% UniProt↔PDB
  identity.
- **Both methods discover at WES/WGS scale and apply at panel scale.** Discovery requires
  cohort-wide background rates (degraded on panels); the published static catalogs can be
  applied as annotation overlays to panel calls without re-running the methods.
- **Hotspot vs domain-loss complementarity.** Oncogenes show hotspot recurrence (BRAF V600, KRAS
  G12, PIK3CA codons 1047/545); tumor suppressors show distributed truncating mutations. Hotspot
  methods catch the former; recurrence-only methods catch both with bias toward the former;
  selection-based methods (dNdScv, see `topic:cancer-driver-genes`) catch the latter.

## Current State of Knowledge

The two reference catalogs are operationally treated as sources of variant-level functional
annotation:
- **OncoKB consumes both** — Chang 2016 hotspots and Gao 2017 3D clusters feed into OncoKB's
  variant-effect ("Oncogenic" / "Likely Oncogenic") calls.
- **cBioPortal annotates per-mutation** with hotspot / 3D-cluster flags from both catalogs.
- Per-residue clinical interpretation is an emerging axis: a hotspot residue is a stronger
  driver claim than gene-level recurrence alone.

## Controversies & Open Questions

- **Method-to-method overlap is small** within the 3D family (only 15 residues common across
  Gao 2017 + Mutation3D + HotMAPS + Hotspot3D). Each tool encodes different sensitivity /
  specificity trade-offs; consensus lists are noisier than for gene-level driver detection.
- **Power at long-tail frequencies.** Both Chang 2016 and Gao 2017 are limited by cohort size
  for very-rare residues; AKT1 D323 (a known driver) misses 3D significance at n ≈ 11,000.
  Cohort scale-ups will promote more long-tail residues.
- **Panel-aware re-discovery.** Running the discovery methods on panel cohorts with a panel-
  restricted null is not done by either paper — open methodological question.

## Relevance to This Project

The Chang 2016 hotspot list and Gao 2017 3D-cluster list are both downloadable as static
reference catalogs. Concrete pipeline addition (extension of the Bailey overlay pattern):

1. Ingest both catalogs as `data/cancerhotspots_1d.feather` (from
   github.com/taylor-lab/hotspots) and `data/3dhotspots.feather` (from 3dhotspots.org).
2. Per-mutation annotation: `is_1d_hotspot`, `is_3d_cluster_residue`. Aggregable to per-gene as
   "fraction of mutations in known hotspots" — a quality-of-driver signal complementary to raw
   recurrence.
3. Per-cancer aggregation: hotspot-fraction per (gene, cancer) is informative when comparing to
   distributed-mutation patterns elsewhere.

These are smaller additions than the dNdScv rule but along the same axis (parallel signals
beyond raw counts).

## Key References

Chang2016 (1D residue-level); Gao2017 (3D spatial — note: Genome Medicine, not Cancer Cell as
some early notes said); Chakravarty2017 (OncoKB integration of both). See
`topic:cancer-driver-genes` for the broader methodology comparison.
