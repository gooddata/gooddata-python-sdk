# (C) 2024 GoodData Corporation
from __future__ import annotations

from typing import Optional

import attr
from gooddata_api_client.model.json_api_memory_item_in import JsonApiMemoryItemIn
from gooddata_api_client.model.json_api_memory_item_in_attributes import JsonApiMemoryItemInAttributes
from gooddata_api_client.model.json_api_memory_item_in_document import JsonApiMemoryItemInDocument
from gooddata_api_client.model.json_api_memory_item_patch import JsonApiMemoryItemPatch
from gooddata_api_client.model.json_api_memory_item_patch_attributes import JsonApiMemoryItemPatchAttributes
from gooddata_api_client.model.json_api_memory_item_patch_document import JsonApiMemoryItemPatchDocument

from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogMemoryItemDocument(Base):
    data: CatalogMemoryItem

    @staticmethod
    def client_class() -> type[JsonApiMemoryItemInDocument]:
        return JsonApiMemoryItemInDocument

    def to_api(self) -> JsonApiMemoryItemInDocument:
        return JsonApiMemoryItemInDocument(data=self.data.to_api())


@attr.s(auto_attribs=True, kw_only=True)
class CatalogMemoryItemPatchDocument(Base):
    data: CatalogMemoryItemPatch

    @staticmethod
    def client_class() -> type[JsonApiMemoryItemPatchDocument]:
        return JsonApiMemoryItemPatchDocument

    def to_api(self) -> JsonApiMemoryItemPatchDocument:
        return JsonApiMemoryItemPatchDocument(data=self.data.to_api())


@attr.s(auto_attribs=True, kw_only=True)
class CatalogMemoryItem(Base):
    id: str
    attributes: CatalogMemoryItemAttributes

    @staticmethod
    def client_class() -> type[JsonApiMemoryItemIn]:
        return JsonApiMemoryItemIn

    @classmethod
    def init(
        cls,
        memory_item_id: str,
        instruction: str,
        strategy: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[list[str]] = None,
        keywords: Optional[list[str]] = None,
        is_disabled: Optional[bool] = None,
    ) -> CatalogMemoryItem:
        attributes = CatalogMemoryItemAttributes(
            instruction=instruction,
            strategy=strategy,
            title=title,
            description=description,
            tags=tags,
            keywords=keywords,
            is_disabled=is_disabled,
        )
        return cls(id=memory_item_id, attributes=attributes)

    def to_api(self) -> JsonApiMemoryItemIn:
        return JsonApiMemoryItemIn(id=self.id, attributes=self.attributes.to_api())


@attr.s(auto_attribs=True, kw_only=True)
class CatalogMemoryItemAttributes(Base):
    instruction: str
    strategy: str
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    keywords: Optional[list[str]] = None
    is_disabled: Optional[bool] = None

    @staticmethod
    def client_class() -> type[JsonApiMemoryItemInAttributes]:
        return JsonApiMemoryItemInAttributes


@attr.s(auto_attribs=True, kw_only=True)
class CatalogMemoryItemPatch(Base):
    id: str
    attributes: CatalogMemoryItemPatchAttributes

    @staticmethod
    def client_class() -> type[JsonApiMemoryItemPatch]:
        return JsonApiMemoryItemPatch

    def to_api(self) -> JsonApiMemoryItemPatch:
        return JsonApiMemoryItemPatch(id=self.id, attributes=self.attributes.to_api())


@attr.s(auto_attribs=True, kw_only=True)
class CatalogMemoryItemPatchAttributes(Base):
    instruction: Optional[str] = None
    strategy: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    keywords: Optional[list[str]] = None
    is_disabled: Optional[bool] = None

    @staticmethod
    def client_class() -> type[JsonApiMemoryItemPatchAttributes]:
        return JsonApiMemoryItemPatchAttributes
