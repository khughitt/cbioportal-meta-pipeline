---
id: "report:bias-audit-h08-agnostic-association"
type: "report"
title: "Bias Audit: H08 agnostic signature-association artifacts"
status: "proposed"
source_refs:
  - "paper:Alexandrov2020"
  - "paper:Degasperi2022"
  - "paper:AACRGENIEConsortium2017"
  - "paper:Jee2024"
related:
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
  - "method:h08-agnostic-association-model"
  - "search:2026-05-30-ehr-rich-substrates-for-agnostic-signature-association"
  - "dataset:aacr-genie-bpc"
created: "2026-05-31"
updated: "2026-05-31"
---

# Bias Audit: H08 agnostic signature-association artifacts

## Scope

This audit covers the recent H08 hypothesis, method note, DAG source, EHR-rich substrate scan, BPC dataset note, and nearby expression-export implementation.
The review was triggered by the 2026-05-30 commits around H08 and the 2026-05-30 expression-export commits that H08 cites as data substrate.

## Cognitive Biases

### Confirmation Bias

- **Rating:** possible
- **Evidence:** The H08 framing is stronger than the current evidence base.
  It correctly encodes R1-R5 as co-equal rivals, but several support claims rely on the unresolved discussion document and unverified background claims.
  The strongest mitigation already exists: H08a makes known-aetiology recovery a gate before H08b discovery claims.

### Anchoring

- **Rating:** possible
- **Evidence:** There is an active stale task, `t164`, that reserved "h08" for a different topographic contamination-QC hypothesis.
  Reusing H08 for agnostic covariate-signature association risks anchoring future readers to two different hypothesis meanings.

### Availability Bias

- **Rating:** possible
- **Evidence:** The two-track substrate plan favors data already visible in the local pipeline and nearby project notes: MC3/PanCanAtlas for signature-grade analysis and GENIE BPC/MSK-CHORD for EHR-rich covariates.
  This is pragmatic, but the search explicitly says adapter search returned no hits and that ranking is LLM-knowledge-driven, so external dataset coverage is not yet systematic.

### Sunk Cost

- **Rating:** not detected
- **Evidence:** H08 is still proposed and explicitly allows the "hand-labelled map is already optimal" outcome.
  The method does not yet appear locked to one implementation.

### Process Bias

- **Rating:** likely
- **Evidence:** The relevant commits landed within roughly two hours by one author, with multiple docs, tasks, graph metadata, and workflow code changing in a single rapid pass.
  That pace increases self-audit and momentum risk.

## Methodological Biases

### Selection Bias

- **Rating:** possible
- **Evidence:** Dataset selection criteria are stated, but the dataset scan is reconnaissance rather than a systematic search.
  BPC and MSK-CHORD are plausible candidates, but BPC accession, cohort sizes, and MSK-CHORD field/license availability remain partly unverified.

### Survivorship Bias

- **Rating:** possible
- **Evidence:** The search emphasizes usable public/controlled datasets and does not yet record datasets rejected because they lacked clinical richness, lacked mutation data, or were inaccessible.

### HARKing

- **Rating:** likely
- **Evidence:** No H08 pre-registration exists yet.
  The hypothesis identifies pre-registration material, but the positive-control and discovery criteria are not yet locked in a `doc/meta/pre-registration-*.md` artifact.

### Multiple Comparisons / p-hacking Risk

- **Rating:** likely
- **Evidence:** H08 proposes a covariate by signature-factor scan across clinical variables, derived molecular variables, and expression modules.
  The hypothesis states FDR control across the full grid, but the grid definition, module construction, tissue-stratified sample-size floors, held-out replication rule, and primary effect-size ranking are not yet specified.

### Confounding

- **Rating:** likely
- **Evidence:** The method correctly identifies tissue, treatment, study/assay, and ancestry as confounders and explicitly downgrades expression-signature hits to ranked hypotheses.
  The remaining gap is implementation-level: no formal registered causal inquiry or adjustment-set validation exists, and `science.yaml` does not enable the `causal-modeling` aspect despite the method note treating it as active.

#### Confound Severity Matrix

| Confound | Severity | Fixability | Mitigation |
|---|---|---|---|
| Tissue of origin | HIGH | EASY | Require within-tissue primary analysis; report pooled/unconditioned only as a confounding diagnostic. |
| Study/assay/panel footprint | HIGH | HARD | Include study/assay nuisance terms; run leave-one-study and platform-stratified sensitivity; flag artifact signatures. |
| Treatment history | HIGH | HARD | Use BPC/MSK-CHORD where available; otherwise stratify pre/post-treatment status or label as unmeasured. |
| Ancestry/germline repair background | MED | HARD | Include available ancestry/race proxies; avoid causal language when germline variation is unavailable. |
| Reverse expression causation | HIGH | HARD | Treat expression hits as hypotheses; require mediation, temporality, or external validation before upstream-cause claims. |
| Panel mutation-count ceiling | HIGH | EASY | Keep panel data out of per-sample signature inference; use WES/WGS for per-sample H and panels only for pooled/refit analyses. |

### Publication Bias

- **Rating:** possible
- **Evidence:** The literature gate exists as `t177`, but it is currently just a task stub.
  The search must deliberately include null/negative prior attempts at signature-covariate association.

### Corpus Independence (Closure Check)

- **Rating:** likely
- **Artifacts under audit:** H08 hypothesis, H08 method note/DAG, dataset scan, BPC note, discussion note.
- **Shared corpus:** The artifacts mostly derive from the same local discussion, local dataset notes, and model-memory reconnaissance.
- **Independent evidence sources:** Not yet sufficient.
  Spot checks against AACR and Nature sources support BPC/MSK-CHORD as plausible substrates, but H08's association design has not yet been checked against an independent literature scan.
- **Verdict:** Internally coherent, not externally validated.
  Do not treat H08 as more than proposed until `t177` and a pre-registration land.

### Author Independence (Self-Audit Check)

- **Rating:** likely
- **Audit author = artifact author?:** The same agent context appears to have authored or substantively edited the artifacts being reviewed.
- **Verdict:** Self-audit only.
  A cooling-off pass or separate-agent review should run before the artifacts are treated as audited.

## Implementation / Documentation Findings

1. **H08 hypothesis fails validation.**
   `science validate` reports that the hypothesis lacks a required `## Falsifiability` section.
   The current `## Test / Falsification` section carries the right content but not the expected heading.

2. **DAG tracking was corrected during review.**
   The first fix attempted to unignore `*.dot` from a nested `models/.gitignore`, but the root `.gitignore` ignored `models/`, so the nested rule could not re-include the DAG source.
   Follow-up commit `6941dc3` moved the negation to the root ignore rules; `models/h08-agnostic-signature-association.dot` is now tracked.

3. **H08 ID collision / stale task risk.**
   `tasks/active.md` still contains `t164`, which reserves H08 for a different signature/topography contamination-QC hypothesis.
   The new H08 is an agnostic covariate-signature association hypothesis.

4. **Causal-modeling aspect mismatch.**
   The H08 hypothesis says causal-modeling is enabled, but `science.yaml` currently lists only `computational-analysis` and `software-development`.

5. **Placeholder questions are now load-bearing.**
   H08 and the dataset scan cite `q018` and `q019`, but both question files still contain template placeholder bodies.

6. **Expression export aggregate target is incomplete as a provenance target.**
   `all_expression` targets only `expression.parquet` and `clinical.parquet`, while `export_study_expression` also writes `datapackage.json` and `qa_report.md`.
   If those sidecars are deleted after the parquet files are up to date, `all_expression` will not restore them.

## Summary

- **Overall threat level:** elevated
- **Top mitigations:**
  1. Fix the validation and provenance defects: rename H08's falsification section, track the DAG source correctly, and include expression sidecars in `all_expression`.
  2. Resolve research-model drift: either retire/update `t164` or renumber the new H08, and enable `hypothesis-testing` / `causal-modeling` if this project wants those checks.
  3. Convert the promising H08 design into locked evidence: complete `t177`, fill `q018`/`q019`, then pre-register the positive-control and discovery analysis before running associations.
- **Recommended next actions:** Treat H08 as a coherent proposed direction, not a validated finding.
  The main scientific strength is the positive-control gate; the main current weakness is that the scaffolding around it is not yet validation-clean or independent.
