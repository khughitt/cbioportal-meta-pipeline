---
id: "synthesis:h03-gene-length-confounds-literature-attention"
type: "synthesis"
title: "Synthesis: h03-gene-length-confounds-literature-attention"
report_kind: "hypothesis-synthesis"
hypothesis: "hypothesis:h03-gene-length-confounds-literature-attention"
generated_at: "2026-06-02T09:52:22Z"
source_commit: "037f0ab2d3c84ecc56bebd843e361c1a9dfbfa66"
provenance_coverage: "thin"
---

# Synthesis: Gene length confounds biomedical-literature attention beyond mutation-count mediation

## State

hypothesis:h03-gene-length-confounds-literature-attention is at proposed/active status. The core
claim — that `log(protein_length)` retains a positive partial slope on `log(PubMed mention count)`
after controlling for `log(mutation count)` — remains untested. The headline number (`beta_length`)
does not yet exist; the hypothesis spec predicts a range of +0.10 to +0.40.

The motivating structural prerequisite is established. interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run
(F5) reports PubTator Spearman correlations of +0.002 (n.s.) for raw rankings, −0.109
(p = 1.4e-48) for length-adjusted rankings, and +0.184 (p = 3.1e-137) for dNdScv v2 rankings at
n = 18,028 genes. This directional pattern is consistent with the mediated path (P1) but magnitudes
are flagged as unstable pending resolution of pooled-mean inflation
(interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run, F4).

interpretation:2026-04-29-q016-panel-induced-ascertainment (F5) adds a concrete assay-stratum
finding: WES-stratum beta_length = −0.078 vs. panel-only beta_length = −0.571 (n = 465 genes),
establishing that assay regime is a required covariate for the h03 regression (task:t129). No
`.edges.yaml` file exists for this hypothesis.

## Arc

Arc reconstruction is limited because no completed interpretations carry `prior_interpretations`
chains connected to this hypothesis before the two interpretations in this bundle.

The investigation opened with the h03 framing, positing mediated and direct gene-length paths to
literature attention. Task task:t131 provided a cheap Phase-1 PubTator readout.
interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run documented the first full-scale results:
pipeline ran to completion (146 cancer types, 474,524 rows), but two data-quality bugs — BH-FDR
floor pile-up for 829 genes producing alphabetical tiebreaking (F2), and fragile-site/pseudogene
inflation in pooled `mean_inclusive` (F4) — degrade confidence in the current correlation
magnitudes. Applying the `n_cancers_significant_q05` tiebreaker (v2) recovered 62/100 Bailey 2018
drivers but left TTN at rank 5, suggesting residual large-protein signal after trinucleotide
correction (F3). interpretation:2026-04-29-q016-panel-induced-ascertainment then confirmed, via
task:t154, that panel-vs-WES ascertainment is a material covariate, with panel-only rankings
covering only 465 genes from one study. The decisive partial-slope regression (task:t129) awaits
stable mutation counts and assay-stratified design.

## Research Fronts

**Open tasks** (all proposed):

- task:t129 (P2) — partial-slope regression; blocked on F4 pooled-mean fix and assay-stratum
  handling per interpretation:2026-04-29-q016-panel-induced-ascertainment.
- task:t130 (P2) — Stoeger & Nunes Amaral 2018 summary; needed for the P3 covariate list (PPI
  degree, domain count, antibody proxies).
- task:t131 (P2) — three-way ranking comparison; pipeline-complete but substantive interpretation
  gated on F2/F4 fixes per interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run.
- task:t161 (P2) — absorb orphan questions q014/q016/q017 into hypothesis spine.
- task:t170 (P1) — integrate PubTator Central, iCite, and OpenAlex for higher-quality mention
  counts.

**Open questions:**

- question:q011-gene-length-as-literature-attention-confounder — primary formal question; task:t129
  is the decisive test.
- question:q016-panel-induced-ascertainment — partially addressed by
  interpretation:2026-04-29-q016-panel-induced-ascertainment; panel signal conflates assay,
  metastatic cohort, and institution-specific ascertainment and is not yet disentangled.

**Known gaps**: the P3 mechanism test (decomposing beta_length via BioGRID PPI degree, UniProt
domain count, antibody proxies) has no assigned task. Time-window extension (pre-2010 vs.
post-2010) and CDS-vs-protein-length sensitivity are specified in the hypothesis spec but
unscheduled. No `topic_gaps` data was present in the bundle.
