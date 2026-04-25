"""Derive per-panel BED files from the GENIE consolidated genomic_information.txt.

Snakemake-driven: input is the GENIE consolidated assay BED, output is one BED
per panel listed in PANEL_TO_ASSAY (MSK-IMPACT 341/410/468/505 and the F1/F1CDx
proxies). Empty placeholder files are written for assays absent from the GENIE
release so downstream rules see a stable file set.

The output BEDs are 4-column TSV (chrom, start, end, symbol) with no header, one
row per (assay x exon interval). Multiple rows per gene are expected; rule (1a)
deduplicates per (panel_id, symbol).
"""

from pathlib import Path

import pandas as pd
from rich import print as rprint

# GENIE assay id -> output BED path (relative to repo root).
# F1/F1CDx are proxies, not pure Foundation Medicine BEDs -- see data/panels/README.md.
PANEL_TO_ASSAY: dict[str, str] = {
    "MSK-IMPACT341": "data/panels/IMPACT341.bed",
    "MSK-IMPACT410": "data/panels/IMPACT410.bed",
    "MSK-IMPACT468": "data/panels/IMPACT468.bed",
    "MSK-IMPACT505": "data/panels/IMPACT505.bed",
    "DUKE-F1-DX1": "data/panels/F1CDx.bed",
    "PROV-FOUNDATIONONELIQUIDCDX": "data/panels/F1.bed",
}


def build_panel_beds(genie_genomic_info: Path, out_paths: dict[str, Path]) -> None:
    """Write one BED per assay in PANEL_TO_ASSAY from the consolidated GENIE file."""
    if not genie_genomic_info.exists():
        raise FileNotFoundError(
            f"GENIE genomic_information.txt missing: {genie_genomic_info}"
        )

    df = pd.read_csv(genie_genomic_info, sep="\t", dtype={"Chromosome": "string"})
    df = df[df["includeInPanel"].fillna(True).astype(bool)]
    df = df[df["Feature_Type"] == "exon"]

    for assay, out in out_paths.items():
        out.parent.mkdir(parents=True, exist_ok=True)
        sub = df[df["SEQ_ASSAY_ID"] == assay]
        if sub.empty:
            out.write_text("")
            rprint(
                f"[yellow]WARN[/]: no rows for {assay}; wrote empty placeholder {out}"
            )
            continue
        bed = sub[
            ["Chromosome", "Start_Position", "End_Position", "Hugo_Symbol"]
        ].copy()
        bed.columns = ["chrom", "start", "end", "symbol"]
        bed.to_csv(out, sep="\t", index=False, header=False)
        rprint(f"wrote {out}: {len(bed)} intervals, {bed['symbol'].nunique()} symbols")


if __name__ == "__main__":
    # Snakemake entry point.
    src = Path(snakemake.input[0])  # type: ignore[name-defined]  # noqa: F821
    out_paths = {
        assay: Path(p)
        for assay, p in zip(PANEL_TO_ASSAY, snakemake.output)  # type: ignore[name-defined]  # noqa: F821
    }
    build_panel_beds(src, out_paths)
