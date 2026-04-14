# Targeted-panel mutation data — best-practices guide

*As-of: 2026-04-14*

This guide codifies the audit checklist for code that ingests, filters, or aggregates **targeted-
panel somatic mutation data** (MSK-IMPACT, GENIE, FoundationOne, Tempus, Caris, etc.). For
whole-exome data (TCGA / MC3), see `wes-mutation-data.md`. For aggregation across mixed panel +
WES cohorts, see `cross-study-aggregation.md`.

The dominant interpretive risks for panel data are documented in the topic stubs:
- `topic:targeted-panel-sequencing-bias` — panel-content heterogeneity, callability denominator
  (the *problem* side).
- `topic:cross-panel-normalization-methods` — the *methods* side: panel-intersection vs
  callable-denominator weighting; Friends of Cancer Research TMB Harmonization Project
  (Merino 2020 Phase I; Vega 2021 Phase II); Buchhalter 2019 ~1 Mb TMB floor.
- `topic:clonal-hematopoiesis-contamination` — matched- vs unmatched-normal calling differences.
- `topic:cohort-selection-bias-representativeness` — clinical-sequencing cohort biases.

## Sources

**Foundational papers** (full reads at `doc/background/papers/`):

- Cheng DT, et al. 2015. "Memorial Sloan Kettering-Integrated Mutation Profiling of Actionable
  Cancer Targets (MSK-IMPACT): A Hybridization Capture-Based Next-Generation Sequencing Clinical
  Assay for Solid Tumor Molecular Oncology." *J Mol Diagn* 17:251–264. PMID 25801821.
  → analytical-validation reference for the IMPACT-341 panel.
- Zehir A, et al. 2017. "Mutational landscape of metastatic cancer revealed from prospective
  clinical sequencing of 10,000 patients." *Nat Med* 23:703–713. PMID 28481359.
  → MSK-IMPACT 10k cohort + matched-buffy-coat design.
- AACR Project GENIE Consortium. 2017. "AACR Project GENIE: Powering Precision Medicine through
  an International Consortium." *Cancer Discov* 7:818–831. PMID 28572459.
  → 8-center launch + 12-panel structure + 44-gene core.
- Pugh TJ, et al. 2022. "AACR Project GENIE: 100,000 Cases and Beyond." *Cancer Discov*
  12:2044–2057. PMID 35819403.
  → 19-center, 91-panel v9.1; 52% tumor-only; per-assay BEDs in Synapse syn24179663.
- Bandlamudi C, et al. 2026. "Cancer type-specific variation in patterns of driver alterations
  across 50,000 tumors." *Cancer Cell*. PMID 41895280.
  → MSK-IMPACT 50k follow-up; non-canonical-context findings.
- Bolton KL, et al. 2020. "Cancer therapy shapes the fitness landscape of clonal hematopoiesis."
  *Nat Genet* 52:1219–1226. PMID 33106634.
  → CH-driver gene spectrum + therapy-selectivity quantification.

**Reviews:** Chakravarty D, Solit DB. 2021. "Clinical cancer genomic profiling." *Nat Rev Genet*
22:483–501. PMID 33762738.

**Cross-panel normalization / TMB harmonization** (full topic: `cross-panel-normalization-methods`):

- Merino DM, et al. 2020. "Establishing guidelines to harmonize tumor mutational burden (TMB):
  in silico assessment of variation in TMB quantification across diagnostic platforms: phase I
  of the Friends of Cancer Research TMB Harmonization Project." *J Immunother Cancer* 8:e000147.
  PMID 32217756.
  → FoCR Phase I in-silico calibration pipeline; seminal reference.
- Vega DM, et al. 2021. "Aligning tumor mutational burden (TMB) quantification across diagnostic
  platforms: phase II of the Friends of Cancer Research TMB Harmonization Project." *Ann Oncol*
  32:1626–1636. PMID 34606929.
  → Empirical multi-lab calibration; panel-size floor ~667 kb for clinical TMB classification;
  public calibration software released.
- Buchhalter I, et al. 2019. "Size matters: Dissecting key parameters for panel-based tumor
  mutational burden analysis." *Int J Cancer* 144:848–858. PMID 30238975.
  → Independent in-silico down-sampling result reaching ~1 Mb TMB floor.
- Fancello L, et al. 2019. "Tumor mutational burden quantification from targeted gene panels:
  major advancements and challenges." *J Immunother Cancer* 7:183. PMID 31307554.
  → Review of panel-TMB methods; entry point to the calibration literature.

**Data sources:** GENIE per-assay BEDs at Synapse syn24179663 (v9.1) — the only population-scale
open BED corpus; FoundationOne / Tempus / Caris BEDs are proprietary. MSK-IMPACT panel-version
gene lists in cBioPortal study definitions (341 → 410 → 468 → 505).

## Audit checklist

| ID | Item | Applicability | Settled? | Evidence expected |
|---|---|---|---|---|
| panel.01 | Per-study panel identifier preserved through aggregation | any panel-data ingestion | settled | `study_id` or explicit `panel_id` column carried into intermediate feathers |
| panel.02 | Matched-vs-unmatched-normal flag per study | any cross-study aggregation | settled | `matched_normal: bool` column on per-study metadata; documented in `topic:clonal-hematopoiesis-contamination` |
| panel.03 | Per-(study, gene) callability mask used as ratio denominator | any cross-study gene-frequency computation | contested | per-study BED ingested (GENIE: syn24179663; MSK-IMPACT: cBioPortal study def; commercial: fallback to gene list as proxy-BED); **either** `gene_callable: bool` + `callable_bp` columns on `gene_cancer_study.feather` used as the GLMM offset (per `cross-panel-normalization-methods` method B), **or** explicit panel-intersection BED with the loss-of-signal rationale documented (method A). Partial-coverage genes (on some panels, off others) must be handled — see `t076` |
| panel.04 | Panel version drift handled within MSK-IMPACT (341/410/468/505) | any MSK-IMPACT ingestion | contested | per-sample `panel_version` field; for genes added in IMPACT-410/468/505 exclude earlier-cohort samples from denominator (NA rather than 0). FoundationOne (F1 → F1CDx → F1H → F1L) and Tempus xT (V2–V5) have analogous drift — apply same rule. Task: `t070` |
| panel.05 | CH-priority gene flag on outputs | any per-gene aggregation | settled | `ch_priority_gene` boolean column for the 7-gene list (DNMT3A, PPM1D, TET2, TP53, ASXL1, CHEK2, PRPF8) per Bolton2020; or explicit downstream filter recipe |
| panel.06 | Cohort-stage descriptor per study (primary / metastatic / pre-treated) | any cross-study aggregation | contested | `cohort_stage` ingested from cBioPortal study definitions; absence flagged in audit report |
| panel.07 | Synonymous mutation handling consistent across studies | mutation-frequency outputs | settled | explicit filter rule (e.g., "non-synonymous coding only") documented in script header; consistent across studies |
| panel.08 | Variant-call source provenance preserved | any aggregation | settled | per-call source (cBioPortal pre-annotated MAF version, Oncotator-canonical-isoform restriction noted) carried as a column or documented in script header |
| panel.09 | TMB computed against per-panel callable-coding denominator + FoCR-style cross-panel calibration applied | any TMB output | contested | `tmb_callable_mb` per (sample, panel) used as denominator (not a fixed pan-cohort Mb); for cross-panel comparisons apply FoCR Phase-II per-panel linear calibration (Vega 2021) or document why omitted. Panels below ~667 kb callable (Vega 2021) or ~1 Mb (Buchhalter 2019) flagged as unreliable for clinical TMB cutoffs. Task: `t081` |
| panel.10 | Long-tail gene calls cross-checked against an external driver catalog | any per-gene ranking output | contested | Bailey 2018 / CGC / OncoKB overlay applied; `is_known_driver: bool` annotation on outputs |
| panel.11 | Partial-panel-coverage genes (NaN vs 0 disambiguation) handled at pooling | any cross-study pooled rate | contested | with callability joined: fill 0 where `gene_callable=True`; keep NaN where `gene_callable=False`. Replaces `.mean(skipna=True)` which drops on-panel-unmutated studies from the denominator. Task: `t076` |
| panel.12 | Commercial-panel (FoundationOne / Tempus / Caris) BED-fallback policy documented | any cross-study aggregation including commercial panels | contested | since vendor BEDs are proprietary, one of: (a) exclude vendor from cross-panel rate tables, (b) use published gene list as proxy-BED and accept sub-gene bias, (c) infer callability empirically from variant-density. Choice documented per-run |

## Common pitfalls

- **Pooling raw counts across panels.** A gene present on the large hybrid-capture panels but
  absent on the small amplicon panels will look under-mutated in pooled counts. Use per-(study,
  gene) callability masks instead.
- **Treating tumor-only and matched-normal cohorts equivalently.** CH-priority gene rates will
  be inflated in tumor-only cohorts. Stratify by `matched_normal` flag for those genes.
- **Unrecognized panel-version drift.** IMPACT-341 → IMPACT-468 added genes over 5+ years; a
  sample sequenced in 2014 doesn't have callable coverage for genes added in 2018. Naive pooling
  treats this as "not mutated" rather than "not callable."
- **Pan-cancer aggregation hiding cohort-stage differences.** AR mutations at 18% in MSK
  metastatic prostate vs 1% in TCGA primary is not biology — it's cohort selection. Stratify or
  flag.
- **Cross-panel TMB reported without per-panel calibration.** Vega 2021 shows that panel-level
  TMB variance dominates biology at clinical cutoffs without linear calibration. Any TMB value
  pooled across vendors should either carry a calibration citation or a "uncalibrated — not
  comparable cross-vendor" warning.
- **Sub-~667 kb panels used for TMB classification.** Below that callable-coding floor
  (Vega 2021; Buchhalter 2019 ~1 Mb) stochastic noise dominates. Flag such panels explicitly.
- **Panel-intersection applied without signal-loss accounting.** Restricting to the GENIE
  44-gene core at v9.1 (91 panels) discards most long-tail genes. Reporting the post-
  intersection gene count alongside the pre-intersection count makes the trade-off explicit.
