---
title: "put_declarative_users_user_groups"
linkTitle: "put_declarative_users_user_grou..."
weight: 200
no_list: true
superheading: "catalog_user."
---

<!-- TODO -->

``put_declarative_users_user_groups(users_user_groups: CatalogDeclarativeUsersUserGroups)``

Set all users and user groups.

## Example

```python
#Load users and user groups from directory
users_and_user_groups = sdk.catalog_user.load_declarative_users_user_groups(layout_root_pat =Path.cwd())

#Do changes...
#users_and_user_groups.users.(...)

#Put on server
sdk.catalog_user.put_declarative_users_user_groups(users_and_user_groups)
```
