# (C) 2024 GoodData Corporation
from __future__ import annotations

from typing import Any

import attrs
from gooddata_api_client.model.knowledge_document_metadata_dto import KnowledgeDocumentMetadataDto
from gooddata_api_client.model.list_knowledge_documents_response_dto import ListKnowledgeDocumentsResponseDto
from gooddata_api_client.model.patch_knowledge_document_request_dto import PatchKnowledgeDocumentRequestDto


@attrs.define(kw_only=True)
class CatalogKnowledgeDocumentMetadata:
    filename: str
    title: str | None = None
    is_disabled: bool | None = None
    scopes: list[str] | None = None

    @classmethod
    def from_api(cls, dto: KnowledgeDocumentMetadataDto) -> CatalogKnowledgeDocumentMetadata:
        return cls(
            filename=dto["filename"],
            title=dto.get("title"),
            is_disabled=dto.get("is_disabled"),
            scopes=list(dto["scopes"]) if "scopes" in dto else None,
        )

    def as_api_model(self) -> PatchKnowledgeDocumentRequestDto:
        kwargs: dict[str, Any] = {}
        if self.title is not None:
            kwargs["title"] = self.title
        if self.is_disabled is not None:
            kwargs["is_disabled"] = self.is_disabled
        if self.scopes is not None:
            kwargs["scopes"] = self.scopes
        return PatchKnowledgeDocumentRequestDto(_check_type=False, **kwargs)


@attrs.define(kw_only=True)
class CatalogListKnowledgeDocumentsResponse:
    documents: list[CatalogKnowledgeDocumentMetadata]
    total_count: int | None = None
    next_page_token: str | None = None

    @classmethod
    def from_api(cls, dto: ListKnowledgeDocumentsResponseDto) -> CatalogListKnowledgeDocumentsResponse:
        documents = [CatalogKnowledgeDocumentMetadata.from_api(d) for d in dto["documents"]]
        return cls(
            documents=documents,
            total_count=dto.get("total_count"),
            next_page_token=dto.get("next_page_token"),
        )


@attrs.define(kw_only=True)
class CatalogPatchKnowledgeDocumentRequest:
    is_disabled: bool | None = None
    title: str | None = None
    scopes: list[str] | None = None

    def as_api_model(self) -> PatchKnowledgeDocumentRequestDto:
        kwargs: dict[str, Any] = {}
        if self.is_disabled is not None:
            kwargs["is_disabled"] = self.is_disabled
        if self.title is not None:
            kwargs["title"] = self.title
        if self.scopes is not None:
            kwargs["scopes"] = self.scopes
        return PatchKnowledgeDocumentRequestDto(_check_type=False, **kwargs)
