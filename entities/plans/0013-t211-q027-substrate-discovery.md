---
type: plan
title: t211 q027 broad therapy-signature substrate discovery
status: proposed
created: '2026-06-01'
updated: '2026-06-01'
id: plan:0013-t211-q027-substrate-discovery
related:
- hypothesis:0009-treatment-induced-signature-frequency-contamination
- question:0027-does-excluding-treatment-signature-high-samples
- question:0024-treatment-exposed-cohort-chemotherapy-signature
- task:t210
- task:t211
---

# t211 q027 broad therapy-signature substrate discovery

## Goal

Discover whether the configured cBioPortal substrate contains a second primary patient cohort suitable for q027 measured therapy-signature-high exclusion.

t210 implemented the q027 machinery and showed that GLASS/SBS11 is a real measured-signature stratum, but the result is non-arbitrating for H10 because it has one contributing study.
This task asks a narrower readiness question: is there another configured study worth adding to a q027 rerun?

## Background

t210 audited only five cohorts selected from the t206-t209 treatment-label work.
That was appropriate for a probe, but the t210 interpretation explicitly limits the "no second substrate" conclusion to that planned candidate set.
The configured project has 198 studies, many of which were not inspected for SBS11/SBS31/SBS35/SBS87 feasibility.

The risk is asymmetric.
Running full per-sample restricted signature assignment across all configured studies is expensive and likely to produce many panel or low-count unevaluable samples.
Stopping at the five-study t210 candidate set may miss a useful second substrate with bland metadata or an unreviewed clinical treatment field.

## Scope

Primary scope is a discovery audit across the configured studies in `code/config/config-full.yml`.
The output is a ranked feasibility table and a recommendation for either:

- no q027 expansion;
- a one-study addition to the existing GLASS q027 config;
- a small multi-study q027 expansion plan if multiple candidates pass.

This is not an H10 verdict run.
It does not change the t210 interpretation unless a follow-up q027 impact rerun is planned, executed, and interpreted separately.

## Inputs

- `code/config/config-full.yml` for the configured study universe and raw `data_dir`.
- Full-config pipeline outputs under `/data/packages/cbioportal/full`.
- Raw cBioPortal clinical files under `/data/raw/cbioportal/{study}/`.
- Existing q027 feasibility code: `code/scripts/audit_q027_therapy_signature_substrate.py`.
- Existing restricted assignment code: `code/scripts/run_restricted_sigprofiler_assignment.py`.
- Existing t207-t209 treatment annotations when available: `/data/packages/cbioportal/full/metadata/samples_treatment_exposure.feather`.

## Approach

### WP1: Cheap configured-study triage

Create or extend an audit script so it can scan all configured studies without a hard-coded five-study candidate list.
For each study and cancer-type stratum, compute:

- total samples;
- broad cancer lookup key used by restricted signature assignment;
- SBS filter-passing variant counts per sample using the existing SigProfiler preparation path;
- number of samples passing the configured WES or matched-normal count floor;
- retained comparator support from `no_detected_treatment_signal` and `positive_naive_or_pretreatment` when treatment annotations exist;
- raw clinical metadata signals for treatment, relapse, recurrence, chemotherapy, radiation, TMZ, platinum, cisplatin, carboplatin, oxaliplatin, and transplant.

The cheap triage must not require running signature assignment.
It should only decide which strata are worth the expensive q027 assignment step.

### WP2: Target-signature expectation rules

Assign candidate target signatures from explicit metadata or cancer/treatment context.

Use conservative rules:

| Signal | Candidate target signatures | Notes |
|---|---|---|
| TMZ / temozolomide / glioma treatment recurrence | `SBS11` | strongest for glioma/TMZ-like alkylation substrates |
| platinum / cisplatin / carboplatin / oxaliplatin | `SBS31`, `SBS35` | require patient denominator, not PDX-primary |
| thiopurine / transplant / immunosuppression therapy where present | `SBS87` | expect rare support in cBioPortal |
| generic chemotherapy with no agent | `SBS11`, `SBS31`, `SBS35` sensitivity-only | do not promote as primary without agent evidence |

If a study has no metadata signal but passes the count-floor gate strongly, keep it in a separate `signature_evaluable_no_treatment_signal` audit tier.
That tier may be useful for future H09 signature reproducibility, but it should not become a q027 treatment-signature candidate without treatment-signature expectation.

### WP3: Feasibility gate

A stratum passes the discovery gate only if all are true:

- primary patient denominator, not PDX sensitivity-only;
- target signatures are present in the configured COSMIC reference;
- at least 25 count-floor-passing samples;
- at least one retained comparator sample after excluding known positive mutagenic treatment labels, unknown treatment metadata, and PDX-only strata;
- at least one explicit treatment-signature expectation signal from WP2.

Report near-misses separately.
For example, a study with many count-floor-passing samples but no clean comparator should be a `no_comparator` near-miss, not a failed null.

### WP4: Assignment recommendation

For each passing or near-passing stratum, write a proposed q027 config fragment:

- `study_id`;
- lookup key;
- target signatures;
- primary vs sensitivity-only status;
- expected output directory suffix;
- reason for inclusion;
- expected power status if added to the GLASS q027 run.

Do not run the q027 impact target as part of this task unless the audit identifies at least one additional primary patient stratum that passes WP3.
If one does pass, write a follow-up implementation task or amendment before running the expanded target.

### WP5: Interpretation

Write `doc/interpretations/2026-06-01-t211-q027-substrate-discovery.md`.
The note should state:

- whether a second q027 primary patient substrate exists in the configured study universe;
- whether the search was exhaustive over configured studies but not over external datasets;
- whether any candidates are only near-misses;
- whether H10 remains non-arbitrating or becomes ready for an expanded q027 impact rerun.

## Key Decisions

### Triage before assignment

Chosen: use mutation-count and metadata triage before restricted assignment.
Rejected: run per-sample therapy-signature assignment for all 198 studies immediately.
Reason: q027 assignment is only informative where count-floor and comparator support exist; the cheap gate avoids spending time on obviously unevaluable panel or PDX strata.

### Metadata can nominate, not decide

Chosen: clinical metadata and study descriptions nominate candidate target signatures.
Rejected: treat treatment metadata as q027 high status.
Reason: q027 is measured-signature-high by definition; metadata is only a substrate-discovery signal.

### Near-misses are deliverables

Chosen: report count-floor-limited, no-comparator, PDX-only, and no-treatment-signal near-misses explicitly.
Rejected: emit only a pass/fail candidate list.
Reason: the main value may be explaining why q027 is underpowered and where future datasets would help.

## Validation

Tests:

- all-config audit mode does not use the hard-coded t210 `DEFAULT_CANDIDATES`;
- unsupported cancer lookup keys are reported rather than silently skipped;
- missing raw clinical files hard-fail or are explicitly marked unavailable depending on config policy;
- count-floor support matches the existing t210 audit for the five original candidates;
- PDX sensitivity-only strata cannot pass the primary gate;
- studies with no target-signature expectation cannot pass the q027 discovery gate even if count-floor support is high.

Workflow checks:

```bash
uv run --frozen --project ~/d/cancer/data-sources/cbioportal pytest code/scripts/tests/test_audit_q027_therapy_signature_substrate.py
uv run --frozen --project ~/d/cancer/data-sources/cbioportal ruff check code/scripts/audit_q027_therapy_signature_substrate.py code/scripts/tests/test_audit_q027_therapy_signature_substrate.py
uv run --frozen --project ~/d/cancer/data-sources/cbioportal ruff format --check code/scripts/audit_q027_therapy_signature_substrate.py code/scripts/tests/test_audit_q027_therapy_signature_substrate.py
uv run --frozen --project ~/d/cancer/data-sources/cbioportal science validate --verbose
```

## Out Of Scope

- New external dataset acquisition.
- De novo extraction of therapy signatures.
- Promoting q027 into canonical frequency tables.
- Treating below-count-floor samples as therapy-signature-negative.
- Reinterpreting the t210 one-study GLASS result as cross-study H10 evidence.

## Acceptance Criteria

- `task:t211` has a committed broad-substrate discovery plan.
- The audit can scan configured studies without relying on the five-study t210 candidate list.
- The report states whether any additional primary patient substrate passes the q027 discovery gate.
- If no substrate passes, the reason is categorized as count-floor-limited, no-comparator, PDX-only, no-treatment-signal, missing-raw-data, or unsupported-signature-context.
- If a substrate passes, the next q027 implementation step is filed separately before any expanded impact run.
