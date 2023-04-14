# (C) 2023 GoodData Corporation
from __future__ import annotations

from typing import Any, Dict, List, Optional, Type

import attr

from gooddata_api_client.model.json_api_user_data_filter_in import JsonApiUserDataFilterIn
from gooddata_api_client.model.json_api_user_data_filter_in_document import JsonApiUserDataFilterInDocument
from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserDataFilterDocument(Base):
    data: CatalogUserDataFilter

    @staticmethod
    def client_class() -> Type[JsonApiUserDataFilterInDocument]:
        return JsonApiUserDataFilterInDocument


def _proces_entity_list_output(list_entity_data: Optional[Dict[str, List[CatalogEntityIdentifier]]]) -> List[str]:
    if list_entity_data:
        return list(map(lambda x: x.id, list_entity_data["data"]))
    return []


def _data_entity(value: Any) -> Dict[str, Any]:
    return {"data": value}


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserDataFilter(Base):
    id: str
    attributes: CatalogUserDataFilterAttributes
    relationships: Optional[CatalogUserDataFilterRelationships] = None

    @staticmethod
    def client_class() -> Type[JsonApiUserDataFilterIn]:
        return JsonApiUserDataFilterIn

    @classmethod
    def init(
        cls,
        user_data_filter_id: str,
        maql: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        user_id: Optional[str] = None,
        user_group_id: Optional[str] = None,
    ) -> CatalogUserDataFilter:
        attributes = CatalogUserDataFilterAttributes(maql=maql, title=title, description=description)
        relationships = CatalogUserDataFilterRelationships.create_user_user_group_relationship(
            user_id=user_id, user_group_id=user_group_id
        )

        return cls(id=user_data_filter_id, attributes=attributes, relationships=relationships)

    @property
    def user_id(self) -> str | None:
        if self.relationships and self.relationships.user:
            return self.relationships.user["data"].id
        return None

    @property
    def user_group_id(self) -> str | None:
        if self.relationships and self.relationships.user_group:
            return self.relationships.user_group["data"].id
        return None

    @property
    def attribute_ids(self) -> List[str]:
        if self.relationships is None:
            return []
        return _proces_entity_list_output(self.relationships.attributes)

    @property
    def label_ids(self) -> List[str]:
        if self.relationships is None:
            return []
        return _proces_entity_list_output(self.relationships.labels)

    @property
    def fact_ids(self) -> List[str]:
        if self.relationships is None:
            return []
        return _proces_entity_list_output(self.relationships.facts)

    @property
    def dataset_ids(self) -> List[str]:
        if self.relationships is None:
            return []
        return _proces_entity_list_output(self.relationships.datasets)

    @property
    def metric_ids(self) -> List[str]:
        if self.relationships is None:
            return []
        return _proces_entity_list_output(self.relationships.metrics)

    def assign_user(self, user_id: str) -> None:
        if self.relationships is None:
            self.relationships = CatalogUserDataFilterRelationships.create_user_user_group_relationship(user_id=user_id)
        else:
            self.relationships.user = _data_entity(CatalogEntityIdentifier(id=user_id))

    def assign_user_group(self, user_group_id: str) -> None:
        if self.relationships is None:
            self.relationships = CatalogUserDataFilterRelationships.create_user_user_group_relationship(
                user_group_id=user_group_id
            )
        else:
            self.relationships.user_group = _data_entity(CatalogEntityIdentifier(id=user_group_id))

    def clean_assignments(self) -> None:
        if self.relationships is not None:
            self.relationships.user = None
            self.relationships.user_group = None


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserDataFilterAttributes(Base):
    maql: str
    title: Optional[str] = None
    description: Optional[str] = None


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserDataFilterRelationships(Base):
    user: Optional[Dict[str, CatalogEntityIdentifier]] = None
    user_group: Optional[Dict[str, CatalogEntityIdentifier]] = None
    attributes: Optional[Dict[str, List[CatalogEntityIdentifier]]] = None
    labels: Optional[Dict[str, List[CatalogEntityIdentifier]]] = None
    datasets: Optional[Dict[str, List[CatalogEntityIdentifier]]] = None
    facts: Optional[Dict[str, List[CatalogEntityIdentifier]]] = None
    metrics: Optional[Dict[str, List[CatalogEntityIdentifier]]] = None

    @classmethod
    def create_user_user_group_relationship(
        cls, user_id: Optional[str] = None, user_group_id: Optional[str] = None
    ) -> CatalogUserDataFilterRelationships | None:
        if user_id is None and user_group_id is None:
            return None
        assignee_user = _data_entity(CatalogEntityIdentifier(id=user_id)) if user_id else None
        assignee_user_group = _data_entity(CatalogEntityIdentifier(id=user_group_id)) if user_group_id else None
        return cls(user=assignee_user, user_group=assignee_user_group)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogEntityIdentifier(Base):
    id: str
    type: Optional[str] = None
