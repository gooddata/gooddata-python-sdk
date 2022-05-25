# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import List, Optional, Type

import attr

from gooddata_metadata_client.model.json_api_user_group_in import JsonApiUserGroupIn
from gooddata_metadata_client.model.json_api_user_group_in_document import JsonApiUserGroupInDocument
from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroupDocument(Base):
    data: CatalogUserGroup

    @staticmethod
    def client_class() -> Type[JsonApiUserGroupInDocument]:
        return JsonApiUserGroupInDocument

    @classmethod
    def create_user_group(
        cls, user_group_id: str, user_group_parents_id: Optional[List[str]] = None
    ) -> CatalogUserGroupDocument:
        relationships = None
        if user_group_parents_id is not None:
            relationships = CatalogUserGroupRelationships(
                parents=CatalogUserGroupParents(
                    data=[CatalogUserGroup(id=user_group_parent_id) for user_group_parent_id in user_group_parents_id]
                )
            )
        return cls(data=CatalogUserGroup(id=user_group_id, relationships=relationships))


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroup(Base):
    id: str
    relationships: Optional[CatalogUserGroupRelationships] = None

    @staticmethod
    def client_class() -> Type[JsonApiUserGroupIn]:
        return JsonApiUserGroupIn


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroupRelationships(Base):
    parents: Optional[CatalogUserGroupParents] = None


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroupParents(Base):
    data: Optional[List[CatalogUserGroup]] = None
