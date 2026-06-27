---
type: search
title: Cross-study meta-analysis statistics for cancer genomics / mutation-frequency
  aggregation
status: active
created: '2026-04-13'
updated: '2026-04-13'
id: search:0002-cross-study-meta-analysis-stats
---

# Cross-study Meta-analysis Statistics — 2026-04-13

## Search Focus

Methods for pooling **gene-level somatic mutation frequencies and sample-level ratios across
heterogeneous cBioPortal-style studies** (not generic clinical-trial meta-analysis). The
downstream need is to replace this project's current naive sample-weighted sum with a
defensible random-effects / hierarchical pooling method that exposes heterogeneity (I², τ²)
and handles zero-event / rare-event genes correctly. This search feeds the flesh-out of
`doc/guides/modalities/cross-study-aggregation.md` (task t062) and the pipeline additions in
tasks t048–t056.

Anchor methods verified by this run:

- DerSimonian–Laird random-effects pooling (seminal).
- REML (Viechtbauer / `metafor`) and the Langan 2018 [@Langan2018] between-study variance comparison.
- Hartung–Knapp–Sidik–Jonkman adjustment for small-K pooled CIs.
- Stijnen 2010 [@Stijnen2010] / Nyaga 2014 [@Nyaga2014] GLMM-based pooling of binomial proportions.
- Barendregt 2013 [@Barendregt2013] (Freeman–Tukey arcsine) and Lin & Xu 2020 [@LinXu2020] (arcsine vs logit/GLMM).
- Higgins & Thompson 2002 [@Higgins2002] (I²) and IntHout 2016 [@IntHout2016] (prediction intervals).
- Rare-events: Stijnen 2010 [@Stijnen2010] (beta-binomial GLMM), Tsujimoto 2024 [@Tsujimoto2024] (continuity corrections),
  Efthimiou 2019 [@Efthimiou2019] (network MH for rare events), Piaget-Rossel 2019 [@PiagetRossel2019] (homogeneous-effect
  framework for rare events).
- Martínez-Jiménez 2020 (IntOGen compendium) as a cancer-genomics-native consensus-voting
  pipeline that sits between "naive pooling" and "random-effects per-gene meta-analysis".

## Query Set

| ID | Query | Source | Purpose |
|----|-------|--------|---------|
| query-01 | `DerSimonian-Laird random effects meta-analysis` | pubmed | Seminal random-effects anchor |
| query-02 | `meta-analysis pooling proportions Freeman-Tukey arcsine logit` | pubmed | Proportions-specific transforms |
| query-03 | `metafor Viechtbauer package meta-analysis` | pubmed | R-package authority |
| query-04 | `Hartung Knapp random effects meta-analysis adjustment` | pubmed | Small-K CI adjustment |
| query-05 | `meta-analysis rare events Mantel-Haenszel Peto odds ratio` | pubmed | Zero-cell / rare-events |
| query-06 | `Bayesian hierarchical meta-analysis proportions` | pubmed | Bayesian hierarchical alternative |
| query-07 | `Paule Mandel meta-analysis estimator` | pubmed | Alt τ² estimator |
| query-08 | `Higgins Thompson heterogeneity meta-analysis I2` | pubmed | Heterogeneity statistics |
| query-09 | `Sidik Jonkman tau squared estimator meta-analysis` | pubmed | Alt τ² estimator |
| query-10 | `Barendregt meta-analysis prevalence arcsine` | pubmed | Seminal proportions paper |
| query-11 | OpenAlex: DOI anchors for DerSimonian1986, Viechtbauer2010, Langan2018, Stijnen2010, Lin2020, Barendregt2013, Higgins2002, IntHout2016, MartinezJimenez2020 | openalex | Identifier verification |
| query-12 | OpenAlex: `Nyaga meta-analysis proportions confidence intervals` | openalex | metaprop / Nyaga 2014 [@Nyaga2014] |
| query-13 | OpenAlex: `generalized linear mixed model meta-analysis proportions binomial` | openalex | GLMM alternative to transforms |

## Sources and Run Metadata

- Primary sources: **PubMed** (E-utilities `esearch` + `esummary`) and **OpenAlex** (`/works`).
- Retrieved: 2026-04-13.
- NCBI API key: not used (unauthenticated).
- Candidate cap: ~25 per PubMed query, ~5–8 per OpenAlex query. Many PubMed queries returned
  hundreds of irrelevant hits (off-topic clinical meta-analyses); shortlist restricted to
  methodological papers + one native-to-cancer-genomics aggregation reference.
- Direct `curl` to NCBI is blocked in this sandbox; PubMed/OpenAlex were hit via `WebFetch`.
- No science-tool literature runtime available (`science-tool literature search` not yet
  shipped); went direct to OpenAlex + PubMed.
- Final shortlist: **13 records**. Candidates screened: ~60+ (most off-topic clinical
  reviews discarded).

## Ranked Results

| # | Citation | Year | IDs | Tier | Why it matters |
|---|---|---|---|---|---|
| 1 | DerSimonian R & Laird N. "Meta-analysis in clinical trials." *Control Clin Trials* | 1986 | DOI: 10.1016/0197-2456(86)90046-2; OpenAlex: W2107328434 | Core now | Seminal random-effects estimator. Default option in `metafor::rma` when `method="DL"`. 38,911 citations. Must be cited when we switch away from naive pooling. |
| 2 | Viechtbauer W. "Conducting Meta-Analyses in R with the metafor Package." *J Stat Softw* | 2010 | DOI: `10.18637/jss.v036.i03`; OpenAlex: W2139168999 | Core now | Canonical `metafor` manual. Defines `rma`, `rma.mh`, `rma.glmm`, `escalc`; describes DL, REML, PM, SJ, HE, ML, EB estimators side-by-side. Primary tool-of-record if we add meta-analytic pooling in R. |
| 3 | Langan D, Higgins JPT, Jackson D, et al. "A comparison of heterogeneity variance estimators in simulated random-effects meta-analyses." *Res Synth Methods* | 2018 | DOI: 10.1002/jrsm.1316; OpenAlex: W2885675882; PMID: 30067315 (not reconfirmed in this note) | Core now | Simulation comparison of DL, REML, PM, SJ, HE, ML, EB τ² estimators. Recommends **REML (with HKSJ for K<30)** as general default — the key modern guidance for *which* random-effects method to use. Directly answers "what should we run by default". |
| 4 | Stijnen T, Hamza TH, Özdemir P. "Random effects meta-analysis of event outcome in the framework of the generalized linear mixed model with applications in sparse data." *Stat Med* | 2010 | DOI: 10.1002/sim.4040; OpenAlex: W2148361291 | Core now | Exact binomial / beta-binomial GLMM for sparse event meta-analysis — the principled alternative to continuity corrections and transforms when per-study mutation counts are small or zero for rare genes. Direct mapping: per-study (gene-mutated, total-sequenced) counts → `rma.glmm(measure="PLO")`. |
| 5 | Lin L & Xu C. "Arcsine-based transformations for meta-analysis of proportions: Pros, cons, and alternatives." *Health Sci Rep* | 2020 | DOI: 10.1002/hsr2.178; OpenAlex: W3044366033 | Core now | 2020 critique of Freeman–Tukey arcsine for meta-analysis of proportions. Argues for **generalized linear mixed models (logit link)** and Bayesian alternatives over arcsine transforms. This is the paper that replaces Barendregt 2013 [@Barendregt2013] as the current-generation default recommendation for pooling proportions. |
| 6 | Barendregt JJ, Doi SA, Lee YY, Norman RE, Vos T. "Meta-analysis of prevalence." *J Epidemiol Community Health* | 2013 | DOI: 10.1136/jech-2013-203104; OpenAlex: W1585424492; PMID: 23963506 | Core now | The canonical Freeman–Tukey double arcsine paper for pooling prevalences. Context read for Lin & Xu 2020's critique. Still widely used in practice; know why we should NOT default to it. |
| 7 | Nyaga VN, Arbyn M, Aerts M. "Metaprop: a Stata command to perform meta-analysis of binomial data." *Arch Public Health* | 2014 | DOI: 10.1186/2049-3258-72-39; OpenAlex: W2133564174 | Core now | The de-facto reference for **meta-analysis of single proportions** (no control arm) — exactly the "per-study mutation-ratio" problem this project has. Covers arcsine vs logit, Wilson/exact CIs, and multiple heterogeneity methods. R equivalent: `meta::metaprop`. |
| 8 | Higgins JPT & Thompson SG. "Quantifying heterogeneity in a meta-analysis." *Stat Med* | 2002 | DOI: 10.1002/sim.1186; OpenAlex: W2126930838 | Core now | Seminal I² paper. Required cite for any heterogeneity diagnostic we report alongside pooled gene-cancer estimates. 36,213 citations. |
| 9 | IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. "Plea for routinely presenting prediction intervals in meta-analysis." *BMJ Open* | 2016 | DOI: 10.1136/bmjopen-2015-010247; OpenAlex: W2464924628 | Core now | Argues prediction intervals (not just pooled CIs) should be routine in random-effects meta-analysis. Directly relevant for reporting per-gene cross-study mutation-rate prediction intervals alongside pooled estimates. Widely cited as the HKSJ practical-guidance paper. |
| 10 | Martínez-Jiménez F, Muiños F, Sentís I, et al. "A compendium of mutational cancer driver genes." *Nat Rev Cancer* | 2020 | DOI: 10.1038/s41568-020-0290-x; OpenAlex: W3047825284 | Core now | IntOGen 2020 — the cancer-genomics-native consensus-voting pipeline that aggregates mutations across **~28,000 samples from ~66 cohorts** for driver discovery. Sits between naive pooling and random-effects meta-analysis (consensus voting rather than effect-size combination). Essential cross-reference when we describe what pipeline-level cancer-genomics aggregation currently looks like and why random-effects is an upgrade. |
| 11 | Tsujimoto Y, Tsutsumi Y, Kataoka Y, et al. "The impact of continuity correction methods in Cochrane reviews with single-zero trials with rare events: A meta-epidemiological study." *Res Synth Methods* | 2024 | DOI: 10.1002/jrsm.1720; OpenAlex: not confirmed in this note; PMID: 38750630 | Relevant next | Empirical 2024 reassessment of 0.5 continuity correction vs. alternatives in sparse/zero-event meta-analysis. Calibrates expectations for how we handle "per-study mutation count is 0 for this gene" rows. |
| 12 | Efthimiou O, Rücker G, Schwarzer G, Higgins JPT, Egger M, Salanti G. "Network meta-analysis of rare events using the Mantel-Haenszel method." *Stat Med* | 2019 | DOI: 10.1002/sim.8158; OpenAlex: not confirmed in this note; PMID: 30997687 | Relevant next | MH for rare events generalised to network meta-analysis. Useful if we eventually attempt cross-cohort gene-level comparisons rather than single-arm prevalence pooling. |
| 13 | Piaget-Rossel R, Taffé P. "Meta-analysis of rare events under the assumption of a homogeneous treatment effect." *Biom J* | 2019 | DOI: 10.1002/bimj.201800381; OpenAlex: not confirmed in this note; PMID: 31172565 | Peripheral monitor | Formalizes the "common true effect" framing for rare-event meta-analysis — useful for contrasting with random-effects assumption when we discuss whether per-study gene rates are genuinely heterogeneous or just noisy. |

## Priority Reading Queue

**Core now (read first):**

1. Langan 2018 [@Langan2018] — which τ² estimator to pick. Closes the DL-vs-REML-vs-PM-vs-SJ debate with simulation data.
2. Lin & Xu 2020 [@LinXu2020] — what to do with proportions specifically. Modern critique of Freeman–Tukey.
3. Stijnen 2010 [@Stijnen2010] — GLMM approach for sparse/zero-event pooling. Directly applicable to per-gene counts.
4. Viechtbauer 2010 [@Viechtbauer2010] — `metafor` as the tool of record.
5. Nyaga 2014 [@Nyaga2014] — single-proportion meta-analysis recipe (what we actually need — no control arm per study).

**Relevant next:**

6. DerSimonian & Laird 1986 [@DerSimonian1986] — seminal citation obligation.
7. Higgins & Thompson 2002 [@Higgins2002] — I² obligation.
8. IntHout 2016 [@IntHout2016] — prediction intervals obligation.
9. Barendregt 2013 [@Barendregt2013] — know why Freeman–Tukey is not our default.
10. Martínez-Jiménez 2020 — cancer-genomics-native aggregation baseline to compare against.
11. Tsujimoto 2024 [@Tsujimoto2024] — zero-event continuity corrections.
12. Efthimiou 2019 [@Efthimiou2019] — network MH extension.

**Peripheral monitor:**

13. Piaget-Rossel 2019 — rare-event common-effect framing.

## Coverage Notes and Gaps

- **Hartung–Knapp–Sidik–Jonkman (HKSJ) primary sources** (Hartung 2001, Sidik & Jonkman 2002 /
  2005) were not retrieved as individual records in this run — they are well covered by
  Langan 2018 [@Langan2018] and IntHout 2016 [@IntHout2016]. Flag as known gap if a future reviewer wants primary cites.
- **Paule–Mandel (1982)** primary paper not retrieved; covered by Langan 2018 [@Langan2018]. Flag as
  potential gap.
- **dmetar / "Doing Meta-Analysis in R" handbook** (2021 Harrer/Cuijpers/Furukawa/Ebert,
  CRC Press) did not surface in OpenAlex — likely because it is a book rather than a
  journal article. Manually record as a reference book in `papers/references.bib`
  BibTeX book entry when adding `dmetar` to the pipeline's dependency list.
- **Bayesian hierarchical pooling of cancer mutation frequencies (`brms` / `rstanarm` / Stan)**:
  no dedicated genomics-application paper found. The closest methodology references are
  Williams, Rast & Bürkner (2018/2019) tutorials — not retrieved this run. Flag as gap; the
  `cross-study-aggregation` modality guide should recommend `brms::brm(... family = binomial,
  (1 | study_id))` as the Bayesian alternative to `metafor::rma.glmm`, but cite Stijnen 2010
  as the methods foundation rather than a genomics-specific example (there doesn't appear
  to be one — genuine research gap).
- **Genomics applications of meta-analytic pooling to somatic-mutation frequencies**: the
  search surfaced essentially zero cancer-genomics papers that run random-effects meta-analysis
  at the per-gene-per-cancer-type level. IntOGen-style consensus voting (Martínez-Jiménez 2020)
  and Bailey 2018 [@Bailey2018] 26-tool consensus are the closest analogues, but neither runs a
  random-effects model. This confirms the "largest methodology gap" framing in
  `topic:cross-study-meta-analysis-cancer-genomics`. **This project would be novel if we
  actually produce per-gene pooled mutation rates with τ² / I² / prediction intervals.**
- **Rare-event methods not covered (Peto one-step OR)**: we did not pull a primary Peto
  1980s reference; Efthimiou 2019 [@Efthimiou2019] covers it indirectly.

## Recommended Next Actions

1. **Default recommendation for the pipeline** (direct input to modality guide t062):
   - Use **GLMM with logit link on per-study (mutated, sequenced) counts** for the primary
     per-gene-per-cancer pooled estimate, via `metafor::rma.glmm(measure="PLO", ...)` (R) or
     equivalent Stan / brms random-intercept binomial model. This handles zero counts natively,
     respects the binomial data-generating process, and scales to thousands of genes.
   - Report **I², τ², and a 95% prediction interval** alongside the pooled estimate
     (Higgins & Thompson 2002 [@Higgins2002]; IntHout 2016 [@IntHout2016]).
   - For K < 30 studies per gene-cancer pair, apply **HKSJ variance adjustment**.
   - Keep **arcsine / Freeman–Tukey** as a disclosed alternative only; do **not** use it as the
     default (Lin & Xu 2020 [@LinXu2020]).
   - Compare pooled estimate against **naive sample-weighted ratio** and against **IntOGen
     consensus** to show value-add.

2. Add BibTeX entries for the 10 Core-now / Relevant-next records to `papers/references.bib`
   (done in this commit).

3. Add compact paper notes under `doc/background/papers/` for Core-now items (done for the 5
   top-priority methodology papers; remaining 5 Core-now deferred to avoid over-lengthening
   this commit — create as tasks via `science-tool tasks add --type research`).

4. Update `doc/background/topics/cross-study-meta-analysis-cancer-genomics.md` `Key References`
   section with the 13 records and unlink the "no strong references" stub line.

5. Feed these references directly into the flesh-out of `doc/guides/modalities/cross-study-aggregation.md`
   (task t062) — especially into a new "Default statistical recipe" subsection.

6. Follow-up search (later, not now): HKSJ primary sources (Hartung 2001, Sidik 2005),
   Paule–Mandel 1982, and a targeted search for any 2023–2026 Bayesian hierarchical
   applications to somatic-mutation frequency pooling.
