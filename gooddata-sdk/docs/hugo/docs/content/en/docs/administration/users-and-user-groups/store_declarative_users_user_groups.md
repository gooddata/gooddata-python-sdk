---
title: "store_declarative_users_user_groups"
linkTitle: "store_declarative_users_user_gro..."
weight: 210
no_list: true
superheading: "catalog_user."
---



``store_declarative_users_user_groups(layout_root_path: Path = Path.cwd())``

Stores all the users and user groups in a directory hierarchy.

    gooddata_layouts
    └── organization_id
            ├── users
            │      └── users.yaml
            └── user_groups
                    └── user_groups.yaml

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory.. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}
{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# Fetch users and user groups from the server and store them to directory
sdk.catalog_user.store_declarative_users_user_groups(layout_root_path: Path = Path.cwd())
```
