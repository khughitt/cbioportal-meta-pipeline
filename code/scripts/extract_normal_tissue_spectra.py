# science:code
# status: workflow-owned
# science:end
"""
extract_normal_tissue_spectra.py

Builds two reference tables from Li 2021 per-variant supplementary data:

- `data/normal_tissue_spectra.tsv` — 96-trinucleotide SBS spectra per normal tissue
  (three aggregations: pooled_counts, donor_averaged_fraction, per_donor)
- `data/normal_tissue_burden.tsv` — per-tissue / per-donor mutation burden with
  callable-Mb denominator and sequencing-modality metadata

Rows are keyed on UBERON ontology IDs; source tissue labels are preserved for audit.

Design: doc/plans/2026-04-18-t111-normal-tissue-spectra-design.md
Plan:   doc/plans/2026-04-18-t111-normal-tissue-spectra-plan.md
"""

import sys
from pathlib import Path  # noqa: F401

import pandas as pd  # noqa: F401

# Assay metadata constants. Sourced from Li 2021 (Nature 597:398-403, DOI
# 10.1038/s41586-021-03836-1, Methods): SureSelectXT Human All Exon V6
# (esophagus biopsies only, all donors) or V7 (all other tissues, all donors).
#
# Agilent SureSelectXT Human All Exon target sizes from product data sheets:
#   V6 ≈ 60 Mb (~58.4 Mb covered)
#   V7 ≈ 48.2 Mb (~48.2 Mb covered)
# Downstream burden calculations divide by these values — treat as
# correctness-critical constants.
#
# Keyed by (source, tissue_label) with (source, None) as the per-source fallback.
# Xu 2025 deferred to t112 per scope amendment.
ASSAY_METADATA: dict[tuple[str, str | None], dict[str, object]] = {
    ("li2021", "Esophagus"): {
        "sequencing_modality": "WES",
        "capture_kit_or_panel": "SureSelectXT V6",
        "callable_mb": 60.0,
    },
    ("li2021", None): {
        "sequencing_modality": "WES",
        "capture_kit_or_panel": "SureSelectXT V7",
        "callable_mb": 48.2,
    },
}


# SigProfiler's canonical 96-trinucleotide context ordering (verified against
# SigProfilerMatrixGenerator/scripts/Benchmark/GRCh37_bench_orig_96.txt):
# {5'-base}[{ref}>{alt}]{3'-base}, with {ref, alt} restricted to pyrimidine-centric
# changes (C>A, C>G, C>T, T>A, T>C, T>G).
#
# Loop nesting is LOAD-BEARING: outer=5'-base, middle=substitution, inner=3'-base.
# The first 24 entries are all A[*]*; entries 25-48 are C[*]*; etc. This matches
# the row order of SigProfiler's SBS96 matrix output — reordering here would
# silently misalign columns when Task 10's wrapper transposes that matrix.
_SUBS: tuple[str, ...] = ("C>A", "C>G", "C>T", "T>A", "T>C", "T>G")
_BASES: tuple[str, ...] = ("A", "C", "G", "T")
CONTEXT_96: list[str] = [
    f"{five}[{sub}]{three}" for five in _BASES for sub in _SUBS for three in _BASES
]
assert len(CONTEXT_96) == 96
assert CONTEXT_96[0] == "A[C>A]A"
assert CONTEXT_96[4] == "A[C>G]A"  # substitution changes within same 5' base
assert CONTEXT_96[-1] == "T[T>G]T"


# Tuples (not sets) so pandas .isin() accepts them cleanly; _VALID_CHROMS_SET is for
# set-difference operations. Pandas accepts sets at runtime but its type stubs do not.
_VALID_CHROMS: tuple[str, ...] = tuple(
    f"chr{c}" for c in list(range(1, 23)) + ["X", "Y"]
)
_VALID_CHROMS_SET: frozenset[str] = frozenset(_VALID_CHROMS)
_MITO_CHROMS: tuple[str, ...] = ("chrM", "chrMT")
_VALID_BASES: tuple[str, ...] = ("A", "C", "G", "T")


def validate_input_contract(
    df: pd.DataFrame, source: str, assembly: str
) -> tuple[pd.DataFrame, dict[str, int]]:
    """Enforce the input contract defined in the design spec.

    Drops (with counters): indels, mitochondrial rows, exact within-donor duplicates.
    Raises ValueError for: multi-allelic rows, non-ACGT alleles, unknown chromosomes.
    Normalises `chrom` to the `chrN` form.

    Returns (cleaned_df, stats_dict) where stats_dict has keys:
    n_indels_dropped, n_mito_dropped, n_duplicates_collapsed.
    """
    required = {"donor_id", "tissue_label", "chrom", "pos", "ref", "alt"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{source}: missing required columns {sorted(missing)}")

    df = df.copy()
    # TODO(t111-followup): assert chrom/pos ranges match the declared assembly.
    # Design spec §Input contract requires this check but defers encoding of
    # per-chromosome lengths for GRCh37/GRCh38. For now, `assembly` is accepted
    # and preserved on the stats object for audit, but no range check is applied.
    _ = assembly  # noqa: ARG001 — preserved for stats + future assembly range-check
    df["chrom"] = (
        df["chrom"].astype(str).apply(lambda c: c if c.startswith("chr") else f"chr{c}")
    )
    df["ref"] = df["ref"].astype(str)
    df["alt"] = df["alt"].astype(str)

    if df["alt"].str.contains(",").any():
        bad = int(df["alt"].str.contains(",").sum())
        raise ValueError(
            f"{source}: {bad} multi-allelic rows (alt contains ','); split upstream"
        )

    # Mitochondrial drop
    mito_mask = df["chrom"].isin(_MITO_CHROMS)
    n_mito = int(mito_mask.sum())
    df = df.loc[~mito_mask].copy()

    # Unknown chromosomes
    unknown = set(df["chrom"].unique()) - _VALID_CHROMS_SET
    if unknown:
        raise ValueError(f"{source}: unknown chromosome values {sorted(unknown)}")

    # Indel drop (ref or alt not length-1, OR equals '-' which encodes indels
    # in some callers — e.g. Li 2021 uses '-' as the absent allele for
    # insertions/deletions).
    indel_mask = (
        (df["ref"].str.len() != 1)
        | (df["alt"].str.len() != 1)
        | (df["ref"] == "-")
        | (df["alt"] == "-")
    )
    n_indels = int(indel_mask.sum())
    df = df.loc[~indel_mask].copy()

    # Non-ACGT rejection
    bad_alleles = ~(df["ref"].isin(_VALID_BASES) & df["alt"].isin(_VALID_BASES))
    if bad_alleles.any():
        raise ValueError(
            f"{source}: {int(bad_alleles.sum())} rows with non-ACGT alleles"
        )

    # Exact-duplicate dedup (within donor + tissue)
    before = len(df)
    df = df.drop_duplicates(
        subset=["donor_id", "tissue_label", "chrom", "pos", "ref", "alt"]
    )
    n_dupes = before - len(df)

    return df.reset_index(drop=True), {
        "n_indels_dropped": n_indels,
        "n_mito_dropped": n_mito,
        "n_duplicates_collapsed": n_dupes,
    }


def attach_uberon(df: pd.DataFrame, mapping_tsv: Path, source: str) -> pd.DataFrame:
    """Left-join `tissue_uberon` and `uberon_label` onto df keyed on (source, tissue_label).

    Raises ValueError listing any unmapped (source, tissue_label) pairs — no silent drops.
    """
    mapping = pd.read_csv(mapping_tsv, sep="\t", dtype=str, na_filter=False)
    mapping = mapping.loc[
        mapping["source"] == source, ["tissue_label", "tissue_uberon", "uberon_label"]
    ]

    out = df.merge(mapping, on="tissue_label", how="left", validate="many_to_one")
    unmapped = out.loc[out["tissue_uberon"].isna(), "tissue_label"].unique().tolist()
    if unmapped:
        raise ValueError(
            f"{source}: unmapped tissue_label values {sorted(unmapped)}. "
            f"Append to {mapping_tsv}."
        )
    return out


def attach_assay_metadata(df: pd.DataFrame, source: str) -> pd.DataFrame:
    """Attach sequencing_modality / capture_kit_or_panel / callable_mb columns
    keyed by (source, tissue_label), with (source, None) as the per-source fallback.

    Raises KeyError if source is unknown to ASSAY_METADATA.
    """
    source_keys = [k for k in ASSAY_METADATA if k[0] == source]
    if not source_keys:
        raise KeyError(f"ASSAY_METADATA has no entry for source={source!r}")

    has_fallback = (source, None) in ASSAY_METADATA
    tissue_specific_keys = {k[1] for k in source_keys if k[1] is not None}

    # If source has no fallback, every tissue_label in df must be explicitly keyed.
    if not has_fallback:
        missing = set(df["tissue_label"].unique()) - tissue_specific_keys
        if missing:
            raise KeyError(
                f"ASSAY_METADATA: source={source!r} has no (None) fallback and no "
                f"entry for tissues {sorted(missing)}"
            )

    def _lookup(tissue_label: str) -> dict[str, object]:
        if (source, tissue_label) in ASSAY_METADATA:
            return ASSAY_METADATA[(source, tissue_label)]
        return ASSAY_METADATA[(source, None)]

    meta = df["tissue_label"].apply(_lookup).tolist()
    out = df.copy()
    out["sequencing_modality"] = [m["sequencing_modality"] for m in meta]
    out["capture_kit_or_panel"] = [m["capture_kit_or_panel"] for m in meta]
    out["callable_mb"] = [float(m["callable_mb"]) for m in meta]
    return out


def aggregate_pooled_counts(per_donor_ctx: pd.DataFrame) -> dict[str, int]:
    """Column-wise sum of per-donor 96-context counts → single pooled row.

    Input: per-donor DataFrame with 96 context columns + 'donor_id'.
    Output: dict with 96 context columns (int), 'total_snvs' (int), 'n_donors' (int).
    """
    context_counts: dict[str, int] = {
        ctx: int(per_donor_ctx[ctx].sum()) for ctx in CONTEXT_96
    }
    total_snvs: int = sum(context_counts.values())
    n_donors: int = int(per_donor_ctx["donor_id"].nunique())
    return {**context_counts, "total_snvs": total_snvs, "n_donors": n_donors}


def aggregate_donor_averaged_fraction(
    per_donor_ctx: pd.DataFrame, threshold: int = 50
) -> tuple[dict[str, float], dict[str, int]]:
    """Normalise each donor's 96-vector to a fraction, then average across donors.

    Donors with fewer than `threshold` SNVs are excluded from the average.

    Returns (row_dict, audit_dict). audit_dict has n_donors_total,
    n_donors_included, n_donors_excluded_low_snvs, low_snv_threshold.
    """
    n_total = int(per_donor_ctx["donor_id"].nunique())
    totals = per_donor_ctx[list(CONTEXT_96)].sum(axis=1)
    include_mask = totals >= threshold
    n_incl = int(include_mask.sum())
    n_excl = n_total - n_incl

    audit: dict[str, int] = {
        "n_donors_total": n_total,
        "n_donors_included": n_incl,
        "n_donors_excluded_low_snvs": n_excl,
        "low_snv_threshold": threshold,
    }

    if n_incl == 0:
        return {ctx: 0.0 for ctx in CONTEXT_96}, audit

    included = per_donor_ctx.loc[include_mask, list(CONTEXT_96)]
    totals_incl = included.sum(axis=1).to_numpy()
    fractions = included.to_numpy() / totals_incl[:, None]
    averaged = fractions.mean(axis=0)

    # Re-normalize to guard against floating-point drift
    averaged = averaged / averaged.sum()

    return {ctx: float(averaged[i]) for i, ctx in enumerate(CONTEXT_96)}, audit


def aggregate_per_donor_rows(per_donor_ctx: pd.DataFrame) -> list[dict[str, object]]:
    """Emit one row per donor, carrying the donor's 96-context counts + total_snvs."""
    rows: list[dict[str, object]] = []
    for _, donor_row in per_donor_ctx.iterrows():
        row: dict[str, object] = {ctx: int(donor_row[ctx]) for ctx in CONTEXT_96}
        row["donor_id"] = str(donor_row["donor_id"])
        total: int = sum(int(donor_row[ctx]) for ctx in CONTEXT_96)
        row["total_snvs"] = total
        rows.append(row)
    return rows


def aggregate_pooled_burden(variants_df: pd.DataFrame) -> dict[str, object]:
    """Pooled per-tissue burden. Expects per-variant rows with donor_id, sample_id,
    callable_mb (constant per tissue, enforced).

    snvs_per_mb = snvs / callable_mb / n_samples (per-sample rate).
    """
    callable_values = variants_df["callable_mb"].unique()
    if len(callable_values) != 1:
        raise ValueError(
            f"aggregate_pooled_burden: mixed callable_mb values {sorted(callable_values)}"
        )
    callable_mb = float(callable_values[0])
    snvs: int = int(len(variants_df))
    n_donors: int = int(variants_df["donor_id"].nunique())
    n_samples: int = int(variants_df["sample_id"].nunique())
    if n_samples == 0:
        raise ValueError(
            "aggregate_pooled_burden: n_samples is 0 (empty or all-NaN sample_id)"
        )
    snvs_per_mb: float = snvs / callable_mb / n_samples
    return {
        "snvs": snvs,
        "n_donors": n_donors,
        "n_samples": n_samples,
        "callable_mb": callable_mb,
        "snvs_per_mb": float(snvs_per_mb),
    }


def aggregate_per_donor_burden_rows(
    variants_df: pd.DataFrame,
) -> list[dict[str, object]]:
    """Per-donor burden rows. Assumes callable_mb constant per donor."""
    rows: list[dict[str, object]] = []
    for donor_id, grp in variants_df.groupby("donor_id"):
        callable_values = grp["callable_mb"].unique()
        if len(callable_values) != 1:
            raise ValueError(
                f"aggregate_per_donor_burden_rows: donor {donor_id} has mixed callable_mb"
            )
        callable_mb = float(callable_values[0])
        n_samples: int = int(grp["sample_id"].nunique())
        snvs: int = int(len(grp))
        if n_samples == 0:
            raise ValueError(
                f"aggregate_per_donor_burden_rows: donor {donor_id} has n_samples=0"
            )
        rows.append(
            {
                "donor_id": str(donor_id),
                "snvs": snvs,
                "n_samples": n_samples,
                "callable_mb": callable_mb,
                "snvs_per_mb": float(snvs / callable_mb / n_samples),
            }
        )
    return rows


def _sigprofiler_matrix(variants_df: pd.DataFrame, assembly: str) -> pd.DataFrame:
    """Run SigProfilerMatrixGenerator on an in-memory per-variant table.

    Writes a temporary VCF-like MAF, invokes the matrix generator, reads the resulting
    SBS96 matrix, returns it as a DataFrame with 96 rows (contexts) × N columns (donors).

    This is the single SigProfiler touch-point. Mocked out by tests except in the slow
    integration test (Task 14).

    First call for a given assembly may fail with FileNotFoundError if the reference
    bundle is not yet installed; we catch, install idempotently, and retry once.
    """
    import tempfile

    from SigProfilerMatrixGenerator import install as sigprofiler_install
    from SigProfilerMatrixGenerator.scripts import (
        SigProfilerMatrixGeneratorFunc as matGen,
    )

    def _run(vcf_dir: Path) -> pd.DataFrame:
        matrices = matGen.SigProfilerMatrixGeneratorFunc(
            "normal_tissue",
            assembly,
            str(vcf_dir),
            exome=False,
            bed_file=None,
            chrom_based=False,
            plot=False,
            tsb_stat=False,
            seqInfo=False,
        )
        return matrices["96"]

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        vcf_dir = tmp_path / "vcfs"
        vcf_dir.mkdir()
        for donor_id, grp in variants_df.groupby("donor_id"):
            vcf_path = vcf_dir / f"{donor_id}.vcf"
            with vcf_path.open("w") as fh:
                fh.write("##fileformat=VCFv4.2\n")
                fh.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
                for _, r in grp.iterrows():
                    fh.write(
                        f"{r['chrom']}\t{r['pos']}\t.\t{r['ref']}\t{r['alt']}\t.\tPASS\t.\n"
                    )

        try:
            sbs96 = _run(vcf_dir)
        except (FileNotFoundError, Exception) as exc:  # noqa: BLE001
            # SigProfilerMatrixGenerator raises a bare Exception (not
            # FileNotFoundError) with the message "The specified genome
            # {assembly} has not been installed" when the reference bundle is
            # absent. Catch both to handle both older and newer versions.
            exc_str = str(exc)
            if "has not been installed" not in exc_str and not isinstance(
                exc, FileNotFoundError
            ):
                raise
            print(
                f"SigProfiler reference bundle for {assembly} not found ({exc}); "
                f"installing and retrying once.",
                file=sys.stderr,
            )
            sigprofiler_install.install(assembly, bash=True)
            sbs96 = _run(vcf_dir)
    return sbs96


def compute_96_context_counts(variants_df: pd.DataFrame, assembly: str) -> pd.DataFrame:
    """Wrapper returning per-donor 96-context counts as a DataFrame with
    columns: [CONTEXT_96..., donor_id, total_snvs].

    Input: validated, SNV-only per-variant rows with `donor_id, chrom, pos, ref, alt`.
    """
    sbs96 = _sigprofiler_matrix(variants_df, assembly=assembly)
    wide = sbs96.T
    wide = wide.reindex(columns=CONTEXT_96, fill_value=0)
    wide = wide.reset_index().rename(columns={"index": "donor_id"})
    wide["total_snvs"] = wide[CONTEXT_96].sum(axis=1).astype(int)
    return wide


def build_spectra_rows_for_tissue(  # noqa: PLR0913
    *,
    per_donor_ctx: pd.DataFrame,
    source_id: str,
    tissue_uberon: str,
    tissue_label: str,
    uberon_label: str,
    assembly: str,
    sequencing_modality: str,
    capture_kit_or_panel: str,
    callable_mb: float,
    n_samples: int,
    low_snv_threshold: int = 50,
) -> list[dict[str, object]]:
    """Produce all spectra rows (pooled + averaged + per-donor) for one tissue."""
    n_donors_total = int(per_donor_ctx["donor_id"].nunique())

    def _common(
        aggregation: str, value_type: str, **audit: object
    ) -> dict[str, object]:
        return {
            "source_id": source_id,
            "tissue_uberon": tissue_uberon,
            "tissue_label": tissue_label,
            "uberon_label": uberon_label,
            "aggregation": aggregation,
            "value_type": value_type,
            "assembly": assembly,
            "sequencing_modality": sequencing_modality,
            "capture_kit_or_panel": capture_kit_or_panel,
            "callable_mb": callable_mb,
            "n_donors_total": n_donors_total,
            "n_samples": n_samples,
            "low_snv_threshold": low_snv_threshold,
            "donor_id": "",
            **audit,
        }

    rows: list[dict[str, object]] = []

    pooled = aggregate_pooled_counts(per_donor_ctx)
    rows.append(
        {
            **_common(
                "pooled_counts",
                "counts",
                n_donors_included=n_donors_total,
                n_donors_excluded_low_snvs=0,
            ),
            **{ctx: pooled[ctx] for ctx in CONTEXT_96},
            "total_snvs": pooled["total_snvs"],
            "n_donors": n_donors_total,
        }
    )

    averaged, audit = aggregate_donor_averaged_fraction(
        per_donor_ctx, threshold=low_snv_threshold
    )
    rows.append(
        {
            **_common(
                "donor_averaged_fraction",
                "fractions",
                n_donors_included=audit["n_donors_included"],
                n_donors_excluded_low_snvs=audit["n_donors_excluded_low_snvs"],
            ),
            **averaged,
            "total_snvs": 0,  # fractions — not a meaningful count
            "n_donors": audit["n_donors_included"],
        }
    )

    for donor_row in aggregate_per_donor_rows(per_donor_ctx):
        rows.append(
            {
                **_common(
                    "per_donor",
                    "counts",
                    n_donors_included=1,
                    n_donors_excluded_low_snvs=0,
                ),
                **{ctx: donor_row[ctx] for ctx in CONTEXT_96},
                "total_snvs": donor_row["total_snvs"],
                "donor_id": donor_row["donor_id"],
                "n_donors": 1,
            }
        )

    return rows


SPECTRA_COLUMNS: list[str] = [
    "source_id",
    "tissue_uberon",
    "tissue_label",
    "uberon_label",
    "aggregation",
    "value_type",
    "donor_id",
    "assembly",
    "sequencing_modality",
    "capture_kit_or_panel",
    "callable_mb",
    "n_donors_total",
    "n_donors_included",
    "n_donors_excluded_low_snvs",
    "low_snv_threshold",
    "n_donors",
    "n_samples",
    "total_snvs",
    *CONTEXT_96,
]

BURDEN_COLUMNS: list[str] = [
    "source_id",
    "tissue_uberon",
    "tissue_label",
    "uberon_label",
    "aggregation",
    "donor_id",
    "assembly",
    "sequencing_modality",
    "capture_kit_or_panel",
    "callable_mb",
    "n_donors",
    "n_samples",
    "snvs",
    "snvs_per_mb",
]


def build_burden_rows_for_tissue(  # noqa: PLR0913
    *,
    variants_df: pd.DataFrame,
    source_id: str,
    tissue_uberon: str,
    tissue_label: str,
    uberon_label: str,
    assembly: str,
    sequencing_modality: str,
    capture_kit_or_panel: str,
) -> list[dict[str, object]]:
    """Produce pooled + per-donor burden rows for one tissue."""

    def _common(aggregation: str) -> dict[str, object]:
        return {
            "source_id": source_id,
            "tissue_uberon": tissue_uberon,
            "tissue_label": tissue_label,
            "uberon_label": uberon_label,
            "aggregation": aggregation,
            "assembly": assembly,
            "sequencing_modality": sequencing_modality,
            "capture_kit_or_panel": capture_kit_or_panel,
            "donor_id": "",
        }

    rows: list[dict[str, object]] = []

    pooled = aggregate_pooled_burden(variants_df)
    rows.append({**_common("pooled"), **pooled})

    for per_donor in aggregate_per_donor_burden_rows(variants_df):
        rows.append({**_common("per_donor"), **per_donor, "n_donors": 1})

    return rows


def write_spectra_tsv(rows: list[dict[str, object]], path: Path) -> None:
    df = pd.DataFrame(rows)
    for col in SPECTRA_COLUMNS:
        if col not in df.columns:
            df[col] = 0
    df = df[SPECTRA_COLUMNS]
    df.to_csv(path, sep="\t", index=False)


def write_burden_tsv(rows: list[dict[str, object]], path: Path) -> None:
    df = pd.DataFrame(rows)
    for col in BURDEN_COLUMNS:
        if col not in df.columns:
            df[col] = 0
    df = df[BURDEN_COLUMNS]
    df.to_csv(path, sep="\t", index=False)


_SOURCE_ASSEMBLY: dict[str, str] = {"li2021": "GRCh37"}


def extract_for_source(  # noqa: PLR0913
    *,
    source: str,
    variants_tsv: Path,
    mapping_tsv: Path,
    assembly: str | None = None,
    low_snv_threshold: int = 50,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Run the full extraction for a single source. Returns (spectra_rows, burden_rows)."""
    if assembly is None:
        assembly = _SOURCE_ASSEMBLY[source]

    raw = pd.read_csv(variants_tsv, sep="\t", dtype=str, na_filter=False)
    raw["pos"] = raw["pos"].astype(int)

    cleaned, contract_stats = validate_input_contract(
        raw, source=source, assembly=assembly
    )
    print(
        f"{source}: {contract_stats['n_indels_dropped']} indel rows dropped, "
        f"{contract_stats['n_mito_dropped']} mitochondrial rows dropped, "
        f"{contract_stats['n_duplicates_collapsed']} within-donor duplicates collapsed",
        file=sys.stderr,
    )

    cleaned = attach_uberon(cleaned, mapping_tsv=mapping_tsv, source=source)
    cleaned = attach_assay_metadata(cleaned, source=source)

    spectra_rows: list[dict[str, object]] = []
    burden_rows: list[dict[str, object]] = []

    group_cols = [
        "tissue_label",
        "tissue_uberon",
        "uberon_label",
        "sequencing_modality",
        "capture_kit_or_panel",
        "callable_mb",
    ]
    for group_key, tissue_df in cleaned.groupby(group_cols):
        # pandas types groupby's key as Hashable, but with a list of group_cols the
        # runtime always emits a tuple; assert-narrow for the type checker.
        assert isinstance(group_key, tuple)
        tissue_label, tissue_uberon, uberon_label, modality, kit, callable_mb = (
            group_key
        )
        # One SigProfiler invocation per tissue — emits per-donor 96-context rows.
        per_donor_ctx = compute_96_context_counts(tissue_df, assembly=assembly)

        # sample_id is optional; fall back to donor_id when absent (assume one sample per donor).
        sample_col = (
            tissue_df["sample_id"]
            if "sample_id" in tissue_df.columns
            else tissue_df["donor_id"]
        )
        n_samples = int(sample_col.nunique())

        spectra_rows.extend(
            build_spectra_rows_for_tissue(
                per_donor_ctx=per_donor_ctx,
                source_id=source,
                tissue_uberon=tissue_uberon,
                tissue_label=tissue_label,
                uberon_label=uberon_label,
                assembly=assembly,
                sequencing_modality=modality,
                capture_kit_or_panel=kit,
                callable_mb=float(callable_mb),
                n_samples=n_samples,
                low_snv_threshold=low_snv_threshold,
            )
        )

        # When sample_id was absent, sample_col was derived from donor_id; assign
        # materialises it as a real column. When sample_id was present this is a no-op.
        # Index alignment is safe because validate_input_contract calls reset_index.
        burden_df = tissue_df.assign(sample_id=sample_col)
        burden_rows.extend(
            build_burden_rows_for_tissue(
                variants_df=burden_df,
                source_id=source,
                tissue_uberon=tissue_uberon,
                tissue_label=tissue_label,
                uberon_label=uberon_label,
                assembly=assembly,
                sequencing_modality=modality,
                capture_kit_or_panel=kit,
            )
        )

    return spectra_rows, burden_rows


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    li2021_tsv = Path(snek.input.li2021)
    mapping_tsv = Path(snek.input.mapping)

    spectra_out = Path(snek.output.spectra)
    burden_out = Path(snek.output.burden)

    # Li 2021 only; Xu 2025 and Lee-Six 2018 will be added in t112.
    spectra_rows, burden_rows = extract_for_source(
        source="li2021",
        variants_tsv=li2021_tsv,
        mapping_tsv=mapping_tsv,
    )

    write_spectra_tsv(spectra_rows, spectra_out)
    write_burden_tsv(burden_rows, burden_out)

    print(
        f"Wrote {len(spectra_rows)} spectra rows to {spectra_out}; "
        f"{len(burden_rows)} burden rows to {burden_out}",
        file=sys.stderr,
    )


if "snakemake" in globals():
    _run_via_snakemake()
