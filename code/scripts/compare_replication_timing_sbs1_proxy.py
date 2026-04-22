"""
compare_replication_timing_sbs1_proxy.py

Re-run the replication-timing burden comparison after restricting mutations to a
lightweight SBS1-like proxy: CpG C>T events and their complementary G>A form,
using the annotated `codons` field as the local context source.
"""

import math
from pathlib import Path

import pandas as pd

from compare_replication_timing_burden import (
    PER_SAMPLE_COLUMNS,
    build_comparison_table,
    build_sample_rt_burden_table as build_all_mutation_rt_burden_table,
    build_symbol_rt_map,
)

VALID_BASES = frozenset({"A", "C", "G", "T"})


def parse_codon_change(codons: str | None) -> tuple[str, str] | None:
    if codons is None or pd.isna(codons):
        return None

    text = str(codons).strip()
    if text.count("/") != 1:
        return None

    ref_codon, alt_codon = text.split("/")
    ref_codon = ref_codon.upper()
    alt_codon = alt_codon.upper()
    if len(ref_codon) != 3 or len(alt_codon) != 3:
        return None
    if set(ref_codon) - VALID_BASES or set(alt_codon) - VALID_BASES:
        return None
    return ref_codon, alt_codon


def codon_single_base_change(codons: str | None) -> tuple[int, str, str] | None:
    parsed = parse_codon_change(codons)
    if parsed is None:
        return None

    ref_codon, alt_codon = parsed
    changed = [(idx, ref_base, alt_base) for idx, (ref_base, alt_base) in enumerate(zip(ref_codon, alt_codon)) if ref_base != alt_base]
    if len(changed) != 1:
        return None
    return changed[0]


def is_sbs1_proxy_mutation(reference_allele: str, alt_allele: str, codons: str | None) -> bool:
    ref = str(reference_allele).upper()
    alt = str(alt_allele).upper()
    if ref not in VALID_BASES or alt not in VALID_BASES:
        return False
    if (ref, alt) not in {("C", "T"), ("G", "A")}:
        return False

    change = codon_single_base_change(codons)
    if change is None:
        return False

    idx, codon_ref, codon_alt = change
    if codon_ref != ref or codon_alt != alt:
        return False

    parsed = parse_codon_change(codons)
    assert parsed is not None
    ref_codon, _ = parsed
    if ref == "C":
        return idx < 2 and ref_codon[idx + 1] == "G"
    return idx > 0 and ref_codon[idx - 1] == "C"


def filter_to_sbs1_proxy_mutations(mutations: pd.DataFrame) -> pd.DataFrame:
    ref = mutations["reference_allele"].astype(str).str.upper()
    alt = mutations["tumor_seq_allele2"].astype(str).str.upper()
    snv_mask = (
        ref.str.len().eq(1)
        & alt.str.len().eq(1)
        & ref.isin(VALID_BASES)
        & alt.isin(VALID_BASES)
        & ((ref.eq("C") & alt.eq("T")) | (ref.eq("G") & alt.eq("A")))
    )
    snvs = mutations.loc[snv_mask].copy()
    if snvs.empty:
        return snvs

    ref = snvs["reference_allele"].astype(str).str.upper()
    alt = snvs["tumor_seq_allele2"].astype(str).str.upper()
    codon_parts = snvs["codons"].astype("string").str.extract(r"^(?P<ref>[ACGTacgt]{3})/(?P<alt>[ACGTacgt]{3})$")
    valid_codon = codon_parts.notna().all(axis=1)
    ref_codon = codon_parts["ref"].str.upper()
    alt_codon = codon_parts["alt"].str.upper()

    diff0 = (ref_codon.str[0] != alt_codon.str[0]).fillna(False)
    diff1 = (ref_codon.str[1] != alt_codon.str[1]).fillna(False)
    diff2 = (ref_codon.str[2] != alt_codon.str[2]).fillna(False)
    single_change = valid_codon & ((diff0.astype(int) + diff1.astype(int) + diff2.astype(int)) == 1)

    c_to_t = ref.eq("C") & alt.eq("T") & single_change & (
        (diff0 & ref_codon.str[0].eq("C") & alt_codon.str[0].eq("T") & ref_codon.str[1].eq("G"))
        | (diff1 & ref_codon.str[1].eq("C") & alt_codon.str[1].eq("T") & ref_codon.str[2].eq("G"))
    )
    g_to_a = ref.eq("G") & alt.eq("A") & single_change & (
        (diff1 & ref_codon.str[1].eq("G") & alt_codon.str[1].eq("A") & ref_codon.str[0].eq("C"))
        | (diff2 & ref_codon.str[2].eq("G") & alt_codon.str[2].eq("A") & ref_codon.str[1].eq("C"))
    )
    proxy_mask = c_to_t | g_to_a
    return snvs.loc[proxy_mask].copy()


def build_sample_rt_burden_table(
    *,
    study_id: str,
    mutations: pd.DataFrame,
    assignments: pd.DataFrame,
    symbol_rt: pd.DataFrame,
    ratio_pseudocount: float,
) -> pd.DataFrame:
    assignment_subset = assignments[["lookup_key", "sample_name"]].drop_duplicates().copy()
    proxy_mutations = filter_to_sbs1_proxy_mutations(mutations)
    if proxy_mutations.empty:
        empty = assignment_subset.copy()
        empty["study_id"] = study_id
        empty["CE"] = 0
        empty["CL"] = 0
        empty["cl_ce_ratio"] = ratio_pseudocount / ratio_pseudocount
        empty["log10_cl_ce_ratio"] = 0.0
        return empty[PER_SAMPLE_COLUMNS].sort_values(["lookup_key", "sample_name"]).reset_index(drop=True)

    counts = build_all_mutation_rt_burden_table(
        study_id=study_id,
        mutations=proxy_mutations,
        assignments=assignments,
        symbol_rt=symbol_rt,
        ratio_pseudocount=ratio_pseudocount,
    )
    out = assignment_subset.merge(
        counts[["lookup_key", "sample_name", "CE", "CL"]],
        on=["lookup_key", "sample_name"],
        how="left",
    )
    out["study_id"] = study_id
    out["CE"] = out["CE"].fillna(0).astype(int)
    out["CL"] = out["CL"].fillna(0).astype(int)
    out["cl_ce_ratio"] = (out["CL"] + ratio_pseudocount) / (out["CE"] + ratio_pseudocount)
    out["log10_cl_ce_ratio"] = out["cl_ce_ratio"].map(math.log10)
    return out[PER_SAMPLE_COLUMNS].sort_values(["lookup_key", "sample_name"]).reset_index(drop=True)


def load_assignment_inputs(
    study_inputs: list[dict[str, str | Path]],
    *,
    symbol_rt: pd.DataFrame,
    ratio_pseudocount: float,
) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for item in study_inputs:
        mutations = pd.read_feather(
            Path(item["mutations"]),
            columns=["symbol", "sample_id_tumor", "reference_allele", "tumor_seq_allele2", "codons"],
        )
        assignments = pd.read_feather(Path(item["assignments"]))
        frame = build_sample_rt_burden_table(
            study_id=str(item["study_id"]),
            mutations=mutations,
            assignments=assignments,
            symbol_rt=symbol_rt,
            ratio_pseudocount=ratio_pseudocount,
        )
        if not frame.empty:
            frames.append(frame)

    if not frames:
        return pd.DataFrame(columns=PER_SAMPLE_COLUMNS)
    return pd.concat(frames, ignore_index=True)


def main() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    gene_rt = pd.read_feather(snek.input.gene_rt)
    symbol_rt = build_symbol_rt_map(gene_rt)

    study_inputs = [
        {
            "study_id": study_id,
            "mutations": mutation_path,
            "assignments": assignment_path,
        }
        for study_id, mutation_path, assignment_path in zip(
            list(snek.params.ids),
            list(snek.input.mutations),
            list(snek.input.assignments),
            strict=True,
        )
    ]

    ratio_pseudocount = float(snek.config.get("signature_ratio_pseudocount", 0.5))
    per_sample = load_assignment_inputs(
        study_inputs,
        symbol_rt=symbol_rt,
        ratio_pseudocount=ratio_pseudocount,
    )
    comparison = build_comparison_table(
        per_sample,
        matched_normal_studies=set(snek.config.get("matched_normal_studies", [])),
        min_samples_per_group=int(snek.config.get("signature_ratio_min_samples_per_group", 25)),
    )
    per_sample.to_feather(snek.output.per_sample)
    comparison.to_feather(snek.output.summary)


if __name__ == "__main__":
    main()
