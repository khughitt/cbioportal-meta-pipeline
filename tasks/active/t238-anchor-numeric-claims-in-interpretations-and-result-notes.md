---
id: t238
project: ''
title: Anchor numeric claims in interpretations and result notes
type: ''
aspects:
- computational-analysis
priority: P2
status: proposed
blocked_by: []
related:
- task:t233
parent: ''
group: science-strict-validation-cleanup
artifacts: []
findings: []
created: '2026-06-28'
completed: null
---

Curation batch for local-result numeric-anchor warnings. Current baseline after the upstream DOI/identifier fix and the first t235 exact-reference passes: 418 warnings in entities/interpretations plus 32 in entities/meta and 23 in entities/plans. Start with clustered interpretation files from /tmp/cbioportal-validation-issues.json: 0030-t207-h10-treatment-impact-full-config, 0032-t208-h10-sample-level-mutagenic-rules, 0043-t221a-sample-level-hypermutator-exclusion, 0002-t070-poc-comparison, 0044-t221b-standing-controls-panel, 0012-t146-external-validation-cgc, 0009-t131-full-pan-cancer-dndscv-run, 0042-t218-cns-exclusion-wes-panel, 0045-t221d-matched-normal-split, and 0021-t173-genie-dndscv-influence. Prefer anchors to workflow-run refs, result paths, scripts, or cited interpretation artifacts; avoid adding literature citations to local-computation outputs unless the number comes from a paper.
