---
type: synthesis
title: 'Cancer neuroscience literature batch (21 papers): does it explain a neural-gene
  mutation signal?'
status: active
created: '2026-06-06'
updated: '2026-06-06'
id: synthesis:0015-cancer-neuroscience-literature-batch-21-papers-does-it-explain-a-neural
report_kind: cluster-digest
source_commit: 110aaf19ed97e16a6887298000a89a29e6f47f22
ontology_terms:
- cancer neuroscience
- neuro-immune crosstalk
- perineural invasion
- oncofetal reprogramming
- neuroendocrine neoplasm
- gene-length confounding
source_refs:
- paper:Mancusi2023
- paper:Keough2022
- paper:Magnon2023
- paper:Hanahan2023
- paper:Venkatesh2019
- paper:Hwang2025a
- paper:Huang2023a
- paper:Huang2025a
- paper:Wang2025b
- paper:Wu2025a
- paper:Kizil2024
- paper:Pu2025
- paper:Cortese2020
- paper:Mravec2008
- paper:Lu2026
- paper:Fan2024
- paper:Xiong2023
- paper:Cao2023
- paper:Kulke2012
- paper:Ahmed2020
- paper:Tan2024
- paper:Zhang2025
related:
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- hypothesis:0003-gene-length-confounds-literature-attention
- topic:cancer-neuroscience-neural-regulation
- topic:neuro-immune-crosstalk-cancer
- topic:perineural-invasion-axon-guidance-genes
- topic:neuroendocrine-neoplasm-lineage-confound
- topic:oncofetal-developmental-reprogramming
---

# Cancer neuroscience literature batch (21 papers): does it explain a neural-gene mutation signal?

**Motivating observation (unverified notes).** An early "top mutated genes" view of the
pan-cancer / cBioPortal aggregation was dominated by neural-associated genes — NKAIN2,
KCNIP4, TAFA2 (FAM19A2), RIT2, CALN1, RBFOX1, LSAMP, SGCZ, OPCML. This batch reviews 21
cancer-neuroscience papers to interpret that observation and design a label-free test. The
candidate gene list comes from unreliable notes and is treated as a hint, not ground truth.

## The single most important cross-paper finding

**The cancer-neuroscience literature does not predict a somatic-mutation signal in neural
genes, and none of the candidate genes appear in it.** Across all 21 papers:

1. **Mechanism is expression / innervation / paracrine / epigenetic — not mutation.** Every
   foundational review (`paper:Mancusi2023`, `paper:Keough2022`, `paper:Magnon2023`,
   `paper:Hanahan2023`, `paper:Wang2025b`) frames neural regulation of cancer as nerves
   signaling *to* tumors (NLGN3, NGF/BDNF, norepinephrine→ADRB2, acetylcholine→CHRM1/3,
   glutamate→GRIN/GRIA) and tumors remodeling nerves — driven by **non-mutational epigenetic
   reprogramming** (stated explicitly in `paper:Hanahan2023`). `paper:Wang2025b` and
   `paper:Xiong2023` make the cleanest version of the point: the circuitry lives in the
   **host** peripheral/central nervous system, not in the tumor genome. A mutation-frequency
   table is therefore *not* the expected readout for this biology. *(Late addition,
   `paper:Zhang2025`, Cell 2025: the sharpest single example — the axon-guidance gene **SLIT2**
   drives an HNSCC immune-escape circuit via **ATF4-dependent secretion (expression)**, not
   somatic mutation. A long "neural" gene can be mechanistically central yet contribute only
   length-scaled passengers to a mutation ranking — precisely the dissociation `hypothesis:0012`
   predicts.)*

2. **The canonical neural-cancer genes are a different set from the candidate list.** The
   field's effectors are NLGN3, ADAM10, NGF, BDNF, NTRK1/2/3 (TrkA/B/C), ADRB1/2/3,
   CHRM1/3/4, CHRNA7, GRIN1/2A/2B, GRIA1-4, GAD1, CALCA (CGRP), RAMP1, TRPV1, GDNF/RET,
   SLIT2/ROBO, SEMA3A/3D, L1CAM, NCAM1, DCX, NF1, FMR1. **Not one** of the user's candidate
   genes (NKAIN2, KCNIP4, TAFA2, RIT2, CALN1, RBFOX1, LSAMP, SGCZ, OPCML) is named in any of
   the 21 papers. (`paper:Lu2026` notes LSAMP/OPCML are structurally in the same IgCAM family
   as the canonical L1CAM/NCAM1 PNI mediators, but are **not** themselves cited as PNI
   actors.)

3. **The candidate genes share the gene-length-confound profile.** LSAMP, OPCML, NKAIN2,
   RBFOX1, SGCZ, CALN1, KCNIP4 are unusually long genes / large genomic footprints (adhesion
   IgCAMs, ion-channel-interacting, splicing-regulator, common-fragile-site overlap). This is
   exactly the class the project already knows is inflated by length-proportional passenger
   mutation (`hypothesis:0003`, `question:0031` on TTN-like residual signal). `paper:Lu2026`'s
   reviewer states it outright: the overlap "is expected under length-proportional background
   mutation without any selection."

**Conclusion the batch forces:** the prior should be **null-first**. The most parsimonious
explanation of the candidate list is **H5 (gene length) + H4 (CNS-glioma and neuroendocrine
histology in the cohort)**, not H1 (active neural hijacking). The literature is rich and the
biology is real — it is simply *orthogonal to somatic mutation frequency*. This is set out as
`hypothesis:0012`.

## Mapping the batch to the five candidate explanations

| Explanation | Verdict from the batch | Key papers |
|---|---|---|
| **H1 — tumors hijack top-down neural circuitry** | Real biology, but acts via expression/innervation, **not** tumor-genome mutation. Cannot, on its own, predict a mutation-frequency signal. | Mancusi2023, Keough2022, Wang2025, Xiong2023, Venkatesh2019 |
| **H2 — neural signal via immune modulation** | Strongly supported as *biology* (NE/ADRB2→MDSC/Treg/CD8 exhaustion; CGRP→T-cell exhaustion; GABA from B cells). Again expression-level, not mutational. | Kizil2024, Pu2025, Cortese2020, Mravec2008 |
| **H3 — byproduct of oncofetal / developmental de-repression** | **Most plausible biological route IF any residual signal survives length+histology correction.** SOX2/MYCN-driven oncofetal reprogramming broadly de-represses the fetal transcriptome, of which neural developmental genes are the largest class. Testable label-free via fetal-vs-adult expression (BrainSpan). | Cao2023 (pivotal), Huang2023, Hanahan2023 |
| **H4 — artifact of brain/CNS + neuroendocrine tumors in the cohort** | Directly implicated. Peripheral-cancer papers (Fan2024, Lu2026) *weaken* a pure-CNS artifact, but CNS gliomas (LSAMP/OPCML are recurrent glioma genes) and **neuroendocrine neoplasms** (MEN1/DAXX/ATRX; CHGA/SYP/NCAM1/INSM1 lineage markers) are concrete histology confounds. | Kulke2012, Ahmed2020, Tan2024, Lu2026 |
| **H5 — misannotation / non-neural function / length** | Length confound is the leading null; "misannotation" is partly dissolved by H3 (these genes are *legitimately* fetal-neural, not mislabeled). | Lu2026, Cao2023; project h03 |

## Tensions and nuances between papers

- **H1 vs H3 are entangled, not exclusive.** `paper:Cao2023` reframes "neural hijacking" in
  non-neural tumors as a *special case* of oncofetal de-repression (the same Wnt/Hedgehog/Hippo
  axes that drive stemness reactivate SOX2/OLIG2/BMI1 neural-developmental TFs). For our
  mutation question this matters: H1-as-selection predicts recurrent, clustered, functional
  mutations in specific effectors; H3-as-byproduct predicts diffuse, length-scaled,
  non-recurrent mutation across many developmentally-regulated genes. These make **opposite
  empirical predictions** in our data.
- **Peripheral vs CNS.** Fan2024/Lu2026/Cortese2020 document deep neural biology in non-CNS
  cancers (PDAC, prostate, gastric), so an enrichment that *survives* CNS-study removal would
  not automatically be artifact — but it still would not be *mutational* per the field.
- **Neuroendocrine ≠ cancer-neuroscience.** Kulke2012/Ahmed2020/Tan2024 are a different
  disease class (tumors *of* neuroendocrine cells). Their value here is purely as a **named
  confound**: MEN1 in a top-mutated list is a near-definitive marker of NET-histology
  contamination; ATRX/NF1 are dual CNS+NET confounds.

## What the batch gives us for a label-free "neural gene" definition

No paper releases a computational neural-gene set, but the recommendations converge on
**expression/developmental enrichment**, not GO labels:

- **Adult tissue specificity:** GTEx (brain regions + tibial nerve), Human Protein Atlas
  tissue-specificity (tau/Z-scores). Distinguishes CNS-only from PNS-expressed genes
  (Cortese2020's point — our candidates are mostly CNS-structural).
- **Developmental stage (for H3):** BrainSpan, Allen Developing Human Brain Atlas, Human Cell
  Atlas fetal — fetal-vs-adult brain expression ratio operationalizes the oncofetal axis
  directly (Cao2023).
- **Single-cell / marker sets:** Allen Brain Cell Atlas, PanglaoDB, CellMarker 2.0, Neftel
  2019 / Filbin 2018 glioma OPC/NPC state signatures (Keough2022, Hwang2025a).
- **Positive-control gene set:** the canonical effectors above (NLGN3, ADRB2, NTRK1/2, CHRM3,
  GRIN2A/B, GAD1, NGF, BDNF) — for an H1 somatic-selection test via dN/dS.

## Downstream entities created from this batch

- **Hypothesis:** `hypothesis:0012-neural-gene-enrichment-length-histology-artifact` (null-first).
- **Questions:** `question:0032`–`question:0037` (length null, CNS exclusion, NET exclusion,
  label-free definition, fetal-vs-adult H3 test, canonical-gene dN/dS H1 test).
- **Topics:** five topic notes (see `related`).
- **Plan:** `doc/plans/2026-06-06-neural-gene-enrichment-meta-analysis-plan.md`.
- **Tasks:** group `neural-gene-meta-analysis` (t215–t221) in `tasks/active.md`.
