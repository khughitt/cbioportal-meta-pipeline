## [t025] Follow-up search: TMB harmonization (Friends-of-Cancer-Research / Buchhalter)
- type: research
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- group: searches
- created: 2026-04-13

Dedicated search for panel-vs-WES TMB calibration methods.

## [t052] Pipeline addition: per-study cohort-stage descriptor
- type: dev
- priority: P1
- status: proposed
- aspects: [software-development]
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: pipeline
- created: 2026-04-13

Ingest per-study primary/metastatic/pre-treated annotation from cBioPortal clinical sample tables. Concrete bias to address: AR 18% in MSK metastatic prostate vs 1% in TCGA primary; ESR1 11% vs 4%. From cohort-selection-bias synthesis.

## [t055] Pipeline addition: M/C-class descriptor (mutation-vs-CNA hyperbola)
- type: dev
- priority: P3
- status: deferred
- aspects: [software-development]
- group: pipeline
- created: 2026-04-13

Compute per-tumor and per-cancer mutation-count vs SCNA-burden axis (Ciriello2013 cancer genome hyperbola). Cheap secondary descriptor. Blocked: requires CNA data ingestion which our pipeline does not currently have.

Blocked on CNA ingestion — no CNA scripts in code/scripts/, no rule in Snakefile, and CNA is outside current specs/research-question.md scope. Revisit when / if CNA modality is added.

## [t056] Pipeline addition: cluster comparison report (mutation-only vs Hoadley integrated)
- type: research
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- group: pipeline
- created: 2026-04-13

Side-by-side: our summary/mut/clusters/cancer.feather vs Hoadley2018 integrated 28-cluster taxonomy. Where do they agree (validates pipeline)? Where do they differ (where mutations carry non-lineage signal)? See pan-cancer-interpretive-frames synthesis.

## [t059] Focused search: ASXL1 / TET2 disambiguation in solid tumors (CH leakage vs real biology)
- type: research
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- group: searches
- created: 2026-04-13

Open question from CH topic: ASXL1 and TET2 are bona fide tumor suppressors in some lineages but also CH leakage. Disambiguation literature for solid-tumor pan-cancer panel data.

## [t072] F10 [Significant] Saturation-aware per-cancer interpretation context column
- type: dev
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [task:t067]
- group: audit-fixes
- created: 2026-04-13

Severity: Significant. From audit F10. Add cancer_saturation_status column derived from per-cancer cohort N + Lawrence 2014 per-cancer required-N. Flag long-tail rankings for under-sampled cancers.

## [t073] F11 [Minor] Add n_studies_contributing column to gene_cancer_study output
- type: dev
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [task:t067]
- group: audit-fixes
- created: 2026-04-13

Severity: Minor. From audit F11. Trivial: count of non-null per-study columns per row, added as explicit column in output.

## [t077] Pipeline addition: random-effects pooled gene×cancer table (GLMM-logit)
- type: dev
- priority: P1
- status: proposed
- aspects: [software-development]
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: meta-analysis
- created: 2026-04-13



## [t078] Pipeline addition: cross-study co-occurrence / mutual-exclusivity statistic (DISCOVER/WeSME + Stouffer)
- type: dev
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [topic:co-occurrence-and-mutual-exclusivity, search:2026-04-13-cooccurrence-mutual-exclusivity-methods, topic:cross-study-harmonization]
- group: meta-analysis
- created: 2026-04-13



## [t082] Pipeline addition: HGNC gene-symbol alias mapping in convert_to_feather.py
- type: dev
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: pipeline
- created: 2026-04-13



## [t083] Pipeline addition: cancer-type label canonicalization (strip+case; optional OncoTree mapping)
- type: dev
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: pipeline
- created: 2026-04-13



## [t084] Pipeline addition: study-prefix patient_id in combined sample table to prevent cross-study collisions
- type: dev
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: pipeline
- created: 2026-04-13



## [t085] Pipeline addition: silhouette/gap-statistic k-selection + stability check for gene/cancer clustering
- type: dev
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: pipeline
- created: 2026-04-13



## [t086] Pipeline addition: length_is_fallback indicator column + per-run excluded_studies.tsv audit trail
- type: dev
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: pipeline
- created: 2026-04-13



## [t087] Graded ch_contamination_prob column replacing uniform ch_priority_gene boolean
- type: dev
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [search:2026-04-14-asxl1-tet2-ch-disambiguation, topic:clonal-hematopoiesis-contamination, paper:Coombs2018, task:t059]
- group: pipeline
- created: 2026-04-14

Replace the uniform ch_priority_gene boolean emitted by annotate_ch.py with a graded ch_contamination_prob column sourced from Coombs 2018 Table 2 (per-gene variant-level CH confirmation rate in paired-tumor/blood cohort). Anchor values: DNMT3A ~64%, TP53 ~4%, overall across the 9-gene CH panel ~8%. ASXL1 and TET2 intermediate — read Coombs 2018 Table 2 for the precise numbers. Keep the boolean as a backward-compatible column (computed by thresholding the graded prob at 0.5) until downstream consumers migrate. Closes the open question surfaced in t059: uniform CH flagging over-masks bona fide solid-tumor ASXL1 biology (MSI-CRC polyG-indel, CRPC, HNSCC per Katoh 2013).

## [t088] Age-adjusted TMB alongside raw TMB (covariate support for t081)
- type: dev
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [search:2026-04-14-tmb-hypermutator-followup, topic:tumor-mutational-burden, paper:Chalmers2017, task:t081, task:t025]
- group: pipeline
- created: 2026-04-14

Chalmers 2017 documents a 2.4x TMB increase between age 10 and age 90 in 100000-case FoundationOne cohort. Once per-sample TMB is computed in t081, emit a parallel age_adjusted_tmb column that regresses TMB on patient age (when available from cBioPortal clinical tables) and reports the residual. Two columns: raw tmb_mut_per_Mb and age_adjusted_tmb_residual. No surveyed TMB tool (Vega 2021 FoCR, jasonwong-lab/TMB, pyTMB) does this adjustment — cheap pipeline contribution.

## [t090] Pathway-layer benchmark on cross-study cBioPortal data (t043 gap)
- type: research
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [search:2026-04-14-pathway-level-pan-cancer-methods, paper:Reyna2020Pathway, paper:Iorio2018SLAPenrich, paper:Paczkowska2020, task:t043, task:t077, task:t079]
- group: meta-analysis
- created: 2026-04-14

Surfaced as a real gap in t043: no pan-cancer benchmark at the pathway rollup level currently exists (Wu 2022 Brief Bioinform benchmark is gene-level only). Run SLAPenrich vs ActivePathways vs HotNet2 on the pipeline's gene_cancer_study output using a shared pathway database (start with Reactome + Sanchez-Vega-10; KEGG and MSigDB Hallmarks as comparators) across multiple cBioPortal cohorts and report method concordance. Natural methodological contribution. Pre-register pathway database + primary method choice before running (ties to t079 pooling pre-registration).

## [t091] Companion search: TET2 in solid tumors (melanoma, glioma, breast) — disambiguate CH vs biology
- type: research
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- related: [search:2026-04-14-asxl1-tet2-ch-disambiguation, topic:clonal-hematopoiesis-contamination, task:t059]
- group: searches
- created: 2026-04-14

Gap surfaced in t059: TET2 solid-tumor biology literature is thinner than ASXL1. ASXL1 has clear MSI-CRC polyG-indel + CRPC / HNSCC / breast evidence (Katoh 2013). TET2 solid-tumor papers cluster around melanoma (catalytic-domain mutations), glioma (IDH-pathway interaction — TET2 is the IDH-pathway target, so IDH-mutant gliomas carry functional TET2 loss without TET2 mutation), and breast. Focused OpenAlex + PubMed search. Produces doc/searches/YYYY-MM-DD-tet2-solid-tumor-biology.md.

## [t102] Audit two single-word commits on main (a2ce3fc save, c0f48af data) and either amend or document
- type: dev
- priority: P2
- status: proposed
- aspects: [software-development]
- group: meta
- created: 2026-04-17

Two recent main-branch commits have single-word messages ('save', 'data'). Terse messages risk losing context for future sessions and blur the t081 execution history. Run: git show a2ce3fc c0f48af (diffs + stats). If the content is meaningful (non-trivial file additions, config changes), write one short note in doc/meta/ describing what landed and why. If the content is trivially recoverable from the surrounding commits, document the rationale inline in this task's close note. Do NOT amend commits already on main unless explicitly approved — git history on main is shared state.

## [t103] Promote closed or partially-closed open questions from topic files to doc/questions/
- type: research
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [topic:tumor-mutational-burden, topic:clonal-hematopoiesis-contamination, topic:targeted-panel-sequencing-bias, topic:pan-cancer-interpretive-frames, task:t095, task:t097]
- group: questions
- created: 2026-04-17

doc/questions/ is still empty; science-tool project index returns rows: []. Five open methodological questions identified in the 2026-04-14 analysis live inside topic files only and are invisible to the project index. At least two are now answered by landed work: (a) 'per-histology vs universal hypermutator cutoff' — resolved by t097 emitting both Campbell-absolute and Samstein-relative flags; (b) 'MSI-status ingestion policy' — resolved by t095's msi_normalization.py. Others (cross-panel intersection vs callability; CH filter granularity; pathway-database choice) remain open. For each: write a doc/questions/*.md entry using the science template with (question, evidence, status: open|resolved, resolving-task-or-commit). Makes the resolution history discoverable via science-tool project index.

## [t104] Optimize create_correlation_matrices.py: gene x gene corr scales O(n_genes^2) and stalls on whole-exome studies
- type: dev
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t100]
- group: pipeline
- created: 2026-04-17

Surfaced by t100 PoC run 2026-04-17: create_correlation_matrices for brca_tcga_pan_can_atlas_2018 (~1090 samples x ~20k genes) took ~55 min; same expected for ucec_tcga and skcm_tcga. Panel studies (MSK-IMPACT ~341 genes) are fast. Script computes patient_mut.T.corr() which is O(n_genes^2) in both time and memory. Options: (a) use numpy.corrcoef on float32 matrix (typically 5-10x faster than pandas corr), (b) restrict to the top-K variance genes before correlation (add config key max_genes_for_corr default 5000), (c) sparse-aware correlation via sklearn.metrics.pairwise when count matrix is sparse (>95% zeros typical for mutation count matrices). Recommend starting with (a)+(b) and only falling back to (c) if still too slow. Ref: code/scripts/create_correlation_matrices.py:27 (patient_mut.T.corr()).

## [t106] Replace output-path provenance with version stamps in annotate_* scripts (bailey2018_source, cgc_source, sanchez_vega_source)
- type: dev
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t100, interpretation:2026-04-17-poc-run]
- group: pipeline
- created: 2026-04-17

Surfaced by t100 PoC 2026-04-17: the bailey2018_source / cgc_source / sanchez_vega_source columns in gene_cancer_study_annotated.feather and gene_cancer_study_ratio_annotated.feather contain values like 'results/poc-2026-04-17/metadata/bailey2018_drivers.feather' — i.e. the output file path from that specific run. They should be version stamps (e.g. 'bailey2018_v1_2018-08-13_cell' or the file's content hash). Per-run paths change every run, break reproducibility, and leak out_dir into a downstream data file. Fix: add module-level VERSION constants to code/scripts/process_bailey2018_drivers.py, process_cgc.py, process_sanchez_vega_pathways.py and have annotate.py / annotate_ch.py read those constants rather than writing snakemake.input[N] path strings. Evidence: doc/interpretations/2026-04-17-poc-run.md Finding 7, bug table row 7.

## [t107] Backport clustering.* defaults to main configs (config-10k-genes.yml, config-full.yml, config-pan-cancer.yml) OR make cluster rules opt-out when missing
- type: dev
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t100]
- group: pipeline
- created: 2026-04-17

Surfaced by t100 PoC 2026-04-17: cluster_genes.py and cluster_cancer_types.py require config['clustering']['gene']['k'], ['gene_min_mutations'], ['cancer_min_mutations'], ['random_seed'] (and mirror keys under ['cancer']). No shipped config prior to config-poc.yml contained these keys. This means every run of the main pipeline prior to this PoC would have crashed at the cluster rules if rule all was fully evaluated — the pre-t081 runs presumably did not have cluster rules in their rule all target list. Fix: either (a) backport the default clustering sub-tree from config-poc.yml to the 3 main configs, or (b) make the cluster scripts fall back to sensible defaults when the key is absent (with a warning). Option (a) is more explicit; option (b) is more forgiving.

## [t108] Investigate is_hypermutator_relative reporting ~45% for BRCA (Samstein top-20% should cap at ~20%)
- type: dev
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t097, task:t100, paper:Samstein2019, interpretation:2026-04-17-poc-run]
- group: pipeline
- created: 2026-04-17

Surfaced by t100 PoC 2026-04-17: is_hypermutator_relative reports 45.5% for brca_tcga_pan_can_atlas_2018 and 36.4% for skcm_tcga_pan_can_atlas_2018 (from doc/interpretations/2026-04-17-poc-run.md Finding 4). The Samstein 2019 definition is 'top-20%% TMB within the sample's histology' — which should yield at most ~20%% hypermutators per cancer type (slightly more with ties at the boundary). 45%% / 36%% far exceed this. Likely causes: (a) tied-sample promotion at the 80th-percentile cut without explicit tiebreak policy, (b) the per-histology grouping key is cancer_type but the TCGA 'cancer_type' labels collapse many distinct histologies into one bucket (e.g. 'Breast Cancer'), so a large fraction of samples tie at a low TMB boundary, or (c) an off-by-one in the quantile cut logic. Inspect _relative_top_quintile_flag in code/scripts/annotate_hypermutators.py (line 200 area).

## [t109] Implement per-study cancer-type signature restriction for SigProfilerAssignment
- type: dev
- priority: P2
- status: active
- aspects: [software-development]
- related: [topic:signature-decomposition-unmatched-normal, question:q008-signature-decomposition-tissue-background-subtraction, paper:Yaacov2023]
- group: pipeline
- created: 2026-04-18

Add a lookup table 'data/cosmic_cancer_type_signatures.tsv' derived from Alexandrov 2020 Extended Data Figure 5 (COSMIC v3 signature x cancer type matrix) and a Snakemake rule that restricts SigProfilerAssignment (or equivalent) to type-appropriate signatures before any per-study decomposition analysis is run. Rationale: unrestricted COSMIC v3 refit over-fits on tissue-nonspecific normal-tissue signatures (SBS1, SBS5, SBS18) in unmatched-normal cBioPortal studies; cancer-type-prior restriction is the cheapest intervention documented in topic:signature-decomposition-unmatched-normal. Blocked-by: none (Alexandrov2020 ED Fig 5 is public). Expected output: per-study signature exposure vector only over cancer-type-allowed signatures; downstream: feeds q008 background subtraction and q009 SBS1-bias QC.

## [t110] Validate SBS1/SBS5 ratio as unmatched-normal contamination proxy (MC3 vs cBioPortal)
- type: research
- priority: P2
- status: blocked
- aspects: [computational-analysis]
- related: [topic:signature-decomposition-unmatched-normal, question:q009-sbs1-lrr-bias-as-normal-contamination-flag, paper:Yaacov2023, paper:Xu2025]
- blocked-by: [task:t109]
- group: pipeline
- created: 2026-04-18

For ≥1 cancer type present in both a matched-normal study (TCGA MC3 pseudo-study, 'tcga_mc3') and an unmatched-normal cBioPortal study, run mutational-signature decomposition on each cohort, extract per-sample SBS1 and SBS5 exposures, and test whether unmatched-normal studies show a statistically significant SBS1 excess (or SBS1/SBS5 ratio shift) vs matched-normal. Rationale: Yaacov2023 established that SBS1 retains strong LRR bias in normal tissue but loses it in cancer — the SBS1 exposure should therefore be systematically elevated in unmatched-normal cohorts if normal-tissue mutations are leaking through. This task quantifies the magnitude before investing in a per-study flag or background subtraction. Depends on: t109 (signature-restriction rule). Outputs: per-cancer-type SBS1 exposure distribution comparison; decision on whether a ratio threshold is operationally useful for q009.

## [t112] Integrate Lee-Six 2018 blood (or Xu 2025 dbGaP) as second normal-tissue source for t111 outputs
- type: dev
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t111, topic:signature-decomposition-unmatched-normal, question:q006-ch-priority-gene-completeness, question:q008-signature-decomposition-tissue-background-subtraction, paper:LeeSix2018, paper:Xu2025]
- group: pipeline
- created: 2026-04-18

Follow-up to t111 (which was reduced to Li2021-only by the 2026-04-19 data-access gate because Xu2025 per-variant data is dbGaP-controlled). Add a second open-access normal-tissue source to enrich data/normal_tissue_spectra.tsv and data/normal_tissue_burden.tsv. Preferred source: Lee-Six 2018 (Nature, DOI 10.1038/s41586-018-0497-0) — single-donor ~140 HSC WGS colonies — complements Li2021's solid-tissue bias with blood where CH matters for q006/q008. Second-choice source: Xu2025 via dbGaP DAR (weeks of calendar time; only worth pursuing if a user has existing GTEx access). This task refactors code/scripts/extract_normal_tissue_spectra.py into the plugin-style adapters/ pattern planned in t111's scope brainstorming (option C: 'start hard-coded to 2 sources, plugin-ize when 3rd arrives').

## [t113] Close t111 assembly range-check TODO — verify chrom/pos against declared assembly
- type: dev
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [task:t111, interpretation:2026-04-19-t111-normal-tissue-spectra-pipeline]
- group: pipeline
- created: 2026-04-19

Current validate_input_contract accepts the assembly parameter but does not range-check chrom/pos against per-chromosome lengths (marked TODO(t111-followup) at code/scripts/extract_normal_tissue_spectra.py:96-100). A caller who declares wrong assembly gets silent acceptance. Fix: encode GRCh37/GRCh38 max-chromosome-lengths as module constants and validate df['pos'].max() <= length_dict[chrom] for each chromosome. Becomes load-bearing when t112 introduces GRCh38 sources. ~30 min + one test.

## [t114] Pre-register q007 null-model correction impact before rolling into frequency pipeline
- type: research
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [task:t111, question:q007-cross-tissue-somatic-mutation-rate-variation-as-null-model, paper:Li2021]
- group: pipeline
- created: 2026-04-19

Before applying the t111 per-tissue snvs_per_mb correction to gene_cancer_study_ratio_annotated.feather frequencies, pre-register: (1) expected number of gene-cancer rankings that shift and by how many positions; (2) head-to-head comparison against a Martincorena 2017 dN/dS-based null as a simpler baseline. If the two approaches rank genes identically, t111's value-add collapses. Prevents ships-before-thinks bias on whether the empirical null is actually discriminating versus a uniform-rate-per-gene-length null. Deliverable: doc/meta/pre-registration-q007-null-model-correction.md.

## [t116] t077: add isolated R meta-analysis env and CLI skeleton
- type: dev
- priority: P1
- status: proposed
- aspects: [software-development]
- related: [task:t077, task:t079, doc:2026-04-22-t077-glmm-logit-plan]
- blocked-by: [task:t077]
- group: meta-analysis
- created: 2026-04-22

Add code/envs/r-meta.yml and the run_gene_cancer_meta_analysis.R entrypoint with a schema-valid round-trip path before fitting real models.

## [t117] t077: implement confirmatory GLMM fit and fallback status logic
- type: dev
- priority: P1
- status: proposed
- aspects: [software-development]
- related: [task:t077, task:t079, doc:2026-04-22-t077-glmm-logit-plan]
- blocked-by: [task:t077]
- group: meta-analysis
- created: 2026-04-22

Implement the pre-registered metafor::rma.glmm fit, cell filters, pooled effect outputs, heterogeneity metrics, and REML-logit fallback/status handling.

## [t118] t077: verification and pre-registration conformance pass
- type: dev
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t077, task:t079, doc:2026-04-22-t077-glmm-logit-plan]
- blocked-by: [task:t077]
- group: meta-analysis
- created: 2026-04-22

Run targeted tests, workflow-level sanity checks, and document any deviation from the active t077 pre-registration before reporting pooled results.

## [t119] t077: add diagnostics and sensitivity outputs
- type: dev
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t077, task:t079, doc:2026-04-22-t077-glmm-logit-plan]
- blocked-by: [task:t077]
- group: meta-analysis
- created: 2026-04-22

Emit convergence/fallback diagnostics plus the hold-out or leave-one-out sensitivity outputs required to evaluate the pre-registered integrity checks.

## [t120] t077: wire Snakemake rule and join pooled outputs onto canonical tables
- type: dev
- priority: P1
- status: proposed
- aspects: [software-development]
- related: [task:t077, doc:2026-04-22-t077-glmm-logit-plan]
- blocked-by: [task:t077]
- group: meta-analysis
- created: 2026-04-22

Add the workflow rules that build the long pooled input and run the R model, then join the resulting pooled metrics onto the consumer-facing annotated output surface.
