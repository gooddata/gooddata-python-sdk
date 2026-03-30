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
from gooddata_pandas.arrow_convertor import (
    _compute_primary_labels_from_fields,
    _compute_primary_labels_from_inline,
    compute_primary_labels,
    compute_row_totals_indexes,
    convert_arrow_table_to_dataframe,
)
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


def test_arrow_converter_unknown_types_mapper() -> None:
    """An unrecognised types_mapper value raises ValueError."""
    cases = _cases()
    assert cases, "no fixtures available"
    table, _, _ = _load_case(cases[0])
    with pytest.raises(ValueError, match="Unknown types_mapper"):
        convert_arrow_table_to_dataframe(table, types_mapper=object())  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# compute_primary_labels — ground-truth fixture tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("case_name", _cases())
def test_compute_primary_labels(case_name: str) -> None:
    """compute_primary_labels matches primary_labels stored in meta.json ground truth."""
    table, _, meta = _load_case(case_name)
    primary_from_index, primary_from_cols = compute_primary_labels(table)
    # meta.json stores dict keys as strings (JSON limitation) — convert back to int.
    expected_idx = {int(k): v for k, v in meta["primary_labels_from_index"].items()}
    expected_cols = {int(k): v for k, v in meta["primary_labels_from_columns"].items()}
    assert primary_from_index == expected_idx
    assert primary_from_cols == expected_cols


# ---------------------------------------------------------------------------
# _compute_primary_labels_from_inline — unit tests for non-identity branches
# ---------------------------------------------------------------------------


def test_primary_labels_from_inline_separate_column() -> None:
    """When primaryLabelId != labelId and a separate column exists, it is used."""
    table = pa.table(
        {
            "__row_type": pa.array([0, 0], type=pa.int8()),
            "display_label": pa.array(["New York", "Los Angeles"], type=pa.string()),
            "primary_label": pa.array(["ny", "la"], type=pa.string()),
        }
    )
    xtab_meta = {"labelMetadata": {"l0": {"labelId": "display_label", "primaryLabelId": "primary_label"}}}
    result = _compute_primary_labels_from_inline(
        table,
        label_refs=["l0"],
        label_ref_to_id={"l0": "display_label"},
        xtab_meta=xtab_meta,
    )
    assert result == {0: {"ny": "New York", "la": "Los Angeles"}}


def test_primary_labels_from_inline_fallback_identity() -> None:
    """When the primaryLabelId column is absent, falls back to identity mapping."""
    table = pa.table(
        {
            "__row_type": pa.array([0, 0], type=pa.int8()),
            "display_label": pa.array(["New York", "Los Angeles"], type=pa.string()),
            # no "primary_label" column
        }
    )
    xtab_meta = {"labelMetadata": {"l0": {"labelId": "display_label", "primaryLabelId": "primary_label"}}}
    result = _compute_primary_labels_from_inline(
        table,
        label_refs=["l0"],
        label_ref_to_id={"l0": "display_label"},
        xtab_meta=xtab_meta,
    )
    assert result == {0: {"New York": "New York", "Los Angeles": "Los Angeles"}}


# ---------------------------------------------------------------------------
# _compute_primary_labels_from_fields — non-string skip branch
# ---------------------------------------------------------------------------


def test_primary_labels_from_fields_skips_non_string() -> None:
    """Non-string entries in label_values / primary_label_values are skipped."""
    gdc_data = {
        "type": "metric",
        "index": 0,
        "label_values": [123, "cat"],
        "primary_label_values": [None, "primary_cat"],
    }
    field = pa.field(
        "metric_group_0",
        pa.float64(),
        metadata={b"gdc": json.dumps(gdc_data).encode()},
    )
    result = _compute_primary_labels_from_fields([field], n_col_labels=2)
    # j=0 skipped (123 is not str); j=1 included
    assert result == {1: {"primary_cat": "cat"}}


# ---------------------------------------------------------------------------
# DataFrameFactory.for_arrow_table — unit test (no live server needed)
# ---------------------------------------------------------------------------


def test_for_arrow_table_without_execution_response() -> None:
    """for_arrow_table returns correct DataFrame and empty metadata when no execution_response."""
    from unittest.mock import MagicMock

    from gooddata_pandas.dataframe import DataFrameFactory

    cases = _cases()
    assert cases, "no fixtures available"
    table, expected_df, _ = _load_case(cases[0])

    gdf = DataFrameFactory(MagicMock(), "test_workspace")
    df, metadata = gdf.for_arrow_table(table)

    _assert_df_matches(df, expected_df)
    assert metadata.execution_response is None
    assert metadata.row_totals_indexes == []
    assert metadata.column_totals_indexes == []
