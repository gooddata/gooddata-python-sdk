---
title: "get_visualization"
linkTitle: "get_visualization"
weight: 15
superheading: "visualizations."
---



``get_visualization(workspace_id: str, visualization_id: str)``

Get a single visualization from a workspace.


{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="visualization_id" p_type="string" >}}
Visualization identifier string e.g. "bikes"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_type="Visualization" >}}
A single Visualization object contains side loaded metadata about the entities it references
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get all visualizations
visualizations = sdk.visualizations.get_visualizations(workspace_id="123", visualization_id="abc")
```
