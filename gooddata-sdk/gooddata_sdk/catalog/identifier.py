# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Type, TypeVar

from gooddata_metadata_client.model.assignee_identifier import AssigneeIdentifier
from gooddata_metadata_client.model.grain_identifier import GrainIdentifier
from gooddata_metadata_client.model.reference_identifier import ReferenceIdentifier
from gooddata_metadata_client.model.workspace_identifier import WorkspaceIdentifier
from gooddata_sdk.catalog.entity import CatalogTypeEntity

T = TypeVar("T", bound="CatalogIdentifierBase")


class CatalogIdentifierBase:
    def __init__(self, id: str):
        self.id = id

    @classmethod
    def from_api(cls: Type[T], entity: dict[str, Any]) -> T:
        return cls(entity["id"])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"


class CatalogWorkspaceIdentifier(CatalogIdentifierBase):
    def to_api(self) -> WorkspaceIdentifier:
        return WorkspaceIdentifier(id=self.id)


class CatalogReferenceIdentifier(CatalogIdentifierBase):
    def to_api(self) -> ReferenceIdentifier:
        return ReferenceIdentifier(self.id)


class CatalogGrainIdentifier(CatalogTypeEntity):
    def to_api(self) -> GrainIdentifier:
        return GrainIdentifier(self.id, self.type)


class CatalogAssigneeIdentifier(CatalogTypeEntity):
    def to_api(self) -> AssigneeIdentifier:
        return AssigneeIdentifier(self.id, self.type)
