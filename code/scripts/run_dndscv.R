# science:code
# status: workflow-owned
# science:end
# run_dndscv.R (rewritten for t131)
#
# Runs dNdScv (Martincorena et al. 2017, Cell — github.com/im3sanger/dndscv) on a
# per-cancer-type combined MAF feather and writes per-gene selection results.
#
# Inputs (snakemake@input):
#   maf  — summary/mut/dndscv_input/{slug}/mut_combined.feather
#          schema: sample_id, chr, pos, ref, alt   (lowercase, project convention)
#   meta — summary/mut/dndscv_input/{slug}/cohort_meta.feather
#          one row with: cancer_type, build, n_samples, n_variants, modality,
#          panel_only, below_threshold, ...
#
# Outputs (snakemake@output):
#   genes — summary/mut/dndscv/per_cancer_per_build/{slug}/genes.feather
#           per-gene rows from dndscv$sel_cv plus provenance + cohort columns.
#   run   — summary/mut/dndscv/per_cancer_per_build/{slug}/run.feather
#           single-row run-level summary (status, retention, package_version,
#           git_sha, refdb).
#
# Params (snakemake@params):
#   refdb     — "hg19" or "hg38"  (drives dndscv refdb argument)
#   git_sha   — pinned dndscv commit SHA (passed through to provenance)
#
# Behavior:
#   - On first run inside the conda env, bootstrap dndscv from the pinned SHA via
#     remotes::install_github("im3sanger/dndscv@<sha>"). dndscv is not on
#     conda-forge or Bioconductor.
#   - If cohort_meta$below_threshold is TRUE: skip dndscv invocation and emit
#     empty genes.feather + a run.feather with status = "below_threshold".
#   - On dndscv() failure (too few synonymous mutations, etc.): catch, emit
#     empty genes.feather + run.feather with status = "failed_qc".
#   - On success: write per-gene rows + run.feather with status = "ok"
#     and retention rate (rows accepted by dndscv / rows in input MAF).
#
# Pinned dndscv commit:
#   im3sanger/dndscv @ 69007c2bbd2d6dae003a30dcfe5dda3df722b2f8 (2025-05-15)
#
# This script is invoked by Snakemake with conda env code/envs/dndscv.yml.

DNDSCV_GIT_SHA <- "69007c2bbd2d6dae003a30dcfe5dda3df722b2f8"

bootstrap_dndscv <- function(sha) {
  if (requireNamespace("dndscv", quietly = TRUE)) return(invisible(NULL))
  message("dndscv not present — installing im3sanger/dndscv@", sha,
          " (one-time per conda env, ~5 min)")
  if (!requireNamespace("remotes", quietly = TRUE)) {
    stop("remotes not available; cannot bootstrap dndscv. ",
         "Add r-remotes to code/envs/dndscv.yml.")
  }
  remotes::install_github(
    paste0("im3sanger/dndscv@", sha),
    upgrade = "never",
    quiet = TRUE
  )
  if (!requireNamespace("dndscv", quietly = TRUE)) {
    stop("dndscv install_github reported success but namespace still missing")
  }
}

bootstrap_dndscv(DNDSCV_GIT_SHA)

suppressPackageStartupMessages({
  library(arrow)
  library(dndscv)
})

# --------------------------------------------------------------------------- #
# Inputs / outputs / params.
# --------------------------------------------------------------------------- #
maf_path  <- snakemake@input[["maf"]]
meta_path <- snakemake@input[["meta"]]
genes_out <- snakemake@output[["genes"]]
run_out   <- snakemake@output[["run"]]
refdb     <- snakemake@params[["refdb"]]

stopifnot(refdb %in% c("hg19", "hg38"))

# Reproducibility — dndscv's poilog negative-binomial fits and indel-rate
# estimation can vary run-to-run on borderline cohorts without a fixed seed.
random_seed <- snakemake@config[["random_seed"]]
if (is.null(random_seed)) {
  stop("run_dndscv: config['random_seed'] is required for reproducibility ",
       "(set in code/config/config-pan-cancer-dndscv.yml).")
}
set.seed(as.integer(random_seed))
message(sprintf("run_dndscv: set.seed(%d)", as.integer(random_seed)))

dir.create(dirname(genes_out), recursive = TRUE, showWarnings = FALSE)
dir.create(dirname(run_out),   recursive = TRUE, showWarnings = FALSE)

cohort <- as.data.frame(arrow::read_feather(meta_path))
stopifnot(nrow(cohort) == 1)
cancer_type     <- as.character(cohort$cancer_type[1])
build           <- as.character(cohort$build[1])
modality        <- as.character(cohort$modality[1])
panel_only      <- as.logical(cohort$panel_only[1])
n_samples       <- as.integer(cohort$n_samples[1])
n_variants      <- as.integer(cohort$n_variants[1])
below_threshold <- as.logical(cohort$below_threshold[1])

message(sprintf(
  "run_dndscv: cancer_type=%s build=%s modality=%s n_samples=%d n_variants=%d below_threshold=%s",
  cancer_type, build, modality, n_samples, n_variants, below_threshold
))

# --------------------------------------------------------------------------- #
# Empty-output writer (used by below_threshold and failed_qc paths).
# --------------------------------------------------------------------------- #
write_empty_genes <- function() {
  empty <- data.frame(
    gene_name        = character(0),
    n_syn            = integer(0),
    n_mis            = integer(0),
    n_non            = integer(0),
    n_spl            = integer(0),
    n_ind            = integer(0),
    wmis_cv          = numeric(0),
    wnon_cv          = numeric(0),
    wspl_cv          = numeric(0),
    wind_cv          = numeric(0),
    pmis_cv          = numeric(0),
    ptrunc_cv        = numeric(0),
    pallsubs_cv      = numeric(0),
    pind_cv          = numeric(0),
    qmis_cv          = numeric(0),
    qtrunc_cv        = numeric(0),
    qallsubs_cv      = numeric(0),
    pglobal_cv       = numeric(0),
    qglobal_cv       = numeric(0),
    stringsAsFactors = FALSE
  )
  arrow::write_feather(empty, genes_out)
}

write_run <- function(status, n_input, n_accepted, package_version_str) {
  retention <- if (n_input > 0) n_accepted / n_input else NA_real_
  run_df <- data.frame(
    cancer_type        = cancer_type,
    build              = build,
    refdb              = refdb,
    modality           = modality,
    panel_only         = panel_only,
    n_samples          = n_samples,
    n_variants_input   = n_input,
    n_variants_used    = n_accepted,
    retention_rate     = retention,
    status             = status,
    package_version    = package_version_str,
    git_sha            = DNDSCV_GIT_SHA,
    stringsAsFactors   = FALSE
  )
  arrow::write_feather(run_df, run_out)
}

# --------------------------------------------------------------------------- #
# Below-threshold short-circuit.
# --------------------------------------------------------------------------- #
if (isTRUE(below_threshold)) {
  message("run_dndscv: below_threshold=TRUE — skipping dndscv invocation")
  write_empty_genes()
  write_run("below_threshold", n_variants, 0L, as.character(packageVersion("dndscv")))
  quit(save = "no", status = 0)
}

# --------------------------------------------------------------------------- #
# Load + validate MAF.
# --------------------------------------------------------------------------- #
maf <- as.data.frame(arrow::read_feather(maf_path))
required_cols <- c("sample_id", "chr", "pos", "ref", "alt")
missing <- setdiff(required_cols, colnames(maf))
if (length(missing) > 0) {
  stop("run_dndscv: input MAF missing required columns: ",
       paste(missing, collapse = ", "))
}

# dndscv schema: sampleID, chr, pos, ref, mut.
mut_dnds <- data.frame(
  sampleID = as.character(maf$sample_id),
  chr      = sub("^chr", "", as.character(maf$chr)),
  pos      = as.integer(maf$pos),
  ref      = as.character(maf$ref),
  mut      = as.character(maf$alt),
  stringsAsFactors = FALSE
)

# Drop rows with bad alleles or coords (defensive — prepare_dndscv_input
# already filters, but cheap to repeat).
mut_dnds <- mut_dnds[
  !is.na(mut_dnds$pos) &
  !is.na(mut_dnds$ref) & !is.na(mut_dnds$mut) &
  mut_dnds$ref != "" & mut_dnds$mut != "" &
  mut_dnds$ref != "-" & mut_dnds$mut != "-",
]

n_input <- nrow(maf)
n_accepted <- nrow(mut_dnds)
message(sprintf(
  "run_dndscv: %d / %d MAF rows survived sanity checks (%.1f%%)",
  n_accepted, n_input, 100 * n_accepted / max(n_input, 1)
))

# --------------------------------------------------------------------------- #
# Run dndscv.
# --------------------------------------------------------------------------- #
res <- tryCatch(
  dndscv(
    mut_dnds,
    refdb                          = refdb,
    outmats                        = FALSE,
    max_muts_per_gene_per_sample   = 3,
    max_coding_muts_per_sample     = 3000
  ),
  error = function(e) {
    message("run_dndscv: dndscv() failed: ", conditionMessage(e))
    NULL
  }
)

if (is.null(res) || is.null(res$sel_cv) || nrow(res$sel_cv) == 0) {
  message("run_dndscv: emitting empty genes.feather (failed_qc)")
  write_empty_genes()
  write_run("failed_qc", n_input, n_accepted, as.character(packageVersion("dndscv")))
  quit(save = "no", status = 0)
}

genes <- res$sel_cv
arrow::write_feather(genes, genes_out)
write_run("ok", n_input, n_accepted, as.character(packageVersion("dndscv")))

message(sprintf(
  "run_dndscv: wrote %d gene rows (%s, %s) to %s",
  nrow(genes), cancer_type, build, genes_out
))
