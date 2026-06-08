---
id: "interpretation:2026-06-08-t218-cns-exclusion-wes-panel"
type: "interpretation"
title: "t218: the neural-gene enrichment is not CNS-driven (q033) and the t217 residual is not panel ascertainment — it is one high-burden WGS cohort's whole-gene-body reach over the candidates' multi-Mb CFS loci; removing it returns them to the genomic-span null, closing the mutational program"
status: "active"
related:
  - "hypothesis:h12-neural-gene-enrichment-length-histology-artifact"
  - "question:q033-neural-enrichment-cns-exclusion"
  - "question:q016-panel-induced-ascertainment"
  - "interpretation:2026-06-08-t217-genomic-span-cfs-null"
  - "interpretation:2026-06-08-t216-label-free-neural-score"
  - "task:t218"
  - "task:t219"
  - "task:t221"
created: "2026-06-08"
updated: "2026-06-08"
---

# Interpretation: t218 — CNS exclusion + WES restriction + panel-membership stratification

> **Verdict: the candidate enrichment is NOT CNS-histology-driven (q033 answered), and the small t217
> residual is NOT panel ascertainment (t217 F5 overturned). The residual lives entirely in the WES/WGS
> studies, is absent in panels, and survives span-, span+replication-timing-, CNS-, and
> hypermutator-controls — but it is driven by a SINGLE high-burden metastatic WGS cohort
> (`pog570_bcgsc_2020`). Dropping that one study returns the candidates to the genomic-span null
> (span-matched p 0.002 → 0.19). WGS sequences the full multi-Mb gene body, so these common-fragile-site
> loci accrue whole-span counts there — the genomic-span confound amplified by assay reach, not biology.
> With no surviving residual, the mutational interpretation of the neural-gene program closes on H5/CFS.**

- **Task:** `t218` (q033 CNS exclusion, P2; plan step 3).
- **Script:** `code/notebooks/t218_cns_exclusion_wes_panel.py`
- **Artifacts:** `results/neural-gene-cns-wes-2026-06-08/` (datapackage.json + 5 resources).
- **Substrate:** `gene_cancer_study.feather` (`full` 196 studies, `pan-cancer` 13); genomic span +
  constitutive-late-replication flag from `data/gene_replication_timing.feather`; `genie_panel_coverage`
  for panel membership; pan-cancer hypermutator-`_exclusive` twins for the hypermutator arm. `random_seed = 0`.
- **Assay class** is read from the substrate (genes-covered-per-study ≥ 5000 ⇒ WES/WGS, else
  panel/limited): `panel_callable_mb` is pinned to the 30 Mb WES default here and cannot discriminate.
  `full` splits 91 WES/WGS + 105 panel; `pan-cancer` 7 + 6.

## Findings

**F1 — q033 answered: the enrichment is NOT CNS-driven.** Excluding all 17 CNS/glioma cancer types
changes nothing — candidate median percentile 0.784 → 0.789, span-matched residual p 0.0062 → 0.0068.
Per-candidate CNS contribution is only **9–19 %** (CALN1 highest 18.5 %, RIT2 lowest 9.2 %); Glioma is a
consistent top-4 contributor but never leads — Melanoma, Esophagogastric, Colorectal, and NSCLC carry the
counts. The enrichment is **diffuse across high-burden epithelial cancers**, not a CNS-lineage signal.

**F2 — t217 F5 overturned: the residual is in WES/WGS, NOT in panels.** The span-matched residual is
present in the 91 WES/WGS studies (`wes_only` p = **0.0022**, candidate median 0.25 %) and **absent in
the 105 panel studies** (`panel_only` p = **0.9996**; candidates sit at the **46th** percentile — not
enriched at all). Panels tile each candidate on only **1–2 of 167** GENIE panels (0.6–1.2 %), so they
barely report these genes. t217 had guessed the residual was panel ascertainment; the opposite is true.
(pan-cancer's apparent "no residual" in t217 was its panel studies *diluting* the WES signal — restricting
pan-cancer to its 7 WES studies brings the residual back: p = 0.16.)

**F3 — The residual is not span, not replication-timing class, not CNS, not hypermutators.** It survives
a genomic-span-matched null (the t217 test), a span **+ constitutive-late-replication-class** matched null
(`p_span_class_matched` = 0.0006 in WES `full`), CNS exclusion (F1), and hypermutator-sample exclusion
(pan-cancer `wes_hypermut_excl` p = 0.16, unchanged from 0.16). And it is not positive selection (t217
dndscv: 0/9 significant). Every standard artifact is ruled out.

**F4 — …because it is one high-burden WGS cohort's whole-gene-body reach.** Leave-one-study-out over the
91 WES/WGS studies flags exactly **one** study moving candidate median by > 0.1 pct: `pog570_bcgsc_2020`,
a 570-sample metastatic **WGS** cohort. Dropping it (`wes_excl_wgs_driver`) returns the candidates to the
genomic-span null: candidate median 0.25 % → **1.06 %**, span-matched p 0.0022 → **0.19**,
span+class p 0.0006 → **0.067**. Mechanism: WES captures only exons, but WGS sequences the entire
multi-Mb gene body — for these CFS loci, whose bulk is intronic, WGS accrues counts proportional to
*genomic span*, an amplified form of the very confound t217 identified. No other study contributes a
comparable effect (next-largest |Δ| = 0.033 pct).

## Bearing on h12 — the mutational program closes

This completes the plan's decision tree for the candidate set:

```
reproduce?            yes  (t215)
length/span-normalize bulk dissolves under genomic span  -> H5 / CFS  (t217)
CNS-exclude           residual unaffected                 -> NOT H4(CNS)  (t218 F1)
residual              = one-WGS-cohort assay reach over CFS loci -> still H5/CFS, not biology  (t218 F4)
```

There is **no surviving residual** to attribute to neural biology. Combined with t216 (a label-free neural
score cannot separate effectors from size-matched CFS loci) and t217 (no positive selection; coding-length
null fails, genomic-span null succeeds), **h12 is confirmed**: the apparent neural-gene mutation enrichment
is a genomic-span / common-fragile-site artifact — diffuse across high-burden cancers, amplified in WGS by
whole-locus reach — onto which a true-but-causally-inert neural expression label was mapped.

## Decision & redirect

1. **Downgrade `t219` (NET exclusion, q034) and `t220` (oncofetal / dN/dS residual interpretation).**
   The plan gated these on a *surviving* residual after CNS exclusion; none survives. Keep `t219` only as
   a quick confirmatory NET-exclusion sanity check (MEN1 canary), not as a residual-explaining step;
   `t220` (H3 oncofetal / H1 dN/dS) is now low priority — there is nothing left to interpret mutationally.
2. **Fold the WGS-reach finding into `q016` / the assay-regime theme.** The single-WGS-cohort effect is a
   concrete instance of assay-regime confounding (WGS whole-locus vs WES exonic vs panel-tiled) for large
   genes; record it under `theme:assay-regime-confounding` and `q016`.
3. **`t221` QA** can run as standing controls (matched-normal, MSI), but its central worry — hypermutator
   inflation — is already shown not to drive the candidate signal (F3).
4. **Close the candidate-set mutational thread of `h12` as confirmed.** Any further neural-cancer work
   should pivot to non-mutational biology (the 21-paper review's conclusion), not to these genes' counts.

## Caveats

- **Single-study attribution rests on one cohort.** The WGS-reach close is driven by `pog570_bcgsc_2020`
  specifically; another WGS cohort (`pancan_pcawg_2020`, primary tumors) does *not* drive it (LOSO Δ =
  −0.009), so the effect is high-burden-metastatic-WGS-specific, not "all WGS". The mechanism (whole-locus
  reach × genomic span) is general; its magnitude here happens to ride on one cohort. This is reported, not
  smoothed over.
- **Assay class is a coverage heuristic.** Genes-covered ≥ 5000 is a clean WES/WGS cutoff (no panel tiles
  that many), but the 1000–5000 band (older/limited studies) is grouped with panels; robustness to the
  threshold was not exhaustively swept (5000 is well clear of both clusters).
- **pan-cancer WES arm is underpowered** (7 studies; residual p ≈ 0.05–0.16). The powered estimates are on
  `full`; pan-cancer is directionally consistent.
- **Neuroendocrine cancers were intentionally left in** (CNS regex excludes them) — their exclusion is
  `t219`/q034, separate from CNS histology.
