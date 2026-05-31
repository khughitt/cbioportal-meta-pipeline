---
id: "dataset:replication-timing-constitutive-regions"
type: "dataset"
title: "Constitutive replication-timing regions (human hg19 / GRCh37)"
status: "active"
source_class: "reference"
source_refs:
  - "paper:Yaacov2023"
related:
  - "question:q003-replication-timing-as-gene-level-mutation-rate-confounder"
  - "question:q009-sbs1-lrr-bias-as-normal-contamination-flag"
created: "2026-04-22"
updated: "2026-04-22"
---

# Constitutive replication-timing regions (human hg19 / GRCh37)

Primary dataset for the first executable `q009` step: public 50 kb human genome bins
annotated as constitutive early (`CE`), constitutive late (`CL`), developmental (`D`), or
unclassified (`N/a`).

## Source

| Source | Paper | DOI | Assembly | Supplementary file URL | SHA256 | Retrieved |
|---|---|---|---|---|---|---|
| dileep2015 | Dileep et al. 2015 *Genome Research* | 10.1101/gr.183699.114 | hg19 / GRCh37 | [Supp-RT-human-50kb-bins.xlsx](https://genome.cshlp.org/content/suppl/2015/05/21/gr.183699.114.DC1/Supp-RT-human-50kb-bins.xlsx) | `bcf18b76e4dee4e7ed32ad6406261f18986ca32e7794f332ff70d4ac013d0e11` | 2026-04-22 |

Supporting references:

- Dileep et al. classify the human genome into constitutive early / constitutive late /
  developmental regions using 21 published human replication-timing data sets, in 50 kb bins.
- The paper explicitly states that these labels are provided as the human supplemental file
  `Supp-RT-human-50kb-bins.xlsx`.
- `question:q009-sbs1-lrr-bias-as-normal-contamination-flag` only needs the **constitutive**
  labels (`CE`, `CL`) for the first panel/WES-feasible gene-level proxy, not the full
  cell-line-specific continuous signals.

## File shape

Observed on 2026-04-22 after loading the public supplement with pandas:

- Rows: `53,213`
- Key columns:
  - `CHR`
  - `Start`
  - `End`
  - `RTlabel`
  - per-cell-line RT signal columns such as `GM12878_seq.RT`, `IMR90`, `HeLaS3`, `K562_seq`
- `RTlabel` counts:
  - `D`: `20,923`
  - `N/a`: `19,884`
  - `CL`: `7,016`
  - `CE`: `5,390`

## Why This Is The Right First Asset

For the current pipeline, the first practical `q009` branch is **gene-level ERR/LRR annotation**
rather than full topography:

- The file is public, stable, and directly linked from the paper supplement.
- It is already on `GRCh37`, matching the project gene-coordinate table at `data/grch37.tsv`
  and the current MC3 / cBioPortal mutation surface.
- It gives a simple first-pass mapping from genes to constitutive early vs late replication,
  which is enough to test the coarse panel/WES question:
  "do SBS1-attributed mutations concentrate more strongly in LRR genes for suspect cohorts?"

## Planned Use

The first consumer should:

1. Stage the spreadsheet into a versioned TSV/feather in `data/`.
2. Keep only `RTlabel in {CE, CL}` for the constitutive branch.
3. Join 50 kb bins to gene coordinates from `data/grch37.tsv`.
4. Emit a gene-level annotation table with at least:
   - `symbol`
   - `chromosome`
   - `start`
   - `end`
   - `rt_constitutive_label`
   - `rt_ce_fraction`
   - `rt_cl_fraction`
   - `rt_assignment_method`

Recommended assignment rule:

- classify a gene as `CE` or `CL` only when the majority of overlapped constitutive-bin span is
  in that class;
- otherwise leave it unresolved / mixed rather than forcing a binary label.

That keeps the panel/WES proxy explicit instead of silently over-calling noisy boundary genes.

## Generated Outputs (2026-04-22)

Rule: `prepare_replication_timing_annotations`

Generated files:

- `data/replication_timing_constitutive_bins.feather`
- `data/gene_replication_timing.feather`
- `data/replication_timing_datapackage.json` from
  `rule package_replication_timing_annotations`

Observed output summary from the first project run:

- constitutive bins: `12,406`
  - `CL`: `7,016`
  - `CE`: `5,390`
- gene-level rows: `66,978`
  - `CE`: `11,394`
  - `CL`: `3,132`
  - `unassigned`: `52,452`

The large `unassigned` fraction is expected at this stage because the current mapping is
deliberately conservative: only genes overlapping constitutive (`CE`/`CL`) bins receive a
label, while genes falling entirely in developmental / unclassified space remain unresolved.

## Not Chosen For The First Step

- **SigProfilerTopography Repli-seq defaults / custom biosamples**
  - useful later for WGS-grade topographic analyses;
  - not the best first dependency for panel/WES `q009`, because the immediate need is a
    gene-level constitutive ERR/LRR map.
- **ENCODE per-biosample Repli-seq tracks**
  - richer, but require an extra choice of biosample and a reduction step to constitutive bins;
  - Dileep 2015 already publishes that reduction as a ready-to-use public supplement.

## Related

- `doc/questions/q003-replication-timing-as-gene-level-mutation-rate-confounder.md`
- `doc/questions/q009-sbs1-lrr-bias-as-normal-contamination-flag.md`
- `doc/papers/Yaacov2023.md`
