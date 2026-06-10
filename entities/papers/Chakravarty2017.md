---
type: paper
title: 'OncoKB: A Precision Oncology Knowledge Base'
status: read
created: '2026-04-13'
updated: '2026-04-13'
id: paper:Chakravarty2017
ontology_terms: []
source_refs:
- article:Chakravarty2017
related:
- paper:Cerami2012
- topic:cancer-driver-genes
- topic:variant-interpretation-oncokb-vus
dataset_usage:
- ref: dataset:oncokb
  role: analyzed
  overlap: unknown
---

# OncoKB: A Precision Oncology Knowledge Base

- **Authors:** Chakravarty D, et al.
- **Year:** 2017
- **Journal:** JCO Precision Oncology
- **PMID:** 28890946
- **DOI:** 10.1200/PO.17.00011
- **BibTeX key:** Chakravarty2017

## Key Contribution

Introduces OncoKB, an expert-curated precision-oncology knowledge base developed at MSK that
assigns an oncogenicity call and a therapeutic level-of-evidence to individual somatic
alterations. It unifies FDA labels, NCCN guidelines, disease-specific expert consensus, and
the primary literature into a single variant-level resource intended for point-of-care
interpretation of tumor-sequencing results. OncoKB is directly embedded in cBioPortal and in
the MSK-IMPACT clinical pipeline.

## Methods

Curation is performed variant-by-variant in a tumor-type-specific way by a network of MSK
clinical/research fellows and faculty, with physician sign-off via the Clinical Genomics
Annotation Committee. For each alteration, curators record (1) an **oncogenic effect**
(Oncogenic / Likely Oncogenic / Neutral / Inconclusive), (2) a **mutation (biological)
effect** (Gain-of-Function / Loss-of-Function / Switch-of-Function / Neutral / Inconclusive),
and (3) tumor-type-specific **therapeutic implications** tagged with a level of evidence:

- **Level 1** - FDA-recognized biomarker predictive of response to an FDA-approved drug in this indication.
- **Level 2A** - Standard-care biomarker (per NCCN or equivalent) predictive of response to an FDA-approved drug in this indication.
- **Level 2B** - Standard-care biomarker in **another** indication, predictive of response to an FDA-approved drug.
- **Level 3A** - Compelling clinical evidence in the same tumor type (investigational or off-label).
- **Level 3B** - Compelling clinical evidence in a different tumor type.
- **Level 4** - Compelling biological evidence only.
- **R1 / R2** - Standard-care / investigational biomarkers of **resistance** to a specific therapy.

Supported alteration types include point mutations, indels, fusions, and copy-number events.
Each entry links out to FDA labels, NCCN guidelines, and matched ClinicalTrials.gov trials.

## Key Findings

At publication OncoKB contained annotations for **>3,000 unique alterations across 418
cancer-associated genes**, covering dozens of targeted drugs. Applied to the MSK-IMPACT
cohort of **5,983 primary tumors across 19 cancer types**, **~41% of samples** carried at
least one potentially actionable alteration under any OncoKB level, while only **~7.5%**
carried a Level 1 alteration (standard-care biomarker of response to an FDA-approved drug in
that indication). Actionability rate was highly tumor-type-dependent: very high in melanoma,
thyroid, GIST, and lung adenocarcinoma (driven by BRAF, RET, KIT/PDGFRA, EGFR/ALK/ROS1),
and much lower in pancreatic, colorectal, and many rare cancers. The gap between the 41%
"any-level" and 7.5% "Level 1" figures motivates the explicit tiering: most actionable
findings at the time were off-label or investigational, not standard-care.

## Relevance

OncoKB annotations are baked into cBioPortal. Any variant-level "functional" or "actionable"
filtering our pipeline eventually applies will route through this knowledge base. Relevant for
any filtered-count view we build beyond raw gene frequencies.

Two concrete consequences for this project: (1) "oncogenic" in cBioPortal mutation tables is
the curator's variant-level assertion, not an algorithmic prediction - coverage is biased
toward genes and hotspots that MSK has prioritized; (2) OncoKB tier assignments are
tumor-type-specific, so the same variant can be Level 1 in one cancer and Level 3B or 4 in
another. Any cross-cancer meta-analysis that filters on "actionable" must pin the OncoKB data
version and decide whether level assignment is context-matched or pooled.

## Limitations

- **Manual-curation bottleneck.** Variant-level evidence must be read, classified, and signed off by humans; this limits both breadth (long-tail variants) and speed.
- **Evidence decay / version drift.** Level assignments move as drugs are approved or indications expand; any downstream "% actionable" statistic is only meaningful against a pinned OncoKB snapshot.
- **Gene-centric / cohort-centric bias.** Coverage is strongest for genes recurrently hit in MSK-IMPACT and in common solid tumors; rare cancers, non-coding variants, and non-recurrent missense events are under-represented.
- **Not a passenger filter.** Absence of an OncoKB entry is not evidence that a variant is benign; it may simply be uncurated.
- **Therapeutic focus.** Prognostic and diagnostic biomarkers are captured less systematically than predictive/therapeutic ones.

## Follow-up

Suehnholz et al. 2024 (*Cancer Discovery*) re-annotated 47,271 MSK-IMPACT tumors against OncoKB
snapshots 5 years apart and showed the Level 1/2 standard-care actionability rate rose from
~8.9% (2017) to ~31.6% (2022), while tumors with only non-actionable drivers nearly halved -
quantifying the evidence-decay concern above and illustrating why OncoKB-derived statistics
must be versioned. OncoKB is now updated on roughly a monthly cadence, with an expedited
(< 2-week) path for new FDA approvals via the Clinical Genomics Annotation Committee.
