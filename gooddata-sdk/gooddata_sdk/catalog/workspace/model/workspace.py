# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any

from gooddata_metadata_client.model.json_api_workspace_in import JsonApiWorkspaceIn
from gooddata_metadata_client.model.json_api_workspace_in_attributes import JsonApiWorkspaceInAttributes
from gooddata_metadata_client.model.json_api_workspace_in_document import JsonApiWorkspaceInDocument
from gooddata_sdk.catalog.entity import CatalogNameEntity


class CatalogWorkspace(CatalogNameEntity):
    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogWorkspace:
        ea = entity["attributes"]
        return cls(
            id=entity["id"],
            name=ea["name"],
        )

    def to_api(self) -> JsonApiWorkspaceInDocument:
        return JsonApiWorkspaceInDocument(
            data=JsonApiWorkspaceIn(
                id=self.id,
                attributes=JsonApiWorkspaceInAttributes(
                    name=self.name,
                ),
            )
        )
