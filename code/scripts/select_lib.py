"""Shared helpers for the t078 SELECT pipeline.

Functions are pure (no I/O) so they are easy to unit-test. I/O lives in the
per-rule scripts.
"""

from collections.abc import Sequence

import numpy as np
import pandas as pd
from scipy import stats


def composite_sample_id(study_id: str, sample_id: str) -> str:
    """Build the canonical (study_id, sample_id) composite key.

    Per design Section 1.3: row index of every per-cell GAM is
    "<study_id>|<sample_id>". The pipe is reserved.
    """
    if "|" in study_id or "|" in sample_id:
        raise ValueError(
            f"pipe character is reserved as the composite separator; "
            f"got study_id={study_id!r}, sample_id={sample_id!r}"
        )
    return f"{study_id}|{sample_id}"


def build_sample_class(
    samples: pd.DataFrame,
    components: Sequence[str],
) -> pd.Series:
    """Return a Series indexed by composite_sample_id with compound-label values.

    `components` controls the label assembly (design Section 4.4 / config key
    `select.sample_class_components`). The MVP uses ["study"]; t135 will pass
    ["study", "age_tertile"].
    """
    if "composite_sample_id" not in samples.columns:
        raise KeyError("samples must include composite_sample_id")
    for c in components:
        if c not in samples.columns:
            raise KeyError(f"component column not present in samples: {c!r}")
    parts = [samples[c].astype(str) for c in components]
    label = parts[0]
    for p in parts[1:]:
        label = label.str.cat(p, sep="|")
    return pd.Series(label.to_numpy(), index=samples["composite_sample_id"].to_numpy())


def bh_fdr_within_groups(
    df: pd.DataFrame,
    group_cols: Sequence[str],
    pvalue_col: str,
) -> pd.Series:
    """Benjamini-Hochberg FDR within groups; preserves NaN p-values as NaN q.

    Returns a Series aligned to df's index with the q-values.
    """
    out = pd.Series(np.nan, index=df.index, dtype="float64")
    grouped = df.groupby(list(group_cols), observed=True, sort=False).indices
    for _, idx in grouped.items():
        sub = df.iloc[idx]
        mask = sub[pvalue_col].notna()
        if not mask.any():
            continue
        ps = sub.loc[mask, pvalue_col].to_numpy()
        # BH: q_i = min over j>=i of p_(j) * n / j (after sorting ascending).
        order = np.argsort(ps, kind="stable")
        n = len(ps)
        sorted_ps = ps[order]
        ranks = np.arange(1, n + 1)
        raw = sorted_ps * n / ranks
        # cumulative min from right to left, then clip at 1.
        adj = np.minimum.accumulate(raw[::-1])[::-1]
        adj = np.clip(adj, 0.0, 1.0)
        # restore original order.
        unsorted = np.empty_like(adj)
        unsorted[order] = adj
        # idx is a numpy array of positions into df; restrict to the masked subset.
        idx_arr = np.asarray(idx)
        out.iloc[idx_arr[mask.to_numpy()]] = unsorted
    return out


def signed_stouffer(
    pvalues: np.ndarray,
    signs: np.ndarray,
    weights: np.ndarray,
) -> tuple[float, float, int]:
    """Sign-aware weighted-Z (Stouffer) combination.

    Returns (combined_z, two_sided_p, n_used). NaN p-values are dropped. Per
    design Section 4.6 step 2: opposing signs cancel by design -- the caller
    is responsible for the separate direction-consensus diagnostic.

    Each input p is converted to a two-sided z = qnorm(1 - p/2) and signed
    with the corresponding sign in {-1, 0, +1}; sign==0 contributes a z of 0
    and still consumes weight.
    """
    pvalues = np.asarray(pvalues, dtype=float)
    signs = np.asarray(signs, dtype=float)
    weights = np.asarray(weights, dtype=float)

    mask = ~np.isnan(pvalues)
    n_used = int(mask.sum())
    if n_used == 0:
        return float("nan"), float("nan"), 0

    p = pvalues[mask]
    s = signs[mask]
    w = weights[mask]

    # Two-sided z. Clamp p to avoid inf at p == 0 / 1.
    p = np.clip(p, 1e-300, 1.0 - 1e-15)
    z_unsigned = stats.norm.isf(p / 2.0)
    z_signed = s * z_unsigned

    z_combined = float(np.sum(w * z_signed) / np.sqrt(np.sum(w * w)))
    p_combined = float(2.0 * stats.norm.sf(abs(z_combined)))
    return z_combined, p_combined, n_used


def direction_consensus_frac(directions: Sequence[str]) -> float:
    """Fraction of contributing studies that agreed on the dominant non-'none' direction.

    Returns NaN when no study reports a CO/ME direction.
    """
    items = [d for d in directions if d in ("CO", "ME")]
    if not items:
        return float("nan")
    n_co = items.count("CO")
    n_me = items.count("ME")
    return max(n_co, n_me) / len(items)
