# (C) 2022 GoodData Corporation
from __future__ import annotations

import logging

from gooddata_api_client.model.afm_cancel_tokens import AfmCancelTokens
from gooddata_api_client.model.chat_history_request import ChatHistoryRequest
from gooddata_api_client.model.chat_history_result import ChatHistoryResult
from gooddata_api_client.model.chat_request import ChatRequest
from gooddata_api_client.model.chat_result import ChatResult

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

        Args:
            workspace_id: workspace identifier
            exec_def: execution definition - this prescribes what to calculate, how to place labels and metric values
         into dimensions
        """
        response, _, headers = self._actions_api.compute_report(
            workspace_id, exec_def.as_api_model(), _check_return_type=False, _return_http_data_only=False
        )

        return Execution(
            api_client=self._api_client,
            workspace_id=workspace_id,
            exec_def=exec_def,
            response=response,
            cancel_token=headers.get("X-Gdc-Cancel-Token")
            if exec_def.is_cancellable or self._api_client.executions_cancellable
            else None,
        )

    def retrieve_result_cache_metadata(self, workspace_id: str, result_id: str) -> ResultCacheMetadata:
        """
        Gets execution result's metadata from GoodData.CN workspace for given execution result ID.

        Args:
            workspace_id: workspace identifier
            result_id: execution result ID
        Returns:
            ResultCacheMetadata: execution result's metadata
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

    def ai_chat(self, workspace_id: str, question: str) -> ChatResult:
        """
        Chat with AI in GoodData workspace.

        Args:
            workspace_id: workspace identifier
            question: question to ask AI
        Returns:
            str: Chat response
        """
        chat_request = ChatRequest(question=question)
        response = self._actions_api.ai_chat(workspace_id, chat_request, _check_return_type=False)
        return response

    def ai_chat_history(self, workspace_id: str, chat_history_interaction_id: int = 0) -> ChatHistoryResult:
        """
        Get chat history with AI in GoodData workspace.

        Args:
            workspace_id: workspace identifier
            chat_history_interaction_id: collect history starting from this interaction id
        Returns:
            str: Chat history response
        """
        chat_history_request = ChatHistoryRequest(chat_history_interaction_id=chat_history_interaction_id)
        response = self._actions_api.ai_chat_history(workspace_id, chat_history_request, _check_return_type=False)
        return response

    def ai_chat_history_reset(self, workspace_id: str) -> None:
        """
        Reset chat history with AI in GoodData workspace.

        Args:
            workspace_id: workspace identifier
        """
        chat_history_request = ChatHistoryRequest(reset=True)
        self._actions_api.ai_chat_history(workspace_id, chat_history_request, _check_return_type=False)

    def cancel_executions(self, executions: list[tuple[str, str]]) -> None:
        """
        Try to cancel given executions using the cancel api endpoint.
        Order of token applications is not guaranteed.

        *Note that this is currently a noop, we will be enabling this functionality soon.*

        Args:
            executions: list of tuples [workspace_id, cancel_token] to send for cancellation
        """
        workspace_to_tokens: dict[str, set[str]] = {}

        for execution in executions:
            workspace_id, cancel_token = execution

            if workspace_id not in workspace_to_tokens:
                workspace_to_tokens[workspace_id] = set()

            workspace_to_tokens[workspace_id].add(cancel_token)

        for workspace_id, token_ids in workspace_to_tokens.items():
            self._actions_api.cancel_executions(workspace_id, AfmCancelTokens(list(token_ids)))
