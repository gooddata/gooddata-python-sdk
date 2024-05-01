---
title: "create_or_update_user"
linkTitle: "create_or_update_user"
weight: 10
no_list: true
superheading: "catalog_user."
---



``create_or_update_user(user: CatalogUser)``

Creates a new user or overwrites an existing user.

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="user" p_type="CatalogUser" >}}
User entity object.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

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
