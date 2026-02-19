# (C) 2022 GoodData Corporation
from __future__ import annotations

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
    def init(cls, user_group_id: str, user_group_parent_ids: list[str] | None = None) -> CatalogUserGroupDocument:
        return cls(data=CatalogUserGroup.init(user_group_id=user_group_id, user_group_parent_ids=user_group_parent_ids))

    def update_user_group(self, user_group_parents_id: list[str] | None = None) -> None:
        relationships = CatalogUserGroupRelationships.create_user_group_relationships(user_group_parents_id)
        self.data.relationships = relationships


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroup(Base):
    id: str
    attributes: CatalogUserGroupAttributes | None = None
    relationships: CatalogUserGroupRelationships | None = None

    @staticmethod
    def client_class() -> type[JsonApiUserGroupIn]:
        return JsonApiUserGroupIn

    @classmethod
    def init(
        cls,
        user_group_id: str,
        user_group_name: str | None = None,
        user_group_parent_ids: list[str] | None = None,
    ) -> CatalogUserGroup:
        attributes = CatalogUserGroupAttributes(name=user_group_name)
        relationships = CatalogUserGroupRelationships.create_user_group_relationships(user_group_parent_ids)
        return cls(id=user_group_id, attributes=attributes, relationships=relationships)

    @property
    def get_parents(self) -> list[str]:
        return self.relationships.get_parents if self.relationships is not None else []

    @property
    def name(self) -> str | None:
        if self.attributes is not None:
            return self.attributes.name
        return None


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroupRelationships(Base):
    parents: CatalogUserGroupParents | None = None

    @classmethod
    def create_user_group_relationships(
        cls, user_group_parent_ids: list[str] | None
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
    name: str | None = None


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroupParents(Base):
    data: list[CatalogUserGroup] | None = None

    @property
    def get_parents(self) -> list[str]:
        return [user_group.id for user_group in self.data] if self.data is not None else []
