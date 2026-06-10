---
type: synthesis
title: 'Synthesis: h02-cross-study-ranking-divergence-is-structured'
status: active
created: '2026-06-02'
updated: '2026-06-02'
id: synthesis:0006-cross-study-ranking-divergence-is-structured
report_kind: hypothesis-synthesis
hypothesis: hypothesis:0002-cross-study-ranking-divergence-is-structured
generated_at: '2026-06-02T09:52:22Z'
source_commit: 037f0ab2d3c84ecc56bebd843e361c1a9dfbfa66
provenance_coverage: thin
---

## State

The hypothesis asserts that cross-study ranking divergence is structured: canonical drivers replicate strongly across ranking schemes (raw frequency, length-adjusted, dNdScv) while long-tail candidates diverge in a bias-determined direction. The foundational empirical anchor is Jaccard@100 = 0.015 between raw and length-adjusted top-100 lists, documented in interpretation:0009-t131-full-pan-cancer-dndscv-run (F5 context).

The full-scale dNdScv run confirmed proposition P3 at K=100 after the tiebreaker fix: dNdScv v2 recovered 62/100 Bailey 2018 drivers versus zero for the raw and length-adjusted schemes (interpretation:0009-t131-full-pan-cancer-dndscv-run, F3–F4). External validation against CGC tier-1 yields 88% recovery at K=100 (299-fold enrichment) and 92% at K=25, against a list curated independently of Bailey (interpretation:0012-t146-external-validation-cgc, F1). The three-way Spearman matrix shows raw and dNdScv ranks are nearly uncorrelated (ρ = +0.043) while length-adjusted and dNdScv are strongly anti-correlated (ρ = −0.468), confirming systematic disagreement (interpretation:0009-t131-full-pan-cancer-dndscv-run, F6).

TTN persists at rank 4–5 despite trinucleotide correction. Replication timing does not explain this: the RT late-score regression coefficient is near zero with bootstrap 95% CI [−1.69, +1.96], and log10 protein length remains the dominant covariate (Spearman ρ = 0.564 versus ρ = −0.004 for RT, interpretation:0014-q003-rt-residual-regression, F1–F2). P4 (RT as dominant residual confounder) is weakened; question:0003-replication-timing-as-gene-level-mutation-rate-confounder remains open pending CFS-specific testing (task:t153). P1 LOSO stability is supported for the dNdScv ranking: two broad non-GENIE holdouts achieved Jaccard@100 of 0.852 and 0.923, while GENIE removal produced 0.429 — establishing GENIE as a structured rather than generic perturbation (interpretation:0020-t173-dndscv-loso-synthesis).

## Arc

Arc reconstruction is limited because six t173 interpretation files lack `prior_interpretations` chains; ordering below relies on file dates.

The investigation began with the PoC finding that raw and length-adjusted top-100 lists are nearly disjoint (Jaccard@100 = 0.015), formalizing question:0011-gene-length-as-literature-attention-confounder. The full pan-cancer dNdScv run (interpretation:0009-t131-full-pan-cancer-dndscv-run) surfaced two blocking artifacts: alphabetical tiebreaker among 829 zero-q genes (F2) and inflated raw top-15 from stale pooled means (F4). Task:t144 fixed the tiebreaker; task:t145 corrected mean inflation (interpretation:0011-t145-mean-inclusive-inflation-diagnostic). External validation (interpretation:0012-t146-external-validation-cgc) then addressed the Bailey-circularity concern.

The LOSO arm bifurcated. The pooled-rate LOSO (interpretation:0013-t149-loso-replication) produced median K=100 recovery of 0.185, attributable to the pooled_rate metric rather than the dNdScv ranking. Three targeted dNdScv holdouts (interpretation:0017-t173-dndscv-loso-pilot, interpretation:0016-t173-dndscv-loso-contrast, interpretation:0019-t173-dndscv-loso-second-broad-contrast) established GENIE as the structured perturbation; attribution analysis (interpretation:0021-t173-genie-dndscv-influence) traced the effect to broad sample-mix shifts across shared hg19 cancer labels. The RT regression null (interpretation:0014-q003-rt-residual-regression) then shifted the TTN residual diagnosis to task:t147 (hypermutator-stratified dNdScv).

## Research Fronts

**Open tasks**: task:t171 (IntOGen 2024 + DepMap external validation, blocked by data acquisition) is the highest-priority remaining external check; task:t155 (aggregator comparison under q=0 floor) addresses question:0015-pan-cancer-aggregator-choice; task:t153 (CFS overlap annotation) and task:t147 are the live diagnostics for the TTN residual after P4 weakening; task:t129 (length × PubMed regression) is the cleaner test for question:0011-gene-length-as-literature-attention-confounder; task:t158 targets question:0017-cross-study-saturation-curve; task:t161 should absorb orphan questions question:0014-cfs-as-distinct-confounder-class and question:0017-cross-study-saturation-curve into the hypothesis spine.

**Live questions**: question:0013-cross-study-replication-rate is partially addressed by the three-holdout dNdScv LOSO but lacks a full distribution; question:0003-replication-timing-as-gene-level-mutation-rate-confounder received a null result for constitutive-RT-late signal and awaits CFS-specific testing; question:0015-pan-cancer-aggregator-choice remains open pending task:t155.

**Blocked work**: task:t166, task:t167, and task:t168 (Hartwig, PCAWG, Genomics England integration) and task:t171 are blocked on data access and acquisition.
