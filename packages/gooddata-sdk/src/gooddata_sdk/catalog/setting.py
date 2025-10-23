# (C) 2022 GoodData Corporation
from __future__ import annotations

import builtins
from typing import Any, Optional

import attr
from gooddata_api_client.model.declarative_custom_application_setting import DeclarativeCustomApplicationSetting
from gooddata_api_client.model.declarative_setting import DeclarativeSetting

from gooddata_sdk.catalog.base import Base, value_in_allowed


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeSetting(Base):
    id: str
    type: str = attr.field(validator=value_in_allowed)
    content: Optional[dict[str, Any]] = None

    @staticmethod
    def client_class() -> builtins.type[DeclarativeSetting]:
        return DeclarativeSetting


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeCustomApplicationSetting(Base):
    id: str
    content: dict[str, Any]
    application_name: str

    @staticmethod
    def client_class() -> type[DeclarativeCustomApplicationSetting]:
        return DeclarativeCustomApplicationSetting
