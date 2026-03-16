# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

from attrs import define
from gooddata_api_client.model.json_api_color_palette_in import JsonApiColorPaletteIn
from gooddata_api_client.model.json_api_color_palette_in_attributes import JsonApiColorPaletteInAttributes

from gooddata_sdk.catalog.base import Base


@define(kw_only=True)
class CatalogColorPalette(Base):
    id: str
    attributes: CatalogColorPaletteAttributes

    @staticmethod
    def client_class() -> type[JsonApiColorPaletteIn]:
        return JsonApiColorPaletteIn

    @classmethod
    def init(
        cls,
        color_palette_id: str,
        name: str,
        content: dict[str, Any],
    ) -> CatalogColorPalette:
        return cls(id=color_palette_id, attributes=CatalogColorPaletteAttributes(content=content, name=name))


@define(kw_only=True)
class CatalogColorPaletteAttributes(Base):
    content: dict[str, Any]
    name: str

    @staticmethod
    def client_class() -> type[JsonApiColorPaletteInAttributes]:
        return JsonApiColorPaletteInAttributes
