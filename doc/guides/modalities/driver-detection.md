# Driver-gene detection — best-practices guide

*As-of: 2026-04-13*

This guide codifies the audit checklist for code that **calls or annotates cancer driver genes**
— either by recurrence (MutSigCV-family), selection (dNdScv), hotspot recurrence (Cancer
Hotspots, 3D Hotspots), or by overlay against curated catalogs (Bailey 2018 [@Bailey2018], CGC, OncoKB).

The interpretive backbone is `topic:cancer-driver-genes`. For variant-level annotation specifics
(OncoKB tiers, VUS handling), see `variant-annotation.md`.

## Sources

**Method papers** (full reads at `doc/background/papers/`):

- Lawrence MS, et al. 2014. "Discovery and saturation analysis of cancer genes across 21 tumour
  types." *Nature* 505:495–501. PMID 24390350. → MutSigCV + saturation framework.
- Martincorena I, et al. 2017. "Universal Patterns of Selection in Cancer and Somatic Tissues."
  *Cell* 171:1029–1041. PMID 29056346. → dNdScv selection-based driver detection.
- Bailey MH, et al. 2018. "Comprehensive Characterization of Cancer Driver Genes and Mutations."
  *Cell* 173:371–385. PMID 30096302. → 26-tool consensus → 299-gene driver list (Table S1).
- Kandoth C, et al. 2013. "Mutational landscape and significance across 12 major cancer types."
  *Nature* 502:333–339. PMID 24132290. → MuSiC SMG, first-generation pan-cancer benchmark.
- Chang MT, et al. 2016. "Identifying recurrent mutations in cancer reveals widespread lineage
  diversity and mutational specificity." *Nat Biotechnol* 34:155–163. PMID 26619011.
  → 1D residue-level hotspot catalog (470 hotspots / 275 genes).
- Gao J, et al. 2017. "3D clusters of somatic mutations in cancer reveal numerous rare
  mutations as functional targets." *Genome Med* 9:4. PMID 28115009.
  → 3D-spatial hotspot catalog (943 clusters / 3,404 residues / 503 genes).

**Reference catalogs:**
- Bailey 2018 [@Bailey2018] Table S1 — pan-cancer + per-cancer driver rosters with Gold/Silver/Bronze tiers.
- COSMIC Cancer Gene Census (Tate 2019 [@Tate2019]) — 750 Tier-1 + Tier-2 genes.
- Cancer Hotspots (Chang 2016 [@Chang2016]) — `github.com/taylor-lab/hotspots`.
- 3D Hotspots (Gao 2017 [@Gao2017]) — `3dhotspots.org`.

**Tooling:**
- dNdScv R package — `github.com/im3sanger/dndscv` (project rule: `code/scripts/run_dndscv.R`).
- Bailey driver overlay — `code/scripts/annotate_drivers.py`.

## Audit checklist

| ID | Item | Applicability | Settled? | Evidence expected |
|---|---|---|---|---|
| driver.01 | Recurrence-only ranking is not the sole driver-claim signal | any per-gene ranking presented as "driver list" | settled | ranking accompanied by external-catalog overlay (Bailey, CGC) OR a selection-based parallel signal (dNdScv) |
| driver.02 | dNdScv on panel data flagged as exploratory | any dNdScv output on panel-restricted cohort | settled | output carries a `panel_only: bool` flag; per-cancer-type sample size noted; results not interpreted as a definitive driver list |
| driver.03 | Bailey 2018 [@Bailey2018] catalog overlay applied | per-(gene, cancer) ranking outputs | settled | `bailey2018_driver` boolean column present (per `code/scripts/annotate_drivers.py`); pan-cancer + per-cancer-type rosters distinguished |
| driver.04 | CGC overlay applied alongside Bailey | per-(gene, cancer) ranking outputs | contested | `cgc_tier_1`, `cgc_tier_2` boolean columns; two-source (Bailey ∧ CGC) consensus annotation reported |
| driver.05 | Hotspot overlay applied | per-mutation or per-(gene, cancer) outputs | contested | per-mutation `is_1d_hotspot` (Chang 2016 [@Chang2016]) and `is_3d_cluster_residue` (Gao 2017 [@Gao2017]); aggregable to per-gene "fraction in hotspots" |
| driver.06 | Saturation considerations cited for long-tail claims | per-cancer driver-discovery claim | settled | per-cancer required-N from Lawrence 2014 [@Lawrence2014] cited; cancer types below saturation flagged when a long-tail novel driver is reported |
| driver.07 | Catalog version stamped | any catalog overlay output | settled | catalog version (Bailey 2018 [@Bailey2018] supplement release date; CGC version; OncoKB snapshot) recorded per overlay column |
| driver.08 | Tissue-borrowed vs tissue-matched drivers distinguished | per-(gene, cancer) annotated outputs | contested | overlay distinguishes "Bailey driver in this cancer" vs "Bailey pan-cancer driver only" — surfaces the 19% tissue-borrowed phenomenon [@Bailey2018] |
| driver.09 | dNdScv hypermutator exclusion handled | dNdScv output | settled | hypermutators excluded from cohort fit per Martincorena 2017 [@Martincorena2017] default (`max_coding_muts_per_sample=3000`); MMR / POLE samples handled with extended context model where applicable |
| driver.10 | Tool-disagreement quantified for novel drivers | any "novel driver" claim | contested | claim accompanied by intersection across ≥2 of (Bailey, CGC, dNdScv, hotspots); single-source novel claims flagged as exploratory |

## Common pitfalls

- **Equating recurrence rank with driver-ness.** Long genes (TTN ~3×TP53 length) appear at the
  top of raw recurrence ranks without being drivers. Background-rate correction (MutSigCV
  family) or selection-based methods (dNdScv) catch this. Lawrence 2014 [@Lawrence2014]: 93% of genes carry ≥5
  mutations, but only 224 are significant after correction.
- **Running dNdScv on panel data and treating output as definitive.** dNdScv's per-cohort
  background fit degrades on panels (insufficient synonymous sites). Panel results should be
  treated as exploratory, with the panel restriction explicitly flagged on outputs.
- **Pan-cancer driver lists used as per-cancer references.** A gene in Bailey 2018's [@Bailey2018] 299-gene
  pan-cancer list may not be a driver in any specific cancer (29 of 299 are detectable only in
  the pooled run). Use per-cancer rosters when annotating per-cancer outputs.
- **Single-tool "novel driver" claims.** Bailey 2018 [@Bailey2018]: union of 8 phase-1 tools = 2,101 genes;
  consensus = 299. Single-tool novel calls are 7× more likely to be false positives.
