---
title: "load_and_put_declarative_users_user_groups"
linkTitle: "load_and_put_declarative_users..."
weight: 230
no_list: true
superheading: "catalog_user."
---

{{< api-ref "sdk.CatalogUserService.load_and_put_declarative_users_user_groups" >}}

## Example

The load and put can be done two ways.

Either by one call:

```python
# Load and put users and user groups in one method
sdk.catalog_user.load_and_put_declarative_users_user_groups(layout_root_path: Path = Path.cwd())
```
Or by two separate calls:

```python
# Load users and user groups from directory
declarative_users_and_user_groups = sdk.catalog_user.load_declarative_users_user_groups(layout_root_path: Path = Path.cwd())
# Put on server
sdk.catalog_user.put_declarative_users_user_groups(declarative_users_and_user_groups)
```

The result is identical.
