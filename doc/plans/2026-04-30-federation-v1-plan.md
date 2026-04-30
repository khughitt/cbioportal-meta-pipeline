# Federation v1.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the minimum upstream support in `~/d/science/` (a.k.a. `science-tool`) for the meta-project federation model defined in `2026-04-30-cancer-meta-project-design.md` §3 — so that a `meta` project can register children, cross-project addresses can be written consistently, the federated knowledge graph can be materialized, and a federated status rollup can be produced.

**Architecture:**
- Add a typed `ProjectConfig` pydantic schema for `science.yaml` (currently parsed ad-hoc) — new fields: `id`, `role`, `parent`, plus `children:` for `meta` projects. Extend the existing `RegisteredProject` global registry to track `parent`/`role`/`id`. Add a new `science-tool federation` click subgroup with `validate` and `status` subcommands. Extend the existing `graph build` command so that, in a child, it auto-registers the parent meta, and in a meta, it runs the standard local materialization first and then a federation pass that unions each child's TriG contexts under `cancer://<child-id>` named graphs. Update the existing `/science:status` skill to dispatch to `science-tool federation status` when `role: meta`.
- Path canonicalization: `science.yaml` stores tilde-prefixed paths; resolution uses `Path.expanduser().resolve()`; comparisons always operate on resolved physical paths.
- All writes are local: a child's commands only write the child's files; meta's commands only write meta's files.

**Tech Stack:** Python 3.11+ (per `science-tool/pyproject.toml`'s `requires-python = ">=3.11"`), pydantic v2, click (CLI; existing group `main` exposed as the `science-tool` entry point), pyyaml, rdflib (existing dep, already used with named graphs and TriG), pytest. All in `~/d/science/science-tool/`. Do NOT use 3.12/3.13-only APIs (e.g., `typing.Self` is fine; `typing.override` is not).

**Plan location:** This plan lives at `~/d/r/cbioportal/doc/plans/2026-04-30-federation-v1-plan.md` for now (paired with the design doc); it moves to `~/d/cancer/meta/doc/plans/` once the umbrella is materialized in Phase 3.

---

## Task 0: Repo orientation (no code)

**Files (read-only):**
- Read: `~/d/science/science-tool/pyproject.toml` (deps, package layout — note `requires-python = ">=3.11"` and `science-tool = "science_tool.cli:main"` script entry: the click group is named **`main`**, not `cli`)
- Read: `~/d/science/science-tool/src/science_tool/cli.py` — locate the click group (line ~100, `@click.group()` `def main()`), the existing `sync` group (line ~3143, with subcommands `run`, `status`, `projects`, `rebuild`), and the `graph` group (line ~552, with `build`/`audit`/`migrate` and `ensure_registered` invoked from `graph_build`).
- Read: `~/d/science/science-tool/src/science_tool/paths.py` (existing `science.yaml` profile resolution)
- Read: `~/d/science/science-tool/src/science_tool/registry/config.py` (existing global cross-project registry at `~/.config/science/config.yaml`)
- Read: `~/d/science/science-tool/src/science_tool/registry/sync.py` (the actual `sync run` engine called by the CLI)
- Read: `~/d/science/science-tool/src/science_tool/graph/sources.py` (`load_project_sources` and `science.yaml` parsing for graph)
- Read: `~/d/science/science-tool/src/science_tool/graph/store.py` — note the existing `GRAPH_LAYERS` constant (`"graph/knowledge"`, `"graph/bridge"`, `"graph/causal"`, `"graph/provenance"`, `"graph/datasets"`). Existing TriG output already uses named graphs; **federated parsing must use `rdflib.Dataset()`, not `rdflib.Graph()`**, or contexts will be silently dropped.
- Read: `~/d/science/commands/status.md` and `~/d/science/commands/sync.md` — these are the *skill* documents (markdown command files) that the user invokes via `/science:status` / `/science:sync`. Note: there is currently **no** `science-tool status` click subcommand. The skill walks project files itself; this plan adds a new CLI command and updates the skill to call it.
- Read existing tests under `~/d/science/science-tool/tests/` to learn the test conventions used (fixture patterns, `CliRunner` usage, mock vs. real fs).
- Read: `2026-04-30-cancer-meta-project-design.md` §3 (Federation v1.0 spec) — the source of truth for what this plan implements.

- [ ] **Step 1: Read the listed files and write a 200-word orientation note** to `~/d/science/science-tool/notes/2026-04-30-federation-orientation.md` (gitignored; just a scratch note). The note must answer:
  1. Where is `science.yaml` currently parsed? (List all call sites)
  2. Is there an existing pydantic schema for `science.yaml`? If yes, where; if no, that's a gap this plan must fill.
  3. How does the existing `science-tool sync run` engine work? Where is the auto-registration of *the current project* triggered? (Hint: `graph build`, via `ensure_registered`.)
  4. What graph IR does `science-tool graph build` emit? Confirm: TriG with named graphs (per `GRAPH_LAYERS`).
  5. What does `/science:status` (the skill) currently do? Note that the federation rollup will be a new `science-tool federation status` CLI command, and the skill is updated to invoke it when the project's `role: meta`.
  6. What test framework + fixture style is conventional?

  This note exists to prevent later tasks from making wrong assumptions. Do **not** edit code in this task.

- [ ] **Step 2: Commit nothing yet.** Move directly to Task 1.

---

## Task 1: `ProjectConfig` pydantic schema (new)

**Files:**
- Create: `~/d/science/science-tool/src/science_tool/project_config.py`
- Test: `~/d/science/science-tool/tests/test_project_config.py`

This task introduces a typed schema for `science.yaml`. The schema is **non-breaking**: it must accept all existing valid `science.yaml` files (cbioportal, mm30, every other registered project) without modification. New fields are optional.

- [ ] **Step 1: Write failing tests** for the schema's accepted fields and validation rules.

```python
# tests/test_project_config.py
from pathlib import Path

import pytest
from pydantic import ValidationError

from science_tool.project_config import (
    ChildEntry,
    ProjectConfig,
    ProjectRole,
    load_project_config,
)


def test_loads_minimal_existing_yaml(tmp_path: Path) -> None:
    """An existing science.yaml without new fields must still load."""
    project_root = tmp_path / "cbioportal"
    project_root.mkdir()
    yaml_text = """
name: cbioportal
created: "2025-02-21"
profile: research
research_question: "What is the structure of somatic mutations across cancers?"
"""
    (project_root / "science.yaml").write_text(yaml_text)

    cfg = load_project_config(project_root)
    assert cfg.name == "cbioportal"
    assert cfg.id == "cbioportal"  # defaults to project_root.name when not declared
    assert cfg.role == "standalone"  # default
    assert cfg.parent is None
    assert cfg.children == []


def test_explicit_id_role_parent(tmp_path: Path) -> None:
    yaml_text = """
name: cbioportal
id: cbioportal
role: data-source
parent: ~/d/cancer/meta
profile: research
research_question: "..."
"""
    (tmp_path / "science.yaml").write_text(yaml_text)
    cfg = load_project_config(tmp_path)
    assert cfg.role == ProjectRole.DATA_SOURCE
    assert cfg.parent == "~/d/cancer/meta"  # raw form preserved; resolution is separate


def test_meta_with_children_manifest(tmp_path: Path) -> None:
    yaml_text = """
name: meta
id: meta
role: meta
profile: research
research_question: "Umbrella: cancer + pre-cancer."
children:
  - id: cbioportal
    path: ~/d/cancer/data-sources/cbioportal
    role: data-source
  - id: multiple-myeloma
    path: ~/d/cancer/cancer-types/multiple-myeloma
    role: cancer-type
"""
    (tmp_path / "science.yaml").write_text(yaml_text)
    cfg = load_project_config(tmp_path)
    assert cfg.role == ProjectRole.META
    assert len(cfg.children) == 2
    assert cfg.children[0].id == "cbioportal"
    assert cfg.children[0].role == ProjectRole.DATA_SOURCE


def test_role_string_extensible(tmp_path: Path) -> None:
    """Unknown roles are accepted but normalized as raw strings (vocabulary is extensible)."""
    yaml_text = """
name: foo
id: foo
role: model-system
profile: research
research_question: "..."
"""
    (tmp_path / "science.yaml").write_text(yaml_text)
    cfg = load_project_config(tmp_path)
    assert cfg.role == "model-system"  # str, not enum-locked


def test_children_only_on_meta(tmp_path: Path) -> None:
    """Non-meta projects must not declare children."""
    yaml_text = """
name: foo
id: foo
role: data-source
profile: research
research_question: "..."
children:
  - id: bar
    path: ~/d/bar
    role: data-source
"""
    (tmp_path / "science.yaml").write_text(yaml_text)
    with pytest.raises(ValidationError, match="children.*only.*meta"):
        load_project_config(tmp_path)


def test_id_uniqueness_in_children(tmp_path: Path) -> None:
    yaml_text = """
name: meta
id: meta
role: meta
profile: research
research_question: "..."
children:
  - id: cbioportal
    path: ~/d/x
    role: data-source
  - id: cbioportal
    path: ~/d/y
    role: data-source
"""
    (tmp_path / "science.yaml").write_text(yaml_text)
    with pytest.raises(ValidationError, match="duplicate.*id"):
        load_project_config(tmp_path)
```

- [ ] **Step 2: Run tests, confirm all fail** with `ModuleNotFoundError: science_tool.project_config`.

```bash
cd ~/d/science/science-tool
uv run --frozen pytest tests/test_project_config.py -v
```

Expected: 6 tests fail (module missing).

- [ ] **Step 3: Implement `project_config.py`** with the schema. Use pydantic v2 (`BaseModel`, `model_validator`). Roles use a `StrEnum` *plus* allow free-form strings via a `BeforeValidator` so the vocabulary is extensible. Preserve all existing fields from the registered projects (run `python -c "import yaml, glob; [print(set(yaml.safe_load(open(p))) ) for p in glob.glob('/mnt/ssd/Dropbox/*/science.yaml') + glob.glob('/mnt/ssd/Dropbox/r/*/science.yaml')]"` if you need to enumerate them) by setting `model_config = ConfigDict(extra='allow')`.

```python
# src/science_tool/project_config.py
"""Typed schema for science.yaml. Non-breaking: extra fields are allowed."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Annotated, Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.functional_validators import BeforeValidator


class ProjectRole(StrEnum):
    META = "meta"
    CANCER_TYPE = "cancer-type"
    DATA_SOURCE = "data-source"
    MECHANISM = "mechanism"
    CONDITION = "condition"
    STANDALONE = "standalone"


def _coerce_role(value: Any) -> Any:
    """Accept known enum values or free-form strings (vocabulary is extensible)."""
    if value is None:
        return ProjectRole.STANDALONE
    if isinstance(value, ProjectRole):
        return value
    if isinstance(value, str):
        try:
            return ProjectRole(value)
        except ValueError:
            return value  # preserve unknown role as raw string
    raise TypeError(f"role must be string, got {type(value).__name__}")


RoleField = Annotated[ProjectRole | str, BeforeValidator(_coerce_role)]


class ChildEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    path: str  # tilde-prefixed; resolved via expanduser().resolve() at use sites
    role: RoleField = ProjectRole.STANDALONE


class ProjectConfig(BaseModel):
    """Typed view of science.yaml. Non-listed fields are preserved as-is."""

    model_config = ConfigDict(extra="allow")

    name: str
    id: str | None = None  # falls back to dirname at load time
    role: RoleField = ProjectRole.STANDALONE
    parent: str | None = None  # tilde-prefixed path
    children: list[ChildEntry] = Field(default_factory=list)

    @model_validator(mode="after")
    def _children_only_on_meta(self) -> "ProjectConfig":
        if self.children and self.role != ProjectRole.META:
            raise ValueError("children: manifest is only valid on role=meta projects")
        return self

    @model_validator(mode="after")
    def _children_unique_ids(self) -> "ProjectConfig":
        ids = [c.id for c in self.children]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate child id in children manifest")
        return self


def load_project_config(project_root: Path) -> ProjectConfig:
    """Load and validate science.yaml at ``project_root``. Defaults id to dirname."""
    yaml_path = project_root / "science.yaml"
    raw = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    if "id" not in raw or raw["id"] is None:
        raw["id"] = project_root.resolve().name
    return ProjectConfig.model_validate(raw)


def resolve_child_path(child: ChildEntry) -> Path:
    """Resolve a tilde-prefixed child path to a physical Path."""
    return Path(child.path).expanduser().resolve()
```

- [ ] **Step 4: Run tests, confirm all pass.**

```bash
uv run --frozen pytest tests/test_project_config.py -v
```

Expected: 6 passed.

- [ ] **Step 5: Run the full test suite to confirm no regression.**

```bash
uv run --frozen pytest -x
```

Expected: green.

- [ ] **Step 6: Commit.**

```bash
git add src/science_tool/project_config.py tests/test_project_config.py
git commit -m "feat(project_config): typed schema for science.yaml with id/role/parent/children"
```

---

## Task 2: Path resolution helpers and validators

**Files:**
- Modify: `~/d/science/science-tool/src/science_tool/project_config.py` (add helpers)
- Test: `~/d/science/science-tool/tests/test_project_config_paths.py`

The canonical path rule (design §3.1): `science.yaml` stores tilde-prefixed paths; resolution uses `expanduser` + `resolve` for symlink-aware comparison.

- [ ] **Step 1: Write failing tests** for path helpers.

```python
# tests/test_project_config_paths.py
from pathlib import Path

import pytest

from science_tool.project_config import (
    ChildEntry,
    ProjectRole,
    paths_equivalent,
    resolve_child_path,
    resolve_parent_path,
)


def test_resolve_child_path_expands_tilde(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    target = tmp_path / "d" / "cancer" / "x"
    target.mkdir(parents=True)
    child = ChildEntry(id="x", path="~/d/cancer/x", role=ProjectRole.MECHANISM)
    assert resolve_child_path(child) == target.resolve()


def test_paths_equivalent_through_symlink(tmp_path: Path) -> None:
    real = tmp_path / "real"
    real.mkdir()
    link = tmp_path / "link"
    link.symlink_to(real)
    assert paths_equivalent(real, link) is True


def test_paths_equivalent_distinct(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    assert paths_equivalent(a, b) is False


def test_resolve_parent_path_none_returns_none() -> None:
    assert resolve_parent_path(None) is None


def test_resolve_parent_path_missing_target_returns_unresolved(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """If the parent path does not exist, return the expanded but unresolved Path
    (callers decide whether missing parent is an error)."""
    monkeypatch.setenv("HOME", str(tmp_path))
    p = resolve_parent_path("~/does/not/exist")
    assert p == (tmp_path / "does" / "not" / "exist")
```

- [ ] **Step 2: Run tests, confirm 5 fail** with `ImportError`.

- [ ] **Step 3: Add the helpers** to `project_config.py`.

```python
def paths_equivalent(a: Path, b: Path) -> bool:
    """Compare two paths after symlink resolution."""
    try:
        return a.expanduser().resolve() == b.expanduser().resolve()
    except OSError:
        return False


def resolve_parent_path(parent: str | None) -> Path | None:
    """Resolve a tilde-prefixed parent path. Returns None if input is None.

    If the path does not exist, returns the expanded but unresolved Path so
    callers can distinguish 'not configured' (None) from 'configured but absent'.
    """
    if parent is None:
        return None
    expanded = Path(parent).expanduser()
    try:
        return expanded.resolve(strict=True)
    except (OSError, FileNotFoundError):
        return expanded
```

- [ ] **Step 4: Run tests, confirm 5 pass.**

- [ ] **Step 5: Commit.**

```bash
git add src/science_tool/project_config.py tests/test_project_config_paths.py
git commit -m "feat(project_config): tilde-prefixed path resolution helpers"
```

---

## Task 3: Federation validation — parent/children round-trip

**Files:**
- Create: `~/d/science/science-tool/src/science_tool/federation.py`
- Test: `~/d/science/science-tool/tests/test_federation_validation.py`

The `science-tool federation validate` CLI subcommand (Task 4) needs to check that meta's `children:` manifest and each child's `parent:` back-reference agree. This task isolates the validation logic so it's testable independently of CLI dispatch.

- [ ] **Step 1: Write failing tests.**

```python
# tests/test_federation_validation.py
from pathlib import Path

import pytest

from science_tool.federation import (
    FederationIssue,
    validate_federation,
)


def _write_yaml(path: Path, body: str) -> None:
    (path / "science.yaml").write_text(body, encoding="utf-8")


def test_consistent_meta_with_two_children(tmp_path: Path) -> None:
    meta = tmp_path / "meta"
    a = tmp_path / "a"
    b = tmp_path / "b"
    for d in (meta, a, b):
        d.mkdir()

    _write_yaml(meta, f"""
name: meta
id: meta
role: meta
profile: research
research_question: "..."
children:
  - id: a
    path: {a}
    role: data-source
  - id: b
    path: {b}
    role: cancer-type
""")
    _write_yaml(a, f"""
name: a
id: a
role: data-source
parent: {meta}
profile: research
research_question: "..."
""")
    _write_yaml(b, f"""
name: b
id: b
role: cancer-type
parent: {meta}
profile: research
research_question: "..."
""")

    issues = validate_federation(meta)
    assert issues == []


def test_child_missing_parent_field(tmp_path: Path) -> None:
    meta = tmp_path / "meta"
    a = tmp_path / "a"
    meta.mkdir(); a.mkdir()
    _write_yaml(meta, f"""
name: meta
id: meta
role: meta
profile: research
research_question: "..."
children:
  - id: a
    path: {a}
    role: data-source
""")
    _write_yaml(a, """
name: a
id: a
role: data-source
profile: research
research_question: "..."
""")  # no parent declared
    issues = validate_federation(meta)
    assert any(i.kind == "missing_parent" and i.child_id == "a" for i in issues)


def test_child_parent_points_elsewhere(tmp_path: Path) -> None:
    meta = tmp_path / "meta"
    other = tmp_path / "other"
    a = tmp_path / "a"
    for d in (meta, other, a):
        d.mkdir()
    _write_yaml(meta, f"""
name: meta
id: meta
role: meta
profile: research
research_question: "..."
children:
  - id: a
    path: {a}
    role: data-source
""")
    _write_yaml(a, f"""
name: a
id: a
role: data-source
parent: {other}
profile: research
research_question: "..."
""")
    issues = validate_federation(meta)
    assert any(i.kind == "parent_mismatch" and i.child_id == "a" for i in issues)


def test_child_path_does_not_exist(tmp_path: Path) -> None:
    meta = tmp_path / "meta"
    meta.mkdir()
    _write_yaml(meta, f"""
name: meta
id: meta
role: meta
profile: research
research_question: "..."
children:
  - id: a
    path: {tmp_path / "missing"}
    role: data-source
""")
    issues = validate_federation(meta)
    assert any(i.kind == "child_path_missing" and i.child_id == "a" for i in issues)


def test_role_disagreement_between_meta_and_child(tmp_path: Path) -> None:
    meta = tmp_path / "meta"
    a = tmp_path / "a"
    meta.mkdir(); a.mkdir()
    _write_yaml(meta, f"""
name: meta
id: meta
role: meta
profile: research
research_question: "..."
children:
  - id: a
    path: {a}
    role: data-source
""")
    _write_yaml(a, f"""
name: a
id: a
role: cancer-type
parent: {meta}
profile: research
research_question: "..."
""")
    issues = validate_federation(meta)
    assert any(i.kind == "role_mismatch" and i.child_id == "a" for i in issues)


def test_id_disagreement_between_meta_and_child(tmp_path: Path) -> None:
    meta = tmp_path / "meta"
    a = tmp_path / "a"
    meta.mkdir(); a.mkdir()
    _write_yaml(meta, f"""
name: meta
id: meta
role: meta
profile: research
research_question: "..."
children:
  - id: a
    path: {a}
    role: data-source
""")
    _write_yaml(a, f"""
name: a
id: bee
role: data-source
parent: {meta}
profile: research
research_question: "..."
""")
    issues = validate_federation(meta)
    assert any(i.kind == "id_mismatch" and i.child_id == "a" for i in issues)
```

- [ ] **Step 2: Run tests; confirm 6 fail** (`ImportError`).

- [ ] **Step 3: Implement `federation.py`.**

```python
# src/science_tool/federation.py
"""Federation validation: meta children manifest vs. child parent back-references."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from science_tool.project_config import (
    ChildEntry,
    ProjectConfig,
    ProjectRole,
    load_project_config,
    paths_equivalent,
    resolve_child_path,
    resolve_parent_path,
)

IssueKind = Literal[
    "child_path_missing",
    "missing_parent",
    "parent_mismatch",
    "role_mismatch",
    "id_mismatch",
    "not_a_meta_project",
]


@dataclass(frozen=True)
class FederationIssue:
    kind: IssueKind
    child_id: str | None
    detail: str


def validate_federation(meta_root: Path) -> list[FederationIssue]:
    """Validate meta's children: against each child's parent: back-reference.

    Returns a list of issues; an empty list means the federation is consistent.
    Raises ValueError if ``meta_root`` is not a meta project.
    """
    meta_cfg = load_project_config(meta_root)
    if meta_cfg.role != ProjectRole.META:
        raise ValueError(f"{meta_root} is role={meta_cfg.role!r}; not a meta project")

    issues: list[FederationIssue] = []
    meta_resolved = meta_root.resolve()

    for child in meta_cfg.children:
        issues.extend(_validate_one_child(child, meta_resolved))

    return issues


def _validate_one_child(child: ChildEntry, meta_resolved: Path) -> list[FederationIssue]:
    issues: list[FederationIssue] = []
    child_path = resolve_child_path(child)

    if not child_path.is_dir() or not (child_path / "science.yaml").is_file():
        issues.append(
            FederationIssue(
                kind="child_path_missing",
                child_id=child.id,
                detail=f"no science.yaml at {child_path}",
            )
        )
        return issues

    child_cfg = load_project_config(child_path)

    if child_cfg.id != child.id:
        issues.append(
            FederationIssue(
                kind="id_mismatch",
                child_id=child.id,
                detail=f"manifest says id={child.id!r}, child science.yaml says id={child_cfg.id!r}",
            )
        )

    if child_cfg.role != child.role:
        issues.append(
            FederationIssue(
                kind="role_mismatch",
                child_id=child.id,
                detail=f"manifest says role={child.role!r}, child says role={child_cfg.role!r}",
            )
        )

    if child_cfg.parent is None:
        issues.append(
            FederationIssue(
                kind="missing_parent",
                child_id=child.id,
                detail="child science.yaml has no parent: declared",
            )
        )
    else:
        resolved_parent = resolve_parent_path(child_cfg.parent)
        if resolved_parent is None or not paths_equivalent(resolved_parent, meta_resolved):
            issues.append(
                FederationIssue(
                    kind="parent_mismatch",
                    child_id=child.id,
                    detail=f"child parent={child_cfg.parent!r} resolves to {resolved_parent}, expected {meta_resolved}",
                )
            )

    return issues
```

- [ ] **Step 4: Run tests, confirm 6 pass.**

- [ ] **Step 5: Commit.**

```bash
git add src/science_tool/federation.py tests/test_federation_validation.py
git commit -m "feat(federation): validate meta/children round-trip"
```

---

## Task 4: Federation CLI subgroup + parent auto-register from `graph build`

**Files:**
- Create: `~/d/science/science-tool/src/science_tool/federation_cli.py` (new click subgroup `federation`)
- Modify: `~/d/science/science-tool/src/science_tool/cli.py` — register the new subgroup with `main` (one-line addition near the other `main.add_command(...)` calls around line 182–189); extend the existing `graph_build` (line ~552) so that when the current project has `parent:` set, it also calls `ensure_registered` for the parent meta.
- Modify: `~/d/science/science-tool/src/science_tool/registry/config.py` — extend `RegisteredProject` with optional `id`/`role`/`parent` fields and update `ensure_registered` to accept and refresh them idempotently.
- Test: `~/d/science/science-tool/tests/test_federation_cli.py`
- Test: `~/d/science/science-tool/tests/test_graph_build_parent_register.py`

### Why a new subgroup, not a `sync` extension

`science-tool sync` is an existing click group with subcommands `run`, `status`, `projects`, `rebuild`. Auto-registration of the *current* project happens in `graph build` (via `ensure_registered`), not in `sync`. Federation validation is a different concern from cross-project sync execution and deserves its own subgroup so users can call it explicitly: `science-tool federation validate`. The plan doesn't shoehorn validation into `sync run`.

The one extension to existing CLI behavior: when `graph build` runs in a project with `parent:` declared, it also registers the parent meta. This keeps the same place where current-project registration already lives, so meta auto-discovery doesn't surprise anyone reading `sync`'s code.

- [ ] **Step 1: Failing tests for the new `federation` subgroup.**

```python
# tests/test_federation_cli.py
from pathlib import Path

import pytest
from click.testing import CliRunner

from science_tool.cli import main


def _write_yaml(path: Path, body: str) -> None:
    (path / "science.yaml").write_text(body, encoding="utf-8")


def test_federation_validate_clean(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SCIENCE_CONFIG_DIR", str(tmp_path / "cfg"))
    meta = tmp_path / "meta"
    a = tmp_path / "a"
    meta.mkdir(); a.mkdir()
    _write_yaml(meta, f"""
name: meta
id: meta
role: meta
profile: research
research_question: "..."
children:
  - id: a
    path: {a}
    role: data-source
""")
    _write_yaml(a, f"""
name: a
id: a
role: data-source
parent: {meta}
profile: research
research_question: "..."
""")
    monkeypatch.chdir(meta)
    runner = CliRunner()
    result = runner.invoke(main, ["federation", "validate"])
    assert result.exit_code == 0, result.output
    assert "ok" in result.output.lower() or "no issues" in result.output.lower()


def test_federation_validate_surfaces_issues(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SCIENCE_CONFIG_DIR", str(tmp_path / "cfg"))
    meta = tmp_path / "meta"
    a = tmp_path / "a"
    meta.mkdir(); a.mkdir()
    _write_yaml(meta, f"""
name: meta
id: meta
role: meta
profile: research
research_question: "..."
children:
  - id: a
    path: {a}
    role: data-source
""")
    _write_yaml(a, """
name: a
id: a
role: data-source
profile: research
research_question: "..."
""")  # no parent: declared
    monkeypatch.chdir(meta)
    runner = CliRunner()
    result = runner.invoke(main, ["federation", "validate"])
    # Issues are surfaced; exit code is non-zero so callers can detect them.
    assert result.exit_code != 0
    assert "missing_parent" in result.output


def test_federation_validate_refuses_non_meta(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SCIENCE_CONFIG_DIR", str(tmp_path / "cfg"))
    a = tmp_path / "a"
    a.mkdir()
    _write_yaml(a, """
name: a
id: a
role: data-source
profile: research
research_question: "..."
""")
    monkeypatch.chdir(a)
    runner = CliRunner()
    result = runner.invoke(main, ["federation", "validate"])
    assert result.exit_code != 0
    assert "not a meta" in result.output.lower() or "not a meta" in (result.stderr or "").lower()
```

- [ ] **Step 2: Failing test for parent auto-registration via `graph build`.**

```python
# tests/test_graph_build_parent_register.py
from pathlib import Path

import pytest
from click.testing import CliRunner

from science_tool.cli import main
from science_tool.registry.config import load_global_config


def test_graph_build_in_child_registers_parent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg_dir = tmp_path / "cfg"
    monkeypatch.setenv("SCIENCE_CONFIG_DIR", str(cfg_dir))

    meta = tmp_path / "meta"
    a = tmp_path / "a"
    meta.mkdir(); a.mkdir()
    (meta / "science.yaml").write_text(f"""
name: meta
id: meta
role: meta
profile: research
research_question: "..."
children:
  - id: a
    path: {a}
    role: data-source
""", encoding="utf-8")
    (a / "science.yaml").write_text(f"""
name: a
id: a
role: data-source
parent: {meta}
profile: research
research_question: "..."
""", encoding="utf-8")

    monkeypatch.chdir(a)
    runner = CliRunner()
    result = runner.invoke(main, ["graph", "build"])
    assert result.exit_code == 0, result.output

    cfg = load_global_config(cfg_dir / "config.yaml")
    paths = {p.path for p in cfg.projects}
    assert any(p.endswith("/a") for p in paths)
    assert any(p.endswith("/meta") for p in paths)
    # Confirm role/parent fields are populated on the registered child.
    child_entry = next(p for p in cfg.projects if p.path.endswith("/a"))
    assert child_entry.role == "data-source"
    assert child_entry.parent and child_entry.parent.endswith("/meta")
```

- [ ] **Step 3: Run tests; confirm 4 fail.**

- [ ] **Step 4: Extend `RegisteredProject`** in `registry/config.py`. Additive; defaults preserve existing config files.

```python
# in src/science_tool/registry/config.py
class RegisteredProject(BaseModel):
    """A project registered for cross-project sync."""

    path: str
    name: str
    registered: date
    id: str | None = None
    role: str | None = None
    parent: str | None = None  # tilde-prefixed; None for non-children
```

Update `ensure_registered`:

```python
def ensure_registered(
    project_root: Path,
    project_name: str,
    config_path: Path | None = None,
    project_id: str | None = None,
    role: str | None = None,
    parent: str | None = None,
) -> None:
    """Register or refresh a project. Idempotent. Refreshes federation fields when supplied."""
    config_path = config_path or get_default_config_path()
    resolved = str(project_root.resolve())
    cfg = load_global_config(config_path)

    for project in cfg.projects:
        if project.path == resolved:
            # refresh federation fields when supplied (no-op when None)
            changed = False
            if project_id is not None and project.id != project_id:
                project.id = project_id
                changed = True
            if role is not None and project.role != role:
                project.role = role
                changed = True
            if parent is not None and project.parent != parent:
                project.parent = parent
                changed = True
            if changed:
                save_global_config(cfg, config_path)
            return

    cfg.projects.append(
        RegisteredProject(
            path=resolved,
            name=project_name,
            registered=date.today(),
            id=project_id,
            role=role,
            parent=parent,
        )
    )
    save_global_config(cfg, config_path)
```

- [ ] **Step 5: Implement `federation_cli.py`.**

```python
# src/science_tool/federation_cli.py
"""CLI subgroup for federation v1.0: validate, status (status added in Task 8)."""

from __future__ import annotations

from pathlib import Path

import click

from science_tool.federation import validate_federation
from science_tool.project_config import ProjectRole, load_project_config


@click.group(name="federation")
def federation_group() -> None:
    """Federation operations: validate and roll up across meta children."""


@federation_group.command("validate")
@click.option(
    "--project-root",
    default=".",
    show_default=True,
    type=click.Path(path_type=Path, file_okay=False, dir_okay=True),
)
def federation_validate(project_root: Path) -> None:
    """Validate meta's children manifest against each child's parent back-reference."""
    root = Path.cwd() if str(project_root) == "." else project_root
    cfg = load_project_config(root)
    if cfg.role != ProjectRole.META:
        raise click.ClickException(f"{root} is not a meta project (role={cfg.role!r})")

    issues = validate_federation(root)
    if not issues:
        click.echo("ok: federation consistent")
        return

    for issue in issues:
        click.echo(
            f"{issue.kind}: child={issue.child_id}: {issue.detail}",
            err=True,
        )
    raise click.exceptions.Exit(1)
```

- [ ] **Step 6: Register the subgroup with `main`** in `cli.py` near the existing `main.add_command(...)` block (around lines 182–189). Add:

```python
from science_tool.federation_cli import federation_group
main.add_command(federation_group)
```

- [ ] **Step 7: Extend `graph_build`** (in `cli.py`, around line 552) to register the parent meta after registering the current project. Locate the existing block:

```python
if _science_yaml.is_file():
    _project_name = (_yaml.safe_load(_science_yaml.read_text()) or {}).get("name", _project_root.name)
    ensure_registered(_project_root, str(_project_name))
```

Replace with:

```python
if _science_yaml.is_file():
    from science_tool.project_config import load_project_config

    _cfg = load_project_config(_project_root)
    ensure_registered(
        _project_root,
        _cfg.name,
        project_id=_cfg.id,
        role=str(_cfg.role),
        parent=_cfg.parent,
    )
    if _cfg.parent is not None:
        from science_tool.project_config import resolve_parent_path

        _parent_path = resolve_parent_path(_cfg.parent)
        if _parent_path is not None and (_parent_path / "science.yaml").is_file():
            _parent_cfg = load_project_config(_parent_path)
            ensure_registered(
                _parent_path,
                _parent_cfg.name,
                project_id=_parent_cfg.id,
                role=str(_parent_cfg.role),
                parent=_parent_cfg.parent,
            )
```

- [ ] **Step 8: Run all tests; confirm green and no regressions.**

```bash
uv run --frozen pytest -x
```

- [ ] **Step 9: Commit.**

```bash
git add src/science_tool/federation_cli.py src/science_tool/cli.py src/science_tool/registry/config.py tests/test_federation_cli.py tests/test_graph_build_parent_register.py
git commit -m "feat(federation): federation validate CLI + parent auto-register from graph build"
```

---

## Task 5: Cross-project addressing — parser and URI form

**Files:**
- Create: `~/d/science/science-tool/src/science_tool/addressing.py`
- Test: `~/d/science/science-tool/tests/test_addressing.py`

The address grammar is `<project-id>:<artifact-id>`. URI form is `<cancer://<project-id>/<artifact-id>>`. v1.0 is convention-only — no resolver yet — but we need parse/render helpers so future tooling can hook in.

- [ ] **Step 1: Failing tests.**

```python
# tests/test_addressing.py
import pytest

from science_tool.addressing import (
    Address,
    parse_address,
    render_uri,
    is_address,
)


def test_parse_simple_question() -> None:
    a = parse_address("cbioportal:q014")
    assert a == Address(project_id="cbioportal", artifact_id="q014")


def test_parse_path_artifact() -> None:
    a = parse_address("cbioportal:topics/clonal-hematopoiesis-contamination")
    assert a.artifact_id == "topics/clonal-hematopoiesis-contamination"


def test_render_uri() -> None:
    a = Address(project_id="multiple-myeloma", artifact_id="h003")
    assert render_uri(a) == "<cancer://multiple-myeloma/h003>"


def test_is_address_positive() -> None:
    assert is_address("evolution:t012") is True


def test_is_address_negative() -> None:
    assert is_address("not an address") is False
    assert is_address("just-a-word") is False
    assert is_address("a:") is False  # empty artifact id
    assert is_address(":x") is False  # empty project id


def test_parse_invalid_raises() -> None:
    with pytest.raises(ValueError):
        parse_address("not an address")
```

- [ ] **Step 2: Run; confirm 6 fail.**

- [ ] **Step 3: Implement `addressing.py`.**

```python
# src/science_tool/addressing.py
"""Cross-project addressing convention: <project-id>:<artifact-id>.

v1.0 is convention-only. This module provides parse/render helpers; resolution
against a meta's children manifest is deferred to v1.1+.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Project ids: lowercase alphanumeric, hyphens; 2–64 chars.
# Artifact ids: any non-whitespace tokens, including '/' for path-like artifacts.
_ADDRESS_RE = re.compile(r"^(?P<project>[a-z][a-z0-9-]{1,63}):(?P<artifact>\S+)$")
_URI_SCHEME = "cancer"


@dataclass(frozen=True)
class Address:
    project_id: str
    artifact_id: str


def parse_address(raw: str) -> Address:
    m = _ADDRESS_RE.match(raw)
    if not m:
        raise ValueError(f"not a valid cross-project address: {raw!r}")
    return Address(project_id=m["project"], artifact_id=m["artifact"])


def is_address(raw: str) -> bool:
    return _ADDRESS_RE.match(raw) is not None


def render_uri(address: Address) -> str:
    """Render the address as a URI suitable for graph triples."""
    return f"<{_URI_SCHEME}://{address.project_id}/{address.artifact_id}>"
```

- [ ] **Step 4: Run; confirm 6 pass.**

- [ ] **Step 5: Commit.**

```bash
git add src/science_tool/addressing.py tests/test_addressing.py
git commit -m "feat(addressing): cross-project address parse/render"
```

---

## Task 6: Federated graph materialization (read-only assembly)

**Files:**
- Create: `~/d/science/science-tool/src/science_tool/graph/federation.py`
- Test: `~/d/science/science-tool/tests/test_graph_federation.py`

Meta's `knowledge/graph.trig` is assembled by:
1. Materializing meta's own local sources (existing pipeline) and capturing their triples in `cancer://meta`.
2. Reading each child's `knowledge/graph.trig` (which uses named graphs per `GRAPH_LAYERS`) and unioning *all of the child's contexts* into a single `cancer://<child-id>` named graph in the federated output.
3. Adding provenance triples (`prov:wasDerivedFrom`, `prov:generatedAtTime`) and meta-level cross-project claims to `cancer://meta`.

Two parsing pitfalls to handle correctly (per code review):
- **Use `rdflib.Dataset()` to parse child TriG, not `rdflib.Graph()`.** A child's `graph.trig` uses named graphs (`graph/knowledge`, `graph/bridge`, etc.); parsing it into a `Graph()` reads only the default-graph triples and drops everything else.
- **Walk all of the source dataset's contexts**, not just the default graph, when copying triples into the destination named graph.

For v1.0 we **collapse** child-side layer graphs into a single `cancer://<child-id>` graph in the federated output (simpler queries, smaller surface area). Preserving the layer hierarchy under `cancer://<child-id>/<layer>` is a future v1.1+ option, not blocking.

- [ ] **Step 1: Read** the existing `materialize_graph` function in `~/d/science/science-tool/src/science_tool/graph/store.py` and confirm:
  - Its signature (likely `materialize_graph(project_root: Path) -> Path`).
  - Whether it writes directly to `<project_root>/knowledge/graph.trig`, or returns the path it wrote.
  - That `GRAPH_LAYERS` are emitted as named graphs in the output (already verified during Task 0; reconfirm here before touching anything).

  Note findings as comments at the top of `graph/federation.py`.

- [ ] **Step 2: Failing tests.** Test fixtures use `Dataset()` to write TriG with named graphs (matching real-world child outputs), not `Graph()` with default-graph triples (which would mask the rdflib bug).

```python
# tests/test_graph_federation.py
from pathlib import Path

import pytest
import rdflib
from rdflib import Dataset, Graph, Literal, URIRef
from rdflib.namespace import PROV, RDF

from science_tool.graph.federation import materialize_federated_graph


def _write_yaml(path: Path, body: str) -> None:
    (path / "science.yaml").write_text(body, encoding="utf-8")


def _write_layered_trig(child_root: Path, child_id: str) -> None:
    """Write a TriG file with multiple named graphs, like real child outputs."""
    knowledge_dir = child_root / "knowledge"
    knowledge_dir.mkdir(exist_ok=True)
    ds = Dataset()
    ex = rdflib.Namespace("https://example.org/")
    knowledge = ds.graph(URIRef(f"https://example.org/{child_id}/graph/knowledge"))
    knowledge.add((ex[f"{child_id}-claim"], RDF.type, ex.Claim))
    bridge = ds.graph(URIRef(f"https://example.org/{child_id}/graph/bridge"))
    bridge.add((ex[f"{child_id}-link"], RDF.type, ex.Bridge))
    ds.serialize(destination=knowledge_dir / "graph.trig", format="trig")


def test_assembles_named_graphs_per_child(tmp_path: Path) -> None:
    meta = tmp_path / "meta"
    a = tmp_path / "a"
    b = tmp_path / "b"
    for d in (meta, a, b):
        d.mkdir()

    _write_yaml(meta, f"""
name: meta
id: meta
role: meta
profile: research
research_question: "..."
children:
  - id: a
    path: {a}
    role: data-source
  - id: b
    path: {b}
    role: cancer-type
""")
    _write_yaml(a, f"""
name: a
id: a
role: data-source
parent: {meta}
profile: research
research_question: "..."
""")
    _write_yaml(b, f"""
name: b
id: b
role: cancer-type
parent: {meta}
profile: research
research_question: "..."
""")
    _write_layered_trig(a, "a")
    _write_layered_trig(b, "b")

    out_path = materialize_federated_graph(meta)
    assert out_path.exists()

    ds = Dataset()
    ds.parse(out_path, format="trig")
    graph_names = {str(g.identifier) for g in ds.graphs() if g.identifier != URIRef("urn:x-rdflib:default")}
    assert "cancer://a" in graph_names
    assert "cancer://b" in graph_names
    assert "cancer://meta" in graph_names

    # Critical: triples from EACH layer of the child's TriG must be present.
    a_graph = ds.graph(URIRef("cancer://a"))
    a_subjects = {str(s) for s in a_graph.subjects()}
    assert "https://example.org/a-claim" in a_subjects, "knowledge-layer triple missing"
    assert "https://example.org/a-link" in a_subjects, "bridge-layer triple missing — Dataset() not used for parse"

    # Provenance triples in cancer://meta
    meta_graph = ds.graph(URIRef("cancer://meta"))
    prov_subjects = {str(s) for s, _, _ in meta_graph.triples((None, PROV.wasDerivedFrom, None))}
    assert "cancer://a" in prov_subjects
    assert "cancer://b" in prov_subjects


def test_includes_meta_local_triples(tmp_path: Path) -> None:
    """Meta's own local graph (its umbrella claims) must end up in cancer://meta."""
    meta = tmp_path / "meta"
    meta.mkdir()
    _write_yaml(meta, f"""
name: meta
id: meta
role: meta
profile: research
research_question: "Umbrella."
children: []
""")
    knowledge_dir = meta / "knowledge"
    knowledge_dir.mkdir()
    pre = Dataset()
    ex = rdflib.Namespace("https://example.org/")
    g = pre.graph(URIRef("https://example.org/meta/graph/knowledge"))
    g.add((ex["meta-claim"], RDF.type, ex.UmbrellaClaim))
    pre.serialize(destination=knowledge_dir / "graph.trig", format="trig")

    out_path = materialize_federated_graph(meta)
    ds = Dataset()
    ds.parse(out_path, format="trig")
    meta_graph = ds.graph(URIRef("cancer://meta"))
    meta_subjects = {str(s) for s in meta_graph.subjects()}
    assert "https://example.org/meta-claim" in meta_subjects, "meta's own local triple lost"


def test_skips_child_without_graph_trig(tmp_path: Path) -> None:
    meta = tmp_path / "meta"
    a = tmp_path / "a"
    meta.mkdir(); a.mkdir()
    _write_yaml(meta, f"""
name: meta
id: meta
role: meta
profile: research
research_question: "..."
children:
  - id: a
    path: {a}
    role: data-source
""")
    _write_yaml(a, f"""
name: a
id: a
role: data-source
parent: {meta}
profile: research
research_question: "..."
""")
    # No graph.trig in a/ — assembler still succeeds and emits just meta + provenance gap.
    out_path = materialize_federated_graph(meta)
    assert out_path.exists()


def test_refuses_non_meta_root(tmp_path: Path) -> None:
    a = tmp_path / "a"
    a.mkdir()
    _write_yaml(a, """
name: a
id: a
role: data-source
profile: research
research_question: "..."
""")
    with pytest.raises(ValueError, match="not a meta"):
        materialize_federated_graph(a)
```

- [ ] **Step 3: Run; confirm 4 fail.**

- [ ] **Step 4: Implement `graph/federation.py`.**

```python
# src/science_tool/graph/federation.py
"""Federated graph assembly.

Existing per-project ``graph.trig`` outputs use named graphs (per
``GRAPH_LAYERS`` in ``graph/store.py``: ``graph/knowledge``, ``graph/bridge``,
``graph/causal``, ``graph/provenance``, ``graph/datasets``). Federation reads
each child's TriG with ``rdflib.Dataset`` (not ``Graph``, which silently drops
non-default contexts) and unions all of the child's contexts into a single
``cancer://<child-id>`` named graph in the federated output.

For v1.0 we collapse child layers; preserving them as
``cancer://<child-id>/<layer>`` is a future option.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from rdflib import Dataset, Literal, URIRef
from rdflib.namespace import PROV

from science_tool.project_config import (
    ChildEntry,
    ProjectRole,
    load_project_config,
    resolve_child_path,
)

_URI_SCHEME = "cancer"
_XSD_DATETIME = URIRef("http://www.w3.org/2001/XMLSchema#dateTime")


def _project_uri(project_id: str) -> URIRef:
    return URIRef(f"{_URI_SCHEME}://{project_id}")


def materialize_federated_graph(meta_root: Path) -> Path:
    """Materialize meta's federated graph.trig.

    Behavior:
    - First materialize meta's own local sources via the existing pipeline.
      The resulting triples land in ``cancer://meta``.
    - Then union each child's TriG contexts into ``cancer://<child-id>``.
    - Annotate ``cancer://meta`` with provenance triples for each included child.

    Returns the output path (``meta_root/knowledge/graph.trig``).
    Raises ValueError if ``meta_root`` is not a meta project.
    """
    cfg = load_project_config(meta_root)
    if cfg.role != ProjectRole.META:
        raise ValueError(f"{meta_root} is role={cfg.role!r}; not a meta project")

    out_dir = meta_root / "knowledge"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "graph.trig"

    ds = Dataset()
    meta_uri = _project_uri(cfg.id or meta_root.name)
    meta_graph = ds.graph(meta_uri)

    # Step A: meta's own local triples → cancer://meta
    _materialize_meta_local(meta_root, meta_graph)

    # Step B: each child's TriG → cancer://<child-id>
    timestamp = Literal(datetime.now(timezone.utc).isoformat(), datatype=_XSD_DATETIME)
    for child in cfg.children:
        child_uri = _project_uri(child.id)
        included = _include_child_graph(ds, child, child_uri)
        if included:
            meta_graph.add((child_uri, PROV.wasDerivedFrom, Literal(str(_child_graph_path(child)))))
            meta_graph.add((child_uri, PROV.generatedAtTime, timestamp))

    ds.serialize(destination=out_path, format="trig")
    return out_path


def _materialize_meta_local(meta_root: Path, dest_graph) -> None:  # type: ignore[no-untyped-def]
    """Materialize meta's own local sources into ``dest_graph``.

    v1.0 implementation: read meta's existing ``knowledge/graph.trig`` if present
    (assumed to have been produced by an earlier ``science-tool graph build``
    against meta's local sources, prior to federation). Union all its contexts
    into ``dest_graph``.

    A future refinement: invoke the existing per-project ``materialize_graph``
    pipeline directly to a memory dataset, avoiding the read-then-overwrite
    round trip. Out of scope for v1.0.
    """
    src_path = meta_root / "knowledge" / "graph.trig"
    if not src_path.is_file():
        return
    src = Dataset()
    src.parse(src_path, format="trig")
    for ctx in src.contexts():
        for triple in ctx:
            dest_graph.add(triple)


def _child_graph_path(child: ChildEntry) -> Path:
    return resolve_child_path(child) / "knowledge" / "graph.trig"


def _include_child_graph(ds: Dataset, child: ChildEntry, child_uri: URIRef) -> bool:
    """Union all contexts of the child's TriG into ``cancer://<child-id>``.

    Returns True if a graph file was found and included.
    """
    src_path = _child_graph_path(child)
    if not src_path.is_file():
        return False
    target = ds.graph(child_uri)
    src = Dataset()
    src.parse(src_path, format="trig")
    for ctx in src.contexts():
        for triple in ctx:
            target.add(triple)
    return True
```

- [ ] **Step 5: Run tests; confirm 4 pass.** The `test_assembles_named_graphs_per_child` test specifically asserts that the *bridge*-layer triple is preserved — this is the regression check for the `Graph()` vs. `Dataset()` parsing pitfall.

- [ ] **Step 6: Run the full suite for regressions.**

- [ ] **Step 7: Commit.**

```bash
git add src/science_tool/graph/federation.py tests/test_graph_federation.py
git commit -m "feat(graph): federated graph assembly preserving child layers + meta local"
```

### Note: read-then-overwrite of meta's `knowledge/graph.trig`

`materialize_federated_graph` reads `meta_root/knowledge/graph.trig` (Step A in `_materialize_meta_local`) and then later overwrites the same path with the federated output. This means: **before federation, meta must have run a standard graph build to produce its own local triples.** Task 7 enforces this ordering by having `graph_build` in a meta project first call the standard `materialize_graph` (writing meta's local triples) and *then* call `materialize_federated_graph` on the same project root, which re-reads those triples and re-emits with children included.

---

## Task 7: Wire federated graph mode into `graph build`

**Files:**
- Modify: `~/d/science/science-tool/src/science_tool/cli.py` (existing `graph_build` function at line ~552)
- Test: `~/d/science/science-tool/tests/test_graph_build_federated.py`

Behavior change: when `science-tool graph build` runs in a `meta` project, after the standard `materialize_graph` produces meta's local triples (so `cancer://meta` will pick them up), the federation assembler runs on top, re-reading those local triples and unioning each child's contexts. The user invokes one command; both phases happen.

- [ ] **Step 1: Failing test.** The fixture writes a child's TriG using `Dataset()` (matching real-world layered output) so the assertion exercises the layer-preserving parser fixed in Task 6.

```python
# tests/test_graph_build_federated.py
from pathlib import Path

import pytest
import rdflib
from click.testing import CliRunner
from rdflib import Dataset, URIRef
from rdflib.namespace import RDF

from science_tool.cli import main


def test_graph_build_in_meta_uses_federated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SCIENCE_CONFIG_DIR", str(tmp_path / "cfg"))
    meta = tmp_path / "meta"
    a = tmp_path / "a"
    meta.mkdir(); a.mkdir()

    (meta / "science.yaml").write_text(f"""
name: meta
id: meta
role: meta
profile: research
research_question: "..."
children:
  - id: a
    path: {a}
    role: data-source
""", encoding="utf-8")
    (a / "science.yaml").write_text(f"""
name: a
id: a
role: data-source
parent: {meta}
profile: research
research_question: "..."
""", encoding="utf-8")

    # Child has a TriG with named graphs (matches real outputs).
    (a / "knowledge").mkdir()
    ex = rdflib.Namespace("https://example.org/")
    a_ds = Dataset()
    a_ds.graph(URIRef("https://example.org/a/graph/knowledge")).add(
        (ex["a-claim"], RDF.type, ex.Claim)
    )
    a_ds.serialize(destination=a / "knowledge" / "graph.trig", format="trig")

    monkeypatch.chdir(meta)
    runner = CliRunner()
    result = runner.invoke(main, ["graph", "build"])
    assert result.exit_code == 0, result.output

    out_ds = Dataset()
    out_ds.parse(meta / "knowledge" / "graph.trig", format="trig")
    graph_names = {str(g.identifier) for g in out_ds.graphs() if g.identifier != URIRef("urn:x-rdflib:default")}
    assert "cancer://a" in graph_names
    assert "cancer://meta" in graph_names

    # Confirm child layer triples landed in cancer://a (the fix for the layer-drop bug).
    a_graph = out_ds.graph(URIRef("cancer://a"))
    a_subjects = {str(s) for s in a_graph.subjects()}
    assert "https://example.org/a-claim" in a_subjects
```

- [ ] **Step 2: Modify `graph_build` in `cli.py`** so that, in a meta project, it runs the standard local materialization first and then federation. The standard path for non-meta projects must remain unchanged.

  Concrete edit shape: after computing `_project_root` and after the existing `ensure_registered` block (already extended in Task 4 Step 7), insert the federation dispatch.

```python
from science_tool.project_config import ProjectRole, load_project_config
from science_tool.graph.federation import materialize_federated_graph

# After the existing ensure_registered block in graph_build:
_cfg = load_project_config(_project_root)
if _cfg.role == ProjectRole.META:
    # Phase A: standard materialization writes meta's local triples to
    # meta_root/knowledge/graph.trig.
    try:
        local_trig_path = materialize_graph(_project_root)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(f"Materialized meta local graph at {local_trig_path}")

    # Phase B: federation re-reads meta's local triples (placing them in
    # cancer://meta) and unions each child's contexts into cancer://<child-id>.
    federated_path = materialize_federated_graph(_project_root)
    click.echo(f"Materialized federated graph at {federated_path}")
    return

# ... existing standalone-graph path follows unchanged
```

- [ ] **Step 3: Run the new test; confirm green. Run full suite for regressions.**

- [ ] **Step 4: Commit.**

```bash
git add src/science_tool/cli.py tests/test_graph_build_federated.py
git commit -m "feat(cli): graph build runs local + federated phases in meta projects"
```

---

## Task 8: `science-tool federation status` CLI + `/science:status` skill update

**Files:**
- Create: `~/d/science/science-tool/src/science_tool/federation_status.py` (rollup logic)
- Modify: `~/d/science/science-tool/src/science_tool/federation_cli.py` (add `status` subcommand to the existing `federation_group` from Task 4)
- Modify: `~/d/science/commands/status.md` (the `/science:status` skill — teach it to invoke the new CLI when the project's `role: meta`)
- Test: `~/d/science/science-tool/tests/test_federation_status_cli.py`

### Why a new CLI subcommand, not a `/science:status` skill rewrite

The `/science:status` skill at `~/d/science/commands/status.md` is the user-facing entry point and currently walks project files itself (no CLI shells out). For federation, rolling up across multiple projects deterministically is real computation that benefits from being a CLI command (testable, scriptable, single source of truth). The skill stays the entry point — it just learns to call `science-tool federation status` when the project's role is `meta`.

The rollup is intentionally simple in v1.0: it produces a markdown document with a per-child summary section + an umbrella header. It does **not** try to deeply mirror everything `/science:status` shows. That depth lives in the per-project skill invocation; federation gives the cross-cutting view.

- [ ] **Step 1: Failing test for the new CLI subcommand.**

```python
# tests/test_federation_status_cli.py
from pathlib import Path

import pytest
from click.testing import CliRunner

from science_tool.cli import main


def test_federation_status_walks_children(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SCIENCE_CONFIG_DIR", str(tmp_path / "cfg"))
    meta = tmp_path / "meta"
    a = tmp_path / "a"
    b = tmp_path / "b"
    for d in (meta, a, b):
        d.mkdir()

    (meta / "science.yaml").write_text(f"""
name: meta
id: meta
role: meta
profile: research
research_question: "Umbrella."
children:
  - id: a
    path: {a}
    role: data-source
  - id: b
    path: {b}
    role: cancer-type
""", encoding="utf-8")
    for child_dir, child_id, child_role, q in (
        (a, "a", "data-source", "child a question"),
        (b, "b", "cancer-type", "child b question"),
    ):
        (child_dir / "science.yaml").write_text(f"""
name: {child_id}
id: {child_id}
role: {child_role}
parent: {meta}
profile: research
research_question: "{q}"
""", encoding="utf-8")

    monkeypatch.chdir(meta)
    runner = CliRunner()
    result = runner.invoke(main, ["federation", "status"])
    assert result.exit_code == 0, result.output
    # Output mentions the umbrella header and each child by id and role.
    assert "Federation:" in result.output or "federation" in result.output.lower()
    assert "data-source" in result.output
    assert "cancer-type" in result.output
    assert "child a question" in result.output
    assert "child b question" in result.output


def test_federation_status_refuses_non_meta(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SCIENCE_CONFIG_DIR", str(tmp_path / "cfg"))
    a = tmp_path / "a"
    a.mkdir()
    (a / "science.yaml").write_text("""
name: a
id: a
role: data-source
profile: research
research_question: "..."
""", encoding="utf-8")
    monkeypatch.chdir(a)
    runner = CliRunner()
    result = runner.invoke(main, ["federation", "status"])
    assert result.exit_code != 0
    assert "not a meta" in result.output.lower() or "not a meta" in (result.stderr or "").lower()


def test_federation_status_handles_missing_child(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A child path declared in meta but absent on disk should not crash the rollup."""
    monkeypatch.setenv("SCIENCE_CONFIG_DIR", str(tmp_path / "cfg"))
    meta = tmp_path / "meta"
    meta.mkdir()
    missing = tmp_path / "missing"
    (meta / "science.yaml").write_text(f"""
name: meta
id: meta
role: meta
profile: research
research_question: "..."
children:
  - id: missing
    path: {missing}
    role: data-source
""", encoding="utf-8")
    monkeypatch.chdir(meta)
    runner = CliRunner()
    result = runner.invoke(main, ["federation", "status"])
    # Rollup should still complete; missing child surfaces as a note.
    assert result.exit_code == 0, result.output
    assert "missing" in result.output
```

- [ ] **Step 2: Implement `federation_status.py`.** v1.0 renders a self-contained summary per child from its `science.yaml` (name, role, research question, count of questions/hypotheses if those dirs exist). It does not invoke the per-project status skill's full rendering — that's a v1.1+ option once we know what's worth aggregating.

```python
# src/science_tool/federation_status.py
"""Federation status rollup: meta umbrella + per-child summary."""

from __future__ import annotations

from io import StringIO
from pathlib import Path

from science_tool.project_config import (
    ChildEntry,
    ProjectConfig,
    ProjectRole,
    load_project_config,
    resolve_child_path,
)


def render_federated_status(meta_root: Path) -> str:
    cfg = load_project_config(meta_root)
    if cfg.role != ProjectRole.META:
        raise ValueError(f"{meta_root} is role={cfg.role!r}; not a meta project")

    buf = StringIO()
    buf.write(f"# Federation: {cfg.id or meta_root.name}\n\n")
    buf.write(f"Research question: {cfg.model_dump().get('research_question', '(none)')}\n\n")
    buf.write(f"Children: {len(cfg.children)}\n\n")

    for child in cfg.children:
        buf.write(f"---\n\n## {child.id} ({child.role})\n\n")
        buf.write(_render_child_summary(child))
        buf.write("\n")

    buf.write("---\n\n## Meta scope\n\n")
    buf.write(_render_meta_scope(meta_root, cfg))
    return buf.getvalue()


def _render_child_summary(child: ChildEntry) -> str:
    child_root = resolve_child_path(child)
    if not (child_root / "science.yaml").is_file():
        return f"_missing_: declared path `{child_root}` has no science.yaml\n"

    try:
        child_cfg = load_project_config(child_root)
    except Exception as exc:
        return f"_failed to load_: {exc}\n"

    raw = child_cfg.model_dump()
    rq = raw.get("research_question", "(none)")
    lines = [
        f"- name: {child_cfg.name}",
        f"- path: {child_root}",
        f"- research question: {rq}",
    ]
    questions_dir = child_root / "doc" / "questions"
    hypotheses_dir = child_root / "doc" / "hypotheses"
    if questions_dir.is_dir():
        lines.append(f"- questions: {sum(1 for _ in questions_dir.glob('*.md'))}")
    if hypotheses_dir.is_dir():
        lines.append(f"- hypotheses: {sum(1 for _ in hypotheses_dir.glob('*.md'))}")
    return "\n".join(lines) + "\n"


def _render_meta_scope(meta_root: Path, cfg: ProjectConfig) -> str:
    raw = cfg.model_dump()
    lines = [f"- name: {cfg.name}", f"- id: {cfg.id}"]
    questions_dir = meta_root / "doc" / "questions"
    if questions_dir.is_dir():
        lines.append(f"- foundational questions: {sum(1 for _ in questions_dir.glob('*.md'))}")
    if "tags" in raw:
        lines.append(f"- tags: {raw['tags']}")
    return "\n".join(lines) + "\n"
```

- [ ] **Step 3: Add `status` subcommand to the existing `federation_group`** in `federation_cli.py` (the group was created in Task 4):

```python
# add to src/science_tool/federation_cli.py

from science_tool.federation_status import render_federated_status


@federation_group.command("status")
@click.option(
    "--project-root",
    default=".",
    show_default=True,
    type=click.Path(path_type=Path, file_okay=False, dir_okay=True),
)
def federation_status(project_root: Path) -> None:
    """Render a cross-project status rollup for a meta umbrella."""
    root = Path.cwd() if str(project_root) == "." else project_root
    try:
        rendered = render_federated_status(root)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(rendered)
```

- [ ] **Step 4: Update `~/d/science/commands/status.md`** to teach the skill to dispatch to the federation CLI when the current project's `role` is `meta`. Add this stanza near the start of the skill's "Setup" section, *before* the existing `Read science.yaml` step:

```markdown
## Federation handling

If `science.yaml` declares `role: meta`, the rest of this skill's per-project
flow is replaced by:

```
science-tool federation status
```

Print the result and stop. Do not attempt to read individual children's
project files yourself — the CLI does that consistently and is the single
source of truth for cross-project rollups.

For non-meta projects (the default), proceed with the existing per-project
status flow below.
```

- [ ] **Step 5: Run tests; full suite.**

```bash
uv run --frozen pytest -x
```

- [ ] **Step 6: Commit.**

```bash
git add src/science_tool/federation_status.py src/science_tool/federation_cli.py ../commands/status.md tests/test_federation_status_cli.py
git commit -m "feat(federation): status rollup CLI + skill dispatch for meta projects"
```

> Note on the path `../commands/status.md`: this file lives in `~/d/science/commands/`, which is the parent of `science-tool/`. The git repo root is `~/d/science/`, so the `git add` from `science-tool/` reaches outside its directory but stays inside the repo. If the science framework keeps `commands/` and `science-tool/` in *separate* git repos, split this into two commits accordingly.

---

## Task 9: Integration test — round-trip with two real children

**Files:**
- Test: `~/d/science/science-tool/tests/test_federation_integration.py`

End-to-end: scaffold a meta + 2 children, run `federation validate`, run `graph build`, run `federation status`, parse outputs, assert the federation is internally consistent.

- [ ] **Step 1: Write test.** Use the same fixture pattern from Task 4/8 but combined. Fixture writes child TriGs with `Dataset()` (named graphs, matching real outputs).

```python
# tests/test_federation_integration.py
from pathlib import Path

import pytest
import rdflib
from click.testing import CliRunner
from rdflib import Dataset, URIRef
from rdflib.namespace import RDF

from science_tool.cli import main


def _make_child(path: Path, child_id: str, role: str, meta_path: Path, with_graph: bool = True) -> None:
    path.mkdir()
    (path / "science.yaml").write_text(f"""
name: {child_id}
id: {child_id}
role: {role}
parent: {meta_path}
profile: research
research_question: "child {child_id}"
""", encoding="utf-8")
    if with_graph:
        (path / "knowledge").mkdir()
        ex = rdflib.Namespace("https://example.org/")
        ds = Dataset()
        ds.graph(URIRef(f"https://example.org/{child_id}/graph/knowledge")).add(
            (ex[f"{child_id}-claim"], RDF.type, ex.Claim)
        )
        ds.serialize(destination=path / "knowledge" / "graph.trig", format="trig")


def test_federation_round_trip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SCIENCE_CONFIG_DIR", str(tmp_path / "cfg"))
    meta = tmp_path / "meta"
    a = tmp_path / "a"
    b = tmp_path / "b"
    meta.mkdir()
    (meta / "science.yaml").write_text(f"""
name: meta
id: meta
role: meta
profile: research
research_question: "Umbrella."
children:
  - id: a
    path: {a}
    role: data-source
  - id: b
    path: {b}
    role: cancer-type
""", encoding="utf-8")
    _make_child(a, "a", "data-source", meta)
    _make_child(b, "b", "cancer-type", meta)

    runner = CliRunner()
    monkeypatch.chdir(meta)

    # 1. federation validate from meta — should be clean
    result = runner.invoke(main, ["federation", "validate"])
    assert result.exit_code == 0, result.output

    # 2. graph build in meta — local + federated phases
    result = runner.invoke(main, ["graph", "build"])
    assert result.exit_code == 0, result.output

    # 3. federation status
    result = runner.invoke(main, ["federation", "status"])
    assert result.exit_code == 0, result.output
    assert "a" in result.output
    assert "b" in result.output

    # 4. Parse the federated graph and confirm shape
    ds = Dataset()
    ds.parse(meta / "knowledge" / "graph.trig", format="trig")
    graph_names = {str(g.identifier) for g in ds.graphs() if g.identifier != URIRef("urn:x-rdflib:default")}
    assert {"cancer://a", "cancer://b", "cancer://meta"}.issubset(graph_names)

    # 5. Confirm the layer-preserving parser actually preserved layered triples.
    a_subjects = {str(s) for s in ds.graph(URIRef("cancer://a")).subjects()}
    assert "https://example.org/a-claim" in a_subjects
```

- [ ] **Step 2: Run test; confirm green.**

- [ ] **Step 3: Commit.**

```bash
git add tests/test_federation_integration.py
git commit -m "test(federation): end-to-end sync + graph build + status round-trip"
```

---

## Task 10: User-facing documentation

**Files:**
- Create: `~/d/science/docs/federation.md`
- Modify: `~/d/science/README.md` (add a brief Federation section pointing at the new doc)

Content of `federation.md` must cover:
1. The meta-project concept and the 5-role taxonomy (link back to `~/d/cancer/meta/doc/plans/2026-04-30-cancer-meta-project-design.md` once that exists).
2. `science.yaml` schema additions: `id`, `role`, `parent`, `children:`. With YAML examples.
3. The canonical path rule (tilde-prefixed, expand on use).
4. Cross-project addressing convention: `<project-id>:<artifact-id>` and `<cancer://project-id/artifact-id>` URI form.
5. Federated graph behavior: named-graph-per-child, provenance triples, read-only.
6. `science-tool federation validate` and `science-tool federation status` usage; the `/science:status` skill dispatch.
7. What's deferred to v1.1+ (link to the design doc's §3.5 deferred table).

- [ ] **Step 1: Write `federation.md`** following the structure above. No placeholders — everything in the design doc §3 is concrete enough to lift in.

- [ ] **Step 2: Add a Federation section to `~/d/science/README.md`** (or equivalent top-level doc) — 4–6 lines pointing readers at `docs/federation.md`.

- [ ] **Step 3: Commit.**

```bash
git add docs/federation.md README.md
git commit -m "docs: federation v1.0 reference"
```

---

## Task 11: Self-check and version bump

**Files:**
- Modify: `~/d/science/science-tool/pyproject.toml` (bump version per the project's existing conventions — minor bump for additive feature)

- [ ] **Step 1: Run the full test suite.**

```bash
cd ~/d/science/science-tool
uv run --frozen pytest -v
```

Expected: green, including the new federation tests.

- [ ] **Step 2: Run linters.** Whatever the project uses (ruff, pyright). Locate via `pyproject.toml` `[tool.ruff]` / `[tool.pyright]` sections.

```bash
uv run --frozen ruff check src/science_tool/project_config.py src/science_tool/federation.py src/science_tool/addressing.py src/science_tool/graph/federation.py src/science_tool/federation_status.py
uv run --frozen pyright src/science_tool/project_config.py src/science_tool/federation.py src/science_tool/addressing.py src/science_tool/graph/federation.py src/science_tool/federation_status.py
```

Expected: clean.

- [ ] **Step 3: Bump version** in `pyproject.toml`. If the project currently follows CalVer or SemVer, follow that. Add a one-line note to whatever changelog the project keeps (e.g., `CHANGELOG.md`) if one exists.

- [ ] **Step 4: Commit.**

```bash
git add pyproject.toml CHANGELOG.md  # only if CHANGELOG.md exists in the repo
git commit -m "chore: science-tool version bump for federation v1.0"
```

---

## Task 12: Validation in dependent projects (smoke check)

**Files:**
- No code changes; this task is a smoke check from inside cbioportal and (if available) mm30.

- [ ] **Step 1: From `~/d/r/cbioportal/`, run `uv sync`** to pick up the new science-tool version (since `pyproject.toml` references it as an editable install at `../../science/science-tool`).

```bash
cd ~/d/r/cbioportal
uv sync
```

- [ ] **Step 2: Run `science-tool graph build`** — must remain green. cbioportal has no `parent:` and no `role: meta`, so behavior should match pre-federation (single-project materialization, no federation phase, no parent auto-register). Also verify `science-tool sync run` still works.

- [ ] **Step 3: Run `bash validate.sh --verbose`** — must remain green.

- [ ] **Step 4: Repeat for `~/d/r/mm30`** if available.

- [ ] **Step 5: If anything broke, fix it before declaring Phase 1 done.** Common breakages to check:
  - Stricter schema rejecting an existing `science.yaml` field
  - Sync command emitting noise that was previously silent
  - Graph build behaving differently for a non-meta project (it shouldn't — the federated branch is gated on `role == META`)

- [ ] **Step 6: No commit needed if nothing broke.** If a fix was applied to `~/d/science/`, commit it as a follow-up.

---

## Phase 1 done. Follow-up phases (reminder).

This plan covers Phase 1 only. The other phases from `2026-04-30-cancer-meta-project-design.md` §9, in order:

| Phase | What | When to plan |
|---|---|---|
| Phase 2 | Migrate cbioportal + mm30 into `~/d/cancer/`; bootstrap minimal `meta/`; backwards-compat symlinks; memory dir renames; per-child validation | After Phase 1 lands and is exercised in the dependent projects |
| Phase 3 | Day-1 scaffolding for `meta/`, `mechanisms/evolution/`, `conditions/pre-cancer/`; foundational questions; cbioportal/MM `science.yaml` + README/AGENTS updates; first `science-tool federation status` run | Immediately after Phase 2 |
| Phase 4 | First literature lap: PDF manifest pre-flight → triage → batched deep read with `science:paper-researcher` sub-agents → lap-1 synthesis | After Phase 3 |
| Phase 5+ | Subsequent laps; Federation v1.1+ features (deferred items in design §3.5) as real usage pressure justifies | Ongoing |

Plans for Phases 2–5 are written when their predecessors land, not preemptively, to avoid designing against a moving target. Phase 1 is the only blocker for the rest of the rollout.

---

## Self-review notes

- **Spec coverage.** Each numbered piece of design §3.6's effort table maps to a task here:
  - `science.yaml` schema additions + validators → Tasks 1, 2
  - `children:` manifest support + federation `validate` CLI + parent auto-register → Task 4 (with Task 3 as the validation library)
  - Addressing convention doc + URI form → Tasks 5, 10
  - Federated `graph build` (local + federated phases, layer-preserving) → Tasks 6, 7
  - Federated status rollup CLI + `/science:status` skill dispatch → Task 8
  - Tests + docs → Task 9 (integration), Task 10 (docs), Task 11 (self-check), Task 12 (smoke)
- **Placeholder scan.** No "TBD"/"fill in details" left in the plan. Where the plan acknowledges discovery (the Task 0 orientation note, the conditional refactor in Task 8 Step 1a), it's because the existing CLI structure can't be assumed without reading the source — this is honest about the unknown rather than a hidden placeholder.
- **Type consistency.** `ProjectConfig`, `ChildEntry`, `ProjectRole`, `Address`, `FederationIssue` defined in Tasks 1/3/5 are referenced consistently in Tasks 4/6/7/8/9. `materialize_federated_graph(meta_root: Path) -> Path` matches between Task 6 and Task 7. `render_project_status(project_root: Path) -> str` is created (or extracted) in Task 8 Step 1a and consumed in Step 3.
- **Granularity.** Each step is 2–5 minutes for an engineer who's read Task 0. Tests-first throughout. Frequent commits (one per task at minimum, with Task 8 having an extra refactor commit if needed).
