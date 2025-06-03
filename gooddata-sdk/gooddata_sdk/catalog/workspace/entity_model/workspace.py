# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Optional

import attr
from gooddata_api_client.model.json_api_workspace_in import JsonApiWorkspaceIn
from gooddata_api_client.model.json_api_workspace_in_attributes import JsonApiWorkspaceInAttributes
from gooddata_api_client.model.json_api_workspace_in_document import JsonApiWorkspaceInDocument
from gooddata_api_client.model.json_api_workspace_in_relationships import JsonApiWorkspaceInRelationships
from gooddata_api_client.model.json_api_workspace_in_relationships_parent import JsonApiWorkspaceInRelationshipsParent
from gooddata_api_client.model.json_api_workspace_to_one_linkage import JsonApiWorkspaceToOneLinkage

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.utils import safeget


@attr.s(auto_attribs=True)
class CatalogWorkspace(Base):
    workspace_id: str
    id: str = attr.field(init=False, default=attr.Factory(lambda self: self.workspace_id, takes_self=True))
    name: str
    parent_id: Optional[str] = attr.field(default=None)
    description: Optional[str] = attr.field(default=None)

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
        )

    def to_api(self) -> JsonApiWorkspaceInDocument:
        kwargs = dict()
        if self.parent_id:
            kwargs["relationships"] = JsonApiWorkspaceInRelationships(
                parent=JsonApiWorkspaceInRelationshipsParent(
                    data=JsonApiWorkspaceToOneLinkage(id=self.parent_id, type="workspace")
                )
            )
        attributes_dict = {"name": self.name}
        if self.description:
            attributes_dict["description"] = self.description
        return JsonApiWorkspaceInDocument(
            data=JsonApiWorkspaceIn(
                id=self.id,
                attributes=JsonApiWorkspaceInAttributes(**attributes_dict),
                **kwargs,
            )
        )
