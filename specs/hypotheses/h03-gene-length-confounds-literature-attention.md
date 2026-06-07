---
id: "hypothesis:h03-gene-length-confounds-literature-attention"
type: "hypothesis"
title: "Gene length confounds biomedical-literature attention beyond mutation-count mediation"
status: "proposed"
phase: "active"
source_refs:
  - "paper:Lawrence2014"
related:
  - "question:q011-gene-length-as-literature-attention-confounder"
  - "question:q042-driver-normal-expression-tissue-cell-type-specificity"
  - "discussion:2026-04-24-gene-length-bias-in-mutation-rankings-and-literature"
  - "interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run"
  - "topic:mutation-rate-normalization"
created: "2026-04-27"
updated: "2026-04-27"
---

# Hypothesis: Gene length confounds literature attention beyond mutation-count mediation

## Organizing Conjecture

The cancer-genomics field has spent two decades correcting mutation-count rankings for gene
length (Lawrence 2014, Martincorena 2017, Bailey 2018) — but no comparable correction exists
on the **literature-attention** axis. Gene length plausibly drives PubMed mention counts via
two paths: (i) a **mediated** path through mutation count (every "top-N mutated genes" list
in a paper inherits the length bias of raw rankings), and (ii) **direct** paths independent
of mutation count (more antibodies and reagents per long protein, more annotated domains and
PTMs, higher PPI degree, more "things to write about" per gene). Stoeger & Nunes Amaral 2018
documented the broader accessibility-bias phenomenon but did not isolate the gene-length
slope specifically. This hypothesis claims that, on the cancer-relevant gene set, **the
partial slope of `log(length)` on `log(PubMed mention count)` is positive and non-trivial
after controlling for `log(mutation count)`** — i.e. literature attention has a length-driven
component that is not explainable as a downstream consequence of length-biased mutation
counting.

If true, the working assumption that "highly mutated AND well-studied" is independent
corroboration of biological importance is wrong: both axes share gene length as a common
cause, and their agreement is partly mechanical.

## Proposition Bundle

### Core Propositions

- **P1 (mediated path exists).** `log(PubMed mention count)` correlates positively with
  `log(raw mutation count)` and (after the t144/t145 fixes) with the dNdScv ranking; the
  PubTator correlation is not zero on aggregated cBioPortal data.
- **P2 (direct path exists, central claim).** The partial slope `β_length` in
  `log(mention) ~ β_length · log(length) + β_count · log(mutation_count) + controls` is
  significantly positive (`β_length > 0`, p < 0.01 on n ≥ 18,000 protein-coding genes), with
  the human-cancer-relevant subset (CGC + Bailey 2018) yielding a slope of similar sign and
  magnitude.
- **P3 (channel decomposition).** The direct slope `β_length` is partly explained by
  measurable accessibility covariates (BioGRID PPI degree, UniProt annotated-domain count,
  antibody availability proxies, structural-biology PDB entry count) — adding these as
  controls reduces but does not eliminate `β_length`. A residual length effect after these
  controls indicates a length-as-a-driver mechanism not yet pinned down.

### Supporting Or Auxiliary Propositions

- The slope `β_length` differs across **time windows**: in older data (1990s–2000s
  publications), `β_length` is larger because driver-discovery work tracked the long-gene-
  passenger artifact directly; in modern data (2015+), `β_length` partially attenuates
  because length-aware methods (MutSigCV, dNdScv) are widely used. A cancer-specific
  replication of Stoeger 2018 over time periods is a natural extension.
- The cancer-gene subset (CGC / Bailey) shows a *smaller* `β_length` than the protein-coding
  background — because cancer genes are pre-selected for biological importance, the length
  bias is partially "absorbed" into selection. If true, this is itself evidence that the
  background `β_length` is *not* explainable by importance alone.

## Current Uncertainty

- The pre-registered partial-slope regression (t129) has not yet been run on the full pan-
  cancer table — the magnitudes from t131 PubTator panel are unstable (PoC ρ vs full-run ρ)
  pending the t144/t145 propagation. The headline number doesn't exist yet.
- The "direct path" decomposition (P3) requires PPI / annotation / antibody data joined to
  the gene level — sources are public (BioGRID, UniProt, Antibodypedia) but the join has not
  been built.
- "Length" is itself a multi-dimensional concept: protein length (UniProt canonical),
  CDS length (Ensembl), genomic span including introns, transcript count, isoform diversity.
  The hypothesis nominally targets protein length but the natural mediator (mutation count)
  scales with CDS length; the right denominator may shift the effect size.

## Predictions

- After the t144/t145 fixes propagate, `cor(log(mention), log(raw_mutation_count))` is
  positive and non-zero on the project's full pan-cancer table; `cor(log(mention),
  length-adjusted-rank)` is negative; `cor(log(mention), dNdScv-rank)` is positive and
  larger than `cor(log(mention), raw)`.
- The partial slope `β_length`, controlling for `log(mutation_count)`, is in the range
  +0.10 to +0.40 (i.e. doubling protein length adds 10–40% to mention count, mutation count
  held constant) on n ≥ 18,000 protein-coding genes.
- The slope is robust to: removing top-1% mutation-count outliers; restricting to 2010+
  publications; restricting to primary research articles (excluding reviews); using CDS
  length instead of protein length.
- After adding PPI degree + annotated domain count as controls, `β_length` decreases by
  ≥30% but remains positive and significant.

## Falsifiability

- If `β_length ≤ 0` (or non-significant) after controlling for `log(mutation_count)` and
  basic covariates (chromosome, gene-discovery year), P2 is falsified — literature attention
  is fully explainable as length-mediated-via-mutation, not length-driven directly.
- If `β_length` reverses sign on the cancer-gene subset (CGC/Bailey), the cancer-specific
  contribution is decoupled from the broader bias and the framing as a cancer-genomics
  problem is wrong.
- If accessibility covariates (PPI / domain / antibody) explain >95% of `β_length`, the
  residual length effect is not a meaningful object — length is a proxy for accessibility,
  not a separate cause.

## Supporting Evidence

- **Discussion (2026-04-24, gene-length-bias-in-mutation-rankings-and-literature):**
  empirical Jaccard@100 (raw, length-adj) = 0.015 establishes the strong length-vs-rank
  divergence prerequisite for the mediated path. PubTator-correlation panel from t131
  (raw +0.002 to +0.184 across schemes at full scale) is consistent with the directional
  prediction.
- **Stoeger 2018 (paper, summary pending — `t130`):** broader accessibility-bias result with
  length as one identified covariate; methodological reference for the regression.
- **Lawrence 2014 (paper):** establishes the gene-length-mediated mutation-count bias that
  forms the mediator path.
- **Gillis & Pavlidis 2014:** prior literature on gene-popularity confounds.

## Disputing Evidence

- No published cancer-specific isolation of `β_length` — this is part of why the hypothesis
  is interesting, but it also means there is no prior empirical anchor for the magnitude.
  The PoC-to-full-run instability of PubTator correlations is a methodological warning:
  the headline result must be hardened against the t144/t145 inflation.
- Reverse causality is possible: well-studied genes have more accurate length annotation,
  more isoforms catalogued, and more reliable UniProt entries — i.e. length-as-measured
  correlates with attention-as-measured for non-causal reasons. Need to use a fixed
  reference-build length (Ensembl GRCh38 canonical) to mitigate.

## Evidence Needed To Shift Belief

- **Decisive test:** Run the partial-slope regression (`t129`, scoped in
  `discussion:2026-04-24-gene-length-bias-in-mutation-rankings-and-literature`) on the full
  pan-cancer table after t144/t145 propagate. Report `β_length` with bootstrap 95% CI on:
  (a) all protein-coding genes, (b) CGC subset, (c) Bailey 2018 subset, (d) 2010+
  publications, (e) primary-research-only.
- **Mechanism test:** Add PPI degree (BioGRID), annotated domain count (UniProt), antibody
  proxy (Antibodypedia or commercial-catalog count) as covariates; report `β_length` change.
- **Time-window test:** Same regression on pre-2010 vs post-2010 publications separately.

## Related Work

- **Questions:** `q011` (this hypothesis is the formal frame for q011).
- **Discussions:** `discussion:2026-04-24-gene-length-bias-in-mutation-rankings-and-literature`
  (full critical analysis + empirical result).
- **Tasks (planned):** `t129` (regression pipeline step), `t130` (Stoeger 2018 summary).
- **Sibling hypotheses:** `h02` (the methodological partner — gene-length on the mutation
  axis); `h01` (the data-quality partner — what mutation-count is *actually* measuring).
- **External:** Stoeger & Nunes Amaral 2018 *Nature Methods*; Gillis & Pavlidis 2014;
  Edwards 2011 ("Too many roads not taken").
