# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Dict, Optional, Type

import attr

from gooddata_api_client.model.declarative_custom_application_setting import DeclarativeCustomApplicationSetting
from gooddata_api_client.model.declarative_setting import DeclarativeSetting
from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeSetting(Base):
    id: str
    content: Optional[Dict[str, Any]] = None

    @staticmethod
    def client_class() -> Type[DeclarativeSetting]:
        return DeclarativeSetting


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeCustomApplicationSetting(Base):
    id: str
    content: Dict[str, Any]
    application_name: str

    @staticmethod
    def client_class() -> Type[DeclarativeCustomApplicationSetting]:
        return DeclarativeCustomApplicationSetting
