---
title: "create_or_update_user"
linkTitle: "create_or_update_user"
weight: 10
no_list: true
superheading: "catalog_user."
---

{{< api-ref "sdk.CatalogUserService.create_or_update_user" >}}

## Example

```python
# Create a user
sdk.catalog_user.create_or_update_user(
    CatalogUser.init(
        user_id="abc",
        firstname="John",
        lastname="Doe",
        email="john.doe@email.com",
        authentication_id="xyz",
        user_group_ids=["demoGroup"]
    )
)
```
