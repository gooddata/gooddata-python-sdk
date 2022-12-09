---
title: "load_declarative_users"
linkTitle: "load_declarative_users"
weight: 120
no_list: true
superheading: "catalog_user."
---

<!-- TODO -->

``load_declarative_users(layout_root_path: Path = Path.cwd())``

Load users from directory hierarchy.

## Example

```python
#Load users from directory
declarative_users = sdk.catalog_user.load_declarative_users(layout_root_path: Path = Path.cwd())
```
