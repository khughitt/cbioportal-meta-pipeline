---
type: meta
title: Pipeline roadmap and task-synthesis (2026-04-13)
status: active
created: '2026-04-13'
updated: '2026-04-13'
id: meta:0002-pipeline-roadmap-and-task-synthesis-2026-04-13
---

# Pipeline roadmap and task-synthesis (2026-04-13)

Consolidated view of the findings from **6 reading batches (22 papers) + 14 topic syntheses + 1 first audit** into a single prioritized plan for the cbioportal pan-cancer mutation meta-analysis pipeline.

## The problem in one sentence

**Our pipeline aggregates somatic mutation data across heterogeneous cBioPortal studies without addressing any of the four bias axes documented in the cross-study cancer-genomics literature** (panel content / matched-normal calling / cohort selection / annotation drift). Outputs should not be cited as cross-study mutation-frequency claims in their current form.

## The goal

Get our pipeline to current-best-practice for cross-study panel-based cancer-genomics aggregation — specifically, **above the methodological bar set by Kandoth 2013** (covariate-aware SMG test on harmonized MAFs) and **approaching Bailey 2018** (consensus driver catalog + per-cancer rosters). Three concrete milestones in priority order:

1. **Immediate (P1 audit-fixes)**: Remove statistically-incoherent outputs; wire the three foundational overlays (Bailey drivers, CH-priority flag, MC3 / panel callability).
2. **Near-term (P1 pipeline additions)**: Callability-masked cross-study ratios; CH-aware stratified outputs; MC3 for the TCGA portion; OncoKB version stamping.
3. **Longer-term (P2 pipeline additions + methodology topics)**: Random-effects pooled effect sizes; pathway-level overlays; tissue-conditional driver flags; cohort-stage stratification.

## Finding clusters → task map

### Cluster A: Critical statistical / aggregation correctness (F1)

**One finding, immediately fixable:**

| Finding | What's wrong | Fix task | Priority |
|---|---|---|---|
| Audit F1 | `num_df.mean(axis=1)` on raw counts ignores per-study sample-size differences — "100 mutations in 10k-sample study" and "100 mutations in 200-sample study" contribute equally | t068 | P1 |

**Immediate action**: remove the offending `mean` / `mean_adj` columns for raw counts; retain them for ratios where the unweighted mean is at least defensible as "exchangeable observations of a per-cancer rate." 5-line change, no dependencies. **Doing this now.**

### Cluster B: Critical bias-axis corrections (F2–F4)

**Four axes compound into the interpretation of every cross-study output.** All have queued pipeline tasks; the audit added specific integration points.

| Axis | Finding(s) | Quantification | Fix task | Priority |
|---|---|---|---|---|
| **Panel content** | Audit F2 | APC ~10× region-length across GENIE panels; 91 distinct assays at v9.1; only 44 genes on all launch panels | t016 (GENIE BED ingestion) + t048 (MC3 for TCGA) | P1 |
| **Matched-normal / CH** | Audit F3, F7 | 7 priority genes (DNMT3A, PPM1D, TET2, TP53, ASXL1, CHEK2, PRPF8); matched-normal yields 6 vs 15 somatic events/sample (Cheng 2015); 52% of GENIE v9.1 is tumor-only | t050 | P1 |
| **Cohort selection** | Audit F5 | AR 18% vs 1%, ESR1 11% vs 4%, EGFR T790M 11.3% vs 2.2% (clinical-seq vs TCGA) | t052 | P2 |
| **Annotation drift** | Audit F4, F8 | OncoKB Level 1/2 actionability 8.9% → 31.6% in 5 years on same cohort | t053 (version stamping) + t069 (annotated feather as canonical) | P1 |

**Sequencing recommendation**: t050 first (CH-aware filter; no external-data dependency); then t069 (redirect consumers to annotated feather); then t048 (MC3 ingestion — solves panel-content for TCGA); then t016 (GENIE BEDs — solves panel-content for GENIE, gated on manual Synapse download).

### Cluster C: Methodology upgrades (F9, plus topic-level items)

Not blocker-severity, but move our pipeline from "raw counting" to "current best practice."

| Axis | Finding / source | Fix task | Priority |
|---|---|---|---|
| Weighted vs unweighted aggregation | Audit F9 (unweighted ratio-mean) | t071 + t062 (cross-study-aggregation guide) | P2 |
| Selection-based driver signal | topic:cancer-driver-genes | t015 (dNdScv rule — already wired) | P1 done |
| Pathway-level view | topic:pan-cancer-interpretive-frames | t049 (Sanchez-Vega 2018 Tables S2/S3 overlay) | P2 |
| Tissue-conditional driver flag | Bailey 2018 19% tissue-borrowed + Bandlamudi 2026 ~1/3 non-canonical | t054 | P2 |
| Saturation-aware long-tail | Audit F10 (Lawrence 2014 required-N) | t072 | P3 |
| M/C-class hyperbola descriptor | topic:pan-cancer-interpretive-frames | t055 (blocked on CNA ingestion) | P3 |
| Cluster concordance vs Hoadley 2018 | topic:pan-cancer-interpretive-frames | t056 | P3 |

### Cluster D: Documentation / provenance / drive-by fixes

| Finding | Fix task | Priority |
|---|---|---|
| F6 MSK-IMPACT panel-version drift | t070 | P2 |
| F11 n_studies_contributing column | t073 | P3 |

### Cluster E: Research gap-filling (focused-discovery searches)

Each queued as a task; none are blockers for the pipeline work.

| Topic | Task |
|---|---|
| Panel comparability / cross-panel normalization | t026 |
| Cross-study meta-analysis stats (Bayesian hierarchical, DerSimonian-Laird alternatives) | t027 |
| Co-occurrence / mutual exclusivity methods (DISCOVER, SELECT, WeSME) | t042 |
| Pathway-level pan-cancer methods | t043 |
| TMB harmonization (Friends-of-Cancer-Research) | t025 |
| ASXL1 / TET2 CH-leakage vs real biology | t059 |

### Cluster F: Modality-guide flesh-out (for future audits)

The first audit (t067) validated the framework but also exposed that most guides have checklist scaffolding without the level-of-detail MM30's `scrna-seq.md` carries. Flesh-outs queued per modality:

| Guide | Task | Priority |
|---|---|---|
| cross-study-aggregation | t062 | P1 |
| panel-mutation-data | t060 | P2 |
| wes-mutation-data | t061 | P2 |
| driver-detection | t063 | P2 |
| variant-annotation | t064 | P2 |
| clinical-cancer-genomics (new) | t065 | P3 |
| mutational-signatures (new, when in-scope) | t066 | P3 |

## Dependency graph of the critical path

```
t068 (F1 fix, in progress) ─────┐
                                 │
t050 (CH-aware filter) ──────────┤
  requires: cBioPortal study     │
  metadata with matched_normal   │
  flag                           ├─→ re-run audit (t067 re-X) → closes F1/F3/F4/F7
                                 │
t069 (redirect to annotated) ────┤
  requires: downstream consumer  │
  audit                          │
                                 │
t048 (MC3 ingestion) ────────────┤
  requires: Synapse download     │
                                 │
t016 (GENIE BEDs) ───────────────┘
  requires: Synapse download + DUA
  gates: F2 partial fix (TCGA-only via t048 is a partial F2 fix)
```

## Where we are on the methodology ladder

| Rung | Our pipeline | Example |
|---|---|---|
| 0: raw counting | ✓ (current) | — |
| 1: first-order normalization (protein length) | ✓ (current, partial) | — |
| 2: covariate-aware SMG test on harmonized MAFs | ✗ | Kandoth 2013 |
| 3: MutSigCV with full covariate set | ✗ (requires external RNA / chromatin tracks) | Lawrence 2014 |
| 4: Selection-based (dNdScv) parallel signal | **partially done** (rule wired, not in rule-all) | Martincorena 2017 |
| 5: Multi-tool consensus + external catalog overlay | **in progress** (Bailey overlay wired; rule-all integration = F4) | Bailey 2018 |
| 6: Tissue-conditional + pathway-collapsed + version-stamped | ✗ | Bandlamudi 2026 / Sanchez-Vega 2018 / Suehnholz 2024 |

**Completing P1 audit-fixes + P1 pipeline additions would put us at rung 5.** Longer-term P2 tasks target rung 6.

## What to do next

**Order of operations (next 5 concrete work items):**

1. **t068 [F1 fix] — now.** Remove `num.mean` / `num.mean_adj`; document aggregation choice. Closes one Critical finding and partially addresses F9. 5-line code change.
2. **t050 [CH-aware filter] — next.** Closes F3 and F7. Requires per-study `matched_normal` flag from cBioPortal study metadata (tractable — config-driven).
3. **t069 [annotated as canonical] — parallel with t050.** Redirect downstream consumers (including `summary.html` report) to `gene_cancer_study_annotated.feather`. Closes F4.
4. **t071 [weighted-mean disposition] — parallel with above.** Document the unweighted-mean-of-ratios aggregation choice in script header (cheap partial F9 close) OR add sample-size-weighted variant.
5. **Re-run audit (re-2 of t067)** after steps 1–4. Verify F1/F3/F4/F7/F9 resolutions. Expected: 4 Critical → 0 Critical; 6 Significant → 3 Significant (F5, F6, F10 remaining).

Then move into pipeline additions in cluster B priority order.

## Closing note

The reading-driven synthesis was **worth the cost**. Every Critical audit finding traces back to a specific paper we read (Bolton 2020 → F3; Pugh 2022 → F2; Bailey 2018 → F4; Cheng 2015 + Pugh 2022 → F7) and a specific topic stub that synthesized across papers (`topic:targeted-panel-sequencing-bias`, `topic:clonal-hematopoiesis-contamination`, `topic:cross-study-harmonization`). Without the reading, we'd have "vague concerns about panel aggregation" instead of 11 specific findings with quantified biases and citation chains to primary sources.
