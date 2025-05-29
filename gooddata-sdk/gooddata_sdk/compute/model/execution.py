# (C) 2022 GoodData Corporation
from __future__ import annotations

import logging
from typing import Any, Optional, Union

from attr.setters import frozen as frozen_attr
from attrs import define, field
from gooddata_api_client import models
from gooddata_api_client.model.afm import AFM
from gooddata_api_client.model.afm_cancel_tokens import AfmCancelTokens
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


@define
class TotalDefinition:
    local_id: str
    """total's local identifier"""

    aggregation: str
    """aggregation function; case insensitive; one of SUM, MIN, MAX, MED, AVG, NAT"""

    metric_local_id: str
    """local identifier of the measure to calculate total for"""

    total_dims: list[TotalDimension]


@define
class TableDimension:
    """Dataclass used during total and dimension computation."""

    item_ids: Optional[list[str]] = field(on_setattr=frozen_attr)
    """table dimension item local identifiers"""

    sorting: list[dict] = field(default=[])
    """sorting defined for the given table dimension"""


class ExecutionDefinition:
    def __init__(
        self,
        attributes: Optional[list[Attribute]],
        metrics: Optional[list[Metric]],
        filters: Optional[list[Filter]],
        dimensions: list[TableDimension],
        totals: Optional[list[TotalDefinition]] = None,
        is_cancellable: bool = False,
    ) -> None:
        self._attributes = attributes or []
        self._metrics = metrics or []
        self._filters = filters or []
        self._dimensions = [dim for dim in dimensions if dim.item_ids is not None]
        self._totals = totals
        self._is_cancellable = is_cancellable

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
    def dimensions(self) -> list[TableDimension]:
        return self._dimensions

    def is_one_dim(self) -> bool:
        return len(self.dimensions) == 1

    def is_two_dim(self) -> bool:
        return len(self.dimensions) == 2

    @property
    def is_cancellable(self) -> bool:
        return self._is_cancellable

    def _create_value_sort_key(self, sort_key: dict) -> models.SortKey:
        sort_key_value = sort_key["value"]
        return models.SortKey(
            value=models.SortKeyValueValue(
                data_column_locators=sort_key_value["dataColumnLocators"], direction=sort_key_value["direction"]
            )
        )

    def _create_attribute_sort_key(self, sort_key: dict) -> models.SortKey:
        sort_key_attribute = sort_key["attribute"]
        # ASC direction is default for Tiger backend.
        # Don't send it to execution to prevent override of possible default sort label direction.
        # It has the same meaning as TigerSortDirection.DEFAULT which does not exist.
        if sort_key_attribute["direction"] == "ASC":
            return models.SortKey(
                attribute=models.SortKeyAttributeAttribute(
                    attribute_identifier=sort_key_attribute["attributeIdentifier"],
                    sort_type=sort_key_attribute["sortType"],
                )
            )
        return models.SortKey(
            attribute=models.SortKeyAttributeAttribute(
                attribute_identifier=sort_key_attribute["attributeIdentifier"],
                direction=sort_key_attribute["direction"],
                sort_type=sort_key_attribute["sortType"],
            )
        )

    def _create_sort_keys(self, sort_keys: list[dict]) -> list[models.SortKey]:
        api_sort_keys: list[models.SortKey] = []
        for sort_key in sort_keys:
            value = sort_key.get("value")
            attribute = sort_key.get("attribute")
            if value is not None:
                api_sort_keys.append(self._create_value_sort_key(sort_key))
            if attribute is not None:
                api_sort_keys.append(self._create_attribute_sort_key(sort_key))
        return api_sort_keys

    def _create_dimensions(self) -> list[models.Dimension]:
        dimensions = []
        for idx, dim in enumerate(self._dimensions):
            if dim.sorting:
                dimensions.append(
                    models.Dimension(
                        item_identifiers=dim.item_ids,
                        local_identifier=f"dim_{idx}",
                        sorting=self._create_sort_keys(dim.sorting),
                    )
                )
            else:
                dimensions.append(
                    models.Dimension(
                        item_identifiers=dim.item_ids,
                        local_identifier=f"dim_{idx}",
                    )
                )

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


ResultSizeDimensions = tuple[Optional[int], ...]


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
        self._metadata: models.ExecutionResultMetadata = result["metadata"]

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

    @property
    def metadata(self) -> models.ExecutionResultMetadata:
        return self._metadata

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
        cancel_token: Optional[str] = None,
    ):
        self._api_client = api_client
        self._actions_api = self._api_client.actions_api
        self._workspace_id = workspace_id

        self._exec_response: models.ExecutionResponse = execution_response["execution_response"]
        self._afm_exec_response = execution_response
        self._cancel_token = cancel_token

    @property
    def workspace_id(self) -> str:
        return self._workspace_id

    @property
    def result_id(self) -> str:
        return self._exec_response["links"]["executionResult"]

    @property
    def dimensions(self) -> Any:
        return self._exec_response["dimensions"]

    @property
    def cancel_token(self) -> Optional[str]:
        return self._cancel_token

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
            **({"x_gdc_cancel_token": self.cancel_token} if self.cancel_token else {}),
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

    def cancel(self) -> None:
        """
        Cancels the execution backing this execution result.
        """
        if self.cancel_token is not None:
            self._api_client.actions_api.cancel_executions(
                self._workspace_id,
                AfmCancelTokens({self.result_id: self.cancel_token}),
            )

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"BareExecutionResponse(workspace_id={self.workspace_id}, result_id={self.result_id}, cancel_token={self.cancel_token})"


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
        cancel_token: Optional[str] = None,
    ):
        self._exec_def = exec_def
        self._bare_exec_response = BareExecutionResponse(
            api_client=api_client, workspace_id=workspace_id, execution_response=response, cancel_token=cancel_token
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

    @property
    def cancel_token(self) -> Optional[str]:
        return self.bare_exec_response.cancel_token

    def get_labels_and_formats(self) -> tuple[dict[str, str], dict[str, str]]:
        """
        Extracts labels and custom measure formats from the execution response.

        :return: tuple of labels dict ({"label_id":"Label"}) and formats dict ({"measure_id":"#,##0.00"})
        """
        labels = {}
        formats = {}
        for dim in self.dimensions:
            for hdr in dim["headers"]:
                if "attributeHeader" in hdr:
                    labels[hdr["attributeHeader"]["localIdentifier"]] = hdr["attributeHeader"].get(
                        "alias", hdr["attributeHeader"]["labelName"]
                    )
                    labels[hdr["attributeHeader"]["label"]["id"]] = labels[hdr["attributeHeader"]["localIdentifier"]]
                elif "measureGroupHeaders" in hdr:
                    for m_group in hdr["measureGroupHeaders"]:
                        if "name" in m_group:
                            labels[m_group["localIdentifier"]] = m_group.get("alias", m_group["name"])
                        if "format" in m_group:
                            formats[m_group["localIdentifier"]] = m_group["format"]
        return labels, formats

    def read_result(self, limit: Union[int, list[int]], offset: Union[None, int, list[int]] = None) -> ExecutionResult:
        return self.bare_exec_response.read_result(limit, offset)

    def cancel(self) -> None:
        """
        Cancels the execution.
        """
        self.bare_exec_response.cancel()

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return (
            f"Execution(workspace_id={self.workspace_id}, result_id={self.result_id}, cancel_token={self.cancel_token})"
        )


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
