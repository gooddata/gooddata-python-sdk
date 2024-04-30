---
title: "store_declarative_user_groups"
linkTitle: "store_declarative_user_groups"
weight: 160
no_list: true
superheading: "catalog_user."
---



``store_declarative_user_groups(layout_root_path: Path = Path.cwd())``

Stores all the user groups in a directory hierarchy.

    gooddata_layouts
    └── organization_id
            └── user_groups
                    └── user_groups.yaml

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory.. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

## Example

```python
# Fetch user groups from the server and store them to directory
sdk.catalog_user.store_declarative_user_groups(layout_root_path = Path.cwd())
```
