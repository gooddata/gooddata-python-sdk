---
title: "load_declarative_analytics_model"
linkTitle: "load_declarative_analytics_model"
weight: 140
superheading: "catalog_workspace_content."
---



``load_declarative_analytics_model(workspace_id: str, layout_root_path: Path = Path.cwd())``

Loads declarative analytics layout, which was stored using [store_declarative_analytics_model](../store_declarative_analytics_model/).

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeAnalytics" >}}
Object Containing declarative Analytical Model
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get analytics layout
declarative_analytics = sdk.catalog_workspace_content.load_declarative_analytics_model(
    workspace_id="123",
    layout_root_path=Path.cwd()
)
```
