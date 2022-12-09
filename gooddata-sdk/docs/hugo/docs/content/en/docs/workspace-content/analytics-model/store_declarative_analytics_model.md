---
title: "store_declarative_analytics_model"
linkTitle: "store_declarative_analytics_model"
weight: 130
superheading: "catalog_workspace_content."
---

<!-- TODO -->

``store_declarative_analytics_model(workspace_id: str, layout_root_path: Path = Path.cwd())``

Store declarative analytics model layout in directory hierarchy.

    gooddata_layouts
    └── organization_id
            └── workspaces
                    └── workspace_id
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
sdk.catalog_workspace_content.store_declarative_analytics_model(
        workspace_id="123",
        layout_root_path=Path.cwd()
)
```
