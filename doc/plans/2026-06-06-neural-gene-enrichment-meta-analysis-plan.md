# Plan: data-driven test of the "neural gene" mutation-enrichment observation

- **Date:** 2026-06-06
- **Hypothesis:** `hypothesis:0012-neural-gene-enrichment-length-histology-artifact` (null-first)
- **Synthesis:** `doc/papers/synthesis-2026-06-06-cancer-neuroscience.md`
- **Questions:** q032 (length null), q033 (CNS exclusion), q034 (NET exclusion), q035 (label-free
  definition), q036 (oncofetal H3), q037 (canonical-effector dN/dS H1)
- **Tasks:** t215–t221 (group `neural-gene-meta-analysis`)

## 0. Framing

The motivating observation — neural genes (NKAIN2, KCNIP4, TAFA2, RIT2, CALN1, RBFOX1, LSAMP,
SGCZ, OPCML) topping a mutation-frequency view — comes from **unreliable notes** and must
first be **reproduced from the pipeline**. The 21-paper cancer-neuroscience review concluded the
field's biology is non-mutational and names none of these genes, so the design is **null-first**:
disprove the cheap confounds (length, histology) before entertaining biology. Prefer
**data-driven / empirical** gene definitions over human/AI labels throughout (q035).

The candidate gene list is a *hint*. The real target is the **enrichment statistic** of a
data-driven neural-gene set among top-mutated genes, and how it moves under each correction.

## 1. Reproduce the observation (gate)

- **t215.** Regenerate the top-mutated-gene view from current pipeline outputs
  (`gene_cancer_study_annotated.feather`, `gene_cancer_study_ratio_annotated.feather`). Confirm
  whether the candidate genes actually rank highly, on which metric (raw count vs sample-ratio),
  in which config (10k-genes / full / pan-cancer), and from which studies. **If the signal does
  not reproduce, stop** and record that the notes were spurious.
- Record exact ranks + contributing studies for the 9 candidates as the baseline.

## 2. Build the label-free neural-gene score (q035)

- **t216.** Per-gene **neural-enrichment score** from expression atlases, no GO labels:
  - GTEx: max/mean Z over brain regions and tibial nerve vs other tissues; tau specificity.
  - Human Protein Atlas tissue-specificity category.
  - (Optional) Allen Brain Cell Atlas / PanglaoDB cell-type marker overlap as a second view.
  - Partition into **CNS-structural**, **PNS/autonomic**, **neuroendocrine-lineage** sub-scores
    (Cortese2020 distinction) — the candidates are mostly CNS-structural.
- **Validation:** the canonical effectors (NLGN3, ADRB2, NTRK1/2, CHRM3, GRIN2A/B, NGF, BDNF)
  should score high (positive control); housekeeping genes low (negative control). Report ROC.
- Output: a reusable `gene_neural_enrichment.feather` covariate.

## 3. Confound corrections (the core tests)

Each step recomputes the **neural-enrichment-of-top-mutated** statistic and the candidate-gene
ranks, reporting the delta.

- **t217 — gene-length null (q032, P1).** Normalize to mutations-per-callable-kb and to the
  project's dndscv background; reuse `data/uniprotkb_hsapiens_protein_lengths.tsv.gz` + Ensembl
  CDS length. Test: does the neural-enrichment statistic remain significant after length
  adjustment? Wilcoxon of candidate-gene length vs background. **Primary, runnable now.**
- **t218 — CNS exclusion (q033, P2).** Re-aggregate with CNS/glioma cancer types removed
  (cancer_type / OncoTree filter). Quantify each excluded study's contribution to LSAMP/OPCML/
  RBFOX1.
- **t219 — neuroendocrine exclusion (q034, P3).** Enumerate NET/NEC OncoTree codes present in
  the pipeline studies; add `is_neuroendocrine_histology` flag; recompute with NEN excluded.
  MEN1 rank is the positive-control canary for NEN contamination.

## 4. Interpret the residual (only if signal survives §3)

- **t220 — oncofetal vs selection (q036/q037, P4/P5).**
  - **H3 test:** BrainSpan fetal-vs-adult brain expression ratio for the residual set; correlate
    residual-gene mutation with stemness/oncofetal activity (AFP/GPC3, Wnt/Hh) in matched-
    expression studies; recurrence/clustering check (diffuse + fetal-enriched ⇒ H3).
  - **H1 test:** run the canonical-effector set through dndscv per cancer type; NF1 = positive
    control; report q-values. Recurrent/clustered/dN/dS>1 in effectors ⇒ the only defensible
    mutational H1; localize to cancer types.

## 5. QA / sanity checks (throughout)

- Matched- vs unmatched-normal stratification (germline-leak control; reuse
  `matched_normal_studies`) — rules out H5-via-germline for candidate genes.
- Hypermutator/MSI stratification (reuse `is_hypermutator`) — long genes accumulate counts in
  hypermutators; check enrichment is not hypermutator-driven.
- Common-fragile-site overlap for candidates (ties to q014/q031).
- Per-study leave-one-out: is the signal one study or many?
- Sensitivity: data-driven neural set vs GO-label set should agree on direction (q035).

## 6. Datasets

- **In-repo / existing:** pipeline annotated feathers; `uniprotkb_hsapiens_protein_lengths`;
  dndscv path; Bailey2018 driver overlay; hypermutator + matched-normal annotations.
- **To acquire (reference, label-free definition):** GTEx (brain + nerve), Human Protein Atlas,
  BrainSpan / Allen Developing Human Brain Atlas (fetal, for H3), Allen Brain Cell Atlas /
  PanglaoDB markers. OncoTree code list for NEN/CNS flagging.

## 7. Decision tree (expected)

```
reproduce? ──no──▶ notes spurious; close
   │yes
length-normalize ──signal gone──▶ H5 confirmed (most likely); close mutational interpretation
   │survives
CNS-exclude ──gone──▶ H4(CNS) confirmed
   │survives
NET-exclude ──gone──▶ H4(NET) confirmed
   │survives (residual)
fetal-enriched + non-recurrent ──▶ H3 (oncofetal byproduct)   [report as lead]
effectors dN/dS>1 ──────────────▶ H1 (selected neural hijacking) [strongest claim; localize]
```

Most probable outcome given the literature review: **H5 + H4 account for the bulk**, with at
most a small fetal-enriched (H3) residual; mutational-H1 expected to be negative except NF1.
