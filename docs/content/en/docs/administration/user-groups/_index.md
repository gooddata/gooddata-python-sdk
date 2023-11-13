---
title: "User Groups"
linkTitle: "User Groups"
weight: 40
no_list: true
---

Manage user groups.

See [Manage Permissions](https://www.gooddata.com/docs/cloud/manage-deployment/manage-permissions/) to learn how permissions work in GoodData.


### Entity Methods

* [create_or_update_user_group](./create_or_update_user_group/)
* [get_user_group](./get_user_group/)
* [delete_user_group](./delete_user_group/)
* [list_user_groups](./list_user_groups/)

### Declarative Methods

* [get_declarative_user_groups](./get_declarative_user_groups/)
* [put_declarative_user_groups](./put_declarative_user_groups/)
* [store_declarative_user_groups](./store_declarative_user_groups/)
* [load_declarative_user_groups](./load_declarative_user_groups/)
* [load_and_put_declarative_user_groups](./load_and_put_declarative_user_groups/)

## Example

List, create and delete user groups:

```python
from gooddata_sdk import GoodDataSdk, CatalogUserGroup

# GoodData base URL, e.g. "https://www.example.com"
host = "https://www.example.com"
# GoodData user token
token = "some_user_token"
sdk = GoodDataSdk.create(host, token)

# List user groups
user_groups = sdk.catalog_user.list_user_groups()

print(user_groups)
#[
#    CatalogUserGroup()
#        id='adminGroup',
#        relationships=None
#    ),
#    CatalogUserGroup(id='adminQA1Group',
#        relationships=CatalogUserGroupRelationships(
#           parents=CatalogUserGroupParents(
#               data=[
#                   CatalogUserGroup(
#                        id='adminGroup',
#                        relationships=None
#                    )
#                ]
#            )
#        )
#    )
#    ...
#]

# Define user group
user_group = CatalogUserGroup.init(user_group_id="xyz", user_group_parent_ids=["demoGroup"])

# Create user group
sdk.catalog_user.create_or_update_user_group(user_group=user_group)

# Delete user group
sdk.catalog_user.delete_user_group(user_group_id=user_group.id)
```
