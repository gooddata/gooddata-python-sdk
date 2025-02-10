# (C) 2021 GoodData Corporation
from __future__ import annotations

from typing import Any, Optional, Union

from gooddata_sdk import (
    Attribute,
    AttributeFilter,
    CatalogAttribute,
    ExecutionDefinition,
    ExecutionResponse,
    Filter,
    GoodDataSdk,
    Metric,
    MetricValueFilter,
    ObjId,
    TableDimension,
)
from gooddata_sdk.utils import IdObjType

from gooddata_pandas.utils import (
    ColumnsDef,
    IndexDef,
    LabelItemDef,
    _str_to_obj_id,
    _to_attribute,
    _to_item,
    _typed_attribute_value,
    get_catalog_attributes_for_extract,
)


class ExecutionDefinitionBuilder:
    _DEFAULT_INDEX_NAME: str = "0"

    def __init__(self, columns: ColumnsDef, index_by: Optional[IndexDef] = None) -> None:
        """
        Initializes the ExecutionDefinitionBuilder instance with columns and an
        optional index_by definition. Processes the given columns and index_by
        definitions to build the internal mappings.

        Args:
            columns (ColumnsDef): Input columns to process and build internal mappings.
            index_by (Optional[IndexDef], optional): Index definition to process. Defaults to None.

        """
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
        """
        Processes the input columns to build internal mappings and add attributes or
        metrics as needed.

        Args:
            columns (ColumnsDef): Input columns to process and build internal mappings.
        """
        for column_name, column_def in columns.items():
            self._add_column(column_name, column_def)

    def _add_column(self, column_name: str, column_def: Union[str, Attribute, Metric, ObjId]) -> None:
        """
        Adds a given column to the internal mappings and appends it to the appropriate list (Attributes or Metrics).

        Args:
            column_name (str): The name of the column to add.
            column_def (Union[str, Attribute, Metric, ObjId]): Defines the column, either an Attribute or Metric object.

        This method prevents duplicate attributes (with the same labels) from being added multiple times,
        which could otherwise lead to an increased load or result size.

        Note: This method is typically called from the _process_columns() method.
        """
        item = _to_item(column_def)
        if isinstance(item, Attribute):
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
        """
        Processes the given index definition (index_by) to determine whether to reference attributes or
        raise an error when attempting to reference metrics. Updates the internal index-to-attribute mapping
        and handles index definition without a column reference.

        Args:
            index_by (Optional[IndexDef], default None): A definition for index columns, it can be a string,
                a dictionary of index keys and column names, or None.

        If the index definition is a known attribute defined in columns, the associated attribute index is
        added to the index-to-attribute mapping (_index_to_attr_idx). If the index is a known metric
        defined in columns, it raises a ValueError since index_by cannot be a metric. Otherwise, if the
        index definition has no direct column reference, the _process_index_item_without_col_ref method is
        called.
        """
        if index_by is None:
            return

        _index_by = {self._DEFAULT_INDEX_NAME: index_by} if not isinstance(index_by, dict) else index_by

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
        """
        Finds the index of an attribute in the attribute list, if the item has the same label as an existing attribute.

        Args:
            item (Attribute): The attribute for which the index is sought.

        Returns:
            Union[int, None]: The index of the attribute with the same label in the attribute list, if it exists.
            Otherwise, returns None.

        This method is used to find the index of an attribute in the _attributes list by checking if the given item
        has the same label as an existing attribute in the list. If found, it returns the index of
        the matching attribute, otherwise, it returns None.
        """
        existing_attr_idx = next(
            (idx for idx, attr in enumerate(self._attributes) if item.has_same_label(attr)),
            None,
        )
        return existing_attr_idx

    def _process_index_item_without_col_ref(self, index_name: str, index_def: LabelItemDef) -> None:
        """
        This method processes an index item without column reference,
        updating the internal state of the object.

        Args:
            index_name (str): The name of the index.
            index_def (LabelItemDef): The definition of the index item.

        Returns:
            None
        """
        norm_index_def = index_def
        if isinstance(index_def, str) and (not index_def.startswith("label/")):
            # it is not an obj id in string form - consider it label_id and extend it to obj id string form
            norm_index_def = f"label/{index_def}"
        attr_item = _to_attribute(norm_index_def)
        attr_index = self._find_attribute_index(attr_item)

        if attr_index is not None:
            self._index_to_attr_idx[index_name] = attr_index
        else:
            self._index_to_attr_idx[index_name] = len(self._attributes)
            self._attributes.append(attr_item)

    def _update_filter_ids(self, filter_by: Optional[Union[Filter, list[Filter]]] = None) -> Optional[list[Filter]]:
        """
        Updates the filter IDs for the given filters. If a filter references a metric/attribute by a string,
        it is converted to the corresponding internal ID.

        Args:
            filter_by (Optional[Union[Filter, list[Filter]]], default None): A filter or list of filters
                to be updated.

        Returns:
            Optional[list[Filter]]: The updated list of filters, or None if no filters were provided.

        Raises:
            ValueError: If an AttributeFilter instance references a metric.
        """
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
                elif (
                    isinstance(_filter, MetricValueFilter)
                    and isinstance(_filter.metric, str)
                    and _filter.metric in self._col_to_metric_idx
                ):
                    # Metric is referenced by local_id which was already generated during creation of columns
                    # When Metric filter contains ObjId reference, it does not need to be modified
                    _filter.metric = self._metrics[self._col_to_metric_idx[_filter.metric]].local_id

        return filters

    def build_execution_definition(
        self, filter_by: Optional[Union[Filter, list[Filter]]] = None
    ) -> ExecutionDefinition:
        """
        Builds an ExecutionDefinition instance with the current configuration of metrics, attributes, and filters.

        Args:
            filter_by (Optional[Union[Filter, list[Filter]]]): A filter or a list of filters to be applied to the
            execution definition. If it's not provided or None, then the current filter configuration is used.

        Returns:
            ExecutionDefinition: An ExecutionDefinition instance containing attributes, metrics, filters,
            and dimensions.
        """
        dimensions = [
            TableDimension(
                item_ids=["measureGroup"] if self._metrics else None,
            ),
            TableDimension(
                item_ids=[a.local_id for a in self._attributes] if self._attributes else None,
            ),
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
    Internal function that computes an execution-by-convention to retrieve data for a data frame with the provided
    columns, optionally indexed by the index_by label and optionally filtered.

    Args:
        sdk (GoodDataSdk): The GoodData SDK instance.
        workspace_id (str): The workspace ID.
        columns (ColumnsDef): The columns definition.
        index_by (Optional[IndexDef]): The index definition, if any.
        filter_by (Optional[Union[Filter, list[Filter]]]): A filter or a list of filters, if any.

    Returns:
        tuple: A tuple containing the following elements:
        - ExecutionResponse: The execution response.
        - dict[str, int]: A mapping of pandas column names to attribute dimension indices.
        - dict[str, int]: A mapping of pandas column names to metric dimension indices.
        - dict[str, int]: A mapping of pandas index names to attribute dimension indices.
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
    """
    Internal function that extracts data for metrics-only columns when there are no attribute columns.

    Args:
        response (ExecutionResponse): The execution response to extract data from.
        cols (list): A list of column names.
        col_to_metric_idx (dict): A mapping of pandas column names to metric dimension indices.

    Returns:
        dict: A dictionary containing the extracted data.
    """
    exec_def = response.exec_def
    result = response.read_result(len(exec_def.metrics))
    if len(result.data) == 0:
        return {col: [] for col in cols}

    return {col: [result.data[col_to_metric_idx[col]]] for col in cols}


def _find_attribute(attributes: list[CatalogAttribute], id_obj: IdObjType) -> Union[CatalogAttribute, None]:
    for attribute in attributes:
        if attribute.find_label(id_obj) is not None:
            return attribute
    return None


def _typed_result(attributes: list[CatalogAttribute], attribute: Attribute, result_values: list[Any]) -> list[Any]:
    """
    Internal function to convert result_values to proper data types.

    Args:
        attributes (list[CatalogAttribute]): The catalog of attributes.
        attribute (Attribute): The attribute for which the typed result will be computed.
        result_values (list[Any]): A list of raw values.

    Returns:
        list[Any]: A list of converted values with proper data types.
    """
    catalog_attribute = _find_attribute(attributes, attribute.label)
    if catalog_attribute is None:
        raise ValueError(f"Unable to find attribute {attribute.label} in catalog")
    return [_typed_attribute_value(catalog_attribute, value) for value in result_values]


def _extract_from_attributes_and_maybe_metrics(
    response: ExecutionResponse,
    attributes: list[CatalogAttribute],
    cols: list[str],
    col_to_attr_idx: dict[str, int],
    col_to_metric_idx: dict[str, int],
    index_to_attr_idx: Optional[dict[str, int]] = None,
) -> tuple[dict, dict]:
    """
    Internal function that extracts data from execution response with attributes columns and
    optionally metrics columns.

    Args:
        response (ExecutionResponse): The execution response to extract data from.
        attributes (list[CatalogAttribute]): The catalog of attributes.
        cols (list[str]): A list of column names.
        col_to_attr_idx (dict[str, int]): A mapping of pandas column names to attribute dimension indices.
        col_to_metric_idx (dict[str, int]): A mapping of pandas column names to metric dimension indices.
        index_to_attr_idx (Optional[dict[str, int]]):
            An optional mapping of pandas index names to attribute dimension indices.

    Returns:
        tuple: A tuple containing the following dictionaries:
        - dict: A dictionary containing the extracted data.
        - dict: A dictionary containing the extracted index data.
    """
    exec_def = response.exec_def
    offset = [0 for _ in exec_def.dimensions]
    limit = [len(exec_def.metrics), _RESULT_PAGE_LEN] if exec_def.has_metrics() else [_RESULT_PAGE_LEN]
    attribute_dim = 1 if exec_def.has_metrics() else 0
    result = response.read_result(limit=limit, offset=offset)
    safe_index_to_attr_idx = index_to_attr_idx if index_to_attr_idx is not None else dict()

    # mappings from column name to Attribute
    index_to_attribute = {index_name: exec_def.attributes[i] for index_name, i in safe_index_to_attr_idx.items()}
    col_to_attribute = {col: exec_def.attributes[i] for col, i in col_to_attr_idx.items()}

    # datastructures to return
    index: dict[str, list[Any]] = {idx_name: [] for idx_name in safe_index_to_attr_idx}
    data: dict[str, list[Any]] = {col: [] for col in cols}

    while True:
        for idx_name in index:
            rs = result.get_all_header_values(attribute_dim, safe_index_to_attr_idx[idx_name])
            attribute = index_to_attribute[idx_name]
            index[idx_name] += _typed_result(attributes, attribute, rs)
        for col in cols:
            if col in col_to_attr_idx:
                rs = result.get_all_header_values(attribute_dim, col_to_attr_idx[col])
                attribute = col_to_attribute[col]
                data[col] += _typed_result(attributes, attribute, rs)
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
    Convenience function that computes and extracts data from the execution response.

    Args:
        sdk (GoodDataSdk): The GoodData SDK instance.
        workspace_id (str): The workspace ID.
        columns (ColumnsDef): The columns definition.
        index_by (Optional[IndexDef]): The index definition, if any.
        filter_by (Optional[Union[Filter, list[Filter]]]): A filter or a list of filters, if any.

    Returns:
        tuple: A tuple containing the following dictionaries:
        - dict: A dictionary with data for each column in `columns`.
        - dict: A dictionary with data for constructing index(es) for each index in index_by.

    Note: For convenience it is possible to pass just single index. in that case the index dict will contain exactly
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
        return _extract_for_metrics_only(response, cols, col_to_metric_idx), dict()
    else:
        attributes = get_catalog_attributes_for_extract(sdk, workspace_id, exec_def.attributes)
        return _extract_from_attributes_and_maybe_metrics(
            response,
            attributes,
            cols,
            col_to_attr_idx,
            col_to_metric_idx,
            index_to_attr_idx,
        )
