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

## [t052] Pipeline addition: per-study cohort-stage descriptor
- type: dev
- priority: P1
- status: proposed
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: pipeline
- created: 2026-04-13

Ingest per-study primary/metastatic/pre-treated annotation from cBioPortal clinical sample tables. Concrete bias to address: AR 18% in MSK metastatic prostate vs 1% in TCGA primary; ESR1 11% vs 4%. From cohort-selection-bias synthesis.

## [t055] Pipeline addition: M/C-class descriptor (mutation-vs-CNA hyperbola)
- type: dev
- priority: P3
- status: deferred
- group: pipeline
- created: 2026-04-13

Compute per-tumor and per-cancer mutation-count vs SCNA-burden axis (Ciriello2013 cancer genome hyperbola). Cheap secondary descriptor. Blocked: requires CNA data ingestion which our pipeline does not currently have.

Blocked on CNA ingestion — no CNA scripts in code/scripts/, no rule in Snakefile, and CNA is outside current specs/research-question.md scope. Revisit when / if CNA modality is added.

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

## [t070] F6 [Significant] MSK-IMPACT panel-version drift handling per sample
- type: dev
- priority: P1
- status: proposed
- related: [task:bias-audit-cross-study-aggregation-pipeline]
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
- priority: P1
- status: proposed
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: pipeline
- created: 2026-04-13

Follow-on to t074 annotation-only pass. Currently per-study NaN conflates three cases: (a) gene not on panel, (b) gene on panel but unmutated, (c) cancer-type not in study cohort. Case (c) disambiguation requires per-(study, cancer_type) sample counts (not currently ingested). With that ingested: fill NaN with 0 where gene-is-on-panel AND cancer-type-is-in-study; keep NaN otherwise. Replaces current .mean(skipna=True) bias where 'on panel, unmutated' studies are dropped.

## [t077] Pipeline addition: random-effects pooled gene×cancer table (GLMM-logit)
- type: dev
- priority: P1
- status: proposed
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: meta-analysis
- created: 2026-04-13



## [t078] Pipeline addition: cross-study co-occurrence / mutual-exclusivity statistic (DISCOVER/WeSME + Stouffer)
- type: dev
- priority: P2
- status: proposed
- related: [topic:co-occurrence-and-mutual-exclusivity, search:2026-04-13-cooccurrence-mutual-exclusivity-methods, guide:cross-study-aggregation]
- group: meta-analysis
- created: 2026-04-13



## [t079] Pre-register pooling-method choice (GLMM-logit) before running on full dataset
- type: research
- priority: P1
- status: proposed
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: meta-analysis
- created: 2026-04-13



## [t080] Commit in-flight pipeline work (annotate scripts, process_* scripts, Snakefile rules, AGENTS.md updates)
- type: dev
- priority: P1
- status: proposed
- related: [guide:cross-study-aggregation]
- group: pipeline
- created: 2026-04-13



## [t081] Pipeline addition: hypermutator / TMB-aware sample exclusion or covariate
- type: dev
- priority: P1
- status: proposed
- related: [topic:tumor-mutational-burden, task:bias-audit-cross-study-aggregation-pipeline, guide:cross-study-aggregation]
- group: pipeline
- created: 2026-04-13



## [t082] Pipeline addition: HGNC gene-symbol alias mapping in convert_to_feather.py
- type: dev
- priority: P2
- status: proposed
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: pipeline
- created: 2026-04-13



## [t083] Pipeline addition: cancer-type label canonicalization (strip+case; optional OncoTree mapping)
- type: dev
- priority: P2
- status: proposed
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: pipeline
- created: 2026-04-13



## [t084] Pipeline addition: study-prefix patient_id in combined sample table to prevent cross-study collisions
- type: dev
- priority: P3
- status: proposed
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: pipeline
- created: 2026-04-13



## [t085] Pipeline addition: silhouette/gap-statistic k-selection + stability check for gene/cancer clustering
- type: dev
- priority: P3
- status: proposed
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: pipeline
- created: 2026-04-13



## [t086] Pipeline addition: length_is_fallback indicator column + per-run excluded_studies.tsv audit trail
- type: dev
- priority: P3
- status: proposed
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: pipeline
- created: 2026-04-13


