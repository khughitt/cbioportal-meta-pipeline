# Cancer Meta-Project Design

**Date:** 2026-04-30
**Status:** Draft for review
**Scope:** New umbrella project (`~/d/cancer/`) spanning cancer + pre-cancer research,
with cbioportal and mm30 migrated in as sub-projects, plus upstream changes to the
science framework (`~/d/science/`) to support a meta-project model.
**Successor doc:** Implementation plan(s) to follow per phase.

> Note on location: this design lives in `cbioportal/doc/plans/` because cbioportal is
> the only existing project at design time. Once the umbrella is materialized, the
> canonical home is `~/d/cancer/meta/doc/plans/2026-04-30-cancer-meta-project-design.md`
> (move with a redirect note left here).

---

## 1. Vision

Reframe what has been a narrow cBioPortal-focused meta-analysis into a sustained,
multi-project effort to build a **multiscale knowledge graph + research framework**
spanning cancers, pre-cancers, and adjacent clonal disorders. The goal is a *process*
for continuously evolving understanding, not the answer to any one question.

Three ideas anchor the framing:

- **Multiscale**: investigate cancer at the pan-cancer level (commonalities), at the
  level of cancer-type subsets, and within specific cancer types — without privileging
  any one scale.
- **Pre-cancer + adjacent disorders**: include disorders that overlap cancer biology
  (e.g., clonal hematopoiesis, MGUS, Barrett's esophagus) without requiring them to be
  labelled "cancer" or "pre-cancer."
- **Evolution as cross-cutting lens**: somatic evolution unifies cancer development
  across individuals and populations, subclone selection, and drug-resistance
  trajectories.

The umbrella connects to existing focused efforts (cbioportal, mm30) and absorbs new
ones lazily as inquiry justifies them. It is *logical integration*, not a wholesale
takeover of the contributing projects.

## 2. Architecture

### 2.1 Directory layout (after migration)

```
~/d/cancer/                        # symlink to /mnt/ssd/Dropbox/cancer/
  meta/                            # role: meta
  cancer-types/
    multiple-myeloma/              # ex-mm30; role: cancer-type
  data-sources/
    cbioportal/                    # ex-cbioportal; role: data-source
  mechanisms/
    evolution/                     # role: mechanism — day-1 unifying lens
  conditions/
    pre-cancer/                    # role: condition — promoted from cbioportal
```

Physical home: `/mnt/ssd/Dropbox/cancer/`, with `~/d/cancer` as a symlink. Consistent
with current cbioportal Dropbox setup.

### 2.2 Role taxonomy

| Role | Definition | Day-1 examples | Future examples |
|---|---|---|---|
| `meta` | Umbrella integration, foundational questions, cross-project synthesis | `meta/` | (one per umbrella) |
| `cancer-type` | One cancer (or natural cancer grouping) studied in depth | `multiple-myeloma/` | `breast/`, `lung-adeno/`, `aml/` |
| `data-source` | Pipeline / evidence stream feeding others | `cbioportal/` | `depmap/`, `pcawg/`, `tcga-mc3/` |
| `mechanism` | Biological process / dynamic operating across cancers (overlaps with the broader notion of "process") | `evolution/` | `chromosomal-instability/`, `replication-stress/`, `metabolism/`, `drug-resistance/`, `plasticity/`, `metastasis/`, `immune-evasion/` |
| `condition` | Disease state adjacent to cancer with its own natural history (overlaps with the broader notion of "disease state") | `pre-cancer/` | `clonal-hematopoiesis/`, `mgus/` |

Vocabulary is extensible: `role` is a free-form string, not an enum. New roles
(`host-context`, `model-system`, `methodology`) can be added later without breaking
existing projects.

**Discriminating tests:**
- *cancer-type vs mechanism*: cancer-type is anchored in a specific tissue/lineage with
  its own taxonomy; mechanism is anchored in a process recurring across cancer-types.
- *mechanism vs condition*: mechanism is a *process* (something happening); condition
  is an *entity* (a disease state with prevalence, natural history, clinical phenotype).
- *mechanism vs data-source*: mechanism produces biological knowledge; data-source
  produces evidence streams (datasets, derived tables).

### 2.3 Operating principles

1. **Roles are organizational, not authoritative.** `meta` integrates; it doesn't *own*
   the science. A finding about MM evolution is canonical in `multiple-myeloma/` and
   *referenced* (not duplicated) from `mechanisms/evolution/` and `meta/`.
2. **Lazy promotion.** Sub-directories aren't pre-stubbed. A topic file inside an
   existing project is promoted to its own sub-project only when sustained inquiry
   justifies the cost. Demotion is also possible (rare).
3. **Tags absorb everything below the role line.** `science.yaml`'s existing `tags:`
   field handles scale labels (`molecular`, `clonal`, `population`), theoretical
   frameworks (`multiscale`, `systems-biology`), methodology (`signatures`,
   `panel-correction`), host-context (`aging`, `sex`), and cancer phenotypes
   (`hypermutator`, `msi`, `aneuploid`). Federation skills can query by tag across
   roles.

## 3. Federation v1.0 — upstream science framework changes

These changes go in `~/d/science/`. They are the structural minimum to make the
meta-project model work; tooling improvements come in later increments based on real
usage pressure.

### 3.1 `science.yaml` schema additions

For all projects:

```yaml
id: cbioportal              # stable short identifier; defaults to dirname; never reused
role: data-source           # free-form string (current vocabulary: meta | cancer-type | data-source | mechanism | condition | standalone)
parent: ~/d/cancer/meta     # optional; absolute path to umbrella's meta project (back-reference, not authoritative)
```

For `meta` projects only, an additional manifest:

```yaml
children:
  - id: cbioportal
    path: ~/d/cancer/data-sources/cbioportal
    role: data-source
  - id: multiple-myeloma
    path: ~/d/cancer/cancer-types/multiple-myeloma
    role: cancer-type
  - id: evolution
    path: ~/d/cancer/mechanisms/evolution
    role: mechanism
  - id: pre-cancer
    path: ~/d/cancer/conditions/pre-cancer
    role: condition
```

Authoritative source-of-truth for federation membership is meta's `children:`. Each
sub-project's `parent:` field is a back-reference, validated by `science:sync` but not
authoritative.

### 3.2 Cross-project addressing (convention)

Format: `<project-id>:<artifact-id>`

Examples:
- `cbioportal:q014` — question 014 in cbioportal
- `multiple-myeloma:h003` — hypothesis 003 in MM
- `evolution:t012` — task 012 in `mechanisms/evolution/`
- `cbioportal:topics/clonal-hematopoiesis-contamination` — non-numeric path artifact

In `graph.trig`, the same form lifts to a URI (e.g., `<cancer://cbioportal/q014>`).

In v1.0 this is **convention only** — humans write the addresses consistently; there's
no automated resolver or link-checker yet. Existing science skills learn to recognize
and link these strings, no more.

### 3.3 Federated knowledge graph (reads only)

Meta's `knowledge/graph.trig` is materialized by a federation-aware variant of
`science:create-graph` / `science:update-graph` that:

1. Walks meta's `children:` manifest.
2. Reads each child's `knowledge/graph.trig`.
3. Includes each child's triples as a *named graph* (one named graph per child id),
   preserving the child's authority over its own assertions.
4. Annotates each named graph with provenance triples
   (`prov:wasDerivedFrom <child/knowledge/graph.trig>` + timestamp).
5. Adds meta-level triples (umbrella-scope claims, cross-project links) in their own
   named graph (`<cancer://meta>`).

**Writes stay local.** A child's `update-graph` only ever writes its own
`graph.trig`. Meta's `update-graph` only ever writes meta's. No write-through
federation in v1.0.

No SPARQL endpoint, no live federation queries — file-based materialization only.

### 3.4 `science:status --federated`

Single skill rollup in v1.0. When invoked inside a `meta` project with `--federated`,
it walks `children:` and produces a combined report: per-child status sections + an
umbrella-level summary. Other rollup skills (`big-picture`, `next-steps`) stay
per-project until we feel pain.

### 3.5 Deferred to v1.1+

| Feature | Why deferred |
|---|---|
| `--federated` flags on `big-picture`, `next-steps` | Manual synthesis works; add when query patterns are clear |
| Automated cross-project address resolver / link-checker | Need real usage to know what edge cases matter |
| Bidirectional sync (meta proposes tasks down to children) | Manual cross-references work for now |
| Promotion tooling (topic-file → sub-project) | Manual move + path rewrite is fine until we do it 3+ times |
| SPARQL endpoint over federated graph | File-based is enough |
| Cross-federation graph schema lints (coreference, role conflicts) | Wait for real conflicts before designing the lint |
| Graph federation *writes* (cross-project triple authoring) | v1.0 is read-only |

### 3.6 Estimated upstream effort

| Piece | Effort |
|---|---|
| `science.yaml` schema additions + validators | 0.5 day |
| `children:` manifest support in `science:sync` | 0.5 day |
| Addressing convention doc + URI form | 0.5 day |
| `create-graph` / `update-graph` federation mode | 1.5 days |
| `science:status --federated` rollup | 0.5 day |
| Tests + docs in `~/d/science` | 1 day |
| **Total** | **~4.5 days focused work** |

## 4. Migration plan

### 4.1 Order

1. **mm30 first** — smaller, lower-risk, shakedown for the procedure.
2. **cbioportal second** — heavier hardcoded path footprint and a working pipeline to
   validate post-move.

### 4.2 Per-project move sequence

For each migrating project:

1. **Verify clean tree** (`git status` clean; no uncommitted work).
2. **Inventory path references**:
   - `.env` files (e.g., `SCIENCE_TOOL_PATH`)
   - `pyproject.toml` editable installs
   - `README.md`, `AGENTS.md`, `CLAUDE.md` text references
   - Snakefile / run config paths (`code/config/*.yml`)
   - External scripts in `~/bin/`, `~/.zshrc`, `~/.config/`, scheduled agents, etc.
3. **Move on Dropbox** (atomic):
   - cbioportal: `mv /mnt/ssd/Dropbox/r/cbioportal /mnt/ssd/Dropbox/cancer/data-sources/cbioportal`
   - mm30: equivalent into `cancer/cancer-types/multiple-myeloma/`
   Git follows the move; remote URLs are unaffected.
4. **Update path references** found in step 2.
5. **Update `science.yaml`**: add `id`, `role`, `parent`.
6. **Rename Claude Code memory directory** to match new path:
   - `/home/keith/.claude/projects/-mnt-ssd-Dropbox-r-cbioportal/` →
     `/home/keith/.claude/projects/-mnt-ssd-Dropbox-cancer-data-sources-cbioportal/`
   Without this, auto-memory is orphaned.
7. **Validate**:
   - cbioportal: `uv run snakemake -s code/workflows/Snakefile -j1 --configfile code/config/config-10k-genes.yml` plus `bash validate.sh --verbose`
   - mm30: equivalent project-specific validation
   - `science:sync` and `science:status --federated` from `meta/`
8. **Commit** the move + path updates as one atomic commit per project.

### 4.3 Backwards-compatibility symlinks

Keep `~/d/r/cbioportal → ~/d/cancer/data-sources/cbioportal` and equivalent for mm30
for **1–2 months** to absorb muscle memory, missed external references, and scheduled
agents. Remove once we're confident nothing depends on the old paths.

## 5. Day-1 sub-project materialization

After Phase 2 (migration) completes, materialize four sub-projects:

| Project | Day-1 contents |
|---|---|
| `meta/` | `science.yaml` (with `children:` manifest); `README.md` establishing vision; `AGENTS.md`; standard `doc/` structure (questions, hypotheses, topics, papers, plans, methods, datasets, discussions, interpretations, reports, searches, audits, background, meta, guides); 10 foundational questions (§6); empty `knowledge/graph.trig` |
| `mechanisms/evolution/` | `science.yaml`; README; AGENTS; standard `doc/`; 3–5 seed questions on evolutionary dynamics; topic stubs (`selection`, `plasticity`, `multiscale-evolution`, `drug-resistance-as-evolution`) |
| `conditions/pre-cancer/` | `science.yaml`; promoted/expanded from `cbioportal:topics/pre-cancer-prevalence-and-impact`; README; AGENTS; standard `doc/`; 3–5 questions about progression, prevalence, and clonal trajectories |
| `cbioportal/` (updates) | `id`/`role`/`parent` added to `science.yaml`; README and AGENTS get a top-of-file pointer to the umbrella; `doc/topics/pre-cancer-prevalence-and-impact.md` moved out (replaced with a redirect note pointing to `conditions/pre-cancer/`) |
| `multiple-myeloma/` (updates) | `id`/`role`/`parent` added; README/AGENTS pointer to umbrella |

## 6. Foundational questions for `meta/`

**Criteria for "foundational":**
- Cuts across cancer types (not type-specific)
- Open in current research (not trivially answerable)
- Not purely methodological (those stay in `data-sources/`)
- Admits progressive evidence accumulation
- Connects to multiple downstream hypotheses or topics

**Seed set (10 questions; expected to evolve as the framework runs):**

1. What is the relative contribution of stochastic mutation accumulation, selection,
   and epigenetic plasticity to cancer initiation?
2. How conserved are evolutionary dynamics across solid and liquid tumors?
3. What distinguishes pre-cancer states that progress from those that don't?
4. To what extent are cancer phenotypes (proliferation, invasion, dormancy, EMT)
   reversible, and what reverses them?
5. How much of a cancer's somatic mutation landscape reflects tissue-of-origin biology
   vs. cancer-specific selection?
6. What is the cross-tissue prevalence and trajectory of non-progressing clonal
   populations (CH, MGUS, Barrett's, oral leukoplakia, ...)?
7. When is a "driver" mutation causal vs. a passenger of selection acting elsewhere
   (CIN, replication stress, microenvironment)?
8. Are there unifying principles of therapeutic resistance across drug classes and
   cancer types?
9. Is cancer evolution path-dependent (history-bound) or reproducible
   (attractor-seeking)?
10. How does host context (immune state, age, sex, comorbidity, exposures) shape
    cancer trajectory across populations?

Questions 1, 3, 6, 7, 8 are flagged as the most load-bearing — they connect to the
greatest number of existing topics and incoming literature.

## 7. Literature ingest plan

56 PDFs in `papers/pdfs/`. Two-pass plan:

### 7.1 Pass 1 — Triage (single sitting)

- Per paper: title + abstract + (if uncertain) brief intro/discussion skim
- Output: a single triage table at `meta/doc/searches/2026-04-30-pdf-pile-triage.md`
  with columns:
  - filename
  - citation (author year, title, journal/preprint, DOI)
  - proposed role-assignment (cancer-type / mechanism / condition / data-source / methodology / theory)
  - target sub-project
  - tag list
  - one-sentence content summary
  - importance (1–3)
- Outcome: each paper assigned to a target sub-project for deeper read in Pass 2.
- Triage performed by main agent (not delegated), since it's the cheapest way to keep
  judgment consistent across the pile.

### 7.2 Pass 2 — Deep read (batched, parallel)

- Group triaged papers into batches of ~5–8 by target sub-project.
- For each batch, dispatch a `science:paper-researcher` sub-agent in parallel
  (`superpowers:dispatching-parallel-agents` skill). Each sub-agent:
  - Reads its assigned papers
  - Writes summaries into the target sub-project's `papers/` dir
  - Adds triples to that sub-project's `graph.trig`
  - Proposes new questions / hypotheses / tasks (some may target other sub-projects via
    cross-project addresses)
  - Returns a short batch-level synthesis to the main agent
- After all batches: main agent writes a meta-level synthesis pulling threads together,
  posted as `meta/doc/reports/2026-05-XX-first-literature-lap.md`.

## 8. Iteration cycle ("one lap" of the framework)

The continuous-evolution framework operates in laps. Each lap follows:

```
ingest → connect → question → synthesize → plan → iterate
```

| Phase | Action | Output |
|---|---|---|
| **Ingest** | Read N papers, run an analysis, or acquire a dataset | Paper summaries / analysis results in the relevant sub-project |
| **Connect** | Add triples to sub-project graphs; surface agreements & conflicts with existing claims | Updated `graph.trig`; conflict notes |
| **Question** | Generate / refine questions and hypotheses | New `q###`/`h###` files; updates to existing ones |
| **Synthesize** | Pull threads at meta level | Lap report in `meta/doc/reports/` |
| **Plan** | Identify highest-leverage next move (more papers, an analysis, a dataset, a new sub-project) | Updated `meta/tasks/` and pointers into sub-project tasks |
| **Iterate** | Pick next focus | (next lap) |

A lap is not always literature-driven. Future laps can be analyses in cbioportal,
deep-dives on one mechanism, dataset acquisitions, etc. The cycle structure is the
same.

**First lap = the 56 PDFs**: triage → deep read in batches → lap-1 synthesis →
priorities-for-lap-2. Roughly 2–4 sittings stretched over a few weeks.

## 9. Sequencing

| Phase | What | Approx effort |
|---|---|---|
| **Phase 0** | Brainstorm → spec doc → implementation plan(s) (this document is Phase 0 output) | done / in-progress |
| **Phase 1** | Federation v1.0 in `~/d/science/` (schema + manifest + addressing + federated graph reads + `status --federated`) | ~4.5 days focused |
| **Phase 2** | Migration: mm30 first, cbioportal second; backwards-compat symlinks; memory dir renames; validation | ~1 day |
| **Phase 3** | Day-1 scaffolding: `meta/`, `mechanisms/evolution/`, `conditions/pre-cancer/`; foundational questions; cbioportal/MM `science.yaml` + README/AGENTS updates | ~1–2 days |
| **Phase 4** | First literature lap: triage all 56 → batched deep read → lap-1 synthesis | spread over weeks |
| **Phase 5+** | Subsequent laps: analyses, more literature, new sub-projects as promoted | ongoing |

## 10. Out of scope

- Wholesale renaming or removal of cbioportal's existing methodological questions
  (q001–q017); they stay where they are and remain the focus of cbioportal's own work.
- Any change to mm30's existing scope or methodology beyond `science.yaml` updates and
  README/AGENTS pointers.
- Federation v1.1+ features (see §3.5).
- Connection to additional umbrella projects beyond `~/d/cancer/`.
- Web/UI artifacts on top of the federation.

## 11. Open questions to surface during execution

(Things not blocking the design but worth noticing as we go.)

- Whether `mm30`'s actual location is in Dropbox or local — affects move command. To
  be confirmed in Phase 2 inventory step.
- Whether any external scheduled agents (`science:schedule`, cron) reference the old
  cbioportal path — to be verified in Phase 2 inventory.
- Whether the `science.yaml` schema additions need a layout-version bump
  (`layout_version: 3`) — depends on `~/d/science/` migration conventions; decide
  during Phase 1.
- Whether to keep cbioportal's existing top-level `specs/` directory (currently holds
  `hypotheses/` and `research-question.md`) or to consolidate into `doc/specs/` for
  consistency with the broader convention. Out of scope for this design; flag as a
  potential cbioportal-internal cleanup.
