---
id: "question:q006-ch-priority-gene-completeness"
type: "question"
title: "Is the 7-gene ch_priority_gene list sufficient to flag CH-related driver inflation in the cross-study mutation tables?"
status: "active"
ontology_terms: []
datasets: []
source_refs:
  - "paper:Poon2021"
  - "paper:Bolton2020"
  - "paper:Coombs2017"
  - "paper:LeeSix2018"
related:
  - "paper:Poon2021"
  - "paper:LeeSix2018"
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

- **Poon 2021:** The 20 most common high-fitness CH variants explain only ~10% of the observed density of high-VAF synonymous passengers in blood; the full 468-gene MSK-IMPACT panel recovers only ~5% more; ~90% of positive selection in blood remains attributable to mutations outside standard cancer-associated gene panels. (Source: full-text PDF verified 2026-04-18.)
- **Lee-Six 2018:** Whole-genome phylogenetic reconstruction of 140 single HSC/progenitor colonies from a single healthy 59-year-old shows effective HSC pool size 50,000–200,000 and dN/dS = 1.001 (neutral drift — no CH drivers in this subject). This population size means a clone must achieve a fitness advantage s >> 1/N_eff (~1/100,000 per division) to rise to detectable VAF; neutral drift alone cannot explain CH clones observable at >0.1% VAF in a 60-year-old. Therefore, the "unexplained ~90% of selection" in Poon 2021 represents genuine positive selection from genes not yet catalogued — not an artifact of drift. (Source: full-text XML via Europe PMC, verified 2026-04-18.)
- **Bolton 2020:** The 7-gene list was selected for clinical CH relevance (therapy-associated CH, adverse cardiovascular outcomes) — not for completeness of somatic selection coverage.
- **Coombs 2017/2018:** DNMT3A alone accounts for ~64% of identified CH driver hits in MSK-IMPACT solid tumor cohorts; TP53 ~4%. This suggests even within known CH drivers, concentration is high — but it also means many CH events in blood studies are DNMT3A-driven and are flagged.
- **Ptashkin 2018:** ~5% patient-level CH misattribution without matched normals in MSK-IMPACT; this rate would be higher in studies using older, smaller panels.

## Thoughts

- Lee-Six 2018's N_eff ~ 100,000 HSCs makes drift-driven large clones essentially impossible (a clone must achieve s > ~0.05/year to reach 1% VAF within a human lifetime starting from a single cell). The "unexplained 90%" of selection in Poon 2021 therefore must arise from real positive selection in genes not yet in standard CH panels — not from drift noise.
- The ~90% "unexplained" figure likely includes indel-driven CH (e.g., SF3B1, U2AF1, SRSF2 splicing factor hotspots), CNV-driven CH (mosaic chromosomal alterations), and possibly very low-frequency coding drivers not yet catalogued. The actual gene list for SNV-driven unexplained CH may be smaller than "90%" implies if non-SNV mechanisms account for a significant fraction.
- For our pipeline's practical purposes, the most impactful gap is probably in hematologic studies. Solid tumor CH contamination is partially mitigated for studies in `matched_normal_studies`.
- A pragmatic extension: add a broader "CH-candidate" tier (e.g., from large CH GWAS / Bick 2020 / Kessler 2022 results) and flag it separately with lower confidence than the 7-gene Bolton list.

## Connections to Project

- Related hypotheses: none formalized yet — candidate for a new hypothesis about CH signal in cross-study aggregation.
- Required data or analyses: (1) Map Poon 2021's unexplained selection fraction to specific gene candidates using the literature on large-scale CH sequencing (Bick 2020 UK Biobank CH GWAS, Kessler 2022, Fabre 2022 clonal dynamics). (2) Check whether adding a broader CH gene list materially changes driver rankings in hematologic cancer studies in the pipeline.
- Priority level: medium — the current 7-gene list handles the most prevalent CH signals (DNMT3A especially); the gap matters more for precision than for the gross cross-study patterns.

## Related

- Topic notes: `topic:clonal-hematopoiesis-contamination`
- Article notes: `paper:Poon2021`, `paper:LeeSix2018`, `paper:Bolton2020 (cite:Bolton2020)`
- Methods/Datasets: `code/scripts/annotate_ch.py`; `matched_normal_studies` config key
- Key quantitative anchor: Lee-Six 2018 N_eff ~100,000 HSCs means drift cannot explain observable large CH clones — confirming Poon 2021's "unexplained selection" is genuine positive selection from uncharacterized drivers, not noise.
