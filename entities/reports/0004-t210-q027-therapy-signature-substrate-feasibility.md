---
type: report
title: t210 q027 therapy-signature substrate feasibility audit
status: active
created: '2026-06-01'
updated: '2026-06-01'
id: report:0004-t210-q027-therapy-signature-substrate-feasibility
source_refs:
- code/scripts/audit_q027_therapy_signature_substrate.py
- code/config/config-full.yml
- doc/plans/2026-06-01-t210-q027-therapy-signature-high-exclusion.md
related:
- hypothesis:0009-treatment-induced-signature-frequency-contamination
- question:0027-does-excluding-treatment-signature-high-samples
- task:t210
---

# t210 question 0027 therapy-signature substrate feasibility audit

Verdict: **continue to WP2, scoped to `difg_glass_2019` / SBS11 only**.

At least one primary patient candidate passed the WP1 gate, but the audit did not exhaustively scan all 198 configured studies.
The candidate universe was the five treatment-signature-plausible cohorts named in the t210 plan from the t206-t209 `hypothesis:0009-treatment-induced-signature-frequency-contamination` treatment-label work.
Therefore, "no second substrate" means no second substrate in this planned candidate set, not proof that no other cBioPortal study could support `question:0027-does-excluding-treatment-signature-high-samples` after a broader search.

| Study | Cancer type | Lookup | Primary patient denominator | Target signatures | Target signatures present | Samples | Count-floor-passing samples | Retained floor-passing comparator | WP1 gate | Rationale |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---|
| `difg_glass_2019` | Glioma | `cns` | yes | `SBS11` | yes | 444 | 160 | 31 | yes | TMZ field with treated, explicit-no, and unknown samples |
| `blca_cornell_2016` | Bladder Cancer | `bladder` | yes | `SBS31`, `SBS35` | yes | 72 | 14 | 5 | no | post-chemotherapy and pre-chemotherapy samples |
| `blca_dfarber_mskcc_2014` | Bladder Cancer | `bladder` | yes | `SBS31`, `SBS35` | yes | 50 | 15 | 0 | no | cisplatin-treated bladder cohort |
| `sclc_cancercell_gardner_2017` | Small Cell Lung Cancer | `lung` | no | `SBS31`, `SBS35` | yes | 20 | 20 | 0 | no | treatment-derived PDX sensitivity-only cohort |
| `pptc_2019` | Cancer of Unknown Primary | unsupported | no | `SBS11`, `SBS31`, `SBS35`, `SBS87` | yes | 2 | 0 | 0 | no | pediatric PDX sensitivity-only cohort |
| `pptc_2019` | Embryonal Tumor | unsupported | no | `SBS11`, `SBS31`, `SBS35`, `SBS87` | yes | 39 | 0 | 0 | no | pediatric PDX sensitivity-only cohort |
| `pptc_2019` | Germ Cell Tumor | unsupported | no | `SBS11`, `SBS31`, `SBS35`, `SBS87` | yes | 1 | 0 | 0 | no | pediatric PDX sensitivity-only cohort |
| `pptc_2019` | Glioma | `cns` | no | `SBS11`, `SBS31`, `SBS35`, `SBS87` | yes | 18 | 1 | 0 | no | pediatric PDX sensitivity-only cohort |
| `pptc_2019` | Leukemia | unsupported | no | `SBS11`, `SBS31`, `SBS35`, `SBS87` | yes | 10 | 0 | 0 | no | pediatric PDX sensitivity-only cohort |
| `pptc_2019` | Peripheral Nervous System | unsupported | no | `SBS11`, `SBS31`, `SBS35`, `SBS87` | yes | 35 | 0 | 0 | no | pediatric PDX sensitivity-only cohort |
| `pptc_2019` | Wilms Tumor | unsupported | no | `SBS11`, `SBS31`, `SBS35`, `SBS87` | yes | 13 | 0 | 0 | no | pediatric PDX sensitivity-only cohort |

The two-study `question:0027-does-excluding-treatment-signature-high-samples` arbitration rule was therefore already unreachable after WP1 selected only GLASS.
The downstream impact tables remain useful as reusable scaffolding and as a single-study deliverable-sensitivity check, but the first `question:0027-does-excluding-treatment-signature-high-samples` pass was known to be non-arbitrating before impact aggregation.
