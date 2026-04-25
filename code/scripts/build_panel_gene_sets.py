"""Rule (1a): emit per-panel callable-gene feathers.

Per design Section 4.2: scatter is per panel_id (NOT per study). Reads a
4-column BED (chrom, start, end, symbol), dedupes per symbol, restricts to
HGNC-canonical symbols via data/grch38.tsv, writes a feather with columns
(symbol, callable, panel_id, source).

The pseudo-panel 'wes' is built differently: every HGNC symbol from grch38
is marked callable=True with source='wes_default'.
"""

from pathlib import Path

import pandas as pd

BED_COLS = ["chrom", "start", "end", "symbol"]
OUT_COLS = ["symbol", "callable", "panel_id", "source"]


def _load_hgnc_symbols(grch38_path: Path) -> set[str]:
    df = pd.read_csv(grch38_path, sep="\t")
    col = "symbol" if "symbol" in df.columns else "Hugo_Symbol"
    return set(df[col].dropna().astype(str).str.strip())


def build_panel_gene_set(
    panel_id: str,
    bed_path: Path,
    grch38_path: Path,
    out_path: Path,
) -> None:
    if not Path(bed_path).exists():
        raise FileNotFoundError(f"panel BED not found: {bed_path}")

    hgnc = _load_hgnc_symbols(Path(grch38_path))

    bed = pd.read_csv(
        bed_path, sep="\t", header=None, names=BED_COLS, dtype={"symbol": "string"}
    )
    if bed.empty:
        # Empty placeholder -- emit zero-row feather with the right schema.
        out = pd.DataFrame(
            {
                c: pd.Series(dtype=t)
                for c, t in [
                    ("symbol", "string"),
                    ("callable", "bool"),
                    ("panel_id", "string"),
                    ("source", "string"),
                ]
            }
        )
    else:
        symbols = bed["symbol"].str.strip().dropna().unique()
        canonical = [s for s in symbols if s in hgnc]
        out = pd.DataFrame(
            {
                "symbol": canonical,
                "callable": True,
                "panel_id": panel_id,
                "source": "bed",
            }
        )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out[OUT_COLS].reset_index(drop=True).to_feather(out_path)


def build_wes_pseudo_panel(grch38_path: Path, out_path: Path) -> None:
    hgnc = sorted(_load_hgnc_symbols(Path(grch38_path)))
    out = pd.DataFrame(
        {
            "symbol": hgnc,
            "callable": True,
            "panel_id": "wes",
            "source": "wes_default",
        }
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out[OUT_COLS].reset_index(drop=True).to_feather(out_path)


if "snakemake" in globals():  # pragma: no cover  # set by Snakemake's script: directive
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    panel_id = snek.wildcards["panel_id"]
    if panel_id == "wes":
        build_wes_pseudo_panel(
            grch38_path=Path(snek.input["grch38"]),
            out_path=Path(snek.output[0]),
        )
    else:
        build_panel_gene_set(
            panel_id=panel_id,
            bed_path=Path(snek.input["bed"]),
            grch38_path=Path(snek.input["grch38"]),
            out_path=Path(snek.output[0]),
        )
