---
title: "create_or_update_user_group"
linkTitle: "create_or_update_user_group"
weight: 50
no_list: true
superheading: "catalog_user."
---

<!-- TODO -->

``create_or_update_user_group(user_group: CatalogUserGroup)``

Create a new user group or overwrite an existing user group.

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="user_group" p_type="CatalogUserGroup" >}}
UserGroup entity object.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example


```python
sdk.catalog_user.create_or_update_user_group(
    CatalogUserGroup.init(
        user_group_id="xyz",
        user_group_parent_ids=["demoGroup"]
    )
)
```
