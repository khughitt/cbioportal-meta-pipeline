## [t025] Follow-up search: TMB harmonization (Friends-of-Cancer-Research / Buchhalter)
- type: research
- priority: P3
- status: proposed
- group: searches
- created: 2026-04-13

Dedicated search for panel-vs-WES TMB calibration methods.

## [t026] Follow-up search: panel comparability / cross-panel normalization
- type: research
- priority: P2
- status: proposed
- group: searches
- created: 2026-04-13

MSK-IMPACT vs FoundationOne vs GENIE panel intersection / callability-denominator methods. Gap from 2026-04-13 search.

## [t043] Focused discovery search: pathway-level pan-cancer analysis methods
- type: research
- priority: P2
- status: proposed
- group: searches
- created: 2026-04-13

Beyond Sanchez-Vega 2018 seed. Cover pan-cancer pathway enrichment methods and pathway-centric interpretation of mutation data. OpenAlex + PubMed.

## [t049] Pipeline addition: Sanchez-Vega2018 pathway overlay
- type: dev
- priority: P2
- status: proposed
- group: pipeline
- created: 2026-04-13

Add per-(sample, pathway) collapse using Sanchez-Vega 2018 Tables S2/S3 (10 canonical signaling pathways). Analogous to the Bailey driver overlay. Outputs: per-(cancer, pathway) alteration-rate table + per-tumor pathway-burden table.

## [t052] Pipeline addition: per-study cohort-stage descriptor
- type: dev
- priority: P2
- status: proposed
- group: pipeline
- created: 2026-04-13

Ingest per-study primary/metastatic/pre-treated annotation from cBioPortal clinical sample tables. Concrete bias to address: AR 18% in MSK metastatic prostate vs 1% in TCGA primary; ESR1 11% vs 4%. From cohort-selection-bias synthesis.

## [t053] Pipeline addition: catalog version stamping for annotated outputs
- type: dev
- priority: P2
- status: proposed
- group: pipeline
- created: 2026-04-13

Every Bailey/CGC/OncoKB annotation in our outputs should carry the catalog version (date, release tag) used. Critical given OncoKB Level 1/2 actionability rose 8.9%->31.6% in 5 years on the same cohort (Suehnholz2024). Avoid silent version-drift in downstream comparisons.

## [t054] Pipeline addition: tissue-conditional driver flag
- type: dev
- priority: P2
- status: proposed
- group: pipeline
- created: 2026-04-13

Per-(gene, cancer-type) annotation distinguishing 'Bailey driver in this specific cancer' vs 'pan-cancer driver only'. Surfaces the 19% tissue-borrowed (Bailey2018) / ~1/3 non-canonical-context (Bandlamudi2026) phenomenon in our outputs.

## [t055] Pipeline addition: M/C-class descriptor (mutation-vs-CNA hyperbola)
- type: dev
- priority: P3
- status: proposed
- group: pipeline
- created: 2026-04-13

Compute per-tumor and per-cancer mutation-count vs SCNA-burden axis (Ciriello2013 cancer genome hyperbola). Cheap secondary descriptor. Blocked: requires CNA data ingestion which our pipeline does not currently have.

## [t056] Pipeline addition: cluster comparison report (mutation-only vs Hoadley integrated)
- type: research
- priority: P3
- status: proposed
- group: pipeline
- created: 2026-04-13

Side-by-side: our summary/mut/clusters/cancer.feather vs Hoadley2018 integrated 28-cluster taxonomy. Where do they agree (validates pipeline)? Where do they differ (where mutations carry non-lineage signal)? See pan-cancer-interpretive-frames synthesis.

## [t059] Focused search: ASXL1 / TET2 disambiguation in solid tumors (CH leakage vs real biology)
- type: research
- priority: P3
- status: proposed
- group: searches
- created: 2026-04-13

Open question from CH topic: ASXL1 and TET2 are bona fide tumor suppressors in some lineages but also CH leakage. Disambiguation literature for solid-tumor pan-cancer panel data.

## [t060] Flesh out modality guide: panel-mutation-data
- type: research
- priority: P2
- status: proposed
- group: guides
- created: 2026-04-13

Expand checklist with sources from focused-search t026 (panel comparability). Add evidence-expected detail. Cross-link to per-(study, gene) callability rule once ingested.

## [t061] Flesh out modality guide: wes-mutation-data
- type: research
- priority: P2
- status: proposed
- group: guides
- created: 2026-04-13

Add MC3 + per-cancer baseline detail. Cross-link to MC3 ingestion task t048. Add hypermutator handling specifics from Lawrence/Bailey/Kandoth methodology.

## [t062] Flesh out modality guide: cross-study-aggregation
- type: research
- priority: P1
- status: active
- related: [search:2026-04-13-cross-study-meta-analysis-stats, search:2026-04-13-cooccurrence-mutual-exclusivity-methods]
- group: guides
- created: 2026-04-13

Highest-priority guide. Add meta-analytic stats sources (DerSimonian-Laird, REML, Bayesian hierarchical, dmetar) once focused search t027 runs. Tie checklist items directly to pipeline addition tasks t048-t056.

## [t063] Flesh out modality guide: driver-detection
- type: research
- priority: P2
- status: proposed
- group: guides
- created: 2026-04-13

Already substantively covered by existing reads. Add tool-disagreement evidence from Bailey 2018 Table S2; refine criteria for novel-driver claims.

## [t064] Flesh out modality guide: variant-annotation
- type: research
- priority: P2
- status: proposed
- group: guides
- created: 2026-04-13

Add Genome Nexus reference (no paper read yet). Add OncoKB API rate-limit / batch-annotation detail. Cross-link to catalog-version-stamping pipeline addition t053.

## [t065] Add modality guide: clinical-cancer-genomics (cohort study design)
- type: research
- priority: P3
- status: proposed
- group: guides
- created: 2026-04-13

New modality guide. Covers clinical-sequencing cohort selection, prospective design, biopsy-source biases. Sources: Zehir2017, Pugh2022, ChakravartySolit2021. Lower priority — bias coverage already in topic stubs and other modality guides.

## [t066] Add modality guide: mutational-signatures (when in-scope)
- type: research
- priority: P3
- status: proposed
- group: guides
- created: 2026-04-13

New modality guide if/when signature decomposition added to pipeline. Sources: Alexandrov2020, Tate2019, SigProfiler/SigMA tooling. Out-of-scope today.

## [t070] F6 [Significant] MSK-IMPACT panel-version drift handling per sample
- type: dev
- priority: P2
- status: proposed
- related: [task:t067]
- group: audit-fixes
- created: 2026-04-13

Severity: Significant. From audit F6. Per-sample panel_version flag from cBioPortal study definitions; for genes added in IMPACT-468/505 exclude earlier-cohort samples from denominator.

## [t072] F10 [Significant] Saturation-aware per-cancer interpretation context column
- type: dev
- priority: P3
- status: proposed
- related: [task:t067]
- group: audit-fixes
- created: 2026-04-13

Severity: Significant. From audit F10. Add cancer_saturation_status column derived from per-cancer cohort N + Lawrence 2014 per-cancer required-N. Flag long-tail rankings for under-sampled cancers.

## [t073] F11 [Minor] Add n_studies_contributing column to gene_cancer_study output
- type: dev
- priority: P3
- status: proposed
- related: [task:t067]
- group: audit-fixes
- created: 2026-04-13

Severity: Minor. From audit F11. Trivial: count of non-null per-study columns per row, added as explicit column in output.

## [t076] Pipeline addition: tighten NaN-vs-0 handling for panel-aware aggregation (F2 full close)
- type: dev
- priority: P2
- status: proposed
- group: pipeline
- created: 2026-04-13

Follow-on to t074 annotation-only pass. Currently per-study NaN conflates three cases: (a) gene not on panel, (b) gene on panel but unmutated, (c) cancer-type not in study cohort. Case (c) disambiguation requires per-(study, cancer_type) sample counts (not currently ingested). With that ingested: fill NaN with 0 where gene-is-on-panel AND cancer-type-is-in-study; keep NaN otherwise. Replaces current .mean(skipna=True) bias where 'on panel, unmutated' studies are dropped.
