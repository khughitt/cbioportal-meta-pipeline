#
# cbioportal / pan-cancer meta-analysis
#
import pathlib

configfile: "config/config.yml"

data_dir = pathlib.Path(config['data_dir'])
out_dir = pathlib.Path(config['out_dir'])

rule create_correlation_matrices:
  input:
    out_dir.joinpath("disease_mutation_count_matrix.feather")
  output:
    out_dir.joinpath("cor/disease.feather"),
    out_dir.joinpath("cor/gene.feather")
  script:
    "scripts/create_correlation_matrices.py"

rule create_disease_mutation_count_matrix:
  input:
    out_dir.joinpath("mut.feather"),
    out_dir.joinpath("mdat.feather")
  output:
    out_dir.joinpath("disease_mutation_count_matrix.feather")
  script:
    "scripts/create_disease_mutation_count_matrix.py"

rule create_freq_tables:
  input:
    out_dir.joinpath("mut.feather"),
    out_dir.joinpath("mdat.feather")
  output:
    out_dir.joinpath("freq/cancer.feather"),
    out_dir.joinpath("freq/cancer_detailed.feather"),
    out_dir.joinpath("freq/gene.feather"),
    out_dir.joinpath("freq/sample_type.feather"),
  script:
    "scripts/create_freq_tables.py"

rule convert_to_feather:
  input:
    data_dir.joinpath("data_mutations_extended.txt"),
    data_dir.joinpath("data_clinical_sample.txt"),
  output:
    out_dir.joinpath("mut.feather"),
    out_dir.joinpath("mdat.feather")
  script:
    "scripts/convert_to_feather.py"

# vi:ft=snakemake

