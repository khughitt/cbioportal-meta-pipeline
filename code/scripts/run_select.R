# code/scripts/run_select.R
#
# Rule (3): per-cell SELECT wrapper.
# Design: doc/plans/2026-04-25-t078-select-cooccurrence-design.md Section 4.5.
#
# Reads one cell's (gam, sample_class, alteration_class, cell_metadata) quad.
# If skip_reason is set, writes a one-row sentinel pair_stats.feather and exits.
# Otherwise calls select::select() with config-knobbed runtime parameters,
# normalises the upstream output schema, and writes pair_stats.feather.
#
# IMPORTANT: GAM input is samples-on-rows, genes-on-columns (design Section 1.2).
# This script does NOT transpose -- passing the GAM through verbatim matches
# select::select()'s expected orientation.

suppressPackageStartupMessages({
  library(arrow)
  library(jsonlite)
})

OUT_COLS <- c(
  "gene_i", "gene_j", "select_score",
  "p_wMI", "p_ME", "direction",
  "n_samples", "n_i_only", "n_j_only", "n_both", "n_neither",
  "cancer_type", "tier", "study", "cohort", "skip_reason"
)


write_sentinel <- function(out_path, cell_descriptor, skip_reason) {
  dir.create(dirname(out_path), recursive = TRUE, showWarnings = FALSE)
  row <- data.frame(
    gene_i = NA_character_, gene_j = NA_character_,
    select_score = NA_real_, p_wMI = NA_real_, p_ME = NA_real_,
    direction = NA_character_,
    n_samples = NA_integer_, n_i_only = NA_integer_, n_j_only = NA_integer_,
    n_both = NA_integer_, n_neither = NA_integer_,
    cancer_type = cell_descriptor$cancer_type,
    tier        = cell_descriptor$tier,
    study       = if (is.null(cell_descriptor$study)) NA_character_
                  else as.character(cell_descriptor$study),
    cohort      = cell_descriptor$cohort,
    skip_reason = skip_reason,
    stringsAsFactors = FALSE
  )
  arrow::write_feather(row, out_path)
}


run_one_cell <- function(cell_dir, out_path, cell_descriptor,
                         runtime_config, random_seed) {
  meta <- jsonlite::read_json(file.path(cell_dir, "cell_metadata.json"))
  skip <- meta$skip_reason
  if (!is.null(skip) && !identical(skip, "null") && nchar(as.character(skip)) > 0) {
    write_sentinel(out_path, cell_descriptor, as.character(skip))
    return(invisible())
  }

  gam_df <- arrow::read_feather(file.path(cell_dir, "gam.feather"))
  sc_df  <- arrow::read_feather(file.path(cell_dir, "sample_class.feather"))
  ac_df  <- arrow::read_feather(file.path(cell_dir, "alteration_class.feather"))

  rownames_vec <- as.character(gam_df$composite_sample_id)
  gam <- as.matrix(gam_df[, setdiff(colnames(gam_df), "composite_sample_id"),
                          drop = FALSE])
  rownames(gam) <- rownames_vec
  storage.mode(gam) <- "logical"

  sample_class_vec <- setNames(as.character(sc_df$sample_class),
                                as.character(sc_df$composite_sample_id))
  alteration_class_vec <- setNames(as.character(ac_df$alteration_class),
                                    as.character(ac_df$symbol))

  stopifnot(identical(rownames(gam), names(sample_class_vec)))
  stopifnot(identical(colnames(gam), names(alteration_class_vec)))

  res <- select::select(
    M                              = gam,
    sample.class                   = sample_class_vec,
    alteration.class               = alteration_class_vec,
    folder                         = tempfile("select_run_"),
    r.seed                         = as.integer(random_seed),
    n.cores                        = as.integer(runtime_config$n_cores),
    n.permut                       = as.integer(runtime_config$n_permut),
    min.feature.support            = as.integer(runtime_config$min_feature_support),
    min.feature.freq               = as.numeric(runtime_config$min_feature_freq),
    remove.0.samples               = TRUE,
    remove.unknown.class.samples   = TRUE,
    rho                            = 0.1,
    lambda                         = 15,
    save.intermediate.files        = isTRUE(runtime_config$save_intermediate_files),
    randomization.switch.threshold = as.integer(runtime_config$randomization_switch_threshold),
    max.memory.size                = as.numeric(runtime_config$max_memory_size_gb),
    FDR.cutoff                     = 1.0,                # we recompute BH per stratum
    calculate_APC_threshold        = TRUE,
    calculate_FDR                  = FALSE,
    verbose                        = FALSE
  )

  # Per-pair contingency from the GAM directly.
  contingency <- function(gi, gj) {
    i <- gam[, gi]
    j <- gam[, gj]
    list(
      n_both    = sum(i & j),
      n_i_only  = sum(i & !j),
      n_j_only  = sum(!i & j),
      n_neither = sum(!i & !j),
      n_samples = length(i)
    )
  }

  out_rows <- vector("list", nrow(res))
  for (k in seq_len(nrow(res))) {
    cont <- contingency(res$SFE_1[k], res$SFE_2[k])
    out_rows[[k]] <- list(
      gene_i       = res$SFE_1[k],
      gene_j       = res$SFE_2[k],
      select_score = res$select_score[k],
      p_wMI        = res$wMI_p.value[k],
      p_ME         = res$ME_p.value[k],
      direction    = res$direction[k],
      n_samples    = cont$n_samples,
      n_i_only     = cont$n_i_only,
      n_j_only     = cont$n_j_only,
      n_both       = cont$n_both,
      n_neither    = cont$n_neither,
      cancer_type  = cell_descriptor$cancer_type,
      tier         = cell_descriptor$tier,
      study        = if (is.null(cell_descriptor$study)) NA_character_
                     else as.character(cell_descriptor$study),
      cohort       = cell_descriptor$cohort,
      skip_reason  = NA_character_
    )
  }
  out_df <- do.call(rbind, lapply(out_rows, as.data.frame, stringsAsFactors = FALSE))

  dir.create(dirname(out_path), recursive = TRUE, showWarnings = FALSE)
  arrow::write_feather(out_df[, OUT_COLS], out_path)
}


# Snakemake entry point.
if (exists("snakemake")) {
  snek <- snakemake
  run_one_cell(
    cell_dir       = snek@input[["cell_dir"]],
    out_path       = snek@output[["pair_stats"]],
    cell_descriptor = list(
      cancer_type = snek@wildcards[["cancer_type"]],
      tier        = snek@wildcards[["tier"]],
      study       = if ("study" %in% names(snek@wildcards))
                    snek@wildcards[["study"]] else NULL,
      cohort      = snek@wildcards[["cohort"]]
    ),
    runtime_config = snek@params[["runtime"]],
    random_seed    = snek@params[["random_seed"]]
  )
}
