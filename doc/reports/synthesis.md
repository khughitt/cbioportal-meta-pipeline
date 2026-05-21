---
id: "synthesis:rollup"
type: "synthesis"
title: "Project synthesis - cbioportal"
report_kind: "synthesis-rollup"
generated_at: "2026-04-28T03:09:06Z"
source_commit: "c1c6b1f29eef8326e3efde948df540ecc23c95ed"
synthesized_from:
  - hypothesis: "hypothesis:h01-non-tumor-signal-contamination"
    file: "doc/reports/synthesis/h01-non-tumor-signal-contamination.md"
    sha: "e367c5d95d1f23c74cc49854be342b60ef523e18"
  - hypothesis: "hypothesis:h02-cross-study-ranking-divergence-is-structured"
    file: "doc/reports/synthesis/h02-cross-study-ranking-divergence-is-structured.md"
    sha: "4a5ab7402a77527981a6a799964ca5287224aebf"
  - hypothesis: "hypothesis:h03-gene-length-confounds-literature-attention"
    file: "doc/reports/synthesis/h03-gene-length-confounds-literature-attention.md"
    sha: "b6325b216fda59fe206224d8b02a210aa990cbf3"
  - hypothesis: "hypothesis:h04-mhn-pathway-ordering"
    file: "doc/reports/synthesis/h04-mhn-pathway-ordering.md"
    sha: "7c0fc6da5091e9dd3073b062403f0b51f42b9b8d"
  - hypothesis: "hypothesis:h05-healthy-somatic-background-atlas"
    file: "doc/reports/synthesis/h05-healthy-somatic-background-atlas.md"
    sha: "566d645b7fbe4793ad5258b04fc74bca70a51339"
  - hypothesis: "hypothesis:h06-pre-malignant-n-minus-1-driver-carriage"
    file: "doc/reports/synthesis/h06-pre-malignant-n-minus-1-driver-carriage.md"
    sha: "ef0f16245645ca463da0bb99c8a4a253135a15e7"
emergent_threads_sha: "a11881f43b9732055f94603ad02645006178ed7a"
orphan_question_count: 5
---

# Project synthesis — cbioportal

## TL;DR

- The active spine is three hypotheses: h01 (non-tumor contamination is detectable and partially correctable), h02 (cross-study ranking divergence is structured, not random), and h03 (gene length confounds literature attention beyond mutation-count mediation). Three additional hypotheses (h04 MHN ordering, h05 healthy somatic background atlas, h06 pre-malignant n-1 driver carriage) sit in candidate phase.
- The strongest empirical results to date sit under h02: the t131 → t144 → t145 dNdScv chain produced 62/100 Bailey driver recovery at K=100, with TP53/KRAS/NRAS/PIK3CA/FBXW7/PTEN/RB1 occupying ranks 1–7, and confirmed that raw and dNdScv rankings are nearly uncorrelated (ρ = +0.043) while length-adjusted and dNdScv rankings are anti-correlated (ρ = −0.468) — divergence is systematic, not random.
- h01 has infrastructure ready (t111 normal-tissue spectra pipeline; 56 per-tissue Li 2021 reference spectra) but no decisive contamination-magnitude estimate yet; one direct test (t110 BRCA SBS1/SBS5 matched-vs-unmatched) returned an opposite-sign verdict and one signature-bias route (t126 SBS1 LRR-bias) was deferred under a pre-registered termination rule due to panel coverage limits.
- The largest unresolved data-quality issue is mean_inclusive inflation (t145) propagating from `create_combined_gene_cancer_freq_table` forward; the raw-frequency and length-adjusted comparison panels cannot be reported externally until downstream feathers are regenerated.
- Five questions (q009, q014, q015, q016, q017) and eight interpretations sit outside the hypothesis spine; the emergent-threads analysis surfaces two candidate hypothesis frames (signature-based contamination QC; pan-cancer aggregator methodology) and proposes folding q014/q016 into h02/h03 rather than spawning new top-level nodes.

## State

The project's collective belief, distilled from the six per-hypothesis files, has three weight centers.

**Cross-study ranking divergence is real and structured (h02, partial provenance).** The full pan-cancer dNdScv run (interpretation:2026-04-26-t131-full-pan-cancer-dndscv-run) is the highest-evidence artifact in the project. After the tiebreaker fix (interpretation:2026-04-27-t144-tiebreaker-fix-rerun) and the diagnosis of the mean_inclusive inflation (task:t145, interpretation:2026-04-27-t145-mean-inclusive-inflation-diagnostic), the structured-divergence claim is empirically supported for the raw-vs-dNdScv pair. Leave-one-study-out replication (task:t149, question:q013) and external IntOGen/Martincorena 2017 validation (task:t146) are the next decisive moves.

**Non-tumor contamination is testable but not yet measured (h01, partial provenance).** The Li 2021 normal-tissue spectra pipeline (interpretation:2026-04-19-t111-normal-tissue-spectra-pipeline) is built and validated. The first quantitative signature-based contamination estimate (task:t127, question:q008) and the first esophagus/colon background pilot (task:t151) have not run. The BRCA matched-vs-unmatched probe (interpretation:2026-04-22-t110-sbs1-sbs5-brca-comparison) returned a result opposite to the contamination-proxy expectation, and the SBS1 LRR-bias diagnostic route (question:q009) hit a pre-registered termination on panel data (interpretation:2026-04-24-t126-sbs1-lrr-bias-per-study).

**The literature-attention claim is well-posed but pre-empirical (h03, thin provenance).** No interpretation cites h03 directly. The motivating Jaccard@100 = 0.015 between raw and length-adjusted top lists (recorded in discussion:2026-04-24-gene-length-bias-in-mutation-rankings-and-literature) is the only available structural anchor. The headline number `beta_length` (predicted +0.10 to +0.40) does not yet exist; task:t129 specifies the regression and task:t154 (panel-vs-WES ascertainment) is the gating prerequisite.

What's contested: TTN at rank 4–5 in the post-fix dNdScv ranking is currently treated as a residual confounder pointing toward replication timing (question:q003), but the gene-level RT correlation with the dNdScv residual has not been computed at full scale; whether it is a methodological artifact (hypermutator leakage; task:t147) or a substantive biological residual remains open.

What's strongest: the dNdScv post-fix top-7 — TP53, KRAS, NRAS, PIK3CA, FBXW7, PTEN, RB1 — replicates the Bailey 2018 consensus core almost exactly, anchoring the project's claim that canonical drivers replicate strongly across schemes.

## Arc

The active hypotheses constitute a coherent two-axis framing. h01 and h03 sit on opposing axes of the same diagnostic problem: h01 asks whether the project's mutation-frequency tables contain non-tumor signal, while h03 asks whether the field's literature-attention measures contain length-confound signal — both are claims about systematic distortion of the rank-and-importance signal that drives "what is a cancer driver." h02 sits between them as the empirical test bench: it is where ranking-scheme comparisons (raw, length-adjusted, dNdScv) are quantified at scale, and is the hypothesis under which the dNdScv chain (t131 → t144 → t145) is run.

**h01 — non-tumor signal contamination (partial provenance).** The investigation moved from literature framing (q001 NOTCH1 esophagus, q007 normal-tissue null, q008 background subtraction) to infrastructure (t111 Li 2021 spectra pipeline) to its first empirical probes (t110 BRCA SBS1/SBS5; t122/t123 BRCA RT pilots; t126 SBS1 LRR-bias per-study). Two probes returned non-confirmatory or terminated verdicts; the next decisive moves are the q008 quantitative pass (task:t127) and the esophagus/colon pilot (task:t151). The structural barrier — panel cohorts being underpowered for SBS1 LRR-bias because driver-gene panels concentrate coverage in early-replicating territory — would be removed by adding a WGS cohort.

**h02 — cross-study ranking divergence is structured (partial provenance).** The investigation began from a PoC-scale Jaccard@100 = 0.015 finding, scaled to the full pan-cancer dNdScv run (task:t131, 146 cancer types, 474,524 annotated rows), and surfaced two data-quality issues that have since been fixed (task:t144 tiebreaker; task:t145 mean_inclusive). The structured-divergence claim is supported for the raw-vs-dNdScv pair; the leave-one-study-out test of P1/P2 is the open empirical front (task:t149).

**h03 — gene length confounds literature attention (thin provenance).** The hypothesis is well-posed with a clear falsification criterion (`beta_length ≤ 0` after covariate adjustment falsifies P2) but no decisive measurement exists. The regression pipeline (task:t129), Stoeger & Nunes Amaral 2018 anchor (task:t130), and ascertainment prerequisite (task:t154) are all open. Promotion of evidence is gated on the t144/t145 fixes propagating downstream so mutation counts in the regression are stable.

The three actives interlock: h02's dNdScv residuals expose the gene-length-vs-RT residual question (q003 + q011) that h03 must control for; h01's contamination correction would change the per-gene mutation counts that feed h02's rankings; h03's ascertainment finding (t154) feeds back into h02's interpretation of which top-rank genes are real biology versus design-induced. None of the three has reached a fully measured headline result yet, but the chain from infrastructure to first decisive estimate is short for h02 (LOSO + IntOGen) and one or two analyses away for h01 (t127 + t151) and h03 (t129 + t154).

## Research fronts

Ranked across the active hypotheses by uncertainty density and decisiveness:

1. **task:t149 — leave-one-study-out top-N replication-rate analysis** (from h02). Decisive test of P1 and P2; no LOSO numbers exist yet. Highest-priority open front.
2. **task:t127 — first q008 quantitative contamination-magnitude estimate** (from h01). Uses the t111 Li 2021 spectra pipeline against tcga_mc3 vs msk_impact_2017; would deliver the first project-internal contamination magnitude.
3. **task:t129 — partial-slope regression for `beta_length`** (from h03). Decisive test of h03's central claim; blocked informally on t144/t145 propagation.
4. **task:t146 — external validation of pan-cancer dNdScv against IntOGen / Martincorena 2017** (from h02). Addresses the Bailey-circularity caveat in the post-fix headline.
5. **task:t151 — esophagus/colon normal-tissue background pilot** (from h01). First end-to-end test of the contamination-correction proposition P3 on a tractable tissue.
6. **task:t154 — panel-vs-WES ascertainment analysis** (from h03). Gating prerequisite for the t129 regression; also feeds back into h02 interpretation.
7. **task:t147 — hypermutator-stratified dNdScv re-run** (from h02). Diagnostic for the TTN-at-rank-4 residual.
8. **task:t153 — CFS overlap annotation and RT-vs-CFS residual regression** (from h02). Tests whether common-fragile-site loci form a distinct confounder channel separable from broad replication timing (also addresses orphan question:q014).
9. **task:t158 — cross-study saturation curve for top-N stability** (from h02). Empirical complement to t149 (also addresses orphan question:q017).
10. **task:t155 — pan-cancer dNdScv aggregation rules under q-value floor pile-up** (from h02). Methodological prerequisite for reporting a pan-cancer ranking (also addresses orphan question:q015).

**Blocking dependency carried across the project**: the task:t145 mean_inclusive fix must propagate downstream from `create_combined_gene_cancer_freq_table` before the raw-frequency, length-adjusted, and length-attention regression panels can be reported.

## Candidate frames

**h04 — MHN pathway-level ordering (thin provenance, candidate).** Proposes that cross-sectional cBioPortal/GENIE data contain enough joint-distribution signal for the observation-event-corrected MHN formulation in paper:Schill2024 (implemented in paper:Vocht2026) to recover a directed per-histology progression order at the Sanchez-Vega 2018 pathway level. Promotion is gated on three criteria: task:t133 VAF availability audit completing; the paper:Schill2024 observation-event correction confirmed usable for diagnostic cBioPortal cohorts with panel-specific missingness; and simulation calibration (task:t152) recovering ≥70% of injected pathway-level edges from synthetic tumors at the project's panel and cohort-size distribution. All five gating tasks (t132, t133, t134, t135, t152) are open.

**h05 — healthy somatic background atlas (thin provenance, candidate).** Proposes that healthy somatic-mutation rates span >2 OoM across tissues and that substituting a meta-analyzed cross-tissue normal null for the project's current within-pipeline null produces calibrated, tissue-specific shifts in apparent driver frequency in unmatched-normal studies. The hypothesis is a generalization of h01: where h01 targets within-sample correction, h05 frames "background" as positive cross-population knowledge. Promotion is gated on task:t150 (normal-tissue WGS cohort feasibility audit). The Li 2021 spectra pipeline (interpretation:2026-04-19-t111-normal-tissue-spectra-pipeline) is the closest existing infrastructure; task:t151 is the scoped pilot that follows.

**h06 — pre-malignant n-1 driver carriage (thin provenance, candidate).** Proposes that cBioPortal pre-malignant cohorts (Barrett's → EAC; MGUS/SMM → MM; MDS → AML; IPMN → PDAC; ASAP/HGPIN → PRAD; adenoma → CRC; CIN → cervical) carry n-1 of the canonical invasive-cancer drivers of the same lineage, with a small residual set of "late-stage" checkpoint-enriched drivers. Distinguished from h04 on operational grounds: h06 uses directly observed pre-malignant vs invasive sequencing data rather than cross-sectional probabilistic inference. Promotion is gated on task:t156 (cBioPortal pre-malignant cohort audit) finding ≥3 cancer types with n ≥ 30 pre-malignant samples; task:t157 (first paired driver-overlap analysis on Barrett's → EAC or MDS → AML) follows.

## Knowledge Gaps (rollup)

No knowledge gaps detected this run.

The project graph currently has zero claim-level rows (graph project-summary returned `claim_count: 0`), so `compute_topic_gaps` produced no scoreable entries this cycle. The Knowledge Gaps surface will populate once specify-model and interpret-results runs begin materializing graph claims.

## Emergent threads

`doc/reports/synthesis/_emergent-threads.md` enumerates **5** orphan questions (q009, q014, q015, q016, q017) and **8** orphan interpretations, and proposes two candidate hypothesis frames (signature-based contamination QC absorbing q009; pan-cancer aggregator methodology absorbing q015) plus folding q014 into h02 and q016 into h03 as extensions rather than new top-level nodes. The cross-hypothesis bridges q007 (h01↔h05), q011 (h02↔h03), and q012 (h04↔h06) are the load-bearing connective tissue of the current spine.
