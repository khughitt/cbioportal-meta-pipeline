---
id: "synthesis:2026-04-18-somatic-mutations-in-normal-tissue"
type: "synthesis"
title: "Somatic mutations in morphologically normal human tissues — cross-paper synthesis"
status: "active"
source_refs:
  - "article:Martincorena2018"
  - "article:Lin2024"
  - "article:Xu2025"
  - "article:Yaacov2023"
  - "article:Gao2023"
  - "article:Poon2021"
  - "article:Li2021"
  - "article:Yoshida2026"
  - "article:LeeSix2018"
related:
  - "topic:clonal-hematopoiesis-contamination"
  - "topic:pan-cancer-mutation-landscape"
  - "topic:mutation-rate-normalization"
  - "topic:signature-decomposition-unmatched-normal"
  - "question:q001-normal-epithelial-clone-contamination-in-esophageal-studies"
  - "question:q002-normal-breast-cna-background-chr1q-chr16q"
  - "question:q003-replication-timing-as-gene-level-mutation-rate-confounder"
  - "question:q004-mca-burden-in-esophageal-vs-other-study-tissues"
  - "question:q005-gli1-normal-tissue-hotspot-inflation"
  - "question:q006-ch-priority-gene-completeness"
  - "question:q007-cross-tissue-somatic-mutation-rate-variation-as-null-model"
  - "question:q008-signature-decomposition-tissue-background-subtraction"
  - "question:q009-sbs1-lrr-bias-as-normal-contamination-flag"
  - "question:q010-cuplr-style-tof-classifier-for-suspect-normal-samples"
created: "2026-04-18"
updated: "2026-04-18"
---

# Somatic mutations in morphologically normal human tissues — cross-paper synthesis

Six papers reviewed together on 2026-04-18, all characterizing somatic mutations (SNVs, CNAs, and mCAs) in phenotypically normal human tissues. Each bears on the same project concern: how much of the gene x cancer signal emerging from the cBioPortal cross-study aggregation pipeline reflects tumor biology versus background mutagenesis in surrounding or contaminating normal cells. The companion review `article:Yoshida2026` provides the integrative frame.

## Papers covered

| Citekey | Scope | Variant class | Key "normal-tissue" claim |
|---------|-------|---------------|---------------------------|
| `Martincorena2018` | 9 donors age 20–75, normal esophagus | SNV (74-gene panel, 870×) | NOTCH1 selected dN/dS>50; covers 30–80% of normal epithelium by middle age vs ~10% of ESCC; TP53 opposite pattern; ~2000 SNVs/cell by late life; no APOBEC in normal |
| `Li2021` | 5 donors, ~29 organs | SNV + limited CNA | Every tissue sampled carries thousands of somatic SNVs; 32 cancer-driver genes show positive selection in normal tissue; esophagus/cardia contain macroscopic driver-clones |
| `Xu2025` | 14 GTEx donors, 46 tissues, 265 samples | Protein-coding SNV | Pan-tissue landscape of 8,470 somatic SNVs; novel mSOMA caller handles tumor-free multi-tissue data; tissue-specific burden and spectra baseline |
| `Lin2024` | 49 healthy women, 83k cells | CNA (single-cell DNA) | Median 3.19% of normal breast epithelial cells are aneuploid and carry cancer-like CNAs (incl. der(1;16)); 82% form detectable clonal expansions |
| `Gao2023` | 948 individuals across tissues | Mosaic chromosomal alterations (mCAs) | mCA prevalence varies ~10-fold across tissues; esophageal mucosa reaches ~10% prevalence |
| `Poon2021` | Blood + esophagus | Synonymous-passenger VAF spectrum | Known drivers explain only ~10% of blood clonal expansions (20 top CH variants) or ~15% with full 468-gene MSK-IMPACT panel — ~90% remain unexplained; NOTCH1+TP53 alone account for ~60% of esophageal clonal expansions |
| `Yaacov2023` | Normal vs matched cancer tissues | Mutational signatures x replication timing | Replication-timing bias is signature-dependent; SBS4 is LRR-only in lung, SBS88 is ERR-only in normal colon, SBS1 loses its LRR bias in cancer but retains it in normal |
| `LeeSix2018` | Single 59-yr-old donor, 140 HSC colonies | WGS phylogeny | HSC effective population size ~50–200k; ~17 genome-wide SBS/year; phylogeny shows clonal drift alone cannot explain the large CH clones Poon2021 measures — forces the "90% unexplained" signal to be real selection, not drift |

## Shared themes

### 1. Normal tissue is not a quiet null — it's a noisy, structured null

All six studies converge on the same headline: "normal" tissue is already carrying thousands of SNVs per cell (`Li2021`, `Xu2025`), detectable cancer-like CNAs in a few percent of cells (`Lin2024`, `Gao2023`), and a dN/dS signal consistent with positive selection across a gene set much broader than the classical cancer drivers (`Poon2021`). Normal-tissue mutagenesis is not uniform noise — it has tissue-specific burden, signature composition (`Xu2025`, `Yaacov2023`), and replication-timing structure (`Yaacov2023`).

**Consequence for cbioportal:** The pipeline's frequency/ratio outputs silently compare one-or-two drivers per tumor against this structured background. Every unmatched-normal cBioPortal study contributes some fraction of variants that exist in the normal tissue surrounding the tumor.

### 2. "Driver genes" are selected for in healthy tissue too

`Li2021`, `Yoshida2026`, and `Poon2021` all report that canonical cancer drivers (NOTCH1, TP53, DNMT3A, PPM1D, CHEK2, among others) are under active positive selection in the *normal* counterparts of the tissues where they also drive cancer. `Lin2024` finds the luminal-A/B hallmark der(1;16) CNA pre-existing in normal breast. The project's `ch_priority_gene` flag (Bolton 2020 7-gene list) covers only the blood lineage — `Poon2021` argues the blood list is a lower bound on the unexplained selection signal, and the other five papers extend the same concern to solid-tissue lineages.

**Consequence for cbioportal:** A gene that recurs cross-study at moderate frequency may be recurring partly because its normal-tissue pre-malignant clones were admixed into cBioPortal tumor specimens before sequencing. This biases exactly the "recurring gene-cancer associations" signal the project is built to detect.

### 3. Selection structure varies by tissue in measurable ways

The papers give empirical gradients the pipeline could use:
- **By tissue** — `Li2021` ranks tissues by mutation burden; `Xu2025` provides the matching protein-coding spectrum; `Gao2023` provides tissue-specific mCA prevalence. Tissues with higher normal-mutation burdens (esophagus, skin, colon) will have more background contamination than tissues with lower burdens (brain, heart).
- **By signature** — `Yaacov2023` shows that SBS1 and SBS5 dominate normal-tissue signatures, and several signatures (SBS4, SBS7a/b, SBS88) have strong replication-timing preferences. This maps signature-space contamination onto gene-space contamination via replication timing.
- **By gene** — replication-timing structure (`Yaacov2023`) means that genes sitting in late-replicating regions will accumulate passenger mutations at a systematically higher rate, inflating their rank without reflecting selection.

**Consequence for cbioportal:** Per-tissue, per-signature, and per-gene replication-timing corrections all now have published priors and would be testable add-ons to `create_freq_tables.py` and `create_combined_gene_cancer_freq_table.py`.

## Tensions between papers

- **Scale of the problem.** `Li2021` and `Yoshida2026` position normal-tissue clonal expansion as a widespread, multi-organ reality with driver-gene enrichment. `Xu2025`'s tumor-free exome landscape finds lower absolute coding burdens than the deep targeted-sequencing numbers implied by Martincorena-style clonal studies — this is methodological (exome vs clone-level) rather than contradictory, but it matters for quantitative calibration. The project should resist conflating "driver-containing clone exists in X% of donors" with "X% of pipeline variants in that tissue are normal-tissue contamination."
- **How much "unexplained" selection there is.** `Poon2021` pins ~90% of blood clonal-expansion selection to signal *outside* the 468-gene MSK-IMPACT panel (only ~10% from the 20 most common high-fitness CH variants, ~5% more from the full panel). `Xu2025` and `Yaacov2023` recover strong tissue-specific passenger structure. Whether the "unexplained" selection is really selection, or substrate/signature-driven hypermutability masquerading as selection under the synonymous-passenger test, is still open — `Yaacov2023`'s replication-timing biases argue part of the signal is substrate, not selection.
- **Variant class coverage.** `Lin2024` and `Gao2023` speak to CNAs/mCAs. The current cbioportal pipeline is SNV-first, so the CNA-only findings do not directly contaminate today's outputs — but they do contaminate any future extension to CNA or structural-variant aggregation.

## Combined implications for the project

Ranked by severity against the current pipeline:

1. **High priority — direct SNV inflation risk.** `Li2021` + `Yoshida2026` + `Poon2021` jointly establish that canonical cancer drivers (notably NOTCH1, TP53, DNMT3A, ARID1A) are already at measurable VAF in normal tissue of the organ they later drive cancer in. Unmatched-normal cBioPortal studies will propagate some of this signal into the `gene_cancer_study.feather` frequencies. The `matched_normal_studies` config list and `tcga_mc3` pseudo-study are partial mitigations; expanding that list wherever the underlying study used patient-matched sequencing is the cheapest next step.

2. **High priority — CH list breadth.** `Poon2021`'s unexplained-selection finding argues directly that the Bolton 7-gene `ch_priority_gene` list is a floor, not a ceiling. Tracked as `question:q006`. Before expanding, we should ask whether an empirical inclusion criterion (e.g., "gene with excess synonymous burden in blood-adjacent tissues in a published CH panel") would serve better than a fixed list.

3. **Medium priority — hypothesis-level calibration.** `Xu2025`'s per-tissue, per-gene normal-tissue burden table is the closest thing to a "null model" for what a cross-study frequency of X% in tissue Y is expected to be under background mutagenesis alone. Attaching this as a background column to the `_annotated` feathers would let downstream analysis explicitly subtract (or flag) background-consistent frequencies. Tracked as `question:q007`.

4. **Medium priority — replication-timing confounder.** `Yaacov2023` means that replication-timing-stratified analyses are worth considering when comparing gene-level ranks across cancer types whose dominant signatures have different RT preferences (e.g., lung/SBS4 vs colon/SBS88). Tracked as `question:q003`.

5. **Lower priority (for now) — CNA/mCA contamination.** `Lin2024` and `Gao2023` flag contamination risks that do not affect current SNV outputs but do affect any future CNA aggregation. Tracked as `question:q002` (breast CNA specifically) and `question:q004` (mCA in esophagus). Keep these in mind before enabling CNA workflows.

6. **Site-specific inflation flags.** `question:q001` (esophageal NOTCH1 from Yoshida2026) and `question:q005` (GLI1 exon 12 hotspot from Xu2025) are narrow, testable predictions — both can be checked directly against current pipeline outputs with a `gene_cancer_study_ratio_annotated.feather` query.

7. **Signature-space contamination, not just gene-space.** See companion synthesis `topic:signature-decomposition-unmatched-normal`. The background tissue-of-origin signal these six papers describe does not only leak through as inflated gene-level frequencies — it also perturbs mutational-signature decomposition in any per-study analysis run on cBioPortal cohorts without matched normals. Tracked as `question:q008` (tissue-background subtraction feasibility), `question:q009` (SBS1 replication-timing bias as a contamination QC flag, per Yaacov2023), and `question:q010` (tissue-of-origin classifier to flag normal-like samples).

## Next reading

- **Martincorena et al. 2018 (Science)** — now summarized as `article:Martincorena2018`; provides primary numbers behind multiple claims in this synthesis and in `question:q001`.
- **Yokoyama et al. 2019 (Science)** — independent normal esophagus clone study; mechanistically addresses the NOTCH1 paradox (mouse model suggesting NOTCH1-mutant cells suppress adjacent cancer proliferation). Complements Martincorena2018.
- **Lee-Six et al. 2018 (Nature)** — normal-blood clone phylogeny and DNMT3A dynamics, complementing `Poon2021` and the CH-gene list question. [DONE — see `article:LeeSix2018`; key addition: N_eff ~100k HSCs confirms Poon 2021's unexplained selection is genuine, not drift.]
- **Yaacov et al. 2022** (cancer-tissue companion to `Yaacov2023`) — completes the signature-RT map for cancer contexts.
- **Cancer-specific vs tissue-specific signature decomposition** in an unmatched-normal study context: open question worth a dedicated literature pass.
