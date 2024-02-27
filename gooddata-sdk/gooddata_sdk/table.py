# (C) 2021 GoodData Corporation
from __future__ import annotations

from operator import attrgetter
from typing import Any, Generator, Optional, Union

from attrs import define

from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.compute.model.attribute import Attribute
from gooddata_sdk.compute.model.execution import (
    ExecutionDefinition,
    ExecutionResponse,
    ExecutionResult,
    TotalDefinition,
    TotalDimension,
)
from gooddata_sdk.compute.model.filter import Filter
from gooddata_sdk.compute.model.metric import Metric
from gooddata_sdk.compute.service import ComputeService
from gooddata_sdk.insight import BucketType, Insight, InsightBucket, InsightMetric, InsightTotal

_MEASURE_GROUP_IDENTIFIER = "measureGroup"
_TOTAL_ORDER = ["SUM", "MAX", "MIN", "AVG", "MED"]

_TABLE_ROW_BATCH_SIZE = 512
"""
Number of rows that the code reads from backed at once.
"""

_MAX_METRICS = 256
"""
Maximum number of metrics that this code is prepared to handle. This is to simplify the paging business - so that
code only pages 'down' across one (row) dimension.
"""

_GET_BUCKET_TYPE_OF_DIM_INDEX = {
    0: BucketType.ROWS,
    1: BucketType.COLS,
}

_GET_DIM_INDEX_OF_BUCKET_TYPE = {
    BucketType.ROWS: 0,
    BucketType.COLS: 1,
}


class ExecutionTable:
    """
    Represents execution result as a table. This is a convenience wrapper for executions constructed using
    the following convention:

    -  all attributes are in the first dimension
    -  all metrics are in the second dimension
    -  if the execution is attribute- or metric-less, then there is always single dimension

    The mapping to rows is then as follows:

    -  both attributes + metrics are on the execution = iteration over first dimension; as many rows as total records
       in the first dimension (paging.total[0])
    -  just attributes = iteration over just headers in first dimension; as many rows as total records in the
       first dimension (paging.total[0])
    -  just metrics = single row, all metrics values returned in one row

    """

    def __init__(self, response: ExecutionResponse, first_page: ExecutionResult) -> None:
        self._exec_def = response.exec_def
        self._response = response
        self._first_page = first_page
        self._pages = [first_page]

    @property
    def result_id(self) -> str:
        return self._response.result_id

    @property
    def attributes(self) -> list[Attribute]:
        return self._exec_def.attributes

    @property
    def metrics(self) -> list[Metric]:
        return self._exec_def.metrics

    @property
    def column_ids(self) -> list[str]:
        """
        Returns column identifiers. Each row will be a mapping of column identifier to column data.
        """
        return [a.local_id for a in self.attributes] + [m.local_id for m in self.metrics]

    @property
    def column_metadata(self) -> dict[str, Union[Attribute, Metric]]:
        """
        Returns mapping of column identifier to definition of either attribute whose elements will be in that column
        or metric whose value will be calculated in that column.
        """
        return {**{a.local_id: a for a in self.attributes}, **{m.local_id: m for m in self.metrics}}

    def _read_next_page(self) -> bool:
        if not self._exec_def.has_attributes():
            # result without attributes has just one row with all the metrics, there is no next page to load
            return False

        last_loaded = self._pages[-1]
        offset = last_loaded.paging_offset
        count = last_loaded.paging_count
        total = last_loaded.paging_total

        # no more data on the backend, bail out
        if offset[0] + count[0] >= total[0]:
            return False

        next_offset = [offset[0] + count[0]] + offset[1:]
        # backend is smart enough to cap if the limit is greater than number of remaining rows
        next_limit = [_TABLE_ROW_BATCH_SIZE] + count[1:]

        next_page = self._response.read_result(offset=next_offset, limit=next_limit)

        self._pages.append(next_page)

        return True

    def _read_all_metrics_in_one_row(self) -> Generator[dict[str, Any], None, None]:
        data = self._first_page.data
        cols = self.column_ids

        yield dict(zip(cols, data))

    def _read_all_paged(self) -> Generator[dict[str, Any], None, None]:
        page_idx = 0
        cols = self.column_ids

        while page_idx < len(self._pages):
            page = self._pages[page_idx]
            attribute_headers = page.headers[0]
            data = page.data
            paging = page.paging
            page_row_idx = 0

            # yield all data from current page
            while page_row_idx < paging["count"][0]:
                headers = [
                    header["headers"][page_row_idx]["attributeHeader"]["labelValue"]
                    for header in attribute_headers["headerGroups"]
                ]
                metric_data = data[page_row_idx] if self._exec_def.has_metrics() else []

                yield dict(zip(cols, headers + metric_data))
                page_row_idx += 1

            # try to read next page of data. False means the end was reached so just bail out
            if not self._read_next_page():
                break

            # otherwise the self._pages was updated so go on with next page
            page_idx += 1

    def read_all(self) -> Generator[dict[str, Any], None, None]:
        """
        Returns a generator that will be yielding execution result as rows. Each row is a dict() mapping column
        identifier to value of that column.

        :return: generator yielding dict() representing rows of the table
        """
        if not self._exec_def.has_attributes():
            return self._read_all_metrics_in_one_row()

        return self._read_all_paged()

    def __len__(self) -> int:
        if self._exec_def.has_attributes():
            # if there are attributes in the result, then the sheet will be sliced with one row per
            # attribute => whatever the paging says is total for the first dimension is the number of rows
            return self._first_page.paging_total[0]
        else:
            # if there are no attributes in the result, then the sheet contains at most one row with all
            # metric values in it; now due such result being single dim, code looks at number of computed metric
            # values in that single dim. if there are any, then there will be one row
            return 1 if self._first_page.paging_total[0] > 0 else 0

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"ExecutionTable(response={self._response}, columns={self.column_ids}, rows={len(self)})"


def _prepare_tabular_definition(
    attributes: list[Attribute], filters: list[Filter], metrics: list[Metric]
) -> ExecutionDefinition:
    dims = [
        [a.local_id for a in attributes] if len(attributes) else None,
        ["measureGroup"] if len(metrics) else None,
    ]

    return ExecutionDefinition(attributes=attributes, metrics=metrics, filters=filters, dimensions=dims)


def _as_table(response: ExecutionResponse) -> ExecutionTable:
    first_page_offset = [0, 0]
    first_page_limit = [_TABLE_ROW_BATCH_SIZE, _MAX_METRICS]

    if not response.exec_def.has_attributes():
        # there are no attributes, there shall be at most one row with the metrics, so get that as first page
        first_page_limit = [first_page_limit[1]]
        first_page_offset = [0]
    elif not response.exec_def.has_metrics():
        # there are no metrics; there may be many attribute headers
        first_page_limit = [first_page_limit[0]]
        first_page_offset = [0]

    first_page = response.read_result(offset=first_page_offset, limit=first_page_limit)

    return ExecutionTable(response=response, first_page=first_page)


@define
class TableDimension:
    item_ids: list[str]
    idx: int
    sorting: Any


@define
class TotalDefinitionOrdering:
    function_order: int
    order: int
    total: TotalDefinition

    @classmethod
    def create(cls, total: TotalDefinition, measures: list[InsightMetric]) -> TotalDefinitionOrdering:
        metric_ordering = [m.local_id for m in measures]
        return cls(
            function_order=_TOTAL_ORDER.index(total.aggregation.upper()),
            order=metric_ordering.index(total.metric_local_id),
            total=total,
        )


def _create_dimension(bucket: InsightBucket, measures_item_identifier: Optional[str] = None) -> TableDimension:
    item_ids = [a.local_id for a in bucket.attributes]
    if measures_item_identifier is not None:
        item_ids.append(measures_item_identifier)
    return TableDimension(
        item_ids=item_ids,
        idx=_GET_DIM_INDEX_OF_BUCKET_TYPE[bucket.type],
        sorting=None,
    )


def _create_dimensions(insight: Insight) -> list[TableDimension]:
    # TODO: measures item id placement should reflect table transposition setting
    measures_item_identifier = _MEASURE_GROUP_IDENTIFIER if insight.metrics else None
    row_bucket = insight.get_bucket_of_type(BucketType.ROWS)
    col_bucket = insight.get_bucket_of_type(BucketType.COLS)
    return [
        _create_dimension(row_bucket),
        _create_dimension(col_bucket, measures_item_identifier),
    ]


def _marginal_total_local_identifier(total: InsightTotal, dim_idx: int) -> str:
    return f"marginal_total_{total.type}_{total.measure_id}_by_{total.attribute_id}_{dim_idx}"


def _sub_total_column_local_identifier(total: InsightTotal, dim_idx: int) -> str:
    return f"subtotal_column_{total.type}_{total.measure_id}_by_{total.attribute_id}_{dim_idx}"


def _sub_total_row_local_identifier(total: InsightTotal, dim_idx: int) -> str:
    return f"subtotal_row_{total.type}_{total.measure_id}_by_{total.attribute_id}_{dim_idx}"


def _grand_total_local_identifier(total: InsightTotal, dim_idx: int) -> str:
    return f"total_of_totals_{total.type}_{total.measure_id}_by_{total.attribute_id}_{dim_idx}"


def _total_local_identifier(total: InsightTotal, dim_idx: int) -> str:
    return f"total_{total.type}_{total.measure_id}_by_{total.attribute_id}_{dim_idx}"


def _convert_total_dimensions(
    total: InsightTotal, dimension: TableDimension, idx: int, all_dims: list[TableDimension]
) -> Any:
    item_idx = dimension.item_ids.index(total.attribute_id)
    total_dim_items = dimension.item_ids[0:item_idx]
    if _MEASURE_GROUP_IDENTIFIER in dimension.item_ids and _MEASURE_GROUP_IDENTIFIER not in total_dim_items:
        total_dim_items.append(_MEASURE_GROUP_IDENTIFIER)
    total_dims = [TotalDimension(idx=d.idx, items=d.item_ids) for d in all_dims if d.idx != idx]
    if len(total_dim_items) > 0:
        total_dims.append(TotalDimension(idx=idx, items=total_dim_items))
    return total_dims


def _get_additional_totals(insight: Insight, dimensions: list[TableDimension]) -> list[TotalDefinition]:
    totals: list[TotalDefinition] = []
    row_bucket = insight.get_bucket_of_type(BucketType.ROWS)
    col_bucket = insight.get_bucket_of_type(BucketType.COLS)
    row_attr_ids = [a.local_id for a in row_bucket.attributes]
    col_attr_ids = [a.local_id for a in col_bucket.attributes]
    measure_group_rows = [_MEASURE_GROUP_IDENTIFIER] if _MEASURE_GROUP_IDENTIFIER in dimensions[0].item_ids else []
    measure_group_cols = [_MEASURE_GROUP_IDENTIFIER] if _MEASURE_GROUP_IDENTIFIER in dimensions[1].item_ids else []
    for row_index, row_total in enumerate(row_bucket.totals):
        has_row_and_column_grand_totals = False
        has_row_and_column_sub_totals = False
        has_row_subtotal_and_column_grand_total = False
        has_column_subtotal_and_row_grand_total = False
        row_dimension_index = 0
        column_dimension_index = 0
        row_subtotal_dimension_index = 0
        column_subtotal_dimension_index = 0
        for col_index, col_total in enumerate(col_bucket.totals):
            # Check for totals from same measure and type
            if row_total.measure_id == col_total.measure_id and row_total.type == col_total.type:
                # Check for grand totals rows/columns
                # Grand total is always defined on the very first attribute of the attribute/columns bucket
                if row_total.attribute_id == row_attr_ids[0] and col_total.attribute_id == col_attr_ids[0]:
                    has_row_and_column_grand_totals = True

                # Check for subtotals rows/columns
                if row_total.attribute_id != row_attr_ids[0] and col_total.attribute_id != col_attr_ids[0]:
                    row_dimension_index = row_attr_ids.index(row_total.attribute_id)
                    column_dimension_index = col_attr_ids.index(col_total.attribute_id)
                    has_row_and_column_sub_totals = True

                # Check for rows subtotals within columns grand totals
                if row_total.attribute_id != row_attr_ids[0] and col_total.attribute_id == col_attr_ids[0]:
                    has_row_subtotal_and_column_grand_total = True
                    row_subtotal_dimension_index = row_attr_ids.index(row_total.attribute_id)

                # Check for columns subtotals within rows grand totals
                if row_total.attribute_id == row_attr_ids[0] and col_total.attribute_id != col_attr_ids[0]:
                    has_column_subtotal_and_row_grand_total = True
                    column_subtotal_dimension_index = col_attr_ids.index(col_total.attribute_id)

            # Extend marginal totals payload
            if has_row_and_column_sub_totals:
                totals.append(
                    TotalDefinition(
                        local_id=_marginal_total_local_identifier(row_total, col_index),
                        aggregation=row_total.type,
                        metric_local_id=row_total.measure_id,
                        total_dims=[
                            TotalDimension(
                                idx=0,
                                items=row_attr_ids[:row_dimension_index] + measure_group_rows,
                            ),
                            TotalDimension(
                                idx=1,
                                items=col_attr_ids[:column_dimension_index] + measure_group_cols,
                            ),
                        ],
                    )
                )

        # Extend marginal totals of rows within column grand totals payload
        if has_row_subtotal_and_column_grand_total:
            totals.append(
                TotalDefinition(
                    local_id=_sub_total_column_local_identifier(row_total, row_index),
                    aggregation=row_total.type,
                    metric_local_id=row_total.measure_id,
                    total_dims=[
                        TotalDimension(
                            idx=0,
                            items=row_attr_ids[:row_subtotal_dimension_index] + measure_group_rows,
                        ),
                        TotalDimension(
                            idx=1,
                            items=measure_group_cols,
                        ),
                    ],
                )
            )

        # Extend marginal of columns within rows grand totals payload
        if has_column_subtotal_and_row_grand_total:
            row_dim = [TotalDimension(idx=0, items=measure_group_rows)] if measure_group_rows else []
            col_dim = [
                TotalDimension(
                    idx=1,
                    items=col_attr_ids[:column_subtotal_dimension_index] + measure_group_cols,
                )
            ]
            totals.append(
                TotalDefinition(
                    local_id=_sub_total_row_local_identifier(row_total, row_index),
                    aggregation=row_total.type,
                    metric_local_id=row_total.measure_id,
                    total_dims=row_dim + col_dim,
                )
            )

        # Extend grand totals payload
        if has_row_and_column_grand_totals:
            row_dim = [TotalDimension(idx=0, items=measure_group_rows)] if measure_group_rows else []
            col_dim = [TotalDimension(idx=1, items=measure_group_cols)] if measure_group_cols else []
            totals.append(
                TotalDefinition(
                    local_id=_grand_total_local_identifier(row_total, row_index),
                    aggregation=row_total.type,
                    metric_local_id=row_total.measure_id,
                    total_dims=row_dim + col_dim,
                )
            )
    return totals


def _get_computable_totals(insight: Insight, dimensions: list[TableDimension]) -> list[TotalDefinition]:
    processed_totals = []
    for dim in dimensions:
        bucket_type = _GET_BUCKET_TYPE_OF_DIM_INDEX[dim.idx]
        bucket = insight.get_bucket_of_type(bucket_type)
        dim_totals_with_order = []
        for total in bucket.totals:
            total_def = TotalDefinition(
                local_id=_total_local_identifier(total, dim.idx),
                aggregation=total.type,
                metric_local_id=total.measure_id,
                total_dims=_convert_total_dimensions(
                    total,
                    dim,
                    dim.idx,
                    dimensions,
                ),
            )
            dim_totals_with_order.append(TotalDefinitionOrdering.create(total_def, insight.metrics))
        dim_totals_with_order.sort(key=attrgetter("function_order", "order"))
        processed_totals.append([t.total for t in dim_totals_with_order])

    totals = [total for dim_totals in processed_totals if dim_totals for total in dim_totals]

    if not insight.has_row_and_col_totals():
        return totals

    new_totals = _get_additional_totals(insight, dimensions)
    return totals + new_totals


def _get_exec_for_pivot(insight: Insight) -> ExecutionDefinition:
    dimensions = _create_dimensions(insight)
    totals = _get_computable_totals(insight, dimensions)
    return ExecutionDefinition(
        attributes=[a.as_computable() for a in insight.attributes],
        metrics=[m.as_computable() for m in insight.metrics],
        filters=[cf for cf in [f.as_computable() for f in insight.filters] if not cf.is_noop()],
        dimensions=[d.item_ids for d in dimensions],
        totals=totals,
    )


def get_exec_for_non_pivot(insight: Insight) -> ExecutionDefinition:
    return _prepare_tabular_definition(
        attributes=[a.as_computable() for a in insight.attributes],
        metrics=[m.as_computable() for m in insight.metrics],
        filters=[cf for cf in [f.as_computable() for f in insight.filters] if not cf.is_noop()],
    )


class TableService:
    """
    The TableService provides a convenient way to drive computations and access the results in a tabular fashion.

    Compared to the ComputeService, with this one here you do not have to worry about the layout of the result and
    do not have to work with execution response, access the data using paging.

    The ExecutionTable returned by the TableService allows you to iterate over the rows of the calculated data.
    """

    def __init__(self, api_client: GoodDataApiClient) -> None:
        self._compute = ComputeService(api_client)

    def for_insight(self, workspace_id: str, insight: Insight) -> ExecutionTable:
        # Assume the received insight is a pivot table if it contains row ("attribute") bucket
        exec_def = (
            _get_exec_for_pivot(insight)
            if insight.has_bucket_of_type(BucketType.ROWS)
            else get_exec_for_non_pivot(insight)
        )
        response = self._compute.for_exec_def(workspace_id=workspace_id, exec_def=exec_def)
        return _as_table(response)

    def for_items(
        self, workspace_id: str, items: list[Union[Attribute, Metric]], filters: Optional[list[Filter]] = None
    ) -> ExecutionTable:
        if filters is None:
            filters = []

        attributes: list[Attribute] = []
        metrics: list[Metric] = []

        for item in items:
            if isinstance(item, Attribute):
                attributes.append(item)
            elif isinstance(item, Metric):
                metrics.append(item)
            else:
                raise ValueError(f"Invalid input item: {item}. Expecting instance of Attribute or Metric")

        exec_def = _prepare_tabular_definition(attributes=attributes, metrics=metrics, filters=filters)
        response = self._compute.for_exec_def(workspace_id=workspace_id, exec_def=exec_def)

        return _as_table(response)
