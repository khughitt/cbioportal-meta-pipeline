"""
stage_li2021_somatic_mutations.py

One-off staging script: converts the Li 2021 Nature Supplementary Table 3
XLSX (41586_2021_3836_MOESM5_ESM.xlsx) into the TSV schema that the t111
extract_normal_tissue_spectra pipeline consumes.

Input schema (XLSX, Sheet1, row 3 headers):
  sampleID, chr, pos, ref, mut, gene, strand, ref_cod, mut_cod, ref3_cod,
  mut3_cod, aachange, ntchange, codonsub, impact, ref_count, alt_count

Output schema (TSV):
  donor_id, tissue_label, sample_id, chrom, pos, ref, alt

sampleID parsing: format is PN{donor_digit}{tissue_code}-{layer}-{biopsy},
e.g. 'PN1C-1-1' → donor_id='PN1', tissue_label='Colon', sample_id='PN1C-1-1'.
Greedy longest-prefix match on tissue_code so 'Ca' beats 'C'. The actual data
uses 'G' (Gastric cardia) for the Cardia tissue (not 'Ca' as the gate record
speculated). Raises on any sampleID that fails to match.

Usage:
    uv run python code/scripts/stage_li2021_somatic_mutations.py \\
        --xlsx data/41586_2021_3836_MOESM5_ESM.xlsx \\
        --out data/li2021_somatic_mutations.tsv
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

# tissue codes are matched greedy longest-prefix (2-char codes must come before
# 1-char codes in this iteration so "Ca" beats "C" for Cardia vs Colon, if
# the 2-char variant ever appears).
#
# NOTE: The gate-record speculated 'Ca' for Cardia based on conventions, but the
# actual XLSX data uses 'G' (Gastric cardia) — donors PN7/8/9 have 'G' where the
# paper's Sheet2 and bib note list "Cardia" as a distinct tissue. 'Ca' does not
# appear in the data.
TISSUE_CODE_MAP: list[tuple[str, str]] = [
    ("Ca", "Cardia"),  # speculative; not seen in the XLSX — 'G' is used instead
    ("G", "Cardia"),  # Gastric cardia; used by PN7/PN8/PN9 (Li 2021 Sheet1)
    ("B", "Bronchia"),
    ("E", "Esophagus"),
    ("S", "Stomach"),
    ("D", "Duodenum"),
    ("C", "Colon"),
    ("R", "Rectum"),
    ("L", "Liver"),
    ("P", "Pancreas"),
]


def _parse_sample_id(sample_id: str) -> tuple[str, str]:
    """Returns (donor_id, tissue_label) from a sampleID like 'PN1C-1-1'.

    donor_id is the 'PN' + first digit(s). tissue_label is looked up from
    the remaining prefix before the first dash via greedy longest-prefix match.
    """
    prefix = sample_id.split("-", 1)[0]  # e.g. "PN1C" or "PN7Ca"
    if not prefix.startswith("PN"):
        raise ValueError(f"Unexpected sampleID format (no PN prefix): {sample_id!r}")
    rest = prefix[2:]  # strip "PN"
    # Consume digits for donor number
    i = 0
    while i < len(rest) and rest[i].isdigit():
        i += 1
    donor_digits = rest[:i]
    tissue_code_raw = rest[i:]
    if not donor_digits:
        raise ValueError(f"Unexpected sampleID format (no donor digits): {sample_id!r}")
    donor_id = f"PN{donor_digits}"
    for code, label in TISSUE_CODE_MAP:
        if tissue_code_raw == code:
            return donor_id, label
    raise ValueError(
        f"Unrecognised tissue code {tissue_code_raw!r} in sampleID {sample_id!r}"
    )


def stage_xlsx_to_tsv(xlsx_path: Path, out_path: Path) -> None:
    """Convert the Li 2021 XLSX to the t111 TSV schema."""
    # Sheet1 has 2 title/meta rows before the header; header is row 2 (0-indexed).
    raw = pd.read_excel(xlsx_path, sheet_name=0, header=2, engine="openpyxl")
    print(f"Read {len(raw)} rows from {xlsx_path}", file=sys.stderr)

    parsed = raw["sampleID"].apply(_parse_sample_id)
    out = pd.DataFrame(
        {
            "donor_id": [x[0] for x in parsed],
            "tissue_label": [x[1] for x in parsed],
            "sample_id": raw["sampleID"].astype(str),
            "chrom": raw["chr"]
            .astype(str)
            .apply(lambda c: c if c.startswith("chr") else f"chr{c}"),
            "pos": raw["pos"].astype(int),
            "ref": raw["ref"].astype(str),
            "alt": raw["mut"].astype(str),
        }
    )
    out.to_csv(out_path, sep="\t", index=False)
    print(
        f"Wrote {len(out)} rows to {out_path}; "
        f"donors: {sorted(out['donor_id'].unique())}; "
        f"tissues: {sorted(out['tissue_label'].unique())}",
        file=sys.stderr,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xlsx", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    stage_xlsx_to_tsv(args.xlsx, args.out)


if __name__ == "__main__":
    main()
