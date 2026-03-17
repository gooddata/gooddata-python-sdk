# (C) 2024 GoodData Corporation
from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from gooddata_sdk.catalog.knowledge.declarative_model.knowledge_document import (
    CatalogCreateKnowledgeDocumentRequest,
    CatalogCreateKnowledgeDocumentResponse,
    CatalogDeleteKnowledgeDocumentResponse,
    CatalogKnowledgeDocumentMetadata,
    CatalogListKnowledgeDocumentsResponse,
    CatalogUpsertKnowledgeDocumentRequest,
    CatalogUpsertKnowledgeDocumentResponse,
)
from gooddata_sdk.catalog.knowledge.service import CatalogKnowledgeService


def _make_metadata_dto(
    filename: str = "doc.txt",
    num_chunks: int = 3,
    created_at: str = "2024-01-01T00:00:00Z",
    created_by: str = "user1",
    updated_at: str = "2024-01-02T00:00:00Z",
    updated_by: str = "user2",
    scopes: list[str] | None = None,
    workspace_id: str | None = None,
    title: str | None = None,
) -> MagicMock:
    dto = MagicMock()
    dto.__getitem__ = lambda self, key: {
        "filename": filename,
        "num_chunks": num_chunks,
        "created_at": created_at,
        "created_by": created_by,
        "updated_at": updated_at,
        "updated_by": updated_by,
        "scopes": scopes or [],
        "workspace_id": workspace_id,
        "title": title,
        "is_disabled": None,
    }[key]
    dto.get = lambda key, default=None: {
        "filename": filename,
        "num_chunks": num_chunks,
        "created_at": created_at,
        "created_by": created_by,
        "updated_at": updated_at,
        "updated_by": updated_by,
        "scopes": scopes or [],
        "workspace_id": workspace_id,
        "title": title,
        "is_disabled": None,
    }.get(key, default)
    return dto


def _make_write_response_dto(
    filename: str = "doc.txt",
    message: str = "OK",
    num_chunks: int = 3,
    success: bool = True,
) -> MagicMock:
    dto = MagicMock()
    dto.__getitem__ = lambda self, key: {
        "filename": filename,
        "message": message,
        "num_chunks": num_chunks,
        "success": success,
    }[key]
    return dto


def _make_delete_response_dto(message: str = "Deleted", success: bool = True) -> MagicMock:
    dto = MagicMock()
    dto.__getitem__ = lambda self, key: {"message": message, "success": success}[key]
    return dto


def _make_list_response_dto(documents: list[MagicMock] | None = None) -> MagicMock:
    dto = MagicMock()
    dto.get = lambda key, default=None: {
        "documents": documents or [],
        "next_page_token": None,
        "total_count": None,
    }.get(key, default)
    return dto


def _make_service() -> tuple[CatalogKnowledgeService, MagicMock]:
    api_client = MagicMock()
    service = CatalogKnowledgeService.__new__(CatalogKnowledgeService)
    service._actions_api = MagicMock()
    return service, service._actions_api


class TestCatalogKnowledgeDocumentMetadata:
    def test_from_api_minimal(self) -> None:
        dto = _make_metadata_dto()
        metadata = CatalogKnowledgeDocumentMetadata.from_api(dto)
        assert metadata.filename == "doc.txt"
        assert metadata.num_chunks == 3
        assert metadata.created_at == "2024-01-01T00:00:00Z"
        assert metadata.created_by == "user1"
        assert metadata.updated_at == "2024-01-02T00:00:00Z"
        assert metadata.updated_by == "user2"
        assert metadata.scopes == []
        assert metadata.workspace_id is None
        assert metadata.title is None

    def test_from_api_with_optional_fields(self) -> None:
        dto = _make_metadata_dto(
            scopes=["scope1", "scope2"],
            workspace_id="ws1",
            title="My Document",
        )
        metadata = CatalogKnowledgeDocumentMetadata.from_api(dto)
        assert metadata.scopes == ["scope1", "scope2"]
        assert metadata.workspace_id == "ws1"
        assert metadata.title == "My Document"


class TestCatalogCreateKnowledgeDocumentRequest:
    def test_as_api_model_required_only(self) -> None:
        request = CatalogCreateKnowledgeDocumentRequest(filename="doc.txt", content="Hello world")
        model = request.as_api_model()
        assert model["filename"] == "doc.txt"
        assert model["content"] == "Hello world"

    def test_as_api_model_with_optional_fields(self) -> None:
        request = CatalogCreateKnowledgeDocumentRequest(
            filename="doc.txt",
            content="Hello world",
            title="My Doc",
            scopes=["scope1"],
            page_boundaries=[100, 200],
        )
        model = request.as_api_model()
        assert model["filename"] == "doc.txt"
        assert model["title"] == "My Doc"
        assert model["scopes"] == ["scope1"]
        assert model["page_boundaries"] == [100, 200]


class TestCatalogUpsertKnowledgeDocumentRequest:
    def test_as_api_model_required_only(self) -> None:
        request = CatalogUpsertKnowledgeDocumentRequest(filename="doc.txt", content="Hello world")
        model = request.as_api_model()
        assert model["filename"] == "doc.txt"
        assert model["content"] == "Hello world"


class TestCatalogKnowledgeService:
    def test_create_document_calls_api(self) -> None:
        service, actions_api = _make_service()
        actions_api.create_document.return_value = _make_write_response_dto()
        request = CatalogCreateKnowledgeDocumentRequest(filename="doc.txt", content="content")
        response = service.create_document("ws1", request)
        actions_api.create_document.assert_called_once()
        assert isinstance(response, CatalogCreateKnowledgeDocumentResponse)
        assert response.filename == "doc.txt"
        assert response.success is True

    def test_upsert_document_calls_api(self) -> None:
        service, actions_api = _make_service()
        actions_api.upsert_document.return_value = _make_write_response_dto()
        request = CatalogUpsertKnowledgeDocumentRequest(filename="doc.txt", content="content")
        response = service.upsert_document("ws1", request)
        actions_api.upsert_document.assert_called_once()
        assert isinstance(response, CatalogUpsertKnowledgeDocumentResponse)
        assert response.success is True

    def test_get_document_calls_api(self) -> None:
        service, actions_api = _make_service()
        actions_api.get_document.return_value = _make_metadata_dto(title="My Doc")
        result = service.get_document("ws1", "doc.txt")
        actions_api.get_document.assert_called_once_with("ws1", "doc.txt", _check_return_type=False)
        assert isinstance(result, CatalogKnowledgeDocumentMetadata)
        assert result.filename == "doc.txt"

    def test_list_documents_calls_api(self) -> None:
        service, actions_api = _make_service()
        doc_dto = _make_metadata_dto(filename="file1.txt")
        actions_api.list_documents.return_value = _make_list_response_dto(documents=[doc_dto])
        result = service.list_documents("ws1")
        actions_api.list_documents.assert_called_once_with("ws1", _check_return_type=False)
        assert isinstance(result, CatalogListKnowledgeDocumentsResponse)
        assert len(result.documents) == 1
        assert result.documents[0].filename == "file1.txt"

    def test_list_documents_empty(self) -> None:
        service, actions_api = _make_service()
        actions_api.list_documents.return_value = _make_list_response_dto(documents=[])
        result = service.list_documents("ws1")
        assert result.documents == []

    def test_delete_document_calls_api(self) -> None:
        service, actions_api = _make_service()
        actions_api.delete_document.return_value = _make_delete_response_dto()
        result = service.delete_document("ws1", "doc.txt")
        actions_api.delete_document.assert_called_once_with("ws1", "doc.txt", _check_return_type=False)
        assert isinstance(result, CatalogDeleteKnowledgeDocumentResponse)
        assert result.success is True
