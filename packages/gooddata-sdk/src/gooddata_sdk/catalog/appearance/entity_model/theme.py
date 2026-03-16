# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

from attrs import define
from gooddata_api_client.model.json_api_color_palette_in_attributes import JsonApiColorPaletteInAttributes
from gooddata_api_client.model.json_api_theme_in import JsonApiThemeIn

from gooddata_sdk.catalog.base import Base


@define(kw_only=True)
class CatalogTheme(Base):
    id: str
    attributes: CatalogThemeAttributes

    @staticmethod
    def client_class() -> type[JsonApiThemeIn]:
        return JsonApiThemeIn

    @classmethod
    def init(
        cls,
        theme_id: str,
        name: str,
        content: dict[str, Any],
    ) -> CatalogTheme:
        return cls(id=theme_id, attributes=CatalogThemeAttributes(content=content, name=name))


@define(kw_only=True)
class CatalogThemeAttributes(Base):
    content: dict[str, Any]
    name: str

    @staticmethod
    def client_class() -> type[JsonApiColorPaletteInAttributes]:
        return JsonApiColorPaletteInAttributes
