#
# cbioportal / pan-cancer meta-analysis
#
import pathlib

configfile: "config/config.yml"

data_dir = pathlib.Path(config['data_dir'])
out_dir = pathlib.Path(config['out_dir'])

ids = config["datasets"]

entities = ['cancer', 'cancer_detailed', 'gene']

rule all:
  input:
    expand(out_dir.joinpath("_summary/freq/{entity}/num.feather"), entity=entities),
    expand(out_dir.joinpath("_summary/freq/{entity}/ratio.feather"), entity=entities),
    expand(out_dir.joinpath("{id}/cor/disease.feather"), id=ids),
    expand(out_dir.joinpath("{id}/cor/gene.feather"), id=ids)

# rule create_combined_gene_cancer_freq_table:
#   input:
#     expand(out_dir.joinpath("{id}/freq/gene_cancer.feather"), id=ids)
#   output:
#     out_dir.joinpath("_summary/freq/gene_cancer/num.feather"),
#     out_dir.joinpath("_summary/freq/gene_cancer/ratio.feather")
#   script:
#     "scripts/create_combined_gene_cancer_freq_table.py"

rule create_combined_freq_tables:
  input:
    expand(out_dir.joinpath("{id}/freq/{{entity}}.feather"), id=ids)
  output:
    out_dir.joinpath("_summary/freq/{entity}/num.feather"),
    out_dir.joinpath("_summary/freq/{entity}/ratio.feather")
  script:
    "scripts/create_combined_freq_tables.py"

rule create_correlation_matrices:
  input:
    out_dir.joinpath("{id}/data/disease_mut.feather")
  output:
    out_dir.joinpath("{id}/cor/disease.feather"),
    out_dir.joinpath("{id}/cor/gene.feather")
  script:
    "scripts/create_correlation_matrices.py"

rule create_disease_mutation_count_matrix:
  input:
    out_dir.joinpath("{id}/data/mut.feather"),
    out_dir.joinpath("{id}/metadata/samples.feather")
  output:
    out_dir.joinpath("{id}/data/disease_mut.feather")
  script:
    "scripts/create_disease_mutation_count_matrix.py"

rule create_freq_tables:
  input:
    out_dir.joinpath("{id}/data/mut.feather"),
    out_dir.joinpath("{id}/metadata/samples.feather")
  output:
    out_dir.joinpath("{id}/freq/cancer.feather"),
    out_dir.joinpath("{id}/freq/cancer_detailed.feather"),
    out_dir.joinpath("{id}/freq/gene.feather"),
    out_dir.joinpath("{id}/freq/gene_cancer.feather")
  script:
    "scripts/create_freq_tables.py"

rule convert_to_feather:
  input:
    data_dir.joinpath("{id}/data_mutations.txt"),
    data_dir.joinpath("{id}/data_clinical_sample.txt"),
  output:
    out_dir.joinpath("{id}/data/mut.feather"),
    out_dir.joinpath("{id}/metadata/samples.feather")
  script:
    "scripts/convert_to_feather.py"

# vi:ft=snakemake
