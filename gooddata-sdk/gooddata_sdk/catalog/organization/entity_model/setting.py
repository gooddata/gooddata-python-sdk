# (C) 2023 GoodData Corporation
from __future__ import annotations

from typing import Any, Dict, Optional, Type

import attr

from gooddata_api_client.model.json_api_organization_setting_in import JsonApiOrganizationSettingIn
from gooddata_api_client.model.json_api_organization_setting_in_attributes import JsonApiOrganizationSettingInAttributes
from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogOrganizationSetting(Base):
    id: str
    attributes: CatalogOrganizationSettingAttributes

    @classmethod
    def init(cls, setting_id: str, setting_type: str, content: Dict[str, Any]) -> CatalogOrganizationSetting:
        return cls(id=setting_id, attributes=CatalogOrganizationSettingAttributes(type=setting_type, content=content))

    @staticmethod
    def client_class() -> Type[JsonApiOrganizationSettingIn]:
        return JsonApiOrganizationSettingIn


@attr.s(auto_attribs=True, kw_only=True)
class CatalogOrganizationSettingAttributes(Base):
    type: Optional[str]
    content: Dict[str, Any]

    @staticmethod
    def client_class() -> Type[JsonApiOrganizationSettingInAttributes]:
        return JsonApiOrganizationSettingInAttributes
