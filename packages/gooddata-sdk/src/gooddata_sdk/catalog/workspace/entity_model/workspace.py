# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any

from attrs import Factory, define, field
from gooddata_api_client.model.json_api_workspace_automation_out_relationships_workspace import (
    JsonApiWorkspaceAutomationOutRelationshipsWorkspace,
)
from gooddata_api_client.model.json_api_workspace_in import JsonApiWorkspaceIn
from gooddata_api_client.model.json_api_workspace_in_attributes import JsonApiWorkspaceInAttributes
from gooddata_api_client.model.json_api_workspace_in_document import JsonApiWorkspaceInDocument
from gooddata_api_client.model.json_api_workspace_in_relationships import JsonApiWorkspaceInRelationships
from gooddata_api_client.model.json_api_workspace_to_one_linkage import JsonApiWorkspaceToOneLinkage

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.utils import safeget


@define
class CatalogWorkspace(Base):
    workspace_id: str
    id: str = field(init=False, default=Factory(lambda self: self.workspace_id, takes_self=True))
    name: str
    parent_id: str | None = field(default=None)
    description: str | None = field(default=None)
    early_access_values: list[str] | None = field(default=None)

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogWorkspace:
        ea = entity["attributes"]
        er = entity.get("relationships")
        return cls(
            workspace_id=entity["id"],
            name=ea["name"],
            parent_id=safeget(
                er,
                ["parent", "data", "id"],
            ),
            description=ea.get("description"),
            early_access_values=ea.get("early_access_values"),
        )

    def to_api(self) -> JsonApiWorkspaceInDocument:
        kwargs = dict()
        if self.parent_id:
            kwargs["relationships"] = JsonApiWorkspaceInRelationships(
                parent=JsonApiWorkspaceAutomationOutRelationshipsWorkspace(
                    data=JsonApiWorkspaceToOneLinkage(id=self.parent_id, type="workspace")
                )
            )
        attributes_dict = {"name": self.name}
        if self.description:
            attributes_dict["description"] = self.description
        if self.early_access_values is not None:
            attributes_dict["early_access_values"] = self.early_access_values
        return JsonApiWorkspaceInDocument(
            data=JsonApiWorkspaceIn(
                id=self.id,
                attributes=JsonApiWorkspaceInAttributes(**attributes_dict),
                **kwargs,
            )
        )
