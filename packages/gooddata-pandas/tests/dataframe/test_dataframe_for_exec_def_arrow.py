# (C) 2026 GoodData Corporation
from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from unittest.mock import MagicMock

import numpy
import pandas
import pyarrow as pa
import pytest
from gooddata_pandas.arrow_convertor import (
    _build_field_index,
    _build_inline_index,
    _compute_primary_labels_from_fields,
    _compute_primary_labels_from_inline,
    compute_primary_labels,
    compute_row_totals_indexes,
    convert_arrow_table_to_dataframe,
)
from gooddata_pandas.arrow_types import TypesMapper
from gooddata_pandas.dataframe import DataFrameFactory
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


_FOR_ARROW_TABLE_CASES = [
    pytest.param("dim_r_m", id="no-totals-flat"),
    pytest.param("dim_m_c", id="transposed"),
    pytest.param("tot_d0_sub_grand", id="row-subtotals"),
    pytest.param("totals_both_dims", id="both-dims-totals"),
]


@pytest.mark.parametrize("case_name", _FOR_ARROW_TABLE_CASES)
def test_for_arrow_table_without_execution_response(case_name: str) -> None:
    """for_arrow_table with no execution_response: DataFrame matches, metadata is empty."""
    if case_name not in _cases():
        pytest.skip(f"fixture {case_name!r} not available")
    table, expected_df, _ = _load_case(case_name)
    gdf = DataFrameFactory(MagicMock(), "test_workspace")
    df, metadata = gdf.for_arrow_table(table)
    _assert_df_matches(df, expected_df)
    assert metadata.execution_response is None
    assert metadata.row_totals_indexes == []
    assert metadata.column_totals_indexes == []


@pytest.mark.parametrize("case_name", _FOR_ARROW_TABLE_CASES)
def test_for_arrow_table_with_execution_response(case_name: str) -> None:
    """for_arrow_table with execution_response populates row_totals_indexes from meta.json."""
    if case_name not in _cases():
        pytest.skip(f"fixture {case_name!r} not available")
    table, expected_df, meta = _load_case(case_name)
    mock_exec_response = MagicMock()
    mock_exec_response.dimensions = meta["dimensions"]
    gdf = DataFrameFactory(MagicMock(), "test_workspace")
    df, metadata = gdf.for_arrow_table(table, execution_response=mock_exec_response)
    _assert_df_matches(df, expected_df)
    assert metadata.execution_response is mock_exec_response
    assert metadata.row_totals_indexes == meta["row_totals_indexes"]
    assert metadata.column_totals_indexes == []


def test_build_inline_index_total_row_no_totals_meta() -> None:
    """Total rows with absent totalsMetadata hit the 'if not refs: continue' branch."""
    table = pa.table(
        {
            "__row_type": pa.array([0, 2], type=pa.int8()),
            "region": pa.array(["West", "sum"], type=pa.string()),
        }
    )
    xtab_meta = {
        "labelMetadata": {"l0": {"labelId": "region", "primaryLabelId": "region"}},
        # intentionally no "totalsMetadata"
    }
    model_meta = {
        "labels": {"region": {"labelTitle": "Region"}},
        "requestedShape": {"metrics": []},
    }
    idx = _build_inline_index(
        table,
        row_label_refs=["l0"],
        label_ref_to_id={"l0": "region"},
        model_meta=model_meta,
        xtab_meta=xtab_meta,
    )
    assert idx is not None
    # Total row: no agg info available → value is uppercased as-is
    assert idx.tolist() == ["West", "SUM"]
    assert idx.name == "Region"


def test_compute_row_totals_measure_in_row_dim() -> None:
    """measureGroupHeaders entry inside the non-transposed row_dim appends []."""
    table, _, _ = _load_case("dim_r_m")
    # Inject a dimension that also contains a measureGroupHeaders entry
    custom_dims = [
        {
            "headers": [
                {"attributeHeader": {"label": {"id": "region"}, "localIdentifier": "region"}},
                {"measureGroupHeaders": [{"localIdentifier": "price"}]},
            ]
        }
    ]
    result = compute_row_totals_indexes(table, custom_dims)
    # dim_r_m has no total rows → total_row_idxs=[] for the attr level;
    assert result == [[], []]


def test_compute_row_totals_unknown_attr_in_row_dim() -> None:
    """Unknown attributeHeader in the non-transposed row_dim appends []."""
    table, _, _ = _load_case("dim_r_m")
    custom_dims = [
        {
            "headers": [
                {"attributeHeader": {"label": {"id": "region"}, "localIdentifier": "region"}},
                {"attributeHeader": {"label": {"id": "unknown_attr"}, "localIdentifier": "unknown"}},
            ]
        }
    ]
    result = compute_row_totals_indexes(table, custom_dims)
    assert result == [[], []]


def test_compute_row_totals_field_rows_unknown_attr() -> None:
    """Unknown attributeHeader in the field-rows row_dim appends []."""
    table, _, _ = _load_case("dim_m_c")
    # dim_m_c: transposed, col_label_refs=[] → metrics-only, row_dim found by measureGroupHeaders
    custom_dims = [
        {
            "headers": [
                {"measureGroupHeaders": [{"localIdentifier": "m0"}]},
                {"attributeHeader": {"label": {"id": "unknown_attr"}, "localIdentifier": "unknown"}},
            ]
        },
        {
            "headers": [
                {"attributeHeader": {"label": {"id": "products.category"}, "localIdentifier": "category"}},
            ]
        },
    ]
    result = compute_row_totals_indexes(table, custom_dims)
    assert result == [[], []]


def test_convert_arrow_no_schema_metadata_raises() -> None:
    """Arrow table without any schema metadata raises ValueError with a clear message."""
    table = pa.table({"col": [1, 2, 3]})
    assert table.schema.metadata is None
    with pytest.raises(ValueError, match="no schema metadata"):
        convert_arrow_table_to_dataframe(table)


@pytest.mark.parametrize("missing_key", ["x-gdc-xtab-v1", "x-gdc-model-v1", "x-gdc-view-v1"])
def test_convert_arrow_missing_required_key_raises(missing_key: str) -> None:
    """Arrow table missing any of the three required schema keys raises ValueError naming it."""
    table, _, _ = _load_case("dim_r_m")
    stripped_meta = {k: v for k, v in table.schema.metadata.items() if k != missing_key.encode()}
    table = table.replace_schema_metadata(stripped_meta)
    with pytest.raises(ValueError, match=re.escape(missing_key)):
        convert_arrow_table_to_dataframe(table)


def test_convert_arrow_missing_row_type_column_raises() -> None:
    """Arrow table missing __row_type control column raises ValueError."""
    table, _, _ = _load_case("dim_r_m")
    # Drop __row_type column.
    idx = table.schema.get_field_index("__row_type")
    table = table.remove_column(idx)
    with pytest.raises(ValueError, match="__row_type"):
        convert_arrow_table_to_dataframe(table)


# ---------------------------------------------------------------------------
# self_destruct parameter
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "case_name",
    [
        pytest.param("dim_r_m", id="no-totals"),
        pytest.param("totals_grand_row_sum", id="row-totals"),
        pytest.param("dim_m_c", id="transposed"),
    ],
)
def test_arrow_converter_self_destruct(case_name: str) -> None:
    """self_destruct=True produces the same DataFrame as the default (False)."""
    if case_name not in _cases():
        pytest.skip(f"fixture {case_name!r} not available")
    # Load twice: self_destruct modifies table buffers in-place.
    table_normal, _, _ = _load_case(case_name)
    table_destruct, _, _ = _load_case(case_name)
    expected = convert_arrow_table_to_dataframe(table_normal, self_destruct=False)
    actual = convert_arrow_table_to_dataframe(table_destruct, self_destruct=True)
    _assert_df_matches(actual, expected)


# ---------------------------------------------------------------------------
# _build_field_index — direct unit tests for total-label padding
# ---------------------------------------------------------------------------


def _make_field(name: str, gdc: dict) -> pa.Field:
    return pa.field(name, pa.float64(), metadata={b"gdc": json.dumps(gdc).encode()})


def test_build_field_index_subtotal_padding() -> None:
    """grand_total fields with partial label_values are right-padded with the agg name."""
    col_label_refs = ["l0", "l1"]  # two col-label levels: status, year
    label_ref_to_id = {"l0": "status", "l1": "year"}
    model_meta = {
        "labels": {
            "status": {"labelTitle": "Status"},
            "year": {"labelTitle": "Year"},
        },
        "requestedShape": {"metrics": ["price", "order_amount"]},
        "metrics": {
            "price": {"title": "Price"},
            "order_amount": {"title": "Order Amount"},
        },
    }
    data_fields = [
        # regular metric: full label_values → no padding
        _make_field("metric_group_0", {"type": "metric", "index": 0, "label_values": ["Active", "2023"]}),
        # subtotal: 1 label kept (status), year padded with "SUM"
        _make_field(
            "grand_total_0", {"type": "total", "metric_index": 0, "agg_function": "sum", "label_values": ["Active"]}
        ),
        # grand total: no labels → both levels padded with "SUM"
        _make_field("grand_total_1", {"type": "total", "metric_index": 1, "agg_function": "sum", "label_values": []}),
    ]

    idx = _build_field_index(data_fields, col_label_refs, label_ref_to_id, model_meta, xtab_meta={})

    assert isinstance(idx, pandas.MultiIndex)
    assert idx.tolist() == [
        ("Active", "2023", "Price"),  # regular
        ("Active", "SUM", "Price"),  # subtotal: status kept, year padded
        ("SUM", "SUM", "Order Amount"),  # grand total: both levels padded
    ]
    assert idx.names == ["Status", "Year", None]


def test_build_field_index_no_col_labels() -> None:
    """When there are no column label refs the index is a flat Index of metric titles."""
    model_meta = {
        "labels": {},
        "requestedShape": {"metrics": ["price", "order_amount"]},
        "metrics": {"price": {"title": "Price"}, "order_amount": {"title": "Order Amount"}},
    }
    data_fields = [
        _make_field("metric_group_0", {"type": "metric", "index": 0, "label_values": []}),
        _make_field("metric_group_1", {"type": "metric", "index": 1, "label_values": []}),
    ]

    idx = _build_field_index(data_fields, col_label_refs=[], label_ref_to_id={}, model_meta=model_meta, xtab_meta={})

    assert isinstance(idx, pandas.Index)
    assert not isinstance(idx, pandas.MultiIndex)
    assert idx.tolist() == ["Price", "Order Amount"]


def test_build_field_index_asymmetric_depth() -> None:
    """Two total fields with different label_values lengths are padded independently."""
    col_label_refs = ["l0", "l1"]
    label_ref_to_id = {"l0": "status", "l1": "year"}
    model_meta = {
        "labels": {"status": {"labelTitle": "Status"}, "year": {"labelTitle": "Year"}},
        "requestedShape": {"metrics": ["price", "order_amount"]},
        "metrics": {"price": {"title": "Price"}, "order_amount": {"title": "Order Amount"}},
    }
    data_fields = [
        # price: 1 label kept → pads year only
        _make_field(
            "grand_total_0", {"type": "total", "metric_index": 0, "agg_function": "sum", "label_values": ["Active"]}
        ),
        # order_amount: 0 labels kept → pads both
        _make_field("grand_total_1", {"type": "total", "metric_index": 1, "agg_function": "max", "label_values": []}),
    ]

    idx = _build_field_index(data_fields, col_label_refs, label_ref_to_id, model_meta, xtab_meta={})

    assert idx.tolist() == [
        ("Active", "SUM", "Price"),
        ("MAX", "MAX", "Order Amount"),
    ]


# ---------------------------------------------------------------------------
# compute_row_totals_indexes — empty execution_dims fallback
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "case_name",
    [
        pytest.param("dim_r_m", id="non-transposed"),
        pytest.param("dim_m_c", id="transposed"),
        pytest.param("tot_d0_sub", id="with-totals"),
    ],
)
def test_compute_row_totals_empty_dims(case_name: str) -> None:
    """execution_dims=[] falls back to an empty row_dim and returns []."""
    if case_name not in _cases():
        pytest.skip(f"fixture {case_name!r} not available")
    table, _, _ = _load_case(case_name)
    assert compute_row_totals_indexes(table, []) == []
