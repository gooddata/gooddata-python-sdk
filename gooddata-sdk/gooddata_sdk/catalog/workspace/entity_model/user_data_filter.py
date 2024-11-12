# (C) 2023 GoodData Corporation
from __future__ import annotations

from typing import Any, Optional, Union

import attr
from gooddata_api_client.model.json_api_user_data_filter_in import JsonApiUserDataFilterIn
from gooddata_api_client.model.json_api_user_data_filter_in_attributes import JsonApiUserDataFilterInAttributes
from gooddata_api_client.model.json_api_user_data_filter_in_document import JsonApiUserDataFilterInDocument
from gooddata_api_client.model.json_api_user_data_filter_in_relationships import JsonApiUserDataFilterInRelationships
from gooddata_api_client.model.json_api_user_data_filter_post_optional_id import JsonApiUserDataFilterPostOptionalId
from gooddata_api_client.model.json_api_user_data_filter_post_optional_id_document import (
    JsonApiUserDataFilterPostOptionalIdDocument,
)

from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserDataFilterDocument(Base):
    data: CatalogUserDataFilter

    @staticmethod
    def client_class() -> type[JsonApiUserDataFilterInDocument]:
        return JsonApiUserDataFilterInDocument

    def to_api(
        self, post: bool = False
    ) -> Union[JsonApiUserDataFilterPostOptionalIdDocument, JsonApiUserDataFilterInDocument]:
        data = self.data.to_api(post)
        if post:
            return JsonApiUserDataFilterPostOptionalIdDocument(data=data)
        else:
            return JsonApiUserDataFilterInDocument(data=data)

    def to_post_api(self) -> JsonApiUserDataFilterPostOptionalIdDocument:
        dictionary = self._get_snake_dict()
        return JsonApiUserDataFilterPostOptionalIdDocument.from_dict(dictionary, camel_case=False)


def _proces_entity_list_output(list_entity_data: Optional[dict[str, list[CatalogEntityIdentifier]]]) -> list[str]:
    if list_entity_data:
        return list(map(lambda x: x.id, list_entity_data["data"]))
    return []


def _data_entity(value: Any) -> dict[str, Any]:
    return {"data": value}


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserDataFilter(Base):
    id: Optional[str] = None
    attributes: CatalogUserDataFilterAttributes
    relationships: Optional[CatalogUserDataFilterRelationships] = None

    @staticmethod
    def client_class() -> type[JsonApiUserDataFilterIn]:
        return JsonApiUserDataFilterIn

    @classmethod
    def init(
        cls,
        user_data_filter_id: str,
        maql: str,
        are_relations_valid: Optional[bool] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[list[str]] = None,
        user_id: Optional[str] = None,
        user_group_id: Optional[str] = None,
    ) -> CatalogUserDataFilter:
        attributes = CatalogUserDataFilterAttributes(
            maql=maql, title=title, are_relations_valid=are_relations_valid, tags=tags, description=description
        )
        relationships = CatalogUserDataFilterRelationships.create_user_user_group_relationship(
            user_id=user_id, user_group_id=user_group_id
        )
        return cls(id=user_data_filter_id, attributes=attributes, relationships=relationships)

    def to_api(self, post: bool = False) -> Union[JsonApiUserDataFilterPostOptionalId, JsonApiUserDataFilterIn]:
        if not post and self.id is None:
            raise ValueError(
                f"The combination for {post=} and {self.id=} is not valid. Id can be None only for post=True."
            )
        attributes = self.attributes.to_api()
        relationships = self.relationships.to_api() if self.relationships is not None else None
        if post:
            return JsonApiUserDataFilterPostOptionalId(id=self.id, attributes=attributes, relationships=relationships)
        else:
            return JsonApiUserDataFilterIn(id=self.id, attributes=attributes, relationships=relationships)

    @property
    def user_id(self) -> Union[str, None]:
        if self.relationships and self.relationships.user:
            return self.relationships.user["data"].id
        return None

    @property
    def user_group_id(self) -> Union[str, None]:
        if self.relationships and self.relationships.user_group:
            return self.relationships.user_group["data"].id
        return None

    @property
    def attribute_ids(self) -> list[str]:
        if self.relationships is None:
            return []
        return _proces_entity_list_output(self.relationships.attributes)

    @property
    def label_ids(self) -> list[str]:
        if self.relationships is None:
            return []
        return _proces_entity_list_output(self.relationships.labels)

    @property
    def fact_ids(self) -> list[str]:
        if self.relationships is None:
            return []
        return _proces_entity_list_output(self.relationships.facts)

    @property
    def dataset_ids(self) -> list[str]:
        if self.relationships is None:
            return []
        return _proces_entity_list_output(self.relationships.datasets)

    @property
    def metric_ids(self) -> list[str]:
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
    are_relations_valid: Optional[bool] = None
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None

    @staticmethod
    def client_class() -> type[JsonApiUserDataFilterInAttributes]:
        return JsonApiUserDataFilterInAttributes


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserDataFilterRelationships(Base):
    user: Optional[dict[str, CatalogEntityIdentifier]] = None
    user_group: Optional[dict[str, CatalogEntityIdentifier]] = None
    attributes: Optional[dict[str, list[CatalogEntityIdentifier]]] = None
    labels: Optional[dict[str, list[CatalogEntityIdentifier]]] = None
    datasets: Optional[dict[str, list[CatalogEntityIdentifier]]] = None
    facts: Optional[dict[str, list[CatalogEntityIdentifier]]] = None
    metrics: Optional[dict[str, list[CatalogEntityIdentifier]]] = None

    @staticmethod
    def client_class() -> type[JsonApiUserDataFilterInRelationships]:
        return JsonApiUserDataFilterInRelationships

    @classmethod
    def create_user_user_group_relationship(
        cls, user_id: Optional[str] = None, user_group_id: Optional[str] = None
    ) -> CatalogUserDataFilterRelationships | None:
        if user_id is None and user_group_id is None:
            return None
        assignee_user = _data_entity(CatalogEntityIdentifier(id=user_id, type="user")) if user_id else None
        assignee_user_group = (
            _data_entity(CatalogEntityIdentifier(id=user_group_id, type="userGroup")) if user_group_id else None
        )
        return cls(user=assignee_user, user_group=assignee_user_group)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogEntityIdentifier(Base):
    id: str
    type: Optional[str] = None
