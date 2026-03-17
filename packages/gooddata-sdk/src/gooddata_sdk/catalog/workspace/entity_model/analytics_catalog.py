# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

from attr import define
from gooddata_api_client.model.generate_title_request import GenerateTitleRequest
from gooddata_api_client.model.generate_title_response import GenerateTitleResponse

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.utils import safeget


@define(kw_only=True)
class CatalogGenerateTitleRequest(Base):
    """Request for generating a title for an analytics object."""

    object_id: str
    object_type: str

    @staticmethod
    def client_class() -> type[GenerateTitleRequest]:
        return GenerateTitleRequest

    def to_api(self) -> GenerateTitleRequest:
        return GenerateTitleRequest(
            object_id=self.object_id,
            object_type=self.object_type,
        )


@define(kw_only=True)
class CatalogGenerateTitleResponse(Base):
    """Response from the generate title endpoint."""

    title: str
    note: str | None = None

    @staticmethod
    def client_class() -> type[GenerateTitleResponse]:
        return GenerateTitleResponse

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CatalogGenerateTitleResponse:
        return cls(
            title=safeget(data, ["title"]) or "",
            note=safeget(data, ["note"]),
        )
