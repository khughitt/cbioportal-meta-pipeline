# science:code
# status: workflow-owned
# science:end
"""Workflow-visible structural QA for canonical mutation pipeline artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import pandas as pd
from pandas.api.types import is_bool_dtype, is_numeric_dtype


ANALYSIS_VIEWS = {"inclusive", "exclusive"}
PANEL_CLASSES = {"large_hybrid_capture", "small_amplicon", "WES", "MC3"}
POOLED_STATUSES = {"ok", "skipped_k", "skipped_n", "skipped_y", "nonconverged"}
HYPERMUTATOR_REASONS = {
    "pole_hotspot",
    "pold1_hotspot",
    "msi_h",
    "gmm_upper_mode",
    "gmm_upper_mode_below_floor",
    "gmm_lower_mode",
    "zscore_fallback_high",
    "zscore_fallback_low",
    "tmb_unavailable",
}


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    details: str


@dataclass(frozen=True)
class QaReport:
    artifact: str
    checks: list[CheckResult]

    @property
    def failures(self) -> list[str]:
        return [check.name for check in self.checks if not check.passed]

    def raise_for_failures(self) -> None:
        if self.failures:
            raise ValueError("; ".join(self.failures))

    def to_markdown(self) -> str:
        status = "PASS" if not self.failures else "FAIL"
        lines = [
            f"# QA report: {self.artifact}",
            "",
            f"Status: {status}",
            "",
            "| Check | Status | Details |",
            "| --- | --- | --- |",
        ]
        for check in self.checks:
            check_status = "PASS" if check.passed else "FAIL"
            details = check.details.replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {check.name} | {check_status} | {details} |")
        lines.append("")
        return "\n".join(lines)


def validate_per_study_mutation_substrates(
    mutations: pd.DataFrame,
    samples: pd.DataFrame,
) -> QaReport:
    checks = [
        _required_columns(
            mutations,
            {"symbol", "sample_id_tumor", "variant_class", "variant_type"},
            "per-study mutation table schema has required columns",
        ),
        _required_columns(
            samples,
            {"sample_id", "patient_id", "cancer_type"},
            "per-study samples table schema has required columns",
        ),
        _unique(samples, ["sample_id"], "samples table is unique on sample_id"),
        _no_missing_values(
            mutations,
            ["symbol", "sample_id_tumor"],
            "mutation symbols and sample ids are populated",
        ),
        _no_missing_values(
            samples,
            ["sample_id", "patient_id", "cancer_type"],
            "sample ids, patient ids, and cancer types are populated",
        ),
    ]
    if {"sample_id_tumor"}.issubset(mutations.columns) and {"sample_id"}.issubset(
        samples.columns
    ):
        unresolved = set(mutations["sample_id_tumor"].dropna().astype(str)).difference(
            set(samples["sample_id"].dropna().astype(str))
        )
        checks.append(
            CheckResult(
                "mutation sample ids resolve to samples.sample_id",
                not unresolved,
                _sample_details(unresolved),
            )
        )
    return QaReport("per_study_mutation_substrates", checks)


def validate_samples_annotated(samples: pd.DataFrame) -> QaReport:
    required = {
        "study_id",
        "sample_id",
        "cancer_type",
        "tmb",
        "hypermutation_score",
        "is_hypermutator",
        "hypermutator_reason",
        "is_hypermutator_absolute",
        "is_hypermutator_ultra",
        "is_hypermutator_relative",
    }
    checks = [
        _required_columns(
            samples, required, "samples_annotated schema has required columns"
        ),
        _unique(
            samples,
            ["study_id", "sample_id"],
            "samples_annotated is unique on (study_id, sample_id)",
        ),
        _no_missing_values(
            samples,
            ["study_id", "sample_id", "cancer_type"],
            "samples_annotated identifiers are populated",
        ),
        _bool_columns(
            samples,
            [
                "is_hypermutator",
                "is_hypermutator_absolute",
                "is_hypermutator_ultra",
                "is_hypermutator_relative",
            ],
            "hypermutator flags are boolean",
        ),
        _valid_values(
            samples,
            "hypermutator_reason",
            HYPERMUTATOR_REASONS,
            "hypermutator_reason uses canonical vocabulary",
        ),
        _numeric_bounds(
            samples,
            ["tmb", "hypermutation_score"],
            lower=0.0,
            upper=None,
            name="TMB and hypermutation scores are non-negative when present",
        ),
        _numeric_bounds(
            samples,
            ["hypermutation_score"],
            lower=0.0,
            upper=1.0,
            name="hypermutation_score stays in [0, 1]",
        ),
    ]
    return QaReport("samples_annotated", checks)


def validate_gene_cancer_pooled_input(df: pd.DataFrame) -> QaReport:
    count_columns = ["y_inclusive", "y_exclusive", "n_inclusive", "n_exclusive"]
    checks = [
        _required_columns(
            df,
            {
                "study_id",
                "cancer_type",
                "symbol",
                *count_columns,
                "panel_class",
                "matched_normal",
            },
            "gene_cancer_pooled_input schema has required columns",
        ),
        _unique(
            df,
            ["study_id", "cancer_type", "symbol"],
            "pooled input is unique on (study_id, cancer_type, symbol)",
        ),
        _integerish_nonnegative(
            df, count_columns, "pooled input count columns are non-negative integers"
        ),
        _valid_values(
            df, "panel_class", PANEL_CLASSES, "panel_class uses canonical vocabulary"
        ),
        _bool_columns(df, ["matched_normal"], "matched_normal is boolean"),
        _pooled_input_count_contract(df),
    ]
    return QaReport("gene_cancer_pooled_input", checks)


def validate_gene_cancer_pooled_bundle(
    *,
    pooled: pd.DataFrame,
    diagnostics: pd.DataFrame,
    leave_one_out: pd.DataFrame,
    panel_sensitivity: pd.DataFrame,
    placebo: pd.DataFrame,
) -> QaReport:
    required = {
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
        "n_total",
        "y_total",
        "converged",
        "status",
    }
    checks = [
        _required_columns(
            pooled, required, "gene_cancer_pooled schema has required columns"
        ),
        _unique(
            pooled,
            ["cancer_type", "symbol", "analysis_view"],
            "pooled results are unique on (cancer_type, symbol, analysis_view)",
        ),
        _valid_values(
            pooled,
            "analysis_view",
            ANALYSIS_VIEWS,
            "pooled analysis_view uses paired inclusive/exclusive vocabulary",
        ),
        _valid_values(
            pooled, "status", POOLED_STATUSES, "pooled status uses canonical vocabulary"
        ),
        _bool_columns(pooled, ["converged"], "pooled converged flag is boolean"),
        _integerish_nonnegative(
            pooled,
            ["k_studies", "n_total", "y_total"],
            "pooled totals are non-negative integers",
        ),
        _count_le_denominator(
            pooled, "y_total", "n_total", "pooled y_total stays within n_total"
        ),
        _numeric_bounds(
            pooled,
            ["pooled_rate", "pooled_ci_lo", "pooled_ci_hi", "pi_lo", "pi_hi"],
            lower=0.0,
            upper=1.0,
            name="pooled rates and intervals stay in [0, 1]",
        ),
        _diagnostics_contract(diagnostics),
        _sidecar_view_contract(leave_one_out, "leave-one-out sidecar"),
        _sidecar_view_contract(panel_sensitivity, "panel-sensitivity sidecar"),
        _sidecar_view_contract(placebo, "placebo sidecar"),
    ]
    return QaReport("gene_cancer_pooled_bundle", checks)


def validate_gene_cancer_annotated(df: pd.DataFrame, *, ratio_table: bool) -> QaReport:
    required = {
        "cancer_type",
        "symbol",
        "bailey2018_driver",
        "cgc_tier_1",
        "cgc_tier_2",
        "sanchez_vega_pathway",
    }
    if ratio_table:
        required.update(
            {
                "mean_inclusive",
                "mean_exclusive",
                "ch_priority_gene",
                "mean_matched",
                "mean_unmatched",
                "n_matched_studies",
                "n_unmatched_studies",
                "pooled_rate_inclusive",
                "pooled_rate_exclusive",
                "status_inclusive",
                "status_exclusive",
            }
        )
    checks = [
        _required_columns(
            df, required, "gene-cancer annotated schema has required columns"
        ),
        _unique(
            df,
            ["cancer_type", "symbol"],
            "gene-cancer table is unique on (cancer_type, symbol)",
        ),
        _bool_columns(
            df,
            ["bailey2018_driver", "cgc_tier_1", "cgc_tier_2"],
            "driver overlay flags are boolean",
        ),
    ]
    if ratio_table:
        checks.extend(
            [
                _bool_columns(df, ["ch_priority_gene"], "CH priority flag is boolean"),
                _valid_values(
                    df,
                    "status_inclusive",
                    POOLED_STATUSES,
                    "status_inclusive uses canonical vocabulary",
                ),
                _valid_values(
                    df,
                    "status_exclusive",
                    POOLED_STATUSES,
                    "status_exclusive uses canonical vocabulary",
                ),
                _integerish_nonnegative(
                    df,
                    ["n_matched_studies", "n_unmatched_studies"],
                    "matched/unmatched study counts are non-negative integers",
                ),
                _numeric_bounds(
                    df,
                    _ratio_columns(df),
                    lower=0.0,
                    upper=1.0,
                    name="ratio-valued columns stay in [0, 1]",
                ),
            ]
        )
    return QaReport(
        "gene_cancer_study_ratio_annotated"
        if ratio_table
        else "gene_cancer_study_annotated",
        checks,
    )


def _required_columns(df: pd.DataFrame, required: set[str], name: str) -> CheckResult:
    missing = sorted(required.difference(df.columns))
    return CheckResult(
        name=name,
        passed=not missing,
        details="all required columns present"
        if not missing
        else "missing: " + ", ".join(missing),
    )


def _unique(df: pd.DataFrame, columns: list[str], name: str) -> CheckResult:
    missing = [col for col in columns if col not in df.columns]
    if missing:
        return CheckResult(name, False, "missing key columns: " + ", ".join(missing))
    duplicates = int(df.duplicated(columns).sum())
    return CheckResult(name, duplicates == 0, f"duplicate rows: {duplicates}")


def _no_missing_values(df: pd.DataFrame, columns: list[str], name: str) -> CheckResult:
    available = [col for col in columns if col in df.columns]
    missing_columns = sorted(set(columns).difference(available))
    missing_values = int(df[available].isna().sum().sum()) if available else 0
    passed = not missing_columns and missing_values == 0
    details = []
    if missing_columns:
        details.append("missing columns: " + ", ".join(missing_columns))
    details.append(f"missing values: {missing_values}")
    return CheckResult(name, passed, "; ".join(details))


def _valid_values(
    df: pd.DataFrame, column: str, allowed: set[str], name: str
) -> CheckResult:
    if column not in df.columns:
        return CheckResult(name, False, f"missing column: {column}")
    observed = set(df[column].dropna().astype(str))
    unexpected = sorted(observed.difference(allowed))
    return CheckResult(
        name,
        not unexpected,
        "all values valid"
        if not unexpected
        else "unexpected: " + ", ".join(unexpected),
    )


def _bool_columns(df: pd.DataFrame, columns: list[str], name: str) -> CheckResult:
    missing = [col for col in columns if col not in df.columns]
    non_bool = [
        col for col in columns if col in df.columns and not is_bool_dtype(df[col])
    ]
    passed = not missing and not non_bool
    details = []
    if missing:
        details.append("missing: " + ", ".join(missing))
    if non_bool:
        details.append("non-boolean: " + ", ".join(non_bool))
    return CheckResult(name, passed, "; ".join(details) if details else "all boolean")


def _integerish_nonnegative(
    df: pd.DataFrame, columns: list[str], name: str
) -> CheckResult:
    missing = [col for col in columns if col not in df.columns]
    bad: list[str] = []
    for col in columns:
        if col not in df.columns:
            continue
        series = df[col].dropna()
        if not is_numeric_dtype(series):
            bad.append(col)
            continue
        numeric = pd.to_numeric(series)
        if ((numeric < 0) | (numeric % 1 != 0)).any():
            bad.append(col)
    passed = not missing and not bad
    details = []
    if missing:
        details.append("missing: " + ", ".join(missing))
    if bad:
        details.append("invalid: " + ", ".join(bad))
    return CheckResult(
        name, passed, "; ".join(details) if details else "all count columns valid"
    )


def _numeric_bounds(
    df: pd.DataFrame,
    columns: list[str],
    *,
    lower: float | None,
    upper: float | None,
    name: str,
) -> CheckResult:
    if not columns:
        return CheckResult(name, True, "no matching columns")
    missing = [col for col in columns if col not in df.columns]
    invalid: list[str] = []
    for col in columns:
        if col not in df.columns:
            continue
        series = pd.to_numeric(df[col], errors="coerce").dropna()
        if lower is not None and (series < lower).any():
            invalid.append(col)
            continue
        if upper is not None and (series > upper).any():
            invalid.append(col)
    passed = not missing and not invalid
    details = []
    if missing:
        details.append("missing: " + ", ".join(missing))
    if invalid:
        details.append("out of bounds: " + ", ".join(invalid))
    return CheckResult(
        name, passed, "; ".join(details) if details else "all numeric bounds satisfied"
    )


def _pooled_input_count_contract(df: pd.DataFrame) -> CheckResult:
    required = {"y_inclusive", "y_exclusive", "n_inclusive", "n_exclusive"}
    if not required.issubset(df.columns):
        return CheckResult(
            "pooled input counts stay within denominators",
            False,
            "missing columns: " + ", ".join(sorted(required.difference(df.columns))),
        )
    invalid = (
        (df["y_inclusive"] > df["n_inclusive"])
        | (df["y_exclusive"] > df["n_exclusive"])
        | (df["y_exclusive"] > df["y_inclusive"])
        | (df["n_exclusive"] > df["n_inclusive"])
    )
    return CheckResult(
        "pooled input counts stay within denominators",
        not bool(invalid.any()),
        f"invalid rows: {int(invalid.sum())}",
    )


def _count_le_denominator(
    df: pd.DataFrame, count_col: str, denominator_col: str, name: str
) -> CheckResult:
    if count_col not in df.columns or denominator_col not in df.columns:
        missing = sorted({count_col, denominator_col}.difference(df.columns))
        return CheckResult(name, False, "missing: " + ", ".join(missing))
    invalid = (df[count_col] > df[denominator_col]).fillna(False)
    return CheckResult(
        name, not bool(invalid.any()), f"invalid rows: {int(invalid.sum())}"
    )


def _diagnostics_contract(diagnostics: pd.DataFrame) -> CheckResult:
    if diagnostics.empty and not diagnostics.columns.tolist():
        return CheckResult(
            "pooled diagnostics sidecar has expected contract",
            True,
            "empty sidecar not emitted in test",
        )
    required = {
        "cancer_type",
        "symbol",
        "analysis_view",
        "status",
        "method_used",
        "fallback_used",
        "heterogeneity_state",
        "k_studies",
        "n_total",
        "y_total",
    }
    missing = sorted(required.difference(diagnostics.columns))
    if missing:
        return CheckResult(
            "pooled diagnostics sidecar has expected contract",
            False,
            "missing: " + ", ".join(missing),
        )
    checks = [
        _valid_values(diagnostics, "analysis_view", ANALYSIS_VIEWS, "diagnostics view"),
        _valid_values(diagnostics, "status", POOLED_STATUSES, "diagnostics status"),
        _count_le_denominator(diagnostics, "y_total", "n_total", "diagnostics y/n"),
    ]
    failures = [check.name for check in checks if not check.passed]
    return CheckResult(
        "pooled diagnostics sidecar has expected contract",
        not failures,
        "all diagnostics checks passed"
        if not failures
        else "failed: " + ", ".join(failures),
    )


def _sidecar_view_contract(df: pd.DataFrame, label: str) -> CheckResult:
    if df.empty and not df.columns.tolist():
        return CheckResult(
            f"{label} has paired analysis_view values when populated",
            True,
            "empty sidecar",
        )
    if "analysis_view" not in df.columns:
        return CheckResult(
            f"{label} has paired analysis_view values when populated",
            False,
            "missing analysis_view",
        )
    return _valid_values(
        df,
        "analysis_view",
        ANALYSIS_VIEWS,
        f"{label} has paired analysis_view values when populated",
    )


def _ratio_columns(df: pd.DataFrame) -> list[str]:
    prefixes = (
        "mean",
        "pooled_rate",
        "pooled_ci",
        "pi_",
        "callable_fraction",
        "callable_sample_fraction",
    )
    return [
        col
        for col in df.columns
        if isinstance(col, str) and any(col.startswith(prefix) for prefix in prefixes)
    ]


def _sample_details(unresolved: set[str]) -> str:
    if not unresolved:
        return "all mutation sample ids found"
    examples = sorted(unresolved)[:5]
    suffix = "" if len(unresolved) <= 5 else f" (+{len(unresolved) - 5} more)"
    return "unresolved examples: " + ", ".join(examples) + suffix


def _load_feather(path: str | Path) -> pd.DataFrame:
    return pd.read_feather(path)


def _report_for_snakemake(kind: str, inputs: Mapping[str, str]) -> QaReport:
    if kind == "per_study_mutation_substrates":
        return validate_per_study_mutation_substrates(
            _load_feather(inputs["mutations"]),
            _load_feather(inputs["samples"]),
        )
    if kind == "samples_annotated":
        return validate_samples_annotated(_load_feather(inputs["samples_annotated"]))
    if kind == "gene_cancer_pooled_input":
        return validate_gene_cancer_pooled_input(_load_feather(inputs["pooled_input"]))
    if kind == "gene_cancer_pooled_bundle":
        return validate_gene_cancer_pooled_bundle(
            pooled=_load_feather(inputs["pooled"]),
            diagnostics=_load_feather(inputs["diagnostics"]),
            leave_one_out=_load_feather(inputs["leave_one_out"]),
            panel_sensitivity=_load_feather(inputs["panel_sensitivity"]),
            placebo=_load_feather(inputs["placebo"]),
        )
    if kind == "gene_cancer_study_annotated":
        return validate_gene_cancer_annotated(
            _load_feather(inputs["table"]), ratio_table=False
        )
    if kind == "gene_cancer_study_ratio_annotated":
        return validate_gene_cancer_annotated(
            _load_feather(inputs["table"]), ratio_table=True
        )
    raise ValueError(f"Unknown mutation QA artifact kind: {kind}")


def _run_via_snakemake() -> None:
    snek = snakemake  # type: ignore[name-defined]  # noqa: F821
    kind = str(snek.params.artifact_kind)
    inputs = {name: str(value) for name, value in snek.input.items()}
    report = _report_for_snakemake(kind, inputs)
    output_path = Path(snek.output[0])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report.to_markdown())
    report.raise_for_failures()


if "snakemake" in globals():
    _run_via_snakemake()
