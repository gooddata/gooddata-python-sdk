---
title: "store_declarative_users"
linkTitle: "store_declarative_users"
weight: 110
no_list: true
superheading: "catalog_user."
---



``store_declarative_users(layout_root_path: Path = Path.cwd())``

Stores the users in directory hierarchy.

    gooddata_layouts
    └── organization_id
            └── users
                    └── users.yaml

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory.. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}
{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# Fetch users from the server and store them to directory
sdk.catalog_user.store_declarative_users(layout_root_path: Path = Path.cwd())
```
