---
title: "load_analytics_model_from_disk"
linkTitle: "load_analytics_model_from_disk"
weight: 132
superheading: "catalog_workspace_content."
---

``load_analytics_model_from_disk(path: Path = Path.cwd())``

Loads the analytics model stored to disk using [store_analytics_model_to_disk](../store_analytics_model_to_disk/).

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="path" p_type="Optional[Path]" >}}
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
# Get Analytics model from disk
declarative_analytics = sdk.catalog_workspace_content.load_analytics_model_from_disk(
    path=Path.cwd()
)
```
