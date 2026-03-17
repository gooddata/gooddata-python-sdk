# (C) 2022 GoodData Corporation
from __future__ import annotations

import builtins

from attrs import define, field
from gooddata_api_client.model.dependent_entities_graph import DependentEntitiesGraph
from gooddata_api_client.model.dependent_entities_node import DependentEntitiesNode
from gooddata_api_client.model.dependent_entities_request import DependentEntitiesRequest
from gooddata_api_client.model.dependent_entities_response import DependentEntitiesResponse
from gooddata_api_client.model.entity_identifier import EntityIdentifier

from gooddata_sdk.catalog.base import Base


@define(kw_only=True)
class CatalogDependentEntitiesRequest(Base):
    identifiers: list[CatalogEntityIdentifier] = field(factory=list)
    relation: str | None = None

    @staticmethod
    def client_class() -> builtins.type[DependentEntitiesRequest]:
        return DependentEntitiesRequest


@define(kw_only=True)
class CatalogDependentEntitiesResponse(Base):
    graph: CatalogDependentEntitiesGraph

    @staticmethod
    def client_class() -> builtins.type[DependentEntitiesResponse]:
        return DependentEntitiesResponse


@define(kw_only=True)
class CatalogDependentEntitiesGraph(Base):
    nodes: list[CatalogDependentEntitiesNode] = field(factory=list)
    edges: list[list[CatalogEntityIdentifier]] = field(factory=list)

    @staticmethod
    def client_class() -> builtins.type[DependentEntitiesGraph]:
        return DependentEntitiesGraph


@define(kw_only=True)
class CatalogDependentEntitiesNode(Base):
    id: str
    type: str
    title: str | None = None

    @staticmethod
    def client_class() -> builtins.type[DependentEntitiesNode]:
        return DependentEntitiesNode


@define(kw_only=True)
class CatalogEntityIdentifier(Base):
    id: str
    type: str

    @staticmethod
    def client_class() -> builtins.type[EntityIdentifier]:
        return EntityIdentifier
