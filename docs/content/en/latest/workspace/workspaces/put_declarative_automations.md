---
title: "put_declarative_automations"
linkTitle: "put_declarative_automations"
weight: 50
superheading: "catalog_workspace."
---

``put_declarative_automations(workspace_id: str, automations: list[CatalogDeclarativeAutomation])``

Set automations for the workspace.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="automations" p_type="list[CatalogDeclarativeAutomation]" >}}
List of declarative automations.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
automations = [CatalogDeclarativeAutomation(id="schedule", ...)]
sdk.catalog_workspace.put_declarative_automations(workspace_id="demo", automations=automations)
```
