# science:code
# status: library
# science:end
from pathlib import Path

import pandas as pd
import pytest

import run_restricted_sigprofiler_assignment as rsa


def test_normalize_cancer_type_maps_cbioportal_labels() -> None:
    assert rsa.normalize_cancer_type("Breast Cancer") == "breast"
    assert rsa.normalize_cancer_type("BRCA") == "breast"
    assert rsa.normalize_cancer_type("Urothelial Carcinoma") == "bladder"
    assert rsa.normalize_cancer_type("BLCA") == "bladder"
    assert rsa.normalize_cancer_type("Lung Adenocarcinoma") == "lung"
    assert rsa.normalize_cancer_type("LUAD") == "lung"
    assert rsa.normalize_cancer_type("Glioblastoma") == "cns"
    assert rsa.normalize_cancer_type("GBM") == "cns"
    assert rsa.normalize_cancer_type("Acute Myeloid Leukemia") == "myeloid"
    assert rsa.normalize_cancer_type("AML") == "myeloid"
    assert rsa.normalize_cancer_type("Mature B-Cell Neoplasms") == "lymphoid"

    with pytest.raises(ValueError, match="Unsupported cancer_type"):
        rsa.normalize_cancer_type("Totally Unknown Cancer")


def test_load_signature_lookup_groups_signatures(tmp_path: Path) -> None:
    lookup_path = tmp_path / "lookup.tsv"
    lookup_path.write_text(
        "\n".join(
            [
                "lookup_key\tfigure_cancer_type\tsignature",
                "breast\tBreast-AdenoCA\tSBS3",
                "breast\tBreast-AdenoCA\tSBS1",
                "breast\tBreast-AdenoCA\tSBS40",
                "lung\tLung-AdenoCA|Lung-SCC\tSBS4",
            ]
        )
        + "\n"
    )

    lookup = rsa.load_signature_lookup(lookup_path)

    assert lookup["breast"] == ["SBS1", "SBS3", "SBS40"]
    assert lookup["lung"] == ["SBS4"]


def test_write_restricted_signature_database_expands_split_aliases(tmp_path: Path) -> None:
    reference_path = tmp_path / "reference.tsv"
    pd.DataFrame(
        {
            "Type": ["A[C>A]A", "A[C>A]C"],
            "SBS1": [0.1, 0.2],
            "SBS3": [0.3, 0.4],
            "SBS22a": [0.5, 0.6],
            "SBS22b": [0.7, 0.8],
            "SBS40a": [0.9, 1.0],
            "SBS40b": [1.1, 1.2],
            "SBS40c": [1.3, 1.4],
        }
    ).to_csv(reference_path, sep="\t", index=False)

    out_path = tmp_path / "restricted.tsv"
    written = rsa.write_restricted_signature_database(
        reference_path=reference_path,
        requested_signatures=["SBS1", "SBS22", "SBS40"],
        output_path=out_path,
    )

    out = pd.read_csv(written, sep="\t")
    assert out.columns.tolist() == ["Type", "SBS1", "SBS22a", "SBS22b", "SBS40a", "SBS40b", "SBS40c"]


def test_build_assignment_table_for_study_uses_restricted_database(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    mutations_path = tmp_path / "mut.feather"
    samples_path = tmp_path / "samples.feather"
    lookup_path = tmp_path / "lookup.tsv"
    reference_path = tmp_path / "reference.tsv"

    pd.DataFrame(
        {
            "sample_id_tumor": ["S1", "S1"],
            "chromosome": ["chr1", "chr1"],
            "start": [101, 202],
            "reference_allele": ["C", "T"],
            "tumor_seq_allele2": ["A", "G"],
        }
    ).to_feather(mutations_path)
    pd.DataFrame({"sample_id": ["S1"], "cancer_type": ["Breast Cancer"]}).to_feather(samples_path)
    lookup_path.write_text(
        "\n".join(
            [
                "lookup_key\tfigure_cancer_type\tsignature",
                "breast\tBreast-AdenoCA\tSBS1",
                "breast\tBreast-AdenoCA\tSBS3",
                "breast\tBreast-AdenoCA\tSBS40",
            ]
        )
        + "\n"
    )
    pd.DataFrame(
        {
            "Type": rsa.CONTEXT_96[:4],
            "SBS1": [0.1, 0.2, 0.3, 0.4],
            "SBS3": [0.2, 0.2, 0.2, 0.2],
            "SBS40a": [0.3, 0.2, 0.1, 0.0],
            "SBS40b": [0.0, 0.1, 0.2, 0.3],
            "SBS40c": [0.4, 0.3, 0.2, 0.1],
        }
    ).to_csv(reference_path, sep="\t", index=False)

    def fake_sigprofiler_matrix(variants_df: pd.DataFrame, assembly: str) -> pd.DataFrame:
        assert assembly == "GRCh37"
        sample_name = str(variants_df["donor_id"].iloc[0])
        return pd.DataFrame({sample_name: [5, 4, 3, 2]}, index=rsa.CONTEXT_96[:4])

    captured_signature_db: dict[str, Path] = {}

    def fake_run_assignment(
        *,
        matrix_path: Path,
        signature_database_path: Path,
        output_dir: Path,
        genome_build: str,
        cosmic_version: str,
        exome: bool,
    ) -> None:
        captured_signature_db["path"] = signature_database_path
        db = pd.read_csv(signature_database_path, sep="\t")
        assert db.columns.tolist() == ["Type", "SBS1", "SBS3", "SBS40a", "SBS40b", "SBS40c"]
        activities_dir = output_dir / "Assignment_Solution" / "Activities"
        stats_dir = output_dir / "Assignment_Solution" / "Solution_Stats"
        activities_dir.mkdir(parents=True)
        stats_dir.mkdir(parents=True)
        pd.DataFrame(
            {
                "Samples": ["study_a__breast"],
                "SBS1": [5.0],
                "SBS3": [0.0],
                "SBS40a": [1.0],
                "SBS40b": [2.0],
                "SBS40c": [3.0],
            }
        ).to_csv(activities_dir / "Assignment_Solution_Activities.txt", sep="\t", index=False)
        pd.DataFrame(
            {
                "Sample Names": ["study_a__breast"],
                "Total Mutations": [14],
                "Cosine Similarity": [0.98],
                "L1 Norm": [1.0],
                "L1_Norm_%": ["10%"],
                "L2 Norm": [0.5],
                "L2_Norm_%": ["5%"],
                "KL Divergence": [0.01],
                "Correlation": [0.95],
            }
        ).to_csv(stats_dir / "Assignment_Solution_Samples_Stats.txt", sep="\t", index=False)

    monkeypatch.setattr(rsa, "_sigprofiler_matrix", fake_sigprofiler_matrix)
    monkeypatch.setattr(rsa, "default_signature_database_path", lambda *args, **kwargs: reference_path)
    monkeypatch.setattr(rsa, "run_sigprofiler_assignment", fake_run_assignment)

    out = rsa.build_assignment_table_for_study(
        study_id="study_a",
        mutations_path=mutations_path,
        samples_path=samples_path,
        lookup_path=lookup_path,
        genome_build="GRCh37",
        cosmic_version="3.5",
        exome=True,
        work_dir=tmp_path / "work",
    )

    assert captured_signature_db["path"].exists()
    assert out["study_id"].unique().tolist() == ["study_a"]
    assert out["cancer_type"].unique().tolist() == ["Breast Cancer"]
    assert out["lookup_key"].unique().tolist() == ["breast"]
    assert out["signature"].tolist() == ["SBS1", "SBS3", "SBS40a", "SBS40b", "SBS40c"]
    assert out["exposure"].tolist() == [5.0, 0.0, 1.0, 2.0, 3.0]
    assert out["total_mutations"].unique().tolist() == [14]


def test_build_assignment_table_for_study_per_sample_preserves_sample_ids(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    mutations_path = tmp_path / "mut.feather"
    samples_path = tmp_path / "samples.feather"
    lookup_path = tmp_path / "lookup.tsv"
    reference_path = tmp_path / "reference.tsv"

    pd.DataFrame(
        {
            "sample_id_tumor": ["S1", "S1", "S2"],
            "chromosome": ["chr1", "chr1", "chr1"],
            "start": [101, 202, 303],
            "reference_allele": ["C", "T", "C"],
            "tumor_seq_allele2": ["A", "G", "T"],
        }
    ).to_feather(mutations_path)
    pd.DataFrame(
        {"sample_id": ["S1", "S2"], "cancer_type": ["BRCA", "BRCA"]}
    ).to_feather(samples_path)
    lookup_path.write_text(
        "\n".join(
            [
                "lookup_key\tfigure_cancer_type\tsignature",
                "breast\tBreast-AdenoCA\tSBS1",
                "breast\tBreast-AdenoCA\tSBS5",
            ]
        )
        + "\n"
    )
    pd.DataFrame(
        {
            "Type": rsa.CONTEXT_96[:4],
            "SBS1": [0.1, 0.2, 0.3, 0.4],
            "SBS5": [0.2, 0.2, 0.2, 0.2],
        }
    ).to_csv(reference_path, sep="\t", index=False)

    def fake_sigprofiler_matrix(variants_df: pd.DataFrame, assembly: str) -> pd.DataFrame:
        donors = list(dict.fromkeys(variants_df["donor_id"].tolist()))
        data = {donor: [1, 2, 3, 4] for donor in donors}
        return pd.DataFrame(data, index=rsa.CONTEXT_96[:4])

    def fake_run_assignment(
        *,
        matrix_path: Path,
        signature_database_path: Path,
        output_dir: Path,
        genome_build: str,
        cosmic_version: str,
        exome: bool,
    ) -> None:
        activities_dir = output_dir / "Assignment_Solution" / "Activities"
        stats_dir = output_dir / "Assignment_Solution" / "Solution_Stats"
        activities_dir.mkdir(parents=True)
        stats_dir.mkdir(parents=True)
        pd.DataFrame(
            {
                "Samples": ["S1", "S2"],
                "SBS1": [5.0, 2.0],
                "SBS5": [1.0, 4.0],
            }
        ).to_csv(activities_dir / "Assignment_Solution_Activities.txt", sep="\t", index=False)
        pd.DataFrame(
            {
                "Sample Names": ["S1", "S2"],
                "Total Mutations": [6, 6],
                "Cosine Similarity": [0.98, 0.95],
                "L1 Norm": [1.0, 1.2],
                "L1_Norm_%": ["10%", "12%"],
                "L2 Norm": [0.5, 0.6],
                "L2_Norm_%": ["5%", "6%"],
                "KL Divergence": [0.01, 0.02],
                "Correlation": [0.95, 0.9],
            }
        ).to_csv(stats_dir / "Assignment_Solution_Samples_Stats.txt", sep="\t", index=False)

    monkeypatch.setattr(rsa, "_sigprofiler_matrix", fake_sigprofiler_matrix)
    monkeypatch.setattr(rsa, "default_signature_database_path", lambda *args, **kwargs: reference_path)
    monkeypatch.setattr(rsa, "run_sigprofiler_assignment", fake_run_assignment)

    out = rsa.build_assignment_table_for_study(
        study_id="tcga_mc3",
        mutations_path=mutations_path,
        samples_path=samples_path,
        lookup_path=lookup_path,
        genome_build="GRCh37",
        cosmic_version="3.5",
        exome=True,
        work_dir=tmp_path / "work",
        assignment_unit="sample",
    )

    assert out["sample_name"].tolist() == ["S1", "S1", "S2", "S2"]
    assert out["assignment_unit"].unique().tolist() == ["sample"]
    assert out["cancer_type"].unique().tolist() == ["BRCA"]


def test_build_assignment_table_for_study_filters_lookup_keys(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    mutations_path = tmp_path / "mut.feather"
    samples_path = tmp_path / "samples.feather"
    lookup_path = tmp_path / "lookup.tsv"
    reference_path = tmp_path / "reference.tsv"

    pd.DataFrame(
        {
            "sample_id_tumor": ["B1", "L1"],
            "chromosome": ["chr1", "chr1"],
            "start": [101, 202],
            "reference_allele": ["C", "T"],
            "tumor_seq_allele2": ["A", "G"],
        }
    ).to_feather(mutations_path)
    pd.DataFrame(
        {
            "sample_id": ["B1", "L1"],
            "cancer_type": ["BRCA", "LUAD"],
        }
    ).to_feather(samples_path)
    lookup_path.write_text(
        "\n".join(
            [
                "lookup_key\tfigure_cancer_type\tsignature",
                "breast\tBreast-AdenoCA\tSBS1",
                "lung\tLung-AdenoCA|Lung-SCC\tSBS1",
            ]
        )
        + "\n"
    )
    pd.DataFrame({"Type": rsa.CONTEXT_96[:2], "SBS1": [0.1, 0.2]}).to_csv(reference_path, sep="\t", index=False)

    def fake_sigprofiler_matrix(variants_df: pd.DataFrame, assembly: str) -> pd.DataFrame:
        donors = list(dict.fromkeys(variants_df["donor_id"].tolist()))
        data = {donor: [1, 2] for donor in donors}
        return pd.DataFrame(data, index=rsa.CONTEXT_96[:2])

    def fake_run_assignment(
        *,
        matrix_path: Path,
        signature_database_path: Path,
        output_dir: Path,
        genome_build: str,
        cosmic_version: str,
        exome: bool,
    ) -> None:
        activities_dir = output_dir / "Assignment_Solution" / "Activities"
        stats_dir = output_dir / "Assignment_Solution" / "Solution_Stats"
        activities_dir.mkdir(parents=True)
        stats_dir.mkdir(parents=True)
        pd.DataFrame({"Samples": ["B1"], "SBS1": [5.0]}).to_csv(
            activities_dir / "Assignment_Solution_Activities.txt", sep="\t", index=False
        )
        pd.DataFrame(
            {
                "Sample Names": ["B1"],
                "Total Mutations": [5],
                "Cosine Similarity": [0.9],
                "L1 Norm": [0.1],
                "L1_Norm_%": ["1%"],
                "L2 Norm": [0.1],
                "L2_Norm_%": ["1%"],
                "KL Divergence": [0.01],
                "Correlation": [0.9],
            }
        ).to_csv(stats_dir / "Assignment_Solution_Samples_Stats.txt", sep="\t", index=False)

    monkeypatch.setattr(rsa, "_sigprofiler_matrix", fake_sigprofiler_matrix)
    monkeypatch.setattr(rsa, "default_signature_database_path", lambda *args, **kwargs: reference_path)
    monkeypatch.setattr(rsa, "run_sigprofiler_assignment", fake_run_assignment)

    out = rsa.build_assignment_table_for_study(
        study_id="tcga_mc3",
        mutations_path=mutations_path,
        samples_path=samples_path,
        lookup_path=lookup_path,
        genome_build="GRCh37",
        cosmic_version="3.5",
        exome=True,
        work_dir=tmp_path / "work",
        allowed_lookup_keys={"breast"},
    )

    assert out["lookup_key"].unique().tolist() == ["breast"]
    assert out["cancer_type"].unique().tolist() == ["BRCA"]


def test_prepare_sigprofiler_variants_normalizes_plain_chromosome_labels() -> None:
    mutations = pd.DataFrame(
        {
            "sample_id_tumor": ["S1", "S1", "S1", "S2"],
            "chromosome": ["1", "X", "chr2", "MT"],
            "start": [101, 202, 303, 404],
            "reference_allele": ["C", "T", "G", "A"],
            "tumor_seq_allele2": ["A", "G", "T", "C"],
        }
    )
    samples = pd.DataFrame(
        {
            "sample_id": ["S1", "S2"],
            "cancer_type": ["BRCA", "BRCA"],
        }
    )

    out = rsa.prepare_sigprofiler_variants(
        mutations=mutations,
        samples=samples,
        cancer_type="BRCA",
        sample_name="study__breast",
        assignment_unit="sample",
    )

    assert out["chrom"].tolist() == ["chr1", "chrX", "chr2"]
    assert out["donor_id"].tolist() == ["S1", "S1", "S1"]
