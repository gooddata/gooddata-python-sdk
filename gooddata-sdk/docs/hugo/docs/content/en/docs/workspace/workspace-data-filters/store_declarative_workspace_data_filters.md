---
title: "store_declarative_workspace_data_filters"
linkTitle: "store_declarative_workspace_dat..."
weight: 160
superheading: "catalog_workspace."
---

<!-- TODO -->

``store_declarative_workspace_data_filters(layout_root_path: Path = Path.cwd())``

Store workspace data filters in directory hierarchy.

    gooddata_layouts
    └── organization_id
            └── workspaces_data_filters
                    ├── filter_1.yaml
                    └── filter_2.yaml

## Example

```Python
# Store the workspace filters
sdk.catalog_workspace.store_declarative_workspace_data_filters(layout_root_path=Path.cwd())
```
