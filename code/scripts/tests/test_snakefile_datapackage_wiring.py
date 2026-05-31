# science:code
# status: library
# science:end
"""Verify reusable substrate datapackages are exposed as Snakemake targets."""

from __future__ import annotations

from pathlib import Path

SNAKEFILE = Path(__file__).resolve().parents[3] / "code" / "workflows" / "Snakefile"
DATASETS = Path(__file__).resolve().parents[3] / "doc" / "datasets"


EXPECTED_PACKAGE_RULES = {
    "package_per_study_mutation_substrates": "studies/{id}/datapackage.json",
    "package_driver_overlay_registry": "metadata/driver_overlays/datapackage.json",
    "package_genie_panel_registry": "metadata/genie_panel_registry/datapackage.json",
    "package_normal_tissue_spectra": "normal_tissue_datapackage.json",
    "package_replication_timing_annotations": "replication_timing_datapackage.json",
    "package_gene_cancer_ratio_product": (
        "summary/mut/table/gene_cancer_study_ratio_annotated.datapackage.json"
    ),
}

EXPECTED_DATASET_DOCS = [
    "data-cbioportal-per-study-mutation-cleanbase.md",
    "data-driver-overlay-registry.md",
    "data-genie-panel-callable-registry.md",
]


def test_datapackage_rules_present_and_use_shared_writer() -> None:
    text = SNAKEFILE.read_text()

    for rule_name, output_path in EXPECTED_PACKAGE_RULES.items():
        block = _extract_rule_block(text, rule_name)
        assert output_path in block
        assert "write_datapackage.py" in block


def test_all_datapackages_target_collects_reusable_manifests() -> None:
    text = SNAKEFILE.read_text()
    block = _extract_rule_block(text, "all_datapackages")

    assert "datapackage_reports" in block
    for output_path in EXPECTED_PACKAGE_RULES.values():
        assert output_path in text


def test_cleanbase_dataset_docs_exist_with_manifest_paths() -> None:
    for filename in EXPECTED_DATASET_DOCS:
        text = (DATASETS / filename).read_text()
        assert "datapackage" in text.lower()
        assert "source_class:" in text
        assert "access" in text.lower()


def _extract_rule_block(text: str, rule_name: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_rule = False
    rule_indent = ""
    for line in lines:
        stripped = line.lstrip()
        indent = line[: len(line) - len(stripped)]
        if stripped.startswith(f"rule {rule_name}:"):
            in_rule = True
            rule_indent = indent
            out.append(line)
            continue
        if in_rule:
            if line.strip() == "":
                out.append(line)
                continue
            if len(indent) > len(rule_indent):
                out.append(line)
            else:
                break
    assert out, f"rule {rule_name} not found"
    return "\n".join(out)
