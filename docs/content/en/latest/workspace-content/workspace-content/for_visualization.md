---
title: "for_visualization"
linkTitle: "for_visualization"
weight: 10
superheading: "tables."
---



``for_visualization(workspace_id: str, visualization: Visualization)``

Get data as an ExecutionTable from the given visualization.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="visualization" p_type="Visualization" >}}
Visualization object, representing a visualization.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_type="ExecutionTable" >}}
Visualization data wrapper object.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get visualization
campaign_spend = sdk.visualizations.get_visualization(workspace_id="123", visualization_id="campaign_spend")
# Get the visualization as Execution Table
sdk.tables.for_visualization(workspace_id="123", visualization=campaign_spend)

# ExecutionTable(
#   response=Execution(
#       workspace_id=demo,
#       result_id=c3899bb07edee259331707f817d710c80218b1ef
#   ),
#   columns=[
#           '291c085e7df8420db84117ca49f59c49',
#           'd9dd143d647d4d148405a60ec2cf59bc',
#           'd319bcb2d8c04442a684e3b3cd063381'
#   ],
#   rows=143
# )
```
