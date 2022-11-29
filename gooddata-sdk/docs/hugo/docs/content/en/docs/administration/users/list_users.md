---
title: "list_users"
linkTitle: "list_users"
weight: 40
no_list: true
superheading: "catalog_user."
---

<!-- TODO -->

``list_users()``

Returns *List[CatalogUser]*.

Get a list of all existing users.

## Example


```python
# List users
users = sdk.catalog_user.list_users()

print(users)
# [
#   CatalogUser(
#       id='demo2',
#       attributes=CatalogUserAttributes(
#            authentication_id='abc'
#       ),
#       relationships=CatalogUserRelationships(
#           user_groups=CatalogUserGroupsData(
#               data=[
#                   CatalogUserGroup(
#                       id='demoGroup',
#                       relationships=None
#                   )
#               ]
#           )
#       )
#  ),
#   ...
# ]
```
