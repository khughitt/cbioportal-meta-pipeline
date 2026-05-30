# science:code
# status: workflow-owned
# science:end
#
# combine_mut_per_cancer_type.py (t131)
#
# Aggregate per-study `dndscv_input.feather` files into per-(cancer_type, build)
# combined MAFs. Used by `checkpoint combine_mut_per_cancer_type` in the
# Snakefile so downstream `run_dndscv_per_cancer` can fan out over the
# discovered (cancer_type, build) tuples.
#
# Inputs (snek.input):
#   list of studies/{id}/mut/dndscv_input.feather paths
#
# Output (snek.output[0]):
#   directory: summary/mut/dndscv_input/
#       Contains, per (cancer_type, build) group:
#         {slug}/mut_combined.feather         — combined SNV rows
#         {slug}/cohort_meta.feather          — cohort-level metadata
#
#   {slug} = "{cancer_type_slug}__{build}" with cancer-type slugified
#   (lowercase, non-alphanumeric -> "_") so it survives wildcard regex.
#
# Behavior:
#   - Drops rows with empty cancer_type.
#   - If config["dndscv_wes_only"] is true, drops rows with modality=="panel"
#     before grouping.
#   - Cohorts smaller than config["dndscv_min_samples"] (default 50) or with
#     fewer than config["dndscv_min_variants"] (default 500) are still written
#     but cohort_meta.feather marks `below_threshold = True`. Downstream
#     run_dndscv_per_cancer inspects this flag and skips dndscv invocation,
#     emitting an empty per-gene feather + status flag instead.
#
import json
import re
import shutil
from pathlib import Path

import pandas as pd

snek = snakemake  # type: ignore[name-defined]  # noqa: F821

OUT_DIR = Path(snek.output[0])
WES_ONLY = bool(snek.config.get("dndscv_wes_only", False))
MIN_SAMPLES = int(snek.config.get("dndscv_min_samples", 50))
MIN_VARIANTS = int(snek.config.get("dndscv_min_variants", 500))


def _slugify(s: str) -> str:
    """Slug for filesystem path. Keeps alphanumerics + underscores."""
    return re.sub(r"[^A-Za-z0-9]+", "_", str(s).strip()).strip("_").lower()


def _classify_modality(values: pd.Series) -> str:
    """wes / panel / mixed depending on per-row modality distribution."""
    uniq = set(values.dropna().astype(str).unique())
    if uniq == {"wes"}:
        return "wes"
    if uniq == {"panel"}:
        return "panel"
    if uniq <= {"wes", "panel"}:
        return "mixed"
    # Unknown values bubble up so we don't silently mislabel.
    return "mixed"


def _write_group(
    group_df: pd.DataFrame, cancer_type: str, build: str, slug: str
) -> dict:
    out_subdir = OUT_DIR / slug
    out_subdir.mkdir(parents=True, exist_ok=True)

    n_variants = len(group_df)
    n_samples = group_df["sample_id"].nunique()
    modality = _classify_modality(group_df["modality"])
    panel_only = modality == "panel"
    below_threshold = n_samples < MIN_SAMPLES or n_variants < MIN_VARIANTS

    # Drop derived/grouping columns when serializing the MAF; dndscv only
    # needs sample_id / chr / pos / ref / alt.
    maf_cols = ["sample_id", "chr", "pos", "ref", "alt"]
    maf = group_df[maf_cols].reset_index(drop=True)
    maf.to_feather(out_subdir / "mut_combined.feather")

    cohort_meta = pd.DataFrame(
        [
            {
                "cancer_type": cancer_type,
                "build": build,
                "slug": slug,
                "n_samples": n_samples,
                "n_variants": n_variants,
                "modality": modality,
                "panel_only": panel_only,
                "below_threshold": below_threshold,
                "min_samples_threshold": MIN_SAMPLES,
                "min_variants_threshold": MIN_VARIANTS,
            }
        ]
    )
    cohort_meta.to_feather(out_subdir / "cohort_meta.feather")

    return {
        "slug": slug,
        "cancer_type": cancer_type,
        "build": build,
        "n_samples": n_samples,
        "n_variants": n_variants,
        "modality": modality,
        "below_threshold": below_threshold,
    }


# ---------------------------------------------------------------------------
# Aggregate.
# ---------------------------------------------------------------------------
print(f"combine_mut_per_cancer_type: reading {len(snek.input):,} per-study inputs")

frames = []
for path in snek.input:
    df = pd.read_feather(path)
    if df.empty:
        continue
    frames.append(df)

# Reset OUT_DIR to a clean state so stale tuples from a previous run don't
# linger in the checkpoint directory and confuse downstream rule expansion.
if OUT_DIR.exists():
    shutil.rmtree(OUT_DIR)
OUT_DIR.mkdir(parents=True, exist_ok=True)

manifest_rows: list[dict] = []

if not frames:
    print("combine_mut_per_cancer_type: no input rows; writing empty manifest")
    pd.DataFrame(
        columns=pd.Index(
            [
                "slug", "cancer_type", "build", "n_samples", "n_variants",
                "modality", "below_threshold",
            ]
        )
    ).to_feather(OUT_DIR / "manifest.feather")
else:
    combined = pd.concat(frames, ignore_index=True)
    print(
        f"combine_mut_per_cancer_type: combined {len(combined):,} rows from "
        f"{len(frames):,} non-empty studies"
    )

    # Drop rows missing cancer_type (cannot be assigned to a cohort).
    combined = combined.dropna(subset=["cancer_type"]).copy()
    combined["cancer_type"] = combined["cancer_type"].astype(str)

    if WES_ONLY:
        n_pre = len(combined)
        combined = combined[combined["modality"].astype(str) != "panel"].copy()
        print(
            f"combine_mut_per_cancer_type: dndscv_wes_only=True dropped "
            f"{n_pre - len(combined):,} panel rows"
        )

    # Group and write.
    for (cancer_type, build), grp in combined.groupby(
        ["cancer_type", "build"], observed=True
    ):
        slug = f"{_slugify(cancer_type)}__{build}"
        manifest_rows.append(_write_group(grp, str(cancer_type), str(build), slug))

    manifest = pd.DataFrame(manifest_rows)
    manifest.to_feather(OUT_DIR / "manifest.feather")

    print(
        f"combine_mut_per_cancer_type: wrote {len(manifest_rows)} (cancer_type, "
        f"build) groups; below-threshold = "
        f"{manifest['below_threshold'].sum() if not manifest.empty else 0}"
    )

# Drop a JSON sidecar for human-readable inspection.
(OUT_DIR / "manifest.json").write_text(
    json.dumps(
        [
            {
                "slug": r["slug"],
                "cancer_type": r["cancer_type"],
                "build": r["build"],
                "n_samples": int(r["n_samples"]),
                "n_variants": int(r["n_variants"]),
                "modality": r["modality"],
                "below_threshold": bool(r["below_threshold"]),
            }
            for r in manifest_rows
        ],
        indent=2,
    )
)
