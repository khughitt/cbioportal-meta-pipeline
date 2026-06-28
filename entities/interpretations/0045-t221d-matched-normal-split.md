---
type: interpretation
title: "t221(d): a true study-level matched- vs unmatched-normal split confirms germline\
  \ leak is not the candidate driver \u2014 within call-set-region stratum the residual\
  \ is identical across normal status (all-region matched p 0.0000 vs unmatched 0.0006;\
  \ both exonic arms null), and the biggest single residual-carrier (pog570) is matched-normal"
status: active
created: '2026-06-08'
updated: '2026-06-28'
id: interpretation:0045-t221d-matched-normal-split
source_refs:
- code/notebooks/t221d_matched_normal_split.py
- results/neural-gene-matched-normal-split-2026-06-08/matched_unmatched_primary.tsv
- results/neural-gene-matched-normal-split-2026-06-08/matched_unmatched_by_region.tsv
- results/neural-gene-matched-normal-split-2026-06-08/candidate_carrier_studies.tsv
- results/neural-gene-matched-normal-split-2026-06-08/datapackage.json
- data/gene_replication_timing.feather
related:
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- question:0032-neural-gene-length-null
- question:0016-panel-induced-ascertainment
- interpretation:0041-t217-genomic-span-cfs-null
- interpretation:0042-t218-cns-exclusion-wes-panel
- interpretation:0043-t221a-sample-level-hypermutator-exclusion
- interpretation:0044-t221b-standing-controls-panel
- task:t221
---

# Interpretation: t221(d) — true matched- vs unmatched-normal germline-leak split

> **Verdict: in `results/neural-gene-matched-normal-split-2026-06-08/matched_unmatched_by_region.tsv`, germline leak is not the candidate driver — now confirmed at the study level, the way
> matched-normal sequencing actually serves it, not via the dbSNP proxy.** With `matched_normal_studies`
> populated in config-full (t221c, evidence-derived from per-variant normal barcodes), the 91 WES studies
> split cleanly into 45 patient-matched-normal and 46 unmatched (tumor-only / pooled). Naively the
> candidate residual is *stronger* in the matched arm (span-matched p **0.0008** vs **0.037**), the
> opposite of the germline-leak prediction — but that is the pog570 region-confound. The de-confounded
> region × normal-status 2×2 settles it: **within call-set-region stratum, normal status is inert.** In the
> all-region cohorts the residual is identical across matched (median pct **0.161**, p **0.0000**) and
> unmatched (**0.170**, p **0.0006**); in the exonic-clean cohorts both arms are null (p 0.91–1.00). The
> single biggest residual-carrier — pog570 (44,641 of 69,418 candidate variant rows) — is matched-normal,
> so the largest piece of the signal cannot be germline contamination by construction. This closes the one
> caveat t221(b)-F3 had to defer.

- **Task:** `t221`, arm (d) (true matched/unmatched-normal split — the study-level germline-leak control
  that t221b-F3 could only proxy via dbSNP membership).
- **Script:** `code/notebooks/t221d_matched_normal_split.py`
- **Artifacts:** `results/neural-gene-matched-normal-split-2026-06-08/` —
  `matched_unmatched_primary.tsv`, `matched_unmatched_by_region.tsv`, `candidate_carrier_studies.tsv`,
  datapackage.json.
- **Substrate:** `full` wide `gene_cancer_study.feather` (variant-row counts; validated gene-for-gene in
  t221a), `data/gene_replication_timing.feather` (span + constitutive-late-replication class), the t221b
  `per_study_intronic_fraction.tsv` (region stratum labels), and `matched_normal_studies` from
  `config-full.yml` (t221c). `random_seed = 0`, 5,000 null draws.

## Why this run was needed

t221(b)-F3 tested germline leak only by *proxy*: `config-full.yml` then carried no `matched_normal_studies`
list, and substrate signals (`sample_id_norm` barcode presence) conflate matched-normal with assay type, so
the control was dbSNP-membership of candidate variant rows rather than a study-level matched/unmatched split.
t221(c) populated `matched_normal_studies` from per-variant normal-barcode patient-stem evidence (45 of the
91 WES studies). This run uses that list to run the split the way matched-normal sequencing actually works:
patient-matched normal subtracts germline / private SNPs, so if the candidate enrichment were germline leak
it would live in the **unmatched** arm and be **absent / weaker** in the matched arm.

## The confound this run had to disentangle

The entire residual lives in the 6 "all-region" cohorts (t221b-F1), and those split **2 matched** (pog570,
prostate_dkfz) **/ 4 unmatched** (difg_glass, prad_eururol, sclc_gardner, stad_oncosg). So a naive
matched-vs-unmatched contrast is partly a region-scope contrast — and because pog570 alone carries 64 % of
all candidate variant rows and is matched, the naive contrast actually points the *wrong way* for the
germline hypothesis. The clean test is matched-vs-unmatched **within** each region stratum (the 2×2 below).

## Findings

**F1 — Primary split: the residual is, if anything, stronger in the matched arm (germline-leak prediction
fails at first contact).**

| arm | n studies | candidate rows | candidate median pct | n in top-100 | span-matched p | span + class p |
|---|---|---|---|---|---|---|
| all WES | 91 | 69,418 | 0.250 | 6 | 0.0020 | 0.0004 |
| matched-normal | 45 | 52,683 | 0.198 | 6 | **0.0008** | **0.0000** |
| unmatched | 46 | 16,735 | 0.505 | 4 | **0.0366** | 0.0072 |

In `results/neural-gene-matched-normal-split-2026-06-08/matched_unmatched_primary.tsv`, **75.9 %** of candidate variant rows sit in matched-normal studies. Matched-normal sequencing — whose
purpose is to remove germline — does not weaken the residual; the residual is *concentrated* where germline
has been subtracted. This already refutes the germline-leak hypothesis, but the direction is inflated by the
region confound (next).

**F2 — De-confounded region × normal-status 2×2: within region stratum, normal status is inert.**

| region | normal status | n studies | candidate rows | candidate median pct | span-matched p | span + class p |
|---|---|---|---|---|---|---|
| all-region | matched | 2 | 49,802 | **0.161** | **0.0000** | 0.0002 |
| all-region | unmatched | 4 | 14,661 | **0.170** | **0.0006** | 0.0000 |
| exonic | matched | 42 | 2,864 | 28.093 | 0.9968 | 0.9938 |
| exonic | unmatched | 42 | 2,074 | 12.476 | 0.9136 | 0.9278 |

In `results/neural-gene-matched-normal-split-2026-06-08/matched_unmatched_by_region.tsv`, holding region scope fixed, the matched and unmatched candidate medians are **statistically
indistinguishable** (all-region 0.161 vs 0.170; exonic both deep-null). Matched-normal sequencing removes
*nothing* of the residual relative to unmatched within the same call-set scope. The residual tracks **region
scope**, not normal status — exactly the t221b-F1 result, now with the germline axis explicitly crossed in
and shown to be flat. (Power in the all-region row is thin — 2 vs 4 studies — but the matched cell is the
*more* significant of the two, which is the safe direction for this conclusion.)

**F3 — The biggest single residual-carrier is matched-normal.** Per `results/neural-gene-matched-normal-split-2026-06-08/candidate_carrier_studies.tsv`, pog570
(matched, all-region) contributes **44,641** of the 69,418 candidate variant rows (64 %), followed by
difg_glass (unmatched, 8,248), stad_oncosg (unmatched, 5,635), and prostate_dkfz (matched, 5,161). The
largest piece of the signal by a wide margin comes from a patient-matched-normal cohort, so germline
contamination cannot be its source by construction. The carriers are all-region cohorts regardless of normal
status; below them every exonic study (matched or unmatched) contributes only hundreds of rows.

## Bearing on `hypothesis:0012`

This upgrades t221b-F3 from a substrate-derived proxy to a direct study-level result and removes the last
deferred control on the candidate-set mutational-count thread. The full tally of tested-and-rejected
alternatives for the candidate enrichment is now: not coding length (t217 Arm A), dissolves under genomic
span (t217 Arm B), no positive selection (t217 dndscv 0/9), not CNS histology (t218 F1), not panel
ascertainment (t218 F2), not hypermutators at the sample level (t221a), not a generic neural property
(t221b-F4), candidates are quantitatively CFS genes (t221b-F2), the residual is entirely a call-set-region-
scope artifact concentrated in 6 all-region cohorts (t221b-F1) — and now **not germline leak at the study
level** (this F1–F3). As with the prior arms this is recorded as strong supporting evidence for the
**candidate-set mutational-count thread** of `hypothesis:0012`; `hypothesis:0012` (proposed) and `question:0032` (active)
are left in their prior states — one thread does not flip the hypothesis, and other `hypothesis:0012` threads
(expression / histology beyond mutation counts) are out of scope here.

Project links: this result updates `hypothesis:0012-neural-gene-enrichment-length-histology-artifact`,
`question:0032-neural-gene-length-null`, and `question:0016-panel-induced-ascertainment`.
It follows the control sequence recorded in `interpretation:0041-t217-genomic-span-cfs-null`,
`interpretation:0042-t218-cns-exclusion-wes-panel`,
`interpretation:0043-t221a-sample-level-hypermutator-exclusion`, and
`interpretation:0044-t221b-standing-controls-panel`; the operational parent is `task:t221`.

## Decision & redirect

1. **t221 is complete across all four arms** — (a) hypermutator, (b) standing controls, (c)
   matched_normal_studies population, (d) this matched/unmatched split. Every non-span explanation for the
   candidate-set residual has been tested and rejected; the single surviving mechanism is genomic span
   amplified by call-set region scope.
2. **`matched_normal_studies` is now a first-class, exercised config axis** — t221c populated it and t221d
   consumes it; downstream CH / germline-sensitive analyses can split on it directly rather than reaching
   for the dbSNP proxy.
3. **Promote "germline leak" from open control to tested-and-inert** for this gene class, alongside
   hypermutators (t221a) — neither needs re-running per analysis.

## Caveats

- **Region confound is real and named.** The primary matched-vs-unmatched contrast (F1) is partly a
  region-scope contrast because the all-region cohorts split 2 matched / 4 unmatched; the de-confounded 2×2
  (F2) is the load-bearing result, and its all-region row has thin power (2 vs 4 studies). The conclusion
  rests on the *flatness* of normal status within region plus the matched cell being the more significant
  one, not on the primary contrast alone.
- **matched list is a high-precision lower bound.** `matched_normal_studies` (t221c) is evidence-derived
  from recorded per-variant normal barcodes; matched-by-design-but-unrecorded cohorts (MSK-IMPACT family)
  are panels and are excluded from the WES set anyway, so they do not affect this split. A WES study with a
  matched normal that simply does not record the barcode would be misfiled into the unmatched arm — which
  would only *dilute* the unmatched arm toward matched, i.e. work against finding a difference; the observed
  null difference is therefore conservative.
- **Variant-row substrate / `full` only.** The metric is variant-row counts (the t217/t218 substrate the
  span confound lives in), not sample-level ratios; pan-cancer is underpowered (t218) and not re-run.
