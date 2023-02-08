---
title: "load_declarative_user_groups"
linkTitle: "load_declarative_user_groups"
weight: 170
no_list: true
superheading: "catalog_user."
---



``load_declarative_user_groups(layout_root_path: Path = Path.cwd())``

Loads the declarative users groups layout, which was stored using [store_declarative_user_groups](../store_declarative_user_groups/).

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory.. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeUserGroups" >}}
Declarative user groups object.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Load user groups from directory
declarative_user_groups = sdk.catalog_user.load_declarative_user_groups(layout_root_path = Path.cwd())
```
