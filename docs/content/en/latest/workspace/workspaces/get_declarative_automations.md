---
title: "get_declarative_automations"
linkTitle: "get_declarative_automations"
weight: 50
superheading: "catalog_workspace."
---

``get_declarative_automations(workspace_id: str)``

Gets the layout of all workspaces and their hierarchy.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="list[CatalogDeclarativeAutomation]" >}}
Retrieve a list of declarative automations.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
declarative_automations = sdk.catalog_workspace.get_declarative_automations(workspace_id="demo")
```
