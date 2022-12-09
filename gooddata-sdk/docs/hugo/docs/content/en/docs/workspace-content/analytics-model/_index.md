---
title: "Analytics Model"
linkTitle: "Analytics Model"
weight: 23
no_list: true
---
Manage Analytics model.

## Methods

* [get_declarative_analytics_model](./get_declarative_analytics_model/)
* [load_and_put_declarative_analytics_model](./load_and_put_declarative_analytics_model/)
* [load_declarative_analytics_model](./load_declarative_analytics_model/)
* [put_declarative_analytics_model](./put_declarative_analytics_model/)
* [store_declarative_analytics_model](./store_declarative_analytics_model/)
* [store_analytics_model_to_disk](./store_analytics_model_to_disk/)
* [load_analytics_model_from_disk](./load_analytics_model_from_disk/)

## Example

```python
from gooddata_sdk import GoodDataSdk

# GoodData base URL, e.g. "https://www.example.com"
host = "https://www.example.com"
# GoodData user token
token = "some_user_token"
sdk = GoodDataSdk.create(host, token)

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

len(declarative_analytics)
```
