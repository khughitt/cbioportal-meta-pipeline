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
  if (is.null(values$`shuffle-seed`)) {
    values$`shuffle-seed` <- "0"
  }
  values$`shuffle-seed` <- as.integer(values$`shuffle-seed`)

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

empty_diagnostics_table <- function() {
  data.frame(
    cancer_type = character(),
    symbol = character(),
    analysis_view = character(),
    status = character(),
    method_used = character(),
    fallback_used = logical(),
    glmm_error = character(),
    reml_error = character(),
    heterogeneity_state = character(),
    high_i2_threshold = numeric(),
    leave_one_out_candidate = logical(),
    k_studies = integer(),
    n_total = integer(),
    y_total = integer(),
    stringsAsFactors = FALSE
  )
}

empty_leave_one_out_table <- function() {
  data.frame(
    cancer_type = character(),
    symbol = character(),
    analysis_view = character(),
    excluded_study_id = character(),
    base_status = character(),
    holdout_status = character(),
    holdout_method_used = character(),
    holdout_k_studies = integer(),
    holdout_n_total = integer(),
    holdout_y_total = integer(),
    holdout_pooled_rate = numeric(),
    holdout_ci_lo = numeric(),
    holdout_ci_hi = numeric(),
    holdout_i2 = numeric(),
    stringsAsFactors = FALSE
  )
}

empty_panel_sensitivity_table <- function() {
  data.frame(
    cancer_type = character(),
    symbol = character(),
    analysis_view = character(),
    sensitivity_name = character(),
    base_status = character(),
    sensitivity_status = character(),
    sensitivity_method_used = character(),
    sensitivity_k_studies = integer(),
    sensitivity_n_total = integer(),
    sensitivity_y_total = integer(),
    sensitivity_pooled_rate = numeric(),
    sensitivity_ci_lo = numeric(),
    sensitivity_ci_hi = numeric(),
    sensitivity_i2 = numeric(),
    dropped_studies = integer(),
    stringsAsFactors = FALSE
  )
}

empty_placebo_table <- function() {
  data.frame(
    cancer_type = character(),
    symbol = character(),
    analysis_view = character(),
    placebo_name = character(),
    base_status = character(),
    placebo_status = character(),
    placebo_method_used = character(),
    placebo_k_studies = integer(),
    placebo_n_total = integer(),
    placebo_y_total = integer(),
    placebo_pooled_rate = numeric(),
    placebo_ci_lo = numeric(),
    placebo_ci_hi = numeric(),
    placebo_i2 = numeric(),
    shuffle_seed = integer(),
    stringsAsFactors = FALSE
  )
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

diagnostic_row <- function(
  cancer_type,
  symbol,
  analysis_view,
  status,
  method_used,
  fallback_used,
  glmm_error,
  reml_error,
  heterogeneity_state,
  leave_one_out_candidate,
  k_studies,
  n_total,
  y_total
) {
  data.frame(
    cancer_type = cancer_type,
    symbol = symbol,
    analysis_view = analysis_view,
    status = status,
    method_used = method_used,
    fallback_used = fallback_used,
    glmm_error = glmm_error,
    reml_error = reml_error,
    heterogeneity_state = heterogeneity_state,
    high_i2_threshold = 75.0,
    leave_one_out_candidate = leave_one_out_candidate,
    k_studies = as.integer(k_studies),
    n_total = as.integer(n_total),
    y_total = as.integer(y_total),
    stringsAsFactors = FALSE
  )
}

fit_glmm_cell <- function(cell_df) {
  rma.glmm(
    measure = "PLO",
    xi = y,
    ni = n,
    mods = ~ panel_class + matched_normal,
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
    mods = ~ panel_class + matched_normal,
    data = esc,
    method = "REML",
    test = "knha"
  )
}

prediction_from_fit <- function(fit) {
  if (isTRUE(fit$int.only) || ncol(fit$X) <= 1L) {
    link_pred <- predict(fit)
    rate_pred <- predict(fit, transf = transf.ilogit)
  } else {
    newmods <- matrix(colMeans(fit$X[, -1, drop = FALSE]), nrow = 1L)
    colnames(newmods) <- colnames(fit$X)[-1]
    link_pred <- predict(fit, newmods = newmods)
    rate_pred <- predict(fit, newmods = newmods, transf = transf.ilogit)
  }

  list(link = link_pred, rate = rate_pred)
}

row_from_fit <- function(fit, cancer_type, symbol, analysis_view, k_studies, n_total, y_total, status) {
  pred <- prediction_from_fit(fit)
  data.frame(
    cancer_type = cancer_type,
    symbol = symbol,
    analysis_view = analysis_view,
    pooled_logit = as.numeric(pred$link$pred[1]),
    pooled_rate = as.numeric(pred$rate$pred[1]),
    pooled_ci_lo = as.numeric(pred$rate$ci.lb[1]),
    pooled_ci_hi = as.numeric(pred$rate$ci.ub[1]),
    tau2 = as.numeric(fit$tau2),
    i2 = as.numeric(fit$I2),
    pi_lo = as.numeric(pred$rate$pi.lb[1]),
    pi_hi = as.numeric(pred$rate$pi.ub[1]),
    k_studies = as.integer(k_studies),
    n_total = as.integer(n_total),
    y_total = as.integer(y_total),
    converged = TRUE,
    status = status,
    stringsAsFactors = FALSE
  )
}

heterogeneity_state_from_row <- function(pooled_row) {
  if (!isTRUE(pooled_row$converged[[1]]) || is.na(pooled_row$i2[[1]])) {
    return("not_evaluable")
  }
  if (pooled_row$i2[[1]] >= 75.0) {
    return("high_i2")
  }
  "not_high_i2"
}

condition_message_or_na <- function(obj) {
  if (!inherits(obj, "try-error")) {
    return(NA_character_)
  }
  condition <- attr(obj, "condition")
  if (!is.null(condition)) {
    return(conditionMessage(condition))
  }
  as.character(obj)
}

analyze_cell <- function(cell_df, analysis_view, force_glmm_failure) {
  cancer_type <- as.character(cell_df$cancer_type[[1]])
  symbol <- as.character(cell_df$symbol[[1]])
  k_studies <- nrow(cell_df)
  n_total <- sum(cell_df$n)
  y_total <- sum(cell_df$y)

  if (k_studies < 3L) {
    pooled <- empty_result_row(cancer_type, symbol, analysis_view, k_studies, n_total, y_total, "skipped_k")
    diagnostics <- diagnostic_row(
      cancer_type,
      symbol,
      analysis_view,
      "skipped_k",
      "not_fit",
      FALSE,
      NA_character_,
      NA_character_,
      "not_evaluable",
      FALSE,
      k_studies,
      n_total,
      y_total
    )
    return(list(pooled = pooled, diagnostics = diagnostics))
  }
  if (n_total < 200L) {
    pooled <- empty_result_row(cancer_type, symbol, analysis_view, k_studies, n_total, y_total, "skipped_n")
    diagnostics <- diagnostic_row(
      cancer_type,
      symbol,
      analysis_view,
      "skipped_n",
      "not_fit",
      FALSE,
      NA_character_,
      NA_character_,
      "not_evaluable",
      FALSE,
      k_studies,
      n_total,
      y_total
    )
    return(list(pooled = pooled, diagnostics = diagnostics))
  }
  if (y_total < 1L) {
    pooled <- empty_result_row(cancer_type, symbol, analysis_view, k_studies, n_total, y_total, "skipped_y")
    diagnostics <- diagnostic_row(
      cancer_type,
      symbol,
      analysis_view,
      "skipped_y",
      "not_fit",
      FALSE,
      NA_character_,
      NA_character_,
      "not_evaluable",
      FALSE,
      k_studies,
      n_total,
      y_total
    )
    return(list(pooled = pooled, diagnostics = diagnostics))
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
    pooled <- row_from_fit(glmm_fit, cancer_type, symbol, analysis_view, k_studies, n_total, y_total, "ok")
    diagnostics <- diagnostic_row(
      cancer_type,
      symbol,
      analysis_view,
      "ok",
      "glmm",
      FALSE,
      NA_character_,
      NA_character_,
      heterogeneity_state_from_row(pooled),
      k_studies >= 4L,
      k_studies,
      n_total,
      y_total
    )
    return(list(pooled = pooled, diagnostics = diagnostics))
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
    pooled <- row_from_fit(
      reml_fit,
      cancer_type,
      symbol,
      analysis_view,
      k_studies,
      n_total,
      y_total,
      "ok"
    )
    diagnostics <- diagnostic_row(
      cancer_type,
      symbol,
      analysis_view,
      "ok",
      "reml_fallback",
      TRUE,
      condition_message_or_na(glmm_fit),
      NA_character_,
      heterogeneity_state_from_row(pooled),
      k_studies >= 4L,
      k_studies,
      n_total,
      y_total
    )
    return(list(pooled = pooled, diagnostics = diagnostics))
  }

  pooled <- empty_result_row(cancer_type, symbol, analysis_view, k_studies, n_total, y_total, "nonconverged")
  diagnostics <- diagnostic_row(
    cancer_type,
    symbol,
    analysis_view,
    "nonconverged",
    "failed",
    FALSE,
    condition_message_or_na(glmm_fit),
    condition_message_or_na(reml_fit),
    "not_evaluable",
    FALSE,
    k_studies,
    n_total,
    y_total
  )
  list(pooled = pooled, diagnostics = diagnostics)
}

build_leave_one_out_rows <- function(cell_df, analysis_view, base_analysis, force_glmm_failure) {
  if (!isTRUE(base_analysis$diagnostics$leave_one_out_candidate[[1]])) {
    return(empty_leave_one_out_table())
  }

  out_rows <- lapply(seq_len(nrow(cell_df)), function(i) {
    excluded_study_id <- as.character(cell_df$study_id[[i]])
    holdout_df <- cell_df[-i, , drop = FALSE]
    holdout_analysis <- analyze_cell(holdout_df, analysis_view, force_glmm_failure)
    holdout_pooled <- holdout_analysis$pooled
    holdout_diag <- holdout_analysis$diagnostics
    data.frame(
      cancer_type = as.character(base_analysis$pooled$cancer_type[[1]]),
      symbol = as.character(base_analysis$pooled$symbol[[1]]),
      analysis_view = analysis_view,
      excluded_study_id = excluded_study_id,
      base_status = as.character(base_analysis$pooled$status[[1]]),
      holdout_status = as.character(holdout_pooled$status[[1]]),
      holdout_method_used = as.character(holdout_diag$method_used[[1]]),
      holdout_k_studies = as.integer(holdout_pooled$k_studies[[1]]),
      holdout_n_total = as.integer(holdout_pooled$n_total[[1]]),
      holdout_y_total = as.integer(holdout_pooled$y_total[[1]]),
      holdout_pooled_rate = as.numeric(holdout_pooled$pooled_rate[[1]]),
      holdout_ci_lo = as.numeric(holdout_pooled$pooled_ci_lo[[1]]),
      holdout_ci_hi = as.numeric(holdout_pooled$pooled_ci_hi[[1]]),
      holdout_i2 = as.numeric(holdout_pooled$i2[[1]]),
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, out_rows)
}

build_panel_sensitivity_rows <- function(cell_df, analysis_view, base_analysis, force_glmm_failure) {
  cancer_type <- as.character(base_analysis$pooled$cancer_type[[1]])
  symbol <- as.character(base_analysis$pooled$symbol[[1]])
  scenarios <- list(
    drop_mc3 = cell_df$panel_class != "MC3",
    drop_genie_tumor_only = !(cell_df$study_id == "genie" & !cell_df$matched_normal)
  )

  out_rows <- lapply(names(scenarios), function(sensitivity_name) {
    mask <- scenarios[[sensitivity_name]]
    sensitivity_df <- cell_df[mask, , drop = FALSE]
    dropped_studies <- nrow(cell_df) - nrow(sensitivity_df)
    sensitivity_analysis <- if (nrow(sensitivity_df) > 0L) {
      analyze_cell(sensitivity_df, analysis_view, force_glmm_failure)
    } else {
      list(
        pooled = empty_result_row(cancer_type, symbol, analysis_view, 0L, 0L, 0L, "skipped_k"),
        diagnostics = diagnostic_row(
          cancer_type,
          symbol,
          analysis_view,
          "skipped_k",
          "not_fit",
          FALSE,
          NA_character_,
          NA_character_,
          "not_evaluable",
          FALSE,
          0L,
          0L,
          0L
        )
      )
    }
    pooled <- sensitivity_analysis$pooled
    diagnostics <- sensitivity_analysis$diagnostics
    data.frame(
      cancer_type = cancer_type,
      symbol = symbol,
      analysis_view = analysis_view,
      sensitivity_name = sensitivity_name,
      base_status = as.character(base_analysis$pooled$status[[1]]),
      sensitivity_status = as.character(pooled$status[[1]]),
      sensitivity_method_used = as.character(diagnostics$method_used[[1]]),
      sensitivity_k_studies = as.integer(pooled$k_studies[[1]]),
      sensitivity_n_total = as.integer(pooled$n_total[[1]]),
      sensitivity_y_total = as.integer(pooled$y_total[[1]]),
      sensitivity_pooled_rate = as.numeric(pooled$pooled_rate[[1]]),
      sensitivity_ci_lo = as.numeric(pooled$pooled_ci_lo[[1]]),
      sensitivity_ci_hi = as.numeric(pooled$pooled_ci_hi[[1]]),
      sensitivity_i2 = as.numeric(pooled$i2[[1]]),
      dropped_studies = as.integer(dropped_studies),
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, out_rows)
}

build_placebo_rows <- function(
  cell_df,
  analysis_view,
  base_analysis,
  force_glmm_failure,
  shuffle_seed
) {
  if (nrow(cell_df) == 0L) {
    return(empty_placebo_table())
  }

  set.seed(shuffle_seed)
  perm <- sample.int(nrow(cell_df))
  if (nrow(cell_df) > 1L && all(perm == seq_len(nrow(cell_df)))) {
    perm <- c(2:nrow(cell_df), 1L)
  }

  placebo_df <- cell_df
  placebo_df$study_id <- cell_df$study_id[perm]
  placebo_df$panel_class <- cell_df$panel_class[perm]
  placebo_df$matched_normal <- cell_df$matched_normal[perm]

  placebo_analysis <- analyze_cell(placebo_df, analysis_view, force_glmm_failure)
  pooled <- placebo_analysis$pooled
  diagnostics <- placebo_analysis$diagnostics
  data.frame(
    cancer_type = as.character(base_analysis$pooled$cancer_type[[1]]),
    symbol = as.character(base_analysis$pooled$symbol[[1]]),
    analysis_view = analysis_view,
    placebo_name = "shuffle_study_labels",
    base_status = as.character(base_analysis$pooled$status[[1]]),
    placebo_status = as.character(pooled$status[[1]]),
    placebo_method_used = as.character(diagnostics$method_used[[1]]),
    placebo_k_studies = as.integer(pooled$k_studies[[1]]),
    placebo_n_total = as.integer(pooled$n_total[[1]]),
    placebo_y_total = as.integer(pooled$y_total[[1]]),
    placebo_pooled_rate = as.numeric(pooled$pooled_rate[[1]]),
    placebo_ci_lo = as.numeric(pooled$pooled_ci_lo[[1]]),
    placebo_ci_hi = as.numeric(pooled$pooled_ci_hi[[1]]),
    placebo_i2 = as.numeric(pooled$i2[[1]]),
    shuffle_seed = as.integer(shuffle_seed),
    stringsAsFactors = FALSE
  )
}

summarize_view <- function(df, analysis_view, y_col, n_col, force_glmm_failure, shuffle_seed) {
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
  analyses <- lapply(
    split_cells,
    analyze_cell,
    analysis_view = analysis_view,
    force_glmm_failure = force_glmm_failure
  )
  pooled_rows <- do.call(rbind, lapply(analyses, `[[`, "pooled"))
  diagnostics_rows <- do.call(rbind, lapply(analyses, `[[`, "diagnostics"))
  leave_one_out_rows <- lapply(
    seq_along(split_cells),
    function(i) build_leave_one_out_rows(split_cells[[i]], analysis_view, analyses[[i]], force_glmm_failure)
  )
  leave_one_out_rows <- Filter(function(df) nrow(df) > 0L, leave_one_out_rows)
  leave_one_out_df <- if (length(leave_one_out_rows) > 0L) {
    do.call(rbind, leave_one_out_rows)
  } else {
    empty_leave_one_out_table()
  }
  panel_sensitivity_rows <- lapply(
    seq_along(split_cells),
    function(i) build_panel_sensitivity_rows(split_cells[[i]], analysis_view, analyses[[i]], force_glmm_failure)
  )
  panel_sensitivity_df <- do.call(rbind, panel_sensitivity_rows)
  placebo_rows <- lapply(
    seq_along(split_cells),
    function(i) build_placebo_rows(split_cells[[i]], analysis_view, analyses[[i]], force_glmm_failure, shuffle_seed)
  )
  placebo_df <- do.call(rbind, placebo_rows)

  list(
    pooled = pooled_rows,
    diagnostics = diagnostics_rows,
    leave_one_out = leave_one_out_df,
    panel_sensitivity = panel_sensitivity_df,
    placebo = placebo_df
  )
}

build_output <- function(df, force_glmm_failure, shuffle_seed) {
  exclusive <- summarize_view(df, "exclusive", "y_exclusive", "n_exclusive", force_glmm_failure, shuffle_seed)
  inclusive <- summarize_view(df, "inclusive", "y_inclusive", "n_inclusive", force_glmm_failure, shuffle_seed)
  out <- rbind(exclusive$pooled, inclusive$pooled)
  view_order <- c("exclusive", "inclusive")
  out <- out[order(out$cancer_type, out$symbol, match(out$analysis_view, view_order)), ]
  rownames(out) <- NULL
  diagnostics <- rbind(exclusive$diagnostics, inclusive$diagnostics)
  diagnostics <- diagnostics[
    order(diagnostics$cancer_type, diagnostics$symbol, match(diagnostics$analysis_view, view_order)),
  ]
  rownames(diagnostics) <- NULL
  leave_one_out_rows <- Filter(function(df) nrow(df) > 0L, list(exclusive$leave_one_out, inclusive$leave_one_out))
  leave_one_out <- if (length(leave_one_out_rows) > 0L) {
    do.call(rbind, leave_one_out_rows)
  } else {
    empty_leave_one_out_table()
  }
  if (nrow(leave_one_out) > 0L) {
    leave_one_out <- leave_one_out[
      order(
        leave_one_out$cancer_type,
        leave_one_out$symbol,
        match(leave_one_out$analysis_view, view_order),
        leave_one_out$excluded_study_id
      ),
    ]
    rownames(leave_one_out) <- NULL
  }
  panel_sensitivity <- rbind(exclusive$panel_sensitivity, inclusive$panel_sensitivity)
  panel_sensitivity <- panel_sensitivity[
    order(
      panel_sensitivity$cancer_type,
      panel_sensitivity$symbol,
      match(panel_sensitivity$analysis_view, view_order),
      panel_sensitivity$sensitivity_name
    ),
  ]
  rownames(panel_sensitivity) <- NULL
  placebo <- rbind(exclusive$placebo, inclusive$placebo)
  placebo <- placebo[
    order(placebo$cancer_type, placebo$symbol, match(placebo$analysis_view, view_order)),
  ]
  rownames(placebo) <- NULL
  list(
    pooled = out,
    diagnostics = diagnostics,
    leave_one_out = leave_one_out,
    panel_sensitivity = panel_sensitivity,
    placebo = placebo
  )
}

main <- function() {
  options <- parse_cli_args(commandArgs(trailingOnly = TRUE))
  input_path <- options$input
  output_path <- options$output

  df <- as.data.frame(arrow::read_feather(input_path))
  validate_input_schema(df)

  out <- build_output(df, isTRUE(options$force_glmm_failure), options$`shuffle-seed`)
  dir.create(dirname(output_path), recursive = TRUE, showWarnings = FALSE)
  arrow::write_feather(out$pooled, output_path)
  if (!is.null(options$`diagnostics-output`)) {
    diagnostics_path <- options$`diagnostics-output`
    dir.create(dirname(diagnostics_path), recursive = TRUE, showWarnings = FALSE)
    arrow::write_feather(out$diagnostics, diagnostics_path)
  }
  if (!is.null(options$`leave-one-out-output`)) {
    leave_one_out_path <- options$`leave-one-out-output`
    dir.create(dirname(leave_one_out_path), recursive = TRUE, showWarnings = FALSE)
    arrow::write_feather(out$leave_one_out, leave_one_out_path)
  }
  if (!is.null(options$`panel-sensitivity-output`)) {
    panel_sensitivity_path <- options$`panel-sensitivity-output`
    dir.create(dirname(panel_sensitivity_path), recursive = TRUE, showWarnings = FALSE)
    arrow::write_feather(out$panel_sensitivity, panel_sensitivity_path)
  }
  if (!is.null(options$`placebo-output`)) {
    placebo_path <- options$`placebo-output`
    dir.create(dirname(placebo_path), recursive = TRUE, showWarnings = FALSE)
    arrow::write_feather(out$placebo, placebo_path)
  }
  message(sprintf("Wrote %d pooled rows to %s", nrow(out$pooled), output_path))
}

tryCatch(
  main(),
  error = function(err) {
    message(conditionMessage(err))
    quit(save = "no", status = 1L)
  }
)
