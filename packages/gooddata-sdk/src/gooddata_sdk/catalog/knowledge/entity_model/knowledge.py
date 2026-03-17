# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

import attrs
from gooddata_api_client.model.create_knowledge_document_request_dto import CreateKnowledgeDocumentRequestDto
from gooddata_api_client.model.create_knowledge_document_response_dto import CreateKnowledgeDocumentResponseDto
from gooddata_api_client.model.delete_knowledge_document_response_dto import DeleteKnowledgeDocumentResponseDto
from gooddata_api_client.model.knowledge_document_metadata_dto import KnowledgeDocumentMetadataDto
from gooddata_api_client.model.knowledge_search_result_dto import KnowledgeSearchResultDto
from gooddata_api_client.model.list_knowledge_documents_response_dto import ListKnowledgeDocumentsResponseDto
from gooddata_api_client.model.patch_knowledge_document_request_dto import PatchKnowledgeDocumentRequestDto
from gooddata_api_client.model.search_knowledge_response_dto import SearchKnowledgeResponseDto
from gooddata_api_client.model.search_statistics_dto import SearchStatisticsDto
from gooddata_api_client.model.upsert_knowledge_document_request_dto import UpsertKnowledgeDocumentRequestDto
from gooddata_api_client.model.upsert_knowledge_document_response_dto import UpsertKnowledgeDocumentResponseDto

from gooddata_sdk.catalog.base import Base


@attrs.define(kw_only=True)
class CatalogKnowledgeDocumentMetadata(Base):
    created_at: str
    created_by: str
    filename: str
    num_chunks: int
    scopes: list[str]
    updated_at: str
    updated_by: str
    is_disabled: bool | None = None
    title: str | None = None
    workspace_id: str | None = None

    @staticmethod
    def client_class() -> type[KnowledgeDocumentMetadataDto]:
        return KnowledgeDocumentMetadataDto


@attrs.define(kw_only=True)
class CatalogKnowledgeSearchResult(Base):
    chunk_index: int
    content: str
    filename: str
    page_numbers: list[int]
    scopes: list[str]
    score: float
    total_chunks: int
    title: str | None = None
    workspace_id: str | None = None

    @staticmethod
    def client_class() -> type[KnowledgeSearchResultDto]:
        return KnowledgeSearchResultDto


@attrs.define(kw_only=True)
class CatalogSearchStatistics(Base):
    average_similarity_score: float
    total_results: int

    @staticmethod
    def client_class() -> type[SearchStatisticsDto]:
        return SearchStatisticsDto


@attrs.define(kw_only=True)
class CatalogSearchKnowledgeResponse(Base):
    results: list[CatalogKnowledgeSearchResult]
    statistics: CatalogSearchStatistics

    @staticmethod
    def client_class() -> type[SearchKnowledgeResponseDto]:
        return SearchKnowledgeResponseDto


@attrs.define(kw_only=True)
class CatalogListKnowledgeDocumentsResponse(Base):
    documents: list[CatalogKnowledgeDocumentMetadata]
    next_page_token: str | None = None
    total_count: int | None = None

    @staticmethod
    def client_class() -> type[ListKnowledgeDocumentsResponseDto]:
        return ListKnowledgeDocumentsResponseDto


@attrs.define(kw_only=True)
class CatalogCreateKnowledgeDocumentResponse(Base):
    filename: str
    message: str
    num_chunks: int
    success: bool

    @staticmethod
    def client_class() -> type[CreateKnowledgeDocumentResponseDto]:
        return CreateKnowledgeDocumentResponseDto


@attrs.define(kw_only=True)
class CatalogUpsertKnowledgeDocumentResponse(Base):
    filename: str
    message: str
    num_chunks: int
    success: bool

    @staticmethod
    def client_class() -> type[UpsertKnowledgeDocumentResponseDto]:
        return UpsertKnowledgeDocumentResponseDto


@attrs.define(kw_only=True)
class CatalogDeleteKnowledgeDocumentResponse(Base):
    message: str
    success: bool

    @staticmethod
    def client_class() -> type[DeleteKnowledgeDocumentResponseDto]:
        return DeleteKnowledgeDocumentResponseDto


@attrs.define(kw_only=True)
class CatalogCreateKnowledgeDocumentRequest(Base):
    content: str
    filename: str
    page_boundaries: list[int] | None = None
    scopes: list[str] | None = None
    title: str | None = None

    @staticmethod
    def client_class() -> type[CreateKnowledgeDocumentRequestDto]:
        return CreateKnowledgeDocumentRequestDto

    def as_api_model(self) -> CreateKnowledgeDocumentRequestDto:
        kwargs: dict[str, Any] = {}
        if self.page_boundaries is not None:
            kwargs["page_boundaries"] = self.page_boundaries
        if self.scopes is not None:
            kwargs["scopes"] = self.scopes
        if self.title is not None:
            kwargs["title"] = self.title
        return CreateKnowledgeDocumentRequestDto(
            content=self.content,
            filename=self.filename,
            _check_type=False,
            **kwargs,
        )


@attrs.define(kw_only=True)
class CatalogUpsertKnowledgeDocumentRequest(Base):
    content: str
    filename: str
    page_boundaries: list[int] | None = None
    scopes: list[str] | None = None
    title: str | None = None

    @staticmethod
    def client_class() -> type[UpsertKnowledgeDocumentRequestDto]:
        return UpsertKnowledgeDocumentRequestDto

    def as_api_model(self) -> UpsertKnowledgeDocumentRequestDto:
        kwargs: dict[str, Any] = {}
        if self.page_boundaries is not None:
            kwargs["page_boundaries"] = self.page_boundaries
        if self.scopes is not None:
            kwargs["scopes"] = self.scopes
        if self.title is not None:
            kwargs["title"] = self.title
        return UpsertKnowledgeDocumentRequestDto(
            content=self.content,
            filename=self.filename,
            _check_type=False,
            **kwargs,
        )


@attrs.define(kw_only=True)
class CatalogPatchKnowledgeDocumentRequest(Base):
    is_disabled: bool | None = None
    scopes: list[str] | None = None
    title: str | None = None

    @staticmethod
    def client_class() -> type[PatchKnowledgeDocumentRequestDto]:
        return PatchKnowledgeDocumentRequestDto

    def as_api_model(self) -> PatchKnowledgeDocumentRequestDto:
        kwargs: dict[str, Any] = {}
        if self.is_disabled is not None:
            kwargs["is_disabled"] = self.is_disabled
        if self.scopes is not None:
            kwargs["scopes"] = self.scopes
        if self.title is not None:
            kwargs["title"] = self.title
        return PatchKnowledgeDocumentRequestDto(_check_type=False, **kwargs)
