---
id: "paper:Kandoth2013"
type: "paper"
title: "Mutational landscape and significance across 12 major cancer types"
status: "read"
ontology_terms: []
datasets: ["tcga-pancanatlas"]
source_refs: ["cite:Kandoth2013"]
related: ["paper:Bailey2018", "paper:Lawrence2014", "topic:pan-cancer-mutation-landscape"]
created: "2026-04-13"
updated: "2026-04-13"
---

# Mutational landscape and significance across 12 major cancer types

- **Authors:** Kandoth C, et al.
- **Year:** 2013
- **Journal:** Nature
- **PMID:** 24132290
- **DOI:** 10.1038/nature12634
- **BibTeX key:** Kandoth2013

## Key Contribution

First-generation TCGA Pan-Cancer mutational landscape: somatic point-mutation and
small-indel analysis across 3,281 tumours from 12 major cancer types, yielding 127
significantly mutated genes (SMGs) spanning ~20 cellular processes. Established the
template for subsequent pan-cancer driver-gene analyses by harmonizing exome mutation
calls from three TCGA genome-sequencing centres and running unified downstream
significance, clustering, and clinical-correlation analyses on the pooled cohort.

## Methods

Cohort: 3,281 tumours across BRCA, LUAD, LUSC, UCEC, GBM, HNSC, COAD/READ, BLCA,
KIRC, OV, and LAML (AML). Input variant calls were ingested as curated MAF files
from TCGA's data coordinating centre — individual centres used differing callers
and no unified re-calling pipeline was applied; Kandoth et al. re-lifted coordinates
to GRCh37 and re-annotated transcripts against Gencode/Ensembl. Standardized
mutation data were deposited on Synapse (syn1729383.2) for reproducibility.
Significantly mutated genes were called using the SMG test in the MuSiC
package (Mutational Significance In Cancer; hypergeometric + likelihood tests across
seven mutation categories), both per cancer type and on the pooled pan-cancer cohort
— MutSigCV (Lawrence et al.) is not used here; it was published the same year and
does not appear in the methods. Mutation-rate comparisons used mutations/Mb of
covered coding territory. Unsupervised hierarchical clustering of tumours by binary
SMG mutation status produced cross-cancer-type relationship maps. Survival analyses
correlated SMG mutation status with clinical outcomes, and subclonal vs. founding-clone
assignments used variant allele fractions.

## Key Findings

- **127 SMGs pan-cancer**, organized into roughly 20 processes: transcription factors
  / regulators, histone modifiers, MAPK / PI(3)K / Wnt/β-catenin signalling, splicing,
  proteolysis, genome integrity, and metabolism.
- **Median mutation rates span ~30×:** LUSC highest at 8.15 mutations/Mb; AML lowest
  at 0.28/Mb; all cancer types except AML average > 1 mutation/Mb.
- **Driver load per tumour is small:** most tumours carry two to six SMG mutations,
  implying relatively few cooperating drivers per cancer.
- **Shared vs. tissue-specific drivers:** TP53 is the most recurrent SMG overall
  (42% pan-cancer; 95% in OV; 89% in endometrial serous UCEC). PIK3CA is second
  (>10% in most types, but depleted in OV, KIRC, LUAD, AML). KRAS/NRAS are largely
  mutually exclusive, with tissue-specific hotspot spectra (e.g., Gly12Cys enriched
  in lung, tracking C>A transversions from tobacco exposure).
- **Clustering relationships:** 72% (1,881/2,611) of tumours cluster adjacent to
  same-tissue tumours, but BLCA, HNSC, LUAD, and LUSC scatter widely, signalling
  cross-tissue heterogeneity. A TP53-driven cluster merges subsets of BRCA, HNSC,
  and OV with few other SMG mutations. KIRC shows the strongest exclusivity from
  the other 11 types.
- **Tissue-specificity pattern:** transcription factor / regulator genes tend to be
  cancer-type-specific, whereas histone modifiers (e.g., MLL family, ARID1A) recur
  across multiple cancer types.
- **Per-cancer-type SMG lists** are provided as Supplementary Table 4; standardized
  MAFs are on Synapse (syn1729383.2).

## Relevance

First-generation TCGA pan-cancer mutational landscape analysis (3,281 tumors, 12 cancer types),
methodologically closer to what our pipeline does than the more sophisticated Bailey2018
consensus, although Kandoth et al. already layer a covariate-aware significance test
(MuSiC's SMG test) on top of the raw counts rather than stopping at frequency. The
simpler architecture — harmonize MAFs, count, test, cluster — makes it useful as a
"what's possible with first-pass aggregation" reference. Pre-dates the consensus
driver-gene methodology that became standard in PanCanAtlas (Bailey2018, Ellrott2018
MC3).

## Limitations

- **Small per-cancer cohorts** (typically ~100–300 tumours per type for this 3,281-total
  cohort) leave driver-gene discovery far from saturation; Lawrence2014 quantifies the
  saturation gap on a contemporaneous ~4,700-tumour cohort and shows many tumour types
  need thousands of samples to find drivers at ~2% frequency.
- **Only 12 cancer types** represented — rarer tumour types and most paediatric /
  non-epithelial cancers are absent.
- **Coding-only:** non-coding regulatory mutations, structural variants, copy-number
  alterations, and fusions are outside scope (authors explicitly note this as a lower
  bound for heterogeneity).
- **Heterogeneous upstream calling:** the analysis inherits non-unified caller
  pipelines from the three TCGA GSCs — a limitation later directly addressed by MC3
  (Ellrott2018), which re-called all TCGA exomes under one protocol.
- **MuSiC SMG test** is less background-model-sophisticated than MutSigCV
  (Lawrence2014), so some reported SMGs overlap the well-known long-gene /
  high-background false-positive set.

## Follow-up

- **Lawrence et al. 2014** (*Nature*, "Discovery and saturation analysis of cancer
  genes across 21 tumour types") — quantified driver-discovery saturation on a larger
  cohort and established MutSigCV with covariate correction as the standard SMG caller.
- **Ellrott et al. 2018** (*Cell Systems*, MC3) — uniformly re-called somatic mutations
  across all ~10,000 TCGA exomes using a seven-caller consensus, fixing the
  heterogeneous-upstream-calling issue Kandoth inherited.
- **Bailey et al. 2018** (*Cell*, PanCanAtlas driver consensus) — consensus driver-gene
  catalogue across 33 cancer types / 9,423 tumours from 26 computational tools,
  superseding the Kandoth 127-SMG list as the canonical pan-cancer driver reference.
