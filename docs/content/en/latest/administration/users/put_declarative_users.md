---
title: "put_declarative_users"
linkTitle: "put_declarative_users"
weight: 100
no_list: true
superheading: "catalog_user."
---

{{< api-ref "sdk.CatalogUserService.put_declarative_users" >}}

## Example

```python
# Get users in declarative form
declarative_users = sdk.catalog_user.get_declarative_users()
# Do changes
declarative_users.(...)
# Put back on server
sdk.catalog_user.put_declarative_users(declarative_users)
```
