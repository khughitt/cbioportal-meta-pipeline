#
# cbioportal / pan-cancer meta-analysis
#
import pathlib

data_dir = pathlib.Path(config['data_dir'])
out_dir = pathlib.Path(config['out_dir'])

ids = config["studies"]

entities = ['cancer', 'cancer_detailed', 'gene']

rule all:
  input:
    expand(out_dir.joinpath("summary/mut/table/{entity}_study.feather"), entity=entities),
    expand(out_dir.joinpath("summary/mut/table/{entity}_study_ratio.feather"), entity=entities),
    expand(out_dir.joinpath("studies/{id}/mut/matrix/cancer_cor.feather"), id=ids),
    expand(out_dir.joinpath("studies/{id}/mut/matrix/gene_cor.feather"), id=ids),
    out_dir.joinpath("metadata/samples.feather"),
    out_dir.joinpath("metadata/studies.feather"),
    out_dir.joinpath("summary/mut/table/gene_cancer_study.feather"),
    out_dir.joinpath("summary/mut/table/gene_cancer_study_ratio.feather"),
    out_dir.joinpath("summary/mut/matrix/gene_cancer.feather"),
    out_dir.joinpath("summary/mut/matrix/gene_cancer_ratio.feather"),
    out_dir.joinpath("summary/mut/matrix/gene_patient.feather"),
    out_dir.joinpath("summary/mut/clusters/cancer.feather"),
    out_dir.joinpath("summary/mut/clusters/gene.feather"),
    out_dir.joinpath("summary/summary.html")

rule create_summary_report:
  input:
    out_dir.joinpath("metadata/studies.feather"),
    out_dir.joinpath("metadata/protein_lengths.feather"),
    out_dir.joinpath("summary/mut/table/cancer_study.feather"),
    out_dir.joinpath("summary/mut/table/gene_study.feather"),
    out_dir.joinpath("summary/mut/table/gene_study_ratio.feather"),
    out_dir.joinpath("summary/mut/matrix/gene_cancer.feather"),
    out_dir.joinpath("summary/mut/table/gene_cancer_study.feather"),
    out_dir.joinpath("summary/mut/clusters/cancer.feather"),
    out_dir.joinpath("summary/mut/clusters/gene.feather")
  output:
    out_dir.joinpath("summary/summary.html")
  script:
    "scripts/summary.Rmd"

rule cluster_genes:
  input:
    out_dir.joinpath("summary/mut/matrix/gene_cancer.feather")
  output:
    out_dir.joinpath("summary/mut/clusters/gene.feather")
  script:
    "scripts/cluster_genes.py"

rule cluster_cancer_types:
  input:
    out_dir.joinpath("summary/mut/matrix/gene_cancer.feather")
  output:
    out_dir.joinpath("summary/mut/clusters/cancer.feather")
  script:
    "scripts/cluster_cancer_types.py"

rule create_combined_gene_cancer_mutation_matrices:
  input:
    out_dir.joinpath("summary/mut/table/gene_cancer_study.feather"),
    out_dir.joinpath("summary/mut/table/gene_cancer_study_ratio.feather"),
  output:
    out_dir.joinpath("summary/mut/matrix/gene_cancer.feather"),
    out_dir.joinpath("summary/mut/matrix/gene_cancer_ratio.feather")
  script:
    "scripts/create_combined_gene_cancer_mutation_matrices.py"

rule create_combined_gene_cancer_freq_table:
  input:
    expand(out_dir.joinpath("studies/{id}/mut/table/gene_cancer_study.feather"), id=ids),
    out_dir.joinpath("metadata/protein_lengths.feather")
  output:
    out_dir.joinpath("summary/mut/table/gene_cancer_study.feather"),
    out_dir.joinpath("summary/mut/table/gene_cancer_study_ratio.feather"),
  script:
    "scripts/create_combined_gene_cancer_freq_table.py"

rule create_combined_freq_tables:
  input:
    expand(out_dir.joinpath("studies/{id}/mut/table/{{entity}}_study.feather"), id=ids),
    out_dir.joinpath("metadata/protein_lengths.feather")
  output:
    out_dir.joinpath("summary/mut/table/{entity}_study.feather"),
    out_dir.joinpath("summary/mut/table/{entity}_study_ratio.feather")
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
    out_dir.joinpath("metadata/samples.feather"),
  script:
    "scripts/create_combined_sample_table.py"

rule create_correlation_matrices:
  input:
    out_dir.joinpath("studies/{id}/mut/matrix/gene_cancer.feather"),
    out_dir.joinpath("studies/{id}/mut/matrix/gene_patient.feather")
  output:
    out_dir.joinpath("studies/{id}/mut/matrix/cancer_cor.feather"),
    out_dir.joinpath("studies/{id}/mut/matrix/gene_cor.feather")
  script:
    "scripts/create_correlation_matrices.py"

rule create_gene_patient_mutation_count_matrix:
  input:
    out_dir.joinpath("studies/{id}/mut/table/mut_filtered.feather"),
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
    out_dir.joinpath("studies/{id}/mut/table/mut_filtered.feather"),
    out_dir.joinpath("studies/{id}/metadata/samples.feather")
  output:
    out_dir.joinpath("studies/{id}/mut/table/cancer_study.feather"),
    out_dir.joinpath("studies/{id}/mut/table/cancer_detailed_study.feather"),
    out_dir.joinpath("studies/{id}/mut/table/gene_study.feather"),
    out_dir.joinpath("studies/{id}/mut/table/gene_cancer_study.feather")
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
    out_dir.joinpath("studies/{id}/mut/table/mut.feather"),
    out_dir.joinpath("metadata/gene_counts.feather"),
    out_dir.joinpath("metadata/studies.feather")
  output:
    out_dir.joinpath("studies/{id}/mut/table/mut_filtered.feather"),
  script:
    "scripts/filter_genes.py"

rule check_gene_coverage:
  input:
    expand(out_dir.joinpath("studies/{id}/mut/table/mut.feather"), id=ids),
  output:
    out_dir.joinpath("metadata/gene_counts.feather")
  script:
    "scripts/check_gene_coverage.py"

rule create_study_summary_table:
  input:
    expand(out_dir.joinpath("studies/{id}/metadata/study.feather"), id=ids)
  output:
    out_dir.joinpath("metadata/studies.feather")
  script:
    "scripts/create_study_summary_table.py"

rule convert_to_feather:
  input:
    data_dir.joinpath("{id}/data_mutations.txt"),
    data_dir.joinpath("{id}/data_clinical_sample.txt"),
    data_dir.joinpath("{id}/data_clinical_patient.txt")
  output:
    out_dir.joinpath("studies/{id}/mut/table/mut.feather"),
    out_dir.joinpath("studies/{id}/metadata/samples.feather"),
    out_dir.joinpath("studies/{id}/metadata/patients.feather"),
    out_dir.joinpath("studies/{id}/metadata/study.feather")
  script:
    "scripts/convert_to_feather.py"

rule download_study:
  output:
    data_dir.joinpath("{id}/data_mutations.txt"),
    data_dir.joinpath("{id}/data_clinical_sample.txt"),
    data_dir.joinpath("{id}/data_clinical_patient.txt"),
  script:
    "scripts/download_study.py"

# vi:ft=snakemake
