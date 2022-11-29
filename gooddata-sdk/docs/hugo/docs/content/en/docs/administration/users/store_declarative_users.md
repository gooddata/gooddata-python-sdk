---
title: "store_declarative_users"
linkTitle: "store_declarative_users"
weight: 110
no_list: true
superheading: "catalog_user."
---

<!-- TODO -->

``store_declarative_users(layout_root_path: Path = Path.cwd())``

Store users in directory hierarchy. Directly from server.

    gooddata_layouts
    └── organization_id
            └── users
                    └── users.yaml

## Example

```python
#Fetch users from the server and store them to directory
sdk.catalog_user.store_declarative_users(layout_root_path: Path = Path.cwd())
```
