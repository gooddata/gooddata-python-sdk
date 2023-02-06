---
title: "list_user_groups"
linkTitle: "list_user_groups"
weight: 80
no_list: true
superheading: "catalog_user."
---



``list_user_groups()``

Gets a list of all existing user groups.

{{% parameters-block  title="Parameters" None="yes" %}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="List[CatalogUserGroup]" >}}
List of all user groups as user group entity object.
{{< /parameter >}}
{{% /parameters-block %}}

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
