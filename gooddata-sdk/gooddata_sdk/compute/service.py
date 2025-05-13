# (C) 2022 GoodData Corporation
from __future__ import annotations

import logging
from typing import Any, Optional

from gooddata_api_client import ApiException
from gooddata_api_client.model.afm_cancel_tokens import AfmCancelTokens
from gooddata_api_client.model.chat_history_request import ChatHistoryRequest
from gooddata_api_client.model.chat_history_result import ChatHistoryResult
from gooddata_api_client.model.chat_request import ChatRequest
from gooddata_api_client.model.chat_result import ChatResult
from gooddata_api_client.model.search_request import SearchRequest
from gooddata_api_client.model.search_result import SearchResult

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
        self._entities_api = self._api_client.entities_api

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

    def get_ai_chat_history(
        self,
        workspace_id: str,
        chat_history_interaction_id: str = "",
        thread_id_suffix: str = "",
    ) -> ChatHistoryResult:
        """
        Get chat history with AI in GoodData workspace.

        Args:
            workspace_id: workspace identifier
            chat_history_interaction_id: collect history starting from this interaction id. If None, complete chat history is returned.
            thread_id_suffix: suffix to identify a specific chat thread. If provided, chat_history_interaction_id is ignored.
        Returns:
            ChatHistoryResult: Chat history response containing interactions and other metadata
        """
        chat_history_request = ChatHistoryRequest(
            chat_history_interaction_id=chat_history_interaction_id, reset=False, thread_id_suffix=thread_id_suffix
        )
        response = self._actions_api.ai_chat_history(workspace_id, chat_history_request, _check_return_type=False)
        return response

    def reset_ai_chat_history(self, workspace_id: str) -> None:
        """
        Reset chat history with AI in GoodData workspace.

        Args:
            workspace_id: workspace identifier
        """
        chat_history_request = ChatHistoryRequest(reset=True)
        self._actions_api.ai_chat_history(workspace_id, chat_history_request, _check_return_type=False)

    def set_ai_chat_history_feedback(
        self,
        workspace_id: str,
        user_feedback: str,
        chat_history_interaction_id: str,
        thread_id_suffix: str = "",
    ) -> None:
        """
        Provide feedback for a specific chat history interaction.

        Args:
            workspace_id: workspace identifier
            user_feedback: feedback to provide ("POSITIVE", "NEGATIVE" or "NONE")
            chat_history_interaction_id: interaction id to provide feedback for
            thread_id_suffix: suffix to identify a specific chat thread
        """
        chat_history_request = ChatHistoryRequest(
            user_feedback=user_feedback,
            chat_history_interaction_id=chat_history_interaction_id,
            thread_id_suffix=thread_id_suffix,
            reset=False,
        )
        self._actions_api.ai_chat_history(workspace_id, chat_history_request, _check_return_type=False)

    def search_ai(
        self,
        workspace_id: str,
        question: str,
        deep_search: Optional[bool] = None,
        limit: Optional[int] = None,
        object_types: Optional[list[str]] = None,
        relevant_score_threshold: Optional[float] = None,
        title_to_descriptor_ratio: Optional[float] = None,
    ) -> SearchResult:
        """
        Search for metadata objects using similarity search.

        Args:
            workspace_id: workspace identifier
            question: keyword/sentence input for search
            deep_search: turn on deep search - if true, content of complex objects will be searched as well
            limit: maximum number of results to return
            object_types: list of object types to search for. Enum items: "attribute", "metric", "fact",
                "label", "date", "dataset", "visualization" and "dashboard"
            relevant_score_threshold: minimum relevance score threshold for results
            title_to_descriptor_ratio: ratio of title score to descriptor score

        Returns:
            SearchResult: Search results

        Note:
            Default values for optional parameters are documented in the AI Search endpoint of the GoodData API.
        """
        search_params: dict[str, Any] = {}
        if deep_search is not None:
            search_params["deep_search"] = deep_search
        if limit is not None:
            search_params["limit"] = limit
        if object_types is not None:
            search_params["object_types"] = object_types
        if relevant_score_threshold is not None:
            search_params["relevant_score_threshold"] = relevant_score_threshold
        if title_to_descriptor_ratio is not None:
            search_params["title_to_descriptor_ratio"] = title_to_descriptor_ratio
        search_request = SearchRequest(question=question, **search_params)
        response = self._actions_api.ai_search(workspace_id, search_request, _check_return_type=False)
        return response

    def cancel_executions(self, executions: dict[str, dict[str, str]]) -> None:
        """
        Try to cancel given executions using the cancel api endpoint.
        Order of token applications is not guaranteed.

        *Note that this is currently a noop, we will be enabling this functionality soon.*

        Args:
            executions: maps workspace_id |-> result_id_to_cancel_token_pairs
        """
        try:
            for workspace_id, cancel_tokens in executions.items():
                self._actions_api.cancel_executions(
                    workspace_id, AfmCancelTokens(result_id_to_cancel_token_pairs=cancel_tokens)
                )
        except ApiException as e:
            print("Exception when calling ActionsApi->cancel_executions: %s\n", e)

    def sync_metadata(self, workspace_id: str, async_req: bool = False) -> None:
        """
        Synchronize metadata for a workspace to update embeddings used by AI features.

        This method triggers a metadata synchronization process that updates the embeddings
        used by AI features like search and chat. The embeddings are created from the
        workspace's metadata model and are essential for accurate AI functionality.

        Note: This is a temporary solution and will be removed in a future release when
        metadata synchronization becomes automatic.

        Args:
            workspace_id: Workspace identifier
            async_req: If True, execute request asynchronously. Default is False.

        Returns:
            None
        """
        self._actions_api.metadata_sync(workspace_id, async_req=async_req, _check_return_type=False)
