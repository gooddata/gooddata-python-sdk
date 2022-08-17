# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, List, Optional, Type

import attr
import cattr
from cattrs.gen import make_dict_structure_fn, make_dict_unstructure_fn, override

from gooddata_metadata_client.model.dependent_entities_edge import DependentEntitiesEdge
from gooddata_metadata_client.model.dependent_entities_graph import DependentEntitiesGraph
from gooddata_metadata_client.model.dependent_entities_node import DependentEntitiesNode
from gooddata_metadata_client.model.dependent_entities_request import DependentEntitiesRequest
from gooddata_metadata_client.model.dependent_entities_response import DependentEntitiesResponse
from gooddata_metadata_client.model.entity_identifier import EntityIdentifier
from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class GraphBase(Base):
    @classmethod
    def _custom_converter(cls) -> Optional[cattr.GenConverter]:
        if cls._converter is None:
            cls._converter = cattr.GenConverter()
            unstructured_hook = make_dict_unstructure_fn(
                CatalogDependentEntitiesEdge, cls._converter, from_=override(rename="_from")
            )
            structured_hook = make_dict_structure_fn(
                CatalogDependentEntitiesEdge, cls._converter, from_=override(rename="_from")
            )
            cls._converter.register_unstructure_hook(CatalogDependentEntitiesEdge, unstructured_hook)
            cls._converter.register_structure_hook(CatalogDependentEntitiesEdge, structured_hook)
        return cls._converter

    def to_api(self) -> Any:
        """
        to_api method is not supported for dependent entities graph for these reasons:
        * there is no endpoint which would require dependent entities as the input
        * it would take some effort to change to_api to support
        conversion regarding the from attribute (from\\_ -> _from)
        """
        return NotImplemented


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDependentEntitiesRequest(Base):
    identifiers: List[CatalogEntityIdentifier] = attr.field(factory=list)

    @staticmethod
    def client_class() -> Type[DependentEntitiesRequest]:
        return DependentEntitiesRequest


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDependentEntitiesResponse(GraphBase):
    graph: CatalogDependentEntitiesGraph

    @staticmethod
    def client_class() -> Type[DependentEntitiesResponse]:
        return DependentEntitiesResponse


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDependentEntitiesGraph(GraphBase):
    nodes: List[CatalogDependentEntitiesNode] = attr.field(factory=list)
    edges: List[CatalogDependentEntitiesEdge] = attr.field(factory=list)

    @staticmethod
    def client_class() -> Type[DependentEntitiesGraph]:
        return DependentEntitiesGraph


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDependentEntitiesNode(Base):
    id: str
    type: str
    title: Optional[str] = None

    @staticmethod
    def client_class() -> Type[DependentEntitiesNode]:
        return DependentEntitiesNode


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDependentEntitiesEdge(GraphBase):
    from_: CatalogEntityIdentifier
    """
    Beware of the attribute from\\_ which may result in several issues.
    Important points:
    * from is a Python keyword and cannot be used as a variable name therefore we use from\\_ in dataclass
    * client class uses _from naming and as a result to_dict contains _from key
    * variable _from results in error
    * using from_dict we expect from\\_
    """
    to: CatalogEntityIdentifier

    @staticmethod
    def client_class() -> Type[DependentEntitiesEdge]:
        return DependentEntitiesEdge


@attr.s(auto_attribs=True, kw_only=True)
class CatalogEntityIdentifier(Base):
    id: str
    type: str

    @staticmethod
    def client_class() -> Type[EntityIdentifier]:
        return EntityIdentifier
