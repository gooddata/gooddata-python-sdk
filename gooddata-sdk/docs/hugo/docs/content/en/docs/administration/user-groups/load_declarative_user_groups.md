---
title: "load_declarative_user_groups"
linkTitle: "load_declarative_user_groups"
weight: 170
no_list: true
superheading: "catalog_user."
---

<!-- TODO -->

``load_declarative_user_groups(layout_root_path: Path = Path.cwd())``

Returns *CatalogDeclarativeUserGroups*.

Load user groups from directory hierarchy.

## Example

```python
#Load user groups from directory
declarative_user_groups = sdk.catalog_user.load_declarative_user_groups(layout_root_path = Path.cwd())
```
