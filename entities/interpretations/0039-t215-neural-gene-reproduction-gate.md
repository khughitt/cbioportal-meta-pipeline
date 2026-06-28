---
type: interpretation
title: "t215: neural-gene mutation-enrichment partially reproduces \u2014 real top-1%\
  \ non-driver enrichment, but a large-locus/CFS class effect, not a neural-specific\
  \ or protein-length one"
status: active
created: '2026-06-08'
updated: '2026-06-08'
id: interpretation:0039-t215-neural-gene-reproduction-gate
source_refs:
- paper:Lu2026
related:
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- question:0032-neural-gene-length-null
- question:0033-neural-enrichment-cns-exclusion
- question:0035-label-free-neural-gene-definition
- task:t215
- task:t217
- task:t216
- task:t221
---

# Interpretation: t215 — neural-gene mutation-enrichment reproduction gate

> **Gate verdict: PARTIAL REPRODUCTION → PROCEED (do not close the program).**
> The 9 candidate neural genes are real and strongly enriched in the high tail of the mutation
> distribution, so there *is* something to explain. But they do **not** literally "top a
> mutation-frequency view" (canonical drivers and long passengers dominate every sensible ranking),
> and the co-top genes are a broad **large-locus / common-fragile-site** class that is only partly
> neural. The decisive correction is therefore **genomic-span / CFS**, not protein length — the
> candidate proteins are *short*.
>
> **Corrected 2026-06-08 after code review** (5 findings): the original run summed pooled-summary
> and metadata columns (`mean`, `mean_adj`; and for `pan-cancer` the `_exclusive` twins + `n_*` /
> `callable_*` columns) as if they were studies, contaminating every metric. With true inclusive
> study columns only (**full 196, pan-cancer 13, 10k 7**), the headline gate verdict is unchanged,
> but the config story is corrected: the high-tail enrichment is **robust across all three configs**
> (Mann–Whitney p < 1e-5 everywhere); only the *extreme top-100 raw-count occupancy* is
> config-dependent. The set-enrichment p-values are **descriptive reproduction statistics**, not
> independent discovery evidence (the candidate list came from prior, related views).

- **Task:** `t215` (gate step of the neural-gene meta-analysis plan,
  `doc/plans/2026-06-06-neural-gene-enrichment-meta-analysis-plan.md`).
- **Script:** `code/notebooks/t215_neural_gene_reproduction_gate.py`
- **Artifacts:** `results/neural-gene-reproduction-2026-06-08/` (datapackage.json + 5 resources).
- **Substrate:** existing pipeline aggregates `gene_cancer_study.feather` /
  `gene_cancer_study_ratio.feather` for configs `full` (196 inclusive studies), `pan-cancer` (13),
  `10k` (7). These are the **unannotated** aggregates; the annotated `full`/`10k` feathers named in
  the task text are not present under `/data/packages` (annotation adds overlay columns, not counts,
  so it does not affect this gate). Inclusive `{study}` columns only — pooled-summary, `_exclusive`,
  and `n_*`/`callable_*` metadata columns are excluded (`study_columns()`).
- **Candidate set:** NKAIN2, KCNIP4, TAFA2 (carried as alias **FAM19A2**), RIT2, CALN1, RBFOX1,
  LSAMP, SGCZ, OPCML. **Positive control:** canonical cancer-neuroscience effectors (NLGN3, ADRB2,
  NTRK1/2, CHRM3, GRIN2A/B, NGF, BDNF).

## What was tested

The motivating "neural genes top a mutation-frequency view" claim came from **unreliable notes**.
The gate reproduces it from the pipeline and asks: on which metric, in which config, from which
studies, and is the candidate *set* enriched beyond chance? Three per-gene metrics were ranked over
~21,000 genes: raw total mutation count, mean sample-ratio (≥20-stratum filter to suppress
tiny-cohort lincRNA artifacts), and raw count among **non-driver** genes (Bailey et al. [@Bailey2018] ∪ COSMIC CGC
removed). Set enrichment was scored by one-sided Mann–Whitney (candidate ranks vs all genes) and a
top-100 hypergeometric test.

## Findings

**F1 — The candidates do not literally top any sensible view.** In `full`, raw-count is dominated
by canonical drivers + long passengers (TP53, KRAS, APC, PIK3CA, KMT2D, LRP1B, TTN, ARID1A …); the
best candidate is RBFOX1 at rank 47/~21,000. The unfiltered mean-ratio top is small-cohort
lincRNA/antisense noise (hence the ≥20-stratum filter); max-ratio is degenerate (≈1.0 for thousands
of genes). The literal notes claim — these 9 genes *topping* a view — is **not reproduced**.

**F2 — But the candidate set is strongly, significantly enriched in the high tail.** In `full`,
median candidate percentile is 0.78 % on raw count (MWU p = 2.1e-7) and **0.27 %** on non-driver
raw count, with **6/9 in the top 100** non-driver genes; `10k` reaches 7/9. So the enrichment is
real — the notes are **not spurious**. *Framing:* because the candidate list was lifted from prior
notes likely derived from these same/related mutation views, these are **descriptive reproduction
statistics**, not independent discovery p-values; the small hypergeometric/MWU tail probabilities
quantify "the set sits unusually high", not "the set was discovered at significance p".

**F3 — The high-tail enrichment is robust across configs; only the extreme top-100 occupancy is
config-dependent.** The candidate set's MWU enrichment is significant in **all three** configs and
**both** metric families (every p < 1e-5): e.g. `pan-cancer` raw count median pct 4.4 %
(MWU p = 1.3e-6), `pan-cancer` non-driver raw count median pct 2.1 % (p = 3.8e-7). What differs is
the *extreme* top-100 raw-count occupancy: `full`/`10k` place 2–7 candidates in the raw-count
top-100, `pan-cancer` places 0 (its 13 large WES/WGS/panel studies rank the same genes near the top
few % rather than the top 100). If anything the **mean-ratio enrichment is strongest in
`pan-cancer`** (7/9 in the top 100; LSAMP #18, RBFOX1 #20, KCNIP4 #30). So the earlier
"vanishes in pan-cancer" read was an artifact of the column bug; the corrected reading is that the
*direction* is invariant and only the top-100 raw-count tail is pool-sensitive — still worth
carrying forward (couples to `question:0016-panel-induced-ascertainment`), but it is **not** a presence/absence flip.

**F4 — Protein length does NOT explain it; the candidates are short proteins.** All 9 candidates now
resolve (FAM19A2 via its primary symbol TAFA2 = 131 aa): candidate lengths are 131–397 aa
(percentiles **8–47 %**, *below* the 417 aa genome median). The canonical neural **effectors are far
longer** (NLGN3 848, NTRK2 822, GRIN2A/B ≈1470 aa; pct 81–95 %) yet rank much lower in mutation
count (median pct 2.6–30 %, mostly outside the top 100). A protein-length null (the literal wording
of `q032`/`t217`) would therefore **under-correct**. The operative covariate is **genomic / CDS span
and common-fragile-site (CFS) status**, not amino-acid length: the candidates (NKAIN2, RBFOX1, LSAMP,
OPCML, SGCZ, CALN1) are textbook *large genomic loci / CFS* genes with small coding sequences.

**F5 — The co-top genes are a large-locus/CFS class, only partly neural.** The non-driver top-20
(`full`) is TTN, CSMD1, EYS, NOTCH3, SYNE1, PCDH15, **RBFOX1**, PRKDC, RYR2, EPHA5, DLG2, PARK2,
DPP10, **LSAMP**, USH2A, MAGI2, LRRC4C, CTNNA3, FLT1, EPHB1 (and in `10k`: CSMD1, EYS, **RBFOX1**,
PCDH15, **LSAMP**, DLG2, LRRC4C, … NRXN1/3, MACROD2, CADM2). The candidates sit *among* these but
are **not distinguished** from non-neural large loci (EYS = retina, USH2A = Usher, RYR2 = cardiac,
TTN = muscle, SYNE1 = nuclear envelope, MACROD2/PARK2/FHIT-class = CFS). "Neural" is largely a
**post-hoc label on a length/CFS-driven non-driver set**.

**F6 — Contributing cancer types are high-TMB / large-cohort, not CNS-dominant.** Per-candidate raw
counts spread across Melanoma, Esophagogastric, Colorectal, NSCLC, Breast, with Glioma present but
rarely leading (Melanoma usually first). This is a burden×cohort-size fingerprint, not a CNS-lineage
one — though the CNS-exclusion test (`t218`/`question:0033-neural-enrichment-cns-exclusion`) is still warranted because Glioma is a
consistent top-5 contributor.

## Bearing on `hypothesis:0012-neural-gene-enrichment-length-histology-artifact`

This is direct early support for `hypothesis:0012-neural-gene-enrichment-length-histology-artifact`
("apparent neural-gene enrichment is a length/histology artifact"), and it sharpens the mechanism: the artifact is **genomic-span / common-fragile-site +
multi-study pooling**, not protein length and not (primarily) CNS histology. It does **not** confirm
the hypothesis — that requires the normalized tests — but it confirms there is a genuine enrichment to dissolve
and predicts the dissolving covariate.

## Decision & redirect for the program

**Proceed to the correction tests.** The gate passes the "is there something to explain?" bar (F2),
so the 11-task program is **not** closed. But three plan adjustments follow from the gate:

1. **`t217` (`question:0032-neural-gene-length-null`, P1) must normalize by genomic/CDS callable territory and add the CFS overlay,
   not protein-aa length.** F4 shows protein length is the wrong yardstick; an aa-length Wilcoxon
   would spuriously *fail to reject* (candidates look short). Use mutations-per-callable-kb on the
   transcribed/CDS footprint + the dndscv background, and fold in `t221`'s CFS overlap as a primary
   covariate rather than a side QA check.
2. **`t216` (`question:0035-label-free-neural-gene-definition`) label-free neural score must be benchmarked against a large-locus/CFS null**, not
   only against housekeeping negatives — F5 shows the top non-driver genes are a neural∪non-neural
   large-locus mixture, so a neural score will look "enriched" unless it beats a size-matched CFS
   control set.
3. **Carry the config contrast forward (as a tail-sensitivity, not a flip).** F3 (corrected) shows
   the enrichment direction is invariant across configs; only the extreme top-100 raw-count tail is
   pool-sensitive. Still report downstream statistics on `full` *and* `pan-cancer` (or per-study
   leave-one-out) so the tail-sensitivity and `question:0016-panel-induced-ascertainment` coupling are visible — but
   do not frame pan-cancer as "no signal."

The expected end-state (per the plan's decision tree) remains **the length + CFS account explains the
bulk**, with at most a small residual — F4–F5 make the length/CFS branch the leading explanation
before any neural biology is entertained.

## Caveats

- **Column-selection bug found in review (now fixed).** The first run summed pooled-summary
  (`mean`, `mean_adj`) and — for `pan-cancer` — `_exclusive` twins and `n_*`/`callable_*` metadata
  columns as if they were studies. This inflated `total_count`/`n_strata`, corrupted the `pan-cancer`
  mean-ratio entirely, and produced the spurious "pan-cancer not enriched" read. The corrected
  `study_columns()` selector keeps only inclusive `{study}` columns (full 196, pan-cancer 13, 10k 7);
  all numbers above are post-fix. The headline verdict (partial reproduction → proceed) was
  unchanged, but F2/F3 ranks and top-100 counts moved.
- **Selection non-independence.** The candidate list came from prior notes likely derived from
  related mutation views, so the enrichment p-values are descriptive reproduction statistics, not
  independent discovery evidence (see F2). The "real signal to explain" conclusion does not rest on
  treating any p-value as confirmatory.
- "Raw count" here is the pipeline's per-(cancer,study) mutation tally summed to gene level; it is
  not callable-territory-normalized (that is exactly `t217`'s job).
- The candidate protein lengths are resolved alias-aware (FAM19A2 ← primary TAFA2 = 131 aa); all 9
  candidates and 9 effectors resolved. A full HGNC alias-mapping (`t082`) is still worth applying
  before the formal `t217` statistic so co-top symbols are not under-counted under legacy aliases.
- The mean-ratio metric is a coarse pooled proxy (no per-stratum denominators in these aggregates);
  the canonical pooled ratio lives in the annotated `mean_inclusive` column. This does not affect
  the raw-count conclusions (F1–F2, F5).
