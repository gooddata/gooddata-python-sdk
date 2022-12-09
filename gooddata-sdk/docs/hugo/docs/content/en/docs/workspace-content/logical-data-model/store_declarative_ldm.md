---
title: "store_declarative_ldm"
linkTitle: "store_declarative_ldm"
weight: 100
superheading: "catalog_workspace_content."
---

<!-- TODO -->

``store_declarative_ldm(workspace_id: str, layout_root_path: Path = Path.cwd())``

Store logical data model layout in directory hierarchy.

    gooddata_layouts
    └── organization_id
            └── workspaces
                    └── workspace_id
                            └── analytics_model
                                    └── ldm
                                        ├── datasets
                                        │       └── dataset.yaml
                                        └── date_instances
                                                └── date_instance.yaml

## Example

```Python
# Store logical data model
sdk.catalog_workspace_content.store_declarative_ldm(workspace_id="123", layout_root_path=Path.cwd())
```
