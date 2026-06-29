---
type: interpretation
title: 'q043 first pass: driver cancer-type-breadth distribution on the poc-2026-04-17
  cohort'
status: active
created: '2026-06-07'
updated: '2026-06-28'
id: interpretation:0037-q043-driver-breadth-distribution
source_refs:
- paper:MartinezJimenez2020
- paper:Hoadley2018
related:
- question:0043-driver-cancer-type-breadth-distribution
- question:0042-driver-normal-expression-tissue-cell-type-specificity
- question:0047-hypermutation-confound-on-driver-tissue-specificity
- hypothesis:0002-cross-study-ranking-divergence-is-structured
- question:0016-panel-induced-ascertainment
- topic:lineage-addiction-and-cell-of-origin-driver-specificity
- interpretation:0036-panel-tmb-denominator-stale-artifact-fix
---

# Interpretation: driver cancer-type-breadth distribution (first pass)

## Verdict

**Supported, qualitatively robust; the quantitative "restricted fraction" is strongly
threshold-dependent.** The breadth distribution is heavy-tailed with a small TSG-dominated
cancer-wide hub set and a long oncogene-enriched restricted tail — reproducing the *shape* of
IntOGen's (`paper:MartinezJimenez2020`) split and its specific 12-gene hub set. The exact percentage
"restricted to 1–2 types" is not a fixed property; it ranges from 8% to 60% depending on the
recurrence threshold, and only approaches IntOGen's 63% at a stringent (≥5% within-type) recurrence
grade.

## Cohort + method

- **Cohort:** `results/poc-2026-04-17/` — 13,006 samples, 58 cancer types, 4 studies (BRCA/SKCM/UCEC
  TCGA WES + MSK-IMPACT panel). Cross-cancer breadth is **panel-ascertainment-limited**: only
  MSK-IMPACT spans all types, so the analysis is restricted to its **410 panel-covered genes**
  (`question:0016-panel-induced-ascertainment`). Non-panel genes can only appear in their one TCGA type and would look
  artificially restricted — they are excluded, not silently counted.
- **Breadth** = number of distinct cancer types (≥25 samples) in which a gene is recurrent
  (within-type frequency ≥ threshold AND ≥3 mutated samples), counted from the **raw, un-broadcast**
  `gene_cancer_study.feather` — **never** the `bailey2018_driver` flag (PANCAN broadcast).
- Script: `code/notebooks/q043_driver_breadth_distribution.py`.

## Key results

**1. Threshold sensitivity (the headline caveat).** Fraction of CGC drivers restricted to 1–2 types:

| Recurrence threshold | inclusive | hypermutator-excluded |
|---|---:|---:|
| ≥1% within-type | 8.4% | 18.2% |
| ≥2% | 18.8% | 41.1% |
| ≥5% | 52.1% | **68.1%** |

IntOGen reference: 63% restricted. At the ≥5% recurrence grade our cohort now **brackets** it —
inclusive 52.1% below, hypermutator-excluded 68.1% above. (Hypermutator-excluded values use the
corrected post-TMB-fix flags; see
`interpretation:0036-panel-tmb-denominator-stale-artifact-fix`.) Either way, "restricted vs
pan-cancer" is a statement about a chosen recurrence bar and a hypermutator-handling choice, not an
intrinsic property.

**2. The hub set reproduces IntOGen.** For `question:0043-driver-cancer-type-breadth-distribution`, TP53 is the single broadest driver (breadth 33/57), followed
by PIK3CA, ARID1A, PTEN, RB1, NF1, KRAS, CDKN2A. **8 of IntOGen's 12 cancer-wide drivers** are
panel-covered here, and all 8 sit at the top of the distribution (median breadth ≈22–24 at the 1–2%
grade). The 4 missing (KMT2D, KMT2C, LRP1B, FAT4) are not on the MSK-IMPACT panel.

**3. CGC role predicts breadth — confirming the `question:0042-driver-normal-expression-tissue-cell-type-specificity` / `question:0043-driver-cancer-type-breadth-distribution` prior.** Tumor suppressors are **broader**
than oncogenes at every threshold (e.g. at ≥2%: TSG median breadth 7 vs oncogene 4); the top-15
broadest drivers are almost entirely TSGs / genome guardians (TP53, ARID1A, PTEN, RB1, NF1, ATM,
APC, SETD2, EP300, FAT1…). Oncogenes concentrate in the restricted tail. This is exactly the
predicted structure: **broad hubs = guardians; restricted tail = (lineage) oncogenes** — the
substrate `question:0042-driver-normal-expression-tissue-cell-type-specificity` needs and the
context tracked by `topic:lineage-addiction-and-cell-of-origin-driver-specificity`.

**4. Bailey cross-check + the PANCAN-handling point.** Bailey et al. [@Bailey2018] per-cancer rosters with PANCAN
**excluded**: 235 genes with ≥1 specific-cancer call, 78.7% restricted to 1–2 cancers (broadest
TP53=26, PIK3CA=18, KRAS=16). **64 genes appear *only* as PANCAN** — they would vanish from a
restricted-vs-pan-cancer count if one kept only PANCAN-encoded rows, concretely validating the rule
from `question:0043-driver-cancer-type-breadth-distribution` that PANCAN rows must be handled
explicitly rather than via the broadcast flag.

**5. Hypermutator breadth inflation (→ `question:0047-hypermutation-confound-on-driver-tissue-specificity`).** Excluding hypermutators raises the restricted
fraction (52% → **68%** at ≥5%, on the corrected post-TMB-fix flags) and **186 drivers lose ≥1
cancer-type of breadth at that same ≥5% grade** (253 at ≥2%) — apparent breadth is partly
hypermutator-driven passenger recurrence. `question:0047-hypermutation-confound-on-driver-tissue-specificity` dissects this per-sample and confirms a driver-share
dilution across 8 cancer types.

## Limitations

- **Panel ascertainment dominates** cross-cancer breadth (410 genes testable; the 4 missing IntOGen
  hubs are simply off-panel). A WES-wide cohort is needed for a complete breadth distribution.
- **Threshold dependence** is the main quantitative caveat — report the sweep, never a single number.
- Cancer-type labels are at the `cancer_type` grain (not cell-of-origin); MSK-IMPACT's per-type
  sample sizes are uneven.

## Implications for the questions

- **`question:0042-driver-normal-expression-tissue-cell-type-specificity`:** the restricted-vs-pan-cancer roster it listed as an unmet prerequisite now exists
  (`results/poc-2026-04-17/analysis/q043/breadth_inclusive_2pct.feather`), and the OG-broad-vs-TSG
  contrast direction (oncogenes restricted) supports its route-1-oncogene framing. Use the ≥5%
  recurrence grade and **stratify on `is_hypermutator`**.
- **`question:0043-driver-cancer-type-breadth-distribution`:** promote a note that the restricted fraction is threshold-defined; the IntOGen 63%
  corresponds to a stringent recurrence bar, not a universal constant.
- **`hypothesis:0002-cross-study-ranking-divergence-is-structured`:** the off-panel truncation of breadth is a concrete instance of composition-driven
  divergence from an external roster.
