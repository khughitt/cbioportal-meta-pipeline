suppressPackageStartupMessages({
  library(arrow)
  library(metafor)
})

parse_cli_args <- function(args) {
  if (length(args) == 0L) {
    stop("Missing required flags: --input and --output", call. = FALSE)
  }

  values <- list()
  i <- 1L
  while (i <= length(args)) {
    key <- args[[i]]
    if (!startsWith(key, "--")) {
      stop(sprintf("Unexpected argument %s; expected a --flag.", key), call. = FALSE)
    }
    if (key == "--force-glmm-failure") {
      values$force_glmm_failure <- TRUE
      i <- i + 1L
      next
    }
    if (i == length(args)) {
      stop(sprintf("Flag %s requires a value.", key), call. = FALSE)
    }
    value <- args[[i + 1L]]
    values[[substring(key, 3L)]] <- value
    i <- i + 2L
  }

  if (is.null(values$input) || is.null(values$output)) {
    stop("Missing required flags: --input and --output", call. = FALSE)
  }
  if (is.null(values$force_glmm_failure)) {
    values$force_glmm_failure <- FALSE
  }

  values
}

validate_input_schema <- function(df) {
  required_cols <- c(
    "study_id",
    "cancer_type",
    "symbol",
    "y_inclusive",
    "y_exclusive",
    "n_inclusive",
    "n_exclusive",
    "panel_class",
    "matched_normal"
  )
  missing <- setdiff(required_cols, colnames(df))
  if (length(missing) > 0L) {
    stop(
      sprintf(
        "Input feather is missing required columns: %s",
        paste(missing, collapse = ", ")
      ),
      call. = FALSE
    )
  }
}

empty_result_row <- function(cancer_type, symbol, analysis_view, k_studies, n_total, y_total, status) {
  data.frame(
    cancer_type = cancer_type,
    symbol = symbol,
    analysis_view = analysis_view,
    pooled_logit = as.numeric(NA),
    pooled_rate = as.numeric(NA),
    pooled_ci_lo = as.numeric(NA),
    pooled_ci_hi = as.numeric(NA),
    tau2 = as.numeric(NA),
    i2 = as.numeric(NA),
    pi_lo = as.numeric(NA),
    pi_hi = as.numeric(NA),
    k_studies = as.integer(k_studies),
    n_total = as.integer(n_total),
    y_total = as.integer(y_total),
    converged = FALSE,
    status = status,
    stringsAsFactors = FALSE
  )
}

fit_glmm_cell <- function(cell_df) {
  rma.glmm(
    measure = "PLO",
    xi = y,
    ni = n,
    data = cell_df,
    test = "t"
  )
}

fit_reml_fallback <- function(cell_df) {
  esc <- escalc(
    measure = "PLO",
    xi = y,
    ni = n,
    data = cell_df,
    add = 1 / 2,
    to = "only0"
  )
  rma.uni(
    yi,
    vi,
    data = esc,
    method = "REML",
    test = "knha"
  )
}

row_from_fit <- function(fit, cancer_type, symbol, analysis_view, k_studies, n_total, y_total, status) {
  pred <- predict(fit, transf = transf.ilogit)
  data.frame(
    cancer_type = cancer_type,
    symbol = symbol,
    analysis_view = analysis_view,
    pooled_logit = as.numeric(fit$beta[1, 1]),
    pooled_rate = as.numeric(pred$pred[1]),
    pooled_ci_lo = as.numeric(pred$ci.lb[1]),
    pooled_ci_hi = as.numeric(pred$ci.ub[1]),
    tau2 = as.numeric(fit$tau2),
    i2 = as.numeric(fit$I2),
    pi_lo = as.numeric(pred$pi.lb[1]),
    pi_hi = as.numeric(pred$pi.ub[1]),
    k_studies = as.integer(k_studies),
    n_total = as.integer(n_total),
    y_total = as.integer(y_total),
    converged = TRUE,
    status = status,
    stringsAsFactors = FALSE
  )
}

summarize_cell <- function(cell_df, analysis_view, force_glmm_failure) {
  cancer_type <- as.character(cell_df$cancer_type[[1]])
  symbol <- as.character(cell_df$symbol[[1]])
  k_studies <- nrow(cell_df)
  n_total <- sum(cell_df$n)
  y_total <- sum(cell_df$y)

  if (k_studies < 3L) {
    return(empty_result_row(cancer_type, symbol, analysis_view, k_studies, n_total, y_total, "skipped_k"))
  }
  if (n_total < 200L) {
    return(empty_result_row(cancer_type, symbol, analysis_view, k_studies, n_total, y_total, "skipped_n"))
  }
  if (y_total < 1L) {
    return(empty_result_row(cancer_type, symbol, analysis_view, k_studies, n_total, y_total, "skipped_y"))
  }

  glmm_fit <- if (isTRUE(force_glmm_failure)) {
    structure(
      simpleError("Forced GLMM failure for regression coverage."),
      class = c("try-error", "error", "condition")
    )
  } else {
    try(fit_glmm_cell(cell_df), silent = TRUE)
  }
  if (!inherits(glmm_fit, "try-error")) {
    return(row_from_fit(glmm_fit, cancer_type, symbol, analysis_view, k_studies, n_total, y_total, "ok"))
  }

  reml_fit <- try(fit_reml_fallback(cell_df), silent = TRUE)
  if (!inherits(reml_fit, "try-error")) {
    message(
      sprintf(
        "GLMM failed for %s / %s / %s; using REML fallback.",
        cancer_type,
        symbol,
        analysis_view
      )
    )
    return(
      row_from_fit(
        reml_fit,
        cancer_type,
        symbol,
        analysis_view,
        k_studies,
        n_total,
        y_total,
        "ok"
      )
    )
  }

  empty_result_row(cancer_type, symbol, analysis_view, k_studies, n_total, y_total, "nonconverged")
}

summarize_view <- function(df, analysis_view, y_col, n_col, force_glmm_failure) {
  view_df <- data.frame(
    study_id = as.character(df$study_id),
    cancer_type = as.character(df$cancer_type),
    symbol = as.character(df$symbol),
    y = as.integer(df[[y_col]]),
    n = as.integer(df[[n_col]]),
    panel_class = as.character(df$panel_class),
    matched_normal = as.logical(df$matched_normal),
    stringsAsFactors = FALSE
  )

  split_cells <- split(view_df, list(view_df$cancer_type, view_df$symbol), drop = TRUE)
  out_rows <- lapply(
    split_cells,
    summarize_cell,
    analysis_view = analysis_view,
    force_glmm_failure = force_glmm_failure
  )
  do.call(rbind, out_rows)
}

build_output <- function(df, force_glmm_failure) {
  exclusive <- summarize_view(df, "exclusive", "y_exclusive", "n_exclusive", force_glmm_failure)
  inclusive <- summarize_view(df, "inclusive", "y_inclusive", "n_inclusive", force_glmm_failure)
  out <- rbind(exclusive, inclusive)
  view_order <- c("exclusive", "inclusive")
  out <- out[order(out$cancer_type, out$symbol, match(out$analysis_view, view_order)), ]
  rownames(out) <- NULL
  out
}

main <- function() {
  options <- parse_cli_args(commandArgs(trailingOnly = TRUE))
  input_path <- options$input
  output_path <- options$output

  df <- as.data.frame(arrow::read_feather(input_path))
  validate_input_schema(df)

  out <- build_output(df, isTRUE(options$force_glmm_failure))
  dir.create(dirname(output_path), recursive = TRUE, showWarnings = FALSE)
  arrow::write_feather(out, output_path)
  message(sprintf("Wrote %d pooled rows to %s", nrow(out), output_path))
}

tryCatch(
  main(),
  error = function(err) {
    message(conditionMessage(err))
    quit(save = "no", status = 1L)
  }
)
