---
id: t187
project: ''
title: 'commons-hygiene: re-run commons promotion after promote-paper tool bug is
  fixed'
type: ''
aspects:
- software-development
priority: P3
status: blocked
blocked_by: []
related: []
parent: ''
group: commons-hygiene
artifacts: []
findings: []
created: '2026-05-31'
completed: null
---

`science commons promote paper --from cbioportal --apply` crashes with `TypeError: unhashable type:
'dict'` (commons/promote.py:2810) — filed as science feedback fb-2026-05-31-001. `promote topic`
aborts the whole run on one schema-invalid entity (fb-2026-05-31-002). Once both are resolved
upstream, re-run paper + topic promotion to publish the reusable mutational-signature corpus
(catalogs, methods, aetiology papers + topics) to the commons store. Blocked on the upstream fixes.
