---
title: "get_visualizations"
linkTitle: "get_visualizations"
weight: 15
superheading: "visualizations."
---

``get_visualizations(workspace_id: str)``

Get a list of visualization objects.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_type="list[Visualization]" >}}
All available visualizations, each visualization will contain side loaded metadata about the entities it references
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get all visualizations
visualizations = sdk.visualizations.get_visualizations(workspace_id="123")
```
