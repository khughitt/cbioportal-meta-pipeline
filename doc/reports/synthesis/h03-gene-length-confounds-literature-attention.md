---
id: "synthesis:h03-gene-length-confounds-literature-attention"
type: "synthesis"
title: "Gene length confounds biomedical-literature attention"
report_kind: "hypothesis-synthesis"
hypothesis: "hypothesis:h03-gene-length-confounds-literature-attention"
generated_at: "2026-04-28T03:09:06Z"
source_commit: "c1c6b1f29eef8326e3efde948df540ecc23c95ed"
provenance_coverage: "thin"
---

# Synthesis: Gene length confounds biomedical-literature attention beyond mutation-count mediation

## State

hypothesis:h03-gene-length-confounds-literature-attention is at proposed/active status with no completed empirical interpretation directly attached to it. The core conjecture — that `log(protein_length)` carries a positive partial slope on `log(PubMed mention count)` after controlling for `log(mutation count)` — has not yet been tested. This is a preliminary framing whose empirical record lives almost entirely in motivating discussion and topic notes rather than in completed interpretations or grounded analyses.

The motivating prerequisite — that raw mutation-count rankings diverge sharply from length-adjusted rankings — is documented in discussion:2026-04-24-gene-length-bias-in-mutation-rankings-and-literature, which records an empirical Jaccard@100 of 0.015 between raw and length-adjusted gene lists. That same discussion records PubTator-correlation values from an exploratory panel (raw +0.002 to +0.184 across ranking schemes), consistent with the directional prediction of P1 (mediated path) but not yet providing the partial-slope estimate required to evaluate P2 (direct path, the central claim).

No `.edges.yaml` file exists for this hypothesis. No completed interpretation has `hypothesis:h03-gene-length-confounds-literature-attention` in its `related:` field. Task t154 references h03 explicitly and frames the ascertainment question (panel vs WES stratification) as a prerequisite for the main regression. Task t129 specifies the regression pipeline; task t130 covers the Stoeger & Nunes Amaral 2018 methodological reference. All three tasks remain at proposed status.

The partial-slope value `beta_length` — the headline number — does not yet exist. Its predicted range is +0.10 to +0.40 per the hypothesis spec.

## Arc

Arc reconstruction is limited because no completed interpretations carry `prior_interpretations` chains directly connected to h03.

The investigation began with discussion:2026-04-24-gene-length-bias-in-mutation-rankings-and-literature, which coupled two questions: whether the pipeline's length-normalized mutation ratios are defensible, and whether an analogous length bias contaminates the literature-attention axis. That discussion established the empirical Jaccard@100 divergence (0.015) as the structural prerequisite for the mediated path, and surfaced a PubTator correlation panel from an exploratory t131 run as directional — not confirmatory — evidence.

From that discussion, three tasks were scoped to translate the conjecture into testable form. Task t129 pre-registers the partial-slope regression. Task t130 targets the Stoeger 2018 methodological anchor. Task t154 adds an assay-stratification prerequisite: before the main regression is interpreted, the analysis must establish whether panel-vs-WES ascertainment differences conflate with the length signal (panel designs include genes partly on the basis of length and biological priority).

The current epistemic position is that h03 is a well-posed conjecture with a clear falsification criterion — `beta_length <= 0` after covariate adjustment falsifies P2 — but no empirical grounding beyond the motivating Jaccard and correlation panel documented in discussion:2026-04-24-gene-length-bias-in-mutation-rankings-and-literature.

## Research Fronts

**Open tasks** (all proposed, none active):

- task:t129 — partial-slope regression (`log(mention) ~ log(length) + log(mutation_count) + controls`) on the full pan-cancer table; pre-registers `beta_length` with bootstrap CIs across five subsets (all protein-coding genes, CGC, Bailey 2018, 2010+ publications, primary research only). Blocked informally on t144/t145 propagation for stable mutation counts.
- task:t130 — Stoeger & Nunes Amaral 2018 paper summary; needed to establish the prior effect-size anchor and the covariate list (PPI degree, domain count, antibody proxies) for the P3 mechanism test.
- task:t154 — panel-vs-WES ascertainment analysis; explicitly tests whether assay regime is a confound that must enter the t129 regression as a stratum covariate. References h03 directly in its `related:` field.

**Open questions** (from hypothesis spec, not yet promoted to doc/questions/):

- question:q011-gene-length-as-literature-attention-confounder — the primary formal question under this hypothesis. The regression specified in t129 is the decisive test.
- question:q016-panel-induced-ascertainment — addressed by t154; whether panel studies inflate the length-attention correlation by design-constrained gene selection.

**Known gaps**: the P3 mechanism test (adding BioGRID PPI degree, UniProt domain count, antibody proxies as covariates to decompose the direct length path) has no task assigned yet. The time-window extension (pre-2010 vs post-2010 publications) and the CDS-length-vs-protein-length sensitivity analysis are specified in the hypothesis but unscheduled. Reverse-causality mitigation (fixing length to GRCh38 canonical Ensembl values) is noted in the hypothesis spec but has no tracking task.

**Knowledge gaps**: no `topic_gaps` data was included in the bundle for this hypothesis.
