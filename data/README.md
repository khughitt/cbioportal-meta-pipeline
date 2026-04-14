# Data Sources

1. `uniprotkb_hsapiens_protein_lengths.tsv.gz`

Human protein lengths from UniProtKB, limited to "reviewed" proteins.

Retrieved Feb 2025.

- https://www.uniprot.org/uniprotkb?dir=descend&query=(taxonomy_id%3A9606)&sort=length&facets=reviewed%3Atrue
- https://rest.uniprot.org/uniprotkb/stream?compressed=true&download=true&fields=accession%2Creviewed%2Cid%2Cprotein_name%2Cgene_names%2Corganism_name%2Clength&format=tsv&query=%28%28taxonomy_id%3A9606%29%29+AND+%28reviewed%3Atrue%29&sort=length+desc

2. `grch37.tsv`, `grch38.tsv`

GRCh37 / GRCh38 gene metadata from Stephen Turner's annotables package.

Source: https://github.com/stephenturner/annotables

3. `data/bailey2018_table_s1.tsv`

Source: [Comprehensive Characterization of Cancer Driver Genes and Mutations: Cell](https://www.cell.com/cell/fulltext/S0092-8674(18)30237-X) (Table S1)

4. `data/mc3.v0.2.8.PUBLIC.maf.gz`, `data/tcga_case_to_project.tsv`, `data/tcga_tss_to_project.tsv`

Source: [Scalable Open Science Approach for Mutation Calling of Tumor Exomes Using Multiple Genomic Pipelines | NCI Genomic Data Commons](https://gdc.cancer.gov/about-data/publications/mc3-2017)

- `mc3.v0.2.8.PUBLIC.maf.gz` — MC3 pan-cancer PASS-filtered MAF (2.9M variants, 9,104 samples, 32 cancer types).
- `tcga_case_to_project.tsv` — full TCGA submitter_id → project_id mapping (11,428 cases); fetched once from the GDC API (`api.gdc.cancer.gov/cases`).
- `tcga_tss_to_project.tsv` — derived TSS-code → project mapping (730 rows).

5. `data/sanchez_vega_2018_tables_s2.xlsx`, `data/sanchez_vega_2018_tables_s3.xlsx`

Source: [Oncogenic Signaling Pathways in The Cancer Genome Atlas: Cell](https://www.cell.com/cell/fulltext/S0092-8674(18)30359-3)

# Not included (requires auth)

6. GENIE release v19

Source: [AACR Project GENIE Public - syn7222066 - Wiki](https://www.synapse.org/Synapse:syn7222066/wiki/405659)
