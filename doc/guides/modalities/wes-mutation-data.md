# Whole-exome (WES) mutation data — best-practices guide

*As-of: 2026-04-13*

This guide codifies the audit checklist for code that ingests, filters, or aggregates **whole-
exome somatic mutation data** — primarily TCGA cohorts via MC3, but also non-TCGA WES studies in
cBioPortal. For panel data see `panel-mutation-data.md`.

The dominant audit risks for WES are: **caller-pipeline heterogeneity** (per-study cBioPortal
TCGA MAFs use different callers), **low-purity / contaminated-normal exclusions**, and
**confusing MC3 (unified) vs PanCan12 (legacy single-caller) MAFs**.

## Sources

**Foundational papers:**

- Ellrott K, et al. 2018. "Scalable Open Science Approach for Mutation Calling of Tumor Exomes
  Using Multiple Genomic Pipelines." *Cell Syst* 6:271–281. PMID 29596782.
  → MC3 — the unified TCGA pan-cancer MAF (~3.6M calls / 10,295 tumors / 33 cancer types).
- Bailey MH, et al. 2018. "Comprehensive Characterization of Cancer Driver Genes and Mutations."
  *Cell* 173:371–385. PMID 30096302.
  → 9,423-tumor consensus driver list (Bailey Table S1) computed on MC3.
- Hoadley KA, et al. 2018. "Cell-of-Origin Patterns Dominate the Molecular Classification of
  10,000 Tumors from 33 Types of Cancer." *Cell* 173:291–304. PMID 29625048.
  → 10k-tumor multi-omic clustering on the same MC3 substrate.
- Kandoth C, et al. 2013. "Mutational landscape and significance across 12 major cancer types."
  *Nature* 502:333–339. PMID 24132290.
  → first-generation 12-cancer pan-cancer landscape (pre-MC3).

**Data sources:** `dataset:tcga-mc3` unified MAF at Synapse syn7214402 (controlled-access — all calls + filter
flags) and the open-access PASS-only MAF (3,600,963 variants from 10,295 tumors).

## Audit checklist

| ID | Item | Applicability | Settled? | Evidence expected |
|---|---|---|---|---|
| wes.01 | TCGA portion of cohort uses MC3 unified MAF, not per-study cBioPortal MAFs | any TCGA WES ingestion | contested | MAF-source path or column documented; if per-study MAFs are used, a "did we consider MC3?" justification is in the script header |
| wes.02 | MC3 filter flags handled explicitly | any MC3 ingestion | settled | which of the 8 MC3 filters (`broad_PoN_v2`, `Common_in_ExAC`, `OxoG`, `ContEst`, `StrandBias`, `ndp`, `bitgt`, `NonExonic`) are kept vs dropped is documented |
| wes.03 | Two-caller-agreement requirement preserved | any aggregation of MC3 calls | settled | aggregation does not back-fill single-caller calls; if it does, justified explicitly |
| wes.04 | Low-purity tumor-type caveat surfaced | per-cancer aggregation | settled | PAAD ~33% recovery, LAML ~44% recovery vs WES in MC3 noted in per-cancer outputs as a coverage caveat |
| wes.05 | Mutation-burden range matches expected per-cancer baselines | any per-cancer mutation-rate computation | settled | per-cancer median mut/Mb falls within Kandoth 2013 [@Kandoth2013] / PCAWG 2020 expected range; outliers explained |
| wes.06 | Driver-gene rankings cross-referenced against Bailey 2018 [@Bailey2018] Table S1 | any per-gene per-cancer ranking output | settled | `bailey2018_driver` boolean overlay applied (`code/scripts/annotate_drivers.py`) |
| wes.07 | Saturation-aware interpretation per cancer type | per-cancer driver-discovery claim | contested | per-cancer-type required-N from Lawrence 2014 [@Lawrence2014] cited; long-tail rankings flagged for cancers below saturation |
| wes.08 | Hypermutator handling consistent | any per-sample / per-cancer aggregation | settled | hypermutators (>3000 coding mutations or >10 mut/Mb) flagged; per-cancer means / medians robust to inclusion choice |
| wes.09 | MC3 vs panel comparability not assumed | any cross-modality aggregation | settled | scripts that combine MC3 + panel calls explicitly handle the difference (e.g., panel-restricted intersection); see `cross-study-aggregation.md` |
| wes.10 | Sample-quality QC inherited from upstream | any per-sample analysis | settled | sample exclusions (low purity, low coverage, contaminated normal) documented as inherited from MC3 / cBioPortal upstream filters |

## Common pitfalls

- **Treating cBioPortal "PanCancer Atlas" studies as MC3.** Some are derived from MC3, others
  are legacy single-caller MAFs. Heterogeneous quality. Switching to the unified MC3 MAF
  resolves this for the TCGA portion of any cohort.
- **Re-running MC3 filters without understanding what they catch.** Each filter targets a
  specific failure mode (e.g., `OxoG` = oxidative-damage artifact during library prep). Naive
  filter relaxation reintroduces known artifacts.
- **Comparing MC3 mutation rates to panel mutation rates without normalization.** WES covers
  ~30 Mb of coding sequence; panels cover ~1.5 Mb. Direct comparison overstates panel cohorts'
  mutation-burden tail.
