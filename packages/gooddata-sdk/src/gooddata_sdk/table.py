# (C) 2021 GoodData Corporation
from __future__ import annotations

import logging
from collections.abc import Generator
from operator import attrgetter
from typing import Any, Callable, Optional, Union

from attrs import define, field, frozen
from attrs.setters import frozen as frozen_attr

from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.compute.model.attribute import Attribute
from gooddata_sdk.compute.model.execution import (
    ExecutionDefinition,
    ExecutionResponse,
    ExecutionResult,
    TotalDefinition,
    TotalDimension,
)
from gooddata_sdk.compute.model.execution import TableDimension as ExecTableDimension
from gooddata_sdk.compute.model.filter import Filter
from gooddata_sdk.compute.model.metric import Metric
from gooddata_sdk.compute.service import ComputeService
from gooddata_sdk.visualization import (
    AttributeSortType,
    BucketType,
    LocatorItemType,
    SortDirection,
    SortType,
    Visualization,
    VisualizationBucket,
    VisualizationMetric,
    VisualizationSort,
    VisualizationSortLocator,
    VisualizationTotal,
)

logger = logging.getLogger(__name__)

_MEASURE_GROUP_IDENTIFIER = "measureGroup"
_TOTAL_ORDER = ["SUM", "MAX", "MIN", "AVG", "MED", "NAT"]

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

_ATTR_SORT_TYPE_TO_API = {
    AttributeSortType.UNDEFINED: "",
    AttributeSortType.DEFAULT: "DEFAULT",
    AttributeSortType.AREA: "AREA",
}


@define
class TableDimension:
    """Dataclass used during total and dimension computation."""

    item_ids: list[str] = field(on_setattr=frozen_attr)
    idx: int = field(on_setattr=frozen_attr)
    sorting: list[dict] = field(default=[])

    def to_exec_table_dimension(self) -> ExecTableDimension:
        return ExecTableDimension(
            item_ids=self.item_ids,
            sorting=self.sorting,
        )


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
        ExecTableDimension(
            item_ids=[a.local_id for a in attributes] if attributes else None,
        ),
        ExecTableDimension(
            item_ids=[_MEASURE_GROUP_IDENTIFIER] if metrics else None,
        ),
    ]

    return ExecutionDefinition(attributes=attributes, metrics=metrics, filters=filters, dimensions=dims)


def _as_table(response: ExecutionResponse, always_two_dimensional: bool = False) -> ExecutionTable:
    first_page_offset = [0, 0]
    first_page_limit = [_TABLE_ROW_BATCH_SIZE, _MAX_METRICS]

    # always adjust paging based on presence of metrics/attrs if not always_two_dimensional
    # (behavior expected in FDW), otherwise, adjust if response contains only one-dimensional data
    if not always_two_dimensional or len(response.dimensions) == 1:
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


@frozen
class TotalDefinitionOrdering:
    """Dataclass used for ordering of total definitions."""

    function_order: int
    order: int
    total: TotalDefinition

    @classmethod
    def create(cls, total: TotalDefinition, measures: list[VisualizationMetric]) -> TotalDefinitionOrdering:
        metric_ordering = [m.local_id for m in measures]
        return cls(
            function_order=_TOTAL_ORDER.index(total.aggregation.upper()),
            order=metric_ordering.index(total.metric_local_id),
            total=total,
        )


@frozen
class AttributeLocator:
    attribute_identifier: str
    element: str

    def to_kv(self) -> tuple[str, str]:
        return self.attribute_identifier, self.element


@frozen
class MeasureLocator:
    measure_identifier: str

    def to_kv(self) -> tuple[str, str]:
        return _MEASURE_GROUP_IDENTIFIER, self.measure_identifier


Locator = Union[AttributeLocator, MeasureLocator]


@frozen
class SortKeyAttribute:
    sort_type: SortType
    direction: SortDirection
    attribute_identifier: str
    attribute_sort_type: AttributeSortType

    def to_dict(self) -> dict:
        return {
            "attribute": {
                "attributeIdentifier": self.attribute_identifier,
                "direction": self.direction.upper(),
                "sortType": _ATTR_SORT_TYPE_TO_API[self.attribute_sort_type],
            }
        }


@frozen
class SortKeyValue:
    sort_type: SortType
    direction: SortDirection
    measure_dim_identifier: str
    data_column_locators: list[Locator]

    def to_dict(self) -> dict:
        locator_tuples = [locator.to_kv() for locator in self.data_column_locators]
        return {
            "value": {
                "dataColumnLocators": {self.measure_dim_identifier: {k: v for k, v in locator_tuples}},
                "direction": self.direction.upper(),
            }
        }


SortKey = Union[SortKeyAttribute, SortKeyValue]


def _create_data_col_locators(locators: list[VisualizationSortLocator]) -> list[Locator]:
    converted_locators: list[Locator] = []
    for locator in locators:
        if locator.type == LocatorItemType.ATTRIBUTE:
            converted_locators.append(
                AttributeLocator(
                    attribute_identifier=locator.locator["attributeIdentifier"],
                    element=locator.locator["element"],
                )
            )
        if locator.type == LocatorItemType.MEASURE:
            converted_locators.append(
                MeasureLocator(
                    measure_identifier=locator.locator["measureIdentifier"],
                )
            )
    return converted_locators


def _get_dim_idx_for_predicate(
    dims: list[TableDimension], predicate: Callable[[TableDimension], bool]
) -> Optional[int]:
    for dim_idx, dim in enumerate(dims):
        if predicate(dim):
            return dim_idx
    return None


def _append_attribute_sort_key(
    dims: list[TableDimension], sort_item: VisualizationSort, sorting: list[list[SortKey]]
) -> None:
    dim_idx = _get_dim_idx_for_predicate(dims, lambda x: sort_item.attribute_identifier in x.item_ids)
    if dim_idx is None:
        log_msg = (
            f'attempting to sort by attribute with localId "{sort_item.attribute_identifier}" '
            "but this attribute is not in any dimension."
        )
        logger.warning(log_msg)
        return

    sorting[dim_idx].append(
        SortKeyAttribute(
            sort_type=sort_item.type,
            direction=sort_item.direction,
            attribute_identifier=sort_item.attribute_identifier,
            attribute_sort_type=sort_item.attribute_sort_type,
        )
    )


def _append_measure_sort_key(
    measure_dim: Optional[TableDimension],
    non_measure_dim_idx: Optional[int],
    sort_item: VisualizationSort,
    sorting: list[list[SortKey]],
) -> None:
    if non_measure_dim_idx is None:
        logger.warning(
            "Trying to use measure sort in an execution that only contains dimension with MeasureGroup. "
            "This is not valid sort. Measure sort is used to sort the non-measure dimension by values "
            "from measure dimension. Skipping."
        )
        return

    if not measure_dim:
        logger.warning("Trying to use measure sort in an execution that does not contain MeasureGroup. Skipping.")
        return

    sorting[non_measure_dim_idx].append(
        SortKeyValue(
            sort_type=sort_item.type,
            direction=sort_item.direction,
            measure_dim_identifier=f"dim_{measure_dim.idx}",
            data_column_locators=_create_data_col_locators(sort_item.locators),
        )
    )


def _merge_dims_with_sorting(dims: list[TableDimension], sorting: list[list[SortKey]]) -> list[TableDimension]:
    for dim in dims:
        dim_sorting = sorting[dim.idx]
        if dim_sorting:
            dim.sorting = [ds.to_dict() for ds in dim_sorting]
    return dims


def _create_dims_with_sorts(dims: list[TableDimension], sorts: list[VisualizationSort]) -> list[TableDimension]:
    """
    Places sorting into dimensions. Returns the same dimensions objects but with modified sorting.

    Tiger does sorting differently from bear so this is somewhat more complicated than pure object conversions.

    1. Sorting is now placed in the dimension that has to be sorted
    2. When sorting by attribute (headers), then the attribute sort key must be placed into the dimension that
       contains the attribute
    3. When sorting by measure, we now fall back to 'bear-like' behavior: the dimension opposite to the one
       that contains the measures will be sorted. It will be sorted using the measure (possibly scoped for
       particular attribute values) located in the MeasureGroup dimension.

    At the end, this function walks the sort items in the order defined by the user and distributes them into
    the dimensions. The function is lenient for now and will log warnings and ignore anything weird that it
    cannot process (e.g. measure sorting when there is no dim with MeasureGroup, or if there is only dim with
    MeasureGroup and no other dim).

    @param dims - dimensions to add sorting to
    @param sorts - sort items defined by SDK user
    """
    if not sorts:
        return dims

    non_measure_dim_idx = _get_dim_idx_for_predicate(dims, lambda x: _MEASURE_GROUP_IDENTIFIER not in x.item_ids)
    measure_dim_idx = _get_dim_idx_for_predicate(dims, lambda x: _MEASURE_GROUP_IDENTIFIER in x.item_ids)
    measure_dim = dims[measure_dim_idx] if measure_dim_idx else None

    sorting: list[list[SortKey]] = [[] for _ in dims]

    for sort_item in sorts:
        if sort_item.type == SortType.ATTRIBUTE:
            _append_attribute_sort_key(dims, sort_item, sorting)
        if sort_item.type == SortType.MEASURE:
            _append_measure_sort_key(measure_dim, non_measure_dim_idx, sort_item, sorting)

    return _merge_dims_with_sorting(dims, sorting)


def _vis_is_transposed(visualization: Visualization) -> bool:
    controls = visualization.properties.get("controls")
    if not controls:
        return False
    return controls.get("measureGroupDimension") == "rows"


def _create_dimension(bucket: VisualizationBucket, measures_item_identifier: Optional[str] = None) -> TableDimension:
    item_ids = [a.local_id for a in bucket.attributes]
    if measures_item_identifier is not None:
        item_ids.append(measures_item_identifier)
    return TableDimension(
        item_ids=item_ids,
        idx=_GET_DIM_INDEX_OF_BUCKET_TYPE[bucket.type],
    )


def _create_dimensions(visualization: Visualization) -> list[TableDimension]:
    measures_item_identifier = _MEASURE_GROUP_IDENTIFIER if visualization.metrics else None
    row_bucket = visualization.get_bucket_of_type(BucketType.ROWS)
    col_bucket = visualization.get_bucket_of_type(BucketType.COLS)
    is_transposed = _vis_is_transposed(visualization)
    row_measure_item_identifier = measures_item_identifier if is_transposed else None
    col_measure_item_identifier = None if is_transposed else measures_item_identifier
    dims = [
        _create_dimension(row_bucket, row_measure_item_identifier),
        _create_dimension(col_bucket, col_measure_item_identifier),
    ]
    return _create_dims_with_sorts(dims, visualization.sorts)


def _marginal_total_local_identifier(total: VisualizationTotal, dim_idx: int) -> str:
    return f"marginal_total_{total.type}_{total.measure_id}_by_{total.attribute_id}_{dim_idx}"


def _sub_total_column_local_identifier(total: VisualizationTotal, dim_idx: int) -> str:
    return f"subtotal_column_{total.type}_{total.measure_id}_by_{total.attribute_id}_{dim_idx}"


def _sub_total_row_local_identifier(total: VisualizationTotal, dim_idx: int) -> str:
    return f"subtotal_row_{total.type}_{total.measure_id}_by_{total.attribute_id}_{dim_idx}"


def _grand_total_local_identifier(total: VisualizationTotal, dim_idx: int) -> str:
    return f"total_of_totals_{total.type}_{total.measure_id}_by_{total.attribute_id}_{dim_idx}"


def _total_local_identifier(total: VisualizationTotal, dim_idx: int) -> str:
    return f"total_{total.type}_{total.measure_id}_by_{total.attribute_id}_{dim_idx}"


def _convert_total_dimensions(
    total: VisualizationTotal, dimension: TableDimension, idx: int, all_dims: list[TableDimension]
) -> Any:
    item_idx = dimension.item_ids.index(total.attribute_id)
    total_dim_items = dimension.item_ids[0:item_idx]
    if _MEASURE_GROUP_IDENTIFIER in dimension.item_ids and _MEASURE_GROUP_IDENTIFIER not in total_dim_items:
        total_dim_items.append(_MEASURE_GROUP_IDENTIFIER)
    total_dims = [TotalDimension(idx=d.idx, items=d.item_ids) for d in all_dims if d.idx != idx]
    if len(total_dim_items) > 0:
        total_dims.append(TotalDimension(idx=idx, items=total_dim_items))
    return total_dims


@define
class TotalsComputeInfo:
    """Dataclass containing different values used for special case construction of pivot table totals."""

    row_attr_ids: list[str] = field(on_setattr=frozen_attr)
    col_attr_ids: list[str] = field(on_setattr=frozen_attr)
    measure_group_rows: list[str] = field(on_setattr=frozen_attr)
    measure_group_cols: list[str] = field(on_setattr=frozen_attr)
    has_row_and_column_grand_totals: bool = False
    has_row_and_column_sub_totals: bool = False
    has_row_subtotal_and_column_grand_total: bool = False
    has_column_subtotal_and_row_grand_total: bool = False
    row_dimension_index: int = 0
    column_dimension_index: int = 0
    row_subtotal_dimension_index: int = 0
    column_subtotal_dimension_index: int = 0

    def reset_to_defaults(self) -> None:
        """Resets mutable fields to theirs default values."""
        self.has_row_and_column_grand_totals = False
        self.has_row_and_column_sub_totals = False
        self.has_row_subtotal_and_column_grand_total = False
        self.has_column_subtotal_and_row_grand_total = False
        self.row_dimension_index = 0
        self.column_dimension_index = 0
        self.row_subtotal_dimension_index = 0
        self.column_subtotal_dimension_index = 0

    def update_compute_info(self, col_total_attr_id: str, row_total_attr_id: str) -> None:
        """Update decision and index variables for totals construction."""
        # Check for grand totals rows/columns
        # Grand total is always defined on the very first attribute of the attribute/columns bucket
        if row_total_attr_id == self.row_attr_ids[0] and col_total_attr_id == self.col_attr_ids[0]:
            self.has_row_and_column_grand_totals = True
        # Check for subtotals rows/columns
        if row_total_attr_id != self.row_attr_ids[0] and col_total_attr_id != self.col_attr_ids[0]:
            self.has_row_and_column_sub_totals = True
            self.row_dimension_index = self.row_attr_ids.index(row_total_attr_id)
            self.column_dimension_index = self.col_attr_ids.index(col_total_attr_id)
        # Check for rows subtotals within columns grand totals
        if row_total_attr_id != self.row_attr_ids[0] and col_total_attr_id == self.col_attr_ids[0]:
            self.has_row_subtotal_and_column_grand_total = True
            self.row_subtotal_dimension_index = self.row_attr_ids.index(row_total_attr_id)
        # Check for columns subtotals within rows grand totals
        if row_total_attr_id == self.row_attr_ids[0] and col_total_attr_id != self.col_attr_ids[0]:
            self.has_column_subtotal_and_row_grand_total = True
            self.column_subtotal_dimension_index = self.col_attr_ids.index(col_total_attr_id)


def _extend_marginal_totals(col_index: int, row_total: VisualizationTotal, tci: TotalsComputeInfo) -> TotalDefinition:
    # Extend marginal totals payload
    return TotalDefinition(
        local_id=_marginal_total_local_identifier(row_total, col_index),
        aggregation=row_total.type,
        metric_local_id=row_total.measure_id,
        total_dims=[
            TotalDimension(
                idx=0,
                items=tci.row_attr_ids[: tci.row_dimension_index] + tci.measure_group_rows,
            ),
            TotalDimension(
                idx=1,
                items=tci.col_attr_ids[: tci.column_dimension_index] + tci.measure_group_cols,
            ),
        ],
    )


def _extend_marginal_totals_of_cols(
    row_index: int, row_total: VisualizationTotal, tci: TotalsComputeInfo
) -> TotalDefinition:
    # Extend marginal of columns within rows grand totals payload
    row_dim = [TotalDimension(idx=0, items=tci.measure_group_rows)] if tci.measure_group_rows else []
    col_dim = [
        TotalDimension(
            idx=1,
            items=tci.col_attr_ids[: tci.column_subtotal_dimension_index] + tci.measure_group_cols,
        )
    ]
    return TotalDefinition(
        local_id=_sub_total_row_local_identifier(row_total, row_index),
        aggregation=row_total.type,
        metric_local_id=row_total.measure_id,
        total_dims=row_dim + col_dim,
    )


def _extend_marginal_totals_of_rows(
    row_index: int, row_total: VisualizationTotal, tci: TotalsComputeInfo
) -> TotalDefinition:
    # Extend marginal totals of rows within column grand totals payload
    return TotalDefinition(
        local_id=_sub_total_column_local_identifier(row_total, row_index),
        aggregation=row_total.type,
        metric_local_id=row_total.measure_id,
        total_dims=[
            TotalDimension(
                idx=0,
                items=tci.row_attr_ids[: tci.row_subtotal_dimension_index] + tci.measure_group_rows,
            ),
            TotalDimension(
                idx=1,
                items=tci.measure_group_cols,
            ),
        ],
    )


def _extend_grand_totals(row_index: int, row_total: VisualizationTotal, tci: TotalsComputeInfo) -> TotalDefinition:
    # Extend grand totals payload
    row_dim = [TotalDimension(idx=0, items=tci.measure_group_rows)] if tci.measure_group_rows else []
    col_dim = [TotalDimension(idx=1, items=tci.measure_group_cols)] if tci.measure_group_cols else []
    return TotalDefinition(
        local_id=_grand_total_local_identifier(row_total, row_index),
        aggregation=row_total.type,
        metric_local_id=row_total.measure_id,
        total_dims=row_dim + col_dim,
    )


def _get_additional_totals(visualization: Visualization, dimensions: list[TableDimension]) -> list[TotalDefinition]:
    """Construct special cases of pivot table totals.

    These special cases are -
      1. Grand totals - is the value obtained from row and column totals.
      2. Marginal totals - is the value obtained within the subgroups from row and column subtotals.

    For `Grand Totals`, in Tiger AFM, you specify that you want total of totals with total that have only
    "measureGroup" present.
    For `Marginal Total`, in Tiger AFM, would need to iterate through both dimensions and obtain the missing
    totalDimensions items based on the attribute and column identifiers order in buckets.
    """
    totals: list[TotalDefinition] = []
    row_bucket = visualization.get_bucket_of_type(BucketType.ROWS)
    col_bucket = visualization.get_bucket_of_type(BucketType.COLS)

    tci = TotalsComputeInfo(
        row_attr_ids=[a.local_id for a in row_bucket.attributes],
        col_attr_ids=[a.local_id for a in col_bucket.attributes],
        measure_group_rows=[_MEASURE_GROUP_IDENTIFIER] if _MEASURE_GROUP_IDENTIFIER in dimensions[0].item_ids else [],
        measure_group_cols=[_MEASURE_GROUP_IDENTIFIER] if _MEASURE_GROUP_IDENTIFIER in dimensions[1].item_ids else [],
    )
    for row_index, row_total in enumerate(row_bucket.totals):
        tci.reset_to_defaults()
        for col_index, col_total in enumerate(col_bucket.totals):
            # Check for totals from same measure and type
            if row_total.measure_id == col_total.measure_id and row_total.type == col_total.type:
                tci.update_compute_info(col_total.attribute_id, row_total.attribute_id)

            if tci.has_row_and_column_sub_totals:
                totals.append(_extend_marginal_totals(col_index, row_total, tci))

        if tci.has_row_subtotal_and_column_grand_total:
            totals.append(_extend_marginal_totals_of_rows(row_index, row_total, tci))

        if tci.has_column_subtotal_and_row_grand_total:
            totals.append(_extend_marginal_totals_of_cols(row_index, row_total, tci))

        if tci.has_row_and_column_grand_totals:
            totals.append(_extend_grand_totals(row_index, row_total, tci))

    return totals


def _get_computable_totals(visualization: Visualization, dimensions: list[TableDimension]) -> list[TotalDefinition]:
    """
    Extracts total definitions from execution definition dimensions and converts them into total specifications for
    Tiger AFM. Execution definition defines totals by a measure, aggregation function, and the attribute for whose
    values we want the totals. In Tiger, measure and aggregation function remain the same, but the `totalDimensions`
    with `totalDimensionItems` are best understood as coordinates for the resulting structure where the totals
    should be placed. This implicitly decides which attributes should be used. This allows for multidimensional totals,
    but such totals are impossible to define in the execution definition.
    """
    processed_totals = []
    for dim in dimensions:
        bucket_type = _GET_BUCKET_TYPE_OF_DIM_INDEX[dim.idx]
        bucket = visualization.get_bucket_of_type(bucket_type)
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
            dim_totals_with_order.append(TotalDefinitionOrdering.create(total_def, visualization.metrics))
        dim_totals_with_order.sort(key=attrgetter("function_order", "order"))
        processed_totals.append([t.total for t in dim_totals_with_order])

    totals = [total for dim_totals in processed_totals if dim_totals for total in dim_totals]

    if not visualization.has_row_and_col_totals():
        return totals

    new_totals = _get_additional_totals(visualization, dimensions)
    return totals + new_totals


def _get_exec_for_pivot(visualization: Visualization) -> ExecutionDefinition:
    dimensions = _create_dimensions(visualization)
    totals = _get_computable_totals(visualization, dimensions)
    return ExecutionDefinition(
        attributes=[a.as_computable() for a in visualization.attributes],
        metrics=[m.as_computable() for m in visualization.metrics],
        filters=[cf for cf in [f.as_computable() for f in visualization.filters] if not cf.is_noop()],
        dimensions=[dim.to_exec_table_dimension() for dim in dimensions],
        totals=totals,
    )


def get_exec_for_non_pivot(visualization: Visualization) -> ExecutionDefinition:
    return _prepare_tabular_definition(
        attributes=[a.as_computable() for a in visualization.attributes],
        metrics=[m.as_computable() for m in visualization.metrics],
        filters=[cf for cf in [f.as_computable() for f in visualization.filters] if not cf.is_noop()],
    )


def _vis_is_table(visualization: Visualization) -> bool:
    attributes = visualization._vo.get("attributes")
    if not attributes:
        return False
    content = attributes.get("content")
    if not content:
        return False
    vis_url = content.get("visualizationUrl")
    if not vis_url:
        return False
    return vis_url.split(":")[-1] == "table"


class TableService:
    """
    The TableService provides a convenient way to drive computations and access the results in a tabular fashion.

    Compared to the ComputeService, with this one here you do not have to worry about the layout of the result and
    do not have to work with execution response, access the data using paging.

    The ExecutionTable returned by the TableService allows you to iterate over the rows of the calculated data.
    """

    def __init__(self, api_client: GoodDataApiClient) -> None:
        self._compute = ComputeService(api_client)

    def for_visualization(
        self, workspace_id: str, visualization: Visualization, always_two_dimensional: bool = False
    ) -> ExecutionTable:
        # Assume the received visualization is a pivot table if:
        # - we can parse out "table" suffix from the attributes.contents.visualizationUrl
        # or
        # - it contains row ("attribute") bucket

        # use always_two_dimensional to ignore special handling of cases where the visualization
        # to be executed should contain only metrics and no attributes or vice-versa.
        exec_def = (
            _get_exec_for_pivot(visualization)
            if _vis_is_table(visualization) or visualization.has_bucket_of_type(BucketType.ROWS)
            else get_exec_for_non_pivot(visualization)
        )
        response = self._compute.for_exec_def(workspace_id=workspace_id, exec_def=exec_def)
        return _as_table(response, always_two_dimensional)

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
