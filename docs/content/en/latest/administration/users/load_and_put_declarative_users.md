---
title: "load_and_put_declarative_users"
linkTitle: "load_and_put_declarative_users"
weight: 130
no_list: true
superheading: "catalog_user."
---



``load_and_put_declarative_users(layout_root_path: Path = Path.cwd())``

This method combines [load_declarative_users](../load_declarative_users/) and [put_declarative_users](../put_declarative_users/) methods to load and set users stored using [store_declarative_users](../store_declarative_users/).

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory.. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}
{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

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
