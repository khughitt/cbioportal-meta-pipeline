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

## [t082] Pipeline addition: HGNC gene-symbol alias mapping in convert_to_feather.py
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [meta:0001-bias-audit-cross-study-aggregation-pipeline-preprocessing-clustering]
- group: pipeline
- created: 2026-04-13



## [t084] Pipeline addition: study-prefix patient_id in combined sample table to prevent cross-study collisions
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [meta:0001-bias-audit-cross-study-aggregation-pipeline-preprocessing-clustering]
- group: pipeline
- created: 2026-04-13



## [t085] Pipeline addition: silhouette/gap-statistic k-selection + stability check for gene/cancer clustering
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [meta:0001-bias-audit-cross-study-aggregation-pipeline-preprocessing-clustering]
- group: pipeline
- created: 2026-04-13



## [t086] Pipeline addition: length_is_fallback indicator column + per-run excluded_studies.tsv audit trail
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [meta:0001-bias-audit-cross-study-aggregation-pipeline-preprocessing-clustering]
- group: pipeline
- created: 2026-04-13



## [t087] Graded ch_contamination_prob column replacing uniform ch_priority_gene boolean
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [search:0004-asxl1-tet2-ch-disambiguation, topic:clonal-hematopoiesis-contamination, paper:Coombs2018, task:t059]
- group: pipeline
- created: 2026-04-14

Replace the uniform ch_priority_gene boolean emitted by annotate_ch.py with a graded ch_contamination_prob column sourced from Coombs 2018 Table 2 (per-gene variant-level CH confirmation rate in paired-tumor/blood cohort). Anchor values: DNMT3A ~64%, TP53 ~4%, overall across the 9-gene CH panel ~8%. ASXL1 and TET2 intermediate — read Coombs 2018 Table 2 for the precise numbers. Keep the boolean as a backward-compatible column (computed by thresholding the graded prob at 0.5) until downstream consumers migrate. Closes the open question surfaced in t059: uniform CH flagging over-masks bona fide solid-tumor ASXL1 biology (MSI-CRC polyG-indel, CRPC, HNSCC per Katoh 2013).

## [t088] Age-adjusted TMB alongside raw TMB (covariate support for t081)
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [search:0006-tmb-hypermutator-followup, topic:tumor-mutational-burden, paper:Chalmers2017, task:t081, task:t025]
- group: pipeline
- created: 2026-04-14

Chalmers 2017 documents a 2.4x TMB increase between age 10 and age 90 in 100000-case FoundationOne cohort. Once per-sample TMB is computed in t081, emit a parallel age_adjusted_tmb column that regresses TMB on patient age (when available from cBioPortal clinical tables) and reports the residual. Two columns: raw tmb_mut_per_Mb and age_adjusted_tmb_residual. No surveyed TMB tool (Vega 2021 FoCR, jasonwong-lab/TMB, pyTMB) does this adjustment — cheap pipeline contribution.

## [t090] Pathway-layer benchmark on cross-study cBioPortal data (t043 gap)
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [search:0005-pathway-level-pan-cancer-methods, paper:Reyna2020Pathway, paper:Iorio2018SLAPenrich, paper:Paczkowska2020, task:t043, task:t077, task:t079]
- group: meta-analysis
- created: 2026-04-14

Surfaced as a real gap in t043: no pan-cancer benchmark at the pathway rollup level currently exists (Wu 2022 Brief Bioinform benchmark is gene-level only). Run SLAPenrich vs ActivePathways vs HotNet2 on the pipeline's gene_cancer_study output using a shared pathway database (start with Reactome + Sanchez-Vega-10; KEGG and MSigDB Hallmarks as comparators) across multiple cBioPortal cohorts and report method concordance. Natural methodological contribution. Pre-register pathway database + primary method choice before running (ties to t079 pooling pre-registration).

## [t091] Companion search: TET2 in solid tumors (melanoma, glioma, breast) — disambiguate CH vs biology
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- related: [search:0004-asxl1-tet2-ch-disambiguation, topic:clonal-hematopoiesis-contamination, task:t059]
- group: searches
- created: 2026-04-14

Gap surfaced in t059: TET2 solid-tumor biology literature is thinner than ASXL1. ASXL1 has clear MSI-CRC polyG-indel + CRPC / HNSCC / breast evidence (Katoh 2013). TET2 solid-tumor papers cluster around melanoma (catalytic-domain mutations), glioma (IDH-pathway interaction — TET2 is the IDH-pathway target, so IDH-mutant gliomas carry functional TET2 loss without TET2 mutation), and breast. Focused OpenAlex + PubMed search. Produces doc/searches/YYYY-MM-DD-tet2-solid-tumor-biology.md.

## [t104] Optimize create_correlation_matrices.py: gene x gene corr scales O(n_genes^2) and stalls on whole-exome studies
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t100]
- group: pipeline
- created: 2026-04-17

Surfaced by t100 PoC run 2026-04-17: create_correlation_matrices for brca_tcga_pan_can_atlas_2018 (~1090 samples x ~20k genes) took ~55 min; same expected for ucec_tcga and skcm_tcga. Panel studies (MSK-IMPACT ~341 genes) are fast. Script computes patient_mut.T.corr() which is O(n_genes^2) in both time and memory. Options: (a) use numpy.corrcoef on float32 matrix (typically 5-10x faster than pandas corr), (b) restrict to the top-K variance genes before correlation (add config key max_genes_for_corr default 5000), (c) sparse-aware correlation via sklearn.metrics.pairwise when count matrix is sparse (>95% zeros typical for mutation count matrices). Recommend starting with (a)+(b) and only falling back to (c) if still too slow. Ref: code/scripts/create_correlation_matrices.py:27 (patient_mut.T.corr()).

## [t107] Backport clustering.* defaults to main configs (config-10k-genes.yml, config-full.yml, config-pan-cancer.yml) OR make cluster rules opt-out when missing
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t100]
- group: pipeline
- created: 2026-04-17

Surfaced by t100 PoC 2026-04-17: cluster_genes.py and cluster_cancer_types.py require config['clustering']['gene']['k'], ['gene_min_mutations'], ['cancer_min_mutations'], ['random_seed'] (and mirror keys under ['cancer']). No shipped config prior to config-poc.yml contained these keys. This means every run of the main pipeline prior to this PoC would have crashed at the cluster rules if rule all was fully evaluated — the pre-t081 runs presumably did not have cluster rules in their rule all target list. Fix: either (a) backport the default clustering sub-tree from config-poc.yml to the 3 main configs, or (b) make the cluster scripts fall back to sensible defaults when the key is absent (with a warning). Option (a) is more explicit; option (b) is more forgiving.

PARTIAL (backlog review 2026-06-01): `config-full.yml` now carries the `clustering:` block (gene/cancer k, min_mutations, random_seed); `config-10k-genes.yml` and `config-pan-cancer.yml` still lack it, and `cluster_genes.py`/`cluster_cancer_types.py` still hard-require the key (KeyError if absent). Remaining work: backport the block to the two missing configs, or add the script-level fallback.

## [t108] Investigate is_hypermutator_relative reporting ~45% for BRCA (Samstein top-20% should cap at ~20%)
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t097, task:t100, paper:Samstein2019, interpretation:0001-poc-run]
- group: pipeline
- created: 2026-04-17

Surfaced by t100 PoC 2026-04-17: is_hypermutator_relative reports 45.5% for brca_tcga_pan_can_atlas_2018 and 36.4% for skcm_tcga_pan_can_atlas_2018 (from doc/interpretations/2026-04-17-poc-run.md Finding 4). The Samstein 2019 definition is 'top-20%% TMB within the sample's histology' — which should yield at most ~20%% hypermutators per cancer type (slightly more with ties at the boundary). 45%% / 36%% far exceed this. Likely causes: (a) tied-sample promotion at the 80th-percentile cut without explicit tiebreak policy, (b) the per-histology grouping key is cancer_type but the TCGA 'cancer_type' labels collapse many distinct histologies into one bucket (e.g. 'Breast Cancer'), so a large fraction of samples tie at a low TMB boundary, or (c) an off-by-one in the quantile cut logic. Inspect _relative_top_quintile_flag in code/scripts/annotate_hypermutators.py (line 200 area).

## [t112] Integrate Lee-Six 2018 blood (or Xu 2025 dbGaP) as second normal-tissue source for t111 outputs
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [task:t111, topic:signature-decomposition-unmatched-normal, question:0006-ch-priority-gene-completeness, question:0008-signature-decomposition-tissue-background-subtraction, paper:LeeSix2018, paper:Xu2025]
- group: pipeline
- created: 2026-04-18

Follow-up to t111 (which was reduced to Li2021-only by the 2026-04-19 data-access gate because Xu2025 per-variant data is dbGaP-controlled). Add a second open-access normal-tissue source to enrich data/normal_tissue_spectra.tsv and data/normal_tissue_burden.tsv. Preferred source: Lee-Six 2018 (Nature, DOI 10.1038/s41586-018-0497-0) — single-donor ~140 HSC WGS colonies — complements Li2021's solid-tissue bias with blood where CH matters for q006/q008. Second-choice source: Xu2025 via dbGaP DAR (weeks of calendar time; only worth pursuing if a user has existing GTEx access). This task refactors code/scripts/extract_normal_tissue_spectra.py into the plugin-style adapters/ pattern planned in t111's scope brainstorming (option C: 'start hard-coded to 2 sources, plugin-ize when 3rd arrives').

## [t113] Close t111 assembly range-check TODO — verify chrom/pos against declared assembly
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [task:t111, interpretation:0003-t111-normal-tissue-spectra-pipeline]
- group: pipeline
- created: 2026-04-19

Current validate_input_contract accepts the assembly parameter but does not range-check chrom/pos against per-chromosome lengths (marked TODO(t111-followup) at code/scripts/extract_normal_tissue_spectra.py:96-100). A caller who declares wrong assembly gets silent acceptance. Fix: encode GRCh37/GRCh38 max-chromosome-lengths as module constants and validate df['pos'].max() <= length_dict[chrom] for each chromosome. Becomes load-bearing when t112 introduces GRCh38 sources. ~30 min + one test.

## [t114] Pre-register q007 null-model correction impact before rolling into frequency pipeline
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [task:t111, question:0007-cross-tissue-somatic-mutation-rate-variation-as-null-model, paper:Li2021]
- group: pipeline
- created: 2026-04-19

Before applying the t111 per-tissue snvs_per_mb correction to gene_cancer_study_ratio_annotated.feather frequencies, pre-register: (1) expected number of gene-cancer rankings that shift and by how many positions; (2) head-to-head comparison against a Martincorena 2017 dN/dS-based null as a simpler baseline. If the two approaches rank genes identically, t111's value-add collapses. Prevents ships-before-thinks bias on whether the empirical null is actually discriminating versus a uniform-rate-per-gene-length null. Deliverable: doc/meta/pre-registration-q007-null-model-correction.md.

## [t127] First q008 quantitative pass: unmatched-normal contamination magnitude using t111 normal_tissue_spectra
- priority: P3
- status: blocked
- aspects: [computational-analysis]
- related: [question:0008-signature-decomposition-tissue-background-subtraction, task:t111, meta:0007-next-steps-and-gap-analysis-2026-04-24]
- blocked-by: [task:t166]
- group: meta-analysis
- created: 2026-04-24

Produce a first numeric estimate of normal-tissue SBS1/SBS5 contamination
magnitude in unmatched-normal cBioPortal-style cohorts, using the Li2021
reference spectra landed by t111 + the existing t109/t110 SigProfiler
assignment surface. Closes the "built-but-unexploited" gap from
meta:0007-next-steps-and-gap-analysis-2026-04-24 gap 2 for question:0008.

Status: deferred 2026-04-28 — workable but materially weaker than originally
scoped. Plan + cohort survey landed; revival is cheap when a better
unmatched-WES cohort becomes available (Hartwig HMF when t166 unblocks is
the obvious candidate).

What landed
-----------
- doc/plans/2026-04-28-t127-q008-quantitative-pass-plan.md (revised plan,
  reuses run_restricted_sigprofiler_assignment.py; threshold pre-registration;
  no-go rules; 9-finding code-review pass).
- code/config/config-t127.yml (study list + signature config).
- tcga_mc3 ingested (commit 16d1a12): 9,104 samples / 32 TCGA project codes
  / GRCh37 in results/q008-quantitative-pass-2026-04-28/studies/tcga_mc3/.
- Cohort survey across 196 pipeline studies for matched/unmatched status.

Why deferred
------------
Original plan paired tcga_mc3 (matched WES) with msk_impact_2017 (assumed
unmatched panel). Survey discovered msk_impact_2017's public release is 98%
matched (MATCHED_STATUS column: 10,702 matched / 242 unmatched / 1 NaN).
Largest unmatched cancer-type stratum is NSCLC at n=24 — below the n=50
floor required for the planned per-cancer-type FDR table.

Best alternative cohort found in survey:
- sarcoma_msk_2022 (n=7,494, 100% unmatched, MSK-IMPACT panel) — pairs with
  MC3 SARC (n=236) for a single-cancer-type matched-vs-unmatched contrast.
  But: Li2021 covers 9 GI/respiratory tissues only — no soft-tissue / bone /
  sarcoma reference, so the subtraction arm of the original plan cannot run
  on this contrast.

GENIE (229,453 samples) does not publish MATCHED_STATUS; per-assay matching
policy curation would be required, out of scope for a pilot.

Revised pilot design (recorded for revival)
-------------------------------------------
Tripartite descriptive design that fits the available cohorts:

1. Primary Δ — sarcoma matched-vs-unmatched. MC3 SARC (n=236 matched WES)
   vs sarcoma_msk_2022 Soft Tissue Sarcoma (n=5,264 unmatched panel) on
   per-sample SBS1+SBS5 fraction. Single cancer type ⇒ no FDR table; verdict
   is descriptive. Confounders: WES vs panel callable territory, TCGA vs
   MSK caller pipeline.

2. Secondary Δ — within-MSK-IMPACT. matched (n=10,702) vs unmatched (n=242)
   pooled across cancer types. Strongest causal-attribution design (same
   assay/caller/cohort) but small unmatched n limits Δ precision.

3. Subtraction-model calibration on matched data. Apply Li2021 c-sweep to
   MC3 GI cancer types (LIHC, COAD/READ, ESCA, STAD, PAAD; n=940 total).
   Answers: how much SBS1+SBS5 mass does the subtraction remove from a
   known-matched cohort? Large removal ⇒ over-aggressive; small removal ⇒
   conservative.

Material weaknesses vs original plan: no per-cancer-type FDR table, no
Δ(c) gap-closing test, primary contrast confounds normal-status with
WES-vs-panel and caller pipeline.

What would unblock the strong design
------------------------------------
A multi-cancer-type unmatched-normal WGS or WES cohort, ideally with a
within-cohort matched comparator. Hartwig HMF (task t166, currently gated
on a 3-6 month DUA) is the leading candidate: WGS, mixed matched/unmatched,
35+ cancer types. When t166 lands, the t127 plan structure runs on that
cohort with minimal modification — the subtraction arm becomes feasible
(WGS removes the t126 panel-sparsity blocker on q009 too), and the
per-cancer-type FDR table comes back.

Cheaper revival paths if a better cohort surfaces unexpectedly:
- Curate a tumor-only subset of GENIE by joining seq_assay_id against the
  AACR Project GENIE matching-policy table (per-contributor metadata).
- Search for newer per-tissue Li2021-equivalent normal references (Moore
  2022 pan-tissue WGS; Xu2025 GTEx coding spectra at t111 follow-up).

To revive: re-read this description, the plan, and config-t127.yml; pick
up at Task 1 of the plan with the new cohort substituted into the
feasibility table.

## [t128] Emit retroactive datapackage.json manifests for results/poc-2026-04-17/ and results/signature-brca-2026-04-22/
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t100, meta:0007-next-steps-and-gap-analysis-2026-04-24]
- group: pipeline
- created: 2026-04-24

Two workflow output directories currently sit on disk with no datapackage.json manifests: results/poc-2026-04-17/ (t100 PoC annotated artifact) and results/signature-brca-2026-04-22/ (t109/t110 signature-restriction outputs). Write Frictionless Data Package manifests retroactively so provenance is filesystem-readable rather than narrative-only. Recurring gap flagged on both 2026-04-22 and 2026-04-24.

## [t129] Length × PubMed-mention regression pipeline step (q011)
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [question:0011-gene-length-as-literature-attention-confounder, topic:mutation-rate-normalization, discussion:0001-gene-length-bias-in-mutation-rankings-and-literature, task:t082]
- group: meta-analysis
- created: 2026-04-24

Implement the regression spec'd in q011: log(mention_count+1) ~ log(protein_length) + log(mutation_count+1) over protein-coding genes (PubTator 2026-01-16 + UniProt + cBioPortal aggregate counts). Report marginal vs partial length slope with bootstrap CIs. Subgroup by Bailey 2018 driver list. Sensitivity: dNdScv-corrected counts, disease-co-mention covariate, non-cancer placebo slice. Output: doc/interpretations/<date>-q011-length-attention-regression.md plus a length-residualized 'attention prior' feather under models/. Requires HGNC alias mapping (t082) for the PubTator↔UniProt join.

## [t130] Paper summary: Stoeger & Nunes Amaral 2018 (gene-attention accessibility features)
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [question:0011-gene-length-as-literature-attention-confounder, topic:mutation-rate-normalization, discussion:0001-gene-length-bias-in-mutation-rankings-and-literature]
- group: searches
- created: 2026-04-24

Use science:research-papers to summarize Stoeger T, Gerlach M, Morimoto RI, Nunes Amaral LA. 2018. 'Large-scale investigation of the reasons why potentially important genes are ignored.' PLOS Biology 16(9):e2006643. doi:10.1371/journal.pbio.2006643. Methodological reference for the literature-attention bias side of q011 — they show chemical/experimental accessibility features predict per-gene publication count better than biological importance. Need: their list of accessibility features, their model form, effect-size estimates, and how (or whether) they treat gene/transcript length specifically.

## [t131] Opt dNdScv into rule all via config-pan-cancer-dndscv.yml + three-way ranking comparison
- priority: P2
- status: proposed
- aspects: [computational-analysis, software-development]
- related: [topic:mutation-rate-normalization, discussion:0001-gene-length-bias-in-mutation-rankings-and-literature, question:0011-gene-length-as-literature-attention-confounder, paper:Martincorena2017]
- group: pipeline
- created: 2026-04-24

Add a side config code/config/config-pan-cancer-dndscv.yml that includes the per-study dNdScv outputs (studies/{id}/mut/dndscv/genes.feather) in rule all. Then write a comparison report: raw vs length-adjusted vs dNdScv-selection rankings, Spearman + Jaccard@10/50/100/500, and per-list correlation with PubTator gene-mention counts. Closes the 'length-only is below the 2013 methodology bar' finding from the bias audit and topic:mutation-rate-normalization. CONSTRAINT (per memory:r-reproducibility): the dNdScv rule must use a conda/mamba env YAML or Docker image — never assume system R.

## [t132] Literature search: mutation-ordering methods for cross-sectional data (MHN / CBN / CAPRI / REVOLVER / PCAWG chronology)
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [question:0012-mutation-ordering-cross-sectional-inference, discussion:0002-mutation-ordering-and-path-dependency, task:t078]
- group: searches
- created: 2026-04-24

Method × assumption table comparing Mutual Hazard Networks (Schill 2020), Conjunctive Bayesian Networks (Beerenwinkel 2007), CAPRI/TRONCO (Caravagna 2016), REVOLVER (Caravagna 2018), HINTRA, PMCE, and PCAWG pan-cancer chronology (Gerstung 2020 Nature 578:122). Deliverable: doc/searches/YYYY-MM-DD-mutation-ordering-methods.md. Goal: decide whether detecting A→B asymmetries in cBioPortal data is a method-selection problem (pick MHN) or a novel-methods problem.

## [t133] Audit VAF availability across cBioPortal/GENIE studies
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [question:0012-mutation-ordering-cross-sectional-inference, discussion:0002-mutation-ordering-and-path-dependency]
- group: audits
- created: 2026-04-24

Hard gate on any clonality-based ordering work. For each study in code/config/config-full.yml, inspect pre-convert_to_feather MAF headers and tally which carry (a) tumor_f / VAF directly, (b) t_alt_count + t_ref_count (can compute VAF), (c) neither. Also record sequencing type (WES vs panel) and matched-normal status. Output: doc/audits/YYYY-MM-DD-vaf-availability-audit.md. Decision rule: if ≥50% of samples retain VAF, unlock pipeline change to preserve VAF; if not, restrict ordering work to CBN/MHN-style population-level inference only.

## [t134] Pipeline addition: retain VAF (t_alt_count, t_ref_count, tumor_f) in per-study variant feathers
- priority: P3
- status: proposed
- aspects: [software-development]
- related: [question:0012-mutation-ordering-cross-sectional-inference]
- blocked-by: [Audit VAF availability across cBioPortal/GENIE studies]
- group: pipeline
- created: 2026-04-24

Extend convert_to_feather.py to retain per-variant allele-count columns alongside gene/sample presence calls. Unblocks clonality-based ordering (MHN validation companion), CCF estimation, per-sample signature deconvolution at variant level, and general driver-evolution work. Contingent on VAF-availability audit confirming retention is worthwhile.

## [t135] MHN fit per histology as directed companion to t078 co-occurrence results
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- related: [question:0012-mutation-ordering-cross-sectional-inference, hypothesis:0004-mhn-pathway-ordering, paper:Schill2024, paper:Vocht2026, task:t078, task:t081, task:t111, task:t152]
- group: meta-analysis
- created: 2026-04-24

t078 co-occurrence/mutual-exclusivity landed 2026-04-25 (no longer blocking). Add observation-event Mutual Hazard Network fit (Schill 2024 / Vocht 2026), using the same sample-specific-background-rate null and per-sample callability mask. Report primary results at Sanchez-Vega 10-pathway level; gene-level as drill-down. Stratify per histology and per hypermutator class (t081). Calibrate against PCAWG Gerstung 2020 pan-cancer chronology Table 1 before reporting any novel edges. Do not report classical cMHN-only edges as biological ordering evidence; cMHN is a baseline for bias comparison only.

Implementation plan: `doc/plans/2026-05-02-t135-t152-ordering-validation-plan.md`.

## [t136] Canonicalize all variant coordinates to GRCh38 at ingestion (liftover from hg19)
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t131, topic:mutation-rate-normalization, discussion:0001-gene-length-bias-in-mutation-rankings-and-literature]
- group: pipeline
- created: 2026-04-24

Add a liftover step in convert_to_feather.py that maps hg19-native study variants to GRCh38 using CrossMap or pyliftover with UCSC hg19ToHg38.over.chain.gz. Retain original chr/pos/build columns for audit. Single canonical build downstream unlocks dNdScv refdb selection, future GRCh38-only annotation sources (gnomAD v4, ClinVar, dbNSFP v4.x, AlphaMissense, latest COSMIC), and removes a class of silent-degradation bugs across the pipeline. Exonic SNV loss expected <0.1% (per UCSC chain coverage). This is the long-term destination flagged during t131 design — t131 itself uses cheaper per-study refdb routing as an interim. Out of scope for this task: re-running upstream tooling against the lifted coordinates (signature callers, replication-timing joins). Plan separately for those once the liftover artifact is in place.

## [t137] t078 SELECT pipeline integration wiring (production prerequisites)
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t078, task:t081]
- blocked-by: [task:t081]
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
- related: [task:t081, paper:Bavisetty2025, paper:Lu2023, paper:Rashid2025, paper:Jung2025, synthesis:0002-canalization-in-gene-regulatory-networks-cross-paper-synthesis-for-the, topic:tumor-mutational-burden]
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
- status: blocked
- aspects: [computational-analysis]
- related: [task:t131, task:t171, interpretation:0012-t146-external-validation-cgc, interpretation:0009-t131-full-pan-cancer-dndscv-run]
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
- related: [task:t131, task:t081, task:t141, interpretation:0009-t131-full-pan-cancer-dndscv-run]
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
- related: [task:t131, task:t144, interpretation:0009-t131-full-pan-cancer-dndscv-run]
- group: pipeline
- created: 2026-04-26

The current `best_cancer_type` column in `dndscv_pooled.feather` and `three_way_ranking_comparison.feather` reports a single cancer type as "best", chosen by `idxmin(min_q)`. At full pan-cancer scale this is dominated by alphabetical-tie artifacts (Ampullary Cancer appears as "best" for TP53, KRAS, PIK3CA, ARID1A, ARID2 — purely because of alphabetical tiebreaking among many cancers all hitting q=0). t144 will partially fix this for the top hits, but the underlying single-cancer field is information-lossy when many cancers tie.

**Replace** `best_cancer_type` with one or more of:
- `cancers_with_significant_q05` (sorted list / count) — already partially captured as `n_cancers_significant_q05`; expose the cancer names too.
- `most_significant_cancer_by_n_samples` (cohort-power-weighted; tie-broken by larger cohort).

**Acceptance**: per-gene rollup carries enough information to identify *which* cancer types contribute to a gene's q-significance, not just one alphabetically-arbitrary "best".

## [t150] Normal-tissue WGS cohort feasibility audit for cross-tissue background atlas
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [hypothesis:0005-healthy-somatic-background-atlas, topic:normal-tissue-mutation-atlas, question:0007-cross-tissue-somatic-mutation-rate-variation-as-null-model]
- group: audits
- created: 2026-04-28

Enumerate published apparently-healthy normal-tissue WGS / deep-sequencing cohorts relevant to `h05`: tissue, n_samples, donor age range, sequencing depth, variant-calling regime, public availability, raw VCF availability, and mapping to cBioPortal cancer-type contexts. Decide whether a uniform-subset meta-analysis or random-effects meta-analysis is feasible.

Acceptance: `doc/audits/<date>-normal-tissue-wgs-cohort-feasibility.md` with a table of cohorts and a promotion recommendation for `h05` (active / keep candidate / retire).

## [t151] Normal-tissue background meta-analysis pilot on one tractable tissue
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [task:t150, hypothesis:0005-healthy-somatic-background-atlas, hypothesis:0001-non-tumor-signal-contamination, question:0007-cross-tissue-somatic-mutation-rate-variation-as-null-model]
- group: meta-analysis
- created: 2026-04-28

After `t150`, run a scoped pilot on the most tractable tissue (likely esophagus or colon). Estimate an age-stratified normal-tissue mutation background and substitute it into the relevant `h01` contamination test (e.g. q001 NOTCH1 in esophagus). Report whether the cross-tissue normal null improves matched-vs-unmatched correction over the current within-pipeline null.

Acceptance: one tissue-specific interpretation document with effect size, uncertainty, and a recommendation on whether to scale the atlas work.

## [t152] Replicate Vocht 2026 LUAD MHN demo and run simulation calibration
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [hypothesis:0004-mhn-pathway-ordering, question:0012-mutation-ordering-cross-sectional-inference, task:t135, paper:Vocht2026, paper:Schill2024]
- group: validation
- created: 2026-04-28

Install `mhn` via `uv add mhn`, reproduce the Vocht 2026 GENIE LUAD demonstration as closely as possible on the project's GENIE release, and benchmark runtime / active-event limits. Then generate synthetic tumors from a known MHN, subsample to project-like panel and cohort-size distributions, and test whether the observation-event MHN recovers >=70% of injected pathway-level edges.

Acceptance: `doc/interpretations/<date>-mhn-luad-demo-and-simulation-calibration.md`; explicit decision on whether `h04` can be promoted or remains candidate.

Implementation plan: `doc/plans/2026-05-02-t135-t152-ordering-validation-plan.md`.

## [t153] CFS overlap annotation and RT-vs-CFS residual regression
- priority: P2
- status: proposed
- aspects: [computational-analysis, software-development]
- related: [question:0014-cfs-as-distinct-confounder-class, question:0003-replication-timing-as-gene-level-mutation-rate-confounder, hypothesis:0001-non-tumor-signal-contamination, hypothesis:0002-cross-study-ranking-divergence-is-structured, task:t121]
- group: meta-analysis
- created: 2026-04-28

Build a per-gene common-fragile-site overlap annotation from published CFS catalogues and join it to the existing gene-level replication-timing map. Regress per-gene mutation-rate residuals on both RT-late status and CFS overlap. If CFS carries a non-zero coefficient after RT adjustment, treat CFS as a distinct correction channel.

Acceptance: CFS annotation artifact under `data/` or `models/`, plus `doc/interpretations/<date>-q014-cfs-vs-rt.md` with coefficient estimates and a correction recommendation.

## [t155] Compare pan-cancer dNdScv aggregation rules under q-value floor pile-up
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- related: [question:0015-pan-cancer-aggregator-choice, hypothesis:0002-cross-study-ranking-divergence-is-structured, task:t144, task:t146, task:t148]
- group: meta-analysis
- created: 2026-04-28

Evaluate candidate per-gene pan-cancer dNdScv aggregators on the existing per-cancer dNdScv outputs: current lexicographic `(min_q, n_cancers_significant_q05)`, Stouffer/Fisher-style combined evidence, rank pooling, and cancer-count weighted variants. Compare Bailey recovery, IntOGen / Martincorena agreement, and leave-one-cancer-out stability.

Acceptance: `doc/interpretations/<date>-q015-dndscv-aggregator-choice.md` and a pre-registered default aggregator recommendation for production outputs.

## [t156] cBioPortal pre-malignant cohort audit
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [hypothesis:0006-pre-malignant-n-minus-1-driver-carriage, topic:pre-cancer-prevalence-and-impact, question:0012-mutation-ordering-cross-sectional-inference]
- group: audits
- created: 2026-04-28

Enumerate cBioPortal studies that include pre-malignant samples or matched precursor/invasive cohorts. Record disease pair, sub-stage labels, n_pre_malignant, n_invasive, assay regime, matched-normal status, available variant modalities, and whether the current mutation-only pipeline can observe the relevant drivers.

Acceptance: `doc/audits/<date>-cbioportal-pre-malignant-cohort-audit.md` with a promotion recommendation for `h06`.

## [t157] First pre-malignant-to-invasive paired driver-overlap analysis
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- related: [task:t156, hypothesis:0006-pre-malignant-n-minus-1-driver-carriage, topic:pre-cancer-prevalence-and-impact]
- group: meta-analysis
- created: 2026-04-28

After `t156`, choose the most tractable paired set (likely Barrett's -> EAC or MDS -> AML) and compute mutation-observable top-25 driver overlap, late-stage residual drivers, and checkpoint/chromatin enrichment. Exclude CNAs, fusions, and translocations unless those modalities are explicitly added.

Acceptance: `doc/interpretations/<date>-pre-malignant-invasive-driver-overlap.md` with local falsification/support for `h06` and a recommendation on whether to scale across pairs.

## [t158] Cross-study saturation curve for top-N ranking stability
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- related: [question:0017-cross-study-saturation-curve, question:0013-cross-study-replication-rate, hypothesis:0002-cross-study-ranking-divergence-is-structured, task:t072, task:t149]
- group: validation
- created: 2026-04-28

Run k-study subsampling ablations for evaluable cancer types and pan-cancer rankings. For k in a pre-registered grid (e.g. 1, 2, 3, 5, 10, 20, all), repeatedly sample k studies, recompute top-N rankings, and estimate variance / Jaccard / Spearman to the full-study reference. Identify the saturation point or mark cancers as unsaturated.

Acceptance: `doc/interpretations/<date>-q017-cross-study-saturation-curve.md` with per-cancer saturation status and recommendations for reporting thresholds.

## [t159] Reconnect t131 interpretation to h02 spine via related: field
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [interpretation:0009-t131-full-pan-cancer-dndscv-run, hypothesis:0002-cross-study-ranking-divergence-is-structured]
- group: spine-hygiene
- created: 2026-04-28

Big-picture validator flagged t131 as orphan because its frontmatter cites question:0011 in source_refs but not in related:. Add hypothesis:0002-cross-study-ranking-divergence-is-structured to the related: list so the resolver picks it up. Pure metadata fix, no analysis change. Acceptance: validator no longer reports t131 as orphan.

## [t161] Absorb orphan questions q014/q016/q017 into hypothesis spine
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [hypothesis:0002-cross-study-ranking-divergence-is-structured, hypothesis:0003-gene-length-confounds-literature-attention, question:0014-cfs-as-distinct-confounder-class, question:0016-panel-induced-ascertainment, question:0017-cross-study-saturation-curve]
- group: spine-hygiene
- created: 2026-04-28

Resolver currently treats q014/q016/q017 as orphan questions even though they substantively belong on the spine. Amend specs/hypotheses/h02-*.md related: to add q014 (CFS gene-level confounder refinement) and q017 (saturation curve). Amend specs/hypotheses/h03-*.md related: to add q016 (panel-induced ascertainment). Pure metadata change. Acceptance: resolve-questions output drops these three from the orphan set; emergent-threads regenerates with smaller orphan_question_count.

## [t175] Integrate standalone analysis scripts into Snakemake when promoted to recurring outputs
- priority: P2
- status: proposed
- aspects: [software-development]
- related: [task:t154, task:t163, question:0016-panel-induced-ascertainment, question:0003-replication-timing-as-gene-level-mutation-rate-confounder]
- group: pipeline
- created: 2026-04-29

The t154 panel-vs-WES ascertainment and t163 RT residual analyses currently run as standalone
tested scripts that write outputs under `/data/packages/cbioportal/pan-cancer/summary/`. That is
appropriate for first-pass hypothesis testing, but if either analysis becomes a recurring
consumer-facing output it should be wired into `code/workflows/Snakefile` with explicit inputs,
outputs, and config-gated inclusion in `rule all` or a named analysis target.

Acceptance: add Snakemake rules for promoted standalone analyses, document their output locations
in `doc/guides/canonical-outputs.md` or the relevant modality guide, and keep one CLI smoke path for
ad-hoc reruns.

## [t164] Draft candidate hypothesis h07: signature/topography-based contamination QC (absorbs q009)
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [question:0009-sbs1-lrr-bias-as-normal-contamination-flag, hypothesis:0001-non-tumor-signal-contamination, interpretation:0006-t123-rt-brca-sbs1-proxy-pilot, interpretation:0007-t126-sbs1-lrr-bias-per-study]
- group: hypothesis-spine
- created: 2026-04-28

Run /science:add-hypothesis to formalize a candidate sub-hypothesis (proposed id h07) absorbing q009, t123, and t126. Working frame: 'a well-powered WGS-based topographic or signature-based diagnostic can directly flag studies with excess normal-tissue contamination, independently of tumor-purity proxies'. Distinguished from h01 because h01 targets correction whereas h07 targets *detection* — a per-study quality flag with a pre-registered threshold (e.g. SBS1 LRR-bias delta, or SBS1 fraction excess vs the matched-cohort pool). Promotion gate: any one WGS cohort added (Hartwig HMF or PCAWG follow-on). Acceptance: specs/hypotheses/h07-*.md with phase: candidate, status: proposed, source_refs to Tomkova 2018 / Sherman 2024, and the three promotion criteria stated.

## [t166] Acquire and integrate Hartwig HMF metastatic WGS cohort (~6,000 tumors)
- priority: P3
- status: blocked
- aspects: [computational-analysis]
- related: [hypothesis:0001-non-tumor-signal-contamination, hypothesis:0002-cross-study-ranking-divergence-is-structured, hypothesis:0005-healthy-somatic-background-atlas, question:0009-sbs1-lrr-bias-as-normal-contamination-flag, topic:signature-decomposition-unmatched-normal, topic:targeted-panel-sequencing-bias]
- group: dataset-acquisition
- created: 2026-04-28

Hartwig Medical Foundation database is a research-access metastatic WGS cohort, ~6000 tumors with matched normals, deeply called and uniformly processed. Adding it would unblock several lines simultaneously. (1) q009 SBS1 LRR-bias diagnostic was deferred (interpretation:0007-t126-sbs1-lrr-bias-per-study) under a pre-registered termination rule because MSK-IMPACT panel coverage of constitutive late-replicating bins is structurally insufficient (~20.7 kb across the panel; n_sbs1_pooled = 176 vs 500-floor; CI half-width 0.194 vs 0.10 ceiling). Hartwig WGS bypasses this entirely — every constitutive LRR bin is fully sampled. (2) h02 panel-vs-WES ascertainment work (t154) currently relies on TCGA MC3 as the WES comparator, which is matched-normal but primary-tumor; Hartwig adds a matched-normal metastatic comparator for stage-effect deconfounding. (3) h05 cross-tissue background atlas: Hartwig matched normals provide a clean cross-tissue normal sample distribution covering ~25 cancer-relevant tissues. (4) Replication-timing residual regression at full WGS scale (t163) becomes possible without panel-coverage caveats. Access: DUA via hartwigmedicalfoundation.nl/applying-for-data, typically 3-6 months. Pipeline integration scope: ingest as a single pseudo-study (parallel to tcga_mc3 MC3 path, code/scripts/process_mc3.py), add it to the matched_normal_studies config list, validate WES-vs-WGS callable-region denominators in build_panel_callable_sizes. Acceptance: data/hartwig_v6/ populated; convert_to_feather pipeline ingests; per-study mutation feathers exist for ≥20 cancer types; one rerun of the t126 SBS1 LRR-bias test on the Hartwig subset reaching a non-deferred verdict.

## [t167] Acquire and integrate PCAWG / ICGC-25K WGS cohort
- priority: P3
- status: blocked
- aspects: [computational-analysis]
- related: [hypothesis:0001-non-tumor-signal-contamination, hypothesis:0002-cross-study-ranking-divergence-is-structured, hypothesis:0004-mhn-pathway-ordering, question:0009-sbs1-lrr-bias-as-normal-contamination-flag, question:0012-mutation-ordering-cross-sectional-inference, paper:PCAWG2020]
- group: dataset-acquisition
- created: 2026-04-28

PCAWG (~2,800 tumors, 38 cancer types, fully WGS, matched normals, harmonized PanCancer Analysis of Whole Genomes consortium calls) is the canonical WGS-tier comparator for any rank-stability or topographic claim. Three motivations specific to this project. (1) Cross-validation against Gerstung 2020: the PCAWG chronology paper provides per-cancer mutation-order benchmarks against which any h04 MHN result must be sanity-checked; we cannot run that benchmark without PCAWG-tier data in our pipeline. (2) Topographic / signature-bias diagnostics (q009, h07 if filed): same payoff as Hartwig but with broader cancer-type coverage and primary-tumor (vs metastatic) sample distribution. (3) h02 LOSO replication test (t149): adding PCAWG as one held-out cohort tests whether the 62/100 Bailey recovery in dNdScv survives leave-one-cohort-out at the WGS stratum level. Access: dbGaP phs001629 (PCAWG mutations) requires institutional DAR; ICGC DACO governs the broader release. Practical scope: ingest the consensus mutation calls TSV (parallel to the MC3 path) as one pseudo-study or per-project pseudo-studies; the difficult bit is CNA calls (not modeled by the pipeline yet, out-of-scope per AGENTS.md). Acceptance: data/pcawg_v2/ ingested; ≥30 cancer types appear in per-study feathers; one held-out LOSO iteration runs successfully; one Gerstung 2020 chronology comparison appended to t152 calibration if h04 has progressed.

## [t168] Investigate Genomics England 100K WGS access for h02 LOSO and h05 atlas
- priority: P3
- status: blocked
- aspects: [computational-analysis]
- related: [hypothesis:0002-cross-study-ranking-divergence-is-structured, hypothesis:0005-healthy-somatic-background-atlas, question:0013-cross-study-replication-rate, question:0017-cross-study-saturation-curve]
- group: dataset-acquisition
- created: 2026-04-28

Genomics England 100K Genomes Project: ~70,000 cancer WGS samples + matched germline, harmonized through the Cancer Programme pipeline. Largest single WGS cancer cohort in the world. Motivations: (1) h02 saturation curve (q017, t158): testing whether top-N ranking stability saturates at the WGS-scale becomes possible only with cohorts in the 50k+ range; cBioPortal+GENIE+Hartwig+PCAWG combined still does not reach this scale uniformly. (2) h05 healthy somatic background: GEL holds matched-germline WGS, which is the closest existing approximation to a population-level normal somatic-mutation reference at scale. Access barrier: UK-only DAC; non-UK researchers must collaborate with a UK-based institution (Genomics England Research Environment is a secure analysis platform — cannot extract raw data). This task is exploratory: file as 'investigate' rather than 'integrate', because the access friction is high and the pipeline would need to run inside the GE Research Environment rather than ingesting locally. Acceptance: a one-page memo at doc/feasibility/2026-XX-genomics-england-feasibility.md with go/no-go recommendation, contingent partnership candidates, and an estimate of integration cost.

## [t169] Acquire GTEx v10 + Yizhak2019 / Rockweiler2023 healthy-tissue somatic call sets for h05 atlas
- priority: P3
- status: blocked
- aspects: [computational-analysis]
- related: [hypothesis:0005-healthy-somatic-background-atlas, hypothesis:0001-non-tumor-signal-contamination, question:0007-cross-tissue-somatic-mutation-rate-variation-as-null-model, task:t150, task:t151, task:t111, topic:normal-tissue-mutation-atlas]
- group: dataset-acquisition
- created: 2026-04-28

The current h05 cross-tissue normal background relies on Li 2021 spectra alone (resolved via task:t111 for 56 per-tissue spectra). Two complementary public sources expand coverage substantially. (1) Yizhak 2019 (RNA-MuTect): somatic variants called from GTEx RNA-seq across 29 tissues, ~6,700 samples, age-stratified. Trades VAF accuracy for breadth and age-coverage. (2) Rockweiler 2023: somatic mutation rates from GTEx WGS for the subset with whole-genome data, more accurate but much smaller n. Together, GTEx-grounded Yizhak + Rockweiler covers age × tissue × mutation-class space far better than Li 2021 alone, which is essential for the P1 '>2 OoM cross-tissue rate variation' claim and for the per-tissue null model that task:t114 wants to pre-register. Access: GTEx v10 expression and metadata are public (gtexportal.org); somatic call tables are supplementary tables to the respective papers (already public). Pipeline integration scope: parallel to the t111 Li 2021 spectra script — extract per-sample spectra from each call set, harmonize tissue labels against the cBioPortal cancer-type axis, emit normal_tissue_spectra.feather extensions covering Yizhak / Rockweiler tissues. Acceptance: data/yizhak2019_rnamutect/ and data/rockweiler2023_gtex_wgs/ populated; t111 script extension produces a unified normal-tissue spectra feather covering ≥40 tissue × age strata; one pilot of the t151 esophagus or colon background null swap uses the expanded reference and reports an effect-size delta versus Li-only.

### Notes

- 2026-05-31: Blocked 2026-05-31: GTEx v10 controlled-access somatic call sets (and the Yizhak2019/Rockweiler2023 dbGaP tiers) require institutional affiliation with a cancer-research institute, which the user does not currently hold. Public GTEx expression/metadata remain accessible but the somatic-variant tables that h05 needs are gated. Revisit when affiliation is re-established. Until then, prioritize tasks that need no gated data access (e.g. t195 h08 positive-control scan on MC3 + existing exposures).

## [t170] Integrate PubTator Central + iCite + OpenAlex for h03 literature-attention regression
- priority: P1
- status: proposed
- aspects: [computational-analysis]
- related: [hypothesis:0003-gene-length-confounds-literature-attention, question:0011-gene-length-as-literature-attention-confounder, task:t129, task:t130, topic:mutation-rate-normalization]
- group: dataset-acquisition
- created: 2026-04-28

t129 (the partial-slope regression for beta_length) and the broader h03 framing both depend on a robust literature-attention metric. PubMed mention count alone has known issues: it conflates primary research with reviews, treats every paper as equally weighted, and cannot disentangle gene-as-subject from gene-as-mention. Three sources together give a triangulated attention signal. (1) PubTator Central: NCBI's BioConcept-tagged corpus, gene-resolved at the entity level (resolves the gene-as-subject problem; provides per-gene primary-research vs review counts). (2) iCite (NIH OPA): per-paper citation counts and the Relative Citation Ratio, lets us weight mentions by paper-level impact and citation-window stability. (3) OpenAlex: independent corpus with author-affiliation and topic metadata, useful as an orthogonal validation of PubTator counts (does the PubTator-derived beta_length replicate against an independently-built corpus?). All three are free public APIs / bulk downloads. Pipeline integration scope: a code/scripts/build_gene_attention_features.py that joins gene HGNC symbol -> NCBI Entrez -> PubTator counts, OpenAlex topic counts, iCite RCR-weighted mentions, and emits gene_attention_features.feather. Acceptance: gene_attention_features.feather exists for all protein-coding genes with: pubtator_mention_count, pubtator_research_only, openalex_mention_count, icite_rcr_weighted_mentions, time-window subsets (pre-2010 / post-2010). t129 regression runs against this feather. PubTator-vs-OpenAlex correlation panel reported as a sanity check.

## [t171] External validation: integrate IntOGen 2024 + DepMap dependency scores
- priority: P1
- status: proposed
- aspects: [computational-analysis]
- related: [hypothesis:0002-cross-study-ranking-divergence-is-structured, task:t146, question:0013-cross-study-replication-rate]
- group: dataset-acquisition
- created: 2026-04-28

t146 (external validation of pan-cancer dNdScv ranking against IntOGen / Martincorena 2017) is the bias-mitigation step for the Bailey-circularity caveat: Bailey 2018 was used to build the project's driver overlay, so reporting Bailey recovery as the headline external-validation number is partially circular. Two independently-constructed external benchmarks resolve this. (1) IntOGen 2024: their 2024 release uses a different driver-detection ensemble (OncodriveFML, OncodriveCLUSTL, MutPanning, etc.) on a different cohort union; recovery against IntOGen is the cleanest 'does the project's rank match independent driver discovery' test. (2) DepMap CRISPR essentiality: orthogonal axis entirely — does the project's top-N pan-cancer driver list intersect more strongly with DepMap-essential genes than chance? This is the biology-not-statistics validation. Both are free public downloads (intogen.org/download; depmap.org/portal). Pipeline integration scope: a code/scripts/build_external_driver_benchmarks.py that pulls IntOGen 2024 driver list (per cancer type and pan-cancer) and DepMap 23Q4+ gene-essentiality scores (mean + cancer-type-stratified), emits external_driver_benchmarks.feather. t146 then computes Spearman, Jaccard@K, and odds-ratio for the project's dNdScv top-N vs each. Acceptance: external_driver_benchmarks.feather exists; t146 produces doc/interpretations/<date>-t146-external-validation.md with three numbers (vs IntOGen, vs Martincorena 2017, vs DepMap) plus interpretation.

## [t172] Investigate MC3 controlled-access tier (TCGA non-PASS variants) for caller-confidence stratification
- priority: P3
- status: blocked
- aspects: [computational-analysis]
- related: [hypothesis:0001-non-tumor-signal-contamination, question:0008-signature-decomposition-tissue-background-subtraction, task:t127]
- group: dataset-acquisition
- created: 2026-04-28

The current ingest uses MC3 v0.2.8 PUBLIC (PASS-only). The controlled-access MC3 tier exposes the non-PASS variants and per-caller filter flags. Motivation specific to h01: when the q008 quantitative contamination-magnitude pass (t127) reports 'this gene shows X% excess SBS1 in unmatched cohorts', a likely critique is 'maybe that excess is low-confidence variants slipping through unmatched-normal filtering'. Having access to per-caller flags lets us stratify the contamination signal by caller-confidence and report which contamination claims are robust to PASS-only restriction. Lower priority because P3 — the public PASS tier should be sufficient for the first contamination magnitude estimate. Access: dbGaP phs000178 (TCGA controlled access), institutional DAR required. Pipeline integration scope: minimal — same MC3 ingest path with an extra column carrying the per-caller filter set. Acceptance: a feasibility memo at doc/feasibility/2026-XX-mc3-controlled-tier.md with go/no-go recommendation. Defer execution until t127 and t146 have produced public-tier results that justify the access friction.

## [t176] Compare driver-gene density on pan-cancer gain arms vs MM hyperdiploidy chromosomes
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [topic:cancer-driver-genes, topic:pan-cancer-interpretive-frames, topic:pan-cancer-mutation-landscape]
- group: meta-analysis
- created: 2026-05-05

Follow-up from MM30 hyperdiploidy mechanism discussion. Test whether common pan-cancer gain arms such as 20q, 7p, 8q, 1q, 7q, and 20p and MM hyperdiploidy chromosomes 3, 5, 7, 9, 11, 15, 19, and 21 are enriched for known cancer drivers or oncogene-dosage targets. Use data/cosmic_cgc.tsv, data/bailey2018_table_s1.tsv, and GRCh37/GRCh38 gene annotations. Compare driver density and aggregate Bailey consensus/frequency scores per arm/chromosome while controlling for gene count and arm size. Deliverable: doc/interpretations/<date>-aneuploidy-driver-dosage-comparison.md with tables separating generic pan-cancer gain targets from plasma-cell/MM-HD-specific dosage-package candidates.

## [t183] Add ERCC2 + stop-gain-enrichment exploratory cross-checks to h08
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- related: [hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and, method:h08-agnostic-association-model, question:0021-positive-control-signature-set-expansion-sbs9]
- group: hypothesis-h08
- created: 2026-05-31

Two exploratory secondary checks: (1) ERCC2 somatic-mutation status as a bladder/urothelial
positive-control covariate targeting SBS5 (paper:Kim2016 ground truth); (2) after any confirmed
SBS4/SBS13 hit, verify elevated nonsense burden in the Adler2023 protein-truncation gene set via
the existing Bailey2018 driver overlay. Sources: paper:Kim2016, paper:Adler2023.

## [t187] commons-hygiene: re-run commons promotion after promote-paper tool bug is fixed
- priority: P3
- status: blocked
- aspects: [software-development]
- group: commons-hygiene
- created: 2026-05-31

`science commons promote paper --from cbioportal --apply` crashes with `TypeError: unhashable type:
'dict'` (commons/promote.py:2810) — filed as science feedback fb-2026-05-31-001. `promote topic`
aborts the whole run on one schema-invalid entity (fb-2026-05-31-002). Once both are resolved
upstream, re-run paper + topic promotion to publish the reusable mutational-signature corpus
(catalogs, methods, aetiology papers + topics) to the commons store. Blocked on the upstream fixes.

## [t188] signature-modality-expansion: indel-call availability census across cBioPortal/MC3
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- related: [hypothesis:0010-joint-indel-sbs-improves-aetiology-discrimination, question:0028-indel-call-availability-across-cbioportal-studies]
- group: signature-modality-expansion
- created: 2026-05-31

Execution arm of `question:0028`: census per-study indel-call presence and depth across the
cBioPortal/MC3 corpus to determine where joint SBS+ID decomposition is feasible (expected: WGS/MC3
yes, most panels no). Deliverable: a per-study indel-feasibility flag.

## [t189] signature-modality-expansion: pilot joint SBS+ID decomposition on MC3 MMRd-vs-MSS
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- related: [hypothesis:0010-joint-indel-sbs-improves-aetiology-discrimination, paper:FerrerTorres2025, paper:Koh2025, paper:Owusu2025]
- group: signature-modality-expansion
- created: 2026-05-31

Cleanest test of `hypothesis:0010`: on MC3 (consensus, indel-bearing), compare aetiology
discrimination (MMRd vs MSS / dMMR status) of SBS-only vs joint SBS+ID assignment using the
redefined indel taxonomy (paper:Koh2025) and multimodal catalogue (paper:FerrerTorres2025).

## [t190] signature-modality-expansion: evaluate copy-number / DBS signatures
- priority: P3
- status: deferred
- aspects: [computational-analysis]
- related: [topic:pan-cancer-signature-catalogs, paper:Everall2026, paper:Steele2022]
- group: signature-modality-expansion
- created: 2026-05-31

Evaluate adding copy-number and doublet-base-substitution (DBS) signatures (paper:Everall2026,
paper:Steele2022). Blocked on CNA ingestion (cross-ref t055 — no CNA modality in the pipeline yet);
DBS is feasible on WGS/WES substrates sooner. Forward-looking.

## [t212] Cross-study signature-exposure reproducibility pass on existing per-study SBS assignments
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [hypothesis:0008-cross-study-signature-exposure-reproducibility, method:h08-agnostic-association-model, question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross]
- group: hypothesis-h09
- created: 2026-06-01

First concrete, data-unblocked test of h09: using per-sample SBS exposures already on disk (run_restricted_sigprofiler_assignment outputs), compare per-cancer-type signature-exposure profiles across independent cBioPortal studies and quantify whether divergences track technical batch (caller/panel/treatment per t178/t179 provenance flags) vs biology. h09 currently has zero tracked tasks (surfaced by 2026-06-01 backlog review). Deliverable: doc/interpretations/<date>-h09-cross-study-exposure-reproducibility.md with a per-cancer reproducibility metric and a batch-vs-biology attribution.

## [t213] Build a unified corpus-capability census inventory (study x cancer_type x assay x matched_normal x n_samples x treatment_flag x indel_depth x caller_provenance)
- priority: P2
- status: proposed
- aspects: [computational-analysis]
- related: [question:0026-cancer-types-with-multiple-independent-cbioportal, question:0028-indel-call-availability-across-cbioportal-studies, question:0017-cross-study-saturation-curve, question:0024-treatment-exposed-cohort-chemotherapy-signature, theme:0001-assay-regime-panel-wes-wgs-as-a-master-technical-confounder-spanning, hypothesis:0008-cross-study-signature-exposure-reproducibility]
- group: corpus-capability-census
- created: 2026-06-02

One inventory feather that multiple hypotheses are independently re-deriving. h10 found only 1 adequate treatment cohort in 198 studies; q026/q028/q017 each separately enumerate corpus capacity. Consolidate into a single per-study capability table so replication-depth questions (per cancer x condition) are answered from one source. Powers q026 (>=2 studies/cancer), q028 (indel depth), q024/q027 (treatment cohorts), q017 (saturation), and the assay-regime theme.

## [t219] Neuroendocrine-histology flag + exclusion sensitivity (q034, P3)
- priority: P2
- status: proposed
- aspects: [computational-analysis, software-development]
- related: [question:0034-neuroendocrine-histology-confound, topic:neuroendocrine-neoplasm-lineage-confound]
- group: neural-gene-meta-analysis
- created: 2026-06-06

Enumerate NET/NEC OncoTree codes present in pipeline studies; add is_neuroendocrine_histology flag; recompute ranks with NEN excluded. MEN1 rank is the positive-control canary; watch ATRX/NF1 as dual CNS+NEN confounds.

### Notes

- 2026-06-08: Downgrade (t218, 2026-06-08): the plan gated NET exclusion on a residual surviving CNS exclusion. t218 shows no residual survives (the candidate enrichment is fully genomic-span/CFS + one WGS cohort's whole-locus reach; not CNS, not panel, not hypermutator, not selection). Keep t219 only as a quick MEN1-canary NET-exclusion sanity check, not as a residual-explaining step. See interpretation:0042-t218-cns-exclusion-wes-panel.

## [t220] Interpret residual: oncofetal (H3) vs selection (H1) (q036/q037, P4/P5)
- priority: P3
- status: proposed
- aspects: [computational-analysis]
- related: [question:0036-oncofetal-fetal-vs-adult-neural-expression, question:0037-canonical-neural-gene-dnds-selection, topic:oncofetal-developmental-reprogramming]
- group: neural-gene-meta-analysis
- created: 2026-06-06

Only if signal survives t217-t219. H3 test: BrainSpan fetal-vs-adult ratio for residual set + stemness/oncofetal correlation in matched-expression studies + recurrence/clustering check. H1 test: dndscv on canonical effectors per cancer type (NF1 = positive control). Opposite predictions decide H1 vs H3.

### Notes

- 2026-06-08: Downgrade (t218, 2026-06-08): H3 oncofetal / H1 dN-dS residual interpretation was gated on a surviving residual after CNS exclusion. None survives (t217+t218 close the candidate enrichment as genomic-span/CFS amplified by one WGS cohort's reach; dndscv 0/9 selected). Low priority - nothing left to interpret mutationally for these genes. See interpretation:0042-t218-cns-exclusion-wes-panel.

## [t221] QA / sanity battery for the neural-gene program
- priority: P2
- status: proposed
- aspects: [computational-analysis, validation]
- related: [hypothesis:0012-neural-gene-enrichment-length-histology-artifact, question:0032-neural-gene-length-null]
- group: neural-gene-meta-analysis
- created: 2026-06-06

Matched- vs unmatched-normal stratification (germline-leak control via matched_normal_studies); hypermutator/MSI stratification (is_hypermutator); common-fragile-site overlap for candidates; data-driven-set vs GO-label-set sensitivity. Runs alongside t217-t220.

### Notes

- 2026-06-08: Arm (a) complete (negative): full-config sample-level hypermutator exclusion across all 91 WES studies (326 hypermutator samples / 1.15M variant rows dropped) leaves the t217 genomic-span residual unchanged (span-matched p 0.002 -> 0.002; per-candidate only 0.4-1.9% of rows dropped). Closes the hypermutator control t218 deferred. Re-aggregation validated: inclusive arm reproduces the canonical wide table gene-for-gene (candidates exact) and t218 wes_only p=0.0022 exactly. Script code/notebooks/t221a_sample_level_hypermutator_exclusion.py; interpretation doc/interpretations/2026-06-08-t221a-sample-level-hypermutator-exclusion.md. Remaining: arm (b) standing-controls panel.
- 2026-06-08: Arm (b) complete: standing-controls panel, all four green. (1) Intronic-fraction stratification — the t218/t221a residual is entirely an all-region call-set artifact: lives in 6 all-region WES studies (intronic>=0.5; span-matched p 0.0002), GONE in 84 exonic-clean studies (candidates at 20.9th pctile, p 0.99). Generalizes pog570 to a 6-study class. (2) CFS positive control — candidates statistically indistinguishable from known CFS genes (~99.8th span pctile, top-0.2% raw). (3) Germline/dbSNP control — candidate rows only 12.7% dbSNP; excluding all dbSNP rows leaves residual intact (p 0.0028->0.0004). (4) Set sensitivity — neither label-free neural_score nor cns_score top-25 reproduces enrichment (small genes, ~33-44th span pctile, p 0.2-0.5). Matched-normal split deferred: config-full lacks matched_normal_studies. Script code/notebooks/t221b_standing_controls_panel.py; interpretation doc/interpretations/2026-06-08-t221b-standing-controls-panel.md. t221 complete (arms a+b).
- 2026-06-08: Populated matched_normal_studies in config-full.yml (closes the t221b F3 gap). Evidence-derived (t221c, code/notebooks/t221c_classify_matched_normal.py): a study is matched iff >=50% of variant rows carry a normal barcode (sample_id_norm) sharing the tumour patient stem (per-patient normal, not pooled/PON). 74/197 studies matched (all TCGA pan_can_atlas, TARGET, pog570, prostate_dkfz, consortium WES). High-precision lower bound: MSK-IMPACT family (msk_impact_2017/msk_chord_2024/msk_impact_50k_2026) is matched-by-design but records no per-variant normal barcode, so flagged + held back (not auto-added). Audit: results/neural-gene-matched-normal-2026-06-08/matched_normal_audit.tsv. Enables a true matched/unmatched germline-leak split (next).
- 2026-06-08: arm (d): ran true study-level matched/unmatched-normal split (t221d_matched_normal_split.py) consuming the t221c-populated matched_normal_studies. Closes t221b-F3 dbSNP proxy. De-confounded region x normal-status 2x2: within region stratum normal-status is inert (all-region matched p 0.0000 / median 0.161 vs unmatched p 0.0006 / median 0.170; both exonic arms null). Biggest residual-carrier pog570 (64% of cand rows) is matched-normal -> germline leak is NOT the driver. Interpretation: doc/interpretations/2026-06-08-t221d-matched-normal-split.md

## [t222] Search/acquire: Schmitt 2023 SCLC neural-gene screen (Nrxn1/Nlgn1/Dcc/Reln)
- priority: P3
- status: proposed
- aspects: [literature-search]
- related: [question:0037-canonical-neural-gene-dnds-selection, paper:Huang2023a, theme:0002-cancer-neuroscience-in-a-mutation-only-pipeline-expression-not-mutation]
- group: searches
- created: 2026-06-07

Cited in Huang2023 as an insertional-mutagenesis + transcriptome screen identifying Nrxn1/Nlgn1/Dcc/Reln in murine + human SCLC — a rare *label-free* neural-gene discovery in a NON-CNS cancer. Confirm peer-review status (was a bioRxiv preprint), get the gene list, and assess whether it offers a data-driven neural-gene set in a peripheral tumor to cross-check against our candidates.

## [t223] Search/acquire: Chen 2025 Cancer Cell pancreatic neural-invasion single-cell + spatial atlas
- priority: P3
- status: proposed
- aspects: [literature-search, dataset-acquisition]
- related: [question:0035-label-free-neural-gene-definition, topic:perineural-invasion-axon-guidance-genes]
- group: searches
- created: 2026-06-07

Flagged by Lu2026 (DOI 10.1016/j.ccell.2025.06.020, "Trace-n-Seq"): integrated single-cell + spatial transcriptomics of pancreatic neural invasion. Candidate source for a data-driven tumor-nerve-interface gene signature to test against the top-mutated list (q035).

## [t224] Search: Lu2026 pan-cancer PNI transcriptomic classifier (2,029 patients, 12 cancer types)
- priority: P3
- status: proposed
- aspects: [literature-search]
- related: [question:0033-neural-enrichment-cns-exclusion, topic:perineural-invasion-axon-guidance-genes]
- group: searches
- created: 2026-06-07

Lu2026 references a pan-cancer perineural-invasion transcriptomic classifier without an accession. Track down the source publication + gene set; useful for cancer-type-structured PNI gene definitions and the CNS-vs-peripheral discrimination.

## [t225] Acquire label-free neural reference atlases (BrainSpan, HPA, Allen Brain Cell Atlas, PanglaoDB)
- priority: P2
- status: proposed
- aspects: [dataset-acquisition]
- related: [question:0035-label-free-neural-gene-definition, question:0036-oncofetal-fetal-vs-adult-neural-expression, dataset:brainspan, dataset:human-protein-atlas, dataset:allen-brain-cell-atlas, dataset:panglaodb]
- group: dataset-acquisition
- created: 2026-06-07

Acquire the reference resources backing the data-driven neural-gene score (t216): GTEx (have), Human Protein Atlas tissue-specificity, Allen Brain Cell Atlas cell-type markers, PanglaoDB markers, and BrainSpan (fetal-vs-adult for the H3 test). Land as per-gene tables joinable to the gene universe. Blocks t216/t220.

## [t231] Normalize Science prose citation lint warnings
- priority: P3
- status: proposed
- aspects: []
- group: science-health-cleanup
- created: 2026-06-27

Reduce the remaining prose_lints warnings from science validate: bare-author-year, short-form-ids, and unsupported-citation-syntax. Work in small batches by file family; prefer canonical citation and entity reference syntax rather than broad search/replace, and rerun science validate after each batch.

## [t232] Audit and resolve Science unverified markers
- priority: P2
- status: active
- aspects: []
- group: science-health-cleanup
- created: 2026-06-27

Review the 50 [UNVERIFIED] warnings from science validate/refs check. For each marker, either verify the claim against the cited source and remove or reword the marker, downgrade unsupported claims to explicit uncertainty, or create a targeted follow-up task when verification requires new source acquisition. Preserve uncertainty labels when they are epistemically meaningful.
