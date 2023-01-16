---
title: "get_declarative_users_user_groups"
linkTitle: "get_declarative_users_user_grou..."
weight: 190
no_list: true
superheading: "catalog_user."
---

<!-- TODO -->

``get_declarative_users_user_groups()``

Retrieves all users and user groups in a declarative form.

{{% parameters-block  title="Parameters" None="yes" %}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeUsersUserGroups" >}}
Declarative Users and User Groups object.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
#Get all users and user groups
users_and_user_groups = sdk.catalog_user.get_declarative_users_user_groups()
```
