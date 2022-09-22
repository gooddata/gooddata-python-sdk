# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import List, Optional, Type

import attr

from gooddata_api_client.model.json_api_user_group_in import JsonApiUserGroupIn
from gooddata_api_client.model.json_api_user_group_in_document import JsonApiUserGroupInDocument
from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroupDocument(Base):
    data: CatalogUserGroup

    @staticmethod
    def client_class() -> Type[JsonApiUserGroupInDocument]:
        return JsonApiUserGroupInDocument

    @classmethod
    def init(cls, user_group_id: str, user_group_parent_ids: Optional[List[str]] = None) -> CatalogUserGroupDocument:
        return cls(data=CatalogUserGroup.init(user_group_id=user_group_id, user_group_parent_ids=user_group_parent_ids))

    def update_user_group(self, user_group_parents_id: Optional[List[str]] = None) -> None:
        relationships = CatalogUserGroupRelationships.create_user_group_relationships(user_group_parents_id)
        self.data.relationships = relationships


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroup(Base):
    id: str
    relationships: Optional[CatalogUserGroupRelationships] = None

    @staticmethod
    def client_class() -> Type[JsonApiUserGroupIn]:
        return JsonApiUserGroupIn

    @classmethod
    def init(cls, user_group_id: str, user_group_parent_ids: Optional[List[str]] = None) -> CatalogUserGroup:
        relationships = CatalogUserGroupRelationships.create_user_group_relationships(user_group_parent_ids)
        return cls(id=user_group_id, relationships=relationships)

    @property
    def get_parents(self) -> List[str]:
        return self.relationships.get_parents if self.relationships is not None else []


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroupRelationships(Base):
    parents: Optional[CatalogUserGroupParents] = None

    @classmethod
    def create_user_group_relationships(
        cls, user_group_parent_ids: Optional[List[str]]
    ) -> CatalogUserGroupRelationships:
        parents = None
        if user_group_parent_ids is not None:
            parents = CatalogUserGroupParents(
                data=[CatalogUserGroup(id=user_group_parent_id) for user_group_parent_id in user_group_parent_ids]
            )
        return cls(parents=parents)

    @property
    def get_parents(self) -> List[str]:
        return self.parents.get_parents if self.parents is not None else []


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroupParents(Base):
    data: Optional[List[CatalogUserGroup]] = None

    @property
    def get_parents(self) -> List[str]:
        return [user_group.id for user_group in self.data] if self.data is not None else []
