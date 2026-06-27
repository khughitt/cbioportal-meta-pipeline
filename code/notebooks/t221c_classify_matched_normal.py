# science:code
# status: exploratory
# science:end
"""t221(c) — evidence-derived classification of patient-matched-normal studies for `matched_normal_studies`.

Task: t221 follow-up. t221(b) F3 flagged that `config-full.yml` carries no `matched_normal_studies` list,
so a true matched/unmatched-normal germline-leak split could not be run (only the dbSNP proxy). This script
populates that list from evidence, reproducibly, instead of hand-asserting it.

Definition used (the rigorous, derivable one): a study uses **patient-matched normal** sequencing if its
per-variant normal barcode (`sample_id_norm`) comes from the SAME patient as the tumor barcode
(`sample_id_tumor`). We test that directly per row via a longest-common-prefix (LCP) patient-stem match:
a normal barcode that shares the tumor's leading identifier (TCGA `...-01` tumour vs `...-10/-11` normal;
pog `11004` vs `11004_N`) is patient-matched; a pooled / panel-of-normals barcode (one constant value) or
an absent/`nan` normal is not. The fraction of rows passing this test is `stem_match`; a study is called
matched if `stem_match >= STEM_THR`.

This is a HIGH-PRECISION LOWER BOUND, which is exactly what the config comment asks for ("populate
conservatively ... studies not in this list are treated as tumor-only"):
  * A study that records patient-matched normal barcodes definitely did matched-normal sequencing -> matched.
  * A study that records NO per-variant normal (e.g. the MSK-IMPACT family: matched-by-design buffy-coat
    normal, but the public MAF does not carry the normal barcode) scores stem_match=0 here and is
    conservatively left OUT. Those by-design-matched-but-unrecorded cohorts are reported separately so a
    human can opt to add them; we do not assert them automatically (no fabrication beyond the evidence).

Outputs: an audit table over every `full` study and the proposed `matched_normal_studies` block to paste
into config-full.yml.

Run:  uv run --frozen python code/notebooks/t221c_classify_matched_normal.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pyarrow as pa
import yaml

CONFIG = Path("code/config/config-full.yml")
PACKAGE_ROOT = Path("/") / "data" / "packages" / "cbioportal"
STUDY_DIR = PACKAGE_ROOT / "full/studies"
OUT = Path("results/neural-gene-matched-normal-2026-06-08")

STEM_THR = 0.50  # fraction of variant rows whose normal shares the tumour's patient stem
MIN_LCP = 4  # minimum shared leading characters to count as a patient-stem match
LCP_FRAC = 0.40  # ... and at least this fraction of the tumour barcode length
PLACEHOLDERS = {"", "nan", "none", "na", "n/a", ".", "-", "<na>", "normal", "unmatched", "pool", "pooled", "pon"}
# matched-by-design cohorts that the public MAF does not stamp with a per-variant normal barcode, so the
# evidence test cannot see them. Reported (not auto-added) so a human can opt in. MSK-IMPACT sequences a
# matched buffy-coat normal (panel_bearing_studies); tcga_mc3 is matched by design (AGENTS.md).
BY_DESIGN_UNRECORDED = {"msk_impact_2017", "msk_chord_2024", "msk_impact_50k_2026", "tcga_mc3"}


def lcp_len(a: str, b: str) -> int:
    a, b = str(a), str(b)
    n = min(len(a), len(b))
    i = 0
    while i < n and a[i] == b[i]:
        i += 1
    return i


def classify(study: str) -> dict:
    path = STUDY_DIR / study / "mut/table/mut_filtered.feather"
    base = {"study": study, "has_table": False, "has_norm_col": False, "n_tumor": 0,
            "frac_real_norm": 0.0, "norm_per_tumor": 0.0, "stem_match": 0.0, "matched": False}
    if not path.exists():
        return base
    base["has_table"] = True
    with pa.memory_map(str(path), "r") as src:
        names = set(pa.ipc.open_file(src).schema.names)
    if "sample_id_norm" not in names or "sample_id_tumor" not in names:
        return base
    base["has_norm_col"] = True
    mf = pd.read_feather(path, columns=["sample_id_tumor", "sample_id_norm"])
    # fillna("") first: nullable string dtypes keep pd.NA through astype(str), which then leaks float NaN
    # into the row iteration. Empty string is caught by the placeholder set.
    t = mf["sample_id_tumor"].fillna("").astype(str).str.strip()
    n = mf["sample_id_norm"].fillna("").astype(str).str.strip()
    real = ~n.str.lower().isin(PLACEHOLDERS)
    base["n_tumor"] = int(t.nunique())
    base["frac_real_norm"] = round(float(real.mean()), 4)
    if real.any():
        tt = t[real].to_numpy()
        nn = n[real].to_numpy()
        base["norm_per_tumor"] = round(float(pd.Series(nn).nunique() / max(base["n_tumor"], 1)), 3)
        hits = sum(
            1 for a, b in zip(tt, nn) if lcp_len(a, b) >= MIN_LCP and lcp_len(a, b) >= LCP_FRAC * max(len(a), 1)
        )
        base["stem_match"] = round(hits / len(tt), 4)
    base["matched"] = bool(base["stem_match"] >= STEM_THR)
    return base


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = yaml.safe_load(CONFIG.read_text())
    studies = [s for s in cfg["studies"] if s != "genie"]  # genie is the AACR pseudo-study (no single MAF)
    print(f"classifying {len(studies)} studies from {CONFIG} ...")

    rows = [classify(s) for s in studies]
    audit = pd.DataFrame(rows).sort_values(["matched", "stem_match"], ascending=[False, False])
    matched = sorted(audit.loc[audit["matched"], "study"].tolist())
    by_design = sorted(s for s in BY_DESIGN_UNRECORDED if s in set(studies) and s not in set(matched))

    audit.to_csv(OUT / "matched_normal_audit.tsv", sep="\t", index=False)
    (OUT / "proposed_matched_normal_studies.json").write_text(
        json.dumps({"matched_evidence": matched, "by_design_unrecorded_not_added": by_design}, indent=2)
    )

    datapackage = {
        "name": "neural-gene-matched-normal-2026-06-08",
        "title": "t221(c) evidence-derived matched_normal_studies classification for config-full",
        "description": "Classifies each full-config study as patient-matched-normal via per-variant "
        "normal-barcode patient-stem match (stem_match >= %.2f). High-precision lower bound; matched-by-"
        "design cohorts that do not record a per-variant normal barcode (MSK-IMPACT family, tcga_mc3) are "
        "reported separately, not auto-added." % STEM_THR,
        "created": "2026-06-08",
        "tasks": ["t221"],
        "related": [
            "hypothesis:h12-neural-gene-enrichment-length-histology-artifact",
            "question:q016-panel-induced-ascertainment",
            "interpretation:2026-06-08-t221b-standing-controls-panel",
        ],
        "resources": [
            {"name": "matched_normal_audit", "path": "matched_normal_audit.tsv"},
            {"name": "proposed_matched_normal_studies", "path": "proposed_matched_normal_studies.json"},
        ],
        "parameters": {"stem_threshold": STEM_THR, "min_lcp": MIN_LCP, "lcp_frac": LCP_FRAC},
    }
    (OUT / "datapackage.json").write_text(json.dumps(datapackage, indent=2))

    n_total = len(studies)
    n_notable = int((~audit["matched"] & (audit["stem_match"] > 0)).sum())
    print(f"\nmatched by evidence: {len(matched)} / {n_total} studies")
    print(f"by-design-but-unrecorded (NOT added): {by_design}")
    print(f"partial-stem (0 < stem_match < {STEM_THR}, NOT matched): {n_notable} studies")
    print("\n================ MATCHED (evidence) — top 20 by stem_match ================")
    pd.set_option("display.width", 200, "display.max_columns", 20)
    print(audit[audit["matched"]].head(20).to_string(index=False))
    print("\n================ PROPOSED matched_normal_studies BLOCK (paste into config-full.yml) ================")
    print("matched_normal_studies:")
    for s in matched:
        print(f"  - {s}")
    print(f"\nArtifacts written to {OUT}/")


if __name__ == "__main__":
    main()
