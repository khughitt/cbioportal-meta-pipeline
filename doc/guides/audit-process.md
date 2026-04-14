# Audit process

*As-of: 2026-04-13*

How to audit a `cbioportal` pan-cancer meta-analysis bioinformatics task against the modality
best-practices guides under `doc/guides/modalities/`. Adapted from the MM30 project
(`~/d/r/mm30/doc/guides/audit-process.md`, 2026-04-12).

This pipeline aggregates somatic-mutation data across heterogeneous cBioPortal cohorts (panel,
WES, mixed). The dominant audit risks are **panel-content heterogeneity, cohort-selection bias,
clonal-hematopoiesis contamination, and annotation-version drift** — each of which has its own
modality guide.

---

## 1. Scope determination

### 1.1 Build the file manifest

Identify the target code:
- If the audit is tied to a task (e.g., a pipeline-addition task like t048 MC3 ingestion), use
  that task's file list from its description.
- Otherwise, list the top-level subdirectory or module under review (e.g., `code/scripts/`,
  `code/workflows/`).

Record the manifest inline in the audit report's "File manifest" field (see §4 Report
template). The manifest is authoritative — files outside it are **not audited** in this run.

### 1.2 Match modalities to files

For each file in the manifest, identify which modality guide(s) apply. A single file can have
multiple applicable guides (e.g., a script that filters MAF rows AND aggregates across studies
applies both `panel-mutation-data.md` and `cross-study-aggregation.md`).

**Modality-match heuristics** (apply in order; a file can match multiple):

| Evidence in file | Applicable guide |
|---|---|
| Reads `data_mutations.txt` / per-study MAFs / panel-derived feathers | `panel-mutation-data.md` |
| References MC3 / unified TCGA WES MAFs / multi-caller consensus calls | `wes-mutation-data.md` |
| Aggregates across studies; pooled per-(gene, cancer) computation; meta-analytic combination | `cross-study-aggregation.md` |
| Calls / overlays driver-gene catalogs; runs MutSigCV / dNdScv / hotspot tests | `driver-detection.md` |
| Annotates variants against OncoKB / CGC / hotspots / Genome Nexus / VEP | `variant-annotation.md` |

If a modality guide for an applicable area does not yet exist as a fleshed-out checklist,
record the file as `modality: <name>`, `status: deferred` — findings against that file's
modality are deferred to the phase that produces the guide.

### 1.3 Freeze the manifest

Before starting checklist walks, freeze the manifest + applied-modalities list into the audit
report. Late additions or removals must be logged as deviations.

---

## 2. Execution

For each applicable (file × modality-guide) pair:

1. Walk the guide's checklist table top-to-bottom.
2. For each checklist item, inspect the target code or documentation for the artifact described
   in the guide's "Evidence expected" column.
3. Record one of four outcomes:
   - **pass** — evidence found; item satisfied.
   - **not-applicable** — item does not apply in this context (justify in the
     Non-findings Note column).
   - **fail** — evidence indicates the item is violated. Promote to Findings section.
   - **needs-judgment** — insufficient or ambiguous evidence; the item requires a case call.
     Promote to Findings section with severity `needs-judgment`.

**Tooling for inspection:**
- `Read` for target file content.
- `Grep` for specific patterns (e.g., panel-version flags, OncoKB version stamps,
  `bailey2018_driver`, `ch_priority_gene`, `matched_normal`).
- `uv run snakemake --lint` for Snakemake rule-structure issues.
- Existing test runs / validate.sh output / pipeline output samples — treat as valid evidence;
  do not re-run expensive computations solely for the audit.

**Partial coverage of a checklist item.** Some items have multiple recommended artifacts (e.g.,
"per-study panel-version flag AND per-study matched-normal flag"). If only a subset is present:
- Mark `pass` when the present subset is sufficient to catch the failure mode the item
  targets, **and** the absence of the missing item is noted in Non-findings.
- Mark `needs-judgment` otherwise. Promote to Findings.

---

## 3. Findings

Every `fail` or `needs-judgment` outcome becomes a Finding with all the template fields below
populated.

| Severity | Definition | Pipeline-blocker? |
|---|---|---|
| Critical | Violates an item whose failure invalidates analysis output (e.g., gene-frequency aggregation pools panel + WES counts without callability adjustment; CH-priority genes reported pan-cohort without matched-normal stratification). | Yes |
| Significant | Violates an item where output is interpretable but biased (e.g., OncoKB annotations without version stamping; dNdScv run on panel data without explicit panel flag). | No — requires explicit disposition |
| Minor | Stylistic / documentation / clarity; no analysis-validity consequence. | No — defer freely |

Every finding must cite evidence matching at least one of:
- Output sample showing the violation (e.g., per-(gene, cancer) ratio without panel-callability
  weighting).
- Failing test or validation-script output.
- Code-path inspection (file:line showing the violation).
- Literature-based rationale citing a topic stub or paper stub (e.g.,
  `topic:targeted-panel-sequencing-bias` § Pipeline Implications).

An item without supporting evidence is **not** a finding — it becomes an "Open question" in the
report. Open questions may register discovery tasks but do not block closure.

---

## 4. Report template

Produce one report per audit run at `doc/audits/YYYY-MM-DD-<scope>-audit.md`. Use exactly this
structure (copy the skeleton into a new file per audit):

```markdown
# Audit: <scope>

*As-of: YYYY-MM-DD*

- **Auditor:** <Claude session id + task ref, or human name>
- **Task ref:** <task ID driving this audit, e.g., t048>
- **File manifest:** <inline list or link to a subsection below>
- **Modalities applied:** <list of guide names>
- **Prior audit:** <path or "none — first audit of this scope">

## Summary

<N findings: X Critical, Y Significant, Z Minor. Closure status: <open|met>. One-sentence
statement of what work this audit unblocks and what its next action is.>

## Findings

### F<N>: <short title>  [<Severity>]

- **Checklist item:** <guide>.<id>  (e.g., `panel-mutation-data.md` `panel.07`)
- **Status:** <fail | needs-judgment>
- **Location:** <file:line>
- **Evidence:** <output sample / test / code-path / topic-stub citation>
- **Why this matters:** <impact on analysis validity; 1–3 sentences>
- **Recommended action:** <what to do to resolve>
- **Blocker status:** <blocks <task ref> | requires disposition | defer OK>
- **Resolution status:** <open | fix-in-progress | fixed:<commit> |
  deferred:<task-id> | wont-fix:<rationale>>
- **Re-audit check:** <how a subsequent audit verifies the fix>
- **Linked task:** <task ref or "none">

### F<N+1>: ...

## Non-findings

Every checklist ID × file in scope appears here if it did not become a finding. Exhaustive:

| File | Checklist ID | Status | Note |
|---|---|---|---|
| code/scripts/create_combined_gene_cancer_freq_table.py | panel.01 | pass | per-study panel-version preserved as study_id |
| code/scripts/annotate_drivers.py | annotation.04 | not-applicable | per-variant annotation deferred to OncoKB pipeline; this script handles gene-level overlay only |

## Open questions

<Items the audit could not resolve with available evidence; not findings. Each open question
may register a discovery task but does not block closure.>

## Recommended fix sequence

<Ordered list of fixes with dependencies noted. Group independent fixes.>
```

---

## 5. Task registration

Findings translate to tasks per severity:

- **Critical** — register a fix task **immediately** via `uv run science-tool tasks add`.
  Type `dev`, priority `P0` or `P1` (blocking). Description includes audit-report path +
  finding ID. Add to `--related` the audit task's ID and any unblocked-task IDs.
- **Significant** — register a **disposition** task (fix-now, defer-with-criterion, or
  wont-fix-with-rationale). Priority `P1`/`P2`.
- **Minor** — listed in the audit report only. No task required unless the auditor elects to
  register one.

Every task registered from an audit must include:
- `--related` entry pointing to the audit-task ID.
- Cross-reference to `doc/audits/<path>.md` §F<N> in the description.
- Severity in the description.

---

## 6. Closure

Apply these closure criteria:

1. Every Critical finding has a merged fix **or** a user-accepted mitigation plan recorded in
   the audit report's Resolution status.
2. Every Significant finding has an explicit disposition (fix-now-task-ID, defer-task-ID, or
   `wont-fix` with rationale).
3. Minor findings are triaged (may all be deferred).
4. Unblocked work's next action is unambiguously stated in the report's Summary line (one
   sentence).

Record closure in the Summary: `closure status: met` or `closure status: open — <blocker>`.

The audit **task** may close once the report is written, findings registered, and Critical
fixes either merged or mitigation accepted by the user. Fixes themselves do not have to be
complete for the audit task to close — they run under their own newly-registered task IDs.

---

## 7. Re-audit

Triggered by **material code change** to files in the prior manifest. A re-audit is a diff
against the prior report:

- Items previously `pass`: re-check by inspection. If the code path for that item is unchanged,
  copy forward and note "re-checked, unchanged".
- Items previously `fail` / `needs-judgment`: re-evaluate against current code. New outcome
  recorded; if `fail→pass`, update prior finding's Resolution status to `fixed:<commit>`.
- New files added to manifest: walk the full checklists for applicable modalities.
- Removed files: log under "Scope change" in the re-audit report.

Re-audit reports go at `doc/audits/YYYY-MM-DD-<scope>-audit-reX.md` (X=2, 3, ...) and link to
the prior audit report in the "Prior audit" field. The prior report remains an immutable
historical snapshot.
