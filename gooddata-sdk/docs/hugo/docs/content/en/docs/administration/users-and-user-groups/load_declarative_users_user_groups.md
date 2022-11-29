---
title: "load_declarative_users_user_groups"
linkTitle: "load_declarative_users_user_gro..."
weight: 220
no_list: true
superheading: "catalog_user."
---

<!-- TODO -->

``load_declarative_users_user_groups(layout_root_path: Path = Path.cwd())``

Returns *CatalogDeclarativeUsersUserGroups*.

Load users and user groups from directory hierarchy.

## Example

```python
#Load users and user groups from directory
users_and_user_groups = sdk.catalog_user.load_declarative_users_user_groups(layout_root_path=Path.cwd())
```
