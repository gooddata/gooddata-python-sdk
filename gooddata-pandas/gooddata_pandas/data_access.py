# (C) 2021 GoodData Corporation
from __future__ import annotations

from gooddata_pandas.utils import ColumnsDef, IndexDef, _to_attribute, _to_filters, _to_item, _typed_attribute_value
from gooddata_sdk import Attribute, Catalog, ExecutionDefinition, ExecutionResponse, Filter, GoodDataSdk, Metric


def _compute(
    sdk: GoodDataSdk,
    workspace_id: str,
    columns: ColumnsDef,
    index_by: IndexDef = None,
    filter_by: list[Filter] = None,
) -> tuple[ExecutionResponse, dict, dict, dict]:
    """
    Creates execution-by-convention to retrieve data for frame with the provided columns that is optionally
    indexed by index_by label and optionally also filtered.

    The convention is as follows:

    -  If the columns contain labels and facts/metric, then two dimensional result will be created. first dim
       will contain measureGroup, second dimension will be all the attributes

    -  If indexing is desired, then the index label will be placed in the attribute dimension and will be the
       first in that dimension

    -  Otherwise the execution will be single-dim and will contain either measureGroup or all attributes

    The compute will return execution response and two mappings:
    -  pandas name to index where headers appear in the attribute dimension
    -  pandas col name to index where headers appear in metric dimension
    -  pandas index name to index where headers appear in the attribute dimension
    """
    _index_by = dict()

    if isinstance(index_by, dict):
        _index_by = index_by
    elif isinstance(index_by, str):
        _index_by = {0: index_by}

    attributes = []
    metrics = []
    col_to_attr_idx = dict()
    index_to_attr_idx = dict()
    col_to_metric_idx = dict()

    for index_name, index_col in (_index_by or dict()).items():
        item = _to_attribute(index_col, local_id=index_name)
        index_to_attr_idx[index_name] = len(attributes)
        attributes.append(item)

    for col_name, col in columns.items():
        item = _to_item(col, local_id=col_name)

        if isinstance(item, Attribute):
            # prevent double-add for attributes that are using same labels. this has no real effect on the result
            # apart from extra load/size of the result that would contain the duplicates.
            #
            # this may typically happen when same labels are used for indexing & data
            existing_attr_idx = next(
                (idx for idx, attr in enumerate(attributes) if item.has_same_label(attr)),
                None,
            )

            if existing_attr_idx is not None:
                col_to_attr_idx[col_name] = existing_attr_idx
            else:
                col_to_attr_idx[col_name] = len(attributes)
                attributes.append(item)
        elif isinstance(item, Metric):
            col_to_metric_idx[col_name] = len(metrics)
            metrics.append(item)

    dimensions = [
        ["measureGroup"] if len(metrics) else None,
        [a.local_id for a in attributes] if len(attributes) else None,
    ]

    exec_def = ExecutionDefinition(
        attributes=attributes,
        metrics=metrics,
        filters=_to_filters(filter_by),
        dimensions=dimensions,
    )

    return (
        sdk.compute.for_exec_def(workspace_id, exec_def),
        col_to_attr_idx,
        col_to_metric_idx,
        index_to_attr_idx,
    )


_RESULT_PAGE_LEN = 1000


#
# Note: both of the extract functions assume the number of measures requested for the data frame is less than
# page limit enforced by the server. The function for getting data frame for measures only does not paging at all
# and the one that gets data from possibly two-dimensional result always pages only through the dimension that
# contains attributes.
#


def _extract_for_metrics_only(response: ExecutionResponse, cols: list, col_to_metric_idx: dict) -> dict:
    exec_def = response.exec_def
    result = response.read_result(len(exec_def.metrics))
    data = dict()

    for col in cols:
        data[col] = [result.data[col_to_metric_idx[col]]]

    return data


def _typed_result(catalog, attribute, result_values):
    """Convert result_values to proper data types."""
    catalog_attribute = catalog.find_label_attribute(attribute.label)
    return [_typed_attribute_value(catalog_attribute, value) for value in result_values]


def _extract_from_attributes_and_maybe_metrics(
    response: ExecutionResponse,
    catalog: Catalog,
    cols: list,
    col_to_attr_idx: dict,
    col_to_metric_idx: dict,
    index_to_attr_idx: dict = None,
) -> tuple[dict, dict]:

    exec_def = response.exec_def
    offset = [0 for _ in exec_def.dimensions]
    limit = [len(exec_def.metrics), _RESULT_PAGE_LEN] if exec_def.has_metrics() else [_RESULT_PAGE_LEN]
    attribute_dim = 1 if exec_def.has_metrics() else 0
    result = response.read_result(limit=limit, offset=offset)

    # mappings from column name to Attribute
    index_to_attribute = {index_name: exec_def.attributes[i] for index_name, i in index_to_attr_idx.items()}
    col_to_attribute = {col: exec_def.attributes[i] for col, i, in col_to_attr_idx.items()}

    # datastructures to return
    index = dict()
    if index_to_attr_idx is not None:
        index = {idx_name: [] for idx_name in index_to_attr_idx}
    data = {col: [] for col in cols}

    while True:
        for idx_name in index:
            rs = result.get_all_header_values(attribute_dim, index_to_attr_idx[idx_name])
            attribute = index_to_attribute[idx_name]
            index[idx_name] += _typed_result(catalog, attribute, rs)
        for col in cols:
            if col in col_to_attr_idx:
                rs = result.get_all_header_values(attribute_dim, col_to_attr_idx[col])
                attribute = col_to_attribute[col]
                data[col] += _typed_result(catalog, attribute, rs)
            else:
                data[col] += result.data[col_to_metric_idx[col]]
        if result.is_complete(attribute_dim):
            break

        offset[attribute_dim] = result.next_page_start(attribute_dim)
        result = response.read_result(limit=limit, offset=offset)

    return data, index


def compute_and_extract(
    sdk: GoodDataSdk,
    workspace_id: str,
    columns: ColumnsDef,
    index_by: IndexDef = None,
    filter_by: list[Filter] = None,
) -> tuple[dict, dict]:
    """
    Convenience function to drive computation & data extraction on behalf of the series and data frame factories.

    Given data columns and index columns, this function will create AFM execution and then read the results and
    populate data and index dicts.

    For each column in `columns`, the returned data will contain key under which there is array of data for that column
    For each index in index_by, the returned data will contain key under which there is array with data to construct the
    index. When there are multiple indexes, feed the indexes to MultiIndex.from_arrays().

    Note that as convenience it is possible to pass just single index. in that case the index dict will contain exactly
    one key of '0' (just get first value from dict when consuming the result).
    """
    result = _compute(
        sdk=sdk,
        workspace_id=workspace_id,
        index_by=index_by,
        columns=columns,
        filter_by=filter_by,
    )

    response, col_to_attr_idx, col_to_metric_idx, index_to_attr_idx = result

    exec_def = response.exec_def
    cols = list(columns.keys())

    catalog = sdk.catalog.get_full_catalog(workspace_id)

    if not exec_def.has_attributes():
        return _extract_for_metrics_only(response, cols, col_to_metric_idx), dict()
    else:
        return _extract_from_attributes_and_maybe_metrics(
            response,
            catalog,
            cols,
            col_to_attr_idx,
            col_to_metric_idx,
            index_to_attr_idx,
        )
