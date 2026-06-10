---
type: meta
title: 'Feedback to upstream science project: /science:search-literature (2026-04-13)'
status: active
created: '2026-04-13'
updated: '2026-04-13'
id: meta:0003-feedback-to-upstream-science-project-science-search-literature-2026-04
---

# Feedback audit — /science:search-literature (2026-04-13)

Five feedback entries submitted via `science-tool feedback add` after the first run of
`/science:search-literature` on this project (see
`doc/searches/2026-04-13-foundational-cbioportal-literature.md`).

| ID | Category | Summary |
|---|---|---|
| fb-2026-04-13-001 | friction | Skill invites verify-instead-of-discover mode without guarding against it |
| fb-2026-04-13-002 | gap | Writing-output step (paper stubs) runs before papers are actually read |
| fb-2026-04-13-003 | friction | `science-tool literature search` referenced as preferred runtime but not implemented |
| fb-2026-04-13-004 | gap | No coverage-self-audit step before closing the search |
| fb-2026-04-13-005 | positive | Tiering framework (Core now / Relevant next / Peripheral monitor) works well |

## Self-critique of our own run

The most important single observation: **our run verified citations rather than discovering them.**
Eight PubMed queries, mostly author+title seeds, <15 results per query. Zero unknown-to-model
papers surfaced. OpenAlex was not used. Result: blind spots on co-occurrence / mutual-exclusivity
methods, OncoKB as a data layer, hotspot-based driver detection, and pathway-level pan-cancer
analysis — all directly relevant to this project and all surfaced only when we audited coverage
post-hoc.

The tiering framework and output scaffolding were, however, a net positive: they produced a
reading queue that maps cleanly onto project task priorities.

## Follow-up actions in this project

- Queued new paper-reading tasks (t028–t037) for the missed papers.
- Queued new topic-development tasks (t038–t041) for the missed sub-topics.
- Queued two genuine discovery searches (t042, t043) to re-run `/science:search-literature` with
  OpenAlex + broader retrieval for the sub-topics that need discovery rather than seed-verification.
