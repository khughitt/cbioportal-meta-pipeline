"""t218b — forensic on the single study that drives the t218 WES residual: pog570_bcgsc_2020.

t218's leave-one-study-out found that dropping pog570_bcgsc_2020 returns the candidate genes to the
genomic-span null (span-matched p 0.0022 -> 0.19). The t218 prose attributed this to "WGS whole-gene-body
reach". Code review (2026-06-08) flagged two gaps:
  (#2) the claim relied on the "WGS" assay label, but data/study_panels.tsv labels pog570 `wes`, and no
       artifact recorded the variant-class evidence; and
  (#1) the only implemented hypermutator-exclusion arm tested an ALREADY-non-significant pan-cancer arm,
       so it could not rule out hypermutators for the significant full-WES residual.

This script answers both directly from pog570's per-variant table
(`.../studies/pog570_bcgsc_2020/mut/table/mut_filtered.feather`) and per-sample annotations, and writes
the evidence as artifacts:

  * Variant-class breakdown of the candidate-gene rows. The mechanism is whole-gene-body / all-region
    sequencing, NOT the assay label: if the candidate rows are overwhelmingly intronic, the counts scale
    with genomic span regardless of whether the study is called wes/wgs.
  * Hypermutator audit: how many of pog570's samples are flagged is_hypermutator, and how concentrated
    the candidate rows are across samples. If pog570 carries no hypermutators (or the rows are diffuse),
    the residual it drives cannot be a hypermutator artifact.

Run:  uv run --frozen python code/notebooks/t218b_pog570_driver_forensics.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

CANDIDATES = [
    "NKAIN2",
    "KCNIP4",
    "FAM19A2",
    "RIT2",
    "CALN1",
    "RBFOX1",
    "LSAMP",
    "SGCZ",
    "OPCML",
]
STUDY = "pog570_bcgsc_2020"
MUT = Path(
    f"/data/packages/cbioportal/full/studies/{STUDY}/mut/table/mut_filtered.feather"
)
SAMPLES = Path("/data/packages/cbioportal/full/metadata/samples_annotated.feather")
PANELS = Path("data/study_panels.tsv")
OUT = Path("results/neural-gene-cns-wes-2026-06-08")


def coarse_region(consequence: str) -> str:
    """Collapse a (possibly comma-joined) VEP consequence string to a coarse genomic region."""
    c = str(consequence).lower()
    if (
        "missense" in c
        or "stop_gain" in c
        or "frameshift" in c
        or "inframe" in c
        or "start_lost" in c
        or "stop_lost" in c
    ):
        return "coding_nonsynonymous"
    if "synonymous" in c or "coding_sequence" in c or "incomplete_terminal" in c:
        return "coding_synonymous"
    if "splice" in c:
        return "splice"
    if "intron" in c:
        return "intronic"
    if "utr" in c:
        return "utr"
    if "upstream" in c or "downstream" in c or "intergenic" in c:
        return "flanking_intergenic"
    if "non_coding" in c or "nmd" in c:
        return "non_coding_other"
    return "other"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    mf = pd.read_feather(MUT)
    sa = pd.read_feather(SAMPLES)
    sa = sa[sa["study_id"] == STUDY]

    panel_label = "n/a"
    if PANELS.exists():
        p = pd.read_csv(PANELS, sep="\t")
        row = p[p["study_id"] == STUDY]
        if not row.empty:
            panel_label = "/".join(
                str(row.iloc[0][c]) for c in row.columns if c != "study_id"
            )

    n_samples = int(sa["sample_id"].nunique())
    n_hyper = int(sa["is_hypermutator"].fillna(False).sum())
    n_hyper_known = int(sa["is_hypermutator"].notna().sum())

    mf["region"] = mf["consequence"].map(coarse_region)
    cand = mf[mf["symbol"].isin(CANDIDATES)].copy()

    # variant-class (region) breakdown: candidates vs the whole study
    overall = mf["region"].value_counts()
    cand_reg = cand["region"].value_counts()
    region_tbl = (
        pd.DataFrame(
            {
                "study_rows": overall,
                "study_frac": (overall / len(mf)).round(4),
                "candidate_rows": cand_reg,
                "candidate_frac": (cand_reg / len(cand)).round(4),
            }
        )
        .fillna(0)
        .sort_values("candidate_rows", ascending=False)
    )
    region_tbl.index.name = "region"

    # per-candidate intronic vs coding split
    cand["is_intronic"] = cand["region"].eq("intronic")
    cand["is_coding"] = cand["region"].isin(
        ["coding_nonsynonymous", "coding_synonymous"]
    )
    per_gene = cand.groupby("symbol").agg(
        rows=("region", "size"),
        intronic_rows=("is_intronic", "sum"),
        coding_rows=("is_coding", "sum"),
    )
    per_gene["intronic_frac"] = (per_gene["intronic_rows"] / per_gene["rows"]).round(4)
    per_gene = per_gene.reindex(CANDIDATES)

    # sample concentration of candidate rows (diffuse vs single-sample)
    by_sample = cand["sample_id_tumor"].value_counts()
    top_share = float(by_sample.iloc[0] / len(cand)) if len(by_sample) else float("nan")

    n_cand = len(cand)
    n_intronic = int(cand["is_intronic"].sum())
    n_coding_nonsyn = int((cand["region"] == "coding_nonsynonymous").sum())

    summary = {
        "study": STUDY,
        "study_panels_label": panel_label,
        "n_samples": n_samples,
        "n_hypermutator_samples": n_hyper,
        "n_samples_hypermutator_known": n_hyper_known,
        "study_total_variant_rows": int(len(mf)),
        "study_intronic_frac": round(float(mf["region"].eq("intronic").mean()), 4),
        "candidate_variant_rows": n_cand,
        "candidate_intronic_rows": n_intronic,
        "candidate_intronic_frac": round(n_intronic / n_cand, 4),
        "candidate_coding_nonsyn_rows": n_coding_nonsyn,
        "candidate_rows_n_samples": int(cand["sample_id_tumor"].nunique()),
        "candidate_rows_top_sample_share": round(top_share, 4),
    }

    region_tbl.to_csv(OUT / "pog570_candidate_variant_class.tsv", sep="\t")
    per_gene.to_csv(OUT / "pog570_per_candidate_region.tsv", sep="\t")
    (OUT / "pog570_driver_forensics.json").write_text(json.dumps(summary, indent=2))

    print(f"[{STUDY}] study_panels label = {panel_label}")
    print(
        f"  samples = {n_samples}; hypermutator samples = {n_hyper}/{n_hyper_known} known"
    )
    print(
        f"  study total variant rows = {len(mf):,} ({summary['study_intronic_frac']:.0%} intronic)"
    )
    print(
        f"  candidate rows = {n_cand:,} -> {summary['candidate_intronic_frac']:.1%} intronic, "
        f"{n_coding_nonsyn} coding-nonsynonymous"
    )
    print(
        f"  candidate rows spread over {summary['candidate_rows_n_samples']} samples; "
        f"top sample = {top_share:.1%}"
    )
    print("\n================ CANDIDATE VARIANT-CLASS (region) ================")
    print(region_tbl.to_string())
    print("\n================ PER-CANDIDATE INTRONIC FRACTION ================")
    print(per_gene.to_string())
    print(f"\nArtifacts written to {OUT}/")


if __name__ == "__main__":
    main()
