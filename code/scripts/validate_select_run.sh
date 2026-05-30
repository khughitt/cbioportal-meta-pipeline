#!/usr/bin/env bash
# science:code
# status: exploratory
# science:end
# validate_select_run.sh
#
# Post-pipeline hook for the t078 SELECT layer. Run this after a full
# `snakemake ... aggregate_select_results` to:
#   1. assert the four headline feathers exist
#   2. run the biological positive-control regression
#      (code/scripts/tests/check_known_biology.py)
#
# Usage:
#   bash code/scripts/validate_select_run.sh                       # uses results/select/
#   bash code/scripts/validate_select_run.sh /path/to/select/dir   # custom dir
#
# Exit code: 0 on success, 1 on missing artefact, 2 on failed positive control.

set -euo pipefail

SELECT_DIR="${1:-results/select}"
HEADLINE="${SELECT_DIR}/gene_pair_select.feather"

if [[ ! -d "${SELECT_DIR}" ]]; then
  echo "[validate] ERROR: SELECT output dir not found: ${SELECT_DIR}" >&2
  exit 1
fi

required_files=(
  "${SELECT_DIR}/gene_pair_select.feather"
  "${SELECT_DIR}/pathway_rollup_gene_pairs.feather"
  "${SELECT_DIR}/gene_cancer_study_select_annotation.feather"
)
for f in "${required_files[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "[validate] ERROR: missing headline output: $f" >&2
    exit 1
  fi
done

echo "[validate] all headline feathers present under ${SELECT_DIR}"
echo "[validate] running biological positive-control regression"

if uv run --frozen python code/scripts/tests/check_known_biology.py "${HEADLINE}"; then
  echo "[validate] positive controls passed"
  exit 0
else
  echo "[validate] positive controls reported failure(s); see output above" >&2
  exit 2
fi
