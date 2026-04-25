# code/scripts/run_select_pathway_aggregated.R
#
# Rule (5): pathway x pathway SELECT on the samples x 10 pathway-aggregated GAM.
# Reuses run_select.R's run_one_cell() unchanged -- the pathway GAM has the same
# orientation contract (rows = samples, cols = pathways) and the same
# sample_class / alteration_class shape, so SELECT does not care that the
# columns are pathway names rather than gene symbols.

suppressPackageStartupMessages({
  library(arrow)
  library(jsonlite)
})

# Source run_select.R from the same directory. When invoked via Snakemake's
# `script:` directive the script is wrapped, but `snakemake@scriptdir` is
# available as the original directory.
script_dir <- if (exists("snakemake")) snakemake@scriptdir else dirname(sys.frame(1)$ofile)
source(file.path(script_dir, "run_select.R"), local = FALSE)

if (exists("snakemake")) {
  snek <- snakemake
  run_one_cell(
    cell_dir       = snek@input[["cell_dir"]],
    out_path       = snek@output[["pair_stats"]],
    cell_descriptor = list(
      cancer_type = snek@wildcards[["cancer_type"]],
      tier        = "B",
      study       = NULL,
      cohort      = "exclusive"
    ),
    runtime_config = snek@params[["runtime"]],
    random_seed    = snek@params[["random_seed"]]
  )
}
