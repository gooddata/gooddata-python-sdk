# (C) 2023 GoodData Corporation
from __future__ import annotations

import functools
from typing import Any, Union

import attr
from gooddata_api_client.model.json_api_organization_setting_in_attributes import JsonApiOrganizationSettingInAttributes
from gooddata_api_client.model.json_api_workspace_setting_in import JsonApiWorkspaceSettingIn
from gooddata_api_client.model.json_api_workspace_setting_in_document import JsonApiWorkspaceSettingInDocument
from gooddata_api_client.model.json_api_workspace_setting_out import JsonApiWorkspaceSettingOut
from gooddata_api_client.model.json_api_workspace_setting_post_optional_id import JsonApiWorkspaceSettingPostOptionalId
from gooddata_api_client.model.json_api_workspace_setting_post_optional_id_document import (
    JsonApiWorkspaceSettingPostOptionalIdDocument,
)

from gooddata_sdk.catalog.base import Base, value_in_allowed
from gooddata_sdk.utils import safeget


@attr.s(auto_attribs=True, kw_only=True)
class CatalogWorkspaceSetting(Base):
    id: str = attr.field(default=None)
    setting_type: str = attr.field(
        validator=functools.partial(value_in_allowed, client_class=JsonApiOrganizationSettingInAttributes)
    )
    content: dict = attr.field(
        repr=False,
        default=attr.Factory(lambda self: safeget(self.json_api_entity.attributes, ["content"]), takes_self=True),
    )

    @staticmethod
    def client_class() -> type[JsonApiWorkspaceSettingOut]:
        return JsonApiWorkspaceSettingOut

    def _attributes(self) -> JsonApiOrganizationSettingInAttributes:
        return JsonApiOrganizationSettingInAttributes(
            content=self.content,
            type=self.setting_type,
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

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogWorkspaceSetting:
        return cls(
            id=entity["id"],
            setting_type=entity["attributes"]["type"],
            content=entity["attributes"]["content"],
        )
