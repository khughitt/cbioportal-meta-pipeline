---
type: interpretation
title: "t218: the candidate mutation enrichment is not CNS-driven (q033) and the t217\
  \ residual is not panel ascertainment \u2014 it is one cohort's all-region (98.5%-intronic)\
  \ mutation table tiling the candidates' multi-Mb loci; removing it returns them\
  \ to the genomic-span null, closing the candidate-set mutational-count thread of\
  \ h12"
status: active
created: '2026-06-08'
updated: '2026-06-08'
id: interpretation:0042-t218-cns-exclusion-wes-panel
related:
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- question:0033-neural-enrichment-cns-exclusion
- question:0016-panel-induced-ascertainment
- interpretation:0041-t217-genomic-span-cfs-null
- interpretation:0040-t216-label-free-neural-score
- task:t218
- task:t221
---

# Interpretation: t218 — CNS exclusion + WES restriction + panel-membership stratification

> **Verdict (scoped to the candidate-set mutational-count thread of h12): the enrichment is NOT
> CNS-histology-driven (q033 answered for this thread), and the small t217 residual is NOT panel
> ascertainment (t217 F5 overturned). The residual lives in the WES/WGS-class studies, is absent in
> panels, and is driven entirely by ONE cohort (`pog570_bcgsc_2020`) whose mutation table is all-region
> — 98.5 % of its candidate variant rows are intronic. Dropping it returns the candidates to the
> genomic-span null (span-matched p 0.0022 → 0.19). That cohort carries zero hypermutator samples and
> spreads its candidate rows across 568 samples, so the residual is whole-gene-body genomic-span reach,
> not hypermutators, CNS lineage, panel ascertainment, or selection. With no surviving residual, the
> candidate-set mutational-count thread of h12 closes on H5/CFS.**

- **Task:** `t218` (q033 CNS exclusion, P2; plan step 3).
- **Scripts:** `code/notebooks/t218_cns_exclusion_wes_panel.py` (restrictions + LOSO) and
  `code/notebooks/t218b_pog570_driver_forensics.py` (driver variant-class + hypermutator forensic).
- **Artifacts:** `results/neural-gene-cns-wes-2026-06-08/` — `enrichment_by_restriction.tsv`,
  `candidate_cns_contribution.tsv`, `leave_one_study_out_wes.tsv`, `assay_classification.tsv`,
  `candidate_panel_membership.tsv`, and (t218b) `pog570_candidate_variant_class.tsv`,
  `pog570_per_candidate_region.tsv`, `pog570_driver_forensics.json`.
- **Assay class** is from genes-covered-per-study (≥ 5000 ⇒ WES/WGS-class, else panel/limited):
  `panel_callable_mb` is pinned to the 30 Mb WES default here and cannot discriminate. `full` = 91
  WES/WGS-class + 105 panel; `pan-cancer` = 7 + 6. `random_seed = 0`.

## Findings

**F1 — q033 answered (this thread): the enrichment is NOT CNS-driven.** Excluding all 17 CNS/glioma
cancer types is inert — candidate median percentile 0.784 → 0.789, span-matched residual p 0.0062 →
0.0068. Per-candidate CNS contribution is only **9–19 %** (CALN1 highest 18.5 %, RIT2 lowest 9.2 %);
Glioma is a steady top-4 contributor but never leads — Melanoma, Esophagogastric, Colorectal, NSCLC carry
the counts. The enrichment is diffuse across high-burden epithelial cancers, not a CNS-lineage signal.

**F2 — t217 F5 overturned: the residual is in the WES/WGS-class studies, NOT in panels.** Span-matched
residual p = **0.0022** in the 91 WES/WGS-class studies (candidate median 0.25 %) and **0.9996** in the
105 panel studies (candidates at the **46th** percentile — not enriched). Panels tile each candidate on
only **1–2 of 167** GENIE panels (0.6–1.2 %), so they barely report these genes. t217 had guessed panel
ascertainment; the opposite holds. (In `pan-cancer`, restricting to its 7 WES studies moves the residual
from p = 0.37 to **p = 0.16** — *directionally consistent but non-significant and underpowered at n = 7*;
the powered evidence is on `full`.)

**F3 — Not span, not replication-timing class, not CNS, and not hypermutators.** The residual survives a
genomic-span-matched null (the t217 test), a span **+ constitutive-late-replication-class** matched null
(`p_span_class_matched` = 0.0006 in WES `full`), CNS exclusion (F1), and is not positive selection (t217
dndscv 0/9). The hypermutator question needs care: the only *aggregate-level* hypermutator arm here is
pan-cancer `wes_hypermut_excl`, which tests an **already-non-significant** arm (p 0.16 → 0.16) and so
cannot bear on the *significant* full-WES residual. The decisive hypermutator evidence comes from the
driver cohort instead (F5): `pog570_bcgsc_2020` carries **0 of 570** hypermutator-flagged samples and
spreads its candidate variant rows across **568 samples** (top sample 6.5 %), so the residual it drives
cannot be a hypermutator/TMB sample-composition artifact. (A full-config *sample-level* hypermutator
re-aggregation across all 91 WES studies is not run here — the `full` aggregate lacks `_exclusive` twins;
that remains the proper job of `t221`, which we keep as a standing control rather than treating as
pre-empted.)

**F4 — The residual is one cohort's all-region mutation table.** Leave-one-study-out over the 91
WES/WGS-class studies flags exactly **one** study moving candidate median by > 0.1 pct:
`pog570_bcgsc_2020` (next-largest |Δ| = 0.033). Dropping it (`wes_excl_wgs_driver`) returns the candidates
to the genomic-span null: candidate median 0.25 % → **1.06 %**, span-matched p 0.0022 → **0.19**,
span+class p 0.0006 → **0.067**.

**F5 — …because that cohort's table is whole-gene-body, not exonic (variant-class forensic).** Direct
inspection of pog570's per-variant table (`mut_filtered.feather`, 3.29 M rows;
`pog570_candidate_variant_class.tsv`): **98.5 %** of the 44,641 candidate variant rows are **intronic**
(per-gene 94.5–99.6 %), versus **26** coding-nonsynonymous rows total. The study as a whole is 85 %
intronic. So although `data/study_panels.tsv` labels pog570 **`wes`**, its mutation table is effectively
**all-region / whole-genome-like**: mutation counts for these multi-Mb loci scale with *genomic span*
(intronic territory), which is exactly the t217 genomic-span confound amplified by the table's region
coverage — independent of the assay label. The effect is a property of this cohort's call set, not of
sequencing chemistry, so we describe it as "all-region / whole-gene-body reach," not "WGS".

## Bearing on h12 — the candidate-set mutational-count thread closes

For the candidate set, the plan's decision tree terminates:

```
reproduce?            yes  (t215)
span-normalize        bulk dissolves under genomic span        -> H5 / CFS     (t217)
CNS-exclude           residual unaffected                       -> NOT H4(CNS)  (t218 F1)
residual              = one cohort's all-region (intronic) table -> still H5/CFS, not biology  (t218 F4/F5)
```

Combined with t216 (a label-free neural score cannot separate effectors from size-matched CFS loci) and
t217 (no positive selection; coding-length null fails, genomic-span null succeeds), **the candidate-set
mutational-count thread of `h12` is confirmed**. This is one thread of h12, not the whole hypothesis: the
project entities `hypothesis:0012` (proposed) and `question:0033` (active) are intentionally left in their
prior states — a single mutational-count thread does not by itself flip the hypothesis to *confirmed*; it
is recorded here as strong supporting evidence with the residual explained. Other h12 threads
(e.g. expression/histology beyond mutation counts) are out of scope for t218.

## Decision & redirect

1. **Downgrade `t219` (NET exclusion, q034) and `t220` (oncofetal / dN/dS residual interpretation).** The
   plan gated these on a *surviving* residual after CNS exclusion; none survives for the candidate set.
   Keep `t219` only as a quick MEN1-canary NET-exclusion sanity check; `t220` is now low priority.
2. **Keep `t221` for the proper sample-level hypermutator control.** F3's hypermutator evidence is driver-
   cohort-specific (pog570 has zero hypermutators); a full-config sample-level hypermutator re-aggregation
   across all 91 WES studies is still the clean general check and is `t221`'s job — not pre-empted here.
3. **Fold the all-region-table finding into `q016` / `theme:0001-assay-regime-panel-wes-wgs-as-a-master-technical-confounder-spanning`.** A cohort whose
   call set includes intronic/all-region variants inflates large-gene counts proportional to genomic span;
   this is a concrete assay-regime / call-set-scope confound for large genes, distinct from panel tiling.

## Caveats

- **Single-cohort attribution.** The close rests on `pog570_bcgsc_2020` specifically; another large-call-
  set cohort (`pancan_pcawg_2020`) does *not* drive it (LOSO Δ = −0.009), so the magnitude here rides on
  one cohort even though the mechanism (all-region reach × genomic span) is general. Reported, not smoothed.
- **`wes`-labelled but all-region.** `study_panels.tsv` labels pog570 `wes`; its mutation table is 85 %
  intronic. We therefore attribute the effect to the **call-set region content** (F5), not to a WES/WGS
  label, which would be unreliable here.
- **pan-cancer WES arm is underpowered** (7 studies; residual p ≈ 0.05–0.16, non-significant). The powered
  estimates are on `full`; pan-cancer is directionally consistent only.
- **Aggregate vs sample-level hypermutator control.** The hypermutator evidence is the driver cohort's
  zero-hypermutator composition (F3/F5), not a full-config sample-level exclusion — that is `t221`.
- **Neuroendocrine cancers intentionally retained** (CNS regex excludes them); their exclusion is `t219`/
  q034, separate from CNS histology.
