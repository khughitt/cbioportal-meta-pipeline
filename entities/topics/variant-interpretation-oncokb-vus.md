---
type: topic
title: Variant interpretation, OncoKB, and VUS handling
status: active
created: '2026-04-13'
updated: '2026-06-28'
id: topic:variant-interpretation-oncokb-vus
ontology_terms: []
source_refs: []
related:
- paper:Chakravarty2017
- paper:Suehnholz2024
- paper:Chang2016
- paper:Gao2017
- paper:Tate2019
- topic:cancer-driver-genes
- topic:cross-study-harmonization
---

# Variant interpretation, OncoKB, and VUS handling

## Summary

Operational classification of individual somatic variants as oncogenic / likely-oncogenic /
VUS / benign, and tier-assignment of therapy-actionability. **OncoKB** (Chakravarty et al.
[@Chakravarty2017]) is the precision-oncology knowledge base baked into cBioPortal; **CGC** (Tate
et al. [@Tate2019]) is the gene-level companion; **Cancer Hotspots / 3D Hotspots** (Chang et al.
[@Chang2016] / Gao et al. [@Gao2017]) are the variant-level recurrence catalogs that feed OncoKB's
oncogenicity calls. Our pipeline currently aggregates raw counts without functional filtering; this
topic defines the gap between "variant count" and "functional variant count."

## Key Concepts

- **OncoKB evidence tiers.** 1 (FDA-recognized in this indication) > 2A (NCCN standard-care
  same-indication) > 2B (NCCN standard-care other-indication) > 3A (compelling clinical evidence
  same-tumor) > 3B (compelling clinical evidence different-tumor) > 4 (biological evidence only) >
  R1/R2 (resistance). **Tumor-type-specific** — same variant can be Level 1 in one cancer and
  Level 3B in another.
- **Oncogenicity calls** (independent of therapy tier): Oncogenic / Likely Oncogenic / Neutral /
  Inconclusive — curator's variant-level assertion of functional impact.
- **VUS = "Variant of Unknown Significance"** — not in OncoKB or Cancer Hotspots, no curated
  call. **Critical**: absence from OncoKB is not evidence of benignity; it usually means
  uncurated.
- **Cancer Gene Census (CGC, Tate et al. [@Tate2019]).** Tier 1 (719 genes in v86) requires ≥2
  publications
  on somatic mutations + ≥2 on functional involvement. Tier 2 (31 genes) has weaker evidence.
  Gene-level reference, not variant-level.
- **Cancer Hotspots / 3D Hotspots.** Variant-level functional annotation via residue-level (1D)
  or 3D-spatial recurrence. See `topic:hotspot-based-driver-detection`.

## Current State of Knowledge

Operational stack:
1. Variant calls → annotated against OncoKB for oncogenicity + therapy tier.
2. OncoKB-Oncogenic + Cancer Hotspots residues → "functional" filter for gene-level aggregations.
3. CGC overlay → "is the gene a known cancer gene" filter at the gene level.
4. Bailey et al. [@Bailey2018] consensus → "is the gene a driver per pan-cancer consensus" overlay.

**Version drift is dramatic.** Suehnholz et al. [@Suehnholz2024]: re-annotating 47,271 MSK-IMPACT
tumors against
OncoKB v2017v1.8 vs v2022v3.17 shifted Level 1/2 actionability from 8.9% → 31.6%. Level 1 gene
count grew from 14 to 45 + MSI-H + TMB-H. Pin OncoKB version on every annotated output.

OncoKB update cadence: roughly monthly data releases; new FDA approvals expedited within ~1-2
weeks via the Clinical Genomics Annotation Committee.

## Controversies & Open Questions

- **Should a "% functional" metric be reported for our pipeline outputs?** The number changes
  dramatically with OncoKB version and depends on which catalogs are combined (OncoKB ∪
  hotspots ∪ CGC ∪ Bailey). Best practice: report multiple "% functional" definitions side-by-
  side, each pinned to a specific catalog version.
- **VUS reclassification rates.** Suehnholz et al. [@Suehnholz2024] show tumors with only
  non-actionable drivers
  fell from 44.2% → 22.8% in 5 years — implying many former VUSs were promoted to actionable.
  Our gene-level outputs are insensitive to this; variant-level outputs would be sensitive.
- **Tissue-context for OncoKB tiers.** A KRAS G12C variant is OncoKB Level 1 in NSCLC (sotorasib)
  but Level 3B in CRC (adagrasib less effective). Our cross-cancer aggregations need tumor-type-
  aware tier assignment, not pooled "Level 1 across all cancers."

## Relevance to This Project

Concrete pipeline additions:
1. **OncoKB oncogenicity flag per variant** — requires per-variant API call against a pinned
   OncoKB version, or pre-annotated OncoKB-flagged MAFs. cBioPortal exposes pre-annotated MAFs
   for many studies.
2. **Hotspot-fraction per gene** — fraction of mutations in known hotspots per (gene, cancer).
   Already discussed in `topic:hotspot-based-driver-detection`.
3. **CGC overlay** — gene-level "is in CGC" boolean. Task t051 queued.
4. **OncoKB version stamping** — task t053 queued. Critical given the drift quantified by Suehnholz
   et al. [@Suehnholz2024].

## Key References

`paper:Chakravarty2017` is the OncoKB original.
`paper:Suehnholz2024` quantifies longitudinal version drift.
`paper:Chang2016` and `paper:Gao2017` cover Cancer Hotspots variant-level catalogs.
`paper:Tate2019` is the CGC gene-level reference.
See `topic:cancer-driver-genes` and `topic:cross-study-harmonization` for broader methodology
context.
