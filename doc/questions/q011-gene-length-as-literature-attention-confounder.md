---
id: "question:q011-gene-length-as-literature-attention-confounder"
type: "question"
title: "Does gene length confound literature attention independently of mutation count?"
status: "active"
ontology_terms: []
datasets:
  - "PubTator gene mentions (/data/proj/lit-explore/pubtator/2026-01-16/counts/gene_concept_ids.feather)"
  - "UniProt H. sapiens protein lengths"
  - "cBioPortal gene_cancer_study_ratio_annotated.feather"
  - "COSMIC Cancer Gene Census / Bailey 2018 299-driver list"
source_refs:
  - "paper:Lawrence2014"
  - "paper:Bailey2018"
related:
  - "topic:mutation-rate-normalization"
  - "discussion:2026-04-24-gene-length-bias-in-mutation-rankings-and-literature"
  - "question:q003-replication-timing-as-gene-level-mutation-rate-confounder"
created: "2026-04-24"
updated: "2026-04-24"
---

# Does gene length confound literature attention independently of mutation count?

## Summary

Gene length is a well-known confounder for mutation-count-based rankings (Lawrence 2014:
TTN, MUC16, OBSCN, RYR2, LRP1B all appear as false-positive "drivers" without length
correction). The question here is whether gene length *also* drives literature attention —
PubMed mention count per gene — through channels that are partly mediated by mutation count
and partly independent (antibody availability, PPI degree, annotation density, structural
features). If so, "well-studied" and "highly mutated" share a common cause and are not
independent corroboration of biological importance.

## Why It Matters

- **Methodological:** the project's pipeline uses Bailey 2018 driver flags and PubMed-derived
  literature priors (implicitly, via citations in interpretations). If length confounds both
  axes, those priors are not independent of the mutation evidence.
- **Discovery framing:** ranking genes by "consensus across mutation frequency and literature
  attention" amplifies the length bias rather than canceling it out.
- **Novelty:** Stoeger & Nunes Amaral 2018 (*PLOS Biology*) showed that chemical / experimental
  accessibility features predict gene-level publication count more strongly than biological
  importance, but they did not isolate the length slope in a cancer-specific cohort. A
  cancer-focused replication using PubTator + cBioPortal is feasible and as far as we know
  unpublished.

## Current Evidence

- Lawrence 2014 quantifies the mutation-side length effect; long genes occupy top-N raw
  frequency lists they do not deserve. (Direct evidence for the mediated channel.)
- Stoeger 2018: gene popularity in PubMed is dominated by accessibility features, not
  biological importance. Gene / transcript length is one of those features. (Direct evidence
  that length-on-publications is real outside of cancer.)
- Edwards 2011 ("Too many roads not taken") and Haynes 2018: rich-get-richer dynamics in
  publication rates. Prior publications predict future publications more than biology does.
- BioGRID / STRING-derived analyses: PPI degree correlates with protein length and
  with publication count — an independent length → attention channel.
- No cancer-specific quantification of the length-on-PubMed slope exists in our literature
  catalogue.

## Thoughts

- The mediated channel (length → mutation count → top-N list inclusion → citation) is almost
  certainly real and large. The interesting question is the *partial* coefficient: how much
  of length's effect on literature attention survives after controlling for mutation count?
- If the partial coefficient is ~zero, length is purely a mediator and our interpretation
  of "well-studied" only needs to be hedged for genes that are length-inflated in mutation
  rankings.
- If the partial coefficient is non-trivial, length is a genuine *confounder* of the
  attention axis on its own (via antibodies, PPIs, annotation surface area, etc.). That has
  broader methodological implications and would justify a length-residualized "attention
  prior" in any future scoring scheme.
- Priority: medium. Cheap to do; conceptually load-bearing for how we report rankings.

## Proposed Analysis

1. Load PubTator gene-mention counts for protein-coding human genes, 2010-2024 window.
   Filter to species:human and primary research articles where possible.
2. Join to UniProt canonical protein length and to per-gene aggregate cBioPortal mutation
   count (sum of per-study counts, before any length normalization).
3. Fit `log(mention_count + 1) ~ log(protein_length) + log(mutation_count + 1)`,
   restricted to protein-coding genes with both PubTator and UniProt entries.
4. Report:
   - Marginal slope of `log(protein_length)` (length-only model).
   - Partial slope of `log(protein_length)` after adjusting for `log(mutation_count)`.
   - Bootstrap CIs.
   - Subgroup analysis: same regression on (a) Bailey 299 drivers, (b) Bailey-excluded
     genes. If the length slope differs across these subgroups, that is informative about
     whether length is more confounding for "background" genes than for known drivers.
5. Sensitivity:
   - Replace cBioPortal mutation count with dNdScv-corrected count (when available from
     parallel pipeline rule).
   - Add `n_distinct_diseases_mentioned_with` (PubTator co-mention with disease concept) as
     a covariate to control for disease-association centrality.
   - Use mention count from a *non-cancer* PubMed slice (cardiovascular / metabolic) as a
     placebo: if length still predicts attention there with a similar slope, the effect is
     not cancer-specific.
6. Output: `doc/interpretations/<date>-q011-length-attention-regression.md` with the
   coefficient table and a length-residualized "attention prior" feather written to
   `models/`.

## Pre-registered Expectations

- Marginal length slope: significantly positive (≥ 0 with high confidence).
- Partial length slope after adjusting for mutation count: positive but smaller
  (~30–60% of marginal). Direction-of-change matters more than the exact magnitude.
- Subgroup: smaller length effect within the Bailey 299 (these genes are studied because
  they are real drivers); larger length effect in the complement.
- Placebo (non-cancer slice): non-zero length slope of comparable magnitude — would
  suggest the mechanism is general (accessibility), not cancer-specific.

If the partial slope crosses zero or flips sign, the literature-bias claim collapses and
length is purely a mediator. That is a clean falsifier for the discussion's central
conjecture.

## Connections to Project

- Related hypotheses: none yet — this question motivates a possible hypothesis about
  shared confounding of mutation-count and literature-attention axes.
- Required data or analyses: PubTator gene counts (already on disk at the path above),
  UniProt lengths (already in the pipeline), cBioPortal aggregate mutation counts (already
  in `gene_cancer_study_ratio_annotated.feather`), HGNC alias map (`task:t082`, currently
  open) for the PubTator ↔ UniProt join.
- Priority level: P2 — cheap, clarifies a methodological assumption that affects all
  downstream interpretation steps.

## Related

- Discussion: `discussion:2026-04-24-gene-length-bias-in-mutation-rankings-and-literature`
- Topic: `topic:mutation-rate-normalization`
- Adjacent question: `question:q003-replication-timing-as-gene-level-mutation-rate-confounder`
  (other gene-level mutation-rate confounders besides length)
- External datasets: PubTator BioCXML 2026-01-16 release; UniProt 2025-XX release;
  Bailey 2018 PanCanAtlas Table S1; COSMIC CGC v100.
