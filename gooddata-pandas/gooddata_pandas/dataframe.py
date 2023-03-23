# (C) 2021 GoodData Corporation
from __future__ import annotations

from typing import Optional, Tuple, Union

import pandas

from gooddata_api_client import models
from gooddata_pandas.data_access import compute_and_extract
from gooddata_pandas.result_convertor import (
    _DEFAULT_PAGE_SIZE,
    DataFrameMetadata,
    LabelOverrides,
    convert_execution_response_to_dataframe,
)
from gooddata_pandas.utils import (
    ColumnsDef,
    DefaultInsightColumnNaming,
    IndexDef,
    LabelItemDef,
    _to_item,
    make_pandas_index,
)
from gooddata_sdk import (
    Attribute,
    BareExecutionResponse,
    ExecutionDefinition,
    Filter,
    GoodDataSdk,
    ResultCacheMetadata,
    ResultSizeDimensions,
)


class DataFrameFactory:
    """
    Factory to create pandas.DataFrame instances.

    There are several methods in place that should provide for convenient construction of data frames:

    - ``indexed()`` - calculate measure values sliced by one or more labels, indexed by those labels
    - ``not_indexed()`` - calculate measure values sliced by one or more labels, but not indexed by those labels,
      label values will be part of the DataFrame and will be in the same row as the measure values calculated
      for them
    - ``for_items()`` - calculate measure values for a one or more items which may be labels or measures. Depending
      what items you specify, this method will create DataFrame with or without index
    - ``for_insight()`` - calculate DataFrame for insight created by GoodData.CN Analytical Designer. Depending
      on what items are in the insight, this method will create DataFrame with or without index.

    Note that all of these methods have additional levels of convenience and flexibility so their purpose is not
    limited to just what is listed above.
    """

    def __init__(self, sdk: GoodDataSdk, workspace_id: str) -> None:
        self._sdk = sdk
        self._workspace_id = workspace_id

    def indexed(
        self, index_by: IndexDef, columns: ColumnsDef, filter_by: Optional[Union[Filter, list[Filter]]] = None
    ) -> pandas.DataFrame:
        """
        Creates a data frame indexed by values of the label. The data frame columns will be created from either
        metrics or other label values.

        The computation to obtain data from GoodData.CN workspace will use all labels that you specify for both
        indexing and in columns to aggregate values of metric columns.

        Note that depending on composition of the labels, the DataFrame's index may or may not be unique.

        :param index_by: one or more labels to index by; specify either:

         - string with reference to columns key - only attribute can be referenced
         - string with id: ``some_label_id``,
         - string representation of object identifier: ``label/some_label_id``
         - object identifier: ``ObjId(id='some_label_id', type='label')``,
         - or an Attribute object used in the compute model: ``Attribute(local_id=..., label='some_label_id')``,
         - dict containing mapping of index name to label to use for indexing - specified in one of the ways list above

        :param columns: dict mapping column name to its definition; column may be specified as:

         - object identifier: ``ObjId(id='some_id', type='<type>')`` - where type is either ``label``, ``fact``
           or ``metric``
         - string representation of object identifier: ``<type>/some_id`` - where type is either ``label``, ``fact`` or
           ``metric``
         - Attribute object used in the compute model: ``Attribute(local_id=..., label='some_label_id')``
         - subclass of Measure object used in the compute model: SimpleMeasure, PopDateMeasure, PopDatasetMeasure,
           ArithmeticMeasure

        :param filter_by: optional filters to apply during computation on the server, reference to filtering column
         can be one of:

         - string reference to column key or index key
         - object identifier in string form
         - object identifier: ``ObjId(id='some_label_id', type='<type>')``
         - Attribute or Metric depending on type of filter

        :return: pandas dataframe instance
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

        The computation to obtain data from GoodData.CN workspace will use all labels that you specify for both columns
        to aggregate values of metric columns.

        :param columns: dict mapping column name to its definition; column may be specified as:

         - object identifier: ``ObjId(id='some_id', type='<type>')`` - where type is either ``label``, ``fact``
           or ``metric``
         - string representation of object identifier: ``<type>/some_id`` - where type is either ``label``,
           ``fact`` or ``metric``
         - Attribute object used in the compute model: ``Attribute(local_id=..., label='some_label_id')``
         - subclass of Measure object used in the compute model: SimpleMeasure, PopDateMeasure, PopDatasetMeasure,
           ArithmeticMeasure

        :param filter_by: optionally specify filters to apply during computation on the server, reference to filtering
         column can be one of:

         - string reference to column key
         - object identifier in string form
         - object identifier: ``ObjId(id='some_label_id', type='<type>')``
         - Attribute or Metric depending on type of filter

        :return: pandas dataframe instance
        """

        data, _ = compute_and_extract(self._sdk, self._workspace_id, columns=columns, filter_by=filter_by)

        return pandas.DataFrame(data=data)

    def for_items(
        self, items: ColumnsDef, filter_by: Optional[Union[Filter, list[Filter]]] = None, auto_index: bool = True
    ) -> pandas.DataFrame:
        """
        Creates a data frame for a named items. This is a convenience method that will create DataFrame with or
        without index based on the context of the items that you pass.

        - If items contain labels and measures, then DataFrame with index will be created. If there is more than
          one label among the items, then hierarchical index will be created.

          You can turn this behavior using 'auto_index' parameter.

        - Otherwise DataFrame without index will be created and will contain column per item.

        You may also optionally specify filters to apply during the computation on the server.

        :param items: dict mapping item name to its definition; item may be specified as:

         - object identifier: ``ObjId(id='some_id', type='<type>')`` - where type is either ``label``, ``fact``
           or ``metric``
         - string representation of object identifier: ``<type>/some_id`` - where type is either ``label``,
           ``fact`` or ``metric``
         - Attribute object used in the compute model: ``Attribute(local_id=..., label='some_label_id')``
         - subclass of Measure object used in the compute model: SimpleMeasure, PopDateMeasure, PopDatasetMeasure,
           ArithmeticMeasure

        :param filter_by: optionally specify filters to apply during computation on the server, reference to filtering
         column can be one of:

         - string reference to item key
         - object identifier in string form
         - object identifier: ``ObjId(id='some_label_id', type='<type>')``
         - Attribute or Metric depending on type of filter

        :return: pandas dataframe instance
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

    def for_insight(self, insight_id: str, auto_index: bool = True) -> pandas.DataFrame:
        """
        Creates a data frame with columns based on the content of the insight with the provided identifier. The
        filters that are set on the insight will be applied and used for the server-side computation of the data
        for the data frame.

        This method will create DataFrame with or without index - depending on the contents of the insight. The
        rules are as follows:

        - if the insight contains both attributes and measures, it will be mapped to a DataFrame with index

          - if there are multiple attributes, hieararchical index (pandas.MultiIndex) will be used
          - otherwise a normal index will be used (pandas.Index)
          - you can use the option 'auto_index' argument to disable this logic and force no indexing

        - if the insight contains either only attributes or only measures, then DataFrame will not be indexed
          and all attribute or measures values will be used as data.

        Note that if the insight consists of single measure only, the resulting data frame is guaranteed to have
        single 'row' of data with one column per measure.

        :param insight_id: insight identifier
        :param auto_index: optionally force creation of DataFrame without index even if the data in the insight is
         eligible for indexing

        :return: pandas dataframe instance
        """
        naming = DefaultInsightColumnNaming()
        insight = self._sdk.insights.get_insight(workspace_id=self._workspace_id, insight_id=insight_id)
        filter_by = [f.as_computable() for f in insight.filters]
        columns: ColumnsDef = {
            **{naming.col_name_for_attribute(a): a.as_computable() for a in insight.attributes},
            **{naming.col_name_for_metric(m): m.as_computable() for m in insight.metrics},
        }

        return self.for_items(columns, filter_by=filter_by, auto_index=auto_index)

    def result_cache_metadata_for_exec_result_id(self, result_id: str) -> ResultCacheMetadata:
        """
        Retrieves result cache metadata for given :result_id:
        :param result_id: ID of execution result to retrieve the metadata for
        :return: corresponding result cache metadata
        """
        return self._sdk.compute.retrieve_result_cache_metadata(workspace_id=self._workspace_id, result_id=result_id)

    def for_exec_def(
        self,
        exec_def: ExecutionDefinition,
        label_overrides: Optional[LabelOverrides] = None,
        result_size_dimensions_limits: ResultSizeDimensions = (),
        result_size_bytes_limit: Optional[int] = None,
        page_size: int = _DEFAULT_PAGE_SIZE,
    ) -> Tuple[pandas.DataFrame, DataFrameMetadata]:
        """
        Creates a data frame using an execution definition. The data frame will respect the dimensionality
        specified in execution definition's result spec.

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

        :param exec_def: execution definition
        :param label_overrides: label overrides for metrics and attributes
        :param result_size_dimensions_limits: A tuple containing maximum size of result dimensions. Optional.
        :param result_size_bytes_limit: Maximum size of result in bytes. Optional.
        :return: tuple holding DataFrame and DataFrame metadata
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
        page_size: int = _DEFAULT_PAGE_SIZE,
    ) -> Tuple[pandas.DataFrame, DataFrameMetadata]:
        """
        Creates a data frame using an execution result's metadata identified by result_id. The data frame will respect
        the dimensionality specified in execution definition's result spec.

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

        :param result_id: executionResult ID from ExecutionResponse
        :param label_overrides: label overrides for metrics and attributes
        :param result_cache_metadata: Metadata for the corresponding exec result. Optional.
        :param result_size_dimensions_limits: A tuple containing maximum size of result dimensions. Optional.
        :param result_size_bytes_limit: Maximum size of result in bytes. Optional.
        :param use_local_ids_in_headers: Use local identifiers of header attributes and metrics. Optional.

        :return: tuple holding DataFrame and DataFrame metadata
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
            page_size=page_size,
        )
