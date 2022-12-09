---
title: "get_declarative_analytics_model"
linkTitle: "get_declarative_analytics_model"
weight: 110
superheading: "catalog_workspace_content."
---

<!-- TODO -->

``get_declarative_analytics_model(workspace_id: str)``

Returns *CatalogDeclarativeAnalytics*.

Retrieve an analytics model layout.

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
