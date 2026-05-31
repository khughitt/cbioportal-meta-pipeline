# science:code
# status: library
# science:end
"""Tests for reusable pipeline datapackage descriptors."""

from __future__ import annotations

import hashlib
from pathlib import Path

from write_datapackage import build_datapackage, build_resource_descriptor


def test_build_resource_descriptor_records_relative_path_size_and_hash(
    tmp_path: Path,
) -> None:
    resource = tmp_path / "tables" / "table.feather"
    resource.parent.mkdir()
    resource.write_bytes(b"abc123")

    descriptor = build_resource_descriptor(
        resource,
        base_dir=tmp_path,
        name="table",
        role="data",
    )

    assert descriptor == {
        "name": "table",
        "path": "tables/table.feather",
        "format": "feather",
        "bytes": 6,
        "hash": f"sha256:{hashlib.sha256(b'abc123').hexdigest()}",
        "role": "data",
    }


def test_build_datapackage_records_provenance_access_and_resources(
    tmp_path: Path,
) -> None:
    table = tmp_path / "table.tsv"
    table.write_text("a\tb\n1\t2\n")
    qa = tmp_path / "qa.md"
    qa.write_text("# QA\n")

    package = build_datapackage(
        name="cbioportal-cleanbase",
        title="cBioPortal clean mutation substrate",
        resources=[
            build_resource_descriptor(table, base_dir=tmp_path, name="table"),
            build_resource_descriptor(qa, base_dir=tmp_path, name="qa", role="qa"),
        ],
        source_dataset="dataset:cbioportal",
        generated_by="rule package_per_study_mutation_substrates",
        access="public source; generated files are local workflow artifacts",
        license="see upstream cBioPortal study terms",
    )

    assert package["profile"] == "tabular-data-package"
    assert package["name"] == "cbioportal-cleanbase"
    assert package["source_dataset"] == "dataset:cbioportal"
    assert package["generated_by"] == "rule package_per_study_mutation_substrates"
    assert (
        package["access"]
        == "public source; generated files are local workflow artifacts"
    )
    assert package["license"] == "see upstream cBioPortal study terms"
    assert [resource["name"] for resource in package["resources"]] == ["table", "qa"]
