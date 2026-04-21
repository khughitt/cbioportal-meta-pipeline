---
id: "paper:Suehnholz2024"
type: "paper"
title: "Quantifying the Expanding Landscape of Clinical Actionability for Patients with Cancer"
status: "read"
ontology_terms: []
datasets: ["msk-impact", "oncokb"]
source_refs: ["cite:Suehnholz2024"]
related: ["paper:Chakravarty2017", "paper:Zehir2017", "topic:variant-interpretation-oncokb-vus", "topic:cross-study-harmonization"]
created: "2026-04-13"
updated: "2026-04-13"
---

# Quantifying the Expanding Landscape of Clinical Actionability for Patients with Cancer

- **Authors:** Suehnholz SP, et al.
- **Year:** 2024
- **Journal:** Cancer Discovery
- **PMID:** 37849038
- **DOI:** 10.1158/2159-8290.CD-23-0467
- **BibTeX key:** Suehnholz2024

## Key Contribution

Quantifies how much the OncoKB-defined "clinically actionable" fraction of a fixed MSK-IMPACT
cohort grows when the same tumors are re-annotated five years apart. By holding the cohort
constant and varying only the OncoKB snapshot (2017 vs 2022), the paper isolates knowledge-base
drift from cohort composition and establishes a reference magnitude (~3.5x for Level 1/2) for
version-induced shifts in precision-oncology summary statistics.

## Methods

- **Cohort:** 47,271 solid-tumor samples from 42,154 patients, all profiled on MSK-IMPACT and
  released in AACR Project GENIE v11.0; 66 cancer types.
- **Longitudinal OncoKB-version comparison framework:** same variants (SNVs, CNAs, SVs) from
  the fixed cohort annotated twice, once against OncoKB v2017v1.8 (March 2017) and once against
  v2022v3.17 (October 2022).
- Each sample assigned its highest OncoKB evidence level (Level 1 > 2 > 3A > 3B > 4); TMB-H
  defined as ≥10 mut/Mb, MSI-H as MSIsensor >10.
- Parallel curation of FDA-approved oncology drugs 1998–2022 used as an external cross-check on
  the OncoKB-level changes.
- Analysis code and per-sample annotations posted at
  `github.com/oncokb/oncokb-datahub/tree/main/PUBLICATION/2023/CANCER_DISCOVERY`.

## Key Findings

- **Pan-cancer Level 1/2 actionability:** 8.9% (2017) → 31.6% (2022); Level 1 alone 7.7% → 30.2%.
- **Non-actionable-driver-only fraction:** 44.2% → 22.8% (roughly halved).
- **Level 4 (compelling biological evidence):** 8.6% → 20.6%.
- **Level 1 gene count:** 14 genes across 12 cancer types (2017) → 45 genes plus MSI-H and TMB-H,
  including 5 tumor-agnostic approvals (2022).
- **Per-cancer-type range (2022 Level 1):** GIST highest at 84.4%; mesothelioma lowest at 2.1%;
  every tumor type showed an increase.
- **Largest single contributors to the Level 1 jump:** pembrolizumab for TMB-H (+9.2 percentage
  points pan-cancer); sotorasib for KRAS G12C (+12 pp in NSCLC); alpelisib covering ~28% of
  breast cancers via PIK3CA; FGFR inhibitors reaching ~24% of FGFR3-mutant bladder cancers; RET
  inhibitors adding 2–11% in lung and thyroid.
- **Genes dominating the residual non-actionable fraction:** TP53 (43.2% of remaining samples),
  KRAS (19.2%), CDKN2A (12.2%), TERT (10.0%); among genes altered in >1% of samples, 51.5% are
  tumor suppressors and 38.2% oncogenes.

## Relevance

The empirical anchor for OncoKB version-drift in our `cross-study-harmonization` topic.
Re-annotated 47,271 MSK-IMPACT tumors against OncoKB snapshots 5 years apart and showed Level
1/2 standard-care actionability rose from ~8.9% (2017) to ~31.6% (2022). Quantifies why catalog
versions must be pinned in any longitudinal claim derived from cBioPortal-OncoKB-annotated data.

## Limitations

- **Single cohort:** MSK-IMPACT alone — tertiary-referral skew, only 6.5% self-identified
  African American/Black, limited generalizability across populations with different variant
  prevalences.
- **Single knowledge base:** OncoKB only; CIViC, CGI, or JAX-CKB might yield different drift
  magnitudes, and the two snapshots are not independent (later version is a superset plus
  revisions of the earlier).
- **Retrospective and annotation-only:** measures eligibility for matched therapy, not receipt
  or response; the authors note real-world match rates of 5% (Singapore) to 13–18% (US, France,
  Canada) and highly variable response rates even within the same biomarker (e.g., KRAS G12C
  adagrasib: 23% in CRC vs 42.9% in NSCLC).
- **Somatic-only:** germline BRCA1/2 and other predictive germline events excluded, modestly
  underestimating total actionability.

## Follow-up

- Re-run the same two-snapshot comparison on a non-MSK cohort (GENIE consortium minus MSK, or
  TCGA PanCancer) to check whether the 8.9% → 31.6% magnitude is cohort-specific.
- Extend to a third snapshot (e.g., 2024) to test whether actionability growth is linear or
  saturating, and whether the TP53/KRAS/CDKN2A non-actionable core is stable.
- Replicate against CIViC to measure inter-knowledge-base agreement on the *same* variants at
  matched dates, decoupling catalog expansion from catalog choice.
- Propagate the per-gene "level-change" deltas into cBioPortal cohort summaries to flag which
  historical papers' actionable-fraction statistics are most sensitive to re-annotation.
