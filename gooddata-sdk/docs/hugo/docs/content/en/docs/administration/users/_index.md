---
title: "Users"
linkTitle: "Users"
weight: 30
no_list: true
---

Manage users.

See [Manage Users and UserGroups](https://www.gooddata.com/developers/cloud-native/doc/cloud/manage-deployment/manage-users/) to learn how user management works in GoodData.


### Entity Methods

* [create_or_update_user](./create_or_update_user/)
* [get_user](./get_user/)
* [delete_user](./delete_user/)
* [list_users](./list_users/)


### Declarative Methods

* [get_declarative_users](./get_declarative_users/)
* [put_declarative_users](./put_declarative_users/)
* [store_declarative_users](./store_declarative_users/)
* [load_declarative_users](./load_declarative_users/)
* [load_and_put_declarative_users](./load_and_put_declarative_users/)


## Example

List, create and delete users:

```python
from gooddata_sdk import GoodDataSdk, CatalogUser

# GoodData host in the form of uri
host = "http://localhost:3000"
# GoodData user token
token = "some_user_token"
sdk = GoodDataSdk.create(host, token)

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

# Define user
user = CatalogUser.init(user_id="abc", authentication_id="xyz",user_group_ids=["demoGroup"])

# Create user
sdk.catalog_user.create_or_update_user(user=user)

# Delete user
sdk.catalog_user.delete_user(user_id=user.id)
```
