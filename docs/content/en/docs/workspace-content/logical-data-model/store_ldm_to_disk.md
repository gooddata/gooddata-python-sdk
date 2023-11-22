---
title: "store_ldm_to_disk"
linkTitle: "store_ldm_to_disk"
weight: 100
superheading: "catalog_workspace_content."
---


``store_ldm_to_disk(workspace_id: str, path: Path = Path.cwd())``

Stores the declarative logical data model for a given workspace in directory hierarchy. This method does not tie the LDM to the workspace and organization, thus it is recommended for migration between organizations. If you want to backup LDM use [store_declarative_ldm](../store_declarative_ldm/).

The directory structure below shows the output for the path set to `Path("ldm_location")`.

        ldm_location
                └── ldm
                        ├── datasets
                        │       └── dataset.yaml
                        └── date_instances
                                └── date_instance.yaml

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# store the logical data model
sdk.catalog_workspace_content.store_ldm_to_disk(workspace_id="123",path=Path.cwd())
```
