# (C) 2023 GoodData Corporation
from __future__ import annotations

from typing import Any

import attr

from gooddata_api_client.model.json_api_organization_setting_in_attributes import JsonApiOrganizationSettingInAttributes
from gooddata_api_client.model.json_api_workspace_setting_in import JsonApiWorkspaceSettingIn
from gooddata_api_client.model.json_api_workspace_setting_in_document import JsonApiWorkspaceSettingInDocument
from gooddata_api_client.model.json_api_workspace_setting_out import JsonApiWorkspaceSettingOut
from gooddata_sdk.catalog.entity import AttrCatalogEntity
from gooddata_sdk.utils import safeget


@attr.s(auto_attribs=True, kw_only=True)
class CatalogWorkspaceSetting(AttrCatalogEntity):
    @staticmethod
    def client_class() -> Any:
        return JsonApiWorkspaceSettingOut

    content: dict = attr.field(
        repr=False,
        default=attr.Factory(lambda self: safeget(self.json_api_entity.attributes, ["content"]), takes_self=True),
    )

    def to_api(self) -> JsonApiWorkspaceSettingInDocument:
        return JsonApiWorkspaceSettingInDocument(
            data=JsonApiWorkspaceSettingIn(
                id=self.id,
                attributes=JsonApiOrganizationSettingInAttributes(
                    content=self.content,
                ),
            )
        )
