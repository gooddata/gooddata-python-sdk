---
title: "store_declarative_users_user_groups"
linkTitle: "store_declarative_users_user_gro..."
weight: 210
no_list: true
superheading: "catalog_user."
---

<!-- TODO -->

``store_declarative_users_user_groups(layout_root_path: Path = Path.cwd())``

Store users and user groups in directory hierarchy.

    gooddata_layouts
    └── organization_id
            ├── users
            │      └── users.yaml
            └── user_groups
                    └── user_groups.yaml

## Example

```python
#Fetch users and user groups from the server and store them to directory
sdk.catalog_user.store_declarative_users_user_groups(layout_root_path: Path = Path.cwd())
```
