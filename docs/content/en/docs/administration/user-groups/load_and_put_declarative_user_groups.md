---
title: "load_and_put_declarative_user_groups"
linkTitle: "load_and_put_declarative_user_g..."
weight: 180
no_list: true
superheading: "catalog_user."
---



``load_and_put_declarative_user_groups(layout_root_path: Path = Path.cwd())``

This method combines [load_declarative_user_groups](../load_declarative_user_groups/) and [put_declarative_user_groups](../put_declarative_user_groups/) methods to load and
set user groups stored using [store_declarative_user_groups](../store_declarative_user_groups/).

{{% parameters-block  title="Parameters" %}}
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
# Load and put user groups in one method
sdk.catalog_user.load_and_put_declarative_user_groups(layout_root_path = Path.cwd())
```
Or by two separate calls:

```python
# Load user groups from directory
declarative_user_groups = sdk.catalog_user.load_declarative_user_groups(layout_root_path = Path.cwd())

# Put on server
sdk.catalog_user.put_declarative_user_groups(declarative_user_groups)
```

The result is identical.
