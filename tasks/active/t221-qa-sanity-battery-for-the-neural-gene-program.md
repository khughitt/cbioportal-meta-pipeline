---
id: t221
project: ''
title: QA / sanity battery for the neural-gene program
type: ''
aspects:
- computational-analysis
- validation
priority: P2
status: proposed
blocked_by: []
related:
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- question:0032-neural-gene-length-null
parent: ''
group: neural-gene-meta-analysis
artifacts: []
findings: []
created: '2026-06-06'
completed: null
---

Matched- vs unmatched-normal stratification (germline-leak control via matched_normal_studies); hypermutator/MSI stratification (is_hypermutator); common-fragile-site overlap for candidates; data-driven-set vs GO-label-set sensitivity. Runs alongside t217-t220.

### Notes

- 2026-06-08: Arm (a) complete (negative): full-config sample-level hypermutator exclusion across all 91 WES studies (326 hypermutator samples / 1.15M variant rows dropped) leaves the t217 genomic-span residual unchanged (span-matched p 0.002 -> 0.002; per-candidate only 0.4-1.9% of rows dropped). Closes the hypermutator control t218 deferred. Re-aggregation validated: inclusive arm reproduces the canonical wide table gene-for-gene (candidates exact) and t218 wes_only p=0.0022 exactly. Script code/notebooks/t221a_sample_level_hypermutator_exclusion.py; interpretation doc/interpretations/2026-06-08-t221a-sample-level-hypermutator-exclusion.md. Remaining: arm (b) standing-controls panel.
- 2026-06-08: Arm (b) complete: standing-controls panel, all four green. (1) Intronic-fraction stratification — the t218/t221a residual is entirely an all-region call-set artifact: lives in 6 all-region WES studies (intronic>=0.5; span-matched p 0.0002), GONE in 84 exonic-clean studies (candidates at 20.9th pctile, p 0.99). Generalizes pog570 to a 6-study class. (2) CFS positive control — candidates statistically indistinguishable from known CFS genes (~99.8th span pctile, top-0.2% raw). (3) Germline/dbSNP control — candidate rows only 12.7% dbSNP; excluding all dbSNP rows leaves residual intact (p 0.0028->0.0004). (4) Set sensitivity — neither label-free neural_score nor cns_score top-25 reproduces enrichment (small genes, ~33-44th span pctile, p 0.2-0.5). Matched-normal split deferred: config-full lacks matched_normal_studies. Script code/notebooks/t221b_standing_controls_panel.py; interpretation doc/interpretations/2026-06-08-t221b-standing-controls-panel.md. t221 complete (arms a+b).
- 2026-06-08: Populated matched_normal_studies in config-full.yml (closes the t221b F3 gap). Evidence-derived (t221c, code/notebooks/t221c_classify_matched_normal.py): a study is matched iff >=50% of variant rows carry a normal barcode (sample_id_norm) sharing the tumour patient stem (per-patient normal, not pooled/PON). 74/197 studies matched (all TCGA pan_can_atlas, TARGET, pog570, prostate_dkfz, consortium WES). High-precision lower bound: MSK-IMPACT family (msk_impact_2017/msk_chord_2024/msk_impact_50k_2026) is matched-by-design but records no per-variant normal barcode, so flagged + held back (not auto-added). Audit: results/neural-gene-matched-normal-2026-06-08/matched_normal_audit.tsv. Enables a true matched/unmatched germline-leak split (next).
- 2026-06-08: arm (d): ran true study-level matched/unmatched-normal split (t221d_matched_normal_split.py) consuming the t221c-populated matched_normal_studies. Closes t221b-F3 dbSNP proxy. De-confounded region x normal-status 2x2: within region stratum normal-status is inert (all-region matched p 0.0000 / median 0.161 vs unmatched p 0.0006 / median 0.170; both exonic arms null). Biggest residual-carrier pog570 (64% of cand rows) is matched-normal -> germline leak is NOT the driver. Interpretation: doc/interpretations/2026-06-08-t221d-matched-normal-split.md
