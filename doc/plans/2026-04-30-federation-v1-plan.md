# Federation v1.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the minimum upstream support in `~/d/science/` (a.k.a. `science-tool`) for the meta-project federation model defined in `2026-04-30-cancer-meta-project-design.md` §3 — so that a `meta` project can register children, cross-project addresses can be written consistently, the federated knowledge graph can be materialized, and `science:status --federated` can roll up status across children.

**Architecture:**
- Add a typed `ProjectConfig` pydantic schema for `science.yaml` (currently parsed ad-hoc) — new fields: `id`, `role`, `parent`, plus `children:` for `meta` projects. Extend the existing `RegisteredProject` global registry to track `parent`/`role`. Keep `science:sync` as the single sync entrypoint, taught to recognize meta/children relationships. Implement federated graph materialization as a new mode in the existing `graph` command. `status --federated` walks `children:` and concatenates per-child status renderings under an umbrella header.
- Path canonicalization: `science.yaml` stores tilde-prefixed paths; resolution uses `Path.expanduser().resolve()`; comparisons always operate on resolved physical paths.
- All writes are local: a child's commands only write the child's files; meta's commands only write meta's files.

**Tech Stack:** Python 3.13+, pydantic v2, click (CLI), pyyaml, rdflib (existing dep), pytest. All in `~/d/science/science-tool/`.

**Plan location:** This plan lives at `~/d/r/cbioportal/doc/plans/2026-04-30-federation-v1-plan.md` for now (paired with the design doc); it moves to `~/d/cancer/meta/doc/plans/` once the umbrella is materialized in Phase 3.

---

## Task 0: Repo orientation (no code)

**Files (read-only):**
- Read: `~/d/science/science-tool/pyproject.toml` (deps, package layout)
- Read: `~/d/science/science-tool/src/science_tool/cli.py` — locate `sync`, `status`, `graph` click commands; note line numbers
- Read: `~/d/science/science-tool/src/science_tool/paths.py` (existing `science.yaml` profile resolution)
- Read: `~/d/science/science-tool/src/science_tool/registry/config.py` (existing global cross-project registry at `~/.config/science/config.yaml`)
- Read: `~/d/science/science-tool/src/science_tool/graph/sources.py` (`load_project_sources` and `science.yaml` parsing for graph)
- Read: `~/d/science/science-tool/src/science_tool/graph/store.py` (graph materialization — TriG output, named graphs)
- Read existing tests under `~/d/science/science-tool/tests/` to learn the test conventions used (fixture patterns, factory style, async/sync, mock vs. real fs)
- Read: `2026-04-30-cancer-meta-project-design.md` §3 (Federation v1.0 spec) — the source of truth for what this plan implements

- [ ] **Step 1: Read the listed files and write a 200-word orientation note** to `~/d/science/science-tool/notes/2026-04-30-federation-orientation.md` (gitignored; just a scratch note). The note must answer:
  1. Where is `science.yaml` currently parsed? (List all call sites)
  2. Is there an existing pydantic schema for `science.yaml`? If yes, where; if no, that's a gap this plan must fill.
  3. How does `science:sync` currently discover peer projects? (Trace the dispatch path.)
  4. What graph IR does `science:graph build` emit? (TriG, single-graph or named-graphs already?)
  5. What test framework + fixture style is conventional?

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
    yaml_text = """
name: cbioportal
created: "2025-02-21"
profile: research
research_question: "What is the structure of somatic mutations across cancers?"
"""
    yaml_path = tmp_path / "science.yaml"
    yaml_path.write_text(yaml_text)

    cfg = load_project_config(tmp_path)
    assert cfg.name == "cbioportal"
    assert cfg.id == "cbioportal"  # defaults to dirname-equivalent
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

`science:sync` (Task 4) needs to validate that meta's `children:` and each child's `parent:` agree. This task isolates the validation logic so it's testable independently of CLI dispatch.

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

## Task 4: Wire federation validation into `science:sync`

**Files:**
- Modify: `~/d/science/science-tool/src/science_tool/cli.py` (sync command — locate via `grep -n "def sync\|@.*sync" cli.py`)
- Modify: `~/d/science/science-tool/src/science_tool/registry/config.py` (extend `RegisteredProject` with optional `parent`/`role`/`id`)
- Test: `~/d/science/science-tool/tests/test_sync_federation.py`

`science:sync` currently auto-registers a project to `~/.config/science/config.yaml`. We extend it so that:
1. When called inside a `meta` project, it also runs `validate_federation` and prints any issues (warning, not error).
2. When called inside a child with a declared `parent:`, it ensures the parent meta is registered too.
3. The global registry tracks each project's role/parent so `status --federated` doesn't have to walk the filesystem.

- [ ] **Step 1: Write failing tests** that drive `science:sync` end-to-end through click's `CliRunner`.

```python
# tests/test_sync_federation.py
from pathlib import Path

import pytest
from click.testing import CliRunner

from science_tool.cli import cli  # adjust if the click group is exported under a different name
from science_tool.registry.config import GlobalConfig, load_global_config


def _write_yaml(path: Path, body: str) -> None:
    (path / "science.yaml").write_text(body, encoding="utf-8")


def test_sync_meta_project_validates_children(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg_dir = tmp_path / "cfg"
    monkeypatch.setenv("SCIENCE_CONFIG_DIR", str(cfg_dir))

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
    runner = CliRunner()
    result = runner.invoke(cli, ["sync"], catch_exceptions=False, env={}, color=False)
    # invoke from meta dir
    monkeypatch.chdir(meta)
    result = runner.invoke(cli, ["sync"])
    assert result.exit_code == 0
    cfg = load_global_config(cfg_dir / "config.yaml")
    assert any(p.path.endswith("/meta") for p in cfg.projects)


def test_sync_meta_surfaces_issues_as_warnings(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg_dir = tmp_path / "cfg"
    monkeypatch.setenv("SCIENCE_CONFIG_DIR", str(cfg_dir))
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
    result = runner.invoke(cli, ["sync"])
    assert result.exit_code == 0  # warnings, not errors
    assert "missing_parent" in result.output


def test_sync_child_registers_parent_meta(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg_dir = tmp_path / "cfg"
    monkeypatch.setenv("SCIENCE_CONFIG_DIR", str(cfg_dir))
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
    monkeypatch.chdir(a)
    runner = CliRunner()
    result = runner.invoke(cli, ["sync"])
    assert result.exit_code == 0
    cfg = load_global_config(cfg_dir / "config.yaml")
    paths = {p.path for p in cfg.projects}
    assert any(p.endswith("/a") for p in paths)
    assert any(p.endswith("/meta") for p in paths)
```

- [ ] **Step 2: Run failing tests.** They will fail because of the new sync behavior.

- [ ] **Step 3: Extend `RegisteredProject` schema** in `registry/config.py` (additive; existing fields unchanged):

```python
class RegisteredProject(BaseModel):
    """A project registered for cross-project sync."""

    path: str
    name: str
    registered: date
    id: str | None = None
    role: str | None = None
    parent: str | None = None  # tilde-prefixed; None for non-children
```

Update `ensure_registered` to accept optional `id`/`role`/`parent` and to refresh those fields on subsequent calls (idempotent update, not just append).

- [ ] **Step 4: Modify `science:sync` command in `cli.py`** to:
  1. Load `ProjectConfig` for the current project.
  2. Pass `id`/`role`/`parent` into `ensure_registered`.
  3. If `role == META`: run `validate_federation(project_root)` and emit each issue as a warning line (`click.echo(f"warning: {kind} for child {id}: {detail}", err=True)`). Do not raise.
  4. If `parent` is set on the current project: also call `ensure_registered` for the parent meta (so a child's sync brings the parent into the registry).

  The existing sync command body must stay intact for non-meta, non-child projects.

  Concrete edit shape (locate the function via `grep -n "def sync\|@cli.command(\"sync\")\|^def sync_" src/science_tool/cli.py`):
  - Right after current project registration, branch on `project_config.role`.
  - Use `from science_tool.federation import validate_federation` and `from science_tool.project_config import load_project_config`.

- [ ] **Step 5: Run all tests; confirm green and no regressions.**

```bash
uv run --frozen pytest -x
```

- [ ] **Step 6: Commit.**

```bash
git add src/science_tool/cli.py src/science_tool/registry/config.py tests/test_sync_federation.py
git commit -m "feat(sync): meta-aware sync with federation validation + parent auto-register"
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

Meta's `knowledge/graph.trig` is assembled by reading each child's `knowledge/graph.trig` and including their triples as named graphs (one named graph per child id), preserving the child's authority. Provenance triples annotate each named graph.

- [ ] **Step 1: Read** `~/d/science/science-tool/src/science_tool/graph/store.py` (lines 1-200 first, then locate the materialize function used by `graph build`). Note:
  - Whether the existing graph is a single TriG default graph or already uses named graphs.
  - The function signature for materialization (probably `materialize_graph(project_root: Path) -> Path`).

  Without this, the federated assembly will fight the existing format. Record findings as a comment at the top of the new file.

- [ ] **Step 2: Failing test.** This test sets up a tiny meta + 2 children, calls the federated assembler, then parses the result and confirms named graphs are present.

```python
# tests/test_graph_federation.py
from pathlib import Path

import pytest
import rdflib

from science_tool.graph.federation import materialize_federated_graph


def _write_trig(path: Path, body: str) -> None:
    (path / "knowledge").mkdir(exist_ok=True)
    (path / "knowledge" / "graph.trig").write_text(body, encoding="utf-8")


def _write_yaml(path: Path, body: str) -> None:
    (path / "science.yaml").write_text(body, encoding="utf-8")


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

    _write_trig(a, """
@prefix ex: <https://example.org/> .
ex:a-claim a ex:Claim .
""")
    _write_trig(b, """
@prefix ex: <https://example.org/> .
ex:b-claim a ex:Claim .
""")

    out_path = materialize_federated_graph(meta)
    assert out_path.exists()

    ds = rdflib.Dataset()
    ds.parse(out_path, format="trig")
    graph_names = {str(g.identifier) for g in ds.graphs() if g.identifier != rdflib.URIRef("urn:x-rdflib:default")}
    # Each child gets its own named graph, plus the meta-level named graph.
    assert "cancer://a" in graph_names
    assert "cancer://b" in graph_names
    assert "cancer://meta" in graph_names

    # Provenance: meta graph should contain prov triples about each child graph.
    meta_graph = ds.graph(rdflib.URIRef("cancer://meta"))
    prov_subjects = {str(s) for s, _, _ in meta_graph.triples((None, rdflib.URIRef("http://www.w3.org/ns/prov#wasDerivedFrom"), None))}
    assert "cancer://a" in prov_subjects
    assert "cancer://b" in prov_subjects


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
    # No graph.trig in a/ — assembler should still succeed and emit just meta.
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

- [ ] **Step 3: Run; confirm 3 fail.**

- [ ] **Step 4: Implement `graph/federation.py`.**

```python
# src/science_tool/graph/federation.py
"""Federated graph assembly: include each child's graph.trig as a named graph."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import rdflib
from rdflib import Dataset, Graph, Literal, URIRef
from rdflib.namespace import PROV, RDF

from science_tool.project_config import (
    ChildEntry,
    ProjectRole,
    load_project_config,
    resolve_child_path,
)

_URI_SCHEME = "cancer"


def _project_uri(project_id: str) -> URIRef:
    return URIRef(f"{_URI_SCHEME}://{project_id}")


def materialize_federated_graph(meta_root: Path) -> Path:
    """Materialize meta's federated graph.trig.

    Each child's knowledge/graph.trig is included as a named graph (one named
    graph per child id). Meta-level claims live in the cancer://meta named graph,
    along with provenance triples annotating each child graph.

    Returns the output path (meta_root/knowledge/graph.trig).
    Raises ValueError if meta_root is not a meta project.
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

    timestamp = Literal(datetime.now(timezone.utc).isoformat(), datatype=URIRef("http://www.w3.org/2001/XMLSchema#dateTime"))

    for child in cfg.children:
        child_uri = _project_uri(child.id)
        included = _include_child_graph(ds, child, child_uri)
        if included:
            meta_graph.add((child_uri, PROV.wasDerivedFrom, Literal(str(_child_graph_path(child)))))
            meta_graph.add((child_uri, PROV.generatedAtTime, timestamp))

    ds.serialize(destination=out_path, format="trig")
    return out_path


def _child_graph_path(child: ChildEntry) -> Path:
    return resolve_child_path(child) / "knowledge" / "graph.trig"


def _include_child_graph(ds: Dataset, child: ChildEntry, child_uri: URIRef) -> bool:
    """Read the child's graph.trig and add its triples under ``child_uri``.

    Returns True if a graph file was found and included.
    """
    src_path = _child_graph_path(child)
    if not src_path.is_file():
        return False
    target = ds.graph(child_uri)
    src = Graph()
    src.parse(src_path, format="trig")
    for triple in src:
        target.add(triple)
    return True
```

- [ ] **Step 5: Run tests; confirm 3 pass.**

- [ ] **Step 6: Run the full suite for regressions.**

- [ ] **Step 7: Commit.**

```bash
git add src/science_tool/graph/federation.py tests/test_graph_federation.py
git commit -m "feat(graph): federated graph materialization with named-graph-per-child"
```

---

## Task 7: Wire federated graph mode into `science:graph build`

**Files:**
- Modify: `~/d/science/science-tool/src/science_tool/cli.py` (locate `graph_build` — line ~552 in the current snapshot)
- Test: `~/d/science/science-tool/tests/test_graph_build_federated.py`

Behavior change: when `science:graph build` is invoked inside a `meta` project, automatically dispatch to `materialize_federated_graph` instead of the standard `materialize_graph`. No flag needed — the project's role determines the mode.

- [ ] **Step 1: Failing test.**

```python
# tests/test_graph_build_federated.py
from pathlib import Path

import pytest
from click.testing import CliRunner

from science_tool.cli import cli


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
    (a / "knowledge").mkdir()
    (a / "knowledge" / "graph.trig").write_text("""
@prefix ex: <https://example.org/> .
ex:a-claim a ex:Claim .
""", encoding="utf-8")

    monkeypatch.chdir(meta)
    runner = CliRunner()
    result = runner.invoke(cli, ["graph", "build"])
    assert result.exit_code == 0
    out = (meta / "knowledge" / "graph.trig").read_text(encoding="utf-8")
    # Federated output must contain a named-graph block for the child id.
    assert "cancer://a" in out or "<cancer://a>" in out
```

- [ ] **Step 2: Modify `graph_build` in `cli.py`** to dispatch on role.

  Concrete edit: at the start of `graph_build`, after computing `_project_root`, load the config and branch:

```python
from science_tool.project_config import ProjectRole, load_project_config
from science_tool.graph.federation import materialize_federated_graph

# inside graph_build, after _project_root is set:
try:
    _cfg = load_project_config(_project_root)
except Exception:
    _cfg = None

if _cfg is not None and _cfg.role == ProjectRole.META:
    trig_path = materialize_federated_graph(_project_root)
    click.echo(f"Materialized federated graph at {trig_path}")
    return

# ... existing standalone-graph path follows unchanged
```

- [ ] **Step 3: Run the new test; confirm green. Run full suite for regressions.**

- [ ] **Step 4: Commit.**

```bash
git add src/science_tool/cli.py tests/test_graph_build_federated.py
git commit -m "feat(cli): graph build auto-dispatches to federated mode in meta projects"
```

---

## Task 8: `science:status --federated` rollup

**Files:**
- Modify: `~/d/science/science-tool/src/science_tool/cli.py` (locate the `status` command via `grep -n "@.*\.command(\"status\")\|def status\b" src/science_tool/cli.py`)
- Create: `~/d/science/science-tool/src/science_tool/federation_status.py` (rollup logic, kept separate from CLI)
- Test: `~/d/science/science-tool/tests/test_status_federated.py`

The rollup walks meta's `children:`, generates each child's status using the existing per-project status renderer (refactor it into a callable function if it's currently inline in the CLI), and prefixes each section with the child's id and role. An umbrella header summarizes counts.

- [ ] **Step 1: Read** the current `status` command body. If status rendering is inline in the CLI, extract it into a function `render_project_status(project_root: Path) -> str` in a new module `src/science_tool/status_render.py` (this refactor itself should be one small commit before the rest of the task — see Step 1a).

- [ ] **Step 1a: Refactor commit (if needed).**

```bash
# only if status logic is inline in CLI
git add src/science_tool/status_render.py src/science_tool/cli.py
git commit -m "refactor(status): extract render_project_status helper"
```

If the status logic is already in a separate module, skip Step 1a.

- [ ] **Step 2: Failing test for `--federated` flag.**

```python
# tests/test_status_federated.py
from pathlib import Path

import pytest
from click.testing import CliRunner

from science_tool.cli import cli


def test_status_federated_walks_children(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
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
    for child_dir, child_id, child_role in ((a, "a", "data-source"), (b, "b", "cancer-type")):
        (child_dir / "science.yaml").write_text(f"""
name: {child_id}
id: {child_id}
role: {child_role}
parent: {meta}
profile: research
research_question: "child {child_id}"
""", encoding="utf-8")

    monkeypatch.chdir(meta)
    runner = CliRunner()
    result = runner.invoke(cli, ["status", "--federated"])
    assert result.exit_code == 0
    # Output mentions both children and the meta umbrella section.
    assert "meta" in result.output.lower()
    assert "data-source" in result.output or "a" in result.output
    assert "cancer-type" in result.output or "b" in result.output


def test_status_federated_rejects_non_meta(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
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
    result = runner.invoke(cli, ["status", "--federated"])
    assert result.exit_code != 0
    assert "not a meta" in result.output.lower() or "not a meta" in (result.stderr or "")
```

- [ ] **Step 3: Implement `federation_status.py`.**

```python
# src/science_tool/federation_status.py
"""Federated status rollup: meta umbrella + per-child sections."""

from __future__ import annotations

from io import StringIO
from pathlib import Path

from science_tool.project_config import (
    ProjectRole,
    load_project_config,
    resolve_child_path,
)

# This import path is the conventional one created in Task 8 Step 1a (or already existing).
from science_tool.status_render import render_project_status


def render_federated_status(meta_root: Path) -> str:
    cfg = load_project_config(meta_root)
    if cfg.role != ProjectRole.META:
        raise ValueError(f"{meta_root} is role={cfg.role!r}; not a meta project")

    buf = StringIO()
    buf.write(f"# Federation: {cfg.id or meta_root.name}\n\n")
    buf.write(f"Children: {len(cfg.children)}\n\n")
    for child in cfg.children:
        buf.write(f"---\n\n## {child.id} ({child.role})\n\n")
        child_root = resolve_child_path(child)
        try:
            buf.write(render_project_status(child_root))
        except Exception as exc:  # surface but continue
            buf.write(f"(failed to render status: {exc})\n")
        buf.write("\n")

    buf.write(f"---\n\n## Meta ({cfg.id})\n\n")
    buf.write(render_project_status(meta_root))
    return buf.getvalue()
```

- [ ] **Step 4: Add `--federated` option to the existing `status` click command** in `cli.py`. When set, dispatch to `render_federated_status`; without it, behavior is unchanged.

- [ ] **Step 5: Run tests; full suite.**

- [ ] **Step 6: Commit.**

```bash
git add src/science_tool/federation_status.py src/science_tool/cli.py tests/test_status_federated.py
git commit -m "feat(status): --federated rollup walks meta children"
```

---

## Task 9: Integration test — round-trip with two real children

**Files:**
- Test: `~/d/science/science-tool/tests/test_federation_integration.py`

End-to-end: scaffold a meta + 2 children, run `sync`, run `graph build`, run `status --federated`, parse outputs, assert the federation is internally consistent.

- [ ] **Step 1: Write test.** Use the same fixture pattern from Task 4/8 but combined.

```python
# tests/test_federation_integration.py
from pathlib import Path

import pytest
import rdflib
from click.testing import CliRunner

from science_tool.cli import cli


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
        (path / "knowledge" / "graph.trig").write_text(f"""
@prefix ex: <https://example.org/> .
ex:{child_id}-claim a ex:Claim .
""", encoding="utf-8")


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

    # 1. sync from meta — should validate cleanly
    result = runner.invoke(cli, ["sync"])
    assert result.exit_code == 0, result.output

    # 2. graph build in meta — federated assembly
    result = runner.invoke(cli, ["graph", "build"])
    assert result.exit_code == 0, result.output

    # 3. status --federated
    result = runner.invoke(cli, ["status", "--federated"])
    assert result.exit_code == 0, result.output
    assert "a" in result.output
    assert "b" in result.output

    # 4. Parse the federated graph and confirm shape
    ds = rdflib.Dataset()
    ds.parse(meta / "knowledge" / "graph.trig", format="trig")
    graph_names = {str(g.identifier) for g in ds.graphs() if g.identifier != rdflib.URIRef("urn:x-rdflib:default")}
    assert {"cancer://a", "cancer://b", "cancer://meta"}.issubset(graph_names)
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
6. `science:status --federated` usage.
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

- [ ] **Step 2: Run `science:sync`** — must remain green and not start emitting warnings (since cbioportal still has no `parent:` and no `children:`, it should behave exactly as before).

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
| Phase 3 | Day-1 scaffolding for `meta/`, `mechanisms/evolution/`, `conditions/pre-cancer/`; foundational questions; cbioportal/MM `science.yaml` + README/AGENTS updates; first `science:status --federated` run | Immediately after Phase 2 |
| Phase 4 | First literature lap: PDF manifest pre-flight → triage → batched deep read with `science:paper-researcher` sub-agents → lap-1 synthesis | After Phase 3 |
| Phase 5+ | Subsequent laps; Federation v1.1+ features (deferred items in design §3.5) as real usage pressure justifies | Ongoing |

Plans for Phases 2–5 are written when their predecessors land, not preemptively, to avoid designing against a moving target. Phase 1 is the only blocker for the rest of the rollout.

---

## Self-review notes

- **Spec coverage.** Each numbered piece of design §3.6's effort table maps to a task here:
  - `science.yaml` schema additions + validators → Tasks 1, 2
  - `children:` manifest support in `science:sync` → Task 4 (with Task 3 as the validation library)
  - Addressing convention doc + URI form → Tasks 5, 10
  - `create-graph` / `update-graph` federation mode → Tasks 6, 7
  - `science:status --federated` rollup → Task 8
  - Tests + docs → Task 9 (integration), Task 10 (docs), Task 11 (self-check), Task 12 (smoke)
- **Placeholder scan.** No "TBD"/"fill in details" left in the plan. Where the plan acknowledges discovery (the Task 0 orientation note, the conditional refactor in Task 8 Step 1a), it's because the existing CLI structure can't be assumed without reading the source — this is honest about the unknown rather than a hidden placeholder.
- **Type consistency.** `ProjectConfig`, `ChildEntry`, `ProjectRole`, `Address`, `FederationIssue` defined in Tasks 1/3/5 are referenced consistently in Tasks 4/6/7/8/9. `materialize_federated_graph(meta_root: Path) -> Path` matches between Task 6 and Task 7. `render_project_status(project_root: Path) -> str` is created (or extracted) in Task 8 Step 1a and consumed in Step 3.
- **Granularity.** Each step is 2–5 minutes for an engineer who's read Task 0. Tests-first throughout. Frequent commits (one per task at minimum, with Task 8 having an extra refactor commit if needed).
