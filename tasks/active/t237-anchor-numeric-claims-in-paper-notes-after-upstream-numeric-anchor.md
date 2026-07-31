---
id: t237
project: ''
title: Anchor numeric claims in paper notes after upstream numeric-anchor cleanup
type: ''
aspects:
- computational-analysis
priority: P2
status: proposed
blocked_by: []
related:
- task:t233
- task:t234
parent: ''
group: science-strict-validation-cleanup
artifacts: []
findings: []
created: '2026-06-28'
completed: null
---

Curation batch for paper-note prose_lints.numeric-anchor warnings after t234 removes parser noise. Current baseline after the upstream DOI/identifier fix and the first t235 exact-reference passes: 1225 numeric-anchor warnings under entities/papers. Start with clustered files from /tmp/cbioportal-validation-issues.json: Deshpande2026 and LeeSix2018 at 50+ each; then Iorio2018SLAPenrich, Pugh2022, Li2021, AACRGENIEConsortium2017, Koh2025, Tan2024, Wan2022, Nguyen2022, Levatic2022, Sorensen2023, Gillani2022, and Kesimoglu2026. For each numeric claim, add a local citation/source anchor, soften or remove unsupported precision, or open a source-specific follow-up.
