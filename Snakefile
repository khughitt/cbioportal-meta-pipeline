#
# cbioportal / pan-cancer meta-analysis
#
import pathlib

data_dir = pathlib.Path(config['data_dir'])
out_dir = pathlib.Path(config['out_dir'])

ids = config["datasets"]

entities = ['cancer', 'cancer_detailed', 'gene']

rule all:
  input:
    expand(out_dir.joinpath("summary/mut/{entity}_dataset.feather"), entity=entities),
    expand(out_dir.joinpath("summary/mut/{entity}_dataset_ratio.feather"), entity=entities),
    expand(out_dir.joinpath("studies/{id}/mut/cor/cancer.feather"), id=ids),
    expand(out_dir.joinpath("studies/{id}/mut/cor/gene.feather"), id=ids),
    out_dir.joinpath("summary/metadata/samples.feather"),
    out_dir.joinpath("summary/mut/gene_cancer_dataset.feather"),
    out_dir.joinpath("summary/mut/gene_cancer_dataset_ratio.feather"),
    out_dir.joinpath("summary/mut/matrix/gene_patient.feather"),
    out_dir.joinpath("summary/datasets.feather"),
    out_dir.joinpath("summary/summary.html")

rule create_summary_report:
  input:
    out_dir.joinpath("summary/datasets.feather"),
    out_dir.joinpath("summary/mut/cancer_dataset.feather"),
    out_dir.joinpath("summary/mut/gene_dataset_ratio.feather"),
    out_dir.joinpath("summary/mut/gene_cancer_dataset_ratio.feather"),
    out_dir.joinpath("metadata/protein_lengths.feather")
  output:
    out_dir.joinpath("summary/summary.html")
  script:
    "scripts/summary.Rmd"

rule create_dataset_summary_table:
  input:
    expand(out_dir.joinpath("studies/{id}/metadata/dataset.feather"), id=ids)
  output:
    out_dir.joinpath("summary/datasets.feather")
  script:
    "scripts/create_dataset_summary_table.py"

rule create_combined_gene_cancer_freq_table:
  input:
    expand(out_dir.joinpath("studies/{id}/mut/gene_cancer/gene_cancer_dataset.feather"), id=ids),
    out_dir.joinpath("metadata/protein_lengths.feather")
  output:
    out_dir.joinpath("summary/mut/gene_cancer_dataset.feather"),
    out_dir.joinpath("summary/mut/gene_cancer_dataset_ratio.feather"),
  script:
    "scripts/create_combined_gene_cancer_freq_table.py"

rule create_combined_freq_tables:
  input:
    expand(out_dir.joinpath("studies/{id}/mut/{{entity}}/{{entity}}_dataset.feather"), id=ids),
    out_dir.joinpath("metadata/protein_lengths.feather")
  output:
    out_dir.joinpath("summary/mut/{entity}_dataset.feather"),
    out_dir.joinpath("summary/mut/{entity}_dataset_ratio.feather")
  script:
    "scripts/create_combined_freq_tables.py"

rule create_combined_gene_patient_matrix:
  input:
    expand(out_dir.joinpath("studies/{id}/mut/matrix/gene_patient.feather"), id=ids)
  output:
    out_dir.joinpath("summary/mut/matrix/gene_patient.feather"),
  script:
    "scripts/create_combined_gene_patient_matrix.py"

rule create_combined_sample_table:
  input:
    expand(out_dir.joinpath("studies/{id}/metadata/samples.feather"), id=ids)
  output:
    out_dir.joinpath("summary/metadata/samples.feather"),
  script:
    "scripts/create_combined_sample_table.py"

rule create_correlation_matrices:
  input:
    out_dir.joinpath("studies/{id}/mut/matrix/gene_cancer.feather"),
    out_dir.joinpath("studies/{id}/mut/matrix/gene_patient.feather")
  output:
    out_dir.joinpath("studies/{id}/mut/cor/cancer.feather"),
    out_dir.joinpath("studies/{id}/mut/cor/gene.feather")
  script:
    "scripts/create_correlation_matrices.py"

rule create_gene_patient_mutation_count_matrix:
  input:
    out_dir.joinpath("studies/{id}/mut/mut_filtered.feather"),
    out_dir.joinpath("studies/{id}/metadata/samples.feather")
  output:
    out_dir.joinpath("studies/{id}/mut/matrix/gene_patient.feather")
  script:
    "scripts/create_gene_patient_mutation_count_matrix.py"

rule create_gene_cancer_mutation_count_matrix:
  input:
    out_dir.joinpath("studies/{id}/mut/mut_filtered.feather"),
    out_dir.joinpath("studies/{id}/metadata/samples.feather")
  output:
    out_dir.joinpath("studies/{id}/mut/matrix/gene_cancer.feather")
  script:
    "scripts/create_gene_cancer_mutation_count_matrix.py"

rule create_freq_tables:
  input:
    out_dir.joinpath("studies/{id}/mut/mut_filtered.feather"),
    out_dir.joinpath("studies/{id}/metadata/samples.feather")
  output:
    out_dir.joinpath("studies/{id}/mut/cancer/cancer_dataset.feather"),
    out_dir.joinpath("studies/{id}/mut/cancer_detailed/cancer_detailed_dataset.feather"),
    out_dir.joinpath("studies/{id}/mut/gene/gene_dataset.feather"),
    out_dir.joinpath("studies/{id}/mut/gene_cancer/gene_cancer_dataset.feather")
  script:
    "scripts/create_freq_tables.py"

rule create_protein_length_mapping:
  input:
    "data/uniprotkb_hsapiens_protein_lengths.tsv.gz"
  output:
    out_dir.joinpath("metadata/protein_lengths.feather")
  script:
    "scripts/create_protein_length_mapping.py"

rule filter_genes:
  input:
    out_dir.joinpath("studies/{id}/mut/mut.feather"),
    out_dir.joinpath("metadata/gene_counts.feather")
  output:
    out_dir.joinpath("studies/{id}/mut/mut_filtered.feather"),
  script:
    "scripts/filter_genes.py"

rule check_gene_coverage:
  input:
    expand(out_dir.joinpath("studies/{id}/mut/mut.feather"), id=ids),
  output:
    out_dir.joinpath("metadata/gene_counts.feather")
  script:
    "scripts/check_gene_coverage.py"

rule convert_to_feather:
  input:
    data_dir.joinpath("{id}/data_mutations.txt"),
    data_dir.joinpath("{id}/data_clinical_sample.txt"),
    data_dir.joinpath("{id}/data_clinical_patient.txt")
  output:
    out_dir.joinpath("studies/{id}/mut/mut.feather"),
    out_dir.joinpath("studies/{id}/metadata/samples.feather"),
    out_dir.joinpath("studies/{id}/metadata/patients.feather"),
    out_dir.joinpath("studies/{id}/metadata/dataset.feather")
  script:
    "scripts/convert_to_feather.py"

rule download_dataset:
  output:
    data_dir.joinpath("{id}/data_mutations.txt"),
    data_dir.joinpath("{id}/data_clinical_sample.txt"),
    data_dir.joinpath("{id}/data_clinical_patient.txt"),
  script:
    "scripts/download_dataset.py"

# vi:ft=snakemake
