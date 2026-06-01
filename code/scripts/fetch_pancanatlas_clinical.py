# science:code
# status: workflow-owned
# science:end
"""Fetch + verify the TCGA PanCanAtlas clinical-with-followup table (h08 Arm-B smoking covariate).

WP0 of `plan:2026-05-31-t199-h08-association-core` — a *hard, first-sequenced* data-access gate.
The file is `clinical_PANCAN_patient_with_followup.tsv`, served **open-access (no auth)** from the
GDC data endpoint at file UUID ``0fc78496-818b-4896-bd83-52db1f533c5c``. It carries the only TCGA
source of `tobacco_smoking_history` + `number_pack_years_smoked` (the cBioPortal per-study
PanCanAtlas clinical does not). See review finding F2' (the route was mis-described as Synapse-gated
in an early draft; the GDC ``/data`` route is open-access — corrected).

This is a download + LOUD verification step, not a silent fetch (per the verify-before-claiming
discipline): we assert the on-disk size, compute + record the md5, confirm the smoking columns are
present, and report LUAD+LUSC non-missingness (the realized Arm-B covariate completeness that feeds
the pre-reg §1b table). Any failed check exits non-zero — a partial/stub download must not pass.

Fallbacks (used only if the GDC direct file becomes unavailable): GDC open-access BCR Biotab
per-tumor clinical, or the GerkeLab/TCGAclinical GitHub mirror of the same GDC file.
"""

import hashlib
import json
import urllib.request
from pathlib import Path

import click
import pandas as pd
from rich.console import Console
from rich.table import Table

console = Console()

GDC_FILE_UUID = "0fc78496-818b-4896-bd83-52db1f533c5c"
GDC_DATA_URL = f"https://api.gdc.cancer.gov/data/{GDC_FILE_UUID}"
EXPECTED_SIZE = 18_633_685  # bytes, per the GDC PanCanAtlas supplemental listing
SMOKING_COLS = ["tobacco_smoking_history", "number_pack_years_smoked"]
ACRONYM_COL = "acronym"  # TCGA cancer-type code column in this table
ARM_B_HISTOLOGIES = ["LUAD", "LUSC"]
PATIENT_BARCODE_COL = (
    "bcr_patient_barcode"  # 12-char TCGA patient barcode (the h08 join key)
)

# TCGA bracketed sentinels that mean "no value", in addition to empty / NaN.
TCGA_MISSING = {
    "[Not Available]",
    "[Unknown]",
    "[Not Applicable]",
    "[Not Evaluated]",
    "[Discrepancy]",
    "[Completed]",
    "",
}


def _is_missing(series: pd.Series) -> pd.Series:
    s = series.astype(str).str.strip()
    return series.isna() | s.isin(TCGA_MISSING)


def _download(dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    console.print(f"[cyan]downloading[/] {GDC_DATA_URL} → {dest}")
    with urllib.request.urlopen(GDC_DATA_URL) as stream:
        dest.write_bytes(stream.read())


def _md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


@click.command()
@click.option(
    "--dest",
    type=click.Path(path_type=Path),
    default=Path("data/pancanatlas_clinical_with_followup.tsv"),
    show_default=True,
    help="Output path for the clinical-with-followup TSV.",
)
@click.option(
    "--sidecar",
    type=click.Path(path_type=Path),
    default=None,
    help="Where to write the verification JSON sidecar (default: <dest>.verification.json).",
)
@click.option(
    "--force", is_flag=True, help="Re-download even if a size-matching file is present."
)
def main(dest: Path, sidecar: Path | None, force: bool) -> None:
    sidecar = sidecar or dest.with_suffix(dest.suffix + ".verification.json")

    # 1. download (skip if already present at the expected size, unless --force)
    if force or not dest.exists() or dest.stat().st_size != EXPECTED_SIZE:
        _download(dest)
    else:
        console.print(
            f"[green]present[/] {dest} already at expected size — skipping download"
        )

    # 2. size check (LOUD: a stub / truncated download must fail here)
    size = dest.stat().st_size
    size_ok = size == EXPECTED_SIZE
    md5 = _md5(dest)

    # 3. read header + smoking columns (TCGA biotab files are latin-1, not utf-8)
    df = pd.read_csv(dest, sep="\t", dtype=str, low_memory=False, encoding="latin-1")
    cols_present = [c for c in SMOKING_COLS if c in df.columns]
    cols_ok = len(cols_present) == len(SMOKING_COLS)
    acronym_ok = ACRONYM_COL in df.columns

    # 4. LUAD + LUSC non-missingness (realized Arm-B covariate completeness)
    completeness: dict[str, dict[str, object]] = {}
    arm_b_ok = acronym_ok and cols_ok
    if acronym_ok and cols_ok:
        for hist in ARM_B_HISTOLOGIES:
            sub = df[df[ACRONYM_COL] == hist]
            entry: dict[str, object] = {"n_patients": int(len(sub))}
            for col in SMOKING_COLS:
                nonmiss = int((~_is_missing(sub[col])).sum())
                entry[col] = {
                    "n_nonmissing": nonmiss,
                    "frac_nonmissing": round(nonmiss / len(sub), 4)
                    if len(sub)
                    else 0.0,
                }
            completeness[hist] = entry
            # Arm B needs *some* usable smoking signal in each lung histology.
            pack = completeness[hist]["number_pack_years_smoked"]["n_nonmissing"]  # type: ignore[index]
            hxy = completeness[hist]["tobacco_smoking_history"]["n_nonmissing"]  # type: ignore[index]
            if max(int(pack), int(hxy)) == 0:
                arm_b_ok = False

    # --- report ---
    tbl = Table(
        title="WP0 verification — PanCanAtlas clinical-with-followup", show_lines=False
    )
    tbl.add_column("check")
    tbl.add_column("result")
    tbl.add_row("size == 18,633,685 B", f"{'PASS' if size_ok else 'FAIL'} ({size:,} B)")
    tbl.add_row("md5", md5)
    tbl.add_row(
        "smoking columns present", f"{'PASS' if cols_ok else 'FAIL'} ({cols_present})"
    )
    tbl.add_row(f"{ACRONYM_COL} column present", "PASS" if acronym_ok else "FAIL")
    tbl.add_row(
        f"{PATIENT_BARCODE_COL} present",
        "PASS" if PATIENT_BARCODE_COL in df.columns else "FAIL",
    )
    tbl.add_row("rows × cols", f"{df.shape[0]:,} × {df.shape[1]:,}")
    console.print(tbl)
    for hist, entry in completeness.items():
        py = entry["number_pack_years_smoked"]  # type: ignore[index]
        hx = entry["tobacco_smoking_history"]  # type: ignore[index]
        console.print(
            f"  [bold]{hist}[/] n={entry['n_patients']}  "
            f"pack_years {py['n_nonmissing']}/{entry['n_patients']} ({py['frac_nonmissing']:.0%})  "  # type: ignore[index]
            f"smoking_history {hx['n_nonmissing']}/{entry['n_patients']} ({hx['frac_nonmissing']:.0%})"  # type: ignore[index]
        )

    verification = {
        "source": GDC_DATA_URL,
        "file_uuid": GDC_FILE_UUID,
        "dest": str(dest),
        "expected_size": EXPECTED_SIZE,
        "observed_size": size,
        "size_ok": size_ok,
        "md5": md5,
        "smoking_columns_present": cols_present,
        "smoking_columns_ok": cols_ok,
        "acronym_column_present": acronym_ok,
        "patient_barcode_column": PATIENT_BARCODE_COL,
        "n_rows": int(df.shape[0]),
        "n_cols": int(df.shape[1]),
        "arm_b_completeness": completeness,
        "all_checks_pass": bool(size_ok and cols_ok and acronym_ok and arm_b_ok),
    }
    sidecar.write_text(json.dumps(verification, indent=2))
    console.print(f"[cyan]wrote[/] {sidecar}")

    if not verification["all_checks_pass"]:
        raise SystemExit(
            "WP0 verification FAILED — do not let WP1 consume this file. "
            "If the GDC direct file is unavailable, fall back to BCR Biotab / GerkeLab mirror "
            "(see plan WP0)."
        )
    console.print(
        "[bold green]WP0 verification PASSED[/] — smoking covariate ready for WP1."
    )


if __name__ == "__main__":
    main()
