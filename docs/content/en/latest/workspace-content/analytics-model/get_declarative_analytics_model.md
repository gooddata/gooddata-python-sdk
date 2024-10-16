---
title: "get_declarative_analytics_model"
linkTitle: "get_declarative_analytics_model"
weight: 110
superheading: "catalog_workspace_content."
---

``get_declarative_analytics_model(workspace_id: str, exclude: Optional[list[str]])``

Gets an analytics model layout.


{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="exclude" p_type="Optional[list[str]]" >}}
Defines properties which should not be included in the payload.
E.g.: ["ACTIVITY_INFO"]
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeAnalytics" >}}
Object Containing declarative Analytical Model.
{{< /parameter >}}
{{% /parameters-block %}}


## Example

```python
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
