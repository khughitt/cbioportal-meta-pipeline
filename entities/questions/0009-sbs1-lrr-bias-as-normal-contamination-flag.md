---
type: question
title: Can the SBS1 late-replicating-region bias (present in normal tissue, absent
  in cancer) serve as a practical contamination quality flag for cBioPortal studies?
status: deferred
created: '2026-04-18'
updated: '2026-04-24'
id: question:0009-sbs1-lrr-bias-as-normal-contamination-flag
revisit_condition: WGS inputs ingested
ontology_terms:
- mutational signatures
- replication timing
- SBS1
- normal tissue contamination
- tumor purity
datasets:
- PCAWG
- SomaMutDB
source_refs:
- paper:Yaacov2023
related:
- topic:signature-decomposition-unmatched-normal
- paper:Yaacov2023
- question:0003-replication-timing-as-gene-level-mutation-rate-confounder
- question:0008-signature-decomposition-tissue-background-subtraction
- task:t122
- task:t123
- task:t124
- task:t126
- dataset:replication-timing-constitutive-regions
- interpretation:0005-t122-rt-brca-pilot
- interpretation:0006-t123-rt-brca-sbs1-proxy-pilot
- interpretation:0007-t126-sbs1-lrr-bias-per-study
- pre-registration:0002-pre-registration-t126-per-study-aggregate-sbs1-lrr-bias-test
---

> **Status note (2026-04-24):** deferred per the t126 pre-registered decision rule.
> The q009 mechanism cannot be evaluated on cBioPortal panel data because the
> MSK-IMPACT panel covers only ~20.7 kb of constitutive late-replicating
> territory (a 23:1 CE:CL bp ratio inside panel coverage), so the published SBS1
> LRR-bias signal is not measurable on the unmatched-normal cohort q009 was
> designed to flag. Revisit when WGS inputs are ingested. See
> `interpretation:0007-t126-sbs1-lrr-bias-per-study` for the verdict trail
> and `pre-registration:0002-pre-registration-t126-per-study-aggregate-sbs1-lrr-bias-test` for the locked thresholds.

# Can the SBS1 late-replicating-region bias (present in normal tissue, absent in cancer) serve as a practical contamination quality flag for cBioPortal studies?

## Summary

Yaacov et al. 2023 (Scientific Reports) demonstrated that SBS1 mutations accumulate preferentially in late-replicating regions (LRR) of the genome in normal tissue, but lose this LRR bias in matched cancer samples. This represents a potential topographic fingerprint: a cBioPortal study showing SBS1 with a detectable LRR enrichment — assessed by mapping SBS1-attributed mutations to constitutive RT regions — would carry an excess of normal-tissue-origin SBS1 relative to tumor-origin SBS1. The question is whether this diagnostic is practically computable from panel/WES-based mutation calls and, if so, whether it provides a usable contamination flag.

## Why It Matters

- If operable, it would provide a direct (not proxy) indicator of normal-tissue contamination in individual studies, independent of assumptions about tumor purity or cohort composition.
- It would complement the SBS1/SBS5 ratio proxy (Intervention 2 in `topic:signature-decomposition-unmatched-normal`) with a mechanistically grounded signal.
- For WGS-based studies in the pipeline (e.g., if the MC3 TCGA WGS data is incorporated), this diagnostic is immediately applicable.

## Current Evidence

- Yaacov 2023: SBS1 LRR bias in normal tissue is highly reproducible (R = 0.967 between two independent cohorts) and statistically significant (Wilcoxon P < 2.2×10⁻¹⁶). The change between normal and cancer contexts is consistent across all four matched tissue pairs examined.
- The signal requires aligning mutations to constitutive RT regions (~40% of the genome) and comparing early vs. late enrichment. For WGS, this is feasible with SigProfilerTopography or equivalent tools.
- For panel/WES data (typical of cBioPortal): per-gene replication timing annotations exist (ENCODE RT data, mapped to RefSeq genes). A coarser version of the test — compare SBS1 mutation density across ERR-annotated vs LRR-annotated genes — is possible but has lower power due to fewer mutations per sample.
- `t122` (BRCA matched vs unmatched, all mutations) produced a mixed result: unmatched `msk_impact_2017` showed a higher `CL/CE` ratio than matched `tcga_mc3`, but absolute `CL` burden remained lower, so the coarse gene-level RT signal was suggestive but still dominated by panel-vs-WES coverage differences.
- `t123` then restricted the BRCA comparison to a simple SBS1-like proxy (coding CpG `C>T` plus complementary `G>A`) on the same assignment sample surface. That branch failed as an operational proxy: the unmatched panel cohort was overwhelmingly zero-inflated (`CE == 0` in 1,157/1,210 samples; `CL == 0` in 1,205/1,210), so the higher pseudocount-stabilized ratio was not persuasive evidence of SBS1-specific late-replication enrichment.

## Thoughts

- The main practical constraint is statistical power. Detecting an LRR enrichment of SBS1 requires enough SBS1-attributed mutations to compare regional distributions. For panel-sequenced studies with 50–200 mutations per sample, this test is unlikely to be powered per-sample; it might be powered at the per-study aggregate level (pooling all samples of the same study).
- A simpler proxy: at the gene level, LRR-resident genes should show higher per-sample SBS1 mutation counts in studies with normal contamination. This can be tested with existing pipeline outputs by crossing gene positions with LRR/ERR annotations.
- The Yaacov 2023 paper does not provide a standalone computational tool for this analysis; the methods use SigProfilerMatrixGenerator + custom RT-region annotation. SigProfilerTopography (a companion tool from the Alexandrov lab) is designed to compute topographic biases and would be the most accessible implementation pathway.
- The coarse SBS1/SBS5 ratio proxy was tested first in `t110` and did **not** separate the first required BRCA matched-vs-unmatched comparison. That negative result raises the value of this more mechanistic RT-based branch: if a contamination flag is going to survive first contact with the data, it is more likely to be the direct LRR-bias path than the ratio proxy.
- The April 22 RT branch materially sharpened that assessment. The all-mutation RT pilot (`t122`) was promising enough to justify a follow-up, but the first SBS1-enriched approximation (`t123`) collapsed under panel sparsity. So the remaining open question is no longer "should we try a proxy?" but "is a true SBS1 context/topography implementation justified here, or should the panel/WES proxy route be retired?"

## Connections to Project

- Related hypotheses: none filed.
- Required data or analyses:
  1. `t121` imported constitutive replication-timing bins and derived the conservative gene-level `CE`/`CL` map (`dataset:replication-timing-constitutive-regions`).
  2. `t122` ran the first BRCA matched-vs-unmatched gene-level `CL/CE` burden pilot on all mutations.
  3. `t123` reran that BRCA pilot on the simple SBS1-enriched proxy subset and found the panel/WES approximation too sparse to be operational.
  4. `t124` is now the active fork decision: either scope a true mutation-context / SBS1-attribution or topography implementation, or retire the panel/WES proxy route for q009.
  5. For WGS-level studies: apply SigProfilerTopography to compute formal LRR bias delta values and compare with expected cancer vs normal tissue values.
- Priority level: medium for WGS studies; low for panel-only studies in the current pipeline. Becomes high if WGS inputs are added.

## Related

- Topic notes: `topic:signature-decomposition-unmatched-normal`
- Article notes: `paper:Yaacov2023`
- Related questions: `question:0003` (RT as gene-level mutation-rate confounder), `question:0008` (SBS1/SBS5 contamination magnitude)
- Recent project evidence: `interpretation:0005-t122-rt-brca-pilot`, `interpretation:0006-t123-rt-brca-sbs1-proxy-pilot`
- Methods/Datasets: SigProfilerTopography; ENCODE replication timing data (constitutive ERR/LRR regions); Yaacov 2023 code (see Yaacov et al. 2022, the companion cancer-RT paper for RT region construction)
