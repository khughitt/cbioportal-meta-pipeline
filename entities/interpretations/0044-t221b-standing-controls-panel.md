---
type: interpretation
title: "t221(b): four standing controls lock down the candidate-set verdict \u2014\
  \ the residual is entirely an all-region call-set artifact (6 studies; gone in 84\
  \ exonic-clean ones), the candidates are statistically indistinguishable from known\
  \ CFS genes, germline (dbSNP) leak is not the driver, and no label-free neural set\
  \ reproduces the enrichment"
status: active
created: '2026-06-08'
updated: '2026-06-28'
id: interpretation:0044-t221b-standing-controls-panel
source_refs:
- code/notebooks/t221b_standing_controls_panel.py
- results/neural-gene-standing-controls-2026-06-08/intronic_fraction_stratified_residual.tsv
- results/neural-gene-standing-controls-2026-06-08/per_study_intronic_fraction.tsv
- results/neural-gene-standing-controls-2026-06-08/cfs_positive_control.tsv
- results/neural-gene-standing-controls-2026-06-08/germline_dbsnp_control.tsv
- results/neural-gene-standing-controls-2026-06-08/data_driven_set_sensitivity.tsv
- results/neural-gene-standing-controls-2026-06-08/data_driven_neural_set.tsv
- data/gene_replication_timing.feather
related:
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- question:0032-neural-gene-length-null
- question:0016-panel-induced-ascertainment
- interpretation:0040-t216-label-free-neural-score
- interpretation:0041-t217-genomic-span-cfs-null
- interpretation:0042-t218-cns-exclusion-wes-panel
- interpretation:0043-t221a-sample-level-hypermutator-exclusion
- task:t221
---

# Interpretation: t221(b) — standing-controls panel

Project links: this interpretation continues `task:t221` after
`interpretation:0040-t216-label-free-neural-score`,
`interpretation:0041-t217-genomic-span-cfs-null`,
`interpretation:0042-t218-cns-exclusion-wes-panel`, and
`interpretation:0043-t221a-sample-level-hypermutator-exclusion`.
It bears on `hypothesis:0012-neural-gene-enrichment-length-histology-artifact`,
`question:0032-neural-gene-length-null`, and `question:0016-panel-induced-ascertainment`.

> **Verdict: in `results/neural-gene-standing-controls-2026-06-08/intronic_fraction_stratified_residual.tsv`, four independent controls all point the same way, closing the candidate-set mutational-count
> thread of `hypothesis:0012-neural-gene-enrichment-length-histology-artifact` with no surviving alternative.** (1) **Intronic-fraction stratification** — the t218/t221a
> residual is *entirely* a call-set-region-scope artifact: it lives in the 6 "all-region" WES studies
> (intronic fraction ≥ 0.5; span-matched p **0.0002**) and is **absent** in the 84 exonic-clean studies,
> where the candidates fall to the **20.9th** percentile (p **0.99**). pog570 was merely the largest of a
> 6-study class. (2) **CFS positive control** — the candidates are statistically indistinguishable from
> known common-fragile-site genes (both ~99.8th span percentile, both top-0.2 % raw, both with the same
> span-matched residual). (3) **Germline-leak (dbSNP) control** — candidate variant rows are only 12.7 %
> dbSNP-catalogued, and excluding *every* dbSNP-flagged row leaves the residual intact (p 0.0028 →
> 0.0004), so germline contamination is not the driver. (4) **Set sensitivity** — neither a label-free
> `neural_score` nor `cns_score` top-25 set reproduces the enrichment (both select small genes, ~33–44th
> span percentile, MWU p 0.2–0.5), so the enrichment is *not* a generic neural-gene property — the 9 are
> unusual in being both neural and huge loci.**

- **Task:** `t221`, arm (b) (standing-controls panel). Follows arm (a) (`t221a`, sample-level hypermutator
  exclusion — ruled out).
- **Script:** `code/notebooks/t221b_standing_controls_panel.py`
- **Artifacts:** `results/neural-gene-standing-controls-2026-06-08/` —
  `intronic_fraction_stratified_residual.tsv`, `per_study_intronic_fraction.tsv`,
  `cfs_positive_control.tsv`, `germline_dbsnp_control.tsv`, `data_driven_set_sensitivity.tsv`,
  `data_driven_neural_set.tsv`, datapackage.json.
- **Substrate:** `full` wide `gene_cancer_study.feather` (variant-row counts; validated gene-for-gene in
  `t221a`), per-study `mut_filtered.feather` (consequence + dbsnp_rs, one schema-aware pass),
  `data/gene_replication_timing.feather` (span + constitutive-late-replication class), and the t216
  `gene_neural_enrichment.feather` (`is_cfs` / `is_candidate` / `is_effector` / `neural_score` /
  `cns_score`). `random_seed = 0`, 5,000 null draws.

## Findings

**F1 — The residual is entirely an all-region call-set artifact (`question:0016-panel-induced-ascertainment` / `question:0032-neural-gene-length-null` closed for this thread).**
Stratifying the 91 WES studies by their measured intronic fraction:

| stratum | n studies | candidate median pct | n in top-100 | span-matched p |
|---|---|---|---|---|
| all WES | 91 | 0.250 | 6 | 0.0020 |
| all-region (intronic ≥ 0.5) | 6 | 0.184 | 7 | **0.0002** |
| exonic-clean (intronic < 0.5) | 84 | **20.851** | 0 | **0.9942** |

In `results/neural-gene-standing-controls-2026-06-08/per_study_intronic_fraction.tsv`, the entire span-matched residual is carried by **6 cohorts whose call set tiles whole gene bodies** —
`prad_eururol_2017` (0.93 intronic), `stad_oncosg_2018` (0.91), `prostate_dkfz_2018` (0.85),
`pog570_bcgsc_2020` (0.85), `difg_glass_2019` (0.74), `sclc_cancercell_gardner_2017` (0.52). In the 84
exonic-clean studies the candidates are **not enriched at all** (20.9th percentile, span-matched p ≈ 1).
This generalises t218's single-cohort (pog570) finding: pog570 was the largest member of an all-region
*class*, and the mechanism — variant-row counts of multi-Mb loci scaling with how much intronic territory
a call set reports — is the same one t217 identified (genomic span), amplified by call-set region scope.
**Intronic fraction is the first-class per-study covariate this gene class needs**, distinct from the
WES/panel assay label (these 6 are all `wes`-labelled).

**F2 — The candidates are statistically indistinguishable from known CFS genes (positive control).**
On the full WES totals, the 9 candidates and the 27-gene t216 CFS panel behave almost identically:
in `results/neural-gene-standing-controls-2026-06-08/cfs_positive_control.tsv`, candidates median span percentile **99.77**, median count percentile **0.250**, span-matched p 0.0016,
span+class p 0.0002; CFS panel **99.92**, **0.156**, p 0.000, p 0.000 (23/27 in the top-100). The
candidates *are* CFS-class loci by every measure — the sharpest single confirmation that the enrichment is
a fragile-site/large-locus phenomenon.

**F3 — Germline (dbSNP) leak is not the driver.** In `results/neural-gene-standing-controls-2026-06-08/germline_dbsnp_control.tsv`, across the 90/91 WES studies that record `dbsnp_rs`,
only **12.7 %** of candidate variant rows are dbSNP-catalogued (not germline-dominated). Excluding **every**
dbSNP-flagged row — a deliberately conservative over-exclusion that also drops rare somatic-but-catalogued
variants — leaves the residual intact (span-matched p **0.0028 → 0.0004**; candidate median 0.250 → 0.208).
So leaked common-SNP/germline variants at these large loci do not explain the enrichment. (A true
study-level matched/unmatched-normal split is not available — see caveats — so this is the substrate-derived
germline control in its place.)

**F4 — The enrichment is not a generic neural-gene property (set sensitivity).** In `results/neural-gene-standing-controls-2026-06-08/data_driven_set_sensitivity.tsv`, a data-driven neural set —
the top-25 genes by t216's label-free `neural_score` *or* by the CNS-structural `cns_score`, candidates and
effectors excluded — does **not** reproduce the enrichment. Both sets select small, mutation-poor neuronal /
neuroendocrine genes (PRL, POMC, GH1… by neural_score; SNCB, HPCA, TAGLN3, PACSIN1, SLC1A2… by cns_score):
median span percentile **33–44**, median count percentile **38–53**, **0** in the top-100, MWU p 0.18–0.52,
span-matched p 0.18–0.31. Label-free neural specificity selects *small* genes; the candidates are the rare
intersection of high neural specificity **and** huge genomic locus. The hand-picked 9 are therefore not
representative neural genes — they are representative **large CNS-structural / CFS** genes, and the enrichment
travels with the CFS panel (F2), not with the neural label (this F4). This is the direct mutation-count
analogue of t216's expression-level result (a neural score cannot beat a size-matched CFS control).

## Bearing on `hypothesis:0012-neural-gene-enrichment-length-histology-artifact` — the candidate-set thread is closed from four sides

Across the program the candidate-set mutational-count thread now has every non-span explanation tested and
rejected: not coding length (t217 Arm A), dissolves under genomic span (t217 Arm B / F2 here), no positive
selection (t217 dndscv 0/9), not CNS histology (t218 F1), not panel ascertainment (t218 F2), not
hypermutators at the sample level (t221a), not germline leak (F3 here), and not a generic neural property
(F4 here) — while the one surviving residual is fully localised to a 6-study all-region call-set class (F1)
and the candidates are quantitatively CFS genes (F2). As with t218/t221a, this is recorded as strong
supporting evidence for the **candidate-set mutational-count thread** of
`hypothesis:0012-neural-gene-enrichment-length-histology-artifact`; `hypothesis:0012` (proposed)
and `question:0032` (active) are intentionally left in their prior states — one thread does not flip the
hypothesis, and other threads in `hypothesis:0012-neural-gene-enrichment-length-histology-artifact`
(expression/histology beyond mutation counts) are out of scope here.

## Decision & redirect

1. **t221 is complete** (arms (a) hypermutator + (b) standing controls). The QA battery is green; the
   candidate-set thread has no surviving residual.
2. **Promote `intronic_fraction` to a standing per-study covariate** (alongside `is_late_cl`) for any
   large-gene mutation-count analysis — it is the call-set-region-scope axis that the WES/panel label misses
   and that F1 shows carries the entire residual. The 6 all-region cohorts are a reusable flag list
   (`per_study_intronic_fraction.tsv`).
3. **Populate `matched_normal_studies` in `config-full.yml`** to enable a true matched/unmatched-normal
   stratification on a future run; F3's dbSNP control is the substrate-derived stand-in until then.
4. The data-driven neural covariate (`gene_neural_enrichment`) is confirmed usable only **size-controlled**
   (t216 decision #1): raw, it selects small genes that are not the candidate class.

## Caveats

- **No study-level matched-normal split.** `config-full.yml` carries no `matched_normal_studies` list, and
  substrate proxies (`sample_id_norm` barcode presence) conflate matched-normal with assay type
  (TCGA/pog record normal barcodes; msk_impact is matched but records none). Section 3 therefore tests
  germline leak via dbSNP membership instead — the purpose matched-normal sequencing serves — and the
  study-level split is deferred to a config update.
- **dbSNP exclusion is conservative.** Dropping all `rs...` rows over-excludes rare somatic-but-catalogued
  variants, so F3 is an upper bound on germline contamination, not a germline-only filter; the residual
  surviving even this over-exclusion is the strong direction.
- **One unclassifiable study.** 1/91 WES studies lacks a `consequence` column, so its intronic fraction is
  undefined; it is excluded from the F1 strata (but contributes to `all_wes` via the wide table).
- **`full` only / variant-row substrate.** Arm (b) targets the powered residual on variant-row counts (the
  substrate the span confound lives in); pan-cancer is underpowered (t218) and the sample-level ratio view
  is a separate question.
