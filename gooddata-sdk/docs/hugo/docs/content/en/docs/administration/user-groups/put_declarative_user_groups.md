---
title: "put_declarative_user_groups"
linkTitle: "put_declarative_user_groups"
weight: 150
no_list: true
superheading: "catalog_user."
---

<!-- TODO -->

``put_declarative_user_groups(user_groups: CatalogDeclarativeUserGroups)``

Set all user groups with their parents eventually.

## Example


```python
#Retrieve user groups in declarative form
declarative_user_groups = sdk.catalog_user.get_declarative_user_groups()

#Do changes
#declarative_user_groups.(...)

#Put back on server
sdk.catalog_user.put_declarative_user_groups(declarative_user_groups)
```
