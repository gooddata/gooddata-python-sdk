---
title: "store_analytics_model_to_disk"
linkTitle: "store_analytics_model_to_disk"
weight: 131
superheading: "catalog_workspace_content."
---

``store_analytics_model_to_disk(workspace_id: str, path: Path = Path.cwd())``

Store the analytics model layout in the directory for a given workspace.
The directory structure below shows the output for the path set to `Path("analytics_model_location")`.

    analytics_model_location
                └── analytics_model
                        ├── analytical_dashboards
                        │       └── analytical_dashboard.yaml
                        ├── dashboard_plugins
                        │       └── dashboard_plugin.yaml
                        ├── filter_contexts
                        │       └── filter_context.yaml
                        ├── metrics
                        │       └── metric.yaml
                        └── visualization_objects
                                └── visualization_object.yaml

## Example

```Python
# Store the analytics model to disk
sdk.catalog_workspace_content.store_analytics_model_to_disk(
        workspace_id="123",
        path=Path.cwd()
)
```
