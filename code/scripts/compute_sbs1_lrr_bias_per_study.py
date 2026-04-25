"""compute_sbs1_lrr_bias_per_study.

Per-study aggregate SBS1 late-replicating-region (LRR) bias test for q009.

Closes task t124 by implementing the per-study aggregate version of the Yaacov 2023
statistic — the only formulation matching both the published mechanism and q009's
framing as a single-study contamination flag. Reuses existing artifacts from t109/t110
(per-sample restricted SigProfilerAssignment) and t121 (gene-level constitutive RT map +
50kb bins). All thresholds and the decision rule are pre-registered in
doc/meta/pre-registration-t126-sbs1-lrr-bias-test.md and must not be moved post-hoc.

Method (per pre-registration §3-§5):

  1. For each SNV in the per-study mut.feather, compute the 96-trinucleotide context by
     reading SigProfilerMatrixGenerator's TSB binary chromosome files and applying the
     pyrimidine-strand convention.
  2. Compute per-mutation SBS1 posterior using per-sample exposures from
     restricted_assignment_per_sample.feather (Bayesian: per-sample exposures as prior,
     COSMIC context probability as likelihood).
  3. Map each mutation to the t121 50kb constitutive RT bin label (CE / CL / unassigned).
  4. Sum SBS1 posteriors per (study, RT bin); divide by panel-coverage-corrected bp to
     get density; compute corrected LRR fraction = rho_CL / (rho_CE + rho_CL).
  5. Cluster-bootstrap by sample for 95% CI. Apply pre-registered decision rule.

Outputs ``sbs1_lrr_bias_per_study.feather`` with one row per (study, lookup_key) and a
``verdict`` column in {pass, retire, defer}.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from resolve_panel_id import normalize_panel_id

# COSMIC v3.4 reference under SigProfilerAssignment (matches the version t109 used).
COSMIC_VERSION: str = "3.4"
GENOME_BUILD: str = "GRCh37"

# Pyrimidine-strand contexts; identical ordering to extract_normal_tissue_spectra.CONTEXT_96
# (verified A[C>A]A first, T[T>G]T last).
_SUBS = ("C>A", "C>G", "C>T", "T>A", "T>C", "T>G")
_BASES = ("A", "C", "G", "T")
CONTEXT_96: list[str] = [
    f"{five}[{sub}]{three}" for five in _BASES for sub in _SUBS for three in _BASES
]

# Reverse complement for pyrimidine-strand normalisation.
_RC = str.maketrans("ACGT", "TGCA")

# TSB binary lookup table from SigProfilerMatrixGenerator. Bytes 0..15 carry the
# {strand, base} pair; bytes 16..19 are N variants. We only need the base.
_TSB_BASE: dict[int, str] = {
    0: "A",
    1: "C",
    2: "G",
    3: "T",
    4: "A",
    5: "C",
    6: "G",
    7: "T",
    8: "A",
    9: "C",
    10: "G",
    11: "T",
    12: "A",
    13: "C",
    14: "G",
    15: "T",
    16: "N",
    17: "N",
    18: "N",
    19: "N",
}


def decode_tsb_byte(byte_value: int) -> str:
    return _TSB_BASE.get(byte_value, "N")


# ---------------------------------------------------------------------------
# Trinucleotide context lookup
# ---------------------------------------------------------------------------


_CHROM_CACHE: dict[tuple[str, str], bytes] = {}


def _load_chromosome_bytes(chrom: str, chrom_dir: Path) -> bytes:
    key = (str(chrom_dir), chrom)
    if key not in _CHROM_CACHE:
        path = chrom_dir / f"{chrom}.txt"
        with path.open("rb") as fh:
            _CHROM_CACHE[key] = fh.read()
    return _CHROM_CACHE[key]


def lookup_trinucleotide_context(
    *, chrom: str, pos: int, ref: str, alt: str, chrom_dir: Path
) -> str | None:
    """Return the pyrimidine-strand 96-context label for an SNV, else None.

    The TSB binary stores chr position 1 at byte offset 0, position 2 at offset 1, etc.
    """
    if len(ref) != 1 or len(alt) != 1:
        return None
    if ref not in "ACGT" or alt not in "ACGT" or ref == alt:
        return None

    chrom_norm = chrom.removeprefix("chr") if isinstance(chrom, str) else str(chrom)
    try:
        seq = _load_chromosome_bytes(chrom_norm, chrom_dir)
    except FileNotFoundError:
        return None

    idx = pos - 1  # 1-based -> 0-based
    if idx < 1 or idx >= len(seq) - 1:
        return None

    five = decode_tsb_byte(seq[idx - 1])
    centre = decode_tsb_byte(seq[idx])
    three = decode_tsb_byte(seq[idx + 1])
    if "N" in (five, centre, three):
        return None
    if centre != ref:
        # Reference base mismatch — could be an alt-build coordinate or a left-aligned
        # indel that slipped through. Fail-quiet: skip the mutation.
        return None

    if ref in "CT":
        return f"{five}[{ref}>{alt}]{three}"
    # Reverse-complement to pyrimidine strand.
    ref_rc = ref.translate(_RC)
    alt_rc = alt.translate(_RC)
    five_rc = three.translate(_RC)
    three_rc = five.translate(_RC)
    return f"{five_rc}[{ref_rc}>{alt_rc}]{three_rc}"


def annotate_trinucleotide_context(
    mutations: pd.DataFrame, *, chrom_dir: Path
) -> pd.DataFrame:
    """Add a ``context_96`` column. SNVs that fail any check get None."""
    contexts: list[str | None] = []
    for chrom, pos, ref, alt in zip(
        mutations["chromosome"].astype(str),
        mutations["start"].astype(int),
        mutations["reference_allele"].astype(str),
        mutations["tumor_seq_allele2"].astype(str),
    ):
        contexts.append(
            lookup_trinucleotide_context(
                chrom=chrom, pos=pos, ref=ref, alt=alt, chrom_dir=chrom_dir
            )
        )
    out = mutations.copy()
    out["context_96"] = contexts
    return out


# ---------------------------------------------------------------------------
# Per-mutation SBS1 posterior
# ---------------------------------------------------------------------------


def per_mutation_sbs1_posterior(
    *,
    mutations: pd.DataFrame,
    exposures: pd.DataFrame,
    cosmic_reference: pd.DataFrame,
) -> pd.DataFrame:
    """Compute P(SBS1 | mutation, sample) for each row in ``mutations``.

    ``mutations`` must carry ``sample_name`` and ``context_96`` columns.
    ``exposures`` is a wide table: ``sample_name`` plus one column per active signature.
    ``cosmic_reference`` is the COSMIC SBS reference in long format with a ``Type``
    column (96-context labels) and one numeric column per signature.

    Output adds a ``sbs1_posterior`` column. Rows whose context is missing or whose
    sample exposures are all zero get posterior = 0.0.
    """
    sig_cols = [c for c in exposures.columns if c != "sample_name"]
    if "SBS1" not in sig_cols:
        raise ValueError("exposures table must contain SBS1 column")

    cosmic = cosmic_reference.set_index("Type")[sig_cols].astype(float)

    # Numerator and denominator per mutation.
    exposures_indexed = exposures.set_index("sample_name")[sig_cols].astype(float)

    out = mutations.copy()
    valid = out["context_96"].notna() & out["sample_name"].isin(exposures_indexed.index)
    posteriors = np.zeros(len(out), dtype=float)

    if valid.any():
        sub = out.loc[valid, ["sample_name", "context_96"]]
        # Vector-aligned numerator: E_sample,SBS1 * pi_SBS1[ctx]
        sample_exposures = exposures_indexed.reindex(sub["sample_name"].to_numpy())
        ctx_probs = cosmic.reindex(sub["context_96"].to_numpy()).fillna(0.0)
        numer = sample_exposures["SBS1"].to_numpy() * ctx_probs["SBS1"].to_numpy()
        denom = (sample_exposures.to_numpy() * ctx_probs.to_numpy()).sum(axis=1)
        with np.errstate(invalid="ignore", divide="ignore"):
            post = np.where(denom > 0, numer / denom, 0.0)
        posteriors[valid.to_numpy()] = post

    out["sbs1_posterior"] = posteriors
    return out


# ---------------------------------------------------------------------------
# RT-bin assignment
# ---------------------------------------------------------------------------


def _norm_chrom(value: str | int) -> str:
    s = str(value).removeprefix("chr")
    return s


def assign_rt_bin_label(mutations: pd.DataFrame, rt_bins: pd.DataFrame) -> pd.DataFrame:
    """Map each mutation's chr/start to a constitutive RT bin label.

    Mutations not falling in any constitutive bin get label ``"unassigned"``.
    """
    out = mutations.copy()
    out["_chrom_norm"] = out["chromosome"].apply(_norm_chrom)
    bins = rt_bins.copy()
    bins["_chrom_norm"] = bins["chromosome"].apply(_norm_chrom)

    labels: list[str] = ["unassigned"] * len(out)
    by_chrom: dict[str, pd.DataFrame] = {
        c: g.sort_values("start").reset_index(drop=True)
        for c, g in bins.groupby("_chrom_norm")
    }

    for i, (chrom, pos) in enumerate(
        zip(out["_chrom_norm"].to_numpy(), out["start"].astype(int).to_numpy())
    ):
        chrom_bins = by_chrom.get(chrom)
        if chrom_bins is None:
            continue
        # Binary search by start; check the candidate bin's end.
        starts = chrom_bins["start"].to_numpy()
        ends = chrom_bins["end"].to_numpy()
        idx = np.searchsorted(starts, pos, side="right") - 1
        if 0 <= idx < len(chrom_bins) and starts[idx] <= pos < ends[idx]:
            labels[i] = chrom_bins.iloc[idx]["rt_constitutive_label"]

    out["rt_bin_label"] = labels
    return out.drop(columns=["_chrom_norm"])


# ---------------------------------------------------------------------------
# Panel-coverage-corrected bp denominators
# ---------------------------------------------------------------------------


def compute_panel_bp_overlap(
    *,
    panel_bed: pd.DataFrame,
    rt_bins: pd.DataFrame,
) -> tuple[int, int]:
    """Return (panel_ce_bp, panel_cl_bp): bp of intersection between panel exons and RT bins."""
    panel = panel_bed.copy()
    panel["_chrom_norm"] = panel["chromosome"].apply(_norm_chrom)
    bins = rt_bins.copy()
    bins["_chrom_norm"] = bins["chromosome"].apply(_norm_chrom)

    ce_bp = 0
    cl_bp = 0
    for chrom, p_grp in panel.groupby("_chrom_norm"):
        b_grp = bins[bins["_chrom_norm"] == chrom]
        if b_grp.empty:
            continue
        b_starts = b_grp["start"].to_numpy()
        b_ends = b_grp["end"].to_numpy()
        b_labels = b_grp["rt_constitutive_label"].to_numpy()
        for ps, pe in zip(p_grp["start"].astype(int), p_grp["end"].astype(int)):
            # Find overlapping bins (bin.start < pe and bin.end > ps).
            overlap = (b_starts < pe) & (b_ends > ps)
            for s, e, lbl in zip(b_starts[overlap], b_ends[overlap], b_labels[overlap]):
                bp = max(0, min(int(e), pe) - max(int(s), ps))
                if lbl == "CE":
                    ce_bp += bp
                elif lbl == "CL":
                    cl_bp += bp
    return ce_bp, cl_bp


# ---------------------------------------------------------------------------
# Aggregate LRR fraction
# ---------------------------------------------------------------------------


def aggregate_lrr_fraction(
    posteriors: pd.DataFrame, panel_bp: pd.DataFrame
) -> pd.DataFrame:
    """Aggregate per-(study) LRR fraction from per-mutation SBS1 posteriors.

    ``posteriors`` columns: study_id, sample_name, rt_bin_label, sbs1_posterior.
    ``panel_bp`` columns: study_id, panel_ce_bp, panel_cl_bp.
    """
    agg = (
        posteriors.groupby(["study_id", "rt_bin_label"])["sbs1_posterior"]
        .sum()
        .unstack("rt_bin_label", fill_value=0.0)
    )
    for required in ("CE", "CL"):
        if required not in agg.columns:
            agg[required] = 0.0
    agg = agg.reset_index().rename(columns={"CE": "n_sbs1_ce", "CL": "n_sbs1_cl"})
    agg["n_sbs1_pooled"] = agg["n_sbs1_ce"] + agg["n_sbs1_cl"]

    merged = agg.merge(panel_bp, on="study_id", how="left")
    merged["rho_ce"] = merged["n_sbs1_ce"] / merged["panel_ce_bp"].replace({0: np.nan})
    merged["rho_cl"] = merged["n_sbs1_cl"] / merged["panel_cl_bp"].replace({0: np.nan})
    merged["f_lrr_uncorrected"] = np.where(
        merged["n_sbs1_pooled"] > 0,
        merged["n_sbs1_cl"] / merged["n_sbs1_pooled"],
        np.nan,
    )
    denom = merged["rho_ce"] + merged["rho_cl"]
    merged["f_lrr_corrected"] = np.where(denom > 0, merged["rho_cl"] / denom, np.nan)
    return merged


# ---------------------------------------------------------------------------
# Cluster bootstrap by sample
# ---------------------------------------------------------------------------


def bootstrap_lrr_ci(
    *,
    posteriors: pd.DataFrame,
    panel_bp: pd.DataFrame,
    n_bootstrap: int,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Cluster-bootstrap by sample within each study; return per-study 95% CI bounds."""
    rows = []
    for study_id, study_df in posteriors.groupby("study_id"):
        study_panel = panel_bp[panel_bp["study_id"] == study_id]
        if study_panel.empty:
            continue
        ce_bp = float(study_panel["panel_ce_bp"].iloc[0])
        cl_bp = float(study_panel["panel_cl_bp"].iloc[0])
        sample_groups: dict[str, pd.DataFrame] = {
            s: g for s, g in study_df.groupby("sample_name")
        }
        sample_ids = np.array(list(sample_groups.keys()))
        if len(sample_ids) == 0:
            continue
        f_lrr_boot = np.empty(n_bootstrap, dtype=float)
        for b in range(n_bootstrap):
            picks = rng.choice(sample_ids, size=len(sample_ids), replace=True)
            n_ce = 0.0
            n_cl = 0.0
            for s in picks:
                g = sample_groups[s]
                # Vectorised: sum posteriors stratified by rt_bin_label.
                lab = g["rt_bin_label"].to_numpy()
                p = g["sbs1_posterior"].to_numpy()
                n_ce += float(p[lab == "CE"].sum())
                n_cl += float(p[lab == "CL"].sum())
            rho_ce = n_ce / ce_bp if ce_bp > 0 else np.nan
            rho_cl = n_cl / cl_bp if cl_bp > 0 else np.nan
            denom = rho_ce + rho_cl
            f_lrr_boot[b] = rho_cl / denom if denom and denom > 0 else np.nan
        valid = f_lrr_boot[~np.isnan(f_lrr_boot)]
        if len(valid) == 0:
            ci_low = np.nan
            ci_high = np.nan
        else:
            ci_low = float(np.quantile(valid, 0.025))
            ci_high = float(np.quantile(valid, 0.975))
        rows.append(
            {
                "study_id": study_id,
                "ci_low": ci_low,
                "ci_high": ci_high,
                "n_bootstrap": n_bootstrap,
            }
        )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Pre-registered decision rule
# ---------------------------------------------------------------------------


def apply_decision_rule(
    rows: pd.DataFrame,
    *,
    matched_study: str,
    panel_study: str,
    midpoint: float,
    n_floor: float,
    max_ci_halfwidth: float,
) -> str:
    matched = rows[rows["study_id"] == matched_study].iloc[0]
    panel = rows[rows["study_id"] == panel_study].iloc[0]
    panel_halfwidth = (panel["ci_high"] - panel["ci_low"]) / 2

    if panel["n_sbs1_pooled"] < n_floor or panel_halfwidth > max_ci_halfwidth:
        return "defer"
    if panel["ci_low"] > matched["ci_high"] and panel["ci_low"] > midpoint:
        return "pass"
    return "retire"


# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------


def load_cosmic_reference(
    *, sigprofiler_root: Path, signatures: Iterable[str]
) -> pd.DataFrame:
    """Load the COSMIC SBS reference and project to the requested signature set."""
    path = (
        sigprofiler_root
        / "data"
        / "Reference_Signatures"
        / GENOME_BUILD
        / (f"COSMIC_v{COSMIC_VERSION}_SBS_{GENOME_BUILD}.txt")
    )
    df = pd.read_csv(path, sep="\t")
    keep = ["Type"] + [s for s in signatures if s in df.columns]
    missing = [s for s in signatures if s not in df.columns]
    if missing:
        raise ValueError(f"missing signatures from COSMIC v{COSMIC_VERSION}: {missing}")
    return df[keep].copy()


def load_genie_panel_bed(
    *, genomic_information: Path, panel_ids: Iterable[str]
) -> pd.DataFrame:
    """Read panel exon intervals for the requested panels from GENIE genomic_information.txt.

    Filters to ``Feature_Type == 'exon'`` and ``includeInPanel == 'True'``.
    Returns columns: chromosome, start, end, panel_id (canonical via normalize_panel_id).
    """
    df = pd.read_csv(genomic_information, sep="\t", dtype=str)
    df = df[(df["Feature_Type"] == "exon") & (df["includeInPanel"] == "True")]
    panel_canon: dict[str, str] = {}
    for raw in df["SEQ_ASSAY_ID"].unique():
        try:
            panel_canon[raw] = normalize_panel_id(raw)
        except ValueError:
            panel_canon[raw] = raw  # unknown panels: keep raw (will be filtered below)
    df = df.assign(panel_id=df["SEQ_ASSAY_ID"].map(panel_canon))
    panel_set = set(panel_ids)
    df = df[df["panel_id"].isin(panel_set)]
    out = df[["Chromosome", "Start_Position", "End_Position", "panel_id"]].rename(
        columns={
            "Chromosome": "chromosome",
            "Start_Position": "start",
            "End_Position": "end",
        }
    )
    out["start"] = out["start"].astype(int)
    out["end"] = out["end"].astype(int)
    return out.reset_index(drop=True)


def load_wes_exome_bp_per_label(*, gene_rt: pd.DataFrame) -> tuple[int, int]:
    """For WES studies (tcga_mc3): use t121 gene-level rt_*_bp totals as the denominator.

    This is the ``gene-CDS approximation`` mentioned in the pre-registration; for WES it is
    the most direct single-source proxy for whole-exome callable territory.
    """
    ce_bp = int(gene_rt["rt_ce_bp"].fillna(0).sum())
    cl_bp = int(gene_rt["rt_cl_bp"].fillna(0).sum())
    return ce_bp, cl_bp


# ---------------------------------------------------------------------------
# CLI / orchestration
# ---------------------------------------------------------------------------


def _resolve_chrom_dir() -> Path:
    """Locate SigProfilerMatrixGenerator's GRCh37 TSB chromosome directory."""
    import SigProfilerMatrixGenerator as smg  # type: ignore

    return (
        Path(smg.__file__).resolve().parent
        / "references"
        / "chromosomes"
        / "tsb"
        / "GRCh37"
    )


def _resolve_sigprofiler_assignment_root() -> Path:
    import SigProfilerAssignment as spa  # type: ignore

    return Path(spa.__file__).resolve().parent


def run_per_study(
    *,
    study_id: str,
    mut_path: Path,
    samples_path: Path,
    assignments_path: Path,
    rt_gene_path: Path,
    rt_bins_path: Path,
    cosmic_reference: pd.DataFrame,
    chrom_dir: Path,
    panel_bed: pd.DataFrame | None,
    is_wes: bool,
    lookup_key: str = "breast",
) -> tuple[pd.DataFrame, tuple[int, int], pd.DataFrame]:
    """Run the full pipeline for one study and return (per_mutation, (ce_bp,cl_bp), exposures)."""
    mut = pd.read_feather(mut_path)
    mut = mut[mut["variant_type"] == "SNP"].copy()
    mut["sample_name"] = mut["sample_id_tumor"]

    assignments = pd.read_feather(assignments_path)
    assignments = assignments[assignments["lookup_key"] == lookup_key]
    samples_with_assignment = set(assignments["sample_name"].unique())
    mut = mut[mut["sample_name"].isin(samples_with_assignment)].copy()

    # Wide exposures (one row per sample, one column per signature).
    exposures = assignments.pivot_table(
        index="sample_name", columns="signature", values="exposure", aggfunc="first"
    ).reset_index()
    exposures.columns.name = None

    sig_cols = [c for c in cosmic_reference.columns if c != "Type"]
    for c in sig_cols:
        if c not in exposures.columns:
            exposures[c] = 0.0
    exposures = exposures[["sample_name", *sig_cols]].fillna(0.0)

    # Trinucleotide context.
    mut = annotate_trinucleotide_context(mut, chrom_dir=chrom_dir)
    mut = mut[mut["context_96"].notna()].copy()

    # Per-mutation SBS1 posterior.
    mut = per_mutation_sbs1_posterior(
        mutations=mut, exposures=exposures, cosmic_reference=cosmic_reference
    )

    # RT bin assignment.
    rt_bins = pd.read_feather(rt_bins_path)
    mut = assign_rt_bin_label(mut, rt_bins)

    mut["study_id"] = study_id

    # Denominators.
    if is_wes:
        gene_rt = pd.read_feather(rt_gene_path)
        ce_bp, cl_bp = load_wes_exome_bp_per_label(gene_rt=gene_rt)
    else:
        if panel_bed is None or panel_bed.empty:
            raise ValueError(f"non-WES study {study_id} requires a panel_bed")
        ce_bp, cl_bp = compute_panel_bp_overlap(panel_bed=panel_bed, rt_bins=rt_bins)

    return mut, (ce_bp, cl_bp), exposures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--results-root",
        type=Path,
        required=True,
        help="Path to a results/<run-name>/ directory containing studies/.",
    )
    parser.add_argument("--matched-study", type=str, default="tcga_mc3")
    parser.add_argument("--panel-study", type=str, default="msk_impact_2017")
    parser.add_argument("--lookup-key", type=str, default="breast")
    parser.add_argument(
        "--rt-gene", type=Path, default=Path("data/gene_replication_timing.feather")
    )
    parser.add_argument(
        "--rt-bins",
        type=Path,
        default=Path("data/replication_timing_constitutive_bins.feather"),
    )
    parser.add_argument(
        "--genie-genomic-info",
        type=Path,
        default=Path("data/genie/genomic_information.txt"),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--n-bootstrap", type=int, default=1000)
    parser.add_argument("--random-seed", type=int, default=0)
    # Pre-registered thresholds.
    parser.add_argument("--midpoint", type=float, default=0.45)
    parser.add_argument("--n-floor", type=float, default=500)
    parser.add_argument("--max-ci-halfwidth", type=float, default=0.10)
    args = parser.parse_args(argv)

    chrom_dir = _resolve_chrom_dir()
    cosmic = load_cosmic_reference(
        sigprofiler_root=_resolve_sigprofiler_assignment_root(),
        signatures=(
            "SBS1",
            "SBS2",
            "SBS3",
            "SBS5",
            "SBS8",
            "SBS13",
            "SBS18",
            "SBS40a",
            "SBS40b",
            "SBS40c",
        ),
    )

    studies_root = args.results_root / "studies"

    # Discover panel BED for the panel study.
    panel_samples = pd.read_feather(
        studies_root / args.panel_study / "metadata/samples.feather"
    )
    if "panel_id" not in panel_samples.columns:
        raise ValueError(f"{args.panel_study}/samples.feather has no panel_id column")
    panel_ids = sorted(panel_samples["panel_id"].dropna().unique().tolist())
    panel_bed = load_genie_panel_bed(
        genomic_information=args.genie_genomic_info, panel_ids=panel_ids
    )
    if panel_bed.empty:
        raise ValueError(
            f"no panel BED rows resolved for panel_ids={panel_ids}; check normalisation"
        )

    per_mut_frames = []
    panel_bp_rows: list[dict[str, object]] = []

    for study, is_wes in [(args.matched_study, True), (args.panel_study, False)]:
        study_dir = studies_root / study
        per_mut, (ce_bp, cl_bp), _exposures = run_per_study(
            study_id=study,
            mut_path=study_dir / "mut/table/mut.feather",
            samples_path=study_dir / "metadata/samples.feather",
            assignments_path=study_dir
            / "mut/signatures/restricted_assignment_per_sample.feather",
            rt_gene_path=args.rt_gene,
            rt_bins_path=args.rt_bins,
            cosmic_reference=cosmic,
            chrom_dir=chrom_dir,
            panel_bed=panel_bed if not is_wes else None,
            is_wes=is_wes,
            lookup_key=args.lookup_key,
        )
        per_mut_frames.append(per_mut)
        panel_bp_rows.append(
            {"study_id": study, "panel_ce_bp": ce_bp, "panel_cl_bp": cl_bp}
        )
        print(
            f"[{study}] mutations: {len(per_mut)}; "
            f"sum_SBS1_posterior: {per_mut['sbs1_posterior'].sum():.1f}; "
            f"panel_ce_bp: {ce_bp:,}; panel_cl_bp: {cl_bp:,}",
            file=sys.stderr,
        )

    posteriors = pd.concat(per_mut_frames, ignore_index=True)
    panel_bp = pd.DataFrame(panel_bp_rows)
    agg = aggregate_lrr_fraction(posteriors, panel_bp)

    rng = np.random.default_rng(args.random_seed)
    ci = bootstrap_lrr_ci(
        posteriors=posteriors[posteriors["rt_bin_label"].isin(["CE", "CL"])],
        panel_bp=panel_bp,
        n_bootstrap=args.n_bootstrap,
        rng=rng,
    )
    out = agg.merge(ci, on="study_id", how="left")
    out["lookup_key"] = args.lookup_key

    verdict = apply_decision_rule(
        out,
        matched_study=args.matched_study,
        panel_study=args.panel_study,
        midpoint=args.midpoint,
        n_floor=args.n_floor,
        max_ci_halfwidth=args.max_ci_halfwidth,
    )
    out["verdict"] = verdict

    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_feather(args.output)
    print(f"Wrote {args.output}", file=sys.stderr)
    print(out.to_string(), file=sys.stderr)
    print(f"VERDICT: {verdict}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
