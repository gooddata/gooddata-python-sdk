---
title: "put_declarative_analytics_model"
linkTitle: "put_declarative_analytics_model"
weight: 120
superheading: "catalog_workspace_content."
---

``put_declarative_analytics_model(workspace_id: str, analytics_model: CatalogDeclarativeAnalytics)``

Sets the declarative analytics model for a given workspace.

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="analytics_model" p_type="CatalogDeclarativeAnalytics" >}}
Object Containing declarative Analytical Model
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

Get an analytics model object `CatalogDeclarativeAnalytics` using [get_declarative_analytics_model](../get_declarative_analytics_model/) from your workspace, modify it and then put it back to the server:

```python
# Get analytics model
declarative_analytics = sdk.catalog_workspace_content.get_declarative_analytics_model(
    workspace_id = "123"
)

# Modify the `CatalogDeclarativeAnalytics` object:
# ...

# Put analytics model object back to the server:
sdk.catalog_workspace_content.put_declarative_analytics_model(
    workspace_id="123",
    analytics_model=declarative_analytics
)
```
