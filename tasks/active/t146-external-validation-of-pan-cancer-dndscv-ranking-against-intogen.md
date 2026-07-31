---
id: t146
project: ''
title: External validation of pan-cancer dNdScv ranking against IntOGen / Martincorena
  2017
type: ''
aspects:
- computational-analysis
priority: P2
status: blocked
blocked_by: []
related:
- task:t131
- task:t171
- interpretation:0012-t146-external-validation-cgc
- interpretation:0009-t131-full-pan-cancer-dndscv-run
parent: ''
group: validation
artifacts: []
findings: []
created: '2026-04-26'
completed: null
---

The 2026-04-26 t131 interpretation flagged **mild circularity** in using Bailey 2018 driver recovery as the primary validation metric — Bailey 2018 used dNdScv as one of seven driver-detection inputs, so high Bailey recovery is partly self-validation. Need an external reference that does NOT include dNdScv as an input.

**Targets**:
- Martincorena 2017 supplementary tables (the original pan-cancer dNdScv ranking).
- IntOGen pan-cancer driver list (uses MutSig + OncodriveCLUSTL + OncodriveFML + dNdScv; pull only the non-dNdScv subset).
- COSMIC Cancer Gene Census tier 1 (curated by literature, not by dNdScv).

**Output**: rank-rank Spearman correlation table; spot-check the top-50 disagreements between our pan-cancer dNdScv and IntOGen's; document any systematic differences (e.g., do we over-rank long genes that IntOGen flags as artifacts?).
