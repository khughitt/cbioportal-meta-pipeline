---
type: search
title: Co-occurrence and mutual exclusivity detection methods in cancer somatic mutation
  data
status: active
created: '2026-04-13'
updated: '2026-04-13'
id: search:0001-cooccurrence-mutual-exclusivity-methods
---

# Co-occurrence / Mutual Exclusivity Methods — 2026-04-13

## Search Focus

Survey the methodological landscape for detecting **co-occurrence** and **mutual exclusivity**
between somatic alterations in cancer cohorts. Primary motivation: the cbioportal pipeline
already computes per-study gene-gene correlation matrices
(`code/scripts/create_correlation_matrices.py`); the next planned step is to formalize
cross-study co-occurrence / mutual-exclusivity statistics with proper null models (sample-specific
background rates, permutation controls, pathway awareness). This search identifies the canonical
methods plus any newer 2020-2026 work we should compare against.

Required anchors (verify + characterize): **DISCOVER**, **SELECT**, **WeSME**, **FishHook**,
**CoMEt**. Extended set: MEMo, Dendrix, Multi-Dendrix, MEGSA, TiMEx, WExT, Mutex, MEMCover,
plus 2022-2026 methods and any benchmark / review papers.

## Query Set

1. **Broad conceptual** — `mutual exclusivity cancer somatic mutation detection` (OpenAlex);
   `"mutual exclusivity"[TI] cancer` sorted by date (PubMed).
2. **Methods-anchor lookup** — named-method queries for each of: DISCOVER (Canisius/Wessels),
   SELECT (Mina/Ciriello), WeSME (Kim/Przytycka), FishHook (Imielinski/Meyerson), CoMEt
   (Leiserson/Raphael), MEMo (Ciriello/Schultz), Dendrix (Vandin/Raphael), Multi-Dendrix,
   MEGSA (Hua/Shi), TiMEx (Constantinescu/Beerenwinkel), WExT (Leiserson/Raphael), Mutex
   (Babur/Sander), MEMCover (Kim/Przytycka).
3. **Mechanism / pathway-aware** — `pathway-informed mutual exclusivity driver`;
   `network-based driver identification mutual exclusivity`.
4. **Benchmark / review** — `benchmark "mutual exclusivity" cancer`;
   `review "mutual exclusivity" cancer driver methods`.
5. **Recent window (2022-2026)** — `"mutual exclusivity" cancer 2022:2026[PDAT]`;
   `epistasis cancer driver interactions somatic mutation`.
6. **Confounder** — epistasis framing; clonal-hematopoiesis contamination context.

## Sources and Run Metadata

- Primary sources: **OpenAlex** `/works?search=...` (candidate expansion) + **PubMed** E-utilities
  (`esearch` + `esummary`) for precise named-method resolution.
- Retrieved: 2026-04-13.
- Shared runtime (`uv run science-tool literature search ...`): **not available** (`science-tool`
  has no `literature` subcommand in the current project install). Direct APIs used instead.
- OpenAlex contact: `mailto=khughitt@umd.edu`. PubMed unauthenticated (no `NCBI_API_KEY`).
- Candidates retrieved (across all query variants, after dedupe): ~52.
- Shortlisted records in this report: **20** (+ 4 recent context items flagged peripheral).
- Dedup order: DOI -> PMID -> normalized title+year. OpenAlex preferred for citation counts,
  PubMed preferred for PMIDs and journal metadata.

## Ranked Results

| # | Citation (short) | Year | IDs | Tier | Why it matters |
|---|---|---|---|---|---|
| 1 | Canisius S, ..., Wessels LFA. "A novel independence test for somatic alterations in cancer shows that biology drives mutual exclusivity but chance explains most co-occurrence." *Genome Biol* | 2016 | PMID: 27986087 / DOI: 10.1186/s13059-016-1114-x / OpenAlex: W2949363897 | **Core now** | **DISCOVER**. The canonical sample-specific-background-rate independence test. Uses per-tumor expected mutation probabilities (Poisson binomial) so it does not penalize exclusivity artifacts arising from tumor-mutation-burden heterogeneity. Directly applicable as a null model for cross-study frequency aggregation. |
| 2 | Mina M, ..., Ciriello G. "Discovering functional evolutionary dependencies in human cancers." *Nat Genet* | 2020 | PMID: 32989323 / DOI: 10.1038/s41588-020-0703-5 / OpenAlex: W3090808618 | **Core now** | **SELECT**. Detects functional genetic interactions (synergy, exclusivity) while controlling for lineage and mutation-burden covariates. Corrects the earlier critique of naive co-occurrence testing; the correct 2020 reference for SELECT (the task brief cited "Cell 2020" but the method paper is Nat Genet 2020; the 2017 Cancer Cell "Conditional Selection..." paper is the conceptual precursor). |
| 3 | Imielinski M, Guo G, Meyerson M. "Insertions and Deletions Target Lineage-Defining Genes in Human Cancers." *Cell* | 2017 | PMID: 28089356 / DOI: 10.1016/j.cell.2016.12.025 / OpenAlex: W2573077199 | **Core now** | **FishHook**. Introduces the Gamma-Poisson regression framework ([https://github.com/mskilab-org/fishHook](https://github.com/mskilab-org/fishHook)) used for background-rate-corrected mutation recurrence detection (chromatin state, replication timing, nucleotide context covariates). Key reference for *coverage/background* normalization that the cbioportal gene-coverage filter currently only approximates. |
| 4 | Kim YA, Cho DY, Przytycka TM. "WeSME: uncovering mutual exclusivity of cancer drivers and beyond." *Bioinformatics* | 2017 | PMID: 27153670 / DOI: 10.1093/bioinformatics/btw242 / OpenAlex: W2963382551 | **Core now** | **WeSME**. Weighted-sampling null that preserves per-sample mutation rates while testing mutual exclusivity — a pragmatic, tractable alternative to DISCOVER's closed-form independence test. Also scales to pathway/module-level tests. |
| 5 | Leiserson MDM, ..., Raphael BJ. "CoMEt: a statistical approach to identify combinations of mutually exclusive alterations in cancer." *Genome Biol* | 2015 | PMID: 26253137 / DOI: 10.1186/s13059-015-0700-7 / OpenAlex: W1911343030 | **Core now** | **CoMEt**. Exact tail-enumeration test for *sets* (not just pairs) of mutually exclusive alterations; supports subtype-specific testing. Reference design for moving beyond pairwise gene-gene matrices into module detection. |
| 6 | Ciriello G, Cerami E, Sander C, Schultz N. "Mutual exclusivity analysis identifies oncogenic network modules." *Genome Res* | 2012 | PMID: 21908773 / DOI: 10.1101/gr.125567.111 / OpenAlex: W2144940507 | **Core now** | **MEMo**. The seminal statistical + network-module approach; 743 citations; still the field benchmark. Establishes the co-mutation vs. network-linked framing the cbioportal pipeline implicitly operates within. |
| 7 | Vandin F, Upfal E, Raphael BJ. "De novo discovery of mutated driver pathways in cancer." *Genome Res* | 2012 | PMID: 21653252 / DOI: 10.1101/gr.120477.111 / OpenAlex: W2121443461 | **Core now** | **Dendrix**. Original coverage-exclusivity weight function + MCMC / greedy pathway discovery without requiring a prior pathway database. |
| 8 | Leiserson MDM, Blokh D, Sharan R, Raphael BJ. "Simultaneous Identification of Multiple Driver Pathways in Cancer." *PLoS Comput Biol* | 2013 | DOI: 10.1371/journal.pcbi.1003054 / OpenAlex: W2042851051 / PMID: [UNVERIFIED — from OpenAlex; not yet reconfirmed via esummary] | Relevant next | **Multi-Dendrix**. Extends Dendrix to discover multiple driver pathways jointly; key when cancer-type-specific co-occurrence modules need to be separated. |
| 9 | Babur O, Gonen M, Aksoy BA, Schultz N, Ciriello G, Sander C, Demir E. "Systematic identification of cancer driving signaling pathways based on mutual exclusivity of genomic alterations." *Genome Biol* | 2015 | PMID: 25887147 / DOI: 10.1186/s13059-015-0612-6 / OpenAlex: W2141811925 | Relevant next | **Mutex**. Pathway-aware mutual-exclusivity detection that uses a curated signaling-network prior; complementary to network-free approaches. |
| 10 | Hua X, ..., Shi J. "MEGSA: A Powerful and Flexible Framework for Analyzing Mutual Exclusivity of Tumor Mutations." *Am J Hum Genet* | 2016 | PMID: 26899600 / DOI: 10.1016/j.ajhg.2015.12.021 / OpenAlex: W2287386959 | Relevant next | **MEGSA**. Likelihood-ratio-based general framework; explicitly benchmarks power against CoMEt, MEMo, muex. Useful reference for power analysis design. |
| 11 | Constantinescu S, ..., Beerenwinkel N. "TiMEx: a waiting time model for mutually exclusive cancer alterations." *Bioinformatics* | 2016 | PMID: 26163509 / DOI: 10.1093/bioinformatics/btv400 / OpenAlex: W2154444902 | Relevant next | **TiMEx**. Generative waiting-time model — interprets exclusivity via tumor-evolution process rather than pure independence testing. |
| 12 | Leiserson MDM, Reyna MA, Raphael BJ. "A weighted exact test for mutually exclusive mutations in cancer." *Bioinformatics* | 2016 | PMID: 27587696 / DOI: 10.1093/bioinformatics/btw462 / OpenAlex: W2592761229 | Relevant next | **WExT**. Exact-test extension with per-sample weights (bridges WeSME ideas with CoMEt exactness). |
| 13 | Kim YA, ..., Przytycka TM. "MEMCover: integrated analysis of mutual exclusivity and functional network reveals dysregulated pathways across multiple cancer types." *Bioinformatics* | 2015 | PMID: 26072494 / DOI: 10.1093/bioinformatics/btv247 / OpenAlex: not confirmed in this note | Relevant next | **MEMCover**. Cross-cancer-type integration of mutual-exclusivity modules — the most directly analogous prior art to what cbioportal's cross-study aggregation is trying to produce. |
| 14 | Mina M, Iyer A, ..., Ciriello G. "Conditional Selection of Genomic Alterations Dictates Cancer Evolution and Oncogenic Dependencies." *Cancer Cell* | 2017 | PMID: 28756993 / DOI: 10.1016/j.ccell.2017.06.010 / OpenAlex: not confirmed in this note | Relevant next | The *conceptual* precursor to SELECT — introduces conditional-selection framing. Useful when writing the rationale section for why naive co-occurrence is biased. |
| 15 | van de Haar J, Canisius S, ..., Ideker T. "Identifying Epistasis in Cancer Genomes: A Delicate Affair." *Cell* | 2019 | PMID: 31150618 / DOI: 10.1016/j.cell.2019.05.005 / OpenAlex: W2947209894 | **Core now** | Perspective / methodological critique. Documents specific failure modes (confounding by cohort composition, mutation-rate heterogeneity) that pan-cancer co-occurrence methods must address. Required reading before claiming any cross-study co-occurrence result. |
| 16 | Mina M, Ciriello G. "Epistasis and evolutionary dependencies in human cancers." *Curr Opin Genet Dev* | 2022 | PMID: 36182742 / DOI: 10.1016/j.gde.2022.101989 / OpenAlex: W4297464117 | Relevant next | 2022 topical review; good compact introduction to the current problem framing. |
| 17 | Van Daele D, Marchal K. "OMEN: network-based driver gene identification using mutual exclusivity." *Bioinformatics* | 2022 | PMID: 35552634 / DOI: 10.1093/bioinformatics/btac312 / OpenAlex: W4280544300 | Peripheral monitor | 2022 network-based method; worth tracking but cites low (~6). |
| 18 | Wang X, ..., Begg CB. "Adaptation of a mutual exclusivity framework to identify driver mutations within oncogenic pathways." *Am J Hum Genet* | 2024 | PMID: 38232729 / DOI: 10.1016/j.ajhg.2023.12.009 / OpenAlex: not confirmed in this note | Relevant next | 2024 adaptation layered on top of DISCOVER/MEGSA-style frameworks — relevant if we want to embed oncogenic-pathway priors. |
| 19 | Shuaibi A, Raphael BJ. "A latent variable model for evaluating mutual exclusivity and co-occurrence between driver mutations in cancer." *bioRxiv* | 2024 | DOI: 10.1101/2024.04.24.590995 / PMID: 38712136 | Peripheral monitor | 2024 preprint — latent-variable model; worth tracking for peer-reviewed version. |
| 20 | Spinou A, ..., Kemmeren P. "A pathway-informed mutual exclusivity framework to detect genetic interactions in pediatric cancer." *BMC Med Genomics* | 2025 | PMID: 41388546 / DOI: 10.1186/s12920-025-02289-z / OpenAlex: not confirmed in this note | Peripheral monitor | 2025; pediatric-cancer-specific but demonstrates the pathway-prior design pattern on small cohorts (relevant for cbioportal's rarer cancer types with low sample counts). |

## Priority Reading Queue

**Core now (read first):**

1. **Canisius 2016 — DISCOVER** — the most directly applicable null model for what the pipeline
   is about to build.
2. **van de Haar 2019 — Epistasis: A Delicate Affair** — read this *before* writing any
   cross-study co-occurrence code. It is the cautionary tale.
3. **Mina 2020 — SELECT** — current-generation covariate-aware method; defines the bar.
4. **Kim 2017 — WeSME** — pragmatic permutation-style alternative; simpler to implement and
   reason about in a Snakemake rule than DISCOVER's Poisson-binomial.
5. **Imielinski 2017 — FishHook** — background-rate framework that complements exclusivity
   testing on the other axis (gene-level significance).

**Relevant next:**

6. Leiserson 2015 — CoMEt (extension to set-level exclusivity).
7. Ciriello 2012 — MEMo (foundational framing + network module layer).
8. Vandin 2012 — Dendrix (coverage-exclusivity weight function).
9. Leiserson 2013 — Multi-Dendrix (multi-pathway extension).
10. Babur 2015 — Mutex (pathway-prior variant).
11. Hua 2016 — MEGSA (likelihood-ratio framework, power-analysis comparisons).
12. Constantinescu 2016 — TiMEx (evolutionary / waiting-time interpretation).
13. Leiserson 2016 — WExT (weighted-exact-test bridge).
14. Kim 2015 — MEMCover (cross-cancer-type integration — closest prior art).
15. Mina 2017 — Conditional Selection (SELECT conceptual precursor).
16. Mina & Ciriello 2022 — review (current framing).
17. Wang 2024 — pathway-prior DISCOVER adaptation.

**Peripheral monitor:**

18. Van Daele 2022 — OMEN (network-based variant).
19. Shuaibi 2024 — latent-variable preprint.
20. Spinou 2025 — pediatric pathway-informed variant.

## Coverage Notes and Gaps

- **No recent (2022-2026) comprehensive benchmark** of mutual-exclusivity methods on a
  standardized test set was found. The 2016 MEGSA paper, the 2018 Zhang & Zhang review
  (PMID: 28113329), and the 2019 van de Haar perspective remain the closest things to a
  comparative reference. This is a **real gap** — the project could contribute here by
  benchmarking DISCOVER vs. WeSME vs. SELECT on cross-study cBioPortal data.
- **Cross-study (not cross-cancer-type) aggregation of co-occurrence statistics** is nearly
  absent from the literature. MEMCover (2015) integrates across cancer types within one cohort
  (TCGA); there is no published method that pools DISCOVER/WeSME/CoMEt *p*-values across
  independent studies with different panels. This is arguably a methodological contribution the
  project could target directly.
- **Clonal-hematopoiesis confounding** as a co-occurrence artifact is not systematically
  addressed in the named methods (DISCOVER/SELECT/WeSME/CoMEt all assume somatic calls are
  tumor-intrinsic). Cross-link to the existing Bolton 2020 reference in
  `doc/background/papers/Bolton2020.md` and the `annotate_ch.py` pipeline step.
- **Panel-heterogeneity handling** (GENIE vs MSK-IMPACT vs WES): only FishHook-style covariate
  regression and the coverage-weighting in WExT/WeSME address this explicitly. Formalize this as
  an input-side correction before running any cross-panel co-occurrence test.
- **Copy-number / structural-variant co-occurrence**: all primary anchors here are SNV/indel
  focused. Extending to CNV is future scope (also an explicit "Out of Scope" item in
  `specs/research-question.md`, but worth a marker).
- **Dendrix original PMID not confirmed via a direct `esearch` for the exact name "Dendrix"** —
  the paper at PMID 21653252 is the canonical reference (Vandin/Upfal/Raphael 2011/2012 *Genome
  Res*) but the tool name "Dendrix" is in the supplement, not the title; verified via the method
  description, but flagged here as a citation-hygiene note.

## Recommended Next Actions

1. Convert the 20 ranked records into per-paper stubs under `doc/background/papers/` (6 Core now
   stubs created in this pass; remaining 14 to be created as tasks by `science:review-tasks` or
   `/science:research-paper` follow-ups).
2. Add BibTeX entries for all 20 to `papers/references.bib` (done in this pass).
3. Create a new topic note `doc/background/topics/co-occurrence-mutual-exclusivity-methods.md`
   consolidating the method taxonomy (pair-level vs set-level; frequentist vs generative;
   with/without network prior; with/without per-sample covariates).
4. Before implementing a new `create_cooccurrence_matrices.py` rule, pre-register (via
   `/science:pre-register`) the choice between DISCOVER and WeSME as the primary null model and
   define the cross-study meta-analysis strategy (Stouffer weighted-Z vs hierarchical model).
5. Queue a follow-up focused search: "cross-study / cross-cohort meta-analysis statistics for
   gene-pair mutation frequencies" — this is a genuine gap surfaced above.
