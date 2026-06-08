---
id: "interpretation:2026-06-08-t217-genomic-span-cfs-null"
type: "interpretation"
title: "t217: neural-gene mutation enrichment is a genomic-span / common-fragile-site artifact — it survives a coding-length null but dissolves under genomic-span normalization; a small residual remains only in the panel-heavy full config (panel ascertainment, not biology)"
status: "active"
related:
  - "hypothesis:h12-neural-gene-enrichment-length-histology-artifact"
  - "hypothesis:h03-gene-length-confounds-literature-attention"
  - "question:q032-neural-gene-length-null"
  - "question:q016-panel-induced-ascertainment"
  - "interpretation:2026-06-08-t215-neural-gene-reproduction-gate"
  - "task:t217"
  - "task:t218"
  - "task:t221"
created: "2026-06-08"
updated: "2026-06-08"
---

# Interpretation: t217 — genomic-span / common-fragile-site null test

> **Verdict: the candidate "neural-gene" mutation enrichment is overwhelmingly a genomic-span /
> common-fragile-site (CFS) artifact, NOT a coding-length one.** Normalizing to coding target size
> (mutations-per-CDS-kb) does **not** dissolve the enrichment — it makes it more extreme, because the
> candidates are *short* proteins. Normalizing to genomic locus size (mutations-per-genomic-kb)
> **dissolves and inverts** it: the candidates fall from the 0.8th to the 82.6th percentile. A
> tightly span-matched empirical null leaves a **small residual only in the panel-heavy `full` config
> (p = 0.006)** and **none in the clean WES `pan-cancer` config (p = 0.38)** — the residual points to
> **panel ascertainment (q016)**, not neural biology. dndscv finds **zero** of the 9 under positive
> selection in any of 68 cancers.
>
> **Correction (2026-06-08, by t218):** the F5 "panel ascertainment" attribution below is **WRONG**.
> t218 shows the residual lives in the **WES/WGS-class** studies and is *absent* in panels (which barely
> tile these genes); pan-cancer's "no residual" was its panel studies diluting the WES signal. The
> residual is driven entirely by **one cohort** (`pog570_bcgsc_2020`) whose mutation table is all-region —
> **98.5 % of its candidate variant rows are intronic** — so counts for these multi-Mb loci scale with
> genomic span (the same confound, amplified by call-set region coverage, not by panel ascertainment or
> CNS histology). That cohort carries zero hypermutator samples. The F2/F3/F4 genomic-span conclusions
> below are unchanged and strengthened. See `interpretation:2026-06-08-t218-cns-exclusion-wes-panel`.

- **Task:** `t217` (q032 length null, P1; plan step 3,
  `doc/plans/2026-06-06-neural-gene-enrichment-meta-analysis-plan.md`).
- **Script:** `code/notebooks/t217_genomic_span_cfs_null.py`
- **Artifacts:** `results/neural-gene-span-null-2026-06-08/` (datapackage.json + 5 resources).
- **Builds on:** the t215 gate (`interpretation:2026-06-08-t215-neural-gene-reproduction-gate`), whose
  F4/F5 redirected the length test from protein-aa length to **genomic / CDS span + CFS**.
- **Substrate:** `gene_cancer_study.feather` for `full` (196 inclusive studies) and `pan-cancer` (13);
  genomic span + replication timing from the version-controlled `data/gene_replication_timing.feather`
  (`end − start`, protein-coding); coding target ≈ `(protein_aa + 1) × 3` from
  `data/uniprotkb_hsapiens_protein_lengths.tsv.gz`; positive selection from the pan-cancer
  `dndscv_pooled.feather` (`min_qglobal` over 68 cancers). `random_seed = 0`.

## What was tested

The t215 gate established a real high-tail mutation enrichment of the 9 candidates but predicted the
**dissolving covariate is genomic span / CFS, not amino-acid length** (the candidates are short
proteins yet huge genomic loci). t217 runs that test as a **two-armed contrast** plus three
confirmatory arms:

- **Arm A — coding-length null** (`per_cds_kb`): mutations ÷ coding target size. If the enrichment is
  the classic "long-gene accumulates more passengers" length effect, this should remove it.
- **Arm B — genomic-span / CFS null** (`per_genomic_kb`): mutations ÷ gene-body span. If the
  enrichment is a large-locus / fragile-site effect, this should remove it.
- **Span Wilcoxon:** is candidate genomic span itself elevated vs background? (the positive confound).
- **dndscv:** are any candidates under positive selection (driver-like), or passenger-like?
- **Span-matched empirical null (k-NN on log-span):** beyond the deterministic ÷span, is the candidate
  raw-count enrichment exceptional vs random genes of *the same size*? Each candidate is matched to its
  200 nearest genes by |Δlog₁₀ span| (median caliper 0.28 dex ≈ within ~2×), candidates excluded from
  pools; 5,000 draws.

## Findings

**F1 — A coding-length null does NOT dissolve the enrichment; it amplifies it.** In `full`, the
candidate median percentile goes from **0.78 %** on raw count (MWU p = 2.1e-7) to **0.067 %** on
mutations-per-CDS-kb, with **9/9 in the top 100** and hypergeometric p = **1.8e-21**. Because the
candidates are short proteins (CDS ≈ 0.4–1.2 kb), dividing by coding target makes their per-kb rate
extraordinary. **The literal `q032` wording — a protein/CDS-length Wilcoxon — would have *failed to
reject* in the wrong direction.** This is the quantitative confirmation of t215 F4: protein length is
the wrong yardstick.

**F2 — A genomic-span / CFS null dissolves and inverts the enrichment.** In `full`, the candidate
median percentile moves from 0.78 % (raw) to **82.6 %** on mutations-per-genomic-kb (MWU p ≈ 1.0,
**0/9** in the top 100); in `pan-cancer`, to **98.9 %**. Once mutation count is expressed per unit of
genomic locus, the candidates are **below-median**, not enriched. The confound is locus size.

**F3 — The candidates are top-1 % genomic loci (the positive confound), though mid-pack proteins.**
Candidate median genomic span is **1,117 kb vs a 25 kb genome median — the 99.4th percentile**
(one-sided MWU p = 1.4e-7). **6/9 are constitutively late-replicating** (`rt_constitutive_label = CL`,
`rt_cl_fraction = 1.0`: NKAIN2, KCNIP4, RBFOX1, LSAMP, SGCZ, OPCML), the textbook CFS signature, and
2/9 (RBFOX1, LSAMP) are in the curated canonical-CFS list. By contrast the canonical neural
**effectors** sit at only the **74th** span percentile (median 67 kb) — they are *longer proteins* but
*smaller loci*, which is exactly why they rank lower in raw mutation count and why a length model
mislabels the situation.

**F4 — No positive selection.** Across 68 cancers, **0/9 candidates are dndscv-significant** at q ≤ 0.05
in *any* cancer (`min_qglobal` 0.064–0.835; NKAIN2 lowest at 0.064, still NS). This is the passenger /
structural-instability fingerprint expected of CFS loci, not driver selection — it removes the
mutational-H1 ("selected neural hijacking") reading for these genes.

**F5 — Span explains the bulk; a small residual survives only in the panel-heavy config.** Under tight
k-NN span matching, a *random gene of the same size* already sits at the ~98th raw-count percentile
(`full` null median 2.06 %), so genomic span alone accounts for almost the entire enrichment. The
candidates sit slightly higher still: in **`full`** the span-matched empirical **p = 0.006** (a small
real residual above span); in **`pan-cancer`** the **p = 0.38** (span fully accounts for it). The
residual's *direction across configs is diagnostic*: it appears in the **196-study, panel-rich `full`**
set and **vanishes in the 13-study WES/WGS `pan-cancer`** set. Real neural selection would survive
*better* in the cleaner WES data, not worse — so the residual is most consistent with **panel
ascertainment** (large neural genes such as RBFOX1/LSAMP are disproportionately tiled by targeted
panels), i.e. `q016`, not biology.

## Bearing on h12

This is strong confirmatory evidence for **h12** ("apparent neural-gene enrichment is a
length/histology artifact"), with the mechanism now pinned: **genomic span / common-fragile-site
instability + multi-study (panel) pooling**, *not* coding length and *not* selection. On the plan's
decision tree (`length-normalize → signal gone → H5 confirmed`), the **genomic-span** branch of H5 is
confirmed as the dominant explanation; the residual is small, config-dependent, and points downstream
to panel ascertainment rather than to a neural mechanism. It also supports `h03` (gene-size confounds
attention) at the genomic-span, not protein-length, granularity.

## Decision & redirect

1. **`q032` answered (genomic-span form): the enrichment does not survive locus-size normalization.**
   Record the answer at the *genomic-span* granularity and note explicitly that the protein/CDS-length
   form of the question is the wrong test (Arm A).
2. **Carry the small `full`-only residual to `t218` (CNS exclusion, q033) and `q016` (panel
   ascertainment), not to neural biology.** Because the residual is absent in WES `pan-cancer`, the
   first test is whether it is panel-driven: re-run the span-matched null restricted to WES studies and
   on a panel-membership-stratified basis. CNS exclusion (`t218`) remains warranted as the histology
   control but is now a second-order check.
3. **`t221` QA:** fold the late-replication / CFS label and the span-matched null into the QA battery as
   standing controls; promote `is_late_cl` to a routine covariate alongside `is_hypermutator`.
4. **`t216` label-free score (next):** benchmark against a **span/late-replication-matched CFS null**,
   per the t215 redirect — F5 shows a same-size random locus is already at the 98th mutation
   percentile, so any neural score must beat a size-matched control to mean anything.

## Caveats

- **Coding target is a proxy.** `per_cds_kb` uses `(aa + 1) × 3` from UniProt rather than summed-exon
  CDS from a GTF. The conclusion is robust to this (the point is only that the candidates are *short*;
  a true CDS length would be smaller still for intron-heavy genes, strengthening F1), but a GTF-summed
  CDS is the clean follow-up if a reviewer presses Arm A.
- **Raw counts are not panel-callable-territory normalized.** `per_genomic_kb` divides by full
  gene-body span; in panel studies only exonic territory is sequenced, so the *true* per-callable rate
  differs. This is exactly the `q016` coupling and is why the `full`-only residual is most plausibly
  ascertainment. The qualitative two-arm contrast (F1 vs F2) does not depend on it.
- **Span-matched null is on raw count.** It asks "is the candidate raw enrichment exceptional vs
  same-size genes"; the deterministic ÷span result (F2) is the complementary "is the per-kb rate
  elevated" view. Both agree: span carries the enrichment.
- **CFS operationalization.** The workhorse is the in-repo constitutive-late-replication label; the
  curated canonical-CFS list is for cross-validation only and is deliberately small (2/9 hits) — late
  replication is the more sensitive, less arbitrary CFS proxy here.
