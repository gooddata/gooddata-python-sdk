# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Optional

from gooddata_api_client.model.json_api_workspace_in import JsonApiWorkspaceIn
from gooddata_api_client.model.json_api_workspace_in_attributes import JsonApiWorkspaceInAttributes
from gooddata_api_client.model.json_api_workspace_in_document import JsonApiWorkspaceInDocument
from gooddata_api_client.model.json_api_workspace_in_relationships import JsonApiWorkspaceInRelationships
from gooddata_api_client.model.json_api_workspace_in_relationships_parent import JsonApiWorkspaceInRelationshipsParent
from gooddata_api_client.model.json_api_workspace_to_one_linkage import JsonApiWorkspaceToOneLinkage
from gooddata_sdk.catalog.entity import CatalogNameEntity


class CatalogWorkspace(CatalogNameEntity):
    def __init__(self, workspace_id: str, name: str, parent_id: Optional[str] = None):
        super(CatalogWorkspace, self).__init__(workspace_id, name)
        self.parent_id = parent_id

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogWorkspace:
        ea = entity["attributes"]
        er = entity.get("relationships")
        return cls(
            workspace_id=entity["id"], name=ea["name"], parent_id=er.get("parent").get("data").get("id") if er else None
        )

    def to_api(self) -> JsonApiWorkspaceInDocument:
        kwargs = dict()
        if self.parent_id:
            kwargs["relationships"] = JsonApiWorkspaceInRelationships(
                parent=JsonApiWorkspaceInRelationshipsParent(data=JsonApiWorkspaceToOneLinkage(id=self.parent_id))
            )
        return JsonApiWorkspaceInDocument(
            data=JsonApiWorkspaceIn(
                id=self.id,
                attributes=JsonApiWorkspaceInAttributes(
                    name=self.name,
                ),
                **kwargs,
            )
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogWorkspace):
            return False
        return self.id == other.id and self.name == other.name and self.parent_id == other.parent_id
