---
title: "put_declarative_user_groups"
linkTitle: "put_declarative_user_groups"
weight: 150
no_list: true
superheading: "catalog_user."
---

{{< api-ref "sdk.CatalogUserService.put_declarative_user_groups" >}}

## Example


```python
# Get user groups in declarative form
declarative_user_groups = sdk.catalog_user.get_declarative_user_groups()

# Do changes
# declarative_user_groups.(...)

# Put back on server
sdk.catalog_user.put_declarative_user_groups(declarative_user_groups)
```
