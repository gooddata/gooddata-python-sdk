---
title: "store_declarative_ldm"
linkTitle: "store_declarative_ldm"
weight: 100
superheading: "catalog_workspace_content."
---



``store_declarative_ldm(workspace_id: str, layout_root_path: Path = Path.cwd())``

Stores the declarative logical data model for a given workspace in directory hierarchy. This method ties the LDM to the workspace and organization, thus it is recommended for backups. If you want to move LDM between workspaces or organizations, use [store_ldm_to_disk](../store_ldm_to_disk/).

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

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# Store logical data model
sdk.catalog_workspace_content.store_declarative_ldm(workspace_id="123", layout_root_path=Path.cwd())
```
