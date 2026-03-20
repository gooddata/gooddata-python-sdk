# (C) 2026 GoodData Corporation
from __future__ import annotations

import ast
import json
from pathlib import Path

import numpy
import pandas
import pyarrow as pa
import pytest
from gooddata_pandas._arrow_types import TypesMapper
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


def _assert_df_matches(actual_df: pandas.DataFrame, expected_df: pandas.DataFrame) -> None:
    assert actual_df.shape == expected_df.shape
    # Compare values only — storage dtype may differ across types_mapper presets.
    assert actual_df.index.tolist() == expected_df.index.tolist(), (
        f"row index mismatch\n  expected: {expected_df.index.tolist()[:5]}\n  actual:   {actual_df.index.tolist()[:5]}"
    )
    assert actual_df.columns.tolist() == expected_df.columns.tolist(), (
        f"column index mismatch\n  expected: {expected_df.columns.tolist()[:5]}\n  actual:   {actual_df.columns.tolist()[:5]}"
    )
    exp_vals = expected_df.to_numpy(dtype=float, na_value=float("nan"))
    act_vals = actual_df.to_numpy(dtype=float, na_value=float("nan"))
    both_nan = numpy.isnan(exp_vals) & numpy.isnan(act_vals)
    assert (numpy.isclose(exp_vals, act_vals, equal_nan=False) | both_nan).all()


@pytest.mark.parametrize("case_name", _cases())
def test_arrow_converter(case_name: str) -> None:
    """Classic (default) conversion matches the JSON-path ground truth."""
    table, expected_df, meta = _load_case(case_name)
    actual_df = convert_arrow_table_to_dataframe(table)  # types_mapper="classic"

    _assert_df_matches(actual_df, expected_df)
    assert compute_row_totals_indexes(table, meta["dimensions"]) == meta["row_totals_indexes"]


@pytest.mark.parametrize("case_name", _cases())
def test_arrow_converter_arrow_strings(case_name: str) -> None:
    """arrow_strings preset: numeric values identical to classic; string columns use Arrow-backed dtype."""
    table, expected_df, meta = _load_case(case_name)
    actual_df = convert_arrow_table_to_dataframe(table, types_mapper=TypesMapper.ARROW_STRINGS)

    _assert_df_matches(actual_df, expected_df)

    # String index levels must use the Arrow-backed StringDtype.
    idx = actual_df.index
    if isinstance(idx, pandas.MultiIndex):
        for level in idx.levels:
            if level.dtype == object:
                # object dtype means a numeric or non-string level — skip
                continue
            assert isinstance(level.dtype, pandas.StringDtype) and level.dtype.na_value is pandas.NA, (
                f"Expected Arrow-backed StringDtype on index level, got {level.dtype}"
            )
    elif idx.dtype != object:
        assert isinstance(idx.dtype, pandas.StringDtype), (
            f"Expected Arrow-backed StringDtype on flat index, got {idx.dtype}"
        )


def test_arrow_converter_custom_mapping() -> None:
    """CUSTOM preset with an explicit mapping works end-to-end."""
    cases = _cases()
    assert cases, "no fixtures available"
    table, expected_df, _ = _load_case(cases[0])
    mapping = {pa.string(): pandas.StringDtype("pyarrow"), pa.large_string(): pandas.StringDtype("pyarrow")}
    actual_df = convert_arrow_table_to_dataframe(table, types_mapper=TypesMapper.CUSTOM, custom_mapping=mapping)
    _assert_df_matches(actual_df, expected_df)


def test_arrow_converter_custom_mapping_missing() -> None:
    """CUSTOM preset without custom_mapping raises ValueError."""
    cases = _cases()
    assert cases, "no fixtures available"
    table, _, _ = _load_case(cases[0])
    with pytest.raises(ValueError, match="custom_mapping"):
        convert_arrow_table_to_dataframe(table, types_mapper=TypesMapper.CUSTOM)
