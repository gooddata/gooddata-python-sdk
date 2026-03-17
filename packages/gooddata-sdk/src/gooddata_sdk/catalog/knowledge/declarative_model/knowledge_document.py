# (C) 2024 GoodData Corporation
from __future__ import annotations

from typing import Any

import attrs

from gooddata_api_client.model.create_knowledge_document_request_dto import CreateKnowledgeDocumentRequestDto
from gooddata_api_client.model.create_knowledge_document_response_dto import CreateKnowledgeDocumentResponseDto
from gooddata_api_client.model.delete_knowledge_document_response_dto import DeleteKnowledgeDocumentResponseDto
from gooddata_api_client.model.knowledge_document_metadata_dto import KnowledgeDocumentMetadataDto
from gooddata_api_client.model.list_knowledge_documents_response_dto import ListKnowledgeDocumentsResponseDto
from gooddata_api_client.model.upsert_knowledge_document_request_dto import UpsertKnowledgeDocumentRequestDto
from gooddata_api_client.model.upsert_knowledge_document_response_dto import UpsertKnowledgeDocumentResponseDto


@attrs.define(kw_only=True)
class CatalogKnowledgeDocumentMetadata:
    """Metadata for a knowledge document stored in GoodData."""

    filename: str
    num_chunks: int
    created_at: str
    created_by: str
    updated_at: str
    updated_by: str
    scopes: list[str] = attrs.field(factory=list)
    workspace_id: str | None = None
    title: str | None = None
    is_disabled: bool | None = None

    @classmethod
    def from_api(cls, dto: KnowledgeDocumentMetadataDto) -> CatalogKnowledgeDocumentMetadata:
        kwargs: dict[str, Any] = {}
        if hasattr(dto, "workspace_id") and dto.get("workspace_id") is not None:
            kwargs["workspace_id"] = dto["workspace_id"]
        if hasattr(dto, "title") and dto.get("title") is not None:
            kwargs["title"] = dto["title"]
        if hasattr(dto, "is_disabled") and dto.get("is_disabled") is not None:
            kwargs["is_disabled"] = dto["is_disabled"]
        scopes = dto.get("scopes") or []
        return cls(
            filename=dto["filename"],
            num_chunks=dto["num_chunks"],
            created_at=dto["created_at"],
            created_by=dto["created_by"],
            updated_at=dto["updated_at"],
            updated_by=dto["updated_by"],
            scopes=scopes,
            **kwargs,
        )


@attrs.define(kw_only=True)
class CatalogCreateKnowledgeDocumentRequest:
    """Request to create a new knowledge document (fails if already exists)."""

    filename: str
    content: str
    title: str | None = None
    scopes: list[str] = attrs.field(factory=list)
    page_boundaries: list[int] = attrs.field(factory=list)

    def as_api_model(self) -> CreateKnowledgeDocumentRequestDto:
        kwargs: dict[str, Any] = {}
        if self.title is not None:
            kwargs["title"] = self.title
        if self.scopes:
            kwargs["scopes"] = self.scopes
        if self.page_boundaries:
            kwargs["page_boundaries"] = self.page_boundaries
        return CreateKnowledgeDocumentRequestDto(
            filename=self.filename,
            content=self.content,
            _check_type=False,
            **kwargs,
        )


@attrs.define(kw_only=True)
class CatalogCreateKnowledgeDocumentResponse:
    """Response from creating a knowledge document."""

    filename: str
    message: str
    num_chunks: int
    success: bool

    @classmethod
    def from_api(cls, dto: CreateKnowledgeDocumentResponseDto) -> CatalogCreateKnowledgeDocumentResponse:
        return cls(
            filename=dto["filename"],
            message=dto["message"],
            num_chunks=dto["num_chunks"],
            success=dto["success"],
        )


@attrs.define(kw_only=True)
class CatalogUpsertKnowledgeDocumentRequest:
    """Request to upsert a knowledge document (create or update)."""

    filename: str
    content: str
    title: str | None = None
    scopes: list[str] = attrs.field(factory=list)
    page_boundaries: list[int] = attrs.field(factory=list)

    def as_api_model(self) -> UpsertKnowledgeDocumentRequestDto:
        kwargs: dict[str, Any] = {}
        if self.title is not None:
            kwargs["title"] = self.title
        if self.scopes:
            kwargs["scopes"] = self.scopes
        if self.page_boundaries:
            kwargs["page_boundaries"] = self.page_boundaries
        return UpsertKnowledgeDocumentRequestDto(
            filename=self.filename,
            content=self.content,
            _check_type=False,
            **kwargs,
        )


@attrs.define(kw_only=True)
class CatalogUpsertKnowledgeDocumentResponse:
    """Response from upserting a knowledge document."""

    filename: str
    message: str
    num_chunks: int
    success: bool

    @classmethod
    def from_api(cls, dto: UpsertKnowledgeDocumentResponseDto) -> CatalogUpsertKnowledgeDocumentResponse:
        return cls(
            filename=dto["filename"],
            message=dto["message"],
            num_chunks=dto["num_chunks"],
            success=dto["success"],
        )


@attrs.define(kw_only=True)
class CatalogListKnowledgeDocumentsResponse:
    """Response from listing knowledge documents."""

    documents: list[CatalogKnowledgeDocumentMetadata] = attrs.field(factory=list)
    next_page_token: str | None = None
    total_count: int | None = None

    @classmethod
    def from_api(cls, dto: ListKnowledgeDocumentsResponseDto) -> CatalogListKnowledgeDocumentsResponse:
        raw_docs = dto.get("documents") or []
        documents = [CatalogKnowledgeDocumentMetadata.from_api(d) for d in raw_docs]
        kwargs: dict[str, Any] = {}
        if dto.get("next_page_token") is not None:
            kwargs["next_page_token"] = dto["next_page_token"]
        if dto.get("total_count") is not None:
            kwargs["total_count"] = dto["total_count"]
        return cls(documents=documents, **kwargs)


@attrs.define(kw_only=True)
class CatalogDeleteKnowledgeDocumentResponse:
    """Response from deleting a knowledge document."""

    message: str
    success: bool

    @classmethod
    def from_api(cls, dto: DeleteKnowledgeDocumentResponseDto) -> CatalogDeleteKnowledgeDocumentResponse:
        return cls(
            message=dto["message"],
            success=dto["success"],
        )
