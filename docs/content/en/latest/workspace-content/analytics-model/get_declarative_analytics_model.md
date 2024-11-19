---
title: "get_declarative_analytics_model"
linkTitle: "get_declarative_analytics_model"
weight: 110
superheading: "catalog_workspace_content."
---

{{< api-ref "sdk.CatalogWorkspaceContentService.get_declarative_analytics_model" >}}

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
