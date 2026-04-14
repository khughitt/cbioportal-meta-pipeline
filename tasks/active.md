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
- status: blocked
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- blocked-by: [t081, t079]
- group: meta-analysis
- created: 2026-04-13



## [t078] Pipeline addition: cross-study co-occurrence / mutual-exclusivity statistic (DISCOVER/WeSME + Stouffer)
- type: dev
- priority: P2
- status: proposed
- related: [topic:co-occurrence-and-mutual-exclusivity, search:2026-04-13-cooccurrence-mutual-exclusivity-methods, guide:cross-study-aggregation]
- group: meta-analysis
- created: 2026-04-13



## [t081] Pipeline addition: hypermutator / TMB-aware sample exclusion or covariate
- type: dev
- priority: P1
- status: blocked
- related: [topic:tumor-mutational-burden, task:bias-audit-cross-study-aggregation-pipeline, guide:cross-study-aggregation]
- blocked-by: [t092, t093, t094, t095, t096, t097, t098, t099]
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



## [t087] Graded ch_contamination_prob column replacing uniform ch_priority_gene boolean
- type: dev
- priority: P2
- status: proposed
- related: [search:2026-04-14-asxl1-tet2-ch-disambiguation, topic:clonal-hematopoiesis-contamination, article:Coombs2018, task:t059]
- group: pipeline
- created: 2026-04-14

Replace the uniform ch_priority_gene boolean emitted by annotate_ch.py with a graded ch_contamination_prob column sourced from Coombs 2018 Table 2 (per-gene variant-level CH confirmation rate in paired-tumor/blood cohort). Anchor values: DNMT3A ~64%, TP53 ~4%, overall across the 9-gene CH panel ~8%. ASXL1 and TET2 intermediate — read Coombs 2018 Table 2 for the precise numbers. Keep the boolean as a backward-compatible column (computed by thresholding the graded prob at 0.5) until downstream consumers migrate. Closes the open question surfaced in t059: uniform CH flagging over-masks bona fide solid-tumor ASXL1 biology (MSI-CRC polyG-indel, CRPC, HNSCC per Katoh 2013).

## [t088] Age-adjusted TMB alongside raw TMB (covariate support for t081)
- type: dev
- priority: P3
- status: proposed
- related: [search:2026-04-14-tmb-hypermutator-followup, topic:tumor-mutational-burden, article:Chalmers2017, task:t081, task:t025]
- group: pipeline
- created: 2026-04-14

Chalmers 2017 documents a 2.4x TMB increase between age 10 and age 90 in 100000-case FoundationOne cohort. Once per-sample TMB is computed in t081, emit a parallel age_adjusted_tmb column that regresses TMB on patient age (when available from cBioPortal clinical tables) and reports the residual. Two columns: raw tmb_mut_per_Mb and age_adjusted_tmb_residual. No surveyed TMB tool (Vega 2021 FoCR, jasonwong-lab/TMB, pyTMB) does this adjustment — cheap pipeline contribution.

## [t089] Per-histology relative + absolute dual hypermutator flags in t081
- type: dev
- priority: P1
- status: proposed
- related: [search:2026-04-14-tmb-hypermutator-followup, article:Campbell2017Hypermutation, article:Samstein2019, task:t081, task:t025]
- group: pipeline
- created: 2026-04-14

Refines t081 design based on the rescoped t025 evidence. Emit THREE flags per sample, not one:\n1. is_hypermutator_absolute (Campbell 2017): tmb >= 10 mut/Mb\n2. is_ultramutator_absolute (Campbell 2017): tmb >= 100 mut/Mb\n3. is_hypermutator_relative (Samstein 2019): top-20% TMB within the sample's histology\n\nSamstein 2019 explicitly argues that per-histology cutpoints vary markedly, so a single universal cutoff under-serves real biology. Keep all three flags; downstream consumers pick. Also emit (when available) an msi_status column — Fabrizio 2018 shows MSI-H / TMB-H intersection is non-1:1.

## [t090] Pathway-layer benchmark on cross-study cBioPortal data (t043 gap)
- type: research
- priority: P2
- status: proposed
- related: [search:2026-04-14-pathway-level-pan-cancer-methods, article:Reyna2020Pathway, article:Iorio2018SLAPenrich, article:Paczkowska2020, task:t043, task:t077, task:t079]
- group: meta-analysis
- created: 2026-04-14

Surfaced as a real gap in t043: no pan-cancer benchmark at the pathway rollup level currently exists (Wu 2022 Brief Bioinform benchmark is gene-level only). Run SLAPenrich vs ActivePathways vs HotNet2 on the pipeline's gene_cancer_study output using a shared pathway database (start with Reactome + Sanchez-Vega-10; KEGG and MSigDB Hallmarks as comparators) across multiple cBioPortal cohorts and report method concordance. Natural methodological contribution. Pre-register pathway database + primary method choice before running (ties to t079 pooling pre-registration).

## [t091] Companion search: TET2 in solid tumors (melanoma, glioma, breast) — disambiguate CH vs biology
- type: research
- priority: P3
- status: proposed
- related: [search:2026-04-14-asxl1-tet2-ch-disambiguation, topic:clonal-hematopoiesis-contamination, task:t059]
- group: searches
- created: 2026-04-14

Gap surfaced in t059: TET2 solid-tumor biology literature is thinner than ASXL1. ASXL1 has clear MSI-CRC polyG-indel + CRPC / HNSCC / breast evidence (Katoh 2013). TET2 solid-tumor papers cluster around melanoma (catalytic-domain mutations), glioma (IDH-pathway interaction — TET2 is the IDH-pathway target, so IDH-mutant gliomas carry functional TET2 loss without TET2 mutation), and breast. Focused OpenAlex + PubMed search. Produces doc/searches/YYYY-MM-DD-tet2-solid-tumor-biology.md.

## [t092] t081.1: Panel callable-Mb registry (build_panel_callable_sizes)
- type: dev
- priority: P1
- status: proposed
- related: [task:t081, plan:2026-04-13-t081-hypermutator-annotation-pipeline-plan, topic:cross-panel-normalization-methods]
- group: pipeline
- created: 2026-04-14

First of 8 subtasks for t081 (hypermutator / TMB annotation pipeline).\n\nImplements: input-side normalization — the TMB denominator. Produces out_dir/metadata/panel_callable_mb.tsv (generated build artifact, NOT version-controlled). Consumes: GENIE coverage feather (existing process_genie_panel_coverage output), config panel_callable_mb_override map, config wes_default_callable_mb. Declares localrules so it runs locally and its output persists via normal Snakemake DAG invalidation. Output cols: [panel_id, callable_mb, source in {bed_sum, config_override, wes_default}].\n\nReusable=true: also consumed by t070 (panel-version drift), t076 (NaN-vs-0), t077 (GLMM-logit covariate).\n\nTDD asserts in the plan doc task 1 section. Validation: MSK-IMPACT panels bed-derived size within 5%% of published; every panel_id in study_panel_map covered.

## [t093] t081.2: Per-sample TMB calculation + study_id propagation (compute_per_sample_tmb)
- type: dev
- priority: P1
- status: proposed
- related: [task:t081, task:t092, plan:2026-04-13-t081-hypermutator-annotation-pipeline-plan, article:Chalmers2017, article:Zehir2017]
- blocked-by: [t092]
- group: pipeline
- created: 2026-04-14

Subtask 2 of 8 for t081. Blocked by t092 (panel callable-Mb registry).\n\nImplements: core continuous-TMB signal + F3 fix (study_id first-class on every sample-level artifact). Protein-altering variant_class filter. Emits new out_dir/studies/{id}/metadata/samples_tmb.feather (does NOT overwrite samples.feather; preserves downstream consumers). Cols: sample_id_tumor, mutation_count, tmb, tmb_log10, tmb_source, study_id.\n\nIntegration validation: on msk_impact_2017 median tmb should be ~3-6 mut/Mb (Chalmers 2017, Zehir 2017); every row has non-null study_id.

## [t094] t081.3: POLE/POLD1 hotspot detector (detect_polymerase_hotspots)
- type: dev
- priority: P1
- status: proposed
- related: [task:t081, plan:2026-04-13-t081-hypermutator-annotation-pipeline-plan, article:Campbell2017Hypermutation]
- group: pipeline
- created: 2026-04-14

Subtask 3 of 8 for t081. No predecessor dependency (independent biological signal input).\n\nImplements: Assumption 4 of t081 plan — independent biological signal for ultra-hypermutation. Per-sample boolean flags pole_hotspot_detected, pold1_hotspot_detected. Canonical hotspot sets:\n  POLE = {P286R, V411L, S297F, S459F, A456P, L424V, M295V, F367L}\n  POLD1 = {P327L, R689W, S478N, L474P, D316H, D316N}\nCitations: Campbell 2017, Rayner 2016, Ma 2018. Per-study output sample_polymerase_hotspots.feather.\n\nIntegration validation: TCGA-UCEC POLE hotspot rate ~7%% (TCGA 2013); assert 4-12%%. Sanity: every POLE-hotspot+ sample should have tmb_log10 > population_median + 1.

## [t095] t081.4: MSI status ingestion (convert_to_feather.py extension)
- type: dev
- priority: P1
- status: proposed
- related: [task:t081, plan:2026-04-13-t081-hypermutator-annotation-pipeline-plan]
- group: pipeline
- created: 2026-04-14

Subtask 4 of 8 for t081. No predecessor dependency (extends existing convert_to_feather.py).\n\nImplements: Assumption 5 — third biological signal when available. Parses MSI columns from data_clinical_sample.txt; normalizes to {MSI-H, MSI-L, MSS, Indeterminate, NaN}. Also parses MSI_SCORE numeric as separate msi_score col. Normalization map documented + exported for testability (Instable/MSI/High -> MSI-H; Stable/Microsatellite stable -> MSS).\n\nIntegration validation: any study with MSI_TYPE in clinical file -> non-null proportion >50%% expected; MSK-IMPACT should have msi_sensor_score equivalents. Log study-by-study availability to audit-trail output.

## [t096] t081.5: Per-cancer-type TMB GMM fit (fit_per_cancer_tmb_gmm)
- type: dev
- priority: P1
- status: proposed
- related: [task:t081, task:t093, plan:2026-04-13-t081-hypermutator-annotation-pipeline-plan, article:Campbell2017Hypermutation, article:Samstein2019]
- blocked-by: [t093]
- group: pipeline
- created: 2026-04-14

Subtask 5 of 8 for t081. Blocked by t093 (needs per-sample TMB values).\n\nImplements: data-driven threshold (Assumption 6). Per-cancer-type 2-component GaussianMixture vs 1-component; select 2 when delta-BIC>10 AND Hartigan dip p<0.1 AND n_samples>=gmm_min_samples. Pin random_state to snek.config['random_seed'] (reproducibility covenant — see review doc finding #1). Always compute tmb_zscore_within_cancer as fallback. Outputs per_cancer_gmm_fits.feather (diagnostics) + samples_gmm_flagged.feather (per-sample flags + gmm_posterior_upper).\n\nIntegration validation: TCGA-UCEC exclusion rate ~20-25%%; TCGA-COAD ~10-15%%; TCGA-SKCM ~5-10%% (all within +-20%% relative). Diagnostic GMM-overlay PNGs per cancer type in results/diagnostics/.

## [t097] t081.6: Composite hypermutation score + final flag (annotate_hypermutators)
- type: dev
- priority: P1
- status: blocked
- related: [task:t081, task:t093, task:t094, task:t095, task:t096, plan:2026-04-13-t081-hypermutator-annotation-pipeline-plan, task:t089]
- blocked-by: [t093, t094, t095, t096]
- group: pipeline
- created: 2026-04-14

Subtask 6 of 8 for t081. Blocked by t093 (TMB) + t094 (POLE/POLD1) + t095 (MSI) + t096 (GMM) — using block command post-creation to add the other three.\n\nImplements: multi-source combination. Emits hypermutation_score (continuous 0-1), is_hypermutator (bool), hypermutator_reason (audit trail). Canonical decision table (F4 fix, see plan): priority 1-8:\n  1. POLE hotspot -> score=1.0, flag=True, reason=pole_hotspot\n  2. POLD1 hotspot -> 1.0 True pold1_hotspot\n  3. MSI-H -> 1.0 True msi_h\n  4. GMM bimodal + upper posterior>0.5 -> posterior True gmm_upper_mode\n  5. GMM bimodal + posterior<=0.5 -> posterior False gmm_lower_mode\n  6. GMM unavailable + z>=1.5 -> piecewise score True zscore_fallback_high\n  7. GMM unavailable + z<1.5 -> piecewise score False zscore_fallback_low\n  8. TMB NaN -> NaN False tmb_unavailable\n\nRows 1-3 deterministic (clinical diagnostic categories override TMB). score_threshold config only affects rows 4/5.\n\nRelated to t089 (dual hypermutator flags) — this rule emits is_hypermutator_absolute (Campbell 2017 10/100 cutoff) and is_hypermutator_relative (Samstein 2019 per-histology top-20%%) as additional columns per t089.

## [t098] t081.7: Per-study inclusive/exclusive ratios + combined passthrough (F1 fix)
- type: dev
- priority: P1
- status: proposed
- related: [task:t081, task:t097, plan:2026-04-13-t081-hypermutator-annotation-pipeline-plan, task:t076]
- blocked-by: [t097]
- group: pipeline
- created: 2026-04-14

Subtask 7 of 8 for t081. Blocked by t097 (needs is_hypermutator flag).\n\nImplements F1 fix: hypermutator-exclusion filter lives at per-study layer (create_freq_tables.py:36-46) where sample IDs are still available; combined scripts only pivot pre-computed values. Two parts:\n\n7a — create_freq_tables.py: accept optional samples_annotated.feather; compute num_inclusive/num_exclusive/ratio_inclusive/ratio_exclusive/n_samples_inclusive/n_samples_exclusive. Preserve num/ratio as aliases for inclusive. Option chosen: always require samples_annotated as input (no legacy escape hatch — pipeline not yet published).\n\n7b — combined-script passthrough in create_combined_gene_cancer_freq_table.py: pivot new columns through to combined output.\n\nDovetails with t076 (NaN-vs-0 at per-(study, gene) layer).

## [t099] t081.8: Documentation + AGENTS.md updates for hypermutator annotation
- type: dev
- priority: P2
- status: proposed
- related: [task:t081, task:t098, plan:2026-04-13-t081-hypermutator-annotation-pipeline-plan, topic:tumor-mutational-burden, guide:cross-study-aggregation]
- blocked-by: [t098]
- group: pipeline
- created: 2026-04-14

Subtask 8 of 8 for t081. Blocked by t098 (full pipeline lands first).\n\nImplements: future-collaborator onboarding + audit-trail hygiene. No tests.\n\n1. AGENTS.md 'Annotations applied in the pipeline' section: new subsection 'Hypermutator / TMB annotation' (continuous cols, boolean flag, composite score, data sources, threshold policy, audit trail).\n2. doc/guides/modalities/cross-study-aggregation.md: link is_hypermutator to new audit-checklist item agg.15 (hypermutator-exclusion applied to cross-study pooled ratios), paralleling agg.07 for CH.\n3. doc/background/topics/tumor-mutational-burden.md 'Relevance to this project' section: point to samples_annotated.feather schema.\n4. Close t081 with note pointing to plan + implementing commits.
