---
id: "topic:cancer-driver-genes"
type: "topic"
title: "Cancer driver genes: methods, reference catalogs, and recommendations"
status: "active"
ontology_terms: []
source_refs: []
related:
  - "article:Kandoth2013"
  - "article:Lawrence2014"
  - "article:Martincorena2017"
  - "article:Bailey2018"
  - "article:Tate2019"
  - "article:Chang2016"
  - "article:Chakravarty2017"
  - "article:Bandlamudi2026"
  - "topic:hotspot-based-driver-detection"
  - "topic:variant-interpretation-oncokb-vus"
  - "topic:mutation-rate-normalization"
created: "2026-04-13"
updated: "2026-04-13"
---

# Cancer driver genes: methods, reference catalogs, and recommendations

## Summary

A "cancer driver gene" is one whose somatic alteration confers a selective growth advantage
to a tumor cell. Operationally, the field detects drivers via four overlapping signals:
(1) **recurrence** (the gene is mutated more often than chance), (2) **selection** (dN/dS
deviates from neutral), (3) **clustering / hotspots** (mutations concentrate in functional
positions), and (4) **functional / clinical evidence** (curated literature support). Each
signal misses different drivers and produces different false positives, so the field has
converged on **consensus catalogs** that combine multiple methods.

For cross-study cBioPortal aggregation, the practical question isn't "which method is
best?" — it's "which external reference catalog should we use to annotate our outputs, and
which methods can we plug in as parallel signals?"

## Key Concepts

### Method evolution (2013 → 2018)

| Year | Method | Cohort | Drivers | Key methodological move |
|---|---|---|---|---|
| 2013 | Kandoth — MuSiC SMG | 3,281 / 12 | 127 | Covariate-aware SMG test on harmonized MAFs (hypergeometric + likelihood, 7 mutation categories) |
| 2014 | Lawrence — MutSigCV | 4,742 / 21 | 224 | Per-gene background rate from gene-expression + replication-timing + chromatin covariates; **saturation analysis** quantifies cohort-size needs |
| 2017 | Martincorena — dNdScv | 7,664 / 29 | 179 | Selection-based: dN/dS deviation from neutral, 192-class trinucleotide model, per-cohort fit |
| 2018 | Bailey — PanCanAtlas consensus | 9,423 / 33 | **299** | Combines 26 tools, scoring genes by consensus across 8 phase-1 detectors + 18 phase-2 mutation scorers |
| 2016 | Chang — residue-level hotspots | 11,119 / 41 | 470 hotspots / 275 genes | Codon-level recurrence with trinucleotide-context background; complementary axis |
| 2026 | Bandlamudi — non-canonical-context drivers | 54,331 (MSK-IMPACT 50k) | 164 new hotspots | "Tissue context matters" — drivers behave differently in non-canonical contexts |

### What each method actually catches

- **Recurrence (Kandoth, Lawrence, MutSig family)** — strong on hotspot drivers (BRAF V600,
  KRAS G12, IDH1 R132). Weak on long-tail truncating drivers spread across the gene body.
  False positives from long genes / high-background-rate regions.
- **Selection (dNdScv)** — catches genes under positive selection without needing single-
  position recurrence. Examples it surfaces that recurrence misses: ZFP36L1/L2, KANSL1,
  BMPR2, MAP2K7, NIPBL. Limitation: needs enough synonymous sites to fit the 192-class
  background, so panel data degrades.
- **Hotspots (Chang 2016, Gao 2017 3D)** — orthogonal to gene-level counting; produces a
  directly downloadable residue-level reference (`github.com/taylor-lab/hotspots`).
- **Curated knowledge (CGC, OncoKB)** — incorporates functional / clinical evidence not
  visible in mutation data alone; biased toward well-studied genes.

### Reference catalogs

| Catalog | Source | Size | Granularity | Access |
|---|---|---|---|---|
| **Bailey2018 Table S1** | PanCanAtlas consensus, 26 tools | 299 genes | Pan-cancer + per-cancer-type rosters; Gold/Silver/Bronze tiers | Cell supplement (free, manual download) |
| **CGC (Tate2019)** | Sanger curation | 750 genes (Tier 1 + Tier 2) | Pan-cancer; OG/TSG/fusion roles | cancer.sanger.ac.uk/cosmic/download (free for academia, account required) |
| **Chang2016 hotspots** | Statistical recurrence at codon level | 470 hotspots / 275 genes | Residue-level; lineage-specific where applicable | github.com/taylor-lab/hotspots (open) |
| **OncoKB (Chakravarty2017)** | Variant-level expert curation | ~3,000+ alterations / 418 genes (2017) | Variant + tumor-type-specific therapy levels | oncokb.org (free for academia, registration required, monthly versioned) |

### Tool agreement is modest

Bailey 2018: union of 8 phase-1 driver-detection tools = **2,101 candidate genes**;
consensus filtering collapses this to **299** (~7× reduction). Individual rankings are
noisy; relying on any single tool produces inflated lists. The consensus / multi-source
approach is the field standard for a reason.

### The "tissue-borrowed" finding

Bailey 2018 reports **19% of driver mutations** (1,719 events in 1,431 patients) occur in
genes that are drivers in a *different* cancer type than the patient's primary site.
Bandlamudi 2026 independently reports **~1/3 of detected driver mutations** are in
"non-canonical" tissue contexts and behave differently (more subclonal, later in tumor
evolution). Two papers, different methods, same conclusion: **driver-ness is partly
tissue-conditional**.

## Current State of Knowledge

The field has consolidated around:

1. **Consensus catalogs as the primary reference** — Bailey 2018 + CGC are the two most
   widely cited. New publications routinely benchmark new candidate driver lists against
   these two.
2. **Multi-tool / multi-signal approaches over single methods** — the era of "we ran
   MutSigCV and called it done" is over. Modern pipelines combine recurrence + selection +
   hotspots + curated knowledge.
3. **Tissue-conditional driver-ness** as a first-class concern — both Bailey 2018 and
   Bandlamudi 2026 push this, OncoKB encodes it operationally (tumor-type-specific tiers),
   and pan-cancer signature decomposition (Alexandrov 2020) similarly stratifies by tissue.

## Controversies & Open Questions

- **Is the long-tail real or noise?** Lawrence 2014's saturation analysis says only 4 of 21
  cancer types were close to driver-discovery saturation in 2014. With current cohorts
  (~50k MSK-IMPACT, ~100k GENIE), we may be approaching saturation for common cancers but
  rare cancers remain under-powered.
- **Should selection-based methods (dNdScv) replace recurrence-based methods, or
  complement them?** Field consensus is "complement"; Bailey 2018 includes both classes
  in its 26-tool ensemble.
- **How should panel-restricted cohorts be analyzed for driver discovery?** dNdScv works
  on panels but with degraded background-rate fits. MutSigCV requires external covariates
  (RNA expression, replication timing) not derivable from panel data. Practical answer:
  use panel data for *annotation* against established catalogs, not for *discovery*.

## Relevance to This Project

Our pipeline ranks genes by raw cross-study mutation frequency. Compared to the field
standard:

- **We are below the 2013 methodological bar.** Kandoth 2013 used MuSiC's covariate-aware
  SMG test on harmonized MAFs. We do not run any significance test.
- **We have no external driver-gene reference annotation** in our outputs. A high-frequency
  gene in our `gene_cancer.feather` could be a known driver, a long-tail candidate, or an
  artifact — we can't distinguish without external annotation.
- **Tissue-conditional driver-ness is invisible** in our current aggregation. We treat
  TP53-in-HGSOC and TP53-in-(other-cancer) as equivalent counts.

## Pipeline Implications

Three concrete additions, two of which are already wired:

1. **[wired] Bailey 2018 driver overlay.** `process_bailey2018_drivers.py` +
   `annotate_drivers.py` Snakemake rules add `bailey2018_driver` boolean column to
   `gene_cancer_study.feather`. Manual prerequisite: download Cell supp Table S1 to
   `data/bailey2018_table_s1.xlsx`.
2. **[wired, opt-in] dNdScv parallel signal.** `run_dndscv.R` + Snakemake rule produces
   per-study `wmis/wnon/wspl/wind` selection scores. Requires R + dndscv install. Output
   not in `rule all` by default — opt in by config. Caveat: panel-only studies should be
   flagged as exploratory.
3. **[planned] CGC overlay.** Analogous to Bailey overlay using the COSMIC CGC TSV. Two-
   source consensus annotation (Bailey ∧ CGC) is more robust than either alone.

Plus the operational addition surfaced from Bandlamudi 2026:

4. **[planned] Tissue-conditional driver flag.** For each (gene, cancer-type) pair, mark
   whether the gene is a driver *in that specific cancer type* per Bailey's per-cancer
   roster — vs only as a pan-cancer driver. This makes the 19% tissue-borrowed phenomenon
   visible in our outputs.

## Key References

- Kandoth2013, Lawrence2014, Martincorena2017, Bailey2018 — methodological evolution.
- Tate2019, Bailey2018 (Table S1) — primary reference catalogs.
- Chang2016 — residue-level hotspot complement.
- Chakravarty2017 — OncoKB variant-level curation.
- Bandlamudi2026 — non-canonical context finding; data on Zenodo.
- See also: `topic:hotspot-based-driver-detection`,
  `topic:variant-interpretation-oncokb-vus`, `topic:mutation-rate-normalization`.
