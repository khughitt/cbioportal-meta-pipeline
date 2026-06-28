---
type: paper
title: Cancer therapy shapes the fitness landscape of clonal hematopoiesis
status: read
created: '2026-04-13'
updated: '2026-06-28'
id: paper:Bolton2020
ontology_terms: []
source_refs:
- article:Bolton2020
- cite:Bolton2020
related:
- topic:clonal-hematopoiesis-contamination
- topic:targeted-panel-sequencing-bias
---

# Cancer therapy shapes the fitness landscape of clonal hematopoiesis

- **Authors:** Bolton KL, et al.
- **Year:** 2020
- **Journal:** Nature Genetics
- **PMID:** 33106634
- **DOI:** 10.1038/s41588-020-00710-0
- **BibTeX key:** Bolton2020

## Key Contribution

This therapy-associated clonal-hematopoiesis note links topic:clonal-hematopoiesis-contamination and topic:targeted-panel-sequencing-bias.

Largest single-institution characterization of clonal hematopoiesis (CH) in solid-tumor
patients (n = 24,146) using paired tumor / blood (buffy-coat) sequencing on the
MSK-IMPACT panel. Establishes that prior cytotoxic therapy and ionizing radiation
preferentially expand CH clones bearing DNA-damage-response (DDR) mutations
(`PPM1D`, `TP53`, `CHEK2`), whereas age and smoking drive expansion of `DNMT3A` /
`TET2` / `ASXL1`. This means the per-gene CH spectrum observed in a tumor cohort is
non-randomly skewed by treatment history [@Bolton2020].

## Methods

- **Cohort.** 24,146 patients sequenced via MSK-IMPACT between 2015-2019, all with
  matched tumor + buffy-coat. A treated/untreated split was used for therapy-effect
  modelling (5,978 treated vs 4,160 untreated in the primary analysis subset). A
  separate sequential-sampling cohort of ~525 patients with serial blood draws was
  used to track clonal trajectories under therapy.
- **Sequencing.** MSK-IMPACT hybrid-capture panel (~410-468 genes across versions);
  blood buffy-coat sequenced as a "matched normal" alongside tumor. Median coverage
  ~500x in blood.
- **CH variant definition.** A blood-detected variant was called somatic (vs germline)
  using a tumor-blood VAF ratio rule: blood VAF >= 2x tumor VAF (or 1.5x if the tumor
  biopsy was a lymph node, to limit leukocyte-contamination false positives).
  Variants further classified as **putative-driver CH (PD-CH)** if they matched a
  curated list of known myeloid driver hotspots / truncating events, vs non-PD-CH.
  Effective lower-bound VAF ~ 2%.
- **Therapy-history annotation.** Structured EHR pull of every cytotoxic agent,
  targeted therapy, immunotherapy and external-beam / radionuclide radiation course
  prior to the blood draw, with cumulative dose and treatment-site fields. Drugs
  grouped into mechanistic classes (platinum, topoisomerase II inhibitors, taxanes,
  antimetabolites, alkylators, IMiDs, etc.).
- **Statistics.** Multivariable logistic regression for CH presence and per-gene CH
  presence, adjusted for age, sex, smoking, ancestry, and prior therapies. Cox
  models for therapy-related myeloid neoplasm (tMN) onset.

## Key Findings

- **Overall CH prevalence ~30%** of patients harbored at least one CH mutation; PD-CH
  prevalence rose monotonically with age (roughly doubling per decade after 50).
- **Per-gene CH driver spectrum** (share of CH-positive patients carrying a mutation
  in each gene; values are approximate, from main-text/Fig. 1 and downstream
  literature citing this dataset):

  | Gene     | ~Share of CH calls | Selection signal                                |
  |----------|--------------------|-------------------------------------------------|
  | DNMT3A   | ~37%               | age-dominant; weakly therapy-modulated          |
  | PPM1D    | ~20%               | strongly therapy-selected (radiation, platinum) |
  | TET2     | ~16%               | age-dominant                                    |
  | ASXL1    | ~8.6%              | smoking-enriched                                |
  | TP53     | ~8.5%              | strongly therapy-selected (radiation, platinum, topo-II) |
  | CHEK2    | (smaller)          | therapy-selected (DDR class)                    |
  | PRPF8    | (smaller)          | therapy-selected splicing factor                |
  | SRSF2 / SF3B1 | (small)       | age-related, MDS-like                           |

- **Therapy-driven enrichment.**
  - **External-beam radiation and radionuclide therapy** showed the largest effect on
    DDR-CH (`TP53`, `PPM1D`, `CHEK2`); site-specific dose mattered: head and neck
    OR ~2.2 (p = 9e-3), pelvis OR ~2.2 (p = 5e-2), brain OR ~1.7 (p = 2e-2),
    thorax OR ~1.5 (p = 3e-2).
  - **Platinum agents** and **topoisomerase II inhibitors** independently selected for
    `PPM1D`/`TP53`/`CHEK2`-mutant clones.
  - **Cytotoxic therapy did not enrich `DNMT3A` / `TET2`** -- their prevalence is
    explained by age, not treatment.
  - **Smoking** specifically enriched `ASXL1`.
  - Sequential-sample analysis confirmed clonal logic: under DNA-damaging therapy,
    pre-existing DDR-mutant clones outcompete DNMT3A/TET2 clones; this is causal
    expansion, not merely co-occurrence.
- **Age dependence.** CH prevalence increases approximately log-linearly with age;
  in the breast-cancer subset, OR per year = 1.05 (95% CI 1.05-1.06).
- **Clinical significance.** Pre-treatment PD-CH (especially `TP53`/`PPM1D` at higher
  VAF) was associated with elevated cumulative incidence of therapy-related myeloid
  neoplasm (AML/MDS) over follow-up, and with shortened survival. The authors propose
  baseline CH genotyping to inform therapy selection (e.g. avoid topo-II /
  high-dose radiation in PD-CH-positive patients where alternatives exist).

## Limitations

- Single institution (MSK), referral-biased cancer population — CH prevalence here
  is not representative of the general adult population.
- Panel-restricted: only CH drivers covered by MSK-IMPACT are detectable; novel /
  rare CH drivers outside the panel are missed.
- Effective VAF floor ~2%; small clones (<1%, the bulk of true CH) are
  systematically under-called.
- Therapy history is observational and confounded with cancer type, stage, and
  prior CH status itself; causality for the radiation/platinum -> DDR-CH link rests
  primarily on the sequential-sampling subset.
- Single time point for most patients — cannot distinguish pre-existing vs
  therapy-induced de novo for a given clone without serial samples.

## Follow-up

- Coombs / Niroula / Miller subsequent work refining tMN-prediction CH features
  (CHRS score) builds directly on this dataset.
- Motivates **genotype-aware filtering** in any pan-cancer panel cohort that
  ingests MSK-IMPACT (matched-normal) data alongside unmatched-normal panel
  cohorts: the matched-normal cohorts will under-report CH-driver mutations as
  "tumor" mutations (because they are correctly subtracted out), while
  unmatched-normal cohorts will over-report them.

## Relevance

**Critical interpretation caveat for this pipeline.** Panel-based tumor calls from unmatched
normals can attribute CH variants (DNMT3A, TET2, ASXL1, PPM1D, TP53, etc.) to the tumor, inflating
per-cancer mutation ratios for CH-driver genes. Should be cross-referenced before reporting
gene-cancer associations for any CH-frequent gene.

The Bolton spectrum gives a concrete prioritization: when aggregating MSK-IMPACT (matched)
with unmatched-normal panel cohorts, the most CH-contaminated genes in the unmatched
arm will be `DNMT3A`, `PPM1D`, `TET2`, `TP53`, `ASXL1` (and `CHEK2`, `PRPF8` in
heavily-pretreated tumor types). A first-pass CH-aware filter should: (i) flag these
genes; (ii) downweight low-VAF (<10%) calls in older patients; (iii) treat splice-site
DDR variants in pretreated cohorts with extra suspicion. Cohort-level: expect
unmatched-normal cancer types to show inflated DDR-gene mutation rates relative to
MSK-IMPACT for the same cancer [@Bolton2020].
