# (C) 2024 GoodData Corporation
from __future__ import annotations

from typing import Any, Optional, Union

import attr
from gooddata_api_client.model.json_api_filter_view_in import JsonApiFilterViewIn
from gooddata_api_client.model.json_api_filter_view_in_attributes import JsonApiFilterViewInAttributes
from gooddata_api_client.model.json_api_filter_view_in_document import JsonApiFilterViewInDocument
from gooddata_api_client.model.json_api_filter_view_in_relationships import JsonApiFilterViewInRelationships

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.identifier import CatalogDeclarativeAnalyticalDashboardIdentifier, CatalogUserIdentifier


@attr.s(auto_attribs=True, kw_only=True)
class CatalogFilterViewDocument(Base):
    data: CatalogFilterView

    @staticmethod
    def client_class() -> type[JsonApiFilterViewInDocument]:
        return JsonApiFilterViewInDocument

    def to_api(self) -> JsonApiFilterViewInDocument:
        return JsonApiFilterViewInDocument(data=self.data.to_api())


def _data_entity(value: Any) -> dict[str, Any]:
    return {"data": value}


@attr.s(auto_attribs=True, kw_only=True)
class CatalogFilterView(Base):
    id: Optional[str] = None
    attributes: CatalogFilterViewAttributes
    relationships: Optional[CatalogFilterViewRelationships] = None

    @staticmethod
    def client_class() -> type[JsonApiFilterViewIn]:
        return JsonApiFilterViewIn

    @classmethod
    def init(
        cls,
        filter_view_id: str,
        content: dict[str, Any],
        title: str,
        are_relations_valid: Optional[bool] = None,
        description: Optional[str] = None,
        is_default: Optional[bool] = None,
        tags: Optional[list[str]] = None,
        user_id: Optional[str] = None,
        analytical_dashboard_id: Optional[str] = None,
    ) -> CatalogFilterView:
        attributes = CatalogFilterViewAttributes(
            content=content,
            title=title,
            are_relations_valid=are_relations_valid,
            description=description,
            is_default=is_default,
            tags=tags,
        )
        relationships = CatalogFilterViewRelationships.create_user_analytical_dashboard_relationship(
            user_id=user_id, analytical_dashboard_id=analytical_dashboard_id
        )
        return cls(id=filter_view_id, attributes=attributes, relationships=relationships)

    def to_api(self) -> JsonApiFilterViewIn:
        attributes = self.attributes.to_api()
        relationships = self.relationships.to_api() if self.relationships is not None else None
        return JsonApiFilterViewIn(id=self.id, attributes=attributes, relationships=relationships)

    @property
    def user_id(self) -> Union[str, None]:
        if self.relationships and self.relationships.user:
            return self.relationships.user["data"].id
        return None

    @property
    def analytical_dashboard_id(self) -> Union[str, None]:
        if self.relationships and self.relationships.analytical_dashboard:
            return self.relationships.analytical_dashboard["data"].id
        return None

    def assign_user(self, user_id: str) -> None:
        if self.relationships is None:
            self.relationships = CatalogFilterViewRelationships.create_user_analytical_dashboard_relationship(
                user_id=user_id
            )
        else:
            self.relationships.user = _data_entity(CatalogUserIdentifier(id=user_id, type="user"))

    def assign_analytical_dashboard(self, analytical_dashboard_id: str) -> None:
        if self.relationships is None:
            self.relationships = CatalogFilterViewRelationships.create_user_analytical_dashboard_relationship(
                analytical_dashboard_id=analytical_dashboard_id
            )
        else:
            self.relationships.analytical_dashboard = _data_entity(
                CatalogDeclarativeAnalyticalDashboardIdentifier(id=analytical_dashboard_id, type="analyticalDashboard")
            )

    def clean_relationships(self) -> None:
        if self.relationships is not None:
            self.relationships.user = None
            self.relationships.analytical_dashboard = None


@attr.s(auto_attribs=True, kw_only=True)
class CatalogFilterViewAttributes(Base):
    content: dict[str, Any]
    title: str
    are_relations_valid: Optional[bool] = None
    description: Optional[str] = None
    is_default: Optional[bool] = None
    tags: Optional[list[str]] = None

    @staticmethod
    def client_class() -> type[JsonApiFilterViewInAttributes]:
        return JsonApiFilterViewInAttributes


@attr.s(auto_attribs=True, kw_only=True)
class CatalogFilterViewRelationships(Base):
    user: Optional[dict[str, CatalogUserIdentifier]] = None
    analytical_dashboard: Optional[dict[str, CatalogDeclarativeAnalyticalDashboardIdentifier]] = None

    @staticmethod
    def client_class() -> type[JsonApiFilterViewInRelationships]:
        return JsonApiFilterViewInRelationships

    @classmethod
    def create_user_analytical_dashboard_relationship(
        cls, user_id: Optional[str] = None, analytical_dashboard_id: Optional[str] = None
    ) -> CatalogFilterViewRelationships | None:
        if user_id is None and analytical_dashboard_id is None:
            return None
        assignee_user = _data_entity(CatalogUserIdentifier(id=user_id, type="user")) if user_id else None
        assignee_analytical_dashboard = (
            _data_entity(
                CatalogDeclarativeAnalyticalDashboardIdentifier(id=analytical_dashboard_id, type="analyticalDashboard")
            )
            if analytical_dashboard_id
            else None
        )
        return cls(user=assignee_user, analytical_dashboard=assignee_analytical_dashboard)
