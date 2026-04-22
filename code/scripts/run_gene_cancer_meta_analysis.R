suppressPackageStartupMessages({
  library(arrow)
})

parse_cli_args <- function(args) {
  if (length(args) == 0L) {
    stop("Missing required flags: --input and --output", call. = FALSE)
  }
  if ((length(args) %% 2L) != 0L) {
    stop("Arguments must be provided as --flag value pairs.", call. = FALSE)
  }

  values <- list()
  i <- 1L
  while (i <= length(args)) {
    key <- args[[i]]
    value <- args[[i + 1L]]
    if (!startsWith(key, "--")) {
      stop(sprintf("Unexpected argument %s; expected a --flag.", key), call. = FALSE)
    }
    values[[substring(key, 3L)]] <- value
    i <- i + 2L
  }

  if (is.null(values$input) || is.null(values$output)) {
    stop("Missing required flags: --input and --output", call. = FALSE)
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

summarize_view <- function(df, analysis_view, y_col, n_col) {
  view_df <- data.frame(
    cancer_type = as.character(df$cancer_type),
    symbol = as.character(df$symbol),
    y = as.integer(df[[y_col]]),
    n = as.integer(df[[n_col]]),
    stringsAsFactors = FALSE
  )

  totals <- aggregate(cbind(y, n) ~ cancer_type + symbol, data = view_df, FUN = sum)
  k_df <- aggregate(rep(1L, nrow(view_df)) ~ cancer_type + symbol, data = view_df, FUN = length)
  colnames(k_df)[[3L]] <- "k_studies"

  out <- merge(totals, k_df, by = c("cancer_type", "symbol"), sort = FALSE)
  out$analysis_view <- analysis_view
  out$pooled_logit <- as.numeric(NA)
  out$pooled_rate <- ifelse(out$n > 0L, out$y / out$n, as.numeric(NA))
  out$pooled_ci_lo <- as.numeric(NA)
  out$pooled_ci_hi <- as.numeric(NA)
  out$tau2 <- as.numeric(NA)
  out$i2 <- as.numeric(NA)
  out$pi_lo <- as.numeric(NA)
  out$pi_hi <- as.numeric(NA)
  out$converged <- FALSE
  out$status <- "not_fit"

  out <- out[
    ,
    c(
      "cancer_type",
      "symbol",
      "analysis_view",
      "pooled_logit",
      "pooled_rate",
      "pooled_ci_lo",
      "pooled_ci_hi",
      "tau2",
      "i2",
      "pi_lo",
      "pi_hi",
      "k_studies",
      "n",
      "y",
      "converged",
      "status"
    )
  ]
  colnames(out)[colnames(out) == "n"] <- "n_total"
  colnames(out)[colnames(out) == "y"] <- "y_total"
  out
}

build_placeholder_output <- function(df) {
  exclusive <- summarize_view(df, "exclusive", "y_exclusive", "n_exclusive")
  inclusive <- summarize_view(df, "inclusive", "y_inclusive", "n_inclusive")
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

  out <- build_placeholder_output(df)
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
