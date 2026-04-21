# (C) 2026 GoodData Corporation
from __future__ import annotations

import ast
import io
import json
import logging
import re
from pathlib import Path
from unittest.mock import MagicMock, patch

import gooddata_pandas.data_access as _da
import numpy
import pandas
import pyarrow as pa
import pytest
from gooddata_pandas.arrow_convertor import (
    _build_field_index,
    _build_inline_index,
    _compute_primary_labels_from_fields,
    _compute_primary_labels_from_inline,
    _metric_title,
    compute_column_totals_indexes,
    compute_primary_labels,
    compute_row_totals_indexes,
    convert_arrow_table_to_dataframe,
    convert_label_values,
    read_model_labels,
    reorder_grand_totals,
)
from gooddata_pandas.arrow_types import ArrowConfig, TypesMapper
from gooddata_pandas.data_access import ExecutionDefinitionBuilder
from gooddata_pandas.dataframe import DataFrameFactory
from gooddata_sdk import ExecutionDefinition
from gooddata_sdk.compute.model.execution import BareExecutionResponse, ResultSizeBytesLimitExceeded
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
    """Classic (default) conversion matches the JSON-path ground truth for all metadata."""
    table, expected_df, meta = _load_case(case_name)
    actual_df = convert_arrow_table_to_dataframe(table)  # types_mapper="classic"

    _assert_df_matches(actual_df, expected_df)
    assert compute_row_totals_indexes(table, meta["dimensions"]) == meta["row_totals_indexes"]
    assert compute_column_totals_indexes(table, meta["dimensions"]) == meta["column_totals_indexes"]
    primary_index, primary_cols = compute_primary_labels(table)
    assert primary_index == {int(k): v for k, v in meta["primary_labels_from_index"].items()}
    assert primary_cols == {int(k): v for k, v in meta["primary_labels_from_columns"].items()}


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


@pytest.mark.parametrize("case_name", _cases())
def test_for_arrow_table_without_execution_response(case_name: str) -> None:
    """for_arrow_table with no execution_response: DataFrame matches, metadata totals are empty."""
    table, expected_df, _ = _load_case(case_name)
    gdf = DataFrameFactory(MagicMock(), "test_workspace")
    df, metadata = gdf.for_arrow_table(table)
    _assert_df_matches(df, expected_df)
    assert metadata.execution_response is None
    assert metadata.row_totals_indexes == []
    assert metadata.column_totals_indexes == []


@pytest.mark.parametrize("case_name", _cases())
def test_for_arrow_table_with_execution_response(case_name: str) -> None:
    """for_arrow_table with execution_response populates all metadata fields correctly."""
    table, expected_df, meta = _load_case(case_name)
    mock_exec_response = MagicMock()
    mock_exec_response.dimensions = meta["dimensions"]
    gdf = DataFrameFactory(MagicMock(), "test_workspace")
    df, metadata = gdf.for_arrow_table(table, execution_response=mock_exec_response)
    _assert_df_matches(df, expected_df)
    assert metadata.execution_response is mock_exec_response
    assert metadata.row_totals_indexes == meta["row_totals_indexes"]
    assert metadata.column_totals_indexes == meta["column_totals_indexes"]
    assert metadata.primary_labels_from_index == {int(k): v for k, v in meta["primary_labels_from_index"].items()}
    assert metadata.primary_labels_from_columns == {int(k): v for k, v in meta["primary_labels_from_columns"].items()}


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


# ---------------------------------------------------------------------------
# label_overrides — attribute and metric title overrides
# ---------------------------------------------------------------------------


def _minimal_model_meta(label_ids: list[str], metric_ids: list[str]) -> dict:
    """Build the minimum model_meta structure needed by _build_inline_index / _build_field_index."""
    return {
        "labels": {lid: {"labelTitle": lid.capitalize()} for lid in label_ids},
        "metrics": {mid: {"title": mid.capitalize()} for mid in metric_ids},
        "requestedShape": {"metrics": metric_ids},
    }


def test_label_override_attribute_title() -> None:
    """label_overrides['labels'] changes the row index level name."""
    table = pa.table(
        {
            "__row_type": pa.array([0, 0], type=pa.int8()),
            "region": pa.array(["East", "West"], type=pa.string()),
        }
    )
    xtab_meta = {
        "labelMetadata": {"l0": {"labelId": "region", "primaryLabelId": "region"}},
        "totalsMetadata": {},
    }
    model_meta = _minimal_model_meta(["region"], [])

    idx_default = _build_inline_index(table, ["l0"], {"l0": "region"}, model_meta, xtab_meta)
    assert idx_default is not None
    assert idx_default.name == "Region"  # original title

    overrides = {"labels": {"region": {"title": "Sales Region"}}}
    idx_overridden = _build_inline_index(
        table, ["l0"], {"l0": "region"}, model_meta, xtab_meta, label_overrides=overrides
    )
    assert idx_overridden is not None
    assert idx_overridden.name == "Sales Region"
    # Values are unchanged — only the level name is overridden.
    assert idx_overridden.tolist() == ["East", "West"]


def test_label_override_metric_title() -> None:
    """label_overrides['metrics'] changes the metric column name in the field index."""
    model_meta = _minimal_model_meta([], ["revenue", "cost"])
    data_fields = [
        _make_field("metric_group_0", {"type": "metric", "index": 0, "label_values": []}),
        _make_field("metric_group_1", {"type": "metric", "index": 1, "label_values": []}),
    ]

    idx_default = _build_field_index(data_fields, [], {}, model_meta, xtab_meta={})
    assert idx_default.tolist() == ["Revenue", "Cost"]

    overrides = {"metrics": {"revenue": {"title": "Gross Revenue"}}}
    idx_overridden = _build_field_index(data_fields, [], {}, model_meta, xtab_meta={}, label_overrides=overrides)
    assert idx_overridden.tolist() == ["Gross Revenue", "Cost"]


def test_label_override_col_attribute_name() -> None:
    """label_overrides['labels'] changes the column-dimension attribute level name."""
    model_meta = _minimal_model_meta(["status"], ["price"])
    data_fields = [
        _make_field("metric_group_0", {"type": "metric", "index": 0, "label_values": ["Active"]}),
        _make_field("metric_group_1", {"type": "metric", "index": 0, "label_values": ["Inactive"]}),
    ]
    col_label_refs = ["l0"]
    label_ref_to_id = {"l0": "status"}

    idx_default = _build_field_index(data_fields, col_label_refs, label_ref_to_id, model_meta, xtab_meta={})
    assert idx_default.names == ["Status", None]

    overrides = {"labels": {"status": {"title": "Account Status"}}}
    idx_overridden = _build_field_index(
        data_fields, col_label_refs, label_ref_to_id, model_meta, xtab_meta={}, label_overrides=overrides
    )
    assert idx_overridden.names == ["Account Status", None]
    assert idx_overridden.tolist() == [("Active", "Price"), ("Inactive", "Price")]


def test_label_override_nonexistent_id_is_noop() -> None:
    """An override for a local_id absent from the result is silently ignored."""
    model_meta = _minimal_model_meta(["region"], ["price"])
    data_fields = [_make_field("metric_group_0", {"type": "metric", "index": 0, "label_values": []})]
    overrides = {"labels": {"nonexistent_attr": {"title": "X"}}, "metrics": {"nonexistent_metric": {"title": "Y"}}}

    idx = _build_field_index(data_fields, [], {}, model_meta, xtab_meta={}, label_overrides=overrides)
    assert idx.tolist() == ["Price"]  # unchanged

    table = pa.table({"__row_type": pa.array([0], type=pa.int8()), "region": pa.array(["East"], type=pa.string())})
    xtab_meta = {"labelMetadata": {"l0": {"labelId": "region", "primaryLabelId": "region"}}, "totalsMetadata": {}}
    inline = _build_inline_index(table, ["l0"], {"l0": "region"}, model_meta, xtab_meta, label_overrides=overrides)
    assert inline is not None
    assert inline.name == "Region"  # unchanged


def test_label_override_end_to_end_via_fixture() -> None:
    """label_overrides applied through convert_arrow_table_to_dataframe on dim_r_m fixture."""
    if "dim_r_m" not in _cases():
        pytest.skip("fixture dim_r_m not available")
    table, _, _ = _load_case("dim_r_m")

    # dim_r_m: row attr = "region" (title "Region"), metrics "price" (title "price"), "order_amount" (title "Order Amount")
    overrides = {
        "labels": {"region": {"title": "Sales Region"}},
        "metrics": {"price": {"title": "Revenue"}, "order_amount": {"title": "Total Orders"}},
    }
    df = convert_arrow_table_to_dataframe(table, label_overrides=overrides)

    assert df.index.name == "Sales Region"
    col_names = [c[0] for c in df.columns.tolist()]
    assert "Revenue" in col_names
    assert "Total Orders" in col_names


def test_label_override_total_agg_label_unchanged() -> None:
    """Aggregation labels on total rows (e.g. 'SUM') are not affected by label_overrides."""
    if "tot_d1_grand" not in _cases():
        pytest.skip("fixture tot_d1_grand not available")
    table, _, _ = _load_case("tot_d1_grand")
    overrides = {"labels": {"region": {"title": "X"}, "category": {"title": "Y"}}}
    df = convert_arrow_table_to_dataframe(table, label_overrides=overrides)

    # Grand total row still uses the aggregation marker, not the override.
    last_row = df.index.tolist()[-1]
    assert "SUM" in last_row


# ---------------------------------------------------------------------------
# reorder_grand_totals — unit tests
# ---------------------------------------------------------------------------


def _make_row_type_table(row_types: list[int]) -> pa.Table:
    """Build a minimal Arrow table with __row_type and one data column."""
    return pa.table(
        {
            "__row_type": pa.array(row_types, type=pa.int8()),
            "value": pa.array(list(range(len(row_types))), type=pa.float64()),
        }
    )


def test_reorder_grand_totals_no_row_type_column() -> None:
    """Table without __row_type is returned as-is for any position."""
    table = pa.table({"value": [1, 2, 3]})
    for pos in ("top", "pinnedTop", "bottom", "pinnedBottom", None):
        result = reorder_grand_totals(table, pos)
        assert result is table


def test_reorder_grand_totals_bottom_positions_are_noop() -> None:
    """position='bottom', 'pinnedBottom', and None leave the table unchanged."""
    table = _make_row_type_table([0, 0, 2])
    for pos in ("bottom", "pinnedBottom", None):
        result = reorder_grand_totals(table, pos)
        assert result is table


def test_reorder_grand_totals_top_moves_grand_total_rows() -> None:
    """position='top' moves __row_type==2 rows to the front."""
    table = _make_row_type_table([0, 0, 0, 2])
    result = reorder_grand_totals(table, "top")

    rt = result.column("__row_type").to_pylist()
    assert rt[0] == 2
    assert rt[1:] == [0, 0, 0]
    # Original value order: grand total (value=3) comes first now.
    assert result.column("value").to_pylist() == [3, 0, 1, 2]


def test_reorder_grand_totals_pinnedTop_same_as_top() -> None:
    """'pinnedTop' behaves identically to 'top'."""
    table = _make_row_type_table([0, 0, 2])
    top_result = reorder_grand_totals(table, "top")
    pinned_result = reorder_grand_totals(table, "pinnedTop")
    assert top_result.column("__row_type").to_pylist() == pinned_result.column("__row_type").to_pylist()
    assert top_result.column("value").to_pylist() == pinned_result.column("value").to_pylist()


def test_reorder_grand_totals_no_grand_total_rows_is_noop() -> None:
    """Table with __row_type column but no grand total rows (type==2) is returned as-is."""
    table = _make_row_type_table([0, 0, 0])
    result = reorder_grand_totals(table, "top")
    assert result is table


def test_reorder_grand_totals_subtotals_stay_in_place() -> None:
    """__row_type==1 subtotal rows are not moved — only __row_type==2 grand totals are."""
    # Pattern: 5 data rows, 1 subtotal, 5 more data rows, 1 grand total
    table = _make_row_type_table([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2])
    result = reorder_grand_totals(table, "top")

    rt = result.column("__row_type").to_pylist()
    # Grand total (was at index 11) is now at index 0.
    assert rt[0] == 2
    # Subtotal (was at index 5) is now at index 6 (shifted by 1 because grand total moved to front).
    assert rt[6] == 1
    # All data rows (type==0) are present.
    assert rt.count(0) == 10
    assert rt.count(1) == 1
    assert rt.count(2) == 1


def test_grand_totals_position_top_integration() -> None:
    """for_arrow_table with grand_totals_position='top' moves grand total to first row."""
    if "tot_d1_grand" not in _cases():
        pytest.skip("fixture tot_d1_grand not available")
    table, _, meta = _load_case("tot_d1_grand")
    mock_exec_response = MagicMock()
    mock_exec_response.dimensions = meta["dimensions"]

    gdf = DataFrameFactory(MagicMock(), "test_workspace")

    # Default (bottom): grand total is at the last row.
    df_bottom, meta_bottom = gdf.for_arrow_table(table, execution_response=mock_exec_response)
    last_idx = df_bottom.index.tolist()[-1]
    assert all(v == "SUM" for v in last_idx), f"expected SUM at last row, got {last_idx}"
    bottom_totals = meta_bottom.row_totals_indexes

    # Top: grand total row moves to index 0.
    df_top, meta_top = gdf.for_arrow_table(table, execution_response=mock_exec_response, grand_totals_position="top")
    first_idx = df_top.index.tolist()[0]
    assert all(v == "SUM" for v in first_idx), f"expected SUM at first row, got {first_idx}"

    # row_totals_indexes with 'top' must have 0 where 'bottom' had the last data index.
    for level_bottom, level_top in zip(bottom_totals, meta_top.row_totals_indexes):
        if level_bottom:
            assert level_top == [0], f"expected [0] in top totals, got {level_top}"


# ---------------------------------------------------------------------------
# AFM/JSON ↔ Arrow parity: label_overrides
#
# The parquet fixture is the JSON-path ground truth (no overrides).
# Parity rule: applying label_overrides must change only names, never values.
# We extract local IDs from Arrow schema metadata so the test is fixture-agnostic.
# ---------------------------------------------------------------------------

_LABEL_OVERRIDE_PARITY_CASES = [
    pytest.param("dim_r_m", id="simple"),
    pytest.param("dim_rc_m", id="two-row-attrs"),
    pytest.param("tot_d1_grand", id="with-grand-totals"),
    pytest.param("tot_d1_sub_grand", id="with-subtotals-and-grand-totals"),
]


def _first_attr_and_metric(table: pa.Table) -> tuple[str | None, str | None]:
    """Return the first row-dimension attribute local_id and first metric local_id from Arrow metadata."""
    xtab_meta = json.loads(table.schema.metadata[b"x-gdc-xtab-v1"])
    model_meta = json.loads(table.schema.metadata[b"x-gdc-model-v1"])
    label_ref_to_id = {ref: info["labelId"] for ref, info in xtab_meta["labelMetadata"].items()}
    row_label_refs: list[str] = xtab_meta["computedShape"]["rows"]
    first_attr = label_ref_to_id[row_label_refs[0]] if row_label_refs else None
    metrics: list[str] = model_meta["requestedShape"]["metrics"]
    first_metric = metrics[0] if metrics else None
    return first_attr, first_metric


@pytest.mark.parametrize("case_name", _LABEL_OVERRIDE_PARITY_CASES)
def test_label_override_parity_values_unchanged(case_name: pytest.param) -> None:
    """
    label_overrides must not change the underlying numeric values — only display names.

    Reference: the parquet fixture is the JSON-path output without overrides.
    Arrow path with overrides must produce identical values to the parquet baseline.
    """
    case_name = case_name if isinstance(case_name, str) else case_name.values[0]
    if case_name not in _cases():
        pytest.skip(f"fixture {case_name!r} not available")

    table, expected_df, _ = _load_case(case_name)
    first_attr, first_metric = _first_attr_and_metric(table)

    overrides: dict = {"labels": {}, "metrics": {}}
    if first_attr:
        overrides["labels"][first_attr] = {"title": "OVERRIDE_ATTR"}
    if first_metric:
        overrides["metrics"][first_metric] = {"title": "OVERRIDE_METRIC"}

    df_with_overrides = convert_arrow_table_to_dataframe(table, label_overrides=overrides)
    df_no_overrides = convert_arrow_table_to_dataframe(table)

    # Shape must be identical.
    assert df_with_overrides.shape == df_no_overrides.shape

    # Numeric values must be identical — overrides touch names only.
    exp_vals = df_no_overrides.to_numpy(dtype=float, na_value=float("nan"))
    act_vals = df_with_overrides.to_numpy(dtype=float, na_value=float("nan"))
    both_nan = numpy.isnan(exp_vals) & numpy.isnan(act_vals)
    assert (numpy.isclose(exp_vals, act_vals, equal_nan=False) | both_nan).all(), (
        "label_overrides changed numeric values — only names should change"
    )

    # The override name must appear somewhere in the output.
    all_names = list(df_with_overrides.index.names) + [
        n for tup in df_with_overrides.columns.tolist() for n in (tup if isinstance(tup, tuple) else (tup,))
    ]
    if first_attr:
        assert "OVERRIDE_ATTR" in all_names, f"attribute override not found in {all_names}"
    if first_metric:
        assert "OVERRIDE_METRIC" in all_names, f"metric override not found in {all_names}"

    # And the matching name from the no-override run must now be absent (replaced).
    no_override_names = list(df_no_overrides.index.names) + [
        n for tup in df_no_overrides.columns.tolist() for n in (tup if isinstance(tup, tuple) else (tup,))
    ]
    if first_attr and "OVERRIDE_ATTR" in all_names:
        original_attr_name = next(
            n
            for n in no_override_names
            if n and n not in ("OVERRIDE_ATTR", "OVERRIDE_METRIC") and df_no_overrides.index.names[0] == n
        )
        assert original_attr_name not in all_names, (
            f"original attr name {original_attr_name!r} still present after override"
        )


# ---------------------------------------------------------------------------
# AFM/JSON ↔ Arrow parity: grand_totals_position
#
# The parquet fixture is the JSON-path ground truth with default ("bottom") placement.
# Parity rules:
#   - Arrow "bottom" == parquet (same rows and values, already covered by test_arrow_converter)
#   - Arrow "top" vs Arrow "bottom": same rows, same values; grand total at position 0
#   - row_totals_indexes reflect the new positions after reordering
# ---------------------------------------------------------------------------

# Fixtures where grand totals appear as rows in the output DataFrame
# (non-transposed, __row_type==2 present).
_GRAND_TOTAL_ROW_CASES = [
    pytest.param("tot_d1_grand", id="grand-only"),
    pytest.param("tot_d1_sub_grand", id="sub-and-grand"),
]


@pytest.mark.parametrize("case_name", _GRAND_TOTAL_ROW_CASES)
def test_grand_totals_bottom_matches_parquet(case_name: pytest.param) -> None:
    """
    Arrow path with grand_totals_position='bottom' must produce the same DataFrame
    as the JSON-path parquet ground truth (default placement).
    """
    case_name = case_name if isinstance(case_name, str) else case_name.values[0]
    if case_name not in _cases():
        pytest.skip(f"fixture {case_name!r} not available")

    table, expected_df, meta = _load_case(case_name)
    mock_exec_response = MagicMock()
    mock_exec_response.dimensions = meta["dimensions"]
    gdf = DataFrameFactory(MagicMock(), "test_workspace")

    df, metadata = gdf.for_arrow_table(table, execution_response=mock_exec_response, grand_totals_position="bottom")
    _assert_df_matches(df, expected_df)
    assert metadata.row_totals_indexes == meta["row_totals_indexes"]


@pytest.mark.parametrize("case_name", _GRAND_TOTAL_ROW_CASES)
def test_grand_totals_top_same_data_as_bottom(case_name: pytest.param) -> None:
    """
    Arrow path with grand_totals_position='top' must contain exactly the same rows
    and values as 'bottom' — only the position of grand total rows differs.
    """
    case_name = case_name if isinstance(case_name, str) else case_name.values[0]
    if case_name not in _cases():
        pytest.skip(f"fixture {case_name!r} not available")

    table, _, meta = _load_case(case_name)
    mock_exec_response = MagicMock()
    mock_exec_response.dimensions = meta["dimensions"]
    gdf = DataFrameFactory(MagicMock(), "test_workspace")

    df_bottom, meta_bottom = gdf.for_arrow_table(
        table, execution_response=mock_exec_response, grand_totals_position="bottom"
    )
    df_top, meta_top = gdf.for_arrow_table(table, execution_response=mock_exec_response, grand_totals_position="top")

    # Same shape.
    assert df_top.shape == df_bottom.shape

    # Grand total row(s) are at the front for "top".
    top_total_idxs = {i for level in meta_top.row_totals_indexes for i in level}
    assert top_total_idxs == {0}, f"expected grand total at row 0, got top_totals={meta_top.row_totals_indexes}"

    # Same set of index values across both DataFrames.
    assert sorted(df_top.index.tolist()) == sorted(df_bottom.index.tolist()), (
        "grand_totals_position='top' changed the set of rows"
    )

    # Same numeric values when both DataFrames are sorted by index.
    df_top_sorted = df_top.sort_index()
    df_bottom_sorted = df_bottom.sort_index()
    exp_vals = df_bottom_sorted.to_numpy(dtype=float, na_value=float("nan"))
    act_vals = df_top_sorted.to_numpy(dtype=float, na_value=float("nan"))
    both_nan = numpy.isnan(exp_vals) & numpy.isnan(act_vals)
    assert (numpy.isclose(exp_vals, act_vals, equal_nan=False) | both_nan).all(), (
        "grand_totals_position='top' changed numeric values"
    )


# ---------------------------------------------------------------------------
# indexed() / not_indexed() use_arrow=True
#
# Tests use Arrow fixtures from the ground-truth directory.
# The SDK execution layer is mocked: `sdk.compute.for_exec_def` returns a
# mock Execution whose `bare_exec_response.read_result_arrow()` yields the
# fixture Arrow table.  `exec_def` is built from real ExecutionDefinitionBuilder
# so attribute and metric local IDs match the fixture column names.
# ---------------------------------------------------------------------------


def _mock_execution(table: pa.Table, columns: dict, index_by=None) -> tuple:
    """
    Build a (mock_sdk, mock_execution) pair where:
    - sdk.compute.for_exec_def() returns mock_execution
    - mock_execution.exec_def is built by ExecutionDefinitionBuilder
    - mock_execution.bare_exec_response.read_result_arrow() returns *table*
    """
    builder = ExecutionDefinitionBuilder(columns, index_by)
    exec_def = builder.build_execution_definition()

    mock_exec = MagicMock()
    mock_exec.exec_def = exec_def
    mock_exec.bare_exec_response.read_result_arrow.return_value = table

    mock_sdk = MagicMock()
    mock_sdk.compute.for_exec_def.return_value = mock_exec

    return mock_sdk, mock_exec, builder


def test_indexed_use_arrow_basic() -> None:
    """indexed() with use_arrow=True returns the expected DataFrame from the dim_r_m fixture."""
    if "dim_r_m" not in _cases():
        pytest.skip("fixture dim_r_m not available")
    table, _, _ = _load_case("dim_r_m")

    columns = {"price": "metric/price", "order_amount": "metric/order_amount"}
    index_by = {"reg": "label/region"}
    mock_sdk, _, _ = _mock_execution(table, columns, index_by)

    gdf = DataFrameFactory(mock_sdk, "workspace", use_arrow=True)
    df = gdf.indexed(index_by=index_by, columns=columns)

    assert len(df) == 5
    assert list(df.columns) == ["price", "order_amount"]
    assert df.index.name == "reg"
    assert list(df.index) == ["Midwest", "Northeast", "South", "Unknown", "West"]
    assert abs(df["price"].iloc[0] - 79837.24) < 0.01
    assert abs(df["order_amount"].iloc[0] - 98425.20) < 0.01


def test_not_indexed_use_arrow_basic() -> None:
    """not_indexed() with use_arrow=True returns a DataFrame with attribute + metric columns."""
    if "dim_r_m" not in _cases():
        pytest.skip("fixture dim_r_m not available")
    table, _, _ = _load_case("dim_r_m")

    columns = {"region": "label/region", "price": "metric/price"}
    mock_sdk, _, _ = _mock_execution(table, columns)

    gdf = DataFrameFactory(mock_sdk, "workspace", use_arrow=True)
    df = gdf.not_indexed(columns=columns)

    assert len(df) == 5
    assert list(df.columns) == ["region", "price"]
    assert list(df["region"]) == ["Midwest", "Northeast", "South", "Unknown", "West"]
    assert abs(df["price"].iloc[2] - 192957.34) < 0.01


def test_not_indexed_use_arrow_metrics_only() -> None:
    """not_indexed() with use_arrow=True handles metrics-only results (no attribute columns)."""
    if "metrics_only" not in _cases():
        pytest.skip("fixture metrics_only not available")
    table, _, _ = _load_case("metrics_only")

    columns = {"price": "metric/price", "order_amount": "metric/order_amount"}
    mock_sdk, _, _ = _mock_execution(table, columns)

    gdf = DataFrameFactory(mock_sdk, "workspace", use_arrow=True)
    df = gdf.not_indexed(columns=columns)

    assert len(df) == 1
    assert list(df.columns) == ["price", "order_amount"]
    assert abs(df["price"].iloc[0] - 430464.45) < 0.01
    assert abs(df["order_amount"].iloc[0] - 516058.34) < 0.01


def test_indexed_use_arrow_column_order_preserved() -> None:
    """indexed() with use_arrow=True preserves the caller-specified column order."""
    if "dim_r_m" not in _cases():
        pytest.skip("fixture dim_r_m not available")
    table, _, _ = _load_case("dim_r_m")

    # Reverse order compared to fixture field ordering.
    columns = {"order_amount": "metric/order_amount", "price": "metric/price"}
    index_by = {"reg": "label/region"}
    mock_sdk, _, _ = _mock_execution(table, columns, index_by)

    gdf = DataFrameFactory(mock_sdk, "workspace", use_arrow=True)
    df = gdf.indexed(index_by=index_by, columns=columns)

    assert list(df.columns) == ["order_amount", "price"]


def test_indexed_use_arrow_matches_default_path() -> None:
    """indexed() with use_arrow=True produces same values as without use_arrow for dim_r_m."""
    if "dim_r_m" not in _cases():
        pytest.skip("fixture dim_r_m not available")
    table, expected_parquet, _ = _load_case("dim_r_m")

    columns = {"price": "metric/price", "order_amount": "metric/order_amount"}
    index_by = {"reg": "label/region"}
    mock_sdk, _, _ = _mock_execution(table, columns, index_by)

    gdf = DataFrameFactory(mock_sdk, "workspace", use_arrow=True)
    df = gdf.indexed(index_by=index_by, columns=columns)

    # Values should match the parquet ground truth (which was generated by the JSON path).
    assert len(df) == 5
    assert sorted(df.index.tolist()) == sorted(["Midwest", "Northeast", "South", "Unknown", "West"])


def test_for_items_use_arrow_basic() -> None:
    """for_items() with use_arrow=True auto-indexes when both attrs and metrics present."""
    if "dim_r_m" not in _cases():
        pytest.skip("fixture dim_r_m not available")
    table, _, _ = _load_case("dim_r_m")

    items = {
        "region": "label/region",
        "price": "metric/price",
        "order_amount": "metric/order_amount",
    }
    # for_items with auto_index=True routes attrs → index, metrics → columns
    # so the exec_def will have region as attribute and price/order_amount as metrics.
    mock_sdk, _, _ = _mock_execution(
        table,
        columns={"price": "metric/price", "order_amount": "metric/order_amount"},
        index_by={"region": "label/region"},
    )

    gdf = DataFrameFactory(mock_sdk, "workspace", use_arrow=True)
    df = gdf.for_items(items=items)

    assert len(df) == 5
    assert "price" in df.columns
    assert "order_amount" in df.columns
    assert df.index.name == "region"


# ---------------------------------------------------------------------------
# Parity tests: indexed() / not_indexed() use_arrow=True vs ground-truth parquet
#
# The parquet files were produced by for_exec_def_arrow() (display-name columns,
# display-name index).  The use_arrow=True path produces the same numeric values
# but under caller-supplied column / index names.  We sort both DataFrames by
# their index tuples and compare the raw numpy arrays with assert_allclose.
# ---------------------------------------------------------------------------


def _sorted_values(df: pandas.DataFrame) -> numpy.ndarray:
    """Return the numeric values of *df* sorted by its index."""
    sort_key = df.index.to_frame(index=False).apply(tuple, axis=1)
    return df.iloc[sort_key.argsort()].to_numpy(dtype=float, na_value=float("nan"))


@pytest.mark.parametrize(
    "case, index_by, columns, parquet_col_order",
    [
        (
            "dim_r_m",
            {"Region": "label/region"},
            {"price": "metric/price", "order_amount": "metric/order_amount"},
            ["price", "order_amount"],
        ),
        (
            "dim_rc_m",
            {"Region": "label/region", "Category": "label/products.category"},
            {"price": "metric/price", "order_amount": "metric/order_amount"},
            ["price", "order_amount"],
        ),
        (
            "dim_rcs_m",
            {
                "Region": "label/region",
                "Category": "label/products.category",
                "Status": "label/order_status",
            },
            {"price": "metric/price", "order_amount": "metric/order_amount"},
            ["price", "order_amount"],
        ),
        (
            "single_metric_many_rows",
            {
                "Region": "label/region",
                "State": "label/state",
                "Category": "label/products.category",
            },
            {"price": "metric/price"},
            ["price"],
        ),
    ],
)
def test_indexed_use_arrow_parity_with_ground_truth(
    case: str,
    index_by: dict,
    columns: dict,
    parquet_col_order: list[str],
) -> None:
    """indexed(use_arrow=True) produces the same numeric values as the parquet ground truth."""
    if case not in _cases():
        pytest.skip(f"fixture {case} not available")

    table, expected_parquet, _ = _load_case(case)
    mock_sdk, _, _ = _mock_execution(table, columns, index_by)

    gdf = DataFrameFactory(mock_sdk, "workspace", use_arrow=True)
    df = gdf.indexed(index_by=index_by, columns=columns)

    assert df.shape == expected_parquet.shape, f"{case}: shape mismatch"

    actual_vals = _sorted_values(df[parquet_col_order])
    expected_vals = _sorted_values(expected_parquet)
    both_nan = numpy.isnan(actual_vals) & numpy.isnan(expected_vals)
    assert (numpy.isclose(actual_vals, expected_vals, equal_nan=False) | both_nan).all(), (
        f"{case}: numeric values differ from parquet ground truth"
    )


def test_not_indexed_use_arrow_parity_with_ground_truth() -> None:
    """not_indexed(use_arrow=True) produces the same numeric values as the parquet ground truth for metrics_only."""
    if "metrics_only" not in _cases():
        pytest.skip("fixture metrics_only not available")

    table, expected_parquet, _ = _load_case("metrics_only")
    columns = {"price": "metric/price", "order_amount": "metric/order_amount"}
    mock_sdk, _, _ = _mock_execution(table, columns)

    gdf = DataFrameFactory(mock_sdk, "workspace", use_arrow=True)
    df = gdf.not_indexed(columns=columns)

    assert len(df) == 1
    assert abs(df["price"].iloc[0] - float(expected_parquet.loc["price", 0])) < 0.01
    assert abs(df["order_amount"].iloc[0] - float(expected_parquet.loc["Order Amount", 0])) < 0.01


# ---------------------------------------------------------------------------
# Review-driven defensive tests
# ---------------------------------------------------------------------------


def test_parse_schema_metadata_ignores_non_gdc_keys() -> None:
    """_parse_schema_metadata decodes only GoodData keys; foreign metadata does not crash."""
    if "dim_r_m" not in _cases():
        pytest.skip("fixture dim_r_m not available")
    table, _, _ = _load_case("dim_r_m")

    # Attach a non-JSON foreign key — the kind third-party tools add to Arrow tables.
    # The old code crashed with JSONDecodeError; the fixed code skips unknown keys.
    foreign_meta = {b"x-custom-tool": b"not valid json at all", **table.schema.metadata}
    table_with_foreign = table.replace_schema_metadata(foreign_meta)

    # Should not raise despite the malformed foreign key.
    df, _ = convert_arrow_table_to_dataframe(table_with_foreign), None
    assert df is not None


def test_for_exec_def_arrow_label_overrides_none_equivalent_to_empty() -> None:
    """for_exec_def_arrow(label_overrides=None) behaves identically to label_overrides={}."""
    if "dim_r_m" not in _cases():
        pytest.skip("fixture dim_r_m not available")
    table, _, _ = _load_case("dim_r_m")

    mock_exec = MagicMock()
    mock_exec.bare_exec_response.read_result_arrow.return_value = table
    mock_exec.bare_exec_response.dimensions = []
    mock_sdk = MagicMock()
    mock_sdk.compute.for_exec_def.return_value = mock_exec

    gdf = DataFrameFactory(mock_sdk, "workspace")
    exec_def = MagicMock(spec=ExecutionDefinition)
    df_none, _ = gdf.for_exec_def_arrow(exec_def, label_overrides=None)
    df_empty, _ = gdf.for_exec_def_arrow(exec_def, label_overrides={})

    assert list(df_none.columns) == list(df_empty.columns)
    assert df_none.shape == df_empty.shape


def test_indexed_use_arrow_result_page_len_warns_at_call_site() -> None:
    """indexed(use_arrow=True, result_page_len=N) emits UserWarning pointing to the caller."""
    if "dim_r_m" not in _cases():
        pytest.skip("fixture dim_r_m not available")
    table, _, _ = _load_case("dim_r_m")

    columns = {"price": "metric/price", "order_amount": "metric/order_amount"}
    index_by = {"reg": "label/region"}
    mock_sdk, _, _ = _mock_execution(table, columns, index_by)

    gdf = DataFrameFactory(mock_sdk, "workspace", use_arrow=True)
    with pytest.warns(UserWarning, match="result_page_len is ignored"):
        gdf.indexed(index_by=index_by, columns=columns, result_page_len=500)


def test_compute_row_totals_indexes_tolerates_field_without_metadata() -> None:
    """compute_row_totals_indexes does not crash when a grand_total field has no metadata."""
    if "tot_d0_sub" not in _cases():
        pytest.skip("fixture tot_d0_sub not available")
    table, _, meta = _load_case("tot_d0_sub")

    # Strip metadata from one grand_total field to simulate the defensive path.
    fields = []
    for i in range(len(table.schema)):
        f = table.schema.field(i)
        if f.name.startswith("grand_total") and i == next(
            j for j in range(len(table.schema)) if table.schema.field(j).name.startswith("grand_total")
        ):
            fields.append(f.with_metadata(None))
        else:
            fields.append(f)
    new_schema = pa.schema(fields, metadata=table.schema.metadata)
    table_no_meta = table.cast(new_schema)

    # Should not raise; total indexes for the stripped field will be empty.
    result = compute_row_totals_indexes(table_no_meta, meta["dimensions"])
    assert isinstance(result, list)


def test_compute_column_totals_indexes() -> None:
    """compute_column_totals_indexes returns correct positions for column-dimension totals."""
    # tot_d1_sub: isTransposed=False, non-empty rows, grand_total_* fields become columns.
    # Column dim headers: order_status (j=0), date.year (j=1), measureGroup.
    # grand_total fields have label_values=['<status>'] (len=1), so they are totals at j=1.
    if "tot_d1_sub" in _cases():
        table, _, meta = _load_case("tot_d1_sub")
        result = compute_column_totals_indexes(table, meta["dimensions"])
        assert result == meta["column_totals_indexes"]
        assert len(result) == 3  # order_status, date.year, measureGroup
        assert result[0] == []  # no totals at order_status level
        assert len(result[1]) > 0  # subtotal columns at date.year level
        assert result[2] == []  # measureGroup always empty

    # tot_d0_sub: isTransposed=True → grand_total_* become rows → column totals empty
    if "tot_d0_sub" in _cases():
        table, _, meta = _load_case("tot_d0_sub")
        result = compute_column_totals_indexes(table, meta["dimensions"])
        assert result == []

    # dim_r_m: no grand_total_* fields → no column totals
    if "dim_r_m" in _cases():
        table, _, meta = _load_case("dim_r_m")
        result = compute_column_totals_indexes(table, meta["dimensions"])
        assert result == []


@pytest.mark.parametrize(
    "case_name",
    [
        pytest.param(c, id=c)
        for c in [
            "tot_d1_sub",
            "tot_d1_sub_grand",
            "totals_subtotal_col",
            "tot_d0_sub",
            "tot_d0_sub_grand",
            "dim_r_m",
            "totals_both_dims",
        ]
    ],
)
def test_compute_column_totals_indexes_parity_with_ground_truth(case_name: str) -> None:
    """compute_column_totals_indexes matches the stored ground-truth value in meta.json."""
    if case_name not in _cases():
        pytest.skip(f"fixture {case_name!r} not available")
    table, _, meta = _load_case(case_name)
    result = compute_column_totals_indexes(table, meta["dimensions"])
    assert result == meta["column_totals_indexes"], (
        f"{case_name}: got {result!r}, expected {meta['column_totals_indexes']!r}"
    )


# ---------------------------------------------------------------------------
# Review-finding fixes: defensive tests
# ---------------------------------------------------------------------------


def test_build_field_index_missing_gdc_metadata_raises() -> None:
    """_build_field_index raises ValueError when a data field has no gdc metadata."""
    field_no_meta = pa.field("metric_group_0", pa.float64())
    with pytest.raises(ValueError, match="gdc"):
        _build_field_index(
            data_fields=[field_no_meta],
            col_label_refs=[],
            label_ref_to_id={},
            model_meta={"labels": {}, "requestedShape": {"metrics": ["m"]}, "metrics": {}},
            xtab_meta={},
        )


def test_build_field_index_label_values_overflow() -> None:
    """grand_total fields with more label_values than col levels produce correct-length tuples."""
    # 1 col label level, but grand_total has 2 label_values → should truncate to 1 then pad
    col_label_refs = ["l0"]
    label_ref_to_id = {"l0": "status"}
    model_meta = {
        "labels": {"status": {"labelTitle": "Status"}},
        "requestedShape": {"metrics": ["price"]},
        "metrics": {"price": {"title": "Price"}},
    }
    data_fields = [
        pa.field(
            "grand_total_0",
            pa.float64(),
            metadata={
                b"gdc": json.dumps(
                    {"type": "total", "metric_index": 0, "agg_function": "sum", "label_values": ["A", "B"]}
                ).encode()
            },
        )
    ]
    xtab_meta: dict = {}
    idx = _build_field_index(data_fields, col_label_refs, label_ref_to_id, model_meta, xtab_meta)
    # Result must be a MultiIndex with 1-element tuples: (label_value, metric_title)
    assert len(idx) == 1
    assert len(idx[0]) == 2  # (col_label_value, metric_title)


def test_metric_title_out_of_range_raises() -> None:
    """_metric_title raises ValueError when metric_idx exceeds requestedShape.metrics length."""
    model_meta = {"requestedShape": {"metrics": ["price"]}, "metrics": {}}
    with pytest.raises(ValueError, match="out of range"):
        _metric_title(5, model_meta, {})


def test_compute_column_totals_indexes_no_matching_dim_returns_empty() -> None:
    """compute_column_totals_indexes returns [] when no execution dim matches col label IDs."""
    if "tot_d1_sub" not in _cases():
        pytest.skip("fixture tot_d1_sub not available")
    table, _, meta = _load_case("tot_d1_sub")
    # Replace all dimensions with one that has no matching attribute headers.
    bogus_dims = [{"headers": [{"measureGroupHeaders": [{"localIdentifier": "price"}]}]}]
    result = compute_column_totals_indexes(table, bogus_dims)
    assert result == []


def test_for_exec_result_id_arrow_types_mapper(tmp_path: Path) -> None:
    """ArrowConfig.types_mapper on the factory controls dtype mapping for use_arrow=True."""
    if "dim_r_m" not in _cases():
        pytest.skip("fixture dim_r_m not available")
    table, expected_df, meta = _load_case("dim_r_m")
    columns = {"price": "metric/price", "order_amount": "metric/order_amount"}
    index_by = {"reg": "label/region"}
    mock_sdk, _, mock_exec_response = _mock_execution(table, columns, index_by)
    mock_exec_response.dimensions = meta["dimensions"]

    mock_result_cache = MagicMock()
    mock_result_cache.execution_response = {}
    mock_sdk.compute.retrieve_result_cache_metadata.return_value = mock_result_cache

    with (
        patch("gooddata_pandas.dataframe.BareExecutionResponse") as MockBareExec,
        patch("gooddata_pandas.dataframe.models.AfmExecutionResponse"),
    ):
        mock_bare = MagicMock()
        mock_bare.read_result_arrow.return_value = table
        mock_bare.dimensions = meta["dimensions"]
        MockBareExec.return_value = mock_bare

        gdf_default = DataFrameFactory(mock_sdk, "workspace", use_arrow=True)
        df_default, _ = gdf_default.for_exec_result_id(result_id="test", result_cache_metadata=mock_result_cache)
        gdf_arrow_strings = DataFrameFactory(
            mock_sdk,
            "workspace",
            use_arrow=True,
            arrow_config=ArrowConfig(types_mapper=TypesMapper.ARROW_STRINGS),
        )
        df_arrow_strings, _ = gdf_arrow_strings.for_exec_result_id(
            result_id="test",
            result_cache_metadata=mock_result_cache,
        )

    # Shape must be identical; string columns differ in dtype only.
    assert df_default.shape == df_arrow_strings.shape


# ---------------------------------------------------------------------------
# convert_label_values — date granularity type conversion
#
# Mirrors the non-Arrow path (AttributeConverterStore in _typed_attribute_value):
#   DAY / MONTH / YEAR → pandas.Timestamp
#   WEEK / QUARTER     → str (unchanged)
#   no granularity     → values unchanged (same object returned)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "granularity, raw, expected",
    [
        ("year", ["2023", "2024"], [pandas.Timestamp("2023-01-01"), pandas.Timestamp("2024-01-01")]),
        ("month", ["2023-01", "2023-03"], [pandas.Timestamp("2023-01-01"), pandas.Timestamp("2023-03-01")]),
        ("day", ["2023-01-15", "2024-06-30"], [pandas.Timestamp("2023-01-15"), pandas.Timestamp("2024-06-30")]),
        ("week", ["2025-1", "2025-49"], ["2025-1", "2025-49"]),
        ("quarter", ["2025-1", "2025-4"], ["2025-1", "2025-4"]),
    ],
)
def test_convert_label_values_date_granularities(granularity: str, raw: list, expected: list) -> None:
    """convert_label_values converts DAY/MONTH/YEAR to Timestamp; WEEK/QUARTER stays string."""
    model_labels = {"date_attr": {"granularity": granularity}}
    result = convert_label_values("date_attr", raw, model_labels)
    assert result == expected


def test_convert_label_values_no_granularity_returns_same_object() -> None:
    """Plain text attributes (no granularity) are returned as the same list object — zero copy."""
    model_labels = {"region": {"granularity": None, "labelType": "TEXT"}}
    values = ["East", "West"]
    assert convert_label_values("region", values, model_labels) is values


def test_convert_label_values_unknown_label_id_returns_same_object() -> None:
    """Label ID absent from model_labels (no metadata) is treated as no-op."""
    values = ["foo", "bar"]
    assert convert_label_values("unknown", values, {}) is values


def test_convert_label_values_none_passthrough() -> None:
    """None values inside a date column are preserved as None (sparse rows)."""
    model_labels = {"date.year": {"granularity": "year"}}
    result = convert_label_values("date.year", ["2023", None, "2025"], model_labels)
    assert result[0] == pandas.Timestamp("2023-01-01")
    assert result[1] is None
    assert result[2] == pandas.Timestamp("2025-01-01")


def test_convert_label_values_empty_list() -> None:
    """Empty input list returns empty list without error."""
    model_labels = {"date.year": {"granularity": "year"}}
    assert convert_label_values("date.year", [], model_labels) == []


# ---------------------------------------------------------------------------
# read_model_labels — schema metadata parsing
# ---------------------------------------------------------------------------


def test_read_model_labels_returns_labels_dict() -> None:
    """read_model_labels extracts the labels sub-dict from x-gdc-model-v1."""
    model_meta = {"labels": {"region": {"granularity": None}}, "metrics": {}}
    schema_meta = {b"x-gdc-model-v1": json.dumps(model_meta).encode()}
    table = pa.table({"col": [1]}).replace_schema_metadata(schema_meta)
    assert read_model_labels(table) == {"region": {"granularity": None}}


def test_read_model_labels_missing_key_returns_empty_dict() -> None:
    """read_model_labels returns {} when x-gdc-model-v1 is absent."""
    table = pa.table({"col": [1]})
    assert read_model_labels(table) == {}


def test_read_model_labels_no_labels_key_returns_empty_dict() -> None:
    """read_model_labels returns {} when model metadata has no 'labels' key."""
    schema_meta = {b"x-gdc-model-v1": json.dumps({"metrics": {}}).encode()}
    table = pa.table({"col": [1]}).replace_schema_metadata(schema_meta)
    assert read_model_labels(table) == {}


# ---------------------------------------------------------------------------
# indexed() / not_indexed() with use_arrow=True — date granularity parity
#
# The non-Arrow path converts year/month/day → datetime via AttributeConverterStore.
# The Arrow path must produce identical types for the same columns/index.
#
# We build a minimal synthetic Arrow table with the required schema metadata
# (x-gdc-model-v1 with granularity field) and wire it into a mocked execution.
# ---------------------------------------------------------------------------


def _make_date_attr_table(
    label_id: str,
    granularity: str,
    str_values: list,
    metric_values: list[float] | None = None,
) -> pa.Table:
    """Build a minimal Arrow table for a single date attribute + one revenue metric.

    The table has the schema metadata (x-gdc-model-v1, x-gdc-xtab-v1, x-gdc-view-v1)
    that _extract_from_arrow reads to determine the label's granularity.

    Args:
        label_id:     GoodData label local ID (used as the Arrow column name).
        granularity:  Lowercase granularity string, e.g. ``"year"``, ``"month"``.
        str_values:   Raw string values for the date attribute column.
        metric_values: Optional metric values; defaults to 0.0 per row.
    """
    n = len(str_values)
    if metric_values is None:
        metric_values = [float(i) for i in range(n)]

    model_meta = {
        "labels": {
            label_id: {
                "granularity": granularity,
                "labelTitle": label_id.capitalize(),
                "labelType": None,
                "primaryLabelId": label_id,
                "attributeId": label_id,
            }
        },
        "requestedShape": {"metrics": ["revenue"]},
        "metrics": {"revenue": {"title": "Revenue"}},
    }
    xtab_meta = {
        "labelMetadata": {"l0": {"labelId": label_id, "primaryLabelId": label_id}},
        "computedShape": {"metrics": ["m0"], "rows": [], "cols": []},
        "totalsMetadata": {},
    }
    view_meta = {"isTransposed": False}
    schema_meta = {
        b"x-gdc-model-v1": json.dumps(model_meta).encode(),
        b"x-gdc-xtab-v1": json.dumps(xtab_meta).encode(),
        b"x-gdc-view-v1": json.dumps(view_meta).encode(),
    }
    gdc_metric = {b"gdc": json.dumps({"type": "metric", "index": 0}).encode()}
    schema = pa.schema(
        [
            pa.field("__row_type", pa.int8()),
            pa.field(label_id, pa.string()),
            pa.field("metric_group_0", pa.float64(), metadata=gdc_metric),
        ],
        metadata=schema_meta,
    )
    return pa.table(
        {
            "__row_type": pa.array([0] * n, type=pa.int8()),
            label_id: pa.array(str_values, type=pa.string()),
            "metric_group_0": pa.array(metric_values, type=pa.float64()),
        },
        schema=schema,
    )


@pytest.mark.parametrize(
    "case_name, index_by, columns, expected_timestamps",
    [
        (
            "date_year_in_rows",
            {"date": "label/date.year"},
            {"revenue": "metric/revenue"},
            [pandas.Timestamp("2023-01-01"), pandas.Timestamp("2024-01-01"), pandas.Timestamp("2025-01-01")],
        ),
        (
            "date_month_in_rows",
            {"date": "label/date.month"},
            {"revenue": "metric/revenue"},
            [pandas.Timestamp("2023-01-01"), pandas.Timestamp("2023-06-01"), pandas.Timestamp("2023-12-01")],
        ),
        (
            "date_day_in_rows",
            {"date": "label/date.day"},
            {"revenue": "metric/revenue"},
            [pandas.Timestamp("2023-01-15"), pandas.Timestamp("2023-06-30")],
        ),
    ],
)
def test_indexed_use_arrow_date_to_timestamp(
    case_name: str,
    index_by: dict,
    columns: dict,
    expected_timestamps: list,
) -> None:
    """indexed() with use_arrow=True converts DAY/MONTH/YEAR date attributes to Timestamp.

    Matches the non-Arrow path behaviour where AttributeConverterStore applies
    DateConverter → pandas.to_datetime for these granularities.
    """
    if case_name not in _cases():
        pytest.skip(f"fixture {case_name!r} not available")
    table, _, _ = _load_case(case_name)
    mock_sdk, _, _ = _mock_execution(table, columns, index_by)

    gdf = DataFrameFactory(mock_sdk, "workspace", use_arrow=True)
    df = gdf.indexed(index_by=index_by, columns=columns)

    assert df.index.tolist() == expected_timestamps


@pytest.mark.parametrize(
    "case_name, index_by, columns, expected_strings",
    [
        (
            "date_week_in_rows",
            {"date": "label/date.week"},
            {"revenue": "metric/revenue"},
            ["2025-1", "2025-49"],
        ),
        (
            "date_quarter_in_rows",
            {"date": "label/date.quarter"},
            {"revenue": "metric/revenue"},
            ["2025-1", "2025-4"],
        ),
    ],
)
def test_indexed_use_arrow_week_quarter_stays_string(
    case_name: str,
    index_by: dict,
    columns: dict,
    expected_strings: list,
) -> None:
    """indexed() with use_arrow=True: WEEK and QUARTER values remain as strings.

    Matches the non-Arrow path where StringConverter is registered for these granularities.
    """
    if case_name not in _cases():
        pytest.skip(f"fixture {case_name!r} not available")
    table, _, _ = _load_case(case_name)
    mock_sdk, _, _ = _mock_execution(table, columns, index_by)

    gdf = DataFrameFactory(mock_sdk, "workspace", use_arrow=True)
    df = gdf.indexed(index_by=index_by, columns=columns)

    assert df.index.tolist() == expected_strings


def test_not_indexed_use_arrow_year_column_to_timestamp() -> None:
    """not_indexed() with use_arrow=True converts a year-granularity column to Timestamp."""
    if "date_year_in_rows" not in _cases():
        pytest.skip("fixture date_year_in_rows not available")
    table, _, _ = _load_case("date_year_in_rows")
    columns = {"year_col": "label/date.year", "revenue": "metric/revenue"}
    mock_sdk, _, _ = _mock_execution(table, columns)

    gdf = DataFrameFactory(mock_sdk, "workspace", use_arrow=True)
    df = gdf.not_indexed(columns=columns)

    assert df["year_col"].tolist() == [
        pandas.Timestamp("2023-01-01"),
        pandas.Timestamp("2024-01-01"),
        pandas.Timestamp("2025-01-01"),
    ]


def test_indexed_use_arrow_date_none_values_preserved() -> None:
    """indexed() with use_arrow=True preserves None (null) entries in date columns."""
    table = _make_date_attr_table("date.year", "year", ["2023", None, "2025"], metric_values=[1.0, 2.0, 3.0])
    columns = {"revenue": "metric/revenue"}
    index_by = {"date": "label/date.year"}
    mock_sdk, _, _ = _mock_execution(table, columns, index_by)

    gdf = DataFrameFactory(mock_sdk, "workspace", use_arrow=True)
    df = gdf.indexed(index_by=index_by, columns=columns)

    idx = df.index.tolist()
    assert idx[0] == pandas.Timestamp("2023-01-01")
    assert idx[1] is None or pandas.isna(idx[1])
    assert idx[2] == pandas.Timestamp("2025-01-01")


def test_indexed_use_arrow_text_attr_unchanged() -> None:
    """indexed() with use_arrow=True: text attributes (no granularity) stay as strings."""
    # Use a fixture that has a plain text attribute (region).
    if "dim_r_m" not in _cases():
        pytest.skip("fixture dim_r_m not available")
    table, _, _ = _load_case("dim_r_m")
    columns = {"price": "metric/price", "order_amount": "metric/order_amount"}
    index_by = {"region": "label/region"}
    mock_sdk, _, _ = _mock_execution(table, columns, index_by)

    gdf = DataFrameFactory(mock_sdk, "workspace", use_arrow=True)
    df = gdf.indexed(index_by=index_by, columns=columns)

    # All index values should be plain strings.
    assert all(isinstance(v, str) for v in df.index.tolist())


def test_indexed_use_arrow_empty_result_preserves_structure() -> None:
    """indexed(use_arrow=True) on a zero-row Arrow table returns empty DataFrame with correct names."""
    model_meta = {
        "labels": {"region": {"granularity": None, "labelTitle": "Region", "primaryLabelId": "region"}},
        "requestedShape": {"metrics": ["revenue"]},
        "metrics": {"revenue": {"title": "Revenue"}},
    }
    xtab_meta = {
        "labelMetadata": {"l0": {"labelId": "region", "primaryLabelId": "region"}},
        "computedShape": {"rows": [], "cols": [], "metrics": ["m0"]},
        "totalsMetadata": {},
    }
    schema_meta = {
        b"x-gdc-model-v1": json.dumps(model_meta).encode(),
        b"x-gdc-xtab-v1": json.dumps(xtab_meta).encode(),
        b"x-gdc-view-v1": json.dumps({"isTransposed": False}).encode(),
    }
    gdc_metric = {b"gdc": json.dumps({"type": "metric", "index": 0}).encode()}
    schema = pa.schema(
        [
            pa.field("__row_type", pa.int8()),
            pa.field("region", pa.string()),
            pa.field("metric_group_0", pa.float64(), metadata=gdc_metric),
        ],
        metadata=schema_meta,
    )
    empty_table = pa.table(
        {
            "__row_type": pa.array([], type=pa.int8()),
            "region": pa.array([], type=pa.string()),
            "metric_group_0": pa.array([], type=pa.float64()),
        },
        schema=schema,
    )

    columns = {"revenue": "metric/revenue"}
    index_by = {"reg": "label/region"}
    mock_sdk, _, _ = _mock_execution(empty_table, columns, index_by)

    gdf = DataFrameFactory(mock_sdk, "workspace", use_arrow=True)
    df = gdf.indexed(index_by=index_by, columns=columns)

    assert len(df) == 0
    assert list(df.columns) == ["revenue"]
    assert df.index.name == "reg"


def test_extract_from_arrow_without_pyarrow_raises_import_error() -> None:
    """_extract_from_arrow raises ImportError (not NameError) when pyarrow is unavailable."""
    original = _da._ARROW_IMPORT_ERROR
    try:
        _da._ARROW_IMPORT_ERROR = ImportError("pyarrow not installed")
        with pytest.raises(ImportError, match="pyarrow"):
            _da._extract_from_arrow(MagicMock(), [], {}, {}, {})
    finally:
        _da._ARROW_IMPORT_ERROR = original


def test_parse_schema_metadata_non_utf8_key_is_skipped() -> None:
    """_parse_schema_metadata skips non-UTF-8 byte keys without raising UnicodeDecodeError."""
    if "dim_r_m" not in _cases():
        pytest.skip("fixture dim_r_m not available")
    table, _, _ = _load_case("dim_r_m")
    non_utf8_meta = {b"\xff\xfe": b"some value", **table.schema.metadata}
    table_with_bad_key = table.replace_schema_metadata(non_utf8_meta)
    # Should not raise despite the non-UTF-8 key.
    df = convert_arrow_table_to_dataframe(table_with_bad_key)
    assert df is not None


def test_build_inline_index_total_row_numeric_label_uses_agg_name() -> None:
    """Total rows with non-string (numeric/null) label values are replaced with the aggregation name."""
    table = pa.table(
        {
            "__row_type": pa.array([0, 2], type=pa.int8()),
            "year": pa.array([2023.0, None], type=pa.float64()),
            # Data row has no total ref; total row refers to "t0" in totalsMetadata.
            "__total_ref": pa.array([None, [0]], type=pa.list_(pa.int32())),
        }
    )
    xtab_meta = {
        "labelMetadata": {"l0": {"labelId": "year", "primaryLabelId": "year"}},
        "totalsMetadata": {"t0": {"aggregation": "sum", "rowLabels": []}},
    }
    model_meta = {
        "labels": {"year": {"labelTitle": "Year"}},
        "requestedShape": {"metrics": []},
    }
    idx = _build_inline_index(
        table,
        row_label_refs=["l0"],
        label_ref_to_id={"l0": "year"},
        model_meta=model_meta,
        xtab_meta=xtab_meta,
    )
    assert idx is not None
    assert idx[0] == 2023.0
    assert idx[1] == "SUM"


def test_arrow_config_max_bytes_forwarded_to_read_result_arrow() -> None:
    """ArrowConfig.max_bytes is passed through to read_result_arrow() by for_exec_def_arrow()."""
    if "dim_r_m" not in _cases():
        pytest.skip("fixture dim_r_m not available")
    table, _, meta = _load_case("dim_r_m")

    mock_exec = MagicMock()
    mock_exec.bare_exec_response.read_result_arrow.return_value = table
    mock_exec.bare_exec_response.dimensions = meta["dimensions"]
    mock_sdk = MagicMock()
    mock_sdk.compute.for_exec_def.return_value = mock_exec

    gdf = DataFrameFactory(mock_sdk, "workspace", arrow_config=ArrowConfig(max_bytes=10_000_000))
    gdf.for_exec_def_arrow(MagicMock(spec=ExecutionDefinition))

    mock_exec.bare_exec_response.read_result_arrow.assert_called_once_with(max_bytes=10_000_000)


def test_arrow_config_max_bytes_raises_when_exceeded() -> None:
    """ResultSizeBytesLimitExceeded from read_result_arrow propagates out of for_exec_def_arrow()."""
    mock_exec = MagicMock()
    mock_exec.bare_exec_response.read_result_arrow.side_effect = ResultSizeBytesLimitExceeded(100, 200)
    mock_sdk = MagicMock()
    mock_sdk.compute.for_exec_def.return_value = mock_exec

    gdf = DataFrameFactory(mock_sdk, "workspace", arrow_config=ArrowConfig(max_bytes=100))
    with pytest.raises(ResultSizeBytesLimitExceeded):
        gdf.for_exec_def_arrow(MagicMock(spec=ExecutionDefinition))


def test_build_inline_index_multiple_total_ref_columns_warns(caplog: pytest.LogCaptureFixture) -> None:
    """_build_inline_index warns when the Arrow table has more than one __total_ref* column."""
    table = pa.table(
        {
            "__row_type": pa.array([0, 2], type=pa.int8()),
            "region": pa.array(["East", "sum"], type=pa.string()),
            "__total_ref": pa.array([None, [0]], type=pa.list_(pa.int32())),
            "__total_ref_x": pa.array([None, [0]], type=pa.list_(pa.int32())),
        }
    )
    xtab_meta = {
        "labelMetadata": {"l0": {"labelId": "region", "primaryLabelId": "region"}},
        "totalsMetadata": {"t0": {"aggregation": "sum", "rowLabels": []}},
    }
    model_meta = {"labels": {"region": {"labelTitle": "Region"}}, "requestedShape": {"metrics": []}}

    with caplog.at_level(logging.WARNING, logger="gooddata_pandas.arrow_convertor"):
        idx = _build_inline_index(table, ["l0"], {"l0": "region"}, model_meta, xtab_meta)

    assert idx is not None
    assert idx[1] == "SUM"
    assert any("__total_ref" in msg for msg in caplog.messages)


def test_compute_row_totals_indexes_no_matching_dim_warns(caplog: pytest.LogCaptureFixture) -> None:
    """compute_row_totals_indexes warns when execution_dims is non-empty but no dim contains the row labels."""
    if "dim_r_m" not in _cases():
        pytest.skip("fixture dim_r_m not available")
    table, _, _ = _load_case("dim_r_m")
    bogus_dims = [{"headers": [{"measureGroupHeaders": [{"localIdentifier": "price"}]}]}]

    with caplog.at_level(logging.WARNING, logger="gooddata_pandas.arrow_convertor"):
        result = compute_row_totals_indexes(table, bogus_dims)

    assert result == []
    assert any("row label IDs" in msg for msg in caplog.messages)


def test_read_result_arrow_max_bytes_raises_when_exceeded() -> None:
    """read_result_arrow raises ResultSizeBytesLimitExceeded when the payload exceeds max_bytes."""
    # Build a valid Arrow IPC payload to pass through open_stream.
    tiny_table = pa.table({"x": pa.array([1, 2, 3], type=pa.int32())})
    buf = io.BytesIO()
    with ipc.new_stream(buf, tiny_table.schema) as writer:
        writer.write_table(tiny_table)
    payload = buf.getvalue()

    mock_response = MagicMock()
    mock_response.read.return_value = payload

    mock_api_client = MagicMock()
    mock_api_client.call_api.return_value = mock_response

    bare = object.__new__(BareExecutionResponse)
    bare._actions_api = MagicMock()
    bare._actions_api.api_client = mock_api_client
    bare._workspace_id = "ws"
    bare._exec_response = {"links": {"executionResult": "result-id"}}
    bare._cancel_token = None

    # Below limit: succeeds and returns the table.
    result = bare.read_result_arrow(max_bytes=len(payload) + 1000)
    assert result.num_rows == 3

    # At or below payload size: raises.
    with pytest.raises(ResultSizeBytesLimitExceeded) as exc_info:
        bare.read_result_arrow(max_bytes=1)
    assert exc_info.value.result_size_bytes_limit == 1
    assert exc_info.value.actual_result_bytes_size == len(payload)


def test_indexed_use_arrow_mixed_date_and_text_index() -> None:
    """indexed() with use_arrow=True: date attr → Timestamp, text attr → str in MultiIndex."""
    n = 3
    year_values = ["2023", "2024", "2025"]
    region_values = ["East", "West", "South"]

    model_meta = {
        "labels": {
            "date.year": {
                "granularity": "year",
                "labelTitle": "Year",
                "labelType": None,
                "primaryLabelId": "date.year",
                "attributeId": "date.year",
            },
            "region": {
                "granularity": None,
                "labelTitle": "Region",
                "labelType": "TEXT",
                "primaryLabelId": "region",
                "attributeId": "region",
            },
        },
        "requestedShape": {"metrics": ["revenue"]},
        "metrics": {"revenue": {"title": "Revenue"}},
    }
    xtab_meta = {
        "labelMetadata": {
            "l0": {"labelId": "date.year", "primaryLabelId": "date.year"},
            "l1": {"labelId": "region", "primaryLabelId": "region"},
        },
        "computedShape": {"metrics": ["m0"], "rows": [], "cols": []},
        "totalsMetadata": {},
    }
    schema_meta = {
        b"x-gdc-model-v1": json.dumps(model_meta).encode(),
        b"x-gdc-xtab-v1": json.dumps(xtab_meta).encode(),
        b"x-gdc-view-v1": json.dumps({"isTransposed": False}).encode(),
    }
    gdc_metric = {b"gdc": json.dumps({"type": "metric", "index": 0}).encode()}
    schema = pa.schema(
        [
            pa.field("__row_type", pa.int8()),
            pa.field("date.year", pa.string()),
            pa.field("region", pa.string()),
            pa.field("metric_group_0", pa.float64(), metadata=gdc_metric),
        ],
        metadata=schema_meta,
    )
    table = pa.table(
        {
            "__row_type": pa.array([0] * n, type=pa.int8()),
            "date.year": pa.array(year_values, type=pa.string()),
            "region": pa.array(region_values, type=pa.string()),
            "metric_group_0": pa.array([10.0, 20.0, 30.0], type=pa.float64()),
        },
        schema=schema,
    )

    columns = {"revenue": "metric/revenue"}
    index_by = {"year": "label/date.year", "region": "label/region"}
    mock_sdk, _, _ = _mock_execution(table, columns, index_by)

    gdf = DataFrameFactory(mock_sdk, "workspace", use_arrow=True)
    df = gdf.indexed(index_by=index_by, columns=columns)

    assert isinstance(df.index, pandas.MultiIndex)
    year_level = df.index.get_level_values("year").tolist()
    region_level = df.index.get_level_values("region").tolist()
    assert year_level == [
        pandas.Timestamp("2023-01-01"),
        pandas.Timestamp("2024-01-01"),
        pandas.Timestamp("2025-01-01"),
    ]
    assert region_level == ["East", "West", "South"]
