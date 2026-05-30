# science:code
# status: workflow-owned
# science:end
"""create_combined_sample_table.py.

Two outputs:
  1. The existing cancer-type combined table (concat of per-study
     samples feathers, projected to the canonical 4 columns).
  2. NEW (t078): sample_panel_map.feather mapping (study_id, sample_id)
     to panel_id, sourced from:
       - GENIE assay table (per-sample, study_id == 'genie_v9.1')
       - data/study_panels.tsv (per-study, sequencing_type='panel')
       - 'wes' pseudo-panel (per-study, sequencing_type='wes')
"""

from pathlib import Path

import pandas as pd

CANONICAL_COLS = ["patient_id", "sample_id", "cancer_type", "cancer_type_detailed"]
GENIE_STUDY_ID = "genie_v9.1"


def _derive_study_id(samples_path: Path) -> str:
    """Recover study_id from a per-study samples.feather path.

    Real layout: studies/{id}/metadata/samples.feather -> parents[1].name.
    Tests/legacy layout: {id}_samples.feather -> stem with suffix stripped.
    """
    p = Path(samples_path)
    if p.parent.name == "metadata" and p.parent.parent.name not in ("", "/"):
        return p.parent.parent.name
    stem = p.stem
    return stem.removesuffix("_samples") if stem.endswith("_samples") else stem


def _load_genie_assay_map(path: Path) -> pd.DataFrame:
    """Return (study_id, sample_id, panel_id) DataFrame.

    Accepts two input formats:
      1. Clean TSV with columns study_id, sample_id, panel_id.
      2. cBioPortal-style data_clinical_sample.txt: header rows prefixed by '#',
         actual columns on the first non-comment row, including
         'Sample Identifier' and 'Sequence Assay ID'. study_id is set to
         GENIE_STUDY_ID for every row.
    """
    p = Path(path)
    if not p.exists():
        return pd.DataFrame(columns=["study_id", "sample_id", "panel_id"])

    with p.open() as fh:
        first = fh.readline()
    if first.startswith("#"):
        df = pd.read_csv(p, sep="\t", comment="#")
        rename: dict[str, str] = {}
        for cand_sid in ("Sample Identifier", "SAMPLE_ID"):
            if cand_sid in df.columns:
                rename[cand_sid] = "sample_id"
                break
        for cand_pid in ("Sequence Assay ID", "SEQ_ASSAY_ID"):
            if cand_pid in df.columns:
                rename[cand_pid] = "panel_id"
                break
        if "sample_id" not in rename.values() or "panel_id" not in rename.values():
            raise KeyError(
                f"GENIE clinical sample file {p} missing Sample Identifier or "
                f"Sequence Assay ID columns; got {list(df.columns)}"
            )
        df = df.rename(columns=rename)[["sample_id", "panel_id"]].copy()
        df["study_id"] = GENIE_STUDY_ID
        return df[["study_id", "sample_id", "panel_id"]]

    return pd.read_csv(p, sep="\t")


def build_combined_sample_table(input_paths: list[Path], out_path: Path) -> None:
    dfs = [pd.read_feather(p)[CANONICAL_COLS] for p in input_paths]
    df = pd.concat(dfs)
    df["patient_id"] = df["patient_id"].astype("str")
    df["sample_id"] = df["sample_id"].astype("str")
    df["cancer_type"] = df["cancer_type"].astype("category")
    df["cancer_type_detailed"] = df["cancer_type_detailed"].astype("category")
    df.to_feather(out_path)


def build_sample_panel_map(
    per_study_samples_paths: list[Path],
    study_panels_tsv: Path,
    genie_assay_table: Path,
    out_path: Path,
) -> None:
    """Emit metadata/sample_panel_map.feather per design Section 1.4."""
    study_panels = pd.read_csv(study_panels_tsv, sep="\t")
    sp_lookup = study_panels.set_index("study_id")[["panel_id", "sequencing_type"]]

    genie = _load_genie_assay_map(Path(genie_assay_table))

    rows: list[pd.DataFrame] = []
    for p in per_study_samples_paths:
        sid = _derive_study_id(Path(p))
        df = pd.read_feather(p)
        if "study_id" not in df.columns:
            df = df.assign(study_id=sid)

        if sid == GENIE_STUDY_ID:
            sub_g = df[["study_id", "sample_id"]].merge(
                genie[["sample_id", "panel_id"]],
                on="sample_id",
                how="left",
                validate="many_to_one",
            )
            if sub_g["panel_id"].isna().any():
                missing = sub_g[sub_g["panel_id"].isna()]["sample_id"].head(3).tolist()
                raise KeyError(f"GENIE samples missing from assay table: {missing} ...")
            sub_g["panel_source"] = "genie_assay_table"
            rows.append(sub_g[["study_id", "sample_id", "panel_id", "panel_source"]])
            continue

        if sid not in sp_lookup.index:
            raise KeyError(
                f"study {sid!r} missing from study_panels.tsv -- "
                "add it before running the SELECT pipeline"
            )
        panel_id = sp_lookup.at[sid, "panel_id"]
        seq_type = sp_lookup.at[sid, "sequencing_type"]
        panel_source = "wes_default" if seq_type == "wes" else "study_panels_tsv"
        mapped = df[["sample_id"]].copy()
        mapped["study_id"] = sid
        mapped["panel_id"] = panel_id
        mapped["panel_source"] = panel_source
        rows.append(mapped[["study_id", "sample_id", "panel_id", "panel_source"]])

    out = pd.concat(rows, ignore_index=True)
    out["study_id"] = out["study_id"].astype("string")
    out["sample_id"] = out["sample_id"].astype("string")
    out["panel_id"] = out["panel_id"].astype("string")
    out["panel_source"] = out["panel_source"].astype("string")
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_feather(out_path)


if "snakemake" in globals():  # pragma: no cover  # set by Snakemake's script: directive
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    per_study_paths = [Path(p) for p in snek.input["per_study"]]
    build_combined_sample_table(
        input_paths=per_study_paths,
        out_path=Path(snek.output["combined"]),
    )
    build_sample_panel_map(
        per_study_samples_paths=per_study_paths,
        study_panels_tsv=Path(snek.input["study_panels"]),
        genie_assay_table=Path(snek.input["genie_assay_table"]),
        out_path=Path(snek.output["sample_panel_map"]),
    )
