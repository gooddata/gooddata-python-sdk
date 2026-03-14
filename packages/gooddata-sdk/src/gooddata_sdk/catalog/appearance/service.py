# (C) 2024 GoodData Corporation
from __future__ import annotations

import functools

from gooddata_api_client.exceptions import NotFoundException
from gooddata_api_client.model.json_api_color_palette_in_document import JsonApiColorPaletteInDocument
from gooddata_api_client.model.json_api_theme_in_document import JsonApiThemeInDocument

from gooddata_sdk.catalog.appearance.entity_model.color_palette import CatalogColorPalette
from gooddata_sdk.catalog.appearance.entity_model.theme import CatalogTheme
from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.utils import load_all_entities


class CatalogAppearanceService(CatalogServiceBase):
    def __init__(self, api_client: GoodDataApiClient) -> None:
        super().__init__(api_client)
        self._appearance_api = api_client.appearance_api

    # Theme methods

    def list_themes(self) -> list[CatalogTheme]:
        """Returns a list of all themes in the current organization.

        Returns:
            list[CatalogTheme]:
                List of themes in the current organization.
        """
        get_themes = functools.partial(self._appearance_api.get_all_entities_themes, _check_return_type=False)
        themes = load_all_entities(get_themes)
        return [CatalogTheme.from_api(theme) for theme in themes.data]

    def get_theme(self, theme_id: str) -> CatalogTheme:
        """Get an individual theme.

        Args:
            theme_id (str):
                Theme identification string e.g. "my_dark_theme"

        Returns:
            CatalogTheme:
                Catalog theme object containing structure of the theme.
        """
        theme_api = self._appearance_api.get_entity_themes(id=theme_id).data
        return CatalogTheme.from_api(theme_api)

    def create_theme(self, theme: CatalogTheme) -> None:
        """Create a new theme.

        Args:
            theme (CatalogTheme):
                A catalog theme object to be created.

        Returns:
            None
        """
        theme_document = JsonApiThemeInDocument(data=theme.to_api())
        self._appearance_api.create_entity_themes(json_api_theme_in_document=theme_document)

    def update_theme(self, theme: CatalogTheme) -> None:
        """Update a theme.

        Args:
            theme (CatalogTheme):
                A catalog theme object to be updated.

        Returns:
            None

        Raises:
            ValueError:
                Theme does not exist.
        """
        try:
            theme_document = JsonApiThemeInDocument(data=theme.to_api())
            self._appearance_api.update_entity_themes(theme.id, json_api_theme_in_document=theme_document)
        except NotFoundException:
            raise ValueError(f"Can not update {theme.id} theme. This theme does not exist.")

    def delete_theme(self, theme_id: str) -> None:
        """Delete a theme.

        Args:
            theme_id (str):
                Theme identification string e.g. "my_dark_theme"

        Returns:
            None

        Raises:
            ValueError:
                Theme does not exist.
        """
        try:
            self._appearance_api.delete_entity_themes(theme_id)
        except NotFoundException:
            raise ValueError(f"Can not delete {theme_id} theme. This theme does not exist.")

    # Color palette methods

    def list_color_palettes(self) -> list[CatalogColorPalette]:
        """Returns a list of all color palettes in the current organization.

        Returns:
            list[CatalogColorPalette]:
                List of color palettes in the current organization.
        """
        get_color_palettes = functools.partial(
            self._appearance_api.get_all_entities_color_palettes, _check_return_type=False
        )
        color_palettes = load_all_entities(get_color_palettes)
        return [CatalogColorPalette.from_api(color_palette) for color_palette in color_palettes.data]

    def get_color_palette(self, color_palette_id: str) -> CatalogColorPalette:
        """Get an individual color palette.

        Args:
            color_palette_id (str):
                Color palette identification string e.g. "my_palette"

        Returns:
            CatalogColorPalette:
                Catalog color palette object containing structure of the color palette.
        """
        color_palette_api = self._appearance_api.get_entity_color_palettes(id=color_palette_id).data
        return CatalogColorPalette.from_api(color_palette_api)

    def create_color_palette(self, color_palette: CatalogColorPalette) -> None:
        """Create a new color palette.

        Args:
            color_palette (CatalogColorPalette):
                A catalog color palette object to be created.

        Returns:
            None
        """
        color_palette_document = JsonApiColorPaletteInDocument(data=color_palette.to_api())
        self._appearance_api.create_entity_color_palettes(json_api_color_palette_in_document=color_palette_document)

    def update_color_palette(self, color_palette: CatalogColorPalette) -> None:
        """Update a color palette.

        Args:
            color_palette (CatalogColorPalette):
                A catalog color palette object to be updated.

        Returns:
            None

        Raises:
            ValueError:
                Color palette does not exist.
        """
        try:
            color_palette_document = JsonApiColorPaletteInDocument(data=color_palette.to_api())
            self._appearance_api.update_entity_color_palettes(
                color_palette.id, json_api_color_palette_in_document=color_palette_document
            )
        except NotFoundException:
            raise ValueError(f"Can not update {color_palette.id} color palette. This color palette does not exist.")

    def delete_color_palette(self, color_palette_id: str) -> None:
        """Delete a color palette.

        Args:
            color_palette_id (str):
                Color palette identification string e.g. "my_palette"

        Returns:
            None

        Raises:
            ValueError:
                Color palette does not exist.
        """
        try:
            self._appearance_api.delete_entity_color_palettes(color_palette_id)
        except NotFoundException:
            raise ValueError(f"Can not delete {color_palette_id} color palette. This color palette does not exist.")
