---
type: interpretation
title: "Panel-induced ascertainment \u2014 combined pan-cancer rankings are WES-dominated,\
  \ while panel-only rankings carry a smaller, assay-shaped driver surface"
status: active
created: '2026-04-29'
updated: '2026-06-28'
id: interpretation:0015-q016-panel-induced-ascertainment
date: '2026-04-29'
related:
- task:t154
- question:0016-panel-induced-ascertainment
- hypothesis:0003-gene-length-confounds-literature-attention
- task:t129
- interpretation:0013-t149-loso-replication
prior_interpretations:
- 2026-04-28-t149-loso-replication
---

# Panel-Induced Ascertainment

Project links: this interpretation follows `task:t154` and `task:t129`, with
`interpretation:0013-t149-loso-replication` as the replication-analysis context.

## Question

Task `t154` asks whether panel-only, WES-only, and combined mutation rankings differ enough that
the `hypothesis:0003-gene-length-confounds-literature-attention` / `question:0011-gene-length-as-literature-attention-confounder` literature-attention regression (`t129`) must include assay stratum as a covariate.

## Method

`code/scripts/analyze_panel_wes_ascertainment.py` consumes the existing pan-cancer build:

- `summary/mut/table/gene_cancer_pooled_input.feather`
- `summary/mut/table/gene_cancer_study_ratio_annotated.feather`
- `summary/mut/table/three_way_ranking_comparison.feather`

It maps `panel_class in {large_hybrid_capture, small_amplicon}` to `panel` and
`panel_class in {WES, MC3}` to `wes`, restricts the comparison to cancer types with at least one
panel study and one WES study, then builds callability-aware `y_total / n_total` rankings for
`wes`, `panel`, and `combined` strata.

Outputs:

- `/data/packages/cbioportal/pan-cancer/summary/panel_wes_ascertainment/cancer_type_eligibility.feather`
- `/data/packages/cbioportal/pan-cancer/summary/panel_wes_ascertainment/stratum_gene_cancer_rankings.feather`
- `/data/packages/cbioportal/pan-cancer/summary/panel_wes_ascertainment/topk_overlap.feather`
- `/data/packages/cbioportal/pan-cancer/summary/panel_wes_ascertainment/attention_regression.feather`

## Findings

### F1 -- 27 cancer types have both panel and WES evidence

The evaluable mixed-assay set contains 27 cancer types. Every mixed cancer type has exactly one
panel study in this run (`msk_met_2021`) and between 2 and 8 WES studies. The largest WES support
is Soft Tissue Sarcoma (8 WES studies), Hepatobiliary Cancer (6), Non-Small Cell Lung Cancer (6),
and a group of 5-WES cancers including Bladder, Breast, Colorectal, Head and Neck, and Melanoma.

This means the panel-vs-WES comparison is informative as an ascertainment check, but not a
balanced design: the combined ranking is expected to be WES-dominated.

### F2 -- Combined top-K is almost identical to WES top-K

At K=100, WES-vs-combined overlap is 97/100 (Jaccard 0.942), and the shared-pair rank Spearman is
0.999. At K=25, WES-vs-combined overlap is 24/25 (Jaccard 0.923).

This is not surprising given the denominators: WES top-100 median `n_total` is 5,654, combined
top-100 median `n_total` is 6,621, while panel top-100 median `n_total` is only 314.

Conclusion: in the current pan-cancer build, "combined" is effectively a WES-weighted ranking for
the mixed-assay cancers.

### F3 -- Panel-only top-K is related but materially different

Panel-vs-WES overlap is moderate:

| K | Intersection | Jaccard | Recovery each way |
|---:|---:|---:|---:|
| 25 | 20 / 25 | 0.667 | 0.80 |
| 100 | 71 / 100 | 0.550 | 0.71 |

The panel top-15 still recovers canonical drivers, but it contains assay-shaped high-frequency
entries such as `TERT` in Bladder Cancer, Skin Cancer Non-Melanoma, and Melanoma. These are real
cancer genes, not obvious artifacts, but their prominence reflects panel design and metastatic
cohort composition more strongly than the WES-dominated combined ranking.

### F4 -- Driver recovery is lower in panel-only rankings

Bailey driver recovery [@Bailey2018]:

| K | WES | Panel | Combined |
|---:|---:|---:|---:|
| 10 | 1.000 | 0.900 | 1.000 |
| 25 | 0.960 | 0.840 | 0.960 |
| 100 | 0.890 | 0.730 | 0.880 |
| 500 | 0.746 | 0.658 | 0.726 |

CGC tier-1 recovery remains high but also drops in panel-only rankings at broader K:
K=100 is 1.000 for WES/combined and 0.890 for panel.

Interpretation: panel-only high-frequency rankings remain biologically enriched, but the panel
surface is narrower and less Bailey-concordant than WES at the same K.

### F5 -- Literature-attention slopes differ sharply by assay stratum

Regression form:

`log10(PubTator mentions + 1) ~ log10(protein length) + log10(mean stratum mutation rate)`

| Stratum | n genes | beta length | beta rate | Spearman attention-rate |
|---|---:|---:|---:|---:|
| WES | 17,918 | -0.078 | 0.679 | 0.195 |
| Panel | 465 | -0.571 | 0.988 | 0.286 |
| Combined | 17,918 | -0.078 | 0.679 | 0.196 |

The combined regression is numerically identical to WES because the combined ranking is
WES-dominated and covers the same gene universe. The panel regression covers only 465 genes and
has a much larger mutation-rate slope. This supports including assay stratum in `t129`: otherwise
the literature-attention model will estimate a WES/global effect and silently ignore the panel
surface.

## Verdict

**Supportive for `question:0016-panel-induced-ascertainment`.** Panel-induced ascertainment is present. It does not overturn the current
combined pan-cancer ranking because the combined signal is WES-dominated, but the panel-only
ranking is materially different: lower top-K overlap with WES, smaller denominators, lower Bailey
recovery, and a distinct attention-rate slope.

## Recommendation

`t129` should include assay stratum explicitly. At minimum, report WES and panel regressions
separately alongside the combined model. A single combined literature-attention regression is acceptable as a
headline only if it is labeled WES-dominated for this run.

For future configs with more panel studies, rerun this script before interpreting any
literature-attention or ranking-stability result. The current conclusion depends on the active
study mix: one panel study versus multiple WES studies per evaluable cancer type.

## Caveats

- The panel stratum is one study (`msk_met_2021`), so panel-vs-WES differences conflate assay,
  metastatic cohort composition, and institution-specific ascertainment.
- The panel regression has only 465 genes because panel callability restricts the observable gene
  universe. Its coefficients should be read as panel-surface diagnostics, not genome-wide effects.
- The analysis uses inclusive counts only. Hypermutator-exclusive sensitivity can be added once
  this result becomes publication-facing.
