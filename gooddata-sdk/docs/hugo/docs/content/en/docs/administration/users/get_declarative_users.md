---
title: "get_declarative_users"
linkTitle: "get_declarative_users"
weight: 90
no_list: true
superheading: "catalog_user."
---

<!-- TODO -->

``get_declarative_users()``

Retrieve all users including authentication properties.

{{% parameters-block  title="Parameters" None="yes" %}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeUsers" >}}
Declarative Users object.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
#Retrieve users in declarative form
declarative_users = sdk.catalog_user.get_declarative_users()
```
