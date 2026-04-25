# code/scripts/tests/test_run_select.R
#
# testthat tests for run_select.R sentinel handling and column mapping.
# Run via: Rscript code/scripts/tests/test_run_select.R (inside the SELECT conda env).

suppressPackageStartupMessages({
  library(testthat)
  library(arrow)
  library(jsonlite)
})

# Resolve scripts dir robustly across (a) Rscript test_run_select.R from repo
# root, (b) testthat::test_file("code/scripts/tests/test_run_select.R") from
# repo root, and (c) the snakemake script wrapper. testthat's loader does not
# set sys.frame(1)$ofile, so we fall back to a fixed repo-relative path.
candidate_paths <- c(
  tryCatch(sys.frame(1)$ofile, error = function(e) NA_character_),
  # testthat::test_file() chdirs into the test file's directory, so the bare
  # basename resolves there.
  "test_run_select.R",
  "code/scripts/tests/test_run_select.R"
)
this_file <- NA_character_
for (cand in candidate_paths) {
  if (!is.na(cand) && nzchar(cand) && file.exists(cand)) {
    this_file <- normalizePath(cand)
    break
  }
}
if (is.na(this_file)) {
  stop("test_run_select.R: cannot locate own path for scripts_dir resolution")
}
scripts_dir <- dirname(dirname(this_file))
source(file.path(scripts_dir, "run_select.R"), local = TRUE)

write_sentinel_inputs <- function(dir, skip_reason) {
  dir.create(dir, recursive = TRUE, showWarnings = FALSE)
  arrow::write_feather(
    data.frame(composite_sample_id = character(0)),
    file.path(dir, "gam.feather"))
  arrow::write_feather(
    data.frame(composite_sample_id = character(0), sample_class = character(0)),
    file.path(dir, "sample_class.feather"))
  arrow::write_feather(
    data.frame(symbol = character(0), alteration_class = character(0)),
    file.path(dir, "alteration_class.feather"))
  jsonlite::write_json(
    list(skip_reason = skip_reason, n_samples = 0L, n_genes = 0L,
         panel_intersection_size = 0L),
    path = file.path(dir, "cell_metadata.json"), auto_unbox = TRUE)
}

test_that("sentinel passthrough writes empty pair_stats with skip_reason", {
  td <- tempfile("sel_test_")
  in_dir  <- file.path(td, "in")
  out_dir <- file.path(td, "out")
  write_sentinel_inputs(in_dir, "n_samples_below_threshold")

  run_one_cell(
    cell_dir       = in_dir,
    out_path       = file.path(out_dir, "pair_stats.feather"),
    cell_descriptor = list(
      cancer_type = "luad", tier = "B", study = NA,
      cohort = "inclusive"),
    runtime_config = list(
      n_permut = 50, n_cores = 1, max_memory_size_gb = 8,
      randomization_switch_threshold = 30,
      min_feature_support = 5, min_feature_freq = 0.001,
      save_intermediate_files = FALSE),
    random_seed = 0L)

  out <- arrow::read_feather(file.path(out_dir, "pair_stats.feather"))
  expect_equal(nrow(out), 1)
  expect_equal(out$skip_reason[[1]], "n_samples_below_threshold")
  expect_true(is.na(out$select_score[[1]]))
})

test_that("non-sentinel cell produces the expected output column set", {
  skip_if_not_installed("select")
  td <- tempfile("sel_real_")
  in_dir  <- file.path(td, "in")
  out_dir <- file.path(td, "out")
  dir.create(in_dir, recursive = TRUE)

  set.seed(0)
  n_samples <- 50
  composite_ids <- sprintf("st1|S%02d", seq_len(n_samples))
  m <- matrix(sample(c(FALSE, TRUE), 50 * 5, replace = TRUE, prob = c(0.7, 0.3)),
              nrow = 50, ncol = 5,
              dimnames = list(composite_ids, c("TP53", "KRAS", "EGFR", "BRAF", "MYC")))
  arrow::write_feather(
    data.frame(composite_sample_id = rownames(m), m, check.names = FALSE),
    file.path(in_dir, "gam.feather"))
  arrow::write_feather(
    data.frame(composite_sample_id = composite_ids,
               sample_class = rep("st1", n_samples)),
    file.path(in_dir, "sample_class.feather"))
  arrow::write_feather(
    data.frame(symbol = colnames(m),
               alteration_class = rep("unknown", ncol(m))),
    file.path(in_dir, "alteration_class.feather"))
  jsonlite::write_json(
    list(skip_reason = NULL, n_samples = n_samples, n_genes = ncol(m),
         panel_intersection_size = ncol(m)),
    path = file.path(in_dir, "cell_metadata.json"),
    auto_unbox = TRUE, null = "null")

  run_one_cell(
    cell_dir = in_dir,
    out_path = file.path(out_dir, "pair_stats.feather"),
    cell_descriptor = list(cancer_type = "luad", tier = "B", study = NA,
                           cohort = "inclusive"),
    runtime_config = list(
      n_permut = 50, n_cores = 1, max_memory_size_gb = 8,
      randomization_switch_threshold = 30,
      min_feature_support = 5, min_feature_freq = 0.001,
      save_intermediate_files = FALSE),
    random_seed = 0L)

  out <- arrow::read_feather(file.path(out_dir, "pair_stats.feather"))
  needed_cols <- c("gene_i", "gene_j", "select_score",
                   "p_wMI", "p_ME", "direction",
                   "n_both", "n_i_only", "n_j_only", "n_neither",
                   "cancer_type", "tier", "cohort")
  expect_true(all(needed_cols %in% colnames(out)))
  expect_true(all(out$direction %in% c("CO", "ME", "none")))
})
