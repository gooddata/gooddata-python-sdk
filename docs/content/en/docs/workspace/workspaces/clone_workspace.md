---
title: "clone_workspace"
linkTitle: "clone_workspace"
weight: 21
superheading: "catalog_workspace."
---



``clone_workspace(source_workspace_id: str, target_workspace_id: Optional[str] = None, target_workspace_name: Optional[str] = None, overwrite_existing: Optional[bool] = None, data_source_mapping: Optional[dict] = None, upper_case: Optional[bool] = True )``

Clone workspace from existing workspace.

Clones complete workspace content - LDM, ADM, permissions. If the target workspace already exists, it's content is overwritten.

This can be useful when testing changes in the clone - once you are satisfied, you can clone it back to the origin workspace.

For the safety, you have to enforce this behavior by the dedicated input argument `overwrite_existing`. Beware of workspace data filters - after the clone you have to set WDF value for the new workspace.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="source_workspace_id" p_type="string" >}}
Source workspace ID, from which we wanna create a clone
{{< /parameter >}}
{{< parameter p_name="target_workspace_id" p_type="Optional[string]" >}}
Target workspace ID, where we wanna clone the source workspaceOptional, if empty, we generate <source_workspace_id>_clone
{{< /parameter >}}
{{< parameter p_name="target_workspace_name" p_type="Optional[string]" >}}
        Target workspace name, if empty, we generate <source_workspace_name> (Clone)
{{< /parameter >}}
{{< parameter p_name="overwrite_existing" p_type="bool" >}}
Overwrite existing workspace.
{{< /parameter >}}
{{< parameter p_name="data_source_mapping" p_type="Optional[dict]" >}}
Optional, allows users to map LDM to different data source ID
{{< /parameter >}}
{{< parameter p_name="upper_case" p_type="Optional[bool]" >}}
Optional, allows users to change the case of all physical object IDs (table names, columns names)

**True** changes it to upper-case, **False** to lower-case, None(default) is noop


Useful when migrating to Snowflake, which is the only DB with upper-case default.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# Clones complete workspace content - LDM, ADM, permissions.
sdk.catalog_workspace.clone_workspace(
        source_workspace_id="123",
        target_workspace_id="xyz",
        target_workspace_name="Demo"
)
```
