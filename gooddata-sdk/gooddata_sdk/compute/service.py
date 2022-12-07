# (C) 2022 GoodData Corporation
from __future__ import annotations

import logging

from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.compute.model.execution import Execution, ExecutionDefinition, ResultCacheMetadata

logger = logging.getLogger(__name__)


class ComputeService:
    """
    Compute service drives computation of analytics for a GoodData.CN workspaces. The prescription of what to compute
    is encapsulated by the ExecutionDefinition which consists of attributes, metrics, filters and definition of
    dimensions that influence how to organize the data in the result.
    """

    def __init__(self, api_client: GoodDataApiClient):
        self._api_client = api_client
        self._actions_api = self._api_client.actions_api

    def for_exec_def(self, workspace_id: str, exec_def: ExecutionDefinition) -> Execution:
        """
        Starts computation in GoodData.CN workspace, using the provided execution definition.

        :param workspace_id: workspace identifier
        :param exec_def: execution definition - this prescribes what to calculate, how to place labels and metric values
         into dimensions
        """
        response = self._actions_api.compute_report(workspace_id, exec_def.as_api_model(), _check_return_type=False)

        return Execution(
            api_client=self._api_client,
            workspace_id=workspace_id,
            exec_def=exec_def,
            response=response,
        )

    def retrieve_result_cache_metadata(self, workspace_id: str, result_id: str) -> ResultCacheMetadata:
        """
        Gets execution result's metadata from GoodData.CN workspace for given execution result ID.

        :param workspace_id: workspace identifier
        :param result_id: execution result ID
        :return: execution result's metadata
        """
        result_cache_metadata, _, http_headers = self._actions_api.retrieve_execution_metadata(
            workspace_id,
            result_id,
            _check_return_type=False,
            _return_http_data_only=False,
        )
        custom_headers = self._api_client.custom_headers
        if "X-GDC-TRACE-ID" in custom_headers and "X-GDC-TRACE-ID" in http_headers:
            logger.info(
                "Received result cache metadata from AFM.",
                extra=dict(
                    requestTraceId=custom_headers["X-GDC-TRACE-ID"],
                    responseTraceId=http_headers["X-GDC-TRACE-ID"],
                ),
            )
        return ResultCacheMetadata(result_cache_metadata=result_cache_metadata)
