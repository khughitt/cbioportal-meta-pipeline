# run_dndscv.R
#
# Runs dNdScv (Martincorena et al. 2017, Cell — github.com/im3sanger/dndscv) per cancer type
# on a filtered MAF feather, outputting the per-gene selection table as a feather.
#
# Inputs (from snakemake@input):
#   [1] mut_filtered.feather   # long-format MAF subset for one study or one cancer type
# Outputs (from snakemake@output):
#   [1] dndscv_genes.feather   # per-gene wmis / wnon / wspl / wind + p / q values
#
# Dependencies:
#   - R >= 4.0
#   - arrow (CRAN)
#   - dndscv (devtools::install_github("im3sanger/dndscv"))
#   - GenomicRanges, Biostrings (Bioconductor — pulled by dndscv)
#
# Notes:
#   - dNdScv expects the input to have at minimum the columns
#     (sampleID, chr, pos, ref, mut). We map our MAF column names to those.
#   - Uses the bundled GRCh37 RefCDS reference shipped with the dndscv package
#     (data("RefCDS_human_GRCh37.p12")). For GRCh38 cohorts, swap to the GRCh38 RefCDS.
#   - Hypermutators (>3000 coding mutations per sample) are excluded by default.
#   - On panel-restricted data (e.g., MSK-IMPACT 341/410/468 genes), the global background
#     model degrades; results should be flagged as panel-only and treated as exploratory.
#   - This is a parallel signal alongside the project's existing recurrence-based gene-cancer
#     frequency tables, NOT a replacement.

suppressPackageStartupMessages({
  library(arrow)
  library(dndscv)
})

input_path  <- snakemake@input[[1]]
output_path <- snakemake@output[[1]]

mut <- as.data.frame(arrow::read_feather(input_path))

# Map our MAF column conventions -> dndscv's expected schema.
required_cols <- c("Tumor_Sample_Barcode", "Chromosome", "Start_Position",
                   "Reference_Allele", "Tumor_Seq_Allele2")
missing <- setdiff(required_cols, colnames(mut))
if (length(missing) > 0) {
  stop("Missing required columns in input MAF: ", paste(missing, collapse = ", "))
}

mut_dnds <- data.frame(
  sampleID = mut$Tumor_Sample_Barcode,
  chr      = sub("^chr", "", as.character(mut$Chromosome)),
  pos      = as.integer(mut$Start_Position),
  ref      = mut$Reference_Allele,
  mut      = mut$Tumor_Seq_Allele2,
  stringsAsFactors = FALSE
)

# Drop variants without a valid (ref, alt) pair.
mut_dnds <- mut_dnds[!is.na(mut_dnds$ref) & !is.na(mut_dnds$mut) &
                       mut_dnds$ref != "" & mut_dnds$mut != "" &
                       mut_dnds$ref != "-" & mut_dnds$mut != "-", ]

if (nrow(mut_dnds) < 100) {
  warning("Fewer than 100 variants after filtering — dNdScv results unreliable.")
}

# Run dNdScv with default settings (GRCh37 RefCDS bundled with the package).
res <- dndscv(mut_dnds, refdb = "hg19", outmats = FALSE, max_muts_per_gene_per_sample = 3,
              max_coding_muts_per_sample = 3000)

genes <- res$sel_cv
genes$pipeline_version <- as.character(packageVersion("dndscv"))
genes$source           <- "dndscv"

arrow::write_feather(genes, output_path)
message(sprintf("Wrote %d gene rows to %s", nrow(genes), output_path))
