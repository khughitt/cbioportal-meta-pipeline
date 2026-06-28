---
type: interpretation
title: t211 q027 broad therapy-signature substrate discovery
status: active
created: '2026-06-01'
updated: '2026-06-28'
id: interpretation:0035-t211-q027-substrate-discovery
source_refs:
- code/scripts/audit_q027_therapy_signature_substrate.py
- code/scripts/tests/test_audit_q027_therapy_signature_substrate.py
- code/config/config-full.yml
- doc/plans/2026-06-01-t211-q027-substrate-discovery.md
- results/q027-substrate-discovery-2026-06-01/therapy_signature_substrate_feasibility.tsv
- results/q027-substrate-discovery-2026-06-01/therapy_signature_substrate_feasibility.md
related:
- hypothesis:0009-treatment-induced-signature-frequency-contamination
- question:0027-does-excluding-treatment-signature-high-samples
- question:0024-treatment-exposed-cohort-chemotherapy-signature
- task:t210
- task:t211
---

# Interpretation: t211 `q027` broad therapy-signature substrate discovery

Project links: this interpretation supports
`hypothesis:0009-treatment-induced-signature-frequency-contamination`,
`question:0027-does-excluding-treatment-signature-high-samples`, and
`question:0024-treatment-exposed-cohort-chemotherapy-signature`.
It extends the `task:t210` measured-signature arm through `task:t211`.

## Verdict

**Verdict:** [?] The configured-study discovery audit found no second primary patient `q027` substrate beyond GLASS.

t211 broadened the t210 feasibility search from the five planned treatment-signature candidates to all 198 configured studies in `code/config/config-full.yml`.
The audit produced 684 study/cancer-type strata.
Only `difg_glass_2019` passed the `q027` discovery gate, so the t210 measured-signature arm remains a one-study GLASS/SBS11 result and remains non-arbitrating for `H10`.

This is a stronger negative readiness result than t210, but it is still not an `H10` biological verdict.
It says the current configured cBioPortal substrate does not provide a second adequate patient cohort for SBS11/SBS31/SBS35/SBS87-high exclusion under the conservative count-floor, comparator, and explicit-treatment-expectation rules.

## Audit Scope

The audit scanned the full configured study list, not only the t210 five-study candidate set.
It used cheap metadata/count triage and did not run per-sample therapy-signature assignment for every configured study.
Studies without treatment-signature metadata expectation were reported as no-signal strata rather than pushed through expensive SBS context counting.

The final discovery table has:

| Category | Strata |
|---|---:|
| Total audited study/cancer strata | 684 |
| Passed `q027` discovery gate | 1 |
| No treatment-signature expectation | 417 |
| Unsupported cancer-type lookup | 222 |
| Candidate/near-miss rows with supported lookup | 45 |

The `transplant` keyword was deliberately not allowed to nominate SBS87 by itself after the first pass showed that post-transplant disease labels can create whole-study false positives.
SBS87 discovery now requires explicit thiopurine drug names such as thiopurine, azathioprine, or mercaptopurine.

## Passing Stratum

| Study | Cancer type | Targets | n | Count-floor passing | Retained comparator | Gate |
|---|---|---|---:|---:|---:|---|
| `difg_glass_2019` | Glioma | SBS11/SBS31/SBS35 | 444 | 160 | 31 | pass |

This is not a new substrate.
It is the same GLASS glioma substrate used by t210.
The broad metadata scan also saw a platinum token in the raw GLASS text, so the discovery row lists SBS31/SBS35 in addition to SBS11.
The already-run t210 `q027` arm remains the cleaner configured GLASS pass because it used the planned TMZ/SBS11 target.

## Near Misses

The best non-GLASS candidates do not pass the gate.

| Study | Cancer type | Targets | Reason not ready |
|---|---|---|---|
| `blca_dfarber_mskcc_2014` | Bladder Cancer | SBS31/SBS35 | 15 count-floor-passing samples but 0 retained comparator samples. |
| `blca_cornell_2016` | Bladder Cancer | SBS31/SBS35 | 14 count-floor-passing samples and 5 retained comparator samples, below the 25-sample floor. |
| `brain_cptac_2020` | CNS Cancer | SBS11/SBS31/SBS35 | 1 count-floor-passing retained comparator sample. |
| `sclc_cancercell_gardner_2017` | Small Cell Lung Cancer | SBS11/SBS31/SBS35 | 20 count-floor-passing samples but PDX sensitivity-only and no retained comparator. |
| `pptc_2019` | Glioma / lymphoblastic strata | SBS31/SBS35 | PDX sensitivity-only and count/comparator limited. |

Several generic chemotherapy studies have non-zero count-floor support, but generic chemotherapy metadata is not treated as an explicit `q027` treatment-signature expectation.
Those rows are useful triage information, not primary `q027` substrates.

## Implementation Notes

The audit script now supports `--all-config-discovery`.
That mode builds candidates from configured raw metadata instead of the hard-coded t210 candidate list, supports wildcard cancer-type lookup scanning, and keeps the original t210 path strict by default.

Two full-config integration issues were repaired during t211:

- sample identifiers are normalized to strings before mutation counting and treatment-annotation joins, because some cBioPortal studies serialize numeric-looking sample IDs differently across files;
- broad-discovery mode records mutation-context count errors as explicit non-passing rows instead of aborting the entire 198-study scan.

These changes are discovery-audit behavior only.
They do not modify `q027` assignment, `q027` impact tables, or canonical frequency outputs.

## Implications

The configured cBioPortal substrate cannot currently arbitrate `q027` through a second patient cohort.
The project should not run an expanded `q027` impact target yet, because it would still be GLASS-only after the discovery pass.

The remaining `H10` options are now clearer:

1. Pause `H10`/`q027` with the current non-arbitrating result.
2. Run a GLASS-specific timing audit to ask whether SBS11-high status is separable from recurrence/progression and TMZ episode.
3. Acquire or add an external treatment-rich WES/WGS substrate before attempting another cross-study `q027` impact pass.

The strongest immediate scientific move is the GLASS timing audit if `H10` remains active.
It will not solve cross-study power, but it can determine whether the one observed `q027` signal is at least clinically interpretable inside GLASS.
