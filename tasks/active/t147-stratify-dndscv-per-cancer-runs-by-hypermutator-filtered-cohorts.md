---
id: t147
project: ''
title: Stratify dNdScv per-cancer runs by hypermutator-filtered cohorts
type: ''
aspects:
- computational-analysis
- software-development
priority: P2
status: proposed
blocked_by: []
related:
- task:t131
- task:t081
- task:t141
- interpretation:0009-t131-full-pan-cancer-dndscv-run
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-26'
completed: null
---

The t131 interpretation noted that even after the t144 tiebreaker fix, TTN persists at v2 rank #5 and AHNAK / AHNAK2 / ABCA13 survive in the q=0 set despite dNdScv's trinucleotide-context correction. The leading explanation is that hypermutated samples (POLE / POLD1 / MSI-H) inflate per-gene mutation counts uniformly across the genome, with the largest absolute inflation at the longest genes — defeating the per-cancer trinucleotide-context background.

**Approach**: re-run `run_dndscv_per_cancer` on cohorts with `is_hypermutator == False` (the existing t081 annotation) and compare the per-cancer q=0 set sizes and top-50 rankings. If hypermutator removal eliminates TTN / AHNAK / AHNAK2 from the top, the inflation is hypermutator-driven; if not, it's something else.

**Cost**: blocked on t141 (R meta-analysis parallelization) being shipped, otherwise the re-runs take 12+ hours each. Could also do this for a single cancer (Endometrial Cancer = UCEC, the most POLE-rich) as a cheap pilot.

**Output**: per-cancer-type comparison feather; recommendation for whether to gate `run_dndscv_per_cancer` on hypermutator-filtered cohorts by default.
