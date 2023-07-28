# (C) 2023 GoodData Corporation
from __future__ import annotations

from typing import Type, Union

import attr

from gooddata_api_client.model.json_api_organization_setting_in_attributes import JsonApiOrganizationSettingInAttributes
from gooddata_api_client.model.json_api_workspace_setting_in import JsonApiWorkspaceSettingIn
from gooddata_api_client.model.json_api_workspace_setting_in_document import JsonApiWorkspaceSettingInDocument
from gooddata_api_client.model.json_api_workspace_setting_out import JsonApiWorkspaceSettingOut
from gooddata_api_client.model.json_api_workspace_setting_post_optional_id import JsonApiWorkspaceSettingPostOptionalId
from gooddata_api_client.model.json_api_workspace_setting_post_optional_id_document import (
    JsonApiWorkspaceSettingPostOptionalIdDocument,
)
from gooddata_sdk.catalog.entity import AttrCatalogEntity
from gooddata_sdk.utils import safeget


@attr.s(auto_attribs=True, kw_only=True)
class CatalogWorkspaceSetting(AttrCatalogEntity):
    id: str = attr.field(default=None)

    @staticmethod
    def client_class() -> Type[JsonApiWorkspaceSettingOut]:
        return JsonApiWorkspaceSettingOut

    content: dict = attr.field(
        repr=False,
        default=attr.Factory(lambda self: safeget(self.json_api_entity.attributes, ["content"]), takes_self=True),
    )

    def _attributes(self) -> JsonApiOrganizationSettingInAttributes:
        return JsonApiOrganizationSettingInAttributes(
            content=self.content,
        )

    def to_api(
        self, post: bool = False
    ) -> Union[JsonApiWorkspaceSettingInDocument, JsonApiWorkspaceSettingPostOptionalIdDocument]:
        if not post and self.id is None:
            raise ValueError(
                f"The combination for {post=} and {self.id=} is not valid. Id can be None only for post=True."
            )
        if post:
            return JsonApiWorkspaceSettingPostOptionalIdDocument(
                data=JsonApiWorkspaceSettingPostOptionalId(id=self.id, attributes=self._attributes())
            )
        else:
            return JsonApiWorkspaceSettingInDocument(
                data=JsonApiWorkspaceSettingIn(id=self.id, attributes=self._attributes())
            )
