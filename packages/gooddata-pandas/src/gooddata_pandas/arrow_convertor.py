# (C) 2026 GoodData Corporation
from __future__ import annotations

import logging
from typing import Callable

import orjson
import pandas
from gooddata_sdk.type_converter import AttributeConverterStore

from gooddata_pandas.arrow_types import TypesMapper

try:
    import pyarrow as pa
except ImportError as _exc:
    raise ImportError(
        "pyarrow is required for Arrow support. Install it with: pip install gooddata-pandas[arrow]"
    ) from _exc

# Strings-only mapper: Arrow-backed StringDtype for both string variants.
# Memory and speed win on string columns; all other types stay as default
# (float64, object) — fully backward compatible with the JSON execution path.
_ARROW_STRINGS_MAPPER: dict = {
    pa.string(): pandas.StringDtype("pyarrow"),
    pa.large_string(): pandas.StringDtype("pyarrow"),
}

# Schema metadata keys written by the GoodData /binary endpoint.
_META_XTAB = "x-gdc-xtab-v1"
_META_MODEL = "x-gdc-model-v1"
_META_VIEW = "x-gdc-view-v1"

# Control columns present in every GoodData Arrow table.
_COL_ROW_TYPE = "__row_type"
_COL_TOTAL_REF_PREFIX = "__total_ref"

# Data-field name prefixes (metric_group_N / grand_total_N).
_FIELD_METRIC_GROUP = "metric_group_"
_FIELD_GRAND_TOTAL = "grand_total_"

# gdc field-metadata type discriminator values.
_GDC_TYPE_METRIC = "metric"
_GDC_TYPE_TOTAL = "total"

_REQUIRED_SCHEMA_KEYS = (_META_XTAB, _META_MODEL, _META_VIEW)

logger = logging.getLogger(__name__)


def read_model_labels(table: pa.Table) -> dict:
    """Return the ``labels`` dict from the Arrow table's ``x-gdc-model-v1`` schema metadata.

    Returns an empty dict when the metadata key is absent so callers can use it
    unconditionally without extra None-checks.
    """
    if not table.schema.metadata or b"x-gdc-model-v1" not in table.schema.metadata:
        return {}
    return orjson.loads(table.schema.metadata[b"x-gdc-model-v1"]).get("labels", {})


def _get_date_converter_for_label(label_id: str, model_labels: dict):
    """Return a type Converter for date-granularity labels, or None for plain text attributes.

    Reads the ``granularity`` field from Arrow model metadata (``x-gdc-model-v1``) and
    looks up the matching converter in ``AttributeConverterStore``.

    - ``DAY`` / ``MONTH`` / ``YEAR`` → ``DateConverter``  (→ ``pandas.Timestamp`` via external fn)
    - ``WEEK`` / ``QUARTER``         → ``StringConverter`` (no-op)
    - ``MINUTE`` / ``HOUR``          → ``DatetimeConverter``
    - No granularity (text attrs)    → ``None`` (caller skips conversion)
    """
    info = model_labels.get(label_id, {})
    granularity = info.get("granularity")
    if not granularity:
        return None
    return AttributeConverterStore.find_converter("DATE", granularity.upper())


def convert_label_values(label_id: str, values: list, model_labels: dict) -> list:
    """Apply date-granularity type conversion to a list of attribute values from an Arrow column.

    Mirrors the non-Arrow execution path (``AttributeConverterStore`` in ``_typed_attribute_value``):

    - ``DAY`` / ``MONTH`` / ``YEAR`` granularity → ``pandas.Timestamp``
    - ``WEEK`` / ``QUARTER``                     → ``str`` (unchanged)
    - No granularity (text attributes)            → values returned as the **same object**

    ``None`` values are passed through unchanged.

    Args:
        label_id:     Arrow column name / GoodData label local ID.
        values:       Raw values from ``table.column(label_id).to_pylist()``.
        model_labels: The ``labels`` dict from ``x-gdc-model-v1`` schema metadata
                      (as returned by :func:`read_model_labels`).

    Returns:
        Converted list, or the original *values* object when no conversion is needed.
    """
    converter = _get_date_converter_for_label(label_id, model_labels)
    if converter is None:
        return values
    return [converter.to_external_type(v) if v is not None else None for v in values]


def build_metric_field_index(table: pa.Table) -> dict[int, str]:
    """Return {metric_dimension_index: arrow_field_name} from the table schema.

    Scans fields whose names start with the ``metric_group_`` prefix and reads
    the ``gdc["index"]`` value from their field-level metadata.  The resulting
    dict maps the zero-based metric dimension index to the Arrow field name,
    which is needed to look up the correct column when the caller knows only the
    position of a metric in the execution definition.
    """
    result: dict[int, str] = {}
    for field in table.schema:
        if field.name.startswith(_FIELD_METRIC_GROUP) and field.metadata and b"gdc" in field.metadata:
            gdc = orjson.loads(field.metadata[b"gdc"])
            if "index" not in gdc:
                raise ValueError(
                    f"Metric field {field.name!r} 'gdc' metadata is missing required key 'index'. "
                    "The Arrow table must originate from the GoodData /binary execution endpoint."
                )
            result[gdc["index"]] = field.name
    return result


def _parse_schema_metadata(table: pa.Table) -> dict:
    """
    Decode and return all GoodData schema metadata keys from an Arrow table.

    Raises ValueError when metadata is absent or either required key is missing.
    Both x-gdc-xtab-v1 and x-gdc-model-v1 must be present to build a DataFrame;
    without them the index, column names, and metric titles cannot be reconstructed.
    """
    if not table.schema.metadata:
        raise ValueError(
            "Arrow table has no schema metadata. Expected GoodData metadata keys: " + ", ".join(_REQUIRED_SCHEMA_KEYS)
        )
    schema_meta = {}
    for _k, _v in table.schema.metadata.items():
        try:
            _k_str = _k.decode()
        except UnicodeDecodeError:
            continue
        if _k_str in _REQUIRED_SCHEMA_KEYS:
            schema_meta[_k_str] = orjson.loads(_v)
    missing = [k for k in _REQUIRED_SCHEMA_KEYS if k not in schema_meta]
    if missing:
        raise ValueError(
            f"Arrow table schema metadata is missing required key(s): {', '.join(missing)}. "
            "The table must originate from the GoodData /binary execution endpoint."
        )
    return schema_meta


def _get_row_types(table: pa.Table) -> list:
    """
    Return the __row_type column as a Python list.

    Raises ValueError when the column is absent — it is a required control column
    in every GoodData Arrow table (0=data, 1/2=total).
    """
    if _COL_ROW_TYPE not in table.schema.names:
        raise ValueError(
            f"Arrow table is missing required control column '{_COL_ROW_TYPE}'. "
            "The table must originate from the GoodData /binary execution endpoint."
        )
    return table.column(_COL_ROW_TYPE).to_pylist()


def _label_ref_to_id_map(xtab_meta: dict) -> dict[str, str]:
    """Map 'l0', 'l1', ... to actual label local IDs."""
    return {ref: info["labelId"] for ref, info in xtab_meta["labelMetadata"].items()}


def _get_computed_shape(xtab_meta: dict) -> dict:
    """Return computedShape from xtab metadata, raising ValueError when absent."""
    computed_shape = xtab_meta.get("computedShape")
    if computed_shape is None:
        raise ValueError(
            "Arrow table xtab metadata is missing required key 'computedShape'. "
            "The table must originate from the GoodData /binary execution endpoint."
        )
    return computed_shape


def _label_title(label_id: str, model_meta: dict) -> str:
    """Get the display title for a label from model metadata."""
    info = model_meta["labels"].get(label_id, {})
    return info.get("labelTitle") or info.get("attributeTitle") or label_id


def _metric_title(metric_idx: int, model_meta: dict, xtab_meta: dict) -> str:
    """
    Get the display title for a metric by its Arrow index (0 = m0, 1 = m1, ...).

    Matches the JSON-path behaviour: use the model metadata title when present,
    otherwise fall back to the local identifier.
    """
    local_ids = model_meta["requestedShape"]["metrics"]
    if metric_idx >= len(local_ids):
        raise ValueError(
            f"metric_idx {metric_idx} is out of range for requestedShape.metrics "
            f"(length {len(local_ids)}). The Arrow schema metadata may be inconsistent "
            "with the model metadata."
        )
    local_id = local_ids[metric_idx]
    info = model_meta["metrics"].get(local_id, {})
    return info.get("title") or local_id


def _apply_label_override(base_title: str, local_id: str, overrides: dict) -> str:
    """
    Return the override title for local_id when present, otherwise base_title.

    overrides is either label_overrides["labels"] or label_overrides["metrics"].
    """
    return overrides.get(local_id, {}).get("title", base_title)


def _build_inline_index(
    table: pa.Table,
    row_label_refs: list[str],
    label_ref_to_id: dict[str, str],
    model_meta: dict,
    xtab_meta: dict,
    resolved_mapper: Callable | None = None,
    label_overrides: dict | None = None,
) -> pandas.Index | None:
    """
    Build the pandas index from Arrow row attribute columns.

    Arrow rows encode either normal data (row_type=0) or totals (row_type=2).
    For total rows the primary label column contains the lowercase aggregation
    function name (e.g. 'sum'); secondary label columns that cover deeper levels
    may be empty string — both are filled with the uppercased aggregation name.

    Returns None when there are no row attribute labels (e.g. metrics-only results).
    """
    if not row_label_refs:
        return None

    col_ids = [label_ref_to_id[ref] for ref in row_label_refs]
    row_types = _get_row_types(table)

    # Build a per-row aggregation-name lookup for total rows.
    # totalsMetadata maps "t0", "t1", ... → {aggregation: "sum", ...}
    # __total_ref column (may carry a Unicode suffix) maps each row to the
    # indices of the totals it belongs to.
    totals_meta = xtab_meta.get("totalsMetadata", {})
    total_ref_vals: list = [None] * table.num_rows
    if totals_meta:
        total_ref_cols = [f.name for f in table.schema if f.name.startswith(_COL_TOTAL_REF_PREFIX)]
        if total_ref_cols:
            if len(total_ref_cols) > 1:
                logger.warning(
                    "Arrow table has %d __total_ref* columns; only %r is used for aggregation names.",
                    len(total_ref_cols),
                    total_ref_cols[0],
                )
            total_ref_vals = table.column(total_ref_cols[0]).to_pylist()

    # Precompute per-row aggregation name and kept-label set for total rows.
    agg_for_row: list[str | None] = [None] * table.num_rows
    kept_labels_for_row: list[frozenset] = [frozenset()] * table.num_rows
    for i, rt in enumerate(row_types):
        if rt == 0:
            continue

        refs = total_ref_vals[i]
        if not refs:
            continue
        key = f"t{refs[0]}"
        entry = totals_meta.get(key, {})
        agg = entry.get("aggregation")
        agg_for_row[i] = agg.upper() if agg else None
        kept_labels_for_row[i] = frozenset(entry.get("rowLabels", []))

    arrays: list[list] = []
    for ref, lid in zip(row_label_refs, col_ids):
        values = table.column(lid).to_pylist()
        processed = []
        for i, v in enumerate(values):
            if row_types[i] != 0:
                if isinstance(v, str):
                    if ref in kept_labels_for_row[i]:
                        processed.append(v)
                    elif v == "":
                        processed.append(agg_for_row[i] if agg_for_row[i] else v)
                    else:
                        processed.append(v.upper())
                else:
                    # Non-string value in a total row — replace with the aggregation name when available.
                    processed.append(agg_for_row[i] if agg_for_row[i] is not None else v)
            else:
                processed.append(v)
        arrays.append(processed)

    attr_overrides = (label_overrides or {}).get("labels", {})
    names = [_apply_label_override(_label_title(lid, model_meta), lid, attr_overrides) for lid in col_ids]

    # Apply resolved_mapper to the string arrays if provided.
    string_dtype = resolved_mapper(pa.string()) if resolved_mapper else None
    typed_arrays = [pandas.array(arr, dtype=string_dtype) for arr in arrays] if string_dtype else arrays

    # A single-level MultiIndex is indistinguishable from a flat Index for the
    # JSON-path output, so return a plain Index in that case.
    if len(col_ids) == 1:
        return pandas.Index(typed_arrays[0], name=names[0])
    return pandas.MultiIndex.from_arrays(typed_arrays, names=names)


def _build_field_index(
    data_fields: list,
    col_label_refs: list[str],
    label_ref_to_id: dict[str, str],
    model_meta: dict,
    xtab_meta: dict,
    label_overrides: dict | None = None,
) -> pandas.Index:
    """
    Build the pandas index from Arrow field (column) metadata.

    Each data field (metric_group_N or grand_total_N) encodes one combination of
    column-attribute label values plus a metric, stored in the 'gdc' field metadata key.

    For metric_group_N:
        gdc = {"type": "metric", "index": N, "label_values": [...], ...}
        → tuple: (*label_values, metric_title)

    For grand_total_N (subtotals):
        gdc = {"type": "total", "agg_function": "sum", "metric_index": N,
               "label_values": [...], ...}
        where label_values may be partial (covers only the outer label levels).
        → tuple: (*label_values, AGG, ..., AGG, metric_title)
          (remaining levels padded with the uppercased aggregation name)

    When there are no column labels (metrics-only dimension) the index is a flat
    Index of metric titles rather than a MultiIndex.
    """
    n_col_labels = len(col_label_refs)
    col_label_ids = [label_ref_to_id[ref] for ref in col_label_refs]
    attr_overrides = (label_overrides or {}).get("labels", {})
    metric_overrides = (label_overrides or {}).get("metrics", {})
    metric_local_ids: list[str] = model_meta.get("requestedShape", {}).get("metrics", [])

    tuples: list = []
    for field in data_fields:
        if not field.metadata or b"gdc" not in field.metadata:
            raise ValueError(
                f"Data field {field.name!r} is missing required 'gdc' field metadata. "
                "The Arrow table must originate from the GoodData /binary execution endpoint."
            )
        gdc = orjson.loads(field.metadata[b"gdc"])
        label_values: list = list(gdc.get("label_values", []))

        gdc_type = gdc.get("type")
        if gdc_type is None:
            raise ValueError(
                f"Data field {field.name!r} 'gdc' metadata is missing required key 'type'. "
                "The Arrow table must originate from the GoodData /binary execution endpoint."
            )
        if gdc_type == _GDC_TYPE_METRIC:
            if "index" not in gdc:
                raise ValueError(f"Metric field {field.name!r} 'gdc' metadata is missing required key 'index'.")
            metric_idx = gdc["index"]
        else:  # "total"
            for _key in ("metric_index", "agg_function"):
                if _key not in gdc:
                    raise ValueError(f"Total field {field.name!r} 'gdc' metadata is missing required key {_key!r}.")
            metric_idx = gdc["metric_index"]
            agg = gdc["agg_function"].upper()
            # Truncate to n_col_labels first (guard against malformed schema),
            # then pad remaining column-label levels with the aggregation name.
            label_values = label_values[:n_col_labels] + [agg] * (n_col_labels - min(len(label_values), n_col_labels))

        m_title = _metric_title(metric_idx, model_meta, xtab_meta)
        if metric_overrides and metric_idx < len(metric_local_ids):
            m_title = _apply_label_override(m_title, metric_local_ids[metric_idx], metric_overrides)

        if n_col_labels == 0:
            tuples.append(m_title)
        else:
            tuples.append(tuple(label_values) + (m_title,))

    if n_col_labels == 0:
        # No column attribute labels — just a flat Index of metric names
        return pandas.Index(tuples, name=None)

    names = [_apply_label_override(_label_title(lid, model_meta), lid, attr_overrides) for lid in col_label_ids] + [
        None
    ]
    return pandas.MultiIndex.from_tuples(tuples, names=names)


def _wrap_for_columns(idx: pandas.Index | None) -> pandas.Index | None:
    """
    Wrap a plain flat Index as 1-tuples when it is used as the DataFrame column
    index.  The JSON-path output always uses at least 1-tuples for column labels
    so that the shape is consistent regardless of how many attribute levels are
    present.  MultiIndex (2+ levels) and None (→ RangeIndex) are returned as-is.
    """
    if idx is None or isinstance(idx, pandas.MultiIndex):
        return idx
    return pandas.Index([(v,) for v in idx])


def reorder_grand_totals(
    table: pa.Table,
    grand_totals_position: str | None,
) -> pa.Table:
    """
    Move grand total rows (``__row_type == 2``) to the top or leave them at the bottom.

    Subtotal rows (``__row_type == 1``) are not repositioned — they remain adjacent to
    their data group.  No-op when ``grand_totals_position`` is not ``"top"`` or
    ``"pinnedTop"``, or when the table has no ``__row_type`` column (no row totals).
    """
    if grand_totals_position not in ("top", "pinnedTop"):
        return table
    if _COL_ROW_TYPE not in table.schema.names:
        return table
    row_type_vals = table.column(_COL_ROW_TYPE).to_pylist()
    grand_mask = pa.array([v == 2 for v in row_type_vals], type=pa.bool_())
    grand_total_rows = table.filter(grand_mask)
    if grand_total_rows.num_rows == 0:
        return table
    data_and_sub_rows = table.filter(pa.array([v != 2 for v in row_type_vals], type=pa.bool_()))
    return pa.concat_tables([grand_total_rows, data_and_sub_rows])


def compute_column_totals_indexes(table: pa.Table, execution_dims: list) -> list[list[int]]:
    """
    Compute column_totals_indexes compatible with DataFrameMetadata from an Arrow table.

    Returns a list with one inner list per header level in the output-column dimension,
    matching the JSON-path DataFrameMetadata.column_totals_indexes format.  Each inner
    list contains the zero-based positions of total columns at that header level.

    Non-transposed case (Arrow fields = output columns):
        grand_total_* fields at position k are a column total at attribute level j when
        ``j >= len(gdc["label_values"])`` (the field aggregates that level and beyond).

    Transposed / metrics-only case (Arrow fields = output rows):
        grand_total_* fields become output rows and are already covered by
        compute_row_totals_indexes.  Returns [] in that case.
    """
    schema_meta = _parse_schema_metadata(table)
    xtab_meta = schema_meta[_META_XTAB]
    is_transposed = schema_meta[_META_VIEW]["isTransposed"]

    computed_shape = _get_computed_shape(xtab_meta)
    row_label_refs: list[str] = computed_shape.get("rows", [])
    col_label_refs: list[str] = computed_shape.get("cols", [])

    # In the transposed / metrics-only layout grand_total_* fields become output rows
    # (handled by compute_row_totals_indexes) → nothing to do here.
    if is_transposed or not row_label_refs:
        return []

    all_data_fields = [
        f for f in table.schema if f.name.startswith(_FIELD_METRIC_GROUP) or f.name.startswith(_FIELD_GRAND_TOTAL)
    ]

    # No grand_total_* fields → no column totals.
    if not any(f.name.startswith(_FIELD_GRAND_TOTAL) for f in table.schema):
        return []

    label_ref_to_id = _label_ref_to_id_map(xtab_meta)
    id_to_ref = {v: k for k, v in label_ref_to_id.items()}
    col_ref_set = set(col_label_refs)

    def _label_ids_in_dim(dim: dict) -> set:
        return {h["attributeHeader"]["label"]["id"] for h in dim.get("headers", []) if "attributeHeader" in h}

    # Find the column execution dimension.
    if col_label_refs:
        col_ref_label_ids = {label_ref_to_id[r] for r in col_label_refs}
        col_dim = next(
            (dim for dim in execution_dims if col_ref_label_ids <= _label_ids_in_dim(dim)),
            {},
        )
        if not col_dim and execution_dims:
            logger.warning(
                "No execution dimension contains column label IDs %s; column_totals_indexes will be empty.",
                col_ref_label_ids,
            )
    else:
        col_dim = next(
            (dim for dim in execution_dims if any("measureGroupHeaders" in h for h in dim.get("headers", []))),
            {},
        )

    # Pre-parse gdc metadata once to avoid O(N×M) orjson.loads calls in the header loop.
    parsed_gdcs: list[dict | None] = [
        orjson.loads(f.metadata[b"gdc"]) if f.metadata and b"gdc" in f.metadata else None for f in all_data_fields
    ]

    result: list[list[int]] = []
    attr_level = 0
    for header in col_dim.get("headers", []):
        if "measureGroupHeaders" in header:
            result.append([])
        else:
            label_id = header["attributeHeader"]["label"]["id"]
            ref = id_to_ref.get(label_id)
            if ref is None or ref not in col_ref_set:
                result.append([])
            else:
                j = attr_level
                total_idxs = [
                    k
                    for k, gdc in enumerate(parsed_gdcs)
                    if gdc is not None and gdc["type"] == _GDC_TYPE_TOTAL and j >= len(gdc.get("label_values", []))
                ]
                result.append(total_idxs)
                attr_level += 1
    return result


def compute_row_totals_indexes(table: pa.Table, execution_dims: list) -> list[list[int]]:
    """
    Compute row_totals_indexes compatible with DataFrameMetadata from an Arrow table.

    Returns a list with one inner list per header column in the output-row dimension,
    matching the JSON-path DataFrameMetadata.row_totals_indexes format (one slot per
    dimension header, including the measureGroup placeholder which always → []).

    Non-transposed case (Arrow rows = output rows):
        Every Arrow row with __row_type != 0 is a total row; it appears in the
        total-indexes list for every attribute-level header in the row dimension.

    Transposed / metrics-only case (Arrow fields = output rows):
        Total rows are grand_total_N fields.  A field is total at level j only when
        j >= len(gdc["label_values"]), i.e. that label level is being aggregated.
    """
    schema_meta = _parse_schema_metadata(table)
    xtab_meta = schema_meta[_META_XTAB]
    is_transposed = schema_meta[_META_VIEW]["isTransposed"]

    computed_shape = _get_computed_shape(xtab_meta)
    row_label_refs: list[str] = computed_shape.get("rows", [])
    col_label_refs: list[str] = computed_shape.get("cols", [])
    label_ref_to_id = _label_ref_to_id_map(xtab_meta)
    id_to_ref = {v: k for k, v in label_ref_to_id.items()}

    use_field_rows = is_transposed or not row_label_refs
    output_row_refs = col_label_refs if use_field_rows else row_label_refs
    output_row_ref_set = set(output_row_refs)

    # Find which execution dimension contains the output-row attribute refs.
    # Use attributeHeader["label"]["id"] (GoodData label object ID) which matches
    # the labelId values in the Arrow labelMetadata — not localIdentifier, which is
    # the user-given alias and may differ.
    def _label_ids_in_dim(dim: dict) -> set:
        return {h["attributeHeader"]["label"]["id"] for h in dim.get("headers", []) if "attributeHeader" in h}

    if output_row_refs:
        ref_label_ids = {label_ref_to_id[r] for r in output_row_refs}
        row_dim = next(
            (dim for dim in execution_dims if ref_label_ids <= _label_ids_in_dim(dim)),
            {},
        )
        if not row_dim and execution_dims:
            logger.warning(
                "No execution dimension contains row label IDs %s; row_totals_indexes will be empty.",
                ref_label_ids,
            )
    else:
        # Metrics-only: the dimension containing measureGroupHeaders is the output-row dim.
        row_dim = next(
            (dim for dim in execution_dims if any("measureGroupHeaders" in h for h in dim.get("headers", []))),
            {},
        )

    if use_field_rows:
        # Output rows are the data fields in schema order.
        all_data_fields = [
            f for f in table.schema if f.name.startswith(_FIELD_METRIC_GROUP) or f.name.startswith(_FIELD_GRAND_TOTAL)
        ]

        # Pre-parse gdc metadata once to avoid O(N×M) orjson.loads calls in the header loop.
        parsed_gdcs: list[dict | None] = [
            orjson.loads(f.metadata[b"gdc"]) if f.metadata and b"gdc" in f.metadata else None for f in all_data_fields
        ]

        result: list[list[int]] = []
        attr_level = 0  # position within output_row_refs
        for header in row_dim.get("headers", []):
            if "measureGroupHeaders" in header:
                result.append([])
            else:
                label_id = header["attributeHeader"]["label"]["id"]
                ref = id_to_ref.get(label_id)
                if ref is None or ref not in output_row_ref_set:
                    result.append([])
                else:
                    j = attr_level
                    total_idxs = [
                        k
                        for k, gdc in enumerate(parsed_gdcs)
                        if gdc is not None and gdc["type"] == _GDC_TYPE_TOTAL and j >= len(gdc.get("label_values", []))
                    ]
                    result.append(total_idxs)
                    attr_level += 1
        return result

    else:
        # Output rows are Arrow rows; every total row (row_type != 0) is listed
        # in the total-indexes for every attribute level.
        row_types = _get_row_types(table)
        total_row_idxs = [i for i, rt in enumerate(row_types) if rt != 0]

        result = []
        for header in row_dim.get("headers", []):
            if "measureGroupHeaders" in header:
                result.append([])
            else:
                label_id = header["attributeHeader"]["label"]["id"]
                ref = id_to_ref.get(label_id)
                if ref is None or ref not in output_row_ref_set:
                    result.append([])
                else:
                    result.append(total_row_idxs)
        return result


def _compute_primary_labels_from_inline(
    table: pa.Table,
    label_refs: list[str],
    label_ref_to_id: dict[str, str],
    xtab_meta: dict,
) -> dict[int, dict[str, str]]:
    """Build primary_labels mapping from Arrow row-attribute columns.

    For each attribute level j the result maps primary_label_value → display_label_value
    for every data row (row_type==0).  Total rows are excluded because their column
    values are aggregation-function markers, not real attribute values.

    When primaryLabelId == labelId the mapping is identity ({v: v}).
    When they differ the function looks for a separate Arrow column named
    primaryLabelId; failing that it falls back to identity.
    """
    result: dict[int, dict[str, str]] = {}
    label_meta = xtab_meta.get("labelMetadata", {})
    row_types = _get_row_types(table)
    data_row_mask = [rt == 0 for rt in row_types]

    for j, ref in enumerate(label_refs):
        info = label_meta.get(ref, {})
        label_id = label_ref_to_id.get(ref, info.get("labelId", ""))
        primary_label_id = info.get("primaryLabelId", label_id)

        display_vals = table.column(label_id).to_pylist()

        if label_id == primary_label_id:
            mapping: dict[str, str] = {
                v: v for v, is_data in zip(display_vals, data_row_mask) if is_data and isinstance(v, str)
            }
        elif primary_label_id in table.schema.names:
            primary_vals = table.column(primary_label_id).to_pylist()
            mapping = {
                p: d
                for p, d, is_data in zip(primary_vals, display_vals, data_row_mask)
                if is_data and isinstance(p, str) and isinstance(d, str)
            }
        else:
            # Fallback: identity (primary label data not present in table)
            mapping = {v: v for v, is_data in zip(display_vals, data_row_mask) if is_data and isinstance(v, str)}

        result[j] = mapping
    return result


def _compute_primary_labels_from_fields(
    all_data_fields: list,
    n_col_labels: int,
) -> dict[int, dict[str, str]]:
    """Build primary_labels mapping from Arrow field (column) metadata.

    Each metric_group field carries gdc.label_values (display) and
    gdc.primary_label_values (primary) for every column-label level.  Total
    (grand_total) fields are skipped, matching the JSON-path behaviour where
    totalHeader rows do not contribute to primary_attribute_labels_mapping.
    """
    result: dict[int, dict[str, str]] = {}
    if n_col_labels == 0:
        return result

    for field in all_data_fields:
        if not field.metadata or b"gdc" not in field.metadata:
            continue
        gdc = orjson.loads(field.metadata[b"gdc"])
        if gdc["type"] != _GDC_TYPE_METRIC:
            continue
        label_values: list = gdc.get("label_values", [])
        primary_label_values: list = gdc.get("primary_label_values", [])
        for j in range(min(n_col_labels, len(label_values), len(primary_label_values))):
            display = label_values[j]
            primary = primary_label_values[j]
            if not isinstance(display, str) or not isinstance(primary, str):
                continue
            if j not in result:
                result[j] = {}
            result[j][primary] = display

    return result


def compute_primary_labels(
    table: pa.Table,
) -> tuple[dict[int, dict[str, str]], dict[int, dict[str, str]]]:
    """
    Compute primary_labels_from_index and primary_labels_from_columns from an Arrow table.

    Mirrors the primary_attribute_labels_mapping built by the JSON execution path so that
    DataFrameMetadata is fully populated by the Arrow path too.

    Returns:
        (primary_labels_from_index, primary_labels_from_columns)
    """
    schema_meta = _parse_schema_metadata(table)
    xtab_meta = schema_meta[_META_XTAB]
    is_transposed = schema_meta[_META_VIEW]["isTransposed"]

    label_ref_to_id = _label_ref_to_id_map(xtab_meta)
    computed_shape = _get_computed_shape(xtab_meta)
    row_label_refs: list[str] = computed_shape.get("rows", [])
    col_label_refs: list[str] = computed_shape.get("cols", [])

    all_data_fields = [
        f for f in table.schema if f.name.startswith(_FIELD_METRIC_GROUP) or f.name.startswith(_FIELD_GRAND_TOTAL)
    ]

    inline_primary = (
        _compute_primary_labels_from_inline(table, row_label_refs, label_ref_to_id, xtab_meta) if row_label_refs else {}
    )
    field_primary = _compute_primary_labels_from_fields(all_data_fields, len(col_label_refs))

    # Mirror convert_arrow_table_to_dataframe's orientation logic:
    #   isTransposed or no inline → field cols become output rows (index)
    if is_transposed or not row_label_refs:
        return field_primary, inline_primary
    return inline_primary, field_primary


def convert_arrow_table_to_dataframe(
    table: pa.Table,
    self_destruct: bool = False,
    types_mapper: TypesMapper = TypesMapper.DEFAULT,
    custom_mapping: dict | None = None,
    label_overrides: dict | None = None,
) -> pandas.DataFrame:
    """
    Convert a pyarrow Table returned by the GoodData /binary execution endpoint
    into a pandas DataFrame matching the output of the JSON-based execution path.

    Arrow table structure
    ---------------------
    Control columns:
        __row_type   int8   0=data row, 2=total/grand-total row
        __total_ref  list   (present only when totals exist) indices being summed

    Row attribute columns:
        One column per label in computedShape.rows, named by the label local ID.
        For total rows (row_type=2) the value is the lowercase aggregation function
        name (e.g. 'sum') — we uppercase it.

    Data columns (in schema order, may be interleaved):
        metric_group_N  double  regular data — gdc metadata has type="metric"
        grand_total_N   double  subtotals    — gdc metadata has type="total"

    Transposition
    -------------
    The server may place either the output-row dimension or the output-column
    dimension as Arrow rows. x-gdc-view-v1.isTransposed records which choice was
    made:

        isTransposed=False:
            Arrow rows  → output rows    (inline_index)
            Arrow cols  → output columns (field_index)
            data matrix stays as-is

        isTransposed=True:
            Arrow rows  → output columns (inline_index)
            Arrow cols  → output rows    (field_index)
            data matrix is transposed

    When there are no row attribute labels (inline_index is None) the field
    dimension always becomes the output rows regardless of isTransposed.
    """
    if types_mapper is TypesMapper.DEFAULT:
        resolved_mapper: Callable | None = None
    elif types_mapper is TypesMapper.ARROW_STRINGS:
        resolved_mapper = _ARROW_STRINGS_MAPPER.get
    elif types_mapper is TypesMapper.CUSTOM:
        if custom_mapping is None:
            raise ValueError("custom_mapping must be provided when types_mapper=TypesMapper.CUSTOM")
        resolved_mapper = custom_mapping.get
    else:
        raise ValueError("Unknown types_mapper value")

    schema_meta = _parse_schema_metadata(table)
    xtab_meta = schema_meta[_META_XTAB]
    model_meta = schema_meta[_META_MODEL]
    is_transposed = schema_meta[_META_VIEW]["isTransposed"]

    label_ref_to_id = _label_ref_to_id_map(xtab_meta)

    # Collect all data columns in their original schema order.
    # metric_group_N and grand_total_N may be interleaved (e.g. for subtotals
    # grouped by the outer dimension label), so preserve schema ordering.
    all_data_fields = [
        f for f in table.schema if f.name.startswith(_FIELD_METRIC_GROUP) or f.name.startswith(_FIELD_GRAND_TOTAL)
    ]

    data_field_names = [f.name for f in all_data_fields]
    data_matrix = (
        table.select(data_field_names)
        .to_pandas(self_destruct=self_destruct, types_mapper=resolved_mapper)
        .to_numpy(dtype=float, na_value=float("nan"))
    )  # shape: (n_arrow_rows, n_data_cols)

    # computedShape.rows  → label refs for Arrow row attribute columns
    # computedShape.cols  → label refs encoded in field metadata
    computed_shape = _get_computed_shape(xtab_meta)
    row_label_refs: list[str] = computed_shape.get("rows", [])
    col_label_refs: list[str] = computed_shape.get("cols", [])

    inline_index = _build_inline_index(
        table, row_label_refs, label_ref_to_id, model_meta, xtab_meta, resolved_mapper, label_overrides
    )
    field_index = _build_field_index(
        all_data_fields, col_label_refs, label_ref_to_id, model_meta, xtab_meta, label_overrides
    )

    # When there are no row attribute labels (inline_index is None) the server
    # packs everything into the field dimension; always use field_index as rows.
    if is_transposed or inline_index is None:
        return pandas.DataFrame(data_matrix.T, index=field_index, columns=_wrap_for_columns(inline_index))

    return pandas.DataFrame(data_matrix, index=inline_index, columns=_wrap_for_columns(field_index))
