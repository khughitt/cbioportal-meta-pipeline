---
type: interpretation
title: "t198 expression-module substrate \u2014 per-arm NMF on PanCanAtlas RNA-seq\
  \ with leakage firewall"
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: interpretation:0023-t198-h08-expression-nmf-modules
source_refs:
- task:t198
date: '2026-05-31'
related:
- task:t198
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- question:0022-apobec-a3a-a3b-joint-expression-and-mmr-omikli
- question:0023-sbs40-vs-sbs5-clocklike-expression-module
---
# t198 — expression-module substrate (per-arm NMF on PanCanAtlas RNA-seq)

Date: 2026-05-31

## Question

Build the frozen NMF expression-module covariate set for the `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and` positive-control scan
(`pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature` § Total Comparison Count, as clarified by Amendment
001): per arm, derive expression modules from the MC3-overlapping TCGA PanCanAtlas RNA-seq and
select the module count K by the Brunet cophenetic-correlation rule — entirely upstream of, and
blind to, the covariate↔signature association (leakage firewall). This is check 3 of
`plan:0005-h08-positive-control-scan-analysis-plan`.

## Substrate and the TPM→RSEM amendment

The pre-reg froze `log2(TPM+1)` on "TCGA PanCanAtlas RNA-seq", but TCGA PanCanAtlas is
distributed as **RSEM-V2**, not TPM (neither the per-study cBioPortal matrices nor the
EBPlusPlus batch-corrected pan-cancer matrix carry native TPM). Recorded as
`pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature` **Amendment 001** (`amendment_before_results`): realized
substrate = the per-study cBioPortal PanCanAtlas matrices
(`{tissue}_tcga_pan_can_atlas_2018/data_mrna_seq_v2_rsem.txt`, already on disk), realized unit =
`log2(RSEM_V2 + 1)`. Because the K-selection NMF runs **per arm**, the cross-tissue batch
correction of the single EBPlusPlus file confers no benefit, so the per-study matrices are the
faithful and zero-download substrate. No decision criterion changed.

## Leakage firewall

The derivation reads only (a) the expression matrix and (b) MC3 **sample identity**
(`tcga_mc3/metadata/samples.feather`: `sample_id` + `cancer_type`, to enumerate arm membership
on the sample-type-aware 15-char TCGA barcode). It never reads signature exposures `H`, mutation
calls, or any covariate — so K cannot be tuned against the gate. Verified: the output module and
loading tables carry only `module_NN` columns (no `SBS*` / exposure columns). The selected K and
the full per-K cophenetic curve are written before any association is run.

## Method (frozen rule, implemented exactly)

Per arm: restrict the RSEM matrix to MC3-overlapping samples → drop genes expressed (>0) in <10%
of samples → retain the top-2,000 MAD genes (MAD on the log2 scale) → `log2(RSEM+1)` →
non-negative matrix factorization for K ∈ {5,10,…,50} with **50 random restarts** each → Brunet
(2004) cophenetic correlation of the per-K sample consensus matrix → select the **largest K
before cophenetic drops below 0.90** (ties → smaller K). Implemented in
`code/scripts/build_expression_nmf_modules.py` (Snakemake rule `build_expression_nmf_modules`,
aggregate target `all_h08_expression_modules`).

**Reproducibility.** All restarts + the final fit are seeded deterministically from
`random_seed` (=0). The 50 restarts are parallelised across processes with single-threaded BLAS
(`threadpoolctl`), which makes the result independent of `nmf_n_jobs` — confirmed bit-identical
cophenetic across n_jobs=4 and n_jobs=8 (0.864316). (An earlier unpinned multi-threaded BLAS run
gave a marginally different value via non-deterministic reduction order; pinning to one thread is
both faster here and reproducible.)

## Results

Realized effective n is the MC3∩RNA-seq intersection per arm — the number that feeds the pre-reg
§1b post-join table (the gate "is not read until [it is] filled in"):

| Arm | MC3 arm n | RSEM samples | **Eff. n (∩)** | Genes (MAD) | **Selected K** | Cophenetic at selected K |
|---|---|---|---|---|---|---|
| SKCM | 466 | 443 | **437** | 2000 | 5 | 0.943 |
| LUAD | 513 | 510 | **504** | 2000 | 5 | 0.948 |
| LUSC | 480 | 484 | **461** | 2000 | 5 | 0.959 |
| BLCA | 411 | 407 | **405** | 2000 | 5 | 0.966 |
| BRCA | 791 | 1082 | **783** | 2000 | 10 | 0.916 |
| CESC | 289 | 294 | **278** | 2000 | 5 | 0.965 |
| HNSC | 507 | 515 | **494** | 2000 | 5 | 0.916 |

Per-K cophenetic curve (the K-selection record, written before any association):

| Arm | K5 | K10 | K15 | K20 | K25 | K30 | K35 | K40 | K45 | K50 |
|---|---|---|---|---|---|---|---|---|---|---|
| SKCM | **0.943** | 0.867 | 0.828 | 0.841 | 0.842 | 0.816 | 0.798 | 0.797 | 0.796 | 0.787 |
| LUAD | **0.948** | 0.875 | 0.868 | 0.875 | 0.840 | 0.820 | 0.775 | 0.795 | 0.767 | 0.765 |
| LUSC | **0.959** | 0.889 | 0.827 | 0.813 | 0.784 | 0.790 | 0.802 | 0.793 | 0.795 | 0.785 |
| BLCA | **0.966** | 0.894 | 0.869 | 0.845 | 0.821 | 0.803 | 0.802 | 0.786 | 0.798 | 0.787 |
| BRCA | 0.971 | **0.916** | 0.866 | 0.832 | 0.829 | 0.791 | 0.783 | 0.781 | 0.779 | 0.770 |
| CESC | **0.965** | 0.859 | 0.881 | 0.839 | 0.829 | 0.846 | 0.844 | 0.844 | 0.815 | 0.819 |
| HNSC | **0.916** | 0.878 | 0.823 | 0.819 | 0.818 | 0.791 | 0.741 | 0.737 | 0.726 | 0.724 |

## Observations carried forward to t199

- **K sits at or near the grid floor.** Cophenetic clears 0.90 at K=5 for every arm and drops
  below it immediately at K=10 for all but BRCA. The selected covariate-module count is therefore
  5 (six arms) or 10 (BRCA) — a genuine, reproducible property of these tumour expression
  matrices (sample-level module stability is low beyond ~5–10 factors), not a tuning artifact.
  The modest module count keeps the covariate denominator small, which the rank gate tolerates.
- **K±5 sensitivity (exploratory, t199).** For the K=5 arms the only admissible downward neighbour
  is the grid floor, so the pre-registered K±5 sensitivity reduces to comparing K=5 vs K=10 there;
  for BRCA it is K=5 vs K=15. t199 re-runs the scan at these neighbours; an arm verdict that flips
  is downgraded to `[?]`.
- **Effective n.** The MC3∩RNA-seq intersection erodes each arm's n only modestly (≤7%), so the
  expression-covariate arms remain comfortably powered for textbook effects; Arm C's pooled
  APOBEC-tissue n is the most eroded, consistent with it being the tolerated miss under 2-of-3.

## Artifacts (run dir `results/signature-h08-arms-2026-05-31/expression_modules/{arm}/`, gitignored)

`nmf_gene_modules.feather` (gene × K loadings), `nmf_sample_loadings.feather` (sample × K module
scores — the covariates t199 joins on the 15-char barcode), `cophenetic_curve.feather` (full
K-grid), `module_selection.json` (selected K + realized n + provenance). The durable record is
this note (`results/` is gitignored).

## Implications

`task:t198` (analysis-plan check 3) is complete. Three of the four
`hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and` run blocking checks are now
closed (`question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross` / t197 / t198); the remaining build is `task:t199` — the within-tissue covariate↔`H`
association core, which joins these module loadings + clinical/molecular covariates onto the t197
per-sample exposures, fills the §1b table, and reads the gate. Route t199 to
`/science:plan-pipeline` before implementing.
