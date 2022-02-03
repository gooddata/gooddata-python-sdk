# (C) 2022 GoodData Corporation
from __future__ import annotations

import gooddata_afm_client.apis as apis
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.compute.model.execution import ExecutionDefinition, ExecutionResponse


class ComputeService:
    """
    Compute service drives computation of analytics for a GoodData.CN workspaces. The prescription of what to compute
    is encapsulated by the ExecutionDefinition which consists of attributes, metrics, filters and definition of
    dimensions that influence how to organize the data in the result.
    """

    def __init__(self, api_client: GoodDataApiClient):
        self._actions_api = apis.ActionsApi(api_client.afm_client)

    def for_exec_def(self, workspace_id: str, exec_def: ExecutionDefinition) -> ExecutionResponse:
        """
        Starts computation in GoodData.CN workspace, using the provided execution definition.

        :param workspace_id: workspace identifier
        :param exec_def: execution definition - this prescribes what to calculate, how to place labels and metric values
            into dimensions

        :return:
        """
        response = self._actions_api.compute_report(workspace_id, exec_def.as_api_model(), _check_return_type=False)

        return ExecutionResponse(
            actions_api=self._actions_api,
            workspace_id=workspace_id,
            exec_def=exec_def,
            response=response,
        )
