---
title: "Workspace Contents"
linkTitle: "Workspace Contents"
weight: 40
no_list: true
---

Workspace content includes all:

* Facts
* Attributes
* Labels
* Metrics
* Visualizations
* Dashboards

Within a multitenant workspace hierarchy, the analytical model of a parent workspace is shared with child workspaces.

### Entity methods

* [get_full_catalog](./get_full_catalog/)
* [get_visualization](./get_visualization/)
* [get_visualizations](./get_visualizations/)
* [get_metrics_catalog](./get_metrics_catalog/)
* [get_facts_catalog](./get_facts_catalog/)
* [get_attributes_catalog](./get_attributes_catalog/)
* [get_labels_catalog](./get_labels_catalog/)

### Entity graph methods

* [get_dependent_entities_graph](./get_dependent_entities_graph/)
* [get_dependent_entities_graph_from_entry_points](./get_dependent_entities_graph_from_entry_points/)

### Table methods

* [for_visualization](./for_visualization/)
* [for_items](./for_items/)

## Example

Connect to a workspace and create lists of all datesets, metrics, attributes and facts the workspace contains:

```python
from gooddata_sdk import GoodDataSdk

# GoodData base URL, e.g. "https://www.example.com"
host = "https://www.example.com"
# GoodData user token
token = "some_user_token"
sdk = GoodDataSdk.create(host, token)

workspace_id = "123"

# Read catalog for demo workspace
catalog = sdk.catalog_workspace_content.get_full_catalog(workspace_id)

# Print all dataset in the workspace
for dataset in catalog.datasets:
    print(str(dataset))

# Print all metrics in the workspace
for metric in catalog.metrics:
    print(str(metric))

# Read list of attributes for demo workspace
attributes = sdk.catalog_workspace_content.get_attributes_catalog(workspace_id)

# Read list of facts for demo workspace
facts = sdk.catalog_workspace_content.get_facts_catalog(workspace_id)
```
