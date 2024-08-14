# (C) 2022 GoodData Corporation
from __future__ import annotations

import builtins
from typing import Optional

import attr
from gooddata_api_client.model.dependent_entities_graph import DependentEntitiesGraph
from gooddata_api_client.model.dependent_entities_node import DependentEntitiesNode
from gooddata_api_client.model.dependent_entities_request import DependentEntitiesRequest
from gooddata_api_client.model.dependent_entities_response import DependentEntitiesResponse
from gooddata_api_client.model.entity_identifier import EntityIdentifier

from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDependentEntitiesRequest(Base):
    identifiers: list[CatalogEntityIdentifier] = attr.field(factory=list)

    @staticmethod
    def client_class() -> builtins.type[DependentEntitiesRequest]:
        return DependentEntitiesRequest


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDependentEntitiesResponse(Base):
    graph: CatalogDependentEntitiesGraph

    @staticmethod
    def client_class() -> builtins.type[DependentEntitiesResponse]:
        return DependentEntitiesResponse


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDependentEntitiesGraph(Base):
    nodes: list[CatalogDependentEntitiesNode] = attr.field(factory=list)
    edges: list[list[CatalogEntityIdentifier]] = attr.field(factory=list)

    @staticmethod
    def client_class() -> builtins.type[DependentEntitiesGraph]:
        return DependentEntitiesGraph


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDependentEntitiesNode(Base):
    id: str
    type: str
    title: Optional[str] = None

    @staticmethod
    def client_class() -> builtins.type[DependentEntitiesNode]:
        return DependentEntitiesNode


@attr.s(auto_attribs=True, kw_only=True)
class CatalogEntityIdentifier(Base):
    id: str
    type: str

    @staticmethod
    def client_class() -> builtins.type[EntityIdentifier]:
        return EntityIdentifier
