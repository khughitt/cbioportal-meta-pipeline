## [t025] Follow-up search: TMB harmonization (Friends-of-Cancer-Research / Buchhalter)
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- group: searches
- created: 2026-04-13

Dedicated search for panel-vs-WES TMB calibration methods.

## [t055] Pipeline addition: M/C-class descriptor (mutation-vs-CNA hyperbola)
- priority: P3
- status: deferred
- aspects: [software-development]
- group: pipeline
- created: 2026-04-13

Compute per-tumor and per-cancer mutation-count vs SCNA-burden axis (Ciriello2013 cancer genome hyperbola). Cheap secondary descriptor. Blocked: requires CNA data ingestion which our pipeline does not currently have.

Blocked on CNA ingestion — no CNA scripts in code/scripts/, no rule in Snakefile, and CNA is outside current specs/research-question.md scope. Revisit when / if CNA modality is added.

## [t056] Pipeline addition: cluster comparison report (mutation-only vs Hoadley integrated)
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- group: pipeline
- created: 2026-04-13

Side-by-side: our summary/mut/clusters/cancer.feather vs Hoadley2018 integrated 28-cluster taxonomy. Where do they agree (validates pipeline)? Where do they differ (where mutations carry non-lineage signal)? See pan-cancer-interpretive-frames synthesis.

## [t059] Focused search: ASXL1 / TET2 disambiguation in solid tumors (CH leakage vs real biology)
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- group: searches
- created: 2026-04-13

Open question from CH topic: ASXL1 and TET2 are bona fide tumor suppressors in some lineages but also CH leakage. Disambiguation literature for solid-tumor pan-cancer panel data.

## [t072] F10 [Significant] Saturation-aware per-cancer interpretation context column
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [task:t067]
- group: audit-fixes
- created: 2026-04-13

Severity: Significant. From audit F10. Add cancer_saturation_status column derived from per-cancer cohort N + Lawrence 2014 per-cancer required-N. Flag long-tail rankings for under-sampled cancers.

## [t073] F11 [Minor] Add n_studies_contributing column to gene_cancer_study output
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [task:t067]
- group: audit-fixes
- created: 2026-04-13

Severity: Minor. From audit F11. Trivial: count of non-null per-study columns per row, added as explicit column in output.

## [t082] Pipeline addition: HGNC gene-symbol alias mapping in convert_to_feather.py
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: pipeline
- created: 2026-04-13



## [t083] Pipeline addition: cancer-type label canonicalization (strip+case; optional OncoTree mapping)
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: pipeline
- created: 2026-04-13



## [t084] Pipeline addition: study-prefix patient_id in combined sample table to prevent cross-study collisions
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: pipeline
- created: 2026-04-13



## [t085] Pipeline addition: silhouette/gap-statistic k-selection + stability check for gene/cancer clustering
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: pipeline
- created: 2026-04-13



## [t086] Pipeline addition: length_is_fallback indicator column + per-run excluded_studies.tsv audit trail
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [task:bias-audit-cross-study-aggregation-pipeline]
- group: pipeline
- created: 2026-04-13



## [t087] Graded ch_contamination_prob column replacing uniform ch_priority_gene boolean
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [search:2026-04-14-asxl1-tet2-ch-disambiguation, topic:clonal-hematopoiesis-contamination, paper:Coombs2018, task:t059]
- group: pipeline
- created: 2026-04-14

Replace the uniform ch_priority_gene boolean emitted by annotate_ch.py with a graded ch_contamination_prob column sourced from Coombs 2018 Table 2 (per-gene variant-level CH confirmation rate in paired-tumor/blood cohort). Anchor values: DNMT3A ~64%, TP53 ~4%, overall across the 9-gene CH panel ~8%. ASXL1 and TET2 intermediate — read Coombs 2018 Table 2 for the precise numbers. Keep the boolean as a backward-compatible column (computed by thresholding the graded prob at 0.5) until downstream consumers migrate. Closes the open question surfaced in t059: uniform CH flagging over-masks bona fide solid-tumor ASXL1 biology (MSI-CRC polyG-indel, CRPC, HNSCC per Katoh 2013).

## [t088] Age-adjusted TMB alongside raw TMB (covariate support for t081)
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [search:2026-04-14-tmb-hypermutator-followup, topic:tumor-mutational-burden, paper:Chalmers2017, task:t081, task:t025]
- group: pipeline
- created: 2026-04-14

Chalmers 2017 documents a 2.4x TMB increase between age 10 and age 90 in 100000-case FoundationOne cohort. Once per-sample TMB is computed in t081, emit a parallel age_adjusted_tmb column that regresses TMB on patient age (when available from cBioPortal clinical tables) and reports the residual. Two columns: raw tmb_mut_per_Mb and age_adjusted_tmb_residual. No surveyed TMB tool (Vega 2021 FoCR, jasonwong-lab/TMB, pyTMB) does this adjustment — cheap pipeline contribution.

## [t090] Pathway-layer benchmark on cross-study cBioPortal data (t043 gap)
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [search:2026-04-14-pathway-level-pan-cancer-methods, paper:Reyna2020Pathway, paper:Iorio2018SLAPenrich, paper:Paczkowska2020, task:t043, task:t077, task:t079]
- group: meta-analysis
- created: 2026-04-14

Surfaced as a real gap in t043: no pan-cancer benchmark at the pathway rollup level currently exists (Wu 2022 Brief Bioinform benchmark is gene-level only). Run SLAPenrich vs ActivePathways vs HotNet2 on the pipeline's gene_cancer_study output using a shared pathway database (start with Reactome + Sanchez-Vega-10; KEGG and MSigDB Hallmarks as comparators) across multiple cBioPortal cohorts and report method concordance. Natural methodological contribution. Pre-register pathway database + primary method choice before running (ties to t079 pooling pre-registration).

## [t091] Companion search: TET2 in solid tumors (melanoma, glioma, breast) — disambiguate CH vs biology
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- related: [search:2026-04-14-asxl1-tet2-ch-disambiguation, topic:clonal-hematopoiesis-contamination, task:t059]
- group: searches
- created: 2026-04-14

Gap surfaced in t059: TET2 solid-tumor biology literature is thinner than ASXL1. ASXL1 has clear MSI-CRC polyG-indel + CRPC / HNSCC / breast evidence (Katoh 2013). TET2 solid-tumor papers cluster around melanoma (catalytic-domain mutations), glioma (IDH-pathway interaction — TET2 is the IDH-pathway target, so IDH-mutant gliomas carry functional TET2 loss without TET2 mutation), and breast. Focused OpenAlex + PubMed search. Produces doc/searches/YYYY-MM-DD-tet2-solid-tumor-biology.md.

## [t102] Audit two single-word commits on main (a2ce3fc save, c0f48af data) and either amend or document
- priority: P3
- status: proposed
- aspects: [software-development]
- group: meta
- created: 2026-04-17

Two recent main-branch commits have single-word messages ('save', 'data'). Terse messages risk losing context for future sessions and blur the t081 execution history. Run: git show a2ce3fc c0f48af (diffs + stats). If the content is meaningful (non-trivial file additions, config changes), write one short note in doc/meta/ describing what landed and why. If the content is trivially recoverable from the surrounding commits, document the rationale inline in this task's close note. Do NOT amend commits already on main unless explicitly approved — git history on main is shared state.

## [t103] Promote closed or partially-closed open questions from topic files to doc/questions/
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [topic:tumor-mutational-burden, topic:clonal-hematopoiesis-contamination, topic:targeted-panel-sequencing-bias, topic:pan-cancer-interpretive-frames, task:t095, task:t097]
- group: questions
- created: 2026-04-17

doc/questions/ is still empty; science-tool project index returns rows: []. Five open methodological questions identified in the 2026-04-14 analysis live inside topic files only and are invisible to the project index. At least two are now answered by landed work: (a) 'per-histology vs universal hypermutator cutoff' — resolved by t097 emitting both Campbell-absolute and Samstein-relative flags; (b) 'MSI-status ingestion policy' — resolved by t095's msi_normalization.py. Others (cross-panel intersection vs callability; CH filter granularity; pathway-database choice) remain open. For each: write a doc/questions/*.md entry using the science template with (question, evidence, status: open|resolved, resolving-task-or-commit). Makes the resolution history discoverable via science-tool project index.

## [t104] Optimize create_correlation_matrices.py: gene x gene corr scales O(n_genes^2) and stalls on whole-exome studies
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t100]
- group: pipeline
- created: 2026-04-17

Surfaced by t100 PoC run 2026-04-17: create_correlation_matrices for brca_tcga_pan_can_atlas_2018 (~1090 samples x ~20k genes) took ~55 min; same expected for ucec_tcga and skcm_tcga. Panel studies (MSK-IMPACT ~341 genes) are fast. Script computes patient_mut.T.corr() which is O(n_genes^2) in both time and memory. Options: (a) use numpy.corrcoef on float32 matrix (typically 5-10x faster than pandas corr), (b) restrict to the top-K variance genes before correlation (add config key max_genes_for_corr default 5000), (c) sparse-aware correlation via sklearn.metrics.pairwise when count matrix is sparse (>95% zeros typical for mutation count matrices). Recommend starting with (a)+(b) and only falling back to (c) if still too slow. Ref: code/scripts/create_correlation_matrices.py:27 (patient_mut.T.corr()).

## [t106] Replace output-path provenance with version stamps in annotate_* scripts (bailey2018_source, cgc_source, sanchez_vega_source)
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t100, interpretation:2026-04-17-poc-run]
- group: pipeline
- created: 2026-04-17

Surfaced by t100 PoC 2026-04-17: the bailey2018_source / cgc_source / sanchez_vega_source columns in gene_cancer_study_annotated.feather and gene_cancer_study_ratio_annotated.feather contain values like 'results/poc-2026-04-17/metadata/bailey2018_drivers.feather' — i.e. the output file path from that specific run. They should be version stamps (e.g. 'bailey2018_v1_2018-08-13_cell' or the file's content hash). Per-run paths change every run, break reproducibility, and leak out_dir into a downstream data file. Fix: add module-level VERSION constants to code/scripts/process_bailey2018_drivers.py, process_cgc.py, process_sanchez_vega_pathways.py and have annotate.py / annotate_ch.py read those constants rather than writing snakemake.input[N] path strings. Evidence: doc/interpretations/2026-04-17-poc-run.md Finding 7, bug table row 7.

## [t107] Backport clustering.* defaults to main configs (config-10k-genes.yml, config-full.yml, config-pan-cancer.yml) OR make cluster rules opt-out when missing
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t100]
- group: pipeline
- created: 2026-04-17

Surfaced by t100 PoC 2026-04-17: cluster_genes.py and cluster_cancer_types.py require config['clustering']['gene']['k'], ['gene_min_mutations'], ['cancer_min_mutations'], ['random_seed'] (and mirror keys under ['cancer']). No shipped config prior to config-poc.yml contained these keys. This means every run of the main pipeline prior to this PoC would have crashed at the cluster rules if rule all was fully evaluated — the pre-t081 runs presumably did not have cluster rules in their rule all target list. Fix: either (a) backport the default clustering sub-tree from config-poc.yml to the 3 main configs, or (b) make the cluster scripts fall back to sensible defaults when the key is absent (with a warning). Option (a) is more explicit; option (b) is more forgiving.

## [t108] Investigate is_hypermutator_relative reporting ~45% for BRCA (Samstein top-20% should cap at ~20%)
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t097, task:t100, paper:Samstein2019, interpretation:2026-04-17-poc-run]
- group: pipeline
- created: 2026-04-17

Surfaced by t100 PoC 2026-04-17: is_hypermutator_relative reports 45.5% for brca_tcga_pan_can_atlas_2018 and 36.4% for skcm_tcga_pan_can_atlas_2018 (from doc/interpretations/2026-04-17-poc-run.md Finding 4). The Samstein 2019 definition is 'top-20%% TMB within the sample's histology' — which should yield at most ~20%% hypermutators per cancer type (slightly more with ties at the boundary). 45%% / 36%% far exceed this. Likely causes: (a) tied-sample promotion at the 80th-percentile cut without explicit tiebreak policy, (b) the per-histology grouping key is cancer_type but the TCGA 'cancer_type' labels collapse many distinct histologies into one bucket (e.g. 'Breast Cancer'), so a large fraction of samples tie at a low TMB boundary, or (c) an off-by-one in the quantile cut logic. Inspect _relative_top_quintile_flag in code/scripts/annotate_hypermutators.py (line 200 area).

## [t112] Integrate Lee-Six 2018 blood (or Xu 2025 dbGaP) as second normal-tissue source for t111 outputs
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [task:t111, topic:signature-decomposition-unmatched-normal, question:q006-ch-priority-gene-completeness, question:q008-signature-decomposition-tissue-background-subtraction, paper:LeeSix2018, paper:Xu2025]
- group: pipeline
- created: 2026-04-18

Follow-up to t111 (which was reduced to Li2021-only by the 2026-04-19 data-access gate because Xu2025 per-variant data is dbGaP-controlled). Add a second open-access normal-tissue source to enrich data/normal_tissue_spectra.tsv and data/normal_tissue_burden.tsv. Preferred source: Lee-Six 2018 (Nature, DOI 10.1038/s41586-018-0497-0) — single-donor ~140 HSC WGS colonies — complements Li2021's solid-tissue bias with blood where CH matters for q006/q008. Second-choice source: Xu2025 via dbGaP DAR (weeks of calendar time; only worth pursuing if a user has existing GTEx access). This task refactors code/scripts/extract_normal_tissue_spectra.py into the plugin-style adapters/ pattern planned in t111's scope brainstorming (option C: 'start hard-coded to 2 sources, plugin-ize when 3rd arrives').

## [t113] Close t111 assembly range-check TODO — verify chrom/pos against declared assembly
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [task:t111, interpretation:2026-04-19-t111-normal-tissue-spectra-pipeline]
- group: pipeline
- created: 2026-04-19

Current validate_input_contract accepts the assembly parameter but does not range-check chrom/pos against per-chromosome lengths (marked TODO(t111-followup) at code/scripts/extract_normal_tissue_spectra.py:96-100). A caller who declares wrong assembly gets silent acceptance. Fix: encode GRCh37/GRCh38 max-chromosome-lengths as module constants and validate df['pos'].max() <= length_dict[chrom] for each chromosome. Becomes load-bearing when t112 introduces GRCh38 sources. ~30 min + one test.

## [t114] Pre-register q007 null-model correction impact before rolling into frequency pipeline
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [task:t111, question:q007-cross-tissue-somatic-mutation-rate-variation-as-null-model, paper:Li2021]
- group: pipeline
- created: 2026-04-19

Before applying the t111 per-tissue snvs_per_mb correction to gene_cancer_study_ratio_annotated.feather frequencies, pre-register: (1) expected number of gene-cancer rankings that shift and by how many positions; (2) head-to-head comparison against a Martincorena 2017 dN/dS-based null as a simpler baseline. If the two approaches rank genes identically, t111's value-add collapses. Prevents ships-before-thinks bias on whether the empirical null is actually discriminating versus a uniform-rate-per-gene-length null. Deliverable: doc/meta/pre-registration-q007-null-model-correction.md.

## [t127] First q008 quantitative pass: unmatched-normal contamination magnitude using t111 normal_tissue_spectra
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [question:q008, task:t111, meta:next-steps-2026-04-24]
- group: meta-analysis
- created: 2026-04-24

Exercise the Li2021+Xu2025 reference spectra landed by t111 against the tcga_mc3 vs msk_impact_2017 pair (or equivalent matched/unmatched study pair) to produce a first numeric estimate of unmatched-normal contamination magnitude. Closes the built-but-unexploited risk called out in meta:next-steps-2026-04-24 gap 2.

## [t128] Emit retroactive datapackage.json manifests for results/poc-2026-04-17/ and results/signature-brca-2026-04-22/
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t100, meta:next-steps-2026-04-24]
- group: pipeline
- created: 2026-04-24

Two workflow output directories currently sit on disk with no datapackage.json manifests: results/poc-2026-04-17/ (t100 PoC annotated artifact) and results/signature-brca-2026-04-22/ (t109/t110 signature-restriction outputs). Write Frictionless Data Package manifests retroactively so provenance is filesystem-readable rather than narrative-only. Recurring gap flagged on both 2026-04-22 and 2026-04-24.

## [t129] Length × PubMed-mention regression pipeline step (q011)
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [question:q011-gene-length-as-literature-attention-confounder, topic:mutation-rate-normalization, discussion:2026-04-24-gene-length-bias-in-mutation-rankings-and-literature, task:t082]
- group: meta-analysis
- created: 2026-04-24

Implement the regression spec'd in q011: log(mention_count+1) ~ log(protein_length) + log(mutation_count+1) over protein-coding genes (PubTator 2026-01-16 + UniProt + cBioPortal aggregate counts). Report marginal vs partial length slope with bootstrap CIs. Subgroup by Bailey 2018 driver list. Sensitivity: dNdScv-corrected counts, disease-co-mention covariate, non-cancer placebo slice. Output: doc/interpretations/<date>-q011-length-attention-regression.md plus a length-residualized 'attention prior' feather under models/. Requires HGNC alias mapping (t082) for the PubTator↔UniProt join.

## [t130] Paper summary: Stoeger & Nunes Amaral 2018 (gene-attention accessibility features)
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [question:q011-gene-length-as-literature-attention-confounder, topic:mutation-rate-normalization, discussion:2026-04-24-gene-length-bias-in-mutation-rankings-and-literature]
- group: searches
- created: 2026-04-24

Use science:research-papers to summarize Stoeger T, Gerlach M, Morimoto RI, Nunes Amaral LA. 2018. 'Large-scale investigation of the reasons why potentially important genes are ignored.' PLOS Biology 16(9):e2006643. doi:10.1371/journal.pbio.2006643. Methodological reference for the literature-attention bias side of q011 — they show chemical/experimental accessibility features predict per-gene publication count better than biological importance. Need: their list of accessibility features, their model form, effect-size estimates, and how (or whether) they treat gene/transcript length specifically.

## [t131] Opt dNdScv into rule all via config-pan-cancer-dndscv.yml + three-way ranking comparison
- priority: P2
- status: proposed
- aspects: [computational-analysis, software-development]
- related: [topic:mutation-rate-normalization, discussion:2026-04-24-gene-length-bias-in-mutation-rankings-and-literature, question:q011-gene-length-as-literature-attention-confounder, paper:Martincorena2017]
- group: pipeline
- created: 2026-04-24

Add a side config code/config/config-pan-cancer-dndscv.yml that includes the per-study dNdScv outputs (studies/{id}/mut/dndscv/genes.feather) in rule all. Then write a comparison report: raw vs length-adjusted vs dNdScv-selection rankings, Spearman + Jaccard@10/50/100/500, and per-list correlation with PubTator gene-mention counts. Closes the 'length-only is below the 2013 methodology bar' finding from the bias audit and topic:mutation-rate-normalization. CONSTRAINT (per memory:r-reproducibility): the dNdScv rule must use a conda/mamba env YAML or Docker image — never assume system R.

## [t132] Literature search: mutation-ordering methods for cross-sectional data (MHN / CBN / CAPRI / REVOLVER / PCAWG chronology)
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [question:q012-mutation-ordering-cross-sectional-inference, discussion:2026-04-24-mutation-ordering-and-path-dependency, task:t078]
- group: searches
- created: 2026-04-24

Method × assumption table comparing Mutual Hazard Networks (Schill 2020), Conjunctive Bayesian Networks (Beerenwinkel 2007), CAPRI/TRONCO (Caravagna 2016), REVOLVER (Caravagna 2018), HINTRA, PMCE, and PCAWG pan-cancer chronology (Gerstung 2020 Nature 578:122). Deliverable: doc/searches/YYYY-MM-DD-mutation-ordering-methods.md. Goal: decide whether detecting A→B asymmetries in cBioPortal data is a method-selection problem (pick MHN) or a novel-methods problem.

## [t133] Audit VAF availability across cBioPortal/GENIE studies
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [question:q012-mutation-ordering-cross-sectional-inference, discussion:2026-04-24-mutation-ordering-and-path-dependency]
- group: audits
- created: 2026-04-24

Hard gate on any clonality-based ordering work. For each study in code/config/config-full.yml, inspect pre-convert_to_feather MAF headers and tally which carry (a) tumor_f / VAF directly, (b) t_alt_count + t_ref_count (can compute VAF), (c) neither. Also record sequencing type (WES vs panel) and matched-normal status. Output: doc/audits/YYYY-MM-DD-vaf-availability-audit.md. Decision rule: if ≥50% of samples retain VAF, unlock pipeline change to preserve VAF; if not, restrict ordering work to CBN/MHN-style population-level inference only.

## [t134] Pipeline addition: retain VAF (t_alt_count, t_ref_count, tumor_f) in per-study variant feathers
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [question:q012-mutation-ordering-cross-sectional-inference]
- blocked-by: [Audit VAF availability across cBioPortal/GENIE studies]
- group: pipeline
- created: 2026-04-24

Extend convert_to_feather.py to retain per-variant allele-count columns alongside gene/sample presence calls. Unblocks clonality-based ordering (MHN validation companion), CCF estimation, per-sample signature deconvolution at variant level, and general driver-evolution work. Contingent on VAF-availability audit confirming retention is worthwhile.

## [t135] MHN fit per histology as directed companion to t078 co-occurrence results
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- related: [question:q012-mutation-ordering-cross-sectional-inference, task:t078, task:t081, task:t111]
- group: meta-analysis
- created: 2026-04-24

t078 co-occurrence/mutual-exclusivity landed 2026-04-25 (no longer blocking). Add Mutual Hazard Network (Schill 2020) fit using the same sample-specific-background-rate null and per-sample callability mask. Report primary results at Sanchez-Vega 10-pathway level; gene-level as drill-down. Stratify per histology and per hypermutator class (t081). Calibrate against PCAWG Gerstung 2020 pan-cancer chronology Table 1 before reporting any novel edges.

## [t136] Canonicalize all variant coordinates to GRCh38 at ingestion (liftover from hg19)
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t131, topic:mutation-rate-normalization, discussion:2026-04-24-gene-length-bias-in-mutation-rankings-and-literature]
- group: pipeline
- created: 2026-04-24

Add a liftover step in convert_to_feather.py that maps hg19-native study variants to GRCh38 using CrossMap or pyliftover with UCSC hg19ToHg38.over.chain.gz. Retain original chr/pos/build columns for audit. Single canonical build downstream unlocks dNdScv refdb selection, future GRCh38-only annotation sources (gnomAD v4, ClinVar, dbNSFP v4.x, AlphaMissense, latest COSMIC), and removes a class of silent-degradation bugs across the pipeline. Exonic SNV loss expected <0.1% (per UCSC chain coverage). This is the long-term destination flagged during t131 design — t131 itself uses cheaper per-study refdb routing as an interim. Out of scope for this task: re-running upstream tooling against the lifted coordinates (signature callers, replication-timing joins). Plan separately for those once the liftover artifact is in place.

## [t137] t078 SELECT pipeline integration wiring (production prerequisites)
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t078, task:t081]
- blocked-by: [t081]
- group: pipeline
- created: 2026-04-25

t078 implementation landed unit-tested + DAG-dry-run-validated, but the
plan referenced upstream artefacts that the existing pipeline does not
currently produce. Discovered when attempting an end-to-end smoke run.
Wiring the gaps closed will let the SELECT rules run on real data:

1. **`gene_sample_long.feather`** — t078 rules read
   `summary/mut/table/gene_sample_long.feather` (per-sample × gene long
   table). No current rule produces it. Needs a new
   `build_gene_sample_long` rule that derives per-(composite_sample_id,
   symbol) rows from the per-study `studies/{id}/mut/table/mut.feather`
   files (concat + project + dedupe).

2. **`samples_annotated.feather`** — t078 expects the
   `metadata/samples_annotated.feather` written by the t081
   hypermutator pipeline. The 10k dataset does not currently have this
   file produced; running the hypermutator pipeline against the 10k
   config would land it. Blocked by t081 readiness for this dataset.

3. **`bailey_alteration_class.feather` schema mismatch** — t078 references
   `metadata/bailey_alteration_class.feather` with cols (symbol,
   alteration_class). The existing `process_bailey2018_drivers` rule
   writes `metadata/bailey2018_drivers.feather` with a different schema.
   Either (i) switch t078 to read the existing feather and adapt its
   loader to the actual schema, or (ii) add a small adapter rule that
   projects the bailey drivers feather to the expected
   (symbol, alteration_class) shape.

4. **`sanchez_vega_pathways.tsv` vs `.feather`** — t078 reads the TSV;
   the existing `process_sanchez_vega_pathways` rule writes a feather.
   Either (i) switch t078 to read the feather, or (ii) add a TSV export
   to the existing rule. Recommend (i) — feather is canonical.

5. **`sample_panel_map.feather`** — producible by the rule t078 added
   (Task 7 of the implementation plan); requires
   `samples_annotated.feather` to exist first (depends on item 2).

After wiring: smoke-run with `n_permut=50` and 1-2 cancer types to
verify production data flows end-to-end, then bump to full
`n_permut=1000` for the headline run.

## [t138] Add canalization-collapse interpretive note to t081 hypermutator topic
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- related: [task:t081, paper:Bavisetty2025, paper:Lu2023, paper:Rashid2025, paper:Jung2025, synthesis:2026-04-25-canalization-gene-regulatory-networks, topic:tumor-mutational-burden]
- group: docs
- created: 2026-04-25

Add a short interpretive section to the hypermutator/TMB topic note (or a new sub-note) framing 'is_hypermutator = True' tumors as cells in which canalization has collapsed, and the 8-category hypermutator_reason audit trail (pole_hotspot / pold1_hotspot / msi_h / gmm_upper_mode / gmm_lower_mode / zscore_fallback_high / zscore_fallback_low / tmb_unavailable) as different *modes* of canalization failure. Source: doc/papers/synthesis-2026-04-25-canalization-gene-regulatory-networks.md (Combined implications #2). Cheap, doc-only — no pipeline code change. Cross-link from the topic note back to the synthesis and to Bavisetty2025, Lu2023, Rashid2025, Jung2025.

## [t139] Promote t077 meta-analysis to canonical cross-study aggregation
- priority: P2
- status: proposed
- aspects: [computational-analysis, software-development]
- related: [task:t077, task:t131, task:t086]
- group: pipeline
- created: 2026-04-25

The simple sample-weighted aggregation in `create_combined_gene_cancer_freq_table.py` bakes in the assumption that all studies measure all cancers identically, which fails for mixed-panel cohorts (e.g., metastatic_solid_tumors_mich_2017, pog570_bcgsc_2020 contributing 4-8 samples to cancer types where another study contributes hundreds). The current guardrail (the `ValueError: Per-cancer cohort-size recovery assumption violated` at line 346) hard-fails the rule rather than computing a biased aggregate.

The project's t077 meta-analysis pipeline (`run_gene_cancer_meta_analysis.R`) is the right long-term home for cross-study aggregation: each study is treated as an independent stratum, between-study heterogeneity is absorbed into variance components, and per-(study, cancer) cohort-size differences are handled correctly without requiring the homogeneity assumption.

**Goal**: promote `gene_cancer_pooled.feather` (t077 output) to the canonical cross-study aggregation. Demote the simple sample-weighted aggregation to "exploratory descriptive only" (or remove if no consumer remains). Have downstream rules — including `join_dndscv_into_annotated` (t131) — source from the meta-analysis output.

**Why dndscv first**: the t131 dNdScv chain's per-gene min_qglobal rollup is itself a meta-analysis-style aggregation. Sourcing its annotation feather from a meta-analysis-based aggregation is more philosophically consistent than sourcing from the naive sample-weighted sum.

**Effects**:
- Removes the load-bearing role of the cohort-size validation in create_combined_gene_cancer_freq_table — that validation can either be retired or moved to a separate diagnostic rule.
- Unblocks future run configs with mixed-panel-cohort studies without requiring per-(study, cancer) exclusion lists.
- Keeps the existing gene_cancer_study.feather long-format output intact (per the t131 review interim split) — this task only changes which AGGREGATION is canonical, not what's available.

**Cross-references**: this task is the long-term destination; a short-term split was applied 2026-04-25 to unblock t131 (see commit history).

## [t140] Adopt 2026-04-25 Science P1 conventions
- priority: P3
- status: proposed
- aspects: [project-conventions]
- created: 2026-04-25

cbioportal already converges on the canonical Science conventions established by the 2026-04-25 P1 rollout (`science/docs/plans/2026-04-25-conventions-audit-p1-rollout.md`). All five script-driven shape rules in `science/scripts/migrate_downstream_conventions.py` produce zero changes against this project (verified 2026-04-25):

- report-id-prefix: 0
- synthesis-type-mm30: 0
- synthesis-type-pl-emergent-threads: 0
- synthesis-report-kind-pl-hyp: 0
- pre-registration-type: 0
- natural-systems-pre-reg-frontmatter: 0 (report-only)

Pending adoption tracks:
- Tasks-archive (Plan #6): current `tasks/active.md` lag = 0; nothing to migrate. When `science-tool tasks archive` ships, no action needed.
- Validator MAV update (Plan #7 + MAV): pending upstream merge. Will pull canonical `validate.sh` via `science-tool project artifacts update validate.sh` once available.
- Code -> task back-link (Plan #9): already adopting Pattern 1 (filename tag) for 3 marimo notebooks under `code/notebooks/`. No action needed.

Surfaced by: 2026-04-25 downstream conventions migration cycle (orchestrator agent).

## [t142] Speed up create_correlation_matrices.py for large studies
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [task:t131]
- group: pipeline
- created: 2026-04-26

**Bottleneck.** `create_correlation_matrices.py` is O(n_genes²) per study and dominates upstream wall time for large cohorts. In the full pan-cancer-dndscv run 2026-04-25, `pancan_pcawg_2020` (~18,500 genes) took 2h 30min for one (cancer_cor.feather, gene_cor.feather) pair; output was 1.33 GB. There are 13 studies in the canonical pan-cancer config; `msk_met_2021` and `genie` are even larger.

**Optimization angles** (in priority order):
1. **`numpy.corrcoef` on the dense matrix** instead of pandas-level pairwise. Order of magnitude.
2. **Pre-filter genes with < K mutations** before correlating — most pairs are noise. Even K=3 should drop 50-80% of genes for most studies.
3. **Sparse representation** for the underlying gene × sample mutation matrix.
4. Per-study parallelism via `-j` already works; per-cell intra-rule multiprocessing could push further.

**Acceptance**: `create_correlation_matrices` for `msk_met_2021` finishes in under 30 minutes on a single core.

**Cross-references**: identified during the t131 full pan-cancer-dndscv run 2026-04-25.

## [t143] Pre-bake dndscv into vendored conda env to remove install_github race
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [task:t131]
- group: pipeline
- created: 2026-04-26

**Issue.** `run_dndscv.R`'s self-bootstrap step (`remotes::install_github("im3sanger/dndscv@<sha>")`) races when called from parallel R processes that share the same conda env's R library. The smoke run 2026-04-25 hit this twice: the first parallel job to attempt install would succeed, but the second would error with `dndscv install_github reported success but namespace still missing` (RcppArmadillo install collision under the same library prefix). The race resolved itself on retry once dndscv was already installed in the env, but it makes the first fresh-env run flaky and bounds `-jN` parallelism for `run_dndscv_per_cancer` until the env warms up.

**Workarounds applied** so far: pre-installing `r-rcpp` and `r-rcpparmadillo` via conda (so they're not compiled from source under the install_github call). This narrows the race window but doesn't eliminate it.

**Real fix** options:
1. **Vendored dndscv tarball** — `code/envs/dndscv.yml` adds `r-dndscv` from a private conda channel built from a pinned dndscv tarball. Eliminates the bootstrap step entirely.
2. **Docker / Apptainer image** with dndscv pre-installed. Snakemake supports `container:` directives.
3. **File-system lock** in `run_dndscv.R`'s bootstrap function — `dir.create()` is atomic on POSIX; first process to create the lock dir does the install, others wait on a `.complete` marker.

**Acceptance**: a fresh `--use-conda` run with `-j8` does not hit the bootstrap race for `run_dndscv_per_cancer`.

**Cross-references**: identified during the t131 smoke run 2026-04-25 (commit `1dd1414` added the rcpparmadillo workaround).

## [t146] External validation of pan-cancer dNdScv ranking against IntOGen / Martincorena 2017
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [task:t131, interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run]
- group: validation
- created: 2026-04-26

The 2026-04-26 t131 interpretation flagged **mild circularity** in using Bailey 2018 driver recovery as the primary validation metric — Bailey 2018 used dNdScv as one of seven driver-detection inputs, so high Bailey recovery is partly self-validation. Need an external reference that does NOT include dNdScv as an input.

**Targets**:
- Martincorena 2017 supplementary tables (the original pan-cancer dNdScv ranking).
- IntOGen pan-cancer driver list (uses MutSig + OncodriveCLUSTL + OncodriveFML + dNdScv; pull only the non-dNdScv subset).
- COSMIC Cancer Gene Census tier 1 (curated by literature, not by dNdScv).

**Output**: rank-rank Spearman correlation table; spot-check the top-50 disagreements between our pan-cancer dNdScv and IntOGen's; document any systematic differences (e.g., do we over-rank long genes that IntOGen flags as artifacts?).

## [t147] Stratify dNdScv per-cancer runs by hypermutator-filtered cohorts
- priority: P2
- status: proposed
- aspects: [computational-analysis, software-development]
- related: [task:t131, task:t081, task:t141, interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run]
- group: pipeline
- created: 2026-04-26

The t131 interpretation noted that even after the t144 tiebreaker fix, TTN persists at v2 rank #5 and AHNAK / AHNAK2 / ABCA13 survive in the q=0 set despite dNdScv's trinucleotide-context correction. The leading explanation is that hypermutated samples (POLE / POLD1 / MSI-H) inflate per-gene mutation counts uniformly across the genome, with the largest absolute inflation at the longest genes — defeating the per-cancer trinucleotide-context background.

**Approach**: re-run `run_dndscv_per_cancer` on cohorts with `is_hypermutator == False` (the existing t081 annotation) and compare the per-cancer q=0 set sizes and top-50 rankings. If hypermutator removal eliminates TTN / AHNAK / AHNAK2 from the top, the inflation is hypermutator-driven; if not, it's something else.

**Cost**: blocked on t141 (R meta-analysis parallelization) being shipped, otherwise the re-runs take 12+ hours each. Could also do this for a single cancer (Endometrial Cancer = UCEC, the most POLE-rich) as a cheap pilot.

**Output**: per-cancer-type comparison feather; recommendation for whether to gate `run_dndscv_per_cancer` on hypermutator-filtered cohorts by default.

## [t148] Replace single-cancer best_cancer_type with multi-cancer set field in per-gene rollup
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [task:t131, task:t144, interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run]
- group: pipeline
- created: 2026-04-26

The current `best_cancer_type` column in `dndscv_pooled.feather` and `three_way_ranking_comparison.feather` reports a single cancer type as "best", chosen by `idxmin(min_q)`. At full pan-cancer scale this is dominated by alphabetical-tie artifacts (Ampullary Cancer appears as "best" for TP53, KRAS, PIK3CA, ARID1A, ARID2 — purely because of alphabetical tiebreaking among many cancers all hitting q=0). t144 will partially fix this for the top hits, but the underlying single-cancer field is information-lossy when many cancers tie.

**Replace** `best_cancer_type` with one or more of:
- `cancers_with_significant_q05` (sorted list / count) — already partially captured as `n_cancers_significant_q05`; expose the cancer names too.
- `most_significant_cancer_by_n_samples` (cohort-power-weighted; tie-broken by larger cohort).

**Acceptance**: per-gene rollup carries enough information to identify *which* cancer types contribute to a gene's q-significance, not just one alphabetically-arbitrary "best".
