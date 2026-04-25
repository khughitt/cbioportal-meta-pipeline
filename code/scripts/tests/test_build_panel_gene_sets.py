"""Unit tests for build_panel_gene_sets."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

import build_panel_gene_sets as mod


@pytest.fixture
def grch38(tmp_path: Path):
    """Tiny grch38.tsv lookup with 4 canonical symbols."""
    p = tmp_path / "grch38.tsv"
    p.write_text(
        "ensgene\tentrez\tsymbol\tchr\tstart\tend\tstrand\tbiotype\tdescription\n"
        "ENSG1\t1\tTP53\t17\t1\t100\t+\tprotein_coding\tt53\n"
        "ENSG2\t2\tKRAS\t12\t1\t100\t+\tprotein_coding\tkras\n"
        "ENSG3\t3\tEGFR\t7\t1\t100\t+\tprotein_coding\tegfr\n"
        "ENSG4\t4\tBRAF\t7\t1\t100\t+\tprotein_coding\tbraf\n"
    )
    return p


def test_panel_gene_set_dedupes_intervals(tmp_path: Path, grch38):
    bed = tmp_path / "tinypanel.bed"
    bed.write_text(
        "chr17\t1\t100\tTP53\n"
        "chr17\t101\t200\tTP53\n"        # second exon -- must dedupe
        "chr12\t1\t100\tKRAS\n"
    )
    out = tmp_path / "tinypanel.feather"
    mod.build_panel_gene_set(
        panel_id="tinypanel",
        bed_path=bed,
        grch38_path=grch38,
        out_path=out,
    )
    df = pd.read_feather(out)
    assert len(df) == 2
    assert set(df["symbol"]) == {"TP53", "KRAS"}
    assert (df["callable"] == True).all()  # noqa: E712
    assert (df["panel_id"] == "tinypanel").all()
    assert (df["source"] == "bed").all()


def test_panel_gene_set_drops_non_hgnc(tmp_path: Path, grch38):
    bed = tmp_path / "tinypanel.bed"
    bed.write_text(
        "chr17\t1\t100\tTP53\n"
        "chr_unknown\t1\t100\tFOOBAR_NOT_HGNC\n"
    )
    out = tmp_path / "out.feather"
    mod.build_panel_gene_set(
        panel_id="tinypanel", bed_path=bed,
        grch38_path=grch38, out_path=out,
    )
    df = pd.read_feather(out)
    assert "FOOBAR_NOT_HGNC" not in set(df["symbol"])
    assert "TP53" in set(df["symbol"])


def test_wes_pseudo_panel_marks_all_callable(tmp_path: Path, grch38):
    """The 'wes' pseudo-panel emits one row per HGNC symbol with callable=True."""
    out = tmp_path / "wes.feather"
    mod.build_wes_pseudo_panel(grch38_path=grch38, out_path=out)
    df = pd.read_feather(out)
    assert len(df) == 4
    assert set(df["symbol"]) == {"TP53", "KRAS", "EGFR", "BRAF"}
    assert (df["callable"] == True).all()  # noqa: E712
    assert (df["panel_id"] == "wes").all()
    assert (df["source"] == "wes_default").all()


def test_panel_gene_set_missing_bed_raises(tmp_path: Path, grch38):
    out = tmp_path / "out.feather"
    with pytest.raises(FileNotFoundError):
        mod.build_panel_gene_set(
            panel_id="missing", bed_path=tmp_path / "does_not_exist.bed",
            grch38_path=grch38, out_path=out,
        )
