# Data

1. `uniprotkb_hsapiens_protein_lengths.tsv.gz`

Human protein lengths from UniProtKB, limited to "reviewed" proteins.

Retrieved Feb 2025.

- https://www.uniprot.org/uniprotkb?dir=descend&query=(taxonomy_id%3A9606)&sort=length&facets=reviewed%3Atrue
- https://rest.uniprot.org/uniprotkb/stream?compressed=true&download=true&fields=accession%2Creviewed%2Cid%2Cprotein_name%2Cgene_names%2Corganism_name%2Clength&format=tsv&query=%28%28taxonomy_id%3A9606%29%29+AND+%28reviewed%3Atrue%29&sort=length+desc

2. `grch37.tsv`, `grch38.tsv`

GRCh37 / GRCh38 gene metadata from Stephen Turner's annotables package.

Source: https://github.com/stephenturner/annotables

