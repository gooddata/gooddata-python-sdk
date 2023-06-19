# (C) 2022 GoodData Corporation
from __future__ import annotations

import logging
from typing import Any, Optional, Tuple, Union, dict

from attrs import define, field

import gooddata_api_client.models as models
from gooddata_api_client.model.afm import AFM
from gooddata_api_client.model.result_spec import ResultSpec
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.compute.model.attribute import Attribute
from gooddata_sdk.compute.model.filter import Filter
from gooddata_sdk.compute.model.metric import Metric

logger = logging.getLogger(__name__)


@define
class TotalDimension:
    idx: int
    """index of dimension in which to calculate the total"""

    items: list[str] = field(factory=list)
    """items to use during total calculation"""

    @classmethod
    def from_dict(cls, data: dict) -> "TotalDimension":
        """
        Converts a dictionary to a TotalDimension object.

        Args:
            data (dict):
                A dictionary containing the following keys:
                -'idx' (int):
                    Index of dimension in which to calculate the total
                -'items' (list of str):
                    Items to use during total calculation

        Returns:
            TotalDimension:
                A TotalDimension object with its 'idx' and 'items' attributes set.
        """
        idx = data.get("idx")
        items = data.get("items")
        return cls(idx=idx, items=items)


@define
class TotalDefinition:
    local_id: str
    """total's local identifier"""

    aggregation: str
    """aggregation function; case insensitive; one of SUM, MIN, MAX, MED, AVG"""

    metric_local_id: str
    """local identifier of the measure to calculate total for"""

    total_dims: list[TotalDimension]

    @classmethod
    def from_dict(cls, data: dict) -> "TotalDefinition":
        """
        Create a TotalDefinition instance from a dictionary.

        Args:
            data (dict):
                Dictionary containing the following keys:
                - local_id (str):
                    Total's local identifier.
                - aggregation (str):
                    Aggregation function (case insensitive); one of SUM, MIN, MAX, MED, AVG.
                - metric_local_id (str):
                    Local identifier of the measure to calculate total for.
                - total_dims (list):
                    List of TotalDimension instances or dictionaries that can be converted to TotalDimension.

        Returns:
            TotalDefinition:
                A TotalDefinition instance created from the input dictionary.
        """
        local_id = data["local_id"]
        aggregation = data["aggregation"]
        metric_local_id = data["metric_local_id"]
        total_dims = [TotalDimension.from_dict(dim_data) for dim_data in data["total_dims"]]
        return cls(local_id, aggregation, metric_local_id, total_dims)


class ExecutionDefinition:
    def __init__(
        self,
        attributes: Optional[list[Attribute]],
        metrics: Optional[list[Metric]],
        filters: Optional[list[Filter]],
        dimensions: list[Optional[list[str]]],
        totals: Optional[list[TotalDefinition]] = None,
    ) -> None:
        self._attributes = attributes or []
        self._metrics = metrics or []
        self._filters = filters or []
        self._dimensions = [dim for dim in dimensions if dim is not None]
        self._totals = totals

    @classmethod
    def from_dict(cls, input_dict: dict):
        """
        Create an ExecutionDefinition instance from a dictionary.

        Args:
            input_dict (dict):
                A dictionary containing the following keys:
            - attributes (list[dict]):
                List of dictionaries containing the following keys:
                - local_id' (str):
                    identifier of the attribute within the execution
                - label (str):
                    identifier of the label to use for slicing or dicing;
                    specified either as ObjId or str containing the label id
                - show_all_values (Optional[bool]):
                    request show all values functionality for a given attribute
            - metrics (list[dict]):
                List of dictionaries containing the key:
                - local_id (str):
                    Metric ID.

            - filters (list[dict]):
            List of Dictionaries dictionary containing the key:
                - 'apply_on_result' (Optional[bool]):
                    Whether the Filter is applied
            - dimensions (list[Optional[list[str]]]):
                List of two lists, where the first list represents attributes in rows and the second list
                represents attributes in columns. The second list also includes a 'measureGroup' constant,
                if the metrics are non-empty.
            - totals (list[dict]):
                List of dictionaries containing the following keys:
                - local_id (str): Total's local identifier.
                - aggregation (str):
                    Aggregation function (case insensitive); one of SUM, MIN, MAX, MED, AVG.
                - metric_local_id (str):
                    Local identifier of the measure to calculate total for.
                - total_dims (list):
                    List of TotalDimension instances or dictionaries that can be converted to TotalDimension.

        Returns:
            ExecutionDefinition: An instance of ExecutionDefinition constructed using the input_dict's entries.
        """
        attributes = [Attribute.from_dict(attr) for attr in input_dict.get("attributes", [])]
        metrics = [Metric.from_dict(m) for m in input_dict.get("metrics", [])]
        filters = [Filter.from_dict(f) for f in input_dict.get("filters", [])]
        dimensions = input_dict.get("dimensions", [])
        totals = [TotalDefinition.from_dict(t) for t in input_dict.get("totals", [])]

        return cls(attributes, metrics, filters, dimensions, totals)

    @property
    def attributes(self) -> list[Attribute]:
        return self._attributes

    def has_attributes(self) -> bool:
        return self.attributes is not None and len(self.attributes) > 0

    @property
    def metrics(self) -> list[Metric]:
        return self._metrics

    def has_metrics(self) -> bool:
        return self.metrics is not None and len(self.metrics) > 0

    @property
    def filters(self) -> list[Filter]:
        return self._filters

    def has_filters(self) -> bool:
        return self.filters is not None and len(self.filters) > 0

    @property
    def dimensions(self) -> list[list[str]]:
        return self._dimensions

    def is_one_dim(self) -> bool:
        return len(self.dimensions) == 1

    def is_two_dim(self) -> bool:
        return len(self.dimensions) == 2

    def _create_dimensions(self) -> list[models.Dimension]:
        dimensions = []
        for idx, dim in enumerate(self._dimensions):
            dimensions.append(models.Dimension(local_identifier=f"dim_{idx}", item_identifiers=dim))

        return dimensions

    def _create_totals(self) -> Optional[list[models.Total]]:
        if not self._totals:
            return None

        totals = []
        for total in self._totals:
            total_dims = [
                models.TotalDimension(
                    dimension_identifier=f"dim_{total_dim.idx}", total_dimension_items=total_dim.items
                )
                for total_dim in total.total_dims
            ]

            totals.append(
                models.Total(
                    local_identifier=total.local_id,
                    metric=total.metric_local_id,
                    function=total.aggregation.upper(),
                    total_dimensions=total_dims,
                )
            )

        return totals

    def _create_result_spec(self) -> models.ResultSpec:
        dimensions = self._create_dimensions()
        totals = self._create_totals()

        if totals is None:
            return models.ResultSpec(dimensions=dimensions)

        return models.ResultSpec(dimensions=dimensions, totals=totals)

    def as_api_model(self) -> models.AfmExecution:
        execution = compute_model_to_api_model(attributes=self.attributes, metrics=self.metrics, filters=self.filters)
        result_spec = self._create_result_spec()

        return models.AfmExecution(execution=execution, result_spec=result_spec)


ResultSizeDimensions = Tuple[Optional[int], ...]


class ResultSizeDimensionsLimitsExceeded(Exception):
    def __init__(
        self,
        result_size_dimensions_limits: ResultSizeDimensions,
        actual_result_size_dimensions: ResultSizeDimensions,
        first_violating_index: int,
    ):
        self.result_size_dimensions_limits = tuple(result_size_dimensions_limits)
        self.actual_result_size = actual_result_size_dimensions
        self.first_violating_index = first_violating_index


class ExecutionResult:
    def __init__(self, result: models.ExecutionResult):
        self._data: list[Any] = result["data"]
        self._headers: list[models.DimensionHeader] = result["dimension_headers"]
        self._grand_totals: list[models.ExecutionResultGrandTotal] = result["grand_totals"]
        self._paging: models.ExecutionResultPaging = result["paging"]

    @property
    def data(self) -> list[Any]:
        return self._data

    @property
    def headers(self) -> list[models.DimensionHeader]:
        return self._headers

    @property
    def grand_totals(self) -> list[models.ExecutionResultGrandTotal]:
        return self._grand_totals

    @property
    def paging(self) -> models.ExecutionResultPaging:
        return self._paging

    @property
    def paging_total(self) -> list[int]:
        return self._paging["total"]

    @property
    def paging_count(self) -> list[int]:
        return self._paging["count"]

    @property
    def paging_offset(self) -> list[int]:
        return self._paging["offset"]

    def is_complete(self, dim: int = 0) -> bool:
        return self.paging_offset[dim] + self.paging_count[dim] >= self.paging_total[dim]

    def next_page_start(self, dim: int = 0) -> int:
        return self.paging_offset[dim] + self.paging_count[dim]

    def get_all_headers(self, dim: int) -> list[list[Any]]:
        header_groups = self.headers[dim]["headerGroups"]

        return [[header for header in header_groups[idx]["headers"]] for idx in range(len(header_groups))]

    def get_all_header_values(self, dim: int, header_idx: int) -> list[str]:
        return [
            header["attributeHeader"]["labelValue"]
            for header in self.headers[dim]["headerGroups"][header_idx]["headers"]
        ]

    def check_dimensions_size_limits(self, result_size_dimensions_limits: ResultSizeDimensions) -> None:
        for dim, dim_size in enumerate(self.paging_total):
            if dim >= len(result_size_dimensions_limits):
                return
            dim_limit = result_size_dimensions_limits[dim]
            if dim_size is None or dim_limit is None:
                continue
            if dim_size > dim_limit:
                raise ResultSizeDimensionsLimitsExceeded(
                    result_size_dimensions_limits=result_size_dimensions_limits,
                    actual_result_size_dimensions=tuple(self.paging_total),
                    first_violating_index=dim,
                )

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"ExecutionResult(paging={self.paging})"


class BareExecutionResponse:
    """
    Holds ExecutionResponse from triggered report computation and allows reading report's results.
    """

    def __init__(
        self,
        api_client: GoodDataApiClient,
        workspace_id: str,
        execution_response: models.AfmExecutionResponse,
    ):
        self._api_client = api_client
        self._actions_api = self._api_client.actions_api
        self._workspace_id = workspace_id

        self._exec_response: models.ExecutionResponse = execution_response["execution_response"]
        self._afm_exec_response = execution_response

    @property
    def workspace_id(self) -> str:
        return self._workspace_id

    @property
    def result_id(self) -> str:
        return self._exec_response["links"]["executionResult"]

    @property
    def dimensions(self) -> Any:
        return self._exec_response["dimensions"]

    def read_result(self, limit: Union[int, list[int]], offset: Union[None, int, list[int]] = None) -> ExecutionResult:
        """
        Reads from the execution result.
        """

        _offset = offset if isinstance(offset, list) else [offset] if offset is not None else None
        _limit = limit if isinstance(limit, list) else [limit]

        # if limit is specified but offset is not, server will ignore paging completely (bug)
        # this makes sure that offset gets defaulted to start of result
        _offset = [0 for _ in _limit] if _limit is not None and _offset is None else _offset

        execution_result, _, http_headers = self._actions_api.retrieve_result(
            workspace_id=self._workspace_id,
            result_id=self.result_id,
            offset=_offset,
            limit=_limit,
            _check_return_type=False,
            _return_http_data_only=False,
        )
        custom_headers = self._api_client.custom_headers
        if "X-GDC-TRACE-ID" in custom_headers and "X-GDC-TRACE-ID" in http_headers:
            logger.info(
                "Received execution result from AFM.",
                extra=dict(
                    requestTraceId=custom_headers["X-GDC-TRACE-ID"],
                    responseTraceId=http_headers["X-GDC-TRACE-ID"],
                ),
            )
        return ExecutionResult(execution_result)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"BareExecutionResponse(workspace_id={self.workspace_id}, result_id={self.result_id})"


class Execution:
    """
    An envelope class holding execution related classes:
        - exec_def              ExecutionDefinition
        - bare_exec_response    BareExecutionResponse
    """

    def __init__(
        self,
        api_client: GoodDataApiClient,
        workspace_id: str,
        exec_def: ExecutionDefinition,
        response: models.AfmExecutionResponse,
    ):
        self._exec_def = exec_def
        self._bare_exec_response = BareExecutionResponse(
            api_client=api_client,
            workspace_id=workspace_id,
            execution_response=response,
        )

    @property
    def bare_exec_response(self) -> BareExecutionResponse:
        return self._bare_exec_response

    @property
    def workspace_id(self) -> str:
        return self.bare_exec_response._workspace_id

    @property
    def exec_def(self) -> ExecutionDefinition:
        return self._exec_def

    @property
    def result_id(self) -> str:
        return self.bare_exec_response._exec_response["links"]["executionResult"]

    @property
    def dimensions(self) -> Any:
        return self.bare_exec_response._exec_response["dimensions"]

    def read_result(self, limit: Union[int, list[int]], offset: Union[None, int, list[int]] = None) -> ExecutionResult:
        return self.bare_exec_response.read_result(limit, offset)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"Execution(workspace_id={self.workspace_id}, result_id={self.bare_exec_response.result_id})"


# Originally ExecutionResponse contained also ExecutionDefinition which was not correct, therefore Execution class was
# created to hold clean BareExecutionResponse class without ExecutionDefinition.
# Newly Execution holds BareExecutionResponse and ExecutionDefinition next to it.
# For backwards compatibility ExecutionResponse -> Execution alias is defined.
ExecutionResponse = Execution


class ResultSizeBytesLimitExceeded(Exception):
    def __init__(
        self,
        result_size_bytes_limit: int,
        actual_result_bytes_size: int,
    ):
        self.result_size_bytes_limit = result_size_bytes_limit
        self.actual_result_bytes_size = actual_result_bytes_size


class ResultCacheMetadata:
    def __init__(self, result_cache_metadata: models.ResultCacheMetadata):
        self._result_cache_metadata = result_cache_metadata

    @property
    def afm(self) -> AFM:
        return self._result_cache_metadata.afm

    @property
    def execution_response(self) -> ExecutionResponse:
        return self._result_cache_metadata.execution_response

    @property
    def result_size(self) -> int:
        return self._result_cache_metadata.result_size

    @property
    def result_spec(self) -> ResultSpec:
        return self._result_cache_metadata.result_spec

    def check_bytes_size_limit(self, result_size_bytes_limit: Optional[int] = None) -> None:
        if result_size_bytes_limit is not None and self.result_size > result_size_bytes_limit:
            raise ResultSizeBytesLimitExceeded(
                result_size_bytes_limit=result_size_bytes_limit,
                actual_result_bytes_size=self.result_size,
            )


def compute_model_to_api_model(
    attributes: Optional[list[Attribute]] = None,
    metrics: Optional[list[Metric]] = None,
    filters: Optional[list[Filter]] = None,
) -> models.AFM:
    """
    Transforms categorized execution model entities (attributes, metrics, facts) into an API model
    that can be used for computations of data results or computations of object availability.

    :param attributes: optionally specify list of attributes
    :param metrics: optionally specify list of metrics
    :param filters: optionally specify list of filters
    """
    return models.AFM(
        attributes=[a.as_api_model() for a in attributes] if attributes is not None else [],
        measures=[m.as_api_model() for m in metrics] if metrics is not None else [],
        filters=[f.as_api_model() for f in filters if not f.is_noop()] if filters is not None else [],
    )
