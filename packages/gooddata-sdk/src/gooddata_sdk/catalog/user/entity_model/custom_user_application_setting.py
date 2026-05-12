# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

import attrs
from gooddata_api_client.model.json_api_custom_user_application_setting_in import (
    JsonApiCustomUserApplicationSettingIn,
)
from gooddata_api_client.model.json_api_custom_user_application_setting_in_attributes import (
    JsonApiCustomUserApplicationSettingInAttributes,
)
from gooddata_api_client.model.json_api_custom_user_application_setting_in_document import (
    JsonApiCustomUserApplicationSettingInDocument,
)
from gooddata_api_client.model.json_api_custom_user_application_setting_post_optional_id import (
    JsonApiCustomUserApplicationSettingPostOptionalId,
)
from gooddata_api_client.model.json_api_custom_user_application_setting_post_optional_id_document import (
    JsonApiCustomUserApplicationSettingPostOptionalIdDocument,
)

from gooddata_sdk.catalog.base import Base


@attrs.define(kw_only=True)
class CatalogCustomUserApplicationSettingAttributes(Base):
    """Attributes of a custom user application setting."""

    application_name: str
    content: dict[str, Any]
    workspace_id: str | None = None

    @staticmethod
    def client_class() -> type[JsonApiCustomUserApplicationSettingInAttributes]:
        return JsonApiCustomUserApplicationSettingInAttributes


@attrs.define(kw_only=True)
class CatalogCustomUserApplicationSetting(Base):
    """Entity representing a per-user application setting."""

    id: str
    attributes: CatalogCustomUserApplicationSettingAttributes

    @staticmethod
    def client_class() -> type[JsonApiCustomUserApplicationSettingIn]:
        return JsonApiCustomUserApplicationSettingIn

    @classmethod
    def init(
        cls,
        setting_id: str,
        application_name: str,
        content: dict[str, Any],
        *,
        workspace_id: str | None = None,
    ) -> CatalogCustomUserApplicationSetting:
        """Convenience factory to create a setting entity without constructing attributes manually."""
        return cls(
            id=setting_id,
            attributes=CatalogCustomUserApplicationSettingAttributes(
                application_name=application_name,
                content=content,
                workspace_id=workspace_id,
            ),
        )

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogCustomUserApplicationSetting:
        ea = entity.get("attributes", {})
        return cls(
            id=entity["id"],
            attributes=CatalogCustomUserApplicationSettingAttributes(
                application_name=ea["applicationName"],
                content=ea["content"],
                workspace_id=ea.get("workspaceId"),
            ),
        )

    def as_post_document(self) -> JsonApiCustomUserApplicationSettingPostOptionalIdDocument:
        """Serialize to the document form used by the POST (create) endpoint."""
        kwargs: dict[str, Any] = {}
        if self.attributes.workspace_id is not None:
            kwargs["workspace_id"] = self.attributes.workspace_id
        api_attrs = JsonApiCustomUserApplicationSettingInAttributes(
            application_name=self.attributes.application_name,
            content=self.attributes.content,
            _check_type=False,
            **kwargs,
        )
        data = JsonApiCustomUserApplicationSettingPostOptionalId(
            attributes=api_attrs,
            id=self.id,
            _check_type=False,
        )
        return JsonApiCustomUserApplicationSettingPostOptionalIdDocument(data=data, _check_type=False)

    def as_patch_document(self) -> JsonApiCustomUserApplicationSettingInDocument:
        """Serialize to the document form used by the PATCH (update) endpoint."""
        kwargs: dict[str, Any] = {}
        if self.attributes.workspace_id is not None:
            kwargs["workspace_id"] = self.attributes.workspace_id
        api_attrs = JsonApiCustomUserApplicationSettingInAttributes(
            application_name=self.attributes.application_name,
            content=self.attributes.content,
            _check_type=False,
            **kwargs,
        )
        data = JsonApiCustomUserApplicationSettingIn(
            attributes=api_attrs,
            id=self.id,
            _check_type=False,
        )
        return JsonApiCustomUserApplicationSettingInDocument(data=data, _check_type=False)
