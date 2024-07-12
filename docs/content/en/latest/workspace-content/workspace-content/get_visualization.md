---
title: "get_visualization"
linkTitle: "get_visualization"
weight: 15
superheading: "visualizations."
---



``get_visualization(workspace_id: str, visualization_id: str, timeout: Optional[Union[int, float, Tuple]] = None)``

Get a single visualization from a workspace.


{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="visualization_id" p_type="string" >}}
Visualization identifier string e.g. "bikes"
{{< /parameter >}}
{{< parameter p_name="timeout" p_type="Optional[Union[int, float, Tuple]]" >}}
Timeout in seconds for the request. If a tuple is provided, the first element is the connect timeout
and the second element is the read timeout. If a single value is provided, it is used as both connect
and read timeout. If None, the default timeout is used.
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
