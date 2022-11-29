---
title: "create_or_update_user"
linkTitle: "create_or_update_user"
weight: 10
no_list: true
superheading: "catalog_user."
---

<!-- TODO -->

``create_or_update_user(user: CatalogUser)``

Create a new user or overwrite an existing user.

## Example

```python
# Create a user
sdk.catalog_user.create_or_update_user(
    CatalogUser.init(
        user_id="abc",
        authentication_id="xyz",
        user_group_ids=["demoGroup"]
    )
)
```
