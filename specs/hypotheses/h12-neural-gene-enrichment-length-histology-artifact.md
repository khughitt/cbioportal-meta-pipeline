---
id: "hypothesis:h12-neural-gene-enrichment-length-histology-artifact"
type: "hypothesis"
title: "Apparent neural-gene enrichment in top-mutated genes is a length + histology artifact, not neural selection"
status: "proposed"
phase: "active"
source_refs:
  - "paper:Mancusi2023"
  - "paper:Hanahan2023"
  - "paper:Cao2023"
  - "paper:Lu2026"
  - "paper:Tan2024"
related:
  - "hypothesis:h03-gene-length-confounds-literature-attention"
  - "hypothesis:h01-non-tumor-signal-contamination"
  - "question:q031-residual-gene-length-signal-mechanism"
  - "question:q032-neural-gene-length-null"
  - "question:q033-neural-enrichment-cns-exclusion"
  - "question:q034-neuroendocrine-histology-confound"
  - "question:q035-label-free-neural-gene-definition"
  - "question:q036-oncofetal-fetal-vs-adult-neural-expression"
  - "question:q037-canonical-neural-gene-dnds-selection"
  - "synthesis:2026-06-06-cancer-neuroscience"
  - "topic:oncofetal-developmental-reprogramming"
created: "2026-06-06"
updated: "2026-06-06"
---

# Hypothesis: Apparent neural-gene enrichment in top-mutated genes is a length + histology artifact

## Organizing Conjecture

An early "top mutated genes" view of the cBioPortal aggregation appeared dominated by
neural-associated genes (NKAIN2, KCNIP4, TAFA2/FAM19A2, RIT2, CALN1, RBFOX1, LSAMP, SGCZ,
OPCML). A 21-paper review of the cancer-neuroscience literature
(`synthesis:2026-06-06-cancer-neuroscience`) establishes two facts that reframe the
observation: (i) the field's mechanism of neural regulation of cancer is **expression,
innervation, paracrine signaling, and non-mutational epigenetic reprogramming**, not somatic
mutation of neural genes in tumor DNA; and (ii) **none** of the candidate genes appear in that
literature, whose canonical effectors (NLGN3, ADRB2, NTRK1/2, CHRM1/3, GRIN/GRIA, NGF/BDNF)
are a disjoint, mostly *short-to-moderate* gene set.

This hypothesis therefore states the **null-first** claim: the observed neural-gene
"enrichment" is explained by two known confounds acting together —

- **Gene length (H5).** The candidate genes are unusually large adhesion/axon-guidance/
  ion-channel/splicing genes; their raw mutation counts inherit the length-proportional
  passenger-mutation bias the project already studies (`hypothesis:h03`, `question:q031`).
- **Histology composition (H4).** CNS/glioma studies (where LSAMP/OPCML/RBFOX1 are recurrent)
  and neuroendocrine neoplasms (MEN1/DAXX/ATRX drivers; CHGA/SYP/NCAM1/INSM1 lineage program)
  in the aggregated cohort inflate neural/neuroendocrine-lineage gene ranks.

— **and that after correcting for both, the neural-gene enrichment largely disappears.** Any
*residual* enrichment that survives length-normalization and CNS+NET exclusion is more
plausibly a **byproduct of oncofetal/developmental de-repression (H3,** `paper:Cao2023`**)**
— diffuse re-expression of the fetal transcriptome, of which neural developmental genes are
the largest class — than evidence of **active neural-circuitry hijacking under positive
selection (H1)**. H1-as-selection is the least-supported reading of a *mutation* signal and
should only be entertained if recurrent, clustered, functional mutations in **canonical**
effectors survive a dN/dS test.

## Proposition Bundle

### Core Propositions

- **P1 (length null, central).** The candidate neural genes have systematically larger
  CDS/gene length than the genome background; after length normalization (mutations per
  callable kb, or dN/dS via the project's dndscv path), they fall out of the top tier. Formally:
  the neural-label enrichment statistic in the top-N raw-count list is not significant in the
  length-normalized list.
- **P2 (CNS-histology contribution).** Excluding CNS/glioma studies from the aggregation
  materially reduces the rank/score of LSAMP, OPCML, RBFOX1 and the neural-label enrichment.
- **P3 (neuroendocrine-histology contribution).** Flagging NET/NEC histologies by OncoTree
  code and excluding them removes MEN1/DAXX/ATRX and neuroendocrine-lineage genes from the
  top tier; MEN1 presence is a positive control for NET contamination.
- **P4 (residual, if any, is developmental not selective).** Whatever neural enrichment
  survives P1–P3 is enriched for **fetal/embryonic-brain** expression over adult-brain
  expression (BrainSpan ratio) and correlates with oncofetal/stemness program activity — the
  H3 signature — rather than showing the recurrence/clustering/dN/dS>1 signature of positive
  selection.
- **P5 (canonical-effector selection test).** The canonical cancer-neuroscience effectors
  (NLGN3, ADRB2/3, CHRM1/3, NTRK1/2, GRIN2A/2B, GAD1, NGF, BDNF) do **not** show genome-wide-
  significant positive selection (dN/dS) across studies; if any do, that is the only
  defensible mutational evidence for H1 and is localized to specific cancer types.

### Label-free commitment

The "neural gene" set used to test P1–P4 must be defined **from data, not human/AI labels**:
tissue/developmental expression enrichment (GTEx, HPA, BrainSpan, Allen atlases). Curated GO
labels are used only as a sensitivity comparator, never as the primary definition. See
`question:q035`.

## Discriminating Evidence

| Observation | Favors |
|---|---|
| Enrichment vanishes after length normalization | P1 (length null) — H5 |
| Enrichment vanishes after CNS exclusion | P2 — H4(CNS) |
| Enrichment vanishes after NET/NEC exclusion; MEN1 disappears | P3 — H4(NET) |
| Residual set is fetal-brain-enriched, correlates with stemness, non-recurrent | P4 — H3 |
| Canonical effectors show dN/dS>1 in specific cancers, recurrent hotspots | P5 — H1 (only defensible mutational H1) |
| Candidate genes show recurrent, clustered, functional mutations after all corrections | would *refute* the null and support H1 |

## Status / Next Steps

Proposed. Operationalized by `doc/plans/2026-06-06-neural-gene-enrichment-meta-analysis-plan.md`
and tasks t215–t221. The length-null (P1) is runnable immediately against existing pipeline
outputs plus the in-repo UniProt protein-length reference — no new data acquisition required.
