---
id: "synthesis:h02-cross-study-ranking-divergence-is-structured"
type: "synthesis"
report_kind: "hypothesis-synthesis"
hypothesis: "hypothesis:h02-cross-study-ranking-divergence-is-structured"
generated_at: "2026-04-28T03:09:06Z"
source_commit: "c1c6b1f29eef8326e3efde948df540ecc23c95ed"
provenance_coverage: partial
---

## State

The hypothesis asserts that divergence between ranking schemes (raw frequency, length-adjusted,
dNdScv selection) is structured and predictable rather than random, with canonical drivers
replicating strongly across schemes and long-tail candidates diverging in a bias-determined
direction.

The most direct empirical test to date is the full pan-cancer dNdScv run
(interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run, F3 and F6). After the tiebreaker
fix landed (interpretation:2026-04-27-t144-tiebreaker-fix-rerun, F1), dNdScv v2 recovered
62/100 Bailey 2018 drivers at K=100 and placed TP53, KRAS, NRAS, PIK3CA, FBXW7, PTEN, and RB1
at ranks 1–7. TTN persists at rank 4–5 despite trinucleotide-context correction
(interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run, F3), consistent with a residual
confounder beyond length — replication timing being the leading candidate under
question:q003-replication-timing-as-gene-level-mutation-rate-confounder, though this remains a
prediction rather than a measurement. The three-way Spearman matrix (F6 of
interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run) shows raw rank and dNdScv rank are
nearly uncorrelated (ρ = +0.043), while length-adjusted rank and dNdScv rank are strongly
anti-correlated (ρ = −0.468), confirming that dNdScv and naive length adjustment disagree
systematically, not randomly. The structured divergence claim for the raw-vs-length-adjusted
pair rests on Jaccard@100 = 0.015 (documented in
interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run, F5 context). The raw-frequency
top-N collapsed to zero Bailey drivers at full scale, but this was traced to a stale mean
calculation upstream of WES zero-fill (task:t145), not to a failure of the divergence
structure itself. Leave-one-study-out rank stability (question:q013-cross-study-replication-rate,
task:t149) has not yet been run; P1 and P2 remain pre-registered expectations rather than
measured results.

## Arc

The investigation began with a PoC-scale observation that raw-frequency and length-adjusted
top-100 gene lists are nearly disjoint (Jaccard@100 = 0.015 at PoC scale), establishing the
raw-vs-length-adjusted divergence as empirically substantial. This framing was formalized in
question:q011-gene-length-as-literature-attention-confounder and anchored in the Lawrence 2014
long-gene-passenger pattern.

The main investigative move was scaling dNdScv to the full pan-cancer cohort via task:t131.
The first run (interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run) ran the 8-step DAG
to completion across 146 cancer types and 474,524 annotated rows, but surfaced two
data-quality issues blocking the headline comparison: an alphabetical tiebreaker among 829
genes sharing min_q = 0 (F2), and inflated mean_inclusive values dominating the raw-frequency
top-15 (F4). These findings reframed the immediate question from "does structured divergence
hold at full scale?" to "what is the valid three-way comparison after methodological fixes?"

The tiebreaker fix (task:t144, interpretation:2026-04-27-t144-tiebreaker-fix-rerun) resolved
the first issue in a single downstream re-run: Bailey driver recovery lifted from 29 to 62 at
K=100, and canonical drivers occupied ranks 1–7. This directly confirmed the strongest reading
of P3 — that dNdScv tops overlap substantially with the Bailey consensus whereas raw tops do
not. TTN at rank 4 emerged as a substantive residual, not an artifact, pointing toward
task:t147 (hypermutator-stratified re-run) as the next diagnostic.

The inflation issue was diagnosed in task:t145: the root cause was stale mean columns computed
before WES zero-fill, allowing singleton small-study hits to dominate the raw-frequency
top-15. After the fix, TP53 rises to the top of the raw ranking, and the inflated
common-fragile-site signal drops substantially. The BRCA replication-timing pilots
(interpretation:2026-04-22-t122-rt-brca-pilot, interpretation:2026-04-22-t123-rt-brca-sbs1-proxy-pilot)
contributed an earlier evidence thread: gene-level CL/CE ratio is directionally separable
between matched and unmatched cohorts (suggestive for question:q003-replication-timing-as-gene-level-mutation-rate-confounder),
but the SBS1-proxy route collapsed under panel sparsity. The current epistemic position is that
the structured-divergence claim is well-supported for the raw-vs-dNdScv pair and the
Jaccard@100 metric, but the three-way picture requires the t145-fixed outputs to propagate
through the full pipeline before the quantitative panel can be reported externally.

## Research Fronts

**Open tasks**: task:t149 (LOSO replication-rate analysis — the decisive test for P1/P2) is
the highest-priority open question for this hypothesis; task:t146 (external validation against
IntOGen / Martincorena 2017) addresses the Bailey circularity caveat; task:t147
(hypermutator-stratified dNdScv) targets the TTN-at-rank-4 residual; task:t148 replaces the
information-lossy single-cancer best_cancer_type field; task:t155 compares pan-cancer
aggregation rules under q-value floor pile-up; task:t158 produces cross-study saturation
curves for top-N stability; task:t153 (CFS overlap annotation) will test the replication-timing
residual prediction (P4).

**Live questions**: question:q013-cross-study-replication-rate (no LOO results yet),
question:q003-replication-timing-as-gene-level-mutation-rate-confounder (gene-level RT
correlation with dNdScv residual not yet computed at full scale),
question:q011-gene-length-as-literature-attention-confounder (PubTator correlation magnitudes
unstable between PoC and full run; Phase-2 partial-slope regression in task:t129 is the
cleaner test).

**Blocking prerequisite**: the task:t145 fix requires downstream feathers to be regenerated
from `create_combined_gene_cancer_freq_table` forward before the raw-frequency and
length-adjusted panels can be reported alongside the corrected dNdScv v2 ranking.
