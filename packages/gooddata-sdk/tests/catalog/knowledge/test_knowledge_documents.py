# (C) 2024 GoodData Corporation
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from gooddata_sdk.catalog.knowledge.model.knowledge_document import (
    CatalogKnowledgeDocumentMetadata,
    CatalogListKnowledgeDocumentsResponse,
    CatalogPatchKnowledgeDocumentRequest,
)


class TestCatalogKnowledgeDocumentMetadata:
    def test_from_api_required_fields(self):
        dto = {
            "filename": "test.pdf",
            "scopes": ["scope1"],
        }
        result = CatalogKnowledgeDocumentMetadata.from_api(dto)
        assert result.filename == "test.pdf"
        assert result.scopes == ["scope1"]
        assert result.title is None
        assert result.is_disabled is None

    def test_from_api_with_optional_fields(self):
        dto = {
            "filename": "test.pdf",
            "title": "Test Document",
            "is_disabled": True,
            "scopes": ["scope1", "scope2"],
        }
        result = CatalogKnowledgeDocumentMetadata.from_api(dto)
        assert result.filename == "test.pdf"
        assert result.title == "Test Document"
        assert result.is_disabled is True
        assert result.scopes == ["scope1", "scope2"]

    def test_from_api_is_disabled_false(self):
        dto = {
            "filename": "test.pdf",
            "is_disabled": False,
            "scopes": [],
        }
        result = CatalogKnowledgeDocumentMetadata.from_api(dto)
        assert result.is_disabled is False


class TestCatalogPatchKnowledgeDocumentRequest:
    def test_as_api_model_empty(self):
        req = CatalogPatchKnowledgeDocumentRequest()
        model = req.as_api_model()
        # only _check_type was passed, no other kwargs
        assert not hasattr(model, "is_disabled") or model.get("is_disabled") is None
        assert not hasattr(model, "title") or model.get("title") is None

    def test_as_api_model_with_is_disabled(self):
        req = CatalogPatchKnowledgeDocumentRequest(is_disabled=True)
        model = req.as_api_model()
        assert model["is_disabled"] is True

    def test_as_api_model_with_title(self):
        req = CatalogPatchKnowledgeDocumentRequest(title="New Title")
        model = req.as_api_model()
        assert model["title"] == "New Title"

    def test_as_api_model_with_scopes(self):
        req = CatalogPatchKnowledgeDocumentRequest(scopes=["workspace1"])
        model = req.as_api_model()
        assert model["scopes"] == ["workspace1"]

    def test_as_api_model_all_fields(self):
        req = CatalogPatchKnowledgeDocumentRequest(is_disabled=False, title="Doc", scopes=["s1"])
        model = req.as_api_model()
        assert model["is_disabled"] is False
        assert model["title"] == "Doc"
        assert model["scopes"] == ["s1"]


class TestCatalogListKnowledgeDocumentsResponse:
    def test_from_api_minimal(self):
        doc_dto = {"filename": "doc.pdf", "scopes": []}
        dto = {"documents": [doc_dto]}
        result = CatalogListKnowledgeDocumentsResponse.from_api(dto)
        assert len(result.documents) == 1
        assert result.documents[0].filename == "doc.pdf"
        assert result.total_count is None
        assert result.next_page_token is None

    def test_from_api_with_pagination(self):
        doc_dto = {"filename": "doc.pdf", "scopes": []}
        dto = {"documents": [doc_dto], "total_count": 100, "next_page_token": "cursor123"}
        result = CatalogListKnowledgeDocumentsResponse.from_api(dto)
        assert result.total_count == 100
        assert result.next_page_token == "cursor123"

    def test_from_api_empty_documents(self):
        dto = {"documents": []}
        result = CatalogListKnowledgeDocumentsResponse.from_api(dto)
        assert result.documents == []


class TestComputeServiceKnowledgeDocuments:
    def _make_service(self):
        from gooddata_sdk.compute.service import ComputeService

        api_client = MagicMock()
        service = ComputeService.__new__(ComputeService)
        service._api_client = api_client
        service._actions_api = api_client.actions_api
        return service

    def test_list_knowledge_documents_no_optional_params(self):
        service = self._make_service()
        mock_response = {"documents": [], "total_count": 0}
        service._actions_api.list_documents.return_value = mock_response

        result = service.list_knowledge_documents("workspace1")

        service._actions_api.list_documents.assert_called_once_with("workspace1", _check_return_type=False)
        assert isinstance(result, CatalogListKnowledgeDocumentsResponse)

    def test_list_knowledge_documents_with_pagination_params(self):
        service = self._make_service()
        mock_response = {"documents": [], "total_count": 50, "next_page_token": "tok"}
        service._actions_api.list_documents.return_value = mock_response

        result = service.list_knowledge_documents("workspace1", size=10, page_token="prev_tok", meta_include="page")

        service._actions_api.list_documents.assert_called_once_with(
            "workspace1",
            _check_return_type=False,
            size=10,
            page_token="prev_tok",
            meta_include="page",
        )
        assert result.total_count == 50
        assert result.next_page_token == "tok"

    def test_patch_knowledge_document(self):
        service = self._make_service()
        service._actions_api.patch_document.return_value = None

        patch_req = CatalogPatchKnowledgeDocumentRequest(is_disabled=True)
        service.patch_knowledge_document("workspace1", "doc.pdf", patch_req)

        service._actions_api.patch_document.assert_called_once()
        call_args = service._actions_api.patch_document.call_args
        assert call_args[0][0] == "workspace1"
        assert call_args[0][1] == "doc.pdf"
        assert call_args[1]["_check_return_type"] is False
