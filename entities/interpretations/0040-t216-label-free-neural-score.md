---
type: interpretation
title: "t216: a reproducible label-free neural score confirms the candidates are genuinely\
  \ CNS-specific \u2014 but the score cannot separate neural effectors from large\
  \ CFS loci (AUC 0.47), so high neural expression does not rescue the candidate enrichment\
  \ from the genomic-span confound"
status: active
created: '2026-06-08'
updated: '2026-06-08'
id: interpretation:0040-t216-label-free-neural-score
related:
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- question:0035-label-free-neural-gene-definition
- interpretation:0041-t217-genomic-span-cfs-null
- interpretation:0039-t215-neural-gene-reproduction-gate
- task:t216
- task:t218
---

# Interpretation: t216 — label-free neural-enrichment gene score (GTEx)

> **Verdict: a reproducible, label-free neural score is delivered (q035), and it confirms the 9
> candidates are genuinely — in fact *more* — CNS-specific than the canonical effectors. But the
> score's decisive hard test FAILS: it cannot tell bona-fide neural cancer effectors apart from large
> common-fragile-site loci (AUC effectors-vs-CFS = 0.47 ≈ chance), because the brain expresses the big
> fragile-site genes. So a high neural score does NOT rescue the candidates from t217's genomic-span
> verdict — "neural" is a real but causally-inert expression label on a size-driven mutation pattern.**

- **Task:** `t216` (q035 label-free neural definition; plan step 2).
- **Script:** `code/notebooks/t216_label_free_neural_score.py`
- **Artifacts:** `results/neural-gene-label-free-2026-06-08/` (datapackage.json + 3 resources;
  `gene_neural_enrichment.feather` is the reusable per-gene covariate).
- **Substrate:** GTEx median TPM over 53 tissues (`/data/raw/expression-atlas/gtex/`, 49,575 genes);
  genomic span from `data/gene_replication_timing.feather` for the size-matched benchmark. No GO labels
  (q035 covenant). `random_seed = 0`.

## What was built

A per-gene **neural-enrichment score** = log₂((mean TPM over neural tissues + 1) / (mean TPM over
non-neural tissues + 1)), with the Cortese-2020 sub-partition into **CNS-structural** (12 brain
regions), **PNS/autonomic** (tibial nerve), and **neuroendocrine-lineage** (pituitary + adrenal)
sub-scores, plus the Yanai-2005 **tau** tissue-specificity index. It is validated against three control
sets: canonical effectors (positive), housekeeping genes (easy negative), and — per the t215 redirect —
a **genomic-span-matched large-locus / CFS** set (hard negative).

## Findings

**F1 — The score is reproducible and the candidates are genuinely, strongly CNS-specific.** All 9
candidates score in the top ~1.2 % of the genome on `neural_score` (median percentile **1.22**), driven
by the CNS sub-score (cns_score 1.6–4.3, tau 0.81–0.96 — highly tissue-restricted). AUC(candidates vs
housekeeping) = **0.994**. The hand-picked list was not arbitrary: these are among the most
brain-specific genes in the genome.

**F2 — The candidates are *more* neural-specific than the canonical effectors.** Candidate median
neural percentile (1.22) is *better* than the effectors' (8.11). The effector positive control is
**heterogeneous**: CNS-synaptic effectors score high (NLGN3, GRIN2A/B, NTRK2 in the top ~2 %), but
receptor / growth-factor effectors are broadly or peripherally expressed and score low-to-negative
(ADRB2 97th pct, NGF 92nd, NTRK1 74th, CHRM3 64th). So the score is, precisely, a **CNS-structural**
score — and the candidates are textbook CNS-structural genes.

**F3 — Moderate AUC vs housekeeping, but ~chance vs CFS — the score is confounded with genomic size.**
AUC(effectors vs housekeeping) = **0.711** (the easy separation works, weakened by the heterogeneous
effectors). But AUC(effectors vs CFS) = **0.468 ≈ 0.5**, and AUC(effectors vs a *genomic-span-matched*
random control) = **0.631** with a 90 % interval of **0.494–0.741** that straddles chance. The neural
score **cannot distinguish bona-fide neural effectors from large fragile-site loci**, because canonical
CFS genes (CSMD1, CNTNAP2, DLG2, NRXN1/3, CADM2 …) are themselves brain-expressed. Neural expression and
large-genomic-locus / CFS status are entangled.

**F4 — Therefore a neural score does not rescue the candidate enrichment.** This is the redirect's exact
prediction realised: because a same-size CFS locus scores as "neural" as a real effector, the candidates'
high neural score is fully consistent with them being incidental large brain loci. Combined with t217
(no positive selection; enrichment dissolves under genomic-span normalization), the causal chain is:
**large CNS-structural genes → large late-replicating loci (CFS) → high passenger mutation counts**, with
neural expression a *correlate* of locus size, not a cause of the mutation burden.

## Bearing on h12 / q035

- **q035 answered:** a label-free neural definition is feasible and reproducible (delivered as
  `gene_neural_enrichment.feather`), removing the dependence on the hand-labelled 9-gene list. But the
  definition is **only usable as a size-controlled covariate** — used raw it re-imports the genomic-span
  confound, since neural-expression specificity tracks locus size in the relevant gene class.
- **h12 strengthened:** the "neural" label is real at the expression level yet causally inert for
  mutation burden. This is the cleanest possible statement of h12 — the enrichment is a
  length/CFS/histology artifact onto which a true-but-non-causal neural label has been mapped.

## Decision & redirect

1. **Use `neural_score` only with size control downstream.** Any enrichment statistic built on the
   label-free score (t218/t219) must be reported *adjusted for genomic span / late-replication*, and
   benchmarked against the span-matched null from t217 — never as a raw neural-vs-rest contrast.
2. **Report sub-scores, not just the composite.** The CNS sub-score carries the signal; PNS and
   neuroendecrine sub-scores are weak (and the neuroendocrine proxy is poor — see caveats). For the
   CNS-exclusion test (`t218`) the CNS sub-score is the relevant stratifier.
3. **The program's expected end-state is reaffirmed:** H5/length + CFS account for the bulk (t217), and
   the label-free route (t216) cannot manufacture a neural signal that beats a size-matched control. The
   residual to chase is the small panel-ascertainment effect (t217 F5 / q016), not neural biology.

## Caveats

- **Effector positive control is heterogeneous.** Peripheral/receptor effectors (ADRB2, NGF, NTRK1,
  CHRM3) are not CNS-specific, which lowers AUC vs housekeeping and makes the score specifically a
  *CNS-structural* instrument. This is a property of cancer-neuroscience biology (effectors act via
  perineural/autonomic signalling, not CNS-structural expression), not a defect of the score — but it
  means "neural score" should be read as "CNS-structural expression score".
- **Neuroendocrine sub-score is a weak proxy.** GTEx has no NET/NEC tissue; pituitary + adrenal are the
  closest, so the neuroendocrine sub-score is not a substitute for the `t219` OncoTree-based NEN flag.
- **HPA deferred.** The plan's secondary atlas (Human Protein Atlas tissue-specificity) is not available
  locally; it is flagged in the script as a deferred sensitivity layer rather than silently skipped. A
  GTEx-only score is sufficient for the q035 conclusion (the CFS-confounding is intrinsic, not an
  atlas-choice artifact).
- **The score is expression specificity, not causation.** It is a covariate for set definition and
  weighting; the causal verdict on mutation burden comes from t217 (span/selection), not from t216.
