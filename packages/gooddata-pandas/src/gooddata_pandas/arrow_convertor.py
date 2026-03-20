# (C) 2026 GoodData Corporation
from __future__ import annotations

import json
from typing import Optional

import pandas

try:
    import pyarrow as pa
except ImportError as _exc:
    raise ImportError(
        "pyarrow is required for Arrow support. Install it with: pip install gooddata-pandas[arrow]"
    ) from _exc


def _label_ref_to_id_map(xtab_meta: dict) -> dict[str, str]:
    """Map 'l0', 'l1', ... to actual label local IDs."""
    return {ref: info["labelId"] for ref, info in xtab_meta["labelMetadata"].items()}


def _label_title(label_id: str, model_meta: dict) -> Optional[str]:
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
    local_id = local_ids[metric_idx]
    info = model_meta["metrics"].get(local_id, {})
    return info.get("title") or local_id


def _build_inline_index(
    table: pa.Table,
    row_label_refs: list[str],
    label_ref_to_id: dict[str, str],
    model_meta: dict,
    xtab_meta: dict,
) -> Optional[pandas.Index]:
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
    row_types = table.column("__row_type").to_pylist()

    # Build a per-row aggregation-name lookup for total rows.
    # totalsMetadata maps "t0", "t1", ... → {aggregation: "sum", ...}
    # __total_ref column (may carry a Unicode suffix) maps each row to the
    # indices of the totals it belongs to.
    totals_meta = xtab_meta.get("totalsMetadata", {})
    total_ref_vals: list = [None] * table.num_rows
    if totals_meta:
        for field in table.schema:
            if field.name.startswith("__total_ref"):
                total_ref_vals = table.column(field.name).to_pylist()
                break

    # Precompute per-row aggregation name and kept-label set for total rows.
    agg_for_row: list[Optional[str]] = [None] * table.num_rows
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
            if row_types[i] != 0 and isinstance(v, str):
                if ref in kept_labels_for_row[i]:
                    # Outer label kept as real attribute value in a subtotal row.
                    processed.append(v)
                elif v == "":
                    # Aggregated level left empty by the server — fill with agg name.
                    processed.append(agg_for_row[i] if agg_for_row[i] else v)
                else:
                    # Aggregation function marker (e.g. 'sum') — uppercase it.
                    processed.append(v.upper())
            else:
                processed.append(v)
        arrays.append(processed)

    names = [_label_title(lid, model_meta) for lid in col_ids]

    # A single-level MultiIndex is indistinguishable from a flat Index for the
    # JSON-path output, so return a plain Index in that case.
    if len(col_ids) == 1:
        return pandas.Index(arrays[0], name=names[0])
    return pandas.MultiIndex.from_arrays(arrays, names=names)


def _build_field_index(
    data_fields: list,
    col_label_refs: list[str],
    label_ref_to_id: dict[str, str],
    model_meta: dict,
    xtab_meta: dict,
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

    tuples: list = []
    for field in data_fields:
        gdc = json.loads(field.metadata[b"gdc"])
        label_values: list = list(gdc.get("label_values", []))

        if gdc["type"] == "metric":
            m_title = _metric_title(gdc["index"], model_meta, xtab_meta)
        else:  # "total"
            m_title = _metric_title(gdc["metric_index"], model_meta, xtab_meta)
            agg = gdc["agg_function"].upper()
            # Pad remaining column-label levels with the aggregation name
            label_values = label_values + [agg] * (n_col_labels - len(label_values))

        if n_col_labels == 0:
            tuples.append(m_title)
        else:
            tuples.append(tuple(label_values) + (m_title,))

    if n_col_labels == 0:
        # No column attribute labels — just a flat Index of metric names
        return pandas.Index(tuples, name=None)

    names = [_label_title(lid, model_meta) for lid in col_label_ids] + [None]
    return pandas.MultiIndex.from_tuples(tuples, names=names)


def _wrap_for_columns(idx: Optional[pandas.Index]) -> Optional[pandas.Index]:
    """
    Wrap a plain flat Index as 1-tuples when it is used as the DataFrame column
    index.  The JSON-path output always uses at least 1-tuples for column labels
    so that the shape is consistent regardless of how many attribute levels are
    present.  MultiIndex (2+ levels) and None (→ RangeIndex) are returned as-is.
    """
    if idx is None or isinstance(idx, pandas.MultiIndex):
        return idx
    return pandas.Index([(v,) for v in idx])


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
    schema_meta = {k.decode(): json.loads(v) for k, v in table.schema.metadata.items()}
    xtab_meta = schema_meta["x-gdc-xtab-v1"]
    is_transposed = schema_meta["x-gdc-view-v1"]["isTransposed"]

    row_label_refs: list[str] = xtab_meta["computedShape"]["rows"]
    col_label_refs: list[str] = xtab_meta["computedShape"]["cols"]
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
            execution_dims[0] if execution_dims else {},
        )
    else:
        # Metrics-only: the dimension containing measureGroupHeaders is the output-row dim.
        row_dim = next(
            (dim for dim in execution_dims if any("measureGroupHeaders" in h for h in dim.get("headers", []))),
            execution_dims[0] if execution_dims else {},
        )

    if use_field_rows:
        # Output rows are the data fields in schema order.
        all_data_fields = [
            f for f in table.schema if f.name.startswith("metric_group_") or f.name.startswith("grand_total_")
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
                        for k, f in enumerate(all_data_fields)
                        if (gdc := json.loads(f.metadata[b"gdc"]))["type"] == "total"
                        and j >= len(gdc.get("label_values", []))
                    ]
                    result.append(total_idxs)
                    attr_level += 1
        return result

    else:
        # Output rows are Arrow rows; every total row (row_type != 0) is listed
        # in the total-indexes for every attribute level.
        row_types = table.column("__row_type").to_pylist()
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


def convert_arrow_table_to_dataframe(table: pa.Table) -> pandas.DataFrame:
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
    schema_meta = {k.decode(): json.loads(v) for k, v in table.schema.metadata.items()}
    xtab_meta = schema_meta["x-gdc-xtab-v1"]
    model_meta = schema_meta["x-gdc-model-v1"]
    is_transposed = schema_meta["x-gdc-view-v1"]["isTransposed"]

    label_ref_to_id = _label_ref_to_id_map(xtab_meta)

    # Collect all data columns in their original schema order.
    # metric_group_N and grand_total_N may be interleaved (e.g. for subtotals
    # grouped by the outer dimension label), so preserve schema ordering.
    all_data_fields = [
        f for f in table.schema if f.name.startswith("metric_group_") or f.name.startswith("grand_total_")
    ]

    data_field_names = [f.name for f in all_data_fields]
    data_matrix = (
        table.select(data_field_names).to_pandas().to_numpy(dtype=float, na_value=float("nan"))
    )  # shape: (n_arrow_rows, n_data_cols)

    # computedShape.rows  → label refs for Arrow row attribute columns
    # computedShape.cols  → label refs encoded in field metadata
    row_label_refs: list[str] = xtab_meta["computedShape"]["rows"]
    col_label_refs: list[str] = xtab_meta["computedShape"]["cols"]

    inline_index = _build_inline_index(table, row_label_refs, label_ref_to_id, model_meta, xtab_meta)
    field_index = _build_field_index(all_data_fields, col_label_refs, label_ref_to_id, model_meta, xtab_meta)

    # When there are no row attribute labels (inline_index is None) the server
    # packs everything into the field dimension; always use field_index as rows.
    if is_transposed or inline_index is None:
        return pandas.DataFrame(data_matrix.T, index=field_index, columns=_wrap_for_columns(inline_index))

    return pandas.DataFrame(data_matrix, index=inline_index, columns=_wrap_for_columns(field_index))
