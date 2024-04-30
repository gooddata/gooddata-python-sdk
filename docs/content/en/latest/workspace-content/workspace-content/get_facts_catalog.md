---
title: "get_facts_catalog"
linkTitle: "get_facts_catalog"
weight: 40
superheading: "catalog_workspace_content."
---



``get_facts_catalog(workspace_id: str)``

Gets all facts in a given workspace.

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_type="list[CatalogFact]" >}}
List of all facts in a given workspace.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get all the facts
facts = sdk.catalog_workspace_content.get_facts_catalog(workspace_id="123")
```
