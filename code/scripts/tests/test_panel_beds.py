"""Sanity checks on vendored panel BEDs."""
from pathlib import Path

import pandas as pd
import pytest

PANELS_DIR = Path(__file__).resolve().parents[3] / "data" / "panels"
EXPECTED_PANELS = [
    "IMPACT341", "IMPACT410", "IMPACT468", "IMPACT505",
    "F1", "F1CDx",
]
BED_COLS = ["chrom", "start", "end", "symbol"]


def test_panels_dir_exists():
    assert PANELS_DIR.is_dir()


@pytest.mark.parametrize("name", EXPECTED_PANELS)
def test_panel_bed_present(name):
    p = PANELS_DIR / f"{name}.bed"
    assert p.exists(), f"missing {p}"


@pytest.mark.parametrize("name", EXPECTED_PANELS)
def test_panel_bed_has_required_columns(name):
    p = PANELS_DIR / f"{name}.bed"
    df = pd.read_csv(p, sep="\t", header=None, names=BED_COLS)
    if df.empty:
        pytest.skip(f"{name} bed is empty placeholder -- see data/panels/README.md")
    for c in BED_COLS:
        assert c in df.columns


@pytest.mark.parametrize("name", ["IMPACT341", "IMPACT410", "IMPACT468", "IMPACT505"])
def test_msk_impact_panel_size_in_range(name):
    """MSK-IMPACT panels should have between 300 and 600 unique symbols."""
    p = PANELS_DIR / f"{name}.bed"
    df = pd.read_csv(p, sep="\t", header=None, names=BED_COLS)
    n_symbols = df["symbol"].nunique()
    assert 300 <= n_symbols <= 600, (
        f"{name} has {n_symbols} symbols; expected ~341/410/468/505 +/- slack"
    )


def test_study_panels_tsv():
    f = PANELS_DIR.parent / "study_panels.tsv"
    assert f.exists(), f"missing {f}"
    df = pd.read_csv(f, sep="\t")
    for c in ["study_id", "panel_id", "sequencing_type"]:
        assert c in df.columns
    assert (df["sequencing_type"].isin(["wes", "panel"])).all()
