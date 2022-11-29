---
title: "store_declarative_user_groups"
linkTitle: "store_declarative_user_groups"
weight: 160
no_list: true
superheading: "catalog_user."
---

<!-- TODO -->

``store_declarative_user_groups(layout_root_path: Path = Path.cwd())``

Store user groups in directory hierarchy.

    gooddata_layouts
    └── organization_id
            └── user_groups
                    └── user_groups.yaml

## Example

```python
#Fetch user groups from the server and store them to directory
sdk.catalog_user.store_declarative_user_groups(layout_root_path = Path.cwd())
```
