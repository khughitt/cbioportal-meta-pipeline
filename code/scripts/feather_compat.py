# science:code
# status: library
# science:end
"""Helpers for making heterogeneous cBioPortal clinical tables Feather-safe."""

import pandas as pd


def coerce_mixed_object_columns_to_string(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with mixed-type object columns converted to pandas strings.

    cBioPortal clinical files can contain arbitrary study-specific columns. Pandas may
    infer those as object arrays with mixed Python scalar types, which PyArrow cannot
    always serialize deterministically. Known typed columns are left alone; only object
    columns with multiple non-null scalar type names are normalized.
    """
    out = df.copy()
    object_columns = [column for column in out.columns if out[column].dtype == object]
    for column in object_columns:
        type_names = (
            out[column].dropna().map(lambda value: type(value).__name__).unique()
        )
        if len(type_names) > 1:
            out[column] = out[column].astype("string")
    return out
