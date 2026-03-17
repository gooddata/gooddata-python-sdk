# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.catalog.knowledge.entity_model.knowledge import (
    CatalogCreateKnowledgeDocumentRequest,
    CatalogCreateKnowledgeDocumentResponse,
    CatalogDeleteKnowledgeDocumentResponse,
    CatalogKnowledgeDocumentMetadata,
    CatalogListKnowledgeDocumentsResponse,
    CatalogPatchKnowledgeDocumentRequest,
    CatalogSearchKnowledgeResponse,
    CatalogUpsertKnowledgeDocumentRequest,
    CatalogUpsertKnowledgeDocumentResponse,
)
from gooddata_sdk.client import GoodDataApiClient


class CatalogKnowledgeService(CatalogServiceBase):
    def __init__(self, api_client: GoodDataApiClient) -> None:
        super().__init__(api_client)

    def create_document(
        self,
        workspace_id: str,
        request: CatalogCreateKnowledgeDocumentRequest,
    ) -> CatalogCreateKnowledgeDocumentResponse:
        result = self._actions_api.create_document(
            workspace_id,
            request.as_api_model(),
            _check_return_type=False,
        )
        return CatalogCreateKnowledgeDocumentResponse.from_dict(result, camel_case=False)

    def upsert_document(
        self,
        workspace_id: str,
        request: CatalogUpsertKnowledgeDocumentRequest,
    ) -> CatalogUpsertKnowledgeDocumentResponse:
        result = self._actions_api.upsert_document(
            workspace_id,
            request.as_api_model(),
            _check_return_type=False,
        )
        return CatalogUpsertKnowledgeDocumentResponse.from_dict(result, camel_case=False)

    def list_documents(
        self,
        workspace_id: str,
        *,
        page_token: str | None = None,
        size: int | None = None,
        scopes: list[str] | None = None,
        query: str | None = None,
    ) -> CatalogListKnowledgeDocumentsResponse:
        kwargs: dict[str, Any] = {}
        if page_token is not None:
            kwargs["page_token"] = page_token
        if size is not None:
            kwargs["size"] = size
        if scopes is not None:
            kwargs["scopes"] = scopes
        if query is not None:
            kwargs["query"] = query
        result = self._actions_api.list_documents(
            workspace_id,
            _check_return_type=False,
            **kwargs,
        )
        return CatalogListKnowledgeDocumentsResponse.from_dict(result, camel_case=False)

    def get_document(
        self,
        workspace_id: str,
        filename: str,
    ) -> CatalogKnowledgeDocumentMetadata:
        result = self._actions_api.get_document(
            workspace_id,
            filename,
            _check_return_type=False,
        )
        return CatalogKnowledgeDocumentMetadata.from_dict(result, camel_case=False)

    def delete_document(
        self,
        workspace_id: str,
        filename: str,
    ) -> CatalogDeleteKnowledgeDocumentResponse:
        result = self._actions_api.delete_document(
            workspace_id,
            filename,
            _check_return_type=False,
        )
        return CatalogDeleteKnowledgeDocumentResponse.from_dict(result, camel_case=False)

    def patch_document(
        self,
        workspace_id: str,
        filename: str,
        request: CatalogPatchKnowledgeDocumentRequest,
    ) -> CatalogKnowledgeDocumentMetadata:
        result = self._actions_api.patch_document(
            workspace_id,
            filename,
            request.as_api_model(),
            _check_return_type=False,
        )
        return CatalogKnowledgeDocumentMetadata.from_dict(result, camel_case=False)

    def search_knowledge(
        self,
        workspace_id: str,
        query: str,
        *,
        limit: int | None = None,
        min_score: float | None = None,
        scopes: list[str] | None = None,
    ) -> CatalogSearchKnowledgeResponse:
        kwargs: dict[str, Any] = {}
        if limit is not None:
            kwargs["limit"] = limit
        if min_score is not None:
            kwargs["min_score"] = min_score
        if scopes is not None:
            kwargs["scopes"] = scopes
        result = self._actions_api.search_knowledge(
            workspace_id,
            query,
            _check_return_type=False,
            **kwargs,
        )
        return CatalogSearchKnowledgeResponse.from_dict(result, camel_case=False)
