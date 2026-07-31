---
id: t169
project: ''
title: Acquire GTEx v10 + Yizhak2019 / Rockweiler2023 healthy-tissue somatic call
  sets for h05 atlas
type: ''
aspects:
- computational-analysis
priority: P3
status: blocked
blocked_by: []
related:
- hypothesis:0005-healthy-somatic-background-atlas
- hypothesis:0001-non-tumor-signal-contamination
- question:0007-cross-tissue-somatic-mutation-rate-variation-as-null-model
- task:t150
- task:t151
- task:t111
- topic:normal-tissue-mutation-atlas
parent: ''
group: dataset-acquisition
artifacts: []
findings: []
created: '2026-04-28'
completed: null
---

The current h05 cross-tissue normal background relies on Li 2021 spectra alone (resolved via task:t111 for 56 per-tissue spectra). Two complementary public sources expand coverage substantially. (1) Yizhak 2019 (RNA-MuTect): somatic variants called from GTEx RNA-seq across 29 tissues, ~6,700 samples, age-stratified. Trades VAF accuracy for breadth and age-coverage. (2) Rockweiler 2023: somatic mutation rates from GTEx WGS for the subset with whole-genome data, more accurate but much smaller n. Together, GTEx-grounded Yizhak + Rockweiler covers age × tissue × mutation-class space far better than Li 2021 alone, which is essential for the P1 '>2 OoM cross-tissue rate variation' claim and for the per-tissue null model that task:t114 wants to pre-register. Access: GTEx v10 expression and metadata are public (gtexportal.org); somatic call tables are supplementary tables to the respective papers (already public). Pipeline integration scope: parallel to the t111 Li 2021 spectra script — extract per-sample spectra from each call set, harmonize tissue labels against the cBioPortal cancer-type axis, emit normal_tissue_spectra.feather extensions covering Yizhak / Rockweiler tissues. Acceptance: data/yizhak2019_rnamutect/ and data/rockweiler2023_gtex_wgs/ populated; t111 script extension produces a unified normal-tissue spectra feather covering ≥40 tissue × age strata; one pilot of the t151 esophagus or colon background null swap uses the expanded reference and reports an effect-size delta versus Li-only.

### Notes

- 2026-05-31: Blocked 2026-05-31: GTEx v10 controlled-access somatic call sets (and the Yizhak2019/Rockweiler2023 dbGaP tiers) require institutional affiliation with a cancer-research institute, which the user does not currently hold. Public GTEx expression/metadata remain accessible but the somatic-variant tables that h05 needs are gated. Revisit when affiliation is re-established. Until then, prioritize tasks that need no gated data access (e.g. t195 h08 positive-control scan on MC3 + existing exposures).
