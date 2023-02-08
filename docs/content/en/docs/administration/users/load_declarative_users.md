---
title: "load_declarative_users"
linkTitle: "load_declarative_users"
weight: 120
no_list: true
superheading: "catalog_user."
---



``load_declarative_users(layout_root_path: Path = Path.cwd())``

Loads declarative users layout, which was stored using [store_declarative_users](../store_declarative_users/).

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory.. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}
{{% parameters-block title="Returns"%}}
{{< parameter p_type="CatalogDeclarativeUsers" >}}
Declarative users object.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Load users from directory
declarative_users = sdk.catalog_user.load_declarative_users(layout_root_path: Path = Path.cwd())
```
