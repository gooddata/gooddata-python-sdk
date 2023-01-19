---
title: "get_declarative_user_groups"
linkTitle: "get_declarative_user_groups"
weight: 140
no_list: true
superheading: "catalog_user."
---

``get_declarative_user_groups()``

Gets all user groups in a declarative form.


{{% parameters-block  title="Parameters" None="yes" %}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeUserGroups" >}}
Declarative User groups object.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get declarative user Groups
declarative_user_groups = sdk.catalog_user.get_declarative_user_groups()
```
