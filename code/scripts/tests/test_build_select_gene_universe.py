"""Unit tests for build_select_gene_universe."""
from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
import pytest

import build_select_gene_universe as mod


def _write_tsv(path: Path, df: pd.DataFrame) -> None:
    df.to_csv(path, sep="\t", index=False)


def _sha256_prefix(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


@pytest.fixture
def sources(tmp_path: Path):
    """Three small source files: Bailey, CGC, Sanchez-Vega, partial overlap."""
    bailey = tmp_path / "bailey2018.tsv"
    _write_tsv(bailey, pd.DataFrame({"Gene": ["TP53", "KRAS", "EGFR"]}))
    cgc = tmp_path / "cgc.tsv"
    _write_tsv(cgc, pd.DataFrame({"Gene Symbol": ["KRAS", "BRAF", "MYC"]}))
    sv = tmp_path / "sanchez_vega.tsv"
    _write_tsv(sv, pd.DataFrame({
        "gene": ["EGFR", "BRAF", "PIK3CA"],
        "pathway": ["RTK_RAS", "RTK_RAS", "PI3K"],
    }))
    return bailey, cgc, sv


def test_build_universe_unions_three_sources(tmp_path: Path, sources):
    bailey, cgc, sv = sources
    out = tmp_path / "universe.tsv"
    mod.build_universe(
        bailey_path=bailey,
        cgc_path=cgc,
        sanchez_vega_path=sv,
        custom_path=None,
        out_path=out,
        bailey_version="2018",
        cgc_version="2024-09",
        sanchez_vega_version="2018",
    )
    df = pd.read_csv(out, sep="\t")
    assert set(df["symbol"]) == {"TP53", "KRAS", "EGFR", "BRAF", "MYC", "PIK3CA"}


def test_build_universe_provenance_columns_populated(tmp_path: Path, sources):
    bailey, cgc, sv = sources
    out = tmp_path / "universe.tsv"
    mod.build_universe(
        bailey_path=bailey, cgc_path=cgc, sanchez_vega_path=sv,
        custom_path=None, out_path=out,
        bailey_version="2018", cgc_version="2024-09",
        sanchez_vega_version="2018",
    )
    df = pd.read_csv(out, sep="\t")
    for col in ["from_bailey", "from_cgc", "from_sanchez_vega", "from_custom",
                "bailey_version", "cgc_version", "sanchez_vega_version",
                "bailey_sha256", "cgc_sha256", "sanchez_vega_sha256"]:
        assert col in df.columns, f"missing {col}"
    # KRAS in Bailey + CGC, not SV / custom
    row = df[df["symbol"] == "KRAS"].iloc[0]
    assert bool(row["from_bailey"]) is True
    assert bool(row["from_cgc"]) is True
    assert bool(row["from_sanchez_vega"]) is False
    assert bool(row["from_custom"]) is False
    assert row["bailey_sha256"] == _sha256_prefix(bailey)


def test_build_universe_custom_genes(tmp_path: Path, sources):
    bailey, cgc, sv = sources
    custom = tmp_path / "custom.tsv"
    custom.write_text("ZNF1\nZNF2\n")  # one symbol per line, no header
    out = tmp_path / "universe.tsv"
    mod.build_universe(
        bailey_path=bailey, cgc_path=cgc, sanchez_vega_path=sv,
        custom_path=custom, out_path=out,
        bailey_version="2018", cgc_version="2024-09",
        sanchez_vega_version="2018",
    )
    df = pd.read_csv(out, sep="\t")
    assert "ZNF1" in set(df["symbol"])
    assert "ZNF2" in set(df["symbol"])
    znf1 = df[df["symbol"] == "ZNF1"].iloc[0]
    assert bool(znf1["from_custom"]) is True
    assert bool(znf1["from_bailey"]) is False


def test_build_universe_empty_custom_path_means_none(tmp_path: Path, sources):
    bailey, cgc, sv = sources
    out = tmp_path / "universe.tsv"
    mod.build_universe(
        bailey_path=bailey, cgc_path=cgc, sanchez_vega_path=sv,
        custom_path=None, out_path=out,
        bailey_version="2018", cgc_version="2024-09",
        sanchez_vega_version="2018",
    )
    df = pd.read_csv(out, sep="\t")
    assert (df["from_custom"] == False).all()  # noqa: E712
