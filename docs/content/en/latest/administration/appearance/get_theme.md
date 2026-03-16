---
title: "get_theme"
linkTitle: "get_theme"
superheading: "catalog_appearance."
weight: 110
---

``get_theme( theme_id: str ) -> CatalogTheme``

Get an individual theme.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="theme_id" p_type="string" >}}
Theme identification string e.g. "my_dark_theme"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogTheme" >}}
Catalog theme object containing structure of the theme.
{{< /parameter >}}
{{% /parameters-block %}}
