---
title: "load_and_put_declarative_users"
linkTitle: "load_and_put_declarative_users"
weight: 130
no_list: true
superheading: "catalog_user."
---

{{< api-ref "sdk.CatalogUserService.load_and_put_declarative_users" >}}

## Example

The load and put can be done two ways.

Either by one call:

```python
# Load and put users in one method
sdk.catalog_user.load_and_put_declarative_users(layout_root_path: Path = Path.cwd())
```
Or by two separate calls:

```python
# Load users from directory
declarative_users = sdk.catalog_user.load_declarative_users(layout_root_path: Path = Path.cwd())
# Put on server
sdk.catalog_user.put_declarative_users(declarative_users)
```

The result is identical.
