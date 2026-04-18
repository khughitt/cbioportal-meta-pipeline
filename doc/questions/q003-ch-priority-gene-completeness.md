---
id: "question:003-ch-priority-gene-completeness"
type: "question"
title: "Is the 7-gene ch_priority_gene list sufficient to flag CH-related driver inflation in the cross-study mutation tables?"
status: "active"
ontology_terms: []
datasets: []
source_refs:
  - "cite:Poon2021"
  - "cite:Bolton2020"
  - "cite:Coombs2017"
related:
  - "article:Poon2021"
created: "2026-04-18"
updated: "2026-04-18"
---

# Is the 7-gene ch_priority_gene list sufficient to flag CH-related driver inflation in the cross-study mutation tables?

## Summary

The pipeline annotates seven CH-priority genes (DNMT3A, TET2, TP53, ASXL1, CHEK2, PPM1D, PRPF8) per the Bolton 2020 list to flag mutations that may reflect clonal hematopoiesis contamination rather than tumor-intrinsic drivers. Poon et al. 2021 (Nature Genetics) show that in healthy blood, known SNV driver genes explain only ~30% of the total genome-wide synonymous passenger burden, implying ~70% of positively selected clonal expansions involve genes or mutation types outside standard CH gene panels. This raises the question of whether the 7-gene list meaningfully bounds the CH inflation risk in our cross-study aggregation.

## Why It Matters

- Genes outside the 7-gene list that are recurrently mutated via CH (but not flagged) will appear as spuriously elevated drivers in studies without matched normals, biasing cross-study frequency tables for blood lineage cancers and contaminated solid tumor data.
- If the unexplained ~70% of blood selection maps to specific loci (e.g., splicing factors, additional epigenetic regulators), those genes may cluster together in our gene x cancer matrix in a way that reflects CH architecture rather than oncogenic signal.
- Under-flagging inflates false-positive driver counts, particularly in hematologic malignancy studies where the tumor and the background blood both carry CH mutations.

## Current Evidence

- **Poon 2021:** ~30% of synonymous passenger excess in healthy blood is explained by known SNV drivers; ~70% is attributable to uncharacterized or non-SNV selection. (Source: abstract + web summaries; [UNVERIFIED from full text].)
- **Bolton 2020:** The 7-gene list was selected for clinical CH relevance (therapy-associated CH, adverse cardiovascular outcomes) — not for completeness of somatic selection coverage.
- **Coombs 2017/2018:** DNMT3A alone accounts for ~64% of identified CH driver hits in MSK-IMPACT solid tumor cohorts; TP53 ~4%. This suggests even within known CH drivers, concentration is high — but it also means many CH events in blood studies are DNMT3A-driven and are flagged.
- **Ptashkin 2018:** ~5% patient-level CH misattribution without matched normals in MSK-IMPACT; this rate would be higher in studies using older, smaller panels.

## Thoughts

- The ~70% "unexplained" figure likely includes indel-driven CH (e.g., SF3B1, U2AF1, SRSF2 splicing factor hotspots), CNV-driven CH (mosaic chromosomal alterations), and possibly very low-frequency coding drivers not yet catalogued. The actual gene list for SNV-driven unexplained CH may be smaller than "70%" implies.
- For our pipeline's practical purposes, the most impactful gap is probably in hematologic studies. Solid tumor CH contamination is partially mitigated for studies in `matched_normal_studies`.
- A pragmatic extension: add a broader "CH-candidate" tier (e.g., from large CH GWAS / Bick 2020 / Kessler 2022 results) and flag it separately with lower confidence than the 7-gene Bolton list.

## Connections to Project

- Related hypotheses: none formalized yet — candidate for a new hypothesis about CH signal in cross-study aggregation.
- Required data or analyses: (1) Map Poon 2021's unexplained selection fraction to specific gene candidates using the literature on large-scale CH sequencing (Bick 2020 UK Biobank CH GWAS, Kessler 2022, Fabre 2022 clonal dynamics). (2) Check whether adding a broader CH gene list materially changes driver rankings in hematologic cancer studies in the pipeline.
- Priority level: medium — the current 7-gene list handles the most prevalent CH signals (DNMT3A especially); the gap matters more for precision than for the gross cross-study patterns.

## Related

- Topic notes: `topic:clonal-hematopoiesis-contamination`
- Article notes: `article:Poon2021`, `article:Bolton2020 (cite:Bolton2020)`
- Methods/Datasets: `code/scripts/annotate_ch.py`; `matched_normal_studies` config key
