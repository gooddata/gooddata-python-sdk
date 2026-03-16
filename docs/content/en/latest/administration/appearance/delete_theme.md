---
title: "delete_theme"
linkTitle: "delete_theme"
superheading: "catalog_appearance."
weight: 140
api_ref: "CatalogAppearanceService.delete_theme"
---

``delete_theme( theme_id: str ) -> None``

Delete a theme.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="theme_id" p_type="string" >}}
Theme identification string e.g. "my_dark_theme"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

{{% parameters-block title="Raises" %}}
{{< parameter p_type="Value Error" >}}
Theme does not exist.
{{< /parameter >}}
{{% /parameters-block %}}
