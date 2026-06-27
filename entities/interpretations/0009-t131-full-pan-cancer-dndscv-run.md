---
type: interpretation
title: "t131 full pan-cancer-dndscv run \u2014 chain works end-to-end; min-q rollup\
  \ tiebreaker and pooled-mean inflation surface as data-quality bugs"
status: active
created: '2026-04-26'
updated: '2026-04-26'
id: interpretation:0009-t131-full-pan-cancer-dndscv-run
source_refs:
- report:0001-t131-dndscv-three-way-comparison-design-review
- discussion:0001-gene-length-bias-in-mutation-rankings-and-literature
- question:0011-gene-length-as-literature-attention-confounder
related:
- task:t131
- task:t139
- interpretation:0001-poc-run
input: /data/packages/cbioportal/pan-cancer/summary/mut/table/three_way_ranking_comparison.feather
workflow_run: config-pan-cancer-dndscv 2026-04-25T17:10:15
prior_interpretations: []
---

# Interpretation: t131 full pan-cancer-dndscv run

## Verdict

**[~] Mixed.** The dNdScv chain ran end-to-end at full pan-cancer scale and produced
canonical outputs (146 cancer types, 474,524 annotated rows, 20,591 q < 0.05).
However, the run surfaced **two independent data-quality issues** that materially
distort the headline three-way comparison: (a) a tiebreaker artifact in the
per-gene min-q rollup (`min_qglobal == 0` for 829 genes, fall-through is
alphabetical), and (b) inflated `mean_inclusive` in the t077 pooled meta-analysis
output (raw-frequency top-15 dominated by snoU13 / Y_RNA / fragile-site genes at
implausible 65–83% rates). Both are fixable; the `q011` falsifier directional
signal is preserved but should be re-read after the fixes land.

## Findings Summary

### F1 — Pipeline-level success (`strong`, `methodological`)

The full pan-cancer-dndscv DAG ran to completion (8/8 steps, exit 0). All
canonical outputs exist:

| Output | Size | Rows |
|---|---|---|
| `dndscv_pooled.feather` | 441K | 20,091 genes (per-gene rollup) |
| `gene_cancer_pooled.feather` | 20M | 949,048 (gene × cancer × meta-analysis stats) |
| `gene_cancer_study_ratio_annotated_dndscv.feather` | 36M | 474,524 (annotated final) |
| `three_way_ranking_comparison.feather` | 1.4M | 19,008 genes (consumer-facing) |

PubTator join coverage: 18,028 / 19,008 (95%) — comparable to the PoC's 96%.
The 12+ hour `run_gene_cancer_meta_analysis.R` step is the dominant bottleneck
(filed as t141).

Evidence type: `benchmark_evidence` (pipeline integration test passed).

### F2 — `min_qglobal` BH-FDR floor pile-up (`strong`, `methodological`)

`empirical_data_evidence` (data-quality finding):

- **829 genes** in the pan-cancer table have `min_qglobal == 0.0` exactly (BH FDR
  numerical underflow). All canonical pan-cancer drivers (TP53, KRAS, NRAS,
  PIK3CA, BRAF, APC, PTEN, RB1, KMT2D, FBXW7, …) sit at `min_q == 0`.
- The current `compare_three_way_rankings.py` ranks dNdScv by `min_qglobal` only.
  Among ties at zero, it falls back to whatever order `pandas.nsmallest()`
  returns — **alphabetical symbol order**.
- Empirical proof: top-100 by `rank_dndscv` is `[AATK, ABCA13, ABCA2, ABCA7,
  ABCB11, ABL1, ACACB, ACTG1, ACVR1, ACVR1B, AGO2, AGRN, AHNAK, AHNAK2,
  AKAP13, AKT1, AKT2, AKT3, ALK, ALMS1, …]` — purely alphabetical, drawn from a
  pool of ~829 q=0 genes.

This is a regime change from the PoC (4 studies, smaller cohorts, far fewer ties
at q=0). At full scale, statistical power inflates; BH-FDR floors out for
hundreds of genes; the rollup loses resolution.

### F3 — Re-ranking with `n_cancers_significant_q05` as tiebreaker recovers the canonical driver list (`strong`, `empirical_data_evidence`)

Using the existing `n_cancers_significant_q05` column as a secondary sort key
(no new computation needed; it is already in the feather), the dNdScv
top-N transforms:

| top-N | v1 (alphabetical tiebreak) | v2 (n_cancers tiebreak) | Bailey expected ceiling |
|---|---|---|---|
| 10 | 2 | **8** | 10 |
| 25 | 5 | **22** | 25 |
| 50 | 17 | **37** | 50 |
| 100 | 29 | **62** | ~74 (PoC reference) |
| 250 | 55 | **112** | ~127 |
| 500 | 104 | **145** | ~145 |

v2 top-15: TP53, KRAS, NRAS, PIK3CA, **TTN**, FBXW7, KMT2D, PTEN, RB1, TET2,
ARID1A, ARID2, DNMT3A, BRAF, SETD2 — 14/15 are canonical pan-cancer drivers
(TTN being the persistent Lawrence et al. [@Lawrence2014] length artifact even after dNdScv
correction at this scale).

**TTN at rank #5 is not a tiebreaker bug**: its `n_cancers_significant_q05 = 48`
genuinely puts it ahead of most drivers on this composite. dNdScv is correcting
for context but not entirely subduing the very-large-protein effect at full
sample sizes.

### F4 — Raw and length-adjusted top-N collapsed to zero Bailey drivers (`strong`, `methodological`)

| Scheme | top-100 Bailey | top-500 Bailey | PoC top-100 |
|---|---|---|---|
| raw | **0** | **0** | 5 |
| length_adj | **0** | **0** | 6 |
| dndscv (v1 broken) | 29 | 104 | 74 |
| dndscv (v2 fixed) | **62** | **145** | (74) |

The raw top-15 by `mean_inclusive` is dominated by:

- pseudogenes / non-coding placeholders: snoU13, Y_RNA, RP11-127H5.1
- known common-fragile-site genes: FHIT, MACROD2, GPC5, IMMP2L, GRID2,
  CNTNAP2, LSAMP, NKAIN3, KCNIP4, SGCZ, LRRTM4

…all reporting `mean_inclusive` between 0.65 and 0.84 (i.e. these "genes" appear
mutated in 65–84% of samples in their best cancer type), which is
implausible for point mutations and is the signature of either (a) inflated
pooled-meta-analysis estimates or (b) a count-vs-callability normalization
failure at the pooling stage. Common-fragile-site signal is real biology but
manifests primarily as structural variants / homozygous deletions, not the
SNV-only pile-up the t077 chain consumes.

The length-adjusted top-15 is similarly degenerate — dominated by tiny
proteins (24–95 aa: MTRNR2L1, GNGT1, COX7B2, GNG7, NREP, RPL39L, …) because
`mean_adj = mean_inclusive / length` blows up further when the numerator is
already inflated.

**Hypothesis (best current explanation, not yet diagnosed):** The
`enforce_callability_nesting_check=false` bypass we used to get past the
`build_pooled_gene_cancer_input` validation gate (see commit `f877ec7`, t139)
let through study/cancer combinations whose callability denominators violate
the nesting assumption the pooled meta-analysis was designed for. The
inflation of common-fragile-site / pseudogene rows is consistent with this:
those gene loci are most sensitive to coverage-vs-callability mismatches.

### F5 — `q011` falsifier signal preserved in direction; magnitudes shifted vs PoC (`suggestive`, `empirical_data_evidence`)

Spearman correlation of each ranking against `log10(PubTator mention count)`
(positive = better-ranked genes get more literature attention; n = 18,028):

| Ranking | full-run ρ | PoC ρ | Δ |
|---|---|---|---|
| raw | **+0.002** (n.s.) | +0.127 | -0.125 |
| length_adj | **−0.109** (p=1.4e-48) | −0.009 | −0.100 |
| dndscv (v1 broken) | +0.183 (p=6.6e-136) | +0.055 | +0.128 |
| dndscv (v2 fixed) | +0.184 (p=3.1e-137) | n/a | n/a |

Direction is consistent with `q011`'s pre-registered conjecture (length confounds
literature attention through the mutation-count mediator), but **the magnitudes
are unstable** between PoC and full run, and the correlations cannot be
trusted while F4 (raw / length_adj inflation) is unresolved. The PubTator
correlation is essentially identical between v1 and v2 dNdScv rankings (rank
correlation is bulk-driven; the tiebreaker artifact is concentrated at the head).

### F6 — Three-way Spearman: dNdScv decorrelated from raw, anti-correlated with length-adj (`descriptive`, `empirical_data_evidence`)

n = 18,645 genes with all three signals, using corrected dNdScv v2 ranking:

| | raw | length_adj | dndscv_v2 |
|---|---|---|---|
| raw | 1.000 | +0.479 | +0.043 |
| length_adj | | 1.000 | **−0.468** |
| dndscv_v2 | | | 1.000 |

Three notable shifts vs PoC (n=18,135):

- `raw ~ length_adj`: +0.476 (PoC: +0.124) — much higher, plausibly reflecting
  the pooled-meta-analysis inflation propagating into both axes
- `raw ~ dndscv`: +0.043 (PoC: +0.088) — both essentially zero, consistent
- `length_adj ~ dndscv`: **−0.468** (PoC: +0.015) — strongly negative now;
  dNdScv at full scale preserves the long-gene signal (TTN, AHNAK, AHNAK2,
  ABCA13) that length_adj penalizes hardest.

The negative dndscv↔length_adj correlation is *expected* if dNdScv genuinely
disagrees with naive length-only adjustment (it should — dNdScv uses
trinucleotide context, not just length). The new question is whether that
disagreement is principled or driven by hypermutator / large-cohort regime
effects.

## Evidence Quality

**Confirmatory vs exploratory:** Confirmatory at the pipeline-integration level
(plan delivered the artifacts it specified). Exploratory at the substantive
level — the rollup methodology and the t077 pooled-mean behaviour at full scale
were not pre-registered in detail.

**Independence:** F1–F4 are independent of prior literature; F5 partially
replicates the PoC direction; F6 partially diverges from PoC.

**Aggregator-circularity:** PubTator is a literature aggregator, not a curated
review; using it for a rank-correlation test against three orthogonal mutation
rankings is appropriate. Bailey et al. [@Bailey2018] driver list is curated by humans using
multiple methods including dNdScv-style selection signals — there is mild
**circularity** in using Bailey driver recovery as the validation metric for a
dNdScv-based ranking. Document explicitly: dNdScv was one of seven inputs
Bailey et al. [@Bailey2018] used. The "62/100" figure should be read as "agreement with the
Bailey et al. [@Bailey2018] consensus that included dNdScv", not as independent corroboration.

**Sample sizes:** n_genes_with_pubtator = 18,028; n_genes_with_full_signals =
18,645. Spearman p-values are tiny but effect sizes (ρ ≈ ±0.1 to ±0.5) are
modest — reportable as directional signal, not as strong association.

**Suspicious results check (per the interpretation skill):**
- F2 (q=0 pile-up) is a **predictable** consequence of large sample sizes hitting
  BH-FDR's machine-precision floor; not a true "too good" result, but a too-uniform
  result that the design did not anticipate.
- F4 (raw/length top-N collapse) is **suspiciously bad** vs PoC. Most plausible
  inflators ranked by likelihood: (i) t077 pooled-mean inflation under the t139
  bypass, (ii) genuine common-fragile-site enrichment becoming visible at full
  cohort, (iii) `mean_inclusive` semantic drift between PoC and full pipeline
  versions. Investigating (i) is the cheapest first step.

## Data Quality Checks

Concerns surfaced during interpretation, recorded as `methodological` findings:

- **DQ1 (== F2)**: 829 genes have `min_qglobal == 0` exactly; tiebreaker is
  alphabetical → top-N output is meaningless without a secondary sort. Fix is
  one-line in `compare_three_way_rankings.py` plus `aggregate_dndscv_per_gene.py`
  (use `(min_q, -n_cancers_significant_q05)` lexicographic sort).
- **DQ2 (== F4)**: `mean_inclusive` for non-driver loci appears inflated. snoU13,
  Y_RNA, RP11-127H5.1 should not be in the top-15 of any defensible mutation
  ranking. Need to diagnose whether `enforce_callability_nesting_check=false`
  let through inflated estimates, or whether the issue is independent of t139
  (e.g., in `build_pooled_gene_cancer_input` itself).
- **DQ3**: `best_cancer_type` for q=0 ties is alphabetical (Ampullary Cancer
  appears as "best" for TP53, KRAS, PIK3CA, ARID1A, ARID2, …). Same root
  cause as DQ1; same fix.

## Proposition-Level Updates

This project does not yet have S-P-O propositions formalized for `q011` or t131;
the closest first-class entities are the open question `q011` and the t131
design plan. Proposed proposition deltas (for the knowledge graph if/when it
catches up):

- **P1 (new):** `dndscv_min_q_rollup_loses_resolution_at_pan_cancer_scale` —
  supported by F2 (829 genes at q=0). Stance: `disputes` the implicit design
  proposition "min-q rollup is sufficient for cross-cancer ranking".
- **P2 (new):** `n_cancers_significant_q05_tiebreaker_recovers_canonical_drivers` —
  supported by F3. Stance: `supports` a fixed rollup design.
- **P3 (`q011` conjecture, partial update):** `gene_length_confounds_literature_attention`
  — directional evidence preserved in dNdScv vs length-adj split (F5), but
  magnitudes unstable. Stance: `supports modestly`; flag as `fragile` until
  F4 is diagnosed.
- **P4 (new):** `pooled_meta_analysis_under_t139_bypass_inflates_fragile_site_loci` —
  supported by F4 (snoU13/Y_RNA/MACROD2/FHIT pile-up). Status: **conjecture;
  needs targeted diagnostic** (see DQ2).
- **P5 (existing — Lawrence et al. [@Lawrence2014] length confounding):** `dndscv_corrects_for_gene_length`
  — *partially refuted at pan-cancer scale* by TTN landing at v2 rank #5 and
  AHNAK/AHNAK2 surviving in the q=0 cluster. dNdScv reduces but does not
  eliminate the long-gene signal under very large cohorts. Stance: `disputes
  modestly` the strongest reading; consistent with the more careful reading
  ("dNdScv reduces length bias relative to raw count, not eliminates it").

## Question-Level Implications

**`q011` — Does gene length confound literature attention independently of
mutation count?**

Status: **partially addressed**. The PubTator correlation pattern at full scale
(raw +0.002, length_adj −0.109, dndscv +0.184) is qualitatively consistent with
the `q011` conjecture's pre-registered direction (length-mediated attention),
but the magnitudes diverge from the PoC (raw was +0.127, dndscv +0.055 in the
PoC). This divergence is most parsimoniously explained by F4 (raw-axis
contamination) — once that is fixed, the `q011` panel can be re-read.

The pre-registered Phase-2 regression (t129) remains the more defensible test;
the t131 PubTator panel was always the cheap Phase-1 readout. The current
verdict for `q011` is **directionally consistent but not decisive**; the formal
falsifier (partial slope of `log(length)` after controlling for
`log(mutation_count)`) has not been computed yet.

**Indirect implications for adjacent questions:**

- **`q003` (replication timing as gene-level rate confounder):** The persistent
  presence of TTN, AHNAK, AHNAK2, ABCA13 in the top dNdScv ranking even after
  trinucleotide context correction is consistent with a residual rate-axis
  confounder beyond length and trinucleotide context — replication-timing being
  the leading candidate. Strengthens the case for `q003` as a high-priority
  follow-up.
- **`q006` (CH priority gene completeness):** The pan-cancer table flags only
  7 CH priority genes (the Bolton et al. [@Bolton2020] panel). Run did not surface new CH
  candidates; `q006` unchanged.

## Evidence vs. Open Questions

Question status updates (relative to pre-run state):

| Question | Status | Change |
|---|---|---|
| `q011` (length × literature) | active | partially addressed; awaiting fix to F4 then re-read |
| `q003` (RT as rate confounder) | active | indirectly strengthened (TTN/AHNAK persistence) |
| `q006` (CH gene completeness) | active | unchanged |
| `q007` (cross-tissue rate variation null model) | active | mildly informative — full run shows some cancer types dominate top-N (Bladder, Endometrial, Ovarian) which is consistent with the cross-tissue variation hypothesis |

## New Questions Raised

1. **Q-new-1 (P1, methodological):** How should multi-cancer dNdScv signals be
   aggregated into a per-gene pan-cancer ranking when BH-FDR floors out for
   hundreds of genes? Candidate aggregators to compare: (min q, n_significant)
   lexicographic; min log10 q + sum log10 q; rank-of-min-rank (ordinal pooling);
   inverse-variance-weighted mean log10 q (Stouffer). Cheap to evaluate against
   the existing per-cancer feathers — no re-run needed.
2. **Q-new-2 (P1, methodological):** Is the pooled-meta-analysis
   `mean_inclusive` inflation caused by the t139 bypass, or independent of it?
   Diagnostic: re-run the meta-analysis on a small cancer subset with
   `enforce_callability_nesting_check=true` and compare top-15 raw vs current
   output. If snoU13/Y_RNA disappear, t139 caused it.
3. **Q-new-3 (P2, theoretical):** Why do common-fragile-site genes (FHIT,
   MACROD2, IMMP2L, GRID2, CNTNAP2, LSAMP) rank so high by raw frequency at
   pan-cancer scale? Is this real CFS biology surfacing or an SNV
   miscall artifact at fragile loci? Adjacent to `q003` (replication-timing
   confounding).
4. **Q-new-4 (P2, methodological):** dNdScv at full sample size leaves TTN at
   rank #5 (v2). Is the residual large-protein signal a coverage artifact, a
   true CFS-overlap signal, or genuine selection in some hypermutator cohort?
   Stratify dNdScv runs by hypermutator-filtered samples (the t081
   annotation chain is in place) and compare per-cancer.
5. **Q-new-5 (P3, methodological):** "Best cancer type" at q=0 ties is
   uninformative. Should we instead report `cancers_with_significant_q05` (set)
   or `most_significant_cancer_by_n_samples` (cohort-power-weighted)?

## User Questions

None raised this session beyond the running interpretation request.

## Limitations & Residual Uncertainty

- **The headline three-way comparison cannot be reported externally without
  fixes to F2 and F4.** v1 dNdScv top-N is alphabetical; raw/length top-N is
  fragile-site/pseudogene-dominated. Both are diagnosable today; both block
  publication-ready conclusions.
- **`q011` magnitude reads are unstable** between PoC and full run (raw_pubtator
  ρ shifted from +0.127 to +0.002; dndscv ρ from +0.055 to +0.184). The
  direction is preserved; the magnitudes should not be trusted until F4 is
  resolved. The Phase-2 partial-slope regression (t129) is the better test.
- **Bailey et al. [@Bailey2018] driver-recovery as a validation metric is mildly circular**
  because Bailey used dNdScv as one of seven driver-detection inputs.
- **No external comparison run.** We have not benchmarked our pan-cancer
  dNdScv output against the published Martincorena et al. [@Martincorena2017] / IntOGen pan-cancer
  ranking. That comparison should be added before publication.

## Updated Priorities

### New tasks to file (this session)

- **t144 (P1):** Fix dNdScv per-gene aggregation tiebreaker. One-line change in
  `aggregate_dndscv_per_gene.py` (already returns the right columns) and the
  corresponding sort in `compare_three_way_rankings.py`. Use lexicographic
  `(min_q, -n_cancers_significant_q05)`. Add regression test: among genes with
  `min_q == 0`, the one with higher `n_cancers_significant_q05` ranks better.
  Re-run only the two terminal rules; no re-compute of dNdScv chain needed.
- **t145 (P1):** Diagnose pooled-meta-analysis `mean_inclusive` inflation
  (DQ2 / F4). Check whether snoU13 / Y_RNA / FHIT / MACROD2 disappear from top-15
  raw ranking when `enforce_callability_nesting_check=true` is enforced (i.e.,
  is this a t139-bypass side-effect or independent?). If it is t139-related,
  bumps t139 from P2 to P1.
- **t146 (P2):** External validation of pan-cancer dNdScv output against
  Martincorena et al. [@Martincorena2017] / IntOGen pan-cancer ranking. Read their published top-N
  per cancer; compute rank-rank Spearman; spot-check disagreements.
- **t147 (P2):** Stratify dNdScv per-cancer runs by hypermutator-filtered cohorts
  (using the existing t081 `is_hypermutator` annotation). Compare per-cancer
  q=0 set sizes pre vs post hypermutator removal. Adjacent to t141 (parallelize
  meta-analysis) so re-runs become tractable.
- **t148 (P3):** Replace `best_cancer_type` (single string) with
  `cancers_with_significant_q05` (set / count) in the per-gene rollup. Drop
  the alphabetical-tiebreaker single-cancer field as a primary output.

### Existing tasks to reprioritize

- **t141** (parallelize R meta-analysis) → keep P2; the 12+ hour bottleneck
  blocked iterative debugging this session and will block any t145 / t147
  diagnostic re-runs.
- **t139** (promote t077 pooled to canonical aggregation) → conditional bump
  to P1 if t145 confirms the bypass caused the F4 inflation. Otherwise stays P2.
- **t131** (current task) → mark functionally complete on the pipeline-delivery
  axis; substantive interpretation gated on t144 + t145.

### Tasks already filed before this session and now better-justified

- **t086** (length_is_fallback indicator + per-run excluded_studies.tsv audit
  trail) — would help diagnose F4 by exposing which study × cancer combinations
  fall back to length-only normalization.
- **t087** (graded `ch_contamination_prob`) — orthogonal to this run; CH gene
  count was unchanged.

## Process Reflection

The interpretation workflow served well here. Two incidental observations:

- The "Suspicious results check" prompt in the skill is what drove me to dig
  past the headline numbers and find the q=0 alphabetical pile-up; without it
  I might have reported the v1 top-100 figure (29 Bailey drivers) as "the result"
  and missed that v2 gives 62/100 with a one-line fix.
- The "aggregator-circularity check" prompt correctly flagged Bailey driver
  recovery as a partly-circular validation metric (Bailey used dNdScv as one
  of its inputs). Worth surfacing this caveat in a project-level methods doc.
