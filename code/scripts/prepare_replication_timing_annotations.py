# science:code
# status: workflow-owned
# science:end
"""
prepare_replication_timing_annotations.py

Stage public constitutive replication-timing bins (Dileep 2015; hg19 / GRCh37)
and derive a conservative gene-level early/late annotation by intersecting the
50 kb bins with `data/grch37.tsv`.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

RT_SOURCE = "dileep2015"

RT_BINS_COLUMNS = [
    "chromosome",
    "start",
    "end",
    "rt_constitutive_label",
    "source",
]

GENE_RT_COLUMNS = [
    "ensgene",
    "entrez",
    "symbol",
    "chr",
    "start",
    "end",
    "strand",
    "biotype",
    "description",
    "rt_constitutive_label",
    "rt_constitutive_bp",
    "rt_ce_bp",
    "rt_cl_bp",
    "rt_ce_fraction",
    "rt_cl_fraction",
    "rt_assignment_method",
    "rt_source",
]


def read_rt_bins(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".xlsx":
        return pd.read_excel(path)
    if suffix in {".tsv", ".txt"}:
        return pd.read_csv(path, sep="\t")
    if suffix == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported replication-timing input format: {path}")


def clean_constitutive_rt_bins(raw: pd.DataFrame) -> pd.DataFrame:
    colmap = {col: str(col).strip().lower() for col in raw.columns}
    df = raw.rename(columns=colmap)
    required = {"chr", "start", "end", "rtlabel"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Replication-timing input missing required columns: {sorted(missing)}")

    out = pd.DataFrame(
        {
            "chromosome": df["chr"].astype(str).str.strip(),
            "start": pd.to_numeric(df["start"], errors="raise").astype(int),
            "end": pd.to_numeric(df["end"], errors="raise").astype(int),
            "rt_constitutive_label": df["rtlabel"].astype(str).str.strip().str.upper(),
        }
    )
    out = out.loc[out["rt_constitutive_label"].isin(["CE", "CL"])].copy()
    out["source"] = RT_SOURCE

    if (out["end"] <= out["start"]).any():
        raise ValueError("Replication-timing bins must satisfy end > start")

    return out.sort_values(["chromosome", "start", "end"]).reset_index(drop=True)[RT_BINS_COLUMNS]


def normalize_gene_chromosome(chromosome: str) -> str:
    text = chromosome.strip()
    if not text:
        return text
    upper = text.upper()
    if upper.startswith("CHR"):
        suffix = upper[3:]
    else:
        suffix = upper
    return f"chr{suffix}"


def _nan() -> float:
    return float("nan")


def _overlap_bp(start_a: int, end_a: int, start_b: int, end_b: int) -> int:
    return max(0, min(end_a, end_b) - max(start_a, start_b))


def annotate_genes_with_constitutive_rt(genes: pd.DataFrame, bins: pd.DataFrame) -> pd.DataFrame:
    required_gene_cols = {"ensgene", "entrez", "symbol", "chr", "start", "end", "strand", "biotype", "description"}
    missing_gene_cols = required_gene_cols - set(genes.columns)
    if missing_gene_cols:
        raise ValueError(f"Gene coordinate input missing required columns: {sorted(missing_gene_cols)}")

    bins_by_chrom: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
    for chromosome, chrom_df in bins.groupby("chromosome", sort=False):
        starts = chrom_df["start"].to_numpy(dtype=np.int64)
        ends = chrom_df["end"].to_numpy(dtype=np.int64)
        labels = chrom_df["rt_constitutive_label"].to_numpy(dtype=object)
        bins_by_chrom[str(chromosome)] = (starts, ends, labels)

    rows: list[dict[str, object]] = []
    for gene in genes.itertuples(index=False):
        gene_dict = {
            "ensgene": gene.ensgene,
            "entrez": gene.entrez,
            "symbol": gene.symbol,
            "chr": gene.chr,
            "start": int(gene.start),
            "end": int(gene.end),
            "strand": gene.strand,
            "biotype": gene.biotype,
            "description": gene.description,
        }

        chromosome = normalize_gene_chromosome(str(gene.chr))
        ce_bp = 0
        cl_bp = 0

        if chromosome in bins_by_chrom:
            starts, ends, labels = bins_by_chrom[chromosome]
            idx = int(np.searchsorted(ends, gene_dict["start"], side="right"))
            while idx < len(starts) and int(starts[idx]) < gene_dict["end"]:
                overlap = _overlap_bp(gene_dict["start"], gene_dict["end"], int(starts[idx]), int(ends[idx]))
                if overlap > 0:
                    if labels[idx] == "CE":
                        ce_bp += overlap
                    elif labels[idx] == "CL":
                        cl_bp += overlap
                idx += 1

        total_constitutive_bp = ce_bp + cl_bp
        if total_constitutive_bp == 0:
            label = "unassigned"
            method = "no_constitutive_overlap"
            ce_fraction = _nan()
            cl_fraction = _nan()
        else:
            ce_fraction = ce_bp / total_constitutive_bp
            cl_fraction = cl_bp / total_constitutive_bp
            method = "majority_constitutive_bp"
            if ce_bp > cl_bp:
                label = "CE"
            elif cl_bp > ce_bp:
                label = "CL"
            else:
                label = "mixed"

        rows.append(
            {
                **gene_dict,
                "rt_constitutive_label": label,
                "rt_constitutive_bp": total_constitutive_bp,
                "rt_ce_bp": ce_bp,
                "rt_cl_bp": cl_bp,
                "rt_ce_fraction": ce_fraction,
                "rt_cl_fraction": cl_fraction,
                "rt_assignment_method": method,
                "rt_source": RT_SOURCE,
            }
        )

    return pd.DataFrame(rows, columns=GENE_RT_COLUMNS)


def main() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    rt_input_path = Path(snek.input.rt_bins)
    gene_input_path = Path(snek.input.genes)
    bins_output_path = Path(snek.output.bins)
    genes_output_path = Path(snek.output.genes)

    raw_bins = read_rt_bins(rt_input_path)
    clean_bins = clean_constitutive_rt_bins(raw_bins)
    genes = pd.read_csv(gene_input_path, sep="\t")
    gene_annotations = annotate_genes_with_constitutive_rt(genes, clean_bins)

    bins_output_path.parent.mkdir(parents=True, exist_ok=True)
    clean_bins.to_feather(bins_output_path)
    gene_annotations.to_feather(genes_output_path)

    print(
        "Prepared "
        f"{len(clean_bins)} constitutive RT bins and "
        f"{len(gene_annotations)} gene-level annotations from {rt_input_path}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
