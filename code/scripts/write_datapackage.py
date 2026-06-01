# science:code
# status: workflow-owned
# science:end
"""Write small Frictionless-style datapackage descriptors for workflow products."""

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


def build_resource_descriptor(
    path: Path,
    *,
    base_dir: Path,
    name: str | None = None,
    role: str = "data",
    file_format: str | None = None,
) -> dict[str, Any]:
    """Build a resource descriptor with relative path, byte size, and SHA-256."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    descriptor = {
        "name": name or _resource_name(path),
        "path": path.relative_to(base_dir).as_posix(),
        "format": file_format or _infer_format(path),
        "bytes": path.stat().st_size,
        "hash": f"sha256:{_sha256(path)}",
        "role": role,
    }
    return descriptor


def build_datapackage(
    *,
    name: str,
    title: str,
    resources: Sequence[Mapping[str, Any]],
    source_dataset: str,
    generated_by: str,
    access: str,
    license: str,
    description: str | None = None,
) -> dict[str, Any]:
    """Build a minimal datapackage descriptor for a reusable pipeline substrate."""
    package: dict[str, Any] = {
        "name": name,
        "title": title,
        "profile": "tabular-data-package",
        "source_dataset": source_dataset,
        "generated_by": generated_by,
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "access": access,
        "license": license,
        "resources": list(resources),
    }
    if description:
        package["description"] = description
    return package


def write_datapackage(path: Path, package: Mapping[str, Any]) -> None:
    """Write a datapackage descriptor as stable, indented JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(package, indent=2, sort_keys=True) + "\n")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _resource_name(path: Path) -> str:
    name = path.name
    for suffix in (
        ".tar.gz",
        ".feather",
        ".parquet",
        ".tsv",
        ".txt",
        ".json",
        ".md",
        ".xlsx",
    ):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return path.stem


def _infer_format(path: Path) -> str:
    name = path.name
    if name.endswith(".tar.gz"):
        return "tar.gz"
    suffix = path.suffix.lstrip(".")
    return suffix or "binary"


def _snakemake_items(named_input: Any) -> list[tuple[str, Path]]:
    items = getattr(named_input, "items", None)
    if callable(items):
        return [(str(name), Path(value)) for name, value in items()]
    return [
        (f"resource_{index + 1}", Path(value))
        for index, value in enumerate(named_input)
    ]


def _params_dict(params: Any) -> dict[str, Any]:
    items = getattr(params, "items", None)
    if callable(items):
        return dict(items())
    return {}


def _run_from_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    params = _params_dict(snek.params)
    output = Path(snek.output[0])
    base_dir = Path(params.get("base_dir", output.parent))
    roles = params.get("resource_roles", {})
    formats = params.get("resource_formats", {})
    resources = [
        build_resource_descriptor(
            path,
            base_dir=base_dir,
            name=name,
            role=roles.get(name, "data"),
            file_format=formats.get(name),
        )
        for name, path in _snakemake_items(snek.input)
    ]
    package = build_datapackage(
        name=params["package_name"],
        title=params["title"],
        resources=resources,
        source_dataset=params["source_dataset"],
        generated_by=params["generated_by"],
        access=params["access"],
        license=params["license"],
        description=params.get("description"),
    )
    write_datapackage(output, package)


if "snakemake" in globals():
    _run_from_snakemake()
