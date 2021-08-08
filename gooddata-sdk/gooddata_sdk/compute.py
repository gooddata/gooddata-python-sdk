# (C) 2021 GoodData Corporation
from typing import Union

import gooddata_afm_client.apis as apis
import gooddata_afm_client.models as models
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.compute_model import (
    Attribute,
    Metric,
    Filter,
    compute_model_to_api_model,
)


class ExecutionDefinition:
    def __init__(
        self,
        attributes: list[Attribute],
        metrics: list[Metric],
        filters: list[Filter],
        dimensions,
    ):
        self._attributes = attributes or []
        self._metrics = metrics or []
        self._filters = filters or []
        self._dimensions = [dim for dim in dimensions if dim is not None]

    @property
    def attributes(self):
        return self._attributes

    def has_attributes(self):
        return self.attributes is not None and len(self.attributes) > 0

    @property
    def metrics(self):
        return self._metrics

    def has_metrics(self):
        return self.metrics is not None and len(self.metrics) > 0

    @property
    def filters(self):
        return self._filters

    def has_filters(self):
        return self.filters is not None and len(self.filters) > 0

    @property
    def dimensions(self):
        return self._dimensions

    def is_one_dim(self):
        return len(self.dimensions) == 1

    def is_two_dim(self):
        return len(self.dimensions) == 2

    def as_api_model(self):
        dimensions = []

        for idx, dim in enumerate(self._dimensions):
            dimensions.append(
                models.Dimension(local_identifier=f"dim_{idx}", item_identifiers=dim)
            )

        execution = compute_model_to_api_model(
            attributes=self.attributes, metrics=self.metrics, filters=self.filters
        )

        result_spec = models.ResultSpec(dimensions=dimensions)

        return models.AfmExecution(execution=execution, result_spec=result_spec)


class ExecutionResult:
    def __init__(self, result):
        self._data = result["data"]
        self._headers = result["dimension_headers"]
        self._grand_totals = result["grand_totals"]
        self._paging = result["paging"]

    @property
    def data(self):
        return self._data

    @property
    def headers(self):
        return self._headers

    @property
    def grand_totals(self):
        return self._grand_totals

    @property
    def paging(self):
        return self._paging

    @property
    def paging_total(self):
        return self._paging["total"]

    @property
    def paging_count(self):
        return self._paging["count"]

    @property
    def paging_offset(self):
        return self._paging["offset"]

    def is_complete(self, dim=0):
        return (
            self.paging_offset[dim] + self.paging_count[dim] >= self.paging_total[dim]
        )

    def next_page_start(self, dim=0):
        return self.paging_offset[dim] + self.paging_count[dim]

    def get_all_header_values(self, dim, header_idx):
        return [
            header["attributeHeader"]["labelValue"]
            for header in self.headers[dim]["headerGroups"][header_idx]["headers"]
        ]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"ExecutionResult(paging={self.paging})"


class ExecutionResponse:
    def __init__(
        self,
        result_api: apis.ResultControllerApi,
        workspace_id: str,
        exec_def: ExecutionDefinition,
        response,
    ):
        self._result_api = result_api
        self._workspace_id = workspace_id
        self._exec_def = exec_def

        self._r = response["execution_response"]
        self._response = response

    @property
    def workspace_id(self):
        return self._workspace_id

    @property
    def exec_def(self):
        return self._exec_def

    @property
    def result_id(self) -> str:
        return self._r["links"]["executionResult"]

    def read_result(
        self, limit: Union[int, list[int]], offset: Union[int, list[int]] = None
    ):
        """
        Reads from the execution result.
        :param offset:
        :param limit:
        :return:
        """

        _offset = (
            offset
            if isinstance(offset, list)
            else [offset]
            if offset is not None
            else None
        )
        _limit = limit if isinstance(limit, list) else [limit]

        # if limit is specified but offset is not, server will ignore paging completely (bug)
        # this makes sure that offset gets defaulted to start of result
        _offset = (
            [0 for _ in _limit] if _limit is not None and _offset is None else _offset
        )

        return ExecutionResult(
            self._result_api.retrieve_result(
                workspace_id=self._workspace_id,
                result_id=self.result_id,
                offset=_offset,
                limit=_limit,
                _check_return_type=False,
            )
        )

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"ExecutionResponse(workspace_id={self.workspace_id}, result_id={self.result_id})"


class ComputeService:
    """
    Compute service drives computation of analytics for a GoodData.CN workspaces. The prescription of what to compute
    is encapsulated by the ExecutionDefinition which consists of attributes, metrics, filters and definition of
    dimensions that influence how to organize the data in the result.
    """

    def __init__(self, api_client: GoodDataApiClient):
        self._exec_api = apis.AfmControllerApi(api_client.afm_client)
        self._result_api = apis.ResultControllerApi(api_client.afm_client)

    def for_exec_def(
        self, workspace_id, exec_def: ExecutionDefinition
    ) -> ExecutionResponse:
        """
        Starts computation in GoodData.CN workspace, using the provided execution definition.

        :param workspace_id: workspace identifier
        :param exec_def: execution definition - this prescribes what to calculate, how to place labels and metric values
        into dimensions
        :return:
        """
        response = self._exec_api.compute_report(
            workspace_id, exec_def.as_api_model(), _check_return_type=False
        )

        return ExecutionResponse(
            result_api=self._result_api,
            workspace_id=workspace_id,
            exec_def=exec_def,
            response=response,
        )
