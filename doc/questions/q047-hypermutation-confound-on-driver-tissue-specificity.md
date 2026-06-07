---
id: "question:q047-hypermutation-confound-on-driver-tissue-specificity"
type: "question"
title: "Are cell-type-restricted lineage drivers depleted, and broad/pan-cancer drivers plus passengers enriched, among hypermutated samples — confounding any driver tissue-specificity test?"
status: "active"
ontology_terms:
  - hypermutation
  - tumor mutational burden
  - driver gene
  - passenger mutation
  - tissue specificity
datasets:
  - "metadata/samples_annotated.feather (is_hypermutator, hypermutation_score, reason, TMB, cancer type)"
  - "gene_cancer_study.feather (per-gene per-cancer mutation counts, hypermutator-stratifiable)"
  - "data/cosmic_cgc.tsv (Role in Cancer — OG/TSG/lineage)"
  - "data/uniprotkb_hsapiens_protein_lengths.tsv.gz (length control)"
source_refs:
  - "paper:MartinezJimenez2020"
related:
  - "question:q042-driver-normal-expression-tissue-cell-type-specificity"
  - "question:q043-driver-cancer-type-breadth-distribution"
  - "topic:tumor-mutational-burden"
  - "topic:lineage-addiction-and-cell-of-origin-driver-specificity"
  - "hypothesis:h03-gene-length-confounds-literature-attention"
  - "interpretation:2026-06-07-q047-hypermutation-specificity-confound"
created: "2026-06-07"
updated: "2026-06-07"
---

# Are cell-type-restricted lineage drivers depleted, and broad/pan-cancer drivers plus passengers enriched, among hypermutated samples — confounding any driver tissue-specificity test?

## First-pass result (2026-06-07, poc-2026-04-17 cohort)

**Partial.** The **breadth-inflation arm is confirmed**: excluding hypermutators raises the
restricted-driver fraction 52%→60% and **232 drivers lose ≥1 cancer-type of breadth** — so q042/q043
must stratify on `is_hypermutator`. The **per-sample dilution arm is under-identified on panel data**:
the MSK-IMPACT panel is driver-enriched, so driver-share of load barely drops in hypermutators
(0.94→0.88 UCEC); and the per-gene prevalence-ratio metric is baseline-confounded (broad oncogenes
inflate *least* — a ceiling artifact, not dilution). Only Melanoma + Endometrial were testable, and
**CRC was under-flagged** as hypermutator (a flag-audit follow-up). Refinements: WES cohort,
prevalence-matched metric, hypermutator-flag audit. See
`interpretation:2026-06-07-q047-hypermutation-specificity-confound`;
`code/notebooks/q047_hypermutation_specificity_confound.py`.

## Summary

Hypermutated tumors (MMR-deficient / MSI-H, POLE/POLD1-mutant) carry **orders of magnitude more
mutations**, most of them passengers. This both *creates a confound* for q042/q043 and *is an
interesting result in its own right*: are the **cell-type-restricted lineage drivers** (q042's route-1
oncogenes — MITF, AR, NKX2-1, IRF4-context) **under-represented** among hypermutators, while
**broad/pan-cancer drivers and passenger noise** are **enriched**? If hypermutators contribute mostly
breadth-inflating passenger recurrence, then any "restricted-oncogene Tau enrichment" (q042) or
breadth distribution (q043) computed without stratifying on `is_hypermutator` is biased.

## Why It Matters

- **Sharpens q042's null.** q042 already says the artifact reading is warranted only if the effect
  vanishes within the restricted-oncogene subset. Hypermutation is a concrete mechanism that could
  *manufacture* spurious breadth/low-specificity in the pooled set — this question quantifies it so
  q042 can stratify rather than guess.
- **De-biases q043.** Breadth (cancer-type count per driver) is mechanically inflated by hypermutators
  (a gene looks "broadly mutated" because MMR/POLE samples recur it everywhere). q043 needs an
  `is_hypermutator`-excluded parallel view; this question supplies the rationale and the magnitude.
- **Standalone biology:** whether lineage-identity selection is *diluted* under hypermutation (the
  cell still depends on its lineage driver, but the signal drowns in passenger load) speaks to how
  selection reads out against a high mutational background.
- Risk if unasked: q042/q043 silently pool hypermutators and over-state driver breadth / under-state
  restricted-oncogene specificity.

## What we can compute (substrate on disk — fully today)

- **Have:** `samples_annotated.feather` (`is_hypermutator`, `hypermutation_score`, the 8-category
  `hypermutator_reason`, TMB, the absolute/ultra/relative views); `gene_cancer_study.feather`
  (per-gene per-cancer counts, stratifiable by joining sample-level hypermutator status);
  `data/cosmic_cgc.tsv` roles. **No external ingest needed.**
- **Test:** for each driver class (restricted-oncogene / broad-oncogene / TSG / passenger-matched
  background), compare recurrence and apparent cancer-type breadth in `is_hypermutator` vs
  non-hypermutator samples, within cancer type; quantify how much breadth (q043) and pooled specificity
  (q042) shift when hypermutators are excluded.

## Confounds that decide interpretability

- **Cancer-type composition.** Hypermutators concentrate in specific types (colorectal, endometrial,
  glioma-treated); always stratify within type so the effect is not just "MSI-rich cancer types differ."
- **Reason heterogeneity.** MSI-H vs POLE vs ultra differ in spectrum; use `hypermutator_reason`, do
  not pool all hypermutators as one class.
- **Gene length (`h03`).** Long genes accrue the most passenger inflation under hypermutation —
  length-matched background is essential to separate "passenger noise" from "broad driver."
- **Selection still operates in hypermutators.** Drivers are not absent in MMR/POLE tumors; the claim
  is *relative dilution of the restricted-lineage signal*, not absence. Avoid over-reading depletion.

## Predictions

- Restricted lineage-oncogene recurrence is **diluted** (lower relative signal) among hypermutators;
  apparent breadth of many genes is **inflated** by hypermutator passenger recurrence.
- Excluding hypermutators **sharpens** q043's restricted tail and **strengthens** q042's
  restricted-oncogene specificity contrast (the artifact-removal direction).
- Broad/pan-cancer drivers (q043 hubs) are comparatively **robust** to hypermutator exclusion.

## Stop / null conditions

- If breadth (q043) and pooled specificity (q042) are **unchanged** by hypermutator exclusion, then
  hypermutation is not a material confound at our cohort's composition → q042/q043 can pool, and this
  question closes as a negative control (still useful).

## Connections to Project

- **De-biases:** `q042` (restricted-oncogene Tau null), `q043` (breadth distribution — supplies its
  hypermutator-excluded view).
- **Infrastructure:** `topic:tumor-mutational-burden` (the t081 hypermutator pipeline — `is_hypermutator`,
  reasons, the absolute/ultra/relative views), `h03` (length null).
- **Priority:** **P2** — fully computable today off `samples_annotated.feather`; the cheapest
  confound-quantification in the batch and a direct input to q042/q043. Natural to run alongside q043.
