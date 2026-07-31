---
id: t088
project: ''
title: Age-adjusted TMB alongside raw TMB (covariate support for t081)
type: ''
aspects:
- software-development
priority: P3
status: proposed
blocked_by: []
related:
- search:0006-tmb-hypermutator-followup
- topic:tumor-mutational-burden
- paper:Chalmers2017
- task:t081
- task:t025
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-14'
completed: null
---

Chalmers 2017 documents a 2.4x TMB increase between age 10 and age 90 in 100000-case FoundationOne cohort. Once per-sample TMB is computed in t081, emit a parallel age_adjusted_tmb column that regresses TMB on patient age (when available from cBioPortal clinical tables) and reports the residual. Two columns: raw tmb_mut_per_Mb and age_adjusted_tmb_residual. No surveyed TMB tool (Vega 2021 FoCR, jasonwong-lab/TMB, pyTMB) does this adjustment — cheap pipeline contribution.
