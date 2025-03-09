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
    expand(out_dir.joinpath("summary/freq/{entity}/num.feather"), entity=entities),
    expand(out_dir.joinpath("summary/freq/{entity}/ratio.feather"), entity=entities),
    expand(out_dir.joinpath("studies/{id}/cor/disease.feather"), id=ids),
    expand(out_dir.joinpath("studies/{id}/cor/gene.feather"), id=ids),
    out_dir.joinpath("summary/freq/gene_cancer/num.feather"),
    out_dir.joinpath("summary/freq/gene_cancer/ratio.feather"),
    out_dir.joinpath("summary/datasets.feather"),
    out_dir.joinpath("summary/summary.html")

rule create_summary_report:
  input:
    out_dir.joinpath("summary/datasets.feather"),
    out_dir.joinpath("summary/freq/cancer/num.feather"),
    out_dir.joinpath("summary/freq/gene/ratio.feather"),
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
    expand(out_dir.joinpath("studies/{id}/freq/gene_cancer.feather"), id=ids)
  output:
    out_dir.joinpath("summary/freq/gene_cancer/num.feather"),
    out_dir.joinpath("summary/freq/gene_cancer/ratio.feather")
  script:
    "scripts/create_combined_gene_cancer_freq_table.py"

rule create_combined_freq_tables:
  input:
    expand(out_dir.joinpath("studies/{id}/freq/{{entity}}.feather"), id=ids),
    out_dir.joinpath("metadata/protein_lengths.feather")
  output:
    out_dir.joinpath("summary/freq/{entity}/num.feather"),
    out_dir.joinpath("summary/freq/{entity}/ratio.feather")
  script:
    "scripts/create_combined_freq_tables.py"

rule create_correlation_matrices:
  input:
    out_dir.joinpath("studies/{id}/data/disease_mut.feather"),
    out_dir.joinpath("studies/{id}/data/patient_mut.feather")
  output:
    out_dir.joinpath("studies/{id}/cor/disease.feather"),
    out_dir.joinpath("studies/{id}/cor/gene.feather")
  script:
    "scripts/create_correlation_matrices.py"

rule create_patient_mutation_count_matrix:
  input:
    out_dir.joinpath("studies/{id}/data/mut.feather"),
    out_dir.joinpath("studies/{id}/metadata/samples.feather")
  output:
    out_dir.joinpath("studies/{id}/data/patient_mut.feather")
  script:
    "scripts/create_patient_mutation_count_matrix.py"

rule create_disease_mutation_count_matrix:
  input:
    out_dir.joinpath("studies/{id}/data/mut.feather"),
    out_dir.joinpath("studies/{id}/metadata/samples.feather")
  output:
    out_dir.joinpath("studies/{id}/data/disease_mut.feather")
  script:
    "scripts/create_disease_mutation_count_matrix.py"

rule create_freq_tables:
  input:
    out_dir.joinpath("studies/{id}/data/mut.feather"),
    out_dir.joinpath("studies/{id}/metadata/samples.feather")
  output:
    out_dir.joinpath("studies/{id}/freq/cancer.feather"),
    out_dir.joinpath("studies/{id}/freq/cancer_detailed.feather"),
    out_dir.joinpath("studies/{id}/freq/gene.feather"),
    out_dir.joinpath("studies/{id}/freq/gene_cancer.feather")
  script:
    "scripts/create_freq_tables.py"

rule create_protein_length_mapping:
  input:
    "data/uniprotkb_hsapiens_protein_lengths.tsv.gz"
  output:
    out_dir.joinpath("metadata/protein_lengths.feather")
  script:
    "scripts/create_protein_length_mapping.py"

rule convert_to_feather:
  input:
    data_dir.joinpath("{id}/data_mutations.txt"),
    data_dir.joinpath("{id}/data_clinical_sample.txt"),
    data_dir.joinpath("{id}/data_clinical_patient.txt")
  output:
    out_dir.joinpath("studies/{id}/data/mut.feather"),
    out_dir.joinpath("studies/{id}/metadata/samples.feather"),
    out_dir.joinpath("studies/{id}/metadata/patients.feather"),
    out_dir.joinpath("studies/{id}/metadata/dataset.feather")
  script:
    "scripts/convert_to_feather.py"

rule download_dataset:
  output:
    data_dir.joinpath("{id}/data_mutations.txt"),
    data_dir.joinpath("{id}/data_clinical_sample.txt"),
  script:
    "scripts/download_dataset.py"

# vi:ft=snakemake
