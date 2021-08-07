# (C) 2021 GoodData Corporation
from gooddata_sdk import (
    ExecutionDefinition,
    ExecutionResponse,
    Attribute,
    Measure,
    Filter,
    GoodDataSdk,
)
from gooddata_pandas.utils import (
    ColumnsDef,
    IndexDef,
    _to_item,
    _to_attribute,
    _to_filters,
)


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
    -  pandas col name to index where headers appear in measure dimension
    -  pandas index name to index where headers appear in the attribute dimension
    """
    _index_by = dict()

    if isinstance(index_by, dict):
        _index_by = index_by
    elif isinstance(index_by, str):
        _index_by = {0: index_by}

    attributes = []
    measures = []
    col_to_attr_idx = dict()
    index_to_attr_idx = dict()
    col_to_measure_idx = dict()

    for index_name, index_col in (_index_by or dict()).items():
        item = _to_attribute(index_col)
        index_to_attr_idx[index_name] = len(attributes)
        attributes.append(item)

    for col_name, col in columns.items():
        item = _to_item(col)

        if isinstance(item, Attribute):
            # prevent double-add for attributes that are using same labels. this has no real effect on the result
            # apart from extra load/size of the result that would contain the duplicates.
            #
            # this may typically happen when same labels are used for indexing & data
            existing_attr_idx = next(
                (
                    idx
                    for idx, attr in enumerate(attributes)
                    if item.has_same_label(attr)
                ),
                None,
            )

            if existing_attr_idx is not None:
                col_to_attr_idx[col_name] = existing_attr_idx
            else:
                col_to_attr_idx[col_name] = len(attributes)
                attributes.append(item)
        elif isinstance(item, Measure):
            col_to_measure_idx[col_name] = len(measures)
            measures.append(item)

    dimensions = [
        ["measureGroup"] if len(measures) else None,
        [a.local_id for a in attributes] if len(attributes) else None,
    ]

    exec_def = ExecutionDefinition(
        attributes=attributes,
        measures=measures,
        filters=_to_filters(filter_by),
        dimensions=dimensions,
    )

    return (
        sdk.compute.for_exec_def(workspace_id, exec_def),
        col_to_attr_idx,
        col_to_measure_idx,
        index_to_attr_idx,
    )


_RESULT_PAGE_LEN = 1000


#
# Note: both of the extract functions assume the number of measures requested for the data frame is less than
# page limit enforced by the server. The function for getting data frame for measures only does not paging at all
# and the one that gets data from possibly two-dimensional result always pages only through the dimension that
# contains attributes.
#


def _extract_for_measures_only(
    response: ExecutionResponse, cols: list, col_to_metric_idx: dict
) -> dict:
    exec_def = response.exec_def
    result = response.read_result(len(exec_def.measures))
    data = dict()

    for col in cols:
        data[col] = [result.data[col_to_metric_idx[col]]]

    return data


def _extract_from_attributes_and_maybe_measures(
    response: ExecutionResponse,
    cols: list,
    col_to_attr_idx: dict,
    col_to_metric_idx: dict,
    index_to_attr_idx: dict = None,
) -> tuple[dict, dict]:
    exec_def = response.exec_def
    offset = [0 for _ in exec_def.dimensions]
    limit = (
        [len(exec_def.measures), _RESULT_PAGE_LEN]
        if exec_def.has_measures()
        else [_RESULT_PAGE_LEN]
    )
    attribute_dim = 1 if exec_def.has_measures() else 0
    result = response.read_result(limit=limit, offset=offset)

    index = (
        dict([(idx_name, []) for idx_name in index_to_attr_idx])
        if index_to_attr_idx is not None
        else dict()
    )
    data = dict([(col, []) for col in cols])

    while True:
        for idx_name in index:
            index[idx_name] += result.get_all_header_values(
                attribute_dim, index_to_attr_idx[idx_name]
            )

        for col in cols:
            if col in col_to_attr_idx:
                data[col] += result.get_all_header_values(
                    attribute_dim, col_to_attr_idx[col]
                )
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

    if not exec_def.has_attributes():
        return _extract_for_measures_only(response, cols, col_to_metric_idx), dict()
    else:
        return _extract_from_attributes_and_maybe_measures(
            response, cols, col_to_attr_idx, col_to_metric_idx, index_to_attr_idx
        )
