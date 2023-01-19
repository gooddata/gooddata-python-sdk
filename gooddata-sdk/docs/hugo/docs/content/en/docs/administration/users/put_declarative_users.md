---
title: "put_declarative_users"
linkTitle: "put_declarative_users"
weight: 100
no_list: true
superheading: "catalog_user."
---



``put_declarative_users(users: CatalogDeclarativeUsers)``

Sets all users and their authentication properties.

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="users" p_type="CatalogDeclarativeUsers" >}}
Declarative users object, incuding authetication properties.
{{< /parameter >}}
{{% /parameters-block %}}
{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# Get users in declarative form
declarative_users = sdk.catalog_user.get_declarative_users()
# Do changes
declarative_users.(...)
# Put back on server
sdk.catalog_user.put_declarative_users(declarative_users)
```
