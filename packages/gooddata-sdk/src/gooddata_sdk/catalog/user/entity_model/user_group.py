# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Optional

import attr
from gooddata_api_client.model.json_api_user_group_in import JsonApiUserGroupIn
from gooddata_api_client.model.json_api_user_group_in_document import JsonApiUserGroupInDocument

from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroupDocument(Base):
    data: CatalogUserGroup

    @staticmethod
    def client_class() -> type[JsonApiUserGroupInDocument]:
        return JsonApiUserGroupInDocument

    @classmethod
    def init(cls, user_group_id: str, user_group_parent_ids: Optional[list[str]] = None) -> CatalogUserGroupDocument:
        return cls(data=CatalogUserGroup.init(user_group_id=user_group_id, user_group_parent_ids=user_group_parent_ids))

    def update_user_group(self, user_group_parents_id: Optional[list[str]] = None) -> None:
        relationships = CatalogUserGroupRelationships.create_user_group_relationships(user_group_parents_id)
        self.data.relationships = relationships


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroup(Base):
    id: str
    attributes: Optional[CatalogUserGroupAttributes] = None
    relationships: Optional[CatalogUserGroupRelationships] = None

    @staticmethod
    def client_class() -> type[JsonApiUserGroupIn]:
        return JsonApiUserGroupIn

    @classmethod
    def init(
        cls,
        user_group_id: str,
        user_group_name: Optional[str] = None,
        user_group_parent_ids: Optional[list[str]] = None,
    ) -> CatalogUserGroup:
        attributes = CatalogUserGroupAttributes(name=user_group_name)
        relationships = CatalogUserGroupRelationships.create_user_group_relationships(user_group_parent_ids)
        return cls(id=user_group_id, attributes=attributes, relationships=relationships)

    @property
    def get_parents(self) -> list[str]:
        return self.relationships.get_parents if self.relationships is not None else []

    @property
    def name(self) -> Optional[str]:
        if self.attributes is not None:
            return self.attributes.name
        return None


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroupRelationships(Base):
    parents: Optional[CatalogUserGroupParents] = None

    @classmethod
    def create_user_group_relationships(
        cls, user_group_parent_ids: Optional[list[str]]
    ) -> CatalogUserGroupRelationships:
        parents = None
        if user_group_parent_ids is not None:
            parents = CatalogUserGroupParents(
                data=[CatalogUserGroup(id=user_group_parent_id) for user_group_parent_id in user_group_parent_ids]
            )
        return cls(parents=parents)

    @property
    def get_parents(self) -> list[str]:
        return self.parents.get_parents if self.parents is not None else []


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroupAttributes(Base):
    name: Optional[str] = None


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroupParents(Base):
    data: Optional[list[CatalogUserGroup]] = None

    @property
    def get_parents(self) -> list[str]:
        return [user_group.id for user_group in self.data] if self.data is not None else []
