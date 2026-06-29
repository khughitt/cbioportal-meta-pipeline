---
type: topic
title: Cross-panel normalization methods for targeted cancer sequencing
status: active
created: '2026-04-13'
updated: '2026-06-28'
id: topic:cross-panel-normalization-methods
ontology_terms: []
source_refs: []
related:
- topic:targeted-panel-sequencing-bias
- topic:tumor-mutational-burden
- topic:cross-study-harmonization
- topic:cross-study-meta-analysis-cancer-genomics
- paper:AACRGENIEConsortium2017
- paper:Pugh2022
- paper:Zehir2017
- paper:Ellrott2018
- paper:Chakravarty2017
- paper:ChakravartySolit2021
- task:t026
- task:t060
---

# Cross-panel normalization methods for targeted cancer sequencing

## Summary

`topic:targeted-panel-sequencing-bias` defines *why* naive pooling of mutation
counts across MSK-IMPACT / FoundationOne / Tempus / Caris / GENIE is biased.
This topic surveys the *methods* that have been proposed to fix it —
panel-intersection analyses, per-(study, gene) callability denominators,
explicit TMB calibration to WES (Friends of Cancer Research TMB Harmonization
Project Phase I/II, Buchhalter et al. [@Buchhalter2019], Fancello et al. [@Fancello2019]), and more recent
panel-aware statistical tooling. The central organizing idea: every per-gene
rate or per-sample burden computed on panel data has a denominator that is
panel-specific, and any cross-panel comparison must either (a) restrict to a
common denominator or (b) model the denominator explicitly.
This methods note is the denominator-focused companion to
`topic:cross-study-harmonization` and `topic:cross-study-meta-analysis-cancer-genomics`.

## Key Concepts

### Two normalization families

**(A) Panel-intersection.** Restrict all cross-study comparisons to the set of
regions (or, more coarsely, genes) *callable on every contributing panel*.
Pro: denominators are identical by construction. Con: rapidly loses signal —
the GENIE v1 44-gene core shrinks to roughly 30 genes at v9.1 (91 panels), and
to an empty set if a WES study is added. At the region level, even "both
panels cover TP53" hides exon-by-exon differences.

**(B) Callable-denominator (aka callable-length correction).** Keep all
per-(study, panel) data but weight each observation by its panel-specific
callable coding length:

  rate_{study,gene} = mutations_{study,gene} / (N_samples_{study} × bp_callable_{study,gene})

This converts per-gene counts into per-Mb-per-sample rates that are panel-
comparable (to first order). It requires:
  1. The panel BED file (or equivalent callable region mask).
  2. Per-gene intersection of that BED with a canonical coding annotation
     (Ensembl/RefSeq CCDS).
  3. Variant-level filtering consistent with the BED (e.g., coding only,
     exclude intronic baits).

Most published pipelines use (B) implicitly in TMB (mutations / coding Mb
callable), but few extend it to per-gene rates.

### What "callable" means operationally

- **BED-level callable.** The panel manufacturer's target BED = regions
  designed to be covered. Available for MSK-IMPACT and GENIE member panels
  (via Synapse `syn24179663`); not released for most commercial FoundationOne
  / Tempus / Caris panels.
- **Depth-filtered callable.** Per-sample: regions sequenced above a
  caller-specific depth threshold (e.g., `GATK CallableLoci ≥ 20×`,
  `samtools depth ≥ 10×`). More accurate denominator but requires BAMs, which
  are rarely distributed with public summary MAFs.
- **Pseudo-callable from empirical variant density.** If BEDs are unavailable,
  infer per-(panel, gene) coverage from the set of genes with ≥1 variant call
  across the full panel cohort. Conservative (silent regions with zero
  variants look "uncovered"); only usable for large genes in large cohorts.

### Calibration-style TMB harmonization (Friends of Cancer Research model)

The **FoCR TMB Harmonization Project** (Merino et al. [@Merino2020] Phase I; Vega et al. [@Vega2021] Phase
II) established the dominant TMB cross-panel method. The approach:

1. Process the same reference samples (Phase I: in silico down-sampling of
   TCGA exomes; Phase II: 29 FFPE tumors + 10 cell lines distributed to 16
   labs) through each panel pipeline and a WES reference pipeline.
2. Fit a per-panel calibration curve mapping panel-TMB → WES-TMB (usually
   linear; intercept often nonzero because panels enrich for driver-rich
   genes).
3. Classification accuracy (TMB-high vs TMB-low at a clinical cutoff) is
   reported as PPA/NPA.
4. Phase II released a public software tool for applying the per-panel
   calibrations.

Key Phase-II quantitative findings:
- Panel sizes **>~667 kb** are required to maintain useful PPA/NPA at clinical
  TMB cutoffs; below that, stochastic TMB noise dominates.
- Filtering germline and pathogenic variants meaningfully shifts panel TMB;
  filtering rules must be spelled out per panel.
- Calibration reduces between-panel TMB variance to within-lab variance
  levels; without calibration, cross-panel TMB comparisons are not reliable
  at clinical cutoffs.

Buchhalter et al. [@Buchhalter2019] ("Size matters", Int J Cancer) reached a similar conclusion
independently by in silico down-sampling a WES cohort: variance in TMB
estimates scales ~1/panel_size, with practical floor around 1 Mb.

### Gene-level analogs of TMB calibration

The TMB calibration model (linear regression, per-panel intercept+slope) has
not been broadly extended to per-gene mutation rates. Two partial approaches
exist:

- **Panel-size-adjusted rates** (rate = mutations / (samples × panel_Mb))
  ignore gene-specific structure; a panel that covers TP53 fully but only
  exon 2 of APC will inflate APC rates.
- **Per-gene callable-fraction rates** (rate = mutations / (samples × gene_
  callable_bp)) condition on the gene — this is what the AACR GENIE
  AACR Project GENIE Consortium [@AACRGENIEConsortium2017] APC ~10× example implicitly argues for, and what
  `process_genie_panel_coverage.py` in this repo computes.
  The project paper notes behind this point include `paper:AACRGENIEConsortium2017`,
  `paper:Pugh2022`, `paper:Zehir2017`, `paper:Ellrott2018`, `paper:Chakravarty2017`,
  and `paper:ChakravartySolit2021`.

### Panel-version drift within a single vendor

For `task:t070`, MSK-IMPACT is itself four panels (341 → 410 → 468 → 505 genes) that accreted
genes across clinical-release cycles:

- 2014–2016: 341-gene panel.
- 2016–2018: 410-gene panel.
- 2018–2021: 468-gene panel.
- 2021+: 505-gene panel.

A sample run on IMPACT-341 in 2015 is "not callable" for the genes
IMPACT-468 added in 2018. Treating these as "not mutated" (rather than "not
observed") inflates the absent-variant cell count in the denominator of any
pooled MSK-IMPACT rate computation.

FoundationOne has a similar version history (F1 → F1CDx → F1H → F1L with
evolving gene lists), as does Tempus xT (V2/V3/V4/V5).

### Matched-vs-unmatched normal as a secondary axis

Cross-panel normalization alone does not make cohorts comparable when some
are matched-normal (MSK-IMPACT: ~98%) and others are predominantly tumor-only
(GENIE overall: 52% tumor-only per Pugh et al. [@Pugh2022]). Tumor-only cohorts retain
germline + CH variants that matched-normal pipelines subtract — see
`topic:clonal-hematopoiesis-contamination`. Any callability-denominator
normalization should carry a matched-normal flag.

## Current State of Knowledge

**Settled (across the panel-methods literature):**

1. Naive pooling is biased. AACR GENIE 2017 documented the problem with the
   APC example; every subsequent panel-methods paper treats it as given.
2. Panel size below ~1 Mb callable coding makes TMB estimates unreliable at
   clinical cutoffs (Buchhalter et al. [@Buchhalter2019]; Vega et al. [@Vega2021]; Fancello et al. [@Fancello2019]).
3. Linear calibration per panel sufficiently reduces cross-panel TMB variance
   for clinical binary classification (Vega et al. [@Vega2021]).
4. Panel BEDs are necessary input for any principled correction; only GENIE
   publishes them at population scale (Pugh et al. [@Pugh2022], Synapse `syn24179663`).
5. MC3 (Ellrott et al. [@Ellrott2018]) provides a panel-free WES baseline for TCGA samples and
   eliminates panel heterogeneity entirely for the TCGA portion of any cohort
   (if the analyst is willing to drop the non-TCGA portion or treat MC3 as a
   single panel alongside the panels).

**Contested / unresolved:**

1. **Intersection vs callable-denominator at the gene-rate level.** FoCR /
   Vega / Buchhalter all operate at the TMB level. No consortium has
   published an analogous "gene-rate harmonization" across MSK-IMPACT,
   FoundationOne, Tempus, Caris simultaneously.
2. **Depth thresholds.** Panel manufacturers use different per-variant depth
   thresholds (F1CDx ~250–500×; MSK-IMPACT ~500×; some research cohorts
   50–100×). Whether the BED itself or the BED ∩ depth-threshold region is
   the "right" denominator remains study-dependent.
3. **Fusions / large indels / TERT promoter.** These are panel-specific
   design decisions that are rarely normalized out; most panel harmonization
   papers report coding-SNV rates only.
4. **Non-coding / regulatory hotspots.** TERT promoter, CDKN2A promoter, and
   intronic hotspots appear on some panels (MSK-IMPACT, FoundationOne) but
   not others. Panel intersection at the SNV level misses these by default.

## Controversies & Open Questions

1. **Per-gene linear calibration — feasible or not?** Applying the FoCR-style
   per-panel slope-and-intercept model to a per-gene rate is in principle
   straightforward but has never been empirically validated at scale. Partial
   coverage (a gene covered by only some panels) breaks the regression.
2. **What to do with FoundationOne / Tempus / Caris when BEDs are
   proprietary?** Options: (a) exclude from cross-study analyses (loses
   ~50%+ of published cohorts), (b) treat the published gene list as a
   proxy-BED and lose sub-gene resolution, (c) infer callability empirically.
   No consensus.
3. **Is panel-intersection ever the right choice?** Proponents argue it
   preserves interpretability and avoids over-correcting. Critics note the
   44-gene GENIE core excludes most of the interesting long-tail biology
   (e.g., ARID1A, BAP1, histone genes) at the full GENIE scale.
4. **How to handle within-vendor panel version drift in pooled outputs?**
   Concretely: should an MSK-IMPACT-341 sample contribute a "0" or a "NA" for
   a gene added in IMPACT-468? Current cBioPortal practice treats everything
   as a single pooled MSK cohort; a principled analysis would mask.
5. **Does normalization interact with cohort-selection bias?** The largest
   panels (MSK-IMPACT, FoundationOne) are deployed disproportionately on
   metastatic / pre-treated patients; the smaller panels in GENIE are
   deployed disproportionately on earlier-stage disease. Panel normalization
   alone cannot separate panel effect from cohort-stage effect. See
   `topic:cohort-selection-bias-representativeness`.

## Relevance to This Project

The pipeline currently:

- Ingests per-study MAFs with no per-(study, gene) callability mask applied
  at the ratio step.
- Uses `.mean(skipna=True)` across per-study columns when pooling to
  `gene_cancer_study_ratio.feather`, which silently drops studies where a
  gene is "not on panel" — but does not distinguish that from "on panel,
  genuinely unmutated." (Audit F2 / task `t076`.)
- Has `process_genie_panel_coverage.py` wired to ingest GENIE per-assay BEDs
  (Synapse `syn24179663`); output can be joined in as a `gene_callable:
  bool` column.
- Has no analog for MSK-IMPACT panel-version drift across a single cBioPortal
  study (audit F6 / task `t070`).
- Has no TMB-harmonization step; `topic:tumor-mutational-burden` and task
  `t081` cover that vertical.

The methods catalog in this topic informs three concrete pipeline choices
the repo has to make:

1. **For panel-intersection restriction:** determine the overlap of panel
   BEDs across all `studies:` in a run config, intersect with the gene list,
   emit a `run_panel_intersection.bed` + mask the output tables to that BED.
   Simple but data-costly.
2. **For callable-denominator weighting:** compute per-(study, gene)
   callable_bp from the ingested BEDs, write a `gene_callable_bp` column, and
   report `mutations / (samples × callable_bp / 1000)` as a per-kb rate
   alongside the current sample-level ratio. This is the approach the
   `process_genie_panel_coverage.py` script was designed to support. It
   requires filling BEDs for non-GENIE studies (MSK-IMPACT from cBioPortal
   study definitions; commercial panels from published gene lists as a
   fallback).
3. **For TMB-style harmonization (future):** re-use the FoCR per-panel
   calibration if / when we compute per-sample TMB from our ingested MAFs;
   tooling from Vega et al. [@Vega2021] is publicly released.

## Pipeline Implications

1. **Closes audit F2 properly** once per-(study, gene) callability is joined:
   NA vs 0 disambiguated, `.mean(skipna=True)` replaced by a callable-weighted
   pooled rate. Task: `t076`.
2. **Inputs the modality-guide `panel-mutation-data.md` expansion** (task
   `task:t060`): the guide's checklist items `panel.03` (callable-denominator)
   and `panel.04` (panel-version drift) are directly operationalized by the
   methods catalogued here.
3. **Provides the framework for `t081` (TMB-aware sample exclusion /
   covariate).** Any per-sample TMB our pipeline computes should go through
   FoCR-style calibration if reported cross-panel.
4. **Informs meta-analysis choices in `t077` (GLMM-logit pooling) and
   `t079` (pre-registration).** If the pooled random-effects rate uses a
   sample-level denominator, the study-level random intercept absorbs panel
   effects only noisily; a cleaner formulation puts `callable_bp` on the
   exposure side of the GLMM offset.

Earlier coverage and panel-ingest scaffolding is tracked under `task:t026`; the current
callability and guide work mostly flows through `task:t060`.

## Tooling & Implementation

- **`process_genie_panel_coverage.py`** (in `code/scripts/`): ingests GENIE
  v9.1 per-assay BEDs from Synapse `syn24179663`; output is per-(assay,
  gene) callable_bp. Currently wired to a Snakemake rule; output not yet
  joined into ratio tables.
- **`jasonwong-lab/TMB`** (GitHub): published two-layer Poisson panel→WES
  TMB correction (Nat Rev Clin Oncol 2024 review cites this lineage).
- **FoCR Phase II tool** (Vega et al. [@Vega2021] supplementary): per-panel calibration
  coefficients for Phase-II participating panels; public release
  specifically to promote reproducibility.
- **GATK `CallableLoci`** / **`mosdepth`**: depth-threshold callable region
  computation when BAMs are available. Not applicable to our summary-MAF
  ingest path, but relevant if we ever process cBioPortal raw BAM-level
  releases (not planned).
- **Ensembl / RefSeq CCDS**: canonical coding annotation used to intersect
  panel BEDs with gene-level coding regions. The pipeline already carries
  `data/grch37.tsv` and `data/grch38.tsv` which are sufficient for this.

## Key References

- Merino et al. [@Merino2020]. "Establishing guidelines to harmonize tumor
  mutational burden (TMB): in silico assessment of variation in TMB
  quantification across diagnostic platforms: phase I of the Friends of
  Cancer Research TMB Harmonization Project." *J Immunother Cancer* 8(1):
  e000147. PMID 32217756.
  → Phase-I in silico down-sampling result; established the pipeline.
- Vega et al. [@Vega2021]. "Aligning tumor mutational burden (TMB)
  quantification across diagnostic platforms: phase II of the Friends of
  Cancer Research TMB Harmonization Project." *Ann Oncol* 32(12):
  1626–1636. PMID 34606929.
  → Empirical Phase-II multi-lab calibration; panel-size floor ~667 kb;
  public calibration tool.
- Buchhalter et al. [@Buchhalter2019]. "Size matters: Dissecting key parameters for
  panel-based tumor mutational burden analysis." *Int J Cancer* 144(4):
  848–858. PMID 30238975.
  → Independent in-silico down-sampling result reaching ~1 Mb floor.
- Fancello et al. [@Fancello2019]. "Tumor mutational burden quantification from
  targeted gene panels: major advancements and challenges." *J Immunother
  Cancer* 7:183. PMID 31307554.
  → Review-style survey of panel-TMB methods; good entry point to the
  calibration literature.
- AACR Project GENIE Consortium [@AACRGENIEConsortium2017]. PMID 28572459.
  → 44-gene core; APC ~10× callable-region example; the seminal framing.
- Pugh et al. [@Pugh2022]. PMID 35819403.
  → 91-panel v9.1; per-assay BEDs in Synapse `syn24179663` = the only
  population-scale open BED corpus.
- Zehir et al. [@Zehir2017]. PMID 28481359.
  → MSK-IMPACT 341/410/468 panel-version history + matched-buffy-coat
  design.
- Ellrott et al. [@Ellrott2018]. PMID 29596782.
  → MC3 unified-WES TCGA recall; the "escape hatch" from panel
  heterogeneity for the TCGA portion.
- ChakravartySolit2021. PMID 33762738.
  → Review of clinical-profiling panels; abstracts the cross-vendor
  design-decision landscape (abstract-read).
