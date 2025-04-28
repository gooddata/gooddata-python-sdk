---
title: "put_declarative_automations"
linkTitle: "put_declarative_automations"
weight: 50
superheading: "catalog_workspace."
---

{{< api-ref "sdk.CatalogWorkspaceService.put_declarative_automations" >}}

## Example

```python
automations = [CatalogDeclarativeAutomation(id="schedule", ...)]
sdk.catalog_workspace.put_declarative_automations(workspace_id="demo", automations=automations)
```
