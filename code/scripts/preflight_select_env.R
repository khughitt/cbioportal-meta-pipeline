# code/scripts/preflight_select_env.R
#
# Rule (0) for the t078 SELECT pipeline. See
# doc/plans/2026-04-25-t078-select-cooccurrence-design.md Section 4.1.
#
# 1. Install CSOgroup/select v1.6.4 from the vendored tarball into the active
#    R library. Idempotent: if already installed at the right version, skip.
# 2. Smoke-test the install by calling select::select() on the package's
#    bundled luad_data with n.permut = 50.
# 3. Verify the result has every column the project's wrapper depends on.
# 4. Write the .preflight_ok token. All other SELECT rules depend on it.
#
# No network fallback. If the tarball is missing, this script aborts with a
# clear error and the entire DAG fails before fan-out.

suppressPackageStartupMessages({
  library(arrow)
})

snek <- snakemake

tarball_path <- snek@input[["tarball"]]
token_path   <- snek@output[["token"]]

stopifnot(file.exists(tarball_path))

target_version <- "1.6.4"

needs_install <- TRUE
if ("select" %in% rownames(installed.packages())) {
  installed_version <- as.character(packageVersion("select"))
  if (installed_version == target_version) {
    needs_install <- FALSE
    message(sprintf("[preflight] select %s already installed; skipping reinstall.",
                    installed_version))
  }
}

if (needs_install) {
  message(sprintf("[preflight] installing select %s from %s ...",
                  target_version, tarball_path))
  install.packages(tarball_path, repos = NULL, type = "source", quiet = TRUE)
  installed_version <- as.character(packageVersion("select"))
  if (installed_version != target_version) {
    stop(sprintf("[preflight] expected select %s, got %s after install.",
                 target_version, installed_version))
  }
}

# Smoke test on bundled luad_data.
suppressPackageStartupMessages({
  library(select)
})

data(luad_data)
M  <- luad_data$gam
sc <- luad_data$samples   # named character vec: names = sample IDs, value = sample.class
ac <- luad_data$alt       # named character vec: names = alteration IDs, value = alteration.class

stopifnot(is.matrix(M) || is.data.frame(M))
stopifnot(!is.null(rownames(M)))
stopifnot(!is.null(colnames(M)))
stopifnot(is.character(sc), !is.null(names(sc)))
stopifnot(is.character(ac), !is.null(names(ac)))

message("[preflight] running select::select on luad_data with n.permut = 50 ...")
res <- select::select(
  M                              = as.matrix(M),
  sample.class                   = sc,
  alteration.class               = ac,
  folder                         = tempfile("select_preflight_"),
  r.seed                         = 0,
  n.cores                        = 1,
  n.permut                       = 50,
  save.intermediate.files        = FALSE,
  randomization.switch.threshold = 30,
  max.memory.size                = 8,
  FDR.cutoff                     = 1.0,
  calculate_FDR                  = FALSE,
  calculate_APC_threshold        = FALSE,  # n.permut=50 is too small for APC
  verbose                        = FALSE
)

required_cols <- c("SFE_1", "SFE_2", "select_score",
                   "wMI_p.value", "ME_p.value", "direction")
missing <- setdiff(required_cols, colnames(res))
if (length(missing) > 0) {
  stop(sprintf("[preflight] select() output missing columns: %s",
               paste(missing, collapse = ", ")))
}

# Verify direction codomain.
allowed_dirs <- c("CO", "ME", "none")
bad_dirs <- setdiff(unique(res$direction), allowed_dirs)
if (length(bad_dirs) > 0) {
  stop(sprintf("[preflight] unexpected direction values: %s",
               paste(bad_dirs, collapse = ", ")))
}

dir.create(dirname(token_path), recursive = TRUE, showWarnings = FALSE)
writeLines(c(
  sprintf("preflight_ok %s", format(Sys.time(), "%Y-%m-%dT%H:%M:%S%z")),
  sprintf("select_version %s", as.character(packageVersion("select"))),
  sprintf("n_pairs_returned %d", nrow(res))
), token_path)

message(sprintf("[preflight] OK -- wrote %s", token_path))
