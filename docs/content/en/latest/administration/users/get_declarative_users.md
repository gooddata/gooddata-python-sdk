---
title: "get_declarative_users"
linkTitle: "get_declarative_users"
weight: 90
no_list: true
superheading: "catalog_user."
---



``get_declarative_users()``


Gets all users including authentication properties.


{{% parameters-block  title="Parameters" None="yes" %}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeUsers" >}}
Declarative users object.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get users in declarative form
declarative_users = sdk.catalog_user.get_declarative_users()
```
