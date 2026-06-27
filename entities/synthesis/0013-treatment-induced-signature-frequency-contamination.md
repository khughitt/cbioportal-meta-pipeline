---
type: synthesis
title: 'Synthesis: h10-treatment-induced-signature-frequency-contamination'
status: active
created: '2026-06-02'
updated: '2026-06-02'
id: synthesis:0013-treatment-induced-signature-frequency-contamination
report_kind: hypothesis-synthesis
hypothesis: hypothesis:0009-treatment-induced-signature-frequency-contamination
generated_at: 2026-06-02 09:52:22+00:00
source_commit: 037f0ab2d3c84ecc56bebd843e361c1a9dfbfa66
provenance_coverage: thin
---

## State

hypothesis:0009-treatment-induced-signature-frequency-contamination proposes that treated/relapsed
cBioPortal cohorts inflate apparent gene-by-cancer mutation frequencies via iatrogenic signatures
(SBS11, SBS31, SBS35, SBS87). As of 2026-06-01 the hypothesis remains **proposed and unresolved**.

The exposure-label substrate is now executable at full-config scale. A scan of 167 non-TCGA studies
(interpretation:0029-t206-treatment-exposure-audit) identified 11 broad treatment-exposed
study candidates and a narrower mutagenic-treatment stratum; only `blca_dfarber_mskcc_2014` was
flagged as a whole-study primary mutagenic label, with `difg_glass_2019` and `blca_cornell_2016`
added at sample level by t208 and t209. The full-config impact run
(`interpretation:0030-t207-h10-treatment-impact-full-config`) covers 383,477 samples across 198
studies; the primary mutagenic-treatment label reaches 280 samples spanning bladder cancer and
glioma. Interpretable `delta_mutagenic_primary` rows exist for bladder and glioma, with median
absolute delta 0.004 and 95th-percentile 0.077, and top-row deltas near -0.17 for bladder-specific
genes — suggestive of local denominator sensitivity but not yet evidence of signature-shaped
driver-frequency inflation (`interpretation:0032-t208-h10-sample-level-mutagenic-rules`).

The measured-signature arm (question:0027-does-excluding-treatment-signature-high-samples) found 36
SBS11-high GLASS samples with strong SBS11 exposure; all `q027` impact rows are
`underpowered_non_arbitrating` because only one primary patient study passed the discovery gate
(`interpretation:0034-t210-q027-therapy-signature-high-exclusion`). A broad substrate scan of
all 198 configured studies confirmed no second adequate patient cohort exists in the current
configured substrate (`interpretation:0035-t211-q027-substrate-discovery`).

## Arc

Arc reconstruction is limited because t181 and t206 lack `prior_interpretations` chains, making the
earliest investigative links partially opaque.

Work on `h10` began with t181 adding explicit treatment-exposure fields to the `h08` covariate
substrate, establishing that MC3/TCGA carries no study-level treated-cohort confound but retains 55
patient-level neoadjuvant positives — closing the `h08`-facing part of
question:0024-treatment-exposed-cohort-chemotherapy-signature without yet testing `h10`
(interpretation:0027-t181-treatment-exposure-stratum).

The investigation then moved to non-TCGA scope. t206 audited 167 cBioPortal studies and produced a
layered label design distinguishing broad cohort-composition flags from the narrower
mutagenic-treatment stratum relevant to SBS11/SBS31/SBS35/SBS87
(interpretation:0029-t206-treatment-exposure-audit). t207 attempted a full-config run, was
briefly blocked by two missing raw studies, resolved those, and delivered the first end-to-end
exposure-label impact table — establishing methodology rather than biology
(`interpretation:0030-t207-h10-treatment-impact-full-config`). t208 added deterministic
sample-level rules for `difg_glass_2019` (TMZ) and `blca_cornell_2016` (post-chemotherapy), growing
the primary mutagenic label from 50 to 280 samples, but exposing a comparator-definition gap for
GLASS blank-TMZ samples (`interpretation:0032-t208-h10-sample-level-mutagenic-rules`). t209
repaired that gap by introducing `treatment_metadata_unknown` and `positive_naive_or_pretreatment`
sample-level rule targets, semantically cleaning the no-detected comparator
(`interpretation:0033-t209-h10-sample-level-unknown-naive-rules`).

The investigation then branched to the measured-signature arm. t210 ran the distinct
question:0027-does-excluding-treatment-signature-high-samples arm against measured SBS11/SBS31/
SBS35/SBS87 exposure, finding 36 strong SBS11-high GLASS samples but a one-study result that
correctly pre-classified as non-arbitrating
(`interpretation:0034-t210-q027-therapy-signature-high-exclusion`). t211 broadened the
feasibility search to all 198 configured studies and confirmed no second primary patient substrate
passes the discovery gate under the conservative rules
(`interpretation:0035-t211-q027-substrate-discovery`). The current epistemic position is that
`h10` has passed an infrastructure gate and produced a useful one-study GLASS sensitivity, but remains
unresolved as a cross-study biological claim.

## Research Fronts

**Live questions.** question:0024-treatment-exposed-cohort-chemotherapy-signature is partially
answered: the exposure-label substrate is executable and covers known cohorts, but audit recall over
109 no-metadata-signal studies is unmeasured and the confirmed-naive contrast remains underpowered.
question:0027-does-excluding-treatment-signature-high-samples is technically answered for GLASS but
scientifically non-arbitrating; no second primary patient substrate exists in the current configured
study set.

**Open tasks.** All bundle tasks (t181, t206, t207, t208, t209, t210, t211) are marked done. No
open backlog tasks remain for `h10` as of this synthesis.

**Next investigative options** (from `interpretation:0035-t211-q027-substrate-discovery` and
`interpretation:0034-t210-q027-therapy-signature-high-exclusion`):
- A GLASS-specific clinical timing audit to determine whether SBS11-high status is separable from
  recurrence/progression and TMZ episode within GLASS.
- Acquisition of an external treatment-rich WES/WGS substrate to enable a second primary patient
  `q027` contrast.
- Pause `h10`/`q027` at the current non-arbitrating result pending other project priorities.

**Knowledge gaps.**
- `topic:clinical-translational-signatures` — 0 papers vs 2 questions referencing it
  (question:0024-treatment-exposed-cohort-chemotherapy-signature,
  question:0027-does-excluding-treatment-signature-high-samples)
