---
title: "get_color_palette"
linkTitle: "get_color_palette"
superheading: "catalog_appearance."
weight: 210
---

``get_color_palette( color_palette_id: str ) -> CatalogColorPalette``

Get an individual color palette.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="color_palette_id" p_type="string" >}}
Color palette identification string e.g. "my_palette"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogColorPalette" >}}
Catalog color palette object containing structure of the color palette.
{{< /parameter >}}
{{% /parameters-block %}}
