---
title: "get_declarative_analytics_model"
linkTitle: "get_declarative_analytics_model"
weight: 110
superheading: "catalog_workspace_content."
---

``get_declarative_analytics_model(workspace_id: str)``

Retrieve an analytics model layout.


{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeAnalytics" >}}
TODO hkad98
{{< /parameter >}}
{{% /parameters-block %}}


## Example

```Python
# Get analytics model layout
declarative_analytics = sdk.catalog_workspace_content.get_declarative_analytics_model(
    workspace_id="123"
)

# CatalogDeclarativeAnalytics(
#   analytics=CatalogDeclarativeAnalyticsLayer(
#       analytical_dashboards=[
#           CatalogDeclarativeAnalyticalDashboard(
#               id='campaign',
#               title='Campaign',
#               content={
#                   'filterContextRef': {
#                       'identifier': {
#                           'id': 'campaign_name_filter',
#                           'type': 'filterContext'
#                       }
#                   },
#                   'layout': {
#                       'type': 'IDashboardLayout',
#                       'sections': [
#                           {
#                               'items': ```
#                               'type': 'IDashboardLayoutSection',
# ...
```
