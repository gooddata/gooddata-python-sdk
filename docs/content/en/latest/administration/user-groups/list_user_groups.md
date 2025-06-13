---
title: "list_user_groups"
linkTitle: "list_user_groups"
weight: 80
no_list: true
superheading: "catalog_user."
---

{{< api-ref "sdk.CatalogUserService.list_user_groups" >}}

## Example

```python
# List user groups
user_groups = sdk.catalog_user.list_user_groups()

print(user_groups)
# [
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
# ]
```
