---
title: "load_and_put_declarative_analytics_model"
linkTitle: "load_and_put_declarative_analyt..."
weight: 150
superheading: "catalog_workspace_content."
---



``load_and_put_declarative_analytics_model(workspace_id: str, layout_root_path: Path = Path.cwd())``

This method combines [load_declarative_analytics_model](../load_declarative_analytics_model/) and [put_declarative_analytics_model](../put_declarative_analytics_model/) methods to load and set layouts stored using [store_declarative_analytics_model](../store_declarative_analytics_model/).

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

The load and put can be done two ways.

Either by one call:

```python
# Load and put on server the stored layout
sdk.catalog_workspace_content.load_and_put_declarative_analytics_model(
    workspace_id="123",
    layout_root_path=Path.cwd()
)
```

Or by two separate calls:

```python
# Get analytics layout
declarative_analytics = sdk.catalog_workspace_content.load_declarative_analytics_model(
    workspace_id="123",
    layout_root_path=Path.cwd()
)

# Put analytics model object back to the server:
sdk.catalog_workspace_content.put_declarative_analytics_model(
    workspace_id="123",
    analytics_model=declarative_analytics
)
```

The result is identical.
