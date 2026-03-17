# (C) 2024 GoodData Corporation
from __future__ import annotations

from gooddata_api_client.exceptions import NotFoundException

from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.catalog.knowledge.declarative_model.knowledge_document import (
    CatalogCreateKnowledgeDocumentRequest,
    CatalogCreateKnowledgeDocumentResponse,
    CatalogDeleteKnowledgeDocumentResponse,
    CatalogKnowledgeDocumentMetadata,
    CatalogListKnowledgeDocumentsResponse,
    CatalogUpsertKnowledgeDocumentRequest,
    CatalogUpsertKnowledgeDocumentResponse,
)
from gooddata_sdk.client import GoodDataApiClient


class CatalogKnowledgeService(CatalogServiceBase):
    """Service for managing knowledge documents in GoodData workspaces."""

    def __init__(self, api_client: GoodDataApiClient) -> None:
        super().__init__(api_client)

    def create_document(
        self,
        workspace_id: str,
        request: CatalogCreateKnowledgeDocumentRequest,
    ) -> CatalogCreateKnowledgeDocumentResponse:
        """Create a new knowledge document (strict create, rejects duplicates).

        Args:
            workspace_id (str): Workspace identifier.
            request (CatalogCreateKnowledgeDocumentRequest): Document creation request.

        Returns:
            CatalogCreateKnowledgeDocumentResponse: Response with document metadata.
        """
        response = self._actions_api.create_document(
            workspace_id,
            request.as_api_model(),
            _check_return_type=False,
        )
        return CatalogCreateKnowledgeDocumentResponse.from_api(response)

    def upsert_document(
        self,
        workspace_id: str,
        request: CatalogUpsertKnowledgeDocumentRequest,
    ) -> CatalogUpsertKnowledgeDocumentResponse:
        """Upsert a knowledge document (create or update).

        Args:
            workspace_id (str): Workspace identifier.
            request (CatalogUpsertKnowledgeDocumentRequest): Document upsert request.

        Returns:
            CatalogUpsertKnowledgeDocumentResponse: Response with document metadata.
        """
        response = self._actions_api.upsert_document(
            workspace_id,
            request.as_api_model(),
            _check_return_type=False,
        )
        return CatalogUpsertKnowledgeDocumentResponse.from_api(response)

    def get_document(
        self,
        workspace_id: str,
        filename: str,
    ) -> CatalogKnowledgeDocumentMetadata:
        """Get metadata for a single knowledge document.

        Args:
            workspace_id (str): Workspace identifier.
            filename (str): Document filename.

        Returns:
            CatalogKnowledgeDocumentMetadata: Document metadata.

        Raises:
            NotFoundException: If the document does not exist.
        """
        response = self._actions_api.get_document(
            workspace_id,
            filename,
            _check_return_type=False,
        )
        return CatalogKnowledgeDocumentMetadata.from_api(response)

    def list_documents(
        self,
        workspace_id: str,
    ) -> CatalogListKnowledgeDocumentsResponse:
        """List all knowledge documents in a workspace.

        Args:
            workspace_id (str): Workspace identifier.

        Returns:
            CatalogListKnowledgeDocumentsResponse: Response containing list of document metadata.
        """
        response = self._actions_api.list_documents(
            workspace_id,
            _check_return_type=False,
        )
        return CatalogListKnowledgeDocumentsResponse.from_api(response)

    def delete_document(
        self,
        workspace_id: str,
        filename: str,
    ) -> CatalogDeleteKnowledgeDocumentResponse:
        """Delete a knowledge document.

        Args:
            workspace_id (str): Workspace identifier.
            filename (str): Document filename.

        Returns:
            CatalogDeleteKnowledgeDocumentResponse: Response confirming deletion.
        """
        response = self._actions_api.delete_document(
            workspace_id,
            filename,
            _check_return_type=False,
        )
        return CatalogDeleteKnowledgeDocumentResponse.from_api(response)
