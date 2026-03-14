---
title: "Appearance"
linkTitle: "Appearance"
weight: 15
no_list: true
---

Manage themes and color palettes for your organization.

## Methods

### Themes

* [list_themes](./list_themes/)
* [get_theme](./get_theme/)
* [create_theme](./create_theme/)
* [update_theme](./update_theme/)
* [delete_theme](./delete_theme/)

### Color Palettes

* [list_color_palettes](./list_color_palettes/)
* [get_color_palette](./get_color_palette/)
* [create_color_palette](./create_color_palette/)
* [update_color_palette](./update_color_palette/)
* [delete_color_palette](./delete_color_palette/)

## Example

Create a custom theme and color palette:

```python
from gooddata_sdk import GoodDataSdk, CatalogTheme, CatalogColorPalette

host = "https://www.example.com"
token = "some_user_token"
sdk = GoodDataSdk.create(host, token)

# Create a custom theme
theme = CatalogTheme.init(
    theme_id="my_dark_theme",
    name="My Dark Theme",
    content={
        "palette": {
            "primary": {"base": "#14B2E2"},
        },
        "dashboards": {
            "content": {
                "widget": {
                    "backgroundColor": "#122330",
                }
            }
        },
    },
)
sdk.catalog_appearance.create_theme(theme)

# List all themes
themes = sdk.catalog_appearance.list_themes()

# Create a custom color palette for charts
palette = CatalogColorPalette.init(
    color_palette_id="my_palette",
    name="My Palette",
    content={
        "colorPalette": [
            {"guid": "01", "fill": {"r": 140, "g": 125, "b": 232}},
            {"guid": "02", "fill": {"r": 125, "g": 219, "b": 232}},
        ]
    },
)
sdk.catalog_appearance.create_color_palette(palette)

# Clean up
sdk.catalog_appearance.delete_theme("my_dark_theme")
sdk.catalog_appearance.delete_color_palette("my_palette")
```
