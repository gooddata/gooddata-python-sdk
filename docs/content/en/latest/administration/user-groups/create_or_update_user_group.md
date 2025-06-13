---
title: "create_or_update_user_group"
linkTitle: "create_or_update_user_group"
weight: 50
no_list: true
superheading: "catalog_user."
---

{{< api-ref "sdk.CatalogUserService.create_or_update_user_group" >}}

## Example


```python
sdk.catalog_user.create_or_update_user_group(
    CatalogUserGroup.init(
        user_group_id="xyz",
        user_group_parent_ids=["demoGroup"]
    )
)
```
