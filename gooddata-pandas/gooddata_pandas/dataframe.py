# (C) 2021 GoodData Corporation
from __future__ import annotations

from typing import Optional, Union

import pandas
from gooddata_api_client import models
from gooddata_sdk import (
    Attribute,
    BareExecutionResponse,
    ExecutionDefinition,
    Filter,
    GoodDataSdk,
    ResultCacheMetadata,
    ResultSizeDimensions,
)

from gooddata_pandas.data_access import compute_and_extract
from gooddata_pandas.result_convertor import (
    _DEFAULT_PAGE_SIZE,
    DataFrameMetadata,
    LabelOverrides,
    convert_execution_response_to_dataframe,
)
from gooddata_pandas.utils import (
    ColumnsDef,
    DefaultVisualizationColumnNaming,
    IndexDef,
    LabelItemDef,
    _to_item,
    make_pandas_index,
)


class DataFrameFactory:
    """
    Factory to create pandas.DataFrame instances.

    Methods:
        - indexed(self, index_by: IndexDef, columns:ColumnsDef, filter_by: Optional[Union[Filter, list[Filter]]] = None)
            -> pandas.DataFrame:
        - not_indexed(self, columns: ColumnsDef, filter_by: Optional[Union[Filter, list[Filter]]] = None)
            -> pandas.DataFrame:
        - for_items(self, items: ColumnsDef, filter_by: Optional[Union[Filter, list[Filter]]] = None,
            auto_index: bool = True) -> pandas.DataFrame:
        - for_visualization(self, visualization_id: str, auto_index: bool = True)
            -> pandas.DataFrame:
        - result_cache_metadata_for_exec_result_id(self, result_id: str)
            -> ResultCacheMetadata:
        - for_exec_def(self, exec_def: ExecutionDefinition, label_overrides: Optional[LabelOverrides] = None,
            result_size_dimensions_limits: ResultSizeDimensions = (), result_size_bytes_limit: Optional[int] = None,
            page_size: int = _DEFAULT_PAGE_SIZE,) -> Tuple[pandas.DataFrame, DataFrameMetadata]:
        - for_exec_result_id(self, result_id: str, label_overrides: Optional[LabelOverrides] = None,
            result_cache_metadata: Optional[ResultCacheMetadata] = None,
            result_size_dimensions_limits: ResultSizeDimensions = (),
            result_size_bytes_limit: Optional[int] = None,
            use_local_ids_in_headers: bool = False, page_size: int = _DEFAULT_PAGE_SIZE,)
            -> Tuple[pandas.DataFrame, DataFrameMetadata]:
    """

    def __init__(self, sdk: GoodDataSdk, workspace_id: str) -> None:
        """
        Args:
            sdk (GoodDataSdk): GoodData SDK instance.
            workspace_id (str): Workspace identifier.
        """
        self._sdk = sdk
        self._workspace_id = workspace_id

    def indexed(
        self, index_by: IndexDef, columns: ColumnsDef, filter_by: Optional[Union[Filter, list[Filter]]] = None
    ) -> pandas.DataFrame:
        """
        Creates a data frame indexed by values of the label. The data frame columns will be created from either
        metrics or other label values.

        Note that depending on composition of the labels, the DataFrame's index may or may not be unique.

        Args:
            index_by (IndexDef): One or more labels to index by.
            columns (ColumnsDef): Dictionary mapping column name to its definition.
            filter_by (Optional[Union[Filter, list[Filter]]]):
                Optional filters to apply during computation on the server.

        Returns:
            pandas.DataFrame: A DataFrame instance.
        """
        data, index = compute_and_extract(
            self._sdk,
            self._workspace_id,
            columns=columns,
            index_by=index_by,
            filter_by=filter_by,
        )

        _idx = make_pandas_index(index)

        return pandas.DataFrame(data=data, index=_idx)

    def not_indexed(
        self, columns: ColumnsDef, filter_by: Optional[Union[Filter, list[Filter]]] = None
    ) -> pandas.DataFrame:
        """
        Creates a data frame with columns created from metrics and or labels.

        Args:
            columns (ColumnsDef): Dictionary mapping column name to its definition.
            filter_by (Optional[Union[Filter, list[Filter]]]): Optionally specify filters to apply during
                computation on the server.

        Returns:
            pandas.DataFrame: A DataFrame instance.
        """

        data, _ = compute_and_extract(self._sdk, self._workspace_id, columns=columns, filter_by=filter_by)

        return pandas.DataFrame(data=data)

    def for_items(
        self, items: ColumnsDef, filter_by: Optional[Union[Filter, list[Filter]]] = None, auto_index: bool = True
    ) -> pandas.DataFrame:
        """
        Creates a data frame for named items. This is a convenience method that will create DataFrame with or
        without index based on the context of the items that you pass.

        Args:
            items (ColumnsDef): Dictionary mapping item name to its definition.
            filter_by (Optional[Union[Filter, list[Filter]]]): Optionally specify filters to apply during computation
                on the server.
            auto_index (bool): Default True. Enables creation of DataFrame with index depending on the contents
                of the items.

        Returns:
            pandas.DataFrame: A DataFrame instance.
        """
        resolved_attr_cols: dict[str, LabelItemDef] = dict()
        resolved_measure_cols: ColumnsDef = dict()
        has_attributes = False
        has_measures = False

        for col_name, col_def in items.items():
            item = _to_item(col_def, local_id=col_name)

            if isinstance(item, Attribute):
                has_attributes = True
                resolved_attr_cols[col_name] = item
            else:
                has_measures = True
                resolved_measure_cols[col_name] = item

        if not auto_index or not has_measures or not has_attributes:
            columns: ColumnsDef = {**resolved_attr_cols, **resolved_measure_cols}

            return self.not_indexed(columns=columns, filter_by=filter_by)

        return self.indexed(
            index_by=resolved_attr_cols,
            columns=resolved_measure_cols,
            filter_by=filter_by,
        )

    def for_visualization(self, visualization_id: str, auto_index: bool = True) -> pandas.DataFrame:
        """
        Creates a data frame with columns based on the content of the visualization with the provided identifier.

        Args:
            visualization_id (str): Visualization identifier.
            auto_index (bool): Default True. Enables creation of DataFrame with index depending on the contents
                of the visualization.

        Returns:
            pandas.DataFrame: A DataFrame instance.
        """
        naming = DefaultVisualizationColumnNaming()
        visualization = self._sdk.visualizations.get_visualization(
            workspace_id=self._workspace_id, visualization_id=visualization_id
        )
        filter_by = [f.as_computable() for f in visualization.filters]
        columns: ColumnsDef = {
            **{naming.col_name_for_attribute(a): a.as_computable() for a in visualization.attributes},
            **{naming.col_name_for_metric(m): m.as_computable() for m in visualization.metrics},
        }

        return self.for_items(columns, filter_by=filter_by, auto_index=auto_index)

    def for_created_visualization(
        self, created_visualizations_response: dict
    ) -> tuple[pandas.DataFrame, DataFrameMetadata]:
        """
        Creates a data frame using a created visualization.

        Args:
            created_visualizations_response (dict): Created visualization response.

        Returns:
            pandas.DataFrame: A DataFrame instance.
        """
        execution_definition = self._sdk.compute.build_exec_def_from_chat_result(created_visualizations_response)
        return self.for_exec_def(exec_def=execution_definition)

    def result_cache_metadata_for_exec_result_id(self, result_id: str) -> ResultCacheMetadata:
        """
        Retrieves result cache metadata for given :result_id:

        Args:
            result_id (str): ID of execution result to retrieve the metadata for.

        Returns:
            ResultCacheMetadata: Corresponding result cache metadata.
        """
        return self._sdk.compute.retrieve_result_cache_metadata(workspace_id=self._workspace_id, result_id=result_id)

    def for_exec_def(
        self,
        exec_def: ExecutionDefinition,
        label_overrides: Optional[LabelOverrides] = None,
        result_size_dimensions_limits: ResultSizeDimensions = (),
        result_size_bytes_limit: Optional[int] = None,
        page_size: int = _DEFAULT_PAGE_SIZE,
    ) -> tuple[pandas.DataFrame, DataFrameMetadata]:
        """
        Creates a data frame using an execution definition.

        Each dimension may be sliced by multiple labels. The factory will create MultiIndex for the dataframe's
        row index and the columns.

        Example of label_overrides structure:

        .. code-block:: python

            {
                "labels": {
                    "local_attribute_id": {
                        "title": "My new attribute label"
                    ,...
                },
                "metrics": {
                    "local_metric_id": {
                        "title": "My new metric label"
                    },...
                }
            }

        Args:
            exec_def (ExecutionDefinition): Execution definition.
            label_overrides (Optional[LabelOverrides]): Label overrides for metrics and attributes.
            result_size_dimensions_limits (ResultSizeDimensions): A tuple containing maximum size of result dimensions.
            result_size_bytes_limit (Optional[int]): Maximum size of result in bytes.
            page_size (int): Number of records per page.

        Returns:
            Tuple[pandas.DataFrame, DataFrameMetadata]: Tuple holding DataFrame and DataFrame metadata.
        """
        if label_overrides is None:
            label_overrides = {}

        execution = self._sdk.compute.for_exec_def(workspace_id=self._workspace_id, exec_def=exec_def)
        result_cache_metadata = self.result_cache_metadata_for_exec_result_id(execution.result_id)

        return convert_execution_response_to_dataframe(
            execution_response=execution.bare_exec_response,
            result_cache_metadata=result_cache_metadata,
            label_overrides=label_overrides,
            result_size_dimensions_limits=result_size_dimensions_limits,
            result_size_bytes_limit=result_size_bytes_limit,
            page_size=page_size,
        )

    def for_exec_result_id(
        self,
        result_id: str,
        label_overrides: Optional[LabelOverrides] = None,
        result_cache_metadata: Optional[ResultCacheMetadata] = None,
        result_size_dimensions_limits: ResultSizeDimensions = (),
        result_size_bytes_limit: Optional[int] = None,
        use_local_ids_in_headers: bool = False,
        use_primary_labels_in_attributes: bool = False,
        page_size: int = _DEFAULT_PAGE_SIZE,
    ) -> tuple[pandas.DataFrame, DataFrameMetadata]:
        """
            Retrieves a DataFrame and DataFrame metadata for a given execution result identifier.

            Example of label_overrides structure:

            .. code-block:: python

                {
                    "labels": {
                        "local_attribute_id": {
                            "title": "My new attribute label"
                        ,...
                    },
                    "metrics": {
                        "local_metric_id": {
                            "title": "My new metric label"
                        },...
                    }
                }

        Args:
            result_id (str): Execution result identifier.
            label_overrides (Optional[LabelOverrides]): Label overrides for metrics and attributes.
            result_cache_metadata (Optional[ResultCacheMetadata]): Cache metadata for the execution result.
            result_size_dimensions_limits (ResultSizeDimensions): A tuple containing maximum size of result dimensions.
            result_size_bytes_limit (Optional[int]): Maximum size of result in bytes.
            use_local_ids_in_headers (bool): Use local identifier in headers.
            use_primary_labels_in_attributes (bool): Use primary labels in attributes.
            page_size (int): Number of records per page.

        Returns:
            Tuple[pandas.DataFrame, DataFrameMetadata]: Tuple holding DataFrame and DataFrame metadata.
        """
        if label_overrides is None:
            label_overrides = {}

        if result_cache_metadata is None:
            result_cache_metadata = self.result_cache_metadata_for_exec_result_id(result_id=result_id)

        return convert_execution_response_to_dataframe(
            execution_response=BareExecutionResponse(
                api_client=self._sdk.client,
                workspace_id=self._workspace_id,
                execution_response=models.AfmExecutionResponse(
                    result_cache_metadata.execution_response, _check_type=False
                ),
            ),
            result_cache_metadata=result_cache_metadata,
            label_overrides=label_overrides,
            result_size_dimensions_limits=result_size_dimensions_limits,
            result_size_bytes_limit=result_size_bytes_limit,
            use_local_ids_in_headers=use_local_ids_in_headers,
            use_primary_labels_in_attributes=use_primary_labels_in_attributes,
            page_size=page_size,
        )
