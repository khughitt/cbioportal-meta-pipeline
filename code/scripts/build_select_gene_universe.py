# science:code
# status: workflow-owned
# science:end
"""Rule (1b): emit the SELECT gene-universe TSV with provenance columns.

See doc/plans/2026-04-25-t078-select-cooccurrence-design.md Section 4.3.

Reads:
  - Bailey 2018 Table S1 TSV (from data/bailey2018_table_s1.tsv)
  - COSMIC CGC TSV (from data/cosmic_cgc.tsv) -- manual prereq
  - Sanchez-Vega pathway TSV (from data/sanchez_vega_pathways.tsv)
  - optional custom genes TSV (one symbol per line, no header)

Writes:
  - results/select/gene_universe.tsv

Columns: symbol, from_bailey, from_cgc, from_sanchez_vega, from_custom,
         bailey_version, cgc_version, sanchez_vega_version,
         bailey_sha256, cgc_sha256, sanchez_vega_sha256
"""

import hashlib
from pathlib import Path

import pandas as pd

GeneSet = set[str]


def _sha256_prefix(path: Path, n_chars: int = 12) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:n_chars]


def _read_bailey(path: Path) -> GeneSet:
    df = pd.read_csv(path, sep="\t")
    return set(df["Gene"].dropna().astype(str).str.strip())


def _read_cgc(path: Path) -> GeneSet:
    df = pd.read_csv(path, sep="\t")
    col = "Gene Symbol" if "Gene Symbol" in df.columns else "symbol"
    return set(df[col].dropna().astype(str).str.strip())


def _read_sanchez_vega(path: Path) -> GeneSet:
    df = pd.read_csv(path, sep="\t")
    col = "gene" if "gene" in df.columns else "Gene"
    return set(df[col].dropna().astype(str).str.strip())


def _read_custom(path: Path | None) -> GeneSet:
    if path is None:
        return set()
    text = Path(path).read_text().strip()
    if not text:
        return set()
    return {line.strip() for line in text.splitlines() if line.strip()}


def build_universe(
    bailey_path: Path,
    cgc_path: Path,
    sanchez_vega_path: Path,
    custom_path: Path | None,
    out_path: Path,
    bailey_version: str,
    cgc_version: str,
    sanchez_vega_version: str,
) -> None:
    bailey = _read_bailey(bailey_path)
    cgc = _read_cgc(cgc_path)
    sv = _read_sanchez_vega(sanchez_vega_path)
    custom = _read_custom(custom_path)

    all_symbols = sorted(bailey | cgc | sv | custom)

    bailey_sha = _sha256_prefix(bailey_path)
    cgc_sha = _sha256_prefix(cgc_path)
    sv_sha = _sha256_prefix(sanchez_vega_path)

    df = pd.DataFrame({"symbol": all_symbols})
    df["from_bailey"] = df["symbol"].isin(bailey)
    df["from_cgc"] = df["symbol"].isin(cgc)
    df["from_sanchez_vega"] = df["symbol"].isin(sv)
    df["from_custom"] = df["symbol"].isin(custom)
    df["bailey_version"] = bailey_version
    df["cgc_version"] = cgc_version
    df["sanchez_vega_version"] = sanchez_vega_version
    df["bailey_sha256"] = bailey_sha
    df["cgc_sha256"] = cgc_sha
    df["sanchez_vega_sha256"] = sv_sha

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, sep="\t", index=False)


# Snakemake entry point.
if "snakemake" in globals():  # pragma: no cover  # set by Snakemake's script: directive
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    build_universe(
        bailey_path=Path(snek.input["bailey"]),
        cgc_path=Path(snek.input["cgc"]),
        sanchez_vega_path=Path(snek.input["sanchez_vega"]),
        custom_path=Path(snek.input["custom"])
        if "custom" in snek.input.keys()
        else None,
        out_path=Path(snek.output["universe"]),
        bailey_version=snek.params["bailey_version"],
        cgc_version=snek.params["cgc_version"],
        sanchez_vega_version=snek.params["sanchez_vega_version"],
    )
