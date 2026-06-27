---
type: hypothesis
title: "Cross-study gene rankings replicate strongly for canonical drivers and weakly\
  \ for length/raw-driven candidates \u2014 divergence between ranking schemes is\
  \ structured, not random"
status: proposed
created: '2026-04-27'
updated: '2026-04-28'
id: hypothesis:0002-cross-study-ranking-divergence-is-structured
phase: active
source_refs:
- paper:Lawrence2014
- paper:Bailey2018
- paper:Martincorena2017
related:
- question:0013-cross-study-replication-rate
- question:0003-replication-timing-as-gene-level-mutation-rate-confounder
- question:0011-gene-length-as-literature-attention-confounder
- task:t149
- discussion:0001-gene-length-bias-in-mutation-rankings-and-literature
- interpretation:0009-t131-full-pan-cancer-dndscv-run
- topic:mutation-rate-normalization
---

# Hypothesis: Cross-study ranking divergence is structured, and canonical drivers replicate

## Organizing Conjecture

The project's flagship research question — *which gene-cancer associations recur across
independent cBioPortal studies?* — has two coupled answers depending on ranking scheme.
**Canonical drivers replicate strongly** across studies and across ranking schemes (raw
frequency, length-adjusted, dNdScv selection): they appear in the top-N of every scheme,
in every well-powered cancer-type, in nearly every leave-one-study-out fold.
**Long-tail candidates replicate weakly** and the divergence between schemes is *structured*:
raw-rank tops are dominated by long-gene passengers (TTN, MUC16, OBSCN, RYR2, LRP1B); pure
length-adjusted tops are dominated by tiny-protein artifacts (BAGE2, PYY2, TMSB4X) plus a
few short canonical drivers; dNdScv tops correctly recover canonical drivers but leave
residual large-gene signal (TTN, AHNAK) that is consistent with replication-timing as a
remaining confounder beyond length and trinucleotide context.

## Proposition Bundle

### Core Propositions

- **P1 (replication, drivers).** For canonical pan-cancer drivers (TP53, KRAS, PIK3CA, APC,
  PTEN, BRAF, EGFR, NRAS, IDH1, BRCA1/2, CDKN2A, RB1, FBXW7), top-N rank stability under
  leave-one-study-out cross-validation is high (≥80% of fold-pairs preserve rank to within
  ±5 positions for any reasonable N ≥ 25), in every well-powered cancer-type with ≥3
  contributing studies.
- **P2 (replication, candidates).** For non-canonical / long-tail candidates (genes that
  enter the top-100 of any scheme but are not in the Bailey et al. [@Bailey2018] driver list), leave-one-out
  rank stability is materially lower (<30% within ±5 positions) and the *direction* of
  rank change correlates with which study is held out (i.e. the candidate is study-specific,
  not study-replicated).
- **P3 (divergence is structured).** The set difference (top-100_raw \ top-100_length-adj)
  is enriched for long genes (>1500 aa) at the canonical Lawrence et al. [@Lawrence2014] list (TTN, MUC16,
  OBSCN, RYR2, LRP1B, USH2A, CSMD1/3, FAT1/4, …); the set difference (top-100_length-adj \
  top-100_raw) is enriched for short proteins (<200 aa) plus short canonical drivers (KRAS,
  TP53, RHOA, CDKN2A); the set difference (top-100_dNdScv \ top-100_raw) overlaps Bailey
  et al. [@Bailey2018] to a greater extent than either of the previous two. **Concrete pre-registered
  expectation: Jaccard@100 (raw, length-adj) ≤ 0.10 — empirical PoC value 0.015.**
- **P4 (residual confounder identification).** Genes that survive in the dNdScv top-100 but
  are not in Bailey et al. [@Bailey2018] (TTN, AHNAK, AHNAK2, ABCA13 at full pan-cancer scale) are enriched
  for late-replicating regions and common-fragile-site overlap, identifying replication
  timing and CFS instability as the dominant *remaining* gene-level confounders after
  length and trinucleotide correction.

### Supporting Or Auxiliary Propositions

- A pre-registered aggregator selection rule (e.g. lexicographic `(min_q ASC,
  n_cancers_significant_q05 DESC)`) reduces leave-one-out rank variance vs naive `min_q`
  alone; choice of rollup methodology is a substantive source of variance, not a bookkeeping
  detail (closes the t131 / t144 finding into a methodological proposition).
- PubTator literature attention correlates positively with raw and dNdScv rankings and
  negatively with length-adjusted rankings, consistent with `hypothesis:0003` and confirming
  that the divergences are *interpretable* (not arbitrary).

## Current Uncertainty

- Leave-one-study-out cross-validation has not yet been run on this project. The baseline
  rank-stability numbers above are pre-registered expectations from PCAWG / Bailey et al. [@Bailey2018]
  follow-on consensus stability literature and from the t131 PoC-vs-full-run shifts;
  empirical numbers may differ. `question:0013-cross-study-replication-rate` / `t149` is the required project-internal test before
  P1 or P2 should be cited as a result.
- The "structured divergence" claim has been demonstrated for the raw-vs-length-adjusted
  pair (Jaccard@100 = 0.015, `question:0011-gene-length-as-literature-attention-confounder`
  notebook) and partially for the dNdScv-vs-others pair
  (t131); the three-way structured-divergence claim requires the t144/t145 fixes plus
  external validation against IntOGen / Martincorena et al. [@Martincorena2017] (`t146`).
- Replication timing as the dominant residual is a *prediction*, not a measurement; testing
  it requires `question:0003-replication-timing-as-gene-level-mutation-rate-confounder`-style
  RT-stratified rate analysis on the full pan-cancer table.

## Predictions

- Top-25 dNdScv at full pan-cancer scale will recover ≥22 of the canonical 25-driver list
  (TP53, KRAS, NRAS, PIK3CA, APC, PTEN, RB1, FBXW7, KMT2D, KMT2C, ARID1A, BRAF, CTNNB1, …).
  *Confirmed at v2 fixed tiebreaker: 22/25.*
- Leave-one-out cross-validation, run per-cancer-type with ≥3 studies, will show ≥80%
  rank-±5 stability for the canonical-driver set and <30% for the long-tail-candidate set.
- After dNdScv correction, the residual top-N is positively correlated with replication-
  timing-late status at the gene level (Spearman ρ ≥ +0.15, p < 0.001 on n ≥ 18,000).

## Falsifiability

- If LOO rank stability for canonical drivers drops below 60% within ±5, P1 is falsified.
  This would mean the project's flagship claim — that aggregation across studies recovers
  cross-study-replicating signal for known biology — is itself fragile, and any new finding
  would need explicit per-study attribution.
- If LOO rank stability for long-tail candidates *equals or exceeds* canonical-driver
  stability, P2 is falsified — the long-tail is not study-specific, and dismissing it would
  be incorrect.
- If structured-divergence Jaccard@100 (raw, length-adj) exceeds 0.30 at full pan-cancer
  scale (i.e. the t131 fixed mean_inclusive run reverts to PoC-like overlap), P3 needs
  re-examination — the divergence may be regime-dependent, not structural.
- If after dNdScv correction the residual top-N shows no enrichment for late-replicating
  regions or CFS overlap, P4 is falsified and the residual confounder is something else
  (panel ascertainment, cohort composition, hypermutator-cohort effects).

## Supporting Evidence

- **t131 full pan-cancer dNdScv run (interpretation, 2026-04-26):** raw and length-adjusted
  top-100 each recovered 0 Bailey drivers; dNdScv v2 (`(min_q, n_cancers)` tiebreak) recovered
  62/100 Bailey drivers and 14/15 canonical drivers in top-15, with TTN at rank #5 as a
  surviving large-gene signal. Direct empirical support for P1 + P3.
- **Gene-length discussion empirical result (2026-04-24):** Spearman ρ(raw, length-adj) =
  0.372; Jaccard@100 = 0.015 against the PoC cohort. Direct support for P3 — the rankings
  are *almost disjoint* at the head, in a structured way.
- **Lawrence et al. [@Lawrence2014]:** establishes the long-gene-passenger pattern as the canonical
  failure mode of raw-frequency ranking; identifies the same set (TTN, MUC16, OBSCN, RYR2,
  LRP1B) the project recovers.
- **Bailey et al. [@Bailey2018]:** 26-tool consensus driver list; serves as the validation oracle
  with the documented circularity caveat (dNdScv was one of seven Bailey inputs).

## Disputing Evidence

- The PoC-vs-full-run instability of PubTator correlations (raw +0.127 → +0.002; dNdScv
  +0.055 → +0.184) suggests P3's structure may be regime-dependent: the Jaccard@100
  observation might tighten at full scale once t144/t145 fixes propagate. Until t146 external
  validation is in, the structure claim remains conditional on the current run quality.
- TTN at v2 rank #5 of dNdScv is *evidence that dNdScv does not eliminate gene-length
  signal* even at full sample size — partially refuting the strongest reading of "dNdScv
  corrects length", but consistent with the more careful "dNdScv reduces but does not
  eliminate" reading. P4 (RT as residual) is consistent with this; an alternative
  explanation is genuine selection in some hypermutator subset.

## Evidence Needed To Shift Belief

- **Decisive supporting test:** Leave-one-study-out cross-validation on the full pan-cancer
  table (post-`t144`/`t145`/`t141`), reporting per-cancer-type and pan-cancer rank-±5
  stability for both the canonical-driver set and the top-100-from-any-scheme candidate set.
  Bootstrap CIs. This is now tracked explicitly as `t149`.
- **Decisive disputing test:** External rank-rank Spearman against IntOGen + Martincorena
  et al. [@Martincorena2017] (`t146`); if our top-100 disagrees with both at ρ < 0.5, the project's aggregation
  is producing a non-replicable ranking.
- **Replication-timing residual test:** Per-gene RT-late status × dNdScv-residual-rank
  Spearman.

## Proposition DAG

The P1–P4 proposition structure and its support/dispute evidence are materialized as a DAG at
`doc/figures/dags/h02-cross-study-ranking-divergence.edges.yaml` (+ `.dot`, auto-rendered PNG),
built by `t214`. Twelve edges carry the per-proposition evidence with task IDs and concrete numbers:
the length→ranking confounds (P3), dNdScv→driver-recovery (P1, supported: 62/100 Bailey, 88% CGC),
the structured divergence (P3, supported: Jaccard@100 = 0.015), the cross-study stability edges (P1/P2,
tentative pending exhaustive LOO), and the residual-confounder arm (P4) — where the late-replication
mechanism is recorded as **eliminated** (t163 null coefficient) and CFS as an **unresolved** open edge.

## Related Work

- **Questions subsumed/refined:** `question:0013-cross-study-replication-rate`,
  `question:0003-replication-timing-as-gene-level-mutation-rate-confounder`, and
  `question:0011-gene-length-as-literature-attention-confounder` — all are sub-claims of the
  structured-divergence picture.
- **Sibling hypotheses:** `h01` (the contamination axis — same residual genes, different
  causal explanation); `h03` (the literature-attention follow-on of the length axis).
- **Methodological prerequisites:** `t141` (parallelize meta-analysis), `t144` (dNdScv
  tiebreaker fix — landed), `t145` (mean_inclusive inflation fix — landed),
  `t146` (external validation), `t149` (LOO replication-rate analysis).
