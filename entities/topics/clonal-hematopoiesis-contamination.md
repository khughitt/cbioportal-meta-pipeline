---
type: topic
title: Clonal hematopoiesis contamination in panel-based tumor mutation calls
status: active
created: '2026-04-13'
updated: '2026-04-13'
id: topic:clonal-hematopoiesis-contamination
ontology_terms: []
source_refs: []
related:
- paper:Bolton2020
- paper:Zehir2017
- paper:Pugh2022
- paper:Martincorena2017
- paper:Yoshida2026
- topic:targeted-panel-sequencing-bias
- topic:cross-study-harmonization
---

# Clonal hematopoiesis contamination in panel-based tumor mutation calls

## Summary

Somatic mutations arising in blood (clonal hematopoiesis, CH) leak into tumor variant calls
when normal-control sequencing is absent or imperfect. CH-driver genes (DNMT3A, TET2, ASXL1,
PPM1D, TP53, CHEK2, PRPF8) appear as spuriously "mutated" across many cancer types in
panel-based cohorts that lack matched-buffy-coat sequencing. Bolton et al. [@Bolton2020] (Nat Genet,
24,146 MSK-IMPACT patients with paired tumor + buffy-coat) is the empirical anchor: ~30% of
solid-tumor patients carry detectable CH at panel sensitivity, prevalence doubles per decade
after 50, and prior cytotoxic therapy + ionizing radiation strongly enrich for *DDR*-CH
clones.

For our cross-study aggregation, the practical consequence is unambiguous: **mixing
matched-normal cohorts (MSK-IMPACT) with unmatched-normal cohorts (~52% of GENIE) without a
CH-aware filter will systematically inflate per-cancer mutation rates for these 7 genes in
the unmatched arm.**

## Key Concepts

- **CH = age-related expansion of clonal blood cell populations** carrying somatic
  mutations, primarily in DNA-methylation regulators and DDR genes. Background prevalence
  in healthy adults rises from <1% under 50 to >10% over 70.
- **CH "drivers" vs CH "passengers."** Bolton et al. [@Bolton2020] distinguish putative-driver CH (PD-CH:
  curated myeloid hotspots / truncating events) from non-driver blood variants. The PD-CH
  spectrum is the leakage risk for tumor panel calls.
- **Matched buffy-coat normal subtraction** removes per-patient CH from the tumor MAF.
  Tumor-only calling cannot distinguish a CH variant present at modest VAF in tumor tissue
  (because blood / lymphocytes infiltrate solid tumors) from a real somatic tumor mutation.
- **VAF / age / tumor-type heuristics** are the substitute when matched normal is
  unavailable: low-VAF (<10%) calls in DDR genes in older patients in pre-treated cohorts
  carry the highest CH-leakage probability.
- **Therapy-driven CH selection** [@Bolton2020]: radiation, platinum, and topoisomerase-II
  inhibitors expand DDR-CH clones (TP53/PPM1D/CHEK2). Smoking enriches ASXL1. DNMT3A and
  TET2 are essentially age-only.

## Current State of Knowledge

The Bolton et al. [@Bolton2020] cohort gives a concrete per-gene CH spectrum (share of CH-positive
patients carrying a variant in each gene):

| Gene | ~Share of CH calls | Selection signal |
|---|---|---|
| DNMT3A | ~37% | age-dominant; weakly therapy-modulated |
| PPM1D | ~20% | strongly therapy-selected (radiation, platinum, topo-II) |
| TET2 | ~16% | age-dominant |
| ASXL1 | ~9% | smoking-enriched |
| TP53 | ~8.5% | strongly therapy-selected (radiation, platinum, topo-II) |
| CHEK2 | smaller | therapy-selected (DDR class) |
| PRPF8 | smaller | therapy-selected splicing factor |
| SRSF2 / SF3B1 | small | age-related, MDS-like |

**Critical interpretation:** PPM1D's ~20% share is dramatically over-represented vs.
general-population CH precisely because the cohort is heavily pretreated. This cohort is
not a baseline-CH paper; it's a *therapy-selected*-CH paper. Cross-cancer aggregations
that pool by-cancer-type without controlling for treatment exposure inherit this bias.

Martincorena et al. [@Martincorena2017] provide the deeper context: dN/dS ≈ 1 across the genome in normal
somatic tissues *including* blood, with positive selection acting on a defined set of
driver genes. CH is therefore a *predictable* phenomenon, not an artifact — but pretending
it isn't there in tumor calls is the artifact.

## Controversies & Open Questions

- **No portable CH-aware filter prescription has been published.** That matched-normal
  matched-normal VAF-ratio rule (blood ≥ 2× tumor VAF; 1.5× for nodal biopsies; ~2% VAF
  floor) only works when matched blood is available. The unmatched-cohort analogue is
  heuristic.
- **What VAF threshold should disqualify a tumor call as likely CH?** Practice varies; <5%
  is a reasonable starting point but produces false negatives for high-purity tumors and
  false positives for low-purity ones.
- **Are ASXL1 / TET2 in solid tumors really CH leakage, or sometimes real?** ASXL1 is a
  bona fide tumor suppressor in some lineages (myeloid, mesenchymal). The frequency
  inflation in panel data is partly real biology + partly CH leakage; disentangling
  requires per-call provenance, which most cross-study aggregations lack.

## Relevance to This Project

Our cross-study mutation aggregation pipeline ingests both matched-normal (MSK-IMPACT) and
tumor-only (much of GENIE) cohorts and combines them into a single per-(gene, cancer)
ratio. Without a CH-aware filter, the 7 priority CH-driver genes will appear *spuriously
elevated* in our gene_cancer outputs — the elevation reflects unmatched-normal cohorts in
the denominator, not real per-cancer biology.

This is amplified in our `summary/mut/clusters/cancer.feather` output: cancer types
dominated by tumor-only studies will cluster together partly because they share CH leakage
in DNMT3A/PPM1D/TET2.

## Pipeline Implications

Concrete additions to plan:

1. **Add a `ch_priority_gene` annotation** to every per-gene output, flagging the 7-gene
   list (DNMT3A, PPM1D, TET2, TP53, ASXL1, CHEK2, PRPF8). Two-line addition; high
   interpretive value.
2. **Per-study `matched_normal` flag** ingested from study metadata (where available).
   MSK-IMPACT cBioPortal studies are matched-normal by design; GENIE per-center varies.
   Pugh et al. [@Pugh2022] report 48% of v9.1 GENIE has matched normals; the 52% remaining are tumor-
   only.
3. **CH-aware ratio recomputation.** For each (CH-priority-gene, cancer-type) pair,
   compute ratios separately on the matched-normal vs tumor-only sub-cohorts. A large
   discordance is the signal that CH is contaminating the pooled ratio.
4. **Optional: VAF-based downweighting** for CH-priority calls in tumor-only cohorts
   (e.g., downweight variants with VAF < 10% in patients > 60). This is the
   unmatched-cohort heuristic substitute for Bolton's VAF-ratio rule.

The first three are tractable from data we already have (per-call gene ID + per-study
matched-normal flag). The fourth needs per-call VAF + per-patient age, which not all
cBioPortal studies expose.

## Key References

- Bolton2020 — 24,146-patient MSK-IMPACT-paired-buffy-coat CH characterization;
  therapy-selectivity quantification; the origin of the 7-gene priority list.
- Zehir2017 — establishes the matched-buffy-coat MSK-IMPACT design that makes Bolton's
  paper possible; demonstrates clean CH-gene calls in a matched cohort.
- Pugh2022 — quantifies that 52% of current GENIE is tumor-only; centralized CH/artifact
  filtering is applied but is not equivalent to per-patient matched normal.
- Martincorena2017 — dN/dS ≈ 1 in normal somatic tissues including blood; reframes CH as
  predictable selection, not artifact.
- Future: Bolton's CH-Risk-Score (CHRS, follow-up work) as a more nuanced filter than
  per-gene flagging.
