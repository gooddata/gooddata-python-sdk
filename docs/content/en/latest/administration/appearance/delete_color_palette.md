---
title: "delete_color_palette"
linkTitle: "delete_color_palette"
superheading: "catalog_appearance."
weight: 240
api_ref: "CatalogAppearanceService.delete_color_palette"
---

``delete_color_palette( color_palette_id: str ) -> None``

Delete a color palette.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="color_palette_id" p_type="string" >}}
Color palette identification string e.g. "my_palette"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

{{% parameters-block title="Raises" %}}
{{< parameter p_type="Value Error" >}}
Color palette does not exist.
{{< /parameter >}}
{{% /parameters-block %}}
