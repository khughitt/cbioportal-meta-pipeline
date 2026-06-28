---
type: synthesis
title: 'Synthesis: hypothesis:0007 agnostic covariate-association recovers known signature aetiologies'
status: active
created: '2026-06-02'
updated: '2026-06-02'
report_kind: hypothesis-synthesis
id: synthesis:0011-agnostic-covariate-association-recovers-known-signature-aetiologies-and
hypothesis: hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
generated_at: 2026-06-02 09:52:22+00:00
source_commit: 037f0ab2d3c84ecc56bebd843e361c1a9dfbfa66
provenance_coverage: thin
---

## State

The hypothesis proposes a phenome-wide, within-tissue association of per-sample mutational-signature exposures against all co-measured covariates — clinical fields, TMB-derived features, and unsupervised mRNA expression modules — with the known aetiology→signature map as a mandatory positive-control gate (H08a) before any discovery work (H08b) is licensed.

The H08a gate was pre-registered with a 2-of-3 pass rule across three arms: UV→SBS7 (SKCM), smoking→SBS4 (LUAD+LUSC), and APOBEC3A/B expression→SBS2/13 (six APOBEC-enriched tissues). The association scan ran on MC3 WES per-sample SBS refit exposures with a BH-FDR-controlled grid (family size 638), using centered-log-ratio coordinates and a frozen covariate denominator (interpretation:0024).

The current verdict is **H08a `[?]` inconclusive (1/3 arms pass)**. Arm C (APOBEC3A/B mRNA→SBS2/13) is the single clean pass: rank 1/10, BH-q ≈ 4.4e-12, permutation p = 0.001, robust to APOBEC3-locus cis-mutation exclusion and to proliferation-score conditioning (interpretation:0026). Arms A (UV) and B (smoking) failed on proxy inadequacy — an anatomic-site UV ordinal saturated by SKCM metastatic deposits and a continuous pack-years variable confounded by missing never-smoker zeros — not on method failure (interpretation:0024). A repaired smoking-arm rerun using a binary ever-smoker covariate recovered a significant positive association (BH-q = 5.1e-4) but ranked 5/8, still below the top-3 gate (interpretation:0025). H08b (discovery) remains locked; question:0022-apobec-a3a-a3b-joint-expression-and-mmr-omikli, question:0023-sbs40-vs-sbs5-clocklike-expression-module, and question:0025-causal-direction-guard-for-expression-signature are open design questions for any future gate repair.

## Arc

Arc reconstruction is limited because 6 interpretations in this bundle carry no `prior_interpretations` chains; the sequence below is reconstructed from task completion order only.

Feasibility and infrastructure came first: task:t177 (literature scan), task:t196 (question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross verdict), task:t178, and task:t179 established that per-sample WES refit is sound and that trust columns must be propagated. Substrate construction ran in two tracks: task:t197 produced MC3 per-sample SBS exposures across all seven arm strata (interpretation:0022), and task:t198 built per-arm NMF expression modules with a leakage firewall, selecting K=5–10 by Brunet cophenetic criterion (interpretation:0023). With substrates in place, task:t199 ran the H08a association core: the APOBEC arm passed cleanly; UV and smoking failed on proxy quality. Diagnostic work (task:t201 via interpretation:0026) and a smoking repair sequence (task:t202–t204 via interpretation:0025) confirmed an operationalization artifact in Arm B but could not promote it. An exploratory SBS40-vs-SBS5 prototype (task:t182) found a suggestive SKCM immune-module signal, not a confirmatory one (interpretation:0028). The hypothesis remains at `proposed`.

## Research fronts

**Open questions.** question:0022-apobec-a3a-a3b-joint-expression-and-mmr-omikli (APOBEC3A+APOBEC3B joint expression + MMR-omikli covariate design), question:0023-sbs40-vs-sbs5-clocklike-expression-module (SBS40-vs-SBS5 separation via age-conditioned expression modules — the H08b flagship test), and question:0025-causal-direction-guard-for-expression-signature (operationalisable causal-direction guard for expression↔signature associations) are the primary open design questions. question:0020-minimum-sample-size-and-caller-provenance-for and question:0021-positive-control-signature-set-expansion-sbs9 are secondary gates for a future expanded pre-registration.

**Open tasks.** task:t212 (cross-study signature-exposure reproducibility pass — P2 proposed) and task:t183 (ERCC2 + stop-gain-enrichment exploratory cross-checks — P3 proposed) are the remaining live tasks. All activation-layer and substrate tasks are closed.

**Gate decision.** task:t205 established that H08b is not opened confirmatorily at `[?]`. The two defensible paths are: (1) design a repaired positive-control pre-registration addressing both the UV proxy weakness and lung burden-dominance before any H08a re-read, or (2) keep H08a inconclusive and proceed with narrowly scoped exploratory work only.

**Knowledge gaps.**
- `topic:clinical-translational-signatures` — 0 papers vs 2 questions referencing it (question:0024-treatment-exposed-cohort-chemotherapy-signature, question:0027-does-excluding-treatment-signature-high-samples)
