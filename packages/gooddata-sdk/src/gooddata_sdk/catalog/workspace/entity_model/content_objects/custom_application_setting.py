# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any, Union

from attrs import define, field
from gooddata_api_client.model.json_api_custom_application_setting_in import JsonApiCustomApplicationSettingIn
from gooddata_api_client.model.json_api_custom_application_setting_in_attributes import (
    JsonApiCustomApplicationSettingInAttributes,
)
from gooddata_api_client.model.json_api_custom_application_setting_in_document import (
    JsonApiCustomApplicationSettingInDocument,
)
from gooddata_api_client.model.json_api_custom_application_setting_out import JsonApiCustomApplicationSettingOut
from gooddata_api_client.model.json_api_custom_application_setting_post_optional_id import (
    JsonApiCustomApplicationSettingPostOptionalId,
)
from gooddata_api_client.model.json_api_custom_application_setting_post_optional_id_document import (
    JsonApiCustomApplicationSettingPostOptionalIdDocument,
)

from gooddata_sdk.catalog.base import Base


@define(kw_only=True)
class CatalogCustomApplicationSetting(Base):
    """A workspace setting owned by a custom application.

    Unlike CatalogWorkspaceSetting, the content is free-form and is scoped by
    `application_name` rather than by a fixed setting type.
    """

    id: str | None = field(default=None)
    application_name: str
    content: dict[str, Any] = field(repr=False)

    @staticmethod
    def client_class() -> type[JsonApiCustomApplicationSettingOut]:
        return JsonApiCustomApplicationSettingOut

    def _attributes(self) -> JsonApiCustomApplicationSettingInAttributes:
        return JsonApiCustomApplicationSettingInAttributes(
            application_name=self.application_name,
            content=self.content,
        )

    def to_api(
        self, post: bool = False
    ) -> Union[JsonApiCustomApplicationSettingInDocument, JsonApiCustomApplicationSettingPostOptionalIdDocument]:
        if post:
            # The generated model rejects id=None; "optional" means the key is omitted
            # so that the backend generates the id.
            kwargs: dict[str, Any] = {"id": self.id} if self.id is not None else {}
            return JsonApiCustomApplicationSettingPostOptionalIdDocument(
                data=JsonApiCustomApplicationSettingPostOptionalId(attributes=self._attributes(), **kwargs)
            )
        if self.id is None:
            raise ValueError(
                f"The combination for {post=} and {self.id=} is not valid. Id can be None only for post=True."
            )
        return JsonApiCustomApplicationSettingInDocument(
            data=JsonApiCustomApplicationSettingIn(id=self.id, attributes=self._attributes())
        )

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogCustomApplicationSetting:
        # Works on a plain dict: list responses are loaded with _check_return_type=False
        # to avoid the composed-schema validation failure on *OutWithLinks items.
        return cls(
            id=entity["id"],
            application_name=entity["attributes"]["applicationName"],
            content=entity["attributes"]["content"],
        )
