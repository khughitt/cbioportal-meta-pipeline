---
id: "discussion:2026-04-24-gene-length-bias-in-mutation-rankings-and-literature"
type: "discussion"
title: "Gene length as a confounder: mutation rankings and literature attention"
status: "in-progress"
source_refs:
  - "paper:Lawrence2014"
  - "paper:Martincorena2017"
  - "paper:Bailey2018"
  - "paper:Chang2016"
  - "paper:Imielinski2017"
created: "2026-04-24"
updated: "2026-04-24"
focus_type: "topic"
focus_ref: "topic:mutation-rate-normalization"
mode: "standard"
related:
  - "topic:mutation-rate-normalization"
  - "question:q003-replication-timing-as-gene-level-mutation-rate-confounder"
  - "question:q007-cross-tissue-somatic-mutation-rate-variation-as-null-model"
  - "task:t082"
  - "task:t086"
---

# Discussion: Gene length as a confounder — mutation rankings and literature attention

## Focus

Two coupled questions. (1) Is gene length a confounder the cancer-genomics field routinely
adjusts for when identifying "highly mutated" / driver genes? (2) Does gene length also
confound the *literature-attention* side — are long genes over-represented in PubMed because
they are mutation-hits in more experiments, independent of biological importance? Our pipeline
currently emits a length-normalized ratio (`mean_adj = mean / protein_length`) alongside raw
counts; the question is whether that is defensible, sufficient, or misleading, and whether an
analogous bias contaminates the "is this gene well-studied" axis.

## Current Position

- Pipeline output: `gene_cancer_study_ratio_annotated.feather` carries both raw per-sample
  ratios and a protein-length-divided version. UniProt single-isoform protein length is used;
  genes without UniProt entries get a median-length fallback (no indicator column yet —
  `t086`).
- Audit stance (`doc/meta/bias-audit-cross-study-aggregation-pipeline.md`): length
  normalization is judged "necessary but not sufficient" — it catches first-order bias but
  misses regional mutation-rate covariates (replication timing, chromatin state, expression).
  The audit rates protein-length-only as "pass-with-caveat."
- MutSigCV / dNdScv / SLAPenrich all explicitly model gene length in their null. Bailey 2018's
  299-driver consensus is what "the field" uses; the pipeline currently does NOT reproduce
  a discovery-grade null model.
- Literature-bias question has not been examined in this project previously — it's a novel
  framing worth a first pass.

---

## Q1. Is adjusting for gene length standard practice in cancer-gene discovery?

**Yes, for discovery; inconsistently, for descriptive lists.** Every serious driver-discovery
tool in the last 15 years models gene length in the null — MutSigCV (Lawrence 2013, 2014),
MuSiC (Dees 2012), dNdScv (Martincorena 2017), OncodriveFML, SLAPenrich (Iorio 2018), Chang
2016's per-codon hotspot model. The difference length-aware correction makes is large: Lawrence
2014 specifically demonstrates that without background correction, **long genes like TTN
(~35 kb CDS), MUC16, OBSCN, RYR2, and LRP1B appear as top "drivers"** — these are the canonical
false positives cited in that paper and are essentially never endorsed by the consensus
lists that correct for length (Bailey 2018).

Where it breaks down is in **secondary reporting**: review articles, news pieces, and many
pan-cancer descriptive summaries still quote "top mutated genes" as raw-count or raw-frequency
lists, which re-introduces the bias MutSigCV was invented to remove. cBioPortal's default
"Mutated Genes" tab in the study view is raw recurrence, not length-adjusted — a user
browsing the portal sees the same confound unless they dig into MutSig results (when present).

**How our pipeline sits.** Dividing by protein length gives a crude rate (mutations /
residue). That is the minimum any credible ranking should do, and it is below the 2013 bar
(MuSiC added covariates). The big wins from MutSigCV-style covariates (expression, replication
timing, chromatin) are approximately orthogonal to length and are the reason length-only still
over-ranks heterochromatic / replication-late genes (this is `question:q003`). So: length
normalization is standard where discovery rigor is required, patchy where rankings are
informal, and length-only is a floor, not a ceiling.

## Q2. Are long genes over-represented in the literature for length-correlated reasons?

**Almost certainly yes, and for several independent reasons that compound.** No paper I'm aware
of has tried to quantify the specific "literature attention ∝ gene length" slope — it would
be publishable if done carefully. Mechanisms that plausibly drive it:

1. **Mutation-count confound propagates to publications.** Every cancer genomics paper that
   lists "top mutated genes" in its abstract or figure 1 is a citation event for that gene.
   If raw mutation-count is length-biased, and raw mutation-count is what's reported, the
   publication record inherits the length bias at a high rate. This is the dominant effect.
2. **Antibody / reagent availability tracks protein size weakly.** Larger proteins have more
   epitopes, more commercial antibodies, and more domain structure to publish on. This
   produces an independent (but smaller) length ∝ study-probability channel.
3. **Functional annotation density.** Longer proteins tend to have more annotated domains,
   more PTMs, more interaction partners in BioGRID / STRING. This isn't *because* they are
   studied more — but it gives more "things to write about" per gene, which increases
   publications per gene conditional on attention.
4. **Structural-biology tractability runs the opposite direction.** Very long proteins are
   harder to crystallize and harder to model (AlphaFold2 length limits, disordered-region
   fraction). So the "structural" sub-literature may under-represent long genes. This
   is a partial anti-correlate that would show up only in that slice.
5. **Network-degree confound.** Longer proteins have more PPIs on average (mechanistic: more
   surface area + more domains). PPI degree correlates with publication count directly
   (hub-protein effect, well known from yeast / PPI studies). Length → degree → publications
   is a separate path from mutation-count.

**So: yes — and the effect is a superposition of at least one large channel (mutations) and
several smaller independent channels.** The concerning implication is that "this gene is
important because it's both highly mutated AND well-studied" is not independent corroboration
— both axes share gene length as a common cause.

## Q3. What has the literature done about length / size biases on each axis?

**Mutation side.** Extensively studied and operationalized:
- Lawrence 2013 (MutSigCV): explicit length-and-covariate null, the field reference.
- Martincorena 2017 (dNdScv): selection-based ratio that is length-aware by construction
  (non-synonymous vs synonymous per gene, trinucleotide-aware).
- Bailey 2018: 26-tool consensus that triages raw-count top-hits as "likely false-positive
  long-gene artifacts" unless ≥2 tools agree.
- Chang 2016: per-codon hotspot null that further refines within-gene position-level bias.
- SLAPenrich (Iorio 2018): length and per-sample rate in the null; our best off-the-shelf
  pathway-level analogue to what we already do for genes.

**Literature side.** Much less formal work. What exists:
- Gillis & Pavlidis 2014 ("Assessing identity...in bioinformatics") and its follow-ups
  documented that gene-level analyses concentrate on a small set of "popular" genes and
  that popularity correlates with technical attributes. They don't isolate length cleanly.
- Stoeger & Nunes Amaral 2018 ("Large-scale investigation of the reasons why potentially
  important genes are ignored"): the landmark paper on this question. They model
  publication count per gene and find that a small number of **chemical and experimental
  accessibility features** predict publication count orders-of-magnitude better than
  biological importance — and gene / transcript length is one of those features. Worth
  a dedicated `paper:` summary.
- Haynes 2018, Edwards 2011 ("Too many roads not taken"): commentary-level — lab reagent
  availability and prior publication drive future publication (rich-get-richer).
- NCBI / NIH analyses: gene mention frequency in PubMed follows a heavy-tailed distribution;
  the long tail of unstudied genes is huge (~20% of protein-coding genes have <5 papers).
  Length is not the only driver of this — chromosome of discovery, year of cloning, and
  disease association matter more — but length is a documented secondary correlate.

**So: the mutation side is handled well at the methodology level and routinely violated at
the reporting level; the literature side is known to be confounded by accessibility features
including length, per Stoeger 2018, but no one has isolated the length slope specifically in
a cancer context.** This is a publishable gap.

## Q4. How would the top-N list shift under length adjustment?

Two comparisons to run, ordered by effort:

**Cheap first pass (1–2 hours, within this repo).** We already have
`gene_cancer_study_ratio_annotated.feather` with both `mean_inclusive` and the per-gene
protein length joined. Sort by `mean_inclusive` vs `mean_inclusive / protein_length` and
compute the Spearman correlation + Jaccard overlap at N = 10, 50, 100, 500, 1000.

**What I expect to see** (based on Lawrence 2014 and everything downstream):
- Top ~30 dominated by *recognized drivers* (TP53, KRAS, PIK3CA, APC, PTEN, BRAF, EGFR,
  BRCA1/2, CDKN2A, NRAS, IDH1, SMAD4, FBXW7, NF1). Most of these are *short-to-medium*
  proteins (PIK3CA ~1,068 aa; KRAS 189 aa; IDH1 414 aa; TP53 393 aa). These will *rise*
  under length normalization. KRAS especially — 189 aa and extremely recurrent — will jump
  to the top of the adjusted list in a way that reflects biology.
- Top ~100 (unadjusted) will contain TTN, MUC16, OBSCN, RYR2/3, LRP1B, USH2A, CSMD1/3,
  FAT1/4, PKHD1, DNAH-family, ZFHX4, SYNE1. These are the textbook long-gene passengers.
  Under length adjustment they crash out of the top 100 (Lawrence 2014 essentially showed
  this for TCGA pan-cancer and it replicated across every follow-up).
- Top ~500 starts to include *genuinely large* bona fide cancer genes that will lose rank
  unfairly: ATM (3,056 aa), BRCA2 (3,418 aa), NF1 (2,818 aa), APC (2,843 aa), MLL / KMT2A-C
  family, ARID1A (2,285 aa). These are long AND real drivers. A pure length division
  penalizes them. This is the failure mode of length-only normalization and the reason the
  field moved to covariate models (MutSigCV) and selection-based models (dNdScv). The dNdScv
  rule — large genes with *enriched truncating* mutations relative to expectation — rescues
  them correctly.
- Jaccard @ top-100 between raw and length-adjusted: my rough expectation is ~0.5–0.7.
  @ top-500: ~0.7–0.85. The movement is concentrated in the ranks you care about (top 30
  is where biology lives and where length adjustment is most clarifying).

**Deeper comparison (harder, requires external tools).** Run dNdScv over the combined
cohort and compare to our raw and length-adjusted rankings. The pipeline already has
`code/scripts/run_dndscv.R`; it is not part of `rule all` by default. This would give us a
three-way comparison (raw / length-adjusted / selection-adjusted) and is the cleanest
answer to "what does length adjustment actually buy, and where does it break?"

## Q5. What other biases confound mutation counts and literature counts?

**Mutation-count biases** (most already tracked in the audit):
- **Regional mutation rate / replication timing.** Large — ~10× between early- and
  late-replicating regions (Lawrence 2014). Not captured by length. `question:q003`.
- **Chromatin state / heterochromatin.** Co-varies with replication timing; both channels are
  what MutSigCV covariates capture that length misses.
- **Sequence-context / trinucleotide.** Genes rich in CpG dinucleotides get more C>T
  transitions under aging / SBS1 signature exposure. This is actually a *gene-composition*
  bias distinct from length. dNdScv and Chang 2016 correct for it.
- **Panel coverage and target-capture bias.** Targeted panels (MSK-IMPACT, FoundationOne)
  enrich for known cancer genes. Counts from those studies are not comparable to WES counts.
  `task:t086` tracks this.
- **Matched-normal vs unmatched calling.** Affects germline leakage, CH contamination
  (Coombs 2018), normal-tissue mutations. `topic:clonal-hematopoiesis-contamination`.
- **Gene-symbol drift over time.** HGNC alias mapping not yet done (`task:t082`). Older
  studies may use superseded symbols; raw joins lose or duplicate counts. This biases toward
  "stable long-standing symbols" which tends to mean longer, earlier-characterized genes.
- **Isoform selection for length.** Our protein length is single-isoform UniProt canonical.
  Some genes (especially titin, MLL-family) have dramatic isoform length variation. Audit
  flagged as MEDIUM severity; revisit if the adjusted ranking changes materially.
- **Hypermutator samples.** Already handled inclusive/exclusive via `t081`.
- **Cohort ascertainment / tissue selection.** Different studies sample different
  primary/metastatic/pre-treated mixes; `t052`.

**Literature-count biases** (new territory for this project):
- **Rich-get-richer citation dynamics.** Prior publication predicts future publication
  more strongly than any biological attribute (Stoeger 2018). A gene that got lucky in 1995
  has a 30-year head start.
- **Reagent / antibody / knockout-mouse availability.** These all correlate with length
  (more antibodies for larger proteins, more surface epitopes) but also with accessibility.
- **Disease-association priors.** A gene mentioned in a disease-gene database (OMIM, CGC)
  gets drastically more citations than comparable un-associated genes — independent of
  biological importance. This is circular for cancer-gene questions.
- **Gene name canonicalization.** PubTator is good at this but not perfect. Common-word
  names (CAT, SET, ACE, PAX) get mis-tagged; rare symbols get missed entirely. Gillis &
  Pavlidis-style identity drift over decades of papers is a real effect.
- **Publication language / model organism.** Drosophila / yeast / mouse gene names contaminate
  PubTator counts if species filtering is imperfect. Human-only filter is essential.
- **Preprint / grey-literature coverage.** PubMed excludes bioRxiv; for a "what is the field
  currently studying" question this matters more each year. The 5-15-year window the user
  proposed helps stabilize identity but gets progressively weaker at capturing currency.
- **Review-article inflation.** A single review mentioning 200 genes inflates all 200 by one
  paper each. Mention-counts are not citation-weighted in PubTator output. Downstream
  weighting by mention-type (primary research vs review) could matter.

---

## Evidence Needed

1. **Empirical top-N comparison** (raw vs length-adjusted, N = 10/50/100/500). Cheap.
2. **Three-way comparison including dNdScv** over combined cBioPortal cohort. Medium cost.
3. **Gene-length × PubMed-mention regression**. Using the PubTator counts at
   `/data/proj/lit-explore/pubtator/2026-01-16/counts/gene_concept_ids.feather` +
   UniProt lengths, fit log(mention_count) ~ log(length) + log(cBioPortal_mutation_count),
   on protein-coding genes, 2010-2024 window. Report: slope of length after controlling for
   mutation count. If slope is non-zero, length has an independent effect on literature
   attention beyond mutation-count mediation. Replicate with a cancer-gene subset (CGC / Bailey
   299) to check if the effect differs inside vs outside canonical cancer genes.
4. **Stoeger 2018 paper summary**. Read and summarize — it is the methodological reference
   for this entire question and we don't have it catalogued.
5. **Three top-N lists side-by-side**: raw, length-adjusted, dNdScv-selected. Check correlation
   with PubTator mention counts on each. If length-adjusted and dNdScv both show substantially
   weaker correlation with mention-count than raw does, that is direct evidence that length
   drives both.

## Prioritized Follow-Ups

| Priority | Action | Why now | Dependencies |
|---|---|---|---|
| P1 [actionable now] | Add a marimo notebook under `code/notebooks/` comparing top-N gene rankings from `gene_cancer_study_ratio_annotated.feather` sorted by `mean_inclusive` vs `mean_inclusive / protein_length`. Report Spearman, Jaccard@10/50/100/500, and a labeled scatterplot with TTN-family vs canonical-driver callouts. | We already have both columns; this is a ~1 hour task that settles Q4 concretely. | Pipeline has run with current config. |
| P1 | New question `q011-gene-length-as-literature-attention-confounder.md` in `doc/questions/`. Frame the regression model, datasets, pre-registered expectation. | Captures the novel framing from this discussion so it doesn't get lost. | None. |
| P2 | New task: `length × PubMed-mention regression` pipeline step. Inputs: PubTator gene counts (filtered for 2010+, human-only), UniProt lengths, CGC / Bailey driver list, cBioPortal per-gene mutation count. Outputs: length slope estimates with and without mutation-count adjustment; per-gene "attention residual" column. | Directly addresses Q2 and Q5-lit. | Requires HGNC/NCBI-Gene ID join between PubTator and UniProt. |
| P2 | Paper summary `doc/papers/Stoeger2018.md` using `science:research-papers`. | Methodological reference for the literature-bias side. | None. |
| P2 | Opt dNdScv into `rule all` in a side config (`config-pan-cancer-dndscv.yml`), accepting the cost. Then emit a three-way ranking comparison report. | Closes the "length-only is below the 2013 bar" finding. Addresses `topic:mutation-rate-normalization` directly. | R env (`feedback:R-reproducibility-pipeline-tasks` — dndscv rule must use conda env YAML, not system R). |
| P3 | Add `length_is_fallback` indicator column in `create_combined_gene_cancer_freq_table.py` (already tracked as `t086`). | Transparency about which genes got median-imputed length. | None. |
| P3 | In any publication-ready ranking output, include both `mean_inclusive` and `mean_inclusive_per_kb` with a clear note that the latter is a first-order correction only; point readers to dNdScv output when available. | Prevents the pipeline from silently reproducing the bias the audit called out. | None. |

## Synthesis

The field answer is clear: gene length is a known and well-modeled confounder for
mutation-rate-based gene ranking; formal driver-discovery tools all correct for it; review-
and portal-level reporting still routinely fails to. Our pipeline sits at the floor of what
is defensible (length division) and is below the 2013 methodology bar (MutSigCV covariates,
dNdScv selection). This is acknowledged in the audit and is a known gap, not a surprise.

The interesting and under-explored claim coming out of this discussion is that **gene length
likely confounds the literature-attention axis too, partly through shared mediation via
mutation counts (long genes hit more top-N lists → more papers cite them) and partly through
independent channels (antibodies, PPI degree, annotation density)**. If that is true, then
"well-studied" and "highly mutated" are not independent pieces of evidence about biological
importance — they share a common cause. Stoeger & Nunes Amaral 2018 is the closest existing
work; a cancer-specific replication using PubTator + cBioPortal is a clean, feasible analysis
and is not, as far as I know, published.

Two concrete commitments come out of this:
1. Run the cheap top-N comparison now (length-adjusted vs raw) and publish the result as a
   notebook. This is ~1 hour and settles Q4 empirically for our cohort.
2. Register a new question for the literature-attention regression and scope a task for it.
   This is the genuinely novel analytical contribution the discussion has surfaced.

Everything else (dNdScv integration, isoform-aware length, Stoeger summary) is already
tracked or derivative of existing roadmap items.
