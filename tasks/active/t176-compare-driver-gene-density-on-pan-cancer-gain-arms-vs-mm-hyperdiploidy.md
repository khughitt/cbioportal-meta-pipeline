---
id: t176
project: ''
title: Compare driver-gene density on pan-cancer gain arms vs MM hyperdiploidy chromosomes
type: ''
aspects:
- computational-analysis
priority: P2
status: proposed
blocked_by: []
related:
- topic:cancer-driver-genes
- topic:pan-cancer-interpretive-frames
- topic:pan-cancer-mutation-landscape
parent: ''
group: meta-analysis
artifacts: []
findings: []
created: '2026-05-05'
completed: null
---

Follow-up from MM30 hyperdiploidy mechanism discussion. Test whether common pan-cancer gain arms such as 20q, 7p, 8q, 1q, 7q, and 20p and MM hyperdiploidy chromosomes 3, 5, 7, 9, 11, 15, 19, and 21 are enriched for known cancer drivers or oncogene-dosage targets. Use data/cosmic_cgc.tsv, data/bailey2018_table_s1.tsv, and GRCh37/GRCh38 gene annotations. Compare driver density and aggregate Bailey consensus/frequency scores per arm/chromosome while controlling for gene count and arm size. Deliverable: doc/interpretations/<date>-aneuploidy-driver-dosage-comparison.md with tables separating generic pan-cancer gain targets from plasma-cell/MM-HD-specific dosage-package candidates.
