---
title: "store_ldm_to_disk"
linkTitle: "store_ldm_to_disk"
weight: 100
superheading: "catalog_workspace_content."
---


``store_ldm_to_disk(workspace_id: str, path: Path = Path.cwd())``

Store the ldm layout in the directory for a given workspace.
The directory structure below shows the output for the path set to `Path("ldm_location")`.

        ldm_location
                └── ldm
                        ├── datasets
                        │       └── dataset.yaml
                        └── date_instances
                                └── date_instance.yaml


## Example

```Python
# store the logical data model
sdk.catalog_workspace_content.store_ldm_to_disk(workspace_id="123",path=Path.cwd())
```
