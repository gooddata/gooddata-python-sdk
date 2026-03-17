# (C) 2026 GoodData Corporation
from __future__ import annotations

import ast
import json
from pathlib import Path

import numpy
import pandas
import pyarrow as pa
import pytest
from gooddata_pandas.arrow_convertor import compute_row_totals_indexes, convert_arrow_table_to_dataframe
from pyarrow import ipc

_ARROW_FIXTURES = Path(__file__).parent / "fixtures" / "arrow"


def _cases() -> list[str]:
    manifest_path = _ARROW_FIXTURES / "manifest.json"
    if not manifest_path.exists():
        return []
    return [
        c["name"]
        for c in json.loads(manifest_path.read_text())
        if (_ARROW_FIXTURES / c["name"] / "result.arrow").exists()
    ]


def _load_case(name: str) -> tuple[pa.Table, pandas.DataFrame, dict]:
    """Return (arrow_table, expected_df, meta) for a ground-truth case."""
    case_dir = _ARROW_FIXTURES / name
    with open(case_dir / "result.arrow", "rb") as f:
        table = ipc.open_file(f).read_all()
    expected = pandas.read_parquet(case_dir / "dataframe.parquet")
    # Parquet serialises MultiIndex column tuples as strings — restore them.
    cols = expected.columns
    if not isinstance(cols, pandas.MultiIndex) and len(cols) > 0:
        first = str(cols[0])
        if first.startswith("(") and first.endswith(")"):
            expected.columns = pandas.MultiIndex.from_tuples([ast.literal_eval(c) for c in cols])
    meta = json.loads((case_dir / "meta.json").read_text())
    return table, expected, meta


@pytest.mark.parametrize("case_name", _cases())
def test_arrow_converter(case_name: str) -> None:
    """Convert an Arrow fixture and assert the DataFrame and metadata match the JSON-path ground truth."""
    table, expected_df, meta = _load_case(case_name)
    actual_df = convert_arrow_table_to_dataframe(table)

    assert actual_df.shape == expected_df.shape
    assert actual_df.index.equals(expected_df.index), (
        f"row index mismatch\n  expected: {expected_df.index.tolist()[:5]}\n  actual:   {actual_df.index.tolist()[:5]}"
    )
    assert actual_df.columns.equals(expected_df.columns), (
        f"column index mismatch\n  expected: {expected_df.columns.tolist()[:5]}\n  actual:   {actual_df.columns.tolist()[:5]}"
    )
    exp_vals = expected_df.to_numpy(dtype=float, na_value=float("nan"))
    act_vals = actual_df.to_numpy(dtype=float, na_value=float("nan"))
    both_nan = numpy.isnan(exp_vals) & numpy.isnan(act_vals)
    assert (numpy.isclose(exp_vals, act_vals, equal_nan=False) | both_nan).all()

    assert compute_row_totals_indexes(table, meta["dimensions"]) == meta["row_totals_indexes"]
