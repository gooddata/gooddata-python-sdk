---
title: "list_users"
linkTitle: "list_users"
weight: 40
no_list: true
superheading: "catalog_user."
---



``list_users()``

Gets a list of all existing users.

{{% parameters-block  title="Parameters" None="yes"%}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="List[CatalogUser]" >}}
List of all Users as User entity objects.
{{< /parameter >}}
{{% /parameters-block %}}

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
