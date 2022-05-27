# (C) 2021 GoodData Corporation
from __future__ import annotations

from typing import Any, Optional, Union

from gooddata_pandas.utils import (
    ColumnsDef,
    IndexDef,
    LabelItemDef,
    _str_to_obj_id,
    _to_attribute,
    _to_item,
    _typed_attribute_value,
)
from gooddata_sdk import (
    Attribute,
    AttributeFilter,
    CatalogWorkspaceContent,
    ExecutionDefinition,
    ExecutionResponse,
    Filter,
    GoodDataSdk,
    Metric,
    MetricValueFilter,
    ObjId,
)


class ExecutionDefinitionBuilder:
    _DEFAULT_INDEX_NAME: str = "0"

    def __init__(self, columns: ColumnsDef, index_by: Optional[IndexDef] = None) -> None:
        self._attributes: list[Attribute] = []
        self._metrics: list[Metric] = []
        self._col_to_attr_idx: dict[str, int] = dict()
        self._index_to_attr_idx: dict[str, int] = dict()
        self._col_to_metric_idx: dict[str, int] = dict()

        self._process_columns(columns)
        self._process_index(index_by)

    @property
    def col_to_attr_idx(self) -> dict[str, int]:
        return self._col_to_attr_idx

    @property
    def index_to_attr_idx(self) -> dict[str, int]:
        return self._index_to_attr_idx

    @property
    def col_to_metric_idx(self) -> dict[str, int]:
        return self._col_to_metric_idx

    def _process_columns(self, columns: ColumnsDef) -> None:
        for column_name, column_def in columns.items():
            self._add_column(column_name, column_def)

    def _add_column(self, column_name: str, column_def: Union[str, Attribute, Metric, ObjId]) -> None:
        item = _to_item(column_def)
        if isinstance(item, Attribute):
            # prevent double-add for attributes that are using same labels. this has no real effect on the result
            # apart from extra load/size of the result that would contain the duplicates.
            #
            # this may typically happen when same labels are used for indexing & data
            attr_index = self._find_attribute_index(item)

            if attr_index is not None:
                self._col_to_attr_idx[column_name] = attr_index
            else:
                self._col_to_attr_idx[column_name] = len(self._attributes)
                self._attributes.append(item)
        elif isinstance(item, Metric):
            self._col_to_metric_idx[column_name] = len(self._metrics)
            self._metrics.append(item)

    def _process_index(self, index_by: Optional[IndexDef] = None) -> None:
        if index_by is None:
            return

        if not isinstance(index_by, dict):
            _index_by = {self._DEFAULT_INDEX_NAME: index_by}
        else:
            _index_by = index_by

        for index_name, index_def in _index_by.items():
            if isinstance(index_def, str) and (index_def in self._col_to_attr_idx):
                # known attribute defined in columns referenced by the column key
                attr_index = self._col_to_attr_idx[index_def]
                self._index_to_attr_idx[index_name] = attr_index
            elif isinstance(index_def, str) and (index_def in self._col_to_metric_idx):
                # known metric defined in columns referenced by the column key - index_by cannot be a metric
                raise ValueError(f"Invalid index_col item {index_def}, type={type(self._col_to_metric_idx[index_def])}")
            else:
                self._process_index_item_without_col_ref(index_name, index_def)

    def _find_attribute_index(self, item: Attribute) -> Union[int | None]:
        existing_attr_idx = next(
            (idx for idx, attr in enumerate(self._attributes) if item.has_same_label(attr)),
            None,
        )
        return existing_attr_idx

    def _process_index_item_without_col_ref(self, index_name: str, index_def: LabelItemDef) -> None:
        norm_index_def = index_def
        if isinstance(index_def, str) and (not index_def.startswith("label/")):
            # it is not a obj id in string form - consider it label_id and extend it to obj id string form
            norm_index_def = f"label/{index_def}"
        attr_item = _to_attribute(norm_index_def)
        attr_index = self._find_attribute_index(attr_item)

        if attr_index is not None:
            self._index_to_attr_idx[index_name] = attr_index
        else:
            self._index_to_attr_idx[index_name] = len(self._attributes)
            self._attributes.append(attr_item)

    def _update_filter_ids(self, filter_by: Optional[Union[Filter, list[Filter]]] = None) -> Optional[list[Filter]]:
        filters = [filter_by] if isinstance(filter_by, Filter) else filter_by
        if filters:
            for _filter in filters:
                if isinstance(_filter, AttributeFilter) and isinstance(_filter.label, str):
                    if _filter.label in self._col_to_attr_idx:
                        _filter.label = self._attributes[self._col_to_attr_idx[_filter.label]].label
                    elif _filter.label in self._index_to_attr_idx:
                        _filter.label = self._attributes[self._index_to_attr_idx[_filter.label]].label
                    elif _filter.label in self._col_to_metric_idx:
                        raise ValueError(f"AttributeFilter instance referencing metric [{_filter.label}]")
                    else:
                        _filter.label = _str_to_obj_id(_filter.label) or _filter.label
                elif isinstance(_filter, MetricValueFilter) and isinstance(_filter.metric, str):
                    if _filter.metric in self._col_to_metric_idx:
                        # Metric is referenced by local_id which was already generated during creation of columns
                        # When Metric filter contains ObjId reference, it does not need to be modified
                        _filter.metric = self._metrics[self._col_to_metric_idx[_filter.metric]].local_id

        return filters

    def build_execution_definition(
        self, filter_by: Optional[Union[Filter, list[Filter]]] = None
    ) -> ExecutionDefinition:
        dimensions = [
            ["measureGroup"] if len(self._metrics) else None,
            [a.local_id for a in self._attributes] if len(self._attributes) else None,
        ]

        filters = self._update_filter_ids(filter_by)

        return ExecutionDefinition(
            attributes=self._attributes,
            metrics=self._metrics,
            filters=filters,
            dimensions=dimensions,
        )


def _compute(
    sdk: GoodDataSdk,
    workspace_id: str,
    columns: ColumnsDef,
    index_by: Optional[IndexDef] = None,
    filter_by: Optional[Union[Filter, list[Filter]]] = None,
) -> tuple[ExecutionResponse, dict[str, int], dict[str, int], dict[str, int]]:
    """
    Creates execution-by-convention to retrieve data for frame with the provided columns that is optionally
    indexed by index_by label and optionally also filtered.

    The convention is as follows:

    -  If the columns contain labels and facts/metric, then two dimensional result will be created. first dim
       will contain measureGroup, second dimension will be all the attributes

    -  If indexing is desired, then the index label will be placed in the attribute dimension and will be the
       first in that dimension

    -  Otherwise the execution will be single-dim and will contain either measureGroup or all attributes

    Only columns contain always full identification of objects in a form { 'index', 'full identification' }.
    index_by and filters may contain references to columns using the index!

    The compute will return execution response and two mappings:
    -  pandas name to index where headers appear in the attribute dimension
    -  pandas col name to index where headers appear in metric dimension
    -  pandas index name to index where headers appear in the attribute dimension
    """

    builder = ExecutionDefinitionBuilder(columns, index_by)
    exec_def = builder.build_execution_definition(filter_by)

    return (
        sdk.compute.for_exec_def(workspace_id, exec_def),
        builder.col_to_attr_idx,
        builder.col_to_metric_idx,
        builder.index_to_attr_idx,
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


def _typed_result(catalog: CatalogWorkspaceContent, attribute: Attribute, result_values: list[Any]) -> list[Any]:
    """Convert result_values to proper data types."""
    catalog_attribute = catalog.find_label_attribute(attribute.label)
    if catalog_attribute is None:
        raise ValueError(f"Unable to find attribute {attribute.label} in catalog")
    return [_typed_attribute_value(catalog_attribute, value) for value in result_values]


def _extract_from_attributes_and_maybe_metrics(
    response: ExecutionResponse,
    catalog: CatalogWorkspaceContent,
    cols: list[str],
    col_to_attr_idx: dict[str, int],
    col_to_metric_idx: dict[str, int],
    index_to_attr_idx: Optional[dict[str, int]] = None,
) -> tuple[dict, dict]:

    exec_def = response.exec_def
    offset = [0 for _ in exec_def.dimensions]
    limit = [len(exec_def.metrics), _RESULT_PAGE_LEN] if exec_def.has_metrics() else [_RESULT_PAGE_LEN]
    attribute_dim = 1 if exec_def.has_metrics() else 0
    result = response.read_result(limit=limit, offset=offset)
    safe_index_to_attr_idx = index_to_attr_idx if index_to_attr_idx is not None else dict()

    # mappings from column name to Attribute
    index_to_attribute = {index_name: exec_def.attributes[i] for index_name, i in safe_index_to_attr_idx.items()}
    col_to_attribute = {col: exec_def.attributes[i] for col, i, in col_to_attr_idx.items()}

    # datastructures to return
    index: dict[str, list[Any]] = {idx_name: [] for idx_name in safe_index_to_attr_idx}
    data: dict[str, list[Any]] = {col: [] for col in cols}

    while True:
        for idx_name in index:
            rs = result.get_all_header_values(attribute_dim, safe_index_to_attr_idx[idx_name])
            attribute = index_to_attribute[idx_name]
            index[idx_name] += _typed_result(catalog, attribute, rs)
        for col in cols:
            if col in col_to_attr_idx:
                rs = result.get_all_header_values(attribute_dim, col_to_attr_idx[col])
                attribute = col_to_attribute[col]
                data[col] += _typed_result(catalog, attribute, rs)
            elif col_to_metric_idx[col] < len(result.data):
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
    index_by: Optional[IndexDef] = None,
    filter_by: Optional[Union[Filter, list[Filter]]] = None,
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

    catalog = sdk.catalog_workspace_content.get_full_catalog(workspace_id)

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
